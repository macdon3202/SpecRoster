"""Read public receipts only; never load a wallet or publish node configuration."""
import argparse
import json
from genlayer_py import create_client
from genlayer_py.chains import studionet

parser=argparse.ArgumentParser()
parser.add_argument("hash")
args=parser.parse_args()
client=create_client(chain=studionet,endpoint="https://studio.genlayer.com/api")
tx=client.get_transaction(args.hash)
receipts=tx.get("consensus_data",{}).get("leader_receipt",[])
if isinstance(receipts,dict): receipts=[receipts]
print(json.dumps({"hash":args.hash,"status":tx.get("status_name"),"consensus":tx.get("result_name"),"receipts":[{
    "mode":r.get("mode"),"vote":r.get("vote"),"execution":r.get("execution_result"),
    "genvm_result":r.get("genvm_result"),"eq_outputs":r.get("eq_outputs")
} for r in receipts]},indent=2,default=str))
