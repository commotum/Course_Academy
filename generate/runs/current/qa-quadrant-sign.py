"""Root audits exact banks/solutions and proves quadrant signs from printed monomials."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186172039;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
p=module('parent_quad_math',R/'quadrant-sign-parser.py');g=module('parent_quad_gen',D.with_suffix('.py'))
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
source_maps={}
for q in qs.values():
 values=p.read(q[':question/problem'])
 for rel in re.findall(r'!\[.*?\]\((.*?)\)',q.get(':question/worked-solution','')):
  assert rel not in source_maps or source_maps[rel]==values[2];source_maps[rel]=values[2];assert (D/rel).read_bytes()==(Path('/media/jake/SSD/EDB/math')/rel).read_bytes()
counts=dict(source_questions=0,source_values=0,source_designations=0,source_missing_designations=0,source_prompts=0,source_solutions=0,printed_instances=0,bank_values=0,statement_steps=0,sign_inequalities=0,monomial_definitions=0,source_plot_instances=0,authored_plot_instances=0,zero_sets=0)
def check(record):
 q=record['question'];values=p.read(q[':question/problem']);expr,(a,b,c),signs,claims,truth=values;f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];sets=[p.subset(answer[':answer/value']) for answer in bank];true=frozenset(i for i,v in enumerate(truth) if v);assert len(bank)==5 and len(set(sets))==5
 assert [answer[':answer/id'] for answer,z in zip(bank,sets) if z==true]==[f[':answer-field/correct'][1]]
 for key,value in p.stages(q[':question/worked-solution'],values).items():counts[key]+=value
 plots=re.findall(r'!\[.*?\]\((.*?)\)',q[':question/worked-solution']);assert len(plots)==1;rel=plots[0];assert (D/rel).is_file()
 if rel in source_maps:assert source_maps[rel]==signs and b>0;counts['source_plot_instances']+=1
 else:
  side=json.loads((D/rel).with_suffix('.json').read_text());assert tuple(side['spec']['signs'])==signs;assert side['spec']['zero_axes']==(['x'] if b==0 else ['x','y']);counts['authored_plot_instances']+=1
 assert expr.subs(p.x,0)==0
 if b==0:assert expr.subs(p.y,0)==expr
 else:assert expr.subs(p.y,0)==0
 counts['zero_sets']+=1;counts['printed_instances']+=1;counts['bank_values']+=5
 profile=record['generation']['bank_profile']
 if profile in ('authored_cycle','authored_sign_errors'):
  mask=sum(1<<i for i,v in enumerate(truth) if v);expected=[mask,mask^7,mask^1,mask^2,mask^4];actual=[sum(1<<i for i in z) for z in sets];assert sorted(actual)==sorted(expected)
 return values
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=qs[sid];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);assert check(r)==p.read(old[':question/problem']);assert old[':question/problem']==r['question'][':question/problem'];counts['source_prompts']+=1
 if old.get(':question/worked-solution'):assert old[':question/worked-solution']==r['question'][':question/worked-solution'];counts['source_solutions']+=1
 of=old[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']);counts['source_values']+=5
 if of.get(':answer-field/correct'):
  val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert val==of[':answer-field/correct'][':answer/value'];counts['source_designations']+=1
 else:counts['source_missing_designations']+=1
 counts['source_questions']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
