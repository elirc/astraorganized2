from pathlib import Path
p=Path(__file__).resolve().parent.parent/'stage/a880d6aae28f/astraupskill'
for f in p.glob('*.md'):
 s=f.read_text(encoding='utf-8-sig').replace('snapshots/GameSetupPage.jsx','snapshots/GameSetupPage.jsx.original.txt').replace('test?s',"test's").replace('root?s',"root's")
 s=s.replace('a delayed delete does not resurrect an addition that completed while the delete awaited the API','a delayed delete does not discard an addition that completed while the delete awaited the API')
 s=s.replace('latest committed value','latest pending state when applying the updater')
 s=s.replace('The old existing-session add path had the API call but did not reliably update the list. The old remove path did not complete the intended server/local CRUD flow. The staged handlers now follow this shape:', 'Both old paths already called the API and updated the list after success. Their problem was computing a replacement array from the captured `players` value after an await. The original setters were `setPlayers([...players, playerResponse.data])` and `setPlayers(players.filter((p) => p.id !== playerId))`. Concurrent completions could discard an addition or restore a removed player. The revised handlers use the current collection:')
 s=s.replace('making existing-session add and remove usable','preserving interleaved existing-session add and remove results')
 f.write_text(s,encoding='utf-8')
