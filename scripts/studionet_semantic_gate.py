"""Run the frozen eight-case semantic corpus on one exact StudioNet deployment.

The main/deployer wallet is never loaded. Wallet A creates rounds and wallet B
registers scope/consents. Every write is checkpointed so an interrupted run can
resume without silently duplicating a case or changing its expectation.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import time

from genlayer_py import create_client
from genlayer_py.chains import studionet

from checkpoint_policy import assert_checkpoint, assert_execution
from studionet_e2e import EXPLORER, POLL_SECONDS, load_aux, plain

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("contract")
    args = parser.parse_args()
    assert len(args.contract) == 42 and args.contract.startswith("0x")

    wallet_a, wallet_b = load_aux()
    client = create_client(chain=studionet, account=wallet_a,
                           endpoint="https://studio.genlayer.com/api")
    source = (ROOT / "contracts" / "spec_roster.py").read_bytes()
    response = client.provider.make_request("gen_getContractCode", [args.contract])
    if isinstance(response, dict):
        assert not response.get("error"), response.get("error")
        response = response["result"]
    assert base64.b64decode(response, validate=True) == source, "DEPLOYED_SOURCE_MISMATCH"

    fixture_path = ROOT / "samples" / "semantic-preflight.json"
    fixture_bytes = fixture_path.read_bytes()
    corpus = json.loads(fixture_bytes)
    public = json.loads((ROOT / "samples" / "public-round.json").read_text(encoding="utf-8"))
    target = ROOT / "docs" / "evidence" / (args.contract.lower() + "-semantic-gate.json")
    proof = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {
        "kind": "STUDIONET_SEMANTIC_GATE",
        "contract": args.contract,
        "network": "studionet",
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "corpus_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "wallet_a": str(wallet_a.address),
        "wallet_b": str(wallet_b.address),
        "main_wallet_used": False,
        "cases": {},
        "status": "RUNNING",
    }
    assert proof["contract"].lower() == args.contract.lower()
    assert proof["source_sha256"] == hashlib.sha256(source).hexdigest()
    assert proof["corpus_sha256"] == hashlib.sha256(fixture_bytes).hexdigest(), "CORPUS_CHANGED"
    assert proof["wallet_a"].lower() == str(wallet_a.address).lower()
    assert proof["wallet_b"].lower() == str(wallet_b.address).lower()

    def save():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")

    def read(method, values=None):
        values = [] if values is None else values
        for attempt in range(8):
            try:
                return plain(client.read_contract(address=args.contract,
                                                  function_name=method,
                                                  args=values, account=wallet_a))
            except Exception:
                if attempt == 7:
                    raise
                time.sleep(POLL_SECONDS)

    def send(case, label, actor, method, values):
        writes = case.setdefault("writes", {})
        item = writes.setdefault(label, {"method": method, "args": values,
                                         "actor": str(actor.address), "expected_error": None})
        assert_checkpoint(item, method, values, str(actor.address), None)
        if item.get("verified"):
            return item
        if "hash" not in item and item.get("ethereum_hash"):
            receipt = client.w3.eth.get_transaction_receipt(item["ethereum_hash"])
            event = client.w3.eth.contract(
                abi=studionet.consensus_main_contract["abi"]).get_event_by_name("NewTransaction")
            events = event.process_receipt(receipt)
            assert len(events) == 1, "SUBMISSION_EVENT_NOT_FOUND"
            item["hash"] = client.w3.to_hex(events[0]["args"]["txId"])
            item["explorer"] = EXPLORER + "/tx/" + item["hash"]
            save()
        if "hash" not in item:
            original_request = client.provider.make_request
            def tracking_request(method, params):
                response = original_request(method, params)
                if method == "eth_sendRawTransaction":
                    item["ethereum_hash"] = response["result"]
                    save()
                return response
            client.provider.make_request = tracking_request
            try:
                item["hash"] = str(client.write_contract(address=args.contract,
                                                         function_name=method,
                                                         args=values, account=actor, value=0))
            finally:
                client.provider.make_request = original_request
            item["explorer"] = EXPLORER + "/tx/" + item["hash"]
            save()
            print(case["id"], label, item["hash"], flush=True)
        for _ in range(200):
            tx = plain(client.get_transaction(item["hash"]))
            if tx.get("status_name") == "FINALIZED":
                break
            time.sleep(POLL_SECONDS)
        else:
            raise TimeoutError(item["hash"])
        receipts = tx.get("consensus_data", {}).get("leader_receipt", [])
        receipts = [receipts] if isinstance(receipts, dict) else receipts
        leader = next((receipt for receipt in receipts if receipt.get("mode") == "leader"), {})
        item["status"] = tx.get("status_name")
        item["consensus"] = tx.get("result_name")
        item["leader"] = {key: leader.get(key) for key in
                          ("execution_result", "result", "genvm_result")}
        assert item["consensus"] == "MAJORITY_AGREE", item["consensus"]
        assert_execution(leader, None)
        item["verified"] = True
        save()
        return item

    config = read("get_config")
    assert config["version"] == "SPEC_ROSTER_V4_CANDIDATE"
    assert config["deployer_authority"] == "NONE"
    proof["config"] = config
    save()

    for definition in corpus["cases"]:
        case = proof["cases"].setdefault(definition["id"], {
            "id": definition["id"], "expected": definition["expected"], "writes": {}})
        assert case["expected"] == definition["expected"], "EXPECTATION_CHANGED"
        template = dict(public["tasks"][definition["task_index"]])
        template["requirement"] = definition["requirement"]
        created = send(case, "create", wallet_a, "create_round", [
            "Semantic gate / " + definition["id"], json.dumps([template]),
            json.dumps([str(wallet_b.address)])])
        if "round_id" not in case:
            case["round_id"] = int(str(created["leader"]["result"]["payload"]["readable"]).strip('"'))
            save()
        round_id = case["round_id"]
        send(case, "scope", wallet_b, "register_scope",
             [round_id, definition["scope"], 1])
        send(case, "freeze", wallet_a, "freeze_round", [round_id])
        digest = read("get_round", [round_id])["round_digest"]
        case.setdefault("round_digest", digest)
        assert case["round_digest"] == digest
        send(case, "consent", wallet_b, "consent_round", [round_id, digest])
        send(case, "allocate", wallet_a, "allocate_round", [round_id, digest])
        observed = read("get_round", [round_id])
        actual = observed["matrix"][0][0]
        case["observed"] = actual
        case["round_state"] = observed["state"]
        case["allocation"] = observed["allocation"]
        case["passed"] = actual == definition["expected"]
        save()
        assert case["passed"], "%s expected %s got %s" % (
            definition["id"], definition["expected"], actual)
        expected_assignments = 1 if definition["expected"] == "FIT" else 0
        assert len(observed["allocation"]) == expected_assignments

    proof["status"] = "PASS"
    save()
    print("STUDIONET_SEMANTIC_GATE_PASS", flush=True)


if __name__ == "__main__":
    main()
