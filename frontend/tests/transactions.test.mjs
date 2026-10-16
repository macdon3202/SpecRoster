import test from 'node:test';
import assert from 'node:assert/strict';
import {normalizeHash,normalizeReadback,receiptState,returnedId,assertReconciled,pendingFor,VERSION,parseRoundId,assertSnapshot} from '../src/transactions.js';
const account='0x'+'11'.repeat(20);
const hash='0x'+'aa'.repeat(32);
const receipt=(execution='SUCCESS',consensus='MAJORITY_AGREE',readable='7')=>({status_name:'FINALIZED',result_name:consensus,consensus_data:{leader_receipt:[{mode:'leader',execution_result:execution,result:{payload:{readable}}}]}});
const state=(round={},assignments=[])=>({config:{version:VERSION},round:{id:7,owner:account,state:'OPEN',title:'Round',reviewers:[],consents:[],round_digest:'digest',...round},assignments});

test('top-level success cannot replace a missing authoritative leader',()=>{
  assert.equal(receiptState({status_name:'FINALIZED',result_name:'MAJORITY_AGREE',execution_result:'SUCCESS'}).verified,false);
  for(const consensus of ['AGREE','ACCEPTED'])assert.equal(receiptState(receipt('SUCCESS',consensus)).verified,false);
});
test('pending journal prevents duplicate signing after a readback/network failure',()=>{
  assert.equal(pendingFor([{state:'PENDING',address:account,account}],account,account),true);
  for(const state of ['FAILED','RECONCILED'])assert.equal(pendingFor([{state,address:account,account}],account,account),false);
  assert.equal(pendingFor([{state:'PENDING',address:account,account}],account,'0x'+'22'.repeat(20)),false);
});
test('SDK bigint readbacks are normalized without unsafe integer rounding',()=>{
  assert.deepEqual(normalizeReadback({id:7n,allocation:[{assignment_id:9n}],capacity:1n}),{id:7,allocation:[{assignment_id:9}],capacity:1});
  assert.throws(()=>normalizeReadback(9007199254740993n));
});
test('normalizes supported hash shapes, rejects invalid wrappers',()=>{
  for(const x of [hash,{txId:hash},{hash}])assert.equal(normalizeHash(x),hash);
  assert.throws(()=>normalizeHash({txId:{hash}}));
});
test('submitted and accepted are never business success',()=>{
  assert.equal(receiptState({status_name:'ACCEPTED',result_name:'MAJORITY_AGREE'}).verified,false);
  assert.equal(receiptState({status_name:'SUBMITTED'}).verified,false);
});
test('finalized execution error or disagreement fail closed',()=>{
  for(const r of [receipt('ERROR'),receipt('SUCCESS','MAJORITY_DISAGREE')]) {
    assert.equal(receiptState(r).verified,false); assert.equal(receiptState(r).failed,true);
  }
});
test('does not select successful validator instead of failed leader',()=>{
  const r=receipt('ERROR');r.consensus_data.leader_receipt.push({mode:'validator',execution_result:'SUCCESS'});
  assert.equal(receiptState(r).verified,false);
});
test('returned ID comes from exact transaction return, never global counter',()=>{
  const r=receipt();r.aggregate_counter=999;
  assert.equal(returnedId(r),7);
  assert.throws(()=>returnedId(receipt('SUCCESS','MAJORITY_AGREE',null)));
});
test('create round readback owner/title/state is validated',()=>{
  const r=state({tasks:[{requirement:'review'}],invites:[account]});const args=['Round','[{"requirement":"review"}]',JSON.stringify([account])];
  assert.doesNotThrow(()=>assertReconciled(r,'create_round',args,account));
  assert.throws(()=>assertReconciled(state({owner:'other'}),'create_round',args,account));
  assert.throws(()=>assertReconciled({...r,round:{...r.round,tasks:[]}},'create_round',args,account));
  assert.throws(()=>assertReconciled({...r,round:{...r.round,invites:[]}},'create_round',args,account));
});

test('incomplete finalized receipt stays pending, never unlocks duplicate signing',()=>{
  for(const r of [{status_name:'FINALIZED'}, {status_name:'FINALIZED',result_name:'MAJORITY_AGREE'},receipt('UNKNOWN')]){
    assert.equal(receiptState(r).verified,false);assert.equal(receiptState(r).failed,false);
  }
});

test('round selection rejects invalid, zero, negative, fractional and unsafe IDs',()=>{
  assert.equal(parseRoundId(''),0);assert.equal(parseRoundId('7'),7);
  for(const x of ['0','-1','NaN','1.5','1e2',' 1','01','9007199254740993'])assert.throws(()=>parseRoundId(x));
});

test('snapshot rejects cross-round, foreign assignee, wrong digest and capacity overflow',()=>{
  const r=state({tasks:[{},{}],reviewers:[{wallet:account,capacity:1}],round_digest:'d',allocation:[{assignment_id:22,task:0,reviewer:0}]},[{id:22,round_id:7,task_index:0,assignee:account,round_digest:'d',state:'ASSIGNED'}]);
  assert.doesNotThrow(()=>assertSnapshot(r,7));
  for(const delta of [{round_id:8},{id:23},{task_index:1},{assignee:'other'},{round_digest:'stale'}])assert.throws(()=>assertSnapshot({...r,assignments:[{...r.assignments[0],...delta}]},7));
  for(const state of ['CLOSED','CANCELLED'])assert.throws(()=>assertSnapshot({...r,round:{...r.round,state}},7));
  const second={...r.assignments[0],id:23,task_index:1};
  assert.throws(()=>assertSnapshot({...r,round:{...r.round,allocation:[...r.round.allocation,{assignment_id:23,task:1,reviewer:0}]},assignments:[...r.assignments,second]},7));
});
test('stale selection and mismatched digest cannot appear successful',()=>{
  assert.throws(()=>assertReconciled(state(),'freeze_round',[8],account));
  assert.throws(()=>assertReconciled(state({state:'FROZEN',consents:[account]}),'consent_round',[7,'stale'],account));
});
test('unresolved allocation is reconciled but never an assignment success',()=>{
  const r=state({state:'UNRESOLVED',attempts:1});
  assert.doesNotThrow(()=>assertReconciled(r,'allocate_round',[7,'digest'],account,{attempts:0}));
  assert.throws(()=>assertReconciled(r,'allocate_round',[7,'digest'],account,{attempts:1}));
});
test('assignment write checks exact ID round digest actor and note',()=>{
  const a={id:22,round_id:7,assignee:account,round_digest:'digest',state:'SUBMITTED',review:'note'};
  assert.doesNotThrow(()=>assertReconciled(state({state:'ALLOCATED'},[a]),'update_assignment',[22,'digest','SUBMIT','note'],account));
  assert.throws(()=>assertReconciled(state({state:'ALLOCATED'},[a]),'update_assignment',[23,'digest','SUBMIT','note'],account));
  assert.throws(()=>assertReconciled(state({state:'ALLOCATED'},[a]),'update_assignment',[22,'digest','SUBMIT','other'],account));
});
test('cancellation must invalidate every unfinished assignment',()=>{
  assert.doesNotThrow(()=>assertReconciled(state({state:'CANCELLED'},[{state:'CANCELLED'}]),'cancel_round',[7,'digest'],account));
  assert.throws(()=>assertReconciled(state({state:'CANCELLED'},[{state:'ACCEPTED'}]),'cancel_round',[7,'digest'],account));
});
