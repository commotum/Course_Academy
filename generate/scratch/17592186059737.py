#!/usr/bin/env python3
"""Cross-product magnitude equations, basis 1356. No database writes.
Observed templates retain their full determinant/minor/product/norm/solve order.
Explicit observed banks are opaque root-set rescalings, not recovered error intent.
Default radios use one complete authored square-root/sign error bank; hard uses
observed one/two ordered blank layouts. See private evidence for scope and repairs.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as s
X=s.Symbol('x',real=True)
KP=17592186059737
ROOT=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
REC=SOURCE['record']; QUESTIONS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
VERSION='cross-equation-2'

def norm(t): return t.replace('\\\\','\\').replace('±',r'\pm')
def tex(e): return s.latex(s.sympify(e),order='lex').replace(' x','x')
def parse(t):
 t=norm(t).replace(r'\,','').replace(r'\left','').replace(r'\right','').strip().rstrip('.')
 while r'\frac' in t:
  m=re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',t)
  if not m:raise ValueError(t)
  t=t[:m.start()]+'(('+m[1]+')/('+m[2]+'))'+t[m.end():]
 while r'\sqrt' in t:
  m=re.search(r'\\sqrt\{([^{}]*)\}',t)
  if not m:raise ValueError(t)
  t=t[:m.start()]+'sqrt('+m[1]+')'+t[m.end():]
 t=t.replace('{','(').replace('}',')').replace('^','**').replace(r'\cdot','*')
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 return parse_expr(t,local_dict={'x':X},transformations=standard_transformations+(implicit_multiplication_application,))
def roots_value(t):
 t=norm(t).replace(r'\,','').replace(' ','');t=re.sub(r'x=', '',t)
 if r'\pm' in t:
  v=parse(t.replace(r'\pm',''));return tuple(sorted([-v,v],key=lambda a:float(a)))
 return tuple(sorted(set(parse(v) for v in t.split(',') if v.strip()),key=lambda a:float(a)))
def value(rs):
 if len(rs)==2 and s.simplify(rs[0]+rs[1])==0:return 'x='+r'\pm '+tex(rs[1])
 return 'x='+r',\,'.join(tex(v) for v in rs)
def vectors_prompt(text):
 vs=re.findall('⟨([^⟩]*)⟩',text)
 a,b=[s.Matrix([parse(v) for v in vs[i].split(',')]) for i in (0,1)]
 rhs=re.search(r'\|\s*=\s*([^$]*)',text)
 if not rhs: raise ValueError(text)
 return a,b,parse(rhs[1])
def eligible(a,b,R,level,observed=False):
 if len(a)!=3 or len(b)!=3 or any(v.has(s.Float) for v in [*a,*b]) or any(s.Poly(v,X).degree()>1 for v in [*a,*b]):raise ValueError('linear coordinates only')
 coeff=[abs(c) for v in [*a,*b] for c in s.Poly(v,X).all_coeffs()]
 if any(c>12 or s.denom(c)>4 for c in coeff):raise ValueError('coordinate workload bounds')
 cross=a.cross(b);N=s.expand(cross.dot(cross));P=s.Poly(N-R**2,X)
 if P.degree()!=2 or R<=0:raise ValueError('nondegenerate positive-magnitude quadratic')
 roots=tuple(sorted(s.solve(P.as_expr(),X),key=lambda v:float(v)))
 if not roots or any(not v.is_real or s.simplify(N.subs(X,v)-R**2)!=0 for v in roots):raise ValueError('full real solution set required')
 if not observed:
  if level in ('easy','moderate'):
   if P.nth(1)!=0 or len(roots)!=2 or any(v!=0 and s.Poly(v,X).degree()==1 and s.Poly(v,X).nth(0)!=0 for v in cross) or not any(v!=0 and s.Poly(v,X).degree()==0 for v in cross):raise ValueError('symmetric unshifted norm required')
   if level=='easy' and (max(coeff)>3 or any(s.denom(c)!=1 for c in coeff) or not roots[1].is_Integer):raise ValueError('easy integer bound')
   if level=='moderate' and (sum(bool(s.diff(v,X)) for v in cross)!=2 or max(coeff)>5):raise ValueError('moderate two slope components bound')
  else:
   primitive=s.Poly(s.polys.polytools.primitive(P.as_expr(),X)[1],X)
   if P.nth(1)==0 or max(abs(c) for c in primitive.all_coeffs())>100 or any(abs(v)>10 or s.denom(v)>4 for v in roots):raise ValueError('hard reduced algebra bounds')
 return cross,N,roots

def polynomial_scale(t,k):
 # Replace complete polynomial monomials, preserving i/j/k basis letters.
 def sub(m):
  c=m.group(1);c=s.Rational(c or '1');power=2 if m.group(2) else 1
  v=c*k**power
  if power==1:return ('' if v==1 else '-' if v==-1 else tex(v))+'x'
  return ('' if v==1 else '-' if v==-1 else tex(v))+r'{x}^{2}'
 return re.sub(r'(?<![A-Za-z\\])(?:(\d+)\s*)?(?:\{x\}|x)(\^\{2\})?',sub,t)
def scale_text(t,k):
 if k==1:return t
 def transform(m):
  display=m.group(1) is not None;p=m.group(1) if display else m.group(2)
  if not display and re.match(r'^x\s*=',p):
   tail=p.split('=',1)[1].rstrip('.')
   try:
    p=value(tuple(v/k for v in roots_value('x='+tail)))+('.' if p.endswith('.') else '')
    return '$'+p+'$'
   except Exception:pass
  p=polynomial_scale(p,k)
  return ('$$'+p+'$$') if display else ('$'+p+'$')
 return re.sub(r'\$\$(.*?)\$\$|\$([^$]*)\$',transform,t,flags=re.S)
def observed_solution(q,k,a,b,R,roots):
 raw=q.get(':question/worked-solution')
 if raw is None:return authored_solution(a,b,R,roots)
 if q[':question/math-academy-id']=='q-103540':raw=raw.replace('⟨-5,-4x,x⟩','⟨-5,4x,-x⟩').replace('(-4x)^{2}+{x}^{2}','(4x)^{2}+(-x)^{2}')
 return scale_text(raw,k)
def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def authored_solution(a,b,R,roots):
 c=a.cross(b);N=s.expand(c.dot(c));P=s.expand(N-R**2)
 pairs=[(a[1],b[2],a[2],b[1]),(a[0],b[2],a[2],b[0]),(a[0],b[1],a[1],b[0])]
 det=lambda rows:'|'+r'\begin{aligned}'+r' \\ '.join(' & '.join(tex(e) if not isinstance(e,str) else e for e in row) for row in rows)+r'\end{aligned}'+'|'
 minors=''.join(('-' if i==1 else '+' if i==2 else '')+det([[u,w],[z,v]])+label for i,((u,v,w,z),label) in enumerate(zip(pairs,'ijk')))
 products=''.join(('-' if i==1 else '+' if i==2 else '')+'('+tex(u)+r'\cdot ('+tex(v)+')-'+tex(w)+r'\cdot ('+tex(z)+'))'+label for i,((u,v,w,z),label) in enumerate(zip(pairs,'ijk')))
 evaluated=''.join(('-' if i==1 else '+' if i==2 else '')+'('+tex(s.expand(u*v))+'-('+tex(s.expand(w*z))+'))'+label for i,((u,v,w,z),label) in enumerate(zip(pairs,'ijk')))
 cross=aligned([r'a\times b & ='+det([list('ijk'),list(a),list(b)]),' & ='+minors,' & ='+products,' & ='+evaluated,' & =⟨'+','.join(tex(v) for v in c)+'⟩.'])
 squares='+'.join('('+tex(v)+')^{2}' for v in c)
 expanded='+'.join('('+tex(s.expand(v*v))+')' for v in c)
 mag=aligned([r'|\,a\times b\,| & =\sqrt{'+squares+'}',r' & =\sqrt{'+expanded+'}',r' & =\sqrt{'+tex(N)+'}.'])
 solve=aligned([r'|\,a\times b\,| & ='+tex(R),r'\sqrt{'+tex(N)+'} & ='+tex(R),tex(N)+' & ='+tex(R**2),tex(P)+' & =0',tex(s.factor(P))+' & =0','x & ='+r',\,'.join(tex(v) for v in roots)+'.'])
 check=' '.join('$'+r'|\,a\times b\,|_{x='+tex(v)+'}='+tex(s.sqrt(N.subs(X,v)))+'='+tex(R)+'$' for v in roots)
 return 'Using the determinant formula, we get\n\n'+cross+'\n\nNow, computing the magnitude, we get\n\n'+mag+'\n\nLastly, we solve for $x$ the following equation:\n\n'+solve+'\n\nTherefore, the '+('solution is ' if len(roots)==1 else 'solutions are ')+ '$'+value(roots)+'.$\n\nChecking in the original magnitude equation: '+check+'.'

def ident(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(v,sort_keys=True,ensure_ascii=False)))
def assemble(level,seed,template,profile,parameters,prompt,solution,banks,roots,recipes):
 content=[VERSION,prompt,solution,[(key,kind,sorted(vals),correct) for key,kind,vals,correct in banks]];qid=ident(content)
 fields=[]
 for key,kind,vals,correct in banks:
  fid=ident([qid,key]);choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
  random.Random(seed+len(fields)).shuffle(choices)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',ident([fid,correct])]})
 a,b,R=vectors_prompt(prompt)
 task=[s.srepr(a),s.srepr(b),s.srepr(R**2)]
 return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':parameters,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'mathematical_fingerprint':hashlib.sha256(json.dumps(task).encode()).hexdigest(),'recipes':recipes,'roots':[str(v) for v in roots]}}

def raw_replay(level,seed,template,field_type,parameters,profile):
 """Parameterized evidence replay. Never infer absent raw attributes or repair raw math."""
 base='observed-'+template
 if template not in QUESTIONS or profile!=base+':raw':raise ValueError('raw source profile')
 supported=generate(level,seed,template,field_type,parameters,base)
 q=QUESTIONS[template];params=supported['generation']['parameters'];k=s.Rational(params['scale'])
 prompt=scale_text(q[':question/problem'],k)
 solution=scale_text(q[':question/worked-solution'],k) if ':question/worked-solution' in q else None
 bank=[]
 for f in q[':question/answer-fields']:
  kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
  transform=lambda v:v if k==1 else value(tuple(r/k for r in roots_value(v))) if kind=='radio' else tex(parse(v)/k)
  vals=[transform(a[':answer/value']) for a in f[':answer-field/choices']]
  correct=transform(f[':answer-field/correct'][':answer/value']) if ':answer-field/correct' in f else None
  bank.append((f[':answer-field/key'],kind,vals,correct))
 qid=ident([VERSION,prompt,solution,[(key,kind,sorted(vals),correct) for key,kind,vals,correct in bank],q.get(':question/difficulty')])
 fields=[]
 for key,kind,vals,correct in bank:
  fid=ident([qid,key]);choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
  random.Random(seed+len(fields)).shuffle(choices)
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices}
  if correct is not None:f[':answer-field/correct']=[':answer/id',ident([fid,correct])]
  fields.append(f)
 question={':question/id':qid,':question/problem':prompt,':question/answer-fields':fields}
 if solution is not None:question[':question/worked-solution']=solution
 if ':question/difficulty' in q:question[':question/difficulty']=q[':question/difficulty'][':db/ident']
 generation=supported['generation'].copy();generation.update(profile=profile,evidence_only=True,eligible_for_learning=False,raw_source_id=q[':db/id'],raw_anomalies={'q-19783':['dot operator inconsistent with cross scope/bank','missing key','missing solution','missing difficulty'],'q-103540':['incorrect final cross-vector signs and norm-substitution signs']}.get(template,[]))
 generation['supported_repair_roots']=generation.pop('roots')
 if template=='q-19783':generation['mathematical_fingerprint']=hashlib.sha256(('raw-dot:'+generation['mathematical_fingerprint']).encode()).hexdigest()
 return {'knowledge_point':supported['knowledge_point'],'question':question,'generation':generation}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if profile and profile.endswith(':raw'):return raw_replay(level,seed,template,field_type,parameters,profile)
 rng=random.Random(seed)
 if template in QUESTIONS:
  q=QUESTIONS[template];expected=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/moderate').split('/')[-1]
  if level!=expected:raise ValueError('observed template level')
  params=parameters or {'scale':rng.choice(['1/2','1','2'])};k=s.Rational(params['scale'])
  if set(params)!={'scale'} or k not in [s.Rational(1,2),1,2]:raise ValueError('observed scaling domain')
  prompt=q[':question/problem'];prompt=prompt.replace(r'\mid a \cdot b|',r'|\,a\times b\,|')
  prompt=scale_text(prompt,k);a,b,R=vectors_prompt(prompt);c,N,roots=eligible(a,b,R,level,True)
  banks=[]
  for f in q[':question/answer-fields']:
   kind=f[':answer-field/type'][':db/ident'].split('/')[-1]
   if field_type and field_type!=kind:raise ValueError('field type')
   vals=[]
   for ans in f[':answer-field/choices']:
    raw=norm(ans[':answer/value']);vals.append(raw if k==1 else value(tuple(v/k for v in roots_value(raw))) if kind=='radio' else tex(parse(raw)/k))
   corr=f.get(':answer-field/correct',{}).get(':answer/value')
   if corr:correct=norm(corr) if k==1 else value(tuple(v/k for v in roots_value(corr))) if kind=='radio' else tex(parse(corr)/k)
   else:correct=next(v for v in vals if roots_value(v)==roots)
   banks.append((f[':answer-field/key'],kind,vals,correct))
  profile=profile or 'observed-'+template
  if profile!='observed-'+template:raise ValueError('source profile required')
  return assemble(level,seed,template,profile,params,prompt,observed_solution(q,k,a,b,R,roots),banks,roots,['opaque observed complete bank; root values rescaled, intent unresolved'])
 # Easy: authored from canonical unshifted cross-magnitude equation, small integers.
 # Moderate: exactly two variable cross components, signed products, integer/radical roots.
 # Hard: shifted quadratic magnitude, one or two rational roots, observed ordered blanks.
 template=template or {'easy':'canonical_symmetric','moderate':'signed_symmetric','hard':'shifted_magnitude'}[level]
 if template!={'easy':'canonical_symmetric','moderate':'signed_symmetric','hard':'shifted_magnitude'}[level]:raise ValueError('template')
 profile=profile or ('ordered_blanks' if level=='hard' else 'sign_square_root')
 expectedprofile='ordered_blanks' if level=='hard' else 'sign_square_root'
 if profile!=expectedprofile:raise ValueError('profile')
 kind='blank' if level=='hard' else 'radio'
 if field_type and field_type!=kind:raise ValueError('field type')
 for attempt in range(200):
  p=parameters
  if p is None:
   if level=='easy':p={'a':[rng.choice([1,2,3]),1,str(rng.choice([1,2,3]))+'*x'],'b':[0,1,str(rng.choice([1,2]))+'*x'],'root':rng.choice([2,3,4])}
   elif level=='moderate':
    p={'a':[rng.choice(['2*x','-2*x','3*x']),rng.choice([2,3]),rng.choice([1,2,3])],'b':[rng.choice(['x','-x']),rng.choice([1,2]),rng.choice([-2,-1,1,2])],'root':rng.choice(['sqrt(2)','sqrt(3)','sqrt(5)',2,3,4])}
   else:p={'a':[rng.choice(['x','2*x','3*x']),rng.choice([1,2,3]),rng.choice([1,2,3,4,5])],'b':[rng.choice([1,2,3]),0,rng.choice([1,2,3])],'offset':rng.choice([0,1,2])}
  try:
   expectedkeys={'a','b','offset'} if level=='hard' else {'a','b','root'}
   if set(p)!=expectedkeys:raise ValueError('parameter keys')
   a=s.Matrix([s.sympify(v,locals={'x':X}) for v in p['a']]);b=s.Matrix([s.sympify(v,locals={'x':X}) for v in p['b']]);N=s.expand(a.cross(b).dot(a.cross(b)))
   if level=='easy' and (a[0] not in [1,2,3] or a[1]!=1 or a[2] not in [X,2*X,3*X] or b[0]!=0 or b[1]!=1 or b[2] not in [X,2*X] or a[2]==b[2]):raise ValueError('canonical coordinate shape')
   if level=='moderate' and (a[0] not in [2*X,-2*X,3*X] or a[1] not in [2,3] or a[2] not in [1,2,3] or b[0] not in [X,-X] or b[1] not in [1,2] or b[2] not in [-2,-1,1,2]):raise ValueError('signed coordinate shape')
   if level=='hard' and (a[0] not in [X,2*X,3*X] or a[1] not in [1,2,3] or a[2] not in [1,2,3,4,5] or b[0] not in [1,2,3] or b[1]!=0 or b[2] not in [1,2,3]):raise ValueError('shifted coordinate shape')
   if level=='hard':
    if s.Rational(p['offset']) not in [0,1,2]:raise ValueError('offset bounds')
    poly=s.Poly(N,X);center=-poly.nth(1)/(2*poly.nth(2));R=s.sqrt(N.subs(X,center+s.Rational(p['offset'])))
   else:
    root=s.sympify(p['root']);
    if root not in [2,3,4,s.sqrt(2),s.sqrt(3),s.sqrt(5)]:raise ValueError('root bounds')
    R=s.sqrt(N.subs(X,root))
   c,N,roots=eligible(a,b,R,level)
   if kind=='radio':
    r=roots[1];sets=[roots,(r,),(-r,),(-r*r,r*r),(-s.sqrt(r),s.sqrt(r))]
    if len(set(sets))!=5:raise ValueError('entire bank collision')
    vals=[value(v) for v in sets];banks=[('selection',kind,vals,vals[0])]
   else:banks=[('field-'+str(i+1),kind,[tex(v)],tex(v)) for i,v in enumerate(roots)]
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('sampling exhausted')
 prefix='Let $a=⟨'+','.join(tex(v) for v in a)+'⟩,$ $b=⟨'+','.join(tex(v) for v in b)+'⟩$ and $'+r'|\,a\times b\,|='+tex(R)+'.$ '
 if kind=='radio':prompt=prefix+'Find $x.$'
 elif len(roots)==1:prompt=prefix+'Find $x.$\n\n$\\,x=$\n{{field-1}}'
 else:prompt=prefix+'Then, in **ascending order**, the possible values of $x$ are\n\n$\\,x=$\n{{field-1}}$\\,$ and $\\,x=$\n{{field-2}}.'
 return assemble(level,seed,template,profile,p,prompt,authored_solution(a,b,R,roots),banks,roots,['correct complete roots','positive root only','negative root only','omit square root','take square root twice'] if kind=='radio' else ['ordered exact root fragments'])
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];out=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  out+='\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n'
 return out+'\n'+q.get(':question/worked-solution','[No captured worked solution.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 rows=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(rows,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
