const $ = (selector) => document.querySelector(selector);
const pretty = (value) => JSON.stringify(value, null, 2);
const equal = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const windowNow = () => ({start_time: new Date(Date.now()-3600000).toISOString(), end_time: new Date(Date.now()+60000).toISOString()});
const resources = {
  streams: {title:'Streams', permission:'streams', help:'Streams define telemetry type, retention, and payload limits. Default streams are protected.', fields:{name:'text', type:['logs','metrics','traces'], retention_days:'number', max_payload_bytes:'number', indexing_options:'json'}, defaults:()=>({name:'',type:'logs',retention_days:14,max_payload_bytes:1048576,indexing_options:{}})},
  dashboards: {title:'Dashboards', permission:'dashboards', help:'Panels store query and visualization configuration. This workshop editor does not render a chart engine.', fields:{name:'text',description:'text',layout:'json',panels:'json'}, defaults:()=>({name:'',description:'',layout:{},panels:[]})},
  alerts: {title:'Alerts', permission:'alerts', help:'Store a bounded telemetry query and threshold. Evaluate through the API; notification delivery behavior is described in the learning guide.', fields:{name:'text',module:['logs','metrics','traces'],condition:'json',notifications:'json',enabled:'boolean',dedupe_window_seconds:'number'}, defaults:()=>({name:'',module:'logs',condition:{...windowNow(),threshold:1,operator:'gte',limit:100},notifications:[],enabled:true,dedupe_window_seconds:300})},
  pipelines: {title:'Pipelines', permission:'pipelines', help:'Apply validated transformations to ingestion. A failing pipeline preserves its input batch and records a failed run. Schedules are metadata; there is no background scheduler.', fields:{name:'text',source_type:['logs','metrics','traces'],schedule:'nullable',definition:'json',enabled:'boolean'}, defaults:()=>({name:'',source_type:'logs',schedule:null,definition:{steps:[{type:'enrich',fields:{env:'local'}}]},enabled:true})},
  'saved-queries': {title:'Saved queries', permission:null, help:'Save reusable query text and parameters. Read and write permissions follow the query’s telemetry module.', fields:{name:'text',module:['logs','metrics','traces'],query_text:'multiline',params:'json'}, defaults:()=>({name:'',module:'logs',query_text:'SELECT message FROM log_events',params:{}})},
};
const operations = {
  'logs-search':['logs/search',()=>({...windowNow(),limit:100,filters:{}})],
  'logs-ingest':['ingest/logs/json',()=>({stream:'logs-default',events:[{timestamp:new Date().toISOString(),message:'Workshop request completed',service:'workshop',dedupe_key:crypto.randomUUID(),attributes:{elapsed:42}}]})],
  'metrics-query':['metrics/query',()=>({...windowNow(),metric_name:'request_duration',aggregate:'avg',step_seconds:60,limit:100})],
  'metrics-ingest':['ingest/metrics',()=>({stream:'metrics-default',points:[{timestamp:new Date().toISOString(),metric_name:'request_duration',value:42,unit:'ms',dedupe_key:crypto.randomUUID(),labels:{service:'workshop'}}]})],
  'traces-search':['traces/search',()=>({...windowNow(),limit:100})],
  'traces-ingest':['ingest/traces',()=>({stream:'traces-default',spans:[{trace_id:crypto.randomUUID(),span_id:'root',service_name:'workshop',operation_name:'GET /example',start_ts:new Date().toISOString(),end_ts:new Date().toISOString()}]})],
  'logs-sql':['logs/sql',()=>({...windowNow(),query:'SELECT message, service FROM log_events ORDER BY id DESC',limit:100})],
  'metrics-sql':['metrics/sql',()=>({...windowNow(),query:'SELECT metric_name, value FROM metric_points ORDER BY id DESC',limit:100})],
  promql:['metrics/promql',()=>({...windowNow(),query:'avg(request_duration)',step_seconds:60})],
};
let token = null;
let permissions = [];
let resource = 'streams';
let record = null;
let base = null;
let offset = 0;
let total = 0;
let pending = false;
let uncertain = false;
let merge = null;

function status(message) { $('#status').textContent = message; }
function element(tag, text) { const node=document.createElement(tag); if(text!==undefined)node.textContent=text; return node; }
function allowed(module, action) { return permissions.includes(`${module}:${action}`); }
function writable() { const cfg=resources[resource]; const module=cfg.permission || $('#field-module')?.value; return allowed(module,'write'); }
function controls() {
  document.querySelectorAll('button,input,select,textarea').forEach(node=>{node.disabled=pending;});
  if(token) {
    $('#previous').disabled=pending || offset===0;
    $('#next').disabled=pending || offset+20>=total;
    $('#save').disabled=pending || !writable() || uncertain || Boolean(merge);
    $('#delete').disabled=pending || !record || !writable() || uncertain || Boolean(merge);
  }
  document.body.setAttribute('aria-busy',String(pending));
}
async function action(work) {
  if(pending)return;
  const region=document.activeElement?.closest('form,section.card');
  if(region)region.append($('#status'));
  pending=true; controls();
  try { await work(); }
  catch(error) { status(error.message); }
  finally { pending=false; controls(); }
}
async function api(path,{method='GET',body,version}={}) {
  const headers={};
  if(token)headers.Authorization=`Bearer ${token}`;
  if(body!==undefined)headers['Content-Type']='application/json';
  if(version!==undefined)headers['If-Match']=`"v${version}"`;
  let response;
  try { response=await fetch('/api/v1/'+path,{method,headers,body:body===undefined?undefined:JSON.stringify(body),credentials:'omit',cache:'no-store'}); }
  catch { const error=new Error(method==='GET'?'Could not load data. Check the local server.':'The request outcome is unknown. Refresh the list and inspect the record before trying another change.');error.network=true;throw error; }
  let data;
  try {data=await response.json();}catch {const error=new Error('The server returned an unreadable response. Inspect the current record before retrying.');error.network=method!=='GET';throw error;}
  if(!response.ok) {
    const detail=Array.isArray(data.detail)?data.detail.map(item=>`${item.loc.join('.')}: ${item.msg}`).join('\n'):data.detail;
    const error=new Error(`${response.status}: ${detail||'Request failed'}`);error.code=response.status;
    if(response.status===401)error.message+=' Sign out and sign in again.';
    throw error;
  }
  return {data,response};
}
function valuesFromRecord(value) {
  const result={};
  for(const key of Object.keys(resources[resource].fields))result[key]=value[key];
  if(resource==='dashboards')result.panels=result.panels.map(({id,...panel})=>panel);
  return result;
}
function draft() {
  const result={};
  for(const [name,type] of Object.entries(resources[resource].fields)) {
    const input=$('#field-'+name);
    if(type==='boolean')result[name]=input.checked;
    else if(type==='json') {
      try {result[name]=JSON.parse(input.value);}catch {throw new Error(`${name.replaceAll('_',' ')} must contain valid JSON`);}
    } else if(type==='number') {
      if(input.value.trim()==='')throw new Error(`${name} is required`);
      result[name]=Number(input.value);
      if(!Number.isFinite(result[name]))throw new Error(`${name} must be finite`);
    } else result[name]=type==='nullable' && input.value.trim()===''?null:input.value;
  }
  return result;
}
function dirty() {try{return !equal(draft(),base);}catch{return true;}}
function mayLeave() {return !dirty() || window.confirm('Discard the unsaved draft in this form?');}
function fill(values) {
  const container=$('#fields');container.replaceChildren();
  for(const [name,type] of Object.entries(resources[resource].fields)) {
    const label=element('label',name.replaceAll('_',' '));
    let input;
    if(Array.isArray(type)) {input=element('select');for(const value of type){const option=element('option',value);option.value=value;input.append(option);}}
    else if(type==='json'||type==='multiline') {input=element('textarea');input.rows=type==='json'?6:4;input.spellcheck=false;}
    else {input=element('input');input.type=type==='boolean'?'checkbox':type==='number'?'number':'text';if(type==='number')input.step='1';}
    input.id='field-'+name;input.name=name;
    if(type==='boolean')input.checked=Boolean(values[name]);
    else input.value=type==='json'?pretty(values[name]):values[name]??'';
    if(name==='name'){input.required=true;input.maxLength=120;}
    input.addEventListener('input',controls);
    label.append(input);container.append(label);
  }
}
function editor(value=null) {
  record=value;base=value?valuesFromRecord(value):resources[resource].defaults();
  merge=null;uncertain=false;$('#conflict').hidden=true;
  fill(base);
  $('#editor-title').textContent=value?'Edit '+value.name:'New '+resources[resource].title.toLowerCase().replace(/s$/,'');
  $('#revision').textContent=value?`Version ${value.version}`:'Unsaved';
  $('#save').textContent=value?'Save changes':'Create record';
  $('#delete').hidden=!value;
  controls();
}
async function list() {
  const {data,response}=await api(`${resource}?limit=20&offset=${offset}`);
  total=Number(response.headers.get('X-Total-Count')||data.length);
  const container=$('#records');container.replaceChildren();
  if(!data.length)container.append(element('li','No records on this page. Create one to begin.'));
  for(const item of data) {
    const li=element('li');const button=element('button',item.name);
    button.setAttribute('aria-current',String(record?.id===item.id));
    button.append(element('small',`#${item.id} · version ${item.version}`));
    button.addEventListener('click',()=>{if(!mayLeave())return;action(async()=>{const {data}=await api(`${resource}/${item.id}`);editor(data);status('Record loaded.');});});
    li.append(button);container.append(li);
  }
  $('#count').textContent=`${total} records in this organization`;
  $('#page-label').textContent=`Page ${Math.floor(offset/20)+1}`;
}
async function selectResource(name) {
  resource=name;offset=0;editor();
  $('#list-title').textContent=resources[name].title;
  $('#resource-help').textContent=resources[name].help;
  document.querySelectorAll('#resources button').forEach(node=>node.setAttribute('aria-current',node.dataset.resource===name?'page':'false'));
  await list();
}
function navigation() {
  const nav=$('#resources');nav.replaceChildren();
  for(const [name,cfg] of Object.entries(resources)) {
    const readable=cfg.permission?allowed(cfg.permission,'read'):['logs','metrics','traces'].some(module=>allowed(module,'read'));
    if(!readable)continue;
    const button=element('button',cfg.title);button.dataset.resource=name;
    button.addEventListener('click',()=>{if(mayLeave())action(()=>selectResource(name));});nav.append(button);
  }
}
async function reviewConflict(mine, originalError) {
  const {data:latest}=await api(`${resource}/${record.id}`);
  if(latest.version===record.version)throw originalError;
  const theirs=valuesFromRecord(latest);const merged={};const conflicts=[];
  for(const name of Object.keys(resources[resource].fields)) {
    if(equal(mine[name],base[name]))merged[name]=theirs[name];
    else if(equal(theirs[name],base[name])||equal(mine[name],theirs[name]))merged[name]=mine[name];
    else conflicts.push(name);
  }
  merge={latest,mine,theirs,merged,conflicts};
  const container=$('#conflict-fields');container.replaceChildren();
  for(const name of conflicts) {
    container.append(element('h3',name.replaceAll('_',' ')));
    container.append(element('pre',`Your draft:\n${pretty(mine[name])}\n\nCurrent server value:\n${pretty(theirs[name])}`));
    const label=element('label','Choose the value to keep');const select=element('select');select.dataset.field=name;
    for(const [value,text] of [['','Choose…'],['mine','Keep my draft'],['theirs','Keep current server value']]){const option=element('option',text);option.value=value;select.append(option);}
    label.append(select);container.append(label);
  }
  if(!conflicts.length)container.append(element('p','No field-level conflicts. Review the automatically merged form after applying it.'));
  $('#conflict').hidden=false;
  status('A newer version exists. Review the merge below; your draft has been preserved.');
}
$('#resolve').addEventListener('click',()=>{
  if(!merge)return;
  for(const select of document.querySelectorAll('#conflict-fields select')) {
    if(!select.value){status('Choose a value for every conflicting field.');return;}
    merge.merged[select.dataset.field]=merge[select.value][select.dataset.field];
  }
  record=merge.latest;base=merge.theirs;fill(merge.merged);merge=null;$('#conflict').hidden=true;
  $('#revision').textContent=`Version ${record.version}`;status('Reviewed merge applied to the form. Check it, then save.');controls();
});
$('#editor').addEventListener('submit',event=>{
  event.preventDefault();
  action(async()=>{
    const mine=draft();
    try {
      const {data}=await api(record?`${resource}/${record.id}`:resource,{method:record?'PUT':'POST',body:mine,version:record?.version});
      editor(data);await list();status('Record saved.');
    } catch(error) {
      if(error.network)uncertain=true;
      if(error.code===409 && record){await reviewConflict(mine,error);return;}
      throw error;
    }
  });
});
$('#delete').addEventListener('click',()=>{
  if(!record||!window.confirm(`Delete “${record.name}”? This also removes its attached panels or execution/delivery history where applicable.`))return;
  action(async()=>{
    try {await api(`${resource}/${record.id}`,{method:'DELETE',version:record.version});editor();await list();status('Record deleted.');}
    catch(error){if(error.network)uncertain=true;throw error;}
  });
});
$('#new').addEventListener('click',()=>{if(mayLeave()){editor();status('New draft ready.');}});
$('#refresh').addEventListener('click',()=>action(async()=>{await list();status('List refreshed. Open a record to load its current version; your current draft is unchanged.');}));
$('#previous').addEventListener('click',()=>action(async()=>{offset=Math.max(0,offset-20);await list();}));
$('#next').addEventListener('click',()=>action(async()=>{offset+=20;await list();}));
$('#access-form').addEventListener('submit',event=>{
  event.preventDefault();
  const form=new FormData(event.currentTarget);
  const body={org_slug:form.get('org_slug'),email:form.get('email'),password:form.get('password')};
  const bootstrap=form.get('bootstrap')==='on';
  if(bootstrap){body.org_name=form.get('org_name');body.display_name=form.get('display_name');}
  action(async()=>{
    const {data}=await api(bootstrap?'setup/bootstrap':'auth/login',{method:'POST',body});
    token=data.token;$('#access-form [name=password]').value='';
    const {data:me}=await api('auth/me');permissions=me.permissions;
    $('#identity').textContent=`${me.organization.name} · ${me.user?.display_name||'Service account'} · ${me.role}`;
    $('#access').hidden=true;$('#workspace').hidden=false;navigation();
    const first=$('#resources button')?.dataset.resource;
    if(first)await selectResource(first);else status('Signed in. This token has no configuration read permissions.');
    explorerTemplate();status('Workspace opened.');
  });
});
$('#signout').addEventListener('click',()=>{
  if(!mayLeave())return;
  action(async()=>{
    let notice='Signed out.';
    try{await api('auth/logout',{method:'POST'});}catch{notice='Local session cleared. Server revocation could not be confirmed; the token expires automatically.';}
    token=null;permissions=[];record=null;base=null;merge=null;
    $('#workspace').hidden=true;$('#access').hidden=false;$('#fields').replaceChildren();$('#records').replaceChildren();$('#explorer-result').textContent='Results appear here.';status(notice);
  });
});
function explorerTemplate(){const operation=$('#operation').value;$('#explorer-json').value=pretty(operations[operation][1]());}
$('#operation').addEventListener('change',explorerTemplate);
$('#explorer-form').addEventListener('submit',event=>{
  event.preventDefault();action(async()=>{
    let body;try{body=JSON.parse($('#explorer-json').value);}catch{throw new Error('Request JSON is invalid.');}
    const {data}=await api(operations[$('#operation').value][0],{method:'POST',body});
    $('#explorer-result').textContent=pretty(data);status('Telemetry request completed.');
  });
});
window.addEventListener('beforeunload',event=>{if(token&&dirty()){event.preventDefault();event.returnValue='';}});
