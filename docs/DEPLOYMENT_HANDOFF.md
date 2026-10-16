# Deploy SpecRoster

Superseded for current source: use [V3_DEPLOYMENT_HANDOFF.md](V3_DEPLOYMENT_HANDOFF.md).
The remainder describes historical V2; its source is archived and is not the
current contracts/spec_roster.py.

Use the main wallet only to deploy `contracts/spec_roster.py` with no constructor
arguments. Do not change the two pinned runner header lines.

Expected source SHA-256:
`47a02ed43013cc4b735a96418554743702842e4f80d7e3885ec06a213587daff`.

V2 is deployed with exact source parity at
`0x7766cD870e3Ed9eA9Beb365550A7315d8E6DC462`. It is not the source deployed at
historical `0x07B305921D3c315EBb6708e4F51797a57485bf90`. The exact historical V1 bytes
are retained in `contracts/archive/spec_roster_v1.py` (SHA-256
`a91d61cbe236cf13ce96b8eead7087e960cce399061db1319c4dc9aa63bc3138`).
V2 preserves fail-closed FIT gating, tightens quote instructions, and prints
bounded diagnostic codes without publishing raw model responses or free-form
reasoning. These changes do not prove that the original UNKNOWN cause is fixed.
V2's main-wallet deployment is complete; no upgrade mechanism exists in V1.
The V2 sample reached CLOSED after one unresolved initial assessment and a
successful second attempt. See `STUDIONET_V2_E2E.md` for exact live coverage.

After deployment record the address and deploy transaction. Verify `get_config`:

```json
{
  "version": "SPEC_ROSTER_V2",
  "architecture": "SEALED_BATCH_SEMANTIC_MATCHING",
  "deployer_authority": "NONE",
  "round_count": 0,
  "assignment_count": 0,
  "max_tasks": 4,
  "max_reviewers": 4,
  "max_attempts": 2,
  "source_repository": "ethereum/EIPs",
  "funds": "NONE",
  "capacity_scope": "PER_ROUND"
}
```

Run live scripts using the two auxiliary wallets. The exact deployment must be
used for happy, guards, source-integrity and cancellation evidence. Production
frontend must then compile the same address or select it explicitly at runtime.
Reviewer-owned wallets can create their own rounds and invite arbitrary other
wallets; the deployer is not a required participant.

After the main-wallet deployment, run:

```powershell
py -3.12 scripts/verify_live_v2.py NEW_CONTRACT_ADDRESS
```

The suite checks exact source bytes before any writes, uses auxiliary keys only,
then runs pre-consent authorization/terminal rollback, source-integrity failure,
happy lifecycle, assignment guards and cancellation/late-submit conflict. It stops
on failure rather than marking later gates passed. This new orchestration script
is now running against the exact V2 address above. Browser
signing remains separate; SDK tests are not labelled browser E2E.
