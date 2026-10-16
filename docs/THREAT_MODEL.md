# Threat model

| Attack sequence | Invariant / safe outcome |
|---|---|
| Creator tries to consent for reviewer | Authenticated sender restriction; no mutation |
| Register scope after freeze | Intake closed; no mutation |
| Allocate before all consents | Rejected before web/AI |
| Copy round A digest into B | Exact round-bound digest rejection |
| Same raw URL with changed bytes | Recomputed digest fails; zero new assignments |
| Valid-looking commit from another repository | Canonical API URL mismatch blocks observation |
| Leader fabricates FIT | Validator reobserves and rejudges; mismatch rejected |
| LLM invents source quote | Substring grounding gate becomes UNKNOWN |
| Prompt injection in scope/source | Delimited untrusted data; independent judgment; bounded output |
| Two tasks compete for one capacity slot | Max-cardinality matching never exceeds declared capacity |
| Greedy choice would strand a task | Full bounded search finds maximum assignment count |
| Creator/stranger submits assigned review | Assignee-only check |
| Submit before accept | Phase rejection |
| Duplicate allocate or terminal submit | Terminal/replay rejection |
| Cancel after reviewer accepts, then late submit | Cancelled assignment and round stay closed |
| Reviewer disappears or source stays unavailable | Owner can cancel, including unfinished assignments |
| Wallet/account/round changes during transaction | UI invalidates previous context; exact readback required |
| FINALIZED but execution error/no majority | UI does not report success |

The owner can cancel voluntarily assigned work, but cannot impersonate a review
submission or erase submitted notes. Cancellation is an explicit trust boundary.
No stake, earnings, compensation or real-world fairness guarantee is claimed.

Fixed origins and tightly constructed paths remove arbitrary user URLs; DNS/TLS
and the provider's network policies remain dependencies. Redirect behavior that
cannot be induced at official endpoints is not labelled live-tested.

Self-authored notes are not accepted as proof of implementation or CI. Scope
authorship is deliberately self-declared because it authorizes only that wallet's
voluntary work queue, not certification, money or external system privileges.
