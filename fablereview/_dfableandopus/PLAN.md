# Plan: `dfableandopus/` interview and job-readiness content, all 153 projects

Fable, 2026-09-18. Spec in [BRIEF.md](BRIEF.md); batches in `batches.json` (D01-D16, ~10 projects each, wave 2 first, then wave 1).

| phase | who | what | gate |
|---|---|---|---|
| 1 | Fable | brief, batches, duplication scanner (`dupscan.py`) | this file |
| 2a | 8 Opus agents (D01-D08) | write the seven files per project, log progress | Fable reviews each batch report; dupscan; citation spot-checks |
| 2b | 8 Opus agents (D09-D16) | same, wave-1 projects incl. the 21 clones (delta-focused) | same |
| 3 | Fable | rework requests for failed batches; final dupscan; `REPORT.md`; pointers from `fablereview/README.md` and each project's `astraupskill/README.md` | REPORT.md |

Risks: template drift in wave 1 (mitigated by the clone rule and the dupscan), invented line numbers (mitigated by spot-checks on disk), machine load (agents only read and write Markdown; no installs).
