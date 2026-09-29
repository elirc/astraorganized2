# _Organized Desktop/08 App And Product Projects/job track/task-queue-system — fix report (B17)

Fable, 2026-09-18.

## Done
- review#1 docker-compose.yml (redis:7-alpine) + redis:up/down scripts + README Docker-alternatives paragraph; review#2 README prerequisites (kitchen course first, hardest course); review#5 .nvmrc, engines, POSIX block
- review#3 05 exercise 7: outbox retention + removeOnComplete policy with the delete-only-after-ack argument
- review#4 04 marks the two regressions versus the seventeen specification tests
- review#5 UTF-8 BOM stripped from 9 course files

## Skipped
- the Redis half (docker compose) was not started here: Docker is not usable on this machine; the compose file and scripts are unexercised

## Verification
- server: temporary npm ci (198 packages) + npm test: 19/19 passed (no code changed; the suite needs no Redis); node_modules removed; BOM absence verified by the strip routine

## Course/code consistency check
- 04 names the two regression tests by their exact titles from campaigns.test.cjs and outbox.test.cjs; 05 exercise 7 quotes the removeOnComplete lines that exist in outbox.js and queues/index.js.

## Phase 3 addendum (code blocks)

The codeblocks gate found no fenced code block in chapter(s) 03, 06. One real excerpt was added to each, quoted from this project and cited in the chapter text:

- **03** - server/src/lib/campaignCommands.js (persistCampaign)
- **06** - server/src/lib/outbox.js (dispatcher flush, guarded status update)

No source code was changed; only the chapter Markdown.
