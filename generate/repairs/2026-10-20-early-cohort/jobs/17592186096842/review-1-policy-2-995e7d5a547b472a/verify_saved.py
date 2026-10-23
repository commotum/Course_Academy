from audit_helpers import *
def eq(a,b):
 # On each source question's positive-radicand real domain, rational powers
 # and sqrt(u^3) agree. Force denesting only for this documented domain.
 return s.simplify(s.powdenest(a,force=True)-s.powdenest(b,force=True))==0
records=sum([json.load(open(ROOT/n)) for n in ['source-replays.json','independent-samples.json','batch-records.json','counterfactual-records.json','focused-samples.json']],[])
cases=[];results=[]
for n,r in enumerate(records):
 a=expected(r);v=latex(correct(r));f=field(r);checks=[]
 if f[':answer-field/type'].endswith('/blank'):
  checks=[{'submitted':str(a).replace('**','^'),'expected':'accepted','purpose':'independent derivative in typed notation'}, {'submitted':s.latex(a),'expected':'accepted','purpose':'independent LaTeX derivative'}, {'submitted':str(a+1).replace('**','^'),'expected':'rejected','purpose':'wrong additive shift'}]
  if a.is_Rational:checks.append({'submitted':f'{a.p*2}/{a.q*2}','expected':'accepted','purpose':'equivalent unreduced rational'})
 else:
  for c in f[':answer-field/choices']:checks.append({'submitted_answer_id':c[':answer/id'],'expected':'accepted' if eq(latex(c[':answer/value']),a) else 'rejected','purpose':'independently checked entire radio bank'})
 cases.append({'label':f'case-{n}-{r["generation"]["template"]}','record':r,'checks':checks})
 results.append({'index':n,'id':r['question'][':question/id'],'expected':str(a),'stored':correct(r),'math_ok':eq(v,a),'correct_count':sum(eq(latex(c[':answer/value']),a) for c in f[':answer-field/choices'])})
save('math-results.json',results);save('grader-input.json',cases)
# Recompute source bank comparisons with positive-domain equivalence.
src=json.load(open(ROOT.parent/'source/source.json'))['material']['kp'][':knowledge-point/questions'];byid={q[':question/math-academy-id']:q for q in src};replay_results=[]
for r in json.load(open('source-replays.json')):
 q=byid[r['generation']['replay_source_id']];f=q[':question/answer-fields'][0];radio=f[':answer-field/type'][':db/ident'].endswith('/radio')
 before=[a[':answer/value'] for a in f[':answer-field/choices']];after=[a[':answer/value'] for a in field(r)[':answer-field/choices']]
 bank_ok=not radio or all(any(eq(latex(a),latex(b)) for b in after) for a in before) and len(before)==len(after)
 replay_results.append({'source_id':q[':question/id'],'source_label':q[':question/math-academy-id'],'radio_bank_equal':bank_ok,'blank_history_preserved':r['generation']['source_capture'][':question/answer-fields']==q[':question/answer-fields'],'correct':correct(r),'expected':str(expected(r)),'math_ok':eq(latex(correct(r)),expected(r)),'prompt_equal':re.sub(r'\s','',q[':question/problem'])==re.sub(r'\s','',r['question'][':question/problem'])})
save('source-replay-results.json',replay_results)
print('math failures', [x for x in results if not x['math_ok'] or x['correct_count']!=1]);print('source exceptions',[x for x in replay_results if not all([x['radio_bank_equal'],x['blank_history_preserved'],x['math_ok'],x['prompt_equal']])])
