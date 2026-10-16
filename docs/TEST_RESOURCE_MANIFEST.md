# Source resource manifest

Current audit checks are in evidence/public-source-audit.json. Both original
pins/digests and expected matrix remain unchanged. V4 additionally requires
canonical master ancestry (exact base/merge-base comparison metadata); the API
page used for ancestry is NOT a code-diff completeness proof. Semantic preflight
expectations are separately frozen in samples/semantic-preflight.json.

See `samples/public-round.json` for machine-readable fields, exact commit URLs,
digests, expected source facts, expected matrix and expected allocation. Expectations
are specified before live AI execution, and must not be rewritten to fit results.

| Resource | Authority | Full commit | Expected role |
|---|---|---|---|
| EIP-712 | ethereum/EIPs published file | `0b06de5e1203b35f1338d9e61d1ccc6965face91` | FIT to typed-signing scope |
| EIP-1559 | ethereum/EIPs published file | `ba6c342c23164072adb500c3136e3ae6eabff306` | OUT: scope explicitly excludes fee markets |

Public retrieval and complete-byte digests checked on 2026-10-16. Validator-network
retrieval and semantic outcomes remain unverified until a real StudioNet run.

Repository is fixed; full 40-character commit and canonical EIP path identify the
artifact. SHA-256 is computed from full response bytes, not a document excerpt.
Local copies are replay material; the contract fetches canonical remote bytes.
GitHub authority is for content publication, not real-world review competence,
implementation changes, CI success or runtime effects.

## Negative controls

- Same pinned document, deliberately wrong digest: UNRESOLVED, no assignments.
- Wrong EIP frontmatter or wrong repository commit URL: UNRESOLVED.
- HTTP 404/429/5xx, timeout, oversize body: safe unresolved outcome.
- Valid source with excluded scope: OUT, no edge for that task.
- Invented FIT quote: UNKNOWN, no allocation for the batch.
- Source bytes changed after leader result: independent validator rejects.

Network fault/model injection controls are synthetic local fixtures, explicitly
not authoritative public evidence. Tests call the actual contract entrypoints.
