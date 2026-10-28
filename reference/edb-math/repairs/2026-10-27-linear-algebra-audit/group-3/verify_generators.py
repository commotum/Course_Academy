import copy,hashlib,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.path.insert(0,'scripts');from question_capture.math_format import validate_generated_record,ENV,environment,cells
H=Path(__file__).resolve().parent;R=Path.cwd();D=json.loads((H/'generator-samples.json').read_text());staged=json.loads((H/'staged-generator-samples.json').read_text());allrecords=[r['record']for r in D]+staged;out=[]
for i,record in enumerate(allrecords):
 validate_generated_record(record);r=copy.deepcopy(record);checks=[]
 for j,f in enumerate(r['question'][':question/answer-fields']):
  f[':answer-field/type']=f[':answer-field/type'].get(':db/ident')if isinstance(f[':answer-field/type'],dict)else f[':answer-field/type']
  for av in f[':answer-field/choices']:av[':answer/type']=av[':answer/type'].get(':db/ident')if isinstance(av[':answer/type'],dict)else av[':answer/type']
  if isinstance(f[':answer-field/correct'],dict):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  right=f[':answer-field/correct'][1];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==right)
  if f[':answer-field/type']==':answer-field.type/blank':checks.extend([{'field_index':j,'submitted':a[':answer/value'],'expected':'accepted'},{'field_index':j,'submitted':'987654321','expected':'rejected'}])
  else:checks.extend({'field_index':j,'submitted_answer_id':a2[':answer/id'],'expected':'accepted'if a2[':answer/id']==right else'rejected'}for a2 in f[':answer-field/choices'])
 out.append({'label':'generated-'+str(i),'record':r,'checks':checks})
for record in staged:
 g=record['generation'];p=g['parameters'];expected=(sp.Matrix(p['A'])*sp.Matrix(p['B']))[p['row']-1,p['column']-1];f=record['question'][':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert sp.Integer(a[':answer/value'])==expected;assert r'\color{lightgray}'in record['question'][':question/worked-solution']
(H/'generator-grading-input.json').write_text(json.dumps(out,indent=2));subprocess.run([str(R/'.local/edb/html-table-repair/check-engine'),str(H/'generator-grading-input.json'),str(H/'generator-grading.json')],check=True)
# Exact source-profile replay compares complete emitted records before and after the display-only change.
row=next(r for r in json.loads((H/'generators.json').read_text())if r[0]==17592186100873);src=Path('/media/jake/SSD/EDB/math')/row[2];dst=H/'generator-17592186100873'/src.name;raw=json.loads((src.parent/'source-data.json').read_text());sids=[q[':question/math-academy-id']for q in raw['record'][':knowledge-point/questions']];replay=[]
for sid in sids:
 args=['--difficulty','easy','--profile','observed:'+sid,'--count','1','--seed','20261027','--format','json'];a=subprocess.run([sys.executable,str(src),*args],capture_output=True,text=True);b=subprocess.run([sys.executable,str(dst),*args],capture_output=True,text=True);assert a.returncode==b.returncode==0,(sid,a.stderr,b.stderr);assert json.loads(a.stdout)==json.loads(b.stdout),sid;replay.append(sid)
(H/'staged-generator-validation.json').write_text(json.dumps({'fresh_current_packages':len(D),'fresh_staged':len(staged),'fresh_staged_math_verified':True,'source_replays_unchanged':replay,'raw_source_data_sha256_unchanged':hashlib.sha256((src.parent/'source-data.json').read_bytes()).hexdigest()==hashlib.sha256((dst.parent/'source-data.json').read_bytes()).hexdigest()},indent=2));print('records',len(out),'source replays',len(replay))
