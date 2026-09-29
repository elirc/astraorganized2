"""Chromium rendering with a synthetic preload bridge: NOT native Electron proof."""
from pathlib import Path
import json, os, sys, traceback
from playwright.sync_api import sync_playwright, expect
ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]).resolve(); OUT.mkdir(parents=True, exist_ok=False)
checks = []
expect.set_options(timeout=20000)
BRIDGE = r"""
window.fixture = {
  state: {revision: 'a'.repeat(64), resume: 'Saved resume', jobDescription: 'Saved role', alwaysOnTop: true,
    credentials: {siliconflowKey: true, deepseekKey: true}}, failSave: false, failRead: false, calls: [], cancellations: 0
};
window.api = {
  async getSettings() { if (fixture.failRead) throw new Error('Invalid JSON data file; preserved'); return structuredClone(fixture.state); },
  async saveSettings(envelope) {
    fixture.calls.push(structuredClone(envelope));
    if (fixture.failSave) throw new Error('Synthetic replacement failure');
    for (const [key, value] of Object.entries(envelope.changes)) {
      if (key.endsWith('Key')) fixture.state.credentials[key] = Boolean(value);
      else fixture.state[key] = value;
    }
    fixture.state.revision = 'b'.repeat(64); return structuredClone(fixture.state);
  },
  ask: async () => { throw new Error('Audio is not available in this renderer fixture'); },
  cancelAsk: async () => { fixture.cancellations++; return {cancelled: true}; },
  onTranscript: cb => { fixture.transcript = cb; return () => {fixture.transcript = null;}; },
  onAnswerChunk: cb => { fixture.chunk = cb; return () => {fixture.chunk = null;}; }
};
"""
def passed(name):
    checks.append({'name': name, 'passed': True}); print('PASS ' + name, flush=True)
def serve(route):
    name = route.request.url.rsplit('/', 1)[-1] or 'index.html'
    if name not in {'index.html','app.js','audio.js','styles.css'}: route.abort(); return
    types = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8'}
    file = ROOT/'src/renderer'/name
    route.fulfill(status=200, body=file.read_bytes(), content_type=types[file.suffix])
code = 1
with sync_playwright() as playwright:
    executable = os.environ.get('ASTRA_BROWSER_EXECUTABLE')
    browser = playwright.chromium.launch(**({'executable_path':executable} if executable else {}))
    page = browser.new_page(viewport={'width':460,'height':700})
    page.route('http://renderer.test/**', serve)
    page.add_init_script(BRIDGE)
    page.on('dialog', lambda dialog: dialog.accept())
    errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
    try:
        page.goto('http://renderer.test/index.html')
        page.locator('#settingsBtn').click()
        expect(page.locator('#settingsView')).to_be_visible()
        expect(page.locator('#siliconflowKey')).to_have_value('')
        expect(page.locator('#deepseekKey')).to_have_value('')
        expect(page.locator('#deepseekKeyStatus')).to_contain_text('never returned')
        passed('saved credentials are represented by presence with blank write-only fields')
        page.locator('#resume').fill('Edited resume')
        page.locator('#alwaysOnTop').uncheck()
        page.locator('#cleardeepseekKey').check()
        page.locator('#saveBtn').click()
        expect(page.locator('#savedNote')).to_contain_text('Settings saved')
        call=page.evaluate('fixture.calls.at(-1)')
        assert call['revision']=='a'*64
        assert call['changes']=={'resume':'Edited resume','alwaysOnTop':False,'deepseekKey':''}
        expect(page.locator('#deepseekKeyStatus')).to_contain_text('No credential')
        passed('settings PATCH preserves omitted key and sends explicit clear and false values')
        page.evaluate('fixture.failSave = true')
        page.locator('#resume').fill('Unsaved draft')
        page.locator('#saveBtn').click()
        expect(page.locator('#errorMsg')).to_contain_text('Your draft remains')
        expect(page.locator('#resume')).to_have_value('Unsaved draft')
        expect(page.locator('#saveBtn')).to_be_disabled()
        page.screenshot(path=str(OUT/'05-settings-draft.png'),full_page=True)
        page.evaluate('fixture.failSave = false')
        page.locator('#reloadSettingsBtn').click()
        expect(page.locator('#resume')).to_have_value('Edited resume')
        expect(page.locator('#saveBtn')).to_be_enabled()
        passed('failed settings save retains draft and requires explicit accepted-state reload')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        page.set_viewport_size({'width':380,'height':520})
        page.locator('#reloadSettingsBtn').scroll_into_view_if_needed()
        expect(page.locator('#reloadSettingsBtn')).to_be_in_viewport()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        passed('expanded settings controls remain reachable in minimum-size window')
        page.locator('#backBtn').click()
        # A synthetic state transition exercises button wiring only, not media capture.
        page.evaluate("setState('transcribing','Synthetic in-flight request')")
        expect(page.locator('#cancelBtn')).to_be_visible()
        page.locator('#cancelBtn').click()
        assert page.evaluate('fixture.cancellations')==1
        page.evaluate("setState('idle','Fixture finished')")
        expect(page.locator('#cancelBtn')).to_be_hidden()
        passed('cancel control invokes dedicated bridge operation for in-flight work')
        page.add_init_script('fixture.failRead = true')
        page.reload()
        expect(page.locator('#errorMsg')).to_contain_text('Invalid JSON')
        expect(page.locator('#statusText')).to_contain_text('could not be loaded')
        assert errors==[], errors
        passed('startup storage errors are displayed instead of silently treated as ready')
        code=0
    except Exception:
        page.screenshot(path=str(OUT/'failure.png'),full_page=True)
        (OUT/'failure.txt').write_text(traceback.format_exc(),encoding='utf-8');traceback.print_exc()
    finally:
        browser.close()
(OUT/'results.json').write_text(json.dumps({'passed':code==0,'checks':checks,'evidence':'Chromium with mocked preload; no native Electron, OS encryption, capture or providers'},indent=2),encoding='utf-8')
sys.exit(code)
