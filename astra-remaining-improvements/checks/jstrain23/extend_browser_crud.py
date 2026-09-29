from pathlib import Path
p=Path(__file__).with_name('browser_check.py');t=p.read_text()
t=t.replace('checks=[];errors=[];server=None;browser=None','checks=[];errors=[];server=None;browser=None\ndef accept_dialog(dialog):dialog.accept()')
t=t.replace("lambda dialog:dialog.accept()","accept_dialog")
needle="passed('authenticated accepted Markdown download includes table content')"
t=t.replace(needle,needle+'''
            database.locator('tbody tr').first.get_by_role('button',name='Delete record',exact=True).click();explicit_save(page);expect(database.get_by_label('Quantity for row',exact=False)).to_have_count(1)
            database.locator('li').filter(has_text='Quantity (number)').get_by_role('button',name='Delete property',exact=True).click();explicit_save(page)
            current=next(item for item in accepted()['state']['blocksByPage'][root] if item['type']=='database')['props'];assert not any(prop['id']==qty for prop in current['properties']);assert all(qty not in row['values'] for row in current['rows']);assert current['views'][0]['sorts']==[];passed('record and referenced property deletion persist with view cleanup')''')
needle="passed('snapshot capture and restore preserve actual page content')"
t=t.replace(needle,needle+'''
            page.locator('.version-row').first.click();page.get_by_role('button',name='Delete this snapshot',exact=True).click();expect(page.locator('.version-row')).to_have_count(0,timeout=15000);passed('snapshot deletion removes history without deleting page')''')
needle="passed('authenticated Markdown import creates code block and selects new page')"
t=t.replace(needle,needle+'''
            page.remove_listener('dialog',accept_dialog);page.once('dialog',lambda dialog:dialog.accept('Review this code'));page.get_by_role('button',name='Comment on block',exact=True).click();page.on('dialog',accept_dialog);explicit_save(page);expect(page.locator('.thread')).to_contain_text('Review this code')
            page.remove_listener('dialog',accept_dialog);page.once('dialog',lambda dialog:dialog.accept('Edited explanation'));page.get_by_role('button',name='Edit comment',exact=True).click();page.on('dialog',accept_dialog);explicit_save(page);expect(page.locator('.thread')).to_contain_text('Edited explanation');passed('comment creation and editing persist through the UI')
            page.remove_listener('dialog',accept_dialog);page.once('dialog',lambda dialog:dialog.accept('Reply with an example'));page.get_by_role('button',name='Reply',exact=True).click();page.on('dialog',accept_dialog);page.get_by_role('button',name='Resolve',exact=True).click();explicit_save(page);expect(page.get_by_role('button',name='Reopen',exact=True)).to_be_visible();passed('comment replies and resolution persist')
            page.get_by_role('button',name='Delete block',exact=True).click();explicit_save(page);expect(page.locator('.thread')).to_have_count(0);assert not accepted()['state']['comments'];passed('block deletion removes dependent thread and comments')''')
p.write_text(t)
