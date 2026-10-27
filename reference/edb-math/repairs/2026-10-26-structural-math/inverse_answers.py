"""Individually reviewed one-row fake determinants; prove exact legacy replay."""
import hashlib,json,re,sys,types
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,validate_tex
module=types.ModuleType('legacy_source_md');module.__file__='/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py';sys.modules[module.__name__]=module;legacy=Path('/tmp/structural-md-prevention/legacy-md.py');exec(compile(legacy.read_text(),module.__file__,'exec'),module.__dict__)
rows=[r for r in json.loads((H/'source-formula-unresolved.json').read_text())if r['a']=='answer/value'];out=[];unresolved=[]
def inverse(text):
 parts=[];depth=0;i=0
 while i<len(text):
  m=ENV.match(text,i)
  if m and m[2]=='vmatrix':
   depth+=1 if m[1]=='begin'else-1;parts.append('|');i=m.end();continue
  if m:parts.append(m[0]);i=m.end();continue
  if text[i:i+2]==r'\\'and depth:parts.append(';');i+=2;continue
  if text[i]=='&'and depth:parts.append('|');i+=1;continue
  parts.append(text[i]);i+=1
 assert depth==0
 return re.sub(r'\\mid(?![A-Za-z])','|',''.join(parts))
canon=lambda s:re.sub(r'\s+','',s)
for d in rows:
 before=d['before'];after=inverse(before)
 try:
  assert ';'not in after
  validate_tex(after)
  replay=module.normalize_math_tex(after)
  assert canon(replay)==canon(before),(replay,before)
  out.append({'e':d['e'],'a':d['a'],'before':before,'after':after,'legacy_replay_matches':True,'legacy_converter_sha256':hashlib.sha256(legacy.read_bytes()).hexdigest(),'review':'Restored paired absolute-value/cardinality bars and retained original expression tokens; not a multirow determinant.'})
 except Exception as ex:unresolved.append({**d,'inverse':after,'reason':str(ex)})
(H/'inverse-answer-repairs.json').write_text(json.dumps(out,indent=2)+'\n');(H/'inverse-answer-unresolved.json').write_text(json.dumps(unresolved,indent=2)+'\n');print('confirmed reversible repairs',len(out),'unresolved',len(unresolved))
for r in unresolved:print(r['e'],r['inverse'],r['reason'][:250])
