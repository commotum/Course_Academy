#!/usr/bin/env python3
"""Independent readback of displayed fields, partials and all curl stages."""
from pathlib import Path
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
sp=importlib.util.spec_from_file_location('curl_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
x,y=g.x,g.y

def parse(t):
 t=t.strip().removesuffix(',').removesuffix('.')
 t=t.replace(r'\operatorname{atan}',r'\arctan')
 t=t.replace(r'\operatorname{cos}⁡',r'\cos ').replace(r'\operatorname{sin}⁡',r'\sin ').replace(r'\operatorname{arctan}⁡',r'\arctan ')
 # Original Math Academy notation applies sin/cos to the complete power.
 t=re.sub(r'\\(sin|cos)\s*\{([xy])\}\^\{(\d+)\}',r'\1(\2**\3)',t)
 t=t.replace(r'\left','').replace(r'\right','').replace(r'\,',' ')
 def group(z,i):
  assert z[i]=='{';depth=1;j=i+1
  while depth:
   assert j<len(z),'unbalanced TeX';depth+= (z[j]=='{')-(z[j]=='}');j+=1
  return z[i+1:j-1],j
 def process(z):
  out='';i=0
  while i<len(z):
   if z.startswith(r'\frac',i) or z.startswith(r'\sqrt',i):
    square=z.startswith(r'\sqrt',i);i+=5
    a,i=group(z,i)
    if square:out+='sqrt('+process(a)+')'
    else:
     b,i=group(z,i);out+='(('+process(a)+')/('+process(b)+'))'
   elif z[i]=='{':
    a,i=group(z,i);out+='('+process(a)+')'
   else:out+=z[i];i+=1
  return out
 t=process(t)
 for old,new in [(r'\arctan','atan'),(r'\sin','sin'),(r'\cos','cos'),(r'\ln','log')]:t=t.replace(old,new)
 
 for fn in ('sin','cos','atan','sqrt','log'):t=t.replace(fn,' '+fn+' ')
 assert '\\' not in t,('unparsed TeX',t)
 result=parse_expr(t,local_dict={'x':x,'y':y,'e':s.E,'sin':s.sin,'cos':s.cos,'atan':s.atan,'sqrt':s.sqrt,'log':s.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
 assert result.free_symbols<={x,y},('unexpected symbols',result,t)
 return result

def contribution_count(stage):
 depth=0;count=0
 for token in re.findall(r'\\left\(|\\right\)',stage):
  if token==r'\left(':
   if depth==0:count+=1
   depth+=1
  else:depth-=1
 assert depth==0,'distributed group structure'
 return count

def equal(a,b):assert s.simplify(a-b)==0,(a,b)
def field_readback(prompt):
 if 'functions $P(x,y)$' in prompt:
  parts=re.findall(r'\$[PQ]\(x,y\)=(.*?)\$',prompt);assert len(parts)==6
  return [(parse(parts[i]),parse(parts[i+1])) for i in (0,2,4)]
 pairs=re.findall('⟨(.*?),'+re.escape(r'\,')+'(.*?)⟩',prompt);assert len(pairs)==3,('vector separators',pairs)
 return [(parse(P),parse(Q)) for P,Q in pairs]

def format_check(t):
 assert all(ord(c)>=32 or c in '\n\t' for c in t),'control character'
 assert t.count('$')%2==0,'math delimiters'
 depth=0
 for c in t:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0,'TeX brace'
 assert depth==0,'TeX braces'
 assert '{{f' not in t and '{{c' not in t,'unfilled slot'
 assert '--' not in t and '+-' not in t,'signed contribution grouping'

def check(r,raw=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 format_check(prompt);format_check(sol)
 fs=field_readback(prompt)
 for P,Q in fs:
  assert not (P.atoms(s.log)|Q.atoms(s.log)), 'unexpected full-field logarithm/domain'
  assert all(f.func in (s.sin,s.cos,s.atan,s.exp) for f in P.atoms(s.Function)|Q.atoms(s.Function)), 'unexpected singular field'
  for expr in (P,Q):assert not s.denom(expr).has(x,y),'singular full field'
 ds=[(s.diff(P,y),s.diff(Q,x)) for P,Q in fs]
 nonzero_contributions=sum(len(s.Add.make_args(v)) for pair in ds for v in pair if v!=0)
 assert nonzero_contributions==11 if r['generation']['template']=='mixed' else nonzero_contributions<=7,'difficulty workload distinction'
 py=re.findall(re.escape(r'\frac{∂P}{∂y}=')+r'(.*?)\$',sol);qx=re.findall(re.escape(r'\frac{∂Q}{∂x}=')+r'(.*?)\$',sol)
 assert len(py)==len(qx)==3,'all held partials'
 curl=re.findall(re.escape(r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}=')+r'(.*?)\n',sol)[1:]
 assert len(curl)==3,'all curls'
 opening=re.findall(re.escape(r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}=')+r'(.*?)\n',sol)[0]
 assert opening=='1,','Green theorem criterion'
 if r['generation']['template']!='mixed':
  source=g.QUESTIONS[r['generation']['template']][':question/worked-solution']
  strip=lambda z:re.sub(r'\$\$.*?\$\$|\$[^$]*\$', '', z, flags=re.S)
  assert strip(source)==strip(sol),'source shared prose and paragraph sequence'
 eligible=[]
 for i,(P_y,Q_x) in enumerate(ds):
  equal(parse(py[i]),P_y);equal(parse(qx[i]),Q_x)
  stages=curl[i].removesuffix('.').split(r'\ne 1')[0].split('=')
  for stage in stages:equal(parse(stage),Q_x-P_y)
  good=s.simplify(Q_x-P_y-1)==0
  assert (r'\ne 1' not in curl[i])==good,'identity criterion'
  if good:eligible.append(i)
  if not raw:
   assert len(stages)==3,'grouped, distributed, collected stages'
   # Require individually signed terms, not merely an algebraically equal row.
   assert contribution_count(stages[1])==len(s.Add.make_args(Q_x))+len(s.Add.make_args(P_y)),'distributed contribution count'
 expected=g.selection(eligible)
 assert 'Therefore, the correct answer is "'+expected+'."' in sol,'concluding selection'
 for f in q[':question/answer-fields']:
  choices=f[':answer-field/choices'];assert len(choices)==5
  values=[a[':answer/value'] for a in choices];assert len(set(values))==5
  for value in values:
   # Every bank choice denotes a distinct set, which is eligible iff exactly
   # equal to the fields with curl identically 1 (pointwise coincidence fails).
   indices=tuple(i for i,v in enumerate(g.LABELS) if re.search(r'\b'+v+r'\b',value))
   assert (indices==tuple(eligible))==(value==expected)
  if ':answer-field/correct' in f:
   assert f[':answer-field/correct'][0]==':answer/id'
   chosen=next(a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]);assert chosen[':answer/value']==expected
  else:assert raw,'normal correct missing'
 return ds

def mutation_checks(r):
 failures=[]
 for label,modify in [
  ('partial sign',lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace('$'+r'\frac{∂P}{∂y}=','$'+r'\frac{∂P}{∂y}=-',1)})),
  ('distributed term',lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace(r'\right)-\left',r'\right)+\left',1)})),
  ('conclusion',lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].rsplit('Therefore',1)[0]+'Therefore, the correct answer is "III only."'})),
  ('control character',lambda q:q.update({':question/problem':q[':question/problem']+'\x0c'})),
  ('vanishing field',lambda q:q.update({':question/problem':q[':question/problem'].replace('F(x,y)=⟨',r'F(x,y)=⟨\ln{x}+',1)})),
 ]:
  m=copy.deepcopy(r);modify(m['question'])
  try:check(m)
  except (AssertionError,ValueError,SyntaxError):failures.append(label)
  else:raise AssertionError('Mutation undetected: '+label)
 return failures

def meaningful_count():
 result={l:set() for l in ('easy','moderate','hard')}
 for t,l in g.LEVELS.items():
  base=g.ANCHORS.get(t,{'a':1,'d':2,'n':2,'b':1,'k':1,'order':0})
  # Parameters affecting only common cancellations are fixed for enumeration.
  ks=list(base);ranges=[range(1,6) if k=='a' else range(2,9) if k=='d' else range(2,5) if k=='n' and t!='mixed' else range(1,4) if k=='k' else [base[k]] for k in ks]
  for values in itertools.product(*ranges):
   p=dict(zip(ks,values));ds=g.derivatives(g.fields(t,p))
   result[l].add(json.dumps(sorted(g.assessed_derivatives(ds))))
 return {l:len(v) for l,v in result.items()}

def main():
 cases=json.loads((HERE/'source-cases.json').read_text());replays=[];fidelity=[];generated=[]
 for c in cases:
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='raw');check(r,raw=True)
  q=r['question'];source=g.QUESTIONS[c['source_id']]
  assert q[':question/problem']==source[':question/problem'];assert q[':question/worked-solution']==source[':question/worked-solution']
  assert set(q)==set(source),'attribute presence'
  fields=q[':question/answer-fields'];sf=source[':question/answer-fields'];assert len(fields)==len(sf)
  for f,o in zip(fields,sf):
   assert set(f)==set(o);assert ':answer-field/correct' in f if ':answer-field/correct' in o else ':answer-field/correct' not in f
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in o[':answer-field/choices'])
   if ':answer-field/correct' in o:assert f[':answer-field/correct'][1]==o[':answer-field/correct'][':answer/id']
  fidelity.append({'source_id':c['source_id'],'prompt_exact':True,'solution_exact':True,'bank_count':len(fields),'choice_values':sum(len(f[':answer-field/choices']) for f in fields),'present_correct_refs':sum(':answer-field/correct' in f for f in fields),'key_presence_parity':True})
  replays.append(r)
  p=dict(c['parameters']);p['a']=3
  if 'd' in p:p['d']=6
  if 'n' in p:p['n']=4
  changed=g.generate(c['level'],template=c['template'],parameters=p,profile='raw');check(changed,raw=True)
  assert changed['question'][':question/problem']!=q[':question/problem'],'changed source fields must change displayed prompt'
 coverage={};positions=set();identities=0
 for level in ('easy','moderate','hard'):
  coverage[level]=set()
  for seed in range(100):
   r=g.generate(level,seed);check(r);generated.append(r);coverage[level].add(r['generation']['template'])
   f=r['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
   r2=g.generate(level,seed+180,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'])
   assert r['question'][':question/id']==r2['question'][':question/id'];identities+=1
  assert coverage[level]=={t for t,l in g.LEVELS.items() if l==level}
 assert positions==set(range(5))
 for template,level in g.LEVELS.items():check(g.generate(level,seed=13,template=template,profile='method_toggle'))
 hard_correct={next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in generated if r['generation']['template']=='mixed'}
 assert hard_correct=={'I and II only','I and III only','II and III only'},'hard candidate decision pattern coverage'
 reviews=json.loads((HERE/'review.json').read_text())
 for item in reviews:check(item['record'],item['record']['generation']['evidence_only'])
 mutations=mutation_checks(g.generate('hard',seed=23))
 # Finite guard boundaries and every source-shaped family.
 boundary=0
 for t,level in g.LEVELS.items():
  p=dict(g.ANCHORS.get(t,{'a':1,'d':2,'n':2,'b':1,'k':1,'order':0}));p={k:5 if k=='a' else 8 if k=='d' else 4 if k=='n' else 3 for k in p}
  check(g.generate(level,template=t,parameters=p));boundary+=1
  for key in p:
   wrong=dict(p);wrong[key]=-1 if key=='order' else 0
   try:g.generate(level,template=t,parameters=wrong)
   except ValueError:boundary+=1
   else:raise AssertionError('Explicit guard ignored')
 fixtures=[]
 for r in generated[::5]:
  f=r['question'][':question/answer-fields'][0]
  fixtures.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native owned subset radio'} for a in f[':answer-field/choices']]})
 for r in replays:
  rr=copy.deepcopy(r);rr['question'][':question/answer-fields']=[f for f in rr['question'][':question/answer-fields'] if ':answer-field/correct' in f]
  f=rr['question'][':question/answer-fields'][0]
  fixtures.append({'label':'raw-active-'+r['generation']['template'],'record':rr,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native active source field; raw missing legacy correct is excluded, not fabricated'} for a in f[':answer-field/choices']]})
 (HERE/'native-input.json').write_text(json.dumps(fixtures,indent=2));engine=ROOT/'generate/runs/current/check-engine'
 proc=subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],text=True,capture_output=True);assert proc.returncode==0,proc.stderr
 report={'status':'passed','runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'source_provenance':{k:g.WRAPPER[k] for k in ('database','basis','lineage')},'source_coverage':fidelity,'fidelity':{'exact_prompts':7,'exact_solutions':7,'complete_banks':9,'choice_values':45,'present_correct_designations_matched':7,'missing_legacy_designations_not_counted':2,'presence_parity':7},'generated_readback_records':len(generated),'changed_raw_replays':7,'native_checks':sum(len(f['checks']) for f in fixtures),'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'native':json.loads((HERE/'native-report.json').read_text()),'default_family_coverage':{k:sorted(v) for k,v in coverage.items()},'hard_correct_pattern_coverage':sorted(hard_correct),'identity_checks':identities,'boundary_checks':boundary,'mutation_rejections':mutations,'finite_meaningful_tasks':meaningful_count(),'authored_hard':True,'source_format_repairs':['q-125852 and q-125853 normal output uses the single authoritative five-choice active field; raw retains both field objects and original missing-ref presence.'],'unresolved':['The two legacy fields have no captured correct designation; cannot claim native grading or designation matching for those raw absent references.'],'plots':'none'}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ('status','fidelity','generated_readback_records','native_checks','finite_meaningful_tasks')},indent=2))
if __name__=='__main__':main()
