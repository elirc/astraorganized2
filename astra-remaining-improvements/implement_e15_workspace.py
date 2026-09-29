from pathlib import Path

root=Path(__file__).parent/'stage/19110bf39fcf'
p=root/'app/static/app.js'
s=p.read_text(encoding='utf-8')
start=s.index('async function initStaff() {');end=s.index('\nfunction renderSimpleList',start)
s=s[:start]+'''async function initWorkspace(portal = false) {
  const state = { activeTicketId: null, version: null, page: 1, listSequence: 0, detailSequence: 0, busy: false };
  const prefix = portal ? "/portal/tickets" : "/tickets";
  const flash = portal ? "#portal-flash" : "#workspace-flash";
  const list = $(portal ? "#portal-ticket-list" : "#ticket-list");
  const editForms = portal ? [$("#portal-reply-form")] : [$("#ticket-update-form"), $("#reply-form"), $("#note-form")];
  let reviewed = null;
  const reportError = (error) => showFlash(flash, error.message, true);
  function hasDraft() { return editForms.some((form) => dirtyForms.has(form)); }
  function paint(ticket) {
    if (portal) {
      $("#portal-ticket-title").textContent = `#${ticket.number} ${ticket.subject}`;
      renderMessages(ticket.messages, $("#portal-ticket-detail"));
      state.activeTicketId = ticket.id; state.version = ticket.version;
    } else renderTicketDetail(ticket, state);
    reviewed = null; $("latest-review")?.remove();
    $("#latest-review").hidden = true; $("#accept-latest").hidden = true;
  }
  async function loadTicket(id, force = false) {
    if (state.busy) return;
    if (!force && hasDraft() && !confirm("Discard unsaved ticket drafts and open this conversation?")) return;
    const sequence = ++state.detailSequence;
    const ticket = await fetchJSON(`${prefix}/${id}`);
    if (sequence !== state.detailSequence) return;
    if (!force) editForms.forEach(clearDraft);
    paint(ticket);
  }
  async function loadTickets() {
    const sequence = ++state.listSequence;
    const params = new URLSearchParams({ page: String(state.page), page_size: "20" });
    if (!portal) { params.set("view", $("#queue-view").value); params.set("search", $("#ticket-search").value.trim()); }
    try {
      const data = await fetchJSON(`${prefix}?${params}`);
      if (sequence !== state.listSequence) return;
      renderTicketList(data.items, list, (id) => loadTicket(id).catch(reportError), state.activeTicketId);
      $("#ticket-page").textContent = `Page ${state.page} - ${data.total ?? data.items.length} tickets`;
      $("#ticket-prev").disabled = state.page <= 1;
      $("#ticket-next").disabled = !data.has_more;
      if (!state.activeTicketId && data.items.length) await loadTicket(data.items[0].id);
    } catch (error) { reportError(error); }
  }
  $("#ticket-prev").addEventListener("click", () => { if(state.page>1) { state.page--; loadTickets(); } });
  $("#ticket-next").addEventListener("click", () => { state.page++; loadTickets(); });
  $("#review-latest").addEventListener("click", async () => {
    if (!state.activeTicketId || state.busy) return;
    try {
      const id = state.activeTicketId;
      const latest = await fetchJSON(`${prefix}/${id}`);
      if (id !== state.activeTicketId) return;
      reviewed = latest;
      $("#latest-review").textContent = JSON.stringify(latest, null, 2);
      $("#latest-review").hidden = false; $("#accept-latest").hidden = false;
      showFlash(flash, "Review the latest fields and conversation above, especially whether your previous message was already saved. Your draft and its old version remain unchanged until you acknowledge this review.");
    } catch(error) { reportError(error); }
  });
  $("#accept-latest").addEventListener("click", () => {
    if (!reviewed || state.busy) return;
    if (!confirm("I reviewed the latest record and checked whether an uncertain submission was already saved. Keep my drafts and use this reviewed version?")) return;
    paint(reviewed);
    showFlash(flash, "Latest version accepted. Review your retained drafts before saving.");
  });
  async function mutate(form, data, suffix, method) {
    if (!state.activeTicketId) throw new Error("Select a ticket first.");
    if (state.busy) throw new Error("Wait for the current ticket operation to finish.");
    state.busy = true;
    try {
      const ticket = await fetchJSON(`${prefix}/${state.activeTicketId}${suffix}`, {
        method, headers: { "If-Match": String(state.version) }, body: data,
      });
      clearDraft(form); paint(ticket);
      showFlash(flash, "Saved. The conversation shows the accepted result.");
    } finally { state.busy = false; }
    await loadTickets();
  }
  if (!portal) {
    const bootstrap = await fetchJSON("/data/bootstrap");
    fillSelect($("#ticket-team"), bootstrap.teams, "No team");
    fillSelect($("#ticket-assignee"), bootstrap.users.filter((u) => u.role !== "light_agent"), "No assignee");
    const customers = await fetchJSON("/customers?page_size=100");
    fillSelect($("#create-requester"), customers.items, "Select customer (first 100 by name)");
    if (bootstrap.me.role === "light_agent") {
      $("#staff-create-panel").hidden = true; $("#ticket-update-form").hidden = true; $("#reply-form").hidden = true;
    }
    $("#delete-ticket").hidden = !["instance_admin", "support_manager"].includes(bootstrap.me.role);
    $("#queue-view").addEventListener("change", () => { state.page=1; loadTickets(); });
    let timer;
    $("#ticket-search").addEventListener("input", () => {
      state.listSequence++; clearTimeout(timer); timer=setTimeout(() => { state.page=1; loadTickets(); },250);
    });
    bindForm($("#ticket-update-form"), async (form, data) => {
      const payload=objectFromData(data);
      payload.team_id=payload.team_id ? Number(payload.team_id) : null;
      payload.assignee_id=payload.assignee_id ? Number(payload.assignee_id) : null;
      await mutate(form, JSON.stringify(payload), "", "PATCH");
    }, flash);
    bindForm($("#reply-form"), (form,data) => mutate(form,data,"/reply","POST"), flash);
    bindForm($("#note-form"), (form,data) => mutate(form,data,"/note","POST"), flash);
    $("#delete-ticket").addEventListener("click", async () => {
      if (!state.activeTicketId || state.busy) return;
      if (!confirm("Delete this ticket from active work? Its conversation and receipts are retained for staff recovery. Unsaved drafts will be discarded after success.")) return;
      state.busy=true;
      try {
        await fetchJSON(`${prefix}/${state.activeTicketId}`,{method:"DELETE",headers:{"If-Match":String(state.version)}});
        editForms.forEach(clearDraft);state.activeTicketId=null;state.version=null;
        $("#ticket-title").textContent="Select a ticket";$("#ticket-messages").replaceChildren();$("#ticket-meta").replaceChildren();
        showFlash(flash,"Ticket removed from active work. Its stored history is retained.");
      } catch(error) { reportError(error); }
      finally { state.busy=false; }
      await loadTickets();
    });
  } else {
    bindForm($("#portal-reply-form"), (form,data) => mutate(form,data,"/reply","POST"), flash);
    bindForm($("#portal-login-form"), async (form,data) => {
      const values=objectFromData(data); await login(values.email,values.password,flash);
    },flash);
  }
  const createForm=$(portal ? "#portal-create-form" : "#staff-create-form");
  bindForm(createForm, async (form,data) => {
    const payload=portal ? data : objectFromData(data);
    if (!portal) payload.requester_id=Number(payload.requester_id);
    const ticket=await fetchJSON(prefix,{method:"POST",body:portal ? payload : JSON.stringify(payload),
      headers:{"Idempotency-Key":creationKey(form)}});
    clearDraft(form); delete form.dataset.operationKey;
    showFlash(flash,`Submitted ticket #${ticket.number}${ticket.duplicate ? " (existing submission)" : ""}.`);
    await loadTickets();
  },flash);
  $(portal ? "#portal-new-operation" : "#staff-new-operation").addEventListener("click", () => {
    if (createForm.dataset.busy === "true") return;
    if (!confirm("Discard this draft and begin a separate submission? If the previous result was uncertain, review ticket history with staff first to avoid creating a duplicate.")) return;
    clearDraft(createForm);delete createForm.dataset.operationKey;
    showFlash(flash,"Ready for a new submission.");
  });
  $("#logout-button")?.addEventListener("click",logout);
  await loadTickets();
}

async function initStaff() { return initWorkspace(false); }
''' + s[end:]
start=s.index('async function initPortal() {');end=s.index('\nconst boot =',start)
s=s[:start]+'async function initPortal() { return initWorkspace(true); }\n'+s[end:]
s=s.replace('    reviewed = null; $("latest-review")?.remove();','    reviewed = null;')
s=s.replace('  showFlash("#login-flash", error.message, true);','  showFlash("#workspace-flash", error.message, true);\n  showFlash("#login-flash", error.message, true);')
p.write_text(s,encoding='utf-8')
(root/'app/templates/portal.html').write_text('''{% extends "base.html" %}
{% set page = "portal" %}
{% set heading = "Customer Portal" %}
{% block content %}
<p class="flash" id="portal-flash" role="status" aria-live="polite"></p>
<section class="portal-grid">
  <div class="panel">
    <h2>Submit a ticket</h2>
    <p>A submission goes to staff for review. An email address alone does not grant access to ticket history.</p>
    <form id="portal-create-form" class="stack">
      <label>Your name <input name="name" maxlength="255" required autocomplete="name"></label>
      <label>Your email <input name="email" type="email" maxlength="255" required autocomplete="email"></label>
      <label>Company (optional) <input name="company" maxlength="255"></label>
      <label>Subject <input name="subject" maxlength="255" required></label>
      <label>How can we help? <textarea name="body" rows="5" maxlength="20000" required></textarea></label>
      <button type="submit">Create ticket</button>
      <button type="button" id="portal-new-operation">Discard draft and start another submission</button>
    </form>
  </div>
  <div class="panel">
    <h2>Sign in for history</h2>
    <form id="portal-login-form" class="stack">
      <label>Email <input type="email" name="email" autocomplete="username" required></label>
      <label>Password <input type="password" name="password" autocomplete="current-password" required></label>
      <button type="submit">Sign in</button>
    </form>
    <div id="portal-ticket-list" class="list-stack"></div>
    <div class="panel-head"><button id="ticket-prev" type="button">Previous</button><span id="ticket-page" role="status"></span><button id="ticket-next" type="button">Next</button></div>
  </div>
  <div class="panel span-two">
    <h2 id="portal-ticket-title">Your conversation</h2>
    <button id="review-latest" type="button">Review latest conversation while keeping your draft</button>
    <pre id="latest-review" hidden></pre>
    <button id="accept-latest" type="button" hidden>I reviewed the latest record; use its version</button>
    <div id="portal-ticket-detail" class="timeline"></div>
    <form id="portal-reply-form" class="stack">
      <label>Follow-up message <textarea name="body" rows="4" required maxlength="20000"></textarea></label>
      <label>Attachments (up to 3, 5 MiB each) <input type="file" name="files" multiple></label>
      <button type="submit">Reply</button>
    </form>
  </div>
</section>
{% endblock %}
''',encoding='utf-8')
print('Updated ticket workspace and portal forms.')
