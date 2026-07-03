# CausalOCPM
**Causal-Explainable Object-Centric Process Mining**

![Status](https://img.shields.io/badge/Status-Fully%20Functional-success?style=for-the-badge) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge) ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)

**🌐 Live Dashboard:** [https://causalocpm-etpavgjhzcyfdhufeftyrz.streamlit.app/](https://causalocpm-etpavgjhzcyfdhufeftyrz.streamlit.app/)

CausalOCPM is an end-to-end analytical framework that bridges **Object-Centric Process Mining (OCPM)** and **Structural Causal Models (SCM)**. It enables rigorous, counterfactual policy evaluation in complex, multi-entity business processes.

---

## The Problem: The Confounding Trap

Traditional process mining relies on correlation. But in complex systems, correlations are often systematically inflated by unmeasured confounders.

Imagine a manufacturing scenario:
> *Complex orders preferentially use Supplier-A AND have inherently longer lead times.* 

Naive analysis overstates Supplier-A's causal contribution to delays by ~20%. **CausalOCPM** automatically identifies these confounders via causal discovery, removes their influence via backdoor adjustment, and recovers the *true* causal effect.

---

## Key Features

- **End-to-End Pipeline**: From OCEL 2.0 event logs to actionable causal insights.
- **Automated Causal Discovery**: Uses the PC Algorithm (Fisher's Z) with domain knowledge constraints to discover causal DAGs.
- **Structural Causal Modeling**: Fits mixed SCMs (Logistic, Linear, Gradient Boosting) without global linearity assumptions.
- **Counterfactual Policy Simulation**: DoWhy-powered backdoor adjustment and sensitivity analysis across random seeds.
- **SCM-Grounded Attribution**: Understand case-level root causes using advanced SHAP techniques applied directly to structural equations.
- **Groq-Powered Decision Intelligence Copilot**: An integrated LLM agent (Llama 3.1 8B via Groq) that translates complex causal math into instant, board-ready executive summaries.
- **Interactive Streamlit Dashboard**: A 5-tab UI to explore event logs, validate structural models, simulate policies, and interact with the AI Copilot.

---

## Architecture Design

CausalOCPM is organized into a linear 5-phase backend pipeline that feeds directly into an interactive frontend dashboard. 

```mermaid
flowchart TD
    %% Data Input
    Data[(OCEL 2.0 Event Logs)]

    %% Pipeline Phases
    subgraph Backend Pipeline
        direction TB
        P1[Phase 1: Object Interaction Graph]
        P2[Phase 2: Automated Causal Discovery]
        P3[Phase 3: Structural Causal Modeling]
        P4[Phase 4: Counterfactual Policy Simulation]
        P5[Phase 5: SCM-Grounded Attribution]
    end

    %% Flow between phases
    Data --> P1
    P1 -->|Typed Object Graph| P2
    P2 -->|Learned Causal DAG| P3
    P3 -->|Fitted Mixed SCM| P4
    P3 -->|Fitted Mixed SCM| P5

    %% Frontend
    subgraph Frontend
        direction TB
        Dashboard{Interactive Streamlit Dashboard}
    end

    %% Connect pipeline to dashboard
    P1 -.->|Event Insights| Dashboard
    P2 -.->|DAG & Ablation Study| Dashboard
    P4 -->|Backdoor Adjustment Results| Dashboard
    P5 -->|Case-level SHAP Values| Dashboard
```

---

## Quick Start

### 1. Installation

Clone the repository and install the required dependencies:
```bash
git clone https://github.com/Aditya0105singh/CAUSALOCPM.git
cd CAUSALOCPM
pip install -r requirements.txt
```

*(Note: `causal-learn` is pip-installed as `causal-learn` but imported as `causallearn`.)*

### 2. Generate Data & Run Pipeline

You can generate synthetic data with planted ground truth for validation:
```bash
# Manufacturing domain
python data/generate_data.py

# Healthcare domain (Cross-domain validation)
python data/generate_healthcare.py
```

Process the data through the 5-phase pipeline:
```bash
python src/phase1_graph.py       # Object interaction graph
python src/phase2_discovery.py   # Causal DAG discovery
python src/phase3_scm.py         # Structural causal model
python src/phase4_dooperator.py  # Backdoor adjustment
python src/phase5_attribution.py # Case attribution
```

*(Optional) Run the full test suite to verify pipeline integrity:*
```bash
pytest -v tests/test_pipeline.py
```

### 3. Launch the Dashboard

```bash
streamlit run app/dashboard.py
```

---

## The Dashboard Experience

The interactive dashboard is divided into 5 specialized tabs:

1. **Overview**: Executive summary — headline causal finding, expected savings, and the top recommended intervention at a glance.
2. **Data & Discovery**: Event log summaries, the object-type interaction graph, the learned causal DAG, and a domain-knowledge ablation study (autonomous discovery vs. domain-constrained discovery).
3. **Model & Impact**: Structural equation summary and coefficient recovery (estimated vs. planted ground truth), treatment-effect heterogeneity across confounder subgroups, an interactive what-if policy simulator, and SCM-grounded SHAP waterfall attribution for individual cases.
4. **Decision Intelligence**: A boardroom-style executive report — naive vs. causal effect, confounding bias removed, ROI-ranked recommended actions, and a condensed cross-domain (Manufacturing vs. Healthcare) validation benchmark.
5. **Causal Copilot**: A Groq-powered conversational agent (Llama 3.1 8B) that answers free-text questions grounded in the live pipeline output, with quick-action shortcuts and an 'Executive Mode' for bottom-line summaries.

*Not currently wired into the live dashboard:* `data/convert_bpi2019.py` is a standalone converter for the BPI Challenge 2019 public event log, intended for a future real-world validation tab — eliminating the "only tested on synthetic data" objection. It exists as a script but isn't yet connected to the app.

---

## Validation Methodology

CausalOCPM rigorously validates its findings using **synthetic event logs with planted causal structures**. This allows for exact verification of recovered causal coefficients (must fall within ±0.5 of planted truth). The framework is robustly tested across 10 random seeds and 6 unmeasured confounder strengths.

| Phase | Component | Description |
|-------|-----------|-------------|
| **1** | `phase1_graph.py` | Extracts typed heterogeneous object interaction graphs from OCEL data. |
| **2** | `phase2_discovery.py`| Learns causal DAGs from data using the PC algorithm, refined by domain priors. |
| **3** | `phase3_scm.py` | Fits structural equations per node tailored to the data type. |
| **4** | `phase4_dooperator.py`| Estimates true causal effects via backdoor adjustment and validates robustness. |
| **5** | `phase5_attribution.py`| Calculates actionable SCM-grounded case attribution using SHAP. |

---

## Novelty & Impact

While tools like **PM4Py** excel at descriptive process analytics and **DoWhy/CausalNex** handle effect estimation, *no public tool integrates them.* 

**CausalOCPM is the first unified application to combine object-centric event logs, automated causal discovery, SCM fitting, interactive counterfactual policy simulation, and a real-time LLM Copilot** — all rigorously validated against planted ground truth across multiple domains. The addition of the ultra-fast Groq-powered Copilot bridges the gap between complex causal mathematics and executive decision-making.

---

## References

- Pearl, J. (2009). *Causality: Models, Reasoning and Inference*
- van der Aalst, W.M.P. et al. (2022). *Object-Centric Process Mining*
- Sharma, A., Kiciman, E. (2020). *DoWhy: An End-to-End Library for Causal Inference*
- Zheng, Y. et al. (2023). *causal-learn: Causal Discovery in Python*
- Heskes, T. et al. (2020). *Causal Shapley Values*
