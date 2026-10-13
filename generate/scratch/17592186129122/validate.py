"""Independent read-back QA of every printed prompt, complete bank and solution."""
import copy, hashlib, importlib.util, json, pathlib, re, subprocess, sys
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=pathlib.Path(__file__).parent;REPO=H.parents[2]
spec=importlib.util.spec_from_file_location('g',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,B=sp.symbols('x B');TRANS=standard_transformations+(implicit_multiplication_application,)
def save(n,v):(H/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def balanced(t):
 assert t.count('$')%2==0,'unbalanced math delimiter'
 level=0
 for i,c in enumerate(t):
  if c=='{':level+=1
  if c=='}':level-=1;assert level>=0,'unbalanced brace'
 assert level==0,'unbalanced brace'
 assert not any(z in t for z in ('@','--','+-')),'bad generated tokens'
def group(t,pos):
 assert t[pos]=='{';depth=1;i=pos+1
 while depth:
  depth+=(t[i]=='{')-(t[i]=='}');i+=1
 return t[pos+1:i-1],i

def parse(t):
 t=t.strip().rstrip('.,?');t=t.replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\dfrac',r'\frac').replace('π',r'\pi')
 # Degree marks denote the source's declared angular scale, not exponentiation.
 t=t.replace('^{∘}','').replace('^∘','')
 while r'\frac' in t:
  i=t.rfind(r'\frac');a,j=group(t,i+5);b,k=group(t,j);t=t[:i]+'(('+str(parse(a))+')/('+str(parse(b))+'))'+t[k:]
 while '|' in t:
  i=t.index('|');j=t.index('|',i+1);t=t[:i]+'Abs('+t[i+1:j]+')'+t[j+1:]
 t=t.replace(r'\pi','pi').replace('{','(').replace('}',')')
 return parse_expr(t,local_dict={'pi':sp.pi,'x':X,'B':B,'Abs':sp.Abs},transformations=TRANS)

def prompt_math(q):
 text=q[':question/problem'];balanced(text);parts=re.findall(r'\$(.*?)\$',text,re.S);assert len(parts)==1
 expr=parts[0];assert expr.split('=',1)[0].strip() in ('f(x)','y'),'incorrect dependent-function label';m=re.search(r'\\(?:operatorname\{(sin|cos)\}|(sin|cos))',expr);assert m
 trig=m.group(1) or m.group(2);tail=expr[m.end():].replace('⁡','').replace(r'\left','').replace(r'\right','').strip();assert tail[0]=='('
 depth=1;i=1
 while depth:depth+=(tail[i]=='(')-(tail[i]==')');i+=1
 inner=parse(tail[1:i-1]);assert sp.diff(inner,X,2)==0
 freq=sp.diff(inner,X);assert freq!=0
 prefix=expr.split('=',1)[1][:m.start()-len(expr.split('=',1)[0])-1].strip() # independently extract amplitude
 amp=parse(prefix) if prefix else sp.Integer(1);assert amp!=0
 unit='degree' if '∘' in expr else 'rad';base=360 if unit=='degree' else 2*sp.pi
 return freq,base/sp.Abs(freq),unit,trig,inner

def verify(r):
 q=r['question'];gen=r['generation'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 freq,period,unit,trig,inner=prompt_math(q)
 assert str(freq)==gen['frequency'];assert unit==gen['unit']
 sol=q.get(':question/worked-solution');stages=0
 if sol:
  balanced(sol)
  for s in re.findall(r'\$(.*?)\$',sol,re.S):
   if 'A' in s or 'Bx+C' in s:continue
   if '=' in s:
    exprs=[parse(part).subs(B,freq) for part in s.split('=')]
    for a,b in zip(exprs,exprs[1:]):assert sp.simplify(a-b)==0,('false displayed stage',s,a,b)
    stages+=1
  # Validate prose rule independently, including the documented raw source error.
  first=sol.split('\n\n')[0];rule=re.findall(r'\$(.*?)\$',first)[-1]
  displayed_rule=parse(rule).subs(B,freq)
  if gen['evidence_only'] and gen['source_ids']==['q-43411']:assert displayed_rule==360 and period==360/freq
  else:assert sp.simplify(displayed_rule-period)==0,('false opening rule',rule,period)
  final_math=re.findall(r'\$(.*?)\$',sol,re.S)[-1]
  assert sp.simplify(parse(final_math.split('=')[-1])-period)==0,'stale period conclusion'
 fs=q.get(':question/answer-fields',[])
 for f in fs:
  choices=f[':answer-field/choices'];vals=[parse(a[':answer/value']) for a in choices]
  assert len(choices)==5 and len(set(vals))==5,'complete or equivalent choice failure'
  matches=[i for i,v in enumerate(vals) if sp.simplify(v-period)==0];assert len(matches)==1
  for a in choices:balanced(a[':answer/value']);assert not '$' in a[':answer/value'];assert a[':answer/type']==':answer.type/math'
  if ':answer-field/correct' in f:assert choices[matches[0]][':answer/id']==f[':answer-field/correct'][1]
  if not gen['evidence_only']:
   base=360 if unit=='degree' else 2*sp.pi
   ops=[period,base*abs(freq),base/(2*abs(freq)),2*base/abs(freq),base]
   assert set(vals)==set(ops),'wrong displayed method bank'
 return stages

sources=g.CAPTURE['record'][':knowledge-point/questions'];cases=json.loads((H/'source-cases.json').read_text());reviews=[];replays=[];fidelity=[];checks=[];stages=0;bank_count=choice_count=solution_count=designation_count=0
for q,c in zip(sources,cases):
 r=g.generate('easy',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);out=r['question'];stages+=verify(r)
 assert set(q)==set(out),('raw question attribute presence',c['source_id'])
 assert q[':question/problem']==out[':question/problem'];assert q.get(':question/worked-solution')==out.get(':question/worked-solution')
 if ':question/worked-solution' in q:solution_count+=1
 for f,of in zip(q.get(':question/answer-fields',[]),out.get(':question/answer-fields',[])):
  assert set(f)==set(of);assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  for a in f[':answer-field/choices']:
   oa=next(z for z in of[':answer-field/choices'] if z[':answer/value']==a[':answer/value']);assert set(a)==set(oa)
  bank_count+=1;choice_count+=len(f[':answer-field/choices'])
  if ':answer-field/correct' in f:
   original=f[':answer-field/correct'][':answer/value'];actual=next(a[':answer/value'] for a in of[':answer-field/choices'] if a[':answer/id']==of[':answer-field/correct'][1]);assert original==actual;designation_count+=1
 replays.append(r);fidelity.append({'source_id':c['source_id'],'prompt_exact':True,'solution_exact_if_present':True,'attribute_presence':True,'bank_options':len(q.get(':question/answer-fields',[{':answer-field/choices':[]}])[0][':answer-field/choices'])})
 reviews.append('## Original '+c['source_id']+' — raw evidence, ineligible\n\n'+g.markdown(r))
 # Every observed template/bank receives two changed-parameter learner variants.
 for seed in (81,91):
  v=g.generate('easy',seed,template=c['template']);stages+=verify(v);reviews.append('### Generated easy variant — authored method bank\n\n'+g.markdown(v));checks.append(v)
for level in ('moderate','hard'):
 for seed in (12,19,29,51):
  v=g.generate(level,seed);stages+=verify(v);reviews.append('## Generated '+level+' — authored scope\n\n'+g.markdown(v));checks.append(v)
# Changed raw parameters exercise the public masked recipes rather than copied payloads.
raw_changed=0
for c in cases:
 p=dict(c['parameters']);factor=3 if c['source_id'] in ('q-117578','q-81513') else 2
 b=sp.Rational(p['b_n'],p['b_d'])/factor;p.update(b_n=int(b.p),b_d=int(b.q))
 for i in range(len(g.SPECS[c['template']]['banks'])):
  v=sp.Rational(p[f'o{i}_n'],p[f'o{i}_d'])*factor;p.update({f'o{i}_n':int(v.p),f'o{i}_d':int(v.q)})
 r=g.generate('easy',template=c['template'],parameters=p,profile=c['bank_profile']);stages+=verify(r);raw_changed+=1
 assert r['question'][':question/problem']!=replays[raw_changed-1]['question'][':question/problem']

# Exhaust every reduced meaningful frequency, each unit, and each source-shaped family.
counts={};tasks={l:set() for l in g.LEVELS};sampled=[];coverage=set()
for level in g.LEVELS:
 n=0
 for seed in range(300):
  r=g.generate(level,seed);stages+=verify(r);tasks[level].add(r['generation']['parameter_fingerprint']);sampled.append(r);n+=1
  if level=='easy':coverage.add(r['generation']['template'])
 for name in [n for n,l in g.TEMPLATES.items() if l==level]:
  domain=g.allowed_frequencies(g.SPECS[name]['bstyle']) if level=='easy' else [(-n,d) for n,d in g.RATIONAL_DOMAIN] if level=='moderate' else g.HARD_DOMAIN
  for pair in domain:
   for unit in (['rad','degree'] if level!='easy' else [g.SPECS[name]['unit']]):
    p=g.sample(level,name,__import__('random').Random(0),False);p.update(b_n=pair[0],b_d=pair[1])
    if level!='easy':p['unit']=unit;p.update(c_n=1,c_d=3 if unit=='rad' else 1)
    if level=='hard':p['k']=pair[2]
    try:r=g.generate(level,template=name,parameters=p)
    except g.SampleRejected:continue
    stages+=verify(r);n+=1;tasks[level].add(r['generation']['parameter_fingerprint'])
 counts[level]=n
assert coverage==set(g.SPECS),'defaults must cover every supported source family'
# Task identity excludes amplitude/shift/trig; content identity includes actual bank.
r=g.generate('moderate',22);p=r['generation']['parameters'];a=g.generate('moderate',1,parameters=p);b=g.generate('moderate',8,parameters=p);assert a['question'][':question/id']==b['question'][':question/id'];assert sorted(z[':answer/id'] for z in a['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(z[':answer/id'] for z in b['question'][':question/answer-fields'][0][':answer-field/choices'])
p2={**p,'a_n':-p['a_n'],'trig':'cos' if p['trig']=='sin' else 'sin'};v=g.generate('moderate',parameters=p2);assert a['generation']['parameter_fingerprint']==v['generation']['parameter_fingerprint'];assert a['question'][':question/id']!=v['question'][':question/id']
# Explicit guards: signed easy, unsigned/integer moderate, absent hard cancellation,
# degenerate bank frequencies, unreduced/zero and amplitude/frequency bounds.
bad=[]
for level in g.LEVELS:
 r=g.generate(level,24);p=r['generation']['parameters'];name=r['generation']['template']
 for update in [{'b_n':0},{'a_n':0},{'b_n':99},{'b_d':0}]+([{'b_n':-abs(p['b_n'])}] if level=='easy' else [{'b_n':abs(p['b_n'])}]):bad.append((level,name,{**p,**update}))
p=g.sample('hard','factored_frequency',__import__('random').Random(2),False);bad.append(('hard','factored_frequency',{**p,'k':1}))
for l,n,p in bad:
 try:g.generate(l,template=n,parameters=p)
 except ValueError:pass
 else:raise AssertionError('Guard accepted invalid explicit input')
p=dict(g.SPECS['rad_cos_fraction']['source_parameters']);p={k:v for k,v in p.items() if not k.startswith('o')};p.update(b_n=1,b_d=2)
try:g.generate('easy',template='rad_cos_fraction',parameters=p)
except g.SampleRejected:pass
else:raise AssertionError('Whole-bank collision not rejected')
# Read-back negative mutation controls catch stale B, period and operation choices.
mutations=0
for r in checks:
 for which in ('prompt','solution','choice'):
  z=copy.deepcopy(r)
  if which=='prompt':z['question'][':question/problem']=z['question'][':question/problem'].replace('x','x+x',1)
  elif which=='solution':z['question'][':question/worked-solution']=z['question'][':question/worked-solution'].replace('B=','B=1+',1)
  else:z['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='99999'
  try:verify(z)
  except (AssertionError,ValueError,SyntaxError,TypeError):mutations+=1
  else:raise AssertionError(('Displayed mutation evaded read-back check',which,r['generation']['template']))
# Real engine UUID choice checks, all bank members for every source with a key
# and completed normal records. Missing raw fields/keys remain explicitly ungraded.
fixtures=[]
for r in checks+sampled[:30]+[r for r in replays if r['question'].get(':question/answer-fields') and ':answer-field/correct' in r['question'][':question/answer-fields'][0]]:
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 fixtures.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned radio selection; math independently verified'} for a in f[':answer-field/choices']]})
save('engine-input.json',fixtures);subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True);native=json.loads((H/'engine-report.json').read_text())
save('review.json',checks);save('raw-replays.json',replays);(H/'review.md').write_text('# Period generator review\n\nRaw originals preserve all omissions. Variants use authored method banks.\n\n'+'\n\n---\n\n'.join(reviews)+'\n')
save('validation.json',{'status':'pass','database':'math','basis':1356,'source_questions':8,'source_fidelity':{'prompts_exact':8,'present_solutions_exact':solution_count,'solutions_present':7,'complete_banks_exact':bank_count,'banks_present':6,'options_exact':choice_count,'options_present':30,'correct_designations_exact':designation_count,'correct_designations_present':5,'missing_correct_designations':1,'fieldless_sources':2,'unrated_sources':1,'attribute_presence_exact':8},'source_repairs_normal_only':{'q-43411':'opening 360° changed to 360°/B','q-53457':'authored easy routing, derived correct 6π, solution added','q-117580/q-117583':'authored supported radio fields added'},'raw_changed_parameter_replays':raw_changed,'documented_raw_mathematical_source_errors':1,'opaque_banks':6,'opaque_eligible_for_learning':False,'displayed_math_checks':stages,'generated_records_checked':counts,'meaningful_task_counts':{l:len(v) for l,v in tasks.items()},'default_easy_family_coverage':sorted(coverage),'explicit_guard_rejections':len(bad),'whole_bank_collision_rejections':1,'mutation_rejections':mutations,'native_grading':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},'raw_ungradable_sources':['q-53457','q-117580','q-117583'],'limits':['Scalar historical banks are opaque independent displayed components, not recovered error recipes.','No source moderate/hard labels exist; negative-rational and factored-frequency levels are authored design claims.','Fieldless/raw missing correct refs cannot enter native fixture grading until authored completion.','q-43411 raw teaching-rule error is deliberately preserved, reported separately and ineligible.','No blank layouts or plots occur in this KP.'],'hashes':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [H.with_suffix('.py'),H/'source.json',H/'topic.json',H/'lesson.json',H/'template-masks.json',REPO/'generate/runs/current/check-engine']}})
print('Passed:',counts,'meaningful tasks',{l:len(v) for l,v in tasks.items()},'native',native['accepted_checks'],native['rejected_checks'])
