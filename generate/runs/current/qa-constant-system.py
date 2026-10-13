"""Parent verifies every printed parameter-system choice, elimination stage and source."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186115242;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
p=module('parent_constant_math',R/'constant-system-parser.py');g=module('parent_constant_gen',D.with_suffix('.py'))
counts=dict(source_questions=0,source_values=0,source_designations=0,source_prompts_exact=0,source_prompts_repaired=0,source_solutions_exact=0,source_solutions_repaired=0,source_math_solution_repairs=0,printed_instances=0,bank_values=0,matrix_stages=0,row_operations=0,corresponding_equations=0,parameter_claims=0,inline_equations=0)
def repair(text):return re.sub(r'(?<!\\)\{(?=\\begin\{aligned\})',lambda _:r'\{',text)
def check(record):
 q=record['question'];M,root,dependent=p.read(q[':question/problem']);f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];assert len(bank)==5
 vals=[];hits=[]
 for a in bank:
  left,right=a[':answer/value'].split('=',1);assert left=='k';v=p.math(right);vals.append(v)
  yes=p.valid(M,v,dependent);assert yes==(s.simplify(v-root)==0)
  if yes:hits.append(a[':answer/id'])
 assert len(set(vals))==5 and hits==[f[':answer-field/correct'][1]]
 for key,value in p.stages(q[':question/worked-solution'],M,root,dependent).items():counts[key]+=value
 for text in (q[':question/problem'],q[':question/worked-solution']):
  text=re.sub(r'\\[{}]','',text);assert text.count('{')==text.count('}'),text
 counts['printed_instances']+=1;counts['bank_values']+=5;return M,root,dependent
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=qs[sid];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);assert check(r)==p.read(old[':question/problem'])
 assert r['question'][':question/problem']==repair(old[':question/problem']);counts['source_prompts_exact']+=r['question'][':question/problem']==old[':question/problem'];counts['source_prompts_repaired']+=1
 raw=old[':question/worked-solution'];expected=raw
 if sid=='q-74695':expected=expected.replace('x+ky=2','x+ky=-2')
 if sid=='q-42021':expected=expected.replace('1 & 2 & -3','1 & 2 & 3').replace('1-2y=3','x+2y=3')
 counts['source_math_solution_repairs']+=expected!=raw;expected=repair(expected);assert expected==r['question'][':question/worked-solution'],sid;counts['source_solutions_exact']+=expected==raw;counts['source_solutions_repaired']+=1
 oldf=old[':question/answer-fields'][0];f=r['question'][':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in oldf[':answer-field/choices']);counts['source_values']+=5
 val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert val==oldf[':answer-field/correct'][':answer/value'];counts['source_designations']+=1;counts['source_questions']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
