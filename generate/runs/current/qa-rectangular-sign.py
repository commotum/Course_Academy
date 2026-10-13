"""Root audits complete banks, fixed sequences, translated zero sets and plots."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186172041;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
p=module('parent_rect_math',R/'rectangular-sign-parser.py');g=module('parent_rect_gen',D.with_suffix('.py'))
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']};source_maps={}
for q in qs.values():
 values=p.read(q[':question/problem']);h,k=values[1][:2]
 for i,rel in enumerate(re.findall(r'!\[.*?\]\((.*?)\)',q.get(':question/worked-solution',''))):
  semantic=(h,k,values[2] if i==1 else None)
  assert rel not in source_maps or source_maps[rel]==semantic;source_maps[rel]=semantic;assert (D/rel).read_bytes()==(Path('/media/jake/SSD/EDB/math')/rel).read_bytes()
counts=dict(source_questions=0,source_values=0,source_designations=0,source_missing_designations=0,source_prompts=0,source_solutions=0,printed_instances=0,bank_values=0,statement_steps=0,sign_inequalities=0,definitions=0,zero_line_pairs=0,source_plot_instances=0,authored_plot_instances=0,plot_regions=0,authored_bank_instances=0)
def check(record):
 q=record['question'];values=p.read(q[':question/problem']);expr,(h,k,a,b,c),signs,claims,truth=values;f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];sets=[p.subset(v[':answer/value']) for v in bank];true=frozenset(i for i,v in enumerate(truth) if v)
 assert len(bank)==len(set(sets))==5 and [v[':answer/id'] for v,z in zip(bank,sets) if z==true]==[f[':answer-field/correct'][1]]
 for key,val in p.stages(q[':question/worked-solution'],values).items():counts[key]+=val
 plots=re.findall(r'!\[.*?\]\((.*?)\)',q[':question/worked-solution']);assert len(plots)==2
 for i,rel in enumerate(plots):
  path=Path(rel) if Path(rel).is_absolute() else D/rel;assert path.is_file()
  if rel in source_maps:assert source_maps[rel]==(h,k,signs if i==1 else None);counts['source_plot_instances']+=1
  else:
   side=json.loads(path.with_suffix('.json').read_text());assert side['role']==('partition' if i==0 else 'signs');assert side['zero_lines']=={'x':int(h),'y':int(k)};assert len(side['regions'])==4
   seen=set()
   for region in side['regions']:
    sx,sy=region['side'];idx=p.REGIONS.index((sx,sy));seen.add(idx);assert region['sign']==signs[idx]
    tx,ty=[s.Rational(str(v)) for v in region['test_point']];assert s.sign(tx-h)==sx and s.sign(ty-k)==sy;assert s.sign(expr.subs({p.x:tx,p.y:ty}))==signs[idx]
    xa,xb,ya,yb=region['bounds'];assert (xa==h if sx==1 else xb==h) and (ya==k if sy==1 else yb==k);assert xa<tx<xb and ya<ty<yb;counts['plot_regions']+=1
   assert seen==set(range(4));counts['authored_plot_instances']+=1
 assert expr.subs(p.x,h)==expr.subs(p.y,k)==0
 if record['generation']['bank_profile']=='authored_truth_flips':
  mask=sum(1<<i for i,v in enumerate(truth) if v);expected={mask,mask^1,mask^2,mask^4,mask^7};assert {sum(1<<i for i in z) for z in sets}==expected;counts['authored_bank_instances']+=1
 level=q[':question/difficulty'].rsplit('/',1)[1]
 if level=='easy':assert (a,b,c)==(1,1,1) and abs(h)==abs(k)==1
 elif level=='moderate':assert (a,b)==(1,1) and max(abs(h),abs(k))>=2
 else:assert (a,b) in ((2,1),(1,2))
 counts['printed_instances']+=1;counts['bank_values']+=5
 return values
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=qs[sid];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);assert check(r)==p.read(old[':question/problem']);assert old[':question/problem']==r['question'][':question/problem'];counts['source_prompts']+=1
 if old.get(':question/worked-solution'):assert old[':question/worked-solution']==r['question'][':question/worked-solution'];counts['source_solutions']+=1
 of=old[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0];assert sorted(v[':answer/value'] for v in of[':answer-field/choices'])==sorted(v[':answer/value'] for v in f[':answer-field/choices']);counts['source_values']+=5
 if of.get(':answer-field/correct'):
  value=next(v[':answer/value'] for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1]);assert value==of[':answer-field/correct'][':answer/value'];counts['source_designations']+=1
 else:counts['source_missing_designations']+=1
 counts['source_questions']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
