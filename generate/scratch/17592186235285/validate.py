"""Independent display, geometry, full source fidelity and real grader checks."""
import concurrent.futures,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;script=H.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',script);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
raw=json.loads((H/'source.json').read_text());qs=raw['record'][':knowledge-point/questions']
# Grid displacements read from every displayed source diagram, origin translated to0.
geometries={'q-120254':([0,-4],[3,-1]),'q-120257':([6,0],[-3,-2]),'q-120260':([0,-3],[-1,2]),'q-325974':([0,-4],[-1,2]),'q-325983':([0,-4],[-2,2]),'q-367051':([0,-2],[2,-1]),'q-367052':([-2,0],[-1,-1]),'q-367059':([-3,0],[1,3]),'q-367060':([-3,0],[2,-2]),'q-367061':([3,0],[2,3]),'q-367062':([3,0],[-1,2]),'q-367064':([2,-2],[1,3]),'q-70148':([4,0],[-4,4]),'q-77451':([-3,0],[-1,-2])}
def clean(s):return s.replace('\\\\frac','\\frac')
def norm(s):return re.sub(r'!\[\]\((.*?)\)', '[DIAGRAM]',s)
def assert_format(s):
 assert s.count('$')%2==0
 stack=0
 for ch in s:
  if ch=='{':stack+=1
  if ch=='}':stack-=1
  assert stack>=0
 assert stack==0
 assert '--' not in s and '+-' not in s

def check(r):
 q=r['question'];p=r['generation']['parameters'];f=q[':question/answer-fields'][0];sol=q[':question/worked-solution'];prompt=q[':question/problem'];a,b=sp.symbols('a b')
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 for obj,key in [(q,':question/id'),(f,':answer-field/id')]+[(answer,':answer/id') for answer in f[':answer-field/choices']]:__import__('uuid').UUID(obj[key])
 computed=g.digest({'version':g.VERSION,'prompt':prompt,'solution':sol,'field':f[':answer-field/type'].rsplit('/',1)[-1],'values':sorted(answer[':answer/value'] for answer in f[':answer-field/choices'])})
 assert computed==r['generation']['content_fingerprint'] and q[':question/id']==g.uid(computed)
 assert_format(sol);assert_format(prompt)
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt
 vals=[g.parse(x[':answer/value']) for x in f[':answer-field/choices']];assert len(vals)==len(set(vals))
 chosen=[x for x in f[':answer-field/choices'] if x[':answer/id']==f[':answer-field/correct'][1]];assert len(chosen)==1
 # Parse actual prompt known coefficient, actual solution magnitude and every numeric stage.
 expr=re.search(r'c=\\lambda a([+-](?:\d+)?b)',prompt).group(1);k=sp.sympify(expr.replace('b','*b') if re.search(r'\d',expr) else expr,locals={'b':1})
 mag=re.search(r'PC=(.*?)\|a\|',sol).group(1);rr=g.parse(mag) if mag else sp.Integer(1)
 actual=-rr;assert g.parse(chosen[0][':answer/value'])==actual
 assert re.search(r'\\lambda =(.*?)\n\$\$',sol)
 final=re.search(r'\\lambda =(.*?)\n\$\$',sol).group(1).rstrip('.');assert g.parse(final)==actual
 def expression(s):
  s=clean(s);s=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'(\1)/(\2)',s)
  s=re.sub(r'(?<=[\d)])(?=[ab])','*',s)
  return sp.sympify(s,locals={'a':a,'b':b})
 stage=re.findall(r'& =([^&]+?)\.\\end',sol)[0]
 assert sp.expand(expression(stage)-(k*b+actual*a))==0
 coefficient=re.search(r'Consequently, \$c=\\lambda a[^=]+=([^$]+)\.\$',sol).group(1)
 assert sp.expand(expression(coefficient)-(k*b+actual*a))==0
 pc=re.search(r'PC\}=([^$]+)\.\$',sol).group(1)
 assert sp.expand(expression(pc)-actual*a)==0
 av=sp.Matrix(p['a']);bv=sp.Matrix(p['b']);cv=k*bv+actual*av;pv=k*bv
 assert sp.det(sp.Matrix.hstack(av,bv))!=0
 assert cv-pv==actual*av
 assert (cv-pv).dot(av)<0
 # Check actual rendered sidecar geometry, not only generation metadata.
 for role,path in r['generation']['plot_assets'].items():
  side=Path(path).with_suffix('.json')
  if Path(path).is_absolute():
   assert Path(path).exists() and side.exists();data=json.loads(side.read_text())
   assert data['role']==role and data['c']==[float(x) for x in cv] and data['p']==[float(x) for x in pv]
 return True
cases=[];replays=[];fidelity=[]
for q in qs:
 sid=q[':question/math-academy-id'];field=q[':question/answer-fields'][0];kind=field[':answer-field/type'][':db/ident'].split('/')[-1];level=q[':question/difficulty'][':db/ident'].split('/')[-1]
 rr=-g.parse(field[':answer-field/correct'][':answer/value']);ks=re.search(r'c=\\lambda a([+-]\d*)b',q[':question/problem']).group(1);k=int(ks+'1' if ks in ('+','-') else ks)
 template='radio' if kind=='radio' else ('blank_standard' if 'then\n\n' in q[':question/problem'] else 'blank_inline')
 params={'r':str(rr),'k':str(k),'a':geometries[sid][0],'b':geometries[sid][1],'ratio_style':'decimal' if sid=='q-70148' else 'fraction','answer_style':['fraction','decimal','fraction','fraction','fraction'] if sid=='q-77451' else 'decimal' if sid in ['q-120254','q-120260','q-367060','q-70148'] else 'fraction','final_dot':sid=='q-325974','source_assets':{role:re.search(r'!\[\]\((.*?)\)',q[key]).group(1) for role,key in [('prompt',':question/problem'),('solution',':question/worked-solution')]}}
 case={'source_id':sid,'template':template,'parameters':params,'bank_profile':sid if kind=='radio' else 'blank','level':level};cases.append(case)
 existing=json.loads((H/'source-cases.json').read_text());existing=[c for c in existing if c['source_id']!=sid]+[case];(H/'source-cases.json').write_text(json.dumps(existing,indent=2)+'\n')
 r=g.generate(level,template=template,parameters=params,profile=case['bank_profile']);check(r);replays.append(r)
 assert r['question'][':question/problem']==q[':question/problem'],sid+' prompt'
 assert r['question'][':question/worked-solution']==q[':question/worked-solution'],sid+' solution'
 original=[g.parse(a[':answer/value']) for a in field[':answer-field/choices']];generated=[g.parse(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
 assert sorted(original)==sorted(generated),sid+' bank';assert -rr==g.parse(field[':answer-field/correct'][':answer/value'])
 fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact':True,'bank_values_equivalent':len(original),'correct_designation':True,'raw_values_exact':sum((__import__('collections').Counter(a[':answer/value'] for a in field[':answer-field/choices']) & __import__('collections').Counter(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])).values()),'raw_notation_exact':sorted(a[':answer/value'] for a in field[':answer-field/choices'])==sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])})
(H/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
# At least two variants per every profile and layout; all levels exercised.
variants=[]
for level in ('easy','moderate','hard'):
 for kind in ('radio','blank'):
  for seed in (21,42):variants.append(g.generate(level,seed,field_type=kind))
for axis in ([0,-2],[0,2],[-2,0],[2,0]):
 variants.append(g.generate('easy',parameters={'r':'2','k':'1','a':axis,'b':[1,2]},field_type='blank'))
for case in cases:
 for seed in (5,8):
  p=dict(case['parameters']);p.pop('source_assets');p['a']=[-x for x in p['a']];p['b']=[-x for x in p['b']]
  if seed==8:
   p['a'],p['b']=[p['a'][1],-p['a'][0]],[p['b'][1],-p['b'][0]]
   p['r']='3/2' if sp.Rational(p['r']).q==2 and p['r']=='1/2' else '3' if sp.Rational(p['r']).q==2 else str(2 if p['r']=='1' else 4 if p['r']=='3' else 3)
   p['k']=str((3 if abs(int(p['k']))!=3 else 4)*(1 if int(p['k'])>0 else -1))
  variants.append(g.generate(case['level'],seed,template=case['template'],parameters=p,profile=case['bank_profile']))
for r in variants:check(r)
# Mathematical task counts exhaust finite sampler domains, without invoking plots.
variety={}
for level in ('easy','moderate','hard'):
 tasks=set()
 for seed in range(2000):
  p=g.sample(level,__import__('random').Random(seed),'blank');a=sp.Matrix(p['a']);b=sp.Matrix(p['b']);div=sp.gcd_list(list(a)+list(b));tasks.add((p['r'],p['k'],tuple(str(x/div) for x in list(a)+list(b))))
 exhaustive=set();radio_tasks=set()
 for rr,kk,av,bv in __import__('itertools').product(([1,2,3,4] if level!='hard' else [sp.Rational(n,2) for n in range(1,9)]),([1] if level=='easy' else [2,3,4] if level=='moderate' else [-1,-2,-3,-4]),([[0,-2],[0,2],[-2,0],[2,0]] if level=='easy' else [[0,-2],[-2,0],[2,0],[2,-2]]),[[1,1],[1,2],[-1,2],[-1,-1]]):
  if sp.det(sp.Matrix.hstack(sp.Matrix(av),sp.Matrix(bv)))==0:continue
  div=sp.gcd_list(av+bv);task=(str(rr),str(kk),tuple(str(x/div) for x in av+bv));exhaustive.add(task)
  if rr!=1:radio_tasks.add(task)
 assert tasks <= exhaustive
 variety[level]={'sampled_unique_math_tasks':len(tasks),'draws':2000,'exhaustive_sampler_math_tasks':len(exhaustive),'authored_radio_eligible_tasks':len(radio_tasks)}
# Stable identity under shuffle, distinct banks, seed permutation coverage.
for case in cases:
 r1=g.generate(case['level'],1,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);r2=g.generate(case['level'],99,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);assert r1['question'][':question/id']==r2['question'][':question/id']
# Fresh simultaneous writes identical/different inputs using private atomic files.
p={'r':'2','k':'2','a':[0,-6],'b':[2,1]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(lambda seed:g.generate('moderate',seed,parameters=p if seed<2 else dict(p,r='3'),field_type='blank'),range(3)))
for r in results:check(r)
assert results[0]['question'][':question/id']==results[1]['question'][':question/id']
assert results[0]['question'][':question/id']!=results[2]['question'][':question/id']
fresh_dir=Path(__import__('tempfile').mkdtemp(prefix='concurrency-',dir=H))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 fresh=list(pool.map(lambda seed:g.render_plots(p if seed<2 else dict(p,r='3'),fresh_dir),range(3)))
for seed,assetmap in enumerate(fresh):
 for role,path in assetmap.items():
  data=json.loads(Path(path).with_suffix('.json').read_text());expected_r=2 if seed<2 else 3
  assert data['c']==[float(x) for x in 2*sp.Matrix(p['b'])-expected_r*sp.Matrix(p['a'])]
assert fresh[0]==fresh[1] and fresh[0]!=fresh[2]
assert not list(fresh_dir.glob('.render-*')) and not list(fresh_dir.glob('.sidecar-*'))
assert not list(H.glob('render-input-*')) and not list((H/'assets').glob('.render-*'))
# Invalid complete banks and level bounds reject rather than silently modifying.
rejects=[('easy',dict(p,k='2')),('moderate',dict(p,k='-2')),('moderate',dict(p,r='3/2')),('hard',dict(p,k='2')),('hard',dict(p,k='-2',r='9/2')),('moderate',dict(p,r='1'))]
for level,pbad in rejects:
 try:g.generate(level,parameters=pbad,field_type='radio')
 except ValueError:pass
 else:raise AssertionError('Invalid parameters accepted')
checks=[]
for i,r in enumerate(replays+variants):
 f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):cs=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'complete bank ID check'} for a in f[':answer-field/choices']]
 else:
  val=g.parse(f[':answer-field/choices'][0][':answer/value']);cs=[{'submitted':str(val),'expected':'accepted','purpose':'canonical scalar'},{'submitted':f'{val.p*3}/{val.q*3}','expected':'accepted','purpose':'unreduced equivalent scalar'},{'submitted':str(-val),'expected':'rejected','purpose':'reversal omitted'}]
 checks.append({'label':str(i),'record':r,'checks':cs})
engine_provenance={str(path):hashlib.sha256(Path(path).read_bytes()).hexdigest() for path in ['generate/runs/current/check-engine','generate/runs/current/check-engine.rs']}
(H/'engine-input.json').write_text(json.dumps(checks,indent=2)+'\n');subprocess.run(['generate/runs/current/check-engine',str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
engine=json.loads((H/'engine-report.json').read_text())
review=[]
for q,r in zip(qs,replays):review.extend([{'kind':'original','source_id':q[':question/math-academy-id'],'question':q},{'kind':'replay','record':r}])
review.extend({'kind':'generated variant','record':r} for r in variants)
(H/'review.json').write_text(json.dumps(review,indent=2)+'\n')
md=['# Direction-reversal review','Originals and normal API replays retain their original source image references. Generated variants use private Matplotlib assets.']
for entry in review:
 q=entry.get('question',entry.get('record',{}).get('question'));md.extend(['\n## '+entry['kind']+' '+entry.get('source_id',entry.get('record',{}).get('generation',{}).get('bank_profile','')),q[':question/problem'],'\nOptions: '+', '.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']),q[':question/worked-solution']])
(H/'review.md').write_text('\n\n'.join(md)+'\n')
report={'passed':True,'source':g.SOURCE,'fidelity':{'practice_questions':len(qs),'prompt_exact':len(qs),'solution_exact':len(qs),'complete_banks':8,'blank_fields':6,'complete_values':sum(x['bank_values_equivalent'] for x in fidelity),'distractors':32,'correct_designations':14,'raw_values_exact':sum(x['raw_values_exact'] for x in fidelity),'raw_bank_notation_exact':sum(x['raw_notation_exact'] for x in fidelity),'details':fidelity},'independent_math_records':len(replays)+len(variants)+len(results),'generated_review_variants':len(variants),'native':engine,'engine_provenance':engine_provenance,'sympy_version':sp.__version__,'variety':variety,'boundary_rejections':len(rejects),'concurrency_calls':3,'source_anomalies':[],'authored_extensions':['easy scope (no captured examples)','separately authored normal radio bank'],'limitations':['Native radio ID checks establish selection wiring, not semantic numeric grading; independent mathematical checks cover displayed values.','Numerical source distractor intent is underdetermined; q-* are explicit observed-shape profiles.','Finite grid displacement samplers have finite task variety; counts exclude common scale and banks.']}
(H/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('native','fidelity')},indent=2));print('Fidelity:',report['fidelity']);print('Native:',{k:v for k,v in engine.items() if k!='records'})
