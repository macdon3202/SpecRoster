# SpecRoster

## Current release boundary

**Current V4: exact-source StudioNet deployment and complete SDK live suite pass;
signed browser-wallet verification remains pending.**
Current source replaces direct verdict selection with three semantic predicates
and deterministic routing. Full findings and release gates:
[comprehensive audit](docs/COMPREHENSIVE_AUDIT.md). Historical V3 source is now
`contracts/archive/spec_roster_v3.py`; historical V1/V2/V3 evidence is NOT proof
for the current source. The frozen eight-case corpus passed directly through
StudioNet validators using the two auxiliary wallets. See the single reviewer
entry point: [V4 StudioNet E2E](docs/STUDIONET_V4_E2E.md).
The paragraphs below preserve deployment history.

**V3 live update:** deployed exact-source at
`0xF7f8Ec0434F3Ca9C4976fcc106b49A2e98E4117B`. The first sample assessment
finalized with OUT/OUT instead of the predeclared FIT/OUT; no assignments were
created. The suite stopped at happy. This is a semantic expectation failure,
not a successful happy path; V3 is not ready for submission. See
[V3 live evidence](docs/STUDIONET_V3_E2E.md).

**Latest:** V2 guards exhausted both attempts with `FIT_GROUNDING`; the suite
stopped before assignment guards/cancel coverage. Current source is an undeployed
**V3 candidate**, 49 tests and GenVM validation pass. Deploy instructions and
exact source hash: [V3 handoff](docs/V3_DEPLOYMENT_HANDOFF.md). Historical V2
source is `contracts/archive/spec_roster_v2.py`; frontend still targets V2.
The V2 results below are historical and do not prove V3 readiness.

Historical **V2** was deployed at
`0x7766cD870e3Ed9eA9Beb365550A7315d8E6DC462` with exact byte parity.
41 contract tests and GenVM lint/validation pass. Frontend: 16 tests pass.
V2 happy lifecycle reached CLOSED after a fail-closed first assessment and a
successful bounded retry; remaining live security modes are still in progress.
Production config now selects V2. Signed browser E2E and public hosting are not
proven. See `docs/STUDIONET_V2_E2E.md`; historical V1 source and evidence remain
separate in `contracts/archive/spec_roster_v1.py` and `docs/STUDIONET_E2E.md`.

Live status: source-matched deployment
[`0x07B305921D3c315EBb6708e4F51797a57485bf90`](https://explorer-studio.genlayer.com/address/0x07B305921D3c315EBb6708e4F51797a57485bf90).
The first live matching round and retry returned `UNRESOLVED`; no assignments
were created. Full happy-path verification is not yet established.
See [actual StudioNet results](docs/STUDIONET_E2E.md).

SpecRoster assigns Ethereum-standard review tasks to consenting reviewer wallets
only after GenLayer validators establish that each assigned task fits the exact
review scope those wallets accepted.

## Scope

This release implements a capacity-bounded review queue inside SpecRoster.
Assignments reserve per-round slots and grant the assigned wallet the exclusive
ability to accept and submit its review note. The creator can cancel unfinished
work; cancelled assignments cannot receive late submissions.

It does not certify expertise, review quality, implementation correctness,
standard adoption, employment eligibility or completion outside this application.
There are no funds, rewards, global reviewer-availability guarantees or wall-clock
deadlines. `SUBMITTED` means the assigned wallet submitted text, not that the
review was independently approved. Capacity is local to a round.

## Why GenLayer

Natural-language task requirements and reviewer scopes contain contextual
inclusions and exclusions. Validators independently read the complete standard
and determine each task–scope relation. This relation controls which assignment
can exist. Deterministic code handles consent, identity, source integrity,
capacity, matching, assignment ownership and terminal transitions.

## Evidence authority

- Evidence: exact file bytes at a full commit in the fixed `ethereum/EIPs` repository.
- GitHub authenticates repository commit identity and published artifact bytes.
- The contract reconstructs canonical URLs, verifies the returned commit/repo
  identity, EIP frontmatter and SHA-256 of the complete fetched source.
- The standard document is evidence of its contents; it does not prove an
  implementation, CI execution or runtime behavior.
- Reviewer scope is a voluntarily authored statement bound to transaction sender;
  it is not a credential.

## Mechanism

```text
create_round → register_scope → freeze_round → consent_round
                                                   ↓
                                    allocate_round (independent validators)
                                      ├─ unresolved → retry once / cancel
                                      └─ matrix FIT/OUT → deterministic matching
                                                          ↓
                                        update_assignment ACCEPT → SUBMIT/DECLINE
                                                          ↓
                                                    close_round
```

`cancel_round` is creator-only, can end unfinished rounds, and atomically cancels
all nonterminal assignments. It cannot erase submitted review history.

The deployer has no stored role. Any wallet can create a round and invite other
wallets; the creator cannot be a reviewer in the same round. Reviewers must consent
to the complete frozen bundle containing every task, source, reviewer scope and
capacity. The digest also binds the exact contract and round ID. Fields cannot be
silently updated after consent.

## Semantic and execution boundary

The current candidate asks for `source_support`, `scope_coverage` and
`scope_exclusion` as YES/NO/UNKNOWN facts with bounded pointers into full source
and scope. Code alone derives FIT from YES/YES/NO; any UNKNOWN blocks the round.
Valid pointers identify actual text, but do not prove semantic truth.
Validators refetch and independently rejudge all cells. A custom validator accepts
only identical consequential matrices and source status; different diagnostic
wording is excluded from consensus.

Any unknown cell or source failure blocks allocation for the entire round. There
are at most two assessment attempts. Known matrices are matched using a bounded
maximum-cardinality search, with deterministic task/reviewer tie-breaks.
Limits: 4 tasks, 4 reviewers, 60,000 bytes per complete source, 16 semantic pairs.

## Originality

This is `SEALED_BATCH_SEMANTIC_MATCHING`, not a renamed ABI compatibility docket.
It combines multi-party consent, a task–reviewer relation matrix, bounded matching
under capacity, and exclusive assignment operations. Its persistent objects are
rounds and work assignments, not standalone compatibility certificates. Its
judgment changes a work queue that the contract itself enforces.

## Local verification

```powershell
py -3.12 -m pip install -r requirements-dev.txt
py -3.12 scripts\verify.py
```

The script runs Direct Mode tests, GenVM lint/validation, a clean frozen frontend
install, frontend tests and production build. See
[verification](docs/VERIFICATION.md) for actual results and limitations.

Frontend preview: `npm run dev --prefix frontend`.
The supplied logo is used directly, without a regenerated replacement.

## Deployment and two-wallet path

The current candidate has passed its pre-deployment local gates. Deploy it once
from the main wallet, then follow the post-deployment gates in
`docs/COMPREHENSIVE_AUDIT.md`. Deploy from the main wallet
with no constructor
arguments. Production configuration points to the source-matched deployment
above; the UI also accepts a runtime address and validates `SPEC_ROSTER_V1` on
sync/write. Production browser signing remains unverified.

Use auxiliary A as creator and auxiliary B as invited reviewer. The live runner
loads only `SERVICE_LEDGER_KEY_A/B` from the existing ignored sibling secrets
file; no main-wallet key is loaded. Run each capability separately:

```powershell
py scripts\studionet_e2e.py CONTRACT_ADDRESS happy
py scripts\studionet_e2e.py CONTRACT_ADDRESS guards
py scripts\studionet_e2e.py CONTRACT_ADDRESS sources
py scripts\studionet_e2e.py CONTRACT_ADDRESS cancel
```

These scripts use real faucet transactions and validator calls. Every submitted
hash is checkpointed before waiting; a rerun resumes the same hash. Happy path
requires eight writes (create, scope, freeze, consent, allocate, accept, submit,
close). Costs/latency depend on StudioNet; no fixed budget is asserted.

Programmatic signing proves contract lifecycle only. A production browser-wallet
journey still must be signed and reconciled separately.

## Verification resources

- [Proof and authority model](docs/PROOF_OBLIGATION.md)
- [Threat model and sequence tests](docs/THREAT_MODEL.md)
- [Source manifest](docs/TEST_RESOURCE_MANIFEST.md)
- [Public replay inputs and immutable documents](samples/public-round.json)
- [Test matrix](docs/TEST_MATRIX.md)
- [Evidence packet](docs/EVIDENCE_PACKET.md)
