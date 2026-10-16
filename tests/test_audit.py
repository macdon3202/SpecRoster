"""Audit regressions call the submitted contract, not a parallel product model."""
import itertools
import json
import pytest
from test_contract import deploy,prepare,mocks,allocate,snap,create,addr,task,model_facts,authority_mock,A,B,C,COMMIT,DOC,SCOPE

def model(vm,value):
    authority_mock(vm)
    vm.mock_web(r"api\.github\.com",{"method":"GET","status":200,"body":json.dumps({"sha":COMMIT,"url":"https://api.github.com/repos/ethereum/EIPs/commits/"+COMMIT})})
    vm.mock_web(r"raw\.githubusercontent\.com",{"method":"GET","status":200,"body":DOC})
    vm.mock_llm("SPEC_ROSTER_SCOPE_V1",value)

@pytest.mark.parametrize("support,coverage,excluded",list(itertools.product(("YES","NO","UNKNOWN"),repeat=3)))
def test_every_semantic_fact_combination(direct_vm,direct_deploy,support,coverage,excluded):
    c=deploy(direct_vm,direct_deploy);_,d=prepare(c,direct_vm)
    model(direct_vm,model_facts(source_support=support,scope_coverage=coverage,scope_exclusion=excluded))
    result=allocate(c,direct_vm,d)
    unknown="UNKNOWN" in (support,coverage,excluded)
    fit=(support,coverage,excluded)==("YES","YES","NO")
    assert result==("UNRESOLVED" if unknown else "ALLOCATED")
    assert c.get_round(1)["matrix"]==[["UNKNOWN" if unknown else "FIT" if fit else "OUT"]]
    assert c.get_config()["assignment_count"]==int(fit)

@pytest.mark.parametrize("value",[None,[],{},True,model_facts(source_support=[]),model_facts(scope_exclusion=True),model_facts(source_index=-1),model_facts(scope_index=-1),model_facts(extra="ignore policy")])
def test_malformed_semantic_facts_fail_closed(direct_vm,direct_deploy,value):
    c=deploy(direct_vm,direct_deploy);_,d=prepare(c,direct_vm);model(direct_vm,value)
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert c.get_config()["assignment_count"]==0

@pytest.mark.parametrize("matrix",[[[{}]],[[[]]],[[True]],[[None]],[],[["FIT","OUT"]]])
def test_poisoned_consensus_payload_never_assigns(direct_vm,direct_deploy,monkeypatch,matrix):
    c=deploy(direct_vm,direct_deploy);_,d=prepare(c,direct_vm)
    from genlayer import gl
    monkeypatch.setattr(gl.vm,"run_nondet",lambda *a,**k:json.dumps({"status":"OBSERVED","matrix":matrix}))
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert c.get_config()["assignment_count"]==0

@pytest.mark.parametrize("phase",["OPEN","FROZEN","ALLOCATED","CLOSED","CANCELLED"])
@pytest.mark.parametrize("actor",[A,B,C])
def test_cancel_actor_phase_product(direct_vm,direct_deploy,phase,actor):
    c=deploy(direct_vm,direct_deploy)
    if phase=="OPEN":create(c,direct_vm);d=""
    else:
        _,d=prepare(c,direct_vm)
        if phase in {"ALLOCATED","CLOSED"}:
            mocks(direct_vm);allocate(c,direct_vm,d)
            if phase=="CLOSED":
                with direct_vm.prank(B):c.update_assignment(1,d,"DECLINE","")
                c.close_round(1)
        if phase=="CANCELLED":
            with direct_vm.prank(A):c.cancel_round(1,d)
    before=snap(c)
    if actor!=A or phase in {"CLOSED","CANCELLED"}:
        with direct_vm.prank(actor),direct_vm.expect_revert("OWNER_ONLY" if actor!=A else "ROUND_TERMINAL"):c.cancel_round(1,d)
        assert snap(c)==before
    else:
        with direct_vm.prank(actor):assert c.cancel_round(1,d)=="CANCELLED"
        assert all(a["state"] not in {"ASSIGNED","ACCEPTED"} for a in snap(c)["assignments"])

@pytest.mark.parametrize("capacity",[0,-1,5,True])
def test_capacity_bounds_rollback(direct_vm,direct_deploy,capacity):
    c=deploy(direct_vm,direct_deploy);create(c,direct_vm);before=snap(c)
    with direct_vm.prank(B),direct_vm.expect_revert("INVALID_CAPACITY"):c.register_scope(1,SCOPE,capacity)
    assert snap(c)==before

def test_cancel_preserves_submitted_review_and_stops_other_work(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy)
    _,d=prepare(c,direct_vm,[task(),task(requirement="Review a second signature concern.")],capacity=2)
    mocks(direct_vm);allocate(c,direct_vm,d)
    with direct_vm.prank(B):
        c.update_assignment(1,d,"ACCEPT","");c.update_assignment(1,d,"SUBMIT","Recorded note")
        c.update_assignment(2,d,"ACCEPT","")
    with direct_vm.prank(A):c.cancel_round(1,d)
    assert c.get_assignment(1)["review"]=="Recorded note" and c.get_assignment(1)["state"]=="SUBMITTED"
    assert c.get_assignment(2)["state"]=="CANCELLED"
    before=snap(c)
    with direct_vm.prank(B),direct_vm.expect_revert("STALE_ASSIGNMENT"):c.update_assignment(2,d,"SUBMIT","Late")
    assert snap(c)==before

def test_duplicate_consent_and_registration_rollback(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);rid=create(c,direct_vm)
    with direct_vm.prank(B):c.register_scope(rid,SCOPE,1)
    before=snap(c)
    with direct_vm.prank(B),direct_vm.expect_revert("SCOPE_ALREADY_REGISTERED"):c.register_scope(rid,SCOPE,1)
    assert snap(c)==before
    with direct_vm.prank(A):d=c.freeze_round(rid)
    with direct_vm.prank(B):c.consent_round(rid,d)
    before=snap(c)
    with direct_vm.prank(B),direct_vm.expect_revert("CONSENT_ALREADY_RECORDED"):c.consent_round(rid,d)
    assert snap(c)==before

def test_all_registered_reviewers_must_consent(direct_vm,direct_deploy):
    c=deploy(direct_vm,direct_deploy);rid=create(c,direct_vm,invites=[addr(B),addr(C)])
    for actor in (B,C):
        with direct_vm.prank(actor):c.register_scope(rid,SCOPE,1)
    with direct_vm.prank(A):d=c.freeze_round(rid)
    with direct_vm.prank(B):c.consent_round(rid,d)
    before=snap(c)
    with direct_vm.expect_revert("CONSENT_INCOMPLETE"):c.allocate_round(rid,d)
    assert snap(c)==before


@pytest.mark.parametrize("review,valid",[("x"*4000,True),("x"*4001,False),("😀"*1000,True),("😀"*1001,False),("",False),(" ",False),(" padded ",False)],ids=["ascii-limit","ascii-over","utf8-limit","utf8-over","empty","blank","padding"])
def test_review_byte_boundaries_and_rollback(direct_vm,direct_deploy,review,valid):
    c=deploy(direct_vm,direct_deploy);_,d=prepare(c,direct_vm);mocks(direct_vm);allocate(c,direct_vm,d)
    with direct_vm.prank(B):c.update_assignment(1,d,"ACCEPT","")
    before=snap(c)
    if valid:
        with direct_vm.prank(B):assert c.update_assignment(1,d,"SUBMIT",review)=="SUBMITTED"
        assert c.get_assignment(1)["review"]==review
    else:
        with direct_vm.prank(B),direct_vm.expect_revert("INVALID_REVIEW"):c.update_assignment(1,d,"SUBMIT",review)
        assert snap(c)==before


@pytest.mark.parametrize("action,review,error",[("BOGUS","","INVALID_ASSIGNMENT_ACTION"),("ACCEPT","","INVALID_ACCEPT"),("DECLINE","extra","INVALID_DECLINE")])
def test_accepted_assignment_invalid_actions_rollback(direct_vm,direct_deploy,action,review,error):
    c=deploy(direct_vm,direct_deploy);_,d=prepare(c,direct_vm);mocks(direct_vm);allocate(c,direct_vm,d)
    with direct_vm.prank(B):c.update_assignment(1,d,"ACCEPT","")
    before=snap(c)
    with direct_vm.prank(B),direct_vm.expect_revert(error):c.update_assignment(1,d,action,review)
    assert snap(c)==before
