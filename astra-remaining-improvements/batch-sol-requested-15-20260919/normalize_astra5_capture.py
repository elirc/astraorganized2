"""Preserve successful direct captures without inventing unavailable command flags."""
from pathlib import Path
import hashlib
import json

B = Path(__file__).resolve().parent.parent
out = B/'checks/37844e1ec56d'
out.mkdir(exist_ok=True)
captures = [
    ('sol15-astra5-dotnet-build.log', 'astra5-captured-build', 'build'),
    ('sol15-astra5-dotnet-test-r2.log', 'astra5-captured-tests', 'test'),
]
for filename, label, verb in captures:
    source = B/'checks'/filename
    raw = source.read_bytes()
    text = raw.decode('utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig')
    assert 'Build succeeded.' in text
    assert '0 Error(s)' in text
    if verb == 'test':
        assert 'Test Run Successful.' in text and 'Total tests: 27' in text
    record = out/(label+'.json')
    assert not record.exists(), 'Preserve existing capture evidence'
    (out/(label+'.log')).write_text(text, encoding='utf-8')
    record.write_text(json.dumps({
        'project': 'astra5', 'id': '37844e1ec56d',
        'command': ['dotnet', verb, 'tests/Fulfil.Tests/Fulfil.Tests.csproj'],
        'commandCompleteness': 'Known command prefix only; additional original flags were not retained. This is not a reconstructed exact invocation.',
        'cwd': str(B/'stage/37844e1ec56d'),
        'status': 'complete', 'exitCode': 0, 'passed': True,
        'log': label+'.log',
        'provenance': 'Successful direct tool capture from the initial implementation phase; normalized by root after stopping subagents.',
        'originalLog': str(source.relative_to(B)),
        'originalLogSha256': hashlib.sha256(raw).hexdigest(),
        'timingCompleteness': 'Original structured timing record unavailable; no timestamps were inferred.',
    }, indent=2)+'\n', encoding='utf-8')
    print(label)
