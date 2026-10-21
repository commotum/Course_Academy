import json,pathlib,ast
import review as t
E=t.E
errors=[]
def validate(x,s,p='$'):
 typ=s.get('type');typemap={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float)}
 if typ and not isinstance(x,typemap[typ]):errors.append(p+' wrong type');return
 if 'enum'in s and x not in s['enum']:errors.append(p+' enum')
 if isinstance(x,dict):
  for k in s.get('required',[]):
   if k not in x:errors.append(p+' missing '+k)
  if s.get('additionalProperties') is False:
   for k in x:
    if k not in s.get('properties',{}):errors.append(p+' extra '+k)
  for k,v in x.items():
   if k in s.get('properties',{}):validate(v,s['properties'][k],p+'.'+k)
 if isinstance(x,list):
  if len(x)<s.get('minItems',0):errors.append(p+' too short')
  for i,v in enumerate(x):validate(v,s.get('items',{}),p+f'[{i}]')
 if isinstance(x,str) and len(x)<s.get('minLength',0):errors.append(p+' empty')
 if isinstance(x,(int,float)):
  if x<s.get('minimum',float('-inf')) or x>s.get('maximum',float('inf')):errors.append(p+' range')

def paths(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ('sample_refs','evidence_paths'):
    for p in v:
     f=E/p
     if pathlib.Path(p).is_absolute() or not f.is_file() or f.stat().st_size==0:errors.append('invalid evidence path '+p)
   else:paths(v)
 elif isinstance(x,list):
  for v in x:paths(v)
ped=json.load(open(E/'pedagogical-variation.json'));schema=json.load(open(t.R/'generate/pipeline/pedagogical-variation.schema.json'));validate(ped,schema);paths(ped)
result=json.load(open(E/'result.json'));paths(result)
assert set(result['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
for n,c in result['checks'].items():
 if c['status']=='passed' and not c['evidence_paths']:errors.append(n+' no evidence')
metadata=[]
for p in [t.W/'generator.py',t.W/'math_format.py']:
 tree=ast.parse(p.read_text());metadata.append({'file':p.name,'imports':[n.module if isinstance(n,ast.ImportFrom) else ','.join(a.name for a in n.names) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]})
t.save('runtime-imports.json',metadata)
a=json.load(open(E/'package-before.json'));b=t.package_hashes();t.save('package-after.json',b)
if a!=b:errors.append('package changed')
for x in json.load(open(E/'affected-inventory.json'))['affected_questions']:
 records=json.load(open(E/x['evidence_path']));assert any(r['question'][':question/id']==x['question_id'] and r['generation'] for r in records)
t.save('evidence-contract-results.json',{'passed':not errors,'errors':errors,'pedagogical_schema':'generate/pipeline/pedagogical-variation.schema.json','package_unchanged':a==b,'checks':{n:c['status'] for n,c in result['checks'].items()}})
print(json.dumps({'passed':not errors,'errors':errors,'package_unchanged':a==b}))
raise SystemExit(bool(errors))
