import copy,hashlib,json,os,re,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;A=json.loads((H/'generator-audit.json').read_text());V=json.loads((H/'generator-validation.json').read_text());K=[17592186096814,17592186124461,17592186129197,17592186129269,17592186129270,17592186129271,17592186129282,17592186129283,17592186133927,17592186172083,17592186172130,17592186172131,17592186179712,17592186198361,17592186198373,17592186198374,17592186198398,17592186198399];stages=[]
helper='''"""Format displayed content before identity; identify image content by bytes."""
import copy,hashlib,re
from pathlib import Path
from math_format import normalize_prose,normalize_tex
_IMAGE=re.compile(r'(?:/[A-Za-z0-9_.~+-]+)+\\.(?:png|jpg|jpeg|svg|webp|gif)')
def asset_payload(value):
    if isinstance(value,str):
        def replace(m):
            p=Path(m[0])
            return 'asset-sha256:'+hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else m[0]
        return _IMAGE.sub(replace,value)
    if isinstance(value,dict):return {k:asset_payload(v)for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [asset_payload(v)for v in value]
    return value

def normalize_question(q):
    q=copy.deepcopy(q)
    for attr in [':question/problem',':question/worked-solution']:
        if attr in q:q[attr]=normalize_prose(q[attr])
    for f in q.get(':question/answer-fields',[]):
        typ=f[':answer-field/type'];typ=typ.get(':db/ident')if isinstance(typ,dict)else typ
        if typ==':answer-field.type/checkbox':f[':answer-field/key']=normalize_prose(f[':answer-field/key'])
        old_to_new={}
        for a in f[':answer-field/choices']:
            typ=a[':answer/type'];typ=typ.get(':db/ident')if isinstance(typ,dict)else typ
            before=a[':answer/value'];after=normalize_tex(before)if typ==':answer.type/math'else normalize_prose(before)if typ==':answer.type/text'else before;a[':answer/value']=after;old_to_new[before]=after
        if isinstance(f.get(':answer-field/correct'),str):f[':answer-field/correct']=old_to_new.get(f[':answer-field/correct'],f[':answer-field/correct'])
    return q
'''
for kp in K:
 g=next(g for g in A if g['kp']==kp);src=Path(g['script']);dest=H/('generator-'+str(kp));dest.mkdir(exist_ok=True)
 if not g.get('legacy_repository_relative'):
  oldmanifest=json.loads((src.parent/'generator-package.json').read_text())
  for name in oldmanifest['files']:
   p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src.parent/name,p);p.chmod(0o644)
 else:
  oldmanifest=None;shutil.copy2(src,dest/src.name);folder=src.with_suffix('')
  if folder.is_dir():
   # Keep retained inputs; output plots and audit products are not package inputs.
   for p in folder.rglob('*'):
    if not p.is_file()or any(c in['__pycache__','plots']for c in p.relative_to(folder).parts):continue
    if p.suffix not in['.json','.py','.png','.svg','.txt','.csv']:continue
    out=dest/folder.name/p.relative_to(folder);out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
  for name in['ca_source_runtime.py','ca_source_policy.py','generator_source_policy.py','generator_policy.py',str(kp)+'-source-policy.json']:
   p=src.parent/name
   if p.exists():shutil.copy2(p,dest/name)
 for p in dest.rglob('*'):
  if p.is_file():p.chmod(0o644)
 (dest/'math_format.py').write_bytes(Path('scripts/question_capture/math_format.py').read_bytes());(dest/'audit_runtime.py').write_text(helper)
 text=(dest/src.name).read_text();oldver=re.search(r"VERSION\s*=\s*['\"]([^'\"]+)['\"]",text)
 if oldver:
  newver=oldver[1]+'-audit9837';text=text[:oldver.start(1)]+newver+text[oldver.end(1):]
 else:newver=None
 # Imports stay local to the immutable package. No repository ancestor dependency.
 text=re.sub(r'^sys\.path\.insert\(0,str\((?:Path\(__file__\)\.resolve\(\)\.parents\[2\]|HERE\.parents\[2\])\s*/\s*["\']scripts/question_capture["\']\)\)\s*$', '',text,flags=re.M)
 if kp==17592186129269:
  start=text.index("_format_spec=importlib.util.spec_from_file_location");end=text.index("SOURCE=",start);text=text[:start]+'import math_format\n'+text[end:]
 # Import early, after future imports, before all functions and identity operations.
 ls=text.splitlines();at=next((i+1 for i,l in enumerate(ls)if l.startswith('from __future__ import')),1);ls[at:at]=['import sys','sys.dont_write_bytecode=True','from audit_runtime import asset_payload,normalize_question','from math_format import normalize_prose,normalize_tex'];text='\n'.join(ls)+'\n'
 # Every asset-bearing digest/UUID receives byte identity, including per-choice IDs.
 text=re.sub(r'json\.dumps\((obj|o|x|content|q),',r'json.dumps(asset_payload(\1),',text)
 text=text.replace("uuid.UUID(KP_UUID),name)","uuid.UUID(KP_UUID),str(asset_payload(name)))").replace("uuid.UUID(KP_UUID),text)","uuid.UUID(KP_UUID),str(asset_payload(text)))")
 if kp==17592186129282:
  marker=' prompt,solution=render(t,p,data);C=data[-1]';assert marker in text;text=text.replace(marker,marker+'\n prompt=normalize_prose(prompt);solution=normalize_prose(solution)')
 elif kp==17592186129197:
  marker=" content={'version':VERSION,'question':question";assert marker in text;text=text.replace(marker," question=normalize_question(question);spelling=[normalize_tex(v)for v in spelling]\n"+marker)
 elif kp==17592186133927:
  marker=' content=copy.deepcopy(q);identity=digest';assert marker in text;text=text.replace(marker,' q=normalize_question(q)\n'+marker)
 elif kp==17592186172130:
  marker='    # Identity depends on displayed content';assert marker in text;text=text.replace(marker,"    if not raw:\n        prompt=normalize_prose(prompt);sol=normalize_prose(sol);spec=[([normalize_tex(v)for v in vals],correct,original)for vals,correct,original in spec]\n"+marker)
 elif kp==17592186172131:
  marker="    normalized={'prompt':prompt";assert marker in text;text=text.replace(marker,"    if not raw:prompt=normalize_prose(prompt);solution=normalize_prose(solution)\n"+marker)
 elif kp==17592186198361:
  marker="    content=dict(version=VERSION";assert marker in text;text=text.replace(marker,"    if not raw:prompt=normalize_prose(prompt);q[':question/problem']=prompt;q[':question/worked-solution']=normalize_prose(q.get(':question/worked-solution',''));choices=[normalize_tex(v)for v in choices]\n"+marker)
 elif kp==17592186198373:
  marker="    content=dict(version=VERSION";assert marker in text;text=text.replace(marker,"    if raw is None:prompt=normalize_prose(prompt);sol=normalize_prose(sol);banks=[([normalize_tex(v)for v in vals],correct)for vals,correct in banks]\n"+marker)
 elif kp==17592186198374:
  marker='    identity=[VERSION,level,prob,sol,sorted(value_strings)]';assert marker in text;text=text.replace(marker,'    prob=normalize_prose(prob);sol=normalize_prose(sol);value_strings=[normalize_tex(v)for v in value_strings]\n'+marker)
  text=text.replace("path=OUT/'plots';path.mkdir(exist_ok=True)","path=Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(OUT/'plots')));path.mkdir(parents=True,exist_ok=True)")
  text=text.replace('dump(identity)', 'dump(asset_payload(identity))')
 elif kp==17592186198398:
  marker='    identity=stable(dict(version=VERSION';assert marker in text;text=text.replace(marker,'    if raw_recipe is None:problem=normalize_prose(problem);solution=normalize_prose(solution);values=[(v,normalize_tex(t))for v,t in values]\n'+marker)
 elif kp==17592186198399:
  marker="    signature={'version':VERSION,'level':level if normal";assert marker in text;text=text.replace(marker,'    if normal:prompt=normalize_prose(prompt);solution=normalize_prose(solution)\n'+marker)
  marker="    q=record['question'];field_signatures=[]";assert marker in text;text=text.replace(marker,"    if not record['generation'].get('evidence_only'):record['question']=normalize_question(record['question'])\n"+marker)
 if kp in[17592186129283,17592186133927]:
  # Specific output roots are supplied by the public execution protocol.
  if 'import os'not in text:text=text.replace('import sys\nsys.dont_write_bytecode', 'import os\nimport sys\nsys.dont_write_bytecode',1)
  text=text.replace("HERE/'plots'/name","Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(HERE/'plots')))/name")
  text=text.replace("HERE.joinpath('plots').mkdir(exist_ok=True)","Path(os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR',str(HERE/'plots'))).mkdir(parents=True,exist_ok=True)")
  text=text.replace("['.venv/bin/python',str(HERE/'render.py')", "[sys.executable,str(HERE/'render.py')")
  text=text.replace("dir=HERE,delete=False", "dir=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'),delete=False")
 # The Stokes helper may contain a differently named plot root (checked after staging).
 (dest/src.name).write_text(text)
 if kp==17592186129283:
  p=dest/str(kp)/'render.py';s=p.read_text();start=s.index('try:import matplotlib');end=s.index("matplotlib.use('Agg')",start);s=s[:start]+'import matplotlib\n'+s[end:];p.write_text(s)
 stages.append({'kp':kp,'old_reference':next(r[2]for r in json.loads((H/'generators.json').read_text())if r[0]==kp),'directory':str(dest),'entrypoint':src.name,'legacy':g.get('legacy_repository_relative',False),'version_before':oldver[1]if oldver else None,'version_after':newver,'dependencies':oldmanifest['dependencies']if oldmanifest else {'python':'3.13','packages':{'sympy':'1.14.0','matplotlib':'3.11.2','numpy':'2.5.4','pillow':'12.3.0'}}})
 print(kp,'staged',flush=True)
(H/'generator-stage-plan.json').write_text(json.dumps(stages,indent=2))
