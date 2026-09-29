from pathlib import Path
import json, os, socket, subprocess, time, urllib.request
from playwright.sync_api import sync_playwright, expect

B = Path(__file__).resolve().parents[2]
S = B / 'stage/077627a58eae'
OUT = B / 'checks/localops/layout-02'
OUT.mkdir(exist_ok=False)
URL = 'http://127.0.0.1:5583'
with socket.socket() as probe:
    assert probe.connect_ex(('127.0.0.1', 5583)) != 0, 'Port occupied'
checks = []
with (OUT / 'server.log').open('wb') as log:
    server = subprocess.Popen(['node', 'node_modules/next/dist/bin/next', 'start', '--hostname', '127.0.0.1', '--port', '5583'], cwd=S, stdout=log, stderr=log, creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        deadline = time.monotonic() + 300
        while True:
            try:
                with urllib.request.urlopen(URL, timeout=5) as response:
                    if response.status == 200: break
            except Exception:
                if time.monotonic() > deadline or server.poll() is not None: raise
                time.sleep(1)
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, executable_path=str(B / 'playwright-browsers/chromium-1223/chrome-win64/chrome.exe'))
            page = browser.new_page(viewport={'width':1440,'height':1000})
            page.set_default_timeout(60000)
            page.on('dialog', lambda dialog: dialog.accept())
            page.goto(URL, wait_until='networkidle', timeout=180000)
            page.get_by_role('button',name='Review empty workspace',exact=True).click()
            page.get_by_role('button',name='Use reviewed workspace',exact=True).click()
            expect(page.get_by_role('status')).to_contain_text('Reviewed workspace saved',timeout=60000)
            page.get_by_role('navigation').get_by_role('button',name='People',exact=True).click()
            page.get_by_role('button',name='New record',exact=True).click()
            editor=page.get_by_role('region',name='Record editor')
            editor.get_by_label('Name',exact=True).fill('Keep this draft')
            for width in [1440,800,390]:
                page.set_viewport_size({'width':width,'height':1000})
                for label in ['Name','Role','Phone','Location','Notes']:
                    expect(editor.get_by_label(label,exact=True)).to_be_visible()
                expect(editor.get_by_label('Role',exact=True)).to_have_value('customer')
                expect(editor.get_by_label('Name',exact=True)).to_have_value('Keep this draft')
                page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
                page.screenshot(path=str(OUT / f'06-form-{width}.png'),full_page=True)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
                checks.append({'width':width,'passed':True})
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=30)
        (OUT/'results.json').write_text(json.dumps({'passed':len(checks)==3,'checks':checks},indent=2),encoding='utf-8')
print(json.dumps({'passed':True,'layoutRechecks':3}))
