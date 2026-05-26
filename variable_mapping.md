# Preliminary API-to-Variable Mapping

This preliminary mapping links the proposal's channel-decomposition variables to observable API fields and documentation sources.

| Proposal variable | Meaning | Preliminary data source | Observable fields | Proof status |
|---|---|---|---|---|
| V_fee | AVAX-denominated L1 validator fee exposure | P-Chain RPC / AvaCloud Data API | validator fee config, validator balance, remainingBalance | Initial API proof completed |
| V_part | L1 validator participation / validator commitment | AvaCloud Data API / P-Chain RPC | validationId, nodeId, subnetId, weight, creationTimestamp | Initial API proof completed |
| V_subnet | L1/subnet-level AVAX-side exposure | AvaCloud Data API / P-Chain records | subnetId, validator count, remainingBalance aggregation | Initial API proof completed |
| U_gas | L1-native gas usage | L1 explorer / EVM chain endpoints | transaction count, gas used, fees spent, gas token | Planned case-study extraction |
| U_route | Fee routing / burn / treasury / validator distribution | L1 documentation and contracts | fee destination, burn rules, treasury routing | Planned case-study coding |
| U_sec | L1-native security and validator demand | L1 documentation / contracts / explorer | staking asset, validator rewards, collateral requirements | Planned case-study coding |
| U_gov | Governance and monetary control localization | L1 documentation / governance docs / contracts | minting rights, reward manager, fee manager, permissioning | Planned qualitative classification |