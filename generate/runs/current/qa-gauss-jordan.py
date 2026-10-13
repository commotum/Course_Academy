"""Root QA for printed Gauss–Jordan systems, full banks, operation chains and fidelity."""
import importlib.util,json,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186115241;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
p=module('parent_gj_math',R/'gauss-jordan-parser.py');g=module('parent_gj_gen',D.with_suffix('.py'))
counts=dict(source_questions=0,source_values=0,source_designations=0,source_missing_designations=0,source_prompts=0,source_solutions=0,printed_instances=0,bank_values=0,matrix_stages=0,row_operations=0,solved_equations=0,vector_components=0)
def check(record):
 q=record['question'];M=p.system(q[':question/problem']);n=M.cols-1;assert M.rank()==M[:,:-1].rank()<n
 f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];assert len(bank)==5;values=[p.vector(a[':answer/value']) for a in bank];signatures=[p.signature(v) for v in values];assert len(set(signatures))==5
 correct=[]
 for a,v in zip(bank,values):
  if v is not None:
   assert v.rows==n
   if all(s.expand(z)==0 for z in M[:,:-1]*v-M[:,-1]):correct.append(a[':answer/id'])
 assert correct==[f[':answer-field/correct'][1]]
 for k,v in p.stages(q[':question/worked-solution'],M).items():counts[k]+=v
 counts['printed_instances']+=1;counts['bank_values']+=5;return M
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=qs[sid];r=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);M=check(r);assert M==p.system(old[':question/problem']);counts['source_prompts']+=1
 nf=r['question'][':question/answer-fields'][0];f=old[':question/answer-fields'][0];assert sorted(map(str,(p.signature(p.vector(a[':answer/value'])) for a in f[':answer-field/choices'])))==sorted(map(str,(p.signature(p.vector(a[':answer/value'])) for a in nf[':answer-field/choices'])));counts['source_values']+=5
 if f.get(':answer-field/correct'):
  v=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert p.signature(p.vector(v))==p.signature(p.vector(f[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 else:counts['source_missing_designations']+=1
 if old.get(':question/worked-solution'):
  a=old[':question/worked-solution'];b=r['question'][':question/worked-solution'];assert p.prose(a)==p.prose(b);assert p.components(a)==p.components(b);assert p.stages(a,M)==p.stages(b,M);counts['source_solutions']+=1
 counts['source_questions']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
