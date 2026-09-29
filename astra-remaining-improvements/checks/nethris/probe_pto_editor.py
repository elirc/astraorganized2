from pathlib import Path
from datetime import date, timedelta
import os
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'stage/71e7b036865c/scripts'))
from learning_server import Server, PASSWORD
from playwright.sync_api import sync_playwright, expect

with Server() as server, sync_playwright() as p:
    server.setup()
    browser = p.chromium.launch(headless=True, executable_path=os.environ['ASTRA_BROWSER_EXECUTABLE'])
    page = browser.new_page()
    page.on('pageerror', lambda error: print('PAGE ERROR:', error, flush=True))
    try:
        page.goto(server.base)
        page.get_by_label('Email', exact=True).fill('employee@example.test')
        page.get_by_label('Password', exact=True).fill(PASSWORD)
        page.get_by_role('button', name='Sign in', exact=True).click()
        expect(page.locator('article.record')).to_have_count(6, timeout=60000)
        page.get_by_role('navigation').get_by_role('button', name='Time off', exact=True).click()
        page.get_by_role('button', name='+ Request time off', exact=True).click()
        day = str(date.today() + timedelta(days=10))
        page.get_by_label('Start date', exact=True).fill(day)
        page.get_by_label('End date', exact=True).fill(day)
        page.get_by_label('Hours', exact=True).fill('7.75')
        page.get_by_label('Reason', exact=True).fill('Probe reason')
        page.get_by_role('button', name='Save changes', exact=True).click()
        expect(page.locator('article.record')).to_contain_text('PendingManager', timeout=60000)
        print('BEFORE EDIT:', page.locator('body').inner_text(), flush=True)
        page.locator('article.record').get_by_role('button', name='Edit', exact=True).click()
        print('AFTER EDIT:', page.locator('body').inner_text(), flush=True)
        expect(page.get_by_label('Reason', exact=True)).to_be_visible(timeout=10000)
    finally:
        print('FINAL BODY:', page.locator('body').inner_text(), flush=True)
        page.screenshot(path=str(Path(__file__).with_suffix('.png')), full_page=True)
        browser.close()
