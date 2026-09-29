from pathlib import Path
import json
from course_writer import write_course

controller = 'jellyfin/Jellyfin.Api/Controllers/UserLibraryController.cs'
tests = 'jellyfin/tests/Jellyfin.Api.Tests/Controllers/UserLibraryLatestMediaTests.cs'
chapters = {}
def add(name, title, body, source, anchor, count):
    chapters[name] = (title, body, [(source, anchor, count)])

add('README.md', 'Jellyfin latest media: validate before library work', '''
This improvement targets one API boundary: the latest-media limit. The existing endpoint defaults to twenty items and forwards a caller-supplied integer into the library query. Zero and negative values do not express a meaningful positive result limit. Extremely large values can also overflow downstream arithmetic that doubles the requested limit when fetching candidate groups.

The controller now rejects limits outside one through int.MaxValue divided by two before resolving a user or querying the library. The bound follows the actual arithmetic constraint. It does not introduce an arbitrary small page-size policy. Existing normal requests, the twenty-item default, filtering options, and the legacy route continue through the existing implementation.

Read the map and concepts chapters first, then inspect the small guard in the worked change. Tests call the real controller with strict mocked collaborators. Invalid inputs must produce a bad-request result without library or user access. Valid inputs must preserve their query values and return the normal result shape. The legacy route delegates into the same guard.

The verification record describes focused API tests, not a complete Jellyfin server deployment or media-library scan. The source-based exercises ask you to reason about the exact arithmetic boundary and distinguish controller behavior from HTTP binding. Existing project documentation is preserved; this course explains the bounded change and its evidence.
''', controller, '    public ActionResult<IEnumerable<BaseItemDto>> GetLatestMedia(', 42)

add('01-CODEBASE-MAP.md', 'Follow the latest-media request', '''
UserLibraryController exposes Items/Latest and the older Users/{userId}/Items/Latest compatibility route. The main method receives the optional user and parent identifiers, requested DTO fields, item kinds, played-state filter, image options, user-data option, integer limit, and grouping flag. The compatibility method forwards the same values into the main method.

After validation, RequestHelpers resolves the authorized user identifier and IUserManager loads the user. Missing users retain the existing not-found behavior. If the caller did not specify isPlayed, the user's HidePlayedInLatest preference can supply the filter. DtoOptions combines the field and image settings before the query.

IUserViewManager.GetLatestItems receives LatestItemsQuery. The controller then resolves grouped items, asks IDtoService for DTOs, restores child counts, and returns an OK result. The new guard is deliberately before these operations: an invalid limit should not trigger authorization-dependent library lookup, candidate allocation, or DTO work.

The focused test class sits beside existing API controller tests and uses the same Moq and xUnit conventions. Strict user, view, and DTO mocks make unexpected invalid-path calls fail. Normal-path tests configure only the expected query and empty result conversion. Follow those collaborator boundaries when determining whether a future failure belongs to input validation, user resolution, library selection, or DTO presentation.
''', controller, '    public ActionResult<IEnumerable<BaseItemDto>> GetLatestMedia(', 40)

add('02-CONCEPTS.md', 'The boundary comes from integer arithmetic', '''
A signed 32-bit integer has a maximum of 2,147,483,647. Doubling 1,073,741,823 produces 2,147,483,646, which is representable. Doubling the next integer exceeds the maximum. The accepted upper bound is therefore int.MaxValue / 2. The lower bound is one because this endpoint asks for a positive maximum number of returned items.

This is an input-validity rule, not a performance capacity guarantee. Accepting a large representable value does not promise that a real media library can satisfy it quickly. A separate product decision could impose a smaller operational limit, but that would need its own compatibility review. This change addresses the demonstrated arithmetic defect while preserving ordinary caller behavior.

Validation belongs before downstream work because later consumers should not have to interpret impossible query values. Testing only an annotation would leave uncertainty when the method is invoked directly or through a compatibility delegate. The explicit guard makes the shared behavior visible in both routes.

Boundary tests should include zero, a negative integer, int.MinValue, the first overflowing double, int.MaxValue, and the highest accepted value. Including both sides of the exact upper boundary prevents an off-by-one implementation from passing a collection of only small examples. Default-value testing separately protects clients that omit the parameter.
''', tests, '    [Theory]\n    [InlineData(0)]', 32)

add('03-WORKED-CHANGE.md', 'Place one guard before all collaborators', '''
The production change is small enough to review directly. At the beginning of GetLatestMedia, reject limit <= 0 or limit > int.MaxValue / 2 and return BadRequest with the accepted range. The endpoint metadata also documents a 400 response. Everything after that guard retains the existing user lookup, filter construction, grouping, and DTO behavior.

The legacy method already delegates to GetLatestMedia, so it needs no duplicate validation implementation. Duplicating the predicate there would create two places that could drift during later maintenance. Its regression test invokes the compatibility method and checks the same bad-request result without downstream calls.

Valid-limit tests supply an authenticated test principal and a known user. The view mock expects the exact limit, parent, grouping flag, played-state filter, and user object. An empty view result flows through the existing DTO conversion and returns an empty collection in an OK response. This verifies that the guard has not accidentally changed normal delegation.

The omitted-limit case calls the method without the optional arguments and expects twenty with grouping enabled. That is distinct from passing twenty explicitly: it protects the signature's default contract. None of these tests creates or modifies a real media library, and the invalid tests need no user fixture because the guard must exit before user resolution.
''', controller, '    public ActionResult<IEnumerable<BaseItemDto>> GetLatestMedia(', 39)

add('04-TESTING-AND-DEBUGGING.md', 'Strict mocks expose forbidden work', '''
The invalid-limit theory uses strict mocks for user lookup, latest-item lookup, and DTO conversion. A bad value must return BadRequestObjectResult. VerifyNoOtherCalls then documents that no collaborator was consulted. This is stronger than checking only the returned status: a controller could otherwise reject input after expensive or stateful work had already occurred.

The valid theory includes the largest safe value without allocating that many items. The view manager is a mock that returns an empty list, so the test checks forwarding and arithmetic-boundary acceptance rather than memory capacity. The resulting empty DTO collection is the expected ordinary response.

The legacy test suppresses the obsolete warning only around the compatibility call. It does not remove the production obsolete marker or weaken project-wide warnings. The default test omits the optional limit and grouping parameters and checks their preserved values.

When a test fails, identify the boundary first. A strict mock exception on invalid input means validation occurred too late or not at all. A failed query predicate on valid input means the controller changed a forwarded value. A compilation or restore error is setup evidence, not a failing request assertion. Run the focused class using the recorded SDK and command, then retain the actual terminal result in the verification chapter.
''', tests, '    public void ValidLimit_ForwardsFilters', 29)

add('05-PRACTICE.md', 'Exercises at both ends of the range', '''
Calculate the largest integer that can be doubled without overflowing a signed 32-bit result. Write down both the accepted value and the immediately following rejected value. Explain why testing only int.MaxValue would miss an off-by-one error in a guard that rejects too many valid values.

Next, propose an implementation that returns BadRequest only after GetLatestItems runs. Predict which existing test fails and why. Identify the observable difference between returning the correct status and avoiding invalid downstream work.

For the compatibility route, imagine copying the predicate into GetLatestMediaLegacy while removing it from the main method. Which callers become unprotected? Explain why delegation to a single validated method is easier to maintain than independent guards.

For defaults, compare a test that explicitly passes twenty with one that omits limit. Change the default mentally to twenty-one and predict which test detects it. Repeat for the grouping default.

Finally, design a normal request with a parent identifier, played-state filter, and grouping disabled. List the query fields that must arrive unchanged at the view manager. Separate that forwarding contract from a claim about actual media selection or HTTP model binding, neither of which is established by a controller test with mocked collaborators.
''', tests, '    [Fact]\n    public void OmittedLimit', 20)

add('06-SOLUTIONS-AND-REVIEW.md', 'Answers and compatibility review', '''
The arithmetic answer is 1,073,741,823. Doubling it yields 2,147,483,646. The next value would exceed int.MaxValue when doubled. A correct predicate rejects values greater than that half-maximum, not values greater than or equal to it. Zero and every negative value are independently invalid.

Moving validation after the library query violates the strict invalid-path tests. The expected bad-request response alone is insufficient: the collaborator calls are part of the regression contract. Invalid input must not reach user resolution, candidate grouping, or DTO conversion.

The compatibility route should retain delegation into the guarded method. Protecting only the legacy route leaves Items/Latest exposed, while maintaining separate predicates risks inconsistent behavior. The obsolete-warning suppression in the test acknowledges that the route is retained for compatibility; it does not declare that new clients should prefer it.

The omitted-parameter test catches a changed signature default that an explicit-twenty test would miss. Normal forwarding must preserve the supplied parent, played state, grouping flag, limit, and user. The empty-list fixture verifies response shape without requiring a media database.

During review, avoid overstating the bound. It prevents the known overflow and nonpositive inputs. It does not implement rate limiting, cap total resource use, or prove server-wide authorization behavior. Those would be separate changes with separate acceptance criteria. Keep the focused regression evidence and those operational limits visible together.
''', tests, '    [Theory]\n    [InlineData(0)]', 32)

add('07-TRACE-LAB.md', 'Trace rejected and accepted requests', '''
Draw columns for the route, controller, user manager, view manager, and DTO service. Trace limit zero first. The route invokes GetLatestMedia, the guard returns a bad-request result, and every collaborator column remains empty. Repeat through the compatibility route: it delegates into the same method and reaches the same early result.

Now trace limit twenty with a valid user and an empty media result. The guard accepts it, RequestHelpers resolves the user, the user manager returns the fixture, and the view manager receives the constructed query. The DTO service receives an empty resolved-item list and returns an empty DTO collection. The controller returns OK. Note where user preference can supply isPlayed when the caller omitted it.

Repeat with int.MaxValue / 2 and observe that the control flow is unchanged in this fixture. The test does not allocate a collection of that size; it verifies that the largest arithmetically valid request is forwarded. Finally, increase the limit by one and return to the early-rejection trace.

This comparison makes the acceptance boundary precise. If a future implementation clamps invalid input instead of rejecting it, the externally visible response contract changes. If it forwards a different valid limit, the query contract changes. Use the tests to distinguish those changes from harmless formatting or documentation edits.
''', controller, '        var list = _userViewManager.GetLatestItems(', 32)

add('VERIFICATION.md', 'Focused verification and limits', '''
The recorded checks below define the verified scope. The new tests execute the actual controller class with mocked user, library-view, and DTO services. Invalid-value assertions inspect both the response and the absence of collaborator calls. Valid-value assertions inspect query forwarding, empty result shape, the default limit, and compatibility delegation.

These checks do not start the full Jellyfin server, scan a real media library, or verify HTTP binding and authentication middleware. They also do not establish production capacity for the largest accepted value. The upper bound follows a known integer-doubling requirement; operational page-size policy remains outside this change.

Use the repository's requested .NET SDK and the exact accepted command when reproducing the tests. Dependency restoration and compilation must finish before a test result counts. Failed or interrupted attempts remain in campaign logs and are not included as passing evidence. The final course links machine-readable results where produced by the runner.

The build reports an existing NU1903 advisory for SQLitePCLRaw.lib.e_sqlite3 2.1.11. This controller change does not upgrade that dependency. The first compile rejected a Guid equality operator in the new test, which was corrected to Equals. The next run exposed Jellyfin's typed OkResult subclass; valid-response assertions now accept the existing OkObjectResult subclass and explicitly check status 200. Neither correction changes the production response contract.

Original snapshots preserve the changed baseline controller, and the new focused test class is included in the delivery manifest. Existing documentation remains in place. Reviewers can compare the small production guard with the boundary examples and decide whether a future HTTP-level or full-library integration check is warranted. Such additional evidence would complement, rather than be implied by, this controller-level regression suite.
''', tests, '    private UserLibraryController CreateController', 16)

write_course('7115d7be5ffc', chapters, 'Review latest-media input bounds, compatibility delegation, and focused controller regressions.')
B = Path(__file__).resolve().parent.parent
(B/'specs/7115d7be5ffc.json').write_text(json.dumps(dict(changedFiles=[], summary=[
    'Rejected nonpositive and integer-doubling-overflow latest-media limits before user or library access.',
    'Preserved the twenty-item default, valid query forwarding, and the shared legacy-route guard.',
    'Added focused controller regressions and nine source-based guide chapters.'
], limits=[
    'Tests use mocked library collaborators, not a running Jellyfin server or real media scan.',
    'The arithmetic bound is not a production capacity or rate-limit guarantee; HTTP binding and middleware are outside these focused tests.'
]), indent=2), encoding='utf-8')
