import audit as a
import json,subprocess,sys
E=a.E;inv=json.load(open(a.B/'source/inventory.json'));findings=json.load(open(E/'inventory-results.json'));records=[]
for f in findings:
 if f['reconstruction']:
  m=f['reconstruction'][0];p=m['parameters'];r=a.g.generate(seed=600021,template=m['template'],parameters={'answer_role':p['answer_role'],'translation':list(map(int,p['translation']))});records.append(r)
a.save('inventory-reconstruction-raw.json',records)
empty={**inv,'questions':[],'fingerprints':[]};a.save('normalization-only-inventory.json',empty)
cmd=[sys.executable,str(a.R/'generate/pipeline/check_delivery.py'),'--input',str(E/'inventory-reconstruction-raw.json'),'--source',str(a.B/'source/source.json'),'--inventory',str(E/'normalization-only-inventory.json'),'--difficulty','moderate','--output',str(E/'inventory-normalized'),'--math-root','/media/jake/SSD/EDB/math']
p=subprocess.run(cmd,capture_output=True,text=True)
a.save('inventory-reproduction-command.json',{'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'purpose':'Normalize candidate reconstructions to publication content IDs only; empty inventory is used deliberately so existing records are retained in this offline evidence output. Real captured inventory still governs all delivery checks.'})
if p.returncode:raise RuntimeError(p.stderr)
rr=json.load(open(E/'inventory-normalized/accepted.json'));byid={r['question'][':question/id']:r for r in rr};stored={q[':question/id']:q for q in inv['questions']};matches=[]
for r in rr:
 q=r['question'];sid=q[':question/id'];orig=stored.get(sid)
 matches.append({'reproduced_id':sid,'matched_captured_question':orig is not None,'metadata':r['generation'],'all_bank_values_equal':orig is not None and sorted(c[':answer/value'] for c in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(c[':answer/value'] for c in orig[':question/answer-fields'][0][':answer-field/choices']),'prompt_equal':orig is not None and q[':question/problem']==orig[':question/problem'],'worked_equal':orig is not None and q[':question/worked-solution']==orig[':question/worked-solution']})
a.save('generated-records.json',rr);a.save('inventory-reproduction-results.json',matches)
print(json.dumps({'normalization_returncode':p.returncode,'count':len(rr),'matched_ids':sum(m['matched_captured_question'] for m in matches)}))
