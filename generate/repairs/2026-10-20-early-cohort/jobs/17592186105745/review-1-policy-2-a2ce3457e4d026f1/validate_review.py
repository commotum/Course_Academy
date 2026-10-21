#!/usr/bin/env python3
"""Validate this review's evidence contract without changing the package."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def validate(x,s,path='$'):
 if 'enum' in s:assert x in s['enum'],path
 tp=s.get('type')
 if tp=='object':
  assert isinstance(x,dict),path
  assert all(k in x for k in s.get('required',[])),path
  if s.get('additionalProperties') is False:assert not(set(x)-set(s['properties'])),path
  for k,v in x.items():
   if k in s.get('properties',{}):validate(v,s['properties'][k],path+'.'+k)
 elif tp=='array':
  assert isinstance(x,list) and len(x)>=s.get('minItems',0),path
  for i,v in enumerate(x):validate(v,s['items'],path+f'[{i}]')
 elif tp=='string':assert isinstance(x,str) and len(x)>=s.get('minLength',0),path
 elif tp=='integer':assert type(x)==int and x>=s.get('minimum',-float('inf')),path
 elif tp=='number':assert type(x) in (int,float) and s.get('minimum',-float('inf'))<=x<=s.get('maximum',float('inf')),path
def main():
 p=read(R/'pedagogical-variation.json');schema=read(pathlib.Path('/home/jake/Developer/Course_Academy/generate/pipeline/pedagogical-variation.schema.json'));validate(p,schema)
 paths=[]
 def refs(x):
  if isinstance(x,dict):
   for k,v in x.items():
    if k in ['sample_refs','evidence_paths']:paths.extend(v)
    else:refs(v)
  elif isinstance(x,list):
   for v in x:refs(v)
 result=read(R/'result.json');refs(result);refs(p)
 for n in paths:
  q=pathlib.Path(n);assert not q.is_absolute() and '..' not in q.parts,n
  assert (R/q).is_file() and (R/q).stat().st_size,n
 assert set(result['checks'])=={'source_replay','math','variety','scope','grading','rendering','packaging','decision_variation'}
 assert all(c['status']=='passed' and c['evidence_paths'] for c in result['checks'].values())
 assert result['verdict']=='accepted' and result['findings']==[]
 assert read(R/'package-hashes-before.json')==read(R/'package-hashes-final.json')
 assert read(R/'affected-inventory.json')=={'affected_questions':[]}
 assert all(len(json.loads((R/folder/'input.json').read_text()))==len(read(R/folder/'rendering.json')['cases']) for folder in ['render','render-remaining'])
 summary={'pedagogical_schema_valid':True,'evidence_refs_checked':len(paths),'unique_nonempty_evidence_files':len(set(paths)),'all_eight_checks_passed':True,'package_unchanged':True,'verdict':'accepted'}
 (R/'evidence-validation.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary))
if __name__=='__main__':main()
