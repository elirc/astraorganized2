from pathlib import Path
import json,re
BASE=Path(__file__).resolve().parent/'stage'
NAMES=json.loads((BASE.parent/'projects.json').read_text(encoding='utf-8'))
COURSES=json.loads((BASE.parent/'courses.json').read_text(encoding='utf-8'))
def source(n,path):return (BASE/n/path).read_text(encoding='utf-8')
def excerpt(text,symbol,limit=85):
 lines=text.splitlines()
 if symbol.startswith('app.'):
  start=next(i for i,l in enumerate(lines) if symbol in l)
 else:
  definitions=[i for i,l in enumerate(lines) if re.search(r'\b'+re.escape(symbol)+r'\s*\(',l) and ('function ' in l or 'const ' in l or re.match(r'\s*'+re.escape(symbol)+r'\s*\(',l))]
  if definitions:start=definitions[0]
  else:
   hit=next(i for i,l in enumerate(lines) if symbol in l)
   starts=[i for i in range(hit+1) if lines[i].startswith('app.') or re.match(r'^(?:export )?(?:async )?function ',lines[i])]
   start=starts[-1] if starts else max(0,hit-8)
 end=min(len(lines),start+limit)
 for i in range(start+1,end):
  if re.match(r'^(?:export )?(?:async )?function\s|^app\.(?:get|post|put|patch|delete)\(',lines[i]):end=i;break
 return '\n'.join(lines[start:end]),start+1

def write(n,file,text):
 p=BASE/n/'astraupskill'/file;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')

for i,c in enumerate(COURSES,21):
 n=f'{i:02}';name=NAMES[i-21]
 testcmd=c['testcmd']
 setup=c['setup']
 code,line=excerpt(source(n,c['source']),c['symbol']);tests=source(n,c['test'])
 lang='typescript' if c['source'].endswith(('.ts','.tsx')) else 'javascript'
 links=[('01-CODEBASE-MAP.md','Codebase map and reading order'),('02-CONCEPTS.md','Concepts explained from first principles'),('03-WORKED-CHANGE.md','Worked implementation and examples'),('04-TESTING-AND-DEBUGGING.md','Tests, failure cases and debugging'),('05-PRACTICE.md','Guided and independent exercises'),('06-SOLUTIONS-AND-REVIEW.md','Solutions, tradeoffs and review rubric'),('07-TRACE-LAB.md','Detailed trace lab and independent checkpoint'),('VERIFICATION.md','Actual verification results and limits')]
 write(n,'README.md',f'''# {c['title']}

This is a hands-on course for a junior software engineer using the actual project in `{name}`. The central skill is **{c['focus']}**. The implementation is already present: use it as a worked example, then recreate a small variation independently.

## What you will be able to do

- Explain the purpose of the changed code and the data it owns.
- Trace an action from input through validation, state/persistence and output.
- Predict a success case and a failure case before running either.
- Read the regression tests and explain what each assertion proves.
- Implement a related change without copying the worked answer.
- Explain a limitation and a reasonable next step without overstating readiness.

## Prerequisites

Be comfortable with variables, arrays, objects, functions, conditionals and calling a function. For React projects, review props, state and event handlers. For API projects, review JSON, HTTP methods and promises, then learn the relevant SQL operations as you trace the request. You do not need to memorize the whole repository first.

## Start the project

{setup}

The commands are run from this project’s folder, not from the Desktop inventory repository. Existing README/Fable material remains available. This folder teaches the implemented change and points to executable source and tests rather than replacing older guides.

## Reading and practice order

'''+ '\n'.join(f'{j}. [{title}]({file})' for j,(file,title) in enumerate(links,1))+f'''

## Your first session

1. Open the app or its tests and reproduce one normal workflow.
2. Read chapter 1 while keeping [{c['source']}](../{c['source']}) open.
3. Write a prediction for the worked example in chapter 3 before executing it.
4. Run the focused test suite and explain one assertion aloud.
5. Complete the first practice exercise, then check the solution discussion.

Keep a short learning log with four fields: prediction, observed result, explanation and next question. A mismatch is useful evidence: find the exact layer where your mental model diverged from the program. Use a disposable browser profile or local test database for failure experiments so your own records are not part of the fixture.

## Scope

{c['after']} This is one bounded improvement, not certification of every feature. Read VERIFICATION.md for checks actually executed. Exercises are intentionally future practice; do not confuse them with completed implementation.
''')
 extras=[]
 for p in (BASE/n).rglob('*'):
  if p.is_file() and p.suffix in ['.js','.jsx','.ts','.tsx'] and not any(x in p.parts for x in ['node_modules','test','astraupskill','dist']):extras.append(p.relative_to(BASE/n).as_posix())
 write(n,'01-CODEBASE-MAP.md',f'''# Codebase map and reading order

[Course index](README.md)

## The problem this project solves

{c['before']} The improvement you will study is: {c['after']}

## Data model

{c['model']}

An object is a named collection of fields. An array is an ordered collection of values. An id answers “which record?”; an index answers “where is it in this array right now?” Those questions are different whenever the list can be filtered, reordered or edited. Persisted data is the form that must survive a process/page restart. Derived data can be recomputed from that persisted state.

## Trace one action

'''+ '\n'.join(f'{j}. {step}.' for j,step in enumerate(c['flow'],1))+f'''

```mermaid
flowchart LR
    A[Input or user action] --> B[Validate and normalize]
    B --> C[Compute intended change]
    C --> D[Commit at the state boundary]
    D --> E[Return or render observed state]
    B --> F[Explain invalid input]
    D --> G[Handle a failed write]
```

This diagram names responsibilities, not necessarily separate files. A small browser program can keep them in app.js. A larger API spreads them across controllers, services and models. Follow the actual sequence above rather than assuming every repository has the same architecture.

## Where to read first

1. [{c['source']}](../{c['source']}): locate `{c['symbol']}` and read its inputs, branches and return/side effects.
2. [{c['test']}](../{c['test']}): read the scenario names before the helper code.
3. The root [README](../README.md): connect setup and the larger application workflow.

## Source navigation

'''+ '\n'.join(f'- [{path}](../{path})' for path in sorted(extras))+f'''

## A practical reading technique

At each function boundary, write down the value coming in, the value going out and any side effect. A side effect includes a storage write, SQL query, network request, timer registration or DOM update. If a function calls another function, inspect only that next dependency until you can finish the chosen trace. Return to unrelated files later.

For this lesson, start with: **{c['example']}** Mark where the id, time, amount or other important value changes representation. For example, JSON serializes values into text; a date field may be a calendar string; SQL aggregates may return a different type from individual rows. Representation changes are common bug locations.

## Check your understanding

Without reading the solution, answer: Who owns the mutable state? Which input is untrusted? Which function first decides whether the operation is valid? What survives reload or restart? What observation would prove that the operation partially failed? Point to a source file for each answer, rather than describing a generic app from memory.
''')
 write(n,'02-CONCEPTS.md',f'''# Concepts explained from first principles

[Course index](README.md)

## The central idea: {c['focus']}

{c['concept']}

## Invariants: a precise way to describe correctness

An invariant is a rule that must remain true before and after an operation. “The app works” is too broad to test. “A failed import writes no records” or “editing preserves the record id” gives you something observable. For this project, derive your invariants from this behavior:

> {c['after']}

Turn each sentence into a small state table. The columns are initial state, input, expected final state and expected feedback. Include one rejected input and one retry/repeated action where relevant. A useful invariant should be meaningful even if the implementation changes from an array to a database or from one UI component to another.

## Validation versus normalization

Validation rejects values the operation cannot accept. Normalization converts acceptable values to the representation the rest of the program expects. Trimming a comparison string is normalization; rejecting an empty required field is validation. Neither operation should silently invent facts. If a quantity is free-form text, do not guess a numerical interpretation. If an imported record is malformed, do not quietly save only the convenient subset unless that is the explicit product policy.

Apply this distinction to the data model:

{c['model']}

Which fields can be omitted? Which can be empty? Which have a bounded vocabulary? Which have stable identity? Write those answers down before adding another conditional. A schema is simply an explicit description of that expected shape and meaning.

## State transitions and failure boundaries

Every change has an ordering. If memory changes first and persistence fails, the UI can show data that will disappear after reload. If persistence succeeds first and rendering fails, the stored data may be correct while the screen is stale. There is no universal answer for every feature, but the choice must be deliberate and observable. The worked change makes one specific promise; the tests check that promise.

A promise represents an operation that completes later. `await` does not make it infallible or atomic; it gives the caller a place to handle success and rejection. Similarly, calling several functions inside one `try` block does not create a database transaction. Atomicity must come from a storage operation or transaction boundary that actually provides it.

## Identity, representation and derived values

Keep a stable id when updating an existing record. Compute display-only values from authoritative data when feasible, so there are fewer independently mutable facts to keep synchronized. Be careful when converting between strings and numbers: `Number('')` is zero, JSON cannot faithfully represent Infinity, and a date string can have different semantics from a timestamp. The specific conversions in this lesson are visible in the worked source, so step through them with a concrete value.

## Small design decisions deserve explanations

Before extracting a new abstraction, explain what repeated responsibility it would own. A helper that merely renames one expression may add little. A pure validator or one transaction boundary can make an important guarantee easier to test. Prefer an explanation tied to this project’s behavior over a rule such as “all code must use a particular pattern.”

Write a short decision note: “We chose X because it preserves Y under Z. It does not yet solve W.” Use the limitations in the worked example to fill in those letters. This is the beginning of engineering judgment: choosing a bounded solution and accurately describing its limits.
''')
 write(n,'03-WORKED-CHANGE.md',f'''# Worked implementation and examples

[Course index](README.md)

## Before and after

**Before:** {c['before']}

**After:** {c['after']}

## Predict this example

{c['example']}

Before running anything, write the exact expected stored values and visible response. Include ids or record counts where they matter. Then run the focused tests and reproduce the matching UI/API action. Do not settle for seeing a success message: inspect the authoritative stored result as well.

## Actual implementation excerpt

The excerpt below comes from [{c['source']}](../{c['source']}) near line {line}. It is a teaching snapshot; the linked source is authoritative if you later edit the project. Read surrounding code for callers and setup.

```{lang}
{code}
```

## How to reason through the code

1. Identify the inputs. Distinguish data supplied by a caller from state read from storage or a trusted context.
2. Find the guard clauses. For each early return or thrown error, describe which invariant it protects and whether anything has already been written.
3. Find the candidate state or query. Explain whether it mutates an existing object or constructs a replacement.
4. Locate the persistence operation. For asynchronous code, follow the promise through success and rejection; for transactions, check that all related writes use the same transaction object.
5. Find the output or state publication. Ask what a repeated invocation would do after the first invocation succeeds.

Use this project-specific reasoning as your guide:

{c['concept']}

## Three variations to work through

**Normal variation:** change one ordinary value in the successful fixture while preserving its shape. Predict which fields should change and which should remain identical. Execute it and explain any difference.

**Invalid variation:** use the invalid case from the tests. Predict the error and the exact number of writes that should happen. Compare the state before and after; error text alone does not prove data integrity.

**Boundary variation:** repeat the action, reload, delay a callback or force a late write failure as appropriate to this lesson. Explain why the boundary differs from the happy path. The test file below contains a concrete example you can adapt rather than inventing an unrealistic failure.

## Executable examples

These are the actual regression tests in [{c['test']}](../{c['test']}). Read each test as arrange → act → assert. Setup creates a controlled initial state, the action exercises the application code, and assertions compare observable behavior with an independently stated expectation.

```{'typescript' if c['test'].endswith('.ts') else 'javascript'}
{tests}
```

## Explain it back

Give a five-minute walkthrough: the original problem, one invariant, the exact changed function, the most revealing failure test, and one remaining limitation. You should be able to explain why the implementation is correct for the worked example without reading the code aloud line by line.
''')
 dbguide=c['dbguide']
 write(n,'04-TESTING-AND-DEBUGGING.md',f'''# Testing and debugging

[Course index](README.md)

## Run the checks

{setup}

```text
{testcmd}
```
{dbguide}
## What the test suite proves

Read [{c['test']}](../{c['test']}). The suite targets **{c['focus']}** and uses the worked fixture:

{c['example']}

The expectation should not be copied from the function being tested. Hand-calculate counts, amounts, identities or elapsed time first. Otherwise the same mistake can appear in both implementation and expected result. Tests that exercise only a mocked dependency prove a narrower contract than tests against the real dependency; read the helper to understand which kind you are running.

For Poll Studio and Kanban Flow, jsdom runs the actual app.js against its HTML and fresh browser storage; the suite can force a storage-write failure. The other projects use their actual Express app over loopback HTTP. PostgreSQL projects additionally load a disposable schema. Chromium checks cover the real built clients and route their API requests to those isolated real servers through a local test proxy. These checks verify different boundaries; none replaces reading the test helper.

## Debugging workflow

1. Reproduce the smallest failing case with the exact input saved in your notes.
2. Inspect the relevant event/request. Confirm the intended handler actually ran.
3. Pause at `{c['symbol']}` and inspect input types as well as values.
4. Follow validation branches, noting whether any state or persistence changed before rejection.
5. Inspect the write result and the subsequent render/response. Separate storage correctness from display correctness.
6. Add a regression reproducing the failure, make the smallest justified fix, then run the focused suite and relevant broader checks.

Avoid changing several layers at once when you do not yet know where the failure starts. A correct backend with a stale UI needs a different fix from a malformed query or an invalid saved document.

## Failure experiments

- Reuse the invalid fixture from the tests and verify no unintended records or fields change.
- Reload or restart after a successful operation to distinguish persistence from temporary screen state.
- Repeat the operation and explain whether it should be idempotent, rejected or intentionally create another record.
- Simulate the relevant timing or storage failure only in a disposable fixture. Restore normal behavior after the experiment.

## Reading an assertion failure

“Expected 3, received 4” is evidence about one observation, not a complete diagnosis. Ask whether the fixture created an extra record, the operation ran twice, an old record survived, or the assertion looked at an unfiltered collection. Start from the state table and trace the first point where the actual value diverges. A stack trace identifies where the program noticed a problem, which may be later than the code that caused it.

## Verification record

The companion [VERIFICATION.md](VERIFICATION.md) records checks actually run for this implementation. Record your own command, date, result and any environmental prerequisite when practicing. A passing test does not imply every route, browser, dependency version or production deployment has been exercised.
''')
 write(n,'05-PRACTICE.md',f'''# Guided and independent practice

[Course index](README.md) · [Solutions](06-SOLUTIONS-AND-REVIEW.md)

## Exercise 0 — reconstruct the existing behavior

Draw the data shape and trace this fixture without running it:

{c['example']}

Write one assertion for success and one for a rejected or failed operation. Then read the existing test and compare its observation with yours. Explain why a message alone would or would not prove the invariant.

## Exercise 1 — guided extension

{c['exercises'][0]}

Start by locating the current input, handler and output. Write an acceptance example before editing. Make one small change, run the focused tests, and demonstrate it through the same public UI/API a user would use. Add one meaningful regression if the behavior can break in a way the existing suite would miss.

## Exercise 2 — independent variation

{c['exercises'][1]}

Close the worked-change chapter while implementing. Describe your design in three sentences: the data you will add or reuse, the rule it must preserve, and the observation that proves it. Compare your answer with the solution only after an independent attempt. If you get stuck, request a hint about the next boundary rather than a complete implementation.

## Exercise 3 — failure-focused extension

{c['exercises'][2]}

Create a failing example in a disposable fixture. Capture the state before the operation and after the failure. Identify what must remain unchanged and what feedback the caller needs. A correct result includes understandable recovery behavior, not just throwing an exception.

## Exercise 4 — stretch design

{c['exercises'][3]}

Write a short design note before coding. List the current guarantee, the stronger guarantee you want and the new failure modes the change introduces. If this requires a larger architectural change, stop at a concrete proposal and test design until you understand the prerequisite. The earlier exercises should remain understandable and runnable.

## Exercise 5 — teach the codebase

Give a five-minute walkthrough to another learner, or record yourself. Use [{c['source']}](../{c['source']}) and one test. Explain the application problem, the data model, the call path, one success case, one failure case and the tradeoff. Ask the listener to predict a new input’s result. Their questions reveal which part of your explanation needs work.

## Exercise 6 — review your own change

Inspect the diff as if you were a teammate encountering it for the first time. Remove unrelated edits. Check names, error feedback, preservation of ids/data, and the order of writes. Update the learning note if the actual code differs from the plan. Record what was tested and what remains an assumption.

## Completion rubric

Score each item 0 (cannot explain), 1 (can explain with help) or 2 (independent): data model, control flow, validation, persistence/failure behavior, regression test design, and tradeoff explanation. Aim for 2 on the first five before taking the stretch exercise. Revisit a weak area with a changed-input example rather than rereading every page.
''')
 write(n,'06-SOLUTIONS-AND-REVIEW.md',f'''# Solutions and engineering review

[Course index](README.md) · [Practice prompts](05-PRACTICE.md)

Attempt each exercise before using these notes. These are solution approaches and review criteria, not claims that every extension has been implemented. The actual completed behavior is described in the worked-change chapter.

## Existing implementation

{c['after']}

The key model is: {c['model']}

The worked fixture should behave as follows: {c['example']}

## Extension solutions

'''+ '\n\n'.join(f'### Exercise {j}\n\n**Prompt:** {prompt}\n\n**Approach:** {answer}\n\n**Review:** Demonstrate an ordinary case and a case that would break a naive implementation. Explain which existing invariant remains unchanged. Keep the code and the learner-facing explanation in agreement.' for j,(prompt,answer) in enumerate(zip(c['exercises'],c['answers']),1))+f'''

## Review questions with answer guidance

**Why not trust input just because it came from this UI?** A caller can bypass the UI, a saved file can be edited, and older data can have a different shape. Validate at the boundary that owns the operation.

**Why keep the id stable?** It identifies the same domain record across views and edits. Changing it can create duplicates, disconnect child records or make reconciliation impossible.

**What makes the failure test meaningful?** It observes the promised state invariant. For this project, explain exactly why the failing scenario in [{c['test']}](../{c['test']}) would detect the original or a plausible regression.

**What does the test not prove?** A bounded suite does not prove all concurrency, browsers, deployment configurations or unrelated domain behavior. Name the real limitation from this lesson instead of adding a generic disclaimer.

**When should you extract a helper?** When it isolates a coherent responsibility, makes an invariant clearer or enables a meaningful test without duplicating application logic. A pure validator and a shared persistence boundary are common examples, but do not abstract solely to increase the number of files.

## A sample change explanation

“The previous behavior was: {c['before']} I changed the implementation so that: {c['after']} The strongest evidence is the regression that exercises the worked fixture and checks authoritative state. A remaining design question is the final stretch exercise.”

Replace that explanation with your own words and actual test results. A strong junior engineer can connect a concrete user problem to code, verification and a clearly stated limit. Completing that explanation independently is the final checkpoint for this course.
''')
 # Add a stable entrypoint without replacing any older tutorial.
 p=BASE/n/'README.md';text=p.read_text(encoding='utf-8')
 if '(astraupskill/README.md)' not in text:p.write_text(text.rstrip()+f'\n\n## Junior SWE learning course\n\n[Start the detailed Astra upskilling course](astraupskill/README.md): {c["focus"]}, with a codebase map, worked implementation, executable examples, debugging labs, exercises and solution discussions.\n',encoding='utf-8')

(BASE.parent/'courses.json').write_text(json.dumps(COURSES,indent=2),encoding='utf-8')
print('Generated 210 detailed learning chapters plus course metadata; trace and verification pages follow.')
