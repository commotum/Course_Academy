import json,re
from pathlib import Path
D=Path(__file__).parent
src=json.loads((D/'source.json').read_text())
Q=src['record'][':knowledge-point/questions']
# Original expressions are complete template components, not fitted error recipes.
families=[('quadratic_ratio','x**2/2','y/x','0','2',3),('exponential_cancel','exp(x)','5*y*exp(-x)','0','E',1),('cubic_product','x**3','x*y','0','2',2),('reciprocal_product','1/x','2*x**3*y','1','2',3),('linear_exponential','5*x+2','y*exp(x)','0','1',2),('linear_difference','2-x/2','x**3-2*y','0','2',4),('exponential_cosine','2*exp(x)','y*cos(x)','0','2',1),('quadratic_sine','2*x**2','y*sin(x)','1','3',0),('log_exponential','log(x)','2*x**2*exp(y)','1','2*E',2)]
endpoints={'quadratic_ratio':['(0, 0)','(2, 2)'],'cubic_product':['(0,0)','(2,8)'],'reciprocal_product':['(1,1)',r'(2,\frac{1}{2})'],'quadratic_sine':['(1,2)','(3,18)']}
records={};cases=[]
for q,(name,g,f,a,b,correct) in zip(Q,families):
 lo={'0':'0','1':'1'}[a];hi={'2':'2','E':'e','1':'1','3':'3','2*E':'2e'}[b]
 def mask(s):
  s=s.replace('_{'+lo+'}^{'+hi+'}','_{@A@}^{@B@}')
  s=s.replace(lo+r'\le t\le '+hi,r'@A@\le t\le @B@').replace(lo+r'\le x\le '+hi,r'@A@\le x\le @B@')
  return s
 prompt=q[':question/problem']
 if name in endpoints:
  prompt=prompt.replace(endpoints[name][0],'@POINT_A@').replace(endpoints[name][1],'@POINT_B@')
 # smallest presentation repair of the legacy curve subscript
 prompt=prompt.replace(r'\int_(C)',r'\int_{C}')
 records[name]={'curve':g,'scalar':f,'prompt_mask':mask(prompt),'solution_mask':mask(q.get(':question/worked-solution','')),'bank_masks':[mask(c[':answer/value']) for c in q[':question/answer-fields'][0][':answer-field/choices']], 'correct_index':correct,'source_id':q[':question/id'],'source_ma_id':q[':question/math-academy-id'],'endpoint_masks':endpoints.get(name),'original_bounds':[a,b],'observed_label':'easy' if ':question/difficulty' in q else None}
 cases.append({'source_id':q[':question/id'],'source_ma_id':q[':question/math-academy-id'],'template':name,'level':'easy','parameters':{'a':a,'b':b},'bank_profile':'observed_evidence','missing_correct_designation':':answer-field/correct' not in q[':question/answer-fields'][0]})
(D/'observed-templates.json').write_text(json.dumps(records,indent=2)+'\n')
(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
