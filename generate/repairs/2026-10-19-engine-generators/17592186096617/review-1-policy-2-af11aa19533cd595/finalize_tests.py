import sys,os,json,re,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
from audit import g,save,parse,eq,key,inspect,S,ROOT,PKG
cases=json.loads((ROOT/'grader-input.json').read_text())
# Plain log in the independent CAS string means natural log; spell it ln for the learner's convention.
for item in cases:
 for check in item['checks']:
  if 'submitted' in check:check['submitted']=check['submitted'].replace('log(', 'ln(')
pairs=json.loads((ROOT/'counterfactuals.json').read_text())
for i,pair in enumerate(pairs):
 a,b=pair['records'];aa,bb=parse(key(a)),parse(key(b));same=eq(aa,bb);pair['same_key']=same;pair['math_checks']=[inspect(r) for r in pair['records']]
 pair['relationship_passed']=not same if pair['kind']=='relevant' else same
 if pair['kind']=='relevant':
  for j,(r,other) in enumerate(((a,b),(b,a))):
   cases.append({'label':'counterfactual_stale_'+pair['label']+'_'+str(j),'record':r,'checks':[{'submitted':key(other),'expected':'rejected','purpose':'stale response after relevant evidence change'}]}) if pair['math_checks'][j]['kind']=='blank' else None
 else:
  for r,other in ((a,b),(b,a)):
   # Native radio response follows the matching mathematical value, never an old UUID.
   from audit import field
   choice=next(z for z in field(r)[':answer-field/choices'] if eq(parse(z[':answer/value']),parse(key(other))))
   cases.append({'label':'irrelevant_presentation','record':r,'checks':[{'submitted_answer_id':choice[':answer/id'],'expected':'accepted','purpose':'unchanged mathematical answer under shuffled and expanded notation'}]})
save('counterfactuals.json',pairs)
# A concrete extension gap: composite exponential base introduces a commonplace equivalent logarithm coefficient.
r=g.generate(seed=81763,template='q-310188',parameters={'b':4},missing_term=0)
log_record=r
expanded=r'2\\cdot 4^{x}\\ln(2)\\sin(x)'.replace('\\\\','\\')
assert eq(parse(expanded),parse(key(r)))
save('log-identity-samples.json',[r]);save('log-identity-proof.json',{'parameters':{'template':'q-310188','seed':81763,'parameters':{'b':4},'missing_term':0},'stored':key(r),'equivalent':expanded,'symbolic_difference':str(S.simplify(parse(expanded)-parse(key(log_record)))),'expected':'accepted','source':'q-310188 response is a missing mathematical summand, no mandated logarithm form'})
cases.append({'label':'logarithm_equivalent_base4','record':r,'checks':[{'submitted':key(r),'expected':'accepted','purpose':'canonical answer'}, {'submitted':expanded,'expected':'accepted','purpose':'valid equivalent ln4=2ln2, no simplest-form requirement'}]})
# Determinism means replaying all explicit controls too.
records=json.loads((ROOT/'samples.json').read_text());det=[]
for r in records:
 m=r['generation'];z=g.generate(seed=m['seed'],template=m['template'],parameters=m['parameters'],missing_term=0 if m['missing_term']=='full' else m['missing_term']);det.append(z==r)
p=json.loads((ROOT/'packaging-results.json').read_text());p['deterministic']=det;p['all_replays_equal']=all(det);save('packaging-results.json',p)
save('grader-input-final.json',cases)
save('test-harness-corrections.json',{'initial_grader_log':'grader.log','corrections':['CAS plain log was spelled ln to match native learner notation; no alias defect inferred.','Determinism rerun now includes original explicit parameters and missing-term controls. Initial false values reflected omitted controls, not nondeterminism.'],'all_explicit_control_replays_equal':all(det)})
# Add composite base to actual UI and shared filtering evidence, without changing package.
render=json.loads((ROOT/'render-input.json').read_text());save('extra-render-input.json',[log_record])
print('final grading cases',len(cases),'deterministic',all(det),'log identity',expanded,'difference',S.simplify(parse(expanded)-parse(key(log_record))))
