"""Regression efa97df560cec8fee6e1: visible math and delivered mixed-role coverage."""
import argparse, importlib.util, json, pathlib, subprocess, sys
sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = pathlib.Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0, str(ROOT/'17592186229165'))
import validate as V
from math_parser import scalar, eq, displays, rows, equal, x, alpha, beta

def load(p): return json.loads(pathlib.Path(p).read_text())
def save(out, name, data): (out/name).write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n')
def module(path):
 spec=importlib.util.spec_from_file_location('candidate',path)
 g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g

def visible_role(r):
 q=r['question'];h,forcing,v,_=V.read_prompt(q[':question/problem'])
 # Read the forcing terms in displayed order, rather than trusting template metadata.
 rhs=displays(q[':question/problem'])[0].split('=',1)[1].split(r',\,')[0]
 import re
 rates=[scalar(k).coeff(x) for k in re.findall(r'\{e\}\^\{([^{}]+)\}',rhs)]
 assert len(rates)==2 and rates[0]!=rates[1]
 return next((i for i,k in enumerate(rates) if k==h),None)

def audit(r):
 V.validate_record(r,'hard')
 q=r['question'];bs=displays(q[':question/worked-solution'])
 pos=visible_role(r)
 if pos is None:
  assert 'Neither exponential' in q[':question/worked-solution']
 else:
  assert 'The '+('first' if pos==0 else 'second')+' exponential is a term' in q[':question/worked-solution']
  _,trial=eq(bs[2]);resonant_symbol=(alpha,beta)[pos];other=(beta,alpha)[pos]
  h,_,_,_=V.read_prompt(q[':question/problem'])
  import sympy as s
  assert equal(trial.coeff(resonant_symbol), x*s.exp(h*x))
  assert not equal(trial.coeff(other), x*s.exp(h*x))
 return pos

def coverage(records):
 from collections import Counter,defaultdict
 groups=defaultdict(Counter);positions=Counter()
 for r in records:
  pos=audit(r);key='none' if pos is None else str(pos+1);positions[key]+=1
  # Cues tested within mixed family. No template/profile metadata used to determine position.
  if pos is not None:
   q=r['question'];h,forcing,_,_=V.read_prompt(q[':question/problem'])
   import sympy as s,re
   rhs=displays(q[':question/problem'])[0].split('=',1)[1].split(r',\,')[0]
   exps=[scalar(k).coeff(x) for k in re.findall(r'\{e\}\^\{([^{}]+)\}',rhs)]
   for cue,value in [('h_sign','positive' if h>0 else 'negative'),('rate_order','ascending' if exps[0]<exps[1] else 'descending'),('first_coefficient_sign','negative' if rhs.startswith('-') else 'positive')]:
    groups[cue+':'+value][key]+=1
 mixed=positions['1']+positions['2']
 return {'positions':dict(positions),'mixed_cases':mixed,'last_term_ordinary_shortcut':{'successes':positions['1'],'attempts':mixed,'role_constant_baseline':max(positions['1'],positions['2'])},'cue_groups':{k:dict(v) for k,v in groups.items()},'semantic_instances':len({r['generation']['mathematical_fingerprint'] for r in records})}

def main():
 a=argparse.ArgumentParser();a.add_argument('--entry',type=pathlib.Path,default=ROOT/'17592186229165.py');a.add_argument('--output',type=pathlib.Path,default=ROOT/'evidence/role-regression');z=a.parse_args()
 out=z.output.resolve();out.mkdir(parents=True,exist_ok=True);g=module(z.entry)
 p=dict(h=1,k=1,f=1,k2=2,f2=1,v=0)
 before=g.generate('hard',template='mixed',parameters=p,seed=90211)
 after=g.generate('hard',template='mixed',parameters=dict(p,k=2,k2=1),seed=90211)
 assert audit(before)==0 and audit(after)==1
 ans=lambda r:scalar(r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])
 import sympy as s
 expected=(x-1)*s.exp(x)+s.exp(2*x)
 assert equal(ans(before),expected) and equal(ans(after),expected)
 assert before['generation']['mathematical_fingerprint']==after['generation']['mathematical_fingerprint']
 # Same displayed forcing and IC; h alone moves the resonant role and changes the answer.
 transfer=g.generate('hard',template='mixed',parameters=dict(p,h=2),seed=90211)
 assert audit(transfer)==1 and not equal(ans(transfer),ans(before))
 assert V.read_prompt(before['question'][':question/problem'])[1:3]==V.read_prompt(transfer['question'][':question/problem'])[1:3]
 controlled=[before,after,transfer]
 # Signed boundaries, unit exponents, unequal forcing, and A=0. Swap whole components.
 for p in [dict(h=-6,k=-6,f=-12,k2=6,f2=12,v=1),dict(h=6,k=6,f=12,k2=-6,f2=-12,v=-1),dict(h=-1,k=-1,f=3,k2=1,f2=4,v=2)]:
  q=dict(p,k=p['k2'],f=p['f2'],k2=p['k'],f2=p['f'])
  r=g.generate('hard',template='mixed',parameters=p);t=g.generate('hard',template='mixed',parameters=q)
  assert audit(r)==0 and audit(t)==1 and equal(ans(r),ans(t))
  controlled.extend([r,t])
 samples=[g.generate('hard',template='mixed',seed=i) for i in range(67031,67055)]
 default=[g.generate('hard',seed=i) for i in range(67031,67039)]
 for r in samples+default: audit(r)
 assert {visible_role(r) for r in samples}=={0,1},'Ordinary sampling must exercise both resonant positions'
 # Neither nonresonance nor duplicate forcing is valid in mixed, even on explicit input.
 for bad in [dict(h=3,k=1,f=1,k2=2,f2=1,v=0),dict(h=1,k=1,f=1,k2=1,f2=1,v=0)]:
  try:g.generate('hard',template='mixed',parameters=bad)
  except ValueError:pass
  else:raise AssertionError(('Invalid mixed admitted',bad))
 records=controlled+samples+default
 save(out,'records.json',records);save(out,'render-records.json',[before,after,transfer,controlled[3],controlled[4]])
 # Shared delivery applies publisher validation, exact difficulty and inventory dedup.
 command=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(out/'records.json'),'--source',str(ROOT.parent/'source/source.json'),'--inventory',str(ROOT.parent/'source/inventory.json'),'--difficulty','hard','--output',str(out/'delivery'),'--asset-root',str(out),'--math-root','/media/jake/SSD/EDB/math']
 proc=subprocess.run(command,text=True,capture_output=True)
 (out/'delivery.log').write_text(proc.stdout+proc.stderr);assert proc.returncode==0,(proc.returncode,proc.stderr[-2000:])
 delivered=load(out/'delivery/accepted.json');post=coverage(delivered);pre=coverage(records)
 assert post['positions'].get('1',0)>0 and post['positions'].get('2',0)>0,'Delivery lost a resonant role'
 # The native engine must accept preserved answers across reorder, reject stale answers after transfer.
 graders=[]
 for i,r in enumerate(controlled):
  y=ans(r);h,_,v,_=V.read_prompt(r['question'][':question/problem'])
  checks=[{'submitted':s.latex(s.factor(y)),'expected':'accepted','purpose':'independently parsed equivalent factored expression'}, {'submitted':s.latex(y+s.exp(h*x)),'expected':'rejected','purpose':'ODE preserved, initial value wrong'}, {'submitted':'0','expected':'rejected','purpose':'nonzero forcing ignored'}]
  if i<3:checks.append({'submitted':s.latex(expected),'expected':'rejected' if i==2 else 'accepted','purpose':'reorder preserves response; exponent overlap transfer changes it'})
  graders.append({'label':'role-'+str(i),'record':r,'checks':checks})
 save(out,'grader-input.json',graders)
 command2=[str(REPO/'generate/runs/current/check-engine'),str(out/'grader-input.json'),str(out/'grader-report.json')]
 proc=subprocess.run(command2,text=True,capture_output=True);(out/'grader.log').write_text(proc.stdout+proc.stderr);assert proc.returncode==0,(proc.returncode,proc.stderr[-2000:])
 report={'finding':'efa97df560cec8fee6e1','status':'passed','controlled':len(controlled),'sampled':len(samples),'default_hard':len(default),'pre_delivery':pre,'post_delivery':post,'commands':[command,command2],'native_report':load(out/'grader-report.json')}
 save(out,'results.json',report)
 print(json.dumps({k:v for k,v in report.items() if k not in ('native_report','commands')},indent=2))
if __name__=='__main__':main()
