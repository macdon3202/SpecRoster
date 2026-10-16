import ast
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import pytest
from test_contract import CONTRACT,COMMIT,DOC,A,B,deploy,prepare,task,allocate,snap,model_facts,authority_mock

def helper(name):
    tree=ast.parse(CONTRACT.read_text())
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    namespace={}
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(CONTRACT),"exec"),namespace)
    return namespace[name]

def test_matching_exhaustive_2_tasks_3_reviewers():
    matching=helper("matching")
    cases=0
    for bits in itertools.product(("FIT","OUT"),repeat=6):
        matrix=[list(bits[:3]),list(bits[3:])]
        for capacities in itertools.product(range(3),repeat=3):
            valid=[]
            for choice in itertools.product((0,1,2,-1),repeat=2):
                if all(r==-1 or matrix[t][r]=="FIT" for t,r in enumerate(choice)) and all(choice.count(r)<=capacities[r] for r in range(3)):valid.append(choice)
            # Independent enumeration/oracle: cardinality then documented tie order.
            optimum=min(valid,key=lambda c:(-sum(r>=0 for r in c),tuple(3 if r<0 else r for r in c)))
            assert matching(matrix,list(capacities))==list(optimum)
            cases+=1
    assert cases==1728

@pytest.mark.parametrize("document",[
    "missing frontmatter", "---\neip: 999\n---\nWrong EIP", "---\neip: 712\n---\nmoved to another repo", "x"*60001,
],ids=["no-frontmatter","wrong-eip","moved-stub","oversized"])
def test_digest_match_does_not_override_source_identity_or_completeness(direct_vm,direct_deploy,document):
    c=deploy(direct_vm,direct_deploy)
    authority_mock(direct_vm)
    _,d=prepare(c,direct_vm,[task(digest=hashlib.sha256(document.encode()).hexdigest())])
    direct_vm.mock_web(r"api\.github\.com",{"method":"GET","status":200,"body":json.dumps({"sha":COMMIT,"url":"https://api.github.com/repos/ethereum/EIPs/commits/"+COMMIT})})
    direct_vm.mock_web(r"raw\.githubusercontent\.com",{"method":"GET","status":200,"body":document})
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert c.get_round(1)["matrix"]==[] and c.get_config()["assignment_count"]==0

@pytest.mark.parametrize("method,args,error",[
    ("get_round",[999],"ROUND_NOT_FOUND"),
    ("get_assignment",[999],"ASSIGNMENT_NOT_FOUND"),
    ("freeze_round",[999],"ROUND_NOT_FOUND"),
    ("register_scope",[999,"scope",1],"ROUND_NOT_FOUND"),
    ("consent_round",[999,"digest"],"ROUND_NOT_FOUND"),
    ("allocate_round",[999,"digest"],"ROUND_NOT_FOUND"),
    ("cancel_round",[999,"digest"],"ROUND_NOT_FOUND"),
    ("close_round",[999],"ROUND_NOT_FOUND"),
    ("update_assignment",[999,"digest","ACCEPT",""],"ASSIGNMENT_NOT_FOUND"),
])
def test_unknown_object_ids_do_not_mutate_any_entity(direct_vm,direct_deploy,method,args,error):
    c=deploy(direct_vm,direct_deploy);prepare(c,direct_vm);before=snap(c)
    with direct_vm.expect_revert(error):getattr(c,method)(*args)
    assert snap(c)==before

def checkpoint_policy():
    path=CONTRACT.parents[1]/"scripts"/"checkpoint_policy.py"
    spec=importlib.util.spec_from_file_location("checkpoint_policy_under_test",path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def test_checkpoint_cannot_silently_reuse_different_arguments_actor_or_expectation():
    policy=checkpoint_policy();item={"method":"consent_round","args":[1,"digest"],"actor":"0xAB","expected_error":None}
    policy.assert_checkpoint(item,"consent_round",[1,"digest"],"0xab",None)
    for method,args,actor,error in [("cancel_round",[1,"digest"],"0xab",None),("consent_round",[2,"digest"],"0xab",None),("consent_round",[1,"digest"],"0xcd",None),("consent_round",[1,"digest"],"0xab","ERROR")]:
        with pytest.raises(AssertionError):policy.assert_checkpoint(item,method,args,actor,error)

def test_error_name_in_stdout_cannot_fake_revert_evidence():
    policy=checkpoint_policy()
    with pytest.raises(AssertionError):policy.assert_execution({"execution_result":"SUCCESS","result":{"text":"EXPECTED"}},"EXPECTED")
    with pytest.raises(AssertionError):policy.assert_execution({"execution_result":"ERROR","result":{"text":"OTHER"},"genvm_result":{"stdout":"EXPECTED"}},"EXPECTED")
    policy.assert_execution({"execution_result":"ERROR","result":{"text":"EXPECTED"}},"EXPECTED")

@pytest.mark.parametrize("comparison",[
    {"status":"diverged","base_commit":{"sha":COMMIT},"merge_base_commit":{"sha":"b"*40}},
    {"status":"behind","base_commit":{"sha":COMMIT},"merge_base_commit":{"sha":"b"*40}},
    {"status":"ahead","base_commit":{"sha":COMMIT},"merge_base_commit":{"sha":"b"*40}},
    {"status":"ahead"},[],
])
def test_fork_or_invalid_ancestry_cannot_authorize_standard(direct_vm,direct_deploy,comparison):
    c=deploy(direct_vm,direct_deploy);_,d=prepare(c,direct_vm)
    authority_mock(direct_vm,comparison)
    direct_vm.mock_web(r"/commits/",{"method":"GET","status":200,"body":json.dumps({"sha":COMMIT,"url":"https://api.github.com/repos/ethereum/EIPs/commits/"+COMMIT})})
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert c.get_round(1)["matrix"]==[] and c.get_config()["assignment_count"]==0


def test_segment_expansion_prompt_budget_blocks_llm(direct_vm,direct_deploy,monkeypatch):
    document="---\neip: 712\n---\n"+"\n"*50000
    c=deploy(direct_vm,direct_deploy)
    _,d=prepare(c,direct_vm,[task(digest=hashlib.sha256(document.encode()).hexdigest())])
    authority_mock(direct_vm)
    direct_vm.mock_web(r"/commits/",{"method":"GET","status":200,"body":json.dumps({"sha":COMMIT,"url":"https://api.github.com/repos/ethereum/EIPs/commits/"+COMMIT})})
    direct_vm.mock_web(r"raw\.githubusercontent\.com",{"method":"GET","status":200,"body":document})
    from genlayer import gl
    calls=[]
    def unexpected(*a,**k):calls.append(True);return model_facts()
    monkeypatch.setattr(gl.nondet,"exec_prompt",unexpected)
    assert allocate(c,direct_vm,d)=="UNRESOLVED"
    assert calls==[] and c.get_config()["assignment_count"]==0
