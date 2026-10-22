import json,pathlib,jsonschema
E=pathlib.Path(__file__).resolve().parent
schema=json.load(open('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'))
p=json.load(open(E/'pedagogical-variation.json'));jsonschema.Draft202012Validator(schema).validate(p)
r=json.load(open(E/'review-result.json'))
required={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
assert set(r['checks'])==required and all(x['status']=='passed' for x in r['checks'].values())
assert r['verdict']=='accepted' and r['findings']==[]
refs=[]
def scan(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k in ('sample_refs','evidence_paths'): refs.extend(x)
   else:scan(x)
 elif isinstance(v,list):
  for x in v:scan(x)
scan(p);scan(r)
for x in refs:
 path=pathlib.Path(x);assert not path.is_absolute() and '..' not in path.parts and (E/path).is_file() and (E/path).stat().st_size,x
assert json.load(open(E/'package-integrity.json'))['unchanged']
out={'pedagogical_schema_valid':True,'eight_checks_present':True,'all_referenced_evidence_nonempty':True,'unique_evidence_paths':len(set(refs)),'package_unchanged':True,'result':'accepted'}
(E/'contract-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
