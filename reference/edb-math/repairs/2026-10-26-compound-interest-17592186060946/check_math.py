import copy,json,math,re,sys
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH
qs=json.loads((H/'repaired-questions.json').read_text());originals={17592186059595:(20500*math.exp(-.052*14),0),17592186059596:(math.log(7210/4350)/9*100,1),17592186059597:(13500*math.exp(-.06*10),0),17592186060056:(math.log(10/102)/-.095,0),17592186060057:(math.log(781/10)/14*100,0),17592186060058:(4120*math.exp(-.0381*7),0),17592186060059:(9830*math.exp(-.18*14),0),17592186060238:(16700*math.exp(-.15*5),0),17592186060389:(3.11*math.exp(.05),2)}
report=[];native=[]
def numeric(v):
 cleaned=v.replace(r'\,','').replace(r'\hspace{0.167em}','');numbers=re.findall(r'-?\d+(?:\.\d+)?',cleaned);assert len(numbers)==1,(v,numbers);return Decimal(numbers[0])
for q in qs:
 e=q[':db/id'];p=q[':question/problem'];places=0
 if e in originals:raw,places=originals[e]
 else:
  vals=[]
  for m in MATH.finditer(p):
   try:vals.append(float(numeric(m[0])))
   except AssertionError:pass
  if 'forex'in p.lower():pct,current,t=vals;rate=pct/100*(-1 if 'decreasing'in p else 1);raw=current*math.exp(-rate*t)
  elif 'gas price'in p:current,pct,t=vals;rate=pct/100*(-1 if 'decreasing'in p else 1);raw=current*math.exp(-rate*t);places=2
  elif 'biology class'in p:initial,t,final=vals;raw=math.log(final/initial)/t*100
  elif 'koalas'in p:initial,pct,final=vals;raw=math.log(final/initial)/(-pct/100)
  elif 'crimes'in p:year,initial,pct,end=vals;raw=initial*math.exp(-pct/100*(end-year))
  elif 'plague'in p:initial,pct,weeks=vals;raw=initial*math.exp(-pct/100*weeks*7)
  else:raise ValueError((e,'unknown context',vals))
 expected=Decimal(str(raw)).quantize(Decimal(1).scaleb(-places),rounding=ROUND_HALF_UP);entry={'entity':e,'raw_computed':raw,'rounding_places':places,'expected':str(expected),'fields':[]};q=copy.deepcopy(q);checks=[]
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  matching=[a for a in f[':answer-field/choices']if numeric(a[':answer/value'])==expected];assert len(matching)==1,(e,expected,matching);assert f[':answer-field/correct'][':db/id']==matching[0][':db/id'];entry['fields'].append({'field':f[':db/id'],'correct':matching[0][':db/id'],'value':matching[0][':answer/value']});correct=f[':answer-field/correct'][':answer/id'];f[':answer-field/correct']=[':answer/id',correct];checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'Every complete radio choice'}for a in f[':answer-field/choices'])
 report.append(entry)
 if checks:native.append({'label':str(e),'record':{'question':q,'knowledge_point':{'title':'Continuous compounding'},'generation':{'template':'lesson-quality-pass'}},'checks':checks})
(H/'independent-math.json').write_text(json.dumps(report,indent=2)+'\n');(H/'native-grading-input.json').write_text(json.dumps(native,indent=2)+'\n');print('Computed and checked',len(report),'questions/examples;',len(native),'practice banks')
