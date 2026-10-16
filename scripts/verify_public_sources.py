"""Read-only network verification of PREEXISTING pins. Never refresh fixtures."""
import hashlib
import json
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
sample=ROOT/"samples"/"public-round.json"
original=sample.read_bytes()
proof={"kind":"REAL_PUBLIC_SOURCE_RETRIEVAL_ONLY","semantic_judgment":False,"validator_network":False,"fixture_sha256":hashlib.sha256(original).hexdigest(),"source_sha256":hashlib.sha256((ROOT/"contracts"/"spec_roster.py").read_bytes()).hexdigest(),"resources":[]}
session=requests.Session();session.headers["User-Agent"]="SpecRoster-audit"
for task in json.loads(original)["tasks"]:
    row={"eip":task["eip"],"commit":task["commit"],"expected_digest":task["digest"]}
    commit_url="https://api.github.com/repos/ethereum/EIPs/commits/"+task["commit"]
    compare_url="https://api.github.com/repos/ethereum/EIPs/compare/"+task["commit"]+"...master?per_page=1&page=2"
    raw_url="https://raw.githubusercontent.com/ethereum/EIPs/"+task["commit"]+"/EIPS/eip-"+str(task["eip"])+".md"
    responses=[session.get(url,timeout=30,allow_redirects=False) for url in (commit_url,compare_url,raw_url)]
    assert all(r.status_code==200 for r in responses),"HTTP_STATUS_OR_REDIRECT"
    assert all(len(r.content)<=cap for r,cap in zip(responses,(180000,180000,60000)))
    commit,comparison=responses[0].json(),responses[1].json()
    assert commit["sha"]==task["commit"] and commit["url"]==commit_url
    assert comparison["status"] in {"ahead","identical"}
    assert comparison["base_commit"]["sha"]==comparison["merge_base_commit"]["sha"]==task["commit"]
    raw=responses[2].content
    assert hashlib.sha256(raw).hexdigest()==task["digest"]
    assert raw==(ROOT/"samples"/("eip-"+str(task["eip"])+".md")).read_bytes()
    row.update({"commit_api":commit_url,"ancestry_api":compare_url,"raw_url":raw_url,"canonical_branch":"master","ancestry_status":comparison["status"],"source_bytes":len(raw),"response_bytes":[len(r.content) for r in responses],"redirects":False,"exact_local_copy":True,"passed":True})
    proof["resources"].append(row)
assert sample.read_bytes()==original,"FIXTURE_CHANGED_DURING_CHECK"
proof["status"]="PASS"
(ROOT/"docs"/"evidence"/"public-source-audit.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
print(json.dumps(proof,indent=2))
