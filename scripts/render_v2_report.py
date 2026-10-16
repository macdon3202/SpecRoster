"""Render only observed checkpoint evidence for an exact V2 deployment."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument("address");parser.add_argument("--version",choices=["V2","V3"],default="V2");args=parser.parse_args()
prefix=args.address.lower()
proof_path=ROOT/"docs"/"evidence"/(prefix+"-"+args.version.lower()+"-suite.json")
proof=json.loads(proof_path.read_text())
lines=["# SpecRoster V2 StudioNet E2E", "", "Contract: ["+args.address+"](https://explorer-studio.genlayer.com/address/"+args.address+")", "", "Source SHA-256: `"+proof["source_sha256"]+"`.", "Exact deployed source match: `"+str(proof["exact_bytes_match"])+"`.", "Main wallet used for lifecycle: `false`.", "", "## Coverage boundary", "", "Completed SDK modes: `"+", ".join(proof["completed_modes"])+"`.", "Signed production browser journey: **not proven**.", "A finalized successful transaction is not by itself a successful business outcome.", "Happy matching requires the predeclared FIT/OUT matrix and exclusive assignment;", "UNKNOWN is not relabelled as FIT and blocked later steps are not counted as passed.", "", "## Exact transactions and authoritative readback", "", "| Scenario / action | Explorer | Finality / consensus | Verified | Expected error / state |", "|---|---|---|---|---|"]
for mode in ("preguards","sources","happy","guards","cancel"):
    path=ROOT/"docs"/"evidence"/(prefix+"-"+mode+".json")
    if not path.exists():continue
    run=json.loads(path.read_text())
    created=run.get("writes",{}).get("create",{})
    try:rid=int(created["leader"]["result"]["payload"]["readable"].strip('"'))
    except (KeyError,ValueError,AttributeError):rid=None
    for label,item in run["writes"].items():
        if not item.get("explorer"):continue
        detail=item.get("expected_error")
        if detail:detail+="; rollback_equal="+str(item.get("rollback_equal",False))
        elif rid and item.get("after"):
            r=next((r for r in item["after"]["rounds"] if r["id"]==rid),None)
            detail=(r["state"]+"; matrix="+json.dumps(r["matrix"])+"; assignments="+str(len(r["allocation"]))) if r else "missing readback"
        else:detail="pending"
        lines.append("| "+mode+" / "+label+" | [tx]("+item["explorer"]+") | "+item.get("status","PENDING")+" / "+item.get("consensus","UNKNOWN")+" | "+str(item.get("verified",False))+" | "+detail+" |")
    lines += ["", "Full receipts, declared inputs and before/after snapshots: ["+mode+"](evidence/"+path.name+").", ""]
if proof.get("failed_mode"):lines += ["", "Suite stopped at: `"+proof["failed_mode"]+"`. Later coverage is not established."]
report="\n".join(lines)+"\n"
report=report.replace("# SpecRoster V2 StudioNet E2E","# SpecRoster "+args.version+" StudioNet E2E")
(ROOT/"docs"/("STUDIONET_"+args.version+"_E2E.md")).write_text(report,encoding="utf-8")
