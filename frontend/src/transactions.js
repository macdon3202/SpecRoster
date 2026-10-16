export const VERSION = 'SPEC_ROSTER_V1';
export const supportedVersion = x => ['SPEC_ROSTER_V1','SPEC_ROSTER_V2','SPEC_ROSTER_V3','SPEC_ROSTER_V4_CANDIDATE'].includes(x);
export function parseRoundId(value) {
  if(value==='')return 0;
  if(!/^[1-9][0-9]*$/.test(String(value)) || !Number.isSafeInteger(Number(value)))throw new Error('Enter a positive round ID.');
  return Number(value);
}
export const stableJSON=value=>JSON.stringify(value,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,v[k]])):v);
export const isAddress = x => typeof x === 'string' && /^0x[0-9a-f]{40}$/i.test(x) && !/^0x0{40}$/i.test(x);
export const sameAddress = (a,b) => typeof a === 'string' && typeof b === 'string' && a.toLowerCase() === b.toLowerCase();
export function normalizeReadback(value) {
  if(typeof value==='bigint') {
    const n=Number(value);
    if(!Number.isSafeInteger(n))throw new Error('Contract integer exceeds safe UI bounds.');
    return n;
  }
  if(Array.isArray(value))return value.map(normalizeReadback);
  if(value instanceof Map)return Object.fromEntries([...value].map(([k,v])=>[k,normalizeReadback(v)]));
  if(value && typeof value==='object')return Object.fromEntries(Object.entries(value).map(([k,v])=>[k,normalizeReadback(v)]));
  return value;
}
export function normalizeHash(x) {
  const hash = typeof x === 'string' ? x : x?.txId ?? x?.hash;
  if (!/^0x[0-9a-f]{64}$/i.test(hash || '')) throw new Error('No valid transaction hash was returned.');
  return hash;
}
export function pendingFor(journal,address,account) {
  return journal.some(e=>e.state==='PENDING' && sameAddress(e.address,address) && sameAddress(e.account,account));
}
export function receiptState(tx) {
  const finalized = tx?.status_name === 'FINALIZED' || tx?.statusName === 'FINALIZED' || tx?.status === 'FINALIZED' || tx?.status === 7;
  const consensus = tx?.result_name ?? tx?.consensus_result_name ?? tx?.consensus_result ?? 'UNKNOWN';
  const data = tx?.consensus_data ?? {};
  let receipts = data.leader_receipt ?? data.validators ?? [];
  if (!Array.isArray(receipts)) receipts = [receipts];
  const leader = receipts.find(x => x.mode === 'leader');
  const execution = leader?.execution_result ?? leader?.genvm_result?.execution_result ?? 'UNKNOWN';
  const readable = leader?.result?.payload?.readable ?? leader?.result?.readable;
  const agree = consensus === 'MAJORITY_AGREE';
  const knownFailure=['ERROR','REVERT','FAILURE'].includes(execution) || ['MAJORITY_DISAGREE','NO_MAJORITY','UNDETERMINED'].includes(consensus);
  return { finalized, consensus, execution, readable, verified:finalized && agree && execution === 'SUCCESS', failed:finalized && knownFailure };
}
export function returnedId(receipt) {
  const x = receiptState(receipt).readable;
  let value = x;
  if (typeof value === 'string') { try { value = JSON.parse(value); } catch { throw new Error('Returned ID could not be decoded.'); } }
  if (!Number.isSafeInteger(value) || value < 1) throw new Error('Exact returned ID is unavailable. Reconcile the transaction before continuing.');
  return value;
}
export function assertReconciled({round, config, assignments}, method, args, account, before) {
  if (method === 'create_round') {
    if (!round || !sameAddress(round.owner,account) || round.state !== 'OPEN' || round.title !== args[0]) throw new Error('Created round readback does not match.');
    const tasks=JSON.parse(args[1]), invites=JSON.parse(args[2]).map(w=>w.toLowerCase()).sort();
    if(stableJSON(round.tasks)!==stableJSON(tasks) || stableJSON(round.invites.map(w=>w.toLowerCase()).sort())!==stableJSON(invites))throw new Error('Created task/invite bundle readback mismatch.');
  } else if (!round || round.id !== Number(args[0]) && !['update_assignment'].includes(method)) throw new Error('Selected round does not match readback.');
  if (method === 'register_scope' && !round.reviewers.some(r=>sameAddress(r.wallet,account) && r.scope === args[1] && r.capacity === args[2])) throw new Error('Scope readback mismatch.');
  if (method === 'freeze_round' && (round.state !== 'FROZEN' || !round.round_digest)) throw new Error('Freeze readback mismatch.');
  if (method === 'consent_round' && (round.round_digest !== args[1] || !round.consents.some(w=>sameAddress(w,account)))) throw new Error('Consent readback mismatch.');
  if (method === 'allocate_round' && (round.round_digest !== args[1] || !['ALLOCATED','UNRESOLVED'].includes(round.state) || round.attempts !== before.attempts+1)) throw new Error('Allocation readback mismatch.');
  if (method === 'update_assignment') {
    const a = assignments.find(x=>x.id===args[0]);
    const expected = {ACCEPT:'ACCEPTED', DECLINE:'DECLINED', SUBMIT:'SUBMITTED'}[args[2]];
    if (!a || a.round_id!==round.id || a.state!==expected || a.round_digest!==args[1] || !sameAddress(a.assignee,account) || args[2]==='SUBMIT' && a.review!==args[3]) throw new Error('Assignment readback mismatch.');
  }
  if (method === 'close_round' && !['CANCELLED','CLOSED'].includes(round.state)) throw new Error('Close readback mismatch.');
  if (method === 'cancel_round' && (round.state!=='CANCELLED' || round.round_digest!==args[1] || assignments.some(a=>['ASSIGNED','ACCEPTED'].includes(a.state)))) throw new Error('Cancellation readback mismatch.');
  if (!supportedVersion(config.version)) throw new Error('Unexpected contract version.');
}

export function assertSnapshot({config,round,assignments},id) {
  if(!supportedVersion(config.version))throw new Error('Unsupported contract version.');
  if(!round || round.id!==id)throw new Error('Round ID mismatch.');
  if(round.allocation.length!==assignments.length)throw new Error('Allocation readback incomplete.');
  const ids=new Set(), tasks=new Set(),used=new Map();
  for(let i=0;i<assignments.length;i++){
    const a=assignments[i], link=round.allocation[i], reviewer=round.reviewers[link.reviewer];
    if(ids.has(a.id)||tasks.has(a.task_index)||a.id!==link.assignment_id||a.round_id!==id||a.task_index!==link.task||!round.tasks[a.task_index]||!reviewer||!sameAddress(a.assignee,reviewer.wallet)||a.round_digest!==round.round_digest)throw new Error('Assignment identity readback mismatch.');
    ids.add(a.id);tasks.add(a.task_index);used.set(link.reviewer,(used.get(link.reviewer)||0)+1);
    if(used.get(link.reviewer)>reviewer.capacity)throw new Error('Capacity readback mismatch.');
    if(round.state==='CANCELLED'&&['ASSIGNED','ACCEPTED'].includes(a.state))throw new Error('Cancelled work is still active.');
    if(round.state==='CLOSED'&&!['SUBMITTED','DECLINED'].includes(a.state))throw new Error('Closed work is still active.');
  }
}
