import os,sys,json,pathlib,importlib.util,hashlib,collections,copy,math
ROOT=pathlib.Path.cwd();JOB=ROOT.parent;REPO=pathlib.Path('/home/jake/Developer/Course_Academy');PKG=JOB/'workspace'
os.environ['PYTHONDONTWRITEBYTECODE']='1';os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(ROOT/'assets');sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('audit_generator',PKG/'17592186172038.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import sympy as S
from fractions import Fraction as F

def save(n,x): (ROOT/n).write_text(json.dumps(x,indent=2)+'\n')
def fields(r):return r['question'][':question/answer-fields'][0]
def answer(r):
 f=fields(r);return next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def parse_rhs(prompt):
 t=prompt.split('=',1)[1].strip().rstrip('?$').strip();t=t.replace('\\left','').replace('\\right','').replace('\\,','')
 def group(t,i):
  assert t[i]=='{',(t,i)
  depth=1;j=i+1
  while depth:
   if t[j]=='{':depth+=1
   if t[j]=='}':depth-=1
   j+=1
  return t[i+1:j-1],j
 def frac(t):
  while '\\frac' in t or '\\dfrac' in t:
   import re
   m=re.search(r'\\(?:d?frac)',t);i=m.end();a,j=group(t,i);b,k=group(t,j);t=t[:m.start()]+'(('+frac(a)+')/('+frac(b)+'))'+t[k:]
  return t
 t=frac(t).replace('{','(').replace('}',')').replace('^','**')
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 return parse_expr(t,transformations=standard_transformations+(implicit_multiplication_application,),local_dict={'x':g.X,'y':g.Y})
def independently_check(r):
 # Parse visible equation, derive each slope by exact arithmetic. Read actual image sidecars and endpoint geometry, not generation.exact_slopes.
 expr=parse_rhs(r['question'][':question/problem']);f=fields(r);matches=[];details=[]
 for a in f[':answer-field/choices']:
  p=pathlib.Path(a[':answer/value']);d=json.load(open(p.with_suffix('.json')));pts=d['exact_points'];expected=[S.simplify(expr.subs({g.X:S.Rational(x),g.Y:S.Rational(y)})) for x,y in pts];sl=[S.oo if v=='inf' else S.Rational(v) for v in d['slopes']]
  if expected==sl:matches.append(a[':answer/id'])
  for v,seg in zip(sl,d['segments']):
   (x0,y0),(x1,y1)=seg['endpoints'];actual=math.inf if x1==x0 else (y1-y0)/(x1-x0)
   assert (math.isinf(actual) if v==S.oo else abs(actual-float(v))<1e-9),(actual,v)
  details.append({'choice':a[':answer/id'],'points':pts,'drawn_slopes':list(map(str,sl)),'expected':list(map(str,expected))})
 assert matches==[f[':answer-field/correct'][1]],(matches,f)
 return {'question_id':r['question'][':question/id'],'visible_rhs':str(expr),'unique_matching_key':matches,'choices':details}
def signs(row):return tuple(0 if v==0 else (1 if v>0 else -1) for v in row)
def visible_bank(r):
 out=[]
 for a in fields(r)[':answer-field/choices']:
  d=json.load(open(pathlib.Path(a[':answer/value']).with_suffix('.json')))
  out.append([S.oo if v=='inf' else S.Rational(v) for v in d['slopes']])
 return out

def mirror_probe(r):
 rows=visible_bank(r);pairs=[(i,j) for i in range(5) for j in range(i) if all(a==-b for a,b in zip(rows[i],rows[j]))]
 out={'question_id':r['question'][':question/id'],'template':r['generation']['template'],'seed':r['generation']['seed'],'pairs':pairs,'signs':[signs(row) for row in rows],'correct_index':next(i for i,a in enumerate(fields(r)[':answer-field/choices']) if a[':answer/id']==fields(r)[':answer-field/correct'][1])}
 if len(pairs)==1:
  pair=pairs[0];scores={i:sum(a==b and a!=0 for j in range(5) if j not in pair for a,b in zip(signs(rows[i]),signs(rows[j]))) for i in pair};best=max(scores.values());wins=[i for i in pair if scores[i]==best]
  out.update(scores=scores,unique=len(wins)==1,predicted=wins[0] if len(wins)==1 else None)
  if len(wins)==1:out['success']=wins[0]==out['correct_index']
 return out

def main():
 initial={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()};save('package-before.json',initial)
 import importlib.metadata as md
 save('runtime.json',{'python':sys.version.split()[0],'packages':{v:md.version(v) for v in ['sympy','matplotlib']},'command':sys.argv})
 source_records=[]
 for i,(profile,(t,p,_)) in enumerate(g.PROFILES.items()):source_records.append(g.generate('easy',seed=73071+i,template=t,parameters=copy.deepcopy(p),profile=profile))
 # Canonical example can be replayed with q-80494 profile; validate original slopes even if no exercise answer field was supplied.
 source_records.append(g.generate('easy',seed=73079,template='quadratic_linear',parameters={'a':2,'b':1,'points':[[1,1],[0,1],[1,2]]},profile='q-80494'))
 save('source-replay-records.json',source_records);save('source-replay-math.json',[independently_check(r) for r in source_records])
 records=[];attempts=[]
 original_sample=g.sample
 def counted(level,t,r):
  p=original_sample(level,t,r);attempts.append({'level':level,'template':t,'parameters':p});return p
 g.sample=counted
 for ti,t in enumerate(g.TEMPLATES):
  for i in range(6):
   seed=73100+100*ti+i;before=len(attempts);r=g.generate('easy',seed=seed,template=t);records.append(r);print('sample',t,seed,'attempts',len(attempts)-before,flush=True)
  save('independent-samples.json',records);save('sampling-attempts.json',attempts)
 save('math-results.json',[independently_check(r) for r in records]);save('shortcut-results.json',[mirror_probe(r) for r in records])
 # Sign of a is relevant for rational square; reverse all slopes with points fixed.
 p={'a':1,'points':[[-2,1],[1,2],[3,-1]]}
 before=g.generate('easy',seed=73661,template='rational_square',parameters=p)
 after=g.generate('easy',seed=73661,template='rational_square',parameters={**p,'a':-1})
 # Reordering points changes neither coordinate-slope associations nor selected mathematical diagram.
 irr=g.generate('easy',seed=73661,template='rational_square',parameters={**p,'points':list(reversed(p['points']))})
 # Change exactly one target point: same remaining arithmetic; at the changed point slope must update.
 point=g.generate('easy',seed=73661,template='rational_square',parameters={**p,'points':[[-2,1],[2,2],[3,-1]]})
 cf=[before,after,irr,point];save('counterfactual-records.json',cf);save('counterfactual-math.json',[independently_check(r) for r in cf])
 invalid=[('zero denominator',{'a':1,'points':[[0,1],[1,2],[2,3]]},'rational_square'),('repeated points',{'a':1,'b':2,'points':[[1,1],[1,1],[2,2]]},'affine'),('bank collision',{'a':1,'points':[[-1,0],[1,0],[2,0]]},'rational_square'),('coordinate outside domain',{'a':1,'b':1,'points':[[5,1],[1,1],[2,1]]},'affine')]
 rejection=[]
 for label,p,t in invalid:
  try:g.generate('easy',seed=73900,template=t,parameters=p);rejection.append({'case':label,'rejected':False})
  except Exception as e:rejection.append({'case':label,'rejected':True,'error':str(e)})
 save('generator-rejections.json',rejection)
 batch=json.load(open(JOB/'samples.json'));save('runner-batch.json',batch);save('runner-math.json',[independently_check(r) for r in batch]);save('runner-shortcuts.json',[mirror_probe(r) for r in batch])
 # Exercise every authored radio choice through actual native grader, with independently derived keys.
 cases=[]
 for r in source_records+records+cf+batch:
  f=fields(r);cases.append({'label':str(r['generation']['seed'])+' '+r['generation']['template'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'independent exact equation/segment match'} for a in f[':answer-field/choices']]})
 # Stale-image keys across coefficient change must reject prior correct geometry when submitted as a choice in the new bank.
 old=visible_bank(before)[next(i for i,a in enumerate(fields(before)[':answer-field/choices']) if a[':answer/id']==fields(before)[':answer-field/correct'][1])]
 f=fields(after);newrows=visible_bank(after);oldidx=newrows.index(old)
 cases.append({'label':'relevant coefficient counterfactual old-correct image rejected','record':after,'checks':[{'submitted_answer_id':f[':answer-field/choices'][oldidx][':answer/id'],'expected':'rejected','purpose':'previous correct slopes are now sign-reversal distractor'}]})
 save('grader-input.json',cases)
 stats={'counts':dict(collections.Counter(r['generation']['template'] for r in records)),'attempts':len(attempts),'accepted':len(records),'shortcut':{}}
 for t in g.TEMPLATES:
  probes=[mirror_probe(r) for r in records if r['generation']['template']==t];active=[p for p in probes if p.get('unique')];stats['shortcut'][t]={'eligible':len(active),'correct':sum(p['success'] for p in active),'total':len(probes)}
 save('audit-summary.json',stats);print(json.dumps(stats),flush=True)
 (ROOT/'session-state.md').write_text('Independent source account saved first. Source replay 8 cases, 36 fresh samples, controlled coefficient/point/reordering pairs and all-choice native grader inputs complete. Read audit-summary.json. Delivery, grader execution, actual UI rendering, inventory effects and relocation remain.\n')
if __name__=='__main__':main()
