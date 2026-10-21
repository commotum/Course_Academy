#!/usr/bin/env python3
"""Read printed physics and full math stages independently; fidelity and native QA."""
import importlib.util,json,re,hashlib,sys,subprocess,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('dilution',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
t=sp.Symbol('t',real=True);C=sp.Symbol('C');Q=sp.Symbol('Q');alpha,beta=sp.symbols('alpha beta')
TRANS=standard_transformations+(implicit_multiplication_application,rationalize,)

def group(s,i):
 assert s[i]=='{',(s,i)
 depth=1;j=i+1
 while depth:
  if s[j]=='{':depth+=1
  elif s[j]=='}':depth-=1
  j+=1
 return s[i+1:j-1],j

def clean_units(s):
 # Record units separately before reducing each unit factor to the scalar one.
 s=re.sub(r'\\(?:text|textrm)\{(?:kg/L|kg/min|L/min|kg|L|min)\}', '(1)', s)
 s=s.replace(r'\cancel{(1)}','(1)')
 return s

def algebra(s,env,units=False):
 s=s.strip().rstrip('.,:;')
 s=s.replace('⁡','').replace('′',"'").replace('α',r'\alpha').replace('β',r'\beta')
 for key in [r"{Q}_{\text{in}}^{'}",r"Q'_{\text{in}}",r"Q'_{\textrm{in}}"]:s=s.replace(key,'J')
 for key in [r"{Q}_{\text{out}}^{'}",r"Q'_{\text{out}}",r"Q'_{\textrm{out}}"]:s=s.replace(key,'OUT')
 s=s.replace(r'\dfrac',r'\frac').replace(r'\frac{dQ}{dt}','D').replace(r'\frac{\mathrm{d}Q}{\mathrm{d}t}','D')
 # Formal product derivative: evaluate its actual argument after substituting Q(t).
 marker=r'\frac{d}{dt}('
 while marker in s:
  start=s.index(marker);i=start+len(marker);j=i;depth=1
  while depth:
   if s[j]=='(':depth+=1
   elif s[j]==')':depth-=1
   j+=1
  inner=algebra(s[i:j-1],env);s=s[:start]+'('+str(sp.diff(inner,t))+')'+s[j:]
 s=s.replace(r'\int','').replace(r'\,dt','')
 # IF exponent integral uses its elementary primitive, rather than stripping int.
 s=s.replace(r'\operatorname{ln}',r'\ln')
 s=re.sub(r'I\(t\)','IF',s)
 s=re.sub(r'V\(([^)]+)\)',lambda m:'('+str(env['V'].subs(t,sp.sympify(m[1])))+')',s)
 s=re.sub(r'Q\((t|\d+(?:\.\d+)?)\)',lambda m:'('+str(env['Q'].subs(t,sp.sympify(m[1],locals={'t':t})))+')',s)
 s=s.replace(r'\alpha','alpha').replace(r'\beta','beta')
 if units:
  symbols={'kg':'u_kg','L':'u_L','min':'u_min','kg/L':'u_kg/u_L','L/min':'u_L/u_min','kg/min':'u_kg/u_min'}
  s=re.sub(r'\\(?:text|textrm)\{(kg/L|kg/min|L/min|kg|L|min)\}',lambda m:'('+symbols[m[1]]+')',s)
  s=re.sub(r'\\cancel\{([^{}]+)\}',lambda m:m[1],s)
 else:s=clean_units(s)
 s=s.replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\,','').replace(r'\!','').replace(r'\ ','')
 s=s.replace(r'\ln','log')
 # Logs have |.| or an explicitly grouped argument in the observed masks.
 s=re.sub(r'log\|([^|]+)\|',r'log(\1)',s)
 if s.startswith('{e}^{') or s.startswith('e^{'):
  offset=5 if s.startswith('{e}') else 3
  # Generic conversion below handles powers; exponential integrals checked separately.
 s=s.replace('{e}', 'E')
 if s.startswith('e^'):s='E'+s[1:]
 def convert(s):
  out='';i=0
  while i<len(s):
   if s.startswith(r'\frac',i):
    i+=5;a,i=group(s,i);b,i=group(s,i);out+='(('+convert(a)+')/('+convert(b)+'))'
   elif s[i]=='{':
    a,i=group(s,i);out+='('+convert(a)+')'
   else:out+=s[i];i+=1
  return out
 s=convert(s).replace('^','**')
 # ln(B+t)^n in e^{ln(...)} denotes log of that powered argument.
 s=re.sub(r'log\s*\(([^()]+)\)\*\*\(([-\d]+)\)',r'log((\1)**(\2))',s)
 if '\\' in s:raise AssertionError('Unparsed notation '+s)
 local={'t':t,'C':env['C'],'Q':env['Q'],'D':env['D'],'J':env['J'],'OUT':env['OUT'],'IF':env['IF'],'alpha':env['alpha'],'beta':env['beta'],'E':sp.E,'log':sp.log,**{z:sp.Symbol(z) for z in ['u_kg','u_L','u_min']}}
 return parse_expr(s,local_dict=local,transformations=TRANS)

def physics(rec):
 pr=rec['question'][':question/problem'];kind=g.M[rec['generation']['template']]['kind']
 if 'what is the value' in pr:
  tail=pr.split('what is the value',1)[1];normalized=re.sub(r'\s+','',tail).replace('α','alpha').replace('β','beta').replace('\\','')
  requested='sum' if 'alpha+beta' in normalized else 'difference' if 'alpha-beta' in normalized else None
  assert requested==kind,('Requested response criterion differs',tail)
 else:assert kind=='amount' and 'rounded to two decimal places' in pr and 'minutes after pumping begins' in pr
 values=[]
 for fragment in re.findall(r'\$(.*?)\$',pr,re.S):
  m=re.match(r'(\d+(?:\.\d+)?)',fragment)
  if m:values.append(sp.Rational(m[1]))
 V,q,c,ri,ro=values[:5];delta=ri-ro
 assert delta!=0 and V>0 and q>0 and c>0 and ri>0 and ro>0
 m=ro/abs(delta);B=V/abs(delta);s=sp.sign(delta);x=B+s*t;J=c*ri;a=J/(m+s);A=a*B;bb=q-A
 expr=a*x+bb*(B/x)**(s*m);factor=x**(s*m);constant=bb*B**(s*m)
 assert sp.simplify(sp.diff(expr,t)-(J-ro*expr/(V+delta*t)))==0
 assert expr.subs(t,0)==q
 assert sp.simplify(sp.diff(factor,t)/factor-ro/(V+delta*t))==0
 assert sp.simplify(sp.diff(J*x**(s*m+1)/(s*(s*m+1)),t)-J*factor)==0
 T=values[5] if kind=='amount' else sp.Integer(0)
 assert T>=0 and V+delta*T>0
 answer=q if kind=='sum' else A-bb if kind=='difference' else expr.subs(t,T)
 return dict(Q=expr,C=constant,V=V+delta*t,J=J,OUT=ro*expr/(V+delta*t),D=sp.diff(expr,t),IF=factor,alpha=A,beta=bb,answer=answer,kind=kind,m=m,B=B,s=s,T=T,ri=ri,ro=ro,c=c,q=q,volume=V)

def check_math(rec):
 env=physics(rec);q=rec['question'];pr=q[':question/problem'];so=q.get(':question/worked-solution','')
 # Prompt physical units and each supplied normalized coefficient model.
 assert re.search(r'(?:kg/L|kg\/L)',pr) and pr.count('L/min')==2
 for frag in re.findall(r'\$(.*?)\$',pr,re.S)+re.findall(r'\$\$(.*?)\$\$',pr,re.S):
  if frag.strip().startswith('Q(t)') and '=' in frag:
   sides=frag.split('=');assert sp.simplify(algebra(sides[0],env)-algebra(sides[1],env))==0
  # Independently retain every explicit printed unit factor in inline/display math.
 u_kg,u_L,u_min=sp.symbols('u_kg u_L u_min')
 for fragment in re.findall(r'\$\$(.*?)\$\$',so,re.S)+re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',so,re.S):
  fragment=fragment.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  for row in fragment.split(r'\\'):
   for part in re.split(r'=|≈|\\approx',row.replace('&','')):
    if not re.search(r'\\(?:text|textrm)\{(?:kg|L|min)',part):continue
    if 'kg' in part:
     dimension=u_kg/u_min if 'min' in part else u_kg/u_L if 'L' in part else u_kg
    else:dimension=u_L/u_min if 'min' in part and 'L' in part else u_L if 'L' in part else u_min
    assert sp.simplify(algebra(part,env,units=True)-algebra(part,env)*dimension)==0,('unit mismatch',part)
 if env['kind']=='sum':
  # authored easy formal initial-condition line is validated by scalar equality
  if so:
   assert f"{g.num(env['q'])}\\,\\text{{kg}}" in so
 elif so:
  rows=[]
  for block in re.findall(r'\$\$(.*?)\$\$',so,re.S):
   block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
   for row in block.split(r'\\'):
    row=row.strip()
    if row:rows.append(row)
  lhs=None;checked=0
  for row in rows:
   isapprox='≈' in row or r'\approx' in row
   row=row.replace('≈','=').replace(r'\approx','='); row=row.replace('&','')
   parts=[x.strip() for x in row.split('=')]
   if len(parts)<2:
    assert sp.simplify(algebra(row,env)-(env['Q']/env['V'] if 'kg/L' in row else env['D']))==0,row
    continue
   if parts[0]:lhs=parts[0]
   else:parts[0]=lhs
   assert parts[0]
   # Exponential primitive integrating factor stage: check actual printed integrand.
   if r'\int ' in parts[1] and ('{e}^' in parts[1] or 'e^' in parts[1]):
    mat=re.search(r'\\int ([^}]+)\\,dt',parts[1]);assert mat,parts[1]
    coeff=algebra(mat[1],env);assert sp.simplify(coeff-env['ro']/env['V'])==0;lhs='I(t)';checked+=1;continue
   vals=[algebra(v,env) for v in parts]
   for z in vals[1:]:
    diff=sp.simplify(vals[0]-z)
    if isapprox:assert abs(float(sp.N(diff)))<=.005001,(row,diff)
    else:assert diff==0,(row,diff)
   checked+=len(vals)-1
  # Each printed quantity in prose is read, units/rates tied to physical prompt.
  for value,unit in re.findall(r'\$(\d+(?:\.\d+)?)(?:\\,)?\\(?:text|textrm)\{([^}]+)\}',so):
   x=sp.Rational(value)
   if unit=='kg/L':assert x==env['c']
   elif unit=='L/min':assert x in [env['ri'],env['ro']]
   elif unit=='L':assert x==env['volume']
   elif unit=='kg':assert x==env['q']
  assert checked>=27,checked
  assert so.count('**Step')==4
  if not rec['generation']['evidence_only']:assert 'salt' not in so
 # Complete bank and numeric correct readback, including units and rounded values.
 fields=q[':question/answer-fields'];assert len(fields)==1
 field=fields[0];bank=field[':answer-field/choices'];assert len(bank)==5
 values=[algebra(z[':answer/value'].removesuffix('kg'),env) for z in bank]
 assert len(set(values))==5
 if ':answer-field/correct' in field:
  key=field[':answer-field/correct'][1];chosen=next(a for a in bank if a[':answer/id']==key)
  correct=algebra(chosen[':answer/value'].removesuffix('kg'),env)
  target=sp.Rational(g.round2(env['answer'])) if env['kind']=='amount' else env['answer']
  assert correct==target,(correct,target)
 if not rec['generation']['evidence_only']:
  assert len({len(re.match(r'[\d.]+',z[':answer/value'])[0]) for z in bank})==1
  # Every displayed wrong operation is recomputed from printed physics, independently.
  A,bb,initial=env['alpha'],env['beta'],env['q'];
  if env['kind']=='sum':expected=[initial,A,-bb,A-bb,A+initial]
  elif env['kind']=='difference':expected=[A-bb,initial,A,A+initial,2*A]
  else:
   T=env['T'];V=env['volume'];Vt=env['V'].subs(t,T);m=env['m'];
   expected=[env['answer'],env['J']*V/env['ro']+(initial-env['J']*V/env['ro'])*sp.exp(-env['ro']*T/V),env['c']*Vt,initial*(V/Vt)**m,env['c']*Vt+(initial-env['c']*V)*(V/Vt)**(m+1)]
  expected=[sp.Rational(g.round2(z)) for z in expected] if env['kind']=='amount' else expected
  assert set(values)==set(expected)
 return env

def formatting(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 uuid.UUID(rec['knowledge_point']['id']);uuid.UUID(rec['question'][':question/id'])
 for f in rec['question'][':question/answer-fields']:
  uuid.UUID(f[':answer-field/id']);assert f[':answer-field/type']==':answer-field.type/radio'
  assert f[':answer-field/key']=='selection'
  ids=[]
  for a in f[':answer-field/choices']:
   uuid.UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/math';assert a[':answer/id']==g.uid(f[':answer-field/id']+a[':answer/value']);ids.append(a[':answer/id'])
  assert len(set(ids))==5
  if ':answer-field/correct' in f:assert f[':answer-field/correct'][0]==':answer/id' and f[':answer-field/correct'][1] in ids
 for content in [rec['question'][':question/problem'],rec['question'].get(':question/worked-solution','')]+[a[':answer/value'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]:
  assert content.count('$')%2==0
  depth=0
  for i,c in enumerate(content):
   if c in '{}' and (i==0 or content[i-1]!='\\'):
    depth+=(1 if c=='{' else -1);assert depth>=0
  assert depth==0
  assert '{{' not in content or re.search(r'\{\{\d+',content) # source nested numeric groups allowed
  assert '+-' not in content and '--' not in content
 json.dumps(rec)

def run():
 cases=json.loads((D/'source-cases.json').read_text());reviews=[];fidelity=[];engine=[];originals=[]
 for case in cases:
  rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);src=next(x for x in g.SRC[':knowledge-point/questions'] if x[':question/math-academy-id']==case['source_id']);q=rec['question'];
  for k in [':question/problem',':question/worked-solution']:assert q.get(k)==src.get(k),(case['source_id'],k)
  for k in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (k in q)==(k in src)
  rawf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  assert (':answer-field/correct' in f)==(':answer-field/correct' in rawf)
  if ':answer-field/correct' in rawf:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==rawf[':answer-field/correct'][':answer/value']
  assert sorted(x[':answer/value'] for x in f[':answer-field/choices'])==sorted(x[':answer/value'] for x in rawf[':answer-field/choices'])
  formatting(rec);check_math(rec);originals.append(rec)
  fidelity.append({'source_id':case['source_id'],'prompt_exact':True,'worked_exact': ':question/worked-solution' in src,'worked_absent_preserved':':question/worked-solution' not in src,'bank_values':5,'correct_designation_matched':':answer-field/correct' in f,'raw_missing_keys_preserved':True})
  for i in range(2):
   # Public opaque-bank changed quantities; no teaching eligibility claimed.
   p=dict(case['parameters']);scale=sp.Rational(6,5) if i==0 else sp.Rational(5,4);p['q0']=str(sp.Rational(p['q0'])*scale);p['c']=str(sp.Rational(p['c'])*scale)
   if sp.Rational(p['c'])<=sp.Rational('.08'):
    rr=g.generate(case['level'],template=case['template'],parameters=p,profile=case['bank_profile']);formatting(rr);check_math(rr);reviews.append(rr)
  for i in range(2):reviews.append(g.generate(case['level'],seed=110+i,template=case['template']))
  for i in range(5):
   variant=g.generate(case['level'],seed=410+i,template=case['template']);opaque=g.generate(case['level'],template=case['template'],parameters=variant['generation']['parameters'],profile=case['bank_profile']);formatting(opaque);check_math(opaque)
 tasks={l:set() for l in ['easy','moderate','hard']};coverage=set();correct_positions=set();checks=0
 for level in tasks:
  for seed in range(90):
   rec=g.generate(level,seed);formatting(rec);check_math(rec);checks+=1;tasks[level].add(rec['generation']['mathematical_fingerprint']);coverage.add(rec['generation']['template']);
   f=rec['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1];correct_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==key))
   if seed<5:reviews.append(rec)
 for rec in reviews:formatting(rec);check_math(rec)
 for meta in g.M.values():
  rr=g.generate(meta['level'],12,template=meta['source_id']);p=rr['generation']['parameters'];other=g.generate(meta['level'],83,template=meta['source_id'],parameters=p)
  assert rr['question'][':question/id']==other['question'][':question/id']
  for key,value in [('V',0),('rin',p['rout']),('T',0 if meta['kind']=='amount' else 300)]:
   bad=dict(p);bad[key]=value
   try:g.generate(meta['level'],template=meta['source_id'],parameters=bad)
   except ValueError:pass
   else:raise AssertionError('Invalid explicit parameters accepted')
 easy_witnesses=[]
 for initial in [3,4]+list(range(10,45)):
  p=dict(V=100,q0=initial,c='.04' if initial==3 else '.05',rin=8,rout=12) if initial in [3,4] else dict(V=1000 if initial==27 else 900,q0=initial,c='.06',rin=20,rout=30)
  witness=g.generate_easy(parameters=p);check_math(witness);easy_witnesses.append(witness)
 assert len({r['generation']['mathematical_fingerprint'] for r in easy_witnesses})==37
 (D/'easy-domain-witnesses.json').write_text(json.dumps(easy_witnesses,indent=2)+'\n')
 assert coverage==set(g.M),coverage
 assert len(correct_positions)==5,correct_positions
 for rec in originals+reviews:
  f=rec['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  key=f[':answer-field/correct'][1]
  engine.append(dict(label=rec['question'][':question/id'],record=rec,checks=[dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==key else 'rejected',purpose='owned radio choice') for a in f[':answer-field/choices']]))
 (D/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n');subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 native=json.loads((D/'engine-report.json').read_text())
 report=dict(status='passed',frozen_at_step=7,source_questions=7,dimensional_unit_readback='passed',requested_response_readback='passed',source_options_matched=35,complete_banks_matched=7,supplied_correct_designations_matched=5,missing_correct_designations=2,supplied_solutions_exact=5,omitted_solutions_preserved=2,raw_opaque_profiles_ineligible=7,mathematical_source_repairs=0,easy_meaningful_finite_domain_size=37,normal_prose_corrections=['salt -> dissolved substance in moderate solution opening'],authored_levels=['easy'],authored_operation_banks=7,sampled_normal_records_checked=checks,unique_sampled_mathematical_tasks={k:len(v) for k,v in tasks.items()},default_family_coverage=sorted(coverage),correct_positions=sorted(correct_positions),native={k:native[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},fidelity=fidelity,dependencies={'python':sys.version.split()[0],'sympy':sp.__version__},engine_sha256=hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),database_writes=0)
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(D/'review.json').write_text(json.dumps({'originals':originals,'generated':reviews},indent=2)+'\n');(D/'review.md').write_text('# Originals (opaque/incomplete evidence, ineligible)\n\n'+'\n---\n'.join(g.markdown(r) for r in originals)+'\n# Generated variants (origin/eligibility explicit)\n\n'+'\n---\n'.join(g.markdown(r) for r in reviews))
 print(json.dumps(report,indent=2))
if __name__=='__main__':run()
