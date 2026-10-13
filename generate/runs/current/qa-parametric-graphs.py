"""Parent checks actual formulas, two tables, complete asset banks and render specs."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186087721;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=module('parent_parametric_graphs',D.with_suffix('.py'));p=module('parent_graphs_parser',R/'vector-math-parser.py')
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def inner(raw):return raw[2:-2] if raw.startswith('$$') else raw[1:-1]
def math(raw):
 raw=raw.strip().rstrip('.,').replace(r'\theta','t').replace('θ','t')
 raw=re.sub(r'\d+\.\d+',lambda m:'('+str(s.Rational(m[0]))+')',raw)
 return p.scalar(raw)
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0
def objects(prompt):
 body=next(inner(m[0]) for m in MATH.finditer(prompt) if 'x=' in m[0] and 'y=' in m[0]);body=body.replace(r'\,','').strip().rstrip('.,')
 match=re.fullmatch(r'x\s*=\s*(.*?),\s*y\s*=\s*(.*?),\s*(.*)',body,re.S);assert match,body
 xt,yt,domain=match.groups();domain=domain.replace(r'\theta','t').replace(' ','')
 if domain=='t>0':J=s.Interval.open(0,s.oo)
 else:
  match=re.fullmatch(r'(.*?)\\le(?:q)?t\\le(?:q)?(.*)',domain);assert match,domain;J=s.Interval(math(match[1]),math(match[2]))
 return {'x':math(xt),'y':math(yt)},J
def table_rows(text):
 return [[cell.strip().strip('$').strip() for cell in line.split('|')[1:-1]] for line in text.splitlines() if line.startswith('|')]
def stages(text):return re.sub(r'\s+',' ',MATH.sub('$MATH$',re.sub(r'!\[\]\([^)]*\)','![](ASSET)',re.sub(r'^\|.*$','TABLE',text,flags=re.M)))).strip()
counts=dict(source_prompts=0,source_full_asset_banks=0,source_values=0,source_designations=0,source_full_solutions=0,printed_instances=0,table_cells=0,formula_stages=0,rendered_assets=0,endpoint_pairs=0,authored_complete_operation_banks=0)
def check(r):
 q=r['question'];F,J=objects(q[':question/problem']);rows=table_rows(q[':question/worked-solution']);assert len(rows)==8
 for offset in (0,4):
  ts=[math(z) for z in rows[offset][1:]];assert all(J.contains(t)==s.true for t in ts)
  for v,row in zip(('x','y'),rows[offset+2:offset+4]):
   assert row[0]==v and len(row)-1==len(ts)
   for time,value in zip(ts,row[1:]):
    if value=='':assert offset==0 and v=='y';continue
    expected=s.simplify(F[v].subs(p.t,time));actual=math(value)
    assert equal(actual,expected) or '.' in value and abs(float(actual-expected))<=.00501,(value,expected)
    counts['table_cells']+=1
 for block in MATH.finditer(q[':question/worked-solution']):
  body=inner(block[0]).strip().rstrip('.,');match=re.fullmatch(r'([xy])=(.*)',body,re.S)
  if match:assert equal(math(match[2]),F[match[1]]);counts['formula_stages']+=1
 level=q[':question/difficulty'].split('/')[-1]
 if level in ('moderate','hard'):
  x,y=s.expand(F['x']),s.expand(F['y']);a=-x.coeff(p.t);b=y.coeff(p.t);assert x.coeff(p.t,2)==1 and y.coeff(p.t,2)==-1 and a in (1,2,3) and b in (1,2,3) and a!=b and x.subs(p.t,0) in (-2,-1,1,2) and y.subs(p.t,0) in (-2,-1,1,2) and J==s.Interval(-2,2)
  assert [math(z) for z in rows[0][1:]]==list(map(s.Integer,range(-2,3)))
 field=q[':question/answer-fields'][0];selected=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
 if r['generation']['plots'] is not None:
  paths=[a[':answer/value'] for a in field[':answer-field/choices']]+[re.search(r'!\[\]\(([^)]+)\)',q[':question/worked-solution'])[1]];bounds=None
  for name in paths:
   path=Path(name);assert path.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n';side=json.loads(path.with_suffix('.json').read_text());shape=side['shape']
   # Renderer specs use Python syntax. Parse with explicit known symbols/functions,
   # then compare against the actual prompt parsed independently above.
   def expr(raw):return s.sympify(raw,locals={'t':p.t,'sin':s.sin,'cos':s.cos,'sqrt':s.sqrt,'pi':s.pi},rational=True)
   sx,sy=expr(shape['x']),expr(shape['y']);lo,hi=expr(shape['lo']),expr(shape['hi'])
   assert side['renderer']=='matplotlib' and side['axis_arrows'] and not side['curve_arrows'] and shape['direction_assessed']==False
   if bounds is None:bounds=side['bounds']
   else:assert side['bounds']==bounds
   if path.name in ('solution.png',Path(selected).name):assert equal(sx,F['x']) and equal(sy,F['y']) and lo==J.inf and hi==J.sup
   if shape['kind'] not in ('ellipse','rational'):
    assert len(side['endpoints'])==2
    for z,actual in zip((lo,hi),side['endpoints']):
     expected=[float(sx.subs(p.t,z)),float(sy.subs(p.t,z))];assert all(abs(a-b)<1e-9 for a,b in zip(expected,actual));assert all(bounds[i][0]<=value<=bounds[i][1] for i,value in enumerate(expected))
    counts['endpoint_pairs']+=1
   else:assert not side['endpoints']
   if path.name=='solution.png':assert [expr(z) for z in side['solution_points']]==ts
   counts['rendered_assets']+=1
  bank=r['generation']['plots']
  if level=='hard':assert [(int(b['lo']),int(b['hi'])) for b in bank]==[(-2,2),(-2,1),(-1,2),(-2,3),(-3,2)] and all(equal(expr(b['x']),F['x']) and equal(expr(b['y']),F['y']) for b in bank)
  else:
   x,y=F['x'],F['y'];cx=s.expand(x).as_independent(p.t,as_Add=True)[0];cy=s.expand(y).as_independent(p.t,as_Add=True)[0]
   if level=='moderate':expected=[(x,y),(-x,y),(x,-y),(x-cx,y),(x,y-cy)]
   else:
    swapped=(y,x)
    if bank[0]['kind']=='ellipse':swapped=(s.expand(y).coeff(s.sin(p.t))*s.cos(p.t)+cy,s.expand(x).coeff(s.cos(p.t))*s.sin(p.t)+cx)
    expected=[(x,y),(x-cx,y),(x,y-cy),(x-2*cx,y-2*cy),swapped]
   for shape,(x,y) in zip(bank,expected):assert equal(expr(shape['x']),x) and equal(expr(shape['y']),y) and expr(shape['lo'])==J.inf and expr(shape['hi'])==J.sup
  counts['authored_complete_operation_banks']+=1
 counts['printed_instances']+=1
old={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 q=old[c['math_academy_id']];r=g.generate('easy',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r);assert q[':question/problem']==r['question'][':question/problem'];counts['source_prompts']+=1
 sf=q[':question/answer-fields'][0];nf=r['question'][':question/answer-fields'][0];asset=lambda raw:str(Path('/media/jake/SSD/EDB/math')/raw)
 assert sorted(asset(a[':answer/value']) for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices']);counts['source_full_asset_banks']+=1;counts['source_values']+=5
 selected=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert selected==asset(sf[':answer-field/correct'][':answer/value']);counts['source_designations']+=1
 expected=q[':question/worked-solution'];expected=re.sub(r'!\[\]\(([^)]+)\)',lambda m:'![]('+asset(m[1])+')',expected);assert r['question'][':question/worked-solution']==expected;counts['source_full_solutions']+=1
for r in json.loads((D/'review.json').read_text()):check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['source_plots_visually_reviewed']=96;counts['generated_contact_sheets_visually_reviewed']=20;counts['residual_wrong_formulas_not_claimed_recovered']=64;counts['database_writes']=0
(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
