"""Parent reads actual arrays, determinant banks and every worked arithmetic row."""
import importlib.util,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=R.parents[2]/f'generate/scratch/{K}-draft'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_det_reader',R/'determinant-readback.py');s=p.s;g=module('root_det_generator',D.with_suffix('.py'))
C=dict(instances=0,displayed_values=0,determinant_formula_checks=0,actual_matrix_cells=0,arithmetic_stages=0,source_banks=0,source_values=0,source_refs=0,source_missing_refs=0,source_exact_solutions=0,source_exact_prompts=0)
def equivalent(a,b):return s.simplify(s.expand(a-b))==0
def matching(a,b):
 assert len(a)==len(b)
 b=list(b)
 for x in a:
  indices=[i for i,y in enumerate(b) if equivalent(x,y)];assert len(indices)==1,(a,b,x);b.pop(indices[0])
def check(r):
 q=r['question'];a,b,c,d=p.array(q[':question/problem']);answer=s.expand(a*d-b*c);f=q[':question/answer-fields'][0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']]
 assert all(not equivalent(x,y) for i,x in enumerate(vals) for y in vals[i+1:]);assert sum(equivalent(v,answer) for v in vals)==1
 if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if equivalent(v,answer)]==[f[':answer-field/correct'][1]]
 C['displayed_values']+=len(vals)
 if ':question/worked-solution' not in q:return q
 blocks=p.displays(q[':question/worked-solution']);assert len(blocks)==2
 fa,fb,fc,fd=p.array(blocks[0]);rhs=blocks[0].split('=')[-1];assert equivalent(fa*fd-fb*fc,p.scalar(rhs));C['determinant_formula_checks']+=1
 arrays=p.arrays(blocks[1]);assert len(arrays)==1;assert arrays[0][1]==(a,b,c,d);C['actual_matrix_cells']+=8
 arithmetic=[]
 for row in p.rows(blocks[1]):
  assert '& =' in row,row
  raw=row.split('& =')[1].strip()
  if 'MATRIX' in raw:assert re.fullmatch(r'\|?MATRIX0\|?',raw);continue
  assert equivalent(p.scalar(raw),answer),(raw,answer);arithmetic.append(raw);C['arithmetic_stages']+=1
 assert len(arithmetic)>=2
 first=re.sub(r'\s+','',arithmetic[0]);atom=r'(\(-?\d+\)|-?\d+)'
 if r'\cdot' in first:
  m=re.fullmatch(atom+r'\\cdot'+atom+'-'+atom+r'\\cdot'+atom,first);assert m,first
 else:m=re.fullmatch(r'\((-?\d+)\)\((-?\d+)\)-\((-?\d+)\)\((-?\d+)\)',first);assert m,first
 actual=[s.Integer(v.strip('()')) for v in m.groups()];expected=[a,d,c,b] if r['generation']['template']=='named_dot_swapped' else [a,d,b,c];assert actual==expected,(actual,expected)
 C['individual_multiplicands']=C.get('individual_multiplicands',0)+4
 product=re.sub(r'\s+','',arithmetic[1]);m=re.fullmatch(r'(-?\d+)([+-])(\(-?\d+\)|-?\d+)',product);assert m,product
 assert (s.Integer(m[1]),s.Integer(m[3].strip('()'))*(1 if m[2]=='+' else -1))==(a*d,-b*c)
 C['signed_products']=C.get('signed_products',0)+2
 assert arithmetic[0].count(r'\cdot')==2 or arithmetic[0].count('(')>=4,arithmetic[0]
 assert r'\cdot' not in arithmetic[-1]
 level=q[':question/difficulty'].split('/')[-1]
 if level=='hard' and K==17592186059748:assert all(z.is_Integer and 6<=abs(z)<=15 for z in (a,b,c,d)) and 2<=sum(bool(z<0) for z in (a,b,c,d))<=3 and min(abs(a*d),abs(b*c))>=50 and max(map(abs,(a,b,c,d)))>=11
 if level=='hard' and K==17592186059749:
  assert all(z.is_Rational and z.q>1 for z in (a,b,c,d));ad=a*d;bc=b*c;assert ad.q>1 and bc.q>1 and ad.q%bc.q!=0 and bc.q%ad.q!=0
 profile=r['generation'].get('profile',r['generation'].get('bank_profile'))
 if f[':answer-field/type'].endswith('/radio') and profile in ('authored_operations','authored'):
  matching(vals,[answer,a*d+b*c,b*c-a*d,a*d,a*b-c*d])
 if f[':answer-field/type'].endswith('/radio') and profile=='authored-operations':matching(vals,[answer,a*d+b*c,-answer,a*d,-b*c])
 C['instances']+=1;return q
source={q[':question/math-academy-id']:q for q in json.loads((R/'refresh-2026-10-14/sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
cases=json.loads((D/'source-cases.json').read_text())
for case in cases:
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile')));old=source[case['source_id']];sf=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
 assert q[':question/problem']==g.normalize_prose(old[':question/problem']);C['source_exact_prompts']+=1
 matching([p.scalar(a[':answer/value']) for a in sf[':answer-field/choices']],[p.scalar(a[':answer/value']) for a in nf[':answer-field/choices']]);C['source_banks']+=1;C['source_values']+=len(sf[':answer-field/choices'])
 if sf.get(':answer-field/correct'):assert equivalent(p.scalar(sf[':answer-field/correct'][':answer/value']),p.scalar(next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])));C['source_refs']+=1
 else:C['source_missing_refs']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==g.normalize_prose(old[':question/worked-solution']);C['source_exact_solutions']+=1
review=json.loads((D/'review.json').read_text())
if isinstance(review,dict):review=[r for group in review.values() if isinstance(group,list) for r in group]
for r in review:check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(100,135):check(g.generate(level,seed))
import hashlib
C['database_writes']=0;out={'status':'passed','script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'independent_readback':C};(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
