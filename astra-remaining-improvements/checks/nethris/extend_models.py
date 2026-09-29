from pathlib import Path

S=Path(__file__).resolve().parents[2]/'stage/71e7b036865c/server/Nethris.Api/Domain'
for name in ['Employee','Department','JobRole','UserAccount','PtoRequest']:
    path=S/(name+'.cs')
    text=path.read_text(encoding='utf-8')
    marker='public sealed class '+name+'\n{'
    assert marker in text and 'IVersioned' not in text
    text=text.replace(marker,'public sealed class '+name+' : IVersioned\n{\n    public long Version { get; set; } = 1;',1)
    if name in ['Department','JobRole']:
        text=text.replace('    public Guid Id { get; set; }','    public Guid Id { get; set; }\n    public bool IsActive { get; set; } = true;',1)
    if name=='PtoRequest':
        text=text.replace('    public PtoStatus Status','    public Guid? AssignedManagerId { get; set; }\n    public Employee? AssignedManager { get; set; }\n    public PtoStatus Status',1)
        text=text.replace('    public PtoDecision Decision','    public required string Stage { get; set; }\n    public PtoDecision Decision',1)
    path.write_text(text,encoding='utf-8')
print('Added versions, catalog archive flags and assigned PTO review-stage identity.')
