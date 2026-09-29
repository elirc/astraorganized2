"""Replace the original CRUD endpoints with the tested shared implementation."""
import ast
from pathlib import Path
S = Path(__file__).resolve().parents[2] / 'stage/ca549816cdd1'
p = S / 'app/api.py'
source = p.read_text()
tree = ast.parse(source)
names = {
    'list_streams', 'create_stream', 'dashboards_list', 'dashboards_create',
    'dashboards_get', 'dashboards_update', 'dashboards_delete', 'alerts_list',
    'alerts_create', 'pipelines_list', 'pipelines_create',
    'saved_queries_list', 'saved_queries_create',
}
nodes = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name in names]
assert {node.name for node in nodes} == names
lines = source.splitlines(keepends=True)
for node in sorted(nodes, key=lambda node: node.lineno, reverse=True):
    start = min([node.lineno] + [decorator.lineno for decorator in node.decorator_list])
    del lines[start-1:node.end_lineno]
source = ''.join(lines)
source = source.replace('from app.config import Settings, settings', 'from app.config import Settings, settings\nfrom app.crud import build_crud_router')
assert '    return app\n' in source
source = source.replace('    return app\n', '    app.include_router(build_crud_router())\n    return app\n')
p.write_text(source, encoding='utf-8')
print('Replaced 13 legacy handlers with 25 CRUD endpoints')
