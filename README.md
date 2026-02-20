# SecureShell-Edge: Retrieval-Augmented Guardrails for Local LLM PowerShell Generation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18636114.svg)](https://doi.org/10.5281/zenodo.18636114)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This repository contains the complete source code, dataset, and reproducibility artifacts for the research paper:

> **SecureShell-Edge: Retrieval-Augmented Guardrails for Local LLM PowerShell Generation**  
> Author Name, et al. (2026)

SecureShell-Edge is a system that provides security guardrails for locally-deployed, quantized Large Language Models (LLMs) generating PowerShell commands. It combines a threat‑weighted retrieval mechanism, multi‑layer validation (static analysis, entropy analysis, AST analysis, semantic similarity), and an isolated sandbox to prevent execution of malicious or accidental harmful commands.

## 📦 Repository Contents

| File | Description |
|------|-------------|
| `secure_llm.py` | Quantized LLM loader with integrity verification (SHA‑256 checksums) and security‑error tracking. |
| `validator.py` | Multi‑layer validator: static patterns, entropy analysis, semantic similarity, quantization‑aware risk scoring. |
| `sandbox.py` | Lightweight isolated execution environment with resource limits and API monitoring (for Windows). |
| `run_evaluation.py` | Main evaluation script that runs the full pipeline on the dataset. |
| `requirements-freeze.txt` | Python dependencies pinned to exact versions for reproducibility. |
| `SecLLM_PowerShell_Dataset.json` | The evaluation dataset of 6,308 PowerShell commands with labels (see [Dataset](#dataset)). |
| `SecureShell_Edge_Reproducibility_StepByStep.ipynb` | Google Colab notebook that reproduces the paper’s figures and demonstrates the code. |
| `LICENSE` | MIT License. |

## 🚀 Getting Started

### Option 1: Run in Google Colab (Recommended for Quick Exploration)

1. Open the Colab notebook:  
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tamerelserwy-research/SecureShell-Edge/blob/main/SecureShell_Edge_Reproducibility_StepByStep.ipynb)

2. Run all cells. The notebook will:
   - Install dependencies.
   - Generate the Python source files.
   - Download the dataset from Zenodo.
   - Execute a mock evaluation (no actual PowerShell required).
   - Reproduce Figures 2, 3, and 4 from the paper.

### Option 2: Local Installation (Windows with PowerShell)

For full reproduction including sandbox execution, you need a Windows machine with PowerShell.

1. Clone the repository:
   ```bash
   git clone https://github.com/tamerelserwy-research/SecureShell-Edge.git
   cd SecureShell-Edge
