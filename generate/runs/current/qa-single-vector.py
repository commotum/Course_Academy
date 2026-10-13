"""Independent parent checks single-scalar vector generators."""
import importlib.util,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_one_vector_readback',R/'single-vector-readback.py');g=module('root_one_vector_generator',D.with_suffix('.py'));s=p.s
cases=json.loads((D/'source-cases.json').read_text());cs={c['source_id']:c for c in cases};counts=dict(instances=0,source_questions=0,source_values=0,source_refs=0,source_prompts=0,source_ordered_solutions=0,source_assets=0)
def images(text):return re.sub(r'!\[\]\(.*?\)','![](ASSET)',text)
def check(r):
 meta=r['generation'];profile=meta.get('profile',meta.get('bank_profile'));geom=cs.get(profile,{}).get('parameters')
 if geom is None and meta.get('parameters',{}).get('source_assets'):
  geom=next(c['parameters'] for c in cases if c['parameters'].get('source_assets')==meta['parameters']['source_assets'])
 stats,factor,known=p.check(r,geom)
 for key,n in stats.items():counts[key]=counts.get(key,0)+n
 level=r['question'][':question/difficulty'].split('/')[-1]
 if K==17592186096701:
  assert factor>0 and known>0
  if meta['authored']:
   if level=='easy':assert known==1
   elif level=='moderate':assert known in (2,3,4)
   else:
    assert known.q in (2,3) and 1<known<3 and factor.q in (3,4)
    prompt=r['question'][':question/problem'];printed=dict(re.findall(r'([OABC])=\(([^)]+)\)',prompt));assert set(printed)=={'O','A','B','C'}
    ref=Path(re.search(r'!\[\]\((.*?)\)',prompt)[1]);side=json.loads(ref.with_suffix('.json').read_text())['plot_data'];A=s.Matrix(side['a']);B=s.Matrix(side['b']);C=s.Rational(side['ca_exact'])*A+s.Rational(side['cb_exact'])*B
    for label,expected in [('O',s.zeros(2,1)),('A',A),('B',B),('C',C)]:assert all(p.same(p.p.scalar(z),v) for z,v in zip(printed[label].split(','),expected))
    assert all((known*z).q>1 for z in B)
 else:
  assert factor<0
  if level=='easy':assert known==1 and factor.q==1
  elif level=='moderate':assert known in (2,3,4) and factor.q==1
  else:assert known in (-1,-2,-3,-4) and factor.q in (1,2)
 counts['instances']+=1;return r['question']
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in cases:
 kwargs=dict(template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')))
 if c.get('field_type'):kwargs['field_type']=c['field_type']
 q=check(g.generate(c['level'],**kwargs));old=sources[c['source_id']]
 assert images(q[':question/problem'])==images(old[':question/problem']);counts['source_prompts']+=1
 assert images(q[':question/worked-solution'])==images(old[':question/worked-solution']);counts['source_ordered_solutions']+=1
 for f,nf in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  oldvals=[p.p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];newvals=[p.p.scalar(z[':answer/value']) for z in nf[':answer-field/choices']];assert sorted(map(str,oldvals))==sorted(map(str,newvals))
  actual=p.p.scalar(next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]));assert actual==p.p.scalar(f[':answer-field/correct'][':answer/value']);counts['source_values']+=len(oldvals);counts['source_refs']+=1
 for source,generated in zip(re.findall(r'!\[\]\((.*?)\)',old[':question/problem']+old[':question/worked-solution']),re.findall(r'!\[\]\((.*?)\)',q[':question/problem']+q[':question/worked-solution'])):
  gen=Path(generated)
  if not gen.is_file():gen=Path('/media/jake/SSD/EDB/math')/generated
  assert gen.read_bytes()==(Path('/media/jake/SSD/EDB/math')/source).read_bytes();counts['source_assets']+=1
 counts['source_questions']+=1
for r in json.loads((D/'review.json').read_text()):
 if r.get('kind')!='original':check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
