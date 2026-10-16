// Opt-in read-only check. Not a browser-wallet signing E2E.
import assert from 'node:assert/strict';
import {snapshot} from '../src/client.js';
const address=process.argv[2];
const id=Number(process.argv[3]);
const data=await snapshot(address,id);
assert.equal(data.round.id,id);
assert.equal(data.config.deployer_authority,'NONE');
assert.equal(data.round.allocation.length,data.assignments.length);
for(const a of data.assignments){
  assert.equal(a.round_id,id);
  assert.equal(a.round_digest,data.round.round_digest);
}
if(data.round.state==='CANCELLED')assert.ok(data.assignments.every(a=>!['ASSIGNED','ACCEPTED'].includes(a.state)));
console.log(JSON.stringify({check:'FRONTEND_SDK_READ_ONLY',signed_browser_e2e:false,address,...data},null,2));
