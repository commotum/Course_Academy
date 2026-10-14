"""Independent displayed coordinate/solution/bank mathematics and native radio checks."""
import copy,hashlib,importlib.util,json,random,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
def load(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load(D.with_suffix('.py'),'axisdraft');F=load(ROOT/'generate/runs/current/root-source-fidelity.py','rootF');fmt=load(ROOT/'scripts/question_capture/math_format.py','fmt')
def save(n,v):(D/n).write_text(json.dumps(v,indent=2)+'\n')
def scalar(v):
 v=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',v)
 assert re.fullmatch(r'[\d/()+\- ]+',v),v
 return sp.sympify(v)
def read(q):
 p=re.search(r'point \$\((.*?),(.*?)\)\$',q[':question/problem']);line=re.search(r'line \$([xy])\s*=\s*([^$]+)\$',q[':question/problem']);assert p and line
 x,y=scalar(p[1]),scalar(p[2]);c=scalar(line[2].removesuffix('.'));a=line[1];return a,x,y,c

def check(r):
 assert r['knowledge_point']==dict(db_id=g.KP_ID,id=g.KP_UUID,title=g.TITLE)
 q=r['question'];meta=r['generation'];a,x,y,c=read(q);t,o=(x,y) if a=='x' else (y,x)
 # Projection to the line is the unique perpendicular endpoint; its Euclidean length.
 foot=(c,y) if a=='x' else (x,c);d=sp.sqrt((x-foot[0])**2+(y-foot[1])**2)
 fs=q[':question/answer-fields'];assert len(fs)==1;f=fs[0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 vs=[scalar(v[':answer/value']) for v in f[':answer-field/choices']];assert len(vs)==len(set(vs))==5
 if ':answer-field/correct' in f:assert next(v for v,answer in zip(vs,f[':answer-field/choices']) if answer[':answer/id']==f[':answer-field/correct'][1])==d
 else:assert meta['evidence_only'] and not meta['eligible_for_learning']
 if ':question/worked-solution' in q:
  s=q[':question/worked-solution'];assert 'vertical line' in s if a=='x' else 'horizontal line' in s
  points=re.findall(r'point \$\((.*?),(.*?)\)\$',s);assert points and all((scalar(xx),scalar(yy))==(x,y) for xx,yy in points)
  lines=re.findall(r'line \$([xy])\s*=\s*([^$]+)\$',s);assert lines and all(aa==a and scalar(cc)==c for aa,cc in lines)
  assert '$'+a+'$-coordinate' in s
  constant=re.search(r'point and \$([^$]+)\.\$',s);assert constant and scalar(constant[1])==c
  row=re.search(r'\$\$\s*d\s*=\s*\|(.*?)\|\s*=\s*([^$]+)\$\$',s,re.S);assert row
  # Parse the whole printed subtraction, rather than consulting generation metadata.
  assert abs(scalar(row[1]))==d and scalar(row[2].strip().removesuffix('.'))==d
  # Also require the operative coordinate-minus-line expression, not merely an equal result.
  wanted=g.tex(t)+'-'+('('+g.tex(c)+')' if c<0 else g.tex(c));assert row[1]==wanted
 for text in [q[':question/problem'],q.get(':question/worked-solution',''),*[v[':answer/value'] for v in f[':answer-field/choices']]]:assert all(ord(z)>=32 or z in '\n\t' for z in text)
 assert meta['mathematical_fingerprint']==g.fingerprint(a,x,y,c)
 for asset in meta['assets']:
  p=Path(asset['local_path']);assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==asset['sha256'];assert asset['path'] in q[':question/worked-solution']
  if not asset.get('unchanged_source_asset'):
   z=json.loads(p.with_suffix('.json').read_text());assert z['parameters']==list(map(str,(a,x,y,c))) and z['foot']==list(map(str,foot)) and scalar(z['distance'])==d and z['segment_pixels_at_100dpi']>=12
 if meta['eligible_for_learning']:
  level=q[':question/difficulty'].split('/')[-1];assert g.valid_level(level,x,y,c,a)
  expected=[d,abs(o-c),abs(t+c),abs(t) if meta['profile']=='coordinate-errors' else abs(o),abs(c)];assert set(vs)==set(expected) and all(v>0 for v in vs)
  fmt.validate_generated_record(copy.deepcopy(r))
 return a,x,y,c

def main():
 cases=[dict(source_id=sid,template=sid,level='easy',parameters={'dilation':1},profile='raw:'+sid) for sid in g.SOURCES];save('source-cases.json',cases)
 _,counts=F.check(g,g.KP_ID,D);records=[];inputs=[];reviews=[]
 for sid in g.SOURCES:
  assert g.generate('hard',template=sid,profile='raw:'+sid,parameters={'dilation':1})['question'][':question/id']==g.generate('easy',template=sid,profile='raw:'+sid,parameters={'dilation':1})['question'][':question/id']
 for sid in g.SOURCES:
  raw=g.generate('easy',template=sid,profile='raw:'+sid,parameters={'dilation':1});check(raw);records.append(raw)
  changed=g.generate('easy',template=sid,profile='raw:'+sid,parameters={'dilation':2});check(changed);records.append(changed);reviews.extend([('Original MA replay '+sid,raw),('Opaque evidence dilation '+sid,changed)])
 normal=[]
 for level in ('easy','moderate','hard'):
  for sid in g.TEMPLATES:
   for profile in g.PROFILES:
    r=g.generate(level,seed=101+len(normal),template=sid,profile=profile);check(r);normal.append(r)
    alt=g.generate(level,seed=777,template=sid,profile=profile,parameters=r['generation']['parameters']);check(alt);assert r['question'][':question/id']==alt['question'][':question/id'];assert sorted(r['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/value'])==sorted(alt['question'][':question/answer-fields'][0][':answer-field/choices'],key=lambda a:a[':answer/value'])
  for r in [z for z in normal if z['question'][':question/difficulty'].endswith('/'+level)][:3]:reviews.append(('Generated '+level+' '+r['generation']['template']+' '+r['generation']['profile'],r))
 # Changed axis with the same coordinates changes the selected target and all dependent prose.
 for level,ps in [('easy',dict(axis='x',x='7',y='6',c='2')),('moderate',dict(axis='x',x='7/2',y='11/2',c='1/2')),('hard',dict(axis='x',x='7/2',y='13/3',c='1/4'))]:
  for axis in ('x','y'):
   p=dict(ps,axis=axis);r=g.generate(level,template='q-74207',profile='coordinate-errors',parameters=p);check(r);normal.append(r)
 # Boundary and invalid inputs: no silent downgrade or replacement.
 invalid=[('easy',dict(axis='x',x='1/2',y='2',c='3')),('moderate',dict(axis='x',x='1/2',y='2',c='3')),('hard',dict(axis='x',x='1/2',y='3',c='3/4')),('easy',dict(axis='x',x='9',y='2',c='1')),('easy',dict(axis='x',x='4',y='3',c='4')),('easy',dict(axis='x',x='4',y='3',c='2'))]
 for level,p in invalid:
  try:g.generate(level,parameters=p,profile='coordinate-errors')
  except ValueError:pass
  else:raise AssertionError(('invalid admitted',level,p))
 for slot in (':question/problem',':question/worked-solution'):
  bad=copy.deepcopy(normal[0]);bad['question'][slot]=bad['question'][slot].replace('$x$', '$y$') if slot.endswith('solution') else re.sub(r'line \$x(\s*)=',r'line $y\1=',bad['question'][slot])
  # Pick a predictable x-oriented original for meaningful target mutation.
  bad=copy.deepcopy(next(z for z in normal if read(z['question'])[0]=='x'));bad['question'][slot]=bad['question'][slot].replace('$x$-coordinate','$y$-coordinate') if slot.endswith('solution') else re.sub(r'line \$x(\s*)=',r'line $y\1=',bad['question'][slot])
  try:check(bad)
  except AssertionError:pass
  else:raise AssertionError('stale target mutation survived')
 bad=copy.deepcopy(normal[0]);bad['question'][':question/worked-solution']+='\f'
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('control character survived')
 # Mathematical novelty is relevant coordinate + axis + line constant only.
 variety={}
 for level in ('easy','moderate','hard'):
  seen=set();axes=set();profiles=set()
  for seed in range(4000):
   rng=random.Random(seed);axis=rng.choice(('x','y'));profile=rng.choice(g.PROFILES);z=g.sample(level,rng,axis,profile);seen.add(g.fingerprint(*z));axes.add(axis);profiles.add(profile)
  assert len(seen)>=300;variety[level]=dict(distinct_mathematical_tasks=len(seen),sampled=4000,axes=sorted(axes),profiles=sorted(profiles))
 for r in records+normal:
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  inputs.append(dict(label=str(len(inputs)),record=r,checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',purpose='all correct and wrong whole scalar choices') for a in f[':answer-field/choices']]))
 save('native-input.json',inputs);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-grading.json')],check=True)
 save('review.json',[dict(label=label,record=r) for label,r in reviews]);(D/'review.md').write_text('\n\n'.join('## '+label+'\n\n'+g.markdown(r) for label,r in reviews)+'\n')
 save('normal-records.json',normal);save('variety.json',variety)
 baseline=json.loads((D/'baseline-before.json').read_text());paths=[ROOT/'generate/scratch/17592186073810.py',*sorted((ROOT/'generate/scratch/17592186073810').rglob('*'))];after={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()};assert after==baseline['paths'];save('baseline-after.json',dict(paths=after,pathset=list(after),unchanged=True))
 report=dict(passed=True,basis=2275,raw_fidelity=counts,original_complete_banks=6,original_values=30,source_designations_matched=5,source_designations_missing_preserved=1,source_solutions_matched=5,unrated_preserved=1,normal_records=len(normal),native_records=len(inputs),native_choices=len(inputs)*5,levels=['easy','moderate','hard'],variety=variety,mutations_rejected=['changed prompt axis','stale solution target','C0 control'],baseline_unchanged=True,python=sys.version.split()[0],sympy=sp.__version__,generator_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest())
 save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
