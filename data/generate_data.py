"""
Manufacturing domain data generator for CausalOCPM.

Generates synthetic event logs for "Prihir Enterprises" (brass parts, Jamnagar)
with a planted causal structure that includes a confounder (order_complexity)
driving both supplier selection and shipment delay. This enables rigorous
validation that causal adjustment recovers the correct effect.

The confounding trap:
  order_complexity → supplier_a (confounder drives treatment selection)
  order_complexity → shipment_delay (confounder also affects outcome)
  supplier_a → material_lead_time → shipment_delay (true causal path)

  Naive analysis: naive effect >> true causal effect (inflated by confounding)
  Causal analysis: backdoor adjustment recovers the planted coefficient
"""

import numpy as np
import pandas as pd
from pathlib import Path


DOMAIN = "manufacturing"

# Planted causal edges — the ground truth structure we try to recover
GROUND_TRUTH_EDGES = [
    ("order_complexity", "supplier_a"),
    ("order_complexity", "machine_queue_length"),
    ("order_complexity", "shipment_delay"),
    ("supplier_a", "material_lead_time"),
    ("material_lead_time", "shipment_delay"),
    ("machine_queue_length", "approval_duration"),
    ("approval_duration", "shipment_delay"),
    ("export_flag", "approval_duration"),
    ("carrier_express", "shipment_delay"),
]

# True planted causal coefficient — used ONLY in the test suite, never in UI
TRUE_SUPPLIER_A_CAUSAL_EFFECT = 7.4 * 0.9

NUMERIC_VARS = [
    'order_complexity', 'supplier_a', 'material_lead_time',
    'machine_queue_length', 'export_flag', 'approval_duration',
    'carrier_express', 'shipment_delay'
]

BINARY_VARS = ['supplier_a', 'export_flag', 'carrier_express']
CONTINUOUS_VARS = ['order_complexity', 'material_lead_time',
                   'machine_queue_length', 'approval_duration']
OUTCOME_VAR = 'shipment_delay'
TREATMENT_VAR = 'supplier_a'

DATA_PATH = Path(__file__).parent / "prihir_synthetic.csv"


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def generate_data(n: int = 3000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic manufacturing event log with planted causal structure.

    Causal generation follows the exact order specified in the build brief.
    The confounding path: order_complexity → supplier_a creates the central
    research demonstration that naive analysis overstates Supplier-A's effect.
    """
    rng = np.random.default_rng(seed)

    # Root variable: order complexity (uniform integer 1–10)
    order_complexity = rng.integers(1, 11, size=n).astype(float)

    # Confounder drives treatment: complex orders preferentially use Supplier-A
    supplier_a_prob = _sigmoid((order_complexity - 5) * 0.9)
    supplier_a = rng.binomial(1, supplier_a_prob).astype(float)

    # Material lead time: Supplier-A's true causal effect = 7.4 days
    material_lead_time = (2.1 + 7.4 * supplier_a
                          + rng.normal(0, 0.8, size=n))
    material_lead_time = np.clip(material_lead_time, 0.5, None)

    # Machine queue: driven by order complexity
    machine_queue_length = (1.2 + 0.8 * order_complexity
                             + rng.normal(0, 1.0, size=n))
    machine_queue_length = np.clip(machine_queue_length, 0, None)

    # Export flag: independent binary variable
    export_flag = rng.binomial(1, 0.5, size=n).astype(float)

    # Approval duration: driven by queue and export complexity
    approval_duration = (4.1 + 1.3 * machine_queue_length
                         + 2.0 * export_flag
                         + rng.normal(0, 1.2, size=n))
    approval_duration = np.clip(approval_duration, 0, None)

    # Express carrier: independent binary variable
    carrier_express = rng.binomial(1, 0.5, size=n).astype(float)

    # Outcome: shipment delay — the full structural equation
    # Note: negatives allowed per spec — do NOT clip
    shipment_delay = (0.6
                      + 0.9 * (material_lead_time - 2.1)
                      + 0.4 * (approval_duration - 4.1) * 0.25
                      + 0.20 * order_complexity
                      - 0.6 * carrier_express
                      + rng.normal(0, 0.5, size=n))

    # Supplementary object-centric columns
    order_ids = [f"ORD_{i:04d}" for i in range(n)]
    machine_ids = [f"MCH_{(i % 8) + 1:02d}" for i in range(n)]
    worker_ids = [f"WRK_{(i % 15) + 1:02d}" for i in range(n)]
    material_ids = ["MAT_A" if s == 1 else "MAT_B" for s in supplier_a]
    shipment_ids = [f"SHP_{i:04d}" for i in range(n)]
    timestamps = pd.date_range("2023-01-01", periods=n, freq="6h")

    df = pd.DataFrame({
        'order_id':            order_ids,
        'order_complexity':    order_complexity,
        'supplier_a':          supplier_a,
        'material_lead_time':  material_lead_time,
        'machine_queue_length': machine_queue_length,
        'export_flag':         export_flag,
        'approval_duration':   approval_duration,
        'carrier_express':     carrier_express,
        'shipment_delay':      shipment_delay,
        'machine_id':          machine_ids,
        'worker_id':           worker_ids,
        'material_id':         material_ids,
        'shipment_id':         shipment_ids,
        'timestamp':           timestamps,
    })

    df.to_csv(DATA_PATH, index=False)
    return df


def load_or_generate(n: int = 3000, seed: int = 42) -> pd.DataFrame:
    """Load cached CSV if present, otherwise generate and save."""
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH, parse_dates=['timestamp'])
    return generate_data(n=n, seed=seed)


if __name__ == "__main__":
    df = generate_data()
    naive = (df[df.supplier_a == 1].shipment_delay.mean()
             - df[df.supplier_a == 0].shipment_delay.mean())
    print("[CONFOUNDING ANALYSIS — MANUFACTURING]")
    print(f"  Naive (confounded)        : +{naive:.3f} days")
    print(f"  True causal effect        : +{TRUE_SUPPLIER_A_CAUSAL_EFFECT:.3f} days")
    print(f"  Confounding inflation     : {naive / TRUE_SUPPLIER_A_CAUSAL_EFFECT:.2f}x")
    print(f"  Data saved. Shape: {df.shape}")
