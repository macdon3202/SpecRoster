"""Checkpointed two-auxiliary-wallet product test; never loads the main wallet.

Usage: py scripts/studionet_e2e.py CONTRACT_ADDRESS happy|guards|sources|cancel
Happy writes seven lifecycle transactions and verifies exact returned IDs.
"""
import argparse
import json
import os
from pathlib import Path
import time
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
from checkpoint_policy import assert_checkpoint, assert_execution

ROOT=Path(__file__).resolve().parents[1]
EXPLORER="https://explorer-studio.genlayer.com"
POLL_SECONDS=12

def plain(value):
    if isinstance(value,dict): return {str(k):plain(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)): return [plain(v) for v in value]
    return value if value is None or isinstance(value,(str,int,bool,float)) else str(value)

def load_aux():
    selected={}
    for line in (ROOT.parent/"secrets"/"genlayer-test-wallets.env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key,value=line.split("=",1)
            if key.strip() in {"SERVICE_LEDGER_KEY_A","SERVICE_LEDGER_KEY_B"}:
                selected[key.strip()]=value.strip().strip("'\"").strip("<>")
    a=create_account(os.environ.get("SERVICE_LEDGER_KEY_A") or selected["SERVICE_LEDGER_KEY_A"])
    b=create_account(os.environ.get("SERVICE_LEDGER_KEY_B") or selected["SERVICE_LEDGER_KEY_B"])
    assert str(a.address).lower()!=str(b.address).lower()
    return a,b

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("contract")
    parser.add_argument("mode",choices=["happy","guards","sources","cancel","preguards"])
    args=parser.parse_args()
    assert len(args.contract)==42 and args.contract.startswith("0x")
    a,b=load_aux()
    client=create_client(chain=studionet,account=a,endpoint="https://studio.genlayer.com/api")
    sample=json.loads((ROOT/"samples"/"public-round.json").read_text())
    target=ROOT/"docs"/"evidence"/(args.contract.lower()+"-"+args.mode+".json")
    target.parent.mkdir(parents=True,exist_ok=True)
    evidence=json.loads(target.read_text()) if target.exists() else {"contract":args.contract,"network":"studionet","mode":args.mode,"wallet_a":str(a.address),"wallet_b":str(b.address),"main_wallet_used":False,"writes":{},"expected_matrix":sample["expected_matrix"]}
    assert evidence["contract"].lower()==args.contract.lower() and evidence["mode"]==args.mode
    assert evidence["wallet_a"].lower()==str(a.address).lower() and evidence["wallet_b"].lower()==str(b.address).lower()
    assert evidence["expected_matrix"]==sample["expected_matrix"],"EXPECTED_MATRIX_CHANGED"
    def save(): target.write_text(json.dumps(evidence,indent=2)+"\n",encoding="utf-8")
    def read(method,values=[]):
        for attempt in range(8):
            try: return plain(client.read_contract(address=args.contract,function_name=method,args=values,account=a))
            except Exception:
                if attempt==7: raise
                time.sleep(POLL_SECONDS)
    def snapshot(method=None,values=None,result=None):
        cfg=read("get_config")
        state={"config":cfg,"focus":{"method":method,"args":values or []}}
        if method=="create_round" and result is not None:
            rid=int(str(result["payload"]["readable"]).strip('"'))
            state["round"]=read("get_round",[rid])
        elif method=="update_assignment" and values:
            assignment=read("get_assignment",[values[0]])
            state["assignment"]=assignment
            state["round"]=read("get_round",[assignment["round_id"]])
        elif method in {"register_scope","freeze_round","consent_round","allocate_round","cancel_round","close_round"} and values:
            state["round"]=read("get_round",[values[0]])
        return state
    def send(label,actor,method,values,error=None):
        item=evidence["writes"].setdefault(label,{"method":method,"args":values,"actor":str(actor.address),"expected_error":error})
        assert_checkpoint(item,method,values,str(actor.address),error)
        if item.get("interrupted_before_post_snapshot"):
            return send(label+"_recheck",actor,method,values,error)
        if item.get("verified"): return item
        if "hash" not in item and item.get("ethereum_hash"):
            receipt=client.w3.eth.get_transaction_receipt(item["ethereum_hash"])
            event=client.w3.eth.contract(abi=studionet.consensus_main_contract["abi"]).get_event_by_name("NewTransaction")
            events=event.process_receipt(receipt)
            assert len(events)==1,"SUBMISSION_EVENT_NOT_FOUND"
            item["hash"]=client.w3.to_hex(events[0]["args"]["txId"])
            item["explorer"]=EXPLORER+"/tx/"+item["hash"]
            save()
        if "hash" not in item:
            item["before"]=snapshot(method,values)
            original_request=client.provider.make_request
            def tracking_request(method,params):
                response=original_request(method,params)
                if method=="eth_sendRawTransaction":
                    item["ethereum_hash"]=response["result"]
                    save()
                return response
            client.provider.make_request=tracking_request
            try:
                item["hash"]=str(client.write_contract(address=args.contract,function_name=method,args=values,account=actor,value=0))
            finally:
                client.provider.make_request=original_request
            item["explorer"]=EXPLORER+"/tx/"+item["hash"]
            save(); print(label,item["hash"],flush=True)
        for _ in range(200):
            try: tx=plain(client.get_transaction(item["hash"]))
            except Exception: time.sleep(POLL_SECONDS); continue
            if tx.get("status_name")=="FINALIZED": break
            time.sleep(POLL_SECONDS)
        else: raise TimeoutError(item["hash"])
        receipts=tx.get("consensus_data",{}).get("leader_receipt",[])
        if isinstance(receipts,dict): receipts=[receipts]
        leader=next((r for r in receipts if r.get("mode")=="leader"),{})
        item["status"]=tx.get("status_name")
        item["consensus"]=tx.get("result_name")
        item["leader"]={k:leader.get(k) for k in ("execution_result","result","genvm_result")}
        item["after"]=snapshot(method,values,leader.get("result")); save()
        assert item["consensus"]=="MAJORITY_AGREE",item["consensus"]
        assert_execution(leader,error)
        if error:
            assert item["before"]==item["after"],"ROLLBACK_MISMATCH"
            item["rollback_equal"]=True
        item["verified"]=True;save()
        return item
    cfg=read("get_config")
    assert cfg["version"] in {"SPEC_ROSTER_V1","SPEC_ROSTER_V2","SPEC_ROSTER_V3","SPEC_ROSTER_V4_CANDIDATE"} and cfg["deployer_authority"]=="NONE"
    evidence["config"]=cfg;save()
    tasks=sample["tasks"]
    if args.mode=="sources":
        tasks=[dict(tasks[0],digest="0"*64)]
    created=send("create",a,"create_round",[sample["round_title"]+" / "+args.mode,json.dumps(tasks),json.dumps([str(b.address)])])
    result=created["leader"]["result"]
    rid=int(str(result["payload"]["readable"]).strip('"'))
    send("scope",b,"register_scope",[rid,sample["reviewer_scope"],sample["capacity"]])
    frozen=send("freeze",a,"freeze_round",[rid])
    digest=read("get_round",[rid])["round_digest"]
    if args.mode in {"guards","preguards"}:
        send("before_consent",a,"allocate_round",[rid,digest],"CONSENT_INCOMPLETE")
        send("wrong_consent",a,"consent_round",[rid,digest],"REVIEWER_ONLY")
        send("wrong_digest",b,"consent_round",[rid,"0"*64],"ROUND_DIGEST_MISMATCH")
    if args.mode=="preguards":
        send("late_scope",b,"register_scope",[rid,sample["reviewer_scope"],1],"INTAKE_CLOSED")
        send("refreeze",a,"freeze_round",[rid],"ROUND_NOT_OPEN")
        send("wrong_cancel_actor",b,"cancel_round",[rid,digest],"OWNER_ONLY")
        send("wrong_cancel_digest",a,"cancel_round",[rid,"0"*64],"ROUND_DIGEST_MISMATCH")
        send("cancel",a,"cancel_round",[rid,digest])
        send("late_consent",b,"consent_round",[rid,digest],"CONSENT_PHASE_CLOSED")
        send("late_allocate",a,"allocate_round",[rid,digest],"ROUND_NOT_ALLOCATABLE")
        evidence["final"]=snapshot("cancel_round",[rid]);save()
        print("VERIFIED",args.mode,"round",rid,flush=True)
        return
    current_round=read("get_round",[rid])
    if str(b.address).lower() in [str(value).lower() for value in current_round["consents"]]:
        evidence["consent_recovery"]={
            "verified_from_state":True,
            "round_id":rid,
            "wallet":str(b.address),
            "reason":"A prior submission completed despite an RPC/receipt interruption; no duplicate write sent.",
        }
        save()
    else:
        send("consent",b,"consent_round",[rid,digest])
    allocation=send("allocate",a,"allocate_round",[rid,digest])
    r=allocation["after"]["round"]
    if args.mode=="sources":
        assert r["state"]=="UNRESOLVED" and r["allocation"]==[] and r["matrix"]==[]
        assert allocation["before"]["config"]["assignment_count"]==allocation["after"]["config"]["assignment_count"]
        send("cancel",a,"cancel_round",[rid,digest])
        evidence["final"]=snapshot("cancel_round",[rid]);save()
        print("VERIFIED",args.mode,"round",rid,flush=True)
        return
    if r["state"]=="UNRESOLVED" and r["attempts"]<2:
        allocation=send("allocate_retry",a,"allocate_round",[rid,digest])
        r=allocation["after"]["round"]
    assert r["state"]=="ALLOCATED" and r["matrix"]==sample["expected_matrix"],r
    assert [(x["task"],x["reviewer"]) for x in r["allocation"]]==[(0,0)]
    aid=r["allocation"][0]["assignment_id"]
    if args.mode=="guards":
        send("replay_allocate",a,"allocate_round",[rid,digest],"ROUND_NOT_ALLOCATABLE")
        send("wrong_assignee",a,"update_assignment",[aid,digest,"ACCEPT",""],"ASSIGNEE_ONLY")
        send("early_submit",b,"update_assignment",[aid,digest,"SUBMIT","Out of order"],"ACCEPT_FIRST")
    send("accept",b,"update_assignment",[aid,digest,"ACCEPT",""])
    if args.mode=="cancel":
        send("cancel",a,"cancel_round",[rid,digest])
        send("late_submit",b,"update_assignment",[aid,digest,"SUBMIT","Late work"],"STALE_ASSIGNMENT")
    else:
        send("submit",b,"update_assignment",[aid,digest,"SUBMIT","Review note: inspect domain separation fields and replay assumptions. This submission does not certify implementation safety."])
        send("close",a,"close_round",[rid])
        if args.mode=="guards":send("terminal_submit",b,"update_assignment",[aid,digest,"SUBMIT","Replay"],"STALE_ASSIGNMENT")
    evidence["final"]=snapshot("close_round" if args.mode!="cancel" else "cancel_round",[rid]);save()
    print("VERIFIED",args.mode,"round",rid,flush=True)

if __name__=="__main__":main()
