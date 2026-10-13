#!/usr/bin/env python3
"""Independent actual-display math, complete source fidelity, and native grading."""
from pathlib import Path
import importlib.util,json,re,subprocess,hashlib,sys
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('gen',HERE.with_suffix('.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
X=sp.Symbol('x',real=True);Z=sp.Symbol('z',positive=True)
MATH=re.compile(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^$]*\$')
EXPO=re.compile(r'(?:\{(?:e|\d+)\}|(?:e|\d+))\^\{([^{}]+)\}')
TRANS=standard_transformations+(implicit_multiplication_application,)

def parse(s):
 s=re.sub(r'\\+',r'\\',s).strip().strip('$').strip().rstrip('.,?')
 s=EXPO.sub('z',s)
 while '\\frac' in s:
  newer=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
  if newer==s:raise AssertionError('Unsupported fraction '+s)
  s=newer
 s=s.replace(r'\cdot','*').replace(r'\,','').replace('{','(').replace('}',')').replace('^','**').replace('&','').strip()
 return parse_expr(s,local_dict={'x':X,'z':Z},transformations=TRANS)

def equation(s):
 lhs,rhs=s.strip().strip('$').strip().rstrip('.,?').split('=')
 return sp.expand(parse(lhs)-parse(rhs))

def actual_display(record):
 q=record['question'];g=record['generation'];p=g['parameters']
 assert set(record['knowledge_point'])=={'db_id','id','title'} and record['knowledge_point']['db_id']==m.KP_ID
 assert record['knowledge_point']['id']==m.KP_UUID and record['knowledge_point']['title']==m.TITLE
 assert '<<' not in q[':question/problem']+q[':question/worked-solution']
 for content in [q[':question/problem'],q[':question/worked-solution']]:
  assert content.count('$')%2==0
  depth=0
  for c in content:
   if c=='{':depth+=1
   if c=='}':depth-=1
   assert depth>=0
  assert depth==0
  assert not re.search(r'\\(?:sinh|cosh|log)\b',content)
 prompt_math=MATH.search(q[':question/problem'])[0]
 exponent_matches=list(EXPO.finditer(prompt_math));assert exponent_matches
 for ex in exponent_matches+list(EXPO.finditer(q[':question/worked-solution'])):
  base=ex[0].split('^')[0].strip('{}')
  assert base==str(p['base'])
  assert parse(ex[1])==p['u']*X+p['v']
 displayed=equation(prompt_math)
 assert not displayed.has(sp.Float)
 assert displayed.has(Z),prompt_math
 poly=sp.cancel(displayed/Z)
 assert not poly.has(Z)
 assert sp.degree(poly,X)==2
 # The answers are solved from the actual printed equation, independently of
 # generator roots/coefficient metadata.
 derived=sorted(sp.solve(poly,X))
 assert len(derived)==2 and all(v.is_real for v in derived)
 expected=[sp.Rational(-p['q'],p['p']),sp.Rational(-p['s'],p['r'])]
 assert sorted(expected)==derived
 # Extract the actual first distributed sum, then the exponential factor row.
 maths=[m[0].strip('$').strip() for m in MATH.finditer(q[':question/worked-solution'])]
 first=maths[0].replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
 rows=first.split(r'\\')
 assert len(rows)==(4 if q[':question/difficulty'].endswith('/hard') else 3)
 assert equation(rows[0])==displayed
 assert equation(rows[1])==displayed
 for row in rows[2:]:assert equation(row)==displayed
 if q[':question/difficulty'].endswith('/hard'):
  assert len(EXPO.findall(rows[1]))==5 and len(EXPO.findall(rows[2]))==3 and len(EXPO.findall(rows[3]))==1
 # The second display applies zero product to the printed quadratic and E.
 pieces=re.split(r'\\,\\text\{and\}\\,',maths[4]);assert len(pieces)==2
 assert equation(pieces[0])==poly
 assert equation(pieces[1])==Z
 assert equation(maths[5])==poly
 factors=maths[6].replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
 for row in factors.split(r'\\'):assert equation(row)==poly,(row,poly)
 assert ')(' in factors.split(r'\\')[-1]
 seen=set()
 for f in q[':question/answer-fields']:
  key=f[':answer-field/key'];kind=f[':answer-field/type'].split('/')[-1]
  assert f[':answer-field/id'] not in seen;seen.add(f[':answer-field/id'])
  vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(vals)==len(set(vals))
  assert len(vals)==(5 if kind=='radio' else 1)
  if kind=='blank':assert '{{'+key+'}}' in q[':question/problem']
  aid=f[':answer-field/correct'][1]
  assert f[':answer-field/correct'][0]==':answer/id'
  correct=next(parse(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==aid)
  assert correct==(derived[0] if key=='field-1' else derived[1]) if kind=='blank' else correct==sp.prod(derived)
  for a in f[':answer-field/choices']:
   assert not re.search(r'[$]',a[':answer/value'])
   assert a[':answer/id'] not in seen;seen.add(a[':answer/id'])
   assert a[':answer/type']==':answer.type/math'
 # Check both displayed root listings and the displayed final product arithmetic.
 line=maths[7].rstrip('.')
 listed=[parse(t.replace('x=','')) for t in line.split(',')]
 assert listed==derived
 if q[':question/answer-fields'][0][':answer-field/type'].endswith('/radio'):
  last=maths[-1].rstrip('.')
  assert equation(last)==0
  assert parse(last.split('=')[1])==sp.prod(derived)
 else:
  last=maths[-1].rstrip('.')
  finals=re.split(r'\\,\\text\{and\}\\,',last)
  assert [parse(t.replace('x=','')) for t in finals]==derived
 return derived

def fixtures(record,label):
 checks=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:
    checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Owned radio selection; displayed mathematics checked independently'})
  else:
   v=parse(f[':answer-field/choices'][0][':answer/value']);n,d=sp.fraction(v)
   for val,expect,purpose in [(m.tex(v),'accepted','Canonical displayed value'),(r'\frac{'+str(2*n)+'}{'+str(2*d)+'}','accepted','Unreduced independently represented rational'),(m.tex(v+1),'rejected','Mathematically wrong nearby root')]:
    checks.append({'field_index':i,'submitted':val,'expected':expect,'purpose':purpose})
 return {'label':label,'record':record,'checks':checks}

def main():
 raw=json.loads((HERE/'source.json').read_text());assert raw['basis']==1356
 qs={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']}
 cases=json.loads((HERE/'source-cases.json').read_text());assert len(cases)==len(qs)==12
 totals={'source_questions':12,'replayed':0,'prompts_exact':0,'source_solution_present':10,'solutions_exact':0,'solutions_repaired':0,'source_answer_values':0,'matched_answer_values':0,'source_fields':0,'matched_field_layouts':0,'source_correct_designations_present':0,'matched_correct_designations':0,'missing_designations':0,'source_radio_banks':0,'matched_radio_banks':0}
 results=[];engine=[];review=[]
 for case in cases:
  sid=case['source_id'];q=qs[sid]
  r=m.generate(case['level'],seed=7,template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
  actual_display(r);totals['replayed']+=1
  assert r['question'][':question/problem']==q[':question/problem'],sid+' prompt fidelity'
  totals['prompts_exact']+=1
  repaired=False
  if ':question/worked-solution' in q:
   expected=q[':question/worked-solution']
   if sid=='q-264791':expected=expected.replace(r'{7}^{x}+ &',r'{7}^{x} &');repaired=True
   assert r['question'][':question/worked-solution']==expected,sid+' full worked-solution sequence/prose fidelity'
   totals['solutions_repaired' if repaired else 'solutions_exact']+=1
  fields={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
  for f in q.get(':question/answer-fields',[]):
   totals['source_fields']+=1;gf=fields[f[':answer-field/key']]
   assert gf[':answer-field/type']==f[':answer-field/type'][':db/ident'];totals['matched_field_layouts']+=1
   orig=[parse(a[':answer/value']) for a in f.get(':answer-field/choices',[])]
   gen=[parse(a[':answer/value']) for a in gf[':answer-field/choices']]
   if orig:
    assert sorted(orig)==sorted(gen),sid+' complete original value bank'
    totals['source_answer_values']+=len(orig);totals['matched_answer_values']+=len(orig)
   if gf[':answer-field/type'].endswith('/radio'):
    totals['source_radio_banks']+=1;totals['matched_radio_banks']+=1
   if ':answer-field/correct' in f:
    correct=parse(f[':answer-field/correct'][':answer/value'])
    gc=next(parse(a[':answer/value']) for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])
    assert correct==gc;totals['source_correct_designations_present']+=1;totals['matched_correct_designations']+=1
   else:totals['missing_designations']+=1
  results.append({'source_id':sid,'prompt_exact':True,'solution_status':'repaired trailing plus' if repaired else 'exact' if ':question/worked-solution' in q else 'missing; authored solution','field_status':'authored field; original fieldless' if sid=='q-88472' else 'original layout','correct_ref_status':'missing; independently derived' if sid in ['q-237949','q-88417','q-88472'] else 'matched'})
  engine.append(fixtures(r,'source '+sid))
  review.append({'label':'Original-parameter replay '+sid,'source_id':sid,'record':r})
  # Two changed-parameter examples for each observed bank/layout, including
  # the separate source-format profiles with honest inference limits.
  for seed in (19,41):
   v=m.generate(case['level'],seed=seed,template=case['template'],profile=case['bank_profile'])
   actual_display(v);engine.append(fixtures(v,'variant '+sid+' '+str(seed)))
   review.append({'label':'Generated observed-layout variant '+sid+' seed '+str(seed),'source_id':sid,'record':v})
 counts={};unique={};correct_positions={}
 for template,(level,kind,_,_) in m.TEMPLATES.items():
  identities=set();maths=set();positions=set()
  for seed in range(120):
   r=m.generate(level,seed=seed,template=template);actual_display(r)
   identities.add(r['question'][':question/id']);maths.add(r['generation']['mathematical_fingerprint'])
   if kind=='radio':
    f=r['question'][':question/answer-fields'][0]
    positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
   if seed<2:
    engine.append(fixtures(r,'authored default '+template+' '+str(seed)))
    review.append({'label':'Authored default bank/level '+template+' seed '+str(seed),'record':r})
   # Changing seed with fixed parameters changes only order/seed metadata.
   replay=m.generate(level,seed=seed+1000,template=template,parameters=r['generation']['parameters'],profile=r['generation']['profile'])
   assert replay['question'][':question/id']==r['question'][':question/id']
   assert replay['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
  minimum=(10 if template in ['difference_integer_blank','difference_unit_product'] else 28 if template in ['difference_rational_blank','difference_rational_product'] else 20 if template=='quadratic_right_const_linear_product' else 25 if level=='moderate' else 35)
  assert len(maths)>=minimum,(template,len(maths))
  counts[template]=120;unique[template]={'content':len(identities),'mathematical_tasks':len(maths)}
  if kind=='radio':assert len(positions)==5;correct_positions[template]=sorted(positions)
  # Exponent/base changes are incidental to the assessed factoring task.
  inc=dict(r['generation']['parameters']);inc['base']='e' if inc['base']!='e' else 2
  if template!='difference_unit_product':inc.update(u=5,v=-6)
  else:inc['v']=1 if inc['v']!=1 else 6
  changed=m.generate(level,seed=902,template=template,parameters=inc,profile=r['generation']['profile']);actual_display(changed)
  assert changed['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
  assert changed['question'][':question/id']!=r['question'][':question/id']
 # Bank profile may change presentation identity, never the math fingerprint.
 for case in cases:
  if case['bank_profile'].startswith('observed:'):
   a=m.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
   try:b=m.generate(case['level'],template=case['template'],parameters=case['parameters'])
   except ValueError:continue # documented whole-bank collision at unit roots
   assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
   if a['question'][':question/answer-fields']!=b['question'][':question/answer-fields']:assert a['question'][':question/id']!=b['question'][':question/id']
 # Explicit parameter guards, including signed magnitude limits and unsupported
 # profile/type combinations, must reject rather than silently resample.
 rejects=0
 examples=[('easy','difference_integer_blank',{'g':2,'p':1,'q':13,'r':1,'s':-13,'base':3,'u':1,'v':0}),('hard','collected_quadratic_blank',{'g':1,'p':2,'q':-7,'r':2,'s':3,'base':3,'u':1,'v':0,'split':1,'linear_split':2}),('moderate','quadratic_left_const_positive_blank',{'g':1,'p':4,'q':1,'r':1,'s':6,'base':3,'u':1,'v':0}),('hard','collected_quadratic_blank',{'g':1,'p':2,'q':2,'r':2,'s':4,'base':3,'u':1,'v':0,'split':1,'linear_split':2}),('moderate','quadratic_right_const_linear_product',{'g':1,'p':2,'q':2,'r':2,'s':-4,'base':3,'u':1,'v':0}),('easy','difference_rational_blank',{'g':1,'p':3,'q':6,'r':3,'s':-6,'base':3,'u':1,'v':0})]
 for level,t,p in examples:
  try:m.generate(level,template=t,parameters=p)
  except ValueError:rejects+=1
  else:raise AssertionError('Explicit invalid scope accepted')
 (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
 grader=ROOT/'generate/runs/current/check-engine';assert grader.exists()
 run=subprocess.run([str(grader),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
 (HERE/'engine-run.log').write_text(run.stdout+run.stderr)
 assert run.returncode==0,'Native grading failed: '+run.stdout+run.stderr
 native=json.loads((HERE/'engine-report.json').read_text())
 report={'status':'pass','source':{k:raw[k] for k in ['database','basis','lineage']},'source_fidelity':totals,'source_results':results,'generated_math_checks':counts,'unique_seed_sample':unique,'radio_correct_positions':correct_positions,'explicit_invalid_scope_rejections':rejects,'native_grader_report':native,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'grader_sha256':hashlib.sha256(grader.read_bytes()).hexdigest(),'authored_hard':'Collect five exponential-polynomial terms across both sides and factor nonmonic quadratic; bounded two linear factors; no exponential-solving branch','unresolved_findings':['No correct designations exist for q237949 two fields or q88417 radio; independent derived values are repairs, not matches.','No original widget for q88472 exists in available 2979 snapshot; generated radio field is an authored repair, not recovered fidelity.','Observed scalar wrong-value recipe intent is unresolved; explicit expression-shape replay profiles are never default banks.']}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 lines=['# Original sources and generated variants','', 'Basis 1356. Original banks/designations and malformed evidence are retained in source.json. Each generated record uses the normal generator. Authored fields/banks/levels are labeled here and in generation metadata.','']
 for q in qs.values():
  lines+=['## Original '+q[':question/math-academy-id'],'',q[':question/problem'],'']
  for f in q.get(':question/answer-fields',[]):lines += [f[':answer-field/key']+' ('+f[':answer-field/type'][':db/ident']+'): '+', '.join('$'+a[':answer/value']+'$' for a in f.get(':answer-field/choices',[]))+'; correct designation: '+f.get(':answer-field/correct',{}).get(':answer/value','MISSING'),'']
  lines+=[q.get(':question/worked-solution','WORKED SOLUTION MISSING'),'']
 for item in review:
  lines+=['## '+item['label'],'','Template: '+item['record']['generation']['template']+'; profile: '+item['record']['generation']['profile'],'',m.markdown(item['record']),'']
 (HERE/'review.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps({'status':'pass','source_fidelity':totals,'generated_cases':sum(counts.values()),'engine_records':len(engine),'engine_checks':sum(len(e['checks']) for e in engine),'generator_sha256':report['generator_sha256']},indent=2))
if __name__=='__main__':main()
