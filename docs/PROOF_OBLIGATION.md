# Proof obligation and authority model

## Claim

This is the intended proof obligation, not a proven accuracy guarantee. Prior
live V2/V3 runs failed the semantic reliability gate. The current candidate must
pass unmocked preflight and same-source StudioNet tests before this claim is
presented as demonstrated functionality. Consensus validates agreement, not
objective truth; colluding or consistently mistaken models remain a limitation.

For an allocated assignment, the material review task is within the assignee's
explicitly consented scope and supported by the complete, pinned standard text.
Its allocation respects per-round capacity and deterministic tie-breaking.

## Falsifiers

A requirement contradicts a scope exclusion; required subject matter is absent
from the source; source bytes do not match the commitment; consent belongs to a
different round; or an assignment violates capacity/ownership.

## Sufficient evidence

The frozen complete task/scope bundle, exact reviewer sender consent, canonical
repository commit record, complete standard bytes and their recomputed digest,
and independently derived validator matrix are required. No interested party can
replace the external standard with its own repository/report.

## Authority separation

| Authority | What it proves | What it cannot prove |
|---|---|---|
| GitHub ethereum/EIPs | Exact repository commit and file content | Implementation or test execution |
| Reviewer transaction sender | Authorship and consent for exact scope/round | Expertise or identity credentials |
| GenLayer validators | Bounded task–scope semantic relationship | Review quality or standard safety |
| SpecRoster deterministic code | Matching, capacity, exclusive task operations | External work performed |

## Consequence

Only validator-accepted FIT edges can become assignments. Only the exact assigned sender can
accept or submit to that assignment, and only with its round digest while that
round is allocated. Assignment creation and counter changes occur atomically.
Cancellation invalidates pending work before any late action can take effect.

`UNKNOWN`, source failure and malformed output do not authorize assignments.
Consensus rejection cannot be treated as business success by the client.

## Consent and time

All task/source/scope/capacity fields exist before freeze. Every registered
reviewer consents to that exact frozen digest. Contract and round identity are
domain-separated. No parent consent authorizes future tasks or changed scopes.
This is a version-bound observation and routing system, not continuous monitoring.
There are no security claims based on unsupported clocks.
