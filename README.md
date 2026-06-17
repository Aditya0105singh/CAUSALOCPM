# CausalOCPM
![Status: Fully Functional](https://img.shields.io/badge/Status-Fully%20Functional-success) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)

## Causal-Explainable Object-Centric Process Mining
### A Generalised Framework for Counterfactual Policy Evaluation

---

## Overview

**CausalOCPM** is a fully functional, end-to-end framework that bridges two previously separate fields — Object-Centric Process Mining (OCPM) and Structural Causal Models (SCMs) — to enable rigorous causal policy evaluation in multi-entity business processes.

The central research demonstration: in process analytics, naive correlation-based estimates of process factor effects are systematically inflated by confounding. CausalOCPM identifies confounders automatically via causal discovery, removes their influence via backdoor adjustment, and recovers the true causal effect — validated against planted ground truth in both manufacturing and healthcare domains.

**The confounding trap (manufacturing domain):**

```
order_complexity ──→ supplier_a ──→ material_lead_time ──→ shipment_delay
         │                                                       ↑
         └───────────────────────────────────────────────────────┘
                        (direct confounding path)
```

Complex orders preferentially use Supplier-A (confounding) AND have longer
delays inherently. Naive analysis overstates Supplier-A's causal contribution
by ~20%. Backdoor adjustment recovers the true effect.

---

## Installation

```bash
pip install -r requirements.txt
```

Required packages include: pandas, numpy, networkx, scikit-learn, dowhy,
causal-learn, shap, streamlit, plotly, scipy, pm4py, pytest.

**Note:** `causal-learn` is pip-installed as `causal-learn` but imported as `causallearn`.

---

## Quick Start

### Generate data and run pipeline

```bash
# Manufacturing domain
python data/generate_data.py

# Healthcare domain (second domain instantiation)
python data/generate_healthcare.py

# BPI 2019 real data (optional — requires XES file download)
python data/convert_bpi2019.py
```

### Verify individual phases

```bash
python src/phase1_graph.py       # Object interaction graph
python src/phase2_discovery.py   # Causal DAG discovery + ablation
python src/phase3_scm.py         # Mixed structural causal model
python src/phase4_dooperator.py  # Backdoor adjustment + sensitivity
python src/phase5_attribution.py # SCM-grounded attribution
```

### Run tests (must pass before using dashboard)

```bash
pytest -v tests/test_pipeline.py
```

Expected: 36 passed.

### Launch dashboard

```bash
streamlit run app/dashboard.py
```

---

## Architecture

```
causal_ocpm/
├── data/
│   ├── generate_data.py          # Manufacturing domain (3,000 events)
│   ├── generate_healthcare.py    # Healthcare domain (3,000 events)
│   └── convert_bpi2019.py        # BPI 2019 XES → OCEL schema
│
├── src/
│   ├── phase1_graph.py           # OCEL → typed object interaction graph
│   ├── phase2_discovery.py       # Causal DAG via PC + domain priors
│   ├── phase3_scm.py             # Mixed SCM (logistic/linear/GBR)
│   ├── phase4_dooperator.py      # Backdoor adjustment + sensitivity
│   └── phase5_attribution.py     # SCM-grounded attribution
│
├── app/
│   └── dashboard.py              # 7-tab Streamlit dashboard
│
├── paper/
│   ├── problem_statement.tex     # Formal definitions + problem statement
│   ├── theorem1_proof.tex        # Cross-object backdoor validity theorem
│   └── comparison_table.tex      # Capability comparison table
│
└── tests/
    └── test_pipeline.py          # Full pytest suite (36 tests)
```

---

## Five-Phase Pipeline

| Phase | Module | Description |
|-------|--------|-------------|
| 1 | `phase1_graph.py` | Builds typed heterogeneous object interaction graph from OCEL data. Connects Case, Resource_Machine, Resource_Worker, Artifact, and Outcome objects that co-occur in events. |
| 2 | `phase2_discovery.py` | PC algorithm (Fisher's Z) learns causal DAG from data. Domain knowledge enforced as post-processing constraints. Ablation study empirically validates this design choice. |
| 3 | `phase3_scm.py` | Fits structural equations per node: LogisticRegression (binary), GradientBoostingRegressor (outcome), LinearRegression (continuous). No global linearity assumption. |
| 4 | `phase4_dooperator.py` | DoWhy backdoor adjustment estimates causal effect. Sensitivity analysis quantifies robustness to unmeasured confounders. Robustness validated across 10 random seeds. |
| 5 | `phase5_attribution.py` | SHAP applied to SCM structural equations. Labelled "SCM-Grounded Attribution" (not "Causal SHAP") — an honest intermediate position relative to Heskes et al. (2020). |

---

## Dashboard — 7 Tabs

| Tab | Contents |
|-----|----------|
| 📊 Event Log | Event log summary, OCEL object interaction graph (sampled subgraph) |
| 🔗 Causal Discovery | Learned DAG with confounding path highlighted, ablation study table |
| ⚙️ Structural Model | Mixed model architecture, coefficient recovery chart, equation quality |
| 🎯 Policy Simulation | **Headline tab**: correlation vs causal vs planted truth, sensitivity analysis, robustness across seeds |
| 🔍 Case Attribution | SCM-grounded SHAP waterfall chart, actionable vs structural breakdown |
| 🌍 Real Data: BPI 2019 | BPI Challenge 2019 real event log (Phases 1–2 only; Phase 4 omitted) |
| 🏥 Domain Comparison | Cross-domain generalisation: manufacturing and healthcare side-by-side |

---

## Validation Methodology

The framework uses synthetic event logs with planted causal structure — the standard validation approach in causal inference research. Key properties:

- **Known ground truth**: causal coefficients are planted at generation time and known exactly
- **Two independent domains**: manufacturing (Prihir Enterprises) and healthcare (Hospital Admissions) share identical causal structure but different variable semantics
- **Recovery test**: causal estimates must fall within ±0.5 of the planted true effect (enforced in test suite)
- **Sensitivity analysis**: estimates validated across 6 unmeasured confounder strengths and 10 random seeds
- **Real data validation**: BPI Challenge 2019 purchase order event log (public benchmark)

---

## BPI 2019 Real Data

To enable the real-world validation tab:

1. Download from: https://doi.org/10.4121/uuid:d06aff4b-79f0-45ab-b737-5954ad1dac79
2. Place `BPI_Challenge_2019.xes` in `data/`
3. Run: `python data/convert_bpi2019.py`
4. Refresh the dashboard

Phase 4 (causal effect estimation) is deliberately omitted from real-data validation
because no ground truth causal structure is available. This is the scientifically
correct position and is acknowledged explicitly in the dashboard.

---

## Theoretical Foundation

- **Definition 1** (OCEL 2.0 Event Log): formal specification in `paper/problem_statement.tex`
- **Definition 2** (Object-Centric Causal Process Model): SCM over OCEL-derived variables
- **Theorem 1** (Cross-Object Backdoor Validity): backdoor adjustment holds for cross-object-type causal edges under OCEL-to-variable aggregation consistency — proved in `paper/theorem1_proof.tex`

---

## Related Work and Novelty

No existing public tool combines all five capabilities in a single application. This is verified, not claimed.

### Capability Comparison

| Project | Stars | Dashboard | Process Mining | Causal Discovery | SCM Fitting | OCEL Support |
|---------|-------|-----------|----------------|------------------|-------------|--------------|
| **CausalOCPM** (this work) | — | ✅ | ✅ | ✅ | ✅ | ✅ |
| CausalDelayPredictor | 0 | ❌ | ✅ | Partial | ❌ | ❌ |
| Causal Deviance Mining (TU/e 2025) | 0 | ❌ | ✅ | Partial | ❌ | ❌ |
| PM4Py | 971 | ❌ | ✅ | ❌ | ❌ | ✅ |
| DoWhy | 8.2k | ❌ | ❌ | ✅ | ✅ | ❌ |
| CausalNex | 2.5k | ❌ | ❌ | ✅ | ❌ | ❌ |

### Closest Existing Work

**CausalDelayPredictor** (github.com/z-008/CausalDelayPredictor, 2022) — the single closest conceptual match. Applies causal inference inside process mining to identify delay drivers. Delivered as a Jupyter notebook with no dashboard, no SCM fitting, and no policy simulation. Abandoned.

**Causal Deviance Mining** (Griffioen, TU/e Master's Thesis, 2025) — combines Causal Rule Mining with Business Process Deviance Mining. Academically adjacent; framing language for "causally grounded process insights" is transferable. Notebook-only, no interactive component.

**PM4Py** (processintelligence.solutions/pm4py) — industry-standard process mining library. Handles OCEL 2.0, Petri nets, conformance checking. Zero causal inference capability; descriptive analytics only. Informs the OCEL data structure and object interaction graph conventions used here.

**DoWhy** (Microsoft/py-why) — gold-standard causal inference library implementing do-calculus, DAG estimation, and refutation tests. No process mining, no event logs, no dashboard. Provides the backdoor adjustment backend used in Phase 4.

**causal-learn** (py-why/causal-learn) — reference Python implementation of the PC Algorithm (Fisher's Z conditional independence). Provides the causal discovery backend used in Phase 2.

### Novelty Claim

> "Existing tools treat process mining and causal inference as separate concerns — PM4Py for descriptive process analytics, DoWhy/CausalNex for causal effect estimation. No public tool integrates object-centric event logs with automated causal discovery, structural causal model fitting, and interactive counterfactual policy simulation. CausalOCPM is the first to unify all five in a single application validated against planted ground truth across two independent domains."

This is verifiable from the table above.

---

## References

- Pearl, J. (2009). *Causality: Models, Reasoning and Inference* (2nd ed.). Cambridge University Press.
- Sharma, A., Kiciman, E. (2020). DoWhy: An End-to-End Library for Causal Inference. arXiv:2011.04216.
- Zheng, Y. et al. (2023). causal-learn: Causal Discovery in Python. JMLR 24(60):1-8.
- Heskes, T. et al. (2020). Causal Shapley Values. NeurIPS 33, 4778-4789.
- van der Aalst, W.M.P. et al. (2022). Object-Centric Process Mining: Dealing with Divergence and Convergence in Event Data. SIMPDA.
