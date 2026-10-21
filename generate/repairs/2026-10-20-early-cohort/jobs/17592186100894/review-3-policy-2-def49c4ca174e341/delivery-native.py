from auditlib import *

cmd=[sys.executable,str(ROOT/'generate/pipeline/check_delivery.py'),'--input',str(E/'sine-current-records.json'),'--source',str(JOB/'source/source.json'),'--inventory',str(JOB/'source/inventory.json'),'--difficulty','easy','--output',str(E/'delivery-sine'),'--asset-root',str(E),'--math-root','/media/jake/SSD/EDB/math']
p=subprocess.run(cmd,capture_output=True,text=True);(E/'delivery-sine-console.txt').write_text(p.stdout+p.stderr)
assert p.returncode==0,p.stdout+p.stderr
raw=json.load(open(E/'sine-current-records.json'));acc=json.load(open(E/'delivery-sine/accepted.json'));assert len(raw)==len(acc)
rs=[]
for name in ['easy','moderate','batch','sine']:rs+=json.load(open(E/('delivery-'+name+'/accepted.json')))
cases=[];batch_probes=[]
for i,r in enumerate(rs):
    f=field(r);mid=r['generation']['template']
    if f[':answer-field/type'].endswith('/radio'):
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
    else:
        checks=[{'submitted':correct(r),'expected':'accepted'},{'submitted':'0','expected':'rejected'}]
        if mid=='q-126765':
            v=expr(correct(r));checks.extend([{'submitted':str(S.expand(v-v.subs(x,0))).replace('**','^'),'expected':'accepted'}, {'submitted':'('+correct(r)+')+1','expected':'accepted'}, {'submitted':'2*('+correct(r)+')','expected':'rejected'}])
        else:
            _,(_,ordinate)=prompt_data(r)
            checks.append({'submitted':str(ordinate).replace('**','^').replace('log(','ln(').replace('E','e'),'expected':'rejected','purpose':'Copy IC without integrating'})
    cases.append({'label':'delivered '+str(i)+' '+mid,'record':r,'checks':checks})
save('delivered-current-grader-input.json',cases)
grade=[str(ROOT/'generate/runs/current/check-engine'),str(E/'delivered-current-grader-input.json'),str(E/'delivered-current-grader-report.json')]
p=subprocess.run(grade,capture_output=True,text=True);(E/'delivered-current-grader-console.txt').write_text(p.stdout+p.stderr)
save('delivered-current-execution.json',{'commands':[cmd,grade],'exit':p.returncode,'raw_sine':len(raw),'delivered_sine':len(acc),'checks':sum(len(c['checks']) for c in cases),'stdout':p.stdout,'stderr':p.stderr})
assert p.returncode==0,p.stdout+p.stderr
batch=json.load(open(E/'delivery-batch/accepted.json'))
save('batch-shortcut-results.json',{'records':len(batch),'zero_strategy':{'correct':0,'total':len(batch)},'copy_initial_ordinate':{'correct':0,'total':sum(r['generation']['template']!='q-126765' for r in batch)},'key_strategy':{'correct':len(batch),'total':len(batch)},'evidence':'delivered-current-grader-report.json','templates':[r['generation']['template'] for r in batch],'sine_constant_shift':'Both exact previous equivalents accepted; derivative-distinct fragment rejected.'})
print(p.stdout.strip())
