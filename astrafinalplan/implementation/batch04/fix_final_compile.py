from pathlib import Path
B=Path('astrafinalplan/implementation/batch04')
p=B/'stage/63/server/src/controllers/chatController.ts';s=p.read_text().replace('req.params.emoji);','String(req.params.emoji));');p.write_text(s)
p=B/'stage/74/src/content/code-quality.ts';s=p.read_text().replace('      if (user.orders > 10) {\\n        return 0.2;\\n      } else {\\n        return 0.05;\\n      }','      if (user.orders > 10) return 0.2;\\n      else return 0.05;');p.write_text(s)
