from pathlib import Path
s=Path('astra-remaining-improvements/stage/b415b13a50ee')
p=s/'extension/model.js';p.write_text(r'''
import { defaults, freshState, transition } from './state.js';
const settingKeys = [...Object.keys(defaults), 'customArt', 'customName'];
const commands = new Set(['start','pause','reset','break','snooze','finish','elapsed']);
function plain(value, keys, label) { if (!value || typeof value !== 'object' || Array.isArray(value) || Object.keys(value).some(key => !keys.includes(key))) throw new Error(`Invalid ${label} fields.`); }
function integer(value, min, max, label) { if (!Number.isSafeInteger(value) || value < min || value > max) throw new Error(`Invalid ${label}.`); }
function boundedText(value, max, label, allowEmpty = false) { if (typeof value !== 'string' || value.length > max || (!allowEmpty && !value.trim())) throw new Error(`Invalid ${label}.`); return value; }
export function validateSettings(value) {
  plain(value, settingKeys, 'settings'); const settings = { ...defaults, ...value };
  integer(settings.focus,1,180,'focus duration'); integer(settings.breakMinutes,1,60,'break duration'); boundedText(settings.message,500,'message',true);
  for (const key of ['shuffle','autoResume','fullscreen']) if (typeof settings[key] !== 'boolean') throw new Error(`Invalid ${key} setting.`);
  if (!['lilies','river','garden','custom'].includes(settings.art)) throw new Error('Invalid artwork selection.');
  if (settings.customArt != null && (typeof settings.customArt !== 'string' || settings.customArt.length > 4*1024*1024 || !/^data:image\/(jpeg|png|webp);base64,[A-Za-z0-9+/]+=*$/.test(settings.customArt))) throw new Error('Invalid or oversized custom artwork.');
  if (settings.customName != null) boundedText(settings.customName,70,'artwork name',true);
  if (settings.art === 'custom' && !settings.customArt) throw new Error('Custom artwork is missing.');
  return settings;
}
function validateState(value, settings) {
  const state = value == null ? freshState(settings) : structuredClone(value);
  plain(state,['phase','running','deadline','remaining','total','completed','focusMinutes','day','breakWindow','snoozed'],'timer state');
  if (!['focus','break'].includes(state.phase) || typeof state.running !== 'boolean') throw new Error('Invalid timer phase.');
  for (const key of ['remaining','total','focusMinutes']) if (typeof state[key] !== 'number' || !Number.isFinite(state[key]) || state[key] < 0) throw new Error('Invalid timer duration or statistics.');
  if (state.total <= 0 || state.total > 180*60000 || state.remaining > state.total) throw new Error('Invalid timer interval.');
  if (state.running ? !Number.isFinite(state.deadline) || state.deadline < 0 : state.deadline !== null) throw new Error('Invalid timer deadline.');
  integer(state.completed,0,Number.MAX_SAFE_INTEGER,'completed count'); boundedText(state.day,100,'statistics day');
  if (state.breakWindow !== null) integer(state.breakWindow,0,Number.MAX_SAFE_INTEGER,'break window');
  if (state.snoozed !== undefined && typeof state.snoozed !== 'boolean') throw new Error('Invalid snooze state.');
  return state;
}
function validatePresets(value) {
  if (!Array.isArray(value) || value.length > 30) throw new Error('Use at most 30 saved messages.'); const ids = new Set();
  return value.map(preset => {
    plain(preset,['id','title','message'],'saved message');
    if (typeof preset.id !== 'string' || !/^[a-zA-Z0-9_-]{1,80}$/.test(preset.id) || ids.has(preset.id)) throw new Error('Invalid or duplicate saved-message identity.'); ids.add(preset.id);
    return { id: preset.id, title: boundedText(preset.title,80,'saved-message title').trim(), message: boundedText(preset.message,500,'saved-message text') };
  });
}
export function normalize(data = {}) {
  plain(data,['settings','state','revision','presets'],'stored snapshot'); const settings = validateSettings(data.settings || {});
  const revision = data.revision ?? 0; integer(revision,0,Number.MAX_SAFE_INTEGER,'settings revision');
  return { settings, state: validateState(data.state,settings), revision, presets: validatePresets(data.presets || []) };
}
export function parsePreview(raw) {
  if (raw === null) return normalize();
  if (typeof raw !== 'string' || raw.length > 5*1024*1024) throw new Error('Saved preview data is invalid or too large.');
  let value; try { value = JSON.parse(raw); } catch { throw new Error('Saved preview data is unreadable. Export it before resetting; no data was changed.'); }
  return normalize(value);
}
export function applyMessage(snapshot, message, now = Date.now()) {
  const current = normalize(snapshot); plain(message,['type','command','settings','expectedRevision','action','preset','id'],'message');
  if (message.type === 'read') return current;
  if (message.type === 'command') {
    if (!commands.has(message.command)) throw new Error('Unknown timer command.');
    return { ...current, state: transition(current.state,current.settings,message.command,now) };
  }
  if (!['settings','preset'].includes(message.type)) throw new Error('Unknown message type.');
  if (message.expectedRevision !== current.revision) throw new Error('Settings or saved messages changed elsewhere. Reopen this view before saving; your draft is preserved.');
  if (current.revision >= Number.MAX_SAFE_INTEGER) throw new Error('Settings revision is exhausted. Export for recovery.');
  if (message.type === 'settings') {
    plain(message.settings,settingKeys,'settings patch'); if (!Object.keys(message.settings).length) throw new Error('Settings patch is empty.');
    const settings = validateSettings({ ...current.settings, ...message.settings });
    const state = !current.state.running && current.state.phase === 'focus' ? transition(current.state,settings,'reset',now) : current.state;
    return { ...current, settings, state, revision: current.revision + 1 };
  }
  let presets = structuredClone(current.presets);
  if (message.action === 'create') {
    const [preset] = validatePresets([message.preset]); if (presets.some(p=>p.id===preset.id)) throw new Error('Saved-message identity already exists.'); presets.push(preset);
  } else if (message.action === 'update') {
    const [preset] = validatePresets([message.preset]); if (preset.id !== message.id) throw new Error('Saved-message identity cannot change.');
    if (!presets.some(p=>p.id===message.id)) throw new Error('Saved message not found.'); presets = presets.map(p=>p.id===message.id?preset:p);
  } else if (message.action === 'delete') {
    if (!presets.some(p=>p.id===message.id)) throw new Error('Saved message not found.'); presets = presets.filter(p=>p.id!==message.id);
  } else throw new Error('Unknown saved-message command.');
  return { ...current, presets: validatePresets(presets), revision: current.revision + 1 };
}
'''.strip()+'\n',encoding='utf-8');print('Shared validation, settings conflicts and saved-message CRUD model written')
