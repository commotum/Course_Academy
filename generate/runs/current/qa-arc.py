"""Root oracle integrates printed coordinates, independent of generator data()."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parent;K=17592186092377;D=R.parents[2]/f'generate/scratch/{K}'
spec=importlib.util.spec_from_file_location('parent_arc',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
T=g.T;mp.mp.dps=45
counts={'source_banks':0,'source_values':0,'source_wrong_values':0,'source_correct_refs':0,'source_shared_prose':0,'printed_curves_integrated':0,'prefilled_fragments_checked':0,'printed_derivative_rows':0,'normal_default_exact_instructions':0}
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
def inspect(r):
 q=r['question'];prompt=q[':question/problem']
 m=re.search(r'x=(.*?),\\,y=(.*?),\\,t\\in \[(.*?),(.*?)\]',prompt,re.S);assert m,prompt
 x,y,a,b=map(g.parse_tex,m.groups());assert b>a
 dx,dy=s.diff(x,T),s.diff(y,T);squared=s.trigsimp(s.expand(dx**2+dy**2))
 # 45-digit quadrature of the actual printed coordinate derivatives. Split
 # the interval to handle zero-speed endpoints without relying on metadata.
 integrand=s.lambdify(T,s.sqrt(squared),'mpmath');lo=mp.mpf(str(s.N(a,48)));hi=mp.mpf(str(s.N(b,48)))
 val=mp.quad(integrand,[lo,lo+(hi-lo)/4,lo+(hi-lo)/2,lo+3*(hi-lo)/4,hi])
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];correct=field[':answer-field/correct'][1]
 prefix=s.Integer(1)
 if '$L=' in prompt and '(${{field-1}}$)' in prompt:
  prefix=g.parse_tex(re.search(r'\$L=(.*?)\(\$',prompt).group(1));counts['prefilled_fragments_checked']+=1
 truth=[]
 for c in choices:
  answer=prefix*g.parse_tex(c[':answer/value']);number=mp.mpf(str(s.N(answer,48)))
  assert number>0
  if abs(number-val)<mp.mpf('1e-37')*max(1,abs(val)):truth.append(c[':answer/id'])
 assert truth==[correct],(prompt,val,truth)
 for i,c in enumerate(choices):
  assert all(not same(g.parse_tex(c[':answer/value']),g.parse_tex(d[':answer/value'])) for d in choices[i+1:])
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
 for block,expected in zip(blocks[1:3],(dx,dy)):
  for chunk in block.split('=')[1:]:
   if r'\frac{\text{d}}' in chunk:continue
   expr=chunk.split(r'\end{aligned}')[0].split(r'\\')[0].replace('&','').strip().rstrip('.,')
   assert same(g.parse_tex(expr),expected),expr;counts['printed_derivative_rows']+=1
 if r['generation'].get('bank_profile')!='observed' and field[':answer-field/type'].endswith('/blank'):
  assert 'round' not in prompt.lower()
  if 'Do not round' in g.TEMPLATES[r['generation']['template']]['source'][':question/problem']:
   assert 'Give an exact answer.' in prompt;counts['normal_default_exact_instructions']+=1
 counts['printed_curves_integrated']+=1
raw=json.loads((R/'sources'/f'{K}.json').read_text())['record'];sources={q[':question/math-academy-id']:q for q in raw[':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_ma_id']];r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);f=r['question'][':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'] and f[':answer-field/key']==of[':answer-field/key']
 actual=[g.parse_tex(a[':answer/value']) for a in f[':answer-field/choices']]
 for a in of[':answer-field/choices']:assert sum(same(g.parse_tex(a[':answer/value']),v) for v in actual)==1;counts['source_values']+=1
 selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert same(g.parse_tex(selected),g.parse_tex(of[':answer-field/correct'][':answer/value']))
 old_prose=re.sub(r'\$\$.*?\$\$','MATH',old[':question/worked-solution'],flags=re.S);new_prose=re.sub(r'\$\$.*?\$\$','MATH',r['question'][':question/worked-solution'],flags=re.S);assert old_prose==new_prose
 inspect(r);counts['source_banks']+=1;counts['source_wrong_values']+=len(actual)-1;counts['source_correct_refs']+=1;counts['source_shared_prose']+=1
records=json.loads((D/'review.json').read_text())+[x['record'] for x in json.loads((D/'engine-input.json').read_text())];seen=set()
for r in records:
 ident=r['question'][':question/id']
 if ident in seen:continue
 seen.add(ident);inspect(r)
counts['distinct_existing_review_and_boundary_records']=len(seen);counts['independent_numeric_precision_digits']=45;counts['database_writes']=0
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
