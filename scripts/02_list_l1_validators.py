import json
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


AVACLOUD_BASE_URL = "https://glacier-api.avax.network/v1"


def main() -> None:
    load_dotenv()

    api_key = os.getenv("AVACLOUD_API_KEY")

    if not api_key:
        raise RuntimeError(
            "AVACLOUD_API_KEY bulunamadı. .env dosyasına API key eklediğinden emin ol."
        )

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    url = f"{AVACLOUD_BASE_URL}/networks/mainnet/l1Validators"

    headers = {
        "accept": "application/json",
        "x-glacier-api-key": api_key,
    }

    params = {
        "pageSize": 10,
        "includeInactiveL1Validators": "true",
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    json_path = output_dir / "l1_validators_sample.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    validators = data.get("validators", [])

    rows = []
    for v in validators:
        rows.append(
            {
                "validationId": v.get("validationId"),
                "validationIdHex": v.get("validationIdHex"),
                "nodeId": v.get("nodeId"),
                "subnetId": v.get("subnetId"),
                "weight": v.get("weight"),
                "remainingBalance": v.get("remainingBalance"),
                "creationTimestamp": v.get("creationTimestamp"),
            }
        )

    df = pd.DataFrame(rows)
    csv_path = output_dir / "l1_validators_sample.csv"
    df.to_csv(csv_path, index=False)

    print("SUCCESS: L1 validator sample retrieved.")
    print(f"JSON saved to: {json_path}")
    print(f"CSV saved to: {csv_path}")
    print(df.head())


if __name__ == "__main__":
    main()