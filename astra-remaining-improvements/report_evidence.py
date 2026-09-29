"""Describe recorded evidence without inventing a unit-test count."""


def check_summary(manifest):
    result = manifest.get('testResults', {})
    harnesses = result.get('harnesses')
    if isinstance(harnesses, int) and not isinstance(harnesses, bool):
        label = f'{harnesses} regression harness' + ('es' if harnesses != 1 else '') + ' passed'
        if result.get('scenarioGroups'):
            label += f' ({result["scenarioGroups"]} scenario groups)'
        return label
    total = result.get('total')
    passed_tests = result.get('passedTests', result.get('passed'))
    if isinstance(total, int) and not isinstance(total, bool) and total == passed_tests:
        return f'{total} tests passed'
    expected = manifest.get('checks', {}).get('expectedTests')
    return f'{expected} recorded checks passed' if expected is not None else 'Recorded verification passed'
