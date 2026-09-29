from pathlib import Path
import re
B=Path('astrafinalplan/implementation/batch04')
for n in (65,66):
 for p in (B/'stage'/str(n)/'server/src/routes').glob('*.ts'):
  s=p.read_text();s='import type {RequestHandler} from "express";\n'+s;s=re.sub(r'(, )(\w+Controller\.\w+)(\);)',r'\1wrap(\2)\3',s);s+='\nfunction wrap(handler:RequestHandler):RequestHandler{return(req,res,next)=>{Promise.resolve(handler(req,res,next)).catch(next);};}\n';p.write_text(s)
p=B/'stage/64/server/src/services/storeService.ts';s=p.read_text();start=s.index('  const product =',s.index('export async function addToCart'));end=s.index('/** Removes a cart item',start)
s=s[:start]+'''  await changeCartQuantity(userId,sessionId,productId,quantity,true);
  return getCart(userId,sessionId);
}

/** Updates a cart item without allowing its quantity to exceed available stock. */
export async function updateCartItem(userId:number|null,sessionId:string|null,productId:number,quantity:number) {
  await changeCartQuantity(userId,sessionId,productId,quantity,false);
  return getCart(userId,sessionId);
}

async function changeCartQuantity(userId:number|null,sessionId:string|null,productId:number,quantity:number,add:boolean) {
  if(!Number.isSafeInteger(quantity)||quantity<1)throw new ValidationError("Quantity must be a positive whole number");
  await db.transaction(async trx=>{
    const cart=await store.getOrCreateCart(userId,sessionId,trx);
    await trx("carts").where({id:cart.id}).forUpdate().first();
    const product=await trx("products").where({id:productId,is_active:true}).forUpdate().first();
    if(!product)throw new NotFoundError("Product not found");
    const existing=await trx("cart_items").where({cart_id:cart.id,product_id:productId}).first();
    if(!add&&!existing)throw new NotFoundError("Cart item not found");
    const next=quantity+(add?(existing?.quantity??0):0);
    if(next>product.stock_quantity)throw new ValidationError("Not enough stock");
    await trx("cart_items").insert({cart_id:cart.id,product_id:productId,quantity:next,unit_price:product.price}).onConflict(["cart_id","product_id"]).merge({quantity:next,unit_price:product.price});
  });
}

'''+s[end:]
s=s.replace('    const items = await store.getCartItems(cart.id, trx);','    await trx("carts").where({id:cart.id}).forUpdate().first();\n    const cartRows=await trx("cart_items").where({cart_id:cart.id});\n    await trx("products").whereIn("id",cartRows.map(row=>row.product_id)).orderBy("id").forUpdate();\n    const items = await store.getCartItems(cart.id, trx);').replace('if (item.product.stock_quantity < item.quantity)','if (!item.product.is_active || item.product.stock_quantity < item.quantity)');p.write_text(s)
p=B/'stage/64/server/src/models/storeModel.ts';s=p.read_text().replace('[cart] = await trx("carts").insert(where).returning("*");','await trx("carts").insert(where).onConflict(userId ? "user_id" : "session_id").ignore();\n    cart = await trx("carts").where(where).first();');p.write_text(s)
p=B/'stage/65/server/src/models/appointmentModel.ts';s=p.read_text();s='import {ConflictError,NotFoundError,ValidationError} from "../utils/errors.js";\n'+s;start=s.index('  const [appointment] = await db("appointments").insert');end=s.index('/** Calculates provider dashboard',start)
s=s[:start]+'''  return db.transaction(async trx=>{
    const provider=await trx("provider_profiles").where({id:values.provider_id}).forUpdate().first();
    if(!provider||!provider.is_accepting_bookings)throw new NotFoundError("Provider is not accepting bookings");
    await ensureNoConflict(trx,values);
    const [appointment]=await trx("appointments").insert(values).returning("*");
    await trx("notifications").insert({user_id:appointment.customer_id,appointment_id:appointment.id,type:"booking_confirmed",subject:"Booking confirmed",body:`Appointment ${appointment.id} is booking confirmed.`,sent_at:trx.fn.now()});
    return appointment;
  });
}

/** All timing/status writes take the provider lock before testing overlaps. */
export async function updateAppointment(id:number,values:Record<string,unknown>) {
  return db.transaction(async trx=>{
    const found=await trx("appointments").where({id}).first();if(!found)throw new NotFoundError("Appointment not found");
    await trx("provider_profiles").where({id:found.provider_id}).forUpdate().first();
    const before=await trx("appointments").where({id}).forUpdate().first();
    const next={...before,...values};
    if(next.status==="confirmed")await ensureNoConflict(trx,next,id);
    const [appointment]=await trx("appointments").where({id}).update({...values,updated_at:trx.fn.now()}).returning("*");
    return appointment;
  });
}
async function ensureNoConflict(trx:any,values:Record<string,any>,id?:number) {
  const start=new Date(values.start_time),end=new Date(values.end_time);
  if(!Number.isFinite(start.getTime())||!Number.isFinite(end.getTime())||end<=start)throw new ValidationError("Appointment must have a valid increasing time range");
  const query=trx("appointments").where({provider_id:values.provider_id,status:"confirmed"}).where("start_time","<",end).where("end_time",">",start);
  if(id)query.whereNot({id});
  if(await query.first())throw new ConflictError("That time slot is no longer available");
}

'''+s[end:];p.write_text(s)
p=B/'stage/65/server/src/services/appointmentService.ts';s=p.read_text().replace('  await notifyBooking(appointment, "booking_confirmed", "Booking confirmed");\n','');p.write_text(s)
p=B/'stage/66/server/src/app.ts';s=p.read_text();start=s.index('app.use((req,res,next) => {');end=s.index('});',start)+3;s=s[:start]+s[end:];p.write_text(s)
p=B/'stage/66/server/src/models/environmentModel.ts';s=p.read_text();s='import {NotFoundError,ValidationError} from "../utils/errors.js";\n'+s
s=s.replace('    await trx("environments").where({ user_id: userId }).update({ is_active: false });','    await trx("users").where({id:userId}).forUpdate().first();\n    const target=await trx("environments").where({id,user_id:userId}).first();\n    if(!target)throw new NotFoundError("Environment not found");\n    await trx("environments").where({ user_id: userId }).update({ is_active: false });')
s=s.replace('where({ id: environmentId, user_id: userId }).first();\n    if (!environment)', 'where({ id: environmentId, user_id: userId }).forUpdate().first();\n    if (!environment)')
s=s.replace('    await trx("env_variables").where({ environment_id: environmentId }).delete();','    const keys=variables.map(v=>String(v.key).trim());\n    if(new Set(keys).size!==keys.length)throw new ValidationError("Variable keys must be unique");\n    await trx("env_variables").where({ environment_id: environmentId }).delete();')
s=s.replace('...variable, environment_id: environmentId','...variable, key:keys[index], environment_id: environmentId');p.write_text(s)
# Metadata CRUD must use the same activation path, not bypass the user lock.
s=p.read_text();start=s.index('  const [environment] =',s.index('export async function createEnvironment'));end=s.index('/** Deletes an environment',start)
s=s[:start]+'''  return db.transaction(async trx=>{
    await trx("users").where({id:userId}).forUpdate().first();
    if(values.is_active)await trx("environments").where({user_id:userId}).update({is_active:false});
    return (await trx("environments").insert({...values,user_id:userId}).returning("*"))[0];
  });
}

/** Updates metadata while preserving one active environment per user. */
export async function updateEnvironment(id:number,userId:number,values:Record<string,unknown>) {
  return db.transaction(async trx=>{
    await trx("users").where({id:userId}).forUpdate().first();
    const target=await trx("environments").where({id,user_id:userId}).first();
    if(!target)throw new NotFoundError("Environment not found");
    if(values.is_active)await trx("environments").where({user_id:userId}).update({is_active:false});
    return (await trx("environments").where({id,user_id:userId}).update({...values,updated_at:trx.fn.now()}).returning("*"))[0];
  });
}

'''+s[end:];p.write_text(s)
