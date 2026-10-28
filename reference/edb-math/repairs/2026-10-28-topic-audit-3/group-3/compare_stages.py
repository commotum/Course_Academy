import concurrent.futures,copy,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
from PIL import Image
sys.path.insert(0,'scripts');from question_capture.math_format import normalize_prose,normalize_tex
H=Path(__file__).resolve().parent;A=json.loads((H/'generator-stage-plan.json').read_text());G={g['kp']:g for g in json.loads((H/'generator-audit.json').read_text())};V=json.loads((H/'generator-validation.json').read_text());work=Path(tempfile.mkdtemp(prefix='ca9837-before-after-'));reports=[];samples=[]
IMAGE=re.compile(r'(?:/[A-Za-z0-9_.~+-]+)+\.(?:png|jpg|jpeg|svg|webp|gif)')
def image_signature(path):
 p=Path(path)
 try:
  with Image.open(p)as im:return 'asset-pixels-sha256:'+hashlib.sha256(str(im.size).encode()+im.convert('RGBA').tobytes()).hexdigest()
 except Exception:return 'asset-sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()
def stable(v):
 if isinstance(v,str):return IMAGE.sub(lambda m:image_signature(m[0])if Path(m[0]).is_file()else m[0],v)
 if isinstance(v,list):return[stable(z)for z in v]
 if isinstance(v,dict):return{k:stable(z)for k,z in v.items()}
 return v
def signature(q):
 out={a:stable(normalize_prose(q[a]))for a in[':question/problem',':question/worked-solution']if a in q};fs=[]
 for f in q.get(':question/answer-fields',[]):
  cid=f.get(':answer-field/correct');cid=cid[1]if isinstance(cid,list)else cid.get(':answer/id')if isinstance(cid,dict)else None;vals=[];correct=None
  for a in f[':answer-field/choices']:
   typ=a[':answer/type'];typ=typ.get(':db/ident')if isinstance(typ,dict)else typ;v=stable(normalize_tex(a[':answer/value'])if typ==':answer.type/math'else normalize_prose(a[':answer/value'])if typ==':answer.type/text'else a[':answer/value']);vals.append((typ,v))
   if a[':answer/id']==cid:correct=(typ,v)
  typ=f[':answer-field/type'];typ=typ.get(':db/ident')if isinstance(typ,dict)else typ;fs.append({'key':normalize_prose(f[':answer-field/key'])if typ==':answer-field.type/checkbox'else f[':answer-field/key'],'type':typ,'values':sorted(vals),'correct':correct})
 out['fields']=fs;return out

def run(g,band):
 kp=g['kp'];base=work/str(kp)/band;old=base/'before';shutil.copytree(Path(g['directory']),old);entry=old/g['entrypoint'];source=Path(G[kp]['script']);text=source.read_text();text=re.sub(r'^sys\.path\.insert\(0,str\((?:Path\(__file__\)\.resolve\(\)\.parents\[2\]|HERE\.parents\[2\])\s*/\s*["\']scripts/question_capture["\']\)\)\s*$', '',text,flags=re.M)
 if kp==17592186129269:
  a=text.index('_format_spec=importlib.util.spec_from_file_location');b=text.index('SOURCE=',a);text=text[:a]+'import math_format\n'+text[b:]
 if kp==17592186129283:text=text.replace("['.venv/bin/python',str(HERE/'render.py')", "[sys.executable,str(HERE/'render.py')")
 entry.write_text(text)
 if not g['legacy']:
  mf=source.parent/'math_format.py'
  if mf.exists():(old/'math_format.py').write_bytes(mf.read_bytes())
 if kp==17592186133927:(old/str(kp)/'assets').mkdir(exist_ok=True)
 recs=[];row={'kp':kp,'band':band,'original':str(source),'baseline_execution':'Disposable original runtime; only local import/interpreter path compatibility patches, no mathematical/render changes.','seed':983779}
 try:
  for name,script in [('before',entry),('after',(Path(g['directory'])/g['entrypoint']).resolve())]:
   output=base/(name+'-assets');output.mkdir(parents=True);env={k:v for k,v in os.environ.items()if k not in['PYTHONPATH','_CA_SOURCE_POLICY_CHILD']};env.update(PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(output),MPLCONFIGDIR=str(base/'mpl'))
   p=subprocess.run([sys.executable,str(script),'--difficulty',band,'--count','1','--seed','983779','--format','json'],cwd='/tmp',env=env,capture_output=True,text=True,timeout=90)
   if p.returncode:raise ValueError(name+': '+p.stderr[-1600:])
   data=json.loads(p.stdout);data=data.get('instances',data)if isinstance(data,dict)else data;recs.append(data[0])
  b,a=recs;bs,ass=signature(b['question']),signature(a['question']);row.update(parameters_unchanged=b['generation'].get('parameters')==a['generation'].get('parameters'),displayed_content_equals_latest_normalized_original=bs==ass,canonical_answers_and_complete_banks_unchanged=bs['fields']==ass['fields'],fresh_question_UUID=b['question'][':question/id']!=a['question'][':question/id']);row['passed']=all(row[k]for k in['parameters_unchanged','displayed_content_equals_latest_normalized_original','canonical_answers_and_complete_banks_unchanged','fresh_question_UUID']);row['changed_parts']=[k for k in bs if bs[k]!=ass.get(k)];return row,[{'kp':kp,'level':band,'record':a,'before_record':b}]
 except Exception as ex:row.update(error=str(ex),passed=False);return row,[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 jobs=[pool.submit(run,g,b)for g in A for b in sorted({r['level']for r in V if r['kp']==g['kp']and r.get('exit')==0 and r['level']in['easy','moderate','hard']})]
 for f in concurrent.futures.as_completed(jobs):
  r,rs=f.result();reports.append(r);samples+=rs;print(r['kp'],r['band'],r['passed'],r.get('error',r.get('changed_parts')),flush=True);(H/'staged-before-after-validation.json').write_text(json.dumps(reports,indent=2));(H/'staged-before-after-samples.json').write_text(json.dumps(samples,indent=2))
