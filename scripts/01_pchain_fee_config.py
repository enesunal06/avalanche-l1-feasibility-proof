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
    output_dir.mkdir(exist_ok=True)

    data = call_pchain("platform.getValidatorFeeConfig")

    output_path = output_dir / "validator_fee_config_sample.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("SUCCESS: P-Chain validator fee config retrieved.")
    print(f"Saved to: {output_path}")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()