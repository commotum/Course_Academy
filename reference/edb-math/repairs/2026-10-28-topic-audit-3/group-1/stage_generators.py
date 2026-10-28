import ast,difflib,json,re,shutil,sys,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];inv=json.loads((H/'generator-inventory.json').read_text());bad={r['kp']['db_id']for r in json.loads((H/'generator-validation-errors.json').read_text())};configs=[];diff=[]
helper=r'''"""Audited presentation boundaries; raw source evidence remains separate."""
import hashlib,re
from pathlib import Path
from math_format import normalize_prose,normalize_tex,MATH

def prose(value):return normalize_prose(value) if value is not None else None

def problem(value):
    value=prose(value)
    # A whole displayed task integral after an explicit calculation/setup cue.
    # Assumptions, small integral references, banks and blank fragments stay inline.
    def replace(m):
        if m[0].startswith(('$$',r'\[',r'\(')):return m[0]
        body=m[0][1:-1].strip();prefix=value[max(0,m.start()-90):m.start()]
        if not re.match(r'(?:\\displaystyle\s*)?(?:\{?\\(?:int|iint|iiint|oint)|[∫∬∭∮])',body):return m[0]
        if not re.search(r'(?:[Ee]valuate|[Cc]alculate|[Ww]hat is|[Ee]xpress(?: the following)?(?: triple)? integral|[Ff]ind the (?:following )?(?:line |double |triple )?integral)\s*$',prefix):return m[0]
        return '\n\n$$\n'+body+'\n$$\n\n'
    return MATH.sub(replace,value)

def values(bank):return [normalize_tex(v) for v in bank]

def question(q):
    q[':question/problem']=problem(q[':question/problem'])
    if ':question/worked-solution'in q:q[':question/worked-solution']=prose(q[':question/worked-solution'])
    return q

def identity_material(value):
    if isinstance(value,dict):return {k:identity_material(v)for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [identity_material(v)for v in value]
    if not isinstance(value,str):return value
    def replace(m):
        p=Path(m[1])
        if not p.is_file():return m[0]
        return '![](sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()+')'
    return re.sub(r'!\[[^\]]*\]\(([^)]+)\)',replace,value)
'''
def copy(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
def insert(s,marker,code):
 assert s.count(marker)==1,(marker,s.count(marker));return s.replace(marker,code+marker,1)
for spec in inv:
 kp=spec['kp']
 if kp not in bad:continue
 old=Path(spec['path']);dst=H/'generator-stages'/str(kp);dst.mkdir(parents=True,exist_ok=True);entry=old.name;files=[]
 if spec['manifest']:
  deps=spec['manifest']['dependencies']
  for name in spec['manifest']['files']:copy(old.parent/name,dst/name);files.append(name)
 else:
  deps={'python':'3.13.5','packages':{'sympy':'1.14.0','matplotlib':'3.11.2','numpy':'2.3.2','mpmath':'1.3.0'}}
  copy(old,dst/entry);files.append(entry)
  for p in old.with_suffix('').rglob('*'):
   if p.is_file()and p.suffix in ['.json','.py','.png','.svg']and not any(x in p.parts for x in ['__pycache__','mpl-cache']):
    name=str(p.relative_to(old.parent));copy(p,dst/name);files.append(name)
  # Explicit runtime local imports and policy files, never ancestor discovery.
  for name in ['ca_source_runtime.py','ca_source_policy.py','mathcheck_17592186083280.py',str(kp)+'-source-policy.json']:
   if(old.parent/name).exists():copy(old.parent/name,dst/name);files.append(name)
 for name,src in [('math_format.py',R/'scripts/question_capture/math_format.py'),('generator_policy.py',R/'scripts/generator_policy.py')]:copy(src,dst/name);files.append(name)
 (dst/'audit_presentation.py').write_text(helper);files.append('audit_presentation.py')
 p=dst/entry;s=p.read_text();before=s
 # The published runtime must import only bundled policy, never repository ancestry.
 s=re.sub(r'_policy_sys\.path\.insert\(0, str\(next\(p for p in _PolicyPath\(__file__\)\.resolve\(\)\.parents if \(p / "scripts/generator_policy.py"\)\.is_file\(\)\)\)\)',r'_policy_sys.path.insert(0, str(_PolicyPath(__file__).resolve().parent))',s)
 s=s.replace('from scripts.generator_policy import','from generator_policy import')
 # Imports go after __future__; the scripts already import Path before runtime use.
 astree=ast.parse(s);idx=max([n.end_lineno for n in astree.body if isinstance(n,ast.ImportFrom)and n.module=='__future__']or[0]);lines=s.splitlines(True);lines.insert(idx,'from audit_presentation import prose as _ca_prose, problem as _ca_problem, values as _ca_values, question as _ca_question, identity_material as _ca_material\n');s=''.join(lines)
 s=re.sub(r"VERSION\s*=\s*(['\"])([^'\"]+)\1",lambda m:'VERSION='+repr(m[2]+'-format-audit-9837-v1'),s,count=1)
 if kp==17592186083245:s=insert(s," material={'version':VERSION", " if rawq is None:problem=_ca_problem(problem);solution=_ca_prose(solution);banks=[_ca_values(b)for b in banks]\n")
 elif kp==17592186083280:s=insert(s,"    content={'level':", "    if not raw:prompt=_ca_problem(prompt);solution=_ca_prose(solution);banks=[_ca_values(b)for b in banks]if atype=='math'else banks\n")
 elif kp==17592186129267:s=insert(s," # Content identity includes actual difficulty", " if not raw:_ca_question(q);raw_banks=[(_ca_values(vals),ci,key)for vals,ci,key in raw_banks]\n")
 elif kp==17592186129268:s=insert(s,"  identity=digest({'version':VERSION,'level':level,'prompt':q[':question/problem'],'solution':q[':question/worked-solution']", "  _ca_question(q);values=_ca_values(values)\n")
 elif kp==17592186133899:s=insert(s,"    difficulty=q.get(':question/difficulty'", "    if not raw:prompt=_ca_problem(prompt);solution=_ca_prose(solution);tex=_ca_values(tex)\n")
 elif kp==17592186133900:s=insert(s," bank=sorted([{'key':", " if not str(profile).startswith('observed:'):\n  prompt=_ca_problem(prompt);solution=_ca_prose(solution)\n  for f in fields:\n   old=f.get(':answer-field/correct',[None,None])[1];correct_value=next((a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==old),None)\n   for a in f[':answer-field/choices']:a[':answer/value']=_ca_values([a[':answer/value']])[0]\n")
 elif kp==17592186133929:
  # Latest helper now canonicalizes all existing normal prose/values before digest.
  s=insert(s,"    identity=digest({'version':VERSION", "    prompt=_ca_problem(prompt);solution=_ca_prose(solution)\n")
 elif kp==17592186157298:
  s=s.replace("qid=uid('question:'+sid+':'+str(scale))","qid=uid('question:'+VERSION+':'+sid+':'+str(scale))")
  s=s.replace("':question/problem':prompt,':question/worked-solution':'\\n\\n'.join(stages)","':question/problem':_ca_problem(prompt),':question/worked-solution':_ca_prose('\\n\\n'.join(stages))")
  s=s.replace("':answer/value':integral(row)","':answer/value':_ca_values([integral(row)])[0]")
 elif kp==17592186172085:
  # Package practice.py also authors records; normalize there before its digest below.
  pass
 elif kp==17592186175987:s=insert(s," content=[VERSION,level,prompt", " if not raw:\n  prompt=_ca_problem(prompt);solution=_ca_prose(solution)\n  for f in fields:f['values']=_ca_values(f['values']);f['correct']=_ca_values([f['correct']])[0]\n")
 elif kp==17592186176023:s=insert(s," content={'difficulty':", " if raw is None:prompt=_ca_problem(prompt);sol=_ca_prose(sol);strings=_ca_values(strings)\n")
 elif kp==17592186176024:s=insert(s," identity={'version':VERSION", " if not raw:problem=_ca_problem(problem);solution=_ca_prose(solution);values_tex=_ca_values(values_tex)\n")
 elif kp==17592186198389:s=insert(s," # Presentation hash excludes seed", " prompt=_ca_problem(prompt);solution=_ca_prose(solution)\n")
 # Runtime images should resolve from their actual package location, not a repo root.
 s=s.replace('str(path.relative_to(ROOT))','str(path.resolve())')
 # Normalize asset reference identities in explicit digest functions, preserving content.
 s=re.sub(r'json\.dumps\((a|v|data|material|z),',lambda m:'json.dumps(_ca_material('+m[1]+'),',s)
 p.write_text(s);diff.extend(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile=spec['reference'],tofile=str(p)))
 # Include source assets which legacy snapshots address through the shared immutable store.
 if 'ASSET_ROOT' in s:
  s=s.replace("ASSET_ROOT = Path('/media/jake/SSD/EDB/math')","ASSET_ROOT = Path(__file__).resolve().parent / 'source-assets'")
  s=s.replace("ASSET_ROOT=Path('/media/jake/SSD/EDB/math')","ASSET_ROOT=Path(__file__).resolve().parent/'source-assets'")
  for ref in set(re.findall(r'images/[a-f0-9]{2}/[a-f0-9]+\.(?:png|svg)', ''.join(q.read_text()for q in dst.rglob('*.json')if q.stat().st_size<20000000))):
   source=Path('/media/jake/SSD/EDB/math')/ref
   if source.exists():name='source-assets/'+ref;copy(source,dst/name);files.append(name)
  p.write_text(s)
 evidence={'basis_t':9837,'kp':kp,'old_reference':spec['reference'],'classification':'Pre-identity authored presentation repair, with original raw source evidence retained','changes':'Latest canonical math formatter before identity creation; narrow standalone-integral task display; unchanged math domains, operations, parameter guards, complete banks and graph geometry. Version bumped. Local bundled policy runtime retained. Asset references in content digests bind image bytes rather than package/output directory spelling.','source_replay':'Explicit raw/observed branches retain original source prose/banks. Original source snapshots are included unchanged; production source replay receives documented presentation repairs.','proof_limit':'Frozen only after outside-repository CLI, all supported bands/templates, source-role/math, grader and strict render tests below.'};(dst/'repair-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');files.append('repair-evidence.json')
 configs.append({'kp':kp,'old_reference':spec['reference'],'old_entity':spec['entity'],'directory':str(dst.resolve()),'entrypoint':entry,'files':sorted(set(files)),'dependencies':deps})
(H/'generator-stage-config.json').write_text(json.dumps(configs,indent=2)+'\n');(H/'generator-format.patch').write_text(''.join(diff));print('staged',len(configs))
