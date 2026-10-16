# SpecRoster StudioNet verification

Contract: [0x07B305921D3c315EBb6708e4F51797a57485bf90](https://explorer-studio.genlayer.com/address/0x07B305921D3c315EBb6708e4F51797a57485bf90)

## Source parity

Historical RPC-fetched V1 source matches archived V1 bytes: `True`.
SHA-256: `a91d61cbe236cf13ce96b8eead7087e960cce399061db1319c4dc9aa63bc3138`.

## Actors

Creator: `0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43`.
Reviewer: `0xc67532aeF9D2879cBA9375a02E6217A3524657B8`.
Main wallet used in lifecycle: `false`.

## Transactions

| Action | Explorer | Observed result |
|---|---|---|
| create | [Transaction](https://explorer-studio.genlayer.com/tx/0x9db7ae3b53982aab5c30d327140d97eceae1ec5e43afe7f4edbe86db80003f98) | FINALIZED / MAJORITY_AGREE / OPEN |
| scope | [Transaction](https://explorer-studio.genlayer.com/tx/0x7c176a5804be8e96742cac1dd41623a0672cc7624dffd4b3357ba22dd4c154d4) | FINALIZED / MAJORITY_AGREE / OPEN |
| freeze | [Transaction](https://explorer-studio.genlayer.com/tx/0x34f635f89afedd24e34be002d8c3cee2b6cf2ddaebb142d3dde189f3d60a041c) | FINALIZED / MAJORITY_AGREE / FROZEN |
| consent | [Transaction](https://explorer-studio.genlayer.com/tx/0x77d29df0197eb20bdd026fadf8f55ae09f5910376e9b2c9338d3b19241c50bf8) | FINALIZED / MAJORITY_AGREE / FROZEN |
| allocate | [Transaction](https://explorer-studio.genlayer.com/tx/0xa2f5eeb1457a52b362dbd82d12e197a4afa388cd8a4ed6f279974b3ba7e25ec6) | FINALIZED / MAJORITY_AGREE / UNRESOLVED / [["UNKNOWN"], ["OUT"]] |
| allocate_retry | [Transaction](https://explorer-studio.genlayer.com/tx/0x1262977a54d756d4d1c635518a618ac6ce71dec36257c53c7bdb94f91f3da0ff) | FINALIZED / MAJORITY_AGREE / UNRESOLVED / [["UNKNOWN"], ["OUT"]] |
| exhausted | [Transaction](https://explorer-studio.genlayer.com/tx/0x393180a37f11d6da5c4a6605fe858b9461e5d1ec6ba1e9a64c6cc199c85283dc) | ATTEMPTS_EXHAUSTED; complete state unchanged |
| cancel | [Transaction](https://explorer-studio.genlayer.com/tx/0x8ac03333e30ada89dd32b9957b733f518a1ab3f826f717df42551b29e5398f60) | CANCELLED; no assignments |

## Coverage boundary

Both initial assessment and bounded retry produced `UNKNOWN / OUT`, so the
contract created zero assignments. The expected FIT/OUT matrix was specified
before execution and was not rewritten. This run does not establish a complete
happy lifecycle, reviewer acceptance/submission, or signed production browser E2E.
The current matrix does not expose why the FIT candidate became UNKNOWN; the
root cause cannot be inferred solely from its returned status.

Full checkpointed receipts and authoritative before/after snapshots: [happy run](evidence/0x07b305921d3c315ebb6708e4f51797a57485bf90-happy.json), [recovery](evidence/unresolved-recovery.json).

## Additional V1 source/authorization runs

These are separate from the incomplete happy journey. A transaction is not
marked verified until finality, leader execution and readbacks have been checked.

| Scenario/action | Explorer | Verified | Rollback equal |
|---|---|---|---|
| sources / create | [Transaction](https://explorer-studio.genlayer.com/tx/0x70e7169022df3a89a5d7bb2d78dbae7d054d011fc53ef9096c0d7681d49506ee) | True | n/a |
| sources / scope | [Transaction](https://explorer-studio.genlayer.com/tx/0x271fb355704690fb7ea752ca3de733baba75e5af13130ec7627e123322058b65) | True | n/a |
| sources / freeze | [Transaction](https://explorer-studio.genlayer.com/tx/0x181ce008d65f34385dd8a16ddc911e7d56b7137c71c351a91a34feae8a2b87c0) | True | n/a |
| sources / consent | [Transaction](https://explorer-studio.genlayer.com/tx/0xebe70b4d38457edd738a8f281b4409853e11c4e61b7afe66b855b394f1d47366) | True | n/a |
| sources / allocate | [Transaction](https://explorer-studio.genlayer.com/tx/0x54d116ccb0b06f854fdc9f329bcff98871c1c1f8db92a3b31afd37cae35e4fe7) | True | n/a |
| sources / cancel | [Transaction](https://explorer-studio.genlayer.com/tx/0xe54cb8f4fbbd29d0f309f5188499c866e282b26e26f2e128e1922c047cf31d8d) | True | n/a |

Full checkpoints: [sources](evidence/0x07b305921d3c315ebb6708e4f51797a57485bf90-sources.json).


Current contracts/spec_roster.py is an undeployed V2 candidate; the V1 parity proof applies only to contracts/archive/spec_roster_v1.py.
