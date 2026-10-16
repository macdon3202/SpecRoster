import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';
import { supportedVersion, isAddress, normalizeHash, normalizeReadback, receiptState, sameAddress, assertSnapshot } from './transactions.js';
export const EXPLORER = 'https://explorer-studio.genlayer.com';
export const reader = () => createClient({chain:studionet});
export function providers() {
  return [...new Set([...(window.ethereum?.providers || []),window.ethereum].filter(p=>typeof p?.request==='function'))];
}
export async function connect(provider) {
  if (!provider) throw new Error('Choose an installed EIP-1193 wallet.');
  const accounts = await provider.request({method:'eth_requestAccounts'});
  if (!isAddress(accounts?.[0])) throw new Error('Wallet did not return an account.');
  const chainId = `0x${studionet.id.toString(16)}`;
  if (BigInt(await provider.request({method:'eth_chainId'})) !== BigInt(studionet.id)) {
    try { await provider.request({method:'wallet_switchEthereumChain',params:[{chainId}]}); }
    catch(e) {
      if (Number(e.code ?? e.data?.originalError?.code)!==4902) throw e;
      await provider.request({method:'wallet_addEthereumChain',params:[{chainId,chainName:studionet.name,nativeCurrency:studionet.nativeCurrency,rpcUrls:studionet.rpcUrls.default.http,blockExplorerUrls:[EXPLORER]}]});
      await provider.request({method:'wallet_switchEthereumChain',params:[{chainId}]});
    }
  }
  if (BigInt(await provider.request({method:'eth_chainId'}))!==BigInt(studionet.id)) throw new Error('Switch to StudioNet.');
  const current=await provider.request({method:'eth_accounts'});
  if(!sameAddress(current?.[0],accounts[0])) throw new Error('Wallet changed during connection. Reconnect.');
  return {account:accounts[0],provider,client:createClient({chain:studionet,account:accounts[0],provider})};
}
export async function read(address, method, args=[]) {
  if (!isAddress(address)) throw new Error('Enter a deployed SpecRoster address.');
  return normalizeReadback(await reader().readContract({address,functionName:method,args}));
}
export async function refreshWallet(provider) {
  const accounts=await provider.request({method:'eth_accounts'});
  if(!isAddress(accounts?.[0])) throw new Error('Wallet disconnected.');
  if(BigInt(await provider.request({method:'eth_chainId'}))!==BigInt(studionet.id)) throw new Error('Switch to StudioNet and reconnect.');
  return {account:accounts[0],provider,client:createClient({chain:studionet,account:accounts[0],provider})};
}
export async function snapshot(address,id) {
  const config=await read(address,'get_config');
  if(!supportedVersion(config.version)) throw new Error('This is not a supported SpecRoster deployment.');
  if(!id) return {config,round:null,assignments:[]};
  const round=await read(address,'get_round',[id]);
  if(Number(round.id)!==id) throw new Error('Round ID mismatch.');
  const assignments=await Promise.all(round.allocation.map(x=>read(address,'get_assignment',[x.assignment_id])));
  const result={config,round,assignments};assertSnapshot(result,id);return result;
}
export async function send(wallet,address,method,args) {
  const accounts=await wallet.provider.request({method:'eth_accounts'});
  if(!sameAddress(accounts?.[0],wallet.account)) throw new Error('Account changed. Reconnect before signing.');
  if(BigInt(await wallet.provider.request({method:'eth_chainId'}))!==BigInt(studionet.id)) throw new Error('Switch to StudioNet before signing.');
  const cfg=await read(address,'get_config');
  if(!supportedVersion(cfg.version)) throw new Error('Contract version mismatch.');
  return normalizeHash(await wallet.client.writeContract({address,functionName:method,args,value:0n}));
}
export async function finalize(hash,onStatus=()=>{}) {
  for(let i=0;i<160;i++) {
    let tx;
    try { tx=await reader().getTransaction({hash}); }
    catch { onStatus('RPC interrupted · checking the same hash'); await new Promise(r=>setTimeout(r,3000)); continue; }
    const state=receiptState(tx);
    onStatus(state.finalized?'Finalized · reconciling':'Validator consensus pending');
    if(state.failed) {
      const error=new Error(`Finalized without successful execution: ${state.consensus} / ${state.execution}`);
      error.finalizedFailure=true;
      throw error;
    }
    if(state.verified) return tx;
    await new Promise(r=>setTimeout(r,3000));
  }
  throw new Error('Still pending. Use Reconcile; do not resubmit.');
}
