import os,sys,json,pathlib,importlib.util,hashlib,shutil,subprocess,re,itertools,collections,copy
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
R=pathlib.Path('/home/jake/Developer/Course_Academy');J=R/'generate/repairs/2026-10-20-early-cohort/jobs/17592186147456'; W=J/'workspace'; PY=R/'.venv/bin/python'
def save(n,d): (E/n).write_text(json.dumps(d,indent=2,default=str)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
def hashes():return {str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()}
if not (E/'package-before.json').exists():save('package-before.json',hashes())
sys.path.insert(0,str(W));sys.path.insert(0,str(W/'checks/vendor'))
spec=importlib.util.spec_from_file_location('review_generator',W/'17592186147456.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import sympy as s
from sympy.parsing.latex import parse_latex
x,y,z=s.symbols('x y z',positive=True)
def parse(t):
 t=t.replace('⁡','').replace('{e}','e'); t=re.sub(r'\\operatorname\{(tan|sin|cos|sec|ln)\}', lambda m:'\\'+m.group(1)+' ',t); t=t.replace('{cos}',r'\cos '); return parse_latex(t).subs({s.Symbol('x'):x,s.Symbol('y'):y,s.Symbol('z'):z})
def eq(t):
 t=t.strip('$').replace('{y}^{′}','z').replace('y^{′}','z').replace("y'",'z')
 lhs,rhs=t.split('='); l=parse(lhs);b=parse(rhs);m=s.diff(l,z);a=s.simplify(l-m*z);assert not a.has(z) and not m.has(z)
 return tuple(map(s.simplify,(m,a,b)))
def independent(e):
 m,a,b=e; A=s.simplify(a/m);B=s.simplify(b/m)
 def power(v):
  n=s.simplify(y*s.diff(v,y)/v);return n if not n.has(y) else None
 pa,pb=power(A),power(B)
 good=pa is not None and pb is not None and pa!=pb and (pa==1 or pb==1)
 return bool(good),A,B,pa,pb

def fieldvalue(f):
 ref=f[':answer-field/correct']; aid=ref[1] if isinstance(ref,list) else ref[':answer/id']
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)
def flags_record(r):
 fs=r['question'][':question/answer-fields']
 if fs[0][':answer-field/type']==':answer-field.type/checkbox':return tuple(fieldvalue(f)=='true' for f in fs[:3])
 v=fieldvalue(fs[0]);return tuple(bool(re.search(r'\b'+label+r'\b',v)) for label in ['I','II','III'])
def prompted_eqs(r):return [eq(t) for t in re.findall(r'- \*\*[IV]+\.\*\* \$(.*?)\$',r['question'][':question/problem'])]

# Source-guided decision coverage, both scalar boundaries, fresh normal seeds.
records=[];index=[]
for ti,(t,(level,_)) in enumerate(g.CASES.items()):
 for flags in g.decision_cases(t):
  for boundary in [1,5]:
   p={'decisions':list(flags),'left_scales':[boundary]*3,'right_scales':[6-boundary]*3}
   records.append(g.generate(level,seed=92000+ti,template=t,parameters=p));index.append({'template':t,'decisions':flags,'boundary':boundary})
normal=[g.generate(level,seed=730901+i) for level in ['easy','moderate'] for i in range(20)]
batch=load(J/'samples.json');save('samples.json',records);save('sample-index.json',index);save('normal-samples.json',normal);save('batch.json',batch)
# Controlled one-row exponent and irrelevant scalar changes.
pairs=[];pairrecords=[]
for t,(level,_) in g.CASES.items():
 cs=g.decision_cases(t);a,b=next((a,b) for a,b in itertools.combinations(cs,2) if sum(u!=v for u,v in zip(a,b))==1)
 base={'decisions':list(a),'left_scales':[2,3,4],'right_scales':[4,3,2]}
 modified={**base,'decisions':list(b)}; irrelevant={**base,'right_scales':[5,3,2]}
 rr=[g.generate(level,seed=80419,template=t,parameters=p) for p in [base,modified,irrelevant]]
 pairrecords+=rr;pairs.append({'template':t,'indices':list(range(len(pairrecords)-3,len(pairrecords))),'before_flags':a,'after_flags':b,'expected_irrelevant_flags':a,'parameters':[base,modified,irrelevant]})
save('counterfactual-records.json',pairrecords);save('counterfactuals.json',pairs)
mathresults=[];failures=[]
for label,rs in [('boundary',records),('normal',normal),('batch',batch),('counterfactual',pairrecords)]:
 for i,r in enumerate(rs):
  es=prompted_eqs(r);assert len(es)==3
  infos=[independent(e) for e in es]; expected=tuple(info[0] for info in infos);actual=flags_record(r)
  errors=[]
  if expected!=actual:errors.append('prompt classification disagrees with key')
  fs=r['question'][':question/answer-fields']
  if fs[0][':answer-field/type']==':answer-field.type/checkbox' and len(fs)==4:
   if (fieldvalue(fs[3])=='true')!= (not any(expected)):errors.append('None key')
  sol=r['question'][':question/worked-solution'];sections=re.split(r'- Equation [IV]+ is ',sol)[1:]
  for j,(e,info,sect) in enumerate(zip(es,infos,sections)):
   if info[0]:
    mm=re.search(r'p\(x\)=(.*?),\\quad q\(x\)=(.*?),\\quad n=(.*?)\.\n',sect)
    if not mm: errors.append('missing p q n')
    else:
     p,q,n=map(parse,mm.groups());m,a,b=e
     if s.simplify((b-a)/m-(-p*y+q*y**n))!=0:errors.append('p q n identity')
   elif '*not*' not in sect:errors.append('wrong classification in solution')
  item={'set':label,'index':i,'question_id':r['question'][':question/id'],'expected_flags':expected,'actual_flags':actual,'errors':errors}
  mathresults.append(item)
  if errors:failures.append(item)
save('math-results.json',{'method':'Parse rendered TeX with ANTLR; normalize derivative coefficient; logarithmic y derivative tests power dependence; check p,q,n identity independently. No generator analyze or metadata used.','checked':len(mathresults),'failures':failures,'results':mathresults})
# Full graded controls for every source decision case, pair and exact batch.
cases=[]
for label,rs in [('boundary',records),('counterfactual',pairrecords),('batch',batch)]:
 for i,r in enumerate(rs):
  checks=[]
  for fi,f in enumerate(r['question'][':question/answer-fields']):
   for a in f[':answer-field/choices']:
    checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==fieldvalue(f) else 'rejected','purpose':'Choose each available bank value, including wrong subsets/boolean states'})
  cases.append({'label':label+':'+str(i),'record':r,'checks':checks})
save('native-input.json',cases)
# Replay every rated source profile, compare all equations as symbolic triples and complete banks.
source=load(J/'source/source.json')['material']; sqs=source['kp'][':knowledge-point/questions'];replays=[];replayresults=[]
for t,(level,_) in g.CASES.items():
 q=next(q for q in sqs if q[':question/math-academy-id']==t)
 rr=g.generate(level,template=t,parameters={'left_scales':[1]*3,'right_scales':[1]*3},replay=True);replays.append(rr)
 if q[':question/answer-fields'][0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
  src_eqs=[eq(f[':answer-field/key']) for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above'];
  flags={s.srepr(e):f[':answer-field/correct'][':answer/value'] for f,e in zip([f for f in q[':question/answer-fields'] if f[':answer-field/key']!='None of the above'],src_eqs)}
  generated=prompted_eqs(rr); matches=all(any(all(s.simplify(u-v)==0 for u,v in zip(a,b)) for b in generated) for a in src_eqs)
  bank_ok=len(rr['question'][':question/answer-fields'])==len(q[':question/answer-fields'])
 else:
  src_eqs=[eq(t) for t in re.findall(r'\$(.*?)\$',q[':question/problem'])];generated=prompted_eqs(rr)
  matches=all(all(s.simplify(u-v)==0 for u,v in zip(a,b)) for a,b in zip(src_eqs,generated))
  bank_ok=sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in rr['question'][':question/answer-fields'][0][':answer-field/choices'])
 replayresults.append({'source_id':q[':question/id'],'template':t,'all_equations_replayed':matches,'complete_bank':bank_ok,'key':flags_record(rr),'source_solution_available':True})
save('source-replay-records.json',replays)
missing=[]
for q in [source['kp'][':knowledge-point/canonical-example']]+sqs:
 if q[':question/math-academy-id'] not in g.CASES:
  try:g.generate('easy',template=q[':question/math-academy-id']);outcome='unexpectedly accepted'
  except Exception as e:outcome=type(e).__name__+': '+str(e)
  missing.append({'source_id':q[':question/id'],'source_template':q[':question/math-academy-id'],'solution_available':':question/worked-solution' in q,'answer_fields_available':':question/answer-fields' in q,'outcome':outcome})
save('source-replay.json',{'rated_results':replayresults,'unrepresented_source':missing,'source_corrections':['q-108916 duplicated equation name corrected','q-108911 malformed final quote corrected'],'limits':'Two unrated drafts lack authoritative key/solution, canonical lacks answer fields. Inferred draft keys are I and III; II only.'})
# Reject malformed/out-of-domain inputs without silently changing them.
reject=[]
for name,args in [('hard',{'level':'hard'}),('wrong rating',{'level':'easy','template':'q-108920'}),('zero scalar',{'level':'easy','template':'q-108911','parameters':{'left_scales':[0,1,1],'right_scales':[1,1,1]}}),('six scalar',{'level':'easy','template':'q-108911','parameters':{'left_scales':[6,1,1],'right_scales':[1,1,1]}}),('bool scalar',{'level':'easy','template':'q-108911','parameters':{'left_scales':[True,1,1],'right_scales':[1,1,1]}}),('unrepresentable radio subset',{'level':'easy','template':'q-108915','parameters':{'decisions':[False,False,False],'left_scales':[1]*3,'right_scales':[1]*3}})]:
 try:g.generate(**args);result='accepted'
 except Exception as e:result=type(e).__name__
 reject.append({'case':name,'arguments':args,'result':result})
save('rejections.json',reject)
print(json.dumps({'boundary_records':len(records),'normal':len(normal),'pairs':len(pairs),'math_checked':len(mathresults),'math_failures':len(failures),'source_replays':replayresults,'unrepresented':missing}))
(E/'session-state.md').write_text('Source analysis saved before package reads. Independently sampled all supported decision cases at coefficient boundaries; parsed prompts/solutions and saved native grader inputs, source replays, and controlled counterfactuals. Next: delivery, native grading, renderer, packaging and variation report.\n')
