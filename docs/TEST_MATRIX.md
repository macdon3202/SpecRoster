# Verification matrix

| Requirement | Local evidence | Live gate |
|---|---|---|
| FIT to exclusive submitted review | `test_complete_happy_journey` | happy runner + browser write |
| OUT never creates an assignment | `test_out_creates_no_assignments` | EIP-1559 excluded scope |
| UNKNOWN blocks all assignment | `test_unknown_is_not_an_edge` | source mode / honest ambiguity |
| Capacity and deterministic tie | `test_capacity_and_task_tie_break` | multi-task round |
| Global optimum rather than greedy | `test_max_matching_not_greedy` | optional larger round |
| Exact consent and cross-round binding | consent and round digest regressions | guards mode |
| Integrity, commit/repo identity | source negative tests | sources mode |
| Wrong leader detected independently | validator rejection tests | actual multi-validator receipts |
| Retry bound and recovery | bounded retry, cancel tests | sources/cancel modes |
| Assignee, order and replay | assignment sequence tests | guards mode |
| Cancel vs late submit | cancellation regressions | cancel mode |
| Wallet Snaps compatibility | wallet tests | browser provider journey |
| Finality/execution/exact ID readback | transaction tests | production signed write |

`test_max_matching_not_greedy` injects a known matrix at the nondeterministic
boundary to test the actual contract's allocation path; it is not evidence that
live validators produced that matrix. Other validator tests separately exercise
independent re-observation.
