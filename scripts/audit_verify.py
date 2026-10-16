"""Auditable local gate; never promotes mock tests into semantic/live proof."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")

ROOT=Path(__file__).resolve().parents[1]
proof={"kind":"COMPREHENSIVE_LOCAL_AUDIT","source_sha256":hashlib.sha256((ROOT/"contracts"/"spec_roster.py").read_bytes()).hexdigest(),"checks":[],"ready_for_submission":False,"live_verified":False}
path=ROOT/"docs"/"evidence"/"local-audit.json"
def save():path.write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
env=dict(os.environ,PYTHONUTF8="1")
for command,cwd in [
    ([sys.executable,"-m","pytest","tests","-q","--tb=short","-p","no:cacheprovider"],ROOT),
    ([sys.executable,"-m","genvm_linter.cli","check","contracts/spec_roster.py"],ROOT),
    (["npm.cmd","run","verify"],ROOT/"frontend"),
]:
    print("RUN",command,flush=True)
    result=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,encoding="utf-8",errors="replace")
    proof["checks"].append({"command":command,"returncode":result.returncode,"stdout":result.stdout,"stderr":result.stderr});save()
    print(result.stdout,flush=True)
    if result.returncode:
        proof["status"]="LOCAL_FAIL";save();raise SystemExit(result.returncode)
proof["paid_api_preflight_required"]=False
deployment=ROOT/"deployments"/"v4-candidate.json"
live=json.loads(deployment.read_text()) if deployment.exists() else {}
proof["live_verified"]=bool(live.get("live_verified"))
if proof["live_verified"] and live.get("source_sha256")==proof["source_sha256"]:
    proof["status"]="LIVE_PASS_BROWSER_PENDING"
    proof["release_blockers"]=["Signed browser-wallet journey and rendered UI reconciliation remain to be proven on the production build."]
else:
    proof["status"]="LOCAL_PASS_DEPLOYMENT_CANDIDATE"
    proof["release_blockers"]=["After one exact-source deployment, the fixed eight-case StudioNet semantic gate must pass.","Full same-address StudioNet security/lifecycle suite and browser-wallet journey are not proven for this candidate."]
save();print(proof["status"],flush=True)
