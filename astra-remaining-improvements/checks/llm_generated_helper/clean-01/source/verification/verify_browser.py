"""Real Chromium against a disposable local workspace; no audio or provider calls."""
from pathlib import Path
import json, os, queue, subprocess, sys, threading, time, traceback
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=False)
expect.set_options(timeout=20000)
checks, screens = [], []
started = time.time()

def passed(name):
    checks.append({'name': name, 'passed': True})
    print('PASS ' + name, flush=True)

def shot(page, name):
    page.screenshot(path=str(OUT / (name + '.png')), full_page=True)
    screens.append(name + '.png')

def run(page, url, token):
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('dialog', lambda dialog: dialog.accept())
    page.goto(url)
    expect(page.locator('#workspace')).to_be_hidden()
    page.locator('#token').fill(token)
    page.locator('#login-form button').click()
    expect(page.locator('#workspace')).to_be_visible()
    expect(page.locator('#refresh')).to_be_enabled()
    assert page.evaluate('localStorage.length') == 0
    expect(page.locator('#token')).to_have_value('')
    passed('explicit sign-in with token held only in tab memory')
    expect(page.locator('#records button')).to_have_count(20)
    page.locator('#next').click()
    expect(page.locator('#records button')).to_have_count(3)
    page.locator('#previous').click()
    expect(page.locator('#records button')).to_have_count(20)
    passed('server pagination across 23 seeded profiles')

    def kind(value):
        page.locator('#resource-kind').select_option(value)
        expect(page.locator('#refresh')).to_be_enabled()
        expect(page.locator('#editor-title')).to_contain_text('New')

    def save():
        page.locator('#save').click()
        expect(page.locator('#notice')).to_contain_text('Saved.')
        expect(page.locator('#refresh')).to_be_enabled()

    def search(value):
        page.locator('#search').fill(value)
        page.locator('#search-form button').click()
        expect(page.locator('#refresh')).to_be_enabled()

    def open_only():
        expect(page.locator('#records button')).to_have_count(1)
        page.locator('#records button').click()
        expect(page.locator('#editor-title')).to_contain_text('Edit')
        expect(page.locator('#refresh')).to_be_enabled()

    def snapshot():
        response = page.request.get(url + '/api/bootstrap', headers={'Authorization': 'Bearer ' + token})
        assert response.status == 200
        return response.json()

    def external_patch(kind_name, record_id, body):
        data = snapshot()
        response = page.request.patch(url + f'/api/{kind_name}/{record_id}', data=body,
            headers={'Authorization': 'Bearer ' + token, 'If-Match': '"' + data['revision'] + '"'})
        assert response.status == 200, response.text()

    page.locator('#field-name').fill('Browser learner profile')
    page.locator('#field-targetRole').fill('Mid-level CRUD developer')
    page.locator('#field-background').fill('Trace validation, persistence and UI state.')
    save()
    profile = next(item for item in snapshot()['profiles'] if item['name'] == 'Browser learner profile')
    passed('create profile and reload accepted representation')
    page.locator('#field-name').fill('Browser learner revised')
    external_patch('profiles', profile['id'], {'targetRole': 'Concurrent accepted role'})
    page.locator('#save').click()
    expect(page.locator('#notice')).to_contain_text('changed')
    expect(page.locator('#save')).to_be_disabled()
    expect(page.locator('#field-name')).to_have_value('Browser learner revised')
    page.locator('#review').click()
    expect(page.locator('#comparison')).to_be_visible()
    expect(page.locator('#latest')).to_contain_text('Concurrent accepted role')
    shot(page, '01-conflict-review')
    page.locator('#accept-review').click()
    expect(page.locator('#field-targetRole')).to_have_value('Concurrent accepted role')
    expect(page.locator('#field-name')).to_have_value('Browser learner revised')
    save()
    passed('stale write retains draft and rebases only edited fields after explicit review')

    kind('questions')
    page.locator('#field-title').fill('Explain <img src=x onerror=alert(1)>')
    page.locator('#field-profileId').select_option(profile['id'])
    page.locator('#field-prompt').fill('Explain why a stale update must not silently replace accepted data.')
    page.locator('#field-topic').fill('Concurrency')
    save()
    question = next(item for item in snapshot()['questions'] if item['title'].startswith('Explain <'))
    assert page.locator('#records img').count() == 0
    expect(page.locator('#editor-title')).to_contain_text('<img')
    passed('create profile-specific question with user text rendered as text')
    kind('sessions')
    page.locator('#field-title').fill('Browser rehearsal')
    page.locator('#field-profileId').select_option(profile['id'])
    save()
    page.locator('#field-status').select_option('in_progress')
    save()
    session = next(item for item in snapshot()['sessions'] if item['title'] == 'Browser rehearsal')
    passed('create planned session and explicitly start it')
    kind('attempts')
    page.locator('#field-sessionId').select_option(session['id'])
    page.locator('#field-questionId').select_option(question['id'])
    page.locator('#field-answer').fill('Compare the accepted revision while holding the writer lease.')
    page.locator('#field-feedback').fill('Explain the uncertain response case too.')
    page.locator('#field-score').fill('0')
    save()
    expect(page.locator('#field-score')).to_have_value('0')
    expect(page.locator('#question-context')).to_contain_text('stale update')
    passed('create scored attempt with immutable question snapshot and valid zero score')
    shot(page, '02-attempt')

    # Deliver a real accepted PATCH but drop its response to the browser.
    page.locator('#field-feedback').fill('Accepted even if the response disappears.')
    def lose_response(route):
        response = route.fetch()
        assert response.status == 200
        route.abort('failed')
    page.route('**/api/attempts/*', lose_response, times=1)
    page.locator('#save').click()
    expect(page.locator('#notice')).to_contain_text('response was lost')
    expect(page.locator('#save')).to_be_disabled()
    page.locator('#review').click()
    expect(page.locator('#latest')).to_contain_text('Accepted even if')
    page.locator('#accept-review').click()
    page.locator('#save').click()
    expect(page.locator('#notice')).to_contain_text('no changed fields')
    passed('accepted write with lost response requires review and avoids duplicate submission')

    kind('sessions')
    search('Browser rehearsal')
    open_only()
    page.locator('#field-status').select_option('completed')
    save()
    kind('attempts')
    open_only()
    page.locator('#field-answer').fill('Changed answer while completed')
    page.locator('#save').click()
    expect(page.locator('#notice')).to_contain_text('Start or reopen')
    expect(page.locator('#field-answer')).to_have_value('Changed answer while completed')
    passed('completed session protects attempts and failed save preserves draft')
    kind('sessions')
    search('Browser rehearsal')
    open_only()
    page.locator('#field-status').select_option('in_progress')
    save()
    passed('explicit reopening enables another review cycle')

    kind('profiles')
    search('Browser learner revised')
    open_only()
    page.locator('#delete').click()
    expect(page.locator('#notice')).to_contain_text('references')
    expect(page.locator('#editor-title')).to_contain_text('Browser learner revised')
    passed('referenced profile deletion rejected without removing the editor')
    page.locator('#review').click()
    expect(page.locator('#comparison')).to_be_visible()
    page.locator('#accept-review').click()
    with page.expect_download() as download_info:
        page.locator('#export').click()
    exported = json.loads(Path(download_info.value.path()).read_text(encoding='utf-8'))
    assert token not in json.dumps(exported) and 'auth' not in exported and 'activity' not in exported
    assert len(exported['attempts']) == 1
    passed('authenticated export includes records without credential or audit internals')
    shot(page, '03-profile')

    # Explicit child-first deletion avoids hidden cascading data loss.
    for resource, query in [('attempts', ''), ('sessions', 'Browser rehearsal'), ('questions', 'Explain <'), ('profiles', 'Browser learner revised')]:
        kind(resource)
        if query: search(query)
        open_only()
        page.locator('#delete').click()
        expect(page.locator('#notice')).to_contain_text('Record deleted.')
        expect(page.locator('#refresh')).to_be_enabled()
    passed('delete attempt session question and profile in explicit dependency order')
    page.set_viewport_size({'width': 390, 'height': 844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    shot(page, '04-mobile')
    page.locator('#sign-out').click()
    expect(page.locator('#login')).to_be_visible()
    assert page.evaluate('localStorage.length') == 0
    assert errors == [], errors
    passed('mobile layout and sign-out without uncaught page errors')

code = 1
process = None
try:
    with (OUT / 'server.log').open('w', encoding='utf-8') as log:
        process = subprocess.Popen(['node', 'verification/browser-fixture.cjs'], cwd=ROOT, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=log, text=True, encoding='utf-8')
        lines = queue.Queue()
        threading.Thread(target=lambda: lines.put(process.stdout.readline()), daemon=True).start()
        fixture = json.loads(lines.get(timeout=120))
        with sync_playwright() as playwright:
            executable = os.environ.get('ASTRA_BROWSER_EXECUTABLE')
            browser = playwright.chromium.launch(**({'executable_path': executable} if executable else {}))
            page = browser.new_page(viewport={'width': 1440, 'height': 1000})
            page.set_default_timeout(20000)
            try:
                run(page, fixture['url'], fixture['token'])
                code = 0
            except Exception:
                shot(page, 'failure')
                (OUT / 'failure.txt').write_text(traceback.format_exc(), encoding='utf-8')
                raise
            finally:
                browser.close()
except Exception:
    traceback.print_exc()
finally:
    if process and process.poll() is None:
        process.stdin.write('close\n'); process.stdin.flush()
        try: process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            process.terminate(); process.wait(timeout=20)
    (OUT / 'results.json').write_text(json.dumps({'passed': code == 0, 'checks': checks, 'screenshots': screens,
        'seconds': round(time.time() - started, 2)}, indent=2), encoding='utf-8')
sys.exit(code)
