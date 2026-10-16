# SpecRoster local verification

## Current comprehensive audit

Current source is the undeployed V4 candidate. **145 Python tests**, 1,728
supplementary matching-oracle cases, **19 frontend tests**, GenVM validation and
production build pass. Real pinned-source retrieval/ancestry checks pass.
No paid-model API is required. The local gate authorizes one exact-source test
deployment; the fixed eight-case semantic corpus must then pass on StudioNet.
See [COMPREHENSIVE_AUDIT.md](COMPREHENSIVE_AUDIT.md) and the machine-readable
`evidence/local-audit.json`. All V1/V2/V3 sections below are historical.

## V3 live result

Exact-source deployment verified at `0xF7f8Ec0434F3Ca9C4976fcc106b49A2e98E4117B`.
Happy semantic expectation FAILED: OUT/OUT observed versus FIT/OUT predefined.
No assignment; later suite modes not run. No pointer exception in leader or
validator diagnostics. Local pass does not override this live failure.

## Latest V3 candidate

49 local tests and GenVM lint/validation pass. V3 is not deployed. Exact hash and
design change: [V3_DEPLOYMENT_HANDOFF.md](V3_DEPLOYMENT_HANDOFF.md).
V2 guards exhausted two attempts at FIT_GROUNDING; later assignment guards and
cancel suite did not run. V2's successful happy round does not erase that failure.

## V2 candidate verification (2026-10-16)

- Current source: `contracts/spec_roster.py`, version `SPEC_ROSTER_V2`.
- SHA-256: `47a02ed43013cc4b735a96418554743702842e4f80d7e3885ec06a213587daff`.
- Public-entrypoint Direct Mode tests: **41 passed** (two expected unused-web-mock warnings).
- GenVM: lint 3 checks and validation pass, 11 methods.
- Frontend: **16 tests passed**, production build passed; bundle-size warning remains.
- Default sandbox denied Node subprocess spawn; approved escalated verify passed.
- V2 is deployed with exact source parity at `0x7766cD870e3Ed9eA9Beb365550A7315d8E6DC462`.
- V2 sample happy lifecycle reached CLOSED after a fail-closed first assessment
  and a successful bounded retry. Other live modes are still in progress.
- Frontend snapshot independently read CLOSED round 2 and SUBMITTED assignment 1.
- No claim of production signed browser verification.
- Historical V1 source remains byte-identical in `contracts/archive/spec_roster_v1.py`.

The sections below are historical V1 verification, not a V2 deployment proof.

## Subsequent StudioNet run

Deployed address: `0x07B305921D3c315EBb6708e4F51797a57485bf90`.
RPC source bytes exactly match the hash below. Initial matching and one retry
finalized with majority agreement but returned `UNKNOWN / OUT`, creating zero
assignments. A third attempt reverted `ATTEMPTS_EXHAUSTED` with complete state
unchanged. Owner cancellation finalized and round became `CANCELLED`.
Happy assignment/accept/submit lifecycle remains unverified. See
[STUDIONET_E2E.md](STUDIONET_E2E.md).

Production build with this address passed. Production hosting and signed browser
journey have not run. Earlier pending-deployment notes below describe the local
verification stage rather than current deployed status.

Date: 2026-10-16 (Asia/Bangkok).

## Results

- Direct Mode: **34 passed**, no failed or skipped tests.
- GenVM lint: 3 checks passed; semantic validation passed.
- Contract interface: 11 public methods, 3 views and 8 writes.
- Clean `npm ci --ignore-scripts`: passed; 236 packages installed; npm reported
  no known vulnerabilities in that run.
- Frontend tests: **15 passed**, no failed or skipped tests.
- Production build: passed (Vite 7.3.7).
- Lifecycle/source/verification scripts: Python compile checks passed.

The full pipeline `py -3.12 scripts/verify.py` passed after stopping Vite so
Windows could replace its locked esbuild executable. A subsequent focused
frontend verification passed after adding the pending-journal regression.

## Source and tools

Contract SHA-256:
`a91d61cbe236cf13ce96b8eead7087e960cce399061db1319c4dc9aa63bc3138`.

Pinned runtime header: v0.2.16 and
`py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.

Python 3.12; genlayer-test 0.29.2; genlayer-py 0.16.3; genvm-linter 0.11.0;
pytest 9.1.1. Node v26.2.0; npm 11.13.0; frontend lockfile tracked for replay.

## Browser inspection

Local browser at `http://127.0.0.1:5176/` displayed the supplied logo, task routing
layout, empty deployment configuration and disabled write action. Clicking Connect
without an injected wallet displayed `Choose an installed EIP-1193 wallet.`
This was visual/missing-provider verification, not a signed wallet lifecycle.

## Warnings and limits

- Two unused raw-source mock warnings are expected in commit/repository rejection
  tests: the contract stops before requesting raw bytes.
- The Windows-only gltest shim defers unlinking the fd0 temporary file; it does
  not replace contract logic or the validator.
- npm reports a transitive ESLint deprecation; it did not fail install/tests.
- Vite reports a roughly 735 kB minified entry chunk (~179 kB gzip), dominated by
  the blockchain SDK. This is a performance warning, not a passing bundle-budget
  claim.
- StudioNet source access, finality, semantic outcomes, exact deployed-source
  parity and browser signing remain pending deployment.
- No GitHub push, public hosting or submission has been performed for this project.
