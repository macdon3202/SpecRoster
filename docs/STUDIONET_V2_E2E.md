# SpecRoster V2 StudioNet E2E

Contract: [0x7766cD870e3Ed9eA9Beb365550A7315d8E6DC462](https://explorer-studio.genlayer.com/address/0x7766cD870e3Ed9eA9Beb365550A7315d8E6DC462)

Source SHA-256: `47a02ed43013cc4b735a96418554743702842e4f80d7e3885ec06a213587daff`.
Exact deployed source match: `True`.
Main wallet used for lifecycle: `false`.

## Coverage boundary

Completed SDK modes: `happy, preguards, sources`.
Signed production browser journey: **not proven**.
A finalized successful transaction is not by itself a successful business outcome.
Happy matching requires the predeclared FIT/OUT matrix and exclusive assignment;
UNKNOWN is not relabelled as FIT and blocked later steps are not counted as passed.

## Exact transactions and authoritative readback

| Scenario / action | Explorer | Finality / consensus | Verified | Expected error / state |
|---|---|---|---|---|
| preguards / create | [tx](https://explorer-studio.genlayer.com/tx/0x4add67313eb4602e891e832a82b4e0d76e4a6174b9efb07dbf01859174db656a) | FINALIZED / MAJORITY_AGREE | True | OPEN; matrix=[]; assignments=0 |
| preguards / scope | [tx](https://explorer-studio.genlayer.com/tx/0x11171fe7cfe67d3bc67e3f4c0fb637b2821ee28d65f1d335b5c3e5202c06dc9a) | FINALIZED / MAJORITY_AGREE | True | OPEN; matrix=[]; assignments=0 |
| preguards / freeze | [tx](https://explorer-studio.genlayer.com/tx/0x2291d0f6c6942ed7434f242f26e4522ba8c4b30226a51da9d5a4eeb6b7ead643) | FINALIZED / MAJORITY_AGREE | True | FROZEN; matrix=[]; assignments=0 |
| preguards / before_consent | [tx](https://explorer-studio.genlayer.com/tx/0xdeaf6904cfa817a124e8b11ee130a9431464d438a24ed68af491a7dbf003650b) | PENDING / UNKNOWN | False | CONSENT_INCOMPLETE; rollback_equal=False |
| preguards / before_consent_recheck | [tx](https://explorer-studio.genlayer.com/tx/0xbdaa5a8331e766df6d66a5a47c2a29adf3551283cdcee23fa19224ccfba28ba6) | FINALIZED / MAJORITY_AGREE | True | CONSENT_INCOMPLETE; rollback_equal=True |
| preguards / wrong_consent | [tx](https://explorer-studio.genlayer.com/tx/0xe0ec5cdfea944fa92e3c423b6374d1261aeb91c111128a92cb805fb6681e8fa0) | FINALIZED / MAJORITY_AGREE | True | REVIEWER_ONLY; rollback_equal=True |
| preguards / wrong_digest | [tx](https://explorer-studio.genlayer.com/tx/0x8ce3d43a0ec3df6537657e18d3842e60d34424d3c41713713b5180243b434aed) | FINALIZED / MAJORITY_AGREE | True | ROUND_DIGEST_MISMATCH; rollback_equal=True |
| preguards / late_scope | [tx](https://explorer-studio.genlayer.com/tx/0x069e786eae4795155be22d887cb65256bf582d7f07e912ff6c22929be7d6d829) | FINALIZED / MAJORITY_AGREE | True | INTAKE_CLOSED; rollback_equal=True |
| preguards / refreeze | [tx](https://explorer-studio.genlayer.com/tx/0x275c32c3ce6093b2a9452c6905b9141a12015fbb6b3e34389394c5c50be62aee) | FINALIZED / MAJORITY_AGREE | True | ROUND_NOT_OPEN; rollback_equal=True |
| preguards / wrong_cancel_actor | [tx](https://explorer-studio.genlayer.com/tx/0x772534a99549b8d91a394502295b5daadcc9193053ca6dff6b1c3619b66c35da) | FINALIZED / MAJORITY_AGREE | True | OWNER_ONLY; rollback_equal=True |
| preguards / wrong_cancel_digest | [tx](https://explorer-studio.genlayer.com/tx/0xdc2df36669c0fe8b4a7262bd617b942afc4a2077ccbaad330b4fb448ef816128) | FINALIZED / MAJORITY_AGREE | True | ROUND_DIGEST_MISMATCH; rollback_equal=True |
| preguards / cancel | [tx](https://explorer-studio.genlayer.com/tx/0xd074c0fac5d3ebeaa362e117057c6e32d842eef534637f9d658e5fb99de4a574) | FINALIZED / MAJORITY_AGREE | True | CANCELLED; matrix=[]; assignments=0 |
| preguards / late_consent | [tx](https://explorer-studio.genlayer.com/tx/0xbdae86b5279f67d01bfede708ed51cc6b56c8b74ef636f923d16019baa30dbf9) | FINALIZED / MAJORITY_AGREE | True | CONSENT_PHASE_CLOSED; rollback_equal=True |
| preguards / late_allocate | [tx](https://explorer-studio.genlayer.com/tx/0xbd3e9a70aa3f6c2e0ae07dec10369f13ea456a4721f8d65e4a659dac357e000d) | FINALIZED / MAJORITY_AGREE | True | ROUND_NOT_ALLOCATABLE; rollback_equal=True |

Full receipts, declared inputs and before/after snapshots: [preguards](evidence/0x7766cd870e3ed9ea9beb365550a7315d8e6dc462-preguards.json).

| sources / create | [tx](https://explorer-studio.genlayer.com/tx/0xc39a97fc5e6c5f5ecf876de9812e560c5457c8ef1d2139fb977ab457b8d58fa1) | FINALIZED / MAJORITY_AGREE | True | OPEN; matrix=[]; assignments=0 |
| sources / scope | [tx](https://explorer-studio.genlayer.com/tx/0xf28de13aaf60dfec4718ef4220a9d86ab986d548171b2a42351aa72ddb7fe57f) | FINALIZED / MAJORITY_AGREE | True | OPEN; matrix=[]; assignments=0 |
| sources / freeze | [tx](https://explorer-studio.genlayer.com/tx/0xb21803b5d89a6d2fad35e20ea6b77545c04fe5064128125d2864954ac1150942) | FINALIZED / MAJORITY_AGREE | True | FROZEN; matrix=[]; assignments=0 |
| sources / consent | [tx](https://explorer-studio.genlayer.com/tx/0xc0fedcd8855e791963ad732a7e86457507d937cec42cf167af8ebe270860a72b) | FINALIZED / MAJORITY_AGREE | True | FROZEN; matrix=[]; assignments=0 |
| sources / allocate | [tx](https://explorer-studio.genlayer.com/tx/0xd7642d1a5a20963ddd06066f25f6538812a5454dbb0993ecac915c8ede590f37) | FINALIZED / MAJORITY_AGREE | True | UNRESOLVED; matrix=[]; assignments=0 |
| sources / cancel | [tx](https://explorer-studio.genlayer.com/tx/0x6facd9601a48ef0169c9d45e6a0fd9225281fdaf9df71d480ea0b297e6576b3f) | FINALIZED / MAJORITY_AGREE | True | CANCELLED; matrix=[]; assignments=0 |

Full receipts, declared inputs and before/after snapshots: [sources](evidence/0x7766cd870e3ed9ea9beb365550a7315d8e6dc462-sources.json).

| happy / create | [tx](https://explorer-studio.genlayer.com/tx/0x714f6f608a5eec5194f1fa29480d9a071712ada670f67a2206b541a28f712c66) | FINALIZED / MAJORITY_AGREE | True | OPEN; matrix=[]; assignments=0 |
| happy / scope | [tx](https://explorer-studio.genlayer.com/tx/0x701ce323c2aec3dd5b7ca454e4bed3d380be3cbce733c4b48c7ca8f46362f986) | FINALIZED / MAJORITY_AGREE | True | OPEN; matrix=[]; assignments=0 |
| happy / freeze | [tx](https://explorer-studio.genlayer.com/tx/0x95d3b1801d4fea83c1d78cac792465b5b8fd93581e6dd866438896c95273c2fa) | FINALIZED / MAJORITY_AGREE | True | FROZEN; matrix=[]; assignments=0 |
| happy / consent | [tx](https://explorer-studio.genlayer.com/tx/0xd47182bfddbc62ef9a3db1640bb59f371a94875b76691d034d096104037b114c) | FINALIZED / MAJORITY_AGREE | True | FROZEN; matrix=[]; assignments=0 |
| happy / allocate | [tx](https://explorer-studio.genlayer.com/tx/0xffb628350f92037e5a31c8881c629a3f7d555994b4f7ad56d2e8c3a69acbbd75) | FINALIZED / MAJORITY_AGREE | True | UNRESOLVED; matrix=[["UNKNOWN"], ["OUT"]]; assignments=0 |
| happy / allocate_retry | [tx](https://explorer-studio.genlayer.com/tx/0x790e78e6409fe3197687af109db46356eaba50206d6ca63f88f2d4c461ceb90d) | FINALIZED / MAJORITY_AGREE | True | ALLOCATED; matrix=[["FIT"], ["OUT"]]; assignments=1 |
| happy / accept | [tx](https://explorer-studio.genlayer.com/tx/0xef6a10b1e58f99af8bcd8bf1523d54c60e8b909faaf323a7183450829b3d745d) | FINALIZED / MAJORITY_AGREE | True | ALLOCATED; matrix=[["FIT"], ["OUT"]]; assignments=1 |
| happy / submit | [tx](https://explorer-studio.genlayer.com/tx/0x23451d5d9a96b0f97b7259367040991286f9fb0a9d055460db1585a58da707a8) | FINALIZED / MAJORITY_AGREE | True | ALLOCATED; matrix=[["FIT"], ["OUT"]]; assignments=1 |
| happy / close | [tx](https://explorer-studio.genlayer.com/tx/0x26ee84405e3ce850673f18c188f6172fa745cae38db5aad21e03d6253f79b91b) | FINALIZED / MAJORITY_AGREE | True | CLOSED; matrix=[["FIT"], ["OUT"]]; assignments=1 |

Full receipts, declared inputs and before/after snapshots: [happy](evidence/0x7766cd870e3ed9ea9beb365550a7315d8e6dc462-happy.json).

| guards / create | [tx](https://explorer-studio.genlayer.com/tx/0xb16c11ec9d60043b81b19552efe665cb1b25c3ca651f7640684fa9946941a2a7) | FINALIZED / MAJORITY_AGREE | True | OPEN; matrix=[]; assignments=0 |
| guards / scope | [tx](https://explorer-studio.genlayer.com/tx/0x8f28b79c1ee3d85dc2855d90fac1ce4b6ce8de014ba008d730ee140c1ae85238) | FINALIZED / MAJORITY_AGREE | True | OPEN; matrix=[]; assignments=0 |
| guards / freeze | [tx](https://explorer-studio.genlayer.com/tx/0xbdd563dc529776f9eb64f598bb5616cdbcb78162b25b3dbd083b060699b83595) | FINALIZED / MAJORITY_AGREE | True | FROZEN; matrix=[]; assignments=0 |
| guards / before_consent | [tx](https://explorer-studio.genlayer.com/tx/0xaba33828f099dd39b631ce053c81f1cadb1939f9989d2d5d091a4b42f459c062) | FINALIZED / MAJORITY_AGREE | True | CONSENT_INCOMPLETE; rollback_equal=True |
| guards / wrong_consent | [tx](https://explorer-studio.genlayer.com/tx/0x033bf817534c32d2cd63cb3eea0791aa0b051deacb765ac1af4b7a24c5dc86bf) | FINALIZED / MAJORITY_AGREE | True | REVIEWER_ONLY; rollback_equal=True |
| guards / wrong_digest | [tx](https://explorer-studio.genlayer.com/tx/0xf2e88220d91740d0965ed5929875cf6b151f4fda6d28d9a30cfe4d7568bd88dd) | FINALIZED / MAJORITY_AGREE | True | ROUND_DIGEST_MISMATCH; rollback_equal=True |
| guards / consent | [tx](https://explorer-studio.genlayer.com/tx/0x5345175b96a4154c2dc2ce62e78bf0e839ce5aa0db0d584a85858b4bac6c3bbe) | FINALIZED / MAJORITY_AGREE | True | FROZEN; matrix=[]; assignments=0 |
| guards / allocate | [tx](https://explorer-studio.genlayer.com/tx/0x475024318616491bb769a42ca74fe881bab5956183d111c10a0967459b6c309f) | FINALIZED / MAJORITY_AGREE | True | UNRESOLVED; matrix=[["UNKNOWN"], ["OUT"]]; assignments=0 |
| guards / allocate_retry | [tx](https://explorer-studio.genlayer.com/tx/0x68b2b5b1dd247a92cc57f6c8b845082dd4d2e4d6072b92ccea3696578a86628e) | FINALIZED / MAJORITY_AGREE | True | UNRESOLVED; matrix=[["UNKNOWN"], ["OUT"]]; assignments=0 |

Full receipts, declared inputs and before/after snapshots: [guards](evidence/0x7766cd870e3ed9ea9beb365550a7315d8e6dc462-guards.json).


Suite stopped at: `guards`. Later coverage is not established.
