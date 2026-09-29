"""Record content-based editorial decisions; never writes to a project."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'documentation-audit'
units=json.loads((O/'location-inventory.json').read_text(encoding='utf-8'))
rows=[
('.netopen2','Orchard Core','Tenant-aware dependency injection and persistence traces lead into post-commit side effects, idempotency and failure-design drills.'),
('mastertwenty','Twenty','Metadata-driven CRM architecture, permission-aware ORM flows and senior projects on outboxes, webhook delivery and contract tests.'),
('masteroutline','Outline','Document mutation traces connect transactions, events, queues and WebSockets; multiple learning packs add ADRs, interview practice and a study plan.'),
('masternocu','NocoBase','Plugin lifecycle, resource actions, ACL and repository traces are paired with concrete pagination and mass-assignment exercises.'),
('masterfinisc','Infisical','Secret-write walkthroughs connect validation, authorization, data access and queues; drills address races, cache behavior and security boundaries.'),
('mastercal','Cal.diy','Booking, reservations, cancellation and webhook traces expose race conditions; scoped tickets turn those flows into hands-on work.'),
('mastertea','Teable','Record updates, recalculation and realtime synchronization connect to an incremental CQRS migration and source-based contribution exercises.'),
('masterform','Formbricks','Survey response validation and browser SDK queues support junior tickets, architecture study and exercises across client/server boundaries.'),
('masterpload','Payload','Config-driven CMS behavior is traced through REST, hooks, authorization and database adapters, followed by contribution and design exercises.'),
('masterdidy','Dify','Chat streaming, tenant boundaries, RAG and background work are explained through concrete flows and scoped implementation tickets.'),
('masterpaper','Paperless-ngx','Upload-to-worker/OCR walkthroughs teach Django, Angular and background processing; contribution tasks connect failures to regression tests.'),
('masterpre','pretalx','Proposal workflows, persistent mail and versioned schedules provide concrete Django architecture lessons, failure analysis and junior tickets.'),
('mastermayan','Mayan EDMS','Document ingestion, ACLs, event decorators and layered Celery workers provide broad operational and authorization learning with twenty starter tickets.'),
('masterzulipPY','Zulip','Message delivery crosses Django actions and realtime event delivery; reading and contribution exercises make a large mixed-language system navigable.'),
('masterplane','Plane','Work-item flows connect Django, Celery, multiple React apps and realtime collaboration; guided tickets cover cross-service ownership.'),
('mastersupa','Supabase Studio workspace','Extensive source-anchored lessons and missions distinguish server data, workspace state, table state, React Query and testable frontend boundaries.'),
('mastertypebot','Typebot','Tiered missions explain durable editor state versus transient graph state, with source excerpts, checkpoints and implementation/testing tracks.'),
('masteropen','OpenStatus','Monitoring architecture and inferred ADRs combine with practical missions about state ownership, cache invalidation and operational tradeoffs.'),
('masternovu','Novu','Notification infrastructure and codebase-health analysis are complemented by junior-to-senior missions on dashboard state, contracts and failure surfaces.'),
('masterhop','Hoppscotch','Request execution, GraphQL services, sandboxing and versioned schemas support detailed walkthroughs and invariant-focused contribution tickets.'),
('masterflag','Flagsmith','Flag evaluation, priority rules, caching and streaming become code-reading exercises and tenant-boundary test tickets.'),
('masterdub','Dub','Short-link redirects, attribution and transactional data expose hot-path/cache tradeoffs; the curriculum includes concrete junior contribution work.'),
('masterlink','Linkwarden','Bookmark writes, collection permissions, preservation workers and search indexing form an approachable full-stack architecture curriculum.'),
('masterpostiz','Postiz','Scheduling traces connect API, workers and durable workflows; exercises explicitly discuss the repository’s testing gaps rather than assuming coverage.'),
('masterumami','Umami','Analytics ingestion and query flows teach privacy, throughput, multiple storage backends and targeted testing through concrete tickets.'),
('masteropenedxPYJS','Open edX','Large LMS/authoring boundaries are paired with source-reading paths and predict-then-verify runtime drills with observable self-grading criteria.'),
('mastertool','ToolJet','Progressive missions connect React state, reusable hooks, API contracts and source-level design reasoning in a substantial application builder.'),
('mastershadcn','shadcn/ui','Registry, website and CLI boundaries teach code distribution and AST-based installation, with source excerpts and senior architecture missions.'),
('masternext','NextCRM','Seven concrete CRM flows expose server actions, read/write authorization asymmetry, cache revalidation and testable cross-layer changes.'),
('masteridur','IDURAR','Authentication, generic CRUD and invoice flows explain dynamic controller discovery, reusable UI and domain-specific overrides through guided missions.'),
('nopsolutionsnet','nopCommerce','Storefront, administration and plugin architecture support localized contribution tickets and a grounded ecommerce system-design exercise.'),
('netopen1','eShop / .NET Aspire','Distributed commerce flows, inferred ADRs and a 72-story bootcamp provide prerequisites, hints, acceptance criteria and operational capstones.'),
('.nettodo','eShopOnWeb','A manageable monolith supports design-before-code feature tickets, authorization regression work and observable junior-to-senior learning rubrics.'),
('netcleanarch','CleanArchitecture','Multiple learning packs explain dependency direction, feature slices and tradeoffs, then add scoped contributions, ADRs and interview practice.'),
('reactbullet','Bulletproof React','Source-based chapters and missions compare domain architecture across Vite and Next.js variants, with exercises on state and boundary ownership.'),
('jstrain5','OpsForge','Nine detailed chapters connect production-oriented Next.js, data access, background work, testing and review of assisted code to concrete source.'),
('jstrain2.2','JavaScript bootcamp and app labs','Extensive drills and coaching include multi-file debugging hunts, prediction checkpoints and spaced practice tied to executable application files.'),
('mastermorphic','Morphic','Streaming AI answers, tool execution, persistence and caching form explicit request traces with test-oriented contribution exercises.'),
('spacegamev2','Warband','Architecture and postmortems teach server authority, deterministic retries, time and database uniqueness; exercises reproduce specific failure classes.'),
('gitvg/atlas','Atlas','A full sprint curriculum connects domain modeling to durable outboxes and webhook delivery, with ADRs, flaw analysis and review exercises.'),
('gitvg/folio','Folio','Progressive collaboration lessons develop identity, ordering, tombstones and CRDT convergence through source-based experiments and fuzzing.'),
('gitvg/tracer','Tracer','The issue-tracker curriculum progresses from REST to offline synchronization, mutation logs and realtime delivery with explicit failure/review lessons.'),
('gitvg/relay','Relay','Workflow-engine sprints teach durable execution, retries, connectors and DAG validation using concrete graph cases and implementation tradeoffs.'),
('gitvg/harbor','Harbor','Support and retrieval lessons teach evaluation before feature expansion, chunking/search tradeoffs and traceable sprint-level engineering decisions.'),
('gitvg/pulse','Pulse analytics','A progressive analytics course links ingestion and insights to storage migration, workload measurement and documented operational exercises.'),
('gitvg/agora','Agora','Commerce sprints and ADRs connect cart/domain events and promotion extensibility to design alternatives and code-review reasoning.'),
('gitvg/bazaar','Bazaar','Fifteen commerce sprints explain cart behavior, caching and consistency across buyer and merchant surfaces, with explicit teaching-adapter limits.'),
('perch','Perch','A progressive PR-oriented course provides learner guidance, local sprint narratives and final restore/incident ownership exercises.'),
('masterindicoPYJS','Indico','A large event platform is made approachable through request-handler/data-layer maps and concrete task, authorization and cleanup-test tickets.'),
('mastersaleorPY','Saleor','GraphQL commerce cartography and contribution tasks introduce transaction tracing, checkout contracts and source-grounded engineering reasoning.')]
def resolve(key):
 return next(u['path'] for u in units if u['path']==key or (not u['path'].startswith('geminiorganized/') and u['path'].endswith('/'+key)))
selection=[];decisions=json.loads((O/'manual-decisions.json').read_text(encoding='utf-8'))
for key,name,reason in rows:
 p=resolve(key);selection.append(p);decisions.append({'path':p,'name':name,'selectionReason':reason})
assert len(selection)==len(set(selection))==50
(O/'ranked-selection.json').write_text(json.dumps(selection,indent=2),encoding='utf-8')
(O/'manual-decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2),encoding='utf-8')
nextrows=[
('.netarchitectureproject','Turn the existing DDD reference into a guided modular-monolith course: bounded contexts, CQRS, transactional outboxes, architecture tests and cross-module changes.'),
('jsharness/VTCode','Convert rich Rust architecture/configuration reference into incremental runtime lessons: tool dispatch, process boundaries, cancellation, sandbox contracts and failure testing.'),
('netopen5','Complete Jellyfin’s promising but incomplete Fable cartography pack with request traces, media-job exercises, authorization tests and legacy-migration lessons.'),
('missioncontrol','Use the implemented control-plane core to teach task state machines, atomic claims, SSE, webhook retries and observability; keep roadmap-only features explicit.'),
('lucasrouter','Build a React architecture course around dispatcher/driver state, optimizer contracts, lazy loading, map interactions and failure tests. The current demo has mock data and no database/auth.'),
('formforge','Expand short sprint briefs into schema/discriminated-union walkthroughs, autosave race experiments, accessibility exercises and cross-layer optimistic-concurrency tests.'),
('meterforge','Expand billing outlines into worked money/temporal-domain examples, tenant isolation, idempotent usage ingestion and transactional invoice/outbox exercises. Distinguish in-memory defaults from durable adapters.'),
('campusops','Teach work-order state machines, permissions, scheduling, inventory reservations and persistence with concrete traces and tests. Explain the demo-header identity boundary.'),
('buildsmallplates','Add a mobile/local-first course covering pure progression logic, units, SQLite persistence, schema evolution, navigation state and reproducible offline failure cases.'),
('task-queue-system','Extend the existing architecture deep dive into BullMQ/Redis/SQLite labs: API-to-queue dual writes, retry/backoff, crash recovery, dead letters, idempotency and reconciliation.')]
(O/'next-batch.json').write_text(json.dumps([{'path':resolve(k),'reason':r} for k,r in nextrows],indent=2),encoding='utf-8')
print('Recorded 50 ranked selections and 10 distinct upgrade recommendations.')
