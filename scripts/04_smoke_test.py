import json
from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("outputs")


def assert_file_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing output file: {path}")


def main() -> None:
    fee_config = OUTPUT_DIR / "validator_fee_config_sample.json"
    validators_json = OUTPUT_DIR / "l1_validators_sample.json"
    validators_csv = OUTPUT_DIR / "l1_validators_sample.csv"
    one_validator = OUTPUT_DIR / "one_l1_validator_pchain_sample.json"

    for path in [fee_config, validators_json, validators_csv, one_validator]:
        assert_file_exists(path)

    with fee_config.open("r", encoding="utf-8") as f:
        fee_data = json.load(f)
    assert "result" in fee_data, "validator_fee_config_sample.json has no result field"

    df = pd.read_csv(validators_csv)
    required_columns = {
        "validationId",
        "nodeId",
        "subnetId",
        "weight",
        "remainingBalance",
        "creationTimestamp",
    }

    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise AssertionError(f"Missing columns in validator CSV: {missing_columns}")

    assert len(df) > 0, "validator CSV is empty"

    with one_validator.open("r", encoding="utf-8") as f:
        validator_data = json.load(f)
    assert "result" in validator_data, "one_l1_validator_pchain_sample.json has no result field"

    print("SUCCESS: Smoke test passed.")
    print(f"Validator sample rows: {len(df)}")
    print("Core feasibility proof outputs are present and structurally valid.")


if __name__ == "__main__":
    main()