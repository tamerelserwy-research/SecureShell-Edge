import re
import math
from sentence_transformers import SentenceTransformer, util

class QuantizationAwareValidator:
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(embedding_model_name)
        self.dangerous_patterns = [
            r"Invoke-Expression",
            r"IEX\s*\(",
            r"DownloadString",
            r"Start-Process.*-WindowStyle Hidden",
            r"Add-Type.*-MemberDefinition.*DllImport",
            r"FromBase64String",
            r"System\.Reflection\.Assembly"
        ]
    
    def static_analysis(self, command: str) -> tuple:
        risk = 0.0
        violations = []
        for pattern in self.dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                risk += 0.3
                violations.append(pattern)
        risk = min(risk, 1.0)
        return risk, violations
    
    def entropy_analysis(self, command: str) -> float:
        if not command:
            return 0.0
        prob = [float(command.count(c)) / len(command) for c in set(command)]
        entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob if p > 0])
        return min(entropy / 8.0, 1.0)
    
    def is_obfuscation_candidate(self, command: str) -> bool:
        return self.entropy_analysis(command) > 0.7
    
    def semantic_similarity(self, query: str, command: str) -> float:
        if not query or not command:
            return 0.5
        emb1 = self.embedder.encode(query, convert_to_tensor=True)
        emb2 = self.embedder.encode(command, convert_to_tensor=True)
        return util.pytorch_cos_sim(emb1, emb2).item()
    
    def validate(self, command: str, query: str,
                 model_quantization: str = "Q4") -> dict:
        static_risk, violations = self.static_analysis(command)
        entropy_risk = self.entropy_analysis(command)
        semantic_risk = 1.0 - self.semantic_similarity(query, command)
        
        from secure_llm import QuantizedSecureLLM
        q_config = QuantizedSecureLLM.SECURITY_CALIBRATION[f"phi-2-{model_quantization}"]
        uncertainty_penalty = q_config["epsilon_sec"]
        
        if self.is_obfuscation_candidate(command):
            entropy_risk += uncertainty_penalty
            entropy_risk = min(entropy_risk, 1.0)
        
        composite = (0.5 * static_risk + 0.3 * entropy_risk + 0.2 * semantic_risk)
        threshold = 0.5 - (0.1 if model_quantization == "Q4" else 0.0)
        passed = composite < threshold
        
        return {
            "passed": passed,
            "risk_score": composite,
            "uncertainty": uncertainty_penalty,
            "violations": violations
        }

if os.path.exists("validator.py"):
    print("✅ validator.py created.")
else:
    print("❌ validator.py creation failed.")
