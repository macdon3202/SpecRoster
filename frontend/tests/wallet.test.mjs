import test from 'node:test';
import assert from 'node:assert/strict';
import {connect} from '../src/client.js';
import {studionet} from 'genlayer-js/chains';
const account='0x'+'11'.repeat(20);
function provider({wrong=false,changed=false,reject=false}={}) {
  const calls=[];let chain=wrong?'0x1':`0x${studionet.id.toString(16)}`;
  return {calls,async request({method}){
    calls.push(method);
    if(method==='eth_requestAccounts')return [account];
    if(method==='eth_accounts')return [changed?'0x'+'22'.repeat(20):account];
    if(method==='eth_chainId')return chain;
    if(method==='wallet_switchEthereumChain'){if(reject)throw Object.assign(Error('Rejected'),{code:4001});chain=`0x${studionet.id.toString(16)}`;return null;}
    throw Error('Unexpected wallet method '+method);
  }};
}
test('connect uses selected EIP1193 provider without any Snap method',async()=>{
  const p=provider();const w=await connect(p);
  assert.equal(w.provider,p);assert.equal(w.account,account);
  assert(!p.calls.some(x=>x.includes('Snap')||x.includes('snap')));
});
test('wallet switches wrong chain and rechecks it',async()=>{
  const p=provider({wrong:true});await connect(p);assert(p.calls.includes('wallet_switchEthereumChain'));
});
test('user rejection and account changes invalidate connection',async()=>{
  await assert.rejects(connect(provider({wrong:true,reject:true})),/Rejected/);
  await assert.rejects(connect(provider({changed:true})),/changed/);
  await assert.rejects(connect(null),/Choose/);
});
