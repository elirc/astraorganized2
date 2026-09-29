from pathlib import Path
s=Path(__file__).resolve().parents[2]/'stage/58c5c289a8ce'
p=s/'src/components/DatabaseBlock.js';t=p.read_text(encoding='utf-8')
for state,label in [('propertyType','New property type'),('view.type','View type'),('view.groupBy ?? ""','Group records by'),('view.dateProperty ?? ""','Date property'),('view.sorts?.[0]?.field ?? ""','Sort field'),('view.sorts[0].direction','Sort direction'),('filterField','Filter field'),('filterOperator','Comparison')]:
    needle='value={'+state+'}';assert needle in t,state;t=t.replace(needle,'aria-label="'+label+'" '+needle)
p.write_text(t,encoding='utf-8')
p=s/'src/components/WorkspaceApp.js';t=p.read_text(encoding='utf-8').replace('Workspace label (owner only)','Workspace label').replace('Public label (owner only)','Public label')
t=t.replace('                </section>\n\n                {/^https:', '                </section>\n                <p className="muted">Visibility labels organize pages; access remains with the local owner.</p>\n\n                {/^https:')
p.write_text(t,encoding='utf-8')
p=s/'src/app/globals.css';t=p.read_text(encoding='utf-8').replace('grid-template-columns: 64px 1fr 180px 160px auto auto;', 'grid-template-columns: 48px minmax(100px, 1fr) minmax(100px, 140px) minmax(100px, 140px) 34px 34px;')
t+='\n.page-meta > input, .page-meta > select { min-width: 0; width: 100%; }\n'
p.write_text(t,encoding='utf-8')
# Capture actionable diagnostics while Playwright still owns a live context.
p=Path(__file__).with_name('browser_check.py');t=p.read_text()
start=t.index('        page=context.new_page();');end=t.index('        browser.close();browser=None',start)
body=t[start:end]
t=t[:start]+'        try:\n'+''.join('    '+line if line.strip() else line for line in body.splitlines(keepends=True))+'''        except BaseException:
            try:
                (out/'failure.txt').write_text(page.locator('body').inner_text(),encoding='utf-8');page.screenshot(path=str(out/'failure.png'),full_page=True)
            except Exception:pass
            raise
'''+t[end:]
p.write_text(t)
