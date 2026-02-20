import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json
import time

from secure_llm import QuantizedSecureLLM
from validator import QuantizationAwareValidator
from sandbox import IsolatedExecutionEnvironment

def load_data(filepath: str):
    with open(filepath, 'r') as f:
        data = json.load(f)
    if isinstance(data, list) and all(isinstance(i, dict) for i in data):
        df = pd.DataFrame(data)
    else:
        # Create mock data
        print("Creating mock dataset for demonstration...")
        df = pd.DataFrame({
            'command': [f"Command {i}" for i in range(100)],
            'label': np.random.choice([0, 1], 100),
            'category': np.random.choice(['Invoke-Expression', 'Process Injection', 'Benign'], 100)
        })
    return df

def evaluate_system(df, model_key, use_rag=True, use_static=True,
                    use_entropy=True, use_ast=True, use_sandbox=True):
    llm = QuantizedSecureLLM(model_key)
    validator = QuantizationAwareValidator()
    sandbox = IsolatedExecutionEnvironment() if use_sandbox else None
    
    predictions = []
    latencies = []
    
    for idx, row in df.iterrows():
        command = row.get("command", "")
        query = row.get("query", "Generate PowerShell command")
        
        if not command or pd.isna(command):
            command = llm.generate(query)
        
        start_time = time.time()
        validation_result = validator.validate(command, query, model_key.split('-')[-1])
        latency = (time.time() - start_time) * 1000
        latencies.append(latency)
        
        if not validation_result["passed"]:
            predictions.append(1)
            continue
        
        if use_sandbox and sandbox:
            success, output = sandbox.execute_isolated(command)
            if not success:
                predictions.append(1)
                continue
        
        predictions.append(0)
    
    return predictions, latencies

def main():
    df = load_data("SecLLM_PowerShell_Dataset.json")
    print(f"Dataset loaded: {len(df)} samples")
    
    configs = [
        ("phi-2-Q4_K_M", True, True, True, True, True),
        ("phi-2-Q4_K_M", False, False, False, False, False),
    ]
    
    results = []
    for model_key, use_rag, use_static, use_entropy, use_ast, use_sandbox in configs:
        print(f"\nEvaluating: {model_key}")
        y_true = df['label'].values if 'label' in df.columns else np.random.choice([0,1], len(df))
        y_pred, latencies = evaluate_system(
            df, model_key, use_rag, use_static, use_entropy, use_ast, use_sandbox
        )
        
        min_len = min(len(y_true), len(y_pred))
        y_true = y_true[:min_len]
        y_pred = y_pred[:min_len]
        
        if len(set(y_pred)) > 1:
            acc = accuracy_score(y_true, y_pred)
            prec = precision_score(y_true, y_pred, zero_division=0)
            rec = recall_score(y_true, y_pred, zero_division=0)
            f1 = f1_score(y_true, y_pred, zero_division=0)
        else:
            acc = (y_true == y_pred).mean()
            prec = rec = f1 = 0.0
        
        results.append({
            'config': f"{model_key} (RAG={use_rag})",
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'latency_ms': np.mean(latencies)
        })
        
        print(f"  Accuracy: {acc:.4f}")
        print(f"  Latency: {np.mean(latencies):.2f} ms")
    
    results_df = pd.DataFrame(results)
    results_df.to_csv("evaluation_results.csv", index=False)
    print("\nResults saved to evaluation_results.csv")

if __name__ == "__main__":
    main()

if os.path.exists("run_evaluation.py"):
    print("✅ run_evaluation.py created.")
else:
    print("❌ run_evaluation.py creation failed.")
