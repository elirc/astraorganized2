from pathlib import Path
s=Path('astra-remaining-improvements/stage/b415b13a50ee')
p=s/'extension/model.js';t=p.read_text(encoding='utf-8').replace('validateSettings(data.settings || {})','validateSettings(data.settings ?? {})').replace('validatePresets(data.presets || [])','validatePresets(data.presets ?? [])').replace('const current = normalize(snapshot); plain(message,',"if (!Number.isFinite(now) || now < 0) throw new Error('Invalid clock value.');\n  const current = normalize(snapshot); plain(message,");p.write_text(t,encoding='utf-8')
p=s/'extension/background.js';p.write_text(r'''
import { normalize, applyMessage } from './model.js';
const alarmName = 'interlude-timer';
let queue = Promise.resolve();
const serial = task => { const result = queue.then(task); queue = result.catch(error => console.error(error.message)); return result; };
async function read() { return normalize(await chrome.storage.local.get(['settings','state','revision','presets'])); }
async function reconcile(snapshot) {
  const state = { ...snapshot.state };
  const desired = state.running ? Math.max(Date.now()+500,state.deadline) : null;
  const existing = chrome.alarms.get ? await chrome.alarms.get(alarmName) : null;
  if (desired === null) { if (existing || !chrome.alarms.get) await chrome.alarms.clear(alarmName); }
  else if (!existing || Math.abs(existing.scheduledTime-desired)>500) { await chrome.alarms.clear(alarmName); await chrome.alarms.create(alarmName,{when:desired}); }
  if (state.phase === 'break') {
    const live = state.breakWindow !== null && await chrome.windows.get(state.breakWindow).catch(()=>null);
    if (!live) {
      const win = await chrome.windows.create({url:chrome.runtime.getURL('index.html?break=1'),type:'popup',state:snapshot.settings.fullscreen?'fullscreen':'maximized',focused:true});
      state.breakWindow = win.id;
      try { await chrome.storage.local.set({state}); }
      catch (error) { await chrome.windows.remove(win.id).catch(()=>{}); throw error; }
    }
  } else if (state.breakWindow !== null) {
    const id = state.breakWindow; const live = await chrome.windows.get(id).catch(()=>null);
    if (live) await chrome.windows.remove(id);
    state.breakWindow = null; await chrome.storage.local.set({state});
  }
  return read();
}
async function synchronize(next, previous) {
  if (next.state.phase==='break' && previous.state.phase!=='break' && next.settings.shuffle) {
    const choices=['lilies','river','garden'].filter(id=>id!==next.settings.art);
    next.settings={...next.settings,art:choices[Math.floor(Math.random()*choices.length)]};next.revision++;
  }
  // One storage call accepts the state and metadata together before external alarm/window effects.
  const accepted=normalize(next);await chrome.storage.local.set(accepted);
  try { return await reconcile(accepted); }
  catch { return {...await read(),warning:'Timer data was saved, but an alarm or break window could not be synchronized. Reopen Interlude to retry.'}; }
}
async function handle(message) {
  const snapshot=await read();
  if(message.type==='read') {
    try { return await reconcile(snapshot); }
    catch { return {...snapshot,warning:'Saved timer loaded, but an alarm or break window still needs repair.'}; }
  }
  return synchronize(applyMessage(snapshot,message),snapshot);
}
chrome.runtime.onMessage.addListener((message,sender,reply)=>{
  if(sender.id!==chrome.runtime.id)return false;
  serial(()=>handle(message)).then(reply,error=>reply({error:error.message}));return true;
});
chrome.alarms.onAlarm.addListener(alarm=>{if(alarm.name===alarmName)serial(()=>handle({type:'command',command:'elapsed'}));});
chrome.windows.onRemoved.addListener(id=>serial(async()=>{const snapshot=await read();if(snapshot.state.breakWindow===id && snapshot.state.phase==='break')await handle({type:'command',command:'finish'});}));
const restore=()=>handle({type:'command',command:'elapsed'});
chrome.runtime.onStartup.addListener(()=>serial(restore));
chrome.runtime.onInstalled.addListener(()=>serial(restore));
chrome.action.onClicked.addListener(()=>chrome.runtime.openOptionsPage());
'''.strip()+'\n',encoding='utf-8');print('Worker now validates snapshots, merges revision-checked commands and reconciles saved effects')
