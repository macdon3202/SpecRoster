"""Pure evidence gates shared with regression tests. No RPC or wallet access."""
def assert_checkpoint(item,method,values,actor,error):
    assert item["method"]==method and item["args"]==values,"CHECKPOINT_ARGUMENT_MISMATCH"
    assert item["actor"].lower()==actor.lower(),"CHECKPOINT_ACTOR_MISMATCH"
    assert item.get("expected_error")==error,"CHECKPOINT_EXPECTATION_MISMATCH"

def assert_execution(leader,expected_error=None):
    if expected_error:
        assert leader.get("execution_result") in {"ERROR","REVERT"},"EXPECTED_REVERT_BUT_EXECUTION_NOT_ERROR"
        # Only authoritative execution result; never arbitrary stdout/model prose.
        import json
        assert expected_error in json.dumps(leader.get("result")),"EXPECTED_ERROR_NOT_IN_RESULT"
    else:
        assert leader.get("execution_result")=="SUCCESS","EXECUTION_NOT_SUCCESS"
