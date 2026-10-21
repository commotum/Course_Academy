import json,pathlib,hashlib
E=pathlib.Path(__file__).resolve().parent;R=pathlib.Path('/home/jake/Developer/Course_Academy');W=E.parent/'workspace'
def load(p):return json.loads(p.read_text())
def validate(v,s,path='$'):
 t=s.get('type');valid={'object':lambda:isinstance(v,dict),'array':lambda:isinstance(v,list),'string':lambda:isinstance(v,str),'integer':lambda:isinstance(v,int) and not isinstance(v,bool),'number':lambda:isinstance(v,(int,float)) and not isinstance(v,bool),'boolean':lambda:isinstance(v,bool)}
 if t:assert valid[t](),(path,t)
 if 'enum' in s:assert v in s['enum'],path
 if isinstance(v,dict):
  assert set(s.get('required',[]))<=set(v),path
  if s.get('additionalProperties') is False:assert set(v)<=set(s.get('properties',{})),path
  for k,x in v.items():
   if k in s.get('properties',{}):validate(x,s['properties'][k],path+'.'+k)
 if isinstance(v,list):
  assert len(v)>=s.get('minItems',0),path
  for i,x in enumerate(v):validate(x,s.get('items',{}),path+f'[{i}]')
 if isinstance(v,str):assert len(v)>=s.get('minLength',0),path
 if isinstance(v,(float,int)):
  if 'minimum' in s:assert v>=s['minimum'],path
  if 'maximum' in s:assert v<=s['maximum'],path
schema=load(R/'generate/pipeline/pedagogical-variation.schema.json');pv=load(E/'pedagogical-variation.json');validate(pv,schema)
paths=[]
def visit(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k in ['sample_refs','evidence_paths']:paths.extend(x)
   else:visit(x)
 elif isinstance(v,list):
  for x in v:visit(x)
result=load(E/'result.json');visit(result);visit(pv)
for x in paths:
 p=pathlib.Path(x);assert not p.is_absolute() and '..' not in p.parts,x;assert (E/p).is_file() and (E/p).stat().st_size>0,x
assert set(result['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
assert 'source-analysis.json' in result['source_analysis']['evidence_paths']
assert all(v['evidence_paths'] for v in result['checks'].values())
assert load(E/'affected-inventory.json')=={'affected_questions':[]}
assert all(x['passed'] for x in load(E/'math-results.json'))
assert load(E/'render-full/rendering.json')['passed'] and load(E/'render-target/rendering.json')['passed']
assert load(E/'package-before.json')=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in W.iterdir() if p.is_file()}
assert len(load(E/'grader-input.json'))==111
summary={'pedagogical_schema_passed':True,'all_relative_evidence_paths_exist_and_nonempty':True,'evidence_references':len(paths),'eight_checks_present':True,'package_root_file_hashes_unchanged':True,'native_grader_records':111,'rendered_records':11,'distinct_rendered_records':10,'verdict':result['verdict'],'inventory_limit':'No certified identity/metadata replay; empty affected list does not verify absence.'}
(E/'evidence-validation.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
(E/'session-state.md').write_text('Review complete: result.json verdict revise for statistical coordinate-order answer leakage. Both prior findings repaired and verified against prior failing code. Source/math/scope/grading/rendering/packaging pass; variety and decision_variation fail. Control median cue: 31/96; actual CLI 77 candidates -> 64 survivors, median 24/64, all survive delivery. Exact batch 2/5, no standalone universal batch failure claimed. Native grader 46 accepted / 125 rejected; 11 actual-UI renders (10 distinct records), representative screenshots inspected. Pedagogical schema and evidence paths validated. Five non-source inventory candidates inspected; no certified matching identity/generation metadata. Package root file hashes unchanged; no package edits or database writes.\n')
