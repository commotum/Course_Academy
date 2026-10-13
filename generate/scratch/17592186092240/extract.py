import json,uuid,re
from pathlib import Path
H=Path(__file__).resolve().parent;source=json.loads((H/'source.json').read_text());kp=source['record'];byid={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions']}
config={
'q-340942':('2*x**2+1','2{x}^{2}+1','2','9','(2,9)',1,1,['1','2','3','4'],'polynomial-plus'),
'q-342163':('4*x-x**3','4x-{x}^{3}','1','3','(1,3)',1,1,['1'],'polynomial-plus'),
'q-340945':('8/x**2',r'\frac{8}{{x}^{2}}','2','2','(2,2)',1,-1,['1','2','3','4'],'reciprocal-minus'),
'q-342162':('6*x**2-7*x+4','6{x}^{2}-7x+4','0','4','(0,4)',1,-1,['0'],'polynomial-minus'),
'q-342168':('x**6/8-7*x**3/4',r'\frac{1}{8}{x}^{6}-\frac{7}{4}{x}^{3}','2','-6','(2,-6)',1,1,['2','3','4'],'polynomial-plus'),
'q-342190':('3*x**(1/3)/2',r'\frac{3}{2}\sqrt[3]{x}',r'\frac{1}{8}',r'\frac{3}{4}',r'(\frac{1}{8},\frac{3}{4})',8,1,['1/8','1','8'],'radical-scaled-plus')}
profiles={}
for sid,(expr,el,pt,yl,pair,L,sign,pts,t) in config.items():
 profiles[sid]={'expression':expr,'expression_latex':el,'point': '1/8' if sid=='q-342190' else pt,'point_latex':pt,'y_latex':yl,'point_pair':pair,'x_coefficient':L,'sign':sign,'points':pts,'template':t,'prompt':byid[sid][':question/problem']}
c={'kp':17592186092240,'kp_uuid':kp[':knowledge-point/id'],'title':kp.get(':knowledge-point/title','Finding Equations of Normal Lines'),'basis':source['basis'],'lineage':source['lineage'],'generator_id':str(uuid.uuid5(uuid.UUID(kp[':knowledge-point/id']),'normal-line-generator')),'profiles':profiles}
(H/'contract.json').write_text(json.dumps(c,indent=2))
