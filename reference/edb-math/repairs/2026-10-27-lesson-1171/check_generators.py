import copy,importlib.util,json,random,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];ns={'__file__':str(H/'audit_math.py')};exec(compile((H/'audit_math.py').read_text().split('for q in Q:')[0],str(H/'audit_math.py'),'exec'),ns);mat,grids,same,scalar=ns['mat'],ns['grids'],ns['same'],ns['scalar'];S=ns['S'];allrecords=[];summary=[];replays=[]
for c in json.loads((H/'generator-candidates.json').read_text()):
 directory=Path(c['directory']);count=18 if c['kp']==17592186100875 else 24
 for level in ['easy','moderate','hard']:
  out=subprocess.run([sys.executable,str(directory/'generator.py'),'--difficulty',level,'--count',str(count),'--seed','117127'],capture_output=True,text=True,check=True);records=json.loads(out.stdout);allrecords.extend(records);summary.append({'kp':c['kp'],'level':level,'count':len(records)})
 cases=json.loads((directory/'source_cases.json').read_text());cases=cases if isinstance(cases,list)else cases['questions']
 for q in cases:
  source=q.get(':question/math-academy-id')
  if not source:continue
  out=subprocess.run([sys.executable,str(directory/'generator.py'),'--replay',source],capture_output=True,text=True)
  if out.returncode:raise RuntimeError((c['kp'],source,out.stderr))
  records=json.loads(out.stdout);allrecords.extend(records);replays.append({'kp':c['kp'],'source':source,'count':len(records)})
checks=[]
for record in allrecords:
 q=record['question'];p=q[':question/problem'];gs=grids(p);ms=list(map(mat,gs));expected=ms[0]
 for m in ms[1:2 if 'student claims'in p else len(ms)]:expected=expected*m
 fs=q[':question/answer-fields'];bank={a[':answer/id']:a for f in fs for a in f[':answer-field/choices']}
 if fs[0][':answer-field/type']==':answer-field.type/blank':
  assert 'matrix-answer-brackets'in p and not re.search(r'(?m)^\|',p);bykey={f[':answer-field/key']:f for f in fs};keys=re.findall(r'\{\{([^{}]+)\}\}',p);assert len(keys)==expected.rows*expected.cols==len(fs)
  for key,v in zip(keys,list(expected)):
   f=bykey[key];right=bank[f[':answer-field/correct'][1]];assert S.simplify(scalar(right[':answer/value'])-v)==0
 else:
  f=fs[0];right=bank[f[':answer-field/correct'][1]];ag=grids(right[':answer/value'])
  if ag:assert len(ag)==1 and same(mat(ag[0]),expected)
  elif 'student claims'in p:
   target=re.search(r'row (\d+), column (\d+)',p)
   if target:
    expr=re.findall(r'\$([^$]+)\$',right[':answer/value'])[-1];lhs,rhs=expr.rsplit('=',1);assert S.simplify(scalar(lhs)-scalar(rhs))==0 and S.simplify(scalar(rhs)-expected[int(target[1])-1,int(target[2])-1])==0
  else:raise AssertionError('Unexpected nonmatrix answer')
 q=copy.deepcopy(q);tests=[]
 for i,f in enumerate(q[':question/answer-fields']):
  cid=f[':answer-field/correct'][1];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==cid)
  if f[':answer-field/type']==':answer-field.type/blank':tests.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Generated exact entry accepted'},{'field_index':i,'submitted':'987654321','expected':'rejected','purpose':'Incorrect entry rejected'}])
  else:tests.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==cid else'rejected','purpose':'Generated choice identity checked'}for a in f[':answer-field/choices'])
 checks.append({'label':q[':question/id'],'record':{**record,'question':q},'checks':tests})
(H/'generator-validation-records.json').write_text(json.dumps(allrecords,indent=2)+'\n');(H/'generator-grading-input.json').write_text(json.dumps(checks,indent=2)+'\n');subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'generator-grading-input.json'),str(H/'generator-grading.json')],check=True);report={'passed':True,'fresh_samples':sum(d['count']for d in summary),'source_replays':len(replays),'levels':summary,'replay_cases':replays,'records':len(allrecords)};(H/'generator-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('Validated',len(allrecords),'records:',report['fresh_samples'],'new samples and',len(replays),'source replays; product, layout and native grading pass.')
