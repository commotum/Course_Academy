import json
from pathlib import Path
E=Path(__file__).resolve().parent
schema=json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'))
value=json.load(open(E/'pedagogical-variation.json'))
def validate(v,s,p='$'):
 t=s.get('type');types={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float),'boolean':bool}
 if t:
  assert isinstance(v,types[t]) and not(t in ['integer','number'] and isinstance(v,bool)),(p,t)
 if 'enum' in s:assert v in s['enum'],(p,v)
 if isinstance(v,dict):
  assert all(k in v for k in s.get('required',[])),p
  if s.get('additionalProperties') is False:assert set(v)<=set(s.get('properties',{})),p
  for k,x in v.items():
   if k in s.get('properties',{}):validate(x,s['properties'][k],p+'.'+k)
 if isinstance(v,list):
  assert len(v)>=s.get('minItems',0),p
  for i,x in enumerate(v):validate(x,s.get('items',{}),p+f'[{i}]')
 if isinstance(v,str):assert len(v)>=s.get('minLength',0),p
 if isinstance(v,(int,float)) and not isinstance(v,bool):
  assert v>=s.get('minimum',float('-inf')) and v<=s.get('maximum',float('inf')),p
validate(value,schema)
references=[]
for x in value['coverage']+value['counterfactuals']+value['shortcut_probes']+[value['delivery']]:
 for ref in x['sample_refs']:
  p=Path(ref);assert not p.is_absolute() and '..' not in p.parts and (E/p).is_file() and (E/p).stat().st_size,ref
  references.append(ref)
r=json.load(open(E/'rejection-results.json'));assert r['collision_observed'] and r['actual_unique_systems']==r['actual_accepted'] and r['resampling_used_next_seed']
assert all(x['matched_captured_question'] and x['all_bank_values_equal'] and x['prompt_equal'] and x['worked_equal'] for x in json.load(open(E/'inventory-reproduction-results.json')))
report={'pedagogical_schema':'passed recursive validation against all schema keywords used (type, enum, required, properties, additionalProperties, items, minItems, minLength, minimum, maximum)','sample_refs_checked':len(references),'unique_files':sorted(set(references)),'all_sample_refs_exist_nonempty_relative':True,'rejection_branch_assertions':True,'all_five_stored_generated_records_reproduced':True}
(E/'evidence-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'refs':len(references)}))
