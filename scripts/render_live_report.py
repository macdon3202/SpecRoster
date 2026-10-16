"""Render current exact-address checkpoints with explicit incomplete coverage."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ADDRESS="0x07B305921D3c315EBb6708e4F51797a57485bf90"
source=json.loads((ROOT/"docs"/"evidence"/"deployed-source.json").read_text())
run=json.loads((ROOT/"docs"/"evidence"/(ADDRESS.lower()+"-happy.json")).read_text())
lines=["# SpecRoster StudioNet verification", "", "Contract: ["+ADDRESS+"](https://explorer-studio.genlayer.com/address/"+ADDRESS+")", "", "## Source parity", "", "RPC-fetched source matches local bytes: `"+str(source["exact_bytes_match"])+"`.", "SHA-256: `"+source["deployed_sha256"]+"`.", "", "## Actors", "", "Creator: `"+run["wallet_a"]+"`.", "Reviewer: `"+run["wallet_b"]+"`.", "Main wallet used in lifecycle: `false`.", "", "## Transactions", "", "| Action | Explorer | Observed result |", "|---|---|---|"]
for label,item in run["writes"].items():
    result=item.get("status","PENDING")+" / "+item.get("consensus","UNKNOWN")
    if item.get("after"):
        r=item["after"]["rounds"][0]
        result+=" / "+r["state"]
        if label.startswith("allocate"):result+=" / "+json.dumps(r["matrix"])
    lines.append("| "+label+" | [Transaction]("+item["explorer"]+") | "+result+" |")
recovery_path=ROOT/"docs"/"evidence"/"unresolved-recovery.json"
if recovery_path.exists():
    recovery=json.loads(recovery_path.read_text())
    for label,item in recovery["writes"].items():
        result="PENDING"
        if item.get("verified"):
            result="ATTEMPTS_EXHAUSTED; complete state unchanged" if label=="exhausted" else "CANCELLED; no assignments"
        if item.get("url"):lines.append("| "+label+" | [Transaction]("+item["url"]+") | "+result+" |")
lines += ["", "## Coverage boundary", "", "Both initial assessment and bounded retry produced `UNKNOWN / OUT`, so the", "contract created zero assignments. The expected FIT/OUT matrix was specified", "before execution and was not rewritten. This run does not establish a complete", "happy lifecycle, reviewer acceptance/submission, or signed production browser E2E.", "The current matrix does not expose why the FIT candidate became UNKNOWN; the", "root cause cannot be inferred solely from its returned status.", "", "Full checkpointed receipts and authoritative before/after snapshots: [happy run](evidence/"+ADDRESS.lower()+"-happy.json), [recovery](evidence/unresolved-recovery.json)."]
lines += ["", "## Additional V1 source/authorization runs", "", "These are separate from the incomplete happy journey. A transaction is not", "marked verified until finality, leader execution and readbacks have been checked.", "", "| Scenario/action | Explorer | Verified | Rollback equal |", "|---|---|---|---|"]
for mode in ("sources","preguards"):
    path=ROOT/"docs"/"evidence"/(ADDRESS.lower()+"-"+mode+".json")
    if not path.exists():continue
    extra=json.loads(path.read_text())
    for label,item in extra["writes"].items():
        if item.get("explorer"):
            lines.append("| "+mode+" / "+label+" | [Transaction]("+item["explorer"]+") | "+str(item.get("verified",False))+" | "+str(item.get("rollback_equal","n/a"))+" |")
    lines += ["", "Full checkpoints: ["+mode+"](evidence/"+path.name+").", ""]
report="\n".join(lines)+"\n"
report=report.replace("RPC-fetched source matches local bytes:","Historical RPC-fetched V1 source matches archived V1 bytes:")
report += "\nCurrent contracts/spec_roster.py is an undeployed V2 candidate; the V1 parity proof applies only to contracts/archive/spec_roster_v1.py.\n"
(ROOT/"docs"/"STUDIONET_E2E.md").write_text(report,encoding="utf-8")
