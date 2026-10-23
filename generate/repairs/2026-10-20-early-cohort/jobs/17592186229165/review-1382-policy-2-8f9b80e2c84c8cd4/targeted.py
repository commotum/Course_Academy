"""Independent repair-focused tests. All outputs remain beside this script."""
from independent_lib import *
from fractions import Fraction
g=G
a=S.Symbol('a'); b=S.Symbol('b'); A=S.Symbol('A')
def displays(r):
 return re.findall(r'\$\$\s*(.*?)\s*\$\$',r['question'][':question/worked-solution'],re.S)
def rhs(block): return texparse(block.split('=',1)[1].rstrip(',.'))
def aligned_rows(block):
 return [z.split('& =',1) for z in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r' \\ ')]
def hardmath(r):
 h,f,v=params_from_prompt(r); ds=displays(r); trial=rhs(ds[2]); derivrows=aligned_rows(ds[3]); derivative=texparse(derivrows[-1][1]); checks={}
 checks['derivative']=S.simplify(S.diff(trial,x)-derivative)==0
 expected_rates=[S.expand_power_exp(z).args for z in []]
 # Solve coefficient equations independently from the displayed trial, ODE and forcing.
 equations=S.expand(derivative-h*trial-f)
 rates=sorted({z.args[0].coeff(x) for z in f.atoms(S.exp)})
 eqs=[S.expand(equations).coeff(S.exp(k*x)) for k in rates]
 coeffs=S.solve(eqs,(a,b)); assert len(coeffs)==2
 for i,row in enumerate(aligned_rows(ds[4])):
  lhs=texparse(row[0]); right=texparse(row[1]); checks['substitution_row_'+str(i)]=S.simplify((lhs-right).subs(coeffs))==0
 for i,piece in enumerate(ds[5].split(r',\qquad ')):
  left,right=piece.split('=');checks['coefficient_equation_'+str(i)]=S.simplify((texparse(left)-texparse(right)).subs(coeffs))==0
 for i,piece in enumerate(ds[6].split(r',\qquad ')):
  left,right=piece.split('=');checks['coefficient_value_'+str(i)]=S.simplify((texparse(left)-texparse(right)).subs(coeffs))==0
 checks['particular']=S.simplify(rhs(ds[7])-trial.subs(coeffs))==0
 pos=next((i for i,symbol in enumerate((a,b)) if S.simplify(trial.coeff(symbol)-x*S.exp(h*x))==0),None)
 if pos is None:checks['explanation']='Neither exponential' in r['question'][':question/worked-solution']
 else:checks['explanation']='The '+('first' if pos==0 else 'second')+' exponential is a term' in r['question'][':question/worked-solution']
 math=checkmath(r)
 return {'id':r['question'][':question/id'],'resonant_position':None if pos is None else pos+1,'checks':checks,'final_math':math,'passed':all(checks.values()) and math['passed']}

p=dict(h=1,k=1,f=1,k2=2,f2=1,v=0)
specs=[('original',p),('reordered',dict(p,k=2,k2=1)),('transfer-h-only',dict(p,h=2))]
for n,p0 in [('negative-boundary',dict(h=-6,k=-6,f=-12,k2=6,f2=12,v=1)),('positive-boundary',dict(h=6,k=6,f=12,k2=-6,f2=-12,v=-1)),('cancellation',dict(h=-1,k=-1,f=3,k2=1,f2=4,v=2))]:
 specs += [(n,p0),(n+'-reordered',dict(p0,k=p0['k2'],f=p0['f2'],k2=p0['k'],f2=p0['f']))]
controlled=[g.generate('hard',seed=90211,template='mixed',parameters=p0) for name,p0 in specs]
save('hard-controlled-records.json',controlled)
fresh=[g.generate('hard',seed=z,template='mixed') for z in range(230101,230125)]
default=[r for r in load(ROOT/'independent-samples.json') if r['question'][':question/difficulty'].endswith('/hard')]
records=controlled+fresh+default
save('hard-samples.json',records)
results=[hardmath(r) for r in records];save('hard-math-results.json',results);assert all(z['passed'] for z in results)
assert {z['resonant_position'] for z in results[len(controlled):len(controlled)+len(fresh)]}=={1,2}
answers_parsed=lambda r:texparse(answers(r)[0])
y0=answers_parsed(controlled[0]);y1=answers_parsed(controlled[1]);y2=answers_parsed(controlled[2])
assert S.simplify(y0-y1)==0 and S.simplify(y0-y2)!=0
for i in [3,5,7]: assert S.simplify(answers_parsed(controlled[i])-answers_parsed(controlled[i+1]))==0
save('controlled-results.json',{'names':[name for name,p in specs],'source':'Exponent overlap in tutorial e6655774-c9ab-58c6-bfec-5013b08b7918 determines the x multiplier; forcing order is incidental.','reorder_same_solution':True,'transfer_h_only_changes_solution':True,'solutions':[str(y0),str(y1),str(y2)],'all_signed_reorders_preserve_solution':True,'explicit_seed':90211,'fresh_seeds':list(range(230101,230125)),'visible_stage_checks':'hard-math-results.json','records':'hard-controlled-records.json'})
grading=load(ROOT/'grader-input.json')
for i,r in enumerate(controlled):
 y=answers_parsed(r);h,_,v=params_from_prompt(r)
 checks=[{'submitted':S.latex(S.factor(y)),'expected':'accepted','purpose':'independent equivalent factored solution'}, {'submitted':S.latex(y+S.exp(h*x)),'expected':'rejected','purpose':'satisfies ODE, violates initial value'}, {'submitted':'0','expected':'rejected','purpose':'ignore forcing'}]
 if i<3:checks.append({'submitted':S.latex(y0),'expected':'rejected' if i==2 else 'accepted','purpose':'reordered response preserved; h-transfer stale key rejected'})
 grading.append({'label':specs[i][0],'record':r,'checks':checks})
# Exercise each sampled second-position instance with a valid equivalent and a plausible missing-x error.
for i,(r,test) in enumerate(zip(records,results)):
 if test['resonant_position']!=2:continue
 y=answers_parsed(r);h,f,v=params_from_prompt(r)
 force_coef=S.expand(f).coeff(S.exp(h*x));wrong=y-force_coef*x*S.exp(h*x)+force_coef*S.exp(h*x)
 grading.append({'label':'second-position-'+str(i),'record':r,'checks':[{'submitted':S.latex(S.factor(y)),'expected':'accepted','purpose':'second-position factorization'}, {'submitted':S.latex(wrong),'expected':'rejected','purpose':'ordinary instead of x-multiplied resonant trial'}]})
save('grader-input.json',grading)
render=load(ROOT/'runner-batch.json')+controlled[:5]+[load(ROOT/'counterfactual-records.json')[i] for i in [0,1,4]]
save('render-records.json',render)
# Exact stored reproduction, including IDs and generation metadata. No source originals relabeled.
inventory=load(JOB/'source/inventory.json');stored={q[':question/id']:q for q in inventory['questions']}
old=load(JOB/'workspace/17592186229165/reference/replenishment/basis-2525/generated.json');rep=[];affected=[];comparisons=[]
for r in old:
 gen=r['generation'];fresh_r=g.generate('hard',seed=gen['seed'],template=gen['template'],parameters=gen['parameters'],profile=gen['bank_profile']);q=stored[r['question'][':question/id']]
 assert fresh_r==r
 assert all(q[k]==r['question'][k] for k in [':question/id',':question/problem',':question/worked-solution'])
 assert [z[':answer/value'] for z in q[':question/answer-fields'][0][':answer-field/choices']]==answers(r)
 rep.append(fresh_r);comparisons.append({'id':q[':question/id'],'entity_id':q[':db/id'],'complete_generated_record_matches':True,'template':gen['template']})
 if gen['template']=='mixed' and not q.get(':question/retired',False):affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Historical generated mixed cohort fixes resonance first; all five captured generated hard questions have an ordinary second trial. Current generator repair admits either position; stored pool is unchanged.','reproduction':str(sys.executable)+' '+str(ROOT/'targeted.py')+'; explicit hard template='+gen['template']+' seed='+str(gen['seed'])+' parameters='+json.dumps(gen['parameters'],sort_keys=True),'evidence_path':'generated-records.json'})
save('generated-records.json',rep);save('affected-inventory.json',{'affected_questions':affected});save('inventory-reproduction-results.json',{'basis':inventory['basis'],'total_questions':len(stored),'generated_reproduced':comparisons,'original_source_questions':15,'retired_mixed_questions':[q[':question/id'] for q in stored.values() if q.get(':question/retired',False)],'historical_cohort_limit':'Four prior mixed questions retain their historical pattern but are retired at captured basis; no eligible affected mixed questions. One generated both-nonresonant hard record remains eligible and is a justified taught family. No database writes.'})
save('targeted-results.json',{'hard_records':len(records),'fresh_mixed':len(fresh),'native_records':len(grading),'render_records':len(render),'affected_historical_mixed':len(affected),'math_passed':True})
print(json.dumps(load(ROOT/'targeted-results.json')))
