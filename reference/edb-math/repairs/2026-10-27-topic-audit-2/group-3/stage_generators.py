import hashlib,json,re,shutil,subprocess,sys,os
from pathlib import Path
sys.path.insert(0,'scripts');from generator_packages import build_manifest,manifest_digest,verify_package
from question_capture.math_format import normalize_prose,validate_generated_record
H=Path(__file__).resolve().parent;G=json.loads((H/'generators.json').read_text());candidates=[];samples=[];evidence=[]
for kp,newversion in [(17592186092260,'linear-e-workspace-5'),(17592186092261,'general-exponential-chain-5'),(17592186078584,'1.2.1')]:
 row=next(r for r in G if r[0]==kp);source=Path('/media/jake/SSD/EDB/math')/row[2];dest=H/('generator-'+str(kp));shutil.copytree(source.parent,dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 for p in [dest,*dest.rglob('*')]:p.chmod(0o755 if p.is_dir()else 0o644)
 for p in dest.rglob('__pycache__'):shutil.rmtree(p)
 text=source.read_text();oldversion=re.search(r"VERSION\s*=\s*'([^']+)'",text)[1];text=re.sub(r"(VERSION\s*=\s*)'[^']+'",lambda m:m[1]+repr(newversion),text,count=1)
 text=text.replace('import sympy as sp','sys.dont_write_bytecode=True\nimport sympy as sp')if 'import sys'in text else text
 if kp==17592186078584:
  text=text.replace('import argparse, hashlib, json, math, random, uuid','import argparse, hashlib, json, math, random, uuid, sys\nsys.dont_write_bytecode=True\nfrom math_format import normalize_prose,normalize_tex')
  marker="    content={'version':VERSION,'level':level,'prompt':prompt,'solution':solution,'bank':sorted(bank),'correct':right}"
  assert marker in text;text=text.replace(marker,"    prompt=normalize_prose(prompt);solution=normalize_prose(solution);bank=[normalize_tex(v)for v in bank];right=normalize_tex(right)\n"+marker)
 (dest/source.name).write_text(text);helper=dest/'math_format.py';helper.write_bytes(Path('scripts/question_capture/math_format.py').read_bytes());oldmanifest=json.loads((source.parent/'generator-package.json').read_text());files=sorted(set(oldmanifest['files'])|{'math_format.py'});manifest=build_manifest(dest,source.name,files,dependencies=oldmanifest['dependencies']);(dest/'generator-package.json').write_text(json.dumps(manifest,indent=2)+'\n');digest=manifest_digest(manifest);verify_package(dest,digest)
 levels=['easy','moderate']if kp==17592186092260 else['easy','moderate','hard'];rows=[]
 for level in levels:
  args=['--difficulty',level,'--count','4','--seed','912227','--format','json'];a=json.loads(subprocess.run([sys.executable,str(source),*args],capture_output=True,text=True,check=True).stdout);b=json.loads(subprocess.run([sys.executable,str(dest/source.name),*args],capture_output=True,text=True,check=True).stdout);assert len(a)==len(b)
  for old,new in zip(a,b):
   validate_generated_record(new);oq,nq=old['question'],new['question'];assert oq[':question/id']!=nq[':question/id']
   assert normalize_prose(oq[':question/problem'])==nq[':question/problem'];assert normalize_prose(oq[':question/worked-solution'])==nq[':question/worked-solution'];assert old['generation']['parameters']==new['generation']['parameters']
   of,nf=oq[':question/answer-fields'],nq[':question/answer-fields'];assert len(of)==len(nf)
   for f,g in zip(of,nf):
    av=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);bv=next(a[':answer/value']for a in g[':answer-field/choices']if a[':answer/id']==g[':answer-field/correct'][1]);assert av==bv,(kp,av,bv)
   samples.append({'kp':kp,'level':level,'record':new});rows.append({'level':level,'template':new['generation']['template'],'before_id':oq[':question/id'],'after_id':nq[':question/id'],'parameters_unchanged':True,'canonical_values_unchanged':True,'only_latest_formatter_normalization':True})
 rawfiles=[name for name in oldmanifest['files']if name.endswith('.json')];assert all((source.parent/name).read_bytes()==(dest/name).read_bytes()for name in rawfiles)
 evidence.append({'kp':kp,'version_before':oldversion,'version_after':newversion,'raw_source_files_unchanged':rawfiles,'fix_before_identity_hash':True,'fresh_identity_proofs':rows});candidates.append({'kp':kp,'old_reference':row[2],'directory':str(dest),'entrypoint':source.name,'files':files,'dependencies':manifest['dependencies'],'approved_digest':digest})
 print('staged',kp,newversion,digest,flush=True)
(H/'generator-candidates.json').write_text(json.dumps(candidates,indent=2));(H/'staged-generator-samples.json').write_text(json.dumps(samples,indent=2));(H/'staged-generator-evidence.json').write_text(json.dumps(evidence,indent=2));print('fresh staged',len(samples))
