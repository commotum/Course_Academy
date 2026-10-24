import ast,collections,json
from pathlib import Path
H=Path('reference/edb-math/repairs/2026-10-23-choice-markers');R=Path.cwd();M=Path('/media/jake/SSD/EDB/math');G=json.loads((H/'all-generators.json').read_text());paths={p for g in G for p in g['scripts']};out=[];missing=[]
for ref in sorted(paths):
 p=(M if ref.startswith('generators/') else R)/ref
 if not p.is_file():missing.append(ref);continue
 text=p.read_text()
 try:tree=ast.parse(text)
 except SyntaxError:continue
 parents={child:n for n in ast.walk(tree) for child in ast.iter_child_nodes(n)};seen=set();sites=[]
 for n in ast.walk(tree):
  if not isinstance(n,ast.Constant) or not isinstance(n.value,str) or '{{' not in n.value:continue
  stmt=n
  while stmt in parents and not isinstance(stmt,ast.stmt):stmt=parents[stmt]
  if isinstance(stmt,ast.Expr) and isinstance(stmt.value,ast.Constant):continue
  if stmt.lineno in seen:continue
  seen.add(stmt.lineno);sites.append({'line':stmt.lineno,'code':ast.get_source_segment(text,stmt)[:650]})
 if sites:out.append({'reference':ref,'path':str(p),'active':any(ref in g['scripts'] and g['active'] for g in G),'sites':sites})
(H/'generator-marker-sites.json').write_text(json.dumps(out,indent=2)+'\n');(H/'missing-generator-files.json').write_text(json.dumps(missing,indent=2)+'\n');print('registered unique paths',len(paths),'with constructions',len(out),'active',sum(x['active'] for x in out),'missing',len(missing));
for r in out:
 for s in r['sites']:
  if 'selection' in s['code'] or 'radio' in s['code'] or "key+'}}'" in s['code'].replace(' ','') or "field['key']" in s['code']:print(r['reference'],s['line'],s['code'][:280].replace('\n',' '))
