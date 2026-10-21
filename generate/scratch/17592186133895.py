#!/usr/bin/env python3
"""Unit scalar curl recognition, frozen math basis 1356. Steps 3–7 only.

Seven observed families; easy/moderate defaults select every source family.
Raw profiles preserve source field omissions and redundant legacy fields. Their
absence of a reference is evidence, never an inferred successful designation.
Public source replay renders parameterized prompt/partial/curl slots, never
returns a literal question payload. Fixed prose and mathematical stages are
retained. Normal presentation adds a distributed subtraction before collection.
Hard is authored: mixed polynomial/exponential held-coordinate derivatives,
three fields, same unit-curl recognition, no integration or area calculation.
All components are C-infinity on R^2, including held-coordinate components.

API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None); wrappers per level below. Explicit invalid inputs raise ValueError.
"""
from pathlib import Path
import argparse, copy, hashlib, itertools, json, random, re, sys, uuid
import sympy as s
HERE=Path(__file__).with_suffix('')
WRAPPER=json.loads((HERE/'source.json').read_text()); KP=WRAPPER['record']
QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
KP_ID=17592186133895; VERSION='unit-curl-1'
x,y=s.symbols('x y',real=True)
LEVELS={'q-125852':'easy','q-126560':'easy','q-125853':'moderate','q-126571':'moderate','q-126577':'moderate','q-126574':'moderate','q-126575':'moderate','mixed':'hard'}
ANCHORS={'q-125852':{'a':1,'n':2},'q-126560':{'a':1,'d':2},'q-125853':{'a':1,'n':2,'d':4},'q-126571':{'a':1,'d':5},'q-126577':{'a':1,'d':7},'q-126574':{'a':1,'d':3},'q-126575':{'a':1,'n':3,'d':2}}
LABELS=['I','II','III']
def tex(v): return s.latex(s.sympify(v),mul_symbol=None).replace(r'\log',r'\ln')
def fields(t,p):
 a=s.Integer(p['a']);n=p.get('n',2);d=s.Integer(p.get('d',2))
 if t=='q-125852': return [(a*y,-a*x),(x/2+s.cos(y**n),y/2),(0,x)]
 if t=='q-126560': return [(s.exp(x+y)-y/d,s.exp(x+y)+(d-1)*x/d),(a*s.sin(y),s.cos(x)),(x,x)]
 if t=='q-125853': return [(-y,a*x**n+x),(-y/d+x,(d-1)*x/d),(-y,0)]
 if t=='q-126571': return [(0,x),(a*s.exp(y),y),(-y/d+s.atan(x),(d-1)*x/d)]
 if t=='q-126577': return [(a*y,y),(y/d,(d-1)*x/d),(s.exp(x)-s.exp(-y),x*s.exp(-y)+x)]
 if t=='q-126574': return [(a*y*s.exp(x),x-a*s.exp(x)),((a+1)*y,x),(-y/d+s.cos(x**2),(d-1)*x/d+1)]
 if t=='q-126575': return [(a*y**n,x**n+1),(y/d+s.sqrt(2)*x,(d+1)*x/d),(x,x)]
 # Hard has two substantive held-coordinate contributions in each partial.
 b=s.Integer(p['b']);k=s.Integer(p['k'])
 h=a*x*y**n
 e=s.exp(k*x+b*y)
 hard=[(s.diff(h,x)-y/d,s.diff(h,y)+(d-1)*x/d),
         (k*e+y/d,b*e+(d+1)*x/d),
         (a*y*s.exp(k*x),x-a*s.exp(k*x))]
 return [hard[i] for i in list(itertools.permutations(range(3)))[p['order']]]
def validate_parameters(t,p):
 keys=set(ANCHORS.get(t,{'a':1,'d':2,'n':2,'b':1,'k':1,'order':0}))
 if set(p)!=keys: raise ValueError('Exact parameter keys required: '+str(sorted(keys)))
 if any(type(v) is not int for v in p.values()):raise ValueError('Integer parameters required')
 if not 1<=p['a']<=5:raise ValueError('a must be 1..5')
 if 'n' in p and not 2<=p['n']<=4:raise ValueError('n must be 2..4')
 if 'd' in p and not 2<=p['d']<=8:raise ValueError('d must be 2..8')
 if t=='mixed' and not 0<=p['order']<=5:raise ValueError('order must be 0..5')
 if t=='mixed' and (not 1<=p['b']<=3 or not 1<=p['k']<=3):raise ValueError('b,k must be 1..3')
def selection(indices):
 ls=[LABELS[i] for i in indices]
 return 'I, II, and III' if len(ls)==3 else (' and '.join(ls)+' only' if ls else 'None')
def derivatives(fs):
 return [(s.diff(s.sympify(P),y),s.diff(s.sympify(Q),x)) for P,Q in fs]
def truths(ds):return tuple(i for i,(py,qx) in enumerate(ds) if s.simplify(qx-py-1)==0)
def mask_source(t):
 """Extract only complete expression slots. Fixed strings remain source evidence."""
 q=QUESTIONS[t];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 if t in ('q-125852','q-126560'):
  originals=re.findall(r'\$[PQ]\(x,y\)=(.*?)\$',prompt)
 else:
  pairs=re.findall('⟨(.*?),'+re.escape(r'\,')+'(.*?)⟩',prompt)
  originals=[v for pair in pairs for v in pair]
 assert len(originals)==6,(t,originals)
 # Replace sequential occurrences within the candidate part, protecting prose.
 cut=prompt.index('\n\n- ' ) if '\n\n- ' in prompt else prompt.index('\n\nI. ')
 head=prompt[:cut];tail=prompt[cut:]
 for i,value in enumerate(originals):
  marker='={'+str(i)+'}' # apply complete RHS including its '=' / vector boundary
  # locate in sequence, avoiding repeated occurrences of 0,x.
  if t in ('q-125852','q-126560'):
   name='P' if i%2==0 else 'Q';needle=name+'(x,y)='+value+'$';tail=tail.replace(needle,name+'(x,y)={{f'+str(i)+'}}$',1)
  elif i%2==0:
   j=i//2;whole='⟨'+originals[i]+','+r'\,'+originals[i+1]+'⟩';tail=tail.replace(whole,'⟨{{f'+str(i)+'}},'+r'\,'+'{{f'+str(i+1)+'}}⟩',1)
 prompt=head+tail
 orig_py=re.findall(re.escape(r'\frac{∂P}{∂y}=')+r'(.*?)\$',sol)
 orig_qx=re.findall(re.escape(r'\frac{∂Q}{∂x}=')+r'(.*?)\$',sol)
 orig_curl=re.findall(re.escape(r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}=')+r'(.*?)\n',sol)[1:]
 assert len(orig_py)==len(orig_qx)==len(orig_curl)==3
 for i in range(3):
  for prefix,values,tag in [(r'\frac{∂P}{∂y}=',orig_py,'py'),(r'\frac{∂Q}{∂x}=',orig_qx,'qx')]:
   v=values[i];punct=',' if v.endswith(',') else '';v=v.removesuffix(',')
   sol=sol.replace(prefix+v+punct+'$',prefix+'{{'+tag+str(i)+'}}'+punct+'$',1)
  sol=sol.replace(r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}='+orig_curl[i]+'\n',r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}={{c'+str(i)+'}}\n',1)
 return prompt,sol,originals,[v.removesuffix(',') for v in orig_py],[v.removesuffix(',') for v in orig_qx],orig_curl
MASKS={t:mask_source(t) for t in QUESTIONS}
def render_source(t,p,normal):
 prompt,sol,orig,opy,oqx,oc=MASKS[t];fs=fields(t,p);ds=derivatives(fs);anch=fields(t,ANCHORS[t]);ads=derivatives(anch)
 values={}
 for i,v in enumerate([v for pair in fs for v in pair]):values['f'+str(i)]=orig[i] if s.sympify(v)==s.sympify([v for pair in anch for v in pair][i]) else tex(v)
 for i,(py,qx) in enumerate(ds):
  values['py'+str(i)]=opy[i] if py==ads[i][0] else tex(py)
  values['qx'+str(i)]=oqx[i] if qx==ads[i][1] else tex(qx)
  c=s.simplify(qx-py);valid=s.simplify(c-1)==0
  collected=tex(c)+(r'\ne 1.' if not valid else '.')
  values['c'+str(i)]=oc[i] if c==s.simplify(ads[i][1]-ads[i][0]) else collected
  if normal:values['c'+str(i)]=r'\left('+values['qx'+str(i)]+r'\right)-\left('+values['py'+str(i)]+r'\right)='+distributed(py,qx)+'='+collected
 for key,v in values.items():prompt=prompt.replace('{{'+key+'}}',v);sol=sol.replace('{{'+key+'}}',v)
 return prompt,sol

def render_hard(p):
 fs=fields('mixed',p);ds=derivatives(fs)
 q=QUESTIONS['q-126575'];prompt=q[':question/problem'].split('\n\nI.')[0]
 prompt+='\n\n'+'\n\n'.join(LABELS[i]+'. $F(x,y)=⟨'+tex(P)+','+r'\,'+tex(Q)+'⟩$' for i,(P,Q) in enumerate(fs))
 sol=q[':question/worked-solution'].split('- Vector field I')[0]
 for i,(py,qx) in enumerate(ds):
  good=i in truths(ds)
  sol+='- Vector field '+LABELS[i]+(' gives' if good else ' does *not* give')+' the required area. '+('In this case,' if i==0 else 'Notice that')+'\n$'+r'\frac{∂P}{∂y}='+tex(py)+'$\nand\n$'+r'\frac{∂Q}{∂x}='+tex(qx)+',$\nwhich gives\n\n$$\n'+r'\frac{∂Q}{∂x}-\frac{∂P}{∂y}=\left('+tex(qx)+r'\right)-\left('+tex(py)+r'\right)='+distributed(py,qx)+'='+tex(s.expand(qx-py))+(r'\ne 1.' if not good else '.')+'\n$$\n\n'
 sol+='Therefore, the correct answer is "'+selection(truths(ds))+'."'
 return prompt,sol

def distributed(py,qx):
 # Retain every signed contribution separately; do not simplify before display.
 qterms=s.Add.make_args(qx);pterms=s.Add.make_args(py)
 return '+'.join(r'\left('+tex(v)+r'\right)' for v in qterms)+''.join(r'-\left('+tex(v)+r'\right)' for v in pterms)

def assessed_derivatives(ds):
 # Remove identical nonconstant additive terms before task counting. Held-only
 # components and canceling gradient decorations cannot inflate practice size.
 result=[]
 for py,qx in ds:
  pp=list(s.Add.make_args(s.expand(py)));qq=list(s.Add.make_args(s.expand(qx)))
  for term in list(pp):
   if term.has(x,y) and term in qq:pp.remove(term);qq.remove(term)
  result.append((s.srepr(s.Add(*pp)),s.srepr(s.Add(*qq))))
 return result

def ident(*parts):return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(parts,sort_keys=True,ensure_ascii=False)))
def normalize_fields(raw):
 result=[]
 for f in raw:
  f=copy.deepcopy(f);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  result.append(f)
 return result

def source_operations(t):
 """Whole eligible observed bank, represented as eligibility decision flips."""
 active=next(f for f in QUESTIONS[t][':question/answer-fields'] if ':answer-field/correct' in f)
 correct=set(truths(derivatives(fields(t,ANCHORS[t]))))
 operations=[]
 for answer in active[':answer-field/choices']:
  selected={i for i,label in enumerate(LABELS) if re.search(r'\b'+label+r'\b',answer[':answer/value'])}
  operations.append(tuple(sorted(correct^selected)))
 return tuple(operations)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio is supported')
 rng=random.Random(seed);eligible=[t for t,l in LEVELS.items() if l==level]
 t=template or rng.choice(eligible)
 if t not in eligible:raise ValueError('Template outside level scope')
 raw=profile=='raw'
 if profile not in (None,'raw','observed','method_toggle'):raise ValueError('Unknown complete bank profile')
 if raw and t=='mixed':raise ValueError('No hard source')
 # Whole bank is chosen before parameters. Source banks are fixed subset banks;
 # method_toggle is five complete response sets from actual candidate decisions.
 profile=profile or ('method_toggle' if t=='mixed' else 'observed')
 if t=='mixed' and profile=='observed':raise ValueError('No observed hard bank')
 bank_operations=source_operations(t) if profile=='observed' else ((),(0,),(1,),(2,),'complement') if profile=='method_toggle' else None
 base=ANCHORS.get(t,{'a':1,'d':2,'n':2,'b':1,'k':1,'order':0})
 p=dict(parameters) if parameters is not None else {k:rng.choice(list(range(6)) if k=='order' else list(range(2,9)) if k=='d' else list(range(2,5)) if k=='n' else list(range(1,4)) if k in ('b','k') else list(range(1,6))) for k in base}
 validate_parameters(t,p);fs=fields(t,p);ds=derivatives(fs);answer=selection(truths(ds))
 prompt,solution=render_hard(p) if t=='mixed' else render_source(t,p,not raw)
 q={':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level}
 if raw:
  q=copy.deepcopy(QUESTIONS[t]);q[':question/problem']=prompt;q[':question/worked-solution']=solution;q[':question/difficulty']=q[':question/difficulty'][':db/ident'];q[':question/answer-fields']=normalize_fields(q[':question/answer-fields'])
 elif profile=='observed':
  true=set(truths(ds));bank=[selection(sorted(true^set(delta))) for delta in bank_operations]
  q[':question/answer-fields']=[]
 else:
  true=set(truths(ds));sets=[set(range(3))-true if delta=='complement' else true^set(delta) for delta in bank_operations]
  bank=[selection(sorted(v)) for v in sets];q[':question/answer-fields']=[]
 if not raw:
  if len(bank)!=5 or len(set(bank))!=5 or bank.count(answer)!=1:raise ValueError('Reject whole bank: ambiguity or missing correct response')
  content=[VERSION,level,prompt,solution,sorted(bank)];qid=ident(content);fid=ident(qid,'selection')
  choices=[{':answer/id':ident(fid,v),':answer/type':':answer.type/text',':answer/value':v} for v in bank];rng.shuffle(choices)
  q[':question/id']=qid;q[':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',ident(fid,answer)]}]
 if raw and p!=ANCHORS[t]:
  qid=ident(VERSION,level,prompt,solution,[[a[':answer/value'] for a in f[':answer-field/choices']] for f in q[':question/answer-fields']]);q[':question/id']=qid
  for index,f in enumerate(q[':question/answer-fields']):
   fid=ident(qid,index);f[':answer-field/id']=fid
   old_correct=f.get(':answer-field/correct',[None,None])[1]
   for a in f[':answer-field/choices']:
    old=a[':answer/id'];a[':answer/id']=ident(fid,a[':answer/value'])
    if old==old_correct:f[':answer-field/correct']=[':answer/id',a[':answer/id']]
 # Mathematical task excludes held-only components and common matching terms.
 # Keep derivative constants and unequal nonconstant contributions; canceling
 # shared decorations and held-coordinate additions are incidental.
 task=[level,sorted(assessed_derivatives(ds))]
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':t,'profile':profile,'seed':seed,'parameters':p,'domain':'R^2; every displayed P,Q is C-infinity','source':{k:WRAPPER[k] for k in ('database','basis','lineage')},'source_ids':[t] if t!='mixed' else [],'evidence_only':raw,'eligible_for_learning':not raw,'bank_operations':bank_operations,'authored':t=='mixed','mathematical_fingerprint':hashlib.sha256(json.dumps(task).encode()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':s.__version__}}}
# Easy: two observed recognition families, familiar exponential/trig derivatives.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: five observed families, fractions, held components, and cancellations.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: authored same recognition; two mixed derivative contributions per pair.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];text=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):text+='\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'
 return text+q.get(':question/worked-solution','')

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
