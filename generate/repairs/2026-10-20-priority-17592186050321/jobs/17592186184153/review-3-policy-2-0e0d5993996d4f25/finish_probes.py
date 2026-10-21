import sys;sys.dont_write_bytecode=True
import json,pathlib,random,subprocess
from audit_math import *
R=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'workspace'));import generator as G
load=lambda p:json.loads((R/p).read_text())
def save(p,x):(R/p).write_text(json.dumps(x,indent=2)+'\n')
rs=load('shortcut-perfect-records.json');before=rs[-1];pi=before['generation']['parameters'];after=G.build(dict(pi,offset=-1,second_offset=-2),random.Random(7761));assert equal(tex(answer(before)[':answer/value']),tex(answer(after)[':answer/value']));verify(after)
save('bound-counterfactual.json',{'before_parameters':pi,'after_parameters':after['generation']['parameters'],'expected':'Same integrand, answer and solution; changed wrong constant assignments remove guaranteed out-of-domain exclusion.','observed':'Same prompt, solution and correct expression. Only before has a single choice with linear coefficient magnitude <=6.','passes':True})
save('bound-counterfactual-records.json',[before,after])
cases=load('additional-grader-input.json')
# This is an observation run after the acceptance-expectation run failed. It preserves the failure rather than claiming the valid response is wrong.
cases[-1]['checks'][0]['expected']='rejected';cases[-1]['checks'][0]['purpose']='Record known incorrect rejection; semantic acceptance expectation failed in additional-grading-run.log.'
for j,r in enumerate(rs+[after]):
 cases.append({'label':'bound shortcut/control '+str(j),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==answer(r)[':answer/id'] else 'rejected','purpose':'all choices independently differentiated; unique bound-cue survivor selected where available'} for a in field(r)[':answer-field/choices']]})
save('native-observation-input.json',cases)
p=subprocess.run(['/home/jake/Developer/Course_Academy/generate/runs/current/check-engine',str(R/'native-observation-input.json'),str(R/'native-observation.json')],capture_output=True,text=True)
save('native-observation-execution.json',{'command':p.args,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'semantic_grading_defect':'Constant shift expected accepted mathematically, rejected by native grader; changed expectation in this observation run only to save actual outcomes.'});assert p.returncode==0
save('final-render-records.json',rs+[after,load('constant-shift-math.json')['record']])
# Preserve exact run inputs and source of every script.
save('scope-results.json',{'passes':True,'scope':'Two elementary power-rule antiderivatives, one arbitrary constant, no new operators; signs, order, variables, small exponents and constant magnitudes vary. Radical reciprocal domain explicitly positive. Nonconstant coefficients unit magnitude.','families':'P n2..6, R n3/7, B n2..6. Moderate source banks replay completely. Unlabelled radical families remain replay-only; hard/no-field cases math-only.','source_refs':['tutorial 701','e-371','q-71167','q-71169','q-133291','tutorial 703'],'limits':['R5 excluded authored extension to avoid a prior bank cue; remaining R3/R7 preserve reciprocal method. Not evidence of all possible rational powers.']})
save('review-milestone.json',{'source_replay':load('source-replay-results.json'),'math_records':load('math-results.json')['count'],'initial_grading':{k:v for k,v in load('grading.json').items() if k!='records'},'delivered':load('delivery/delivery.json')['accepted_count'],'runner_delivered':load('batch-delivery/delivery.json')['accepted_count'],'demonstrated_defects':['Out-of-range linear coefficient cue has unique correct survivor on four delivered items.','Native grader rejects correct additive-constant-shifted antiderivative under arbitrary external +C.']})
(R/'session-state.md').write_text('Completed source replay, exact math, runtime/relocation, shared delivery, native initial+observation grading, coverage and selection probes. Found 4/4 delivered perfect bound-cue cases and valid constant-shift rejection. Full UI renders running; visual inspection and pedagogical/report finalization pending. Run review.py, check_delivery commands, selection_check.py, variation_current.py, finish_probes.py to reproduce. Package unchanged at runtime milestone; final hash comparison pending.\n')
print(json.dumps({'observation_status':p.returncode,'perfect_shortcuts':len(rs),'native_observation_records':len(cases)}))
