"""Validate required report fields, references, and package immutability."""
import hashlib,json,pathlib
E=pathlib.Path(__file__).resolve().parent
R=pathlib.Path('/home/jake/Developer/Course_Academy')
def read(p):return json.loads(p.read_text())
report=read(E/'result.json');variation=read(E/'pedagogical-variation.json');schema=read(R/'generate/pipeline/pedagogical-variation.schema.json')
# Recursive subset of the schema is sufficient here and independent of runtime deps.
def validate(value,s,path='$'):
 if 'enum' in s:assert value in s['enum'],path
 t=s.get('type')
 if t=='object':
  assert isinstance(value,dict),path
  assert all(k in value for k in s.get('required',[])),path
  if s.get('additionalProperties') is False:assert set(value)<=set(s.get('properties',{})),path
  for k,v in value.items():
   if k in s.get('properties',{}):validate(v,s['properties'][k],path+'.'+k)
 elif t=='array':
  assert isinstance(value,list) and len(value)>=s.get('minItems',0),path
  for i,v in enumerate(value):validate(v,s.get('items',{}),path+f'[{i}]')
 elif t=='string':assert isinstance(value,str) and len(value)>=s.get('minLength',0),path
 elif t in ('number','integer'):
  assert type(value) in ((int,) if t=='integer' else (int,float)),path
  assert value>=s.get('minimum',float('-inf')) and value<=s.get('maximum',float('inf')),path
validate(variation,schema)
refs=[]
def visit(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ('sample_refs','evidence_paths'):refs.extend(v)
   else:visit(v)
 elif isinstance(x,list):
  for v in x:visit(v)
visit(variation);visit(report)
for ref in refs:
 p=pathlib.Path(ref);assert not p.is_absolute() and '..' not in p.parts,ref
 assert (E/p).is_file() and (E/p).stat().st_size>0,ref
assert 'source-analysis.json' in report['source_analysis']['evidence_paths']
assert set(report['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
assert all(x['status']=='passed' and x['evidence_paths'] for x in report['checks'].values())
assert {x['kind'] for x in variation['counterfactuals']}=={'relevant','irrelevant'}
assert any(x['scope']!='overall' for x in variation['shortcut_probes'])
P=E.parent/'workspace';actual={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
assert actual==read(E/'package-before.json')==read(E/'package-after.json')
assert report['verdict']=='accepted' and not report['findings']
(E/'evidence-contract.json').write_text(json.dumps({'passed':True,'pedagogical_schema':'generate/pipeline/pedagogical-variation.schema.json','references_checked':len(refs),'unique_nonempty_evidence_files':len(set(refs)),'eight_checks_present':True,'package_files_unchanged':len(actual)},indent=2)+'\n')
print(json.dumps(read(E/'evidence-contract.json')))
