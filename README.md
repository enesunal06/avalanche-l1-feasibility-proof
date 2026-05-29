# Avalanche L1 Value Accrual — Preliminary Data Feasibility Proof

This repository contains a small technical proof-of-concept for the proposed Avalanche Research Grant project on post-Etna Avalanche L1 value accrual.

The purpose is not to build the full dataset yet. The purpose is to demonstrate that the core AVAX-side measurement pipeline is technically feasible using documented Avalanche data sources.

This repo is not a price-prediction model. It is a preliminary data feasibility proof.

## Completed Proofs

1. `01_pchain_fee_config.py`
   - Retrieves P-Chain validator fee configuration.
   - Output: `outputs/validator_fee_config_sample.json`

2. `02_list_l1_validators.py`
   - Retrieves a sample of Avalanche L1 validator records from AvaCloud Data API.
   - Outputs:
     - `outputs/l1_validators_sample.json`
     - `outputs/l1_validators_sample.csv`

3. `03_get_one_l1_validator.py`
   - Uses a sampled `validationId` to retrieve validator-specific details from P-Chain RPC.
   - Output: `outputs/one_l1_validator_pchain_sample.json`

4. `04_smoke_test.py`
   - Checks that the main output files exist and have the expected structure.

5. `05_minimal_avax_side_decomposition.py`
   - Builds a minimal AVAX-side decomposition table from the sampled validator records.
   - Outputs:
     - `outputs/minimal_avax_side_decomposition_sample.csv`
     - `outputs/minimal_avax_side_decomposition_sample.json`

## Sample Outputs

### Script 1 — P-Chain Validator Fee Configuration

`01_pchain_fee_config.py` retrieves the current fee configuration from the P-Chain. This is the starting point for measuring AVAX-denominated validator fee exposure after ACP-77.

| Field | Value |
|---|---|
| capacity | 20000 |
| target | 10000 |
| minPrice | 512 (nAVAX) |
| excessConversionConstant | 1246488515 |

### Script 2 — Avalanche L1 Validator Records

`02_list_l1_validators.py` retrieves a sample of L1 validator records from the AvaCloud Data API. Each row represents one sampled validator record associated with an Avalanche L1.

| Field | Example value |
|---|---|
| validationId | 2iq93TLZsZXxjhzDBPy5RVmh1Two7Uddrvf3Zo95NQe6HWeZFb |
| nodeId | NodeID-ERsmGLYQWuwx8nibHTig6JGYbS4uUYW2D |
| subnetId | 2sseUhPNj1G7rV5hUQzoadUx15kybrjQdVrAiNS1MnxeZSn1fs |
| weight | 100 |
| remainingBalance | 0 or 15995948544 |
| creationTimestamp | 1779459623 |

`remainingBalance` gives a first observable field for studying validator-level AVAX-side fee exposure. This proof-of-concept does not yet treat it as a complete economic measure.

### Script 3 — Single Validator Detail from P-Chain RPC

`03_get_one_l1_validator.py` uses a sampled `validationId` to query validator-level detail directly from the P-Chain RPC.

| Field | Example value |
|---|---|
| nodeID | NodeID-ERsmGLYQWuwx8nibHTig6JGYbS4uUYW2D |
| weight | 100 |
| validationID | 2iq93TLZsZXxjhzDBPy5RVmh1Two7Uddrvf3Zo95NQe6HWeZFb |
| remainingBalanceOwner | P-avax1z8877h4pyw376309jy0uywzl7hf7u7fkwt5vlg |
| deactivationOwner | P-avax12pdvdwgvx8tzlxc0syvxuph9mp2yuxu9a0uc8d |
| balance | 0 |
| subnetID | 2sseUhPNj1G7rV5hUQzoadUx15kybrjQdVrAiNS1MnxeZSn1fs |
| height | 24996982 |

This step checks that validator records sampled from the AvaCloud API can be linked back to P-Chain validator state.

### Script 5 — Minimal AVAX-Side Decomposition Table

`05_minimal_avax_side_decomposition.py` groups the sampled validator records by `subnetId` and produces a minimal AVAX-side decomposition table.

| subnetId | V_part_sample | sample_total_remainingBalance_raw | assumed_monthly_validation_fee_avax | V_fee_min_avax_per_month |
|---|---:|---:|---:|---:|
| 2sseUhPNj1G7rV5hUQzoadUx15kybrjQdVrAiNS1MnxeZSn1fs | 5 | 0 | 1.33 | 6.65 |
| o4Eariv2Cx1fTvPFXYofpJfS9KgwFaiGN8KFGcCeZM9t87GJr | 3 | 47908783168 | 1.33 | 3.99 |
| eYwmVU67LmSfZb1RwqCMhBYkFyG8ftxn6jAwqzFmxC9STBWLC | 2 | 666906581 | 1.33 | 2.66 |

This is the smallest worked example of the proposal's AVAX-side measurement logic. It shows how sampled validator records can be grouped by `subnetId` and converted into preliminary variables such as `V_part_sample`, `V_fee_min_avax_per_month`, and `V_subnet`.

## What This Proves

This proof-of-concept shows that the first part of the proposed research pipeline is technically feasible:

- Avalanche L1 validator records can be collected.
- Validator records can be exported into structured CSV and JSON files.
- Sampled validators can be linked back to P-Chain validator state.
- A minimal AVAX-side channel-decomposition table can be generated from the collected data.

The current repo only covers the AVAX-side variables of the proposal:

- `V_fee`
- `V_part`
- `V_subnet`

It does not yet compute the L1-native channels:

- `U_gas`
- `U_route`
- `U_sec`
- `U_gov`

Those are planned for the full research project.

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file with your AvaCloud API key:

```bash
AVACLOUD_API_KEY=your_api_key_here
```

Run the scripts:

```bash
python scripts/01_pchain_fee_config.py
python scripts/02_list_l1_validators.py
python scripts/03_get_one_l1_validator.py
python scripts/04_smoke_test.py
python scripts/05_minimal_avax_side_decomposition.py
```

The generated files will be saved in the `outputs/` folder.

## Preliminary Variable Mapping

See `variable_mapping.md`.

## Security Note

The AvaCloud API key is stored locally in `.env` and is excluded from version control through `.gitignore`.

The `.env` file must not be committed to version control.

Before making this repository public, make sure no private API keys or local environment files are included.