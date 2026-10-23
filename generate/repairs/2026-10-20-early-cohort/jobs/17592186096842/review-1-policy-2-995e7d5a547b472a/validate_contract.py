import json,pathlib,jsonschema
r=pathlib.Path.cwd();ped=json.load(open('pedagogical-variation.json'));schema=json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'));jsonschema.validate(ped,schema)
result=json.load(open('result.json'));paths=[]
def scan(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in ['sample_refs','evidence_paths']:paths.extend(v)
   else:scan(v)
 elif isinstance(x,list):
  for v in x:scan(v)
scan(ped);scan(result)
for p in paths:
 assert not pathlib.Path(p).is_absolute(),p
 assert (r/p).is_file() and (r/p).stat().st_size>0,p
assert set(result['checks'])==set('source_replay math variety scope grading rendering packaging decision_variation'.split())
assert len(json.load(open('math-results.json')))==89
assert all(x['math_ok'] and x['correct_count']==1 for x in json.load(open('math-results.json')))
assert json.load(open('grader-results.json'))['documented_unresolved_checks']==0
assert all(json.load(open(p))['passed'] for p in ['render/rendering.json','render-extra/rendering.json'])
assert json.load(open('packaging-results.json'))['final_package_unchanged']
report={'pedagogical_schema':'passed','all_evidence_paths_nonempty':True,'path_references':len(paths),'math_records':89,'native_grader_checks':414,'verdict':result['verdict']}
(r/'evidence-contract.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
