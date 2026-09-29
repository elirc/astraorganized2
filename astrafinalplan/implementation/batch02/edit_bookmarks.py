from pathlib import Path
import json
R=Path('astrafinalplan/implementation/batch02/stage/20')
(R/'server/src/services/metadata.ts').write_text('''import https from "node:https";
import { resolve4 } from "node:dns/promises";
import { isIP } from "node:net";
import { ValidationError } from "../utils/errors";

export function bookmarkUrl(value: unknown): string {
  if (typeof value !== "string" || value.length > 255) throw new ValidationError("URL must be text up to 255 characters.");
  let url: URL;
  try { url = new URL(value.trim()); } catch { throw new ValidationError("Use an absolute http or https URL."); }
  if (!["http:", "https:"].includes(url.protocol) || url.username || url.password || url.href.length > 255) throw new ValidationError("Use an http or https URL without credentials, up to 255 characters.");
  return url.href;
}

/** Conservative IPv4-only metadata policy. Saving a URL does not fetch it. */
export function isPublicIPv4(address: string): boolean {
  if (isIP(address) !== 4) return false;
  const [a,b,c] = address.split(".").map(Number);
  return !(a === 0 || a === 10 || a === 127 || a >= 224 ||
    (a === 100 && b >= 64 && b <= 127) || (a === 169 && b === 254) ||
    (a === 172 && b >= 16 && b <= 31) || (a === 192 && (b === 168 || b === 0 || (b === 88 && c === 99))) ||
    (a === 198 && (b === 18 || b === 19 || (b === 51 && c === 100))) ||
    (a === 203 && b === 0 && c === 113));
}
interface TransferOptions { signal: AbortSignal; maxBytes: number }
type Transfer = (url: URL, address: string, options: TransferOptions) => Promise<string>;
interface MetadataOptions {
  allowedHosts?: string[];
  resolve?: (hostname: string) => Promise<string[]>;
  transfer?: Transfer;
  timeoutMs?: number;
  maxBytes?: number;
}

/** No redirect following. DNS is pinned to a checked address for the connection. */
export const requestHtml: Transfer = (url, address, { signal, maxBytes }) => new Promise((resolve, reject) => {
  const request = https.get(url, {
    signal,
    family: 4,
    lookup: ((_hostname: string, _options: unknown, callback: Function) => callback(null, address, 4)) as any,
    headers: { Accept: "text/html", "Accept-Encoding": "identity", "User-Agent": "BookmarkLearningApp/1.0" },
    maxHeaderSize: 16384,
  }, (response) => {
    const fail = (message: string) => { response.destroy(); request.destroy(); reject(new ValidationError(message)); };
    if (response.statusCode !== 200) return fail("Metadata requires a direct 200 response; redirects are not followed.");
    if (!/^text\\/html(?:;|$)/i.test(String(response.headers["content-type"] || ""))) return fail("Metadata requires an HTML response.");
    if (response.headers["content-encoding"] && response.headers["content-encoding"] !== "identity") return fail("Compressed metadata responses are not supported.");
    if (Number(response.headers["content-length"]) > maxBytes) return fail("Metadata response is too large.");
    const chunks: Buffer[] = []; let bytes = 0;
    response.on("data", (chunk: Buffer) => {
      bytes += chunk.length;
      if (bytes > maxBytes) return fail("Metadata response is too large.");
      chunks.push(chunk);
    });
    response.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    response.on("error", reject);
  });
  request.on("error", reject);
});

export async function fetchMetadata(input: unknown, options: MetadataOptions = {}) {
  const url = new URL(bookmarkUrl(input));
  const allowed = options.allowedHosts ?? (process.env.BOOKMARK_METADATA_HOSTS || "").split(",").map((host) => host.trim().toLowerCase()).filter(Boolean);
  if (url.protocol !== "https:" || (url.port && url.port !== "443") || isIP(url.hostname) || !allowed.includes(url.hostname.toLowerCase())) throw new ValidationError("Metadata is enabled only for explicitly configured HTTPS hostnames on port 443. Enter a title manually for other links.");
  const controller = new AbortController();
  const timeoutMs = options.timeoutMs ?? 5000, maxBytes = options.maxBytes ?? 65536;
  let timer: ReturnType<typeof setTimeout>;
  const expired = new Promise<never>((_resolve, reject) => {
    timer = setTimeout(() => { controller.abort(); reject(new ValidationError("Metadata request timed out.")); }, timeoutMs);
  });
  try {
    return await Promise.race([expired, (async () => {
      const addresses = await (options.resolve ?? resolve4)(url.hostname);
      if (controller.signal.aborted) throw new ValidationError("Metadata request timed out.");
      if (!addresses.length || addresses.some((address) => !isPublicIPv4(address))) throw new ValidationError("Metadata destination must resolve exclusively to public IPv4 addresses.");
      const html = await (options.transfer ?? requestHtml)(url, addresses[0], { signal: controller.signal, maxBytes });
      if (Buffer.byteLength(html, "utf8") > maxBytes) throw new ValidationError("Metadata response is too large.");
      const raw = /<title\\b[^>]*>([\\s\\S]*?)<\\/title\\s*>/i.exec(html)?.[1] || url.hostname;
      const title = raw.replace(/<[^>]*>/g, "").replace(/&(amp|lt|gt|quot|apos);/g, (_match, key: string) => ({ amp: "&", lt: "<", gt: ">", quot: '"', apos: "'" }[key] || "")).replace(/\\s+/g, " ").trim().slice(0,255);
      return { url: url.href, title: title || url.hostname };
    })()]);
  } catch (error) {
    if (error instanceof ValidationError) throw error;
    throw new ValidationError("Could not fetch page metadata. Enter a title manually.");
  } finally { clearTimeout(timer!); controller.abort(); }
}
''',encoding='utf-8')
(R/'server/src/services/service.ts').write_text('''import { z } from "zod";
import * as model from "../models/model";
import { NotFoundError, ValidationError } from "../utils/errors";
import { bookmarkUrl, fetchMetadata } from "./metadata";
const text = z.string().trim().min(1).max(255);
const schema = z.object({
  title: text,
  url: z.string().transform((value, context) => {
    try { return bookmarkUrl(value); }
    catch { context.addIssue({ code: z.ZodIssueCode.custom, message: "Use an absolute http or https URL without credentials, up to 255 characters." }); return z.NEVER; }
  }),
  collection: text,
  status: text,
  tags: z.array(z.string().trim().min(1).max(50)).max(30).default([]),
});
function parseId(value: string) {
  const id = Number(value);
  if (!Number.isInteger(id) || id < 1 || id > 2147483647) throw new ValidationError("Id must be a positive 32-bit integer.");
  return id;
}
function sanitizePayload(payload: unknown, partial = false): Record<string, unknown> {
  const result = (partial ? schema.partial() : schema).safeParse(payload);
  if (!result.success) throw new ValidationError(result.error.issues.map((issue) => `${issue.path.join(".")}: ${issue.message}`).join("; "));
  if (!Object.keys(result.data).length) throw new ValidationError("Supply at least one bookmark field.");
  return result.data.tags ? { ...result.data, tags: [...new Set(result.data.tags)] } : result.data;
}
export function list(query: { search?: string; status?: string }) {
  for (const value of [query.search, query.status]) if (value !== undefined && (typeof value !== "string" || value.length > 255)) throw new ValidationError("Filters must be text up to 255 characters.");
  return model.listRecords(query);
}
export async function get(value: string) {
  const record = await model.findRecord(parseId(value));
  if (!record) throw new NotFoundError("bookmark not found.");
  return record;
}
export function create(payload: unknown) { return model.createRecord(sanitizePayload(payload)); }
export async function update(value: string, payload: unknown) { await get(value); return model.updateRecord(parseId(value), sanitizePayload(payload, true)); }
export async function remove(value: string) { await get(value); return model.deleteRecord(parseId(value)); }
export function getStats() { return model.stats(); }
export function metadata(payload: unknown) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) throw new ValidationError("Supply a URL object.");
  return fetchMetadata((payload as Record<string, unknown>).url);
}
''',encoding='utf-8')
p=R/'server/src/models/model.ts';s=p.read_text();s=s.replace('/** Finds one record', 'function databasePayload(payload: Record<string, unknown>) { return payload.tags === undefined ? payload : { ...payload, tags: JSON.stringify(payload.tags) }; }\n\n/** Finds one record');s=s.replace('.insert(payload)', '.insert(databasePayload(payload))').replace('.update({ ...payload, updated_at:', '.update({ ...databasePayload(payload), updated_at:');p.write_text(s,encoding='utf-8')
p=R/'server/src/controllers/controller.ts';s=p.read_text();s+='\n/** Explicit metadata preview; it never saves or changes a bookmark. */\nexport async function metadata(req: Request, res: Response) { return sendSuccess(res, await service.metadata(req.body)); }\n';p.write_text(s,encoding='utf-8')
p=R/'server/src/routes/routes.ts';s=p.read_text().replace('router.get("/:id"', 'router.post("/metadata", wrap(controller.metadata));\nrouter.get("/:id"');p.write_text(s,encoding='utf-8')
p=R/'client/src/services/api.ts';s=p.read_text();s+='\nexport async function previewMetadata(url: string): Promise<{ url: string; title: string }> {\n  return unwrap(await api.post("/bookmarks/metadata", { url }));\n}\n';p.write_text(s,encoding='utf-8')
p=R/'client/src/App.tsx';s=p.read_text().replace('createRecord, deleteRecord,','createRecord, previewMetadata, deleteRecord,');s=s.replace('  const [error, setError] = useState("");','  const [error, setError] = useState("");\n  const [metadataBusy, setMetadataBusy] = useState(false);');needle='  /** Loads a record into the form for editing. */';s=s.replace(needle,'''  async function usePageTitle() {
    const url = form.url;
    setMetadataBusy(true); setError("");
    try {
      const metadata = await previewMetadata(url);
      setForm((current) => current.url === url ? { ...current, title: metadata.title, url: metadata.url } : current);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Could not load page title");
    } finally { setMetadataBusy(false); }
  }

'''+needle);s=s.replace('          <button>{editingId ? "Update" : "Create"}</button>','          <button type="button" disabled={metadataBusy} onClick={usePageTitle}>{metadataBusy ? "Loading title…" : "Use page title"}</button>\n          <button>{editingId ? "Update" : "Create"}</button>');s=s.replace('    await deleteRecord(id);\n    await refresh();','    try { await deleteRecord(id); await refresh(); }\n    catch (error) { setError(error instanceof Error ? error.message : "Could not delete bookmark"); }');p.write_text(s,encoding='utf-8')
p=R/'server/package.json';d=json.loads(p.read_text());d['scripts']['test']='tsx --test test/*.test.ts';p.write_text(json.dumps(d,indent=2)+'\n')
p=R/'.env.example';s=p.read_text();s+='\n# Optional exact HTTPS hostnames allowed for explicit metadata previews. Empty disables fetching.\nBOOKMARK_METADATA_HOSTS=\n';p.write_text(s,encoding='utf-8')
print('Bookmark runtime validation and opt-in bounded metadata preview implemented.')
