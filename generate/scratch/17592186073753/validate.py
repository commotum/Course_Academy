#!/usr/bin/env python3
"""Independent displayed-equation/stage mathematics, bank fidelity, native grading."""
import importlib.util,json,re,hashlib,subprocess,uuid,sys
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
qa_spec=importlib.util.spec_from_file_location('shared_qa',ROOT/'generate/runs/current/qa.py');qa=importlib.util.module_from_spec(qa_spec);qa_spec.loader.exec_module(qa)
X,Y=s.symbols('X Y')

def write(name,obj): (H/name).write_text(json.dumps(obj,indent=2)+'\n')
def parse(tex,x,y):
 tex=tex.replace('\\left','').replace('\\right','').replace('−','-')
 while re.search(r'\\(?:dfrac|frac)\{([^{}]+)\}\{([^{}]+)\}',tex):
  tex=re.sub(r'\\(?:dfrac|frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',tex)
 assert '\\' not in tex and '{' not in tex and '}' not in tex,tex
 return parse_expr(tex,local_dict={x:X,y:Y},transformations=standard_transformations+(implicit_multiplication_application,))
def residual(eq,x,y):
 left,right=eq.split('=');return s.expand(parse(left.replace('&',''),x,y)-parse(right,x,y))
def normalized(tex):return re.sub(r'\s+','',tex)
def brace_check(text):
 depth=0
 for i,c in enumerate(text):
  if i and text[i-1]=='\\':continue
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,text
 assert depth==0,text
 assert text.count('$')%2==0
 assert '--' not in text and '+-' not in text

def prompt_coeffs(rec):
 prompt=rec['question'][':question/problem'];p=rec['generation']['parameters'];x,y=p['x'],p['y']
 hit=re.search(r'\$\\\{([^$]+)\$',prompt);assert hit,prompt
 eqs=hit[1].split(';');assert len(eqs)==2
 poly=[residual(z,x,y) for z in eqs]
 for z in poly:assert s.Poly(z,X,Y).total_degree()==1
 a,b,c=poly[0].coeff(X),poly[0].coeff(Y),-poly[0].subs({X:0,Y:0})
 d,e,f=poly[1].coeff(X),poly[1].coeff(Y),-poly[1].subs({X:0,Y:0})
 assert all(z.is_Integer for z in (a,b,c,d,e,f))
 assert a*e-b*d
 ans=s.solve(poly,(X,Y));return (a,b,c,d,e,f,x,y,ans[X],ans[Y])

def verify(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 assert rec['knowledge_point']['db_id']==g.KP_ID
 q=rec['question'];assert q[':question/difficulty']==':question.difficulty/'+rec['generation']['level'];p=rec['generation']['parameters'];t=rec['generation']['template'];profile=rec['generation']['profile'];raw=profile=='source_q12457_raw'
 if not raw:qa.record_checks(rec)
 for z in (q[':question/problem'],q[':question/worked-solution']):brace_check(z)
 a,b,c,d,e,f,x,y,xv,yv=prompt_coeffs(rec)
 assert xv==g.values(p)[0] and yv==g.values(p)[1]
 field=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and len(field[':answer-field/choices'])==5
 uuid.UUID(q[':question/id']);uuid.UUID(field[':answer-field/id'])
 val=[];ids=[]
 for z in field[':answer-field/choices']:
  uuid.UUID(z[':answer/id']);brace_check(z[':answer/value']);ids.append(z[':answer/id'])
  if t=='difference':v=parse(z[':answer/value'],x,y)
  else:
   frags=z[':answer/value'].split(',');assert len(frags)==2
   assert frags[0].split('=')[0].strip()==x and frags[1].split('=')[0].strip()==y
   v=tuple(parse(k.split('=')[1],x,y) for k in frags)
  assert all(n.is_Rational for n in v) if isinstance(v,tuple) else v.is_Rational
  val.append(v)
 assert len(set(val))==5 and len(set(ids))==5
 # Independently derive ALL displayed values from the printed operation.
 if profile=='source_q12444':expected_bank=[(xv,yv-1),(xv,-yv/3),(xv,yv),(yv,xv),(-xv,yv)]
 elif profile.startswith('source_q12457'):
  scale=c/(abs(a)+b);expected_bank=[(-2*scale,2*scale),(3*scale/2,-3*scale/2),(2*scale,-2*scale),(scale,-scale),(-scale,scale)]
  if profile.endswith('repaired'):expected_bank[0]=(xv,yv)
 elif profile=='source_q18483':expected_bank=[xv+yv,xv-yv,-xv-yv,yv,xv]
 elif t=='difference':
  wy=-yv;wx=(f-e*wy)/d;expected_bank=[xv-yv,xv+yv,yv-xv,xv,wx-wy]
 else:
  if t=='pair_first':div,n,k,oa,ob,oc=b,-a,c,d,e,f;isolated_first=False
  elif t=='pair_second':div,n,k,oa,ob,oc=e,-d,f,a,b,c;isolated_first=False
  else:div,n,k,oa,ob,oc=d,-e,f,b,a,c;isolated_first=True
  hh,mm=k/div,n/div
  def ordered(v,w):return (v,w) if isolated_first else (w,v)
  wrong_w=(oc-ob*hh)/(oa-ob*mm)
  omitted_w=(oc-hh)/(oa+ob*mm)
  omitted_division_w=oc-ob*hh
  expected_bank=[(xv,yv),ordered(hh-mm*wrong_w,wrong_w),ordered(hh+mm*omitted_w,omitted_w),ordered(hh+mm*omitted_division_w,omitted_division_w),(yv,xv)]
 assert set(val)==set(expected_bank),(profile,val,expected_bank)
 correct=xv-yv if t=='difference' else (xv,yv)
 identity=g.digest({'version':g.VERSION,'problem':q[':question/problem'],'solution':q[':question/worked-solution'],'bank':sorted(a[':answer/value'] for a in field[':answer-field/choices']),'field':'radio','difficulty':rec['generation']['level']})
 assert rec['generation']['content_identity']==identity and q[':question/id']==g.uid(identity)
 hits=[i for i,v in enumerate(val) if v==correct]
 if raw:assert hits==[] and ':answer-field/correct' not in field
 else:assert len(hits)==1 and field[':answer-field/correct']==[':answer/id',ids[hits[0]]]
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
 rows=[[z.strip() for z in bl.split('\\\\')] for bl in blocks]
 if t=='difference':
  assert list(map(len,rows))==[3,5]
  expected=[[b*Y-c,b*Y-c,Y-yv],[d*X+e*Y-f,d*X+e*yv-f,d*X+e*yv-f,d*X-(f-e*yv),X-xv]]
 else:
  if t=='pair_first':v,w,V,W,div,n,k,ia,ib,ic,oa,ob,oc=Y,X,yv,xv,b,-a,c,a,b,c,d,e,f
  elif t=='pair_second':v,w,V,W,div,n,k,ia,ib,ic,oa,ob,oc=Y,X,yv,xv,e,-d,f,d,e,f,a,b,c
  else:v,w,V,W,div,n,k,ia,ib,ic,oa,ob,oc=X,Y,xv,yv,d,-e,f,e,d,f,b,a,c
  h,m=k/div,n/div
  assert list(map(len,rows))==([3,6,6] if t=='pair_first' else [5,6,6])
  expected=[[ib*v+ia*w-ic,ib*v+ia*w-ic,div*v-k-n*w,v-(k+n*w)/div,v-h-m*w],
   [ob*v+oa*w-oc,ob*(h+m*w)+oa*w-oc,ob*h+ob*m*w+oa*w-oc,ob*h-oc+(ob*m+oa)*w,(ob*m+oa)*w-(oc-ob*h),w-W],
   [ob*v+oa*w-oc,ob*v+oa*W-oc,ob*v+oa*W-oc,ob*v+oa*W-oc,ob*v-(oc-oa*W),v-V]]
  if t=='pair_first':expected[0]=expected[0][:3]
  # Structural distribution operation: expanded row cannot still contain
  # the substitution parentheses, nor silently collect both variable terms.
  distr=rows[1][2].split('&=')[0]
  assert '\\left' not in distr and '\\dfrac' not in distr
  name=x if w==X else y
  assert distr.count(name)==2,(distr,'distribution requires the two uncollected terms')
  # Explicit nonzero canonical/default affine operands make rows substantive.
  if profile=='method':assert m and h
 for block,exp in zip(rows,expected):
  for row,reference in zip(block,exp):
   got=residual(row,x,y)
   assert s.expand(got-reference)==0,(row,got,reference)
 # The final prose tuple/scalar is also read back, not trusted metadata.
 if t=='difference':
  tail=q[':question/worked-solution'].split('Therefore, ')[1];assert parse(tail.split('=')[-1].strip(' $.').strip(),x,y)==xv-yv
 else:
  tup=re.findall(r'\\left\(([^\n]+)\\right\)',q[':question/worked-solution'])[-1]
  z=tup.split(',');assert tuple(parse(i,x,y) for i in z)==(xv,yv)
 return sum(map(len,rows))

cases=[{'source_id':'q-12444','level':'easy','template':'pair_first','bank_profile':'source_q12444','parameters':g.SOURCE_PARAMETERS['q-12444']},{'source_id':'q-12457','level':'hard','template':'pair_second','bank_profile':'source_q12457_raw','parameters':g.SOURCE_PARAMETERS['q-12457']},{'source_id':'q-18483','level':'easy','template':'difference','bank_profile':'source_q18483','parameters':g.SOURCE_PARAMETERS['q-18483']}]
write('source-cases.json',cases)
originals={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']}
reviews=[];source_results=[];mathrows=0;native=[]
def engine_checks(rec,label):
 f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Every displayed complete choice selected by owned answer ID'} for a in f[':answer-field/choices']]}
for case in cases:
 rec=g.generate(case['level'],19,case['template'],parameters=case['parameters'],profile=case['bank_profile']);mathrows+=verify(rec);orig=originals[case['source_id']]
 got=rec['question'][':question/answer-fields'][0][':answer-field/choices'];old=orig[':question/answer-fields'][0][':answer-field/choices']
 def comparable(v):return normalized(v).replace('\\dfrac','\\frac')
 assert sorted(comparable(z[':answer/value']) for z in got)==sorted(comparable(z[':answer/value']) for z in old)
 assert normalized(rec['question'][':question/problem'])==normalized(orig[':question/problem'].replace('${','$\\{'))
 result={'source_id':case['source_id'],'original_unrated':True,'authored_level':case['level'],'bank_values_matched':5,'raw_correct_refs_present':False,'derived_correct_value':str(g.values(case['parameters'])) if case['template']!='difference' else str(g.values(case['parameters'])[0]-g.values(case['parameters'])[1]),'correct_options_in_original':0 if case['source_id']=='q-12457' else 1,'worked_solution_present':False,'presentation_repair':'escape unmatched literal system brace; whitespace normalization only'}
 source_results.append(result);reviews.append({'label':'Original replay '+case['source_id'],'record':rec})
 if not rec['generation']['evidence_only']:native.append(engine_checks(rec,case['source_id']))
 # Two changed-parameter whole-bank variants for every empirical profile.
 for n in (1,2):
  p=dict(case['parameters'])
  if case['source_id']=='q-12444':p['C']=-9-2*n;p['F']=32+9*n
  elif case['source_id']=='q-12457':p['C']=18+9*n
  else:p['C']=-55-5*n;p['F']=-3+2*n
  r=g.generate(case['level'],n,case['template'],parameters=p,profile=case['bank_profile']);mathrows+=verify(r);reviews.append({'label':'Generated explicit empirical-profile variant '+case['source_id']+' #'+str(n),'record':r})
  if not r['generation']['evidence_only']:native.append(engine_checks(r,case['source_id']+' variant '+str(n)))
repaired=g.generate('hard',19,'pair_second',parameters=g.SOURCE_PARAMETERS['q-12457'],profile='source_q12457_repaired');mathrows+=verify(repaired);native.append(engine_checks(repaired,'q12457 supported minimal bank repair'));reviews.append({'label':'Supported bank repair q-12457; authored correct option replaces first raw value','record':repaired})
# Canonical method/prose fidelity is separate from practice fidelity.
canon=g.generate('hard',21,'canonical_second',parameters=g.SOURCE_PARAMETERS['e-13010']);mathrows+=verify(canon)
raw=g.SOURCE['record'][':knowledge-point/canonical-example']
assert normalized(canon['question'][':question/problem'])==normalized(raw[':question/problem'].replace('${','$\\{'))
assert normalized(canon['question'][':question/worked-solution'])==normalized(raw[':question/worked-solution'].replace('\n{2u','\n\\{2u'))
reviews.append({'label':'Canonical method replay e-13010 (authored bank)','record':canon});native.append(engine_checks(canon,'canonical method'))
diversity={};instances=0
for level in ('easy','moderate','hard'):
 tasks=set();positions=set()
 for seed in range(120):
  r=g.generate(level,seed);mathrows+=verify(r);instances+=1;tasks.add(r['generation']['mathematical_fingerprint'])
  fid=r['question'][':question/answer-fields'][0];positions.add([a[':answer/id'] for a in fid[':answer-field/choices']].index(fid[':answer-field/correct'][1]))
  rr=g.generate(level,seed+1000,r['generation']['template'],parameters=r['generation']['parameters'])
  assert r['question'][':question/id']==rr['question'][':question/id'] and r['generation']['mathematical_fingerprint']==rr['generation']['mathematical_fingerprint']
  if seed<2:reviews.append({'label':'Generated authored '+level+' #'+str(seed+1),'record':r});native.append(engine_checks(r,level+' '+str(seed)))
 assert len(tasks)>100 and len(positions)>3,(level,len(tasks),positions)
 diversity[level]={'samples':120,'distinct_meaningful_system_tasks':len(tasks),'correct_option_positions':sorted(positions)}
# Every supported default template at each eligible level, signed parameters.
for level,ts in [('easy',('pair_first','canonical_second','pair_second','difference')),('moderate',('pair_second','canonical_second')),('hard',('pair_second','canonical_second'))]:
 for t in ts:
  for seed in range(15):mathrows+=verify(g.generate(level,seed,t))
# Every explicit empirical profile also supports seeded recipe sampling.
for level,profile,t in [('easy','source_q12444','pair_first'),('hard','source_q12457_raw','pair_second'),('hard','source_q12457_repaired','pair_second'),('easy','source_q18483','difference')]:
 for seed in range(20):mathrows+=verify(g.generate(level,seed,t,profile=profile))
# Different complete banks share a mathematical task but not content identity.
empirical=g.generate('easy',7,'pair_first',parameters=g.SOURCE_PARAMETERS['q-12444'],profile='source_q12444')
method=g.generate('easy',7,'pair_first',parameters=g.SOURCE_PARAMETERS['q-12444'])
assert empirical['generation']['mathematical_fingerprint']==method['generation']['mathematical_fingerprint']
assert empirical['question'][':question/id']!=method['question'][':question/id']
assert g.SOURCE==json.loads((ROOT/'generate/runs/current/sources/17592186073753.json').read_text())
# Explicit invalid/level workload requests must fail, never resample.
rejected=0
for level,t,p in [('moderate','pair_first',g.SOURCE_PARAMETERS['q-12444']),('hard','canonical_second',dict(g.SOURCE_PARAMETERS['e-13010'],B=1)),('moderate','canonical_second',g.SOURCE_PARAMETERS['e-13010']),('easy','pair_second',g.SOURCE_PARAMETERS['q-12457'])]:
 try:g.generate(level,0,t,parameters=p)
 except ValueError:rejected+=1
 else:raise AssertionError('Invalid workload accepted')
# Mutation probes show validator catches printed stages, not only final roots.
import copy
for original,old,new in [(canon,'8 - 6v + 9v - 6','8 + 6v + 9v - 6'),(canon,'2(4','2(5')]:
 mutated=copy.deepcopy(original)
 if old not in mutated['question'][':question/worked-solution']:continue
 mutated['question'][':question/worked-solution']=mutated['question'][':question/worked-solution'].replace(old,new,1)
 try:verify(mutated)
 except AssertionError:pass
 else:raise AssertionError('Wrong stage not detected')
mapping=[]
for case in cases:
 orig=originals[case['source_id']];p=case['parameters'];vals,recipes=g.bank(p,case['template'],case['bank_profile'])
 rendered=[p['x']+' = '+g.tex(v[0])+', '+p['y']+' = '+g.tex(v[1]) if isinstance(v,tuple) else g.tex(v) for v in vals]
 field=orig[':question/answer-fields'][0]
 for a in field[':answer-field/choices']:
  i=[comparable(v) for v in rendered].index(comparable(a[':answer/value']))
  mapping.append({'source_id':case['source_id'],'source_field':field[':answer-field/id'],'source_field_type':field[':answer-field/type'],'source_key':field[':answer-field/key'],'source_answer':a,'profile':case['bank_profile'],'parameters':p,'recipe':recipes[i],'generated_value':rendered[i],'intent':'empirical numerical pattern; original intent not recovered','original_correct_ref_present':False})
write('source-choice-map.json',mapping)
write('review.json',reviews);write('engine-input.json',native)
binary=ROOT/'generate/runs/current/check-engine';subprocess.run([str(binary),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
report=json.loads((H/'engine-report.json').read_text())
validation={'pass':True,'status':'supported assessments pass; raw q12457 retained with explicit mathematical failure','provenance':g.PROVENANCE,'source_practice_count':3,'source_original_unrated_count':3,'source_bank_matches':3,'source_choice_value_matches':15,'source_raw_prompt_matches':0,'source_presentation_normalized_prompt_matches':3,'original_correct_designations_present':0,'original_correct_designations_matched':0,'mathematically_derived_missing_refs':2,'source_bank_mathematical_failures':1,'supported_source_bank_repairs':1,'practice_worked_solutions_present':0,'practice_solutions_authored':3,'canonical_solution_whitespace_and_literal_brace_normalized_match':True,'source_results':source_results,'default_random_instances_verified':instances,'displayed_equation_stage_rows_verified':mathrows,'difficulty_diversity':diversity,'explicit_workload_rejections':rejected,'incorrect_displayed_stage_mutation_probes':2,'native':{'accepted':report['accepted_checks'],'rejected':report['rejected_checks'],'unresolved':report['documented_unresolved_checks'],'entry_point':report['entry_point'],'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest()},'plots':'none','database_writes':0,'unresolved_findings':['Original q-12457 bank has no correct answer; public raw profile is evidence-only and lacks correct ref. Supported minimal bank repair documented.','Original practice difficulty, correct refs and worked solutions absent. Difficulty ratings and solutions are authored; inferred refs are not fidelity matches.','Empirical pair-bank numerical intent is underdetermined. Explicit observed profiles preserve full banks; defaults use whole method-derived banks.']}
write('validation.json',validation)
parts=['# Review: challenging substitution systems\n\nAll original practice questions are UNRATED. Ratings below are authored. The raw q-12457 profile is incomplete source evidence, with five wrong options and no correct ref.\n']
for case in cases:
 orig=originals[case['source_id']]
 parts.append('## Raw captured original '+case['source_id']+'\n\nUnrated; no correct ref or worked solution captured. Literal Markdown retained below as a code block so its unmatched source brace is visible.\n\n```text\n'+orig[':question/problem']+'\n```\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in orig[':question/answer-fields'][0][':answer-field/choices'])+'\n')
for item in reviews:
 r=item['record'];parts.append('## '+item['label']+'\n\nProfile `'+r['generation']['profile']+'`; authored level `'+r['generation']['level']+'`.\n\n'+g.markdown(r)+'\n')
(H/'review.md').write_text('\n'.join(parts))
print(json.dumps(validation,indent=2))
