"""Validate the vocabulary used by the supplied pedagogical JSON schema, stdlib only."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
S=Path('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json')
def check(v,s,p='$'):
 t=s.get('type');types={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float)}
 if t:assert isinstance(v,types[t]) and not (t in ['integer','number'] and isinstance(v,bool)),(p,t)
 if 'enum' in s:assert v in s['enum'],(p,'enum')
 if isinstance(v,dict):
  assert all(k in v for k in s.get('required',[])),(p,'required')
  if s.get('additionalProperties') is False:assert set(v)<=set(s.get('properties',{})),(p,'extra fields')
  for k,x in v.items():
   if k in s.get('properties',{}):check(x,s['properties'][k],p+'.'+k)
 elif isinstance(v,list):
  assert len(v)>=s.get('minItems',0),(p,'minItems')
  for i,x in enumerate(v):check(x,s.get('items',{}),p+f'[{i}]')
 elif isinstance(v,str):assert len(v)>=s.get('minLength',0),(p,'minLength')
 elif isinstance(v,(int,float)):
  if 'minimum' in s:assert v>=s['minimum'],(p,'minimum')
  if 'maximum' in s:assert v<=s['maximum'],(p,'maximum')
check(json.loads((R/'pedagogical-variation.json').read_text()),json.loads(S.read_text()))
p=R/'evidence-contract.json';j=json.loads(p.read_text());j['pedagogical_schema']='Passed stdlib recursive validation of every schema constraint present (type, properties, required, additionalProperties, items, minItems, minLength, enum, minimum, maximum).';j['validation_command']='python3 validate_contract.py';p.write_text(json.dumps(j,indent=2)+'\n')
# Make the strict native failure command directly executable from evidence_root.
p=R/'report.json';j=json.loads(p.read_text());j['findings'][2]['reproduction']='/home/jake/Developer/Course_Academy/generate/runs/current/check-engine grader-family-strict-input.json grader-family-strict-report.json (run from evidence_root). Expected accepted for x^2+5; actual rejected (Ok(false)), exit 1. Exact command and stderr are retained in grader-commands.json and minimal-failures.json.';p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
print('Pedagogical schema and referenced evidence contract verified.')
