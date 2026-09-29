from pathlib import Path
p=Path(__file__).with_name('browser_check.py');t=p.read_text();t=t.replace("get_by_role('status')","locator('.sync-toolbar [role=status]')");p.write_text(t)
