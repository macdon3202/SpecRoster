"""Verify attempt exhaustion and owner cancellation of a recorded unresolved run."""
import json
import time
from pathlib import Path
from genlayer_py import create_client
from genlayer_py.chains import studionet
from studionet_e2e import load_aux, plain, ROOT, EXPLORER

ADDRESS="0x07B305921D3c315EBb6708e4F51797a57485bf90"

def main():
    a,_=load_aux()
    c=create_client(chain=studionet,account=a,endpoint="https://studio.genlayer.com/api")
    path=ROOT/"docs"/"evidence"/"unresolved-recovery.json"
    evidence=json.loads(path.read_text()) if path.exists() else {"contract":ADDRESS,"writes":{}}
    def save():path.write_text(json.dumps(evidence,indent=2)+"\n")
    def read(method,args=[]):return plain(c.read_contract(address=ADDRESS,function_name=method,args=args,account=a))
    def snap():return {"round":read("get_round",[1]),"config":read("get_config")}
    digest=read("get_round",[1])["round_digest"]
    for label,method,args,error in [("exhausted","allocate_round",[1,digest],"ATTEMPTS_EXHAUSTED"),("cancel","cancel_round",[1,digest],None)]:
        entry=evidence["writes"].setdefault(label,{})
        if entry.get("verified"):continue
        if "hash" not in entry:
            entry["before"]=snap()
            entry["hash"]=str(c.write_contract(address=ADDRESS,function_name=method,args=args,account=a,value=0))
            entry["url"]=EXPLORER+"/tx/"+entry["hash"];save()
            print(label,entry["hash"],flush=True)
        for _ in range(200):
            try:tx=plain(c.get_transaction(entry["hash"]))
            except Exception:time.sleep(3);continue
            if tx.get("status_name")=="FINALIZED":break
            time.sleep(3)
        else:raise TimeoutError(entry["hash"])
        receipts=tx.get("consensus_data",{}).get("leader_receipt",[])
        if isinstance(receipts,dict):receipts=[receipts]
        leader=next((r for r in receipts if r.get("mode")=="leader"),{})
        entry["consensus"]=tx.get("result_name")
        entry["leader"]={k:leader.get(k) for k in ("execution_result","result","genvm_result")}
        entry["after"]=snap();save()
        assert entry["consensus"]=="MAJORITY_AGREE"
        if error:
            assert error in json.dumps(entry["leader"])
            assert entry["before"]==entry["after"]
            entry["rollback_equal"]=True
        else:
            assert leader.get("execution_result")=="SUCCESS"
            assert entry["after"]["round"]["state"]=="CANCELLED"
        assert entry["after"]["config"]["assignment_count"]==0
        entry["verified"]=True;save()
    print("RECOVERY_VERIFIED",flush=True)

if __name__=="__main__":main()
