"""Rerun affected checks after sign-aware hard solution formatting."""
import json
import validate_repair as a
count=0
for name in ('records.json','controlled-bank-records.json','render-records.json'):
 rs=json.loads((a.E/name).read_text())
 for i,r in enumerate(rs):
  d=r['generation']
  if d['template']=='q-16401':
   rr=a.g.generate(d['difficulty'],d['seed'],d['template'],parameters=d['parameters'],decision=d['decision']);assert a.math.check(rr)['passed'];rs[i]=rr;count+=1
 a.save(name,rs)
rs=json.loads((a.E/'records.json').read_text());out=json.loads((a.E/'math-results.json').read_text());cases=[]
for i,r in enumerate(rs):
 if r['generation']['template']=='q-16401':out[i]=a.math.check(r)
 z=out[i];assert z['passed'];cases.append({'label':r['generation']['template']+':'+r['question'][':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':c['choice_id'],'expected':'accepted' if c['standard'] and c['equivalent'] else 'rejected','purpose':'independently parsed displayed standard-form equivalence'} for c in z['choices']]})
a.save('math-results.json',out);a.save('grader-input.json',cases)
cs=[]
for r in json.loads((a.E/'controlled-bank-records.json').read_text()):
 f=r['question'][':question/answer-fields'][0];cs.append({'label':'fixed bank '+r['generation']['template'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/value']==a.key(r) else 'rejected','purpose':'identical complete bank with changed key assignment'} for c in f[':answer-field/choices']]})
a.save('controlled-bank-grader-input.json',cs)
a.save('hard-display-refresh-results.json',{'affected_records_checked':count,'passed':True,'change':'Write signed square and cross-term rows without double minus signs. All earlier easy/source checks retained.'})
print('Affected hard display checks:',count,'passed.')
