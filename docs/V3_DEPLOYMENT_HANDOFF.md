# V3 deployment handoff — not yet live verified

Historical only. Current source is an undeployed V4 audit candidate; follow
COMPREHENSIVE_AUDIT.md. Do not use the old hash below for current source or deploy
the historical V3 hash for the current source. V4 now uses a post-deployment
StudioNet semantic gate because no paid model API is available.

Deployment complete at `0xF7f8Ec0434F3Ca9C4976fcc106b49A2e98E4117B`, exact-byte
parity verified. Live happy failed its predefined semantic expectation:
OUT/OUT observed, FIT/OUT expected. Leader and validator logs both report OUT
for each pair, without pointer/schema exceptions. No assignment was created.
The suite stopped at happy; guards, source and cancellation modes on this V3
address were not reached. See STUDIONET_V3_E2E.md and
evidence/v3-happy-diagnostics.json. The historical preparation notes below do
not mean another deployment is currently requested.

Deploy `contracts/spec_roster.py` with the main wallet, no constructor arguments.
SHA-256: `c92c5890070afaf9513545aacff44b729708b9d3bad8c517d33953511f9a175b`.
Expected `get_config().version`: `SPEC_ROSTER_V3`.

V2's happy round 2 reached CLOSED after one retry. However guards round 4
exhausted both attempts with UNKNOWN/OUT. Leader and validator diagnostics
reported FIT_GROUNDING. V2 is therefore not demonstrated reliably operational;
assignment guards and cancellation of allocated work were not reached by that
suite. Do not claim all security tests passed.

V3 replaces model-copied quote strings with bounded integer pointers into
lossless segments of the full fetched source and declared scope. Concatenation
reconstructs the exact input; no source content is removed or summarized.
FIT rejects absent, negative, out-of-range, non-integer, boolean or blank-segment
pointers. Independent validators still refetch source, verify identity/digest,
read all context/exclusions, and independently judge the consequential relation.
Pointer existence alone is NOT a proof of semantic relevance. This change avoids
quote transcription errors; it does not guarantee model accuracy or live success.

Local verification: 49 public-entrypoint/helper tests pass, GenVM lint and
validation pass. Two unused web mocks are expected early-rejection warnings.
No V3 address, transaction or production browser signing evidence exists yet.
Historical V2 bytes remain at `contracts/archive/spec_roster_v2.py`.

After deployment:

```powershell
py -3.12 scripts/verify_live_v2.py NEW_ADDRESS --version SPEC_ROSTER_V3
```

The filename is retained for compatibility; explicit version gate and exact-byte
source parity prevent tests from silently targeting the wrong release.
Frontend production config remains the V2 address until V3 is supplied and
verified. Main wallet must not participate in lifecycle tests.
