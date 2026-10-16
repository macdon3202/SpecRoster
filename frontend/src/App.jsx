import React,{useState,useEffect,useRef} from 'react';
import {connect,refreshWallet,providers,snapshot,send,finalize,EXPLORER} from './client.js';
import {isAddress,sameAddress,returnedId,assertReconciled,pendingFor,parseRoundId} from './transactions.js';

const short=x=>x?`${x.slice(0,6)}…${x.slice(-4)}`:'Not connected';
const roles=['Intake','Consent','Matching','Work queue'];
const initialAddress=()=>localStorage.getItem('specroster.address')||import.meta.env.VITE_CONTRACT_ADDRESS||'';
function Tag({children}){return <span className={`tag ${String(children).toLowerCase()}`}>{children}</span>}
function Field({label,children}){return <label className="field"><span>{label}</span>{children}</label>}

export default function App(){
  const [address,setAddress]=useState(initialAddress),[selected,setSelected]=useState(''),[data,setData]=useState(null);
  const [wallet,setWallet]=useState(null),[providerIndex,setProviderIndex]=useState(0),[available,setAvailable]=useState([]);
  const [sample,setSample]=useState(null),[title,setTitle]=useState('Wallet standards review sprint'),[tasks,setTasks]=useState('[]'),[invites,setInvites]=useState('');
  const [scope,setScope]=useState(''),[capacity,setCapacity]=useState(1),[reviews,setReviews]=useState({});
  const [busy,setBusy]=useState(false),[notice,setNotice]=useState('Connect your wallet and configure a deployment to start.'),[error,setError]=useState('');
  const [journal,setJournal]=useState(()=>{try{return JSON.parse(localStorage.getItem('specroster.journal')||'[]')}catch{return []}});
  const generation=useRef(0),[now,setNow]=useState('');
  const round=data?.round, config=data?.config;
  const owner=round&&sameAddress(round.owner,wallet?.account);
  const member=round?.reviewers.find(x=>sameAddress(x.wallet,wallet?.account));
  const consented=round?.consents.some(x=>sameAddress(x,wallet?.account));
  const allConsent=round?.reviewers.length>0&&round.consents.length===round.reviewers.length;
  useEffect(()=>{setAvailable(providers());fetch('/public-round.json').then(r=>r.json()).then(s=>{setSample(s);setTasks(JSON.stringify(s.tasks,null,2));setScope(s.reviewer_scope)}).catch(()=>setError('Public sample failed to load.'));},[]);
  useEffect(()=>{localStorage.setItem('specroster.journal',JSON.stringify([...journal.filter(e=>e.state==='PENDING'),...journal.filter(e=>e.state!=='PENDING').slice(-30)]))},[journal]);
  useEffect(()=>{
    const provider=wallet?.provider;
    if(!provider?.on)return;
    const changed=async()=>{
      const token=++generation.current;setWallet(null);setData(null);setError('');setNotice('Wallet changed · reloading role and state.');
      try{const current=await refreshWallet(provider);if(token!==generation.current)return;setWallet(current);if(isAddress(address)){const fresh=await snapshot(address,selected?Number(selected):0);if(token!==generation.current)return;setData(fresh);setNow(new Date().toLocaleTimeString())}setNotice('Wallet role and authoritative state refreshed.');}
      catch(e){if(token===generation.current)setError(e.message)}
    };
    provider.on('accountsChanged',changed);provider.on('chainChanged',changed);
    return()=>{provider.removeListener?.('accountsChanged',changed);provider.removeListener?.('chainChanged',changed)};
  },[wallet,address,selected]);
  function invalidate(){generation.current++;setData(null);setError('');setNow('')}
  async function sync(){
    setBusy(true);setError('');const token=generation.current;
    try{const id=parseRoundId(selected);const fresh=await snapshot(address,id);if(token!==generation.current)return;setData(fresh);localStorage.setItem('specroster.address',address);setNow(new Date().toLocaleTimeString());setNotice('Authoritative state synchronized.');}
    catch(e){if(token===generation.current){setData(null);setError(e.message)}}finally{setBusy(false)}
  }
  async function connectWallet(){setError('');setBusy(true);try{const w=await connect(available[providerIndex]);generation.current++;setWallet(w);setData(null);setNotice('Wallet connected. Sync the deployment to load your role.')}catch(e){setError(e.message)}finally{setBusy(false)}}
  async function finish(entry,receipt,token){
    let id=entry.method==='create_round'?returnedId(receipt):entry.roundId;
    const fresh=await snapshot(entry.address,id);
    if(token!==generation.current)throw Error('Selection or wallet changed. Reconcile this transaction in its original context.');
    assertReconciled(fresh,entry.method,entry.args,entry.account,entry.before);
    setSelected(String(id));setData(fresh);setNow(new Date().toLocaleTimeString());
    setJournal(prev=>prev.map(e=>e.hash===entry.hash?{...e,state:'RECONCILED',roundId:id}:e));
    setNotice(fresh.round.state==='UNRESOLVED'?'Finalized: unresolved evidence. No assignments were created.':`Finalized and reconciled · ${fresh.round.state}`);
  }
  async function act(method,args){
    if(!wallet||!config||busy)return;
    if(pendingFor(journal,address,wallet.account)){setError('Reconcile the pending transaction before signing another write.');return;}
    setBusy(true);setError('');const token=generation.current;
    let hash;
    try{
      hash=await send(wallet,address,method,args);
      const entry={hash,method,args,address,account:wallet.account,roundId:round?.id||0,before:round?{attempts:round.attempts}:null,state:'PENDING'};
      setJournal(prev=>[...prev,entry]);
      const receipt=await finalize(hash,status=>{if(token===generation.current)setNotice(status)});
      await finish(entry,receipt,token);
    }catch(e){if(e.finalizedFailure&&hash)setJournal(prev=>prev.map(x=>x.hash===hash?{...x,state:'FAILED'}:x));setError(e.message);setNotice('Write not reconciled. Inspect the transaction journal.')}finally{setBusy(false)}
  }
  async function reconcile(entry){
    if(!wallet||busy)return;
    if(!sameAddress(wallet.account,entry.account)||entry.address.toLowerCase()!==address.toLowerCase()){setError('Connect the original account and deployment before reconciling.');return;}
    setBusy(true);setError('');const token=generation.current;
    try{const receipt=await finalize(entry.hash,setNotice);await finish(entry,receipt,token)}catch(e){if(e.finalizedFailure)setJournal(prev=>prev.map(x=>x.hash===entry.hash?{...x,state:'FAILED'}:x));setError(e.message)}finally{setBusy(false)}
  }
  const phase=!round||round.state==='OPEN'?0:round.state==='FROZEN'&&!allConsent?1:['FROZEN','UNRESOLVED'].includes(round.state)?2:3;
  const canWrite=!!wallet&&!!config&&!busy&&!pendingFor(journal,address,wallet?.account);
  return <div className="app-shell">
    <header className="topbar"><a className="brand" href="#"><img src="/logo.png" alt="SpecRoster routing logo"/><span>SpecRoster<small>ETHEREUM REVIEW WORKBENCH</small></span></a><div className="top-actions"><span className="network"><i/>StudioNet</span>{available.length>1&&<select aria-label="Choose wallet" value={providerIndex} onChange={e=>setProviderIndex(Number(e.target.value))}>{available.map((p,i)=><option key={i} value={i}>{p.isMetaMask?'MetaMask':p.isRabby?'Rabby':`Wallet ${i+1}`}</option>)}</select>}<button className="wallet" disabled={busy} onClick={connectWallet}>{wallet?short(wallet.account):'Connect wallet'} <span>↗</span></button></div></header>
    <main>
      <section className="intro"><div><div className="eyebrow"><span className="tiny-lines">▤</span> A BETTER FIT FOR EVERY REVIEW</div><h1>Good work.<br/><em>The right reviewer.</em></h1><p>Turn Ethereum standards into a focused review queue.<br/>Agree on scope. Match thoughtfully. Keep ownership clear.</p></div><div className="intro-graphic" aria-hidden="true"><img src="/logo.png"/><span className="graphic-label">TASKS → SCOPE → PEOPLE</span></div></section>
      <section className="connection panel"><div className="section-cap"><span>01 / WORKSPACE</span><span className="sync-state">{now?`Synced ${now}`:'No deployment synced'}</span></div><div className="connection-grid"><Field label="Active contract"><input placeholder="0x… deployed SpecRoster address" value={address} disabled={busy} onChange={e=>{setAddress(e.target.value);invalidate()}}/></Field><Field label="Round ID"><input inputMode="numeric" placeholder="New round" value={selected} disabled={busy} onChange={e=>{setSelected(e.target.value);invalidate()}}/></Field><button className="secondary sync" disabled={busy||!isAddress(address)} onClick={sync}>{busy?'Working…':'Sync workspace ↻'}</button></div><div className="connection-foot"><span>Contract is the source of truth · no funds held</span>{isAddress(address)&&<a href={`${EXPLORER}/address/${address}`} target="_blank" rel="noreferrer">View deployment ↗</a>}<button className="text-button" disabled={busy} onClick={()=>{setSelected('');invalidate()}}>Create a new round</button></div></section>
      <div className="feedback" role="status" aria-live="polite"><span className={error?'signal error':'signal'}/><span>{error||notice}</span></div>
      <div className="workspace-heading"><div><div className="eyebrow">REVIEW OPERATIONS</div><h2>{round?round.title:'Your next review round'}</h2></div>{round&&<Tag>{round.state}</Tag>}</div>
      <nav className="steps" aria-label="Round workflow">{roles.map((label,i)=><div key={label} className={phase===i?'step active':'step'}><span>0{i+1}</span>{label}<b>{i===phase?'●':'—'}</b></div>)}</nav>
      {!round?<section className="new-round-layout"><div className="panel create-panel"><div className="section-cap"><span>START WITH THE WORK</span><span>Up to 4 tasks</span></div><h3>Make room for focused review.</h3><p className="muted">Invite reviewer wallets, attach exact standard revisions, and describe the review tasks.</p><Field label="Round name"><input value={title} onChange={e=>setTitle(e.target.value)} maxLength={120}/></Field><Field label="Invited reviewer wallets"><textarea rows={2} placeholder="0x… one address per line. Use a different wallet from the creator." value={invites} onChange={e=>setInvites(e.target.value)}/></Field><details><summary>Review source-bound task bundle <span>↗</span></summary><Field label="Task JSON · full commit and SHA-256 required"><textarea className="code-input" rows={12} value={tasks} onChange={e=>setTasks(e.target.value)}/></Field></details><button className="primary" disabled={!canWrite} onClick={()=>{try{const parsed=JSON.parse(tasks);if(!Array.isArray(parsed)||parsed.length<1||parsed.length>4)throw Error('Use one to four tasks.');const invited=invites.split(/[\n,]+/).map(x=>x.trim()).filter(Boolean);if(invited.length<1||invited.length>4||invited.some(x=>!isAddress(x)))throw Error('Enter one to four valid reviewer wallets.');act('create_round',[title,JSON.stringify(parsed),JSON.stringify(invited)])}catch(e){setError(e.message)}}}>Create review round <span>→</span></button></div><aside className="how-panel"><span className="index-chip">THE PROCESS</span><h3>Clear scope.<br/>Shared consent.<br/>Real assignments.</h3><ol><li><b>Define the round</b><p>Source-bound tasks, invited people, and each person's capacity.</p></li><li><b>Agree before matching</b><p>Reviewers consent to the exact frozen task and scope bundle.</p></li><li><b>Put the match to work</b><p>Only the assigned wallet can accept and submit its review.</p></li></ol><div className="footnote">Matching routes work. It does not certify expertise or the quality of a submitted review.</div></aside></section>:
      <>
        <div className="work-grid"><section className="panel tasks-panel"><div className="section-cap"><span>THE TASK BOARD</span><span>{round.tasks.length} / 4 tasks</span></div>{round.tasks.map((task,i)=><article className="task" key={i}><div className="task-number">{String(i+1).padStart(2,'0')}</div><div><span className="source-label">EIP-{task.eip} <span>· {task.commit.slice(0,8)}</span></span><h3>{task.title}</h3><p>{task.requirement}</p><a href={`https://raw.githubusercontent.com/ethereum/EIPs/${task.commit}/EIPS/eip-${task.eip}.md`} target="_blank" rel="noreferrer">Exact standard revision ↗</a><details><summary>Source commitment</summary><code>{task.digest}</code></details></div></article>)}</section>
        <aside className="panel roster-panel"><div className="section-cap"><span>THE PEOPLE</span><span>{round.reviewers.length} joined</span></div>{round.reviewers.length===0&&<p className="empty">Waiting for an invited reviewer to register scope.</p>}{round.reviewers.map((r,i)=><article className="reviewer" key={r.wallet}><div className={`avatar color-${i}`}>{i+1}</div><div><b>{short(r.wallet)} {sameAddress(r.wallet,wallet?.account)&&<small>You</small>}</b><p>{r.scope}</p><span className="meta">Capacity {r.capacity} · {round.consents.includes(r.wallet)?'Consented':'Awaiting consent'}</span></div></article>)}
        {round.state==='OPEN'&&!member&&round.invites.some(w=>sameAddress(w,wallet?.account))&&<div className="action-form"><h3>Where do you fit?</h3><Field label="Review scope and exclusions"><textarea rows={4} value={scope} onChange={e=>setScope(e.target.value)}/></Field><Field label="Capacity in this round"><select value={capacity} onChange={e=>setCapacity(Number(e.target.value))}>{[1,2,3,4].map(n=><option key={n}>{n}</option>)}</select></Field><button className="primary" disabled={!canWrite} onClick={()=>act('register_scope',[round.id,scope,capacity])}>Register my scope →</button></div>}
        {owner&&round.state==='OPEN'&&<button className="primary" disabled={!canWrite||!round.reviewers.length} onClick={()=>act('freeze_round',[round.id])}>Freeze this round →</button>}
        {member&&!consented&&round.state==='FROZEN'&&<div className="consent-box"><h3>Review before agreeing.</h3><p>Your consent binds these tasks, sources, scopes and capacities. They cannot change within this round.</p><code>{round.round_digest}</code><button className="primary" disabled={!canWrite} onClick={()=>act('consent_round',[round.id,round.round_digest])}>Consent to this exact round →</button></div>}
        {['FROZEN','UNRESOLVED'].includes(round.state)&&allConsent&&<div className="action-form"><p>All reviewers consented. Matching uses the frozen bundle. Attempts: {round.attempts} / 2.</p><button className="primary" disabled={!canWrite||round.attempts>=2} onClick={()=>act('allocate_round',[round.id,round.round_digest])}>Run semantic matching →</button></div>}
        </aside></div>
        {round.matrix.length>0&&<section className="panel matrix-panel"><div className="section-cap"><span>THE MATCH MATRIX</span><span>Capacity enforced by contract</span></div><div className="table-wrap"><table><thead><tr><th>Task</th>{round.reviewers.map(r=><th key={r.wallet}>{short(r.wallet)}</th>)}</tr></thead><tbody>{round.matrix.map((row,i)=><tr key={i}><td>{round.tasks[i].title}</td>{row.map((cell,j)=><td key={j}><Tag>{cell}</Tag></td>)}</tr>)}</tbody></table></div></section>}
        <section className="panel queue-panel"><div className="section-cap"><span>THE WORK QUEUE</span><span>{data.assignments.length} assignments</span></div>{data.assignments.length===0?<p className="empty">No assignments recorded. Unresolved evidence never reserves a work slot.</p>:data.assignments.map(a=><article className="assignment" key={a.id}><div className="assignment-top"><div><span className="source-label">ASSIGNMENT #{a.id} · {short(a.assignee)}</span><h3>{round.tasks[a.task_index].title}</h3></div><Tag>{a.state}</Tag></div>{a.review&&<blockquote>{a.review}</blockquote>}{sameAddress(a.assignee,wallet?.account)&&['ASSIGNED','ACCEPTED'].includes(a.state)&&<div className="assignment-actions">{a.state==='ASSIGNED'?<button className="primary" disabled={!canWrite} onClick={()=>act('update_assignment',[a.id,round.round_digest,'ACCEPT',''])}>Accept assignment →</button>:<><Field label="Submit a review note · no certification implied"><textarea rows={3} value={reviews[a.id]||''} onChange={e=>setReviews({...reviews,[a.id]:e.target.value})}/></Field><button className="primary" disabled={!canWrite||!reviews[a.id]?.trim()} onClick={()=>act('update_assignment',[a.id,round.round_digest,'SUBMIT',reviews[a.id]])}>Submit review →</button></>}<button className="text-button" disabled={!canWrite} onClick={()=>act('update_assignment',[a.id,round.round_digest,'DECLINE',''])}>Decline assignment</button></div>}</article>)}</section>
        {owner&&!['CLOSED','CANCELLED'].includes(round.state)&&<button className="text-button danger" disabled={!canWrite} onClick={()=>act('cancel_round',[round.id,round.round_digest])}>Cancel round and stop unfinished assignments</button>}
        {round.state==='ALLOCATED'&&data.assignments.every(a=>['SUBMITTED','DECLINED'].includes(a.state))&&<button className="secondary" disabled={!canWrite} onClick={()=>act('close_round',[round.id])}>Close completed round →</button>}
      </>}
      <section className="journal"><div className="section-cap"><span>TRANSACTION JOURNAL</span><span>Local history · on-chain confirmation required</span></div>{journal.length===0?<p className="muted">Signed transactions will appear here, with a direct link to Explorer.</p>:journal.slice().reverse().map(e=><div className="journal-row" key={e.hash}><div><b>{e.method.replaceAll('_',' ')}</b><small>{short(e.address)} · {short(e.account)}</small></div><Tag>{e.state}</Tag><a href={`${EXPLORER}/tx/${e.hash}`} target="_blank" rel="noreferrer">{short(e.hash)} ↗</a>{e.state!=='RECONCILED'&&<button className="secondary" disabled={busy||!wallet} onClick={()=>reconcile(e)}>Reconcile</button>}</div>)}</section>
    </main><footer><span className="brand-name">SpecRoster<span> / </span>Standards deserve thoughtful review.</span><span>Scoped work. Explicit consent. Verifiable state.</span></footer>
  </div>
}
