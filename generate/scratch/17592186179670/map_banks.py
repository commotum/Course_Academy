import importlib.util,json
from pathlib import Path
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
F={
'q-39954':['c*speed','correct','3*c*speed/8','c*speed/3','5*c/2'],
'q-76565':['sqrt(a^2+c^2)','correct=0','c*a','2*c*a^2','sqrt(c*a)'],
'q-123363':['a+1','unweighted_integral-7/6','a+2*sqrt(k*dy)','correct-1','correct'],
'q-123366':['dy*e^slope-1','dy*(e^(2*slope)-1)','dy*(e^slope-1)','correct','speed*(e^(2*slope)-1)/slope'],
'q-76564':['2*correct','correct','correct/dy','speed/2','dy*sqrt(dx)/2'],
'q-76605':['correct','tan(slope)/slope','speed*slope*tan(slope)','slope*tan(slope)','speed*tan(slope)/pi'],
'q-76650':['speed*e^(q0+1)*(e^(q1-q0-1)-1)','e^q1-e^q0','correct','correct/2','dx*(e^q1-e^q0)']}
rows=[]
for q in json.load(open(P/'source.json'))['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id'];lev,f,p=g.ANCHORS[sid];z=g.instance(f,p);values,_=g.source_bank(sid,p,z);ff=q[':question/answer-fields'][0]
 bank=[]
 for i,a in enumerate(ff[':answer-field/choices']):
  bank.append({'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'formula':F[sid][i],'derived_anchor_value':g.tex(values[i]),'semantic_correct_by_independent_integral':g.equivalent(values[i],z['answer']),'source_designated_correct':a[':answer/id']==ff.get(':answer-field/correct',{}).get(':answer/id') if ':answer-field/correct' in ff else None,'interpretation':'Empirical source expression pattern only; original author intent underdetermined. Offsets/scales preserve evidence and are not default distractor operations.'})
 rows.append({'source_id':sid,'source_question_id':q[':question/id'],'source_field_id':ff[':answer-field/id'],'template':f,'profile':'source:'+sid,'parameters':p,'eligible_for_learning':False,'evidence_only':True,'complete_bank':bank,'raw_correct_attribute_present':':answer-field/correct' in ff})
(P/'bank-mapping.json').write_text(json.dumps({'basis':2275,'lineage':g.SOURCE['lineage'],'definitions':{'speed':'sqrt(dx^2+dy^2)','slope':'c*dx+d*dy (exponential), pi*(dy-dx)/n (secant)','q0':'a*b','q1':'(a+dx)*(b+dy)','correct':'speed*(primitive(1)-primitive(0)), derived before bank'},'banks':rows},indent=2)+'\n')
