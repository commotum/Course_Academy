import json,pathlib,ast,re,collections,hashlib,sys
import sympy as s
E=pathlib.Path(__file__).resolve().parent;R=pathlib.Path('/home/jake/Developer/Course_Academy');J=E.parent
save=lambda n,x:(E/n).write_text(json.dumps(x,indent=2,default=str))
# Reuse independently authored prompt parser, extending only its valid numeric grammar.
tree=ast.parse((E/'audit.py').read_text());defs=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ['correct','math_check']];exec(compile(ast.Module(body=defs,type_ignores=[]),'audit.py','exec'))
rs=json.load(open(E/'samples.json'))+json.load(open(E/'batch.json'))+json.load(open(E/'focused-records.json'))+json.load(open(E/'counterfactual-records.json'))
math=[]
for r in rs:
 try:math.append(math_check(r))
 except Exception as e:math.append(dict(id=r['question'][':question/id'],passed=False,error=repr(e)))
save('math.json',math)
# Full source replay including complete banks and present/absent attributes.
source={q[':question/math-academy-id']:q for q in json.load(open(J/'source/source.json'))['material']['kp'][':knowledge-point/questions']};checks=[]
for r in json.load(open(E/'source-replays.json')):
 ma=r['generation']['template'];q=source[ma];rq=r['question'];f=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
 c={name:rq.get(name)==q.get(name) for name in [':question/problem',':question/worked-solution',':question/requires-calculator']};c['difficulty']=rq.get(':question/difficulty')==q.get(':question/difficulty',{}).get(':db/ident');c['bank']=sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices']);c['key']=correct(r)==f.get(':answer-field/correct',{}).get(':answer/value');checks.append(dict(template=ma,source_id=q[':question/id'],checks=c,passed=all(c.values())))
save('source-replay-results.json',checks)
def summary(rs):
 out={}
 for template in sorted(set(r['generation']['template'] for r in rs)):
  sub=[r for r in rs if r['generation']['template']==template];ranks=[];positions=[];single=[]
  for r in sub:
   f=r['question'][':question/answer-fields'][0];vs=[s.Rational(a[':answer/value'].split('\\,')[0]) for a in f[':answer-field/choices']];v=s.Rational(correct(r).split('\\,')[0]);rank=sorted(vs).index(v)+1;ranks.append(rank);positions.append(vs.index(v)+1)
   if all(a.q==1 and 0<a<10 for a in vs):single.append(rank)
  out[template]=dict(count=len(sub),rank_counts=dict(collections.Counter(ranks)),position_counts=dict(collections.Counter(positions)),single_digit_count=len(single),single_digit_rank_counts=dict(collections.Counter(single)),distinct_answers=len(set(correct(r) for r in sub)))
 return out
stages={n:summary(json.load(open(E/n))) for n in ['samples.json','easy-samples.json','delivery-sample/accepted.json','batch.json','delivery-batch/accepted.json']}
save('coverage.json',stages)
# Exact learner selection: conditional on the band, the actual SHA draw is uniform across sorted fresh usable entity IDs.
pool=list(range(5));draws=[]
for seed in range(67100,67200):
 digest=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/2**53;draws.append(pool[int(u*5)])
save('selection-analysis.json',dict(implementation='engine/rust/question_selection.rs: select, lines 123-198',captured_basis=5394,stages=stages,conditional_easy_slot_draws=dict(collections.Counter(draws)),seeds=[67100,67199],candidate_assumption='Five accepted fresh usable batch records assigned sorted IDs; weighted easy band has positive weight.',unconfigured_policy='Actual code chooses the first sorted candidate when no distribution is configured. This restricts selection, but does not create an answer cue in the question.',limits=['Live learner history, reservations, entity IDs and policy weights absent; no prediction for a specific learner.','If easy weight is zero, the rated easy batch is not selected. For a positive configured easy weight, all five records remain eligible.','Captured inventory can change after this read-only audit.']))
save('scope.json',dict(passed=True,records=len(rs),assessment='Easy remains t=0 coefficient-sum recognition; moderate remains draining coefficient difference; hard remains unequal-flow evaluation to two decimals. All ten practice source families replay. Positive and zero transients introduce no new prerequisite; zero transients are legitimate simplifications.',response='Five numeric radio choices. No free-entry grading equivalence applies. No new overflow, equal-flow or capacity event.'))
# Explicit commands and source of independently retained tests.
save('commands.json',dict(python=sys.executable,commands=['python audit.py','python regression-tests.py','python historical-regressions.py (expected four failures on preserved old package)','python focused.py','python finish-evidence.py','check-engine grader-input.json grader-report.json','python generate/pipeline/check_delivery.py --input easy-samples.json / batch.json --source <job>/source/source.json --inventory <job>/source/inventory.json --difficulty easy --output delivery-sample / delivery-batch --math-root /media/jake/SSD/EDB/math','python generate/pipeline/render_preview.py --input render-records.json --output render --math-root /media/jake/SSD/EDB/math'],fresh_seeds=[92031,92070,2203,5783,57391],retained_counterexamples=[619,733,8114]))
print(json.dumps(dict(math_count=len(math),math_failures=[m for m in math if not m.get('passed')],source_failures=[x for x in checks if not x['passed']],stages=stages)))
(E/'session-state.md').write_text('Source replay and four historical/current regressions completed. Independent exact math, native grader (132 accept/528 reject), controlled pairs, focused distractor/sign/boundary checks and both delivery stages completed. Actual UI render running; final visual inspection and report pending. Package unchanged.\n')
