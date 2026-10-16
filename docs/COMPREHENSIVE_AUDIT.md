# SpecRoster comprehensive audit — 2026-10-16

## Outcome

Current source: `SPEC_ROSTER_V4_CANDIDATE`, **not deployed, ready for one
test deployment but NOT submission-ready**.
SHA-256: `a2b9d42a8e42ac746008b2d327413eeb71b0a8184249ff9d07c09faedcbac46a`.
One exact-source replacement deployment is now requested. This is required to
run the real StudioNet validator gate because the project owner has no paid model
API. It is not evidence of semantic success by itself.

The earlier process promoted local mock success into deployment requests before
the semantic design had been demonstrated. That was insufficient. Historical V2
had one successful happy round but failed its later guards round. V3's first
sample returned OUT/OUT rather than the predefined FIT/OUT. Neither failure is
deleted, relabelled, or replaced by another favourable sample.

## Findings and the consolidated fixes

| ID | Finding | Candidate change / regression | Evidence boundary |
|---|---|---|---|
| A01 | Opaque verdict provided no stable separation between source support, reviewer capability and exclusion | Three YES/NO/UNKNOWN predicates; task requirement only; capabilities are union, not extra obligations; code derives FIT only from YES/YES/NO | Logic verified across all 27 combinations; real-model accuracy NOT proven |
| A02 | Literal quote transcription blocked valid-looking FITs; V3 pointer change did not establish semantic reliability | Bounded pointers retained, boolean/invalid/blank pointers rejected; independent validators re-read full input; diagnostic fact tuple recorded | Pointer existence is not truth; no claim that a wrong model cannot agree |
| A03 | Malformed consensus cell such as list/dict could raise during set membership | Validate cell type before enum membership | Public-entrypoint poisoned-consensus regressions |
| A04 | Commit object retrieval alone did not explicitly establish canonical-branch ancestry | Verify ahead/identical comparison, exact base and merge-base SHA on ethereum/EIPs:master; policy bound into freeze digest | Mock regressions + actual public endpoint checks; NOT yet tested inside validator network |
| A05 | Segment expansion had no separate prompt budget | Full input retained; >100,000 prompt bytes → UNKNOWN before model call | Expanded-newline adversarial regression proves no LLM call |
| A06 | Create readback checked title/owner but not full tasks/invites | Canonical exact bundle comparison | Frontend regression tests |
| A07 | Assignment reads were not fully linked to allocation/reviewer/capacity | Check exact ID, round, task, assignee, digest, uniqueness, capacity and terminal state | Frontend regression tests; no new signed browser claim |
| A08 | Incomplete finalized RPC receipt was treated like a known revert | Missing authoritative data remains pending; only known errors fail | Prevents unlocking duplicate signing from missing receipt fields |
| A09 | Invalid numeric selection and stale sync error could corrupt selection UX | Positive safe-integer parser; stale sync errors ignored | Frontend tests; further rendered account-switch tests remain required |
| A10 | Persisted journal could evict old pending entries | Retain every PENDING entry; bound only completed history | Code correction; storage quota/browser crash durability not guaranteed |
| A11 | Resume could reuse a hash after args, actor or expectation changed | Checkpoint locks method/args/actor/error and corpus expectation | Runner policy tests; no silent fixture refresh by default |
| A12 | Expected-error substring could be accepted from a successful receipt or unrelated stdout | Require authoritative ERROR/REVERT plus error in result and complete pre/post equality | False-error evidence regression |
| A13 | Stopping the whole suite on first semantic failure hid independent security coverage | Record failed modes and continue independent modes; overall suite still fails | Candidate runner policy; not yet exercised as a full live suite |
| A14 | Zero assignments could look like successful positive routing | Explicit NO_ELIGIBLE_REVIEWERS reason; reports distinguish transaction and business success | Contract enum regression and existing no-edge test |
| A15 | Documentation mixed current source with old deployment proofs | Archive V1/V2/V3 exact sources; current audit status takes precedence | Source hashes and retained historical evidence |

## Verification actually completed

- **145 Python tests passed**, zero failures/skips/warnings in final run.
- Includes actual public entrypoint lifecycle, sender, wrong digest, missing
  consent, duplicate consent/registration, stale and unknown IDs, phase and actor
  permutations, cancellation/late submission, review UTF-8 byte boundaries,
  source identity/digest/frontmatter/size failures, bad ancestry, malformed model
  output, unknown predicates and independent validator disagreement.
- One supplementary property test enumerates **1,728** 2-task/3-reviewer matrix
  and capacity combinations against an independent matching oracle. These are
  not 1,728 additional live transactions or AI judgments.
- **19 frontend tests passed**; production build passed. Vite SDK-bundle size
  warning remains. No new dependency install/audit was claimed in this run.
- GenVM: 3 lint checks and interface validation passed, 11 public methods.
- Two real public EIP resources were fetched without redirects. Exact existing
  source hashes and local copies matched; both commits are ancestors of master.
  Fixture pins and expected FIT/OUT matrix were NOT changed.

Machine evidence: [local gate](evidence/local-audit.json),
[public source checks](evidence/public-source-audit.json),
[unmocked preflight status](evidence/semantic-preflight.json).

## Release gates — no more deploy-by-guessing

1. Local gate above passes for exact source.
2. Deploy this exact byte sequence once using the main wallet. Confirm the RPC
   source bytes and `get_config` version before any lifecycle test.
3. Run `scripts/studionet_semantic_gate.py ADDRESS`. It exercises the frozen
   eight-case corpus through the deployed contract and StudioNet validators.
   Wallet A creates; wallet B registers and consents. Expectations cannot change,
   every write is checkpointed, and failed observations remain in evidence.
4. Only after all eight cases pass, run the complete same-address StudioNet
   lifecycle, source, authorization, assignment/replay and cancellation suite.
   Any source change invalidates the deployment and requires all gates again.
5. Signed browser-wallet lifecycle and UI readback are separate required gates.
   SDK reads, mocked EIP-1193 tests and a frontend build do not count as that gate.

## Current blocker, not a hidden pass

The only current blocker is the missing exact-source V4 StudioNet deployment.
No paid provider credential is needed. `scripts/semantic_preflight.py` remains an
optional local live-provider tool, but it is not a release prerequisite.
The mandatory replacement is `scripts/studionet_semantic_gate.py` using the fixed
`samples/semantic-preflight.json` corpus. The runner does not load the main wallet
and cannot deploy; it uses only the two existing auxiliary test wallets.

Unit tests cannot establish semantic accuracy or guarantee all possible attacks
are absent. The StudioNet semantic/lifecycle and browser gates are mandatory.
Current status is LOCAL_PASS_DEPLOYMENT_CANDIDATE, not submission-ready.

Reference for testing boundaries: [GenLayer testing documentation](https://docs.genlayer.com/developers/intelligent-contracts/testing).
