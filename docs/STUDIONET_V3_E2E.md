# SpecRoster V3 StudioNet E2E

Contract: [0xF7f8Ec0434F3Ca9C4976fcc106b49A2e98E4117B](https://explorer-studio.genlayer.com/address/0xF7f8Ec0434F3Ca9C4976fcc106b49A2e98E4117B)

Source SHA-256: `c92c5890070afaf9513545aacff44b729708b9d3bad8c517d33953511f9a175b`.
Exact deployed source match: `True`.
Main wallet used for lifecycle: `false`.

## Coverage boundary

Completed SDK modes: ``.
Signed production browser journey: **not proven**.
A finalized successful transaction is not by itself a successful business outcome.
Happy matching requires the predeclared FIT/OUT matrix and exclusive assignment;
UNKNOWN is not relabelled as FIT and blocked later steps are not counted as passed.

## Exact transactions and authoritative readback

| Scenario / action | Explorer | Finality / consensus | Verified | Expected error / state |
|---|---|---|---|---|
| happy / create | [tx](https://explorer-studio.genlayer.com/tx/0xe2b4e265c468b74cebb4c9b2341f6ea924b8715d8d323b2f92aa03c2663ae4c6) | FINALIZED / MAJORITY_AGREE | True | OPEN; matrix=[]; assignments=0 |
| happy / scope | [tx](https://explorer-studio.genlayer.com/tx/0x71b29b84ded5468816c283464a16b1141a1c281caf7be0137e86f403234198ae) | FINALIZED / MAJORITY_AGREE | True | OPEN; matrix=[]; assignments=0 |
| happy / freeze | [tx](https://explorer-studio.genlayer.com/tx/0xe37ed9e1081753edb99744dc4402f93456092e1f50f8d59786b8873a49d3482e) | FINALIZED / MAJORITY_AGREE | True | FROZEN; matrix=[]; assignments=0 |
| happy / consent | [tx](https://explorer-studio.genlayer.com/tx/0xee6e88cbce1e142a3b7e9c2b72233269c1b14e76064a66a1195609be0036d6fc) | FINALIZED / MAJORITY_AGREE | True | FROZEN; matrix=[]; assignments=0 |
| happy / allocate | [tx](https://explorer-studio.genlayer.com/tx/0x702cdac4d7944debfe446deabe963d3f75d6872e26a63dfd488fb2993371447b) | FINALIZED / MAJORITY_AGREE | True | ALLOCATED; matrix=[["OUT"], ["OUT"]]; assignments=0 |

Full receipts, declared inputs and before/after snapshots: [happy](evidence/0xf7f8ec0434f3ca9c4976fcc106b49a2e98e4117b-happy.json).


Suite stopped at: `happy`. Later coverage is not established.
