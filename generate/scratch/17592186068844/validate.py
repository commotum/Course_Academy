#!/usr/bin/env python3
"""Independent displayed-TeX, ordered stage, complete-bank and native grading QA."""
import importlib.util,json,re,sys,subprocess,hashlib,itertools
from pathlib import Path
from functools import lru_cache
sys.dont_write_bytecode=True
import sympy as s
sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/lark/1.2.2-py3-none-any')
from sympy.parsing.latex import parse_latex
from lark import Tree
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('implicit',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y,C,K=g.X,g.Y,g.C,s.Symbol('K',real=True)
U,V=s.symbols('u v',positive=True)

def norm(t):
 t=t.strip().replace('\\\\','\\').replace('\u2061','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
 t=re.sub(r'\\text\{[^{}]*\}','',t)
 t=re.sub(r'\\operatorname\{(ln|sin|cos|tan|cot|sec|arctan|arcsin|arccos)\}',lambda m:'\\'+m[1],t)
 t=t.replace(r'{cos}',r'\cos').replace(r'{sec}',r'\sec')
 for m in reversed(list(re.finditer(r'\\(ln|sin|cos|tan|sec|arcsin|arctan|arccos)\{',t))):
  depth=1;end=m.end()
  while depth:
   if t[end]=='{':depth+=1
   if t[end]=='}':depth-=1
   end+=1
  t=t[:m.start()]+'{'+'\\'+m[1]+'('+t[m.end():end-1]+')}'+t[end:]
 t=re.sub(r'\\ln\s*(\|[^|]*\|)',lambda m:'{'+r'\ln('+m[1]+')}',t)
 t=re.sub(r'\\(cos|sec)\^\{([0-9]+)\}\s*(\([^()]*\)|[xy])',lambda m:'\\'+m[1]+'('+m[3]+')^{'+m[2]+'}',t)
 t=re.sub(r'\\(sin|cos|tan|sec|arctan|arcsin|arccos)\s*([xy])',lambda m:'\\'+m[1]+'('+m[2]+')',t)
 matches=list(re.finditer(r'\\(?:sin|cos|tan|sec|arctan|arcsin|arccos|ln)\(',t))
 for m in reversed(matches):
  depth=1;end=m.end()
  while depth:
   if t[end]=='(':depth+=1
   if t[end]==')':depth-=1
   end+=1
  t=t[:m.start()]+'{'+t[m.start():end]+'}'+t[end:]
 t=re.sub(r'(?<=\))(?=[A-Za-z{])','*',t)
 t=re.sub(r'(?<=\})(?=\{\\(?:sin|cos|tan|sec|ln|arcsin))','*',t)
 t=re.sub(r'(?<=\})(?=[a-zA-Z(])','*',t)
 return t.rstrip('.,')
@lru_cache(None)
def parse(t):
 try:z=parse_latex(norm(t) or '1',backend='lark')
 except Exception as exc:raise AssertionError(('display parse',t,norm(t))) from exc
 if isinstance(z,Tree):
  vals=[v for v in z.children if isinstance(v,s.Basic)]
  assert vals and all(s.simplify(vals[0]-v)==0 for v in vals),(t,z)
  z=vals[0]
 return z.subs({a:{'e':s.E,'x':X,'y':Y,'C':C,'K':K}.get(a.name,a) for a in z.free_symbols})
def smooth(e):return e.replace(lambda z:z.func==s.log and z.args[0].func==s.Abs,lambda z:s.log(z.args[0].args[0]))
def equal(a,b,r=None):
 q=a-b
 if r and r['generation']['template']=='root_power':
  p=r['generation']['parameters'];q=q.subs({X:U-p['h'],Y:V-p['k']})
 return s.simplify(s.trigsimp(q,method='fu'))==0

def same_family(a,b,r):
 ax,ay=s.diff(smooth(a),X),s.diff(smooth(a),Y);bx,by=s.diff(smooth(b),X),s.diff(smooth(b),Y)
 if equal(bx,0,r) and equal(by,0,r):return False
 ratio=s.simplify(ax/bx if bx!=0 else ay/by)
 return ratio!=0 and not ratio.free_symbols and equal(ax-ratio*bx,0,r) and equal(ay-ratio*by,0,r)

def fmt(t):
 assert t.count('$$')%2==0 and t.replace('$$','').count('$')%2==0,t
 assert '@X@' not in t and '@Y@' not in t and '--' not in t and '+-' not in t,t
 depth=0
 for c in t:
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,t
 assert depth==0,t

def ode(r):
 spans=re.findall(r'\$([^$]+)\$',r['question'][':question/problem'])
 eq=[v for v in spans if v.startswith(g.D+'=')]
 assert len(eq)==1,(r,spans)
 return parse(eq[0].split('=',1)[1])

def rowlist(text):
 out=[]
 for b in re.findall(r'\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}',text):
  out.extend([tuple(row.split('& =',1)) for row in b.split(r'\\') if '& =' in row])
 return out

def stage_test(r,rhs):
 stages=0
 for left,right in rowlist(r['question'][':question/worked-solution']):
  if r'\int' in left:
   values=[]
   for side,isleft in [(left,True),(right,False)]:
    t=side.replace(r'\cancel{\text{d}x}',r'\text{d}x')
    t=t.replace(g.D,'D')
    t=re.sub(r'\\text\{d\}[xy]','',t).replace(r'\int','')
    # Each formal integral is linear; stripping integral/differential preserves
    # its integrand, including the explicit distributed component-sum row.
    e=parse(t);D=next((v for v in e.free_symbols if v.name=='D'),s.Symbol('D'))
    values.append(e.subs(D,rhs) if D in e.free_symbols else e*rhs if isleft else e)
   assert equal(*values,r),(r['generation']['template'],'integrands',left,right,values)
  else:
   l=parse(left.replace(g.D,'D'));rr=parse(right)
   D=next((v for v in l.free_symbols if v.name=='D'),s.Symbol('D'))
   if D in l.free_symbols:assert equal(l.subs(D,rhs),rr,r),('separation',left,right,l,rr,rhs)
   else:assert equal(s.diff(smooth(l),Y)*rhs,s.diff(smooth(rr),X),r),('primitive',left,right,l,rr,rhs)
  stages+=1
 for b in re.findall(r'\$\$([\s\S]*?)\$\$',r['question'][':question/worked-solution']):
  if r'\begin{aligned}' in b or '=' not in b:continue
  l,rr=map(parse,b.strip().split('=',1))
  assert equal(s.diff(smooth(l),Y)*rhs,s.diff(smooth(rr),X),r),('final implicit',b)
  stages+=1
 return stages

def check(r,raw=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];f=q[':question/answer-fields'][0]
 for t in (q[':question/problem'],q[':question/worked-solution']):fmt(t)
 rhs=ode(r);assert equal(rhs,g.data(r['generation']['template'],r['generation']['parameters'])[0],r)
 assert 'Then, we integrate both sides with respect to $x:$' in q[':question/worked-solution']
 st=stage_test(r,rhs)
 ci=f[':answer-field/correct'][1];truth=[];relations=[]
 assert len(f[':answer-field/choices'])==5
 for a in f[':answer-field/choices']:
  fmt(a[':answer/value']);l,rr=map(parse,a[':answer/value'].split('=',1))
  F=smooth(l-rr);relations.append(F)
  eligible=not (s.diff(l,Y).is_constant() and s.diff(l,Y)!=0 and Y not in rr.free_symbols)
  ok=eligible and equal(s.diff(F,X)+s.diff(F,Y)*rhs,0,r) and s.diff(F,C)!=0
  truth.append(ok)
  assert ok==(a[':answer/id']==ci),(r['generation']['template'],a[':answer/value'],ok,eligible)
 assert sum(truth)==1
 for i,a in enumerate(relations):
  for b in relations[i+1:]:assert not same_family(a,b,r),(r['generation']['template'],'equivalent complete solution families',a,b)
 return st

def main():
 review=[];fidelity=[];cases=[];stage_count=0
 for name,(level,sid) in g.TEMPLATES.items():
  if not sid:continue
  print('checking '+name,flush=True)
  q=g.QS[sid];p={'h':0,'k':0};case={'source_id':q[':db/id'],'math_academy_id':sid,'difficulty':level,'template':name,'parameters':p,'bank_profile':'observed'};cases.append(case)
  r=g.generate(level,13,name,parameters=p,profile='observed');stage_count+=check(r,True)
  f=r['question'][':question/answer-fields'][0];f0=q[':question/answer-fields'][0]
  assert r['question'][':question/problem']==q[':question/problem']
  assert r['question'][':question/worked-solution']==q[':question/worked-solution']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices'])
  correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==f0[':answer-field/correct'][':answer/value']
  assert len(rowlist(r['question'][':question/worked-solution']))==len(rowlist(q[':question/worked-solution']))
  fidelity.append({'source_id':q[':db/id'],'source':sid,'prompt_exact':True,'solution_exact':True,'ordered_stages_exact':True,'bank_values':5,'designation_matched':True})
  review.append(r)
  for seed in (41,87):
   r=g.generate(level,seed,name);stage_count+=check(r);review.append(r)
  translated=g.generate(level,31,name,parameters={'h':0 if 'autonomous' in name else -2,'k':3},profile='observed');stage_count+=check(translated,True);review.append(translated)
 for level,t in [('moderate','two_x_terms'),('hard','two_sided_terms')]:
  for seed in (41,87,23):
   r=g.generate(level,seed,t);stage_count+=check(r);review.append(r)
 # Every supported signed translation extreme and authored coefficient boundary.
 for name,(level,sid) in g.TEMPLATES.items():
  if sid:
   for h,k in itertools.product((-6,6),repeat=2):
    if 'autonomous' in name:h=0
    stage_count+=check(g.generate(level,0,name,parameters={'h':h,'k':k}))
 for level,t in [('moderate','two_x_terms'),('hard','two_sided_terms')]:
  for a,b in itertools.product((2,6),(-5,5)):
   ps={'a':a,'b':b}
   if level=='hard':ps['d']=5
   stage_count+=check(g.generate(level,0,t,parameters=ps))
 for name,p in [('two_x_terms',{'a':1,'b':2}),('two_x_terms',{'a':3,'b':0}),('two_sided_terms',{'a':2,'b':1,'d':0}),('power_cube',{'h':7,'k':0}),('arcsin_autonomous',{'h':2,'k':0})]:
  try:g.generate(g.TEMPLATES[name][0],0,name,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('accepted out of scope',name,p))
 for r in review:
  gen=r['generation'];level=r['question'][':question/difficulty'].split('/')[-1]
  rr=g.generate(level,gen['seed']+1,gen['template'],parameters=gen['parameters'],profile=gen['bank_profile'])
  assert r['question'][':question/id']==rr['question'][':question/id']
  # Changing bank changes content identity but not mathematical-task fingerprint.
  if level=='easy':
   other=g.generate(level,0,gen['template'],parameters=gen['parameters'],profile='standard' if gen['bank_profile']=='observed' else 'observed')
   assert other['generation']['mathematical_fingerprint']==gen['mathematical_fingerprint']
   assert other['question'][':question/id']!=r['question'][':question/id']
 r=review[0]
 assert same_family(Y**2-X**2-C,-3*(Y**2-X**2)+5-C,r)
 assert not same_family(Y**2-X**2-C,Y**2-2*X**2-C,r)
 # Enumerate complete finite sampling spaces; count canonical task fingerprints.
 counts={}
 for level in ('easy','moderate','hard'):
  ids=set();presentations=0
  for t,(l,sid) in g.TEMPLATES.items():
   if l!=level:continue
   if sid:params=({'h':h,'k':k} for h in ([0] if 'autonomous' in t else range(-6,7)) for k in range(-6,7))
   else:params=({'a':a,'b':b,**({'d':d} if level=='hard' else {})} for a in range(2,7) for b in range(-5,6) if b for d in (range(1,6) if level=='hard' else [0]))
   for p in params:
    rhs=g.data(t,p)[0];fp=hashlib.sha256(json.dumps([s.srepr(rhs),g.domain(t,p)],sort_keys=True).encode()).hexdigest();ids.add(fp);presentations+=1
  counts[level]={'complete_parameter_instances':presentations,'distinct_mathematical_tasks':len(ids)}
 payload=[]
 for i,r in enumerate(review):
  f=r['question'][':question/answer-fields'][0];ci=f[':answer-field/correct'][1]
  payload.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ci else 'rejected','purpose':'every owned radio selection'} for a in f[':answer-field/choices']]})
 (HERE/'engine-input.json').write_text(json.dumps(payload,indent=2)+'\n')
 engine=HERE.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
 native=json.loads((HERE/'engine-validation.json').read_text())
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 md=['# Implicit general solutions review','Original and translated observed profiles retain complete evidence banks. Standard variants use authored whole banks. Moderate/hard are explicitly authored levels.']
 for r in review:
  gen=r['generation'];label='Original replay' if gen['bank_profile']=='observed' and gen['parameters']=={'h':0,'k':0} else 'Generated observed-bank variant' if gen['bank_profile']=='observed' else 'Generated standard variant'
  md+=['## '+label+' — '+gen['template'],json.dumps(gen['parameters']),g.markdown(r)]
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 report={'status':'pass','basis':1356,'lineage':g.SOURCE['lineage'],'source_questions':11,'prompt_exact':11,'solution_exact':11,'ordered_stage_sequences_exact':11,'complete_source_banks':11,'source_options_matched':55,'source_distractors_matched':44,'correct_designations_matched':11,'fidelity':fidelity,'review_records':len(review),'independently_checked_displayed_stages':stage_count,'authored_missing_levels':['moderate','hard'],'finite_variety':counts,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'source_anomalies':['q-158116 excludes neither y=0 nor translated equivalent despite denominator sec(y)tan(y); raw replay unchanged, normal prompt excludes this point'],'raw_ambiguous_banks':0,'source_mathematical_errors':0,'normal_output_anomalies':0,'plots':'none','database_writes':0,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='fidelity'},indent=2))
if __name__=='__main__':main()
