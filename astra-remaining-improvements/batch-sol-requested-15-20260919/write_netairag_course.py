from course_writer import write_course
from pathlib import Path
import json

retriever = 'src/Application/Retrieval/LexicalRetriever.cs'
service = 'src/Infrastructure/Operations/OperationsService.cs'
tests = 'tests/UnitTests/LexicalRetrieverTests.cs'
persistence = 'tests/UnitTests/OperationsServiceTests.cs'
chapters = {}
def add(name, title, body, file, anchor, count):
    chapters[name] = (title, body, [(file, anchor, count)])

add('README.md', 'Netairag: evidence before recommendations', '''
This course follows the incident investigation command from authorization to persisted evidence. Previously the command counted log rows and constructed a recommendation without retrieving the knowledge documents already stored by the application. Its recorded confidence, token estimates, tool count, and timestamps could imply work that never happened. The improvement makes the implemented behavior explicit: lexical retrieval, bounded log evidence, two recorded tools, and a human approval request.

Start with the codebase map, then calculate the scoring example in Concepts. Read the worked change before running tests. The practice chapter asks you to predict behavior for missing evidence and unauthorized callers; compare your reasoning with the supplied solutions before attempting a variation. The trace lab ties those predictions to the saved JSON and approval record.

The central distinction is between a document matching an incident description and a document proving its cause. Search finds candidates. The system still asks a person to compare runbook instructions with incident evidence. A lexical score is therefore named heuristicScore, modelConfidence is null, and modelUsed is false. No model service is contacted by this path.

The tests exercise ranking directly and application persistence through an isolated EF InMemory fixture. That fixture can demonstrate the service's saved relationships and serialized fields; it cannot establish PostgreSQL transaction isolation or production query performance. Read the final verification evidence with that boundary in mind. Existing project guides remain useful for setup and architecture, while this course concentrates on one observable investigation workflow.
''', retriever, 'public static partial class', 32)

add('01-CODEBASE-MAP.md', 'Follow the investigation through the codebase', '''
The entry into this change is OperationsService.RunIncidentInvestigationAsync. It accepts the authenticated RequestContext and incident identifier. Its first branch checks IsAdminOrEngineer, before looking up the incident or constructing an AgentRun. A permitted request for a missing incident returns null. These branches explain why the test fixture needs both an incident and a meaningful caller role.

The service queries Logs using the primary service name and a fixed time interval. It records the total match count separately from a bounded sample of at most twenty identifiers. That separation prevents a sample size from being presented as the total evidence population. Timestamp and identifier ordering make the selected sample stable when timestamps tie.

KnowledgeDocuments supply title, tags, and content to the application-layer LexicalRetriever. The retriever has no dependency on EF, HTTP, or a model provider. Its records make the handoff inspectable: RetrievalDocument describes an input document, while RetrievalMatch carries the identifier, title, heuristic score, and matched terms.

The service then builds an AgentRun with SearchLogs and SearchKnowledge children, a HumanApproval, an incident candidate summary, and an audit event. SaveChangesAsync persists those tracked changes. The unit test project contains direct ranking cases and a separate service fixture. The JSON evaluation file is copied to the test output and actually loaded by a test; it is not merely a decorative example. Follow these files in this order when diagnosing a changed recommendation.
''', service, '    public async Task<AgentRunDto?> RunIncidentInvestigationAsync', 39)

add('02-CONCEPTS.md', 'Deterministic ranking and truthful measurements', '''
Lexical retrieval answers a narrow question: which stored documents contain the query's meaningful tokens? Tokens are lowercased ASCII letter-or-digit runs. A small stop-word set removes common investigation vocabulary. Distinct query terms prevent repeating a word in an incident description from multiplying its contribution. Each document field is also represented as a set, so repeating a keyword within one field does not increase its score.

A term found in the title contributes four points, in tags three, and in content one. The contributions are additive across fields. A document with queue in its title and content scores five for that query; one with queue only in tags scores three. Both pass the default minimum of three. A content-only occurrence scores one and is excluded. These weights are an explicit heuristic, not a calibrated probability.

Results sort by descending score, then case-insensitive ordinal title, then identifier. The final identifier tie-break prevents equal-title documents from changing places with input enumeration order. Take applies the requested bound after filtering and ordering. Nonpositive bounds or thresholds return no results.

The current tokenizer has a clear limitation: it does not provide stemming, semantic equivalence, or general multilingual segmentation. A useful next experiment would add a fixed evaluation case demonstrating the desired behavior before changing tokenization. Increasing complexity without an evaluation expectation makes ranking changes difficult to review. The investigation output separately records that no model was used, rather than dressing these integer scores as model confidence.
''', retriever, '    private static RetrievalMatch Score', 26)

add('03-WORKED-CHANGE.md', 'From invented metadata to saved evidence', '''
Read the command as four phases. First, authorize and load the incident. Second, gather evidence with explicit bounds. Third, describe the evidence and proposed next step. Fourth, persist the run and approval. Keeping those phases visible helps distinguish a failed search from a failed save.

The log interval begins two hours before detection and ends at the command's captured start time. Both the count and identifier sample use this same predicate. Retrieval combines the primary service, title, description, and affected services into a query. The knowledge projection supplies the fields needed by the pure ranking function. Three matches is the current output bound; the knowledge corpus itself is loaded in memory, so this implementation does not claim bounded database scanning for a large corpus.

JsonSerializer constructs the input and output documents. Service names containing quotation marks or backslashes therefore remain valid JSON. SearchKnowledge saves the selected document identifiers, scores, and terms. SearchLogs saves its actual interval and sample identifiers. TotalToolCalls is two because precisely those two child records are created.

When no runbook passes the threshold, the recommendation explicitly requests manual investigation. When a match exists, it asks a reviewer to validate the runbook against logs. Both paths create a pending approval. Zero model tokens and zero model cost describe this command's actual provider usage; they do not mean the database or hosting is free. The incident candidate and audit summary use the same deterministic-retrieval description.
''', service, '        var outputJson = JsonSerializer.Serialize', 36)

add('04-TESTING-AND-DEBUGGING.md', 'Use each test at its proper boundary', '''
The ranking tests provide quick feedback without a database. They cover billing and authentication queries, top-k selection, ordering ties, unrelated words, and stop-word-only input. The evaluation test deserializes the checked-in JSON cases and applies their expected title or match count. If a case fails, inspect tokens and field membership before adjusting weights. A lower threshold can make a positive example pass while introducing unrelated matches elsewhere.

The service fixture seeds an incident, one matching log, and one relevant knowledge document in an isolated EF InMemory context. A deliberately awkward service name includes quotes and a backslash. The test parses the saved JSON, rather than matching an escaped string, and checks identifiers, counts, timestamps, model metadata, tool children, approval, and audit. A separate viewer test checks that authorization failure leaves no run or approval.

InMemory is useful for these service assertions but does not emulate relational transactions or every provider translation rule. A deployment confidence claim would need a separate PostgreSQL integration environment. These tests do not make that claim.

On this host, the initial test process could not find .NET 8 because it selected the global .NET 10 installation. The successful rerun uses the installed local .NET 8 toolchain and records the exact command. Treat a missing runtime as a runner failure, not a failing domain assertion. The verification chapter links accepted command evidence and leaves unsuccessful attempts in the campaign history.
''', persistence, '        var service = new OperationsService(db);', 47)

add('05-PRACTICE.md', 'Exercises in ranking and evidence inspection', '''
Exercise one: predict scores for the query queue. Document A has queue in its title and content, document B only in tags, and document C only in content. Use the production weights and threshold. State the returned order and explain which document is excluded. Then repeat with topK equal to one. Write the expected identifiers, not just the number of results.

Exercise two: give two documents the same score and title but different identifiers. Reverse their input order. Predict the output before reading the tie-break expression. Explain why a stable sort alone would not provide the same guarantee when the source enumeration changes.

Exercise three: design an incident investigation with no relevant knowledge document. List the persisted records and the output values you expect. Pay attention to modelUsed, modelConfidence, tool count, approval status, and the recommendation. Absence of a runbook is a valid search outcome and should not be translated into a fabricated mitigation.

Exercise four: propose a service test containing twenty-five matching logs, one log before the lower bound, and one log after the upper bound. Predict the total count and sample size separately. Specify how you would make time boundaries deterministic instead of relying on a sleep.

Finally, describe what an unauthorized viewer request may change. Compare your answer with the existing authorization test. Keep proposed fixture changes local and isolated; none of these exercises requires a provider credential, a deployed incident, or access to an existing operational database.
''', tests, '    [Fact]\n    public void Ranking_is_stable', 18)

add('06-SOLUTIONS-AND-REVIEW.md', 'Answers and review criteria', '''
For the first exercise, A scores five, B scores three, and C scores one. A and B pass the default threshold and appear in that order. With topK one, only A remains. The result is explained by field membership, not term frequency: repeating queue ten times in C's content still contributes one point for that field.

For the second exercise, the identifier comparison resolves the remaining tie. Reversing input order must not reverse the result. A stable sorting implementation only preserves the supplied order among equal keys; it cannot make an unstable source enumeration deterministic. The explicit final key is therefore part of the observable contract.

For the no-match investigation, both searches still occurred. The AgentRun has two tool children, zero model tokens and cost, modelUsed false, and null modelConfidence. The recommendation asks for manual investigation and the approval remains pending. No-match does not grant permission to skip human review or claim a root cause.

For the log fixture, the expected match count is twenty-five and the saved identifier sample contains twenty. Out-of-window rows must affect neither. A clock abstraction would make exact endpoint tests clearer if introduced in a future bounded change; this patch uses an actual captured command start time and its tests assert permissible ordering.

The viewer request throws before persistence, so there is no AgentRun or HumanApproval. Review proposed changes for regressions at these boundaries. Reject a solution that adds a hardcoded confidence value or labels lexical matching as model inference. Also reject claims of relational rollback based solely on this InMemory test fixture.
''', tests, '    [Fact]\n    public void Unrelated', 27)

add('07-TRACE-LAB.md', 'Trace one incident into its saved records', '''
Use the seeded billing incident in OperationsServiceTests as a controlled trace. Write down its identifier, primary service, detection time, log identifier, and knowledge-document identifier. Follow the command's role check before drawing any arrows to persistence. The request context is part of the input contract even though it is not a search term.

Mark the captured start time and calculate the lower log bound. The seeded log lies inside the interval and matches the exact service string. The service counts it and saves its identifier. Next construct the retrieval query from the incident fields and locate billing, capture, and timeout terms in the runbook. The precise score matters less than being able to account for every contribution using the title, tags, and content weights.

Now inspect the two tool records. SearchLogs should contain one sample identifier, while SearchKnowledge should contain the runbook identifier. Parse the parent input and output JSON and compare them with those children. A parent summary that names a document absent from the saved tool evidence would be a consistency defect.

Finish at the pending HumanApproval and incident candidate. Neither applies a mitigation. Record this distinction in your trace: retrieval completed, a recommendation exists, and execution has not been approved. Repeat the trace mentally with unrelated knowledge and then with a viewer caller. The first still produces a truthful no-match investigation; the second exits before creating the run. These three traces make the workflow's success, uncertainty, and rejection paths concrete.
''', persistence, '        var logCall = run.ToolCalls.Single', 19)

add('VERIFICATION.md', 'Verification scope and reproducible evidence', '''
Accepted checks below are generated from completed command records. Their logs and machine-readable results define the tested scope. Do not infer that every frontend, deployment, or provider workflow has been exercised from a successful unit suite. The change is centered on the .NET investigation service and its pure retrieval component.

The unit suite includes existing project tests as well as the new retrieval and persistence regressions. The evaluation JSON is read from the test output directory, so its copy configuration is part of the test setup. The service fixture uses a unique InMemory database for each test, avoiding the original application database. No model provider or external mitigation endpoint is involved.

The local runtime matters for reproduction. The project targets .NET 8 and this workstation also has .NET 10 installed globally. Use the recorded .NET 8 executable and environment setting when repeating the accepted tests here. Earlier missing-runtime or incomplete-restore attempts are retained separately and are not counted as passes. A terminal exit of zero is required before a check is accepted.

Important limits remain explicit: ranking is lexical and ASCII-token based; all knowledge rows are materialized before ranking; log counts and samples use separate queries; and InMemory tests do not verify PostgreSQL isolation or query performance. These limits constrain the evidence, not the test result. A future scaling or relational-integration task should define its own acceptance criteria before changing this bounded implementation. Original source snapshots accompany the delivered changes so reviewers can inspect the exact before-and-after behavior.
''', tests, '    public async Task Checked_in_evaluation_cases', 27)

write_course('6ee92f3ab313', chapters, 'Trace deterministic incident retrieval, truthful evidence, and pending human approval.')
B = Path(__file__).resolve().parent.parent
(B/'specs/6ee92f3ab313.json').write_text(json.dumps(dict(changedFiles=[], summary=[
    'Added deterministic runbook retrieval with weighted fields, stable ties, bounded results and explicit no-match handling.',
    'Persisted actual log and document evidence using JSON serialization, accurate tool counts and timestamps, and explicit zero model usage.',
    'Added loaded evaluation fixtures, permission and saved-evidence regressions, and nine source-based course chapters.'
], limits=[
    'Service tests use EF InMemory, not PostgreSQL; no relational isolation or deployed end-to-end claim is made.',
    'Retrieval uses ASCII lexical tokens and materializes the knowledge corpus; model services are not called.'
]), indent=2), encoding='utf-8')
