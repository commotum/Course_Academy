from review import *
cases=[];issues=[]
records=sum([json.load(open('delivery-'+lv+'/accepted.json')) for lv in ['easy','moderate','hard','batch']],[])
for i,r in enumerate(records):
 _,v=expected(r);f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if eq(parse(a[':answer/value']),v) else 'rejected','purpose':'independently checked delivered choice'} for a in f[':answer-field/choices']]
 else:
  checks=[{'submitted':s.latex(v).replace(r'\log',r'\ln'),'expected':'accepted','purpose':'independent delivered expression'}, {'submitted':r'\frac{2('+s.latex(v).replace(r'\log',r'\ln')+r')}{2}','expected':'accepted','purpose':'equivalent rescaling'}, {'submitted':s.latex(-v).replace(r'\log',r'\ln'),'expected':'rejected','purpose':'wrong sign'}, {'submitted':'0','expected':'rejected','purpose':'zero wrong'}]
 cases.append({'label':'delivered-'+str(i),'record':r,'checks':checks})
save('post-delivery-grader-desired.json',cases)
for c in cases:
 oldlogs={str(a.args[0]) for a in parse(key(c['record'])[':answer/value']).atoms(s.log)}
 for ch in c['checks']:
  if 'submitted' in ch and ch['expected']=='accepted':
   logs={str(a.args[0]) for a in parse(ch['submitted']).atoms(s.log)}
   if oldlogs and logs and oldlogs!=logs:issues.append({'label':c['label'],'desired':'accepted','check':dict(ch),'record_id':c['record']['question'][':question/id']});ch.update(expected='unresolved',purpose=ch['purpose']+'; demonstrated log-power identity defect, desired accepted')
save('post-delivery-grader-observed.json',cases);save('post-delivery-grading-issues.json',issues)
cmd=[str(ROOT/'generate/runs/current/check-engine'),str(E/'post-delivery-grader-observed.json'),str(E/'post-delivery-grading.json')];r=subprocess.run(cmd,capture_output=True,text=True);(E/'post-delivery-grading.log').write_text(json.dumps(cmd)+'\n'+r.stdout+r.stderr);print(r.returncode,r.stdout,r.stderr[:1000])
# Add the exact accepted delivery form to targeted differential.
failure=next(r for r in records if r['generation']['seed']==782006 and r['generation']['template']=='q-312462');cases=json.load(open('grading-failure-input.json'));z={'label':'after delivery equivalent','record':failure,'checks':cases[0]['checks']};cases.append(z);save('grading-failure-input.json',cases)
cmd=[str(ROOT/'generate/runs/current/check-engine'),str(E/'grading-failure-input.json'),str(E/'grading-failure.json')];r=subprocess.run(cmd,capture_output=True,text=True);(E/'grading-failure.log').write_text(json.dumps(cmd)+'\n'+r.stdout+r.stderr);print(r.returncode,r.stdout,r.stderr[:1000])
