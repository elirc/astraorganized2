from pathlib import Path
P=Path(__file__).resolve().parent.parent/'stage/abcd8cc338ec/astraupskill'
for f in P.glob('*.md'):
    t=f.read_text(encoding='utf-8-sig')
    t=t.replace('The fixture stubs parsing and response conversion, so it demonstrates control flow and call order.','The fixture stubs parsing and the NextResponse adapter, while executing the real ok/fromError helpers. It demonstrates control flow, response conversion and call order.')
    t=t.replace('inspect the first argument to the failing operation.','inspect the receiver of the failing operation.')
    t=t.replace('which the fixture represents as a 500 response carrying the message.','whose real implementation creates a 500 response carrying the message through the test NextResponse adapter.')
    t=t.replace('The test uses explicit Drizzle, authentication, schema, validation, and response doubles.','The test uses explicit Drizzle, authentication, schema, validation, and NextResponse adapter doubles. The route and its ok/fromError response helpers execute from production source.')
    t=t.replace('a tenant fixture with identical workflow ids in separate tenants if the database permits such fixtures.','two tenants with distinct workflow ids, then attempt to update tenant B’s workflow while authenticated as tenant A. The workflow id is globally primary-keyed, so a duplicate-id fixture would violate the schema.')
    t=t.replace('the fixture verifies route/API/domain/data/auth interactions through explicit doubles','the fixture verifies route control flow, API response helpers and data mapping with explicit authentication and database doubles')
    t=t.replace('`sql\\`${workflows.version} + 1\\``','a SQL expression that adds one to `workflows.version`')
    f.write_text(t,encoding='utf-8')
