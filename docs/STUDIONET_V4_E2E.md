# SpecRoster V4 StudioNet E2E

Contract: [0xB404f8Da18cc736aD21917929dc52993913F1D98](https://explorer-studio.genlayer.com/address/0xB404f8Da18cc736aD21917929dc52993913F1D98)

Source SHA-256: `a2b9d42a8e42ac746008b2d327413eeb71b0a8184249ff9d07c09faedcbac46a`.
Exact RPC source bytes match: `True`.
Main/deployer wallet used in lifecycle: `false`.

## Outcome

- Fixed semantic corpus: **8/8 passed**.
- Completed SDK modes: `semantic, preguards, sources, happy, guards, cancel`.
- Source failure, expected reverts and rollback equality are checked from authoritative receipts/state.
- Signed production browser journey remains a separate gate; it is not claimed here.

## Semantic transactions

| Case | Expected | Observed | Allocation | Explorer transactions |
|---|---|---|---|---|
| typed-domain-in-scope | FIT | FIT | 1 | [create](https://explorer-studio.genlayer.com/tx/0x35ce698b7d58d42e21f8e324473cdab3fdcef1f1e69425aae12b75bce63dc7b8) · [scope](https://explorer-studio.genlayer.com/tx/0x2692981245c99fb73c93c8d48b76db731f50ecee665a3a4eb840b6bed8d47907) · [freeze](https://explorer-studio.genlayer.com/tx/0x23f927aa822eb08cb620b9f8f8161e2514b87f05ff8a97b35f868446fbfb3efa) · [consent](https://explorer-studio.genlayer.com/tx/0x41adfb19c227daef730517d46a7255c3939861a755dbb8822be53614e1251270) · [allocate](https://explorer-studio.genlayer.com/tx/0x2dd7371d8939597e96cf82634b1d9b04091701750458857e975ab3da2bb7c116) |
| fee-market-excluded | OUT | OUT | 0 | [create](https://explorer-studio.genlayer.com/tx/0x4d60760e162cc2d8c985f6f3e89b43427d5a99c4337e3431dc88c06cff3d5833) · [scope](https://explorer-studio.genlayer.com/tx/0xb24321b3b3650855ca91eb77cd53dfdb49f4ac496e05feb38fab7653544b9fa3) · [freeze](https://explorer-studio.genlayer.com/tx/0xc186207045bf3997790e2105c1a67fd7600434c056aa8d8978b21a7ec324f8d9) · [consent](https://explorer-studio.genlayer.com/tx/0x0c1b1306dc1f4037a1a61ff4bc3a19dea3861bf5bf75d3880ce461c58ad00299) · [allocate](https://explorer-studio.genlayer.com/tx/0x6849ba90d1735559a9f11f7e7bdafb906b3798358377e2e6fc3610963207b78c) |
| fee-market-in-scope | FIT | FIT | 1 | [create](https://explorer-studio.genlayer.com/tx/0x594544820e7661cf53414fe15774d485eae5d2e77cf9fdc58bff135c8a280316) · [scope](https://explorer-studio.genlayer.com/tx/0xc23d314e45b54c8fbcda1bc9d93941a61f6678f4af35e04fb43620ef9a33791e) · [freeze](https://explorer-studio.genlayer.com/tx/0xa223e7d11b0af711da78e2cad3d63c057f58f3aef088ce0c8b60bfcea2b2af02) · [consent](https://explorer-studio.genlayer.com/tx/0x5d199a1c4cd7fd27f89c40a47f06404a271ff4b6608033725b528b6a444fc084) · [allocate](https://explorer-studio.genlayer.com/tx/0x4e804ba96a64b497f6f5ed24a63d24c1219b095fba5bd6a14095f473d13f2c04) |
| signature-explicitly-excluded | OUT | OUT | 0 | [create](https://explorer-studio.genlayer.com/tx/0x98848a329d82ad3d34af09b05a11f98dc6880952c7e52b72140de8d4699dd2a1) · [scope](https://explorer-studio.genlayer.com/tx/0x66b29e9755c1a7923a7054cb1a9366bbe4ed8a8767bf531582bb0c70f350325a) · [freeze](https://explorer-studio.genlayer.com/tx/0xe09259ce4062ff27e60af8d4f088298bfe5d139368710137ab8eff10190a0b92) · [consent](https://explorer-studio.genlayer.com/tx/0x0358292a7c9214ae14d435bff157b1ab30bd96d5214a87a17891a2d2641bd647) · [allocate](https://explorer-studio.genlayer.com/tx/0xcc5822d6caf02561851808b557efb392d1911d6c42f76d994568fdda3775050f) |
| unrelated-capability-not-required | FIT | FIT | 1 | [create](https://explorer-studio.genlayer.com/tx/0x78b0b313ff6dff1518c877ff83127b8044537775c91052a5265810cf5343e4e1) · [scope](https://explorer-studio.genlayer.com/tx/0x8dbd2c0685cb337f117a84405bdcb8ecd14fa66dbca62dee6f0cbc8581c8241f) · [freeze](https://explorer-studio.genlayer.com/tx/0xcf4184604a3e7da9b817a74c48b989348adf08ce6f348f47acd233010e393748) · [consent](https://explorer-studio.genlayer.com/tx/0x540a93aa7876fd30c16c1ebfaf23c907ad75750c2fa6b5e1da589a54af00700e) · [allocate](https://explorer-studio.genlayer.com/tx/0x68b34ddfbb0846febd9bb21defa30adf721779f3c013eb20012cf939bb443362) |
| unsupported-feature | OUT | OUT | 0 | [create](https://explorer-studio.genlayer.com/tx/0xb21bcd52af93f244acf27d311a73088d4362c341d5aac717ae74dd44282cf375) · [scope](https://explorer-studio.genlayer.com/tx/0xc25ee21afaa0b92b7008884bdef528decf4e40fa2a8b90355678809eaea66dfb) · [freeze](https://explorer-studio.genlayer.com/tx/0x9f2448f4a6d00bbbf02860cdefe7e49f89c04521ec64aae9fa5b0f4d644200b9) · [consent](https://explorer-studio.genlayer.com/tx/0xaf6bf500a9af2fe4bbe832ca1d9425955aa4c7bfd45d01615b1e5ac52c568231) · [allocate](https://explorer-studio.genlayer.com/tx/0xa2f9c28a99d21f9f662e86b6d14ca54954ad940875ca513637f14b43c333cc7d) |
| explicit-scope-contradiction | UNKNOWN | UNKNOWN | 0 | [create](https://explorer-studio.genlayer.com/tx/0x9974493758f031967090de968cc8af945408a8355020f4cfc12e86fb25783c57) · [scope](https://explorer-studio.genlayer.com/tx/0x7ae0941c5b39f1310b924f8aaeae282491296dafb74185049f73f68337457f21) · [freeze](https://explorer-studio.genlayer.com/tx/0xae73e878334ff3813fa26bf70395f480782fa1d98e45a40a3cf6d48d5f36775e) · [consent](https://explorer-studio.genlayer.com/tx/0x4a64e244ca73c547c8403fd776afa7508a09fdb318d6d4c9ef852dcb562c7fed) · [allocate](https://explorer-studio.genlayer.com/tx/0x12174e6cf4f063557503799b2c1138f121b043573d73855ee855fd7f1b0c32a0) |
| injection-not-authority | OUT | OUT | 0 | [create](https://explorer-studio.genlayer.com/tx/0x1ad7ea22a1df5d613d84c73af742f791cac939ddf11de8e6597f4f169bf623b8) · [scope](https://explorer-studio.genlayer.com/tx/0x2daf62779214c354a3e5ce835703480e4e8e4e06bb61a3995766b77264ba5686) · [freeze](https://explorer-studio.genlayer.com/tx/0xb77787cc56a4ffbacd3f821ab7b99eebb99a4368a841161c15630248d90f06be) · [consent](https://explorer-studio.genlayer.com/tx/0x1cc84a43a9dc761e7df2f4fa4d3974a61b401cc0e30dc157266b62e21132c647) · [allocate](https://explorer-studio.genlayer.com/tx/0x5ddb510c1c840492bfc47e449932b693d9e4fc8e169a86e7da885b4e0f248659) |

## Lifecycle, failure and conflict transactions

| Mode / action | Result | Expected error or observed state | Explorer |
|---|---|---|---|
| preguards / create | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xba1fd4c405b4e8ed3ab13cecdca079b3f214f615eaf6b40cf18b3277a3c70a72) |
| preguards / scope | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x7e3433f908f1ad21bc42976ccb4745870f6cbb2123fe56bb4b8572e0cb29945b) |
| preguards / freeze | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xd1446f77c61b1a9140baaf41ee94d1352efb6b1c6a2f55d19515fdf94688f251) |
| preguards / before_consent | FINALIZED / MAJORITY_AGREE | CONSENT_INCOMPLETE; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0x5d790350217fd4a1891a180a2a3c0813327e4ea801a1c61b7264013fcdd7fe9d) |
| preguards / wrong_consent | FINALIZED / MAJORITY_AGREE | REVIEWER_ONLY; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0x8b1f1bd2601039848b388f082577aa336c1378ef1b207df54c5ae22fdf88a597) |
| preguards / wrong_digest | FINALIZED / MAJORITY_AGREE | ROUND_DIGEST_MISMATCH; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xd338185f5e392ebe65df0285e85dab4900716a61196416e29b17afcf65d650fb) |
| preguards / late_scope | FINALIZED / MAJORITY_AGREE | INTAKE_CLOSED; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0x3cb8d963fbcf993a2a647616b701fc18d8bc2252c382d8c29ea597f63109e36d) |
| preguards / refreeze | FINALIZED / MAJORITY_AGREE | ROUND_NOT_OPEN; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xe5ca04a4278f4f0da405fd39429bc2a56e578b064db611f73bce0d03c701f30f) |
| preguards / wrong_cancel_actor | FINALIZED / MAJORITY_AGREE | OWNER_ONLY; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xa71d39ce8c7152eb240b25460e962c46fc26e6411430efff103f25420536a9cb) |
| preguards / wrong_cancel_digest | FINALIZED / MAJORITY_AGREE | ROUND_DIGEST_MISMATCH; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xe74e589352366656f3c9a778986e5f76e2dceedc507cfd5bdeae341d0c33f4ef) |
| preguards / cancel | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x27e28b9b8617c3828fba9ad02880e53afa26b1e3335fd5cced1833c3cea47264) |
| preguards / late_consent | FINALIZED / MAJORITY_AGREE | CONSENT_PHASE_CLOSED; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xb7d8d3f59629ce9e78fbaf88461bc6169bb0b8106abfedc16e8a33af4fbd872d) |
| preguards / late_allocate | FINALIZED / MAJORITY_AGREE | ROUND_NOT_ALLOCATABLE; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xbffcd5ddd710d1474107e884514ac31b66a4794fddfc48d1ee3bc787faa26b8e) |

Full machine evidence: [`0xb404f8da18cc736ad21917929dc52993913f1d98-preguards.json`](evidence/0xb404f8da18cc736ad21917929dc52993913f1d98-preguards.json).

| sources / create | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xbae551fba4063d9011f7a7214e9b4992a5af9a93f3be60964d6fe9688d6f5488) |
| sources / scope | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x1682a8e356f1e6e7186fcf90fb033cf861281170c932e4d54231e9cff0bc94b0) |
| sources / freeze | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x7eaf4299c936f1fead9fbc709275e5b410269a75a70c2db68313888baaa05222) |
| sources / consent | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xd24648d86d0e1af3cc7907a4534c01f06aa762c8b20ce115de4ac42e30e4c764) |
| sources / allocate | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x1d30a39089aac6c5b942a501ef0b99d9ff2dd0f9a392cb911dc895e97a88b3d2) |
| sources / cancel | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x3b4cce8cdb4cdec4a0ee54ba37655faf9c9353abcf8572f7e69dc58da9de3eb0) |

Full machine evidence: [`0xb404f8da18cc736ad21917929dc52993913f1d98-sources.json`](evidence/0xb404f8da18cc736ad21917929dc52993913f1d98-sources.json).

| happy / create | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x8eaeb41c737a992ac04e62deb2554ab687d2c17119617736cf3e8a47761bf43a) |
| happy / scope | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xc160e6204e5827de5f20456473a95447793080bc02698643c658ce75314d5204) |
| happy / freeze | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xd9e071864ba6121ab6c426e04cd18c28752e9738258345ad28f9e4108e392ad8) |
| happy / consent | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xe7e54ae1e6b51de7997e20d5468d05c81f2c4db906c0c1f2a7eae0093e5099bc) |
| happy / allocate | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x5fc0cb705dd0553aee9df59339ba86aea24a9d224cc7fa19635f9f4e87ea3c3e) |
| happy / accept | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xe8bb96b7bf6a514245dc8ca4be9b5ebdc0c078fd469e6505e039bcdbf6c91ee9) |
| happy / submit | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x6693a91937ea64fb6e74c20a47c49aed4f44f74c66405868224c6ebc5e86345c) |
| happy / close | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x55b753722786da90716bf3a53b7ef4f5cc1f48d9c8aea10acdcc4259586c2a66) |

Full machine evidence: [`0xb404f8da18cc736ad21917929dc52993913f1d98-happy.json`](evidence/0xb404f8da18cc736ad21917929dc52993913f1d98-happy.json).

| guards / create | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x0eba4cba6fe1a2830a6c77f9fb8a2d008d87dd5c7b2785693faf4f3bc4cdb118) |
| guards / scope | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xe34c80586fd8cbe43832e2e6804262c04ab869bf753e0fce845e7fd1efe9002d) |
| guards / freeze | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xd0a991b240ca698f1322733998f2ea8b391c3929b569506401c4eb464d8549f4) |
| guards / before_consent | FINALIZED / MAJORITY_AGREE | CONSENT_INCOMPLETE; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0x6b91947ed0866e0951e1b12260a7bf208a9214f02ebdab4032e1d5aefd28d15a) |
| guards / wrong_consent | FINALIZED / MAJORITY_AGREE | REVIEWER_ONLY; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xe5ef96b68fe7d639e668596758654cbffb99388a543023cd2b273345281e670f) |
| guards / wrong_digest | FINALIZED / MAJORITY_AGREE | ROUND_DIGEST_MISMATCH; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xbfa241a688fa28f50309837dbd1d9a3fd1f2a26b8685cda472f59dfa9b01f5fe) |
| guards / consent | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xcd6bba94555c45802e54660315f64300fbe3cb8c49d353d2c78d969a3fb2f76b) |
| guards / allocate | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x5930587fd00431900f5cf246bb4bea44111f74b93088044b6d3f740055302813) |
| guards / replay_allocate | FINALIZED / MAJORITY_AGREE | ROUND_NOT_ALLOCATABLE; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xd3e6af525843b7b3d8c10fae471e2006f3ce549a9f4d3fd1889179b9ec80e58e) |
| guards / wrong_assignee | FINALIZED / MAJORITY_AGREE | ASSIGNEE_ONLY; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0x8b4f9b3ba5824e180f9f2db1251f5342cffd068110609d3d30efed5700221a3c) |
| guards / early_submit | FINALIZED / MAJORITY_AGREE | ACCEPT_FIRST; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0x4c31b86acd403cd6715c84fa33c61cb201d1fcdb9ffee9e29e08de9e9e86c638) |
| guards / accept | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x159b934f68dad5d0b376c9fb00ffdc87f45e7df289ef753d39d8c06e9a7de89d) |
| guards / submit | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x1fb54ec487f8c948a08dadca341f782a7bc1b70a008451ecc123996b44d5d98e) |
| guards / close | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xa8425b0f30371cef64497094db6291b713a802cd55fdebac5f0ef0c48a9b657f) |
| guards / terminal_submit | FINALIZED / MAJORITY_AGREE | STALE_ASSIGNMENT; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xa5d043515a4274c568940e5778319e695ea699cc9753567482a9a49debf30aad) |

Full machine evidence: [`0xb404f8da18cc736ad21917929dc52993913f1d98-guards.json`](evidence/0xb404f8da18cc736ad21917929dc52993913f1d98-guards.json).

| cancel / create | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xeb92c8bcf3b1b39712520256e870ca97524acb3cdd64a542f1c5d233315e2e89) |
| cancel / scope | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x457471262f85e9e6735e62ffeb7665451bc9b18770e45fb66814472df8917ea5) |
| cancel / freeze | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x3de00caa3154b1f7addbc15dde09904ae9afabb124fff5f2f2e71c8fd5782738) |
| cancel / consent | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xcd548c13209dcce5faf0824e39361b4ad3bb944df0c6a30f19e6dbf36d0de2e4) |
| cancel / allocate | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xe112e7b3a5c4913a85e41c82fe9ecc246eecd6f53590922a2cb2a42a8e97dea4) |
| cancel / accept | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0x6efb58fd227f1659591e3601a991e95130a893022f63d5182794bf45cf47fddf) |
| cancel / cancel | FINALIZED / MAJORITY_AGREE | SUCCESS | [tx](https://explorer-studio.genlayer.com/tx/0xfa8194ab948f9c25cbd888e152b661b91a7d90bb628108660f8cb104a309cf56) |
| cancel / late_submit | FINALIZED / MAJORITY_AGREE | STALE_ASSIGNMENT; rollback_equal=True | [tx](https://explorer-studio.genlayer.com/tx/0xc3a9b6ff808d7b146fe19c97ee7157ae2431e1aea74dd96c70003a3e7bd02771) |

Full machine evidence: [`0xb404f8da18cc736ad21917929dc52993913f1d98-cancel.json`](evidence/0xb404f8da18cc736ad21917929dc52993913f1d98-cancel.json).

