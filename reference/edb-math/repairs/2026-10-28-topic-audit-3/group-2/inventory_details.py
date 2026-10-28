import json,ast,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];D=json.loads((H/'current.json').read_text());I=json.loads((H.parent/'inventory.json').read_text());links={q:k for t,k,q in I['links']};Q={q[':db/id']:q for q in D['questions']};K={k[':db/id']:k for k in D['kps']};inc=json.loads((H/'incomplete.json').read_text());context=[];gs=[]
for q in inc:
 k=K[links[q[':db/id']]];c=k.get(':knowledge-point/canonical-example');cid=c.get(':db/id')if isinstance(c,dict)else c;near=[p for p in D['questions']if links[p[':db/id']]==k[':db/id']and p.get(':question/worked-solution')and all(f.get(':answer-field/correct')for f in p.get(':question/answer-fields',[]))][:2];context.append({'q':q,'kp':k[':db/id'],'title':k.get(':knowledge-point/title'),'canonical':Q.get(cid),'nearby':near})
for k in D['kps']:
 g=k.get(':knowledge-point/question-generator')
 if not g:continue
 p=Path('/media/jake/SSD/EDB/math')/g[':question-generator/script'];p=p if p.exists()else R/g[':question-generator/script'];row={'kp':k[':db/id'],'title':k[':knowledge-point/title'],'path':str(p),'registration':g,'exists':p.exists()}
 if p.exists():
  s=p.read_text();(H/('generator-'+str(k[':db/id'])+'.py.txt')).write_text(s);manifest=p.parent/'generator-package.json'
  if manifest.exists():row['manifest']=json.loads(manifest.read_text());files=set(row['manifest']['files'])|{'generator-package.json'}
  else:
   files={p.name};data=p.with_suffix('')
   if data.is_dir():files|={str(f.relative_to(p.parent))for f in data.rglob('*')if f.is_file()and'__pycache__'not in f.parts}
   for n in ast.walk(ast.parse(s)):
    if isinstance(n,ast.ImportFrom)and n.module and(p.parent/(n.module+'.py')).is_file():files.add(n.module+'.py')
  row['files']=sorted(files)
 gs.append(row)
(H/'completion-context.json').write_text(json.dumps(context,indent=2)+'\n');(H/'generators.json').write_text(json.dumps(gs,indent=2)+'\n');print('incomplete',len(inc),'missing solutions',sum(not q.get(':question/worked-solution')for q in inc),'missingkeys',sum(not f.get(':answer-field/correct')for q in inc for f in q.get(':question/answer-fields',[])),'generators',len(gs),'legacy',sum('manifest'not in g for g in gs));print('missing generator scripts',[g['kp']for g in gs if not g['exists']])
