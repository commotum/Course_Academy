import json,sys,subprocess,shutil,tempfile,re,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from math_tools import *
from generator_publish import Publisher,normalized_question,answer_id,enum
from generate.pipeline.check_delivery import audit
from scripts.generator_evidence import record_sha256
read=lambda p:json.loads(Path(p).read_text())
def save(p,v):p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,default=str)+'\n')
publisher=Publisher.from_environment();M=publisher.config.math_root
allcases=[];representatives=[];ledger=[];coverage=[]
for kp in [17592186092240,17592186092384,17592186092385]:
 D=H/str(kp);K=read(D/'kp.json');source=read(D/'source/source.json');inventory=read(D/'inventory/inventory.json');excluded={r[':db/id'] for r in source['material']['source_eligibility']['excluded_questions']}
 for q in K[':knowledge-point/questions']:
  row=dict(entity=q[':db/id'],imported=bool(q.get(':question/math-academy-id')),ma_id=q.get(':question/math-academy-id'),retired=q.get(':question/retired',False),excluded=q[':db/id'] in excluded,missing=[])
  fields=q.get(':question/answer-fields',[])
  if not fields:row['missing'].append('answer-fields')
  if not q.get(':question/worked-solution'):row['missing'].append('worked-solution')
  for f in fields:
   if not f.get(':answer-field/choices'):row['missing'].append(f[':answer-field/key']+':choices')
   if not f.get(':answer-field/correct'):row['missing'].append(f[':answer-field/key']+':correct')
  if row['excluded']:row['math_status']='context-dependent excluded multistep part';ledger.append(row);continue
  try:
   f,x,y,m,n,b=extract(q);row.update(function=str(f),point=[str(x),str(y)],tangent=str(m),normal=str(n),intercept=str(b));expected={}
   if kp==17592186092384:expected={field[':answer-field/key']:n for field in fields}
   elif kp==17592186092385:
    axis='x' if '$x$-axis' in q[':question/problem'] else 'y';xy=[s.simplify(-b/n),s.Integer(0)] if axis=='x' else [s.Integer(0),b];row['axis']=axis
    expected={field[':answer-field/key']:(xy if enum(field[':answer-field/type'])==':answer-field.type/radio' else xy[int(field[':answer-field/key'].split('-')[-1])-1]) for field in fields}
   else:
    keys={field[':answer-field/key'] for field in fields};problem=q[':question/problem']
    if keys=={'slope','intercept'}:expected={'slope':n,'intercept':b}
    elif keys=={'coefficient','constant'}:expected={'coefficient':m,'constant':s.simplify(x+m*y)}
    elif len(fields)==2:
     # Imported equations can fix the sign/scaling of their y coefficient.
     if '$8x' in problem:expected={'field-1':8*m,'field-2':8*(x+m*y)}
     else:
      sign=-1 if re.search(r'\$x\\\\?\s*,-|\$x\\,-',problem) or '$x\\,-$' in problem else 1
      expected={'field-1':sign*m,'field-2':x+m*y}
    elif len(fields)==1:
     coef=n if '$y=ax+b$' in problem else m;constant=b if '$y=ax+b$' in problem else x+m*y
     expr=re.search(r'values? of \$([^$]+)\$',problem);target=expr[1].rstrip('.')
     terms={'a':coef,'b':constant,'p':coef,'q':constant};expected={fields[0][':answer-field/key']:s.sympify(target,locals=terms)}
   failures=[]
   for field in fields:
    if not field.get(':answer-field/correct'):continue
    value=key_value(field);wanted=expected[field[':answer-field/key']]
    observed=tuple_tex(value) if isinstance(wanted,list) else parse(value)
    equal=all(s.simplify(a-b)==0 for a,b in zip(observed,wanted)) if isinstance(wanted,list) else s.simplify(observed-wanted)==0
    if not equal:failures.append(dict(field=field[':answer-field/key'],expected=str(wanted),actual=value))
   row['math_status']='wrong-key' if failures else 'passed';row['failures']=failures
  except Exception as err:row['math_status']='needs-manual-review';row['reason']=str(err)
  ledger.append(row)
 if kp==17592186092240:continue
 script=K[':knowledge-point/question-generator'][':question-generator/script'];package=M/Path(script).parent;manifest=read(package/'generator-package.json')
 with tempfile.TemporaryDirectory(prefix='normal-lesson-audit-',dir='/tmp') as tmp:
  T=Path(tmp)
  for name in manifest['files']:shutil.copy2(package/name,T/name)
  for band in ['easy','moderate','hard']:
   records=json.loads(subprocess.check_output([sys.executable,str(T/'generator.py'),'--difficulty',band,'--count','20','--seed','202611111'],cwd=T,timeout=120));save(D/'samples'/f'{band}.json',records)
   delivery=audit(records,inventory,source,band,D/'delivery'/band,T,M);accepted=read(D/'delivery'/band/'accepted.json');coverage.append(dict(kp=kp,band=band,sampled=len(records),delivered=len(accepted),seed=202611111))
   seen=set()
   for r in accepted:
    q=r['question'];f,x,y,m,n,b=extract(q);fields=q[':question/answer-fields'];checks=[]
    for i,field in enumerate(fields):
     wanted=n if kp==17592186092384 else ([s.simplify(-b/n),s.Integer(0)] if '$x$-axis' in q[':question/problem'] else [s.Integer(0),b])[int(field[':answer-field/key'].split('-')[-1])-1]
     observed=parse(key_value(field));assert s.simplify(observed-wanted)==0,(q,wanted,observed)
     checks += [dict(field_index=i,submitted=s.sstr(wanted),expected='accepted',control='equivalent',purpose='Independent derivative and normal-line calculation in rational notation'),dict(field_index=i,submitted=s.sstr(wanted+1),expected='rejected',control='wrong',purpose='Adding one changes the unique normal slope or coordinate')]
    allcases.append(dict(label=f'{kp}-{band}',record=r,checks=checks))
    family=r['generation']['template'];axis=r['generation'].get('parameters',{}).get('axis');case=(family,axis)
    if case not in seen:representatives.append(r);seen.add(case)
 # Read-only source replays from disposable copy; inspect content separately.
 with tempfile.TemporaryDirectory(prefix='normal-replay-audit-',dir='/tmp') as tmp:
  T=Path(tmp)
  for name in manifest['files']:shutil.copy2(package/name,T/name)
  replay=json.loads(subprocess.check_output([sys.executable,str(T/'generator.py'),'--replay-sources'],cwd=T,timeout=120));save(D/'source-replays.json',replay)
save(H/'stored-ledger.json',ledger);save(H/'coverage.json',coverage);save(H/'native-input.json',allcases);save(H/'render-input.json',representatives)
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'native-input.json'),str(H/'native-report.json')],check=True)
print('Coverage',coverage);print('Stored manual/wrong',[(r['entity'],r.get('reason',r.get('failures'))) for r in ledger if r['math_status'] not in ['passed','context-dependent excluded multistep part']]);print('Render reps',len(representatives))
