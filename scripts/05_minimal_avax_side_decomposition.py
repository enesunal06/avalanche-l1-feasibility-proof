import json
from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path("outputs")
INPUT_CSV = OUTPUT_DIR / "l1_validators_sample.csv"

if not INPUT_CSV.exists():
    raise FileNotFoundError(
        "Missing outputs/l1_validators_sample.csv. "
        "Run scripts/02_list_l1_validators.py first."
    )

df = pd.read_csv(INPUT_CSV)

required_columns = {"validationId", "subnetId", "remainingBalance"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

# Proposal-level approximation used only for the minimal worked example.
# The full project will use validator-level P-Chain fee-state,
# fee-configuration, balance, and top-up records where available.
assumed_monthly_validation_fee_avax = 1.33

df["remainingBalance_numeric"] = pd.to_numeric(
    df["remainingBalance"],
    errors="coerce"
)

subnet_summary = (
    df.groupby("subnetId")
    .agg(
        V_part_sample=("validationId", "nunique"),
        sample_total_remainingBalance_raw=("remainingBalance_numeric", "sum"),
    )
    .reset_index()
)

subnet_summary["assumed_monthly_validation_fee_avax"] = assumed_monthly_validation_fee_avax

subnet_summary["V_fee_min_avax_per_month"] = (
    subnet_summary["V_part_sample"] * assumed_monthly_validation_fee_avax
)

subnet_summary = subnet_summary.sort_values(
    by="V_part_sample",
    ascending=False
)

selected_base_case = subnet_summary.iloc[0].to_dict()

result = {
    "description": (
        "Minimal AVAX-side channel-decomposition example using sampled "
        "Avalanche L1 validator records. This is not the final dataset "
        "and not a price-prediction model. It is the smallest working "
        "implementation of the proposal's AVAX-side measurement logic."
    ),
    "input_file": str(INPUT_CSV),
    "definitions": {
        "V_part_sample": (
            "Number of unique sampled L1 validators grouped by subnetId."
        ),
        "V_fee_min_avax_per_month": (
            "V_part_sample multiplied by the proposal-level monthly "
            "P-Chain validation-fee approximation."
        ),
        "V_subnet": (
            "Subnet-level aggregation of sampled validator participation, "
            "remaining balance, and minimal AVAX-side fee exposure."
        ),
    },
    "limitations": [
        "This example uses a small sampled validator dataset.",
        "It only demonstrates the AVAX-side channels V_part, V_fee, and V_subnet.",
        "It does not compute L1-native channels such as U_gas, U_route, U_sec, or U_gov.",
        "The full project will generalize this logic to a complete post-Etna dataset.",
    ],
    "selected_base_case": selected_base_case,
    "all_sampled_subnet_summaries": subnet_summary.to_dict(orient="records"),
}

json_output = OUTPUT_DIR / "minimal_avax_side_decomposition_sample.json"
csv_output = OUTPUT_DIR / "minimal_avax_side_decomposition_sample.csv"

with json_output.open("w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

subnet_summary.to_csv(csv_output, index=False)

print("Saved minimal AVAX-side decomposition outputs:")
print(f"- {json_output}")
print(f"- {csv_output}")
print()
print("Selected base-case subnet:")
print(f"subnetId: {selected_base_case['subnetId']}")
print(f"V_part_sample: {selected_base_case['V_part_sample']}")
print(
    "V_fee_min_avax_per_month: "
    f"{selected_base_case['V_fee_min_avax_per_month']}"
)
