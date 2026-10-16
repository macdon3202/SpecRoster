# V4 StudioNet live status

Contract: [0xB404f8Da18cc736aD21917929dc52993913F1D98](https://explorer-studio.genlayer.com/address/0xB404f8Da18cc736aD21917929dc52993913F1D98)

- Exact RPC source bytes match `contracts/spec_roster.py`.
- Source SHA-256: `a2b9d42a8e42ac746008b2d327413eeb71b0a8184249ff9d07c09faedcbac46a`.
- Fixed StudioNet semantic corpus: **8/8 passed**.
- Preguards, authoritative revert receipt checks and rollback equality: **passed**.
- Source failure, happy lifecycle, assignment guards and cancellation: **passed**.
- SDK live suite status: **PASS** on the same exact-source address.
- Remaining independent gate: signed browser/UI reconciliation.

The runner was corrected to use focused snapshots, 12-second finality polling,
durable Ethereum submission hashes and completed-mode skipping. Transient 502,
disconnect and rate-limit incidents are retained in the audit history and were
recovered without redeploying the contract.

Machine evidence:

- `docs/evidence/0xb404f8da18cc736ad21917929dc52993913f1d98-semantic-gate.json`
- `docs/evidence/0xb404f8da18cc736ad21917929dc52993913f1d98-preguards.json`
- `docs/evidence/0xb404f8da18cc736ad21917929dc52993913f1d98-v4_candidate-suite.json`
