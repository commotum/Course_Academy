import json,re,sys,subprocess,shutil,hashlib,runpy
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];M=runpy.run_path(str(H/'cross_math_review.py'));expected=M['expected'];vector=M['vector'];response=M['response'];unfont=M['unfont'];rows=[];records=[];fixtures=[];render=[]
S=json.loads((H/'current.json').read_text());packages=[]
for kp,g in S['generators']:
 path=Path('/media/jake/SSD/EDB/math')/g[':question-generator/script'];manifest=json.loads((path.parent/'generator-package.json').read_text());assert all(hashlib.sha256((path.parent/f).read_bytes()).hexdigest()==v['sha256']for f,v in manifest['files'].items());rel=H/'generator-readonly-copies'/path.parent.name;rel.mkdir(parents=True,exist_ok=True)
 for f in manifest['files']:shutil.copyfile(path.parent/f,rel/f)
 shutil.copyfile(path.parent/'generator-package.json',rel/'generator-package.json');package={'kp':kp,'registered_generator':g[':db/id'],'script':str(path),'manifest':manifest,'bands':[]}
 for band in['easy','moderate','hard','unclassified']:
  for seed in[17,101]:
   cmd=[str(R/'.venv/bin/python'),str(path),'--difficulty',band,'--count','32','--seed',str(seed)];out=subprocess.run(cmd,check=True,capture_output=True,text=True);rs=json.loads(out.stdout);assert len(rs)==32
   if seed==17:
    relocated=subprocess.run([str(R/'.venv/bin/python'),str(rel/path.name),'--difficulty',band,'--count','32','--seed',str(seed)],check=True,capture_output=True,text=True);assert json.loads(relocated.stdout)==rs
   for i,rec in enumerate(rs):
    q=rec['question'];ans,terms=expected(q);values={};checks=[]
    for j,f in enumerate(q[':question/answer-fields']):
     right=f[':answer-field/correct'][1];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==right);values[f[':answer-field/key']]=a[':answer/value']
     if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':j,'submitted':a[':answer/value'],'expected':'accepted','purpose':'Generator canonical accepted'},{'field_index':j,'submitted':'987654321','expected':'rejected','purpose':'Generator wrong value rejected'}])
     else:checks.extend({'field_index':j,'submitted_answer_id':b[':answer/id'],'expected':'accepted'if b[':answer/id']==right else'rejected','purpose':'Every generated option checked'}for b in f[':answer-field/choices'])
    if'selection'in values:
     qualified=[a[':answer/id']for a in q[':question/answer-fields'][0][':answer-field/choices']if vector(a[':answer/value'])==ans];assert qualified==[q[':question/answer-fields'][0][':answer-field/correct'][1]]
    else:assert vector(unfont(response(q,values)).rsplit('=',1)[-1])==ans
    assert r'\times'in q[':question/problem'];assert all(len(t['value'])==3 for t in terms)
    label=f'{kp}-{band}-{seed}-{i}';fixtures.append({'label':label,'record':rec,'checks':checks});records.append(rec);rows.append({'label':label,'expected':list(ans),'ordered_terms':terms,'rank':'3-component cross product','native_checks':len(checks)})
    for a in[':question/problem',':question/worked-solution']:render.append({'entity':label,'attribute':a[1:],'value':q[a]})
    for f in q[':question/answer-fields']:
     for a in f[':answer-field/choices']:render.append({'entity':a[':answer/id'],'attribute':'answer/value','value':a[':answer/value'],'bare_math':a[':answer/type']==':answer.type/math'})
   package['bands'].append({'band':band,'seed':seed,'count':32,'relocated_identical':seed==17})
 packages.append(package)
for name,data in [('generator-verification',{'passed':True,'packages':packages,'checks':rows,'defects':[],'successors_staged':False,'database_writes':0}),('generator-records',records),('generator-grading-input',fixtures),('generator-render-input',render)]: (H/(name+'.json')).write_text(json.dumps(data,default=str,indent=2)+'\n')
print('Verified',len(rows),'generator records; all bands, two seeds and relocated copies; no successors needed')
