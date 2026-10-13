"""Independent displayed-math, source fidelity, raster and real grading checks."""
import importlib.util,json,re,hashlib,subprocess,itertools,concurrent.futures,sys
from pathlib import Path
from PIL import Image
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('gen',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,C=sp.symbols('x C',real=True)

def math_read(s):
 s=s.strip().rstrip('.,?').replace('\u2061','').replace(r'\,','').replace(' ','').replace(r'\pi','pi')
 # Independent complete algebra reader, recursively reading simple TeX fractions.
 while r'\frac' in s:
  new=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
  if new==s:raise AssertionError('Unparsed fraction '+s)
  s=new
 return parse_expr(s,local_dict={'x':x,'C':C,'pi':sp.pi},transformations=standard_transformations+(implicit_multiplication_application,))

def source_no_paths(s):return re.sub(r'!\[\]\(.*?\)','![](PLOT)',s)

def formatting(s):
 # Actual decoded strings, balanced math delimiters and braces (no masking).
 assert s.count('$$')%2==0
 rest=re.sub(r'\$\$.*?\$\$','',s,flags=re.S);assert rest.count('$')%2==0
 n=0
 for ch in s:
  if ch=='{':n+=1
  elif ch=='}':n-=1;assert n>=0
 assert n==0
 assert '--' not in s and '+-' not in s

def validate_record(r):
 assert set(r)=={'knowledge_point','question','generation'} and set(r['knowledge_point'])=={'db_id','id','title'}
 json.dumps(r)
 q=r['question'];p=r['generation']['parameters'];B=sp.Rational(p['B']);a=sp.Rational(p['c'])*sp.pi;fn=p['fn']
 prompt=q[':question/problem'];solution=q[':question/worked-solution'];formatting(prompt);formatting(solution)
 # Read displayed prompt's function argument independently of generation metadata.
 m=re.search(r'\$y=\\operatorname\{(tan|cot)\}\u2061\((.*?)\),\$',prompt)
 assert m and m[1]==fn
 arg=math_read(m[2]);assert sp.expand(arg-(B*x+C))==0
 assert r'-\frac{\pi }{2}<C<\frac{\pi }{2}' in prompt
 field=q[':question/answer-fields'][0];assert field[':answer-field/type']==':answer-field.type/radio'
 values=[math_read(v[':answer/value']) for v in field[':answer-field/choices']]
 correct=next(v for v in field[':answer-field/choices'] if v[':answer/id']==field[':answer-field/correct'][1]);assert sp.simplify(math_read(correct[':answer/value'])-a)==0
 if r['generation']['eligible_for_learning']:
  expected=[a,-a,a/B,a/(B*B),a-sp.sign(a)*sp.pi/2]
  assert len(values)==len(expected)==5
  for v in expected:assert sum(sp.simplify(v-w)==0 for w in values)==1
  for v,w in itertools.combinations(values,2):assert not sp.simplify((v-w)/sp.pi).is_integer
 # All actual displayed function arguments in fixed solution; formal row must
 # preserve Bx+C, baseline Bx, or factored B(x+C/B); validate expanded args.
 function_args=re.findall(r'(?:\\operatorname\{(?:tan|cot)\}\u2061|(?:tan|cot)\\,)\((.*?)\)(?=\$|\.|\\end| \\\\|\n)',solution)
 assert len(function_args)>=3
 for body in function_args:
  parsed=math_read(body)
  assert sp.expand(parsed-B*x) in [0,C],(body,parsed)
 block=re.findall(r'\$\$(.*?)\$\$',solution,re.S)
 assert len(block)==2
 assert r'\begin{aligned}y & =' in block[0] and r' \\  & =' in block[0]
 # Explicit first factorization arguments extracted structurally from printed row.
 left,right=block[0].strip().removeprefix(r'\begin{aligned}y & =').removesuffix(r'\end{aligned}').split(r' \\  & =')
 def inner(form):
  return re.sub(r'^\\operatorname\{(?:tan|cot)\}\u2061\(','',form).removesuffix(')')
 assert sp.expand(math_read(inner(left))-math_read(inner(right)))==0
 # Check every calculation chain equality using actual printed fragments.
 stages=block[1].strip().rstrip('.').split(r'\,⟹\,')
 assert len(stages)==(3 if q[':question/difficulty'].endswith('/hard') else 2)
 for stage in stages:
  lhs,rhs=stage.split('=');assert sp.simplify(math_read(lhs).subs(C,a)-math_read(rhs).subs(C,a))==0,(stage,a)
 # Read distance expression and the direction from final prose. Every displayed
 # subtraction term remains separately verified before its reduced scalar.
 dm=re.search(r'by \$(.*?)\$ units to the (left|right)',solution);assert dm
 terms=dm[1].split('=');distance=abs(a/B)
 for term in terms:assert sp.simplify(math_read(term)-distance)==0
 assert dm[2]==('left' if a>0 else 'right')
 if q[':question/difficulty'].endswith('/easy'):
  em=re.search(r'displacement between the two marked zeros is \$(.*?)\$ units to the (left|right)',prompt)
  assert em and sp.simplify(math_read(em[1])-distance)==0 and em[2]==dm[2]
 if 'Since $' in solution:
  am=re.search(r'the value of \$C\$ is \$(.*?)\$',solution);assert am and sp.simplify(math_read(am[1])-a)==0
 if r['generation']['eligible_for_learning']:
  for asset in r['generation']['plot_assets'].values():
   side=json.load(open(Path(asset).with_suffix('.json')))
   assert side['input']=={'B':str(B),'c':str(a/sp.pi),'fn':fn,'level':q[':question/difficulty'].split('/')[-1]}
   inferred_phase=-float(B)*side['zero']+(0 if fn=='tan' else float(sp.pi/2))
   assert abs(inferred_phase-float(a))<1e-12
   assert side['minimum_label_curve_clearance_px']>10
   assert all(s['blue_pixels']>0 for s in side['curve_pixel_samples'])
   assert all(s['gray_pixels']>0 for s in side['asymptote_pixels'])
 return True

def inspect_sources():
 """Own origin/scale per plot; actual pixel zero/pole and branch-order checks."""
 assets=json.load(open(HERE/'assets.json'));out=[]
 sources={q[':question/math-academy-id']:q for q in g.RAW['record'][':knowledge-point/questions']}
 for i,a in enumerate(assets):
  im=Image.open(HERE/'inspection'/f'{i}.png').convert('RGB');w,h=im.size
  import numpy as np
  pixels=np.array(im).astype(int)
  if a['source_id']=='e-3669':B=sp.Rational(2);c=sp.Rational(-1,4);fn='tan'
  else:
   cfg=g.RECIPES[a['source_id']];B=sp.Rational(cfg['B']);c=sp.Rational(cfg['c']);fn=cfg['fn']
  if w<200 or h<100:
   out.append({'index':i,**a,'dimensions':[w,h],'kind':'canonical math glyph','inspected_individually':True});continue
  # All source plots use the main horizontal axis at row 157/158, but detect it.
  black=pixels.max(2)<90;y0=int(np.argmax(black[90:220,:].sum(1)))+90
  x0=int(np.argmax(black[:140,:].sum(0)))
  gray=(pixels.max(2)-pixels.min(2)<10)&(pixels.min(2)>110)&(pixels.min(2)<220)
  columns=[j for j in range(w) if gray[20:140,j].sum()>14]
  groups=[]
  for j in columns:
   if not groups or j>groups[-1][-1]+1:groups.append([j])
   else:groups[-1].append(j)
  poles=[sum(k)/len(k) for k in groups]
  phase=c*sp.pi;z0=0 if fn=='tan' else sp.pi/(2*B);z=z0-phase/B;L=z-sp.pi/(2*B);R=z+sp.pi/(2*B)
  # Prompt exact original L/R guides are separately identified by nearest expected
  # positions under the fitted origin; solution may also add baseline guides.
  viable=[]
  for l,r in itertools.combinations(poles,2):
   scale=(r-l)/float(R-L);origin=l-scale*float(L)
   if abs(origin-x0)<4:viable.append((abs(origin-x0),l,r,scale,origin))
  assert viable,(a,poles,x0)
  _,lp,rp,scale,origin=min(viable)
  blue=(pixels[:,:,2]-pixels[:,:,0]>40)&(pixels[:,:,2]-pixels[:,:,1]>12)
  zero_px=origin+scale*float(z)
  roi=blue[y0-6:y0+7,max(0,int(zero_px)-6):int(zero_px)+7]
  assert roi.any(),(a,'zero',zero_px,y0)
  # Read curve samples on each side of the marked zero: tan increases, cot falls.
  order=[]
  for sign in [-1,1]:
   px=int(round(zero_px+sign*(rp-lp)*.12));ys=np.where(blue[:h,px])[0]
   expected_side=-sign if fn=='tan' else sign
   assert any((v-y0)*expected_side>0 for v in ys),(a,px,ys)
   order.append({'x_pixel':px,'blue_rows':[int(v) for v in ys]})
  out.append({'index':i,**a,'dimensions':[w,h],'kind':'graph','inspected_individually':True,'origin_px':[x0,y0],'fitted_origin_px':origin,'x_pixels_per_unit':scale,'left_right_guide_pixels':[lp,rp],'left_right_values':[str(L),str(R)],'zero_value':str(z),'zero_pixel':zero_px,'branch_domain':[str(L),str(R)],'monotonicity':'increasing' if fn=='tan' else 'decreasing','actual_blue_order_samples':order,'ordinate_scale':'unlabelled; no quantitative y-tick recovery claimed'})
 (HERE/'source-plot-inspection.json').write_text(json.dumps(out,indent=2)+'\n')
 return len(out)

def main():
 cases=json.load(open(HERE/'source-cases.json'));originals=g.RAW['record'][':knowledge-point/questions'];all_records=[];counts={'sources':len(cases),'complete_bank_values':0,'exact_bank_spelling':0,'correct_designations':0,'exact_prompt_solution_masks':0,'opaque_ineligible':0,'periodic_source_banks':[]}
 for case,q in zip(cases,originals):
  r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);validate_record(r);all_records.append(r)
  # Attribute-presence parity for every captured assessment attribute: all here
  # have fields, difficulty, worked solution and correct refs. Capture-only DB
  # IDs / MA IDs are provenance, not invented generated entities.
  for key in [':question/problem',':question/answer-fields',':question/difficulty',':question/worked-solution']:
   assert (key in q)==(key in r['question'])
  for role in ['problem','worked-solution']:
   assert r['question'][':question/'+role]==q[':question/'+role]
  counts['exact_prompt_solution_masks']+=1
  field=r['question'][':question/answer-fields'][0];old=q[':question/answer-fields'][0]
  before=[math_read(v[':answer/value']) for v in old[':answer-field/choices']];after=[math_read(v[':answer/value']) for v in field[':answer-field/choices']]
  assert sorted(v[':answer/value'] for v in old[':answer-field/choices'])==sorted(v[':answer/value'] for v in field[':answer-field/choices'])
  counts['exact_bank_spelling']+=5
  assert len(before)==len(after)==5
  for v in before:assert sum(sp.simplify(v-w)==0 for w in after)==1;counts['complete_bank_values']+=1
  assert sp.simplify(math_read(old[':answer-field/correct'][':answer/value'])-math_read(next(v[':answer/value'] for v in field[':answer-field/choices'] if v[':answer/id']==field[':answer-field/correct'][1])))==0
  counts['correct_designations']+=1;counts['opaque_ineligible']+=1
  if r['generation']['source_bank_issue']:counts['periodic_source_banks'].append(case['source_id'])
  # Parameterized raw replay is exercised through normal public API.
  varied=dict(case['parameters']);varied['c']=str(sp.Rational(varied['c'])*sp.Rational(4,5))
  vr=g.generate(case['level'],template=case['template'],parameters=varied,profile=case['bank_profile']);validate_record(vr);all_records.append(vr)
  varied_B=dict(varied);varied_B['B']='3/4' if case['level']=='hard' else '4'
  validate_record(g.generate(case['level'],template=case['template'],parameters=varied_B,profile=case['bank_profile']))
 normal=[];task_counts={}
 for level in ['easy','moderate','hard']:
  meaningful=set()
  for B,c,fn in itertools.product(g.parameter_domain(level),g.PHASES,['tan','cot']):
   try:g.authored_bank(B,c,fn)
   except ValueError:continue
   meaningful.add((str(B),str(c),fn))
  task_counts[level]=len(meaningful)
  # Default sampler serves BOTH source-shaped families, all levels.
  seen=set()
  for seed in range(8):
   r=g.generate(level,seed);validate_record(r);normal.append(r);seen.add(r['generation']['parameters']['fn'])
   replay=g.generate(level,seed+900,template=r['generation']['template'],parameters=r['generation']['parameters'])
   assert r['question'][':question/id']==replay['question'][':question/id']
  assert seen=={'tan','cot'}
  # Phase aliases and scope-degenerate rational B values must be rejected explicitly.
  for bad in [{'B':'1','c':'1/5','fn':'tan'},{'B':'2','c':'6/5','fn':'tan'}]:
   try:g.generate(level,parameters=bad);raise AssertionError('Accepted invalid explicit parameters')
   except ValueError:pass
 # Concurrency with fresh unique assets; no active-cache pruning.
 for f in (HERE/'plots').glob('render-*.json'):raise AssertionError('Leaked renderer input '+str(f))
 fresh=[]
 for fn in ['tan','cot']:
  for B,c in itertools.product(g.parameter_domain('moderate'),g.PHASES):
   try:g.authored_bank(B,c,fn)
   except ValueError:continue
   key=hashlib.sha256(json.dumps([str(B),str(c),fn,'moderate',g.VERSION]).encode()).hexdigest()[:24]
   if not (HERE/'plots'/(key+'-prompt.png')).exists():
    fresh.append({'B':str(B),'c':str(c),'fn':fn});break
  else:raise AssertionError('No remaining fresh concurrency case')
 concurrent_params=[fresh[0],fresh[0],fresh[1]]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  parallel=list(pool.map(lambda p:g.generate('moderate',parameters=p),concurrent_params))
 assert parallel[0]['question'][':question/id']==parallel[1]['question'][':question/id']
 for r in parallel:validate_record(r)
 all_records+=normal+parallel
 # Real native grader: radio IDs assess the actual representative, not CAS phase
 # aliases. Independent phase checks above prevent ambiguity even outside bounds.
 engine=[]
 for i,r in enumerate(all_records):
  field=r['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1]
  checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'exact source-shaped principal scalar radio selection'} for a in field[':answer-field/choices']]
  engine.append({'label':str(i),'record':r,'checks':checks})
 (HERE/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
 subprocess.run([str(HERE.parents[1]/'runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 source_assets=inspect_sources()
 result={'passed':True,'source_fidelity':counts,'source_assets_individually_inspected':source_assets,'normal_records_checked':len(normal),'changed_B_evidence_records_checked':len(cases),'concurrent_records_checked':len(parallel),'meaningful_eligible_task_counts':task_counts,'full_solution_stages_checked':len(all_records)+len(cases),'native_grading':json.load(open(HERE/'engine-report.json')),'native_equivalence_limitation':'Radio selection tests IDs only. Phase aliases are checked mathematically and rejected whole-bank; representative criterion disqualifies outside-interval entries. No invented blank-equivalence claim.','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(all_records,indent=2,ensure_ascii=False)+'\n')
 review=['# Source originals and generated variants\n','Frozen math basis 1356. Every observed profile is opaque evidence only; normal variants use the labeled authored method bank.\n']
 for case,q,r,variant in zip(cases,originals,all_records[::2],all_records[1::2]):
  review+=['## '+case['source_id']+' — original\n',q[':question/problem'], '\nBank: '+', '.join('$'+v[':answer/value']+'$' for v in q[':question/answer-fields'][0][':answer-field/choices']),q[':question/worked-solution'],'\n### Parameterized generated evidence variant\n',variant['question'][':question/problem'],variant['question'][':question/worked-solution'],'\nBank: '+', '.join('$'+v[':answer/value']+'$' for v in variant['question'][':question/answer-fields'][0][':answer-field/choices'])]
 for r in normal:
  review+=['\n## Authored generated '+r['question'][':question/difficulty'].split('/')[-1]+' — '+r['generation']['template']+'\n',r['question'][':question/problem'],'\nBank: '+', '.join('$'+v[':answer/value']+'$' for v in r['question'][':question/answer-fields'][0][':answer-field/choices']),r['question'][':question/worked-solution']]
 (HERE/'review.md').write_text('# Source originals and generated variants\n\nFrozen math basis 1356; raw profiles are ineligible evidence.\n\n'+'\n\n'.join(markdown_record(r) for r in all_records)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='native_grading'},indent=2))
def markdown_record(r):
 q=r['question'];meta=r['generation'];level=q[':question/difficulty'].split('/')[-1];raw=meta['evidence_only']
 original=raw and all(str(meta['parameters'][k])==str(g.RECIPES[meta['profile'].split(':',1)[1]][k]) for k in ('B','c','fn'))
 label='ORIGINAL SOURCE' if original else 'GENERATED EVIDENCE VARIANT' if raw else 'GENERATED VARIANT'
 def preview(z):return re.sub(r'(!\[[^]]*\]\()(images/[^)]+)(\))',lambda m:m[1]+'/media/jake/SSD/EDB/math/'+m[2]+m[3],z)
 f=q[':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 return '## '+label+' — '+level+' / '+meta['template']+'\n\n'+meta['profile']+'; '+('ineligible evidence' if raw else 'eligible authored bank')+'\n\n'+preview(q[':question/problem'])+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **designated correct**' if a[':answer/id']==key else '') for a in f[':answer-field/choices'])+'\n\n'+preview(q[':question/worked-solution'])
if __name__=='__main__':main()
