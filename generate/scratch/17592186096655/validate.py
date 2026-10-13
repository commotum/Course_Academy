"""Parse printed integrands independently; check calculus, complete banks and grader."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE))
from scalar_parser import scalar,same
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
native=[]
def save(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def target(q):
 f,limits=g.printed(q)
 return g.sp.integrate(f,(g.x,*limits)) if limits else g.sp.integrate(f,g.x)
def value(s):
 try:return scalar(s.replace('z','x').replace(' + C','').replace('+C',''))
 except Exception:
  print('PARSER FAILED',repr(s),flush=True);raise
def row_value(rhs,p):
 from scalar_parser import group
 rhs=rhs.replace('z','x').replace('+C','')
 if r'\int' in rhs:
  prefix=rhs.split(r'\int',1)[0].strip();coef=value(prefix) if prefix else g.sp.Integer(1)
  transformed=r'\text{d}u' in rhs
  rhs=rhs.replace(r'\text{d}u',r'\text{d}x').replace('u','x') if transformed else rhs
  f,limits=g.printed({':question/problem':rhs})
  result=g.sp.integrate(f,(g.x,*limits)) if limits else g.sp.integrate(f,g.x)
  if transformed and not limits:result=result.subs(g.x,g.sp.Rational(p['k'])*g.x+g.sp.Rational(p['b']))
  return coef*result
 if r'\left[' in rhs:
  pre,rest=rhs.split(r'\left[',1);func,rest=rest.split(r'\right]_',1);lo,j=group(rest,0);assert rest[j]=='^';hi,j=group(rest,j+1)
  F=value(func.replace('u','x'));coef=value(pre) if pre.strip() else g.sp.Integer(1)
  return coef*(F.subs(g.x,value(hi))-F.subs(g.x,value(lo)))
 result=value(rhs.replace('u','x'))
 if 'u' in rhs:result=result.subs(g.x,g.sp.Rational(p['k'])*g.x+g.sp.Rational(p['b']))
 return result

def ordered(q):
 q=copy.deepcopy(q)
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
 return q

def validate(rec):
 q=rec['question'];m=rec['generation'];assert rec['knowledge_point']['db_id']==g.KP_ID and rec['knowledge_point']['id']==g.KP_UUID
 expected=g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],m['template'],parameters=m['parameters'],profile=m['profile'])
 assert ordered(q)==ordered(expected['question']) and m['math_fingerprint']==g.fingerprint(q)
 t=target(q);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];cid=f[':answer-field/correct'][1]
 vals=[value(a[':answer/value']) for a in choices];assert len(set(a[':answer/id'] for a in choices))==len(choices)
 assert sum(same(v,t) for v in vals)==1;assert same(next(v for a,v in zip(choices,vals) if a[':answer/id']==cid),t)
 assert not any(same(v,w) for i,v in enumerate(vals) for w in vals[:i])
 # Reparse every printed mathematical parameter in substitution and the final solution.
 solution=q[':question/worked-solution'];u=re.search(r'If we let \$u=(.*?)\$',solution)[1].rstrip(',');u=value(u)
 actual,_=g.printed(q);p=m['parameters'];assert same(g.sp.diff(u,g.x),g.sp.Rational(p['k']))
 assert same(g.sp.Rational(p['a'])*g.sp.exp(u),actual)
 final=solution.split('&=')[-1].split(r'\end{aligned}')[0];assert same(value(final),t)
 for rhs in solution.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\'):
  assert same(row_value(rhs.split('&=')[1],p),t),(m['template'],rhs)
 if 'bound' in p:
  table=solution.split('| $u$ | ')[1].split('\n')[0];lo,hi=re.findall(r'\$(.*?)\$',table)[:2]
  limits=g.printed(q)[1];assert same(value(lo.strip('$')),u.subs(g.x,limits[0]));assert same(value(hi.strip('$')),u.subs(g.x,limits[1]))
 else:assert same(g.sp.diff(value(final),g.x),actual)
 if f[':answer-field/type'].endswith('/radio'):
  assert len(choices)==5;checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==cid else 'rejected',purpose='Full owned bank designation') for a in choices]
 else:
  assert len(choices)==1 and q[':question/problem'].count('{{field-1}}')==1
  canonical=choices[0][':answer/value'];checks=[dict(submitted=canonical,expected='accepted',purpose='Exact canonical'),dict(submitted='('+canonical+')*2/2',expected='accepted',purpose='Equivalent independently scaled entry'),dict(submitted=g.tex(t+1),expected='rejected',purpose='Incorrect additive term'),dict(submitted=g.tex(-t),expected='rejected',purpose='Incorrect sign')]
 native.append(dict(label=q[':question/id'],record=rec,checks=checks))

def validate_existing(q):
 assert q.get(':question/math-academy-id') not in ('q-13775','q-30922','q-51160'),'Source solution contains wrong differential or unsubstituted exponent; preserved but excluded'
 assert q.get(':question/worked-solution') and len(q.get(':question/answer-fields',[]))==1
 f=q[':question/answer-fields'][0];assert ':answer-field/correct' in f
 t=target(q);assert same(value(f[':answer-field/correct'][':answer/value']),t)
 vals=[value(a[':answer/value']) for a in f[':answer-field/choices']]
 assert any(a[':answer/id']==f[':answer-field/correct'][':answer/id'] for a in f[':answer-field/choices'])
 assert sum(same(v,t) for v in vals)==1
 if f[':answer-field/type'][':db/ident'].endswith('/radio'):assert len(vals)==5 and not any(same(v,w) for i,v in enumerate(vals) for w in vals[:i])
 return True

def main():
 fidelity=[];review=[];records=[];components=[];coverage={};matched=0;distractors=0
 for c in g.CASES:
  s=g.QS[c['source_id']];r=g.generate(c['level'],0,c['template'],parameters=c['parameters']);validate(r);records.append(r)
  orig=s[':question/answer-fields'][0];out=r['question'][':question/answer-fields'][0];remaining=list(out[':answer-field/choices']);options=[]
  for a in orig[':answer-field/choices']:
   match=next((v for v in remaining if same(value(a[':answer/value']),value(v[':answer/value']))),None);assert match,(c['source_id'],a)
   remaining.remove(match);matched+=1
   correct=same(value(a[':answer/value']),target(s));distractors+=not correct
   options.append(dict(source_answer_id=a[':answer/id'],observed_value=a[':answer/value'],recipe_index=out[':answer-field/choices'].index(match),exact_replay=True,correct=correct))
  assert not remaining and g.fingerprint(s)==r['generation']['math_fingerprint']
  if ':answer-field/correct' in orig:assert same(value(orig[':answer-field/correct'][':answer/value']),target(s))
  fidelity.append(dict(source_id=c['source_id'],complete_bank=True,options=len(options),prompt_math=True,literal_prompt=s[':question/problem']==r['question'][':question/problem'],literal_solution=s.get(':question/worked-solution')==r['question'][':question/worked-solution']))
  components.append(dict(**c,options=options,original_problem=s[':question/problem'],original_solution=s.get(':question/worked-solution'),recipe_definition='bank() branch '+c['profile'],recipe_interpretation='Observed coefficient patterns; error interpretation unresolved' if c['profile'] in ('negative-log','negative-coefficient-log') else 'Explicit algebraic recipes in bank()'))
  review+=['## '+c['source_id'],'### Original',s[':question/problem'],'\n'.join(a[':answer/value'] for a in orig[':answer-field/choices']),s.get(':question/worked-solution','Missing original solution; new solution authored from canonical substitution.'),'### Replay',g.markdown(r)]
  coverage[c['template']]=0
  for seed in range(8):
   r=g.generate(c['level'],seed,c['template']);validate(r);records.append(r);coverage[c['template']]+=1
  # Signed shift extremes and zero, with each original coefficient condition.
  if 'bound' not in c['parameters'] and c['profile']!='product' or c['parameters'].get('bound')=='numeric' and c['profile']!='unit-definite':
   for shift in (-5,0,5):
    p=dict(c['parameters']);p['b']=shift
    r=g.generate(c['level'],92,c['template'],parameters=p);validate(r);records.append(r);coverage[c['template']]+=1
  # Explicit original and sign/shift boundaries of each source condition.
  for a in (1,20,-1,-20):
   p=dict(c['parameters']);p['a']=a
   try:r=g.generate(c['level'],91,c['template'],parameters=p)
   except ValueError:continue
   validate(r);records.append(r);coverage[c['template']]+=1
  review+=['### Variant',g.markdown(records[-1])]
 a=g.generate('easy',0,'q-113833',parameters=dict(a=1,k='1/7',b=-2));b=g.generate('easy',8,'q-113833',parameters=dict(a=1,k='1/7',b=-2));assert a['question']==b['question']
 try:g.generate('hard')
 except ValueError:pass
 else:raise AssertionError('Hard unsupported')
 save(HERE/'native-input.json',native);save(HERE/'review.json',records);save(HERE/'template-extraction.json',components);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 subprocess.run([str(HERE/'check-current-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 nr=json.loads((HERE/'native-report.json').read_text());assert nr['documented_unresolved_checks']==0
 result=dict(passed=True,source_basis=g.SOURCE['basis'],lineage=g.SOURCE['lineage'],fidelity=dict(complete_banks=len(fidelity),total_banks=12,matched_options=matched,total_options=44,matched_distractors=distractors,details=fidelity),correctness='Independent printed-integrand integration, substitution, bounds, every displayed solution row, final solution and complete bank checks',grading={k:nr[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},coverage=coverage,seed_invariance=True,hard_rejected=True,database_writes=0)
 assert matched==44
 save(HERE/'validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
