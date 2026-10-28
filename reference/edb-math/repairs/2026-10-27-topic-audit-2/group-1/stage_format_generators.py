import difflib,json,re,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];D=json.loads((H/'current.json').read_text());rows=json.loads((H/'fresh-notation-review.json').read_text());wanted={r['kp']for r in rows if r['validation_error']or not r['integral_display']};display={r['kp']for r in rows if not r['integral_display']};stages=[];diffs=[]
helper='''"""Presentation repair for individually reviewed standalone integral prompts."""
from math_format import MATH,normalize_prose
def display_integral(problem):
    # Called only at four audited generator problem-authoring boundaries.
    # Source evidence, solution references, banks and blank fragments are untouched.
    def replace(m):
        value=m[0]
        if value.startswith(('$$',r'\\[',r'\\(')) or r'\\int' not in value:return value
        return '\\n\\n$$\\n'+value[1:-1].strip()+'\\n$$\\n\\n'
    return normalize_prose(MATH.sub(replace,problem))
'''
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);dst.chmod(0o644)
for kp,g in D['generators']:
 if kp not in wanted:continue
 old=Path('/media/jake/SSD/EDB/math')/g[':question-generator/script'];old=old if old.exists()else R/g[':question-generator/script'];dst=H/'generator-stages'/str(kp);dst.mkdir(parents=True,exist_ok=True)
 if(old.parent/'generator-package.json').exists():
  manifest=json.loads((old.parent/'generator-package.json').read_text());files=list(manifest['files']);deps=manifest['dependencies']
  for f in files:copy(old.parent/f,dst/f)
 else:
  files=[old.name];deps={'python':'3.13','packages':{'sympy':'1.14.0'}};copy(old,dst/old.name)
  if kp==17592186176047:
   files+=['ca_source_policy.py','ca_source_runtime.py','17592186176047-source-policy.json']+[str(p.relative_to(old.parent))for p in(old.with_suffix('')).rglob('*')if p.is_file()and(p.name in['recipes.json','source-cases.json','current-source.json']or'assets'in p.parts)]
   for f in files[1:]:copy(old.parent/f,dst/f)
 copy(R/'scripts/question_capture/math_format.py',dst/'math_format.py');files.append('math_format.py')
 if kp in display:(dst/'integral_display.py').write_text(helper);files.append('integral_display.py')
 for filename in files.copy():
  if not filename.endswith('.py')or filename in['math_format.py','integral_display.py']:continue
  p=dst/filename;s=p.read_text();before=s
  s=re.sub(r"VERSION\s*=\s*'([^']+)'",lambda m:"VERSION='"+m[1]+"-format-audit-9122-v1'",s,count=1)
  if kp in display and filename in[old.name,'forward.py']:
   if'from math_format import'in s:s=s.replace('from math_format import','from integral_display import display_integral\nfrom math_format import',1)
   if kp==17592186064167:
    s=s.replace('p=normalize_prose(problem);sol=', 'p=display_integral(normalize_prose(problem));sol=');s=s.replace('problem=normalize_prose(problem);sol=', 'problem=display_integral(normalize_prose(problem));sol=')
   elif kp==17592186064168:s=s.replace("':question/problem':normalize_prose(text)","':question/problem':display_integral(normalize_prose(text))")
   elif kp==17592186064169:s=s.replace(" identity=slug({'version':VERSION", " text=display_integral(text)\n identity=slug({'version':VERSION",1)
   elif kp==17592186184155 and filename=='forward.py':
    s=s.replace(' qid=uuid.uuid5(', ' prompt=display_integral(prompt)\n qid=uuid.uuid5(',1);s=s.replace('json.dumps([prompt,sorted(values)', 'json.dumps([VERSION,prompt,sorted(values)',1)
  if kp==17592186176047 and filename==old.name:
   s=s.replace('import sympy as sp','import sympy as sp\nfrom math_format import normalize_prose,normalize_tex',1)
   marker=" content=digest({'version':VERSION,'prompt':q[':question/problem']";assert marker in s;s=s.replace(marker," q[':question/problem']=normalize_prose(q[':question/problem']);q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])\n fields=[(key,atype,[normalize_tex(v)for v in bank]if atype=='math'else bank,normalize_tex(correct)if atype=='math'else correct)for key,atype,bank,correct in fields]\n"+marker,1)
  if kp==17592186176048 and filename==old.name:
   s=s.replace('import sympy as sp','import sympy as sp\nfrom math_format import normalize_prose,normalize_tex',1);marker='  content=hash_data([VERSION,prompt,solution,sorted(values)])';assert marker in s;s=s.replace(marker,"  if profile!='observed_raw_q103242':prompt=normalize_prose(prompt);solution=normalize_prose(solution);values=[normalize_tex(v)for v in values]\n"+marker,1)
  if kp==17592186229181 and filename==old.name:
   s=s.replace('import sympy as sp','import sympy as sp\nfrom math_format import normalize_prose,normalize_tex',1);marker=" q={':question/problem':prompt}";assert marker in s;s=s.replace(marker," if not raw:prompt=normalize_prose(prompt);solution=normalize_prose(solution)if solution is not None else None;values=[normalize_tex(v)for v in values]\n"+marker,1)
  if kp==17592186229182 and filename==old.name:
   s=s.replace('import sympy as sp','import sympy as sp\nfrom math_format import normalize_prose,normalize_tex',1);marker=' identity=fingerprint(dict(version=VERSION';assert marker in s;s=s.replace(marker," if not raw:prompt=normalize_prose(prompt);solution=normalize_prose(solution)if solution is not None else None;vals=[normalize_tex(v)for v in vals]\n"+marker,1)
  if before!=s:p.write_text(s);diffs.extend(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile=str(old.parent/filename),tofile=str(p)))
 evidence={'basis_t':9122,'kp':kp,'old_reference':g[':question-generator/script'],'classification':'Authored presentation/validation repair before content identity creation, distinct from raw source byte replay','changes':'Latest stable shared formatter canonicalizes authored prose and math before identities; scalar values, banks, parameter validators and graph geometries preserved.'+(' Individually reviewed standalone integral calculations promoted to display in problem only.'if kp in display else''),'source_replay':'Original source JSON/masks retained unchanged; explicit raw branches are not presentation-promoted. Original-parameter production replay may receive the documented authored presentation repair.','identity':'Version bumped before hash. Sum-rule UUID payload additionally includes VERSION because prior identity omitted it. No existing database IDs touched.'};(dst/'repair-evidence.json').write_text(json.dumps(evidence,indent=2));files.append('repair-evidence.json');stages.append({'kp':kp,'old_reference':g[':question-generator/script'],'old_entity':g[':db/id'],'directory':str(dst),'entrypoint':old.name,'files':sorted(set(files)),'dependencies':deps})
(H/'format-generator-stage-config.json').write_text(json.dumps(stages,indent=2));(H/'format-generator.diff').write_text(''.join(diffs));print('stages',len(stages))
