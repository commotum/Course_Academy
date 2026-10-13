#!/usr/bin/env python3
"""Fail-closed independent display readback and native radio-grade validation."""
import importlib.util,json,re,subprocess,sys,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('readback',D/'display_parser.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
V=(p.x,p.y,p.z);B=(p.i,p.j,p.k)
counts={'display_records':0,'display_choices':0,'formal_partial_inputs':0,'checked_scalar_rows':0,'checked_vector_rows':0,'raw_source_label_errors':0,'source_banks':0,'source_values':0,'source_prompts_exact':0,'source_solutions_exact':0,'source_correct_designations':0,'source_presence':0}
def scalar(t):return p.scalar(re.sub(r'\\text\{[^}]*\}','',t).replace(r'\mathbf','').replace('⁡',''))
def vector(t):
 v=s.expand(scalar(t));out=tuple(v.coeff(b) for b in B);assert s.simplify(v-sum(d*b for d,b in zip(out,B)))==0,t;return out

def eq(a,b):
 d=s.sympify(a)-s.sympify(b)
 if d==0:return True
 value=d.subs({p.x:7,p.y:8,p.z:9})
 if value.is_zero is False:return False
 return s.simplify(d)==0

def point(prompt):
 m=re.search(r'at the point \$\((.*?)\)\$',prompt)
 return tuple(scalar(v) for v in m[1].split(',')) if m else None

def expression(prompt):
 m=re.search(r'[fgh]\(x,y,z\)\s*=([^$]+)',prompt);assert m,prompt
 return scalar(m[1].strip().rstrip('.,'))

def derivative_rhs(rhs,F):
 m=re.match(r'\s*\\frac\{∂\}\{∂([xyz])\}\(',rhs)
 if not m:return None
 text=rhs[m.end():].strip();assert text.endswith(')');inside=text[:-1];actual=scalar(inside);assert eq(actual,F),(inside,F)
 counts['formal_partial_inputs']+=1;return m[1],s.diff(actual,dict(zip('xyz',V))[m[1]])

def component_replace(rhs,G):
 for v,deriv in zip('xyz',G):
  rhs=re.sub(r'\{[fgh]\}_\{'+v+r'\}\(x,y,z\)',lambda m:'('+s.latex(deriv).replace(r'\log',r'\ln')+')',rhs)
 return rhs

def formatting(t):
 assert t.count('$$')%2==0
 assert (t.replace('$$','').count('$')%2)==0
 assert t.count('{')==t.count('}'),t
 depth=0
 for ch in t:
  depth+=(ch=='{')-(ch=='}');assert depth>=0,t
 assert depth==0,t
 assert '\\\\frac' not in t
 assert not re.search(r'(?<!\\)[+]\s*[-]|[-]\s*[-]',t),t

fixtures=[]
def check(record,label):
 q=record['question'];meta=record['generation'];assert set(record['knowledge_point'])=={'db_id','id','title'};assert record['knowledge_point']['db_id']==17592186124444
 assert meta['eligible_for_learning']==(not meta['evidence_only'])
 for t in (q[':question/problem'],q[':question/worked-solution']):formatting(t)
 if meta['template'] in g.ORIGINALS:
  original=g.ORIGINALS[meta['template']][':question/worked-solution'];generated=q[':question/worked-solution']
  def shape(t):
   blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',t,re.S)
   return [(len(b.split(r'\\')),b.count(r'\frac{∂}{∂'),b.count(r'\cdot')) for b in blocks]
  assert shape(generated)==shape(original),(label,'missing ordered operation stage')
  if meta['template'] not in g.POINTS:
   # Held-coordinate zero contributions and family-specific operation masks
   # remain even where a CAS would collapse them algebraically.
   for fragment in ('+0','0+',r'\frac{1}{\sqrt',r'\frac{yz}{xyz}',r'\frac{xz}{xyz}',r'\frac{xy}{xyz}'):
    if fragment in original and not any(meta['parameters']['shifts']):assert fragment in generated
  # An algebraically equal dropped reduction row must fail the shape validator.
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',generated,re.S)
  first=blocks[0];rows=first.split(r'\\')
  mutated=generated.replace(first,r'\\'.join(rows[:1]+rows[2:]),1)
  assert shape(mutated)!=shape(original)
 F=expression(q[':question/problem']);G=tuple(s.diff(F,v) for v in V);pt=point(q[':question/problem']);E=tuple(d.subs(dict(zip(V,pt))) for d in G) if pt else G
 for f in q[':question/answer-fields']:
  assert f[':answer-field/type']==':answer-field.type/radio';assert len(f[':answer-field/choices'])==5
  vals=[vector(a[':answer/value']) for a in f[':answer-field/choices']]
  for i,val in enumerate(vals):
   assert not any(t.has(s.zoo,s.nan,s.oo) for t in val)
   assert not any(all(eq(a,b) for a,b in zip(val,other)) for other in vals[:i]),label
  good=[i for i,val in enumerate(vals) if all(eq(a,b) for a,b in zip(val,E))];assert len(good)==1,(label,F,E,vals)
  assert f[':answer-field/correct']==[':answer/id',f[':answer-field/choices'][good[0]][':answer/id']]
  assert len(set(a[':answer/id'] for a in f[':answer-field/choices']))==5
  for a in f[':answer-field/choices']:formatting(a[':answer/value'])
  counts['display_choices']+=len(vals)
  fixtures.append({'label':label,'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==good[0] else 'rejected','purpose':'Owned choice ID; displayed vector mathematics checked independently'} for i,a in enumerate(f[':answer-field/choices'])]})
 for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S):
  rows=block.split(r'\\');derivative=None;evaluated=False;vectorblock=False
  for ix,row in enumerate(rows):
   lhs,rhs=row.strip().split('& =',1);rhs=rhs.strip().rstrip('.')
   d=derivative_rhs(rhs,F)
   if d is not None:
    var,derivative=d;lm=re.search(r'\{[fgh]\}_\{([xyz])\}',lhs);assert lm and lm[1]==var;continue
   if derivative is not None:
    assert eq(scalar(rhs),derivative),(label,lhs,rhs,scalar(rhs),derivative);counts['checked_scalar_rows']+=1
   else:
    vectorblock=True
    if '∇' in lhs and '(x,y,z)' not in lhs:
     m=re.search(r'∇[fgh]\((.*?)\)',lhs);assert m;lp=tuple(scalar(v) for v in m[1].split(','));assert lp==pt;(evaluated:=True)
    val=vector(component_replace(rhs,G));expected=E if evaluated else G
    if not all(eq(a,b) for a,b in zip(val,expected)):
     if meta['evidence_only'] and ix==0 and meta['template'] in ('log_point','expcos_point','sine_point'):
      assert len(re.findall(r'\{[fh]\}_\{x\}',rhs))==3;counts['raw_source_label_errors']+=1
     else:raise AssertionError((label,lhs,rhs,val,expected))
    else:counts['checked_vector_rows']+=1
 counts['display_records']+=1

old={q[':question/id']:q for q in g.KP[':knowledge-point/questions']}
review=[]
for case in json.loads((D/'source-cases.json').read_text()):
 r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check(r,'original-'+case['source_id']);o=old[case['source_id']];q=r['question']
 assert q[':question/problem']==o[':question/problem'];counts['source_prompts_exact']+=1
 assert q[':question/worked-solution']==o[':question/worked-solution'];counts['source_solutions_exact']+=1
 for attr in (':question/difficulty',':question/answer-fields',':question/worked-solution'):assert (attr in q)==(attr in o)
 counts['source_presence']+=1
 for a,b in zip(q[':question/answer-fields'],o[':question/answer-fields']):
  assert a[':answer-field/key']==b[':answer-field/key'];assert a[':answer-field/type']==b[':answer-field/type'][':db/ident']
  assert sorted(v[':answer/value'] for v in a[':answer-field/choices'])==sorted(v[':answer/value'] for v in b[':answer-field/choices']);counts['source_banks']+=1;counts['source_values']+=len(a[':answer-field/choices'])
  assert next(v[':answer/value'] for v in a[':answer-field/choices'] if v[':answer/id']==a[':answer-field/correct'][1])==b[':answer-field/correct'][':answer/value'];counts['source_correct_designations']+=1
 review.append({'label':'Original replay: '+case['template'],'record':r})
for level,templates in g.TEMPLATES.items():
 for template in templates:
  print('Checking '+level+'/'+template,flush=True)
  for seed in range(2):
   r=g.generate(level,seed+71,template=template);check(r,'generated-'+template+'-'+str(seed))
   replay=g.generate(level,seed+919,template=template,profile=r['generation']['bank_profile'],parameters=r['generation']['parameters']);assert replay['question'][':question/id']==r['question'][':question/id'];assert sorted(a[':answer/value'] for a in replay['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])
   if seed<2:review.append({'label':'Generated '+level+': '+template,'record':r})
  if level=='moderate' and template not in g.POINTS:
   for shifts in ((3,-3,2),(-3,2,-1)):
    check(g.generate(level,template=template,parameters={'shifts':shifts}),'boundary-'+template+str(shifts))
   raw=g.generate(level,template=template,profile='observed_raw',parameters={'shifts':(2,-1,3)});check(raw,'raw-changed-'+template);review.append({'label':'Generated historical bank evidence only: '+template,'record':raw})
  elif level=='moderate':
   changed={'log_point':[4,2,3],'sine_point':[2,-1,'pi/2'],'expcos_point':['1/3',2,'pi/2']}[template]
   raw=g.generate(level,template=template,profile='observed_raw',parameters={'point':changed});check(raw,'raw-changed-'+template);review.append({'label':'Generated historical bank evidence only: '+template,'record':raw})
for level in g.TEMPLATES:
 seen=set()
 for i in range(100):
  seen.add(g.generate(level,i)['generation']['template'])
  if seen==set(g.TEMPLATES[level]):break
 assert seen==set(g.TEMPLATES[level]),(level,seen)
for level,kwargs in [('easy',{'coefficients':[0,2,3]}),('easy',{'powers':[1,2,3]}),('hard',{'coefficients':[4,1,1]}),('hard',{'point':[0,2,1]}),('moderate',{'shifts':[4,0,0]})]:
 try:g.generate(level,template=g.TEMPLATES[level][0],parameters=kwargs)
 except ValueError:pass
 else:raise AssertionError('Invalid explicit workload admitted')
(D/'native-input.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
subprocess.run([sys.executable,str(D/'bank-operations.py')],check=True)
subprocess.run([sys.executable,str(D/'operation-structure.py')],check=True)
engine=D.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
(D/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
md=['# Original and generated review','Each original is a public parameterized raw replay; source errors remain visibly documented. Generated examples use eligible method banks.']
for item in review:md.extend(['## '+item['label'],g.markdown(item['record'])])
(D/'review.md').write_text('\n\n'.join(md)+'\n')
report={'status':'pass','counts':counts,'operation_structure':json.loads((D/'operation-structure-report.json').read_text()),'authored_bank_operations':json.loads((D/'bank-operation-report.json').read_text()),'native':json.loads((D/'native-report.json').read_text()),'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'scope':'All 10 observed moderate families; authored easy polynomial and hard quotient evaluation','limitations':['Three original formal-gradient component labels are mathematically wrong and remain in raw replay; repaired in normal practice.','Five raw/partly opaque banks reproduce parameterized expression patterns without claiming recovered distractor intent, and are evidence only.','Native radio ID tests validate selection; all displayed choices/solution math checked separately.'],'variety':json.loads((D/'variety.json').read_text()),'environment':json.loads((D/'environment.json').read_text()),'review_records':len(review),'plots':'none','database_writes':0,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()}
(D/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':'pass','counts':counts}))
