from pathlib import Path
s=Path('astra-remaining-improvements/stage/da9c28730758')
(s/'applybot/profile.py').write_text('''"""Bounded profile loading; unknown boolean answers remain unknown."""
from __future__ import annotations

import math
from pathlib import Path

import yaml

MAX_PROFILE_BYTES = 256 * 1024
MAPPING_SECTIONS = {"personal", "links", "documents", "work_authorization", "background", "preferences", "canned_answers", "eeo"}

class ProfileError(ValueError):
    pass


def validate_profile(value: object) -> dict:
    if not isinstance(value, dict):
        raise ProfileError("Profile YAML must be a mapping of named sections.")
    active, count = set(), 0
    def copy(item, depth=0):
        nonlocal count
        count += 1
        if depth > 12 or count > 10000:
            raise ProfileError("Profile nesting or size exceeds the supported limit.")
        if item is None or isinstance(item, bool):
            return item
        if isinstance(item, (int, float)) and not isinstance(item, bool):
            if not math.isfinite(item):
                raise ProfileError("Profile numbers must be finite.")
            return item
        if isinstance(item, str):
            if len(item) > 10000:
                raise ProfileError("Profile text fields are limited to 10,000 characters.")
            return item
        if not isinstance(item, (dict, list)):
            raise ProfileError("Profile values must be plain mappings, lists, text, booleans or numbers.")
        identity = id(item)
        if identity in active:
            raise ProfileError("Recursive YAML aliases are not supported.")
        if len(item) > 1000:
            raise ProfileError("Profile collections are limited to 1,000 entries.")
        active.add(identity)
        try:
            if isinstance(item, list):
                return [copy(child, depth + 1) for child in item]
            if any(not isinstance(key, str) or not key or len(key) > 256 for key in item):
                raise ProfileError("Profile mapping keys must be bounded nonempty text.")
            return {key: copy(child, depth + 1) for key, child in item.items()}
        finally:
            active.remove(identity)
    profile = copy(value)
    for section in MAPPING_SECTIONS:
        if section in profile and not isinstance(profile[section], dict):
            raise ProfileError(f"Profile section {section} must be a mapping.")
    for section in ("personal", "links", "documents", "canned_answers", "eeo"):
        if any(child is not None and not isinstance(child, str) for child in profile.get(section, {}).values()):
            raise ProfileError(f"Values in {section} must be text or null.")
    for section, key in (("work_authorization", "authorized_to_work_us"), ("work_authorization", "require_sponsorship"), ("preferences", "willing_to_relocate")):
        answer = profile.get(section, {}).get(key)
        if answer is not None and not isinstance(answer, bool):
            raise ProfileError(f"{section}.{key} must be true, false or null for unknown.")
    if profile.get("writing_style") is not None and not isinstance(profile["writing_style"], str):
        raise ProfileError("writing_style must be text.")
    return profile


def load_profile(path: str | Path) -> dict:
    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise ProfileError("Profile not found. Run python -m applybot init, then fill in profile.yaml.")
    with source.open("rb") as stream:
        raw = stream.read(MAX_PROFILE_BYTES + 1)
    if len(raw) > MAX_PROFILE_BYTES:
        raise ProfileError("Profile YAML exceeds 256 KiB.")
    try:
        value = yaml.safe_load(raw.decode("utf-8-sig"))
    except (yaml.YAMLError, UnicodeDecodeError):
        raise ProfileError("Profile is not valid UTF-8 YAML. The original file was not changed.") from None
    profile = validate_profile(value)
    for key, value in profile.get("documents", {}).items():
        if not value:
            continue
        document = Path(value).expanduser()
        if not document.is_absolute():
            document = source.parent / document
        document = document.resolve()
        profile["documents"][key] = str(document)
        if not document.is_file():
            print(f"[warn] Document {key} is unavailable; its upload will be skipped.")
    return profile


def profile_as_yaml(profile: dict) -> str:
    output = yaml.safe_dump(validate_profile(profile), sort_keys=True, allow_unicode=True)
    if len(output.encode("utf-8")) > 512 * 1024:
        raise ProfileError("Expanded profile exceeds the 512 KiB planner limit.")
    return output
''',encoding='utf-8')
(s/'profile.example.yaml').write_text('''# Copy to profile.yaml and enter only facts you want to use in applications.
# Blank text and null booleans mean unknown; review every filled form yourself.
personal:
  first_name: ""
  last_name: ""
  full_name: ""
  email: ""
  phone: ""
  address: ""
  city: ""
  state: ""
  zip: ""
  country: ""
links:
  linkedin: ""
  github: ""
  portfolio: ""
documents:
  # Relative paths are resolved against this profile file's directory.
  resume: ""
  cover_letter: ""
work_authorization:
  authorized_to_work_us: null
  require_sponsorship: null
  note: ""
background:
  current_title: ""
  years_experience: null
  summary: ""
  skills: []
  education: []
  work_history: []
preferences:
  desired_salary: ""
  earliest_start_date: ""
  willing_to_relocate: null
  remote_preference: ""
  how_did_you_hear: ""
canned_answers: {}
eeo:
  gender: ""
  race_ethnicity: ""
  veteran_status: ""
  disability_status: ""
writing_style: "Concise, first person, and grounded in the supplied profile."
''',encoding='utf-8')
p=s/'applybot/cli.py';t=p.read_text(encoding='utf-8').replace('import shutil\n','import shutil\nimport sqlite3\n').replace('    logged = False','    logged = False\n    recording_attempted = False').replace('''            if cmd == "d":
                tracker.log_application''','''            if cmd == "d":
                recording_attempted = True
                tracker.log_application''').replace('''            if cmd == "q":
                tracker.log_application''','''            if cmd == "q":
                recording_attempted = True
                tracker.log_application''').replace('            if not logged and (company or job_title):','            if not logged and not recording_attempted and (company or job_title):')
t=t.replace('''    except (StoreError, ValueError, OSError) as error:''','''    except sqlite3.Error:
        print("Error: the tracker database is unavailable. Review the local data directory and keep any pending record for retry.", file=sys.stderr)
        raise SystemExit(1) from None
    except (StoreError, ValueError, OSError) as error:''');p.write_text(t,encoding='utf-8')
p=s/'.gitignore';p.write_text(p.read_text(encoding='utf-8')+'\n.venv/\n.verification/\ntest-results/\nplaywright-report/\n*.sqlite3\n*.sqlite3-wal\n*.sqlite3-shm\n',encoding='utf-8')
print('Added bounded profile validation, neutral examples and truthful unknown-answer handling; preserved personal profile.yaml')
