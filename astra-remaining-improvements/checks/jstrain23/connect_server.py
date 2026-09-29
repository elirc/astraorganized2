from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parents[2];S=B/'stage/58c5c289a8ce'
baseline=json.loads((B/'baselines/58c5c289a8ce.json').read_text(encoding='utf-8'))['files']
file=S/'src/lib/sqlite.js';assert hashlib.sha256(file.read_bytes()).hexdigest()==baseline['src/lib/sqlite.js']
file.write_text('''import path from "node:path";
import { createWorkspaceRepository } from "./workspaceRepository.mjs";

const KEY=Symbol.for("jstrain23.workspaceRepository");
export function getWorkspaceRepository() {
  const file=path.resolve(process.env.WORKSPACE_DB_FILE||".data/workspace.sqlite");
  if(globalThis[KEY]) {
    if(globalThis[KEY].file!==file)throw new Error("Restart the server before changing WORKSPACE_DB_FILE");
    return globalThis[KEY].repository;
  }
  const repository=createWorkspaceRepository(file);
  globalThis[KEY]={file,repository};
  return repository;
}
''',encoding='utf-8')
routes={'workspace':['GET','PUT','POST'],'workspace/version':['GET','PATCH','DELETE'],'search':['GET'],'import/markdown':['POST'],'export/markdown':['GET'],'export/html':['GET'],'export/json':['GET']}
for route,methods in routes.items():
    relative='src/app/api/'+route+'/route.js';file=S/relative
    if relative in baseline:assert hashlib.sha256(file.read_bytes()).hexdigest()==baseline[relative],relative
    else:assert not file.exists()
    file.parent.mkdir(parents=True,exist_ok=True)
    source='import { handleWorkspaceRequest } from "@/lib/httpRoute";\n\nexport const runtime = "nodejs";\nexport const dynamic = "force-dynamic";\n\n'
    source+=''.join(f'export const {method} = handleWorkspaceRequest;\n' for method in methods)
    file.write_text(source,encoding='utf-8')
print('Connected existing routes to revision-checked authenticated workspace API; browser integration remains pending.')
