"""Step 7 fail-closed replay, displayed mathematics, identity, scope and grading."""
import importlib.util,json,re,hashlib,subprocess,sys
from pathlib import Path
import sympy as s
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('ellipse',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
C,S=s.symbols('C S',real=True)
def read(expr):
 expr=expr.strip().rstrip('.,').replace('&','').strip()
 for trig,token in [('cos','C'),('sin','S')]:
  expr=re.sub(r'\{'+trig+r'\}\^\{2\}⁡(?:\\theta|t)',token+'^{2}',expr)
  expr=re.sub(r'\\'+trig+r'\^2\\theta',token+'^{2}',expr)
  expr=re.sub(r'\\operatorname\{'+trig+r'\}⁡(?:\\theta|t)',token,expr)
  expr=re.sub(r'\\'+trig+r'\\theta',token,expr)
 value=g.tex_expr(expr)
 return value.subs({s.Symbol('C'):C,s.Symbol('S'):S})
def reduce(expr):return s.simplify(s.expand(expr).subs(S**2,1-C**2))
def formula_from_prompt(q):
 block=re.findall(r'\$\$(.*?)\$\$',q[':question/problem'],re.S)[0]
 if r'\frac{x}' in block:
  eqs=block.split(r',\quad ')[:2];vals=[]
  for v,eq in zip([g.X,g.Y],eqs):
   left,right=eq.split('=');vals.append(s.solve(read(left)-read(right),v)[0])
 else:
  m=re.search(r'x=(.*?),\\(?:,|quad )y=(.*?),\\(?:,|quad )0',block)
  assert m,block
  vals=[read(m.group(1)),read(m.group(2))]
 ax=vals[0].coeff(C);by=vals[1].coeff(S);h=vals[0].subs(C,0);k=vals[1].subs(S,0)
 assert ax>0 and by>0
 return vals, (g.X-h)**2/ax**2+(g.Y-k)**2/by**2

def check(record):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==g.KP_ID
 q=record['question'];f=q[':question/answer-fields'][0]
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:
  assert text.count('$')%2==0
  depth=0
  for char in text:
   if char=='{':depth+=1
   if char=='}':depth-=1
   assert depth>=0
  assert depth==0
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 vals,expected=formula_from_prompt(q)
 p=record['generation']['parameters'];a,b,h,k=[s.sympify(p[z]) for z in ['a','b','h','k']]
 assert s.simplify(vals[0]-(a*C+h))==0 and s.simplify(vals[1]-(b*S+k))==0
 # Every printed algebraic row including formal first equations and final prose
 # conclusion must describe the actually printed parametric object.
 blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
 counts=[];rows_checked=0
 for block in blocks:
  body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=body.split('\\\\');counts.append(len(rows))
  for row in rows:
   sides=[read(x) for x in row.split('=')]
   for left,right in zip(sides,sides[1:]):
    assert reduce((left-right).subs({g.X:vals[0],g.Y:vals[1]}))==0,(record['generation'],row,left,right)
   rows_checked+=1
 target=g.tex_expr(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]).split('=')[0])
 assert s.simplify(target-expected)==0,(record['generation'],target,expected)
 residuals=[]
 for answer in f[':answer-field/choices']:
  # Complete equations are normalized by their constant, independently of sides.
  if '=' in answer[':answer/value']:
   lhs,rhs=answer[':answer/value'].split('=');res=g.tex_expr(lhs)-g.tex_expr(rhs)
  else:res=g.tex_expr(answer[':answer/value'])-1
  res=s.Poly(res,g.X,g.Y,extension=True);res=res.monic().as_expr();residuals.append(res)
 assert len(set(map(str,residuals)))==len(residuals)
 return {'template':record['generation']['template'],'parameters':p,'rows_checked':rows_checked,'block_row_counts':counts,'correct_displayed_math':True}

source_cases=[];fidelity=[];engine=[];review=[];display=[];matched=0
for t,q in g.Q.items():
 params=dict(zip(['a','b','h','k'],g.ORIGINAL[t]));level=g.TEMPLATES[t]['level'];case={'source_id':t,'template':t,'parameters':params,'bank_profile':'observed:'+t,'difficulty':level};source_cases.append(case)
 record=g.generate(level,template=t,parameters=params,profile=case['bank_profile']);n=record['question'];f=n[':question/answer-fields'][0];old=q[':question/answer-fields'][0]
 assert n[':question/problem']==q[':question/problem'] and n[':question/worked-solution']==q[':question/worked-solution']
 assert set(n)=={k for k in q if k not in {':db/id',':question/math-academy-id'}}
 assert f[':answer-field/key']==old[':answer-field/key'] and f[':answer-field/type']==old[':answer-field/type'][':db/ident']
 oldvals=sorted(a[':answer/value'] for a in old[':answer-field/choices']);newvals=sorted(a[':answer/value'] for a in f[':answer-field/choices']);assert oldvals==newvals
 cor=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert cor==old[':answer-field/correct'][':answer/value']
 matched+=len(oldvals);display.append(check(record));fidelity.append({'source_id':t,'prompt_exact':True,'solution_prose_sequence_exact':True,'answer_values_matched':len(oldvals),'complete_bank_exact':True,'correct_designation_matched':True,'key_presence_parity':True,'eligible_for_learning':record['generation']['eligible_for_learning']})
 review.append({'label':'Original faithful replay '+t,'record':record})
for t,info in g.TEMPLATES.items():
 for seed in [17,83]:
  record=g.generate(info['level'],seed=seed,template=t);display.append(check(record));review.append({'label':'Generated '+info['level']+' '+t+' seed '+str(seed),'record':record})
# Exercise source bank recipes at changed parameters, including opaque evidence.
for t in g.Q:
 record=g.generate(g.TEMPLATES[t]['level'],seed=57,profile='observed:'+t);display.append(check(record))
# Boundary families: signed shifted cases and all source structures under 120 seeds.
for level in ['easy','moderate','hard']:
 fingerprints=set();families=set()
 for seed in range(120):
  r=g.generate(level,seed);display.append(check(r));families.add(r['generation']['template']);fingerprints.add(r['generation']['mathematical_fingerprint'])
 expected={t for t,v in g.TEMPLATES.items() if v['level']==level};assert families==expected,(level,families,expected)
# Fixed math/bank/level identity does not depend on option order or seed.
for t,info in g.TEMPLATES.items():
 r=g.generate(info['level'],seed=11,template=t);p=r['generation']['parameters'];r2=g.generate(info['level'],seed=901,template=t,parameters=p)
 assert r['question'][':question/id']==r2['question'][':question/id'];assert r['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint']
for level,t,params in [('easy','easy_supplied_isolation',{'a':'2','b':'3','h':'1','k':'0'}),('hard','hard_translated_authored',{'a':'2','b':'3','h':'0','k':'1'}),('moderate','q-106405',{'a':'-5','b':'4','h':'0','k':'0'})]:
 try:g.generate(level,template=t,parameters=params)
 except ValueError:pass
 else:raise AssertionError('Invalid explicit scope accepted')
for item in review:
 r=item['record'];f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete displayed bank selection'} for a in f[':answer-field/choices']]
 else:
  ans=f[':answer-field/choices'][0][':answer/value'];expr=g.tex_expr(ans)
  checks=[{'submitted':ans,'expected':'accepted','purpose':'canonical LHS fragment'},{'submitted':s.latex(s.expand(expr)),'expected':'accepted','purpose':'independently expanded equivalent LHS'},{'submitted':s.latex(expr+1),'expected':'rejected','purpose':'incorrect constant'}]
 engine.append({'label':item['label'],'record':r,'checks':checks})
(D/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n');(D/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine.json')],check=True)
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n');(D/'review.md').write_text('\n\n'.join('## '+i['label']+'\n\nProfile: `'+i['record']['generation']['profile']+'`; eligible: '+str(i['record']['generation']['eligible_for_learning'])+'\n\n'+g.markdown(i['record']) for i in review))
result={'pass':True,'source_provenance':{k:g.RAW[k] for k in ['database','basis','lineage']},'source_questions':15,'source_values_matched':matched,'source_values_total':matched,'complete_original_banks':15,'exact_original_prose_sequences':15,'correct_designations_matched':15,'source_fidelity':fidelity,'displayed_math_records':len(display),'displayed_stages':display,'native_grading':json.loads((D/'engine.json').read_text()),'native_engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'authored_missing_levels':['easy'],'authored_bank_extensions':['q-79375','q-79377'],'source_repairs':['q-327811: normal prompt trig parameter t replaced with theta; raw profile preserved evidence-only'],'unresolved_findings':['Historical intent of compound q-79375/q-79377 banks remains opaque; explicit raw replay is ineligible.'],'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'plots':'none; no source raster or plotted choices','database_writes':0}
(D/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
freeze={'generator_version':g.VERSION,'generator_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'capture_sha256':hashlib.sha256((D/'source.json').read_bytes()).hexdigest(),'runtime':result['runtime'],'step':7,'status':'ready for independent parent QA','source_exact':15,'plot_assets':0}
(D/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
print('PASS: 15 exact source banks, '+str(matched)+' values; '+str(len(display))+' independently read records; native engine passed.')
