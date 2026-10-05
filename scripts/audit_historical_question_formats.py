#!/usr/bin/env python3
"""Audit the committed history batch against exact-KP saved lesson examples.

Original captures and the original import are immutable evidence. Repairs use
locally authored options, never claim to recover missing historical MA options.
"""
import ast,cmath,collections,copy,hashlib,json,math,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'question_capture'))
from edn import loads
from prepare_historical_questions import clean_math, validate_ready, runtime_check
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'reference/mathacademy/history-question-import-2026-10-04'
OUT=BASE/'format-audit'
DATA=Path('/home/jake/Developer/MA/DATA/Lessons')

def save(name,value):
 (OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def index_sources(questions):
 topics={}
 for p in (BASE/'import-ready/database-import').glob('after-topics-*.edn'):
  if re.fullmatch(r'after-topics-\d+\.edn',p.name):
   for row in loads(p.read_text()):topics[row[0][':topic/math-academy-id']]=row[0]
 index={}
 for tid in sorted({q['topic_id'] for q in questions}):
  path=DATA/str(tid)/'Source'/f'{tid}.json'
  if not path.exists():continue
  lesson=json.loads(path.read_text()); groups={};current=None
  for item in lesson['lesson']['items']:
   if item['item_type']=='step' and item.get('step_type')=='example':
    current='e-'+str(item['content_id']);groups.setdefault(current,{'title':item['title'],'questions':[]})
   elif item['item_type']=='question' and current:groups[current]['questions'].append(item)
  for kp in topics[tid][':topic/knowledge-points']:
   kid=str(kp[':knowledge-point/id']);canon=kp.get(':knowledge-point/canonical-example',{}).get(':question/math-academy-id');match=groups.get(canon);method='canonical-example'
   if not match:
    names=[g for g in groups.values() if g['title'].strip().lower()==kp[':knowledge-point/title'].strip().lower()]
    if len(names)==1:match=names[0];method='exact-title'
   if match:index[kid]={'topic_id':tid,'title':kp[':knowledge-point/title'],'canonical_example':canon,'match_method':method,'source':str(path),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'format_counts':dict(collections.Counter(q['question_format'] for q in match['questions'])),'questions':match['questions']}
 return index

# Small, closed expression interpreter for rejecting ambiguous distractors.
# It is an authoring check, NOT the learner-facing symbolic grader. An option
# is admitted only with a concrete numerical witness that it differs from the
# saved canonical expression. Unhandled structures remain in the review queue.
class ParseError(ValueError):pass
class MathExpression:
 def __init__(self,tex,symbols=()):
  self.symbols=set(symbols)
  s=tex.strip().strip('$').replace('−','-')
  if re.search(r'[fgh]\}?\^\{?-1\}?\(',s):raise ParseError('Inverse function requires semantic review')
  s=s.replace('√',r'\sqrt')
  s=re.sub(r'\\(?:left|right|displaystyle|textstyle)\b','',s)
  s=re.sub(r'\\[,;! ]','',s).replace('\\cdot','*').replace('\\times','*')
  s=s.replace('\\dfrac','\\frac').replace('\\tfrac','\\frac')
  # TeX permits unbraced one-character fraction arguments.
  s=re.sub(r'\\frac\s*([0-9A-Za-z])\s*([0-9A-Za-z])',r'\\frac{\1}{\2}',s)
  s=re.sub(r'(?<![A-Za-z])\{(sin|cos|tan|sec|csc|cot|log|ln)\}',lambda m:'\\'+m[1],s)
  s=s.replace('\\theta','t').replace('\\alpha','a').replace('\\beta','b')
  s=re.sub(r'\\(?:text|textrm|mathrm)\{\s*i\s*\}','i',s)
  # Keep units in a signature; compare only options with identical dimensions.
  units=[]
  def unit(m):units.append((m[1].strip(),m[2] or ''));return '1'
  s=re.sub(r'\{?\\(?:text|textrm|mathrm)\{([^{}]+)\}\}?(\^\{?\d+\}?)?',unit,s)
  self.units=tuple(units)
  s=re.sub(r'(\{[+-]?\d+(?:\.\d+)?\}|\d+(?:\.\d+)?)\^\{?(?:∘|\\circ)\}?',lambda m:'('+m[1]+r'*\frac{\pi}{180})',s)
  s=s.replace('∘','').replace('\\circ','')
  s=re.sub(r'\{\|\}','|',s)
  s=re.sub(r'\|([^|]+)\|',lambda m:r'\operatorname{abs}{'+m[1]+'}',s)
  self.tokens=re.findall(r'\\[A-Za-z]+|\d+(?:\.\d+)?|[A-Za-z]|[^\s]',s);self.pos=0
  self.tree=self.expr()
  if self.pos!=len(self.tokens):raise ParseError('Unconsumed math')
  self.variables=set()
  def visit(n):
   if n[0]=='var':self.variables.add(n[1])
   for c in n[1:]:
    if isinstance(c,tuple):visit(c)
  visit(self.tree)
 def peek(self):return self.tokens[self.pos] if self.pos<len(self.tokens) else ''
 def take(self):t=self.peek();self.pos+=1;return t
 def group(self):
  t=self.peek()
  if t in ('{','('):
   self.take();x=self.expr();end='}' if t=='{' else ')'
   if self.take()!=end:raise ParseError('Unbalanced group')
   return x
  return self.atom()
 def atom(self):
  t=self.take()
  if re.fullmatch(r'\d+(?:\.\d+)?',t):return ('num',float(t))
  if t in ('{','('):
   self.pos-=1;return self.group()
  if t=='\\frac':return ('/',self.group(),self.group())
  if t=='\\sqrt':
   degree=('num',2.)
   if self.peek()=='[':
    self.take();degree=self.expr()
    if self.take()!=']':raise ParseError('Bad root')
   return ('^',self.group(),('/',('num',1.),degree))
  if t in ('\\pi','e','i') and t not in self.symbols:return ('num',{'\\pi':math.pi,'e':math.e,'i':1j}[t])
  funcs=('sin','cos','tan','sec','csc','cot','ln','log','arcsin','arccos','arctan','exp','abs')
  if t=='\\operatorname':
   if self.take()!='{':raise ParseError('Bad function')
   name=''
   while self.peek() and self.peek()!='}':name+=self.take()
   if self.take()!='}':raise ParseError('Bad function')
   t='\\'+name
  if t.startswith('\\') and t[1:] in funcs:
   name=t[1:];base=None;power=None
   if self.peek()=='_':self.take();base=self.group()
   if self.peek()=='^':self.take();power=self.group()
   arg=self.group() if self.peek() in ('(','{') else self.product(function_argument=True)
   result=('func',name,arg) if base is None else ('/',('func','ln',arg),('func','ln',base))
   return ('^',result,power) if power else result
  if re.fullmatch('[A-Za-z]',t):return ('var',t)
  raise ParseError('Unsupported atom '+t)
 def power(self):
  if self.peek() in ('+','-'):
   op=self.take();return ('*',('num',-1. if op=='-' else 1.),self.power())
  x=self.atom()
  if self.peek()=='^':self.take();x=('^',x,self.group())
  return x
 def product(self,function_argument=False):
  x=self.power()
  while self.peek() and self.peek() not in ('+','-',')','}',']',',','=','<','>'):
   if function_argument and self.peek() in ('\\operatorname','\\sin','\\cos','\\tan','\\sec','\\csc','\\cot','\\ln','\\log'):break
   if self.peek() in ('*','/'):
    op=self.take();x=(op,x,self.power())
   elif self.peek()=='_':raise ParseError('Unsupported subscript')
   else:x=('*',x,self.power())
  return x
 def expr(self):
  x=self.product()
  while self.peek() in ('+','-'):
   op=self.take();x=(op,x,self.product())
  return x
 def evaluate(self,values):
  def go(t):
   k=t[0]
   if k=='num':return t[1]
   if k=='var':return values[t[1]]
   if k=='func':
    v=go(t[2]);name=t[1]
    if name=='abs':return abs(v)
    if name=='ln':return cmath.log(v)
    if name=='log':return cmath.log10(v)
    if name in ('sec','csc','cot'):return 1/getattr(cmath,{'sec':'cos','csc':'sin','cot':'tan'}[name])(v)
    return getattr(cmath,{'arcsin':'asin','arccos':'acos','arctan':'atan'}.get(name,name))(v)
   a,b=go(t[1]),go(t[2])
   if k=='+':return a+b
   if k=='-':return a-b
   if k=='*':return a*b
   if k=='/':return a/b
   if k=='^':return a**b
   raise ParseError(k)
  z=complex(go(self.tree))
  if not math.isfinite(z.real) or not math.isfinite(z.imag):raise ParseError('Nonfinite')
  return z

def inequality_witness(a,b,arbitrary_constant=False):
 try:x,y=MathExpression(a),MathExpression(b)
 except (ParseError,ValueError,IndexError,RecursionError):return None
 if x.units!=y.units or x.variables!=y.variables:return None
 previous_difference=None
 for n in (0.23,0.71,1.37,2.19,3.83,-0.47,-1.63):
  env={v:n+(i*.173) for i,v in enumerate(sorted(x.variables))}
  if arbitrary_constant:
   for v in ('C','K'):
    if v in env:env[v]=1.17
  try:p,q=x.evaluate(env),y.evaluate(env)
  except (ValueError,ZeroDivisionError,OverflowError,ParseError):continue
  if abs(p-q)>1e-7*max(1,abs(p),abs(q)):
   if arbitrary_constant:
    difference=p-q
    if previous_difference is None:previous_difference=difference;continue
    if abs(difference-previous_difference)<1e-6*max(1,abs(difference)):continue
   return {'substitution':env,'canonical':[p.real,p.imag],'alternative':[q.real,q.imag]}
 return None

def choice_value(choice):
 if choice.get('images'):return None
 s=choice['readable_text'].strip()
 m=re.fullmatch(r'\[MATH:\s*(.*)\]',s,re.S)
 if m:return {'type':'math','value':m[1].strip()}
 if '[MATH:' not in s and '[IMG:' not in s:return {'type':'text','value':s}
 return None

def source_problem(q):
 # Prepared asset URLs are local; restore source wording without discarding assets.
 s=q['problem']
 # Only remove our appended response locations; never touch source controls.
 positions=[m.start() for m in re.finditer(r'\n\n[^\n]*\{\{',s)]
 if positions:s=s[:min(positions)]
 original=q['preparation']['source_problem']
 # Reapply only source wording changes to the prepared asset-preserving prompt.
 if '![](' not in original:s=original
 s=re.sub(r'(?m)^(I|II|III|IV|V|VI)\. - ',r'\1. ',s)
 return s.strip()

def assemble(q,source,options,checks,kind='local-radio'):
 new=copy.deepcopy(q);new['problem']=source_problem(q)
 key=q['answer_fields'][0]['key'] if len(q['answer_fields'])==1 else 'selection'
 new['answer_fields']=[{'key':key,'type':'radio','choices':options,'correct_value':options[0]['value'],'evidence':'Saved canonical answer; locally assembled choices using exact-KP lesson response format'}]
 new['preparation']['response_repair']={'kind':kind,'original_answer_origin':q['preparation']['answer_origin'],'source':source['source'],'match_method':source['match_method'],'source_question_ids':['q-'+x['question_id'] for x in source['questions']],'options_recovered_from_original_question':False,'distractors':checks}
 validate_ready(new)
 return new,None

def composite_radio(q,source):
 fields=q['answer_fields'];origin=q['preparation']['answer_origin']
 def render(values):
  if origin=='matrix-components':
   columns=max(int(f['key'][-1]) for f in fields)
   return {'type':'math','value':r'\begin{bmatrix}'+r' \\ '.join(' & '.join(values[i:i+columns]) for i in range(0,len(values),columns))+r'\end{bmatrix}'}
  if origin=='coordinate-components':return {'type':'math','value':'('+','.join(values)+')'}
  if origin=='ordered-real-roots':return {'type':'math','value':r'\{'+','.join(values)+r'\}'}
  return {'type':'text','value':'; '.join(f['key'].replace('-',' ')+' = '+('$'+v+'$' if f['choices'][0]['type']=='math' else v) for f,v in zip(fields,values))}
 values=[f['correct_value'] for f in fields];options=[render(values)];checks=[]
 # Change one identified component, preserving the meaning of every other one.
 for i,f in enumerate(fields):
  if f['choices'][0]['type']!='math':continue
  try:parsed=MathExpression(values[i])
  except (ParseError,ValueError,IndexError):continue
  for delta in (1,-1,2,-2,3):
   candidate=list(values);candidate[i]='('+values[i]+')'+('+' if delta>0 else '')+str(delta)
   witness=inequality_witness(values[i],candidate[i])
   if not witness:continue
   if origin=='ordered-real-roots':
    # Numeric roots are unordered; a changed root must not collide with another.
    try:
     if any(abs(MathExpression(v).evaluate({})-MathExpression(candidate[i]).evaluate({}))<1e-8 for j,v in enumerate(values) if j!=i):continue
    except (ParseError,KeyError,ValueError,ZeroDivisionError):return None,'symbolic-root-set-needs-review'
   if 'Unit Vector' in q['knowledge_point'] and not inequality_witness('-('+values[i]+')',candidate[i]):continue
   option=render(candidate)
   if any(option==o for o in options):continue
   options.append(option);checks.append({'value':option['value'],'origin':'Local error in component '+f['key'],'difference_witness':witness})
   if len(options)==5:return assemble(q,source,options,checks)
 return None,'multipart-needs-template-review'

def limit_radio(q,source):
 value=q['answer_fields'][0]['correct_value']
 canonical={'type':'math','value':value}
 if value not in (r'\infty',r'-\infty',r'\text{DNE}'):return None
 options=[canonical]+[{'type':'math','value':s} for s in (r'\infty',r'-\infty',r'\text{DNE}','0','1') if s!=value]
 return assemble(q,source,options,[{'value':o['value'],'origin':'Locally authored mutually distinct limit outcomes'} for o in options[1:]])

def categorical_radio(q,source):
 value=q['answer_fields'][0]['correct_value'];groups={
 'Undefined':['Undefined','0','1','-1'],
 'No maximum value':['No maximum value','0','1','-1'],
 'No minimum value':['No minimum value','0','1','-1'],
 'No real solutions':['No real solutions','0','1','2'],
 'No real roots':['No real roots','0','1','-1'],
 'No roots have the requested multiplicity':['No roots have the requested multiplicity','0','1','-1'],
 'No horizontal asymptotes':['No horizontal asymptotes',r'$y=0$',r'$y=1$',r'$y=-1$'],
 'No vertical asymptotes':['No vertical asymptotes',r'$x=0$',r'$x=1$',r'$x=-1$'],
 'All real numbers':['All real numbers',r'$(0,\infty)$',r'$(-\infty,0)$',r'$[0,\infty)$'],
 'Dollars per point':['Dollars per point','Points per dollar','Dollars times points','Dollars'],
 'Visitors per hour':['Visitors per hour','Hours per visitor','Visitors times hours','Visitors'],
 }
 if value not in groups:return None,'text-answer-needs-category-review'
 return assemble(q,source,[{'type':'text','value':v} for v in groups[value]],[{'value':v,'origin':'Locally authored distinct categorical alternatives; saved solution confirms canonical outcome'} for v in groups[value][1:]])

def interval_membership(value,point):
 s=re.sub(r'\\[,;! ]|\s','',value).replace('−','-')
 if r'\Rightarrow' in s:s=s.split(r'\Rightarrow')[-1]
 membership=re.search(r'\\in(?!fty)',s)
 if membership:s=s[membership.end():]
 if s==r'\mathbbR':return True
 if s==r'\emptyset':return False
 if r'\cup' in s:return any(interval_membership(part,point) for part in s.split(r'\cup'))
 if s[:1] in ('[','(') and s[-1:] in (']',')') and ',' in s:
  lo,hi=s[1:-1].split(',')
  def bound(x):
   if x==r'\infty':return math.inf
   if x==r'-\infty':return -math.inf
   return MathExpression(x).evaluate({}).real
  a,b=bound(lo),bound(hi)
  return (point>=a if s[0]=='[' else point>a) and (point<=b if s[-1]==']' else point<b)
 parts=re.split(r'(\\le|\\ge|\\ne|<|>)',s)
 if len(parts)<3:raise ParseError('Not an interval or inequality')
 def term(x):
  if re.fullmatch('[A-Za-z]',x):return point
  return MathExpression(x).evaluate({}).real
 for i in range(1,len(parts),2):
  a,b=term(parts[i-1]),term(parts[i+1]);op=parts[i]
  if not {'<':a<b,'>':a>b,r'\le':a<=b,r'\ge':a>=b,r'\ne':a!=b}[op]:return False
 return True

def structured_radio(q,source):
 value=q['answer_fields'][0]['correct_value']
 # Explicit finite sets: omission or addition gives a demonstrably different set.
 finite=re.fullmatch(r'\{([A-Za-z0-9,]+)\}',value)
 if finite and ',' in finite[1]:
  parts=finite[1].split(',')
  if len(parts)<2:return None
  canonical=r'\{'+','.join(parts)+r'\}'
  extra=next(x for x in ['0','1','2','z','99'] if x not in parts)
  variants=[parts[:-1],parts[1:],parts+[extra],parts[:-1]+[extra]]
  options=[{'type':'math','value':canonical}]+[{'type':'math','value':r'\{'+','.join(v)+r'\}'} for v in variants]
  checks=[{'value':o['value'],'origin':'Local insertion/omission; finite set membership differs from saved key'} for o in options[1:]]
  return assemble(q,source,options,checks)
 try:interval_membership(value,0.)
 except (ParseError,ValueError,IndexError,KeyError,ZeroDivisionError):return None
 candidates=[]
 for example in source['questions']:
  for c in example.get('choices',[]):
   v=choice_value(c)
   if v and v['type']=='math':candidates.append(v['value'])
 for n in ('-3','-1','0','1','3'):
  candidates.extend(['(-\\infty,'+n+')','['+n+',\\infty)','['+n+','+str(int(n)+2)+']'])
 candidates.extend([r'\emptyset',r'(-\infty,\infty)'])
 options=[{'type':'math','value':value}];checks=[]
 for candidate in candidates:
  witnesses=[]
  # Include endpoints themselves, so open/closed alternatives are checked.
  points=[float(n)/4 for n in range(-80,81)]+[float(n) for n in re.findall(r'(?<![A-Za-z])[-+]?\d+(?:\.\d+)?',value+candidate)]
  for previous in options:
   found=None
   for point in points:
    try:a,b=interval_membership(previous['value'],point),interval_membership(candidate,point)
    except (ParseError,ValueError,IndexError,KeyError,ZeroDivisionError):break
    if a!=b:found={'point':point,'canonical_membership':a,'alternative_membership':b};break
   if found is None:break
   witnesses.append(found)
  if len(witnesses)!=len(options):continue
  options.append({'type':'math','value':candidate});checks.append({'value':candidate,'origin':'Locally assembled interval alternative','membership_witnesses':witnesses})
  if len(options)==5:return assemble(q,source,options,checks)
 return None

def finite_sum(tex):
 s=tex.strip();s=re.sub(r'\{\s*\\sum\s*\}',r'\\sum',s)
 match=re.search(r'\\sum_\{([A-Za-z])=([^{}]+)\}\^\{([^{}]+)\}',s)
 if not match:raise ParseError('No finite sigma template')
 variable,lo,hi=match.groups();prefix=s[:match.start()].strip() or '1';term=s[match.end():].strip()
 if term.startswith('[') and term.endswith(']'):term=term[1:-1]
 if r'\infty' in hi:raise ParseError('Infinite sum')
 upper=MathExpression(hi);lower=MathExpression(lo);factor=MathExpression(prefix);expression=MathExpression(term,symbols=(variable,'n'))
 env={'n':7.0};a,b=int(lower.evaluate(env).real),int(upper.evaluate(env).real)
 if b<a or b-a>100:raise ParseError('Unexpected finite sum bounds')
 result=sum(expression.evaluate({**env,variable:float(k)}) for k in range(a,b+1))*factor.evaluate(env)
 return result

def sigma_radio(q,source):
 value=q['answer_fields'][0]['correct_value'];mid=q['math_academy_id']
 positive_limits={'q-73186','q-113886','q-73158','q-49189','q-113927','q-113941'}
 if mid in positive_limits:
  evidence='Reviewed saved integrand: continuous, positive in the integration interval interior; integral is nonzero'
 elif r'\sum' in value:
  try:result=finite_sum(value)
  except (ParseError,ValueError,IndexError,KeyError,ZeroDivisionError,OverflowError):return None
  if abs(result)<1e-7:return None
  evidence={'finite_sum_witness':{'n':7,'value':[result.real,result.imag]},'reason':'Nonzero saved finite sum; changing its coefficient changes the requested value'}
 else:return None
 options=[{'type':'math','value':value}]+[{'type':'math','value':factor+r'\left('+value+r'\right)'} for factor in ('2',r'\frac12','-1','3')]
 return assemble(q,source,options,[{'value':o['value'],'origin':'Local incorrect total coefficient','nonzero_evidence':evidence} for o in options[1:]])

def make_radio(q,source):
 if len(q['answer_fields'])!=1:return composite_radio(q,source)
 f=q['answer_fields'][0]
 if f['type']!='blank':return None,'already-choice-format'
 correct=copy.deepcopy(f['choices'][0]);assert correct['value']==f['correct_value']
 # Scalar blank decomposition must be restored to its complete equation for MC.
 if q['preparation']['answer_origin']=='equation-component':
  a=q['preparation']['answer_evidence'];correct={'type':a['type'],'value':clean_math(a['value'])}
 if correct['type']!='math':return categorical_radio(q,source)
 value=correct['value'];prefix=''
 limit=limit_radio(q,source)
 if limit:return limit
 structured=structured_radio(q,source)
 if structured:return structured
 sigma=sigma_radio(q,source)
 if sigma:return sigma
 if '=' in value:
  bits=value.split('=')
  if len(bits)!=2:return None,'equation-chain'
  prefix=bits[0]+'=';expression=bits[1]
 else:expression=value
 try:parsed=MathExpression(expression)
 except (ParseError,ValueError,IndexError,RecursionError):return None,'complex-response-needs-review'
 options=[correct];checks=[]
 # Reuse same-KP option families where their expression vocabulary matches.
 candidates=[]
 for example in source['questions']:
  if example['question_format']!='multiple-choice':continue
  for c in example['choices']:
   v=choice_value(c)
   if v and v['type']=='math':candidates.append((v,'Saved same-KP option q-'+example['question_id']))
 # A sign or coefficient perturbation is locally authored and can be verified.
 # These are fallbacks, rather than claimed historical choices.
 candidates += [({'type':'math','value':prefix+'-('+expression+')'},'Local sign error'),
                ({'type':'math','value':prefix+'2('+expression+')'},'Local factor-of-two error'),
                ({'type':'math','value':prefix+r'\frac{1}{2}('+expression+')'},'Local missing factor'),
                ({'type':'math','value':prefix+'3('+expression+')'},'Local factor-of-three error'),
                ({'type':'math','value':prefix+r'\frac{1}{3}('+expression+')'},'Local missing factor')]
 if not parsed.units:candidates += [({'type':'math','value':prefix+'('+expression+')+1'},'Local additive error'),
                ({'type':'math','value':prefix+'('+expression+')-1'},'Local subtractive error'),
                ({'type':'math','value':prefix+'('+expression+')+2'},'Local additive error')]
 arbitrary_constant='Integrat' in q['knowledge_point'] and bool(re.search(r'\b[CK]\b',expression))
 for candidate,provenance in candidates:
  cv=candidate['value']
  if prefix:
   if not cv.startswith(prefix):continue
   ce=cv[len(prefix):]
  elif '=' in cv:continue
  else:ce=cv
  witness=inequality_witness(expression,ce,arbitrary_constant)
  if not witness:continue
  if 'coterminal' in source_problem(q).lower():
   try:
    a,b=MathExpression(expression).evaluate({}).real,MathExpression(ce).evaluate({}).real
   except (ValueError,KeyError,ParseError):continue
   if abs((a-b)/(2*math.pi)-round((a-b)/(2*math.pi)))<1e-8:continue
  # Keep angle choices in the requested notation (degrees versus radians).
  if bool(re.search(r'∘|\\circ',expression))!=bool(re.search(r'∘|\\circ',ce)):continue
  # Require evidence against ALL prior options to prevent duplicate/equivalent choices.
  if any(not inequality_witness(old['value'][len(prefix):] if prefix else old['value'],ce,arbitrary_constant) for old in options):continue
  options.append(candidate);checks.append({'value':cv,'origin':provenance,'difference_witness':witness})
  if len(options)==5:break
 if len(options)<3:return None,'insufficient-distinct-options'
 return assemble(q,source,options,checks)

def explicit_repairs(q,source):
 # The four examples that exposed the import issue have direct worked keys and
 # screenshot-backed format patterns. Use normal MA-style distractors here.
 reviewed={
 'q-10289':[r'24{x}^{5}',r'4{x}^{5}',r'24{x}^{6}',r'24{x}^{7}',r'28{x}^{7}'],
 'q-64921':[r'\frac{\sqrt{3}}{2}',r'-\frac{\sqrt{3}}{2}',r'\frac{1}{2}',r'\frac{\sqrt{2}}{2}','0'],
 'q-118705':[r'\frac{8}{27}\,{\text{yd}}^{3}',r'\frac{2}{3}\,{\text{yd}}^{3}',r'\frac{4}{9}\,{\text{yd}}^{3}',r'\frac{8}{9}\,{\text{yd}}^{3}',r'\frac{27}{8}\,{\text{yd}}^{3}'],
 }
 mid=q['math_academy_id']
 linear_inequalities={'q-29440':('<','-2x+1'),'q-6054':(r'\ge',r'\frac{x}{2}-1'),'q-6056':(r'\le',r'\frac{3x}{2}')}
 if mid in linear_inequalities:
  relation,boundary=linear_inequalities[mid];assert re.sub(r'\s','',q['answer_fields'][0]['correct_value'])=='y'+relation+boundary
  new=copy.deepcopy(q);new['problem']=source_problem(q)+r' $y$ {{relation}} {{boundary-expression}}'
  new['answer_fields']=[{'key':key,'type':'blank','choices':[{'type':'math','value':value}],'correct_value':value,'evidence':'Saved inequality split using same-KP two-free-entry template'} for key,value in [('relation',relation),('boundary-expression',boundary)]]
  new['preparation']['response_repair']={'kind':'source-two-blank-inequality','source':source['source'],'source_question_ids':['q-'+x['question_id'] for x in source['questions']],'original_answer':q['answer_fields'][0]['correct_value'],'requires_symbolic_grader':True,'options_recovered_from_original_question':False}
  validate_ready(new);return new,None
 if mid=='q-23188':
  choices=['I only','II only','III only','I and II only','I and III only','II and III only','I, II, and III','None of those listed']
  assert 'So the correct answer is II and III only.' in q['worked_solution']
  choices.remove('II and III only');choices.insert(0,'II and III only')
  new,_=assemble(q,source,[{'type':'text','value':v} for v in choices],[{'value':v,'origin':'Exhaustive statement subsets; worked solution explicitly identifies II and III only'} for v in choices[1:]])
  new['preparation']['response_repair']['correct_answer_correction']={'previous':q['answer_fields'][0]['correct_value'],'correct':'II and III only','evidence':'Explicit final sentence in the saved worked solution; previous reconstruction selected an intermediate angle'}
  return new,None
 if mid in reviewed:
  values=reviewed[mid];assert values[0]==q['answer_fields'][0]['correct_value']
  checks=[]
  for v in values[1:]:
   witness=inequality_witness(values[0],v);assert witness
   checks.append({'value':v,'origin':'Reviewed local coefficient/power/sign or unit-volume distractor','difference_witness':witness})
  return assemble(q,source,[{'type':'math','value':v} for v in values],checks)
 if mid=='q-16295':
  assert q['answer_fields'][0]['correct_value']==r'81+15\,\text{i}'
  new=copy.deepcopy(q);new['problem']=source_problem(q)+r' ${{real-part}}+{{imaginary-coefficient}}\,\mathrm{i}$'
  new['answer_fields']=[{'key':k,'type':'blank','choices':[{'type':'math','value':v}],'correct_value':v,'evidence':'Saved product 81+15i; numeric component pattern from same-KP q-218539 and q-250605 screenshots'} for k,v in [('real-part','81'),('imaginary-coefficient','15')]]
  new['preparation']['response_repair']={'kind':'numeric-complex-components','source':source['source'],'source_question_ids':['q-218539','q-250605'],'original_answer':q['answer_fields'][0]['correct_value'],'options_recovered_from_original_question':False}
  validate_ready(new);return new,None
 if mid in {'q-26182','q-26115','q-72243','q-26198'}:
  newq=copy.deepcopy(q);value=q['answer_fields'][0]['correct_value'];assert re.fullmatch(r'\d{1,3}(,\d{3})+',value)
  scalar=value.replace(',','');newq['answer_fields'][0]['correct_value']=scalar;newq['answer_fields'][0]['choices'][0]['value']=scalar
  new,reason=make_radio(newq,source)
  if new:
   new['preparation']['response_repair']['display_normalization']={'saved':value,'numeric_value':scalar,'reason':'Thousands separators are not separate roots'}
  return new,reason
 if mid in {'q-79870','q-104021','q-110799','q-70435','q-76881','q-1301','q-1389','q-1324','q-1300','q-101019'}:
  value=q['answer_fields'][0]['correct_value'];vector=value.startswith('⟨');parts=value.strip('⟨⟩').split(',')
  assert len(parts)>=2
  newq=copy.deepcopy(q);newq['answer_fields']=[{'key':'component-'+str(i+1),'type':'blank','choices':[{'type':'math','value':v}],'correct_value':v} for i,v in enumerate(parts)]
  newq['preparation']['answer_origin']='coordinate-components' if vector else 'ordered-real-roots'
  new,reason=composite_radio(newq,source)
  if new:
   new['preparation']['answer_origin']=q['preparation']['answer_origin'];new['preparation']['response_repair']['original_answer_origin']=q['preparation']['answer_origin'];new['preparation']['response_repair']['decomposed_saved_value']=value
   if vector:
    for option in new['answer_fields'][0]['choices']:option['value']=r'\langle'+option['value'][1:-1]+r'\rangle'
    new['answer_fields'][0]['correct_value']=new['answer_fields'][0]['choices'][0]['value']
  return new,reason
 if mid=='q-16149':
  values=[r'$x\ge-\frac14$ and $y\ge-2$',r'$x\ge\frac14$ and $y\ge-2$',r'$x\ge-\frac14$ and $y\ge2$',r'$x\le-\frac14$ and $y\ge-2$',r'$x\ge-\frac14$ and $y\le-2$']
  assert [f['correct_value'] for f in q['answer_fields']]==[r'[-\frac14,\infty)',r'[-2,\infty)']
  return assemble(q,source,[{'type':'text','value':v} for v in values],[{'value':v,'origin':'Reviewed vertex bounds x=(t+1/2)^2-1/4 and y=t^2-2'} for v in values[1:]])
 infinite_sums={'q-103257':'Positive geometric series (8/5)*(3/4)/(1-3/4)=24/5','q-40691':'2.3 plus positive geometric series (43/10)*(1/100)/(1-1/100)'}
 inverse_derivatives={'q-3299','q-51348','q-110047','q-51351','q-47989','q-32640','q-32634'}
 if mid in infinite_sums or mid in inverse_derivatives:
  value=q['answer_fields'][0]['correct_value'];options=[{'type':'math','value':value}]+[{'type':'math','value':v+r'\left('+value+r'\right)'} for v in ('2',r'\frac12','-1','3')]
  reason=infinite_sums.get(mid,'Inverse derivative is reciprocal of the given nonzero derivative on its stated inverse-function domain; wrong overall factors change that derivative')
  return assemble(q,source,options,[{'value':v['value'],'origin':'Reviewed incorrect overall coefficient','nonzero_evidence':reason} for v in options[1:]])
 infinite_sets={'q-86603':(['2','3','5','6'],'Intersection is powers of 4; inserted values are not powers of 4'),'q-81533':(['1','2','3','5'],'Intersection is positive multiples of 4'),'q-81562':(['1','2','3','6'],'Union is positive multiples of 4 or 5'),'q-102146':(['1','2','3','6'],'Union is positive multiples of 4 or 5'),'q-101992':(['0','2','4','8'],'Set is odd integers greater than 8')}
 if mid in infinite_sets:
  bads,reason=infinite_sets[mid];value=q['answer_fields'][0]['correct_value'];assert value.startswith('{') and value.endswith('}') and '…' in value
  entries=value[1:-1].split(',');canonical=r'\{'+','.join(entries[:-1])+r',\ldots\}'
  options=[{'type':'math','value':canonical}]+[{'type':'math','value':r'\{'+bad+','+','.join(entries[:-1])+r',\ldots\}'} for bad in bads]
  return assemble(q,source,options,[{'value':v['value'],'origin':'Reviewed insertion of element outside the requested set','evidence':reason} for v in options[1:]])
 return None,None

def main():
 OUT.mkdir(exist_ok=True)
 qs=json.loads((BASE/'import-ready/questions.json').read_text())['questions'];idx=index_sources(qs)
 original={q['math_academy_id']:q for q in json.loads((BASE/'prepared.json').read_text())['questions']}
 readiness={q['math_academy_id']:q['accepted_by_current_grader'] for q in json.loads((BASE/'import-ready/runtime-readiness.json').read_text())['questions']}
 records=[];revised=[];repairs=[]
 for q in qs:
  mid=q['math_academy_id'];src=idx.get(q['knowledge_point_id']);types=src['format_counts'] if src else {}
  status='original-controls-preserved' if original[mid]['answer_fields'] else 'no-same-kp-source' if not types else 'reconstructed-blank-in-mc-kp' if set(types)=={'multiple-choice'} and any(f['type']=='blank' for f in q['answer_fields']) else 'mixed-or-other-source-format'
  new=None;reason=None
  if src:new,reason=explicit_repairs(q,src)
  if status=='reconstructed-blank-in-mc-kp' and new is None:new,reason=make_radio(q,src)
  if (new is None and not original[mid]['answer_fields'] and not readiness[mid]
      and 'multiple-choice' in types and status=='mixed-or-other-source-format'):
   new,reason=make_radio(q,src)
  if new:repairs.append({'id':mid,'before':q,'after':new})
  revised.append(new or q)
  decision='repair' if new else 'preserve-observed-controls' if status=='original-controls-preserved' else 'review' if reason or not readiness[mid] else 'retain-compatible-reconstruction'
  if mid=='q-133897':decision='retain-source-supported-symbolic-blank';reason='Same-KP examples confirm a single full symbolic blank; needs symbolic grading, not a format change'
  records.append({'id':mid,'topic_id':q['topic_id'],'kp_id':q['knowledge_point_id'],'kp':q['knowledge_point'],'origin':q['preparation']['answer_origin'],'engine_ready_before':readiness[mid],'status':status,'source_format_counts':types,'decision':decision,'review_reason':reason})
 save('kp-source-index.json',idx);save('audit.json',{'questions':records});save('repairs.json',{'questions':repairs});save('questions.json',{'questions':revised})
 rr=runtime_check(OUT)
 report={'question_count':len(qs),'kp_count':len({q['knowledge_point_id'] for q in qs}),'topic_count':len({q['topic_id'] for q in qs}),'matched_kps':len({q['knowledge_point_id'] for q in qs}&set(idx)),'statuses':dict(collections.Counter(r['status'] for r in records)),'decisions':dict(collections.Counter(r['decision'] for r in records)),'review_reasons':dict(collections.Counter(r['review_reason'] for r in records if r['review_reason'])),'engine_ready_before':sum(readiness.values()),'engine_ready_after':rr['current_engine_ready_count'],'database_writes':0}
 save('report.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
