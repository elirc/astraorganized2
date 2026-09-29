from pathlib import Path
import json
B=Path(__file__).resolve().parent.parent
P=B/'stage/e0e5886e8464'
def save(name,text):
    p=P/name
    if p.exists():
        snap=P/'astraupskill/snapshots'/(name.replace('/','__')+'.original.txt')
        snap.parent.mkdir(parents=True,exist_ok=True)
        if not snap.exists():snap.write_bytes(p.read_bytes())
    p.write_text(text,encoding='utf-8')
name='app/api/recipes/route.ts'
t=(P/name).read_text()
t=t.replace('import { Preferences, Recipe } from "@/lib/types";','import type { Preferences } from "@/lib/types";\nimport type { GenerationInput } from "@/lib/validation";\nimport { generateRecipeResponse } from "@/lib/generation";')
a=t.index('function validateRecipes(');b=t.index('async function callClaude(',a)
t=t[:a]+t[b:]
t=t.replace('  ingredients: string[],\n  timeLimit: number,\n  preferences: Preferences\n): Promise<Recipe[]> {','  { ingredients, timeLimit, preferences }: GenerationInput\n): Promise<unknown> {')
t=t.replace('  const text = message.content[0].type === "text" ? message.content[0].text : "";\n  const parsed = JSON.parse(text);\n  return validateRecipes(parsed);','  const block = message.content.find((item) => item.type === "text");\n  return JSON.parse(block?.type === "text" ? block.text : "");')
a=t.index('  const { ingredients, timeLimit, preferences } = body as')
t=t[:a]+'  const response = await generateRecipeResponse(body, callClaude);\n  return NextResponse.json(response.body, { status: response.status });\n}\n'
save(name,t)
name='lib/storage.ts';t=(P/name).read_text()
t=t.replace('import { GenerationResult, Recipe } from "./types";','import type { GenerationResult, Recipe } from "./types";\nimport { parseGenerationResult, parseRecipe } from "./validation.ts";')
t=t.replace('const updated = [result, ...history].slice(0, MAX_HISTORY);','const updated = [parseGenerationResult(result), ...history].slice(0, MAX_HISTORY);')
t=t.replace('    return JSON.parse(raw) as GenerationResult[];','    return readValidItems(raw, parseGenerationResult).slice(0, MAX_HISTORY);')
t=t.replace('    const favorites = getFavorites();\n    const exists', '    recipe = parseRecipe(recipe);\n    const favorites = getFavorites();\n    const exists',1)
t=t.replace('    return JSON.parse(raw) as Recipe[];','    return readValidItems(raw, parseRecipe);')
t+='\n/** A corrupt entry must not hide unrelated valid learning history. */\nfunction readValidItems<T>(raw: string, parse: (value: unknown) => T): T[] {\n  const value: unknown = JSON.parse(raw);\n  if (!Array.isArray(value)) return [];\n  return value.flatMap((item) => {\n    try { return [parse(item)]; } catch { return []; }\n  });\n}\n'
save(name,t)
name='package.json';pkg=json.loads((P/name).read_text());pkg['scripts']['test']='node --experimental-strip-types --test tests/*.test.mjs';pkg['scripts']['typecheck']='tsc --noEmit';save(name,json.dumps(pkg,indent=2)+'\n')
name='tsconfig.json';cfg=json.loads((P/name).read_text());cfg['compilerOptions']['allowImportingTsExtensions']=True;save(name,json.dumps(cfg,indent=2)+'\n')
print('Recipe adapters updated; original byte snapshots retained.')
