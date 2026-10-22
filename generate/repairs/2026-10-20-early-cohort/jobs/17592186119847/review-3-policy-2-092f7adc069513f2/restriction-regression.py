"""Strict expected-success regression; exits 1 on the current generator."""
import sys,json,importlib.util,pathlib
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
package=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else E.parent/'workspace'
s=importlib.util.spec_from_file_location('candidate',package/'17592186119847.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
for p,expected in [({'name':'A','rows':3,'columns':4,'count':2,'kind':'non-pivot'},2),({'name':'A','rows':4,'columns':7,'count':3,'kind':'non-pivot'},4)]:
 accepted=[];errors={}
 for profile in g.PROFILES['moderate']:
  try:r=g.generate('moderate',17,parameters=p,bank_profile=profile)
  except ValueError as error:errors[profile]=str(error);continue
  f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
  assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)==str(expected)
  assert len({a[':answer/value'] for a in f[':answer-field/choices']})==5
  accepted.append(r)
 assert accepted, f'Feasible source-method instance was rejected by every profile: {p}; {errors}'
 print(json.dumps(accepted[0],indent=2))
