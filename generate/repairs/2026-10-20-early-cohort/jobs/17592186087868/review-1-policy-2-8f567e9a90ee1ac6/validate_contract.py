import json,pathlib
E=pathlib.Path(__file__).parent
schema=json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'));data=json.load(open(E/'pedagogical-variation.json'))
def validate(v,s,p='$'):
 t=s.get('type');ok={'object':lambda:isinstance(v,dict),'array':lambda:isinstance(v,list),'string':lambda:isinstance(v,str),'integer':lambda:type(v)==int,'number':lambda:type(v) in (int,float)}
 if t:assert ok[t](),(p,'type',t)
 if 'enum' in s:assert v in s['enum'],(p,'enum')
 if isinstance(v,dict):
  assert all(k in v for k in s.get('required',[])),(p,'required')
  props=s.get('properties',{})
  if s.get('additionalProperties') is False:assert set(v)<=set(props),(p,'unknown keys')
  for k,w in v.items():
   if k in props:validate(w,props[k],p+'.'+k)
 if isinstance(v,list):
  assert len(v)>=s.get('minItems',0),(p,'minItems')
  for i,w in enumerate(v):validate(w,s.get('items',{}),p+f'[{i}]')
 if isinstance(v,str):assert len(v)>=s.get('minLength',0),(p,'minLength')
 if type(v) in (int,float):
  if 'minimum' in s:assert v>=s['minimum'],p
  if 'maximum' in s:assert v<=s['maximum'],p
validate(data,schema)
# Every keyword used by this concrete schema has a validation above; $schema is metadata.
def known(s):
 assert set(s)<={'type','properties','required','additionalProperties','enum','items','minItems','minLength','minimum','maximum','$schema'}
 for v in s.get('properties',{}).values():known(v)
 if 'items' in s:known(s['items'])
known(schema)
report=json.load(open(E/'evidence-contract.json'));report['status']='passed: every keyword in supplied schema validated by standard-library recursive validator';(E/'evidence-contract.json').write_text(json.dumps(report,indent=2))
assert all((E/ref).stat().st_size for check in json.load(open(E/'review.json'))['checks'].values() for ref in check['evidence_paths'])
print('Pedagogical schema and evidence paths passed')
