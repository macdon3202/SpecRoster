"""Opt-in real web/LLM preflight of actual contract entrypoints, NOT StudioNet.

Requires two explicit provider:model configurations and their environment keys.
Never reads project wallet secrets or deploys a network contract. Calls paid APIs
only with --allow-paid-api. No mocks, no fixture-output injection, no auto retry.
Uses pinned gltest/glsim live handlers, whose simulator limits remain explicit.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import sys

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument("--provider",action="append",default=[])
parser.add_argument("--repeats",type=int,default=3)
parser.add_argument("--allow-paid-api",action="store_true")
args=parser.parse_args()
path=ROOT/"docs"/"evidence"/"semantic-preflight.json"
packet=ROOT/"samples"/"semantic-preflight.json"
proof={"kind":"UNMOCKED_DIRECT_MODE_PREFLIGHT","studionet":False,"signed_browser_e2e":False,"source_sha256":hashlib.sha256((ROOT/"contracts"/"spec_roster.py").read_bytes()).hexdigest(),"corpus_sha256":hashlib.sha256(packet.read_bytes()).hexdigest(),"status":"BLOCKED","results":[]}
def save():path.write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
def block(reason):proof["reason"]=reason;save();print(reason);raise SystemExit(2)
if not args.allow_paid_api:block("Explicit paid-API authorization not supplied; no model call made.")
if len(set(args.provider))<2:block("Require at least two distinct explicit provider:model configurations.")
if not 1<=args.repeats<=5:block("Repeats must be between 1 and 5.")
for config in args.provider:
    provider,sep,model=config.partition(":")
    key={"openai":"OPENAI_API_KEY","anthropic":"ANTHROPIC_API_KEY"}.get(provider)
    if not sep or not model or not key or not os.environ.get(key):block("Supported provider configuration or required environment credential missing.")
from gltest.direct import VMContext,deploy_contract
from glsim.live_io import create_web_handler,create_llm_handler
runpy.run_path(str(ROOT/"tests"/"conftest.py")) # same Windows pinned-SDK compatibility fix
sample=json.loads((ROOT/"samples"/"public-round.json").read_text())
cases=json.loads(packet.read_text())["cases"]
for config in args.provider:
    for case in cases:
        for repetition in range(args.repeats):
            vm=VMContext();vm._live_web_handler=create_web_handler(use_browser=False)
            live_llm=create_llm_handler(config)
            io_errors=[]
            def llm(data):
                response=live_llm(data)
                value=response.get("ok")
                if isinstance(value,str) and (value.startswith("live_io LLM error:") or value.startswith("Unsupported LLM provider:")):
                    io_errors.append("PROVIDER_CALL_FAILED")
                if isinstance(value,str):
                    try:response={"ok":json.loads(value)}
                    except ValueError:pass
                return response
            vm._live_llm_handler=llm
            row={"case":case["id"],"provider":config,"repeat":repetition,"expected":case["expected"]}
            try:
                with vm.activate():
                    c=deploy_contract(ROOT/"contracts"/"spec_roster.py",vm,sdk_version="v0.2.16")
                    task=dict(sample["tasks"][case["task_index"]],requirement=case["requirement"])
                    with vm.prank(bytes.fromhex("11"*20)):rid=c.create_round(case["id"],json.dumps([task]),json.dumps(["0x"+"22"*20]))
                    with vm.prank(bytes.fromhex("22"*20)):c.register_scope(rid,case["scope"],1)
                    with vm.prank(bytes.fromhex("11"*20)):digest=c.freeze_round(rid)
                    with vm.prank(bytes.fromhex("22"*20)):c.consent_round(rid,digest)
                    c.allocate_round(rid,digest)
                    state=c.get_round(rid);row["state"]=state
                    row["independent_validator_agreed"]=vm.run_validator()
                    row["provider_io_errors"]=io_errors[:]
                    row["passed"]=not io_errors and state["matrix"]==[[case["expected"]]] and row["independent_validator_agreed"] is True and c.get_config()["assignment_count"]==int(case["expected"]=="FIT")
            except Exception as error:
                row["passed"]=False;row["error_type"]=type(error).__name__
            proof["results"].append(row);proof["status"]="RUNNING";save()
            print(config,case["id"],repetition,row["passed"],flush=True)
proof["status"]="PASS" if all(r["passed"] for r in proof["results"]) else "FAIL"
save();raise SystemExit(0 if proof["status"]=="PASS" else 1)
