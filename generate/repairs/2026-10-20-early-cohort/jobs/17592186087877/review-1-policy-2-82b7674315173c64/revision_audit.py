"""Independent bounded revision audit. Run with context venv; all writes under this directory."""
import sys
sys.dont_write_bytecode=True
import collections,copy,difflib,hashlib,importlib.util,json,pathlib,shutil,subprocess
HERE=pathlib.Path(__file__).resolve().parent; JOB=HERE.parent; REPO=pathlib.Path('/home/jake/Developer/Course_Academy');PKG=JOB/'workspace'; PREV=JOB/'review-0-policy-2-34bbd6ba8ad34ac5'
def save(n,v): (HERE/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
def module(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
A=module('independent_helpers',HERE/'independent_helpers.py');G=A.G;S=A.S

def value(r):return next(a[':answer/value'] for a in A.field(r)[':answer-field/choices'] if a[':answer/id']==A.key(r))
def bank(r):return sorted(a[':answer/value'] for a in A.field(r)[':answer-field/choices'])
def coefficient(a):
 left=A.clean(a[':answer/value']).split('=')[0]; f=A.scalar(left[len('\\frac{d}{dx}'):])/A.Y
 return S.simplify(S.diff(f,A.X)/f)
def probes(rows,label):
 out=[]
 for t in [None]+sorted({r['generation']['template'] for r in rows}):
  rs=[r for r in rows if t is None or r['generation']['template']==t]
  strategies={n:[] for n in ['first_position','smallest_abs','largest_abs','smallest_signed','largest_signed','double_exponent']}
  for r in rs:
   choices=A.field(r)[':answer-field/choices'];cs=[(a[':answer/id'],coefficient(a)) for a in choices];preds={'first_position':cs[0][0],'double_exponent':A.shortcut(r)}
   for n,fn,which in [('smallest_abs',abs,min),('largest_abs',abs,max),('smallest_signed',lambda x:x,min),('largest_signed',lambda x:x,max)]:
    v=which(fn(c) for _,c in cs);w=[aid for aid,c in cs if fn(c)==v];preds[n]=w[0] if len(w)==1 else None
   for n,p in preds.items():strategies[n].append({'question_id':r['question'][':question/id'],'prediction':p,'key':A.key(r),'success':p==A.key(r)})
  for name,attempts in strategies.items():out.append({'dataset':label,'template':t or 'overall','strategy':name,'correct':sum(x['success'] for x in attempts),'total':len(rs),'attempts':attempts})
 return out

def source_replay():
 qs={q[':question/math-academy-id']:q for q in load(JOB/'source/source.json')['material']['kp'][':knowledge-point/questions']}; records=[]; checks=[]
 for sid,t,p in G.CASES:
  r=G.generate(G.TEMPLATES[t][0],seed=82917,template=t,parameters=p,profile='observed_raw');q=qs[sid];unmatched=list(A.field(r)[':answer-field/choices']);matches=[]
  for a in q[':question/answer-fields'][0][':answer-field/choices']:
   if 'dx^{2}' in A.clean(a[':answer/value']):m=next(b for b in unmatched if 'dx^{2}' in b[':answer/value'])
   else:m=next(b for b in unmatched if S.simplify(A.normalized(A.equation(b[':answer/value']))-A.normalized(A.equation(a[':answer/value'])))==0)
   unmatched.remove(m);matches.append({'source_answer':a[':answer/id'],'generated_answer':m[':answer/id']})
  assert not unmatched
  sf=q[':question/answer-fields'][0]; designation='inferred: no captured key'
  if ':answer-field/correct' in sf:
   assert next(x['generated_answer'] for x in matches if x['source_answer']==sf[':answer-field/correct'][':answer/id'])==A.key(r);designation='captured correct link matched'
  # Reuse earlier independent normalization of source prompt, verify current exact equation unchanged.
  old=next(x for x in load(PREV/'source-replay-records.json') if x['generation']['template']==t)
  assert S.simplify(A.normalized(A.prompt_equation(old)[1])-A.normalized(A.prompt_equation(r)[1]))==0
  # Construction outside affected easy bank is unchanged; raw prompt + solution exact replay.
  assert r['question'][':question/problem']==old['question'][':question/problem']
  assert r['question'][':question/worked-solution']==old['question'][':question/worked-solution']
  records.append(r);checks.append({'source_id':q[':question/id'],'template':t,'all_five_matched':True,'designation':designation,'prompt_and_solution_equal_previous_independently_checked_replay':True,'matches':matches})
 canonical=G.generate('easy',82917,'constant_exp',parameters={'a':'2','b':2,'c':-2}); target=A.V+2*A.Y-2*S.exp(-2*A.X)
 assert S.simplify(A.normalized(A.prompt_equation(canonical)[1])-target)==0
 A.math_check(canonical);records.append(canonical)
 save('source-replay-records.json',records);save('source-replay-results.json',{'cases':checks,'canonical_reachable':True,'canonical_math':A.math_check(canonical),'limitations':load(HERE/'source-analysis.json')['gaps_and_source_corrections'],'prior_evidence':'provenance.json'})
 return canonical

def run():
 save('package-before.json',A.snapshot())
 old=module('old_generator',PREV/'relocated-package/17592186087877.py')
 (HERE/'implementation.diff').write_text(''.join(difflib.unified_diff((PREV/'relocated-package/17592186087877.py').read_text().splitlines(True),(PKG/'17592186087877.py').read_text().splitlines(True),fromfile='previous',tofile='current')))
 retained=[];old_records=[];new_records=[]
 for name,g in [('previous',old),('current',G)]:
  rs=[g.generate('easy',8173,'signed_constant_power',parameters={'a':a,'n':2}) for a in ['1','-1']]
  outcomes=[A.shortcut(r)==A.key(r) for r in rs]
  canonical=None
  if 'constant_exp' in g.TEMPLATES:canonical=g.generate('easy',19073,'constant_exp',parameters={'a':'2','b':2,'c':-2})
  else:
   candidates=[g.generate('easy',19073,t,parameters=({'a':'2','b':v} if t=='constant_cos' else {'a':'2','n':v})) for t in ['constant_cos','scaled_constant_power','signed_constant_power'] for v in range(1,5)]
   old_records+=candidates
   assert not any(S.simplify(A.normalized(A.prompt_equation(r)[1])-(A.V+2*A.Y-2*S.exp(-2*A.X)))==0 for r in candidates)
  retained.append({'implementation':name,'double_exponent_outcomes':outcomes,'shortcut_regression_passed':not all(outcomes),'canonical_reachable':canonical is not None})
  if name=='previous':old_records+=rs
  else:new_records+=rs+[canonical]
 assert retained[0]['shortcut_regression_passed']==False and retained[0]['canonical_reachable']==False
 assert retained[1]['shortcut_regression_passed'] and retained[1]['canonical_reachable']
 save('retained-findings-results.json',{'command':f'{sys.executable} revision_audit.py','findings':retained,'preflight':load(JOB/'repair-preflight.json'),'not_only_self_authored_checks':True})
 save('previous-failing-records.json',old_records);save('repaired-counterexamples.json',new_records)
 canonical=source_replay()
 # Small independent stratified sample, with new seeds selected here.
 samples=[];trace=[]
 original_sample=G.sample
 for t,(level,_) in G.TEMPLATES.items():
  for seed in ([741801,741823,741877,741901,741917,741953] if level=='easy' else [741823]):
   calls=[]
   def instrumented(tt,rng):
    pp=original_sample(tt,rng);calls.append(copy.deepcopy(pp));return pp
   G.sample=instrumented
   r=G.generate(level,seed,t);G.sample=original_sample
   samples.append(r);trace.append({'template':t,'seed':seed,'calls':calls,'accepted':r['question'][':question/id']})
 save('samples.json',samples);easy=[r for r in samples if r['question'][':question/difficulty'].endswith('/easy')];save('easy-samples.json',easy)
 save('generator-rejection-trace.json',trace)
 # Full identical-bank target orbits: a prior defect could hide within a template.
 coeffs=['-3','-1/2','1/3','1','2'];orbits=[];controlled=[]
 for t in ['constant_cos','constant_exp','scaled_constant_power','signed_constant_power']:
  rs=[]
  for a in coeffs:
   p={'a':a,**({'b':2,'c':-2} if t=='constant_exp' else {'b':2} if t=='constant_cos' else {'n':2})}
   rs.append(G.generate('easy',951147,t,parameters=p,bank_coefficients=coeffs))
  assert len({tuple(bank(r)) for r in rs})==1 and len({value(r) for r in rs})==5
  assert len({r['question'][':question/worked-solution'] for r in rs})==5
  orbits.append({'template':t,'bank_held_fixed':True,'target_coefficients':coeffs,'correct_equations':[value(r) for r in rs]});controlled+=rs
 base=controlled[0];permuted=G.generate('easy',951149,'constant_cos',parameters=base['generation']['parameters'],bank_coefficients=coeffs)
 assert base['question'][':question/problem']==permuted['question'][':question/problem'] and value(base)==value(permuted)
 assert base['question'][':question/worked-solution']==permuted['question'][':question/worked-solution']
 assert A.field(base)[':answer-field/choices']!=A.field(permuted)[':answer-field/choices']
 controlled.append(permuted)
 # Relevant forcing change: I unchanged but IQ and solution must change, canonical cancellation/noncancellation.
 changed_q=G.generate('easy',951147,'constant_exp',parameters={'a':'2','b':2,'c':1},bank_coefficients=coeffs)
 controlled.append(changed_q)
 # Explicit boundaries in changed constant/exp family.
 boundaries=[G.generate('easy',54019,'constant_exp',parameters={'a':a,'b':b,'c':c}) for a,b,c in [('-4',-4,4),('4',4,-4),('-11/3',1,1),('11/3',-1,-1)]]
 save('boundary-records.json',boundaries);save('counterfactual-records.json',controlled);save('counterfactual-results.json',{'orbits':orbits,'irrelevant_permutation_preserved_prompt_solution_response':True,'forcing_pair_indices':[9,len(controlled)-1],'forcing_expected':'same I=e^(2x), changed IQ; cancellation versus noncancellation','command':f'{sys.executable} revision_audit.py'})
 batch=load(JOB/'samples.json');save('runner-batch.json',batch)
 allrows=samples+controlled+boundaries+new_records+batch
 save('math-results.json',{'command':f'{sys.executable} revision_audit.py','cases':[A.math_check(r) for r in allrows]})
 save('shortcut-results.json',probes(easy,'fresh default')+probes(controlled[:20],'controlled five-target orbits')+probes(batch,'runner batch'))
 cases=[]
 for r in allrows:
  cases.append({'label':r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==A.key(r) else 'rejected','purpose':'Independent printed product-rule and normalized-equation comparison'} for a in A.field(r)[':answer-field/choices']]})
 # Submit before-response mathematical choice using after-record UUID; each is a real owned bank choice.
 for i in [0,5,10,15]:
  before,after=controlled[i],controlled[i+4]
  a=next(a for a in A.field(after)[':answer-field/choices'] if a[':answer/value']==value(before))
  cases.append({'label':f'old response invalid after P change {i}','record':after,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'rejected','purpose':'Relevant coefficient changes invalidate old mathematical equation even with identical entire bank'}]})
 save('grader-input.json',cases)
 render=[controlled[i] for i in [0,4,5,9,10,14,15,19,20,21]]+[canonical]
 save('render-input.json',render)
 # Runtime/package contract and explicit rejection boundaries.
 rejects=[]
 for label,kw in [('zero a',{'a':'0','b':1,'c':1}),('a above bound',{'a':'13/3','b':1,'c':1}),('denominator 4',{'a':'1/4','b':1,'c':1}),('zero b',{'a':'1','b':0,'c':1}),('zero c',{'a':'1','b':1,'c':0}),('fractional c',{'a':'1','b':1,'c':'1/2'}),('missing c',{'a':'1','b':1}),('extra slot',{'a':'1','b':1,'c':1,'n':2})]:
  try:G.generate('easy',54019,'constant_exp',parameters=kw)
  except ValueError as e:rejects.append({'case':label,'rejected':True,'message':str(e)})
  else:raise AssertionError(label)
 for label,kwargs in [('bank duplicate',{'bank_coefficients':['1']*5}),('bank missing target',{'parameters':{'a':'4','b':1,'c':1},'bank_coefficients':coeffs}),('wrong field',{'field_type':'free'}),('bad profile',{'profile':'absent'}),('outside difficulty',{'template':'linear_sin'})]:
  try:G.generate('easy',54019,**({'template':'constant_exp'} if 'template' not in kwargs else {}),**kwargs)
  except (ValueError,KeyError) as e:rejects.append({'case':label,'rejected':True,'message':str(e)})
  else:raise AssertionError(label)
 deps=load(PKG/'package.json')['dependencies'];assert deps=={'python':sys.version.split()[0],'packages':{'sympy':S.__version__}}
 assert all(G.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],r['generation']['template'])==r for r in samples)
 save('packaging-results.json',{'versions':{'python':sys.version.split()[0],'sympy':S.__version__},'manifest':deps,'rejections':rejects,'deterministic_replay':True,'external_output':'Generator imports only standard library, declared SymPy and bundled source JSON; no writes or generated external assets.'})
 # Retain the prior independently reproduced affected inventory; bindings match.
 inv=load(JOB/'source/inventory.json');byid={q[':question/id']:q for q in inv['questions']};historical=load(PREV/'generated-records.json')
 for r in historical:
  q=byid[r['question'][':question/id']];assert q[':question/problem']==r['question'][':question/problem'];assert q[':question/worked-solution']==r['question'][':question/worked-solution'];f=q[':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==bank(r)
  assert f[':answer-field/correct'][':answer/id']==A.key(r)
 save('generated-records.json',historical);save('affected-inventory.json',load(PREV/'affected-inventory.json'))
 affected=load(HERE/'affected-inventory.json');
 for a in affected['affected_questions']:a['reproduction']=f'{sys.executable} revision_audit.py; retained complete historical generated records verified against captured inventory; old version seed/template/parameters/profile in generated-records.json'
 save('affected-inventory.json',affected)
 save('inventory-results.json',{'basis':inv['basis'],'total_questions':len(inv['questions']),'historical_generated_reproductions':len(historical),'affected_historical_easy':len(affected['affected_questions']),'current_generator_fixed':True,'original_sources_not_marked_generated':True,'limits':'Reused previous independent exact old implementation replay, confirmed current inventory content, keys and banks. Historical generator metadata is retained, not relabelled as current. No database modification performed.'})
 save('scope-results.json',{'source_reasoning':'a6a381ed Steps 1-4; stop before integrating IQ','changed_templates':['constant_cos','constant_exp','scaled_constant_power','signed_constant_power'],'judgment':'All generated records retain normalization, elementary integration of constant P and product-rule rewriting. Independent b,c change forcing only; all-exp distractors compare same constant-integration operation. Rational bounds already admitted by previous explicit contract. Six unchanged moderate/hard samples only regression coverage, not new scope expansion.','source_refs':['1e3c0253-226d-596c-a831-7c68ec76b21c','dba525fe-7e4d-5319-88bd-1b806feb0904'],'records':'samples.json'})
 save('provenance.json',{'previous_review':str(PREV),'bindings':'runner matched source hash and policy; inventory sha256 '+hashlib.sha256((JOB/'source/inventory.json').read_bytes()).hexdigest(),'reused_files':{n:hashlib.sha256((PREV/n).read_bytes()).hexdigest() for n in ['audit.py','source-analysis.json','generated-records.json','affected-inventory.json','source-replay-records.json']},'changes':'Imported independent parser/math checks, reran against current records. Reused source replay baseline and immutable inventory exact replay evidence; no prior verdict used as certification.'})
 (HERE/'session-state.md').write_text('Revision milestone: retained failures reproduced on previous implementation and repaired on current. Eight source banks and canonical replayed. Fresh sample, controlled target orbits, boundaries, exact math checks and native grader inputs saved. Historical inventory verified. Await delivery, native grader, actual UI render, selection, relocation, final report.\n')
 print(json.dumps({'samples':len(samples),'math_records':len(allrows),'counterfactuals':len(controlled),'source_cases':9,'native_cases':sum(len(c['checks']) for c in cases),'historical_affected':len(affected['affected_questions'])}))
if __name__=='__main__':run()
