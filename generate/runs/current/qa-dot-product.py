"""Parent reads actual components, full banks and ordered dot-product teaching rows."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186059730;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_dot_math',R/'ode-scalar-parser.py');s=p.s;g=module('root_dot_generator',D.with_suffix('.py'))
C=dict(instances=0,displayed_values=0,arithmetic_stages=0,formal_component_rows=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs=0,source_exact_solutions=0,source_exact_prompts=0,source_standalone_repairs=0)
def check(r):
 q=r['question'];problem=q[':question/problem'];pairs=re.findall(r'(?:\\overset\{\\to \}\{([a-z])\}|([a-z]))\s*=\s*⟨(.*?)⟩',problem);assert len(pairs)==2,(problem,pairs)
 names=[a or b for a,b,v in pairs];vectors=[tuple(p.scalar(v) for v in raw.split(',')) for a,b,raw in pairs];a,b=vectors;assert len(a)==len(b) in (2,3);terms=[u*v for u,v in zip(a,b)];answer=sum(terms)
 f=q[':question/answer-fields'][0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(set(vals))==len(vals)
 assert [z[':answer/id'] for z,v in zip(f[':answer-field/choices'],vals) if v==answer]==[f[':answer-field/correct'][1]];C['displayed_values']+=len(vals)
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S);assert len(blocks) in (1,2)
 rows=[row.split('& =',1)[1].strip() for block in blocks for row in block.split(chr(92)*2)];assert len(rows)==4
 formal='+'.join('{'+names[0]+'}_{'+v+r'}\cdot {'+names[1]+'}_{'+v+'}' for v in 'xyz'[:len(a)]);assert rows[0]==formal
 for row in rows[1:]:assert s.simplify(p.scalar(row)-answer)==0,(row,answer);C['arithmetic_stages']+=1
 assert rows[1].count(r'\cdot')==len(a);assert r'\cdot' not in rows[2] and r'\cdot' not in rows[3]
 if r['generation']['bank_profile']=='authored_operations':assert set(vals)=={answer,sum(a)+sum(b),sum(a)*sum(b),sum(terms[1:]),sum(terms[:-1])}
 level=q[':question/difficulty'].split('/')[-1]
 if level=='moderate':assert len(a)==3 and all(z.is_Integer and 2<=abs(z)<=12 for z in a+b) and min(terms)<0<max(terms)
 if level=='hard':assert len(a)==3 and all(1<=abs(z)<=6 and 10%z.q==0 for z in a+b) and sum(z.q!=1 for z in terms)>=2 and min(terms)<0<max(terms)
 C['formal_component_rows']+=1;C['instances']+=1;return q
source={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=source[case['source_id']];sf=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
 assert sorted(p.scalar(a[':answer/value']) for a in sf[':answer-field/choices'])==sorted(p.scalar(a[':answer/value']) for a in nf[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(sf[':answer-field/choices'])
 if sf.get(':answer-field/correct'):
  assert p.scalar(sf[':answer-field/correct'][':answer/value'])==p.scalar(next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]));C['source_existing_refs']+=1
 else:C['source_missing_refs']+=1
 if old.get(':question/worked-solution'):assert old[':question/worked-solution']==q[':question/worked-solution'];C['source_exact_solutions']+=1
 if case['source_id']=='q-168035':assert q[':question/problem'].endswith(old[':question/problem']);C['source_standalone_repairs']+=1
 else:assert old[':question/problem']==q[':question/problem'];C['source_exact_prompts']+=1
for r in json.loads((D/'review.json').read_text())+json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(80,120):check(g.generate(level,seed))
C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
