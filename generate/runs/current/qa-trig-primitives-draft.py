"""Root full direct-trig banks and every displayed formal integral stage."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);sys.modules[n]=m;z.loader.exec_module(m);return m
G=mod('root_trig_generator',D.with_suffix('.py'));P=mod('root_trig_reader',R/'trig-primitive-readback.py');F=mod('root_trig_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
C=dict(records=0,actual_integrands=0,formal_integral_inputs=0,displayed_equalities=0,primitive_derivatives=0,values=0,pairs=0,whole_banks=0,grade_guards=0,documented_raw_errors=0,unresolved_raw_integrands=0,blank_fragments=0)
def bank(t,p,e,v):
 a=s.Rational(p.get('a',0));b=s.Rational(p.get('b',0));c=s.Rational(p.get('c',0));F=P.primitive(e,v);S,T,U,V,W,Z=s.sin(v),s.cos(v),s.sec(v),s.csc(v),s.tan(v),s.cot(v)
 if K==17592186064179:
  if t=='q-113920':return [a*V*Z,-a*V,a*V,a*U,-a*U]
  if t=='q-71656':return [a*V,-a*U,a*U,-a*V,a*V*Z]
  if t=='q-71659':return [a*U,V**a,-a*U,-a*V,U**a]
  if t=='q-113926':return [-a*T-b*V,a*T+b*V**2,-a*T+b*V,a*T+b*U,-a*T-b*Z]
  if t=='q-113928':return [-U+b*S,-U-b*S,W**2+b*S,W-b*S,U-b*S]
  if t=='q-113930':return [(a+b)*U**2,-a*W+b*Z,a*U-b*V,-a*U-b*Z,a*U+b*V]
  parts=[P.primitive(z,v) for z in s.Add.make_args(s.expand(e))]
  if len(parts)==1:return [F,-F,a*U,-a*U,e]
  A,B=parts;return [F,-A+B,A-B,-F,e]
 if K==17592186064180:
  if t=='q-113936':return [a*U,-a*V,-V**2,W**2,a*W]
  if t=='q-113937':return [-a*U,a*W,a*U**2,a*Z,-a*W]
  if t=='q-113944':return [W+b*V,Z-b*V**2,W-b*Z,Z+b*V,-W+b*V**2]
  if t=='q-2164':return [b*V+W,-b*V-W,b*V+U,-b*Z+W,-b*V+W]
  if t=='q-49122':return [-a*W+b*V,-a*W-b*V,a*W+b*U,a*Z+b*U,a*Z-b*U]
  if t=='fraction':a=-s.Rational(p['n'],p['d']);return [a*W,-a*W,a*U,a*Z,a*U**2]
  if t=='single-positive':return [a*W,a*Z,a*U*W,a*U,a*V]
  if t=='sine-sum':return [F,a*W-b*T,a*U**2+b*T,a*Z+b*T,a*W+b*S]
  if t=='secant-difference':return [F,-a*U-b*W,a*U+b*W,a*U-b*U**2,a*U-b*Z]
  if t=='reverse-product':return [F,a*W-b*U,-a*W+b*U,a*Z+b*U,a*W+b*V]
  sign=1 if t=='three-term-plus' else -1;return [F,a*W+b*U+sign*c*V,-a*W+b*U-sign*c*V,a*U**2+b*U-sign*c*V,a*W+b*U-sign*c*Z]
 if K==17592186064178:
  if t=='q-113907':return [-T/a,a*T,-a*S,a*S,-a*T]
  if t=='q-113908':return [-S/a,S/a,a*T,a*S,-a*T]
  if t in ('q-113909','sum'):return [F,a*S+b*T,a*T-b*S,b*T-a*S,b*S-a*T]
  if t=='q-2161':return [-a*S-b*T,-a*S+b*T,(a+b)*S,a*S+b*T,a*S-b*T]
  if t=='grouped':return [F,(a-b)*S-(a+b)*T,a*S-b*T,(a+b)*T-(b-a)*S,-(a+b)*S+(b-a)*T]
  assert t in ('sin','cos');base=-T if t=='sin' else S;return [F,-F,-base/a,e,-e]
 if K==17592186064181:
  if t=='q-113947':return [-a*V*Z,a*U*W,-a*Z,-a*W,a*Z]
  if t=='q-71663':return [a*W,a*Z,-a*W,-a*Z,a*V*Z]
  if t=='q-49121':return [-a*V-b*Z,-b*T+b*W,a*V-b*U,-a*V-b*W,a*S**3-b*Z]
  if t=='fraction':a=s.Rational(p['n'],p['d']);return [a*Z,-a*Z,a*W,a*V,a*V**2]
  if t=='single-negative':return [a*Z,a*U*W,a*W,-a*W,-a*Z]
  if t=='secant-difference':return [F,a*Z-b*U,-a*Z+b*U,-a*W-b*U,-a*Z-b*U*W]
  if t=='sine-difference':return [F,T+a*Z,-T-a*Z,-S+a*Z,-T+a*W]
  if t=='reverse-product':return [F,a*Z+b*V,-a*Z-b*V,-a*W+b*V,-a*Z+b*Z]
  if t=='three-term':return [F,-a*U+b*Z-c*T,a*U-b*Z-c*T,a*U+b*Z+c*T,-F]
 raise AssertionError(('unmapped root bank',K,t))
def check(r,raw=False):
 q,m=r['question'],r['generation'];t=m['template'];prompt=q[':question/problem'];sol=q.get(':question/worked-solution')
 if 'h(x)' in prompt:
  if raw:assert K==17592186064178 and not m['eligible_for_learning'] and m['domain']['status']=='unresolved';C['unresolved_raw_integrands']+=1;C['records']+=1;return
  definition=re.search(r'Given \$h\(x\)=(.*?)\$',prompt);assert definition;e=P.scalar(definition[1]);assert e==-s.Rational(m['parameters']['a'])*s.sin(P.P.x)
  prompt=prompt.replace('h(x)','('+definition[1]+')');sol=sol.replace('h(x)','('+definition[1]+')')
 if 'v(t)' in prompt:
  if raw:assert K==17592186064181 and not m['eligible_for_learning'];C['unresolved_raw_integrands']+=1;C['records']+=1;return
  definition=re.search(r'Given \$v\(t\)=(.*?)\$',prompt);assert definition;e=P.scalar(definition[1]);assert e==s.Rational(m['parameters']['a'])*s.csc(P.P.t)**2
  prompt=prompt.replace('v(t)','('+definition[1]+')');sol=sol.replace('v(t)','('+definition[1]+')')
 e,v=P.integral(prompt);C['actual_integrands']+=1
 if not raw:
  level=q[':question/difficulty'].split('/')[-1];terms=s.Add.make_args(s.expand(e));assert all(f.args[0]==v for f in e.atoms(s.Function))
  if level=='easy':assert len(terms)==1
  elif level=='moderate':assert len(terms)==2
  else:assert len(terms)==(3 if K in (17592186064180,17592186064181) else 2)
  if K==17592186064179 and level=='hard':assert all(s.Rational(z).q>1 for z in m['parameters'].values())
  if K==17592186064178:
   assert all(f.func in (s.sin,s.cos) for f in e.atoms(s.Function));d=m['domain'];assert d['status']=='established' and d['independent_variable']=={P.P.x:'x',P.P.y:'y',P.P.u:r'\theta'}[v]
   assert d['integrand_domain']==d['correct_primitive_domain']=='All real values of the independent variable.' and d['integration_constant']['range']=='all real numbers'
  else:assert 'pole' in m['domain'] and 'C' in m['domain']
  C['grade_guards']+=1
 if sol:
  assert 'Recall that' in sol and 'Therefore,' in sol;blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==2
  for bi,block in enumerate(blocks):
   prior=None;rows=re.split(r'\\\\|\\qquad',block.replace(r'\begin{aligned}','').replace(r'\end{aligned}',''))
   for row in rows:
    if raw and K==17592186064179 and t=='q-113925' and r'\operatorname{cos}\operatorname{csc}' in row:
     assert row.count(r'\int')==3;prior=P.primitive(e,v);C['documented_raw_errors']+=1;continue
    if raw and K==17592186064181 and t=='q-113958' and r'\int sin\,' in row:
     assert bi==0;C['documented_raw_errors']+=1;continue
    parts=row.replace('&','').strip().rstrip('.,').split('=');assert len(parts)>=2;vals=[]
    for ii,part in enumerate(parts):
     if not part.strip():assert ii==0 and prior is not None;value=prior;formal=[]
     else:value,formal=P.expression(part)
     if formal:
      assert all(zv==v for body,zv in formal);C['formal_integral_inputs']+=len(formal)
     if not raw:assert value.free_symbols<={v,P.CONST},('stale variable',row,value,v)
     vals.append(value)
    for a,b in zip(vals,vals[1:]):
     ok=P.zero(s.diff(a-b,v))
     if not ok and raw and K==17592186064179 and t=='q-113925' and r'\operatorname{cos}\operatorname{csc}' in row:C['documented_raw_errors']+=1
     else:assert ok,(t,row,vals)
     C['displayed_equalities']+=1
    if bi==1:assert P.zero(s.diff(vals[-1],v)-e) or raw and K==17592186064179 and t=='q-113925' and r'\operatorname{cos}\operatorname{csc}' in row
    prior=vals[-1]
   if bi==1:assert P.zero(s.diff(prior,v)-e);C['primitive_derivatives']+=1
  if not raw and K==17592186064180 and m['template'].startswith('three-term'):
   assert len(rows)==5 and rows[0].count(r'\int')==2 and rows[1].count(r'\int')==3 and rows[2].count(r'\int')==3 and '+C' in rows[3] and '+C' in rows[4]
  if not raw and K==17592186064178 and m['template']=='grouped':
   assert len(rows)==5 and [row.count(r'\int') for row in rows]==[2,1,2,0,0]
   assert rows[0].count(r'\cos')==4 and rows[0].count(r'\sin')==4 and rows[1].count(r'\cos')==rows[1].count(r'\sin')==1
 fields=q.get(':question/answer-fields',[])
 for f in fields:
  vals=[]
  for a in f.get(':answer-field/choices',[]):
   if raw and K==17592186064181 and t=='q-71666' and re.search(r'(?<![A-Za-z])csc[+-]',a[':answer/value']):vals.append(None);C['documented_raw_errors']+=1
   else:vals.append(P.scalar(a[':answer/value']))
  C['values']+=len(vals)
  if not raw:
   assert all(a.free_symbols<={v,P.CONST} for a in vals)
   if f[':answer-field/type']==':answer-field.type/blank':
    assert len(vals)==1 and not vals[0].has(P.CONST) and '{{field-1}}' in prompt and re.search(r'\$\+C[,\.]?\$',prompt.replace(r'\,',''));C['blank_fragments']+=1
   else:assert len(vals)==5
   assert sum(P.zero(s.diff(a,v)-e) for a in vals)==1
   for a,b in itertools.combinations(vals,2):assert not P.zero(s.diff(a-b,v));C['pairs']+=1
   expected=bank(t,m['parameters'],e,v) if len(vals)==5 else [P.primitive(e,v)];assert len(expected)==len(vals) and all(sum(P.zero(s.diff(a-b,v)) for a in vals)==1 for b in expected),(t,m['parameters'],vals,expected);C['whole_banks']+=1
  if ':answer-field/correct' in f:
   correct=next(a for a,z in zip(vals,f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1]);assert P.zero(s.diff(correct,v)-e)
 C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
families=G.DEFAULTS if K in (17592186064180,17592186064181) else G.BANKS if K==17592186064179 else {'easy':['cos','sin','q-113907','q-113908','repaired_h','completed_q-71653'],'moderate':['sum','q-113909','q-2161','completed_q-71654'],'hard':['grouped']}
for level,templates in families.items():
 for t in templates:
  for seed in (49,153,271):check(G.generate(level,seed,template=t))
if K==17592186064178:
 for level,t in (('easy','sin'),('easy','cos'),('moderate','sum'),('hard','grouped')):
  check(G.generate(level,309,template=t,field_type='blank'))
for case in json.loads((D/'source-cases.json').read_text()):check(G.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case.get('profile',case.get('bank_profile'))),True)
result=dict(status='passed',source=fidelity,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),database_writes=0);(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
