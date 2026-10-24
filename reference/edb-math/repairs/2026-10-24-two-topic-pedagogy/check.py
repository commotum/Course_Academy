"""Read printed expressions independently; verify transformation, primitive and answer."""
from collections import Counter
import copy,importlib.util,json,re,sys
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'generate'))
from generator_publish import prepare_records,content_fingerprint,validate_question
from substitution_pedagogy_batch_policy import validate_delivery_batch
from read_math import scalar,integral,X,U
import substitution_pedagogy as model

def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def equal(a,b):return s.simplify(s.expand_log(a-b,force=True))==0
def check(row):
 q=row['question'];problem=q[':question/problem'];sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
 body,var,lo,hi=integral(re.findall(r'\$\$\s*(.*?)\s*\$\$',problem,re.S)[0]);assert var==X
 inner=scalar(re.search(r'Let \$u=(.*?)\$',sol)[1]);du=scalar(re.search(r'\\mathrm\{d\}u=\((.*?)\)\\,',sol)[1]);assert equal(s.diff(inner,X),du)
 substitution=next(b for b in blocks if b.count(r'\int')==2).replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace(r'\\','').replace('&','')
 left,right=substitution.split('=',1);leftbody,_,ll,lh=integral(left);trans,uv,u0,u1=integral(right.rstrip('.'))
 assert equal(leftbody,body)and lo==ll and hi==lh and uv==U
 assert equal(trans.subs(U,inner)*du,body),(body,trans,inner,du)
 if lo is not None:
  assert lo<hi and equal(inner.subs(X,lo),u0)and equal(inner.subs(X,hi),u1)
 f=q[':question/answer-fields'][0];key=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])
 easy=row['question'][':question/difficulty'].endswith('/easy')
 if easy:
  vals=[];matches=[]
  for a in f[':answer-field/choices']:
   t,v,l,h=integral(a[':answer/value']);assert v==U and l==u0 and h==u1
   # All banks differ only by scalar on this nonzero integrand.
   ratio=s.simplify(t/trans);assert ratio.is_number and ratio!=0
   assert all(not equal(ratio,z)for z in vals);vals.append(ratio)
   if ratio==1:matches.append(a[':answer/id'])
  assert matches==[f[':answer-field/correct'][1]]
  answer=None
 else:
  formula=re.search(r'You may use \$(.*?)\$',problem)[1];lhs,rhs=formula.rsplit('=',1);tf,tv,_,_=integral(lhs);primitive=scalar(rhs.removesuffix('+C'))
  derivative=s.diff(primitive,U)
  # SymPy differentiates asec with sqrt(1-1/u²); verify on both real components.
  if derivative.has(s.Abs)or tf.has(s.Abs):
   for sign in(1,-1):
    z=s.Symbol('v',positive=True);assert equal((derivative-tf).subs(U,sign*(z+1)),0),(derivative,tf)
  else:assert equal(derivative,tf),(derivative,tf)
  factor=s.simplify(trans/tf);assert not factor.has(U)
  if lo is None:
   value=scalar(key.removesuffix('+C'));expected=factor*primitive.subs(U,inner)
   assert equal(value,expected),(key,expected)
   answer=value
   if f[':answer-field/type']==':answer-field.type/radio':
    values=[scalar(a[':answer/value'].removesuffix('+C'))for a in f[':answer-field/choices']]
    assert len({str(s.simplify(v/expected))for v in values})==5
    assert sum(equal(v,expected)for v in values)==1
  else:
   answer=factor*(primitive.subs(U,u1)-primitive.subs(U,u0));assert equal(scalar(key),answer),(key,answer)
 assert blocks[-1].strip().rstrip('.')==key+('+C'if not easy and lo is None and f[':answer-field/type']==':answer-field.type/blank'else '')
 return key,lo,answer

def main():
 summary={};render=[]
 for kp in model.CASES:
  d=H/str(kp);ev=json.loads((d/'package/source-evidence.json').read_text());pool=[];samples=[]
  for band in('easy','moderate','hard'):
   pool+=model.batch(kp,band,8,20261024,evidence=ev);samples+=model.batch(kp,band,8,112358,evidence=ev)
  for row in pool+samples:validate_question(row['question']);check(row);validate_delivery_batch([row],kp)
  inv=json.loads((d/'inventory/inventory.json').read_text());fingerprints={content_fingerprint(q)for q in inv['questions']+[inv['canonical_example']]}
  accepted,dup=prepare_records(pool,kp,ev['kp']['id'],fingerprints,ROOT,d/'package');assert len(accepted)==24 and dup==0
  grader=[]
  for i,row in enumerate(accepted):
   key,lo,answer=check(row);f=row['question'][':question/answer-fields'][0]
   if f[':answer-field/type']==':answer-field.type/radio':checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected'}for a in f[':answer-field/choices']]
   else:
    checks=[{'submitted':key,'expected':'accepted'},{'submitted':r'\frac{2\left('+key+r'\right)}{2}','expected':'accepted'},{'submitted':'2('+key+')'if lo is None else '('+key+')+1','expected':'rejected'}]
    if lo is None:checks.append({'submitted':'('+key+')+1','expected':'accepted'})
   grader.append({'label':str(kp)+' '+str(i),'record':row,'checks':checks})
  bad=copy.deepcopy(pool[8]);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('You may use $','Recall $')
  try:validate_delivery_batch([bad],kp)
  except ValueError:pass
  else:raise AssertionError('Missing primitive allowed')
  old=json.loads((d/'retirement-candidates.json').read_text());save(d/'retirement-evidence.json',[{'entity':q[':db/id'],'uuid':q[':question/id'],'finding':'Superseded generated pool under the reviewed scaffolding/difficulty contract','record_before':q}for q in old])
  report={'passed':True,'pool_counts':dict(Counter(r['question'][':question/difficulty']for r in pool)),'printed_records_checked':len(pool)+len(samples),'delivered_records_rechecked':len(accepted),'retirements':len(old),'negative_control_missing_primitive_rejected':True,'source_counts':ev['source_counts'],'band_origin':ev['band_origin']}
  for name,value in[('candidate-pool',pool),('accepted-pool',accepted),('regression-samples',samples),('grader-input',grader),('generator-verification',report)]:save(d/(name+'.json'),value)
  summary[str(kp)]=report;render.extend([accepted[i]for i in(0,8,16)]);print(kp,'checked',flush=True)
 save(H/'render-input.json',render);save(H/'generator-verification.json',summary)
if __name__=='__main__':main()
