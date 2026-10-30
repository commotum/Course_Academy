"""Individually reviewed truth vectors, checked against every owned radio/checkbox option."""
import json,re
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());pm={(p['entity'],p['attribute']):p['after']for p in P}
truths={
'e-5424':'TFF','e-9961':'FTT','q-34834':'FTF','q-34936':'FTF','q-47586':'FTT','q-47599':'FTF','q-141199':'FTT','q-141200':'TTF','q-142358':'FFT','q-142474':'FFT','q-142475':'TFT','q-142476':'FFT','q-35425':'FFT','q-47587':'TFF','q-79334':'FTT','q-139978':'TFT','q-142367':'TFF','q-139977':'TFT','q-79349':'FFT','q-141201':'TFT','q-34929':'TFF','q-141198':'TTF','q-141196':'TFF','q-141215':'FFT','q-142479':'FFT','q-141341':'TFT','q-142472':'FTF','q-141342':'FTF','q-142473':'FTF','q-141205':'TTT','q-141197':'TFF','q-141217':'FTT','q-142478':'FTT','q-47604':'FTF','q-141214':'FTF',
'17592186673117':'FFT','17592186673124':'FTF','17592186673141':'TFF','17592186673148':'TTF','17592186673150':'FFT','17592186673190':'FTT','17592186673201':'FFFT','17592186673204':'TTF','17592186673226':'TFF','17592186673230':'TFT'}
rows=[]
for q in D['questions']:
 sid=q.get(':question/math-academy-id')or str(q[':db/id'])
 if sid not in truths:continue
 ts=[x=='T'for x in truths[sid]];fs=q.get(':question/answer-fields',[]);records=[]
 for i,f in enumerate(fs):
  aid=pm.get((f[':db/id'],'answer-field/correct'),f.get(':answer-field/correct',{}).get(':db/id'));right=next(a for a in f[':answer-field/choices']if a[':db/id']==aid)
  if f[':answer-field/type'][':db/ident'].endswith('checkbox'):
   # None of the above is appended separately; it is true exactly when no substantive statement is true.
   target=(not any(ts))if f[':answer-field/key']=='None of the above'else ts[i];assert(right[':answer/value']=='true')==target,(sid,f)
   records.extend({'answer':a[':db/id'],'value':a[':answer/value'],'mathematically_correct':(a[':answer/value']=='true')==target}for a in f[':answer-field/choices'])
  else:
   expected=[j for j,t in enumerate(ts)if t];correct=[]
   for a in f[':answer-field/choices']:
    inds=[['I','II','III'].index(x)for x in re.findall(r'\b(?:III|II|I)\b',a[':answer/value'])];ok=inds==expected;records.append({'answer':a[':db/id'],'value':a[':answer/value'],'mathematically_correct':ok})
    if ok:correct.append(a[':db/id'])
   assert correct==[aid],(sid,correct,aid)
 rows.append({'entity':q[':db/id'],'identity':sid,'independently_reviewed_truths':ts,'proof':'For square A, invertible iff rank=n iff nullity=0 iff Null(A)={0} iff Col(A)=R^n iff det(A)≠0. A nonzero null vector implies singularity. A parameterized null space has dimension equal to its independent parameter directions. Every finite-dimensional null space has a basis, including the empty basis for {0}. Proper column subspace implies singularity.','bank_checks':records,'passed':True})
(H/'theorem-bank-verification.json').write_text(json.dumps({'passed':True,'questions':len(rows),'checks':rows},indent=2)+'\n');print('Individually reviewed theorem questions',len(rows),'owned option evaluations',sum(len(r['bank_checks'])for r in rows))
