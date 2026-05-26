import json
from pathlib import Path

import requests


PCHAIN_RPC_URL = "https://api.avax.network/ext/bc/P"


def call_pchain(method: str, params: dict | None = None) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {},
    }

    response = requests.post(PCHAIN_RPC_URL, json=payload, timeout=30)
    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(data["error"])

    return data


def main() -> None:
    output_dir = Path("outputs")
    sample_path = output_dir / "l1_validators_sample.json"

    if not sample_path.exists():
        raise RuntimeError(
            "Önce 02_list_l1_validators.py scriptini çalıştırmalısın."
        )

    with sample_path.open("r", encoding="utf-8") as f:
        sample_data = json.load(f)

    validators = sample_data.get("validators", [])

    if not validators:
        raise RuntimeError("l1_validators_sample.json içinde validator bulunamadı.")

    # İlk validator kaydının validationId değerini alıyoruz.
    validation_id = validators[0].get("validationId")

    if not validation_id:
        raise RuntimeError("İlk validator kaydında validationId bulunamadı.")

    data = call_pchain(
        "platform.getL1Validator",
        {
            "validationID": validation_id,
        },
    )

    output_path = output_dir / "one_l1_validator_pchain_sample.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("SUCCESS: Single L1 validator details retrieved from P-Chain RPC.")
    print(f"validationID: {validation_id}")
    print(f"Saved to: {output_path}")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()