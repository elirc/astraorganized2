# buildsql / IPSKILL review checkpoint

Eligible canonical project `buildsql`, id `0f3292fc93dc`, staged with145files. Original Desktop files are untouched. No implementation changes, spec, tests or new learning course yet. No AGENTS.md found in the original project; `.openai/hosting.json` is absent.

This is an existing React/TypeScript learning game, not a SQL CRUD backend. Preserve its substantial curriculum and recognizable dark/yellow interface. Index declares six tracks,310lessons,2155missions. Track counts: SQL115/779, TypeScript39/275, Node39/274, React39/275, C#41/289, .NET37/263. Complete content validation has not yet been run, so those are currently index counts.

Read in full: root README/package manifest; src/types.ts,game.ts,content.ts,App.tsx,game.test.ts,App.test.tsx,Markdown.tsx,main.tsx,test-setup.ts,styles.css; vite.config.ts; three tsconfigs; scripts/validate-content.mjs and merge-content.mjs; public/content/index.json. Remaining review includes content-src/vol3/assemble.mjs, representative content/resources and lock versions. Old docs should be inventoried before marking historical. Do not claim every lesson's educational accuracy has been manually audited.

Concrete defects:

- loadSave catches malformed/read errors and returns a shallow initial state. The unconditional effect persistSave(save) then overwrites the original raw save. Runtime imported objects are only checked for version1; invalid playerName, maps, timestamps, XP and review entries can crash or mislead the UI.
- localStorage writes on every state update/keystroke have no quota/failure handling, transaction, acknowledgement or cross-tab protection. UI always says SAVE ONLINE and AUTOSAVED even though data is only local and a write can fail.
- content fetches are unchecked casts; track ID comes from persisted/imported state and is interpolated into a path; failures only console.error and can leave endless loading. Out-of-order track loads can replace the newest selection.
- LibraryView opens any mission directly, bypassing journey gates; domain completion receives an arbitrary ID/reward rather than looking up a known mission and prerequisites.
- Math.floor(completed/8) labels an invented count as Challenge gates. Core reward display uses core.length*100 rather than actual configured rewards. Repeat completions display +XP although XP is only awarded once.
- Run checkpoint merely enables manual comparison after8characters; no code executes. The product should explicitly describe self-review, preserve meaningful evidence and distinguish it from automated verification.
- failed recall has no scheduling outcome, and completeMission mixes UTC day strings with local setDate arithmetic. Need a defined date/streak/review policy and deterministic boundary tests.
- Library filter selects the first matching lesson rather than filtering results; long lists lack pagination. MissionView local hint/checkpoint state can survive a mission change unless explicitly keyed/reset. Resource/content failures lack recovery controls.
- merge-content validates portions but skips incomplete authored lessons, writes every live pack sequentially and updates index last. A failure can leave inconsistent published content. Volume path is not bounded. Prefer validated candidate output in a new directory, explicit review, and no automatic partial overwrite of the live archive.

Improvement direction (not implemented): validated transactional local progress with preserved legacy raw text and reviewed import/recovery; explicit save/draft/conflict UI; known catalog IDs and coherent completion/review rules; truthful self-assessment and actual statistics; robust content loading/error handling; responsive accessible navigation; filtered/paginated archive. Add a bounded CRUD practice/project evidence tracker or similarly concrete CRUD learning workflow that complements the existing six-track curriculum. Retain all source curriculum packs unless a specific evidence-backed correction is needed. New astraupskill course should teach actual code and map a mid-level CRUD progression to existing missions plus applied tickets.

Existing dependencies: React19.1 ranges, Vite7.1 range, TS5.9, Vitest3.2.4, ReactMarkdown10.1/remark-gfm4, lucide0.542; package-lock exists. Pin observed lock versions and avoid speculative upgrades. Original6tests cover a few progression/UI happy paths, with localStorage assumptions that will need meaningful replacement when persistence changes.

Some PowerShell Get-Content output displayed mojibake for Unicode punctuation. Do not assume file corruption or globally replace characters: inspect actual UTF-8 bytes with Python before any text correction.

## Additional review

Read assemble.mjs and the first mission in each of the six packs. Actual parsed counts match the index310/2155; this is not yet the complete validator run. The packs total about62.7MB: SQL20,757,633bytes, TypeScript8,161,344, Node8,631,660, React8,021,391, C#8,912,879, .NET8,250,445. Lazy loading is a real strength; avoid loading/rendering all packs or all collapsed Markdown archives eagerly. Consider bounded cache/conditional detail rendering and explicit content-size limits that accommodate the existing SQL pack.

Important educational gap: archived prompts refer to `uv run dojo test ...`, solution.ts/sql/tsx and .NET lesson source paths that are not present in this browser project. Preserve the archive but clearly label those as historical/source-workspace instructions. Provide a concrete runnable CRUD practice path in this repository and do not imply the current Run checkpoint button executes those graders.

assemble.mjs reads fixed parts subdirectories and writes csharp-c.json directly. It requires PROMPT/HINTS/IMPORTANT/REF sections but duplicate section markers overwrite prior values. Together with merge-content's sequential live writes, authoring tools need reviewed candidate output and stronger validation, without running them against original content during this audit.

Observed lock versions to pin (do not replace with guessed latest): lucide-react0.542.0; React/ReactDOM19.2.8; react-markdown10.1.0; remark-gfm4.0.1; testing-library/jest-dom6.9.1; testing-library/react16.3.3; types/node22.20.1; types/react19.2.18; types/react-dom19.2.7; vitejs/plugin-react5.2.0; jsdom26.1.0; TypeScript5.9.3; Vite7.3.6; Vitest3.2.7.


Scope metadata identifies an actual separate eligible SQL Dojo project at geminiorganized/LLM_Generated_Buildsql, id420e3223f23b. Its paths/CLI have not yet been inspected. It may provide a useful source-workspace link for archived SQL exercises, but do not assume all later expansion lessons or other five runtimes are implemented there. No edits to that project have been made.
