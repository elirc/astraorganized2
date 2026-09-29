from pathlib import Path

root=Path(__file__).parent/'stage/19110bf39fcf'
(root/'app/templates/admin.html').write_text('''{% extends "base.html" %}
{% set page = "admin" %}
{% set heading = "Help Desk Administration" %}
{% block content %}
<p id="admin-flash" class="flash" role="status" aria-live="polite"></p>
<section class="workspace-grid">
  <aside class="panel stack">
    <label>Manage <select id="resource-kind">
      <option value="customers">Customers</option><option value="teams">Teams</option>
      <option value="channels">Channels</option><option value="slas">Service level agreements</option>
      <option value="business-hours">Business hours</option><option value="automations">Automations</option>
      <option value="canned-replies">Canned replies</option>
    </select></label>
    <label>Find by name (or customer email) <input id="resource-search" type="search" maxlength="255"></label>
    <button id="resource-new" type="button">New record</button>
    <div id="resource-list" class="list-stack"></div>
    <div class="panel-head"><button id="resource-prev" type="button">Previous</button><span id="resource-page" role="status"></span><button id="resource-next" type="button">Next</button></div>
  </aside>
  <section class="panel stack">
    <h2 id="resource-title">New customer</h2>
    <p id="resource-help"></p>
    <form id="resource-form" class="stack"><div id="resource-fields" class="stack"></div><button type="submit">Save record</button></form>
    <div class="pill-row"><button id="resource-review" type="button">Review latest while keeping draft</button><button id="resource-delete" type="button">Delete record</button></div>
    <pre id="resource-latest" hidden></pre>
    <button id="resource-accept" type="button" hidden>I reviewed the latest record; use its version</button>
  </section>
</section>
<section class="panel">
  <div class="panel-head"><h2>Reporting snapshot</h2><a class="pill-link" href="/reports/export">Download CSV</a><button id="reports-refresh" type="button">Refresh report</button></div>
  <div id="report-summary" class="report-grid"></div>
</section>
{% endblock %}
''',encoding='utf-8')
p=root/'app/static/app.js';s=p.read_text(encoding='utf-8')
start=s.index('async function initAdmin() {');end=s.index('\nasync function initPortal()',start)
s=s[:start]+'''const resourceForms = {
  customers: { label:"customer", help:"Profiles hold contact details. Linked sign-in identities require a separate verified email-change workflow.", fields:[
    ["name","Name","text",true],["email","Email","email",true],["phone","Phone (optional)","text"],
    ["company","Company (optional)","text"],["notes","Staff notes (optional)","textarea"]]},
  teams: {label:"team",help:"Team members must be active staff. Reassign tickets before removing their assigned agent.",fields:[
    ["name","Name","text",true],["description","Description (optional)","textarea"],
    ["business_hours_id","Business hours (blank uses default)","business-hours"],["member_ids","Members (Ctrl/Cmd to select several)","users",false,[]]]},
  channels: {label:"channel",help:"Incoming requests use the channel's routing team. This local project records requests; it does not send email or call an external provider.",fields:[
    ["name","Name","text",true],["type","Type",["web","email","api","chat"],true,"web"],
    ["address","Address (optional)","text"],["signature","Signature (optional)","textarea"],
    ["routing_team_id","Routing team (optional)","teams"],["config","Additional settings (JSON object)","json",false,{}]]},
  slas: {label:"service level agreement",help:"Durations are business minutes, including zero. The existing default policy remains required. Updating a policy does not rewrite deadlines already stored on tickets.",fields:[
    ["name","Name","text",true],["business_hours_id","Business hours (blank uses default)","business-hours"],
    ["first_response_minutes","First response minutes","number",true,60],
    ["next_response_minutes","Next response minutes","number",true,240],["resolution_minutes","Resolution minutes","number",true,480],
    ["pause_on_pending","Pause while pending","checkbox",false,true],["pause_on_hold","Pause while on hold","checkbox",false,true],
    ["is_default","Default policy","checkbox",false,false]]},
  "business-hours": {label:"business calendar",help:'Use an IANA timezone, such as UTC or America/Los_Angeles. Schedule keys 0 to 6 mean Monday to Sunday. Example: {"0":[["09:00","12:00"],["13:00","17:00"]]}. Windows cannot overlap or cross midnight.',fields:[
    ["name","Name","text",true],["timezone","Timezone","text",true,"UTC"],
    ["schedule","Weekly schedule (JSON object)","json",true,{"0":[["09:00","17:00"]],"1":[["09:00","17:00"]],"2":[["09:00","17:00"]],"3":[["09:00","17:00"]],"4":[["09:00","17:00"]]}]]},
  automations: {label:"automation",help:'Rules run in position order. Example condition: {"text_match":"billing"}. Example action: {"set_priority":"high","add_tags":["billing"]}. Unknown fields are rejected. A canned reply is recorded only when a full staff user triggers the rule.',fields:[
    ["name","Name","text",true],["event","Event",["on_create","on_update","on_reply","on_time_elapsed"],true,"on_create"],
    ["enabled","Enabled","checkbox",false,false],["position","Position","number",true,0],
    ["conditions","Conditions (JSON object)","json",true,{}],["actions","Actions (JSON object)","json",true,{"set_priority":"high"}]]},
  "canned-replies": {label:"canned reply",help:"Available placeholders: {{ customer_name }}, {{ ticket_number }}, and {{ ticket_subject }}. Replies are stored locally; outbound delivery is not implemented.",fields:[
    ["title","Title","text",true],["body_template","Reply template","textarea",true]]},
};

async function initAdmin() {
  const state={kind:"customers",item:null,page:1,sequence:0,busy:false,reviewed:null};
  const form=$("#resource-form");
  const flash="#admin-flash";
  const error=(value)=>showFlash(flash,value.message,true);
  const lookups={};
  async function refreshLookups() {
    const [teams,calendars,bootstrap]=await Promise.all([fetchJSON("/manage/teams?page_size=100"),fetchJSON("/manage/business-hours?page_size=100"),fetchJSON("/data/bootstrap")]);
    lookups.teams=teams.items;lookups["business-hours"]=calendars.items;lookups.users=bootstrap.users;
  }
  function resetReview() { state.reviewed=null;$("#resource-latest").hidden=true;$("#resource-accept").hidden=true; }
  function renderForm(item=null) {
    state.item=item;resetReview();dirtyForms.delete(form);
    const spec=resourceForms[state.kind];
    $("#resource-title").textContent=`${item ? "Edit" : "New"} ${spec.label}${item ? ` - version ${item.version}` : ""}`;
    $("#resource-help").textContent=spec.help;
    $("#resource-fields").replaceChildren();
    for (const [name,label,type,required=false,fallback=null] of spec.fields) {
      const wrap=textElement("label",label);
      let input;
      const value=item ? item[name] : fallback;
      if (Array.isArray(type) || lookups[type]) {
        input=document.createElement("select");
        if (name==="member_ids") input.multiple=true;
        if (!required && !input.multiple) { const blank=textElement("option","None / default");blank.value="";input.append(blank); }
        const options=Array.isArray(type) ? type.map((value)=>({id:value,name:value})) : lookups[type];
        for(const option of options) {
          const node=textElement("option",option.name);node.value=option.id;
          node.selected=input.multiple ? (value || []).includes(option.id) : String(value)===String(option.id);
          input.append(node);
        }
        // Keep an existing reference selectable even if it is outside the first lookup page.
        if (!input.multiple && value!=null && !options.some((option)=>String(option.id)===String(value))) {
          const current=textElement("option",`Current record #${value}`);current.value=value;current.selected=true;input.append(current);
        }
      } else if (type==="textarea" || type==="json") {
        input=document.createElement("textarea");input.rows=type==="json" ? 6 : 4;
        input.value=type==="json" ? JSON.stringify(value ?? {},null,2) : value ?? "";
        input.maxLength=name==="notes" ? 5000 : 20000;
      } else {
        input=document.createElement("input");input.type=type;
        if(type==="checkbox")input.checked=Boolean(value);
        else input.value=value ?? "";
        if(type==="number"){input.min="0";input.max=name==="position" ? "10000" : "525600";input.step="1";}
        else input.maxLength=name==="phone" ? 64 : 255;
      }
      input.name=name;input.required=required;wrap.append(input);$("#resource-fields").append(wrap);
    }
    $("#resource-delete").disabled=!item;$("#resource-review").disabled=!item;
  }
  function payload(data) {
    const result={};
    for(const [name,,type] of resourceForms[state.kind].fields) {
      const value=data.get(name);
      if(type==="checkbox") result[name]=data.has(name);
      else if(name==="member_ids")result[name]=data.getAll(name).map(Number);
      else if(type==="number" || lookups[type])result[name]=value==="" || value===null ? null : Number(value);
      else if(type==="json")result[name]=JSON.parse(value || "{}");
      else result[name]=value==="" ? null : value;
    }
    return result;
  }
  function mayLeave() { return !state.busy && (!dirtyForms.has(form) || confirm("Discard this unsaved administration draft?")); }
  async function selectRecord(id) {
    if(!mayLeave())return;
    const kind=state.kind;const sequence=++state.sequence;
    try { const item=await fetchJSON(`/manage/${kind}/${id}`);if(kind===state.kind && sequence===state.sequence)renderForm(item); }
    catch(value){error(value);}
  }
  async function load() {
    const kind=state.kind;const sequence=++state.sequence;
    const params=new URLSearchParams({page:String(state.page),page_size:"20",search:$("#resource-search").value.trim()});
    try {
      const data=await fetchJSON(`/manage/${kind}?${params}`);
      if(kind!==state.kind || sequence!==state.sequence)return;
      $("#resource-list").replaceChildren();
      for(const item of data.items) {
        const button=textElement("button",`${item.name || item.title} - version ${item.version}`,"list-item");button.type="button";
        button.addEventListener("click",()=>selectRecord(item.id));$("#resource-list").append(button);
      }
      if(!data.items.length)$("#resource-list").append(textElement("p","No matching records."));
      $("#resource-page").textContent=`Page ${state.page} - ${data.total} records`;
      $("#resource-prev").disabled=state.page<=1;$("#resource-next").disabled=!data.has_more;
    } catch(value){error(value);}
  }
  $("#resource-kind").addEventListener("change",async()=>{
    if(!mayLeave()){$("#resource-kind").value=state.kind;return;}
    state.kind=$("#resource-kind").value;state.page=1;state.sequence++;$("#resource-search").value="";
    try {await refreshLookups();renderForm();await load();}catch(value){error(value);}
  });
  $("#resource-new").addEventListener("click",()=>{if(mayLeave()){state.sequence++;renderForm();}});
  $("#resource-prev").addEventListener("click",()=>{if(state.page>1){state.page--;load();}});
  $("#resource-next").addEventListener("click",()=>{state.page++;load();});
  let timer;
  $("#resource-search").addEventListener("input",()=>{state.sequence++;clearTimeout(timer);timer=setTimeout(()=>{state.page=1;load();},250);});
  bindForm(form,async(form,data)=>{
    if(state.busy)return;state.busy=true;
    try {
      const item=state.item;
      const result=await fetchJSON(`/manage/${state.kind}${item ? `/${item.id}` : ""}`,{
        method:item ? "PUT" : "POST",headers:item ? {"If-Match":String(item.version)} : {},body:JSON.stringify(payload(data)),
      });
      renderForm(result);showFlash(flash,"Saved. The form shows the accepted record.");await load();
    }finally{state.busy=false;}
  },flash);
  $("#resource-review").addEventListener("click",async()=>{
    if(!state.item || state.busy)return;
    const kind=state.kind,id=state.item.id;
    try {
      const latest=await fetchJSON(`/manage/${kind}/${id}`);
      if(state.kind!==kind || state.item?.id!==id)return;
      state.reviewed=latest;$("#resource-latest").textContent=JSON.stringify(latest,null,2);
      $("#resource-latest").hidden=false;$("#resource-accept").hidden=false;
      showFlash(flash,"Compare the latest record above with your retained draft. Saving will replace all editable fields.");
    }catch(value){error(value);}
  });
  $("#resource-accept").addEventListener("click",()=>{
    if(!state.reviewed || state.busy)return;
    if(!confirm("Use the reviewed version with your retained draft? A save replaces all editable fields."))return;
    state.item=state.reviewed;resetReview();
    $("#resource-title").textContent=`Edit ${resourceForms[state.kind].label} - version ${state.item.version}`;
    showFlash(flash,"Reviewed version accepted. Your draft remains unsaved.");
  });
  $("#resource-delete").addEventListener("click",async()=>{
    if(!state.item || state.busy)return;
    if(!confirm(`Delete this ${resourceForms[state.kind].label}? Referenced records are protected. Unsaved changes will be discarded after success.`))return;
    state.busy=true;
    try {
      await fetchJSON(`/manage/${state.kind}/${state.item.id}`,{method:"DELETE",headers:{"If-Match":String(state.item.version)}});
      renderForm();showFlash(flash,"Record deleted.");await load();
    }catch(value){error(value);}finally{state.busy=false;}
  });
  async function report() {
    try {
      const summary=await fetchJSON("/reports/summary");
      $("#report-summary").replaceChildren(labeledValue("Open backlog",summary.open_backlog),labeledValue("Closed tickets",summary.closed_tickets),
        labeledValue("Overdue tickets",summary.overdue_tickets),labeledValue("First response",`${summary.average_first_response_minutes} minutes`),
        labeledValue("Resolution",`${summary.average_resolution_minutes} minutes`));
    }catch(value){error(value);}
  }
  $("#reports-refresh").addEventListener("click",report);
  $("#logout-button").addEventListener("click",logout);
  await refreshLookups();renderForm();await load();await report();
}
''' +s[end:]
s=s.replace('    showFlash(flashSelector, `Signed in as ${payload.user.full_name}`);','''    dirtyForms.delete($("#login-form"));dirtyForms.delete($("#portal-login-form"));
    showFlash(flashSelector, `Signed in as ${payload.user.full_name}`);''')
start=s.index('async function initIndex() {');end=s.index('\nasync function initWorkspace',start)
s=s[:start]+'''async function initIndex() {
  $("#logout-button")?.addEventListener("click",logout);
  bindForm($("#login-form"),async(form,data)=>{const values=objectFromData(data);await login(values.email,values.password);},"#login-flash");
}
''' +s[end:]
s=s.replace('    fillSelect($("#create-requester"), customers.items, "Select customer (first 100 by name)");','''    fillSelect($("#create-requester"), customers.items, "Select customer (search to narrow results)");
    let customerSequence=0,customerTimer;
    $("#create-customer-search").addEventListener("input",()=>{
      const sequence=++customerSequence;clearTimeout(customerTimer);
      customerTimer=setTimeout(async()=>{
        try {
          const data=await fetchJSON(`/customers?page_size=100&search=${encodeURIComponent($("#create-customer-search").value.trim())}`);
          if(sequence===customerSequence)fillSelect($("#create-requester"),data.items,"Select a matching customer");
        }catch(value){reportError(value);}
      },250);
    });''')
s=s.replace('  showFlash("#workspace-flash", error.message, true);','  showFlash("#admin-flash", error.message, true);\n  showFlash("#workspace-flash", error.message, true);')
p.write_text(s,encoding='utf-8')
with (root/'app/static/app.css').open('a',encoding='utf-8') as f:f.write('''
/* Forms remain usable on small screens and with long customer content. */
[hidden] { display: none !important; }
.panel, .workspace-grid > *, .portal-grid > *, .admin-grid > * { min-width: 0; }
.list-item, .message-card, .meta-grid, .flash, h2 { overflow-wrap: anywhere; }
.list-item { text-align: left; width: 100%; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; max-height: 28rem; overflow: auto; padding: 1rem; background: #fffaf2; border: 1px solid var(--line); }
button:disabled { opacity: .55; cursor: wait; }
button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible { outline: 3px solid #146c75; outline-offset: 3px; }
select[multiple] { min-height: 8rem; }
input[type=checkbox] { width: auto; margin-left: .75rem; }
input[type=file] { max-width: 100%; }
nav.pill-row, details.panel { margin-bottom: 1rem; }
#resource-fields > label { display: grid; gap: .4rem; }
@media (max-width: 760px) {
  .workspace-grid, .portal-grid, .admin-grid, .reply-grid, .compact-form, .meta-grid { grid-template-columns: 1fr; }
  .span-two { grid-column: auto; }
  .site-header { flex-wrap: wrap; }
  .layout { padding: 0 1rem 1rem; }
  .panel-head, .pill-row { flex-wrap: wrap; }
}
''')
print('Replaced administration console with labeled versioned CRUD forms and draft review.')
