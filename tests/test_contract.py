import hashlib
import json
from pathlib import Path
import pytest

CONTRACT = Path(__file__).parents[1] / "contracts" / "spec_roster.py"
A = bytes.fromhex("11" * 20)
B = bytes.fromhex("22" * 20)
C = bytes.fromhex("33" * 20)
SCOPE = "I review typed signatures and replay protection. I exclude fee markets."
DOC = "---\neip: 712\ntitle: Typed signatures\n---\nTyped signatures support domain separation."
COMMIT = "a" * 40

def addr(w): return "0x" + w.hex()

def task(**changes):
    return {"title": "Signing domain review", "requirement": "Review domain separation for typed signatures.", "eip": 712, "commit": COMMIT, "digest": hashlib.sha256(DOC.encode()).hexdigest(), **changes}

def deploy(vm, direct_deploy):
    vm.strict_mocks = True
    vm.check_pickling = True
    with vm.prank(bytes.fromhex("99" * 20)):
        return direct_deploy(CONTRACT, sdk_version="v0.2.16")

def create(c, vm, tasks=None, invites=None):
    with vm.prank(A):
        return c.create_round("Wallet standards sprint", json.dumps(tasks or [task()]), json.dumps(invites or [addr(B)]))

def prepare(c, vm, tasks=None, scope=SCOPE, capacity=1, consent=True):
    rid = create(c, vm, tasks)
    with vm.prank(B): c.register_scope(rid, scope, capacity)
    with vm.prank(A): digest = c.freeze_round(rid)
    if consent:
        with vm.prank(B): c.consent_round(rid, digest)
    return rid, digest

def mocks(vm, relation="FIT", document=DOC, status=200, commit=None):
    if commit is None:authority_mock(vm)
    vm.mock_web(r"^https://api\.github\.com/repos/ethereum/EIPs/commits/" + COMMIT + "$", {"method":"GET", "status":200, "body":json.dumps(commit or {"sha":COMMIT,"url":"https://api.github.com/repos/ethereum/EIPs/commits/"+COMMIT})})
    if commit is None:
        vm.mock_web(r"^https://raw\.githubusercontent\.com/ethereum/EIPs/"+COMMIT+r"/EIPS/eip-712\.md$", {"method":"GET","status":status,"body":document})
    if status == 200 and document == DOC and commit is None:
        vm.mock_llm("SPEC_ROSTER_SCOPE_V1", model_facts(relation))

def model_facts(relation="FIT", **changes):
    return {"source_support":"YES" if relation in {"FIT","OUT"} else relation,
            "scope_coverage":"NO" if relation=="OUT" else "YES",
            "scope_exclusion":"NO","source_index":4,"scope_index":0,**changes}

def authority_mock(vm, comparison=None):
    vm.mock_web(r"^https://api\.github\.com/repos/ethereum/EIPs/compare/"+COMMIT+r"\.\.\.master\?per_page=1&page=2$",{"method":"GET","status":200,"body":json.dumps(comparison if comparison is not None else {"status":"ahead","base_commit":{"sha":COMMIT},"merge_base_commit":{"sha":COMMIT}})})

def allocate(c, vm, digest):
    with vm.prank(A): return c.allocate_round(1, digest)

def snap(c):
    cfg = c.get_config()
    return {"config":cfg,"rounds":[c.get_round(i) for i in range(1,cfg["round_count"]+1)],"assignments":[c.get_assignment(i) for i in range(1,cfg["assignment_count"]+1)]}

def test_complete_happy_journey(direct_vm, direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm)
    assert allocate(c,direct_vm,d)=="ALLOCATED"
    result=c.get_round(1)
    aid=result["allocation"][0]["assignment_id"]
    assert result["matrix"]==[["FIT"]] and c.get_assignment(aid)["assignee"].lower()==addr(B)
    with direct_vm.prank(B):
        assert c.update_assignment(aid,d,"ACCEPT","")=="ACCEPTED"
        assert c.update_assignment(aid,d,"SUBMIT","Checked domain separation; this is a submitted review, not a safety certificate.")=="SUBMITTED"
    with direct_vm.prank(C): assert c.close_round(1)=="CLOSED"

def test_out_creates_no_assignments(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm,"OUT")
    assert allocate(c,direct_vm,d)=="ALLOCATED"
    assert c.get_round(1)["allocation"]==[] and c.get_config()["assignment_count"]==0
    assert c.close_round(1)=="CLOSED"

def test_unknown_is_not_an_edge(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm,"UNKNOWN")
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert c.get_config()["assignment_count"]==0

def test_capacity_and_task_tie_break(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy)
    _,d=prepare(c,direct_vm,[task(),task(title="Second task",requirement="Review replay protection for typed signatures.")])
    mocks(direct_vm)
    allocate(c,direct_vm,d)
    assert [a["task"] for a in c.get_round(1)["allocation"]]==[0]
    assert c.get_config()["assignment_count"]==1

def test_max_matching_not_greedy(direct_vm,direct_deploy,monkeypatch):
    c=deploy(direct_vm,direct_deploy)
    rid=create(c,direct_vm,[task(),task(requirement="Review a second aspect.")],[addr(B),addr(C)])
    for w in (B,C):
        with direct_vm.prank(w): c.register_scope(rid,SCOPE,1)
    with direct_vm.prank(A): d=c.freeze_round(rid)
    for w in (B,C):
        with direct_vm.prank(w): c.consent_round(rid,d)
    from genlayer import gl
    monkeypatch.setattr(gl.vm,"run_nondet",lambda *a,**k:json.dumps({"status":"OBSERVED","matrix":[["FIT","FIT"],["FIT","OUT"]]}))
    allocate(c,direct_vm,d)
    assert [(a["task"],a["reviewer"]) for a in c.get_round(1)["allocation"]]==[(0,1),(1,0)]

def test_consent_required_before_ai(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm,consent=False); before=snap(c)
    with direct_vm.expect_revert("CONSENT_INCOMPLETE"): c.allocate_round(1,d)
    assert snap(c)==before

@pytest.mark.parametrize("actor,error",[(A,"REVIEWER_ONLY"),(C,"REVIEWER_ONLY")])
def test_owner_cannot_supply_reviewer_consent(direct_vm,direct_deploy,actor,error):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm,consent=False); before=snap(c)
    with direct_vm.prank(actor),direct_vm.expect_revert(error): c.consent_round(1,d)
    assert snap(c)==before

def test_wrong_digest_consent_rolls_back(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); prepare(c,direct_vm,consent=False); before=snap(c)
    with direct_vm.prank(B),direct_vm.expect_revert("ROUND_DIGEST_MISMATCH"): c.consent_round(1,"0"*64)
    assert snap(c)==before

def test_scope_cannot_change_after_freeze(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); prepare(c,direct_vm); before=snap(c)
    with direct_vm.prank(B),direct_vm.expect_revert("INTAKE_CLOSED"): c.register_scope(1,"New scope",4)
    assert snap(c)==before

def test_round_digest_cannot_authorize_other_round(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d1=prepare(c,direct_vm); _,d2=prepare(c,direct_vm)
    assert d1!=d2
    before=snap(c)
    with direct_vm.expect_revert("ROUND_DIGEST_MISMATCH"): c.allocate_round(2,d1)
    assert snap(c)==before

@pytest.mark.parametrize("kwargs",[{"status":503},{"status":404},{"document":DOC+"changed"},{"commit":{"sha":"b"*40,"url":"https://api.github.com/repos/ethereum/EIPs/commits/"+COMMIT}},{"commit":{"sha":COMMIT,"url":"https://api.github.com/repos/attacker/EIPs/commits/"+COMMIT}}])
def test_source_integrity_identity_failure_never_assigns(direct_vm,direct_deploy,kwargs):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm,**kwargs)
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert c.get_config()["assignment_count"]==0

def test_invalid_model_and_invented_quote(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm,"BOGUS")
    assert allocate(c,direct_vm,d)=="UNRESOLVED"

def test_bounded_retry_then_cancel(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm,status=503)
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    before=snap(c)
    with direct_vm.expect_revert("ATTEMPTS_EXHAUSTED"): c.allocate_round(1,d)
    assert snap(c)==before
    with direct_vm.prank(A): assert c.close_round(1)=="CANCELLED"

@pytest.mark.parametrize("action,review,error",[("SUBMIT","My review","ACCEPT_FIRST"),("ACCEPT","extra","INVALID_ACCEPT")])
def test_forbidden_assignment_sequence_rolls_back(direct_vm,direct_deploy,action,review,error):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm); allocate(c,direct_vm,d); before=snap(c)
    with direct_vm.prank(B),direct_vm.expect_revert(error): c.update_assignment(1,d,action,review)
    assert snap(c)==before

def test_other_actor_wrong_digest_and_terminal_replay(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm); allocate(c,direct_vm,d); before=snap(c)
    with direct_vm.prank(A),direct_vm.expect_revert("ASSIGNEE_ONLY"): c.update_assignment(1,d,"ACCEPT","")
    assert snap(c)==before
    with direct_vm.prank(B),direct_vm.expect_revert("STALE_ASSIGNMENT"): c.update_assignment(1,"0"*64,"ACCEPT","")
    assert snap(c)==before
    with direct_vm.prank(B): c.update_assignment(1,d,"DECLINE","")
    before=snap(c)
    with direct_vm.prank(B),direct_vm.expect_revert("ASSIGNMENT_TERMINAL"): c.update_assignment(1,d,"ACCEPT","")
    assert snap(c)==before

def test_allocated_round_cannot_cancel_open_work_or_allocate_twice(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm); allocate(c,direct_vm,d); before=snap(c)
    with direct_vm.prank(A),direct_vm.expect_revert("WORK_STILL_OPEN"): c.close_round(1)
    with direct_vm.expect_revert("ROUND_NOT_ALLOCATABLE"): c.allocate_round(1,d)
    assert snap(c)==before

@pytest.mark.parametrize("tasks,invites,error",[([task()]*5,[addr(B)],"INVALID_LIST_SIZE"),([task()],[addr(A)],"OWNER_CANNOT_REVIEW"),([task(),task()],[addr(B)],"DUPLICATE_TASK"),([task(commit="main")],[addr(B)],"INVALID_COMMIT")])
def test_invalid_creation_no_mutation(direct_vm,direct_deploy,tasks,invites,error):
    c=deploy(direct_vm,direct_deploy); before=snap(c)
    with direct_vm.prank(A),direct_vm.expect_revert(error): c.create_round("Test",json.dumps(tasks),json.dumps(invites))
    assert snap(c)==before

def test_no_deployer_authority(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy)
    assert c.get_config()["deployer_authority"]=="NONE"
    create(c,direct_vm)
    with direct_vm.prank(C),direct_vm.expect_revert("NOT_INVITED"): c.register_scope(1,SCOPE,1)

def test_exact_header():
    assert CONTRACT.read_text().splitlines()[:2]==["# v0.2.16",'# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }']


def test_cancel_allocated_round_invalidates_pending_work(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm); allocate(c,direct_vm,d)
    with direct_vm.prank(B): c.update_assignment(1,d,"ACCEPT","")
    with direct_vm.prank(A): assert c.cancel_round(1,d)=="CANCELLED"
    assert c.get_assignment(1)["state"]=="CANCELLED"
    before=snap(c)
    with direct_vm.prank(B),direct_vm.expect_revert("STALE_ASSIGNMENT"): c.update_assignment(1,d,"SUBMIT","Late work")
    assert snap(c)==before


def test_attacker_cannot_cancel_round(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); before=snap(c)
    with direct_vm.prank(C),direct_vm.expect_revert("OWNER_ONLY"): c.cancel_round(1,d)
    assert snap(c)==before


def test_invented_grounding_quote_cannot_fit(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm)
    authority_mock(direct_vm)
    direct_vm.mock_web(r"api\.github\.com",{"method":"GET","status":200,"body":json.dumps({"sha":COMMIT,"url":"https://api.github.com/repos/ethereum/EIPs/commits/"+COMMIT})})
    direct_vm.mock_web(r"raw\.githubusercontent\.com",{"method":"GET","status":200,"body":DOC})
    direct_vm.mock_llm("SPEC_ROSTER_SCOPE_V1",{"relation":"FIT","source_quote":"invented words","scope_quote":"typed signatures"})
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert c.get_config()["assignment_count"]==0


def test_consensus_exception_never_creates_work(direct_vm,direct_deploy,monkeypatch):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm)
    from genlayer import gl
    def fail(*a,**k): raise RuntimeError("No majority")
    monkeypatch.setattr(gl.vm,"run_nondet",fail)
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert c.get_config()["assignment_count"]==0


def test_validator_independently_rejects_wrong_leader(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm,"OUT")
    allocate(c,direct_vm,d)
    assert direct_vm.run_validator(leader_result=json.dumps({"status":"OBSERVED","matrix":[["FIT"]]})) is False
    assert direct_vm.run_validator(leader_result=json.dumps({"status":"OBSERVED","matrix":[["OUT"]]})) is True


def test_validator_reobserves_changed_source_and_rejects_prior_fit(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm); mocks(direct_vm)
    allocate(c,direct_vm,d)
    direct_vm.clear_mocks()
    mocks(direct_vm,document=DOC+"changed")
    assert direct_vm.run_validator() is False


@pytest.mark.parametrize("output",[
    {"relation": [], "source_quote":"domain separation", "scope_quote":"typed signatures"},
    {"relation":"FIT", "source_quote":"Domain separation", "scope_quote":"typed signatures"},
    {"relation":"FIT", "source_quote":"domain ... separation", "scope_quote":"typed signatures"},
    {"relation":"FIT", "source_quote":"domain separation", "scope_quote":"invented scope"},
    {"relation":"FIT", "source_quote":"x"*601, "scope_quote":"typed signatures"},
    {"relation":"FIT", "source_quote":"", "scope_quote":"typed signatures"},
    {"relation":"FIT", "source_quote":"domain separation"},
])
def test_legacy_quotes_rejected_by_v3_schema(direct_vm,direct_deploy,output):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm)
    authority_mock(direct_vm)
    direct_vm.mock_web(r"api\.github\.com",{"method":"GET","status":200,"body":json.dumps({"sha":COMMIT,"url":"https://api.github.com/repos/ethereum/EIPs/commits/"+COMMIT})})
    direct_vm.mock_web(r"raw\.githubusercontent\.com",{"method":"GET","status":200,"body":DOC})
    direct_vm.mock_llm("SPEC_ROSTER_SCOPE_V1",output)
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert c.get_round(1)["matrix"]==[["UNKNOWN"]]
    assert c.get_config()["assignment_count"]==0


@pytest.mark.parametrize("source_index,scope_index",[(-1,0),(999,0),(4,999),(True,0),(4,False),("4",0),(4,1.5)])
def test_invalid_evidence_pointer_never_assigns(direct_vm,direct_deploy,source_index,scope_index):
    c=deploy(direct_vm,direct_deploy); _,d=prepare(c,direct_vm)
    authority_mock(direct_vm)
    direct_vm.mock_web(r"api\.github\.com",{"method":"GET","status":200,"body":json.dumps({"sha":COMMIT,"url":"https://api.github.com/repos/ethereum/EIPs/commits/"+COMMIT})})
    direct_vm.mock_web(r"raw\.githubusercontent\.com",{"method":"GET","status":200,"body":DOC})
    direct_vm.mock_llm("SPEC_ROSTER_SCOPE_V1",model_facts(source_index=source_index,scope_index=scope_index))
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert c.get_config()["assignment_count"]==0


def test_segments_are_lossless_and_bounded():
    import ast
    tree=ast.parse(CONTRACT.read_text())
    function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="evidence_segments")
    namespace={}
    exec(compile(ast.Module(body=[function],type_ignores=[]),str(CONTRACT),"exec"),namespace)
    for original in (DOC,"\n\nA\r\nB\n","é😀"*500,"x"*1000):
        segments=namespace["evidence_segments"](original)
        assert "".join(segments)==original
        assert all(0<len(s)<=120 and len(s.encode())<=480 for s in segments)
