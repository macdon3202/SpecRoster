"""One exact-address V2 suite. Stops on any failure; never deploys or loads main key."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from genlayer_py import create_client
from genlayer_py.chains import studionet
from studionet_e2e import load_aux

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("address")
parser.add_argument("--version",choices=["SPEC_ROSTER_V2","SPEC_ROSTER_V3","SPEC_ROSTER_V4_CANDIDATE"],default="SPEC_ROSTER_V2")
args=parser.parse_args()
aux_a,_=load_aux()
client=create_client(chain=studionet,account=aux_a,endpoint="https://studio.genlayer.com/api")
response=client.provider.make_request("gen_getContractCode",[args.address])
if isinstance(response,dict):
    assert not response.get("error"),response.get("error")
    response=response["result"]
code=base64.b64decode(response,validate=True)
local=(ROOT/"contracts"/"spec_roster.py").read_bytes()
assert code==local,"DEPLOYED_SOURCE_MISMATCH: do not run against historical V1"
config=client.read_contract(address=args.address,function_name="get_config",args=[])
assert config["version"]==args.version and config["deployer_authority"]=="NONE"
path=ROOT/"docs"/"evidence"/(args.address.lower()+"-"+args.version.lower().replace("spec_roster_","")+"-suite.json")
proof=json.loads(path.read_text()) if path.exists() else {"address":args.address,"version":args.version,"source_sha256":hashlib.sha256(code).hexdigest(),"exact_bytes_match":True,"main_wallet_used":False,"completed_modes":[],"signed_browser_e2e":False}
assert proof["source_sha256"]==hashlib.sha256(code).hexdigest()
path.parent.mkdir(parents=True,exist_ok=True)
def save():path.write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
save()
failed_modes=[]
if "semantic" in proof["completed_modes"]:
    print("SKIP_COMPLETED semantic",flush=True)
else:
    print("LIVE_MODE semantic",flush=True)
    semantic=subprocess.run([sys.executable,str(ROOT/"scripts"/"studionet_semantic_gate.py"),args.address],cwd=ROOT)
    if semantic.returncode:
        failed_modes.append("semantic")
    else:
        proof["completed_modes"].append("semantic")
    save()
for mode in ("preguards","sources","happy","guards","cancel"):
    if mode in proof["completed_modes"]:
        print("SKIP_COMPLETED",mode,flush=True)
        continue
    print("LIVE_MODE",mode,flush=True)
    result=subprocess.run([sys.executable,str(ROOT/"scripts"/"studionet_e2e.py"),args.address,mode],cwd=ROOT)
    if result.returncode:
        failed_modes.append(mode)
        proof["failed_modes"]=failed_modes;save()
        continue # retain failure, but do not suppress independent security tests
    if mode not in proof["completed_modes"]:proof["completed_modes"].append(mode)
    proof.pop("failed_mode",None);save()
proof["failed_modes"]=failed_modes
save()
if failed_modes:
    print("SDK_LIVE_SUITE_FAIL",failed_modes,flush=True);raise SystemExit(1)
proof.pop("failed_modes",None);save()
print("SDK_LIVE_SUITE_PASS — signed browser journey remains a separate gate",flush=True)
