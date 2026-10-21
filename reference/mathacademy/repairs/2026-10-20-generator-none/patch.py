"""Repair reviewed source-backed checkbox families; preserve immutable old packages."""
import ast,shutil
from read import *

def replace_once(text,old,new):
 assert text.count(old)==1,(old,text.count(old));return text.replace(old,new)

def patch(text,kp):
 old='globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])'
 text=replace_once(text,old,"globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')")
 if kp==17592186100888:
  text=replace_once(text,'CASES = ((False, True), (True, False), (True, True))','CASES = ((False, False), (False, True), (True, False), (True, True))')
 if kp==17592186054815:text=replace_once(text,'rng.randrange(1,16)','rng.randrange(16)')
 if kp==17592186147456:
  old="    # This captured None-only family is invariant under the coefficient scales;\n    # it cannot yield a nonempty correct checkbox subset.\n    if template == 'q-108916':\n        raise ValueError('q-108916 has no correct selectable option and is evidence-only')\n    eligible=[t for t,(l,_) in CASES.items() if l==level and t != 'q-108916']"
  text=replace_once(text,old,"    # The captured None family has an explicit, correctly keyed selectable answer.\n    eligible=[t for t,(l,_) in CASES.items() if l==level]")
 if kp==17592186119848:
  text=replace_once(text,"if typ=='three-matrix-checkbox':return [original_matches(sid)] if original_matches(sid) else []","if typ=='three-matrix-checkbox':return sorted({original_matches(sid), ()})")
 ast.parse(text);return text

if __name__=='__main__':
 rows=json.loads((HERE/'affected.json').read_text());patched=[]
 for row in rows:
  kp=row['kp'];path=Path(row['runtime_script'])
  if row['packaged']:
   target=HERE/'packages'/str(kp);target.mkdir(parents=True,exist_ok=True)
   for name in row['manifest']['files']:
    dst=target/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path.parent/name,dst)
   path=target/row['manifest']['entrypoint'];(target/'generator_policy.py').write_bytes((ROOT/'scripts/generator_policy.py').read_bytes())
   save('packages/'+str(kp)+'/source-none-evidence.json',{'source_basis':json.loads((HERE/'identity.json').read_text())['basis'],'kp':kp,'source_math_academy_ids':row['source_none'],'rule':'Preserve visible None in this checkbox family; correct iff every ordinary option is false.'})
  else:
   backup=HERE/'legacy-before'/str(kp)/path.name;backup.parent.mkdir(parents=True,exist_ok=True)
   if not backup.exists():
    assert sha(path)==row['before_sha256'];shutil.copy2(path,backup)
   else:assert sha(backup)==row['before_sha256']
  original=path.read_text();path.write_text(patch(original,kp))
  patched.append({**row,'updated_script':str(path),'updated_sha256':sha(path),'policy_sha256':sha(ROOT/'scripts/generator_policy.py')})
 save('patched.json',patched)
 print(json.dumps({'patched':len(patched),'legacy':sum(not r['packaged']for r in patched),'immutable_packages':sum(r['packaged']for r in patched)}))
