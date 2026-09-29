from pathlib import Path
import json
B=Path('astrafinalplan/implementation/batch02/stage');R=B/'18'
# Keep validation independent so its runtime contract is readable and testable.
(R/'server/src/validation.ts').write_text('''import type { NewBooking } from "../../shared/types.js";
export class ValidationError extends Error {}
export function uuid(value: unknown): string {
  if (typeof value !== "string" || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value)) throw new ValidationError("Use a valid room or booking id.");
  return value;
}
export function realDate(value: unknown): value is string {
  if (typeof value !== "string" || !/^\\d{4}-\\d{2}-\\d{2}$/.test(value) || value.startsWith("0000")) return false;
  const date = new Date(`${value}T00:00:00Z`);
  return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value;
}
export function timestamp(value: unknown): string {
  if (typeof value !== "string" || !/^\\d{4}-\\d{2}-\\d{2}T(?:[01]\\d|2[0-3]):[0-5]\\d(?::[0-5]\\d(?:\\.\\d{1,3})?)?(?:Z|[+-](?:0\\d|1[0-4]):[0-5]\\d)$/.test(value) || !realDate(value.slice(0,10)) || !Number.isFinite(Date.parse(value))) throw new ValidationError("Times must be real ISO timestamps with an explicit timezone offset.");
  return new Date(value).toISOString();
}
export function parseBooking(body: unknown): NewBooking {
  if (!body || typeof body !== "object" || Array.isArray(body)) throw new ValidationError("Supply a booking object.");
  const data = body as Record<string, unknown>;
  const text = (key: string) => {
    const value = data[key];
    if (typeof value !== "string" || !value.trim() || value.length > 255) throw new ValidationError(`${key} must be nonempty text up to 255 characters.`);
    return value.trim();
  };
  const startsAt = timestamp(data.startsAt), endsAt = timestamp(data.endsAt);
  if (endsAt <= startsAt) throw new ValidationError("End time must be after the start time.");
  return { roomId: uuid(data.roomId), title: text("title"), bookedBy: text("bookedBy"), startsAt, endsAt };
}
''',encoding='utf-8')
p=R/'server/src/index.ts';s=p.read_text();s=s.replace('import "dotenv/config";', 'import "dotenv/config";\nimport { pathToFileURL } from "node:url";\nimport { parseBooking, uuid, realDate, timestamp, ValidationError } from "./validation.js";')
s=s.replace('const app = express();','export const app = express();\nconst wrap = (handler: express.RequestHandler): express.RequestHandler => (req, res, next) => { Promise.resolve(handler(req, res, next)).catch(next); };')
s=s.replace('app.get("/api/rooms", async (_req, res) => {','app.get("/api/rooms", wrap(async (_req, res) => {').replace('ORDER BY name"));\n});','ORDER BY name"));\n}));')
a=s.index('app.get("/api/bookings",');b=s.index('\napp.post(',a)
s=s[:a]+'''app.get("/api/bookings", wrap(async (req, res) => {
  const roomId = req.query.roomId ? uuid(req.query.roomId) : null;
  let start: string | null = null, end: string | null = null;
  if (req.query.dayStart !== undefined || req.query.dayEnd !== undefined) {
    start = timestamp(req.query.dayStart); end = timestamp(req.query.dayEnd);
    if (end <= start || Date.parse(end) - Date.parse(start) > 26 * 3600000) throw new ValidationError("Supply a forward day window no longer than 26 hours.");
  } else if (req.query.date !== undefined) {
    if (!realDate(req.query.date)) throw new ValidationError("Use a real YYYY-MM-DD date.");
    start = `${req.query.date}T00:00:00.000Z`;
    end = new Date(Date.parse(start) + 86400000).toISOString();
  }
  const rows = await query<BookingRow>(`${BOOKING_SELECT}
    WHERE ($1::uuid IS NULL OR b.room_id = $1)
      AND ($2::timestamptz IS NULL OR tstzrange(b.starts_at,b.ends_at,'[)') && tstzrange($2::timestamptz,$3::timestamptz,'[)'))
    ORDER BY b.starts_at, b.id`, [roomId, start, end]);
  res.json(rows.map(toBooking));
}));
'''+s[b:]
s=s.replace('[req.params.id, input.roomId,','[uuid(req.params.id), input.roomId,')
s=s.replace('app.delete("/api/bookings/:id", async (req, res) => {','app.delete("/api/bookings/:id", wrap(async (req, res) => {').replace('[req.params.id]);','[uuid(req.params.id)]);').replace('  res.status(204).send();\n});','  res.status(204).send();\n}));')
s=s.replace('  if (code === CHECK_VIOLATION) {','  if (code === "23503") return res.status(400).json({ error: "Choose an existing room." });\n  if (code === CHECK_VIOLATION) {')
a=s.index('app.listen(port,');s=s[:a]+'''if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  app.listen(port, () => console.log(`Room Booking API on http://localhost:${port}`));
}
''';p.write_text(s,encoding='utf-8')
# Convert local user input at the browser boundary; preserve calendar rollover.
p=R/'client/src/api.ts';s=p.read_text().replace('const BASE = "http://localhost:4112/api";','const BASE = import.meta.env.VITE_API_URL || "http://localhost:4112/api";');s=s.replace('  if (filters.date) params.set("date", filters.date);','''  if (filters.date) {
    const start = new Date(`${filters.date}T00:00`);
    const end = new Date(start); end.setDate(end.getDate() + 1);
    params.set("dayStart", start.toISOString());
    params.set("dayEnd", end.toISOString());
  }''')
s=s.replace('export function deleteBooking(id: string) {','export function updateBooking(id: string, input: NewBooking) {\n  return request<Booking>(`/bookings/${id}`, { method: "PUT", body: JSON.stringify(input) });\n}\n\nexport function deleteBooking(id: string) {');p.write_text(s,encoding='utf-8')
p=R/'client/src/App.tsx';s=p.read_text().replace('useMemo, useState','useMemo, useState, useRef').replace('createBooking, deleteBooking,','createBooking, updateBooking, deleteBooking,')
a=s.index('const today =');b=s.index('\nexport default',a)
s=s[:a]+'''function localInput(date: Date) {
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth()+1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}
const today = () => localInput(new Date()).slice(0,10);
function defaultSlot(dateStr: string, hourOffset: number) {
  const start = new Date(`${dateStr}T00:00`);
  start.setHours(new Date().getHours() + hourOffset, 0, 0, 0);
  return localInput(start);
}
'''+s[b:]
s=s.replace('  const [conflict, setConflict] = useState(false);','  const [conflict, setConflict] = useState(false);\n  const [editingId, setEditingId] = useState<string | null>(null);\n  const [busy, setBusy] = useState(false);\n  const requestVersion = useRef(0);')
s=s.replace('    if (roomId) refresh();\n  }, [roomId, date]);','    if (roomId) refresh();\n    return () => { requestVersion.current += 1; };\n  }, [roomId, date]);')
s=s.replace('  async function refresh() {\n    try {\n      setBookings(await listBookings({ roomId, date }));','  async function refresh() {\n    const version = ++requestVersion.current;\n    try {\n      const data = await listBookings({ roomId, date });\n      if (version === requestVersion.current) setBookings(data);')
s=s.replace('    setConflict(false);\n    try {\n      await createBooking({ roomId, ...form } as NewBooking);','''    setConflict(false);
    if (busy) return;
    setBusy(true);
    try {
      const input: NewBooking = { roomId, ...form, startsAt: new Date(form.startsAt).toISOString(), endsAt: new Date(form.endsAt).toISOString() };
      if (editingId) await updateBooking(editingId, input);
      else await createBooking(input);
      setEditingId(null);''')
s=s.replace('setMessage("Booked. The database guaranteed no overlap.");','setMessage(editingId ? "Booking updated. The database checked for overlap." : "Booked. The database guaranteed no overlap.");')
s=s.replace('      setMessage((error as Error).message);\n    }\n  }\n\n  async function remove','      setMessage((error as Error).message);\n    } finally { setBusy(false); }\n  }\n\n  async function remove')
s=s.replace('    await deleteBooking(id);\n    await refresh();','    try { await deleteBooking(id); if (editingId === id) cancelEdit(); await refresh(); }\n    catch (error) { setConflict(true); setMessage((error as Error).message); }')
s=s.replace('  const timeFmt =', '''  function cancelEdit() {
    setEditingId(null);
    setForm({ title: "", bookedBy: "", startsAt: defaultSlot(date,1), endsAt: defaultSlot(date,2) });
  }
  function edit(booking: Booking) {
    setEditingId(booking.id);
    setForm({ title: booking.title, bookedBy: booking.bookedBy, startsAt: localInput(new Date(booking.startsAt)), endsAt: localInput(new Date(booking.endsAt)) });
    setMessage("Editing an existing booking. Its id will be preserved.");
  }
  const timeFmt =''')
s=s.replace('<h2>Reserve a slot</h2>','<h2>{editingId ? "Edit booking" : "Reserve a slot"}</h2>')
s=s.replace('onChange={(event) => setRoomId(event.target.value)}','onChange={(event) => { cancelEdit(); setRoomId(event.target.value); }}')
s=s.replace('<button type="submit">Book room</button>','<button type="submit" disabled={busy}>{busy ? "Saving…" : editingId ? "Save changes" : "Book room"}</button>\n          {editingId && <button type="button" onClick={cancelEdit} disabled={busy}>Discard edit</button>}')
s=s.replace('<p className={`message','<p role="status" className={`message')
s=s.replace('                <button type="button" className="danger small-btn"','                <button type="button" className="small-btn" onClick={() => edit(booking)}>Edit</button>\n                <button type="button" className="danger small-btn"')
# Associate existing form labels with fields.
for label,idname in [('Room','room'),('Title','title'),('Booked by','booked-by'),('Start','starts-at'),('End','ends-at')]:s=s.replace(f'<label>{label}</label>',f'<label htmlFor="{idname}">{label}</label>')
s=s.replace('<select value={roomId}','<select id="room" value={roomId}').replace('<input value={form.title}','<input id="title" value={form.title}').replace('<input value={form.bookedBy}','<input id="booked-by" value={form.bookedBy}').replace('<input type="datetime-local" value={form.startsAt}','<input id="starts-at" type="datetime-local" value={form.startsAt}').replace('<input type="datetime-local" value={form.endsAt}','<input id="ends-at" type="datetime-local" value={form.endsAt}').replace('<input type="date" value={date}','<input aria-label="Schedule date" type="date" value={date}')
p.write_text(s,encoding='utf-8');(R/'client/src/vite-env.d.ts').write_text('/// <reference types="vite/client" />\n')
p=R/'package.json';d=json.loads(p.read_text());d['scripts']['test']='tsx --test test/*.test.ts';d['scripts']['build']='vite build';p.write_text(json.dumps(d,indent=2)+'\n')
print('Room Booking editing, timestamp boundary and API validation implemented.')
