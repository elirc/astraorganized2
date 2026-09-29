from pathlib import Path

p = Path(__file__).resolve().parents[2] / 'stage/4de416cd300b/src/main.ts'
t = p.read_text(encoding='utf-8')
t = t.replace(".querySelector<HTMLButtonElement>('.modal-close')?.focus()", ".querySelector<HTMLButtonElement>('.modal-close,button')?.focus()")
t = t.replace("const panelHeader=", "function focusConfirmation(){queueMicrotask(()=>$('#modal').querySelector<HTMLButtonElement>('button')?.focus());}\nconst panelHeader=", 1)
t = t.replace('</button></div></section>`;return;', '</button></div></section>`;focusConfirmation();return;')
t = t.replace('onTile:(islandId,x,z)=>{if(placement)', 'onTile:(islandId,x,z)=>{if(switching)return;if(placement)')
t = t.replace('onIsland:id=>{if(!placement)', 'onIsland:id=>{if(switching)return;if(!placement)')
t = t.replace('onBuilding:(islandId,buildingId)=>{if(placement)', 'onBuilding:(islandId,buildingId)=>{if(switching)return;if(placement)')
t = t.replace('if(library.isOpen)return;', 'if(library.isOpen||switching)return;')
t = t.replace('if(!document.hidden){accumulator', 'if(!document.hidden&&!switching){accumulator')
t = t.replace("try{if(!repository)throw new Error('Storage is unavailable.');const saved=await repository.read(pendingSlot);await switchVoyage(saved.state,saved);", "try{if(!repository)throw new Error('Storage is unavailable.');switching=true;const saved=await repository.read(pendingSlot);switching=false;await switchVoyage(saved.state,saved);")
t = t.replace("catch(error){toast(error instanceof Error?error.message:'Unable to open this save.','warning');}return;", "catch(error){switching=false;toast(error instanceof Error?error.message:'Unable to open this save.','warning');}return;")
t = t.replace("const raw=await file.text();parseSave(raw);pendingImport=raw;", "const raw=await file.text();const imported=parseSave(raw);pendingImport=raw;")
t = t.replace("'The import is valid. Confirm to replace your active world and automatic save. Save a separate checkpoint first if you need your current progress.'", "`World ${esc(imported.seed)}, day ${Math.floor(imported.time/120)+1}. Confirm to replace your active world and automatic save. Save a separate checkpoint first if you need your current progress.`")
t = t.replace('</button></div></section>`;\n }catch(error)', '</button></div></section>`;focusConfirmation();\n }catch(error)')
p.write_text(t, encoding='utf-8')
print('Added focus for confirmations and prevented active-game edits during a pending load.')
