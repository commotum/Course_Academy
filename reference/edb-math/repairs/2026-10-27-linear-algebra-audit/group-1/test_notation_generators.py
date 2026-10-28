import concurrent.futures,copy,json,os,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,validate_math_structure,validate_math_boundaries
C=json.loads((H/'generator-candidates.json').read_text());out=[];records=[];items=[];checks=[]
def run(c,old):
 path=Path('/media/jake/SSD/EDB/math')/c['old_reference']if old else Path(c['directory'])/c['entrypoint'];r=subprocess.run([sys.executable,str(H/'notation_worker.py'),str(path),str(c['kp'])],text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},timeout=120)
 if r.returncode:raise RuntimeError(str(c['kp'])+' '+str(old)+' '+r.stderr)
 return json.loads(r.stdout)
def canon(value):
 value=re.sub(r'\\(?:mathbf|mathcal)\{([abxB0])\}',r'\1',value);return re.sub(r'\s+|[{}]','',value)
for c in C:
 old=run(c,True);new=run(c,False);oldmap={r['case']:r['record']for r in old};assert set(oldmap)=={r['case']for r in new};report={'kp':c['kp'],'records':len(new),'fresh':sum(r['case'].startswith('fresh-')for r in new),'source_replays':sum(r['case'].startswith('source-')for r in new),'checks':[]}
 for row in new:
  label=row['case'];r=row['record'];q=r['question'];oq=oldmap[label]['question'];assert q[':question/id']!=oq[':question/id'],('identity reused',c['kp'],label)
  # Batch UI position balancing may sample a different second pivot-basis task.
  fixed=not(c['kp']==17592186119857 and label.startswith('fresh-'))
  if fixed:
   for a in [':question/problem',':question/worked-solution']:assert canon(q[a])==canon(oq[a]),(c['kp'],label,a)
   for f,of in zip(q.get(':question/answer-fields',[]),oq.get(':question/answer-fields',[])):
    assert sorted(canon(a[':answer/value'])for a in f[':answer-field/choices'])==sorted(canon(a[':answer/value'])for a in of[':answer-field/choices'])
    right=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);oright=next(a for a in of[':answer-field/choices']if a[':answer/id']==of[':answer-field/correct'][1]);assert canon(right[':answer/value'])==canon(oright[':answer/value'])
  assert r'\mathbf'in q[':question/problem']and r'\mathbf'in q[':question/worked-solution'],(c['kp'],label,'font')
  assert not re.search(r'\\mathbf\{x\}\s*\}?\s*_',q[':question/problem']+q[':question/worked-solution']),('bold scalar component',label)
  if c['kp']==17592186119857:
   assert r'\mathcal{B}'in q[':question/problem']and r'\mathcal{B}'in q[':question/worked-solution']
   assert all(r'\mathcal{B}'in a[':answer/value']and r'\{'in a[':answer/value']and r'\}'in a[':answer/value']for f in q[':question/answer-fields']for a in f[':answer-field/choices'])
  for a in ['question/problem','question/worked-solution']:
   value=q[':'+a];validate_math_structure(value);validate_math_boundaries(value,strict=True);items.append([q[':question/id'],a,value,False])
  recordchecks=[]
  for i,f in enumerate(q.get(':question/answer-fields',[])):
   rightid=f[':answer-field/correct'][1]
   for a in f[':answer-field/choices']:
    bare=a[':answer/type']==':answer.type/math';validate_math_structure(a[':answer/value'],bare_math=bare);items.append([a[':answer/id'],'answer/value',a[':answer/value'],bare]);recordchecks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==rightid else'rejected','purpose':'Notation repair canonical bank/choice identity dispatch'})
  checks.append({'label':str(c['kp'])+'/'+label,'record':r,'checks':recordchecks});records.append({'kp':c['kp'],'case':label,'record':r});report['checks'].append({'case':label,'new_content_identity':True,'mathematical_content_and_bank_equivalent':fixed,'source_vector_fonts_present':True})
 out.append(report);print(c['kp'],'validated',len(new),flush=True)
(H/'notation-generator-records.json').write_text(json.dumps(records,indent=2));(H/'notation-render-items.json').write_text(json.dumps(items,indent=2));(H/'notation-grading-input.json').write_text(json.dumps(checks,indent=2));subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'notation-grading-input.json'),str(H/'notation-grading.json')],check=True);(H/'notation-generator-validation.json').write_text(json.dumps({'passed':True,'packages':out,'records':len(records),'render_items':len(items),'live_database_writes':False},indent=2));print('total',len(records),'render items',len(items))
