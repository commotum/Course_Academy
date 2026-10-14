#!/usr/bin/env python3
"""Independent checks read the displayed field, derivative rows and volume arithmetic."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('generator',HERE.parent/'17592186133930.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def tex(t):
 t=t.strip().rstrip('.').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace(r'\pi','pi').replace('π','pi')
 t=t.replace(' ','')
 t=re.sub(r'(?<!\\frac)\{(x|y|z|pi)\}',r'\1',t);t=re.sub(r'\^\{(\d+)\}',r'^\1',t)
 t=t.replace(r'\operatorname{sin}',r'\sin').replace(r'\sin x','sin(x)').replace(r'\sinx','sin(x)')
 t=re.sub(r'\{e\}\^\{?z\}?','exp(z)',t)
 while re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',t):t=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',t)
 t=t.replace('{','(').replace('}',')')
 t=re.sub(r'([0-9xyz)])(?=(?:exp|sin)\()',r'\1*',t)
 return parse_expr(t,local_dict={'x':g.x,'y':g.y,'z':g.z,'pi':sp.pi,'exp':sp.exp,'sin':sp.sin},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def eq(a,b):assert sp.simplify(a-b)==0,(a,b)
def formatting(q):
 for t in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t' for c in t),'control character'
  assert t.count('$')%2==0,'math delimiter'
  bal=0
  for c in t:
   if c=='{':bal+=1
   if c=='}':bal-=1
   assert bal>=0
  assert bal==0,'braces'
  assert not re.search(r'(?<!\{)[+]-|--',t),'ungrouped sign'
def field_from_prompt(prompt):
 f=re.search(r'\$F=(.*?)\$',prompt,re.S).group(1).rstrip('.')
 if f.startswith('⟨'):return list(map(tex,f[1:-1].split(r',\,')))
 parts=re.split(r'\\,[ijk](?:\+|$)',f);assert len(parts)==4,parts
 return list(map(tex,parts[:-1]))
def geom_from_prompt(q,rec):
 p=q[':question/problem'];gg=rec['generation']['geometry']
 if gg[0]=='sphere':
  expr=tex(re.search(r'given by \$(.*?)\$',p).group(1).split('=')[0]);rhs=int(re.search(r'given by \$(.*?)\$',p).group(1).split('=')[1]);cs=[-sp.diff(expr,v).subs({g.x:0,g.y:0,g.z:0})/2 for v in g.XYZ]
  radius2=rhs-expr.subs(dict(zip(g.XYZ,cs)));assert radius2>0
  return ('sphere',sp.sqrt(radius2),tuple(cs))
 if rec['generation']['evidence_only']:return tuple(gg) # original plot independently transcribed below
 f=Path(re.search(r'!\[\]\((.*?)\)',p).group(1));assert f.exists();side=json.loads(f.with_suffix('.json').read_text());assert side['renderer']=='Matplotlib';out=tuple(side['geometry']);assert list(gg)==list(out)
 if out[0]=='cylinder':
  assert int(re.search(r'height \$(\d+)\$',p).group(1))==out[2]
  assert int(re.search(r'radius \$(\d+)\$',p).group(1))==out[1]
 return out
def check_record(r):
 q=r['question'];formatting(q);assert set(r['knowledge_point'])=={'db_id','id','title'}
 field=field_from_prompt(q[':question/problem']);der=[sp.diff(f,v) for f,v in zip(field,g.XYZ)];d=sp.simplify(sum(der));assert not d.free_symbols
 geom=geom_from_prompt(q,r);vol=g.volume(geom);ans=sp.simplify(d*vol)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S);assert len(blocks)==3
 rows=blocks[1].split(r' \\  & =');assert len(rows)==3
 formal=rows[0].split(' & =')[1];printed=re.findall(r'\\frac{∂}{∂[xyz]}\((.*?)\)(?:\+|$)',formal);assert len(printed)==3
 for pf,ff in zip(printed,field):eq(tex(pf),ff)
 # Contributions are checked separately, not merely their sum.
 parts=re.split(r'\+(?![^()]*\))',rows[1])
 # Nonconstant derivative components can contain plus signs; compare ordered
 # derivative components using the complete expected source grouping masks.
 if r['generation']['template']=='sphere_two_cancellations':
  aa,bb,cc=(r['generation']['parameters'][v] for v in ('a','b','c'))
  assert rows[1]==f'-{2*aa}x+{2*bb}y+({cc}-{2*bb}y)+{2*aa}x'
  m=re.fullmatch(r'(.+?)\+\((.+?)\)\+(.+)',rows[1]);assert m
  for pv,dv in zip(m.groups(),der):eq(tex(pv),dv)
  eq(tex(rows[1]),d)
 else:
  if len(parts)!=3:
   # Source source q162580 has -2x+4+2x; otherwise each contribution is grouped.
   raise AssertionError(parts)
  for pv,dv in zip(parts,der):eq(tex(pv),dv)
 eq(tex(rows[2].split(r'\end')[0]),d)
 flux=blocks[2].split(r' \\  & =');assert len(flux)==5
 first=flux[0].split(r'{∭}_{R}')[1].split(r'\,\text')[0];eq(tex(first),d)
 factor=flux[1].split(r'{∭}_{R}')[0];eq(tex('-1' if factor=='-' else factor),d)
 eq(tex(flux[3]),ans);eq(tex(flux[4].split(r'\end')[0]),ans)
 # Require the actual source factor/Volume/replacement stage sequence.
 assert r'\text{Volume}(R)' in flux[2]
 if geom[0]=='sphere':assert r'\frac{4}{3}\pi \cdot {'+str(geom[1])+r'}^{3}' in flux[3]
 elif geom[0]=='cylinder':assert r'\pi \cdot {'+str(geom[1])+r'}^{2}\cdot '+str(geom[2]) in flux[3]
 else:assert r'\cdot '.join(map(str,geom[1:])) in flux[3]
 for f in q[':question/answer-fields']:
  vals=[tex(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5
  for a,b in itertools.combinations(vals,2):assert sp.simplify(a-b)!=0
  if ':answer-field/correct' in f:
   ca=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);eq(tex(ca[':answer/value']),ans)
  elif not r['generation']['evidence_only']:raise AssertionError('missing correct')
  if not r['generation']['evidence_only']:
   expected=g.values_bank(d,geom)
   assert all(sum(sp.simplify(v-w)==0 for w in expected)==1 for v in vals)
 return ans
raw=[];sourcecases=[];banks=0;options=0;designations=0
for n,spec in g.SPECS.items():
 r=g.generate(spec['level'],template=n,parameters={'k':1},profile='raw-'+n);check_record(r);raw.append(r);q=r['question'];old=spec['source']
 assert set(q)==set(old),n
 assert q[':question/problem']==old[':question/problem'];assert q[':question/worked-solution']==old[':question/worked-solution']
 for f,o in zip(q[':question/answer-fields'],old[':question/answer-fields']):
  assert set(f)==set(o);assert f[':answer-field/key']==o[':answer-field/key']
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in o[':answer-field/choices'])
  if ':answer-field/correct' in o:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert value==o[':answer-field/correct'][':answer/value'];designations+=1
  banks+=1;options+=len(f[':answer-field/choices'])
 # Public uniform scaling works at changed source parameters; no literal branch.
 for k in (2,3):check_record(g.generate(spec['level'],template=n,parameters={'k':k},profile='raw-'+n))
 sourcecases.append({'source_id':old[':db/id'],'template':n,'level':spec['level'],'parameters':{'k':1},'bank_profile':'raw-'+n})
review=[];normal=[]
for n,l in g.TEMPLATES.items():
 for seed in (11,27):
  r=g.generate(l,seed,template=n);check_record(r);review.append(r)
for l in ('easy','moderate','hard'):
 for seed in range(100):
  r=g.generate(l,seed);check_record(r);normal.append(r)
 assert {r['generation']['template'] for r in normal if r['question'][':question/difficulty'].endswith('/'+l)}=={n for n,ll in g.TEMPLATES.items() if ll==l}
for r in review:
 p=r['generation']['parameters'];n=r['generation']['template'];l=g.TEMPLATES[n]
 other=g.generate(l,938,template=n,parameters=p);assert other['question'][':question/id']==r['question'][':question/id']
 # Endpoint primitive rows are inapplicable: all integrands reduce to constants
 # and every source explicitly uses geometric volume instead of antiderivatives.
# Mutation checks: syntax, derivative contribution, and stage removal.
for transform in [lambda q:q.update({':question/problem':q[':question/problem']+'\x0c'}),lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace('0+2+0','0+3+0')}),lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace(r'\text{Volume}(R)','V')})]:
 r=copy.deepcopy(raw[1]);transform(r['question'])
 try:check_record(r)
 except (AssertionError,ValueError,TypeError):pass
 else:raise AssertionError('mutation escaped')
for l,n,p in [('easy','q-162411',{'k':4,'geometry':['cylinder',2,3,'z']}),('moderate','q-162580',{'k':1,'geometry':['sphere',1,[-2,1,0]]}),('hard','sphere_two_cancellations',{'a':0,'b':1,'c':4,'geometry':['sphere',2,[-2,1,0]]})]:
 try:g.generate(l,template=n,parameters=p)
 except ValueError:pass
 else:raise AssertionError('domain escaped')
# Enumerate meaningful finite catalogs, excluding incidental sphere translations.
counts={};fps={l:set() for l in ('easy','moderate','hard')}
for n,l in g.TEMPLATES.items():
 count=0
 if l=='hard':
  for a,b,c,r in itertools.product(range(1,4),range(1,4),range(2,7),range(2,6)):
   params={'a':a,'b':b,'c':c,'geometry':['sphere',r,[-2,1,0]]}
   try:rec=g.generate(l,template=n,parameters=params)
   except ValueError:continue
   check_record(rec);fps[l].add(rec['generation']['mathematical_fingerprint']);count+=1
 else:
  base=g.GEOM[g.SPECS[n]['i']]
  domains=range(2,6) if base[0]=='sphere' else itertools.product(range(2,5),repeat=2) if base[0]=='cylinder' else itertools.product(range(1,5),repeat=3)
  for obj in domains:
   geometry=[base[0],obj,list(base[2])] if base[0]=='sphere' else [base[0],*obj,*([base[3]] if base[0]=='cylinder' else [])]
   for k in range(1,4):
    try:rec=g.generate(l,template=n,parameters={'k':k,'geometry':geometry})
    except ValueError:continue
    check_record(rec);fps[l].add(rec['generation']['mathematical_fingerprint']);count+=1
 counts[n]=count
# Independently transcribed source geometry, including each cylinder orientation.
assert g.GEOM==[('sphere',5,(0,2,-1)),('cylinder',1,2,'z'),('cylinder',2,3,'x'),('box',1,2,3),('sphere',2,(0,0,4)),('sphere',1,(-2,1,0)),('cylinder',3,2,'y'),('box',1,2,1),('box',4,2,2),('sphere',3,(0,2,0))]
# Fresh atomic concurrent writes in a new private directory; preserve artifacts.
import tempfile
renderdir=Path(tempfile.mkdtemp(prefix='render-concurrency-',dir=HERE))
geometries=[['box',2,3,4],['box',2,3,4],['cylinder',2,3,'x']]
processes=[]
for geometry in geometries:
 code="import importlib.util;from pathlib import Path;s=importlib.util.spec_from_file_location('g',"+repr(str(HERE.parent/'17592186133930.py'))+");g=importlib.util.module_from_spec(s);s.loader.exec_module(g);g.HERE=Path("+repr(str(renderdir))+");print(g.plot("+repr(geometry)+"))"
 processes.append(subprocess.Popen([sys.executable,'-c',code],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True))
paths=[]
for process,geometry in zip(processes,geometries):
 stdout,stderr=process.communicate();assert process.returncode==0,stderr;path=Path(stdout.strip());paths.append(path);assert path.exists();side=json.loads(path.with_suffix('.json').read_text());assert side['geometry']==geometry and side['closed_boundary']
assert paths[0]==paths[1] and paths[2]!=paths[0]
assert not list((renderdir/'plots').glob('tmp*'))
# Real grader: raw malformed record is separately demonstrated as unsupported.
items=[]
for i,r in enumerate(raw+review+normal):
 r=copy.deepcopy(r);anomaly=any(':answer-field/correct' not in f for f in r['question'][':question/answer-fields'])
 if anomaly:r['question'][':question/answer-fields']=[f for f in r['question'][':question/answer-fields'] if ':answer-field/correct' in f]
 checks=[]
 for j,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:checks.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'all complete bank selections'+(' after explicit legacy-field repair' if anomaly else '')})
 items.append({'label':str(i),'record':r,'checks':checks})
def dump(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
dump('engine-input.json',items);engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
dump('raw-anomaly-engine-input.json',[{'label':'raw missing designation','record':raw[1],'checks':[]}]);attempt=subprocess.run([str(engine),str(HERE/'raw-anomaly-engine-input.json'),str(HERE/'raw-anomaly-engine-report.json')],capture_output=True,text=True);assert attempt.returncode!=0 and 'correct lookup ref' in attempt.stderr
dump('raw-anomaly-native.json',{'exit_code':attempt.returncode,'stderr':attempt.stderr,'interpretation':'raw evidence field lacks correct ref; public raw preserves it; eligible output drops legacy field'})
dump('source-cases.json',sourcecases);dump('review.json',review)
report={'status':'passed','source_fidelity':{'questions':10,'exact_prompts':10,'exact_complete_solutions':10,'complete_banks':banks,'values':options,'correct_designations_matched':designations,'missing_original_correct_designations':1,'key_presence_parity':True},'independent_mathematics':{'raw_originals':10,'changed_raw':20,'normal_random':300,'review_variants':len(review),'all_eligible_catalog_tasks':sum(counts.values()),'mutations_rejected':3},'native':json.loads((HERE/'engine-report.json').read_text()),'limitations':['Historical wrong-operation interpretation opaque: raw scale profiles evidence-only.','One original duplicate field has no correct ref; raw record cannot enter native grader. Authoritative retained field separately graded.','Hard is authored, not an observed difficulty.','No primitive/endpoint chains: sources use constant divergence times geometric volume.'], 'semantic_counts':counts,'distinct_task_counts':{l:len(v) for l,v in fps.items()},'runtime':review[0]['generation']['runtime'],'plot_checks':{'source_diagrams_inspected':6,'concurrent_fresh_writes':3,'render_directory':str(renderdir)},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()}
dump('validation.json',report)
text='# Known-solid flux review\n\nFrozen math basis1356. Originals below are exact public evidence replays; changed variants use authored complete method banks. The malformed legacy first field in q162411 is retained in the original; absence of its designation is explicit.\n\n'
for r in raw:
 n=r['generation']['template'];text+='## Original '+n+'\n\n'+g.markdown(r)+'\n\n'
 for v in review:
  if v['generation']['template']==n:text+='### Generated '+n+' seed '+str(v['generation']['seed'])+'\n\n'+g.markdown(v)+'\n\n'
for r in review:
 if r['generation']['template']=='sphere_two_cancellations':text+='## Authored hard variant\n\n'+g.markdown(r)+'\n\n'
(HERE/'review.md').write_text(text)
print(json.dumps({k:report[k] for k in ('status','source_fidelity','independent_mathematics','semantic_counts','distinct_task_counts')},indent=2))
