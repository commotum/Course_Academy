"""Read-only policy controls: no generation, publication, or database access."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from scripts.trig_substitution_batch_policy import validate_delivery_batch

def record(problem,key,*,slope='2',amplitude='2',family='def_cos',lower='0',upper='pi/4'):
 return {'question':{':question/problem':problem,':question/worked-solution':'$$\n'+key+'\n$$',':question/difficulty':':question.difficulty/moderate',':question/answer-fields':[{':answer-field/key':'answer',':answer-field/type':':answer-field.type/blank',':answer-field/correct':[':answer/id','a'],':answer-field/choices':[{':answer/id':'a',':answer/value':key}]}]},'generation':{'batch_contract':'trig-substitution-recognition-v6','family':family,'support_policy':'mastered-prerequisite-recall','provided_primitive':False,'provided_endpoint_values':False,'provided_substitution':False,'operation':'evaluate','parameters':{'slope':slope,'amplitude':amplitude},'model':{'substitution':slope+'*x','lower':lower,'upper':upper}}}

cases=[
 ('nonzero_control',record(r'Calculate $\int_0^{\pi/4} 2\cos(2x)\,dx$.','1'),'accepted','Antiderivative sin(2x); sin(pi/2)-sin(0)=1.'),
 ('zero_cancellation_control',record(r'Calculate $\int_0^{\pi} 2\cos(2x)\,dx$.','0',upper='pi'),'rejected','Antiderivative sin(2x); sin(2pi)-sin(0)=0. Same substitution and familiar endpoint operation.'),
 ('canonical_fractional_slope_control',record(r'Calculate $\int 2\sin(x/3)\,dx$.',r'-6\cos(x/3)',slope='1/3',family='indef_sin',lower=None,upper=None),'rejected','Canonical e-464 has exactly this integrand; derivative of -6cos(x/3) is 2sin(x/3). This fixture tests arithmetic policy, not full source replay.'),
]
results=[]
for label,row,expected,math in cases:
 try:validate_delivery_batch([row],17592186068915);actual='accepted';reason=None
 except ValueError as e:actual='rejected';reason=str(e)
 assert actual==expected,(label,actual)
 results.append({'label':label,'observed':actual,'reason':reason,'independent_math':math,'record':row})
out={'scope':'Controlled calls to active current trig delivery policy only. Minimal policy fixtures do not establish full publisher acceptance. No DB/publication/generator changes.','results':results}
print(json.dumps(out,indent=2))
