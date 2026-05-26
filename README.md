# Avalanche L1 Value Accrual — Preliminary Data Feasibility Proof

This repository contains a small technical proof-of-concept for the proposed Avalanche Research Grant project on post-Etna Avalanche L1 value accrual.

The purpose is not to build the full dataset yet. The purpose is to demonstrate that the core AVAX-side measurement pipeline is technically feasible using documented Avalanche data sources.

## Completed Proofs

1. `01_pchain_fee_config.py`
   - Retrieves P-Chain validator fee configuration.
   - Output: `outputs/validator_fee_config_sample.json`

2. `02_list_l1_validators.py`
   - Retrieves a sample of Avalanche L1 validator records from AvaCloud Data API.
   - Output:
     - `outputs/l1_validators_sample.json`
     - `outputs/l1_validators_sample.csv`

3. `03_get_one_l1_validator.py`
   - Uses a sampled `validationId` to retrieve validator-specific details from P-Chain RPC.
   - Output: `outputs/one_l1_validator_pchain_sample.json`

## Preliminary Variable Mapping

See `variable_mapping.md`.

## Security Note

The AvaCloud API key is stored locally in `.env` and is excluded from version control through `.gitignore`.