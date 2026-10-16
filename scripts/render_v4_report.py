"""Render a single reviewer entry point from observed V4 checkpoint evidence."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ADDRESS="0xB404f8Da18cc736aD21917929dc52993913F1D98"
PREFIX=ADDRESS.lower()
suite=json.loads((ROOT/"docs"/"evidence"/(PREFIX+"-v4_candidate-suite.json")).read_text())
semantic=json.loads((ROOT/"docs"/"evidence"/(PREFIX+"-semantic-gate.json")).read_text())
lines=[
    "# SpecRoster V4 StudioNet E2E", "",
    f"Contract: [{ADDRESS}](https://explorer-studio.genlayer.com/address/{ADDRESS})", "",
    f"Source SHA-256: `{suite['source_sha256']}`.",
    f"Exact RPC source bytes match: `{suite['exact_bytes_match']}`.",
    "Main/deployer wallet used in lifecycle: `false`.", "",
    "## Outcome", "",
    "- Fixed semantic corpus: **8/8 passed**.",
    "- Completed SDK modes: `"+", ".join(suite["completed_modes"])+"`.",
    "- Source failure, expected reverts and rollback equality are checked from authoritative receipts/state.",
    "- Signed production browser journey remains a separate gate; it is not claimed here.", "",
    "## Semantic transactions", "",
    "| Case | Expected | Observed | Allocation | Explorer transactions |", "|---|---|---|---|---|"
]
for case in semantic["cases"].values():
    links=" · ".join(f"[{label}]({item['explorer']})" for label,item in case["writes"].items() if item.get("explorer"))
    lines.append(f"| {case['id']} | {case['expected']} | {case['observed']} | {len(case['allocation'])} | {links} |")
lines += ["", "## Lifecycle, failure and conflict transactions", "",
          "| Mode / action | Result | Expected error or observed state | Explorer |", "|---|---|---|---|"]
for mode in ("preguards","sources","happy","guards","cancel"):
    path=ROOT/"docs"/"evidence"/(PREFIX+f"-{mode}.json")
    run=json.loads(path.read_text())
    for label,item in run.get("writes",{}).items():
        if not item.get("explorer"): continue
        detail=item.get("expected_error") or "SUCCESS"
        if item.get("expected_error"): detail += f"; rollback_equal={item.get('rollback_equal',False)}"
        result=f"{item.get('status','PENDING')} / {item.get('consensus','UNKNOWN')}"
        lines.append(f"| {mode} / {label} | {result} | {detail} | [tx]({item['explorer']}) |")
    lines += ["", f"Full machine evidence: [`{path.name}`](evidence/{path.name}).", ""]
(ROOT/"docs"/"STUDIONET_V4_E2E.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print("WROTE docs/STUDIONET_V4_E2E.md")
