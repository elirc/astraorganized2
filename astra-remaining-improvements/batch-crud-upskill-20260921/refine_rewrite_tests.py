from pathlib import Path
import json
b=Path(__file__).resolve().parent.parent;p=b/'stage/c81c4e873d3b'
f=p/'tests/comment-delete-boundary.test.mjs';s=f.read_text(encoding='utf-8-sig')
s=s.replace("import path from 'node:path';", "import path from 'node:path';\nimport { fileURLToPath } from 'node:url';")
s=s.replace("path.resolve('fastapi-realworld-example-app')", "fileURLToPath(new URL('../fastapi-realworld-example-app/', import.meta.url))")
pos=s.index("test('the route supplies")
s=s[:pos]+'''test('actual nested DELETE handler passes slug and maps repository outcomes', async () => {
  const routes = new Map();
  const router = Object.fromEntries(['get','post','put','delete'].map(method => [method, (url, ...handlers) => {
    routes.set(`${method} ${url}`, handlers.at(-1));
  }]));
  await loadTypeScript('src/routes/articles.ts', { root, stubs: {
    express: { Router: () => router },
    '../repositories/ArticleRepository': { ArticleRepository: {} },
    '../repositories/CommentRepository': { CommentRepository: repository.CommentRepository },
    '../middleware/auth': { authenticate: () => {}, optionalAuthenticate: () => {} },
    '../middleware/validate': { validate: () => () => {} },
    '../schemas': { NewArticleSchema: {}, UpdateArticleSchema: {}, NewCommentSchema: {} },
  }});
  const handler = routes.get('delete /articles/:slug/comments/:id');
  assert.equal(typeof handler, 'function');
  for (const [comment, expected] of [[{id:9,authorId:4},204],[null,404],[{id:9,authorId:8},403]]) {
    const calls = db({comment}); let status, ended=false, body;
    const res = {status(code) {status=code;return this;}, json(value) {body=value;return this;}, end(){ended=true;}};
    await handler({params:{id:'9',slug:'alpha'},user:{id:4}}, res, error => {throw error;});
    assert.equal(status,expected); assert.equal(ended,expected===204);
    assert.equal(JSON.stringify(calls.findFirst[0].where), JSON.stringify({id:9,article:{slug:'alpha'}}));
    assert.equal(calls.delete.length,expected===204?1:0);
    if(expected!==204) assert.ok(body.errors.body.length);
  }
  db({comment:{id:9,authorId:4}}); const failure = new Error('database unavailable');
  prisma.comment.delete = async () => {throw failure;}; let forwarded;
  await handler({params:{id:'9',slug:'alpha'},user:{id:4}}, {status(){throw new Error('unexpected response');}}, error=>{forwarded=error;});
  assert.equal(forwarded,failure);
});
'''
f.write_text(s,encoding='utf-8')
f=b/'specs/c81c4e873d3b.json';spec=json.loads(f.read_text(encoding='utf-8-sig'));spec['limits'][0]='Four runtime cases execute the actual repository and, in the fourth case, the actual registered DELETE handler with explicit Prisma and Express router/response doubles. No Express server is mounted.';f.write_text(json.dumps(spec,indent=2),encoding='utf-8')
