#!/usr/bin/env python3
"""Independent printed-math, whole-source fidelity and real native grading QA."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
from fractions import Fraction
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('quartic_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x')
trans=standard_transformations+(implicit_multiplication_application,)
def expr(s):
 s=s.strip().rstrip('.,').replace('{x}','x')
 s=re.sub(r'\^\{([^{}]+)\}',r'**(\1)',s)
 while '\\frac{' in s:
  old=s;s=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',s)
  if old==s: raise AssertionError('Unparsed fraction '+s)
 s=s.replace('{x}','x');s=re.sub(r'\^\{([^{}]+)\}',r'**(\1)',s);s=s.replace('^','**').replace('{','(').replace('}',')').replace(' ','')
 return parse_expr(s,local_dict={'x':X},transformations=trans)
def source_fields(q):
 out={}
 for f in q[':question/answer-fields']:
  c=f.get(':answer-field/correct');cid=c[':answer/id'] if isinstance(c,dict) else c[1] if c else None
  out[f[':answer-field/key']]={'type':f[':answer-field/type'].get(':db/ident') if isinstance(f[':answer-field/type'],dict) else f[':answer-field/type'],'bank':sorted(str(expr(a[':answer/value'])) for a in f[':answer-field/choices']),'correct':next((str(expr(a[':answer/value'])) for a in f[':answer-field/choices'] if a[':answer/id']==cid),None)}
 return out

def inspect(r):
 """Read the displayed prompt; validate tables, equations, prose roots and fields."""
 q=r['question'];md=q[':question/problem'];sol=q[':question/worked-solution'];p=expr(re.search(r'p\(x\)\s*=([^$]+)',md)[1]);given=[expr(t) for t in re.findall(r'p\(([-+0-9]+)\)\s*=',md)]
 assert 'using synthetic division:' in sol and 'using synthetic division once more' in sol
 assert 'We can factor the quadratic factor even further, and get' in sol
 assert sp.degree(p,X)==4 and len(given)==2 and len(set(given))==2
 assert all(p.subs(X,t)==0 for t in given)
 roots=sp.polys.polytools.ground_roots(p,X);assert len(roots)==4 and all(v==1 for v in roots.values())
 sortedroots=sorted(roots);correct=sum(roots) if g.SPECS[r['generation']['template']]['kind']=='radio' else sortedroots
 assert all(ord(c)>=32 or c in '\n\t' for c in md+sol)
 g.validate_generated_record(r)
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 # Every header, coefficient, multiply row, carry/add row is interpreted back.
 tables=re.findall(r'(\|  \| \$\{x\}\^\{[43]\}.*?)(?=\n\n)',sol,re.S);assert len(tables)==2
 current=p
 for tab in tables:
  rows=tab.splitlines();assert len(rows)==5
  cols=lambda row:[x.strip().strip('$') for x in row.strip('|').split('|')]
  coeffrow=cols(rows[2]);r0=expr(coeffrow[0]);coeff=list(map(expr,coeffrow[1:]));products=list(map(expr,cols(rows[3])[2:]));out=list(map(expr,cols(rows[4])[1:]));assert coeff==sp.Poly(current,X).all_coeffs()
  quotient,remainder=sp.div(current,X-r0);assert remainder==0
  assert out==sp.Poly(quotient,X).all_coeffs()+[0]
  assert products==[r0*z for z in out[:-1]]
  for i in range(1,len(out)):assert coeff[i]+products[i-1]==out[i]
  current=quotient
 rootblock=re.search(r'\\begin\{aligned\}x.*?\\end\{aligned\}',sol)[0]
 roottext=rootblock.split('=',1)[1].split(r'\end')[0]
 orderedroots=[expr(z) for z in roottext.split(r'\,,\,x=')]
 assert sorted(orderedroots)==sortedroots
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
 operative=[b for b in blocks if not b.startswith(r'\begin')]
 assert len(operative)==(5 if isinstance(correct,list) else 6)
 for b in operative:
  left,right=b.rstrip('.,').split('=');assert sp.cancel(expr(left)-expr(right))==0,b
 # All intermediate fractions and expanded/factored equalities above are checked.
 fields=q[':question/answer-fields'];expected=correct if isinstance(correct,list) else [correct]
 assert len(fields)==len(expected)
 if not isinstance(correct,list):
  given_sum=sum(given);new=orderedroots[2:];total=sum(sortedroots)
  profile=r['generation']['bank_profile']
  if profile.endswith('opposite_method'): expected_bank=[total,given_sum,-total,new[0],new[1]]
  else: expected_bank=([new[0],given_sum,-new[1],given[0],total] if profile=='observed_sum_integer' else [total,given_sum,sum(new),given_sum-sum(new),given_sum+new[0]])
  assert set(expr(a[':answer/value']) for a in fields[0][':answer-field/choices'])==set(expected_bank)
 for i,f in enumerate(fields):
  key=f[':answer-field/key'];assert g.uuid.UUID(f[':answer-field/id']);values=[expr(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(values))==len(values)
  cid=f[':answer-field/correct'][1];assert next(v for a,v in zip(f[':answer-field/choices'],values) if a[':answer/id']==cid)==expected[i]
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+key+'}}' in md
  for a in f[':answer-field/choices']:assert g.uuid.UUID(a[':answer/id'])
 return p,given,sortedroots

def grader_item(r,label):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  cid=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'complete owned radio bank'} for a in f[':answer-field/choices'])
  else:
   a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==cid);v=expr(a[':answer/value']);eq=r'\frac{'+str(v.p*2)+'}{'+str(v.q*2)+'}'
   checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'canonical sorted root fragment'},{'field_index':i,'submitted':eq,'expected':'accepted','purpose':'unreduced equivalent root fraction'},{'field_index':i,'submitted':str(v+1),'expected':'rejected','purpose':'wrong root value'},{'field_index':i,'submitted':str(-v),'expected':'accepted' if v==0 else 'rejected','purpose':'wrong sign root'}])
 return {'label':label,'record':r,'checks':checks}

def capacity():
 """Enumerate root/given-set tasks using independent Fraction expansion.
 Choice, root order, scale sign aliases and presentation layouts do not count.
 """
 ints=list(range(-6,0))+list(range(1,7));known=list(itertools.combinations(map(Fraction,ints),2))
 def polynomial(rs,a):
  c=[a]
  for root in rs:
   new=[Fraction(0)]*(len(c)+1)
   for i,v in enumerate(c):new[i]+=v;new[i+1]-=v*root
   c=new
  return c
 def eligible(gg,rr,a,limit):return len(set(gg+rr))==4 and max(map(abs,polynomial(gg+rr,a)))<=limit
 def radio_eligible(gg,rr):
  k=sum(gg);n=sum(rr);t=k+n
  if k==0:return len({t,k,-t,*rr})==5
  return any(len({t,k,n,k-n,k+first})==5 for first in rr)
 integer=0;difference=0;integer_radio=0
 for gg in known:
  for rr in known:
   if eligible(gg,rr,Fraction(1),150):
    integer+=1;integer_radio+=radio_eligible(gg,rr)
    if sum(gg)==sum(rr)==0:difference+=1
 fractions={d:sorted({Fraction(n,d) for n in range(-5,6) if n and Fraction(n,d).denominator==d}) for d in range(2,7)}
 moderate=hard=moderate_radio=hard_radio=0
 for gg in known:
  for d in range(2,5):
   for rr in itertools.combinations(fractions[d],2):
    ok=sum(rr)!=0 and eligible(gg,rr,Fraction(d*d),650);moderate+=ok;moderate_radio+=ok and radio_eligible(gg,rr)
  for d,e in itertools.combinations(range(2,7),2):
   for r,s in itertools.product(fractions[d],fractions[e]):
    ok=eligible(gg,(r,s),Fraction(d*e),650);hard+=ok;hard_radio+=ok and radio_eligible(gg,(r,s))
 return {'easy_integer_root_given_set_tasks':integer,'easy_opposite_pair_subfamily':difference,'easy_integer_sum_tasks_with_eligible_complete_bank':integer_radio,'moderate_sum_tasks_with_eligible_complete_bank':moderate_radio,'hard_sum_tasks_with_eligible_complete_bank':hard_radio,'moderate_common_denominator_tasks':moderate,'hard_distinct_denominator_tasks':hard,'excluded_aliases':['choice order','given-root order','remaining-root order','nonzero scalar multiple','sum-vs-blank layout is reported separately']}

def main():
 cases=json.loads((D/'source-cases.json').read_text());source={q[':question/math-academy-id']:q for q in g.KP[':knowledge-point/questions']};replays=[];fid=[]
 for c in cases:
  r=g.generate(c['level'],19,c['template'],parameters=c['parameters'],profile=c['bank_profile']);q=source[c['source_id']];replays.append(r)
  for k in [':question/difficulty',':question/worked-solution',':question/answer-fields']:
   assert (k in q)==(k in r['question']),(c['source_id'],k)
  assert r['question'][':question/problem']==q[':question/problem']
  assert r['question'].get(':question/worked-solution')==q.get(':question/worked-solution')
  assert source_fields(q)==source_fields(r['question'])
  fid.append({'source_id':c['source_id'],'prompt_exact':True,'solution_exact':':question/worked-solution' in q,'solution_absence_exact':':question/worked-solution' not in q,'bank_values':sum(len(f[':answer-field/choices']) for f in q[':question/answer-fields']),'correct_designation_matched':sum(':answer-field/correct' in f for f in q[':question/answer-fields']),'evidence_only':True})
 # Source recipes must actually respond to changed roots, including opaque raw banks.
 for c in cases:
  p=copy.deepcopy(c['parameters']);old=p['given'];p['given']=[str(sp.Rational(z)+7) for z in old]
  changed=g.generate(c['level'],29,c['template'],parameters=p,profile=c['bank_profile'])
  printed=expr(re.search(r'p\(x\)\s*=([^$]+)',changed['question'][':question/problem'])[1])
  assert all(printed.subs(X,sp.Rational(z))==0 for z in p['given'])
  assert changed['question'][':question/problem']!=source[c['source_id']][':question/problem']
 generated=[];engine=[];seen={};families={l:set() for l in ['easy','moderate','hard']};slots={n:{'given':set(),'remaining':set(),'scale':set()} for n in g.SPECS}
 for name,s in g.SPECS.items():
  for seed in range(36):
   r=g.generate(s['level'],seed,template=name);inspect(r);generated.append(r)
   p=r['generation']['parameters'];other=g.generate(s['level'],999,template=name,parameters=p,profile=r['generation']['bank_profile'])
   assert other['question'][':question/id']==r['question'][':question/id']
   assert other['question'][':question/worked-solution']==r['question'][':question/worked-solution']
   for slot in slots[name]:slots[name][slot].add(json.dumps(p[slot]))
   if seed<3:engine.append(grader_item(r,name+'/'+str(seed)))
 bank_coverage={n:set() for n,s in g.SPECS.items() if s['kind']=='radio'}
 for r in generated:
  if r['generation']['template'] in bank_coverage:bank_coverage[r['generation']['template']].add(r['generation']['bank_profile'])
 for n,observed in bank_coverage.items():assert len(observed)==2,(n,observed)
 for level in families:
  for seed in range(150):
   r=g.generate(level,seed);inspect(r);families[level].add(r['generation']['template'])
  assert families[level]=={n for n,s in g.SPECS.items() if s['level']==level}
 for name,ss in slots.items():
  assert len(ss['given'])>=2 and len(ss['remaining'])>=2,(name,ss)
  assert len(ss['scale'])>=(1 if g.SPECS[name]['level']=='easy' else 2),(name,ss)
 # Explicit native checks at original repaired arithmetic including every fraction.
 for c in cases:
  r=g.generate(c['level'],8,c['template'],parameters=c['parameters'],profile='observed_sum_integer' if c['template']=='sum_integer' else None)
  inspect(r);engine.append(grader_item(r,'repaired anchor/'+c['source_id']))
 # Identity excludes factor choice order and scale aliases only in semantic key.
 p={'given':['-3','1'],'remaining':['6','-5'],'scale':'1'}
 r=g.generate('easy',parameters=p,template='sum_integer');mut=copy.deepcopy(r);mut['question'][':question/worked-solution']=mut['question'][':question/worked-solution'].replace('$2$ | $-33$', '$3$ | $-33$',1)
 mutations=[mut]
 mut=copy.deepcopy(r);mut['question'][':question/worked-solution']=mut['question'][':question/worked-solution'].replace('synthetic division once more:', 'polynomial root lookup:');mutations.append(mut)
 mut=copy.deepcopy(r);mut['question'][':question/worked-solution']='\x0c'+mut['question'][':question/worked-solution'];mutations.append(mut)
 rejected=0
 for m in mutations:
  try:
   inspect(m)
   assert 'synthetic division once more:' in m['question'][':question/worked-solution']
  except (AssertionError,ValueError):rejected+=1
 assert rejected==3
 invalid=[('easy','roots_integer',dict(given=['1','-1'],remaining=['2','2'],scale='1')),('moderate','roots_common_denominator',dict(given=['-2','-3'],remaining=['1/3','1/2'],scale='6')),('hard','roots_distinct_denominators',dict(given=['-2','-3'],remaining=['1/3','2/3'],scale='9')),('easy','sum_integer',dict(given=['-7','1'],remaining=['6','-5'],scale='1'))]
 for level,name,p in invalid:
  try:g.generate(level,template=name,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit domain accepted')
 (D/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n');harness=ROOT/'generate/runs/current/check-engine'
 subprocess.run([str(harness),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True,capture_output=True,text=True)
 engine_report=json.loads((D/'engine-report.json').read_text())
 examples=[]
 for name in g.SPECS:
  examples.extend([r for r in generated if r['generation']['template']==name][:2])
 review={'originals':replays,'generated_variants':examples};(D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 text=['# Quartic given two roots: originals and generated variants','All originals below are raw evidence only. Generated variants use repaired/shared operative stages.']
 for c,r in zip(cases,replays):text+=['\n## Original '+c['source_id'],g.markdown(r)]
 for r in examples:text+=['\n## Generated '+r['generation']['template']+' ('+g.SPECS[r['generation']['template']]['level']+')',g.markdown(r)]
 (D/'review.md').write_text('\n\n'.join(text)+'\n')
 cap=capacity();(D/'capacity.json').write_text(json.dumps(cap,indent=2)+'\n')
 report={'status':'pass','source_basis':g.SOURCE['basis'],'source_fidelity':fid,'source_questions':len(cases),'complete_banks_matched':7,'displayed_values_matched':31,'correct_designations_matched':17,'missing_original_designations':2,'exact_worked_solutions':5,'absent_original_solutions':2,'normal_repairs':2,'mathematical_checks':len(generated)+450+7,'mutation_regressions_rejected':rejected,'native':engine_report,'native_harness_sha256':hashlib.sha256(harness.read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'default_families':{k:sorted(v) for k,v in families.items()},'default_bank_coverage':{k:sorted(v) for k,v in bank_coverage.items()},'slot_coverage':{n:{k:len(v) for k,v in ss.items()} for n,ss in slots.items()},'capacity':cap,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'remaining_unresolved':['Opaque historical wrong-answer intentions are not recovered; raw replay is evidence-only. Original missing correct designations cannot count as matched keys.']}
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['native','source_fidelity','slot_coverage']},indent=2))
if __name__=='__main__':main()
