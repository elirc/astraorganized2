from pathlib import Path
P=Path(__file__).resolve().parent/'stage/092c5e5b7052'
p=P/'client/src/index.css';s=p.read_text();s+='''
/* Text actions need their natural width; the original toolbar sizing was for icons. */
.toolbar { flex-wrap: wrap; overflow: visible; }
.toolbar button { width: auto; min-width: 38px; min-height: 40px; height: auto; padding: 9px 12px; flex: 0 0 auto; white-space: nowrap; }
.toolbar[aria-label="Document details"] { align-items: flex-end; }
.toolbar .field { margin: 0; }
.avatar { display: grid; place-items: center; width: 25px; height: 25px; color: #102822; font-size: 0.78rem; font-weight: 700; box-shadow: none; }
.section-title button { padding: 6px 9px; border: 1px solid var(--line); border-radius: 6px; color: var(--text); background: var(--panel-strong); }
@media (max-width: 520px) { .toolbar[aria-label="Document details"] .field { flex-basis: 100%; min-width: 0; } }
''';p.write_text(s,encoding='utf-8')
p=P/'tests/collaboration.spec.ts';s=p.read_text().replace("  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)", "  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)\n  expect(await page.locator('.toolbar button').evaluateAll(buttons => buttons.every(button => button.scrollWidth <= button.clientWidth))).toBe(true)");p.write_text(s,encoding='utf-8')
