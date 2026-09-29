from pathlib import Path
import ast

root=Path(__file__).parent/'stage/19110bf39fcf'
p=root/'app/services.py';s=p.read_text(encoding='utf-8')
s=s.replace('from app import contracts','from app import contracts\nfrom app.references import assignment, referenced\nfrom app.attachments import save_attachments as store_attachments')
start=s.index('async def save_attachments(');end=s.index('\n\nasync def add_message',start)
s=s[:start]+'''def transition_status(ticket, new_status):
    """Terminal states stop timers; reopening starts a new resolution window."""
    previous=ticket.status
    if previous==new_status:return
    ticket.status=new_status
    now=utcnow()
    terminal={TicketStatus.RESOLVED,TicketStatus.CLOSED,TicketStatus.SPAM}
    if new_status==TicketStatus.RESOLVED:
        ticket.resolved_at=now;ticket.closed_at=None
    elif new_status==TicketStatus.CLOSED:
        ticket.closed_at=now
        if ticket.resolved_at is None:ticket.resolved_at=now
    elif new_status not in terminal:
        ticket.resolved_at=None;ticket.closed_at=None
        if previous in terminal:
            metadata=dict(ticket.metadata_json or {});metadata['sla_reopened_at']=now.isoformat()
            ticket.metadata_json=metadata
    if new_status in terminal:
        ticket.first_response_due_at=None;ticket.next_response_due_at=None;ticket.resolution_due_at=None
        metadata=dict(ticket.metadata_json or {});metadata.pop('sla_pause',None)
        ticket.metadata_json=metadata
    ticket.updated_at=now


def public_reply_state(db,ticket,at,actor_user=None,actor_customer=None):
    if actor_customer:
        ticket.last_customer_message_at=at
        if ticket.status in {TicketStatus.PENDING,TicketStatus.RESOLVED,TicketStatus.CLOSED,TicketStatus.SPAM}:
            transition_status(ticket,TicketStatus.OPEN)
        if ticket.first_responded_at:
            sla=ticket.sla or default_sla(db)
            ticket.next_response_due_at=add_business_minutes(at,sla.next_response_minutes,team_business_hours(ticket,db))
    elif actor_user:
        ticket.last_agent_reply_at=at
        if ticket.first_responded_at is None:ticket.first_responded_at=at
        ticket.first_response_due_at=None;ticket.next_response_due_at=None
        if ticket.status in {TicketStatus.NEW,TicketStatus.PENDING,TicketStatus.RESOLVED,TicketStatus.CLOSED,TicketStatus.SPAM}:
            transition_status(ticket,TicketStatus.OPEN)
    ticket.updated_at=at
''' + s[end:]
s=s.replace('    body = contracts.validate({"body": body}, contracts.MessageBody)["body"]', '''    if actor_user and kind==MessageKind.PUBLIC and not can_reply_externally(actor_user):
        raise HTTPException(status_code=403,detail='This role cannot send public replies.')
    if actor_customer and (actor_customer.id!=ticket.requester_id or kind!=MessageKind.PUBLIC):
        raise HTTPException(status_code=403,detail='Customer conversation access denied.')
    if actor_user is None and actor_customer is None:
        raise HTTPException(status_code=403,detail='An authenticated message author is required.')
    body = contracts.validate({"body": body}, contracts.MessageBody)["body"]''')
s=s.replace('await save_attachments(ticket, message, files)','await store_attachments(db, ticket, message, files, UPLOAD_DIR)')
start=s.index('    if kind == MessageKind.PUBLIC:',s.index('async def add_message('));end=s.index('    add_event(db, ticket, "message_added"',start)
s=s[:start]+'''    if kind == MessageKind.PUBLIC:
        public_reply_state(db,ticket,message.created_at,actor_user,actor_customer)
'''+s[end:]
s=s.replace('    changed: dict[str, object] = {}','''    selected_team=payload.get('team_id',ticket.team_id)
    selected_agent=payload.get('assignee_id',ticket.assignee_id)
    if 'team_id' in payload or 'assignee_id' in payload:
        assignment(db,selected_team,selected_agent,actor_user)
    changed: dict[str, object] = {}''',1)
s=s.replace('''            ticket.status = new_status
            if new_status == TicketStatus.RESOLVED:
                ticket.resolved_at = utcnow()
            if new_status == TicketStatus.CLOSED:
                ticket.closed_at = utcnow()''','''            transition_status(ticket,new_status)''')
s=s.replace('    if changed:\n        refresh_sla(ticket, db)','    if changed:\n        ticket.updated_at=utcnow()\n        refresh_sla(ticket, db)',1)
s=s.replace('            ticket.team_id = team_id','            ticket.team_id = team_id\n            ticket.team = db.get(Team,team_id) if team_id else None',1)
s=s.replace('            ticket.assignee_id = assignee_id','            ticket.assignee_id = assignee_id\n            ticket.assignee = db.get(User,assignee_id) if assignee_id else None',1)
s=s.replace('''        actions = rule.actions_json or {}
        if actions.get("set_priority"):''','''        actions = contracts.validate(rule.actions_json or {}, contracts.Actions)
        if actions.get('assign_team_id') is not None or actions.get('assign_agent_id') is not None:
            assignment(db,actions.get('assign_team_id',ticket.team_id),actions.get('assign_agent_id',ticket.assignee_id))
        if actions.get("set_priority"):''')
s=s.replace('            ticket.status = TicketStatus(actions["set_status"])','            transition_status(ticket,TicketStatus(actions["set_status"]))')
s=s.replace('            ticket.team_id = actions["assign_team_id"]','            ticket.team_id = actions["assign_team_id"]\n            ticket.team = db.get(Team,ticket.team_id)')
s=s.replace('            ticket.assignee_id = actions["assign_agent_id"]','            ticket.assignee_id = actions["assign_agent_id"]\n            ticket.assignee = db.get(User,ticket.assignee_id)')
s=s.replace('''                ticket.last_agent_reply_at = utcnow()
                ticket.next_response_due_at = None''','''                public_reply_state(db,ticket,utcnow(),actor_user=actor_user)''')
s=s.replace('''        if details:
            add_event''','''        if details:
            ticket.updated_at=utcnow()
            add_event''')
s=s.replace('''    sla = ticket.sla or default_sla(db)
    business_hours = team_business_hours(ticket, db)
    if sla_paused_for_status''','''    if ticket.deleted or ticket.archived or ticket.status in {TicketStatus.RESOLVED,TicketStatus.CLOSED,TicketStatus.SPAM}:
        ticket.first_response_due_at=None;ticket.next_response_due_at=None;ticket.resolution_due_at=None
        return
    sla = ticket.sla or default_sla(db)
    business_hours = team_business_hours(ticket, db)
    origin=ticket.created_at
    if (ticket.metadata_json or {}).get('sla_reopened_at'):
        origin=datetime.fromisoformat(ticket.metadata_json['sla_reopened_at'])
    if sla_paused_for_status''')
s=s.replace('add_business_minutes(ticket.created_at, sla.first_response_minutes','add_business_minutes(origin, sla.first_response_minutes')
s=s.replace('add_business_minutes(ticket.created_at, sla.resolution_minutes','add_business_minutes(origin, sla.resolution_minutes')
s=s.replace('''    selected_team_id = team_id if team_id is not None else (channel.routing_team_id if channel else None)
    ticket = Ticket(''','''    selected_team_id = team_id if team_id is not None else (channel.routing_team_id if channel else None)
    assignment(db,selected_team_id,None,actor_user)
    ticket = Ticket(''')
s=s.replace('''    if target.id == source.id:
        raise HTTPException(status_code=400, detail="Cannot merge a customer into itself")''','''    if actor_user.role not in {Role.INSTANCE_ADMIN,Role.SUPPORT_MANAGER}:
        raise HTTPException(status_code=403,detail='Customer merges require a manager.')
    if target.id == source.id:
        raise HTTPException(status_code=400, detail="Cannot merge a customer into itself")
    if db.scalar(select(User.id).where(User.customer_id.in_([source.id,target.id]))):
        raise HTTPException(status_code=409,detail='A customer has a linked sign-in identity. Use a separate verified identity migration; this merge cannot transfer account access.')
    target.version+=1''')
s=s.replace('term = f"%{search.lower()}%"','term = search.lower()')
s=s.replace('.like(term)', '.contains(term, autoescape=True)')
s=s.replace('''    if status_value:
        stmt = stmt.where(Ticket.status == TicketStatus(status_value))
    if priority:
        stmt = stmt.where(Ticket.priority == TicketPriority(priority))''','''    if status_value:
        try:state=TicketStatus(status_value)
        except ValueError:raise HTTPException(status_code=422,detail='Unknown ticket status.')
        stmt = stmt.where(Ticket.status == state)
    if priority:
        try:level=TicketPriority(priority)
        except ValueError:raise HTTPException(status_code=422,detail='Unknown ticket priority.')
        stmt = stmt.where(Ticket.priority == level)''')
ast.parse(s);p.write_text(s,encoding='utf-8')
for file in ['app/db.py','tests/conftest.py']:
 p=root/file;s=p.read_text(encoding='utf-8')
 if file=='app/db.py':s=s.replace('    finally:\n        db.close()','    finally:\n        if db.in_transaction():db.rollback()\n        db.close()')
 else:s=s.replace('            yield db','            try:\n                yield db\n            finally:\n                if db.in_transaction():db.rollback()')
 p.write_text(s,encoding='utf-8')
print('Updated shared lifecycle, relationship guards, upload transaction cleanup and literal search.')
