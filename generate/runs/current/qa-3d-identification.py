"""Parent checks qualitative diagram criterion and every actual elimination argument."""
import importlib.util,json,re,itertools,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186172088;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_3d_math',R/'ode-scalar-parser.py');s=p.s;g=module('root_3d_generator',D.with_suffix('.py'))
# Independently read from all ten original images, before inspecting recipes.
TARGET={'q-122559':(1,0,0),'q-122664':(0,0,2),'q-122651':(2,0,0),'q-122668':(0,-1,0),'q-122670':(0,0,-1),'q-123748':(-2,0,0),'q-123749':(0,-1,0),'q-123750':(1,0,0),'q-122662':(0,3,0),'q-122667':(-1,0,0)}
C=dict(instances=0,displayed_formulas=0,plot_components=0,elimination_checks=0,explanation_claims=0,source_banks=0,source_values=0,source_refs=0,source_raw_solutions=0,source_normal_solutions=0,source_solution_repairs=0)
tasks={};fps={}
def formulas(text):return [(m[1],tuple(p.vector(m[2]))) for m in re.finditer(r'([FGHK])\(x,y,z\)=(.*?)(?=,\\,|\n|\$|$)',text)]
def check(r):
 q=r['question'];f=q[':question/answer-fields'][0];meta=r['generation'];offer={};ids={}
 for a in f[':answer-field/choices']:
  if a[':answer/value']=='None of the listed':none=a[':answer/id'];continue
  name,vec=formulas(a[':answer/value'])[0];offer[name]=vec;ids[name]=a[':answer/id']
 assert len(offer)==4 and len(set(offer.values()))==4
 plot=meta['plot'];path=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]);assert path==Path(plot['prompt']) and path.exists()
 profile=meta['bank_profile'];params=meta['parameters']
 if plot['source_asset']:
  target=TARGET[profile];old=g.QUESTIONS[profile];ref=re.search(r'!\[\]\((.*?)\)',old[':question/problem'])[1];assert hashlib.sha256(path.read_bytes()).digest()==hashlib.sha256((Path('/media/jake/SSD/EDB/math')/ref).read_bytes()).digest()
 else:
  side=json.loads(Path(plot['sidecar']).read_text());assert side['renderer']=='Matplotlib mplot3d' and side['axis_arrowheads'];target=tuple(s.Rational(z) for z in side['exact_components']);assert len(side['grid'])==len(side['vectors'])==27
  for vec in side['vectors']:assert tuple(s.Rational(z) for z in vec)==target;C['plot_components']+=3
  assert side['plot_scale']>0
  base=TARGET[profile] if profile!='authored-easy' else (1,0,0);want=[0,0,0]
  for i,z in enumerate(base):want['xyz'.index(params['permutation'][i])]=z*params['flip']*params['scale']
  assert tuple(want)==target
 axis=next(i for i,v in enumerate(target) if v);assert sum(v!=0 for v in target)==1;sign=s.sign(target[axis]);others=[i for i in range(3) if i!=axis]
 matches=[name for name,vec in offer.items() if all(vec[i]==0 for i in others) and not vec[axis].free_symbols and s.sign(vec[axis])==sign]
 assert len(matches)<=1;assert f[':answer-field/correct'][1]==(ids[matches[0]] if matches else none)
 solution=q[':question/worked-solution'];bullets=re.findall(r'- ([\s\S]*?)\n\n\$\$\n([\s\S]*?)\n\$\$',solution);assert len(bullets)==(2 if profile=='authored-easy' else 3);eliminated=[]
 for n,(prose,block) in enumerate(bullets):
  if n==0:
   assert f'${"xyz"[axis]}$-axis' in prose and all(f'${"ijk"[i]}$' in prose for i in others);predicate=lambda vec:all(vec[i]==0 for i in others)
  elif n==1:
   word='positive' if sign>0 else 'negative';assert f'*{word}* ${"xyz"[axis]}$-direction' in prose and f'${"ijk"[axis]}$ component' in prose;predicate=lambda vec:not vec[axis].free_symbols and s.sign(vec[axis])==sign
  else:
   if 'every component' in prose:predicate=lambda vec:all(not z.free_symbols for z in vec)
   else:assert f'${"ijk"[axis]}$ component' in prose;predicate=lambda vec:not vec[axis].free_symbols
  assert predicate(tuple(map(s.sympify,target)));C['explanation_claims']+=1
  for name,vec in formulas(block):assert offer[name]==vec and not predicate(vec),(prose,name,vec);eliminated.append(name);C['elimination_checks']+=1
 assert sorted(eliminated)==sorted(set(offer)-set(matches))
 if matches:assert formulas(solution)[-1]==(matches[0],offer[matches[0]])
 else:assert "doesn't correspond to any" in solution
 level=q[':question/difficulty'].split('/')[-1];shape=(axis,int(sign));tasks.setdefault(level,set()).add(shape);assert fps.setdefault(shape,meta['mathematical_fingerprint'])==meta['mathematical_fingerprint'];C['instances']+=1;C['displayed_formulas']+=4;return q
for case in json.loads((D/'source-cases.json').read_text()):
 old=g.QUESTIONS[case['math_academy_id']];raw=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];normal=check(g.generate(case['level'],parameters=case['parameters'],profile=case['math_academy_id']));nf=normal[':question/answer-fields'][0];sf=old[':question/answer-fields'][0]
 assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(sf[':answer-field/choices'])
 assert sf[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);C['source_refs']+=1
 assert raw[':question/worked-solution']==old[':question/worked-solution'];C['source_raw_solutions']+=1
 expected=old[':question/worked-solution']
 if case['math_academy_id']=='q-123750':expected=expected.replace('so the $i$ component of our vector field is constant','so every component of our vector field is constant');C['source_solution_repairs']+=1
 assert normal[':question/worked-solution']==expected;C['source_normal_solutions']+=1
for profile,definition in g.PROFILES.items():
 for perm,flip in itertools.product(itertools.permutations('xyz'),(-1,1)):check(g.generate(definition[0],profile=profile,parameters=dict(permutation=''.join(perm),flip=flip,scale=1)))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
assert all(len(vals)==6 for vals in tasks.values());C['finite_actual_targets']={level:len(vals) for level,vals in tasks.items()};C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
