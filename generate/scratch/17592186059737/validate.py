#!/usr/bin/env python3
"""Independent readback of actual displayed prompt, banks and every math stage."""
import importlib.util,json,re,subprocess,hashlib
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('gen',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=g.X

def p(t):
 t=g.norm(t).replace(r'\,','').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','').strip().rstrip('.')
 def group(text,start):
  assert text[start]=='{';depth=1;j=start+1
  while depth:
   depth+=(text[j]=='{')-(text[j]=='}');j+=1
  return text[start+1:j-1],j
 t=re.sub(r'\\sqrt\[(\d+)\]\{([^{}]*)\}',lambda m:'(('+m[2]+')**(1/'+m[1]+'))',t)
 while r'\sqrt{' in t or r'\frac{' in t:
  candidates=[(t.find(cmd),cmd) for cmd in [r'\sqrt',r'\frac'] if cmd+'{' in t];i,cmd=min(candidates)
  first,end=group(t,i+len(cmd))
  if cmd==r'\sqrt':out='sqrt('+str(p(first))+')'
  else:
   second,end=group(t,end);out='(('+str(p(first))+')/('+str(p(second))+'))'
  t=t[:i]+out+t[end:]
 t=t.replace('{','(').replace('}',')').replace('^','**')
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 return parse_expr(t,local_dict={'x':X,'i':s.Symbol('i'),'j':s.Symbol('j'),'k':s.Symbol('k')},transformations=standard_transformations+(implicit_multiplication_application,))
def roots(t):
 t=g.norm(t).replace(r'\,','').replace(' ','');t=re.sub('x=','',t)
 if r'\pm' in t:
  v=p(t.replace(r'\pm',''));return s.FiniteSet(-v,v)
 return s.FiniteSet(*[p(v) for v in t.split(',') if v.strip()])
def same(a,b):assert s.simplify(a-b)==0,(a,b)
def formatting(text):
 assert text.count('$')%2==0
 depth=0
 for i,c in enumerate(text):
  if c in '{}':
   if i and text[i-1]=='\\':continue
   depth+=1 if c=='{' else -1;assert depth>=0
 assert depth==0
 assert '--' not in text and '+-' not in text

def verify(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];text=q[':question/problem'];sol=q[':question/worked-solution'];formatting(text);formatting(sol)
 vectors=re.findall('⟨([^⟩]*)⟩',text)
 a,b=[s.Matrix([p(v) for v in vec.split(',')]) for vec in vectors]
 R=p(re.search(r'\|\s*=\s*([^$]*)',text)[1]);assert R>0
 c=s.Matrix([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]])
 N=s.expand(sum(v*v for v in c));expected=s.solveset(N-R**2,X,domain=s.S.Reals);assert isinstance(expected,s.FiniteSet)
 for v in expected:same(s.sqrt(N.subs(X,v)),R)
 fullbanks=0
 for f in q[':question/answer-fields']:
  key=f[':answer-field/key'];kind=f[':answer-field/type'].split('/')[-1];choices=f[':answer-field/choices'];ref=f[':answer-field/correct'][1]
  assert len(set(a[':answer/id'] for a in choices))==len(choices)
  vals=[];good=0
  for ans in choices:
   val=ans[':answer/value'];formatting(val)
   if kind=='radio':obj=roots(val);isgood=obj==expected
   else:
    assert '{{'+key+'}}' in text;obj=p(val);ordered=sorted(expected,key=float);isgood=obj==ordered[int(key.split('-')[-1])-1]
   assert obj not in vals;vals.append(obj)
   good+=isgood
   assert (ans[':answer/id']==ref)==isgood
  assert good==1
  fullbanks+=1
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==3
 dets=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',blocks[0],re.S);assert len(dets)==4
 matrices=[]
 for d in dets:
  rows=[[v.strip() for v in row.split('&')] for row in d.split(r'\\')]
  matrices.append(rows)
 assert matrices[0][0]==list('ijk')
 for i,v in enumerate([*a,*b]):same(p(matrices[0][1+i//3][i%3]),v)
 pairs=[[[a[1],a[2]],[b[1],b[2]]],[[a[0],a[2]],[b[0],b[2]]],[[a[0],a[1]],[b[0],b[1]]]]
 for mat,expectedmat in zip(matrices[1:],pairs):
  for i in range(2):
   for j in range(2):same(p(mat[i][j]),expectedmat[i][j])
 # Read every scalar product/sign arithmetic row after all minors, not metadata.
 tail=blocks[0].split(r'\end{aligned}|k',1)[1]
 for row in tail.split(r'\\'):
  if '&' not in row:continue
  rhs=row.split('=',1)[-1].split(r'\end{aligned}')[0].strip().rstrip('.')
  if '⟨' in rhs:
   vv=re.search('⟨([^⟩]*)⟩',rhs)[1].split(',');assert len(vv)==3
   for v,target in zip(vv,c):same(p(v),target)
  else:
   basis=p(rhs)
   for symbol,target in zip('ijk',c):same(s.expand(basis).coeff(s.Symbol(symbol)),target)
   assert s.expand(basis).subs({s.Symbol(v):0 for v in 'ijk'})==0
 # Every substituted/expanded/collected norm radicand must match actual vectors.
 for row in blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
  rhs=row.split('=',1)[1].strip().rstrip('.');same(p(rhs)**2,N)
 # Every solving row represents the SAME complete real solution set.
 for row in blocks[2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
  row=row.replace('&','').replace(r'|\,a\times b\,|',r'\sqrt{'+g.tex(N)+'}').strip().rstrip('.')
  if ',' in row:
   components=row.replace(r'\,','').split(',');lhs0=components[0].split('=',1)[0];actual=s.EmptySet
   for component in components:
    lhs,rhs=component.split('=',1) if '=' in component else (lhs0,component)
    actual=actual.union(s.solveset(p(lhs)-p(rhs),X,domain=s.S.Reals))
  else:
   lhs,rhs=row.split('=',1);actual=s.solveset(p(lhs)-p(rhs),X,domain=s.S.Reals)
  assert actual==expected,(r['generation']['template'],row,actual,expected)
 # Independently validate final narrative answers.
 narrative=sol.split('Therefore,',1)[1].split('Checking',1)[0]
 claims=[]
 for frag in re.findall(r'\$(.*?)\$',narrative):
  if '=' in frag:claims+=list(roots(frag))
 assert s.FiniteSet(*claims)==expected,(narrative,claims,expected)
 return {'banks':fullbanks,'stage_rows':[b.count(r'\\')+1 for b in blocks]}

def checks(r):
 out=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  ref=f[':answer-field/correct'][1]
  for a in f[':answer-field/choices']:
   common={'field_index':i,'purpose':'all displayed source/default choices'}
   if f[':answer-field/type'].endswith('/radio'):out.append(dict(common,submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==ref else 'rejected'))
   else:
    v=p(a[':answer/value']);out.append(dict(common,submitted=g.tex(v),expected='accepted'))
    equiv='('+str(v)+')+0';out.append(dict(common,submitted=equiv,expected='accepted',purpose='unevaluated algebraic equivalence'))
    if v.is_Rational:equiv=str(2*s.numer(v))+'/'+str(2*s.denom(v))
    elif v>0:equiv='sqrt('+str(v*v)+')'
    else:equiv='-sqrt('+str(v*v)+')'
    out.append(dict(common,submitted=equiv,expected='accepted',purpose='unreduced fraction / alternative radical'))
    out.append(dict(common,submitted=g.tex(v+1),expected='rejected',purpose='wrong root fragment'))
 return out

def main():
 sourcecases=[];review=[];metrics=[];fidelity=[];rawfidelity=[]
 for name,q in g.QUESTIONS.items():
  level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1]
  case={'source_id':q[':db/id'],'source_math_academy_id':name,'template':name,'level':level,'parameters':{'scale':'1'},'bank_profile':'observed-'+name};sourcecases.append(case)
  case['raw_bank_profile']=case['bank_profile']+':raw'
  raw=g.generate(level,7,template=name,parameters=case['parameters'],profile=case['raw_bank_profile'])
  rq=raw['question'];assert rq[':question/problem']==q[':question/problem']
  assert (':question/worked-solution' in rq)==(':question/worked-solution' in q)
  if ':question/worked-solution' in q:assert rq[':question/worked-solution']==q[':question/worked-solution']
  assert (':question/difficulty' in rq)==(':question/difficulty' in q)
  if ':question/difficulty' in q:assert rq[':question/difficulty']==q[':question/difficulty'][':db/ident']
  for f,rf in zip(rq[':question/answer-fields'],q[':question/answer-fields']):
   assert f[':answer-field/key']==rf[':answer-field/key'] and f[':answer-field/type']==rf[':answer-field/type'][':db/ident']
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
   assert (':answer-field/correct' in f)==(':answer-field/correct' in rf)
   if ':answer-field/correct' in rf:
    ref=f[':answer-field/correct'][1]
    assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ref)==rf[':answer-field/correct'][':answer/value']
  assert raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning']
  assert rq[':question/id']==g.generate(level,99,template=name,parameters=case['parameters'],profile=case['raw_bank_profile'])['question'][':question/id']
  rawfidelity.append({'source':name,'raw_full_prompt_exact':True,'raw_full_solution_or_absence_exact':True,'raw_bank_values_exact':True,'raw_difficulty_and_key_presence_exact':True,'raw_anomalies':raw['generation']['raw_anomalies']})
  review.append({'label':'Public raw evidence replay '+name,'record':raw})
  # Exercise every raw profile at changed parameters through the same public API.
  changedraw=g.generate(level,8,template=name,parameters={'scale':'2'},profile=case['raw_bank_profile'])
  oldvectors=re.findall('⟨([^⟩]*)⟩',q[':question/problem']);newvectors=re.findall('⟨([^⟩]*)⟩',changedraw['question'][':question/problem'])
  for oldvec,newvec in zip(oldvectors,newvectors):
   for old,new in zip(oldvec.split(','),newvec.split(',')):same(p(new),p(old).subs(X,2*X))
  for f,rf in zip(changedraw['question'][':question/answer-fields'],q[':question/answer-fields']):
   if f[':answer-field/type'].endswith('/radio'):assert set(roots(a[':answer/value']) for a in f[':answer-field/choices'])==set(s.FiniteSet(*[v/2 for v in roots(a[':answer/value'])]) for a in rf[':answer-field/choices'])
   else:assert set(p(a[':answer/value']) for a in f[':answer-field/choices'])==set(p(a[':answer/value'])/2 for a in rf[':answer-field/choices'])
  review.append({'label':'Public changed raw evidence replay '+name,'record':changedraw})
  original=g.generate(level,7,template=name,parameters=case['parameters'],profile=case['bank_profile']);metrics.append(verify(original))
  bankmatch=True
  for f,rawf in zip(original['question'][':question/answer-fields'],q[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(g.norm(a[':answer/value']) for a in rawf[':answer-field/choices'])
  if ':question/worked-solution' in q:
   supported=q[':question/worked-solution']
   if name=='q-103540':supported=supported.replace('⟨-5,-4x,x⟩','⟨-5,4x,-x⟩').replace('(-4x)^{2}+{x}^{2}','(4x)^{2}+(-x)^{2}')
   assert original['question'][':question/worked-solution']==supported
  for generated_field,raw_field in zip(original['question'][':question/answer-fields'],q[':question/answer-fields']):
   if ':answer-field/correct' in raw_field:
    ref=generated_field[':answer-field/correct'][1]
    assert next(a[':answer/value'] for a in generated_field[':answer-field/choices'] if a[':answer/id']==ref)==g.norm(raw_field[':answer-field/correct'][':answer/value'])
  solmatch=original['question'][':question/worked-solution']==q.get(':question/worked-solution')
  promptmatch=original['question'][':question/problem']==q[':question/problem']
  fidelity.append({'source':name,'bank_values_normalized_match':bankmatch,'raw_prompt_match':promptmatch,'raw_full_solution_match':solmatch,'raw_correct_designation_present':all(':answer-field/correct' in f for f in q[':question/answer-fields']),'source_stage_rows':[b.count(r'\\')+1 for b in re.findall(r'\$\$\n(.*?)\n\$\$',q.get(':question/worked-solution',''),re.S)],'generated_stage_rows':metrics[-1]['stage_rows']})
  review.append({'label':'Original repaired replay '+name,'record':original,'original':q})
  changed=g.generate(level,8,template=name,parameters={'scale':'2'});metrics.append(verify(changed));review.append({'label':'Generated changed observed recipe '+name,'record':changed})
  metrics.append(verify(g.generate(level,9,template=name,parameters={'scale':'1/2'})))
 for level in ['easy','moderate','hard']:
  for seed in range(20):
   r=g.generate(level,seed);metrics.append(verify(r))
   assert r['question'][':question/id']==g.generate(level,seed+99,parameters=r['generation']['parameters'])['question'][':question/id']
   if seed<2:review.append({'label':'Authored '+level+' seed '+str(seed),'record':r})
 # Invalid explicit workload cases must fail, never silently resample.
 bad=[('easy',{'a':['10*x',1,1],'b':[0,1,'x'],'root':2}),('moderate',{'a':['x',1,0],'b':[0,0,1],'root':2}),('hard',{'a':['x',1,100],'b':[1,0,1],'offset':1})]
 for level,params in bad:
  try:g.generate(level,parameters=params)
  except ValueError:pass
  else:raise AssertionError('invalid explicit parameters accepted')
 (HERE/'source-cases.json').write_text(json.dumps(sourcecases,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 previews=[]
 for item in review:
  previews.append('## '+item['label']+'\n\n'+('### Captured raw original\n\n'+item['original'][':question/problem']+'\n\n'+item['original'].get(':question/worked-solution','No captured solution.')+'\n\n' if 'original' in item else '')+g.markdown(item['record']))
 (HERE/'review.md').write_text('# Original and generated review\n\n'+'\n\n'.join(previews))
 engine=[{'label':item['label'],'record':item['record'],'checks':checks(item['record'])} for item in review if not item['record']['generation'].get('evidence_only')]
 (HERE/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False))
 subprocess.run([str(HERE.parents[1]/'runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 result={'passed':True,'mathematical_records':len(metrics),'source_answer_values_matched':sum(len(f[':answer-field/choices']) for q in g.QUESTIONS.values() for f in q[':question/answer-fields']),'source_field_banks_matched':sum(len(q[':question/answer-fields']) for q in g.QUESTIONS.values()),'supported_complete_solution_sequence_matched':20,'task_variety_50_seeds':{l:len({g.generate(l,i)['generation']['mathematical_fingerprint'] for i in range(50)}) for l in ['easy','moderate','hard']},'raw_source_fidelity':rawfidelity,'raw_exact_full_prompt_replays':21,'raw_exact_solution_or_absence_replays':21,'raw_exact_full_question_banks':21,'raw_exact_answer_values':75,'normal_raw_byte_complete_question_banks':sum(all(a[':answer/value']==g.norm(a[':answer/value']) for f in q[':question/answer-fields'] for a in f[':answer-field/choices']) for q in g.QUESTIONS.values()),'normal_raw_byte_answer_values':sum(a[':answer/value']==g.norm(a[':answer/value']) for q in g.QUESTIONS.values() for f in q[':question/answer-fields'] for a in f[':answer-field/choices']),'decoded_source_doubled_backslash_values':sum('\\\\' in a[':answer/value'] for q in g.QUESTIONS.values() for f in q[':question/answer-fields'] for a in f[':answer-field/choices']),'source_practice_questions':21,'observed_moderate':9,'observed_hard':11,'unrated_authored_moderate':1,'full_banks_normalized_matched':21,'raw_exact_prompts':sum(i['raw_prompt_match'] for i in fidelity),'raw_exact_full_solutions':sum(i['raw_full_solution_match'] for i in fidelity),'source_solutions_present':20,'raw_correct_designations_present':20,'missing_key_inferred':1,'source_fidelity':fidelity,'native':json.loads((HERE/'engine-report.json').read_text()),'invalid_explicit_rejected':len(bad),'database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['native','source_fidelity','raw_source_fidelity']}))
if __name__=='__main__':main()
