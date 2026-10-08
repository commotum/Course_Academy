import sys,json,shutil,math
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'scripts/question_capture'))
from capture import arguments
from solver import Solver
from core import atomic_json
p=Path('reference/mathacademy/question-capture-workers/differential/14039776').resolve()
r=p/'manual-recovery';r.mkdir(exist_ok=True)
for name in ['state.json','q-128452-before.json','q-128452-before.png','q-128452/solve-answer.json','q-128452/solve-input.json','q-128452/solve-events.jsonl','solver-session/state.json']:
 dest=r/'original'/name;dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.exists():shutil.copy2(p/name,dest)
try:math.log(-2);raise AssertionError('expected real-domain error')
except ValueError:pass
# On an open interval about -1, ln|2t| = ln(-2t), derivative 1/t.
value=(-8/math.sqrt(3-(-1))-(2*(-1)-1),2*math.pi*math.cos(-math.pi)-2*math.pi*(-1),2/(-1)+2*(-1))
assert value==(-1,0,-4)
def corrected(t):return [16*math.sqrt(3-t)-(t*t-t),2*math.sin(math.pi*t)-math.pi*t*t,2*math.log(abs(2*t))-(1-t*t)]
h=1e-5; numeric=[(a-b)/(2*h) for a,b in zip(corrected(-1+h),corrected(-1-h))]
assert all(abs(a-b)<1e-8 for a,b in zip(numeric,value))
atomic_json(r/'mathematical-check.json',{'original_real_derivative':'undefined: ln(2t) not defined at t=-1','local_prompt_correction':'replace ln(2t) by ln|2t|','corrected_derivative':'<-8/sqrt(3-t)-(2t-1),2*pi*cos(pi*t)-2*pi*t,2/t+2*t>','corrected_value':value,'central_difference_check':numeric,'passed':True})
args=arguments(['run','--codex-bin','/home/jake/.local/bin/codex'])
s=Solver(args);sf=p/'solver-session/state.json';session=json.loads(sf.read_text());payload=json.loads((p/'q-128452/solve-input.json').read_text())
context,keys=s.activity_context(p,session['context_keys']);payload['activity_context']=context
payload['mode']='authorized_source_error_recovery'
payload['source_error_review']={
'original_mathematical_result':'The REAL-valued derivative is undefined at t=-1 because ln(2t) is undefined there. Do not call the original mathematics correct.',
'verified_local_repair':'Replace ln(2t) with ln|2t|, whose derivative is 1/t near -1. All components then give <-1,0,-4>, exactly displayed option e.',
'authorization':'User explicitly authorizes completing source captures for decisive website mathematical errors, preserving the original evidence and source accepted answer, then applying this verified local correction to study database prompt, worked solution and answer key. This turn concerns ONLY the unambiguous expected formal answer used to obtain server grading evidence. Confident refers to this website intent under the documented local repair, not validity of original real-valued prompt.',
'request':'Independently verify derivative components and displayed e. Return expected website option with a precise explanation retaining the original domain defect and corrected interpretation. Do not alter the original prompt or invent a displayed undefined choice.'}
phase='source-error-review';atomic_json(p/'q-128452'/f'{phase}-input.json',payload)
answer=s.codex_turn(payload,p/'q-128452-before.png',p/'q-128452',phase,sf,session,keys)
s.validate(json.loads((p/'q-128452-before.json').read_text()),answer)
atomic_json(p/'q-128452'/f'{phase}-answer.json',answer)
atomic_json(p/'q-128452/solve-answer.json',answer)
atomic_json(r/'recovery.json',{'task':14039776,'question':'q-128452','original_real_derivative':'undefined','local_corrected_prompt':'ln|2t|','website_formal_answer':'<-1,0,-4>','solver_session':session['session_id'],'repair_attempt':2,'original_uncertainty_preserved':str(r/'original/q-128452/solve-answer.json'),'mathematical_check':str(r/'mathematical-check.json')})
print(json.dumps(answer,ensure_ascii=False))
