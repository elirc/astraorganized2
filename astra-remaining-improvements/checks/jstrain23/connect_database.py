from pathlib import Path
s=Path(__file__).resolve().parents[2]/'stage/58c5c289a8ce'
p=s/'src/components/WorkspaceApp.js';t=p.read_text(encoding='utf-8')
t=t.replace('import Image from "next/image";','import Image from "next/image";\nimport DatabaseBlock from "./DatabaseBlock";')
start=t.index('function DatabaseBlock(');end=t.index('function PageTree(',start);t=t[:start]+t[end:]
p.write_text(t,encoding='utf-8')
p=s/'src/app/globals.css';t=p.read_text(encoding='utf-8')
t+='''
/* Acceptance, draft recovery and small-screen editing. */
.login-shell { max-width: 720px; margin: 8vh auto; padding: 28px; border: 1px solid var(--line); border-radius: 16px; background: white; }
.login-shell form, .database-block form { display: flex; flex-wrap: wrap; gap: 12px; align-items: end; }
.login-shell label, .database-block label { display: grid; gap: 4px; }
.login-shell input { min-width: min(360px, 75vw); }
.sync-toolbar { padding: 12px 24px; border-bottom: 2px solid #1f7a8c; background: #eef8f8; }
.sync-toolbar > div { display: flex; flex-wrap: wrap; gap: 8px; }
.sync-toolbar p { margin: 6px 0; }
button, input, select, textarea { font: inherit; }
button { cursor: pointer; }
button:disabled { opacity: .55; cursor: default; }
button:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible, summary:focus-visible { outline: 3px solid #086b87; outline-offset: 2px; }
.sync-toolbar button, .login-shell button, .database-block button { padding: 6px 10px; border: 1px solid #aac6ca; border-radius: 6px; background: white; color: #17383e; }
.draft-review { max-height: 60vh; overflow: auto; padding: 12px; border: 1px solid #789ca3; background: white; }
.draft-review fieldset { margin: 12px 0; min-width: 0; }
.draft-review label { display: block; }
.draft-review pre { white-space: pre-wrap; overflow-wrap: anywhere; max-height: 180px; overflow: auto; }
[role="alert"] { color: #8c2718; }
.database-block details { padding: 10px; border-top: 1px solid var(--line); }
.database-block details > label, .database-block details > button { margin: 8px; }
.record-card { min-width: 180px; padding: 10px; border: 1px solid var(--line); background: white; border-radius: 8px; margin: 8px 0; }
.record-card label { margin-bottom: 8px; }
.record-card input, .record-card select { max-width: 100%; min-width: 0; }
.db-list { display: grid; gap: 8px; }
.doc-area, .right-panel, .sidebar, .block-body, .database-block { min-width: 0; }
.database-header, .database-actions, .doc-header-actions { flex-wrap: wrap; }
.workspace-shell { min-height: calc(100vh - 140px); }
@media(max-width: 600px) {
 .login-shell { margin: 16px; padding: 16px; }
 .sync-toolbar { padding: 12px; }
 .doc-area { padding: 12px; }
 .doc-header { flex-direction: column; align-items: stretch; gap: 8px; }
 .page-meta { grid-template-columns: 48px minmax(0,1fr); }
 .page-meta select { max-width: 100%; }
 .block-row { grid-template-columns: 24px minmax(0,1fr); }
 .block-type-chip { display: none; }
 .page-title { min-width: 0; font-size: 1.5rem; }
 .db-board { overflow-x: auto; }
 .db-gallery { grid-template-columns: 1fr; }
}
'''
p.write_text(t,encoding='utf-8')
