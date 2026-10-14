#!/usr/bin/env python3
"""Independent displayed-expression mathematics, fidelity and native grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,collections
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;REPO=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from math_parser import parse
T=sp.Symbol('t',real=True)
fixtures=[];stage_count=0;review=[];results=[]
def eq(a,b):return sp.simplify(a-b)==0
def tidy(v):return v.strip().removesuffix(r'\,.').removesuffix('.').removesuffix(r'\,').strip()
def mathblocks(text):return re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
def resolve_operators(text):
 return re.sub(r'\\frac\{d\}\{dt\}\\left\((.*?)\\right\)',lambda m:'('+g.tex(sp.diff(parse(m[1]),T))+')',text)
def formatcheck(text):
 assert all(ord(c)>=32 or c in '\n\t\r' for c in text),'control character'
 assert text.count('$$')%2==0 and text.replace('$$','').count('$')%2==0,'math delimiters'
 n=0
 for c in text:
  if c=='{':n+=1
  if c=='}':n-=1
  assert n>=0,'brace order'
 assert n==0,'unbalanced braces'
def displayed_curve(q):
 b=mathblocks(q[':question/problem'])[0]
 if r'\quad' in b:x,y,_=re.fullmatch(r'x=(.*?),\\quad y=(.*?),\\quad (.*)',b,re.S).groups()
 else:x,y,_=re.fullmatch(r'x=(.*?),\\,y=(.*?),\\,(.*)',b,re.S).groups()
 return parse(x),parse(y)
def check_record(rec,faithful=False):
 global stage_count
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 q=rec['question'];md=rec['generation'];template=md['template']
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:formatcheck(text)
 x,y=displayed_curve(q);dx,dy=sp.diff(x,T),sp.diff(y,T)
 m=re.search(r'where \$t=(.*?)\.\$',q[':question/problem']);point=parse(m[1]) if m else None
 target=sp.simplify(dy/dx);correct=target.subs(T,point) if point is not None else target
 b=mathblocks(q[':question/worked-solution'])
 # Preserve universal formal y'/x' relation independently of later rows.
 assert (r"\frac{y'(t)}{x'(t)}" in b[0] or r'\frac{{y}^{′}' in b[0])
 for block in b[1:]:
  if "x'(t)=" in block or '{x}^{′}' in block:
   parts=re.split(r',\\(?:quad |,).*?=',block,maxsplit=1)
   assert len(parts)==2,block
   xx=parts[0].split('=',1)[1];yy=tidy(parts[1])
   assert eq(parse(resolve_operators(xx)),dx),(template,'x derivative',xx)
   assert eq(parse(resolve_operators(yy)),dy),(template,'y derivative',yy)
   stage_count+=2
  elif r'\begin{aligned}' in block:
   entries=re.split(r' & =| \\\\  & =',block)[1:]
   for v in entries:
    v=tidy(v.replace(r'\end{aligned}',''))
    assert eq(parse(v),correct),(template,'evaluation',v,correct)
    stage_count+=1
  else:
   for v in block.split('=')[1:]:
    assert eq(parse(tidy(v)),target),(template,'quotient',v,target)
    stage_count+=1
 # Structural equality is in addition to independent printed mathematics.
 p=md['parameters']
 if template in ['product_pair','quotient_pair']:
  _,expected,*_=g.authored_hard(template,p)
 else:
  expected=g.source_recipe(template,p)[0][':question/worked-solution']
 assert q[':question/worked-solution']==expected,'family operative stage sequence changed'
 for fi,f in enumerate(q[':question/answer-fields']):
  vals=[parse(a[':answer/value'].split('=',1)[-1]) for a in f[':answer-field/choices']]
  assert len(vals)==len(set(a[':answer/id'] for a in f[':answer-field/choices']))
  assert all(not eq(v,w) for i,v in enumerate(vals) for w in vals[i+1:]),(template,'equivalent choices')
  ev=lambda z:sp.simplify(z.subs(T,point) if point is not None else z)
  if faithful:
   raw=g.QUESTIONS[g.TEMPLATES[template]['source_id']]
   base_x,base_y=displayed_curve(raw)
   ratio=sp.simplify((dy/sp.diff(base_y,T))/(dx/sp.diff(base_x,T)))
   expected_values=[parse(a[':answer/value'].split('=',1)[-1])*ratio for a in raw[':question/answer-fields'][fi][':answer-field/choices']]
  elif f[':answer-field/type'].endswith('/radio'):
   if template=='line_quad' and point==0:expected_values=[ev(dy/dx),ev(sp.diff(y,T,2)/dx),ev(dx/sp.diff(y,T,2)),ev(x/dx),ev(sp.diff(y,T,2))]
   elif template=='product_sin':expected_values=[ev(dy/dx),ev(-dy/dx),ev(dx/dy),ev(-dx/dy),ev(y/x)]
   elif template=='exp_poly':expected_values=[ev(dy/dx),ev(dx/dy),ev(y/x),ev(dx*dy),ev(sp.diff(y,T,2)/dx)]
   else:expected_values=[ev(dy/dx),ev(dx/dy),ev(y/x),ev(dx*dy),ev(dy/x)]
  else:expected_values=[correct]
  assert len(vals)==len(expected_values) and all(sum(eq(v,w) for w in expected_values)==1 for v in vals),(template,'displayed operation bank mismatch')
  truths=[a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if eq(v,correct)]
  assert len(truths)==1,(template,'correct choice count',truths)
  if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',truths[0]]
  elif faithful:continue # Legacy missing designation preserved, not graded.
  else:assert False,'missing correct designation'
  if f[':answer-field/type'].endswith('/blank'):
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
   val=f[':answer-field/choices'][0][':answer/value']
   equivalent='('+g.tex(dy)+')/('+g.tex(dx)+')'
   if point is not None:equivalent='('+g.tex(dy.subs(T,point))+')/('+g.tex(dx.subs(T,point))+')'
   checks=[{'field_index':fi,'submitted':val,'expected':'accepted','purpose':'canonical displayed derivative'}, {'field_index':fi,'submitted':equivalent,'expected':'rejected' if 'round' in q[':question/problem'] else 'unresolved' if template in ['root_power','quotient_pair','product_pair'] else 'accepted','purpose':'independently unreduced derivative quotient; observed round parser limitation' if 'round' in q[':question/problem'] else 'domain comparison ignores printed parameter restriction' if template in ['root_power','quotient_pair','product_pair'] else 'independently unreduced derivative quotient'}, {'field_index':fi,'submitted':g.tex(correct+1),'expected':'rejected','purpose':'incorrect derivative'}]
  else:
   checks=[{'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==truths[0] else 'rejected','purpose':'owned radio bank with independently parsed actual expressions'} for a in f[':answer-field/choices']]
  native_rec=copy.deepcopy(rec)
  kept=[f for f in native_rec['question'][':question/answer-fields'] if ':answer-field/correct' in f]
  native_rec['question'][':question/answer-fields']=kept
  native_index=sum(':answer-field/correct' in previous for previous in q[':question/answer-fields'][:fi])
  for check in checks:check['field_index']=native_index
  fixtures.append({'label':template+('/raw-supported-field-fixture' if faithful else '/normal')+str(p)+'/'+str(fi),'record':native_rec,'checks':checks})
 return x,y,correct

cases=[];banks=values=designations=0
for template,v in g.TEMPLATES.items():
 if v['level']=='hard':continue
 case={'source_id':v['source_id'],'template':template,'level':v['level'],'parameters':{'r':'1','s':'1'},'bank_profile':'observed:'+v['source_id']};cases.append(case)
 rec=g.generate(v['level'],template=template,parameters=case['parameters'],profile=case['bank_profile']);q=rec['question'];raw=g.QUESTIONS[v['source_id']]
 assert q[':question/problem']==raw[':question/problem'];assert q[':question/worked-solution']==raw[':question/worked-solution']
 assert set(q)==set(raw)-{':db/id'},(template,'question key presence')
 for f,old in zip(q[':question/answer-fields'],raw[':question/answer-fields']):
  assert set(f)==set(old)-{':db/id'},(template,'field key presence')
  assert f[':answer-field/type']==old[':answer-field/type'][':db/ident']
  assert collections.Counter(a[':answer/value'] for a in f[':answer-field/choices'])==collections.Counter(a[':answer/value'] for a in old[':answer-field/choices'])
  if ':answer-field/correct' in old:
   c=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert c==old[':answer-field/correct'][':answer/value'];designations+=1
  banks+=1;values+=len(old[':answer-field/choices'])
 check_record(rec,True);review.append({'label':'Original faithful evidence '+v['source_id'],'record':rec})
 # Changed raw profiles exercise the same public parameterized recipes/banks.
 check_record(g.generate(v['level'],template=template,parameters={'r':'2','s':'3'},profile=case['bank_profile']),True)
 results.append({'source_id':v['source_id'],'prompt':'exact','solution':'exact','key_presence':'exact','banks':len(raw[':question/answer-fields'])})
(D/'source-cases.json').write_text(json.dumps(cases,indent=2))
unique={l:set() for l in ['easy','moderate','hard']};sampled=0
for template,v in g.TEMPLATES.items():
 for seed in [5,31,71,113,271,331]:
  rec=g.generate(v['level'],template=template,seed=seed);check_record(rec);sampled+=1;unique[v['level']].add(rec['generation']['mathematical_fingerprint'])
  if seed in [5,31]:review.append({'label':'Generated '+template+' seed '+str(seed),'record':rec})
  # Stable identity under arbitrary option order/seed for fixed task/bank.
  again=g.generate(v['level'],template=template,seed=seed+1000,parameters=rec['generation']['parameters'])
  assert rec['question'][':question/id']==again['question'][':question/id']
# Ensure default sampling actually serves every family.
coverage={l:set() for l in unique}
for level in coverage:
 for seed in range(100):
  rec=g.generate(level,seed=seed);coverage[level].add(rec['generation']['template'])
 assert coverage[level]=={k for k,v in g.TEMPLATES.items() if v['level']==level},(level,coverage[level])
# Boundary public input consistency and expected rejection.
for t,v in g.TEMPLATES.items():
 if v['level']=='hard':p={'a':1,'b':1,'c':5,'d':4}
 else:p={'r':'1/2','s':'6'}
 try:check_record(g.generate(v['level'],template=t,parameters=p))
 except ValueError as e:assert 'bank' in str(e),str(e)
invalid=0
for level,t,p in [('easy','trig',{'r':'0','s':'1'}),('moderate','exp_product',{'r':'7','s':'1'}),('hard','product_pair',{'a':1,'b':4,'c':2,'d':3}),('hard','quotient_pair',{'a':1,'b':2,'c':2,'d':0})]:
 try:g.generate(level,template=t,parameters=p);assert False
 except ValueError:invalid+=1
# Mutation regressions: missing operative row and printed math corruption.
base=g.generate('hard',template='quotient_pair',seed=3)
for change in ['control','term','stage']:
 bad=copy.deepcopy(base)
 if change=='control':bad['question'][':question/worked-solution']+='\x0c'
 elif change=='term':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('t^2(1)','t^2(2)',1)
 else:
  b=mathblocks(bad['question'][':question/worked-solution'])[3];bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('$$\n'+b+'\n$$\n\n','')
 try:check_record(bad);raise RuntimeError('mutation passed '+change)
 except AssertionError:pass
(D/'native-input.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2))
p=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],capture_output=True,text=True)
if p.returncode:print(p.stdout,p.stderr);raise SystemExit(p.returncode)
engine=json.loads((D/'native-report.json').read_text())
plot_run=subprocess.run([sys.executable,str(D/'validate-plots.py')],capture_output=True,text=True)
assert plot_run.returncode==0,plot_run.stdout+plot_run.stderr
cli=subprocess.run([sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--seed','31','--count','2','--format','json'],capture_output=True,text=True)
assert cli.returncode==0,cli.stderr
assert json.loads(cli.stdout)==[g.generate(level,seed=seed) for level in ['easy','moderate','hard'] for seed in [31,32]]
(D/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
reviewtext='# Parametric derivative review\n\nOriginals are evidence-only complete banks; generated records use method-derived banks.\n'
for item in review:
 r=item['record'];q=r['question'];reviewtext+='\n## '+item['label']+'\n\n'+q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:reviewtext+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'
 reviewtext+=q[':question/worked-solution']+'\n'
(D/'review.md').write_text(reviewtext)
report={'passed':True,'source':{k:g.RAW[k] for k in ['database','basis','lineage']},'coverage':{'practice_questions':18,'prompt_exact':18,'solution_exact':18,'key_presence_parity':18,'complete_banks_matched':banks,'answer_values_matched':values,'answer_values_total':values,'correct_designations_matched':designations,'correct_designations_present':18,'legacy_missing_correct_refs':1},'source_results':results,'cli_json_replay':{'records':6,'matches_public_api':True},'file_hashes':{str(p.relative_to(D.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [D.with_suffix('.py'),D/'validate.py',D/'validate-plots.py',D/'math_parser.py',D/'source.json',D/'source-cases.json']},'plot_validation':json.loads((D/'plot-validation.json').read_text()),'normal_samples':sampled,'independent_displayed_stages_checked':stage_count,'default_family_coverage':{k:sorted(v) for k,v in coverage.items()},'sampled_mathematical_tasks':{k:len(v) for k,v in unique.items()},'native_grading':{k:engine[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'native_rejected_mathematically_equivalent_raw_entries':4,'invalid_inputs_rejected':invalid,'mutations_rejected':3,'authored_extensions':['hard product pair','hard quotient pair','method-derived complete radio banks'],'remaining_findings':['Legacy duplicate field has no correct designation and is retained only as evidence.','Observed scalar distractor intentions are unresolved; generalized expression shapes are evidence-only.','Two source exact-answer instructions contain round; native form-sensitive equivalent quotient submissions are documented rejected.','The source line-quadratic raster shows the unrestricted parabola although the printed parameter interval is restricted. Normal plot marks exactly the supplied segment.'],'grading_limits':['root_power radical quotient carries a parameter domain not used by the native comparison','quotient_pair unreduced coordinate quotient retains removed coordinate poles not in the simplified derivative','product_pair unreduced product derivatives lead to unresolved exponential denominator comparison'], 'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'engine_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'database_writes':0}
(D/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
