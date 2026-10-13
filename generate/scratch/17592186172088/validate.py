#!/usr/bin/env python3
"""Independent displayed mathematics, source fidelity, finite scope and native QA."""
import importlib.util,itertools,json,re,subprocess,uuid,concurrent.futures,tempfile,hashlib
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z,i,j,k=s.symbols('x y z i j k',real=True);coordinates=(x,y,z);bases=(i,j,k)
ORIGINAL={'q-122559':(1,0,0),'q-122664':(0,0,2),'q-122651':(2,0,0),'q-122668':(0,-1,0),'q-122670':(0,0,-1),'q-123748':(-2,0,0),'q-123749':(0,-1,0),'q-123750':(1,0,0),'q-122662':(0,3,0),'q-122667':(-1,0,0),'authored-easy':(1,0,0)}

def parse(value):
 if value=='None of the listed':return None
 value=re.sub(r'(?:[.,]|\\,)+$', '', value)
 m=re.fullmatch(r'[FGHK]\(x,y,z\)=(.+)',value);assert m,value
 body=m[1].replace(r'\,','').replace('⁡','')
 body=re.sub(r'\\operatorname\{ln\}([xyz])',r'log(\1)',body);body=re.sub(r'\\operatorname\{sin\}([xyz])',r'sin(\1)',body)
 body=re.sub(r'\{e\}\^\{([xyz])\}',r'exp(\1)',body);body=body.replace('{','(').replace('}',')').replace('^','**')
 body=re.sub(r'([0-9xyz)])(?=[ijk])',r'\1*',body)
 expr=s.expand(parse_expr(body,local_dict={'x':x,'y':y,'z':z,'i':i,'j':j,'k':k,'sin':s.sin,'log':s.log,'exp':s.exp},transformations=standard_transformations+(implicit_multiplication_application,)))
 components=tuple(expr.coeff(b) for b in bases);assert s.simplify(expr-sum(c*b for c,b in zip(components,bases)))==0,value
 return components

def expected(profile,p):
 result=[0]*3
 for a,c in zip('xyz',ORIGINAL[profile]):result['xyz'.index(p['permutation']['xyz'.index(a)])]=c*p['flip']*p['scale']
 return tuple(map(s.sympify,result))
def compatible(pair,target):
 if pair is None:return False
 axis=next(n for n,c in enumerate(target) if c)
 return all(c==0 for n,c in enumerate(pair) if n!=axis) and not pair[axis].free_symbols and pair[axis]!=0 and s.sign(pair[axis])==s.sign(target[axis])

def formatting(text):
 assert text.count('$')%2==0,text
 assert text.count('{')==text.count('}'),text
 assert '@@' not in text
 assert not any(t in text for t in ('+-','--'))

def shape_math(r,allow_source_error=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 assert f[':answer-field/type']==':answer-field.type/radio';assert f[':answer-field/key']=='selection'
 answers=f[':answer-field/choices'];assert len(answers)==5;assert len({a[':answer/id'] for a in answers})==5
 for data,key in [(q,':question/id'),(f,':answer-field/id')]+[(a,':answer/id') for a in answers]:assert str(uuid.UUID(data[key]))==data[key]
 assert f[':answer-field/correct'][0]==':answer/id'
 selected=next(a[':answer/value'] for a in answers if a[':answer/id']==f[':answer-field/correct'][1])
 meta=r['generation'];profile=meta['bank_profile'].removeprefix('observed:');p=meta['parameters'];target=expected(profile,p)
 parsed={a[':answer/value']:parse(a[':answer/value']) for a in answers};math=[v for v in parsed.values() if v is not None];assert len(math)==4 and len(set(math))==4
 matches=[v for v,c in parsed.items() if compatible(c,target)]
 assert selected==(matches[0] if matches else 'None of the listed');assert len(matches)<=1
 assert tuple(map(s.sympify,meta['components']))==target
 # The generated plot/sidecar corresponds to the independent target; source image
 # sign/axis was inspected in original-contact.png, rather than inferred from IDs.
 plot=meta['plot'];assert Path(plot['prompt']).exists()
 if not plot['source_asset']:
  side=json.loads(Path(plot['sidecar']).read_text());assert tuple(map(s.sympify,side['exact_components']))==target
  assert side['zero_set']=='empty';assert len(side['grid'])==27 and len(side['vectors'])==27
  for vec in side['vectors']:assert tuple(vec)==tuple(float(v) for v in target)
 for a in answers:
  if a[':answer/type']==':answer.type/math':formatting(a[':answer/value'])
  else:assert a[':answer/value']=='None of the listed'
 for text in (q[':question/problem'],q[':question/worked-solution']):formatting(text)
 solution=q[':question/worked-solution'];axis=next(n for n,c in enumerate(target) if c);letter='xyz'[axis];basis='ijk'[axis]
 assert 'parallel to the $'+letter+'$-axis' in solution
 direction='positive' if target[axis]>0 else 'negative';assert '*'+direction+'* $'+letter+'$-direction' in solution
 bullets=re.findall(r'\n- (.*?)\n\n\$\$\n(.*?)\n\$\$',solution,re.S)
 assert len(bullets)==(2 if meta['authored'] else 3)
 eliminated=[]
 for stage,(prose,formula_block) in enumerate(bullets):
  expressions=re.split(r'\\,\s*(?=[FGHK]\()',formula_block)
  for formula in expressions:
   pair=parse(formula);assert pair in math,(formula,math);eliminated.append(pair)
   if stage==0:assert any(pair[n]!=0 for n in range(3) if n!=axis)
   elif stage==1:assert pair[axis].is_number and pair[axis]!=0 and s.sign(pair[axis])!=s.sign(target[axis])
   else:
    if allow_source_error and profile=='q-123750':
     assert pair[axis]==0 # source invalid component-only inference, explicitly counted
     assert any(c.free_symbols for c in pair)
    elif 'every component' in prose:assert any(c.free_symbols for c in pair)
    else:assert pair[axis].free_symbols,(prose,pair)
 assert len(eliminated)==(3 if matches else 4)
 if matches:assert 'vector field $'+selected+'.$' in solution
 else:assert "doesn't correspond to any of the listed" in solution
 # Constant targets have no zero set; variable distractor zero sets are checked
 # from actual displayed expressions at independent signed points.
 assert any(target) and all(not c.free_symbols for c in target)
 for pair in math:
  for c in pair:
   if c==0:continue
   if len(c.free_symbols)==1:
    var=next(iter(c.free_symbols))
    if c.has(s.exp):assert c.subs(var,-2)!=0 and c.subs(var,0)!=0 and c.subs(var,2)!=0
    elif c.has(s.log):assert c.subs(var,1)==0 and c.subs(var,2)!=0
    elif c.has(s.sin):assert c.subs(var,0)==0 and c.subs(var,s.pi/2)!=0
    else:assert c.subs(var,0)==0 and c.subs(var,-2)!=0 and c.subs(var,2)!=0
 return r

def fixture(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'each owned radio option'} for a in f[':answer-field/choices']]}

def main():
 source=json.loads((HERE/'source.json').read_text());assert source['basis']==1356
 cases=json.loads((HERE/'source-cases.json').read_text());assert len(cases)==10
 originals=[];native=[];matched_values=matched_designations=matched_solutions=0
 for case in cases:
  q=g.QUESTIONS[case['math_academy_id']];r=g.generate(case['level'],template=case['template'],profile=case['bank_profile'],parameters=case['parameters']);shape_math(r,True)
  f=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices']);matched_values+=5
  assert f[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);matched_designations+=1
  assert q[':question/worked-solution']==r['question'][':question/worked-solution'];matched_solutions+=1
  assert q[':question/problem'].split('\n\n',1)[1]==r['question'][':question/problem'].split('\n\n',1)[1]
  originals.append(r);native.append(fixture(case['math_academy_id']+' source',r))
 reviewed=[];catalog={level:set() for level in g.TEMPLATES};checked=0
 # Enumerate the whole finite signed-permutation/scale domain for every profile.
 for profile,(level,*_) in g.PROFILES.items():
  for perm,flip,scale in itertools.product(('xyz','xzy','yxz','yzx','zxy','zyx'),(-1,1),(1,2,3)):
   p={'permutation':perm,'flip':flip,'scale':scale};r=shape_math(g.generate(level,profile=profile,parameters=p,seed=checked));checked+=1;catalog[level].add(r['generation']['mathematical_fingerprint'])
   if perm in ('zxy','yzx') and flip==-1 and scale==2:
    reviewed.append(r);native.append(fixture(profile+' '+perm,r))
  # Seed/choice order and a common scale do not change task identity.
  p={'permutation':'zxy','flip':-1,'scale':2};a=g.generate(level,seed=2,profile=profile,parameters=p);b=g.generate(level,seed=100,profile=profile,parameters=p)
  assert a['question'][':question/id']==b['question'][':question/id'];assert a['generation']['content_fingerprint']==b['generation']['content_fingerprint']
  c=g.generate(level,profile=profile,parameters={**p,'scale':3});assert a['generation']['mathematical_fingerprint']==c['generation']['mathematical_fingerprint'];assert a['question'][':question/id']!=c['question'][':question/id']
  for bad in ({**p,'scale':0},{**p,'scale':4},{**p,'flip':0},{**p,'permutation':'xxx'},{**p,'scale':True}):
   try:g.generate(level,profile=profile,parameters=bad)
   except ValueError:pass
   else:raise AssertionError('Invalid explicit input accepted')
 assert all(len(v)==6 for v in catalog.values())
 # Fresh writes in private directory, concurrent identical and distinct geometry.
 with tempfile.TemporaryDirectory(prefix='kp3d-',dir=HERE) as td:
  pairs=[(s.Integer(1),s.Integer(0),s.Integer(0)),(s.Integer(1),s.Integer(0),s.Integer(0)),(s.Integer(0),s.Integer(-1),s.Integer(0))]
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
   outputs=list(pool.map(lambda pair:g.render_plots(pair,'authored-easy',{'permutation':'yzx','flip':1,'scale':1},td),pairs))
  for pair,out in zip(pairs,outputs):assert json.loads(Path(out['sidecar']).read_text())['exact_components']==[str(c) for c in pair]
  assert not list(Path(td).glob('input-*.json'))
 (HERE/'engine-input.json').write_text(json.dumps(native,indent=2));engine=HERE.parents[1]/'runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-results.json')],check=True)
 (HERE/'review.json').write_text(json.dumps(reviewed,indent=2,ensure_ascii=False)+'\n')
 text=['# Originals and generated variants\n\nOriginals use exact captured bank/prose. Generated variants are labeled and preserve the same elimination demands.']
 for r in originals:
  text.append('\n## ORIGINAL '+r['generation']['bank_profile']+'\n\n'+g.markdown(r))
  profile=r['generation']['bank_profile'].removeprefix('observed:')
  for v in reviewed:
   if v['generation']['bank_profile']==profile:text.append('\n### GENERATED '+str(v['generation']['parameters'])+'\n\n'+g.markdown(v))
 text.append('\n## AUTHORED EASY (missing observed level)')
 for v in reviewed:
  if v['generation']['authored']:text.append('\n### GENERATED '+str(v['generation']['parameters'])+'\n\n'+g.markdown(v))
 (HERE/'review.md').write_text('\n'.join(text))
 results={'status':'pass','source_questions':10,'source_bank_values':{'matched':matched_values,'total':50},'source_distractors':{'matched':40,'total':40},'source_complete_banks':{'matched':10,'total':10},'source_correct_designations':{'matched':matched_designations,'total':10},'source_worked_solutions_raw_exact':{'matched':matched_solutions,'total':10},'normal_solutions_mathematically_supported':{'matched':10,'total':10},'source_solution_reasoning_error':{'q-123750':'component constancy cannot exclude a different-axis field; observed replay preserved, normal every-component constancy repair'},'authored_missing_level':'easy constant axis/sign recognition','enumerated_instances':checked,'meaningful_target_catalog_by_level':{k:len(v) for k,v in catalog.items()},'review_records':len(reviewed),'engine_provenance':{'binary_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(engine.with_suffix('.rs').read_bytes()).hexdigest()},'native':json.loads((HERE/'engine-results.json').read_text()),'fresh_concurrent_plot_checks':3,'database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS: 10 source banks, 50 values, 10 solutions; '+str(checked)+' complete domain instances; native '+str(len(native)*5)+' checks.')
if __name__=='__main__':main()
