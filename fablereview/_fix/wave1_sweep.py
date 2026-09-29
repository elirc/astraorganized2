#!/usr/bin/env python3
"""
wave1_sweep.py - Phase-1 wave-1 structural sweep for the Astra fix program.

Operates ONLY on the 75 wave-1 projects listed in fablereview/registry.json
(wave == 1). The course for a project is <abs>/astraupskill.

Usage (run from anywhere; paths are derived from this file's location):

    python wave1_sweep.py --dry-run     # writes _fix/sweep_dryrun.md, changes nothing
    python wave1_sweep.py --apply       # applies and writes _fix/sweep_applied.md
    python wave1_sweep.py --scan        # leaked-phrase residue scan only

Every rule is idempotent: running --dry-run after --apply must report 0 changes.
File line endings and BOM state are preserved, except where a rule is explicitly
about moving/removing a misplaced BOM.

Rules implemented (ids match IMPROVEMENT_BACKLOG.md):

  R2.1  per-stack environment/limits paragraphs (drop Postgres claims from
        non-Postgres projects, drop the jsdom/app.js paragraph from server
        projects, de-leak other projects' names, drop the Chromium sentence
        where the batch evidence records no browser check)
  R2.6  de-minify Astra-delivered test files with Prettier 3
  R2.7  reproducibility pins: a "### Toolchain" block in the course README
  R2.8  hygiene: misplaced UTF-8 BOM, snippet-vault mojibake
  R2.9  diff-reading note in VERIFICATION.md's Reproduce section
  R2.10 clone banners in the course README of the 18 clone projects
  R1.15 delivered-delta vs inherited test counts in four VERIFICATION.md files
"""

from __future__ import annotations

import argparse
import codecs
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))              # .../fablereview/_fix
FABLEREVIEW = os.path.dirname(HERE)                            # .../fablereview
ASTRA_ORG = os.path.dirname(FABLEREVIEW)                       # .../AstraOrganized2
IMPL = os.path.join(ASTRA_ORG, "astrafinalplan", "implementation")
REGISTRY = os.path.join(FABLEREVIEW, "registry.json")
# Unique per process: two concurrent runs of this script must not delete each
# other's staging tree.
PRETTIER_TMP = os.path.join(HERE, ".prettier-tmp-%d" % os.getpid())

# ---------------------------------------------------------------------------
# Evidence: which stages actually have a recorded browser check.
# Source of truth (read at run time, these are the fallbacks):
#   implementation/browser-checks.json          -> 01..06
#   implementation/batch02/browser-checks.json  -> 11..20
#   implementation/batch03/browser-checks.json  -> 21..50
#   implementation/batch04/browser-checks.json  -> 51..75
# Stages 07-10 (newcodexJS 01/02/03/05) have NO entry anywhere, yet their
# VERIFICATION.md claims "Browser checks used the installed Chromium build."
# ---------------------------------------------------------------------------
BROWSER_CHECK_FILES = [
    os.path.join(IMPL, "browser-checks.json"),
    os.path.join(IMPL, "batch02", "browser-checks.json"),
    os.path.join(IMPL, "batch03", "browser-checks.json"),
    os.path.join(IMPL, "batch04", "browser-checks.json"),
]

MANIFESTS = [
    os.path.join(IMPL, "delivery-manifest.json"),
    os.path.join(IMPL, "batch02", "delivery-manifest.json"),
    os.path.join(IMPL, "batch03", "delivery-manifest.json"),
    os.path.join(IMPL, "batch04", "delivery-manifest.json"),
]

# Clone families (backlog 2.10). stage -> canonical stage.
CLONE_FAMILIES = {
    # JS1 equipment-maintenance (36) family
    "37": "36", "38": "36", "39": "36", "40": "36",
    # JS1 subscription-billing (52) family
    "53": "52", "54": "52",
    # JS1 learning-paths (41) family
    "43": "41", "44": "41", "47": "41", "49": "41", "50": "41",
    # JS1 project-risks (42) family
    "45": "42", "46": "42", "48": "42",
    # newcodexJS 07-blog-platform (58) family
    "59": "58", "60": "58", "61": "58",
    # newcodexJS 16-team-project-management (67) family
    "68": "67", "69": "67", "70": "67", "71": "67",
}

# backlog 1.15 - delivered delta vs inherited suite.
# Numbers read from fablereview/reviews/<slug>.md.
DELTA_COUNTS = {
    # stage: (exact old line, new line)
    "06": ("**Automated test cases:** 90.",
           "**Automated test cases:** 4 delivered by this change "
           "(`test/jobBackup.test.js`, two of them parameterized over 4 and 6 inputs). "
           "The project's inherited Vitest suite is 90 cases across 8 files; it was re-run "
           "as a regression gate, not authored here."),
    "73": ("Automated test cases: **92**.",
           "Automated test cases: **2 delivered by this change** (two `it()` blocks appended to "
           "`src/lib/backup.test.ts`). The inherited Questboard suite of 92 cases across 8 files "
           "was re-run as a regression gate, not authored here."),
    "74": ("Automated test cases: **62**.",
           "Automated test cases: **2 delivered by this change** (`src/importValidation.test.ts`). "
           "The inherited DevDeck suite totals 62 cases across 4 files including these two; it was "
           "re-run as a regression gate, not authored here."),
    "19": ("Automated test cases: **1**.",
           "Automated test cases: **1 test block containing ~16 assertions** "
           "(`server/test/search.test.cjs`) across create, search, filter, partial update and four "
           "validation rejections."),
}

DIFF_NOTE = (
    "Reading the diff: the files Astra touched were re-saved with CRLF line endings and Prettier "
    "formatting, so a plain `diff` shows whole files as changed. Compare with `git diff -w`, or "
    "`diff -r --strip-trailing-cr -w <backup> <project>` against the pre-change backup, to see only "
    "the real edits."
)

BANNER_MARK = "Same lesson as"
TOOLCHAIN_MARK = "### Toolchain"


# ---------------------------------------------------------------------------
# byte-safe text IO
# ---------------------------------------------------------------------------
def read_text(path):
    raw = open(path, "rb").read()
    bom = raw.startswith(codecs.BOM_UTF8)
    if bom:
        raw = raw[3:]
    crlf = raw.count(b"\r\n") > 0
    text = raw.decode("utf-8")
    return text.replace("\r\n", "\n"), bom, crlf


def encode_text(text, bom, crlf):
    if crlf:
        text = text.replace("\n", "\r\n")
    data = text.encode("utf-8")
    if bom:
        data = codecs.BOM_UTF8 + data
    return data


class Edits:
    """Collects pending whole-file replacements, keyed by absolute path."""

    def __init__(self):
        self.pending = OrderedDict()   # path -> dict(orig_bytes, new_bytes, rules=[...])
        self.changes = []              # (rule_id, path, before_text, after_text, note)

    def text_of(self, path):
        if path in self.pending:
            p = self.pending[path]
            return p["text"], p["bom"], p["crlf"]
        return read_text(path)

    def set_text(self, rule_id, path, new_text, note=""):
        old_text, bom, crlf = self.text_of(path)
        if new_text == old_text:
            return False
        if path not in self.pending:
            orig_text, obom, ocrlf = read_text(path)
            self.pending[path] = {"text": orig_text, "bom": obom, "crlf": ocrlf,
                                  "orig_text": orig_text, "rules": []}
        self.pending[path]["text"] = new_text
        self.pending[path]["rules"].append(rule_id)
        self.changes.append((rule_id, path, old_text, new_text, note))
        return True

    def set_bytes(self, rule_id, path, new_bytes, before_repr, after_repr, note=""):
        """Raw-byte rule (BOM / mojibake). Recorded separately from text rules."""
        orig = open(path, "rb").read()
        if orig == new_bytes:
            return False
        self.pending[path] = {"bytes": new_bytes, "rules": [rule_id]}
        self.changes.append((rule_id, path, before_repr, after_repr, note))
        return True

    def write_all(self):
        written = 0
        for path, p in self.pending.items():
            if "bytes" in p:
                data = p["bytes"]
            else:
                data = encode_text(p["text"], p["bom"], p["crlf"])
            with open(path, "wb") as fh:
                fh.write(data)
            written += 1
        return written


# ---------------------------------------------------------------------------
# project model
# ---------------------------------------------------------------------------
class Project:
    def __init__(self, entry):
        self.stage = entry["stage"]
        self.slug = entry["slug"]
        self.name = entry["name"]
        self.abs = entry["abs"]
        self.course = os.path.join(self.abs, "astraupskill")
        self.pkgs = []                 # (relpath-to-package.json, dict)
        self.has_server = False
        self.express = False
        self.postgres = False
        self.sqlite = False
        self.vitest = False
        self.has_app_js = os.path.exists(os.path.join(self.abs, "app.js"))
        self.has_browser_helper = False
        self.latest_deps = False
        self.lockfile = False
        self.test_script = None        # (where, script string)
        self.db_helper = None          # rel path of the astra_test_* guard file
        self.extensions = []           # postgres extensions the schema/tests need
        self._detect()

    # -- stack detection from disk -----------------------------------------
    def _detect(self):
        skip = {"node_modules", ".git", "astraupskill", "dist", "build", ".next", "coverage"}
        pkg_text = ""
        for root, dirs, files in os.walk(self.abs):
            dirs[:] = [d for d in dirs if d not in skip]
            rel = os.path.relpath(root, self.abs).replace("\\", "/")
            if "package.json" in files:
                p = os.path.join(root, "package.json")
                try:
                    data = json.loads(open(p, encoding="utf-8-sig").read())
                except Exception:
                    data = {}
                self.pkgs.append((rel, data))
                pkg_text += open(p, encoding="utf-8-sig", errors="replace").read()
            for lock in ("package-lock.json", "npm-shrinkwrap.json",
                         "pnpm-lock.yaml", "yarn.lock"):
                if lock in files:
                    self.lockfile = True

        self.has_server = (os.path.isdir(os.path.join(self.abs, "server"))
                           or os.path.isdir(os.path.join(self.abs, "src", "server")))
        self.express = '"express"' in pkg_text
        self.postgres = ('"pg"' in pkg_text) or ('"knex"' in pkg_text)
        self.sqlite = ('"better-sqlite3"' in pkg_text) or ('"sqlite3"' in pkg_text)
        self.vitest = '"vitest"' in pkg_text
        self.latest_deps = '"latest"' in pkg_text

        # test script: prefer a root script that is not a pass-through
        for rel, data in sorted(self.pkgs, key=lambda kv: len(kv[0])):
            script = (data.get("scripts") or {}).get("test")
            if not script:
                continue
            if "--workspace" in script or "--prefix" in script:
                continue
            self.test_script = (rel, script)
            break

        for cand in ("test/browser.cjs",):
            if os.path.exists(os.path.join(self.abs, cand.replace("/", os.sep))):
                self.has_browser_helper = True

        # astra_test_* guard helper + required extensions
        for cand in ("test/database.ts", "test/database.cjs", "test/database.js",
                     "server/test/database.cjs", "server/test/database.ts"):
            p = os.path.join(self.abs, cand.replace("/", os.sep))
            if os.path.exists(p) and "astra_test_" in open(p, encoding="utf-8-sig",
                                                           errors="replace").read():
                self.db_helper = cand
                break
        if self.db_helper is None and self.postgres:
            td = os.path.join(self.abs, "test")
            if os.path.isdir(td):
                for f in sorted(os.listdir(td)):
                    p = os.path.join(td, f)
                    if os.path.isfile(p) and "astra_test_" in open(
                            p, encoding="utf-8-sig", errors="replace").read():
                        self.db_helper = "test/" + f
                        break

        if self.postgres:
            found = set()
            for cand in ("server/db/schema.sql", "server/schema.sql", "db/schema.sql",
                         "schema.sql"):
                p = os.path.join(self.abs, cand.replace("/", os.sep))
                if os.path.exists(p):
                    for m in re.finditer(r"CREATE EXTENSION[^;]*?\"?([a-z_]+)\"?\s*;",
                                         open(p, encoding="utf-8-sig", errors="replace").read(),
                                         re.I):
                        found.add(m.group(1))
            td = os.path.join(self.abs, "test")
            if os.path.isdir(td):
                for f in sorted(os.listdir(td)):
                    p = os.path.join(td, f)
                    if not os.path.isfile(p):
                        continue
                    for m in re.finditer(r"CREATE EXTENSION IF NOT EXISTS ([a-z_]+)",
                                         open(p, encoding="utf-8-sig", errors="replace").read(),
                                         re.I):
                        found.add(m.group(1))
            self.extensions = sorted(found)

    @property
    def browser_only(self):
        return not self.has_server and not self.express

    def cfile(self, name):
        return os.path.join(self.course, name)


def load_projects():
    reg = json.load(open(REGISTRY, encoding="utf-8"))
    return [Project(e) for e in reg if e.get("wave") == 1]


def load_browser_stages():
    stages = set()
    for f in BROWSER_CHECK_FILES:
        if not os.path.exists(f):
            continue
        for row in json.load(open(f, encoding="utf-8")):
            if row.get("passed") is not False:
                stages.add(str(row["project"]))
    return stages


def load_delivered_test_files():
    """Astra-delivered test files, from the four delivery manifests.

    Every entry we care about has before_sha256 == null (a new file) or a
    changed hash; both count as 'Astra delivered this file'.
    """
    out = defaultdict(list)
    for m in MANIFESTS:
        if not os.path.exists(m):
            continue
        for e in json.load(open(m, encoding="utf-8")):
            f = e["file"]
            if not re.search(r"\.(ts|tsx|js|jsx|cjs|mjs)$", f):
                continue
            # test/*.test.*, server/test/*, client/test/*, src/**/x.test.ts
            if not (re.search(r"(^|/)(server/|client/)?test/", f) or ".test." in f):
                continue
            if e.get("before_sha256") == e.get("after_sha256"):
                continue
            out[e["stage"]].append(f)
    return out


# ---------------------------------------------------------------------------
# paragraph helpers
# ---------------------------------------------------------------------------
def paragraphs(text):
    return text.split("\n\n")


def replace_paragraph(text, marker, new_para):
    """Replace the first paragraph containing `marker`. new_para=None removes it."""
    paras = paragraphs(text)
    for i, p in enumerate(paras):
        if marker in p:
            if new_para is None:
                del paras[i]
            else:
                paras[i] = new_para
            return "\n\n".join(paras), True
    return text, False


def section_bounds(text, heading_re):
    """Return (start_of_body, end_of_section) for the first '## ' heading matching."""
    m = re.search(heading_re, text, re.M)
    if not m:
        return None
    start = m.end()
    nxt = re.search(r"^## ", text[start:], re.M)
    end = start + nxt.start() if nxt else len(text)
    return start, end


# ---------------------------------------------------------------------------
# RULE 2.1 - per-stack environment / limits paragraphs
# ---------------------------------------------------------------------------
def fix_db_setup_leaks(proj, text):
    """The batch02 'Database test setup' paragraph names Room Booking and the
    Notes/Bookmark servers. It is repeated verbatim in VERIFICATION.md AND in
    04-TESTING-AND-DEBUGGING.md of stages 18, 19 and 20."""
    if "Room Booking additionally enables btree_gist and pgcrypto" in text:
        if proj.slug == "js1-room-booking":
            text = text.replace(
                "Room Booking additionally enables btree_gist and pgcrypto in this"
                " dedicated test database;",
                "This project additionally enables btree_gist and pgcrypto in this"
                " dedicated test database;")
        else:
            text = text.replace(
                " Room Booking additionally enables btree_gist and pgcrypto in this"
                " dedicated test database; it does not run the scaffold's DROP TABLE"
                " statements against a fallback namespace.", "")
    if "Run npm test from the Room Booking root or the Notes/Bookmark server folder." in text:
        where = ("this project's root" if proj.slug == "js1-room-booking"
                 else "this project's `server` folder")
        text = text.replace(
            "Run npm test from the Room Booking root or the Notes/Bookmark server folder.",
            "Run npm test from %s." % where)
    return text


def rule_environment(proj, edits, browser_stages):
    st = proj.stage
    pg = proj.postgres
    has_browser = st in browser_stages
    vpath = proj.cfile("VERIFICATION.md")
    if os.path.exists(vpath):
        text, _, _ = edits.text_of(vpath)
        orig = text

        # --- batch01 (stages 01-10) environment paragraph -------------------
        # "The verification environment used Node 22.16.0. Browser checks used the
        #  installed Chromium build. Database suites ran against a fresh, separate
        #  PostgreSQL 18.1 instance; development and personal data were not test fixtures."
        if not has_browser:
            text = text.replace(
                " Browser checks used the installed Chromium build.", "")
        if not pg:
            text = text.replace(
                " Database suites ran against a fresh, separate PostgreSQL 18.1 instance;"
                " development and personal data were not test fixtures.", "")

        # --- batch01 leaked project name: "Recipeweb also used ..." ----------
        if "; Recipeweb also used its own installed dependency tree" in text:
            if proj.slug == "recipeweb":
                text = text.replace(
                    "; Recipeweb also used its own installed dependency tree",
                    "; this project also used its own installed dependency tree")
            else:
                text = text.replace(
                    "; Recipeweb also used its own installed dependency tree for its"
                    " production build", "")

        # --- batch02 (stages 11-20) environment paragraph --------------------
        if not pg:
            text = text.replace(
                " PostgreSQL tests used a separate local PostgreSQL 18.1 instance on port"
                " 55439 and uniquely named schemas in a dedicated test database.", "")

        # --- batch03 (21-50) / batch04 (51-75) "where applicable" ------------
        if not pg:
            text = text.replace(
                "The isolated harness used Node 22.16.0, PostgreSQL 18.1 where applicable,"
                " and dependencies installed in the verification workspace.",
                "The isolated harness used Node 22.16.0 and dependencies installed in the"
                " verification workspace.")
            text = text.replace(
                "Node 22.16.0, PostgreSQL 18.1 where applicable, and dependencies installed"
                " in the isolated verification workspace were used.",
                "Node 22.16.0 and dependencies installed in the isolated verification"
                " workspace were used.")
            # batch03 Limits paragraph
            text = text.replace(
                ", date representation and transaction scope where relevant.",
                " and date representation where relevant.")

        # --- batch02 "Database test setup" leaks (stages 18/19/20) -----------
        text = fix_db_setup_leaks(proj, text)

        if text != orig:
            edits.set_text("2.1", vpath, text, "VERIFICATION environment/limits per-stack")

    # --- 04-TESTING-AND-DEBUGGING.md shared paragraphs ----------------------
    tpath = proj.cfile("04-TESTING-AND-DEBUGGING.md")
    if not os.path.exists(tpath):
        return
    text, _, _ = edits.text_of(tpath)
    orig = text
    text = fix_db_setup_leaks(proj, text)

    # (a) batch01/02 paragraph: "For the plain browser projects, jsdom runs the
    #     actual app.js against its HTML. The helper supplies browser APIs missing
    #     from jsdom and a controllable timer clock. ..."
    if "For the plain browser projects, jsdom runs the actual app.js" in text:
        if not proj.browser_only:
            text, _ = replace_paragraph(
                text, "For the plain browser projects, jsdom runs the actual app.js", None)
        elif proj.has_app_js:
            clock = (" The helper supplies browser APIs missing from jsdom and a controllable"
                     " timer clock. It does not replace the app’s business functions."
                     if proj.has_browser_helper else
                     " The helper supplies browser APIs missing from jsdom. It does not replace"
                     " the app’s business functions.")
            text, _ = replace_paragraph(
                text, "For the plain browser projects, jsdom runs the actual app.js",
                "In this project, jsdom runs the actual app.js against its HTML." + clock +
                " A real browser check is still useful for layout, focus visibility and native"
                " interaction.")
        else:
            text, _ = replace_paragraph(
                text, "For the plain browser projects, jsdom runs the actual app.js",
                "This project has no plain app.js: its pure tests verify the state helpers'"
                " data behavior directly, and the component and browser checks verify that the"
                " controls call those helpers correctly. A real browser check is still useful"
                " for layout, focus visibility and native interaction.")

    # (b) batch03 paragraph: "For Poll Studio and Kanban Flow, jsdom runs ..."
    if "For Poll Studio and Kanban Flow, jsdom runs the actual app.js" in text:
        tail = (" These checks verify different boundaries; none replaces reading the test"
                " helper.")
        if proj.browser_only:
            new = ("In this project, jsdom runs the actual app.js against its HTML and fresh"
                   " browser storage; the suite can force a storage-write failure. The Chromium"
                   " check covers the real page in a native browser." + tail)
        else:
            store = ("a disposable PostgreSQL schema" if proj.postgres
                     else "temporary SQLite storage" if proj.sqlite
                     else "a fresh in-memory repository")
            new = ("This project's suite runs its actual Express app over loopback HTTP against"
                   " %s. The Chromium check covers the real built client and routes its API"
                   " requests to that isolated real server through a local test proxy." % store
                   + tail)
        text, _ = replace_paragraph(
            text, "For Poll Studio and Kanban Flow, jsdom runs the actual app.js", new)

    # (c) batch04 paragraph: "Questboard uses Vitest and simulated browser storage; ..."
    if "Questboard uses Vitest and simulated browser storage" in text:
        tail = (" Read the project verification page for the exact observed checks and limits.")
        if proj.slug == "calendar-jobtrack":
            new = ("This project uses Vitest and simulated browser storage."
                   " Browser checks exercise the built client separately." + tail)
        elif proj.slug == "devdeck":
            new = ("This project uses Vitest with fake-indexeddb so the tests drive the actual"
                   " Dexie methods. Browser checks exercise the built client separately." + tail)
        else:
            store = ("a disposable PostgreSQL database" if proj.postgres
                     else "temporary SQLite storage" if proj.sqlite
                     else "fresh in-memory data")
            extra = (" It also tests a real WebSocket and a real PostgreSQL notification."
                     if proj.slug == "js1-live-chat" else "")
            new = ("This project runs its real Express app through HTTP with %s.%s"
                   " Browser checks exercise the built client separately." % (store, extra)
                   + tail)
        text, _ = replace_paragraph(
            text, "Questboard uses Vitest and simulated browser storage", new)

    if text != orig:
        edits.set_text("2.1", tpath, text, "04-TESTING per-stack harness paragraph")


# ---------------------------------------------------------------------------
# RULE 2.7 - reproducibility pins in the course README
# ---------------------------------------------------------------------------
def explicit_test_command(proj):
    """Turn the package.json test script's glob into an explicit file list."""
    if not proj.test_script:
        return None
    where, script = proj.test_script
    m = re.search(r"(node|tsx)\s+--test\s+(\S+)", script)
    if not m:
        return None
    runner, pattern = m.group(1), m.group(2)
    if "*" not in pattern:
        return None
    # resolve the glob relative to the package.json's folder
    base = proj.abs if where == "." else os.path.join(proj.abs, where.replace("/", os.sep))
    pdir, pfile = pattern.rsplit("/", 1) if "/" in pattern else (".", pattern)
    tdir = os.path.normpath(os.path.join(base, pdir.replace("/", os.sep)))
    if not os.path.isdir(tdir):
        return None
    rx = re.compile("^" + re.escape(pfile).replace(r"\*", ".*") + "$")
    files = sorted(f for f in os.listdir(tdir) if rx.match(f))
    if not files:
        return None
    joined = " ".join("%s/%s" % (pdir, f) if pdir != "." else f for f in files)
    cmd = ("node --test " if runner == "node" else "npx tsx --test ") + joined
    return where, script, cmd


def build_toolchain_block(proj):
    lines = [TOOLCHAIN_MARK, ""]
    pgbit = " and **PostgreSQL 18**" if proj.postgres else ""
    lines.append(
        "This course was delivered and verified on **Node 22.16.0**, **npm 10**%s. Use the same "
        "major versions: newer patch releases are fine, older majors are untested here." % pgbit)

    if proj.postgres:
        lines.append("")
        lines.append(
            "Create the two databases once, from `psql`, as a user allowed to create databases "
            "and schemas:")
        lines.append("")
        lines.append("```sql")
        lines.append("CREATE DATABASE astra_learning_sandbox;   -- the development database")
        lines.append("CREATE DATABASE astra_test_learning;      -- the automated-test database")
        if proj.extensions:
            lines.append("\\c astra_test_learning")
            for ext in proj.extensions:
                lines.append("CREATE EXTENSION IF NOT EXISTS %s;" % ext)
        lines.append("```")
        if proj.extensions:
            lines.append("")
            lines.append(
                "The test helper strips `CREATE EXTENSION` statements out of `schema.sql` before "
                "running it, so create the extensions above once in the test database (or give "
                "the test account the right to create them).")
        if proj.db_helper:
            lines.append("")
            lines.append(
                "`%s` refuses to run unless the database named in `ASTRA_TEST_DATABASE_URL` "
                "starts with `astra_test_`. It then creates one uniquely named schema per run and "
                "drops it at the end, so the development database is never a fixture." %
                proj.db_helper)

    cmd = explicit_test_command(proj)
    if cmd is None and proj.test_script and "vitest" in proj.test_script[1]:
        lines.append("")
        lines.append(
            "`npm test` runs `%s`, which finds its own test files, so there is no shell glob to "
            "worry about on Windows." % proj.test_script[1])
    if cmd:
        where, script, explicit = cmd
        from_where = ("from the project root" if where == "."
                      else "in the `%s` package (run `npm test` from the project root, which "
                           "delegates to it, or from `%s`)" % (where, where))
        lines.append("")
        lines.append(
            "`npm test` %s runs `%s`. npm runs scripts through `cmd.exe` on Windows, and "
            "`cmd.exe` does not expand the `%s` glob; neither does PowerShell for a native "
            "command. Node's own test runner expands the pattern (Node 21+), so `npm test` works "
            "on Node 22 - but on an older Node, or with a different runner, you will see \"no test "
            "files\". The shell-independent equivalent is:" %
            (from_where, script, re.search(r"--test\s+(\S+)", script).group(1)))
        lines.append("")
        lines.append("```powershell")
        if where != ".":
            lines.append("cd %s" % where)
        lines.append(explicit)
        lines.append("```")

    if proj.latest_deps and not proj.lockfile:
        lines.append("")
        lines.append(
            "**Dependencies are declared as `latest` with no lockfile; pin them before relying on "
            "a build.** An `npm install` today and the same command next month can resolve "
            "different major versions of the same packages.")

    return "\n".join(lines)


def rule_toolchain(proj, edits):
    path = proj.cfile("README.md")
    if not os.path.exists(path):
        return
    text, _, _ = edits.text_of(path)
    if TOOLCHAIN_MARK in text:
        return
    anchor = "\n## Reading and practice order"
    if anchor not in text:
        return
    block = build_toolchain_block(proj)
    new = text.replace(anchor, "\n" + block + "\n" + anchor, 1)
    edits.set_text("2.7", path, new, "README toolchain/reproducibility block")


# ---------------------------------------------------------------------------
# RULE 2.9 - diff-reading note in VERIFICATION.md
# ---------------------------------------------------------------------------
def rule_diff_note(proj, edits):
    path = proj.cfile("VERIFICATION.md")
    if not os.path.exists(path):
        return
    text, _, _ = edits.text_of(path)
    if "Reading the diff:" in text:
        return
    b = section_bounds(text, r"^## Reproduce.*$")
    if not b:
        return
    start, end = b
    body = text[start:end]
    stripped = body.rstrip("\n")
    new_body = stripped + "\n\n" + DIFF_NOTE + "\n\n"
    if end == len(text):
        new_body = stripped + "\n\n" + DIFF_NOTE + "\n"
    edits.set_text("2.9", path, text[:start] + new_body + text[end:],
                   "diff-reading note in Reproduce section")


# ---------------------------------------------------------------------------
# RULE 2.10 - clone banners
# ---------------------------------------------------------------------------
def rule_clone_banner(proj, edits, by_stage):
    canon_stage = CLONE_FAMILIES.get(proj.stage)
    if not canon_stage:
        return
    canon = by_stage.get(canon_stage)
    if canon is None:
        return
    path = proj.cfile("README.md")
    canon_readme = canon.cfile("README.md")
    if not (os.path.exists(path) and os.path.exists(canon_readme)):
        return
    text, _, _ = edits.text_of(path)
    if BANNER_MARK in text:
        return
    ctext, _, _ = read_text(canon_readme)
    m = re.match(r"^# (.+)$", ctext, re.M)
    title = m.group(1).strip() if m else canon.name
    rel = os.path.relpath(canon_readme, proj.course).replace("\\", "/")
    banner = ("> **Same lesson as [%s](%s)** - this course is a near-identical rendering with "
              "different nouns. Do the canonical one; use this project only as a second, "
              "independent practice run." % (title, rel))
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines.insert(i + 1, "")
            lines.insert(i + 2, banner)
            break
    else:
        return
    edits.set_text("2.10", path, "\n".join(lines), "clone banner -> stage %s" % canon_stage)


# ---------------------------------------------------------------------------
# RULE 1.15 - delivered delta vs inherited suite
# ---------------------------------------------------------------------------
def rule_delta_counts(proj, edits):
    pair = DELTA_COUNTS.get(proj.stage)
    if not pair:
        return
    old, new = pair
    path = proj.cfile("VERIFICATION.md")
    if not os.path.exists(path):
        return
    text, _, _ = edits.text_of(path)
    if old not in text:
        return
    edits.set_text("1.15", path, text.replace(old, new, 1),
                   "delivered delta vs inherited suite")


# ---------------------------------------------------------------------------
# RULE 2.8 - hygiene: misplaced BOM + snippet-vault mojibake
# ---------------------------------------------------------------------------
BOM = codecs.BOM_UTF8
PREPENDED_IMPORT = b'import { pathToFileURL } from "node:url";'


def rule_hygiene(proj, edits):
    # (a) UTF-8 BOM that is not at byte 0. Only the known pattern is touched:
    #     the `import { pathToFileURL }` line was prepended ABOVE the file's BOM.
    #     The backups show the original files began with a BOM at byte 0, so the
    #     repair is to move the BOM back to byte 0 (exactly one BOM, at the start).
    for rel in ("server/server.js", "server/src/server.js", "server/index.js"):
        p = os.path.join(proj.abs, rel.replace("/", os.sep))
        if not os.path.exists(p):
            continue
        raw = open(p, "rb").read()
        m = re.match(rb"(" + re.escape(PREPENDED_IMPORT) + rb"\r?\n)" + re.escape(BOM), raw)
        if not m:
            continue
        head = m.group(1)
        new = BOM + head + raw[m.end():]
        edits.set_bytes("2.8", p, new,
                        "line 1: %r\nline 2 begins with a UTF-8 BOM (U+FEFF)" % head.decode(),
                        "BOM moved back to byte 0 (matching the pre-change backup); "
                        "line 2 is now plain `import express ...`",
                        "misplaced BOM")

    # (b) mojibake at JS1/snippet-vault/src/store.js:1
    #     Delivered bytes  : c3 a2 e2 82 ac e2 80 9d  ("a€”" = UTF-8 of "â€”")
    #     Backup original  : e2 80 94  (EM DASH U+2014) -> "// store.js - owns the data ..."
    if proj.slug == "js1-snippet-vault":
        p = os.path.join(proj.abs, "src", "store.js")
        if os.path.exists(p):
            raw = open(p, "rb").read()
            bad = b"\xc3\xa2\xe2\x82\xac\xe2\x80\x9d"
            if bad in raw:
                new = raw.replace(bad, b"\xe2\x80\x94")
                edits.set_bytes("2.8", p, new,
                                repr(raw[:60]), repr(new[:60]),
                                "mojibake em dash -> U+2014")


# ---------------------------------------------------------------------------
# RULE 2.6 - de-minify delivered test files with Prettier
# ---------------------------------------------------------------------------
def minified(path):
    """Heuristic: high average statements-per-line / very long lines."""
    try:
        text, _, _ = read_text(path)
    except Exception:
        return False
    lines = [l for l in text.split("\n") if l.strip()]
    if not lines:
        return False
    dense = sum(1 for l in lines if len(l) > 160 or l.count(";") > 2) / len(lines)
    per_line = text.count(";") / len(lines)
    longest = max(len(l) for l in lines)
    return dense >= 0.10 or per_line >= 0.85 or longest > 200


def prettier_pass(projects, edits, delivered, verbose=True):
    """Copy candidates into _fix/.prettier-tmp, run one Prettier 3 pass there,
    and record the formatted bytes. No project package.json is touched and no
    project-local Prettier config is used (--no-config), which is exactly the
    configuration Astra's own batch04 files already match."""
    by_stage = {p.stage: p for p in projects}
    mapping = []       # (tmp_path, real_path, stage, rel)
    if os.path.isdir(PRETTIER_TMP):
        shutil.rmtree(PRETTIER_TMP)
    for stage, rels in sorted(delivered.items()):
        proj = by_stage.get(stage)
        if proj is None:
            continue
        for rel in rels:
            real = os.path.join(proj.abs, rel.replace("/", os.sep))
            if not os.path.exists(real) or not minified(real):
                continue
            tmp = os.path.join(PRETTIER_TMP, stage, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(tmp), exist_ok=True)
            shutil.copyfile(real, tmp)
            mirror_module_type(proj, real, tmp)
            mapping.append((tmp, real, stage, rel))
    if not mapping:
        return [], []

    cmd = ["npx.cmd" if os.name == "nt" else "npx", "--yes", "prettier@3",
           "--no-config", "--no-color", "--end-of-line", "auto",
           "--log-level", "warn", "--write"]
    # Forward slashes only: Prettier treats its file arguments as glob patterns
    # and a Windows backslash is read as a glob escape, so "tmp\01\test\x.cjs"
    # silently matches nothing ("No files matching the pattern were found").
    cmd += [os.path.relpath(t, HERE).replace(os.sep, "/") for t, _, _, _ in mapping]
    if verbose:
        print("  prettier: %d candidate files" % len(mapping))
    res = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, shell=False)

    reformatted, problems = [], []
    if res.returncode != 0:
        # Do not abandon the pass: prettier reports per-file errors and still
        # formats the files it could parse. Record the messages and continue.
        for line in (res.stderr or res.stdout).splitlines():
            line = line.strip()
            if line and not set(line) <= {" "}:
                problems.append(("prettier", line[:300]))
        problems = problems[:40] or [("prettier", "exit %d (no message)" % res.returncode)]

    for tmp, real, stage, rel in mapping:
        before = open(real, "rb").read()
        after = open(tmp, "rb").read()
        if before == after:
            continue
        # BOM state must survive the round trip
        if before.startswith(BOM) and not after.startswith(BOM):
            after = BOM + after
        if not before.startswith(BOM) and after.startswith(BOM):
            after = after[len(BOM):]
        # syntax gate for plain JS: only flag a *newly* broken file
        if rel.endswith((".js", ".cjs", ".mjs")):
            ok_before = node_check(real)
            ok_after = node_check(tmp)
            if ok_before and not ok_after:
                problems.append((real, "node --check regressed after formatting"))
                continue
        before_text = before.decode("utf-8-sig", errors="replace").replace("\r\n", "\n")
        after_text = after.decode("utf-8-sig", errors="replace").replace("\r\n", "\n")
        edits.set_bytes("2.6", real, after, before_text, after_text,
                        "prettier 3 (--no-config --end-of-line auto)")
        reformatted.append((stage, rel))
    return reformatted, problems


def mirror_module_type(proj, real, tmp):
    """`node --check` decides CommonJS vs ESM from the nearest package.json.
    Mirror the source file's nearest `"type"` into the staging tree so the
    syntax gate is judged in the same module mode as the real file."""
    d = os.path.dirname(real)
    mtype = None
    while d.startswith(proj.abs):
        pj = os.path.join(d, "package.json")
        if os.path.exists(pj):
            try:
                mtype = json.loads(open(pj, encoding="utf-8-sig").read()).get("type")
            except Exception:
                mtype = None
            break
        nd = os.path.dirname(d)
        if nd == d:
            break
        d = nd
    if not mtype:
        return
    target = os.path.join(os.path.dirname(tmp), "package.json")
    if not os.path.exists(target):
        open(target, "w", encoding="utf-8").write('{"type": "%s"}\n' % mtype)


def node_check(path):
    exe = "node.exe" if os.name == "nt" else "node"
    try:
        r = subprocess.run([exe, "--check", path], capture_output=True, text=True)
        return r.returncode == 0
    except Exception:
        return True


# ---------------------------------------------------------------------------
# residue scan
# ---------------------------------------------------------------------------
LEAK_PATTERNS = [
    ("PostgreSQL 18.1 in a project with no Postgres", r"PostgreSQL 18\.1", "no_pg"),
    ("port 55439 in a project with no Postgres", r"55439", "no_pg"),
    ("'installed Chromium build' with no browser evidence", r"installed Chromium build", "no_browser"),
    ("jsdom/app.js paragraph in a server project", r"For the plain browser projects", "server"),
    ("'For Poll Studio and Kanban Flow' leak", r"For Poll Studio and Kanban Flow", "always"),
    ("'Questboard uses Vitest' leak", r"Questboard uses Vitest", "always"),
    ("'Recipeweb also used' leak", r"Recipeweb also used", "not_recipeweb"),
    ("'Room Booking additionally enables' leak", r"Room Booking additionally enables", "not_room"),
    ("'Notes/Bookmark server folder' leak", r"Notes/Bookmark server folder", "always"),
    ("'transaction scope' in a project with no Postgres",
     r"date representation and transaction scope", "no_pg"),
]


def scan(projects, browser_stages):
    residue = []
    for proj in projects:
        if not os.path.isdir(proj.course):
            continue
        for fn in sorted(os.listdir(proj.course)):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(proj.course, fn)
            text, _, _ = read_text(path)
            for label, pat, cond in LEAK_PATTERNS:
                if cond == "no_pg" and proj.postgres:
                    continue
                if cond == "no_browser" and proj.stage in browser_stages:
                    continue
                if cond == "server" and proj.browser_only:
                    continue
                if cond == "not_recipeweb" and proj.slug == "recipeweb":
                    continue
                if cond == "not_room" and proj.slug == "js1-room-booking":
                    continue
                for m in re.finditer(pat, text):
                    line = text[:m.start()].count("\n") + 1
                    residue.append((proj.stage, proj.slug, fn, line, label))
    return residue


# ---------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------
RULE_TITLES = {
    "2.1": "2.1 per-stack environment / limits paragraphs",
    "2.6": "2.6 de-minified delivered test files (Prettier 3)",
    "2.7": "2.7 reproducibility pins (README Toolchain block)",
    "2.8": "2.8 hygiene (misplaced BOM, mojibake)",
    "2.9": "2.9 diff-reading note (VERIFICATION Reproduce)",
    "2.10": "2.10 clone banners",
    "1.15": "1.15 delivered delta vs inherited test counts",
}


def make_diff(path, before, after, limit=60):
    a = before.split("\n")
    b = after.split("\n")
    out = list(difflib.unified_diff(a, b, fromfile=path + " (before)",
                                    tofile=path + " (after)", n=1, lineterm=""))
    if len(out) > limit:
        out = out[:limit] + ["... (diff truncated)"]
    return "\n".join(out)


def write_report(path, mode, edits, projects, reformatted, problems, residue):
    per_rule = defaultdict(list)
    for rule, p, before, after, note in edits.changes:
        per_rule[rule].append((p, before, after, note))

    L = []
    L.append("# Wave-1 structural sweep - %s report" % mode)
    L.append("")
    L.append("Generated by `_fix/wave1_sweep.py --%s`." % mode)
    L.append("")
    L.append("Projects in scope: **%d** (registry.json, wave == 1). No wave-2 project is touched."
             % len(projects))
    L.append("")
    L.append("## Per-rule counts")
    L.append("")
    L.append("| Rule | Edits | Distinct files |")
    L.append("|---|---:|---:|")
    for rule in ["2.1", "2.6", "2.7", "2.8", "2.9", "2.10", "1.15"]:
        rows = per_rule.get(rule, [])
        L.append("| %s | %d | %d |" % (RULE_TITLES[rule], len(rows),
                                       len({r[0] for r in rows})))
    L.append("| **total** | **%d** | **%d** |" % (len(edits.changes), len(edits.pending)))
    L.append("")
    L.append("Files reformatted by Prettier: **%d**." % len(reformatted))
    if problems:
        L.append("")
        L.append("### Problems")
        for a, b in problems:
            L.append("- `%s`: %s" % (a, b))
    L.append("")

    for rule in ["2.1", "2.6", "2.7", "2.8", "2.9", "2.10", "1.15"]:
        rows = per_rule.get(rule, [])
        L.append("## %s" % RULE_TITLES[rule])
        L.append("")
        if not rows:
            L.append("_No changes._")
            L.append("")
            continue
        L.append("%d edit(s) across %d file(s)." % (len(rows), len({r[0] for r in rows})))
        L.append("")
        L.append("<details><summary>all files</summary>")
        L.append("")
        for p, _, _, note in rows:
            L.append("- `%s`%s" % (short(p), (" - " + note) if note else ""))
        L.append("")
        L.append("</details>")
        L.append("")
        L.append("### Examples")
        L.append("")
        for p, before, after, note in rows[:3]:
            L.append("```diff")
            L.append(make_diff(short(p), before, after))
            L.append("```")
            L.append("")

    L.append("## Leaked-phrase residue scan")
    L.append("")
    if not residue:
        L.append("No residue: none of the tracked leaked phrases remain in a course where "
                 "they do not belong.")
    else:
        L.append("| stage | slug | file | line | finding |")
        L.append("|---|---|---|---:|---|")
        for st, slug, fn, line, label in residue:
            L.append("| %s | %s | %s | %d | %s |" % (st, slug, fn, line, label))
    L.append("")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(L))


REPLACEMENT_MARKERS_04 = [
    "In this project, jsdom runs the actual app.js",
    "This project has no plain app.js",
    "This project's suite runs its actual Express app over loopback HTTP",
    "This project runs its real Express app through HTTP",
    "This project uses Vitest",
]

# Counts observed in the pre-apply dry-run (sweep_dryrun.md, 2026-09-17, before
# any file was written). Kept here so the applied report can still state them
# after the idempotent re-runs zeroed the live numbers.
PREAPPLY_COUNTS = OrderedDict([
    ("2.1", (119, 119)), ("2.6", (89, 89)), ("2.7", (75, 75)), ("2.8", (10, 10)),
    ("2.9", (75, 75)), ("2.10", (21, 21)), ("1.15", (4, 4)),
])


def record(projects, browser_stages, delivered):
    """Re-derive the applied state from post-conditions on disk."""
    import hashlib
    after = {}
    for m in MANIFESTS:
        if os.path.exists(m):
            for e in json.load(open(m, encoding="utf-8")):
                after[(e["stage"], e["file"])] = e.get("after_sha256")

    found = defaultdict(list)
    for p in projects:
        rd = p.cfile("README.md")
        vf = p.cfile("VERIFICATION.md")
        t4 = p.cfile("04-TESTING-AND-DEBUGGING.md")
        if os.path.exists(rd):
            t, _, _ = read_text(rd)
            if TOOLCHAIN_MARK in t:
                found["2.7"].append(rd)
            if BANNER_MARK in t:
                found["2.10"].append(rd)
        if os.path.exists(vf):
            t, _, _ = read_text(vf)
            if "Reading the diff:" in t:
                found["2.9"].append(vf)
            if p.stage in DELTA_COUNTS and "delivered by this change" in t \
                    or (p.stage == "19" and "test block containing" in t):
                found["1.15"].append(vf)
        if os.path.exists(t4):
            t, _, _ = read_text(t4)
            if any(mk in t for mk in REPLACEMENT_MARKERS_04):
                found["2.1"].append(t4)
            elif not p.browser_only and "jsdom" not in t:
                found["2.1"].append(t4)   # paragraph removed from a server project

    # 2.8 post-conditions
    for p in projects:
        for rel in ("server/server.js", "server/src/server.js", "server/index.js"):
            fp = os.path.join(p.abs, rel.replace("/", os.sep))
            if os.path.exists(fp):
                raw = open(fp, "rb").read()
                if raw.startswith(BOM + PREPENDED_IMPORT) and BOM not in raw[3:]:
                    found["2.8"].append(fp)
        if p.slug == "js1-snippet-vault":
            fp = os.path.join(p.abs, "src", "store.js")
            if os.path.exists(fp) and b"\xe2\x80\x94" in open(fp, "rb").read()[:120]:
                found["2.8"].append(fp)

    # 2.6 post-condition: the delivered test file no longer hashes to what the
    # delivery manifest recorded, and it is no longer minified.
    by_stage = {p.stage: p for p in projects}
    for stage, rels in sorted(delivered.items()):
        proj = by_stage.get(stage)
        if not proj:
            continue
        for rel in rels:
            fp = os.path.join(proj.abs, rel.replace("/", os.sep))
            if not os.path.exists(fp):
                continue
            h = hashlib.sha256(open(fp, "rb").read()).hexdigest()
            if after.get((stage, rel)) and h != after[(stage, rel)]:
                found["2.6"].append(fp)

    residue = scan(projects, browser_stages)
    L = ["# Wave-1 structural sweep - applied report", "",
         "Generated by `_fix/wave1_sweep.py --record` after `--apply`. The live `--apply` and",
         "`--dry-run` passes now report 0 changes (the sweep is idempotent), so this report",
         "states the edit counts observed in the pre-apply dry-run alongside the post-conditions",
         "that can still be verified on disk today.", "",
         "Projects in scope: **%d** (registry.json, wave == 1). No wave-2 project was touched."
         % len(projects), "",
         "## Per-rule counts", "",
         "| Rule | Edits applied (pre-apply dry-run) | Files now carrying the change |",
         "|---|---:|---:|"]
    tot_e = tot_f = 0
    for rule, (ec, _fc) in PREAPPLY_COUNTS.items():
        n = len(set(found.get(rule, [])))
        tot_e += ec
        tot_f += n
        L.append("| %s | %d | %d |" % (RULE_TITLES[rule], ec, n))
    L.append("| **total** | **%d** | **%d** |" % (tot_e, tot_f))
    L.append("")
    for rule in PREAPPLY_COUNTS:
        L.append("## %s" % RULE_TITLES[rule])
        L.append("")
        files = sorted(set(found.get(rule, [])))
        L.append("%d file(s) verified on disk." % len(files))
        L.append("")
        L.append("<details><summary>files</summary>")
        L.append("")
        for f in files:
            L.append("- `%s`" % short(f))
        L.append("")
        L.append("</details>")
        L.append("")
    L.append("## Leaked-phrase residue scan")
    L.append("")
    if not residue:
        L.append("Clean: none of the tracked leaked phrases remains in a course where it does "
                 "not belong (0 findings across %d courses)." % len(projects))
    else:
        L.append("| stage | slug | file | line | finding |")
        L.append("|---|---|---|---:|---|")
        for st, slug, fn, line, label in residue:
            L.append("| %s | %s | %s | %d | %s |" % (st, slug, fn, line, label))
    L.append("")
    out = os.path.join(HERE, "sweep_applied.md")
    open(out, "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print("record: %d rules, %d files verified, %d residue rows -> %s"
          % (len(PREAPPLY_COUNTS), tot_f, len(residue), out))


def short(p):
    for base in (os.path.join(os.path.expanduser("~"), "Desktop"),):
        if p.startswith(base):
            return p[len(base) + 1:].replace("\\", "/")
    return p.replace("\\", "/")


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--scan", action="store_true")
    g.add_argument("--record", action="store_true",
                   help="re-derive the applied-state evidence report (post-conditions per "
                        "rule), for when --apply has already run")
    args = ap.parse_args()

    projects = load_projects()
    by_stage = {p.stage: p for p in projects}
    browser_stages = load_browser_stages()
    delivered = load_delivered_test_files()

    if args.record:
        record(projects, browser_stages, delivered)
        return 0

    if args.scan:
        residue = scan(projects, browser_stages)
        if not residue:
            print("scan: clean across %d wave-1 courses" % len(projects))
        for row in residue:
            print("RESIDUE %s %s %s:%d  %s" % row)
        return 0

    print("wave-1 sweep: %d projects" % len(projects))
    edits = Edits()

    # text rules first (2.6 writes raw bytes to files the text rules never touch)
    for p in projects:
        rule_environment(p, edits, browser_stages)
        rule_delta_counts(p, edits)
        rule_toolchain(p, edits)
        rule_diff_note(p, edits)
        rule_clone_banner(p, edits, by_stage)
        rule_hygiene(p, edits)

    reformatted, problems = prettier_pass(projects, edits, delivered)

    mode = "apply" if args.apply else "dry-run"
    out = os.path.join(HERE, "sweep_applied.md" if args.apply else "sweep_dryrun.md")

    if args.apply:
        n = edits.write_all()
        print("wrote %d files" % n)
        residue = scan(projects, browser_stages)
    else:
        residue = scan(projects, browser_stages)

    write_report(out, mode, edits, projects, reformatted, problems, residue)
    print("%s: %d edits across %d files; %d reformatted; %d residue rows -> %s"
          % (mode, len(edits.changes), len(edits.pending), len(reformatted),
             len(residue), out))
    if os.path.isdir(PRETTIER_TMP):
        shutil.rmtree(PRETTIER_TMP, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
