"""Exercise current repaired CLIs without publishing questions or learner state."""
import concurrent.futures,os,sys
from read import *
from scripts.generator_policy import checkbox_selection

def records(v):return v.get('records',[v])if isinstance(v,dict)else v

def run(row):
 out=HERE/'samples'/str(row['kp']);out.mkdir(parents=True,exist_ok=True);reports=[]
 prior=json.loads((ROOT/'reference/mathacademy/repairs/2026-10-19-checkbox-nonempty/patched-audit.json').read_text());prior=next(r for r in prior if r['kp']==row['kp'])
 for level in ('easy','moderate','hard'):
  supported=next(r for r in prior['levels']if r['level']==level)
  if row['kp']==17592186147456:
   if level=='hard':reports.append({'level':level,'unsupported':True});continue
   command=[str(ROOT/'.venv/bin/python'),'-B',row['updated_script'],'--difficulty',level,'--seed','37']
  elif row['kp']==17592186119848:
   if level!='easy':reports.append({'level':level,'unsupported':True});continue
   command=[str(ROOT/'.venv/bin/python'),'-B',row['updated_script'],'--difficulty',level,'--count','21','--seed','37','--format','json']
  else:
   if supported.get('unsupported')or 'error'in supported:reports.append({'level':level,'unsupported':True});continue
   command=[str(ROOT/'.venv/bin/python'),'-B',row['updated_script'],'--difficulty',level,'--count','12','--seed','37','--format','json']
  try:
   r=subprocess.run(command,capture_output=True,text=True,cwd=ROOT,env=dict(os.environ,COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(out/'assets')),timeout=120);(out/(level+'.stdout')).write_text(r.stdout);(out/(level+'.stderr')).write_text(r.stderr);r.check_returncode();values=records(json.loads(r.stdout));count=0;none_true=0;evidence=0
   for rec in values:
    selection=checkbox_selection(rec)
    if not selection:continue
    if rec.get('generation',{}).get('eligible_for_learning')is False or rec.get('generation',{}).get('evidence_only'):evidence+=1;continue
    q=rec.get('question',rec);fields=q[':question/answer-fields'];none=[f for f in fields if f.get(':answer-field/key')=='None of the above'];assert len(none)==1
    ordinary=checkbox_selection({':question/answer-fields':[f for f in fields if f is not none[0]]});correct=checkbox_selection({':question/answer-fields':none})[0]
    assert correct==(not any(ordinary))and any(selection)
    assert 'leave all boxes unchecked'not in q[':question/problem']
    assert len({f[':answer-field/id']for f in fields})==len(fields)
    ids=[str(a[':answer/id'])for f in fields for a in f[':answer-field/choices']];assert len(ids)==len(set(ids))
    count+=1;none_true+=correct
   reports.append({'level':level,'records':len(values),'checkbox_records':count,'none_correct':none_true,'evidence_only':evidence,'passed':True})
  except Exception as error:reports.append({'level':level,'error':str(error),'stderr':(out/(level+'.stderr')).read_text()[-1200:]if(out/(level+'.stderr')).exists()else''})
 result={'kp':row['kp'],'levels':reports,'passed':not any('error'in r for r in reports)};save('samples/'+str(row['kp'])+'/audit.json',result);return result
if __name__=='__main__':
 rows=json.loads((HERE/'patched.json').read_text());reports=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:
  for f in concurrent.futures.as_completed([ex.submit(run,r)for r in rows]):
   r=f.result();reports.append(r);save('cli-audit.json',sorted(reports,key=lambda r:r['kp']));print(json.dumps({'completed':len(reports),'kp':r['kp'],'passed':r['passed'],'errors':[v for v in r['levels']if'error'in v]}),flush=True)
 assert all(r['passed']for r in reports)
