"""Independent printed-expression calculus, complete source banks and actual grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE))
from scalar_parser import scalar,same,group
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
native=[]
def save(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def value(s):return scalar(s.replace(' + C','').replace('+C',''))
def integrate_printed(f,limits=None):
 # Recognize a constant logarithmic derivative from the independently parsed expression.
 slope=g.sp.simplify(g.sp.diff(f,g.x)/f)
 assert not slope.has(g.x) and slope!=0, 'Printed function is not a nonconstant linear exponential'
 primitive=f/slope
 assert g.sp.simplify(g.sp.diff(primitive,g.x)-f)==0
 return g.sp.simplify(primitive.subs(g.x,limits[1])-primitive.subs(g.x,limits[0])) if limits else primitive

def target(q):
 f,limits=g.printed(q);return integrate_printed(f,limits)
def row_value(rhs,p):
 rhs=rhs.replace('+C','')
 if r'\int' in rhs:
  prefix=rhs.split(r'\int',1)[0].strip();coef=value(prefix) if prefix else g.sp.Integer(1)
  transformed=r'\text{d}u' in rhs;rhs=rhs.replace(r'\text{d}u',r'\text{d}x').replace('u','x') if transformed else rhs
  f,limits=g.printed({':question/problem':rhs});result=integrate_printed(f,limits)
  if transformed and not limits:result=result.subs(g.x,g.sp.Rational(p['k'])*g.x+g.sp.Rational(p['b']))
  return coef*result
 if r'\left[' in rhs:
  pre,rest=rhs.split(r'\left[',1);func,rest=rest.split(r'\right]_',1);lo,j=group(rest,0);assert rest[j]=='^';hi,j=group(rest,j+1)
  F=value(func.replace('u','x'));coef=value(pre) if pre.strip() else g.sp.Integer(1);return coef*(F.subs(g.x,value(hi))-F.subs(g.x,value(lo)))
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
 t=target(q);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];cid=f[':answer-field/correct'][1];vals=[value(a[':answer/value']) for a in choices]
 assert len(set(a[':answer/id'] for a in choices))==len(choices)
 assert sum(same(v,t) for v in vals)==1;assert same(next(v for a,v in zip(choices,vals) if a[':answer/id']==cid),t)
 assert not any(same(v,w) for i,v in enumerate(vals) for w in vals[:i])
 solution=q[':question/worked-solution'];p=m['parameters'];u=value(re.search(r'If we let \$u=(.*?)\$',solution)[1].rstrip(','));actual,_=g.printed(q)
 assert same(g.sp.diff(u,g.x),g.sp.Rational(p['k']));assert same(g.sp.Rational(p['a'])*g.sp.Integer(p['n'])**u,actual)
 differential=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(.*?)\\quad\\Longrightarrow\\quad (.*?)\\,\\text\{d\}u',solution)
 assert same(value(differential[1]),g.sp.diff(u,g.x)) and same(value(differential[2]),1/g.sp.diff(u,g.x))
 final=solution.split('&=')[-1].split(r'\end{aligned}')[0];assert same(value(final),t)
 for row in solution.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0].split(r'\\'):
  assert same(row_value(row.split('&=')[1],p),t),(m['template'],row)
 if 'L' in p:
  table=solution.split('| $u$ | ')[1].split('\n')[0];lo,hi=re.findall(r'\$(.*?)\$',table)[:2];limits=g.printed(q)[1]
  assert same(value(lo),u.subs(g.x,limits[0])) and same(value(hi),u.subs(g.x,limits[1]))
 else:assert same(g.sp.diff(value(final),g.x),actual)
 if f[':answer-field/type'].endswith('/radio'):
  assert len(choices)==5;checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==cid else 'rejected',purpose='All field-owned choices') for a in choices]
 else:
  assert len(choices)==1 and q[':question/problem'].count('{{field-1}}')==1
  canonical=choices[0][':answer/value'];checks=[dict(submitted=canonical,expected='accepted',purpose='Canonical exact answer'),dict(submitted='('+canonical+')*2/2',expected='accepted',purpose='Equivalent scalar entry'),dict(submitted=g.tex(t+1),expected='rejected',purpose='Incorrect additive value'),dict(submitted=g.tex(-t),expected='rejected',purpose='Incorrect sign')]
 native.append(dict(label=q[':question/id'],record=rec,checks=checks))

def validate_existing(q):
 assert q.get(':question/worked-solution') and len(q.get(':question/answer-fields',[]))==1
 f=q[':question/answer-fields'][0];assert ':answer-field/correct' in f;t=target(q)
 assert same(value(f[':answer-field/correct'][':answer/value']),t)
 vals=[value(a[':answer/value']) for a in f[':answer-field/choices']];assert sum(same(v,t) for v in vals)==1
 assert any(a[':answer/id']==f[':answer-field/correct'][':answer/id'] for a in f[':answer-field/choices'])
 if f[':answer-field/type'][':db/ident'].endswith('/radio'):assert len(vals)==5 and not any(same(v,w) for i,v in enumerate(vals) for w in vals[:i])
 # Source final solution must agree with the independently evaluated integral.
 final=q[':question/worked-solution'].split('& =')[-1].split('&=')[-1].split(r'\end{aligned}')[0];assert same(value(final),t)
 return True

def main():
 fidelity=[];review=[];records=[];components=[];coverage={};matched=0;distractors=0
 for c in g.CASES:
  print('Validating '+c['source_id'],flush=True)
  s=g.QS[c['source_id']];r=g.generate(c['level'],0,c['template'],parameters=c['parameters']);validate(r);records.append(r)
  orig=s[':question/answer-fields'][0];out=r['question'][':question/answer-fields'][0];remaining=list(out[':answer-field/choices']);options=[]
  for a in orig[':answer-field/choices']:
   match=next((v for v in remaining if same(value(a[':answer/value']),value(v[':answer/value']))),None);assert match,(c['source_id'],a)
   remaining.remove(match);matched+=1;correct=same(value(a[':answer/value']),target(s));distractors+=not correct
   options.append(dict(source_answer_id=a[':answer/id'],observed_value=a[':answer/value'],recipe_index=out[':answer-field/choices'].index(match),exact_replay=True,correct=correct))
  assert not remaining and g.fingerprint(s)==r['generation']['math_fingerprint']
  if ':answer-field/correct' in orig:assert same(value(orig[':answer-field/correct'][':answer/value']),target(s))
  fidelity.append(dict(source_id=c['source_id'],complete_bank=True,options=len(options),prompt_math=True,literal_prompt=s[':question/problem']==r['question'][':question/problem'],literal_solution=s.get(':question/worked-solution')==r['question'][':question/worked-solution'],legacy_missing_solution=not s.get(':question/worked-solution')))
  components.append(dict(**c,options=options,original_problem=s[':question/problem'],original_solution=s.get(':question/worked-solution'),recipe_definition='bank() branch '+c['profile'],recipe_interpretation='Observed complete mathematical expressions; error psychology unresolved. Fixed -7 in positive bank remains observed constant.'))
  review+=['## '+c['source_id'],'### Original',s[':question/problem'],'\n'.join(a[':answer/value'] for a in orig[':answer-field/choices']),s.get(':question/worked-solution','Missing source solution; generated replay uses canonical e-460 substitution.'),'### Replay',g.markdown(r)]
  coverage[c['template']]=0
  for seed in range(6):
   r=g.generate(c['level'],seed,c['template']);validate(r);records.append(r);coverage[c['template']]+=1
  for n in (2,6):
   p=dict(c['parameters']);p['n']=n
   try:r=g.generate(c['level'],90,c['template'],parameters=p)
   except ValueError:continue
   validate(r);records.append(r);coverage[c['template']]+=1
  if c['profile']=='blank':
   for shift in (-4,0,8):
    p=dict(c['parameters']);p['b']=shift;r=g.generate(c['level'],91,c['template'],parameters=p);validate(r);records.append(r);coverage[c['template']]+=1
   for low,high in [(-2,4),(0,1)]:
    p=dict(c['parameters']);p.update(L=low,H=high);r=g.generate(c['level'],92,c['template'],parameters=p);validate(r);records.append(r);coverage[c['template']]+=1
  review+=['### Variant',g.markdown(records[-1])]
 a=g.generate('easy',0,'q-31413',parameters=dict(a=1,k=4,b=0,n=3));b=g.generate('easy',10,'q-31413',parameters=dict(a=1,k=4,b=0,n=3));assert a['question']==b['question']
 try:g.generate('hard')
 except ValueError:pass
 else:raise AssertionError('Hard unsupported')
 save(HERE/'native-input.json',native);save(HERE/'review.json',records);save(HERE/'template-extraction.json',components);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 subprocess.run([str(HERE/'check-current-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 nr=json.loads((HERE/'native-report.json').read_text());assert nr['documented_unresolved_checks']==0
 result=dict(passed=True,source_basis=g.SOURCE['basis'],lineage=g.SOURCE['lineage'],fidelity=dict(complete_banks=len(fidelity),total_banks=11,matched_options=matched,total_options=35,matched_distractors=distractors,details=fidelity),correctness='Independent printed-integrand integration, every displayed solution row, differential and bound transformations; full bank pairwise comparisons',grading={k:nr[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},coverage=coverage,seed_invariance=True,hard_rejected=True,database_writes=0)
 assert matched==35
 save(HERE/'validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
