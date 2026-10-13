"""Root oracle reads actual product functions, formal rows and slopes."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186096619;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_slope_parser',R/'product-readback.py');g=module('root_slope_generator',D.with_suffix('.py'));s=p.s;x=p.x
def same(a,b):return s.simplify(s.trigsimp(a-b))==0
C=dict(instances=0,values=0,formal_argument_checks=0,derivative_equations=0,evaluated_equations=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs=0,source_fieldless=0,source_normalized_prose=0)
def spans(text):return [m[1] if m[1] is not None else m[2] for m in re.finditer(r'\$\$([\s\S]*?)\$\$|\$([^$]*)\$',text)]
def tex(expr):return '('+s.latex(expr).replace(r'\log',r'\ln')+')'
def read(raw,functions):
 raw=raw.strip().rstrip('.,')
 raw=re.sub(r'\\frac\{\\mathrm d([yuvfh])\}\{\\mathrm dx\}',lambda m:tex(s.diff(functions[m[1]],x)),raw)
 operator=r'\frac{\mathrm d}{\mathrm dx}'
 while operator in raw:
  at=raw.index(operator);start=at+len(operator)
  while raw[start].isspace():start+=1
  assert raw[start]=='(',raw
  depth=0
  for n in range(start,len(raw)):
   if raw[n]=='(':depth+=1
   elif raw[n]==')':
    depth-=1
    if not depth:break
  arg=read(raw[start+1:n],functions);raw=raw[:at]+tex(s.diff(arg,x))+raw[n+1:];C['formal_argument_checks']+=1
 # Resolve named functions and their derivatives before bare component symbols.
 for name,expr in functions.items():
  raw=re.sub(name+r"'\s*\(x\)",lambda m:tex(s.diff(expr,x)),raw)
  raw=re.sub(name+r'\s*\(x\)',lambda m:tex(expr),raw)
 raw=re.sub(r'\\[A-Za-z]+|[uvfh]',lambda m:m[0] if m[0].startswith('\\') else tex(functions[m[0]]),raw)
 return p.scalar(raw)
def point_expr(raw,t,functions):
 # Normal generated evaluation bars always bind the displayed question point.
 raw=raw.replace(r'\left.','')
 m=re.search(r'\\right\|_\{x=(.*)\}$',raw)
 if m:
  assert same(p.scalar(m[1]),t);raw=raw[:m.start()]
 return read(raw,functions).subs(x,t)
def rows(block):
 block=re.sub(r'\\(?:begin|end)\{aligned\}','',block)
 return [z.replace('&','').strip().rstrip('.,') for z in block.split(r'\\') if '=' in z]
def prose(text):return re.sub(r'\s+',' ',re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$','<math>',text)).strip()
def structure(worked):
 blocks=[z for z in spans(worked) if r'\begin{aligned}' in z]
 return [len(rows(z)) for z in blocks]
def check(record):
 q=record['question'];prompt=q[':question/problem'];worked=q[':question/worked-solution'];ms=spans(prompt)
 defs={z.split('=',1)[0][0]:p.scalar(z.split('=',1)[1].rstrip('.,')) for z in ms if re.match(r'[fh]\(x\)=',z)}
 y=next(z.split('=',1)[1].rstrip('.,') for z in ms if re.match(r'y\s*=',z));F=read(y,defs)
 t=p.scalar(next(z.split('=',1)[1].rstrip('.,') for z in ms if re.match(r'x\s*=',z)))
 slope=s.diff(F,x).subs(x,t);assert not slope.has(s.zoo,s.nan,s.oo,-s.oo)
 funcs={name:p.scalar(raw.rstrip('.,')) for name,raw in re.findall(r'\$([uvfh])\(x\)=(.*?)\$',worked,re.S)}
 assert len(funcs)==2 and same(s.prod(funcs.values()),F);funcs['y']=F
 initial,rest=worked.split('Applying the product rule gives',1);product,evaluation=rest.split('To find the slope of the tangent line',1)
 for block in re.findall(r'\$\$(.*?)\$\$',initial,re.S):
  if r'\begin{aligned}' in block:
   rr=rows(block);assert len(rr)==2
  else:rr=re.split(r',\\quad\s*',block.strip())
  assert len(rr)==2
  for row in rr:
   vals=[read(z,funcs) for z in row.split('=')];assert len(vals)>=2 and all(same(z,vals[0]) for z in vals[1:]),row;C['derivative_equations']+=len(vals)-1
 for block in re.findall(r'\$\$(.*?)\$\$',product,re.S):
  carry=None
  for row in rows(block):
   parts=row.split('=');carry=parts[0] or carry;assert carry
   vals=[read(z,funcs) for z in [carry]+parts[1:]];assert all(same(z,s.diff(F,x)) for z in vals),row;C['derivative_equations']+=len(vals)-1
 for block in re.findall(r'\$\$(.*?)\$\$',evaluation,re.S):
  for row in rows(block):
   row=re.sub(r'\\right\|_\{x=(.*?)\}',lambda m:r'\right|_{x:'+m[1]+'}',row)
   parts=row.split('=',1);rhs=parts[1]
   # Evaluation-bar subscripts contain an equals sign, unlike subsequent values.
   rhs=re.sub(r'\\right\|_\{x=(.*?)\}',lambda m:r'\right|_{x:'+m[1]+'}',rhs)
   pieces=rhs.split('=')
   for z in pieces:
    z=z.replace(r'\right|_{x:',r'\right|_{x=');assert same(point_expr(z,t,funcs),slope),(row,z,slope);C['evaluated_equations']+=1
 f=q[':question/answer-fields'][0];vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];good=[same(z,slope) for z in vals]
 assert sum(good)==1 and good[next(n for n,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])]
 for n,a in enumerate(vals):assert all(not same(a,b) for b in vals[:n])
 final=spans(worked)[-1];assert same(p.scalar(final.rstrip('.,')),slope)
 if q[':question/difficulty'].endswith('/hard'):
  u,v=[z for name,z in funcs.items() if name!='y'];poly=u if u.is_polynomial(x) else v;other=v if u.is_polynomial(x) else u
  pp=s.Poly(poly,x);assert pp.degree()==2 and len(pp.terms())==3 and all(0<abs(coef)<=5 for _,coef in pp.terms())
  assert s.diff(poly,x).subs(x,t)!=0 and poly.subs(x,t)!=0 and other.subs(x,t)!=0 and s.diff(other,x).subs(x,t)!=0
  assert structure(worked)==[3,3]
 C['instances']+=1;C['values']+=len(vals);return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];new=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']))
 if old.get(':question/worked-solution'):
  assert prose(old[':question/worked-solution'])==prose(new[':question/worked-solution']);assert structure(old[':question/worked-solution'])==structure(new[':question/worked-solution']);C['source_normalized_prose']+=1
 fields=old.get(':question/answer-fields',[])
 if not fields:C['source_fieldless']+=1;C['source_missing_refs']+=1
 for of,nf in zip(fields,new[':question/answer-fields']):
  pending=[p.scalar(z[':answer/value']) for z in nf[':answer-field/choices']]
  for z in of[':answer-field/choices']:
   value=p.scalar(z[':answer/value']);n=next(n for n,b in enumerate(pending) if same(value,b));pending.pop(n);C['source_values']+=1
  assert not pending;C['source_banks']+=1
  if of.get(':answer-field/correct'):
   actual=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert same(p.scalar(actual),p.scalar(of[':answer-field/correct'][':answer/value']));C['source_existing_refs']+=1
  else:C['source_missing_refs']+=1
for record in json.loads((D/'review.json').read_text())+json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(record)
C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
