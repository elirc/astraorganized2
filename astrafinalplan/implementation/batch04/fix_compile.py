from pathlib import Path
B=Path('astrafinalplan/implementation/batch04')
p=B/'stage/63/server/src/services/chatService.ts';s=p.read_text().replace('.count<{ count: string }>("id")','.count<{ count: string }[]>("id")');p.write_text(s)
p=B/'stage/64/client/src/App.tsx';s=p.read_text().replace('onClick={() => checkout.mutate({ addressId: firstAddress.id','onClick={() => firstAddress && checkout.mutate({ addressId: firstAddress.id');p.write_text(s)
p=B/'run_checks.py';s=p.read_text().replace("files=[* (root/'test')", "files=[* (root/'test')")
s=s.replace(" if files:tasks.append", " if n in (73,74):tasks.append((str(n),'tests',root,['node',str(root/'node_modules/vitest/vitest.mjs'),'run']))\n if files:tasks.append")
s=s.replace("str(H/'node_modules/vite/bin/vite.js')","str((root if n in (73,74) else H)/'node_modules/vite/bin/vite.js')")
s=s.replace("if config.exists():tasks.append((str(n),label,root,['node',str(H/'node_modules/typescript/bin/tsc'),'--noEmit','-p',str(config)]))","if config.exists():tasks.append((str(n),label,root,['node',str((root if n in (73,74) else H)/'node_modules/typescript/bin/tsc'),*(['-b','--noEmit'] if n in (73,74) and label=='typecheck' else ['--noEmit','-p',str(config)])]))")
p.write_text(s)
