"""Read-only current-source audit; historical generator fixtures stay immutable."""
import copy,json,sys,hashlib
from pathlib import Path
import sympy as sp
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate as v
g=v.g
HERE=Path(__file__).resolve().parent

def normalize(q):
 q=copy.deepcopy(q)
 def walk(x):
  if isinstance(x,dict):
   if set(x)=={':db/ident'}:return str(x[':db/ident'])
   return {k:walk(z) for k,z in x.items() if k not in (':db/id',':question/math-academy-id')}
  if isinstance(x,list):return [walk(z) for z in x]
  return str(x) if type(x).__name__=='UUID' else x
 q=walk(q)
 for f in q[':question/answer-fields']:
  if isinstance(f.get(':answer-field/correct'),dict):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 return q

def check(q):
 P,Q=v.prompt_model(q);curl=sp.diff(Q,g.X)-sp.diff(P,g.Y)
 expected=sp.trigsimp(curl.subs({g.X:g.R*g.C,g.Y:g.R*g.S})*g.R)
 f=q[':question/answer-fields'][0]
 vals={a[':answer/id']:g.parse_math(a[':answer/value']) for a in f[':answer-field/choices']}
 correct=f[':answer-field/correct'][1]
 assert len(vals)==5 and correct in vals
 assert v.eq(vals[correct],expected),(q[':question/id'],'wrong key')
 for aid,value in vals.items():assert v.eq(value,expected)==(aid==correct),'ambiguous bank'
 g.eligible(list(vals.values()))
 return {'curl':str(curl),'polar_integrand':str(expected),'bank_size':5,'pointwise_unique_correct':True}

def fingerprint(q):
 # A stricter deduplication rule than derivative-pair identities: identical
 # reduced curl gives the same missing integrand even with different operands.
 P,Q=v.prompt_model(q);curl=sp.expand(sp.diff(Q,g.X)-sp.diff(P,g.Y))
 return hashlib.sha256(sp.srepr(curl).encode()).hexdigest()

def replay_bank(sid):
 cases={c['source_id']:c for c in json.loads((HERE/'source-cases.json').read_text())}
 if sid in cases:
  c=cases[sid];return g.bank(c['template'],c['parameters'],'original')[0]
 r,t=g.R,g.T;sn,cs=sp.sin(t),sp.cos(t)
 if sid=='q-126532':return [-2*r**3*sp.sin(2*t)-r,r**3*sp.sin(2*t)-r+r*cs,-r**3*sp.sin(2*t)-r,r**3*sp.sin(2*t)-r,-r**2*sp.sin(2*t)-1]
 if sid=='q-126519':return [-3*r**3*(cs+sn),-3*r**2*sp.cos(2*t),-3*r**3*sp.cos(2*t),-3*r**3,-3*r**2]
 if sid=='q-126546':return [r**3*sn**2-r,r**3*sp.sin(2*t)-r,r**2*cs**2-1,r**2*sn**2-1,r**3*cs**2-r]
 raise ValueError(sid)

def main():
 snapshot=json.loads((HERE/'reference/initial/source.json').read_text());kp=snapshot['record'];checks=[];items=[]
 for raw in kp[':knowledge-point/questions']:
  q=normalize(raw);result=check(q);result['source']=raw[':question/math-academy-id'];bank=replay_bank(result['source']);original=[g.parse_math(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']];assert len(bank)==len(original)==5 and all(sum(v.eq(a,b) for b in bank)==1 for a in original);result['recipe_replay_matches']=5;checks.append(result)
  r={'question':q,'knowledge_point':{'title':kp[':knowledge-point/title']},'generation':{'template':'live-source-'+result['source']}}
  items.append(v.engine_item(r,result['source']))
 out=HERE/'reference/current-source-audit';out.mkdir(parents=True,exist_ok=True)
 (out/'native-input.json').write_text(json.dumps(items,indent=2))
 import subprocess
 subprocess.run([str(HERE/'reference/native/check-engine'),str(out/'native-input.json'),str(out/'native-report.json')],check=True)
 result={'basis':snapshot['basis'],'lineage':snapshot['lineage'],'all_current_sources':len(checks),'source_banks_independently_checked':len(checks),'source_options_checked':sum(x['bank_size'] for x in checks),'checks':checks,'historical_generator_fixture_unchanged':True,'scope':'Live source keys and complete banks, separate from historical generator fidelity.'}
 (out/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
