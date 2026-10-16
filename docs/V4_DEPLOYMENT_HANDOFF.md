# V4 exact-source deployment handoff

## Deploy exactly this file

- Source: `contracts/spec_roster.py`
- Version: `SPEC_ROSTER_V4_CANDIDATE`
- SHA-256: `a2b9d42a8e42ac746008b2d327413eeb71b0a8184249ff9d07c09faedcbac46a`
- Constructor arguments: none
- Main wallet activity: deployment only

Do not edit, reformat or copy/paste the source through another editor before
deployment. The RPC-returned contract bytes must match the file byte-for-byte.

## Mandatory order after deployment

1. Run `py scripts/verify_live_v2.py ADDRESS --version SPEC_ROSTER_V4_CANDIDATE`.
2. The runner first executes the frozen eight-case StudioNet semantic gate.
3. It then continues independent preguards, source failure, happy, assignment
   guards and cancellation modes even if a semantic mode fails.
4. Do not update the frontend or call the project submission-ready unless every
   mode passes on this same address.
5. Then update the production contract address and run the signed browser-wallet
   lifecycle with receipt-to-state-to-UI reconciliation.

Evidence is written incrementally under `docs/evidence/`; interruptions resume
from locked method, arguments, actor and expected result. Failed model outcomes
are retained and must not be relabelled or removed.
