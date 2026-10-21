import json,math
from pathlib import Path
E=Path(__file__).resolve().parent
schema=json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'))
def validate(v,s,p='$'):
 t=s.get('type')
 good={'object':lambda:isinstance(v,dict),'array':lambda:isinstance(v,list),'string':lambda:isinstance(v,str),'integer':lambda:isinstance(v,int) and not isinstance(v,bool),'number':lambda:isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v),'boolean':lambda:isinstance(v,bool)}
 if t:assert good[t](),(p,'type',t)
 if 'enum'in s:assert v in s['enum'],(p,'enum')
 if isinstance(v,dict):
  assert set(s.get('required',[]))<=set(v),(p,'required')
  if s.get('additionalProperties') is False:assert set(v)<=set(s.get('properties',{})),(p,'extra')
  for k,z in v.items():
   if k in s.get('properties',{}):validate(z,s['properties'][k],p+'.'+k)
 if isinstance(v,list):
  assert len(v)>=s.get('minItems',0),(p,'minItems')
  for i,z in enumerate(v):validate(z,s.get('items',{}),p+f'[{i}]')
 if isinstance(v,str):assert len(v)>=s.get('minLength',0),(p,'minLength')
 if isinstance(v,(int,float)):
  if 'minimum'in s:assert v>=s['minimum'],(p,'minimum')
  if 'maximum'in s:assert v<=s['maximum'],(p,'maximum')
validate(json.load(open(E/'pedagogical-variation.json')),schema)
r=json.load(open(E/'review-result.json'))
for z in [r['source_analysis']]+list(r['checks'].values()):
 for ref in z['evidence_paths']:assert not Path(ref).is_absolute() and (E/ref).is_file() and (E/ref).stat().st_size
p=E/'report-validation.json';x=json.load(open(p));x['pedagogical_schema']='Passed full supplied schema vocabulary via validate_contract.py (stdlib validator).';p.write_text(json.dumps(x,indent=2)+'\n');print('Pedagogical schema and all source/check evidence paths pass.')
