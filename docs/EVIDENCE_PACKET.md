# SpecRoster evidence packet

Current authority: [COMPREHENSIVE_AUDIT.md](COMPREHENSIVE_AUDIT.md). Current V4
candidate passed pre-deployment local checks and is ready for one exact-source
test deployment. It is not submission-ready until the eight-case StudioNet
semantic gate, lifecycle suite and signed browser journey pass. No paid API is
required. Earlier deployment-readiness paragraphs are historical.

Latest: V2 suite stopped at guards after two FIT_GROUNDING failures. Current V3
candidate is locally verified only; see V3_DEPLOYMENT_HANDOFF.md. Historical
readiness statements below must not be treated as current all-tests-passed claims.

Readiness: V2 deployed with exact source parity and sample happy lifecycle
verified after a bounded retry. Remaining security modes are in progress.
See [STUDIONET_V2_E2E.md](STUDIONET_V2_E2E.md). V1 live matching remained
unresolved; recovery was verified. Full positive lifecycle and production UI
verification are still pending. See [STUDIONET_E2E.md](STUDIONET_E2E.md).

1. Read proof boundaries in README and `PROOF_OBLIGATION.md`.
2. Run `py -3.12 scripts/verify.py`.
3. Inspect `contracts/spec_roster.py` and pinned two-line runner header.
4. Inspect `samples/public-round.json`, both complete standards and their digests.
5. After deployment, record source hash, exact network/chain, address and deploy tx.
6. Run capability-specific StudioNet scripts, retaining every checkpointed hash.
7. Complete a production browser-wallet write and compare the same round/assignment
   to authoritative readback and Explorer.

No deployment, transaction hash or browser signing result is invented in this
packet. `docs/evidence/` will contain exact-address JSON after real runs.

## Release identity requirements

Bind repository commit, exact deployed source SHA-256, deploy tx, address, runner,
SDK version, frontend build commit and production URL. Contract changes require
replacement deploy and fresh evidence. Failed/old deployments remain historical.

For every rejected live transaction capture complete round(s), assignment(s),
counters and digest before/after; verify actual leader error and equality.

## What is not claimed

- Live StudioNet lifecycle or deployment has not yet run.
- Local browser inspection is not wallet-signing E2E.
- No production URL, financial settlement or external review certification.
- Model/network faults covered by local injection are not called live tests.
- This is self-verification, not independent third-party assurance.
