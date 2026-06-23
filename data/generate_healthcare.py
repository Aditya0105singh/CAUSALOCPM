"""
Healthcare domain data generator for CausalOCPM.

Second domain instantiation proving the "generalised framework" claim.
Mirrors the manufacturing confounding structure in a hospital admissions setting:

The confounding trap (healthcare):
  patient_complexity → specialist_required (complex patients need specialists)
  patient_complexity → length_of_stay (complex patients stay longer inherently)
  specialist_required → treatment_duration → length_of_stay (true causal path)

  Naive analysis overstates specialist's contribution to length of stay.
  Causal adjustment recovers the true planted coefficient.

This domain was selected because Swiss researchers actively work in healthcare
informatics — it creates immediate relevance for the target panel.
"""

import numpy as np
import pandas as pd
from pathlib import Path


DOMAIN = "healthcare"

GROUND_TRUTH_EDGES = [
    ("patient_complexity", "specialist_required"),
    ("patient_complexity", "bed_occupancy_rate"),
    ("patient_complexity", "length_of_stay"),
    ("specialist_required", "treatment_duration"),
    ("treatment_duration", "length_of_stay"),
    ("bed_occupancy_rate", "approval_wait"),
    ("approval_wait", "length_of_stay"),
    ("emergency_admission", "approval_wait"),
    ("insurance_expedited", "length_of_stay"),
]

# True planted causal coefficient — used ONLY in test suite, never in UI
TRUE_SPECIALIST_CAUSAL_EFFECT = 6.2 * 0.85

NUMERIC_VARS = [
    'patient_complexity', 'specialist_required', 'treatment_duration',
    'bed_occupancy_rate', 'emergency_admission', 'approval_wait',
    'insurance_expedited', 'length_of_stay'
]

BINARY_VARS = ['specialist_required', 'emergency_admission', 'insurance_expedited']
CONTINUOUS_VARS = ['patient_complexity', 'treatment_duration',
                   'bed_occupancy_rate', 'approval_wait']
OUTCOME_VAR = 'length_of_stay'
TREATMENT_VAR = 'specialist_required'

DATA_PATH = Path(__file__).parent / "hospital_synthetic.csv"

VARIABLE_LABELS = {
    'patient_complexity':   'Patient Complexity',
    'specialist_required':  'Specialist Required',
    'treatment_duration':   'Treatment Duration (days)',
    'bed_occupancy_rate':   'Bed Occupancy Rate',
    'emergency_admission':  'Emergency Admission',
    'approval_wait':        'Approval Wait (days)',
    'insurance_expedited':  'Insurance Expedited',
    'length_of_stay':       'Length of Stay (days)',
}


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def generate_data(n: int = 15000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic hospital admission event log with planted causal structure.

    Analogous to manufacturing domain: patient_complexity is the confounder
    driving both specialist assignment and length of stay directly.
    """
    rng = np.random.default_rng(seed)

    # Root variable: patient complexity (analogous to order_complexity)
    patient_complexity = rng.integers(1, 11, size=n).astype(float)

    # Confounder drives treatment: complex patients preferentially see specialists
    specialist_prob = _sigmoid((patient_complexity - 5) * 0.9)
    specialist_required = rng.binomial(1, specialist_prob).astype(float)

    # Treatment duration: specialist's true causal effect = 6.2 days
    treatment_duration = (1.8 + 6.2 * specialist_required
                          + rng.normal(0, 0.7, size=n))
    treatment_duration = np.clip(treatment_duration, 0.3, None)

    # Bed occupancy: driven by patient complexity
    bed_occupancy_rate = (0.3 + 0.06 * patient_complexity
                          + rng.normal(0, 0.08, size=n))
    bed_occupancy_rate = np.clip(bed_occupancy_rate, 0, 1)

    # Emergency admission: independent binary variable
    emergency_admission = rng.binomial(1, 0.4, size=n).astype(float)

    # Approval wait: driven by occupancy and emergency complexity
    approval_wait = (3.2 + 2.1 * bed_occupancy_rate
                     + 1.8 * emergency_admission
                     + rng.normal(0, 0.9, size=n))
    approval_wait = np.clip(approval_wait, 0, None)

    # Insurance expedited: independent binary variable
    insurance_expedited = rng.binomial(1, 0.45, size=n).astype(float)

    # Outcome: length of stay — the full structural equation
    length_of_stay = (0.8
                      + 0.85 * (treatment_duration - 1.8)
                      + 0.35 * (approval_wait - 3.2) * 0.3
                      + 0.18 * patient_complexity
                      - 0.55 * insurance_expedited
                      + rng.normal(0, 0.5, size=n))

    # Supplementary object-centric columns
    patient_ids = [f"PAT_{i:04d}" for i in range(n)]
    ward_ids = [f"WRD_{(i % 6) + 1:02d}" for i in range(n)]
    clinician_ids = [f"CLN_{(i % 20) + 1:02d}" for i in range(n)]
    medication_ids = ["MED_S" if s == 1 else "MED_G" for s in specialist_required]
    discharge_ids = [f"DIS_{i:04d}" for i in range(n)]
    timestamps = pd.date_range("2023-01-01", periods=n, freq="4h")

    df = pd.DataFrame({
        'patient_id':          patient_ids,
        'patient_complexity':  patient_complexity,
        'specialist_required': specialist_required,
        'treatment_duration':  treatment_duration,
        'bed_occupancy_rate':  bed_occupancy_rate,
        'emergency_admission': emergency_admission,
        'approval_wait':       approval_wait,
        'insurance_expedited': insurance_expedited,
        'length_of_stay':      length_of_stay,
        'ward_id':             ward_ids,
        'clinician_id':        clinician_ids,
        'medication_id':       medication_ids,
        'discharge_id':        discharge_ids,
        'timestamp':           timestamps,
    })

    return df


def load_or_generate(n: int = 15000, seed: int = 42) -> pd.DataFrame:
    """Load cached CSV if present, otherwise generate and save."""
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH, parse_dates=['timestamp'])
    df = generate_data(n=n, seed=seed)
    df.to_csv(DATA_PATH, index=False)
    return df


if __name__ == "__main__":
    df = generate_data()
    df.to_csv(DATA_PATH, index=False)
    naive = (df[df.specialist_required == 1].length_of_stay.mean()
             - df[df.specialist_required == 0].length_of_stay.mean())
    print("[CONFOUNDING ANALYSIS — HEALTHCARE]")
    print(f"  Naive (confounded)     : +{naive:.3f} days LOS")
    print(f"  True causal effect     : +{TRUE_SPECIALIST_CAUSAL_EFFECT:.3f} days")
    print(f"  Confounding inflation  : {naive / TRUE_SPECIALIST_CAUSAL_EFFECT:.2f}x")
    print(f"  Data saved. Shape: {df.shape}")
