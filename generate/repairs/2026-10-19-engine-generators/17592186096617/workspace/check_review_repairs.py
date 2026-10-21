"""Focused author-2 regressions; retain a grading failure instead of masking it."""
import copy,json,re,subprocess,sys
from pathlib import Path
import sympy as s
import generator as g
E=Path('evidence/author-2');E.mkdir(exist_ok=True)
ROOT=Path('/home/jake/Developer/Course_Academy')
def save(n,v):(E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False))
def key(r):
 f=r['question'][':question/answer-fields'][0]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def eq(a,b):return s.trigsimp(s.simplify(s.expand(a-b)))==0
source=json.loads(Path('../source/source.json').read_text())['material']['kp'][':knowledge-point/canonical-example']
assert source[':question/math-academy-id']=='e-3634'
canonical=g.generate('easy',seed=517171,template='q-1907',parameters={'c':1,'n':1,'trig':'cos'})
canonical_product=g.parse(re.search(r'\$([^$]*)\$',source[':question/problem'])[1].rstrip('.'))
assert eq(canonical_product,g.parse(re.search(r'\$([^$]*)\$',canonical['question'][':question/problem'])[1].rstrip('.')))
assert eq(g.parse(key(canonical)),s.diff(canonical_product,g.X))
assert ':question/answer-fields' not in source
save('canonical-replay.json',{'source':source,'generated':canonical,'passed':True,'response_design':'q-1907 five-choice bank, not recovered historical fields','historical_response_field_absent':True})
records=[];pairs=[]
for t in ['q-1907','q-104300','q-47965','q-319357']:
 for trig in (['sin','cos','tan'] if t in ['q-1907','q-104300'] else [None]):
  for c in [1,-1,6]:
   for role in ([0,1] if t=='q-319357' else [0]):
    p={'c':c,'n':1}
    if trig:p['trig']=trig
    a=g.generate('easy',seed=120+len(records),template=t,parameters=p,missing_term=role)
    b=g.generate('easy',seed=120+len(records),template=t,parameters={**p,'n':2},missing_term=role)
    assert not eq(g.parse(key(a)),g.parse(key(b)))
    assert a['question'][':question/problem']!=b['question'][':question/problem']
    assert a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']
    records.append(a);pairs.append({'kind':'degree','before':a,'after':b})
 for n in [0,5]:
  try:g.generate('easy',template=t,parameters={'c':1,'n':n})
  except ValueError:pass
  else:raise AssertionError((t,n,'out-of-range accepted'))
 # Small, deterministic normal-sampling reachability probe, not a variety count.
 for seed in range(30):
  r=g.generate('easy',seed=seed,template=t)
  if r['generation']['parameters']['n']==1:break
 else:raise AssertionError((t,'degree 1 unreachable'))
 pairs.append({'kind':'normal-sampler-degree-1','template':t,'seed':seed,'record':r})
# Source tangent presentation probes at the new boundary, held mathematically fixed.
for seed in [0,1,2,4]:
 records.append(g.generate('easy',seed=seed,template='q-47965',parameters={'c':1,'n':1}))
records.insert(0,canonical)
cases=[]
for i,r in enumerate(records+[p['after'] for p in pairs if p['kind']=='degree']):
 prompt=r['question'][':question/problem'];product=g.parse(re.search(r'\$([^$]*)\$',prompt)[1].rstrip('.'));full=s.diff(product,g.X)
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  assert sum(eq(g.parse(a[':answer/value']),full) for a in f[':answer-field/choices'])==1
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'degree-1 complete bank or fixed-data degree-2 control'} for a in f[':answer-field/choices']]
 else:
  filled=prompt.split('\n\n',1)[1].replace('{{field-1}}','$'+key(r)+'$')
  assert eq(g.parse(filled.split('=',1)[1].replace('$','')),full)
  checks=[{'submitted':key(r),'expected':'accepted','purpose':'linear missing contribution'}, {'submitted':g.tex(g.parse(key(r))+1),'expected':'rejected','purpose':'wrong linear contribution'}]
 cases.append({'label':f'linear:{i}:{r["generation"]["template"]}','record':r,'checks':checks})
save('linear-records.json',records);save('degree-counterfactuals.json',pairs);save('linear-grader-input.json',cases)
# Require acceptance of both plain and TeX forms demonstrated by independent review.
r=g.generate('easy',seed=81763,template='q-310188',parameters={'b':4},missing_term=0)
save('delivery-input.json',records+[r])
reps=[canonical]
for t,trig,role in [('q-104300','sin',0),('q-47965',None,0),('q-319357',None,0),('q-319357',None,1)]:
 reps.append(next(item for item in records if item['generation']['template']==t and (not trig or item['generation']['parameters']['trig']==trig) and item['generation']['missing_term']==role))
save('render-records.json',reps)
assert eq(g.parse(key(r)),2*4**g.X*s.log(2)*s.sin(g.X))
assert s.expand_log(s.log(s.Integer(4)),force=False)==2*s.log(2)
checks=[{'submitted':key(r),'expected':'accepted','purpose':'canonical base-4 value'},
 {'submitted':r'2\cdot 4^{x}\ln(2)\sin(x)','expected':'accepted','purpose':'valid ln(4)=2 ln(2), TeX'},
 {'submitted':'2*4^x*ln(2)*sin(x)','expected':'accepted','purpose':'valid ln(4)=2 ln(2), plain'}]
mandatory=[{'label':'review-base-4-equivalent','record':r,'checks':checks}]
save('log-required-input.json',mandatory)
exe=ROOT/'generate/runs/current/check-engine'
proc=subprocess.run([str(exe),str(E/'log-required-input.json'),str(E/'log-required-report.json')],capture_output=True,text=True)
(E/'log-required.log').write_text(proc.stdout+proc.stderr)
# Diagnostic batch: observe all cases, explicitly not a grading acceptance pass.
diag=copy.deepcopy(mandatory)
for c in diag[0]['checks'][1:]:c['expected']='unresolved'
# Reversing the canonical key simply reverses which equivalent is unsupported.
reverse=copy.deepcopy(r);f=reverse['question'][':question/answer-fields'][0];f[':answer-field/choices'][0][':answer/value']=checks[1]['submitted']
diag.append({'label':'expanded-key-does-not-fix-equivalence','record':reverse,'checks':[{'submitted':key(r),'expected':'unresolved','purpose':'original ln(4) form remains mathematically valid'}]})
save('log-diagnostic-input.json',diag)
d=subprocess.run([str(exe),str(E/'log-diagnostic-input.json'),str(E/'log-diagnostic-report.json')],capture_output=True,text=True)
(E/'log-diagnostic.log').write_text(d.stdout+d.stderr)
assert d.returncode==0,(d.stdout,d.stderr)
save('repair-summary.json',{'canonical_linear_case':'passed','linear_boundary_records':len(records),'degree_counterfactual_pairs':sum(p['kind']=='degree' for p in pairs),'all_polynomial_profiles_sample_degree_1':True,'log_equivalence_required_acceptance_passed':proc.returncode==0,'required_engine_exit_code':proc.returncode,'log_identity_exact_difference':'0','diagnostic_expected_unresolved_is_not_a_pass':True,'delivery_status':'unsupported' if proc.returncode else 'pending_other_checks','reason':'Native grader does not prove ln(4)=2 ln(2); generator package has no grader extension interface and only workspace changes are authorized.'})
print(json.dumps(json.loads((E/'repair-summary.json').read_text()),indent=2))
