# Reviewer-owned wallet walkthrough

Contract V2: `0x7766cD870e3Ed9eA9Beb365550A7315d8E6DC462`.

No deployer permission or supplied test-wallet private key is required. This is a
two-party workflow: use two different accounts you control, or invite a willing
reviewer. One wallet cannot act as both creator and reviewer in the same round.
No automated counterparty service is claimed.

1. Open the locally built frontend, select an installed EIP-1193 wallet, connect
   to StudioNet and Sync workspace at the V2 address. Keep Round ID empty.
2. As creator A, use the published sample tasks. Invite reviewer B's address and
   create the round. Wait for finalized execution and exact returned-ID readback.
3. Switch to account B and sync the same round ID. Register the sample scope,
   capacity 1. The UI reloads role and authoritative state on account changes.
4. Switch to A, sync, inspect tasks and reviewer scope, then Freeze.
5. Switch to B, sync, inspect the frozen digest and Consent to that exact round.
6. Trigger semantic matching from either account. Expected sample matrix is
   FIT for EIP-712 and OUT for EIP-1559. UNKNOWN is safely unresolved; at most one
   retry remains after an unresolved first attempt. Do not relabel UNKNOWN or
   assume transaction SUCCESS means an assignment was created.
7. If ALLOCATED, B accepts its exact assignment, submits a review note, and then
   either account closes the completed round. Verify the note and state by
   syncing and opening transaction Explorer links.
8. Alternatively, A can cancel a nonterminal round. Pending assignments become
   CANCELLED; late submission must fail. Never resubmit a timed-out transaction:
   use Reconcile with its original hash first.

The deployment's creator/reviewer test accounts do not impose an allowlist on
new reviewer-created rounds. Capacity is per-round, not global. Submitted notes
are not review-quality or implementation-safety certificates. This workflow
holds no funds and pays no rewards.

Evidence and limitations: `STUDIONET_V2_E2E.md`. SDK live tests and SDK readback
are distinct from a production browser-wallet signing journey.
