from pathlib import Path
import ast

root=Path(__file__).parent/'stage/19110bf39fcf'
p=root/'app/main.py';s=p.read_text(encoding='utf-8')
s=s.replace('Request, Response, UploadFile, status','Request, Response, UploadFile, Query, status')
s=s.replace('HTMLResponse, JSONResponse, StreamingResponse','HTMLResponse, JSONResponse, StreamingResponse, FileResponse')
s=s.replace('from app.http_boundary import HttpBoundary','from app.http_boundary import HttpBoundary\nfrom app import management\nimport app.services as services\nfrom app.attachments import download_path\nfrom app.references import referenced')
s=s.replace('    ApiToken,','    ApiToken,\n    Attachment,',1)
tree=ast.parse(s);lines=s.splitlines(keepends=True)
replacements={}
for name,kind in [('customer_create','customers'),('team_create','teams'),('channel_create','channels'),('sla_create','slas'),('business_hours_create','business-hours'),('automation_create','automations'),('canned_reply_create','canned-replies')]:
 body=f'''    item = management.save_record(db, {kind!r}, payload, user, request.state.request_id)
    db.commit()
    return management.serialize({kind!r}, item)
'''
 if kind=='customers':body='''    if not can_reply_externally(user):
        raise HTTPException(status_code=403,detail='This role cannot create customers.')
'''+body
 replacements[name]=body
for node in sorted(tree.body,key=lambda n:getattr(n,'lineno',0),reverse=True):
 if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and node.name in replacements:
  lines[node.body[0].lineno-1:node.end_lineno]=[replacements[node.name]]
s=''.join(lines)
s=s.replace('''    search: str | None = None,
    db: Session = Depends(get_db),''','''    search: str | None = Query(default=None,max_length=255),
    page: int = Query(default=1,ge=1,le=100000),
    page_size: int = Query(default=20,ge=1,le=100),
    db: Session = Depends(get_db),''',1)
s=s.replace('''    tickets = db.scalars(stmt.limit(100)).unique().all()
    return {"items": [serialize_ticket(ticket, include_messages=False) for ticket in tickets]}''','''    total=db.scalar(select(func.count()).select_from(stmt.order_by(None).subquery()))
    tickets = db.scalars(stmt.offset((page-1)*page_size).limit(page_size)).unique().all()
    return {"items": [serialize_ticket(ticket, include_messages=False) for ticket in tickets],
            "page":page,"page_size":page_size,"total":total,"has_more":page*page_size<total}''')
s=s.replace('''    channel = db.get(Channel, payload.get("channel_id")) if payload.get("channel_id") else db.scalar(select(Channel).where(Channel.type == ChannelType.WEB))''','''    channel = referenced(db,Channel,payload.get("channel_id"),"Channel") if payload.get("channel_id") else db.scalar(select(Channel).where(Channel.type == ChannelType.WEB))''')
start=s.index('def customer_list(');end=s.index('\n\n@app.post("/customers")',start)
s=s[:start]+'''def customer_list(search: str = Query(default='',max_length=255), page: int = Query(default=1,ge=1,le=100000),
                  page_size: int = Query(default=20,ge=1,le=100),db: Session = Depends(get_db),user: User = Depends(get_staff_user)):
    return management.list_records(db,'customers',page,page_size,search)
'''+s[end:]
start=s.index('def portal_ticket_list(');end=s.index('\n\n@app.get("/portal/tickets/{ticket_id}")',start)
s=s[:start]+'''def portal_ticket_list(page: int = Query(default=1,ge=1,le=100000),page_size: int = Query(default=20,ge=1,le=100),
                       db: Session = Depends(get_db),user: User = Depends(get_customer_user)):
    stmt=select(Ticket).where(Ticket.requester_id==user.customer_id,Ticket.deleted.is_(False))
    total=db.scalar(select(func.count()).select_from(stmt.subquery()))
    tickets=db.scalars(stmt.order_by(Ticket.updated_at.desc(),Ticket.id.desc()).offset((page-1)*page_size).limit(page_size)).all()
    return {'items':[serialize_ticket(ticket,include_messages=False,staff_view=False) for ticket in tickets],
            'page':page,'page_size':page_size,'total':total,'has_more':page*page_size<total}
'''+s[end:]
s=s.replace('    run_automations(db, AutomationEvent(payload["event"]), ticket,','    services.require_writable_ticket(ticket)\n    run_automations(db, AutomationEvent(payload["event"]), ticket,')
for name in ['ticket_follow','ticket_unfollow']:
 start=s.index('def '+name+'(');end=s.index('\n\n@app.',start)
 part=s[start:end].replace('    check_expected_version(request, ticket)','    check_expected_version(request, ticket)\n    services.require_writable_ticket(ticket)')
 s=s[:start]+part+s[end:]
s+='''

@app.get('/manage/{kind}')
def manage_list(kind: str,page: int=Query(default=1,ge=1,le=100000),page_size: int=Query(default=20,ge=1,le=100),
                search: str=Query(default='',max_length=255),db: Session=Depends(get_db),user: User=Depends(get_admin_user)):
    return management.list_records(db,kind,page,page_size,search)


@app.get('/manage/{kind}/{identifier}')
def manage_detail(kind: str,identifier: int,db: Session=Depends(get_db),user: User=Depends(get_admin_user)):
    return management.serialize(kind,management.get_record(db,kind,identifier))


@app.post('/manage/{kind}')
def manage_create(kind: str,payload: dict,request: Request,db: Session=Depends(get_db),user: User=Depends(get_admin_user)):
    item=management.save_record(db,kind,payload,user,request.state.request_id)
    db.commit()
    return management.serialize(kind,item)


@app.put('/manage/{kind}/{identifier}')
def manage_update(kind: str,identifier: int,payload: dict,request: Request,db: Session=Depends(get_db),user: User=Depends(get_admin_user)):
    item=management.get_record(db,kind,identifier)
    check_expected_version(request,item)
    management.save_record(db,kind,payload,user,request.state.request_id,item)
    db.commit()
    return management.serialize(kind,item)


@app.delete('/manage/{kind}/{identifier}')
def manage_delete(kind: str,identifier: int,request: Request,db: Session=Depends(get_db),user: User=Depends(get_admin_user)):
    item=management.get_record(db,kind,identifier)
    check_expected_version(request,item)
    management.delete_record(db,kind,item,user,request.state.request_id)
    db.commit()
    return {'deleted':True,'id':identifier}


@app.delete('/tickets/{ticket_id}')
def ticket_delete(ticket_id: int,request: Request,db: Session=Depends(get_db),user: User=Depends(get_admin_user)):
    ticket=get_ticket(db,ticket_id)
    check_expected_version(request,ticket)
    services.require_writable_ticket(ticket)
    ticket.deleted=True;ticket.updated_at=utcnow()
    services.refresh_sla(ticket,db)
    audit(db,entity_type='ticket',entity_id=str(ticket.id),action='soft_deleted',details={},actor_user=user,request_id=request.state.request_id)
    db.commit()
    return {'deleted':True,'id':ticket.id,'version':ticket.version}


@app.get('/attachments/{attachment_id}')
def attachment_download(attachment_id: int,db: Session=Depends(get_db),user: User=Depends(get_current_user)):
    attachment=db.get(Attachment,attachment_id)
    if not attachment or not attachment.message or attachment.message.ticket_id!=attachment.ticket_id:
        raise HTTPException(status_code=404,detail='Attachment not found.')
    ticket=get_ticket(db,attachment.ticket_id)
    require_ticket_access(ticket,user)
    if user.role==Role.CUSTOMER and attachment.message.kind!=MessageKind.PUBLIC:
        raise HTTPException(status_code=403,detail='Internal attachments are not available to customers.')
    path=download_path(attachment,services.UPLOAD_DIR)
    return FileResponse(path,media_type='application/octet-stream',filename=attachment.filename,
                        content_disposition_type='attachment',headers={'X-Content-Type-Options':'nosniff'})
'''
ast.parse(s);p.write_text(s,encoding='utf-8')
print('Connected management CRUD, paginated ticket queues, soft deletion and attachment downloads.')
