"""Fetch immutable, canonical standard bytes and record expected outcomes before AI."""
import hashlib
import json
from pathlib import Path
import requests
import argparse
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--refresh-pins",action="store_true",help="Explicitly replace sample pins; invalidates prior release evidence.")
    args=parser.parse_args()
    if (ROOT/"samples"/"public-round.json").exists() and not args.refresh_pins:
        subprocess.run([sys.executable,str(ROOT/"scripts"/"verify_public_sources.py")],check=True)
        return
    session = requests.Session()
    session.headers["User-Agent"] = "SpecRoster-source-manifest"
    manifest = []
    tasks = []
    for number, title, requirement, expected in [
        (712, "Typed signing domains", "Review domain separation in typed structured data signatures.", "FIT"),
        (1559, "Fee market review", "Review the base fee adjustment mechanism for transaction fee markets.", "OUT"),
    ]:
        response = session.get(f"https://api.github.com/repos/ethereum/EIPs/commits?path=EIPS/eip-{number}.md&per_page=1", timeout=30)
        response.raise_for_status()
        commit = response.json()[0]["sha"]
        commit_url = f"https://api.github.com/repos/ethereum/EIPs/commits/{commit}"
        identity = session.get(commit_url, timeout=30)
        identity.raise_for_status()
        assert identity.json()["sha"] == commit and identity.json()["url"] == commit_url
        assert len(identity.content) <= 180_000
        url = f"https://raw.githubusercontent.com/ethereum/EIPs/{commit}/EIPS/eip-{number}.md"
        source = session.get(url, timeout=30)
        source.raise_for_status()
        assert 0 < len(source.content) <= 60_000
        document = source.content.decode("utf-8")
        assert f"eip: {number}" in document.split("\n---\n",1)[0].splitlines()
        digest = hashlib.sha256(source.content).hexdigest()
        (ROOT / "samples" / f"eip-{number}.md").write_bytes(source.content)
        task = {"title": title, "requirement": requirement, "eip": number, "commit": commit, "digest": digest}
        tasks.append(task)
        manifest.append({"resource_id":f"eip-{number}", "purpose":"positive" if expected == "FIT" else "negative-scope", "authoritative_owner":"ethereum/EIPs maintainers", "canonical_origin":"raw.githubusercontent.com/ethereum/EIPs", "commit_api":commit_url, "canonical_url_or_api":url, "repository_and_object_id":f"ethereum/EIPs:EIPS/eip-{number}.md", "revision_or_commit":commit, "expected_content_type":"UTF-8 Markdown", "expected_digest_algorithm":"SHA-256", "expected_digest":digest, "source_bytes":len(source.content), "expected_deterministic_facts":["exact commit repository", "matching EIP frontmatter", "full content digest"], "expected_contract_relation":expected, "mutable_or_immutable":"full-commit-pinned", "claim_being_proved":"task scope relation to the published standard text", "github_authority_scope":"exact commit and file bytes, not implementation or CI", "publisher_controller":"ethereum/EIPs maintainers", "positive_state_beneficiary":"reviewer gains one in-app work assignment", "can_beneficiary_manufacture_fact_alone":False, "what_this_source_cannot_prove":"expertise, implemented behavior, CI success, adoption, or review quality"})
    data = {"round_title":"Wallet standards review sprint", "reviewer_scope":"I review typed signatures, domain separation and replay protection. I exclude transaction fee markets and base fee economics.", "capacity":1, "tasks":tasks, "resources":manifest, "expected_matrix":[["FIT"],["OUT"]], "expected_allocation":[{"task":0,"reviewer":0}], "source_check":"Public fetch successful; validator-network access remains unverified until deployment."}
    (ROOT / "samples" / "public-round.json").write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"resources":[{"eip":t["eip"],"commit":t["commit"],"digest":t["digest"]} for t in tasks]}))

if __name__ == "__main__": main()
