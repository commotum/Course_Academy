import copy,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,'scripts');from generator_packages import build_manifest,manifest_digest,verify_package
from question_capture.math_format import normalize_prose,validate_generated_record
H=Path(__file__).resolve().parent;row=next(r for r in json.loads((H/'generators.json').read_text())if r[0]==17592186184172);source=Path('/media/jake/SSD/EDB/math')/row[2];dest=H/'generator-17592186184172-labels';shutil.copytree(source.parent,dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
for p in [dest,*dest.rglob('*')]:p.chmod(0o755 if p.is_dir()or p.suffix=='.py'and p.name==source.name else 0o644)
s=source.read_text();assert "VERSION='1.1.1'"in s;s=s.replace("VERSION='1.1.1'","VERSION='1.1.2'");s=s.replace('import sympy as sp','import sympy as sp\nfrom math_format import normalize_prose');helper="""def statement_key(value):
 # Original Col(A) statements refer to real Euclidean space. Preserve that
 # source mathematical role before decisions and identity hashes are formed.
 if r'\\text{Col}(A)' in value:value=value.replace('{R}',r'{\\mathbb{R}}')
 return normalize_prose(value)

""";s=s.replace('def clean(q):',helper+'def clean(q):');old="':answer-field/key':f[':answer-field/key']";assert old in s;s=s.replace(old,"':answer-field/key':statement_key(f[':answer-field/key'])");(dest/source.name).write_text(s);(dest/'math_format.py').write_bytes(Path('scripts/question_capture/math_format.py').read_bytes());oldmanifest=json.loads((source.parent/'generator-package.json').read_text());files=sorted([*oldmanifest['files'],'math_format.py']);manifest=build_manifest(dest,source.name,files,dependencies=oldmanifest['dependencies']);(dest/'generator-package.json').write_text(json.dumps(manifest,indent=2)+'\n');digest=manifest_digest(manifest);verify_package(dest,digest)
raw=json.loads((source.parent/'17592186184172/source-current.json').read_text());source_questions=raw['record'][':knowledge-point/questions'];records=[];replay=[]
for i,q in enumerate(source_questions):
 sid=q[':question/math-academy-id'];level=q[':question/difficulty'][':db/ident'].split('/')[-1];args=['--difficulty',level,'--count','1','--seed',str(908500+i),'--template',sid,'--format','json'];before=json.loads(subprocess.run([sys.executable,str(source),*args],capture_output=True,text=True,check=True).stdout)[0];after=json.loads(subprocess.run([sys.executable,str(dest/source.name),*args],capture_output=True,text=True,check=True).stdout)[0];validate_generated_record(after)
 assert before['question'][':question/problem']==after['question'][':question/problem'],sid
 labels=[]
 for a,b in zip(before['question'][':question/answer-fields'],after['question'][':question/answer-fields']):
  av=next(x[':answer/value']for x in a[':answer-field/choices']if x[':answer/id']==a[':answer-field/correct'][1]);bv=next(x[':answer/value']for x in b[':answer-field/choices']if x[':answer/id']==b[':answer-field/correct'][1]);assert av==bv,(sid,av,bv)
  expected=normalize_prose(a[':answer-field/key'].replace('{R}',r'{\mathbb{R}}'))if r'\text{Col}(A)'in a[':answer-field/key']else normalize_prose(a[':answer-field/key']);assert b[':answer-field/key']==expected,(sid,a[':answer-field/key'],b[':answer-field/key']);labels.append({'before':a[':answer-field/key'],'after':b[':answer-field/key'],'correct_value_unchanged':True})
 records.append(after);replay.append({'source_identity':sid,'difficulty':level,'seed':908500+i,'problem_unchanged':True,'labels':labels})
# Source data is evidence and is never rewritten.
assert (source.parent/'17592186184172/source-current.json').read_bytes()==(dest/'17592186184172/source-current.json').read_bytes()
(H/'checkbox-generator-samples.json').write_text(json.dumps(records,indent=2));(H/'checkbox-generator-recurrence.json').write_text(json.dumps({'kp':row[0],'source_data_unchanged':True,'version_before':'1.1.1','version_after':'1.1.2','changes_before_identity_hash':True,'templates':replay},indent=2));candidate={'kp':row[0],'directory':str(dest),'entrypoint':source.name,'old_reference':row[2],'files':files,'dependencies':manifest['dependencies'],'approved_digest':digest,'generator_entity':row[1]};(H/'checkbox-generator-candidates.json').write_text(json.dumps([candidate],indent=2));print('templates',len(records),'changed_labels',sum(a['before']!=a['after']for r in replay for a in r['labels']),'digest',digest)
