#!/usr/bin/env python3
"""Step 3–7 local ellipse Cartesian-equation generator. No database operations.

Observed masks retain the complete fixed solution prose and its ordered stages;
parameters populate complete expression components, never bare numeric prose.
Observed opaque banks remain public, evidence-only profiles. Normal sampling
chooses an eligible complete family/bank first and rejects entire colliding banks.
Easy is authored scaffolding (isolation supplied), moderate origin isolation,
hard translated isolation. All assets are absent; plot steps are explicit no-ops.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
D=Path(__file__).with_suffix('')
RAW=json.loads((D/'source.json').read_text())
SOURCE=RAW['record']; KP_ID=17592186152188
VERSION='ellipse-cartesian-1'
X,Y=s.symbols('x y',real=True)
Q={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
# Source radius/translation components, exact and independently checked.
ORIGINAL={
'q-6881':('2','1','0','0'),'q-79375':('4','1','-1','1'),
'q-106405':('5','4','0','0'),'q-106406':('1/2','1/3','0','0'),
'q-106407':('2/3','3/2','0','0'),'q-106408':('1/2','1/2','2','3'),
'q-106715':('3','5','0','0'),'q-15792':('5','3','0','0'),
'q-15843':('6','2','0','0'),'q-327798':('6','2*sqrt(7)','3','-5'),
'q-327803':('10','3*sqrt(11)','-4','12'),'q-327808':('4*sqrt(6)','5*sqrt(2)','0','0'),
'q-327809':('9','4*sqrt(3)','0','0'),'q-327811':('6*sqrt(2)','11','0','0'),
'q-79377':('3','6','-5','-2')}
OPAQUE={'q-79375','q-79377'}
RECIPE_ORDER={}
TEMPLATES={k: {'level':q[':question/difficulty'][':db/ident'].split('/')[-1], 'type':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]} for k,q in Q.items()}
TEMPLATES['easy_supplied_isolation']={'level':'easy','type':'radio'}
TEMPLATES['hard_translated_authored']={'level':'hard','type':'radio'}
def latex(v):return s.latex(s.sympify(v)).replace(' \\sqrt',r'\sqrt')
def signed(n):return ('+' if n>0 else '-')+latex(abs(n)) if n else ''
def atom(v,h):return v+signed(-h)
def simultaneous(text,mapping):
 mapping={k:v for k,v in mapping.items() if k}
 return re.sub('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)),lambda m:mapping[m.group()],text) if mapping else text

def axis_block(text,v,old,new):
 """Populate complete axis-expression components inside an extracted block."""
 a,h=old; b,k=new; trig='cos' if v=='x' else 'sin'
 mapping={atom(v,h):atom(v,k)} if h else {}
 # Source coefficients occur only as complete trig coefficients, fraction
 # denominators, evaluated reciprocal multipliers, and squared denominators.
 ca,cb=latex(a),latex(b)
 mapping[ca+r'\operatorname{'+trig+'}']=(cb if b!=1 else '')+r'\operatorname{'+trig+'}'
 if a==1:
  mapping[r'\operatorname{'+trig+'}']=(cb if b!=1 else '')+r'\operatorname{'+trig+'}'
 # Translation occurs in the initial equation RHS, not in trig powers.
 if h:
  mapping[r'\theta '+signed(h)]=r'\theta '+signed(k)
 for aa,bb in [(a,b),(a*a,b*b)]:
  mapping['}{'+latex(aa)+'}']='}{'+latex(bb)+'}'
 mapping['}{{'+ca+'}^{2}}']='}{{'+cb+'}^{2}}'
 mapping['}{('+ca+')^{2}}']='}{('+cb+')^{2}}'
 # Reciprocal rows multiply the entire variable expression.
 for aa,bb in [(1/a,1/b),(1/a**2,1/b**2)]:
  for suffix in [v,'('+atom(v,h)+')','{'+v+'}','{('+atom(v,h)+')}']:
   mapping[latex(aa)+suffix]=latex(bb)+(suffix.replace(atom(v,h),atom(v,k)) if h else suffix)
 return simultaneous(text,mapping)

def split_terms(text):
 """Split the complete source LHS at its top-level binary sign."""
 lhs=text.split('=')[0];depth=0
 for i,c in enumerate(lhs):
  if c in '{(':depth+=1
  elif c in '})':depth-=1
  elif c in '+-' and i and depth==0:return lhs[:i],c,lhs[i+1:]
 raise ValueError('No source term split: '+text)

def term_like(old,v,c,h):
 """Retain numerator/group shells; replace complete coefficient/shift slots."""
 # Whole-term fractions have denominator after the numerator closing brace.
 m=re.fullmatch(r'\\frac\{(.+)\}\{([^{}]+)\}',old)
 coord=atom(v,h)
 if m:
  num=m.group(1);num=re.sub(v+r'[+-]\d+',lambda _:coord,num)
  return r'\frac{'+num+'}{'+latex(1/c)+'}'
 # Scalar multiplier before the source coordinate square, keeping all groups.
 idx=old.find(v);start=idx
 while start and old[start-1] in '{(':start-=1
 shell=old[start:];shell=re.sub(v+r'[+-]\d+',lambda _:coord,shell)
 return (latex(c) if c!=1 else '')+shell

def recipes(profile,p):
 a,b,h,k=p;cx,cy=1/a**2,1/b**2; C=(cx,cy,h,k,'+')
 if profile=='q-6881':return [(1,1,h,k,'+'),(cx,-cy,h,k,'+'),C,(1/a,cy,h,k,'+'),(cy,cx,h,k,'+')]
 if profile in {'q-106405','q-106715','q-15792'}:return [(cy,cx,h,k,'+'),(cx,-cy,h,k,'+'),C,(1/a,1/b,h,k,'+'),(cy,-cx,h,k,'+')]
 if profile=='q-15843':return [(-cy,cx,h,k,'+'),(cy,cx,h,k,'+'),(1/a,1/b,h,k,'+'),(cy,-cx,h,k,'+'),C]
 if profile=='q-106406':return [C,(cx,-cy,h,k,'+'),(cy,cx,h,k,'+'),(a*a,b*b,h,k,'+'),(a*a,-b*b,h,k,'+')]
 if profile=='q-106407':return [(cx,cx,h,k,'+'),(cx,-cy,h,k,'+'),(cy,cx,h,k,'+'),(cy,-cx,h,k,'+'),C]
 if profile=='q-106408':return [(a*a,b*b,h,k,'+'),(cx,-cy,h,k,'+'),(cx,cy,k,h,'+'),(a*a,-b*b,h,k,'+'),C]
 if profile=='q-79375':return [(cx,1/a,h,k,'+'),(cx,cy,-h,-k,'+'),(1/a,1/a,h,0,'+'),(1/a,cy,-h,-k,'+'),C]
 if profile=='q-79377':return [(cx,cy,-h,-k,'+'),(1/(2*a),cy,h,k,'+'),(cx,1/(3*b),h,k,'+'),C,(1/a,1/b,-h,-h,'+')]
 return [C]

def source_render(t,p,profile):
 q=Q[t];old=tuple(map(s.sympify,ORIGINAL[t]));a,b,h,k=p
 prompt=q[':question/problem']; sol=q[':question/worked-solution']
 # Full parametric formulas in prompt, isolated by x/y boundaries.
 m=re.search(r'x=(.*?),\\,y=(.*?),\\,0',prompt);assert m
 nx=axis_block(m.group(1),'x',(old[0],old[2]),(a,h));ny=axis_block(m.group(2),'y',(old[1],old[3]),(b,k))
 prompt=prompt[:m.start(1)]+nx+prompt[m.end(1):m.start(2)]+ny+prompt[m.end(2):]
 # Ordered source block structure retained; numbers cannot enter prose.
 blocks=list(re.finditer(r'\$\$(.*?)\$\$',sol,re.S)); replacements={}
 replacements[blocks[0].group(1)]=axis_block(blocks[0].group(1),'x',(old[0],old[2]),(a,h))
 replacements[blocks[1].group(1)]=axis_block(blocks[1].group(1),'y',(old[1],old[3]),(b,k))
 correct=q[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
 tx,sign,ty=split_terms(correct)
 newx=term_like(tx,'x',1/a**2,h);newy=term_like(ty,'y',1/b**2,k)
 for block in blocks[2:]:replacements[block.group(1)]=simultaneous(block.group(1),{tx:newx,ty:newy})
 sol=simultaneous(sol,replacements)
 field=q[':question/answer-fields'][0];bank=[]
 # Map each complete source option to its explicit operation tuple; recipes
 # above are a whole bank, never an arbitrary wrong-value pool.
 old_recipes=recipes(profile,old);new_recipes=recipes(profile,p)
 for src in field[':answer-field/choices']:
  observed=tex_expr(src[':answer/value'].split('=')[0])
  key=(profile,src[':answer/value'])
  matches=RECIPE_ORDER.get(key)
  if matches is None:
   matches=[i for i,(cx,cy,hx,ky,_) in enumerate(old_recipes) if s.simplify(observed-(cx*(X-hx)**2+cy*(Y-ky)**2))==0]
   RECIPE_ORDER[key]=matches
  if len(matches)!=1:raise ValueError('Unmapped source bank member')
  r=new_recipes[matches[0]]
  ox,sg,oy=split_terms(src[':answer/value']);vx='x' if 'x' in ox else 'y';vy='y' if vx=='x' else 'x'
  cx,cy,hx,ky,_=r
  if vx=='y':cx,cy=cy,cx;hx,ky=ky,hx
  # Separate binary sign from signed coefficient.
  newsign='-' if cy<0 else '+'
  value=term_like(ox,vx,cx,hx)+newsign+term_like(oy,vy,abs(cy),ky)
  if '=' in src[':answer/value']:value+='=1'
  bank.append(value)
 return prompt,sol,bank

def expression_term(v,c,h):
 num='{'+v+'}^{2}' if not h else '('+atom(v,h)+')^{2}'
 return num if c==1 else r'\frac{'+num+'}{'+latex(1/c)+'}'
def normal_bank(p):
 a,b,h,k=p;cx,cy=1/a**2,1/b**2
 if h or k:return [(cx,cy,h,k),(cx,cy,-h,-k),(1/a,1/b,h,k),(cy,cx,h,k),(cx,-cy,h,k)]
 return [(cx,cy,0,0),(cy,cx,0,0),(1/a,1/b,0,0),(cx,-cy,0,0),(cx,1/b,0,0)]
def authored_render(t,p):
 a,b,h,k=p;easy=t=='easy_supplied_isolation'
 param=(r'\frac{x}{'+latex(a)+r'}=\cos\theta,\quad \frac{y}{'+latex(b)+r'}=\sin\theta') if easy else ('x='+latex(a)+r'\cos\theta'+signed(h)+r',\quad y='+latex(b)+r'\sin\theta'+signed(k))
 prompt='Find the Cartesian equation of the ellipse defined by\n\n$$\n'+param+r',\quad 0\leq\theta<2\pi.'+'\n$$'
 opening='To find the Cartesian equation of the ellipse, we need to eliminate the parameter $\\theta .$ We can do this using the Pythagorean theorem.'
 sol=opening
 for v,radius,shift,trig in [('x',a,h,'cos'),('y',b,k,'sin')]:
  inv=r'\frac{'+atom(v,shift)+'}{'+latex(radius)+'}'
  rows=[] if easy else [v+' & ='+latex(radius)+'\\'+trig+r'\theta'+signed(shift)]
  rows.extend([inv+' & ='+'\\'+trig+r'\theta',r'\frac{'+('('+atom(v,shift)+')^{2}' if shift else '{'+v+'}^{2}')+'}{('+latex(radius)+')^{2}} & ='+'\\'+trig+r'^2\theta',expression_term(v,1/radius**2,shift)+' & ='+'\\'+trig+r'^2\theta'])
  sol+='\n\nBy '+('squaring' if easy else 'isolating')+' the $\\'+trig+'\\theta$ term in the $'+v+'$-equation'+('' if easy else ' and squaring')+', we get\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+r'.\end{aligned}'+'\n$$'
 correct=expression_term('x',1/a**2,h)+'+'+expression_term('y',1/b**2,k)
 sol+='\n\nAdding the two equations and using $\\cos^2\\theta+\\sin^2\\theta=1,$ we get\n\n$$\n'+correct+r'=\cos^2\theta+\sin^2\theta=1.'+'\n$$\n\nSo the Cartesian equation of the ellipse is\n\n$$\n'+correct+'=1.\n$$'
 bank=[expression_term('x',cx,hx)+('+' if cy>0 else '-')+expression_term('y',abs(cy),ky)+'=1' for cx,cy,hx,ky in normal_bank(p)]
 return prompt,sol,bank

# EASY — authored isolation supplied; two unequal integer radii 2..12.
# MODERATE — observed origin masks; normal radii both nonunit. Integers,
# reciprocal rationals and familiar radicals preserve each source row family.
# HARD — observed translated masks; both shifts nonzero (|shift| <=12).
def sample(t,rng):
 if t=='easy_supplied_isolation':return tuple(map(s.Integer,[rng.randint(2,12),rng.randint(2,12),0,0]))
 if t=='hard_translated_authored':return tuple(map(s.Integer,[rng.randint(2,12),rng.randint(2,12),rng.choice([i for i in range(-12,13) if i]),rng.choice([i for i in range(-12,13) if i])]))
 old=tuple(map(s.sympify,ORIGINAL[t]));p=[]
 for i,v in enumerate(old):
  if i>=2:p.append(s.Integer(rng.choice([j for j in range(-12,13) if j])) if v else s.Integer(0))
  elif v==1:p.append(v)
  elif v.is_Integer:p.append(s.Integer(rng.randint(2,12)))
  elif v.is_Rational:p.append(s.Rational(1,rng.randint(2,9)) if v.p==1 else s.Rational(rng.randint(2,9),rng.randint(2,9)))
  else:p.append(rng.randint(2,6)*s.sqrt(rng.choice([2,3,5,6,7,10,11])))
 if t=='q-106408':p[1]=p[0]
 return tuple(p)
def validate_parameters(t,p,raw):
 a,b,h,k=p
 if not h.is_Integer or not k.is_Integer:raise ValueError('Translations must be integers')
 if any(not v.is_real for v in p) or a<=0 or b<=0 or a*a>400 or b*b>400 or abs(h)>12 or abs(k)>12:raise ValueError('Outside familiar source arithmetic bounds')
 if t in Q:
  orig=tuple(map(s.sympify,ORIGINAL[t]))
  for i in range(4):
   if i>=2 and bool(p[i])!=bool(orig[i]):raise ValueError('Source zero/nonzero translation stage must stay fixed')
   if i<2:
    v=orig[i]
    if v==1 and p[i]!=1:raise ValueError('Unit stage radius fixed')
    if v.is_Integer and v!=1 and (not p[i].is_Integer or p[i]<2 or p[i]>12):raise ValueError('Integer radius family')
    if v.is_Rational and not v.is_Integer and (not p[i].is_Rational or p[i].q==1 or p[i].p>9 or p[i].q>9 or (v.p==1 and p[i].p!=1)):raise ValueError('Reduced rational family')
    if not v.is_Rational:
     coefficient,root=p[i].as_coeff_Mul()
     if coefficient not in range(2,7) or root not in [s.sqrt(n) for n in [2,3,5,6,7,10,11]]:raise ValueError('Familiar radical family')
  if t=='q-106408' and a!=b:raise ValueError('Equal-radius source family')
 else:
  if not a.is_Integer or not b.is_Integer or not 2<=a<=12 or not 2<=b<=12:raise ValueError('Authored integer radii 2..12')
  if t=='easy_supplied_isolation' and (h or k):raise ValueError('Easy has supplied origin isolation')
  if t=='hard_translated_authored' and (not h or not k):raise ValueError('Hard requires two translations')


def uid(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,value))
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in {'easy','moderate','hard'}:raise ValueError('Unknown difficulty')
 if parameters is not None and set(parameters)!={'a','b','h','k'}:raise ValueError('Parameters require exactly a,b,h,k')
 if profile and profile.startswith('source-method:'):
  selected=profile.split(':',1)[1]
  if template and template!=selected:raise ValueError('Profile/template mismatch')
  template=selected
 if profile=='repaired:q-327811':
  if template and template!='q-327811':raise ValueError('Profile/template mismatch')
  template='q-327811'
 rng=random.Random(seed)
 raw=bool(profile and profile.startswith('observed:'))
 if raw:
  chosen=profile.split(':',1)[1]
  if template and template!=chosen:raise ValueError('Source profile/template mismatch')
  template=chosen
 eligible=[k for k,v in TEMPLATES.items() if v['level']==level and (not field_type or v['type']==field_type) ]
 if template is None:template=rng.choice(eligible)
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level:raise ValueError('Template/difficulty mismatch')
 if field_type and TEMPLATES[template]['type']!=field_type:raise ValueError('Field type mismatch')
 if profile and not raw and profile not in {'method-derived','repaired:q-327811','source-method:'+template}:raise ValueError('Unknown profile')

 p=tuple(s.sympify(parameters[k]) for k in ['a','b','h','k']) if parameters else None
 for attempt in range(1000):
  if p is None:p=sample(template,rng)
  try:
   validate_parameters(template,p,raw)
   prompt,sol,bank=source_render(template,p,template) if template in Q else authored_render(template,p)
   if template in OPAQUE and not raw:
    bank=[expression_term('x',cx,hx)+('+' if cy>0 else '-')+expression_term('y',abs(cy),ky)+'=1' for cx,cy,hx,ky in normal_bank(p)]
   if template=='q-327811' and not raw:prompt=prompt.replace('⁡t','⁡\\theta ')
   # Source bank recipes remain default for defensible observed families.
   from sympy.parsing.sympy_parser import parse_expr
   exprs=[tex_expr(v.split('=')[0]) for v in bank]
   if any(s.simplify(exprs[i]-exprs[j])==0 for i in range(len(bank)) for j in range(i)):raise ValueError('Whole bank ambiguity')
   break
  except ValueError:
   if parameters:raise
   p=None
 else:raise ValueError('No eligible whole bank')
 kind=TEMPLATES[template]['type']; src=Q.get(template)
 fieldkey=src[':question/answer-fields'][0][':answer-field/key'] if src else 'selection'
 if src and (raw or template not in OPAQUE):correct_index=next(i for i,a in enumerate(src[':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==src[':question/answer-fields'][0][':answer-field/correct'][':answer/id'])
 else:correct_index=0
 identity=digest([VERSION,level,prompt,sol,sorted(bank),kind,fieldkey])
 fid=uid(identity+'/field/'+fieldkey)
 answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
 correct=answers[correct_index][':answer/id'];rng.shuffle(answers)
 question={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':fieldkey,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'template':template,'profile':profile or ('method-derived' if not src or template in OPAQUE else 'source-method:'+template), 'seed':seed,'parameters':dict(zip(['a','b','h','k'],map(str,p))),'source':{k:RAW[k] for k in ['database','basis','lineage']},'source_ids':[template] if src else [],'authored':not bool(src),'authored_bank':template in OPAQUE and not raw,'eligible_for_learning':not (template in OPAQUE and raw) and not (template=='q-327811' and raw),'evidence_only':(template in OPAQUE and raw) or (template=='q-327811' and raw),'mathematical_fingerprint':digest([('supplied-isolation' if level=='easy' else 'isolate'),str(s.expand((X-p[2])**2/p[0]**2+(Y-p[3])**2/p[1]**2-1))]),'content_identity':identity,'plot':{'rating':'none','assets':[]},'runtime':{'python':sys.version.split()[0],'sympy':s.__version__}}}

def tex_expr(tex):
 """Small independent displayed-expression reader; fractions and roots recurse."""
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 def group(text,i):
  assert text[i]=='{';depth=1;j=i+1
  while depth:
   if text[j]=='{':depth+=1
   if text[j]=='}':depth-=1
   j+=1
  return text[i+1:j-1],j
 def convert(text):
  out='';i=0
  while i<len(text):
   if text.startswith(r'\frac',i):
    n,j=group(text,i+5);d,i=group(text,j);out+='(('+convert(n)+')/('+convert(d)+'))'
   elif text.startswith(r'\sqrt',i):
    n,i=group(text,i+5);out+='sqrt('+convert(n)+')'
   else:
    c=text[i];out+= {'{':'(', '}':')','^':'**'}.get(c,c);i+=1
  return out
 return parse_expr(convert(tex),local_dict={'x':X,'y':Y,'C':s.Symbol('C'),'S':s.Symbol('S')},transformations=standard_transformations+(implicit_multiplication_application,))
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def render_plots(instance,output_dir=None):return {}
def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 text=q[':question/problem']+'\n\n'
 for a in f[':answer-field/choices']:text+=('- **Correct:** ' if a[':answer/id']==f[':answer-field/correct'][1] else '- ')+ '$'+a[':answer/value']+'$\n'
 return text+'\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n'.join('### '+('ORIGINAL SOURCE EVIDENCE / parameterized replay' if str(r['generation']['profile']).startswith('observed:') else 'GENERATED')+' — '+r['question'][':question/difficulty'].split('/')[-1]+('; authored level/template' if r['generation']['authored'] else '; observed level, '+('authored bank' if r['generation']['authored_bank'] else 'source-shaped template'))+'\n\n'+markdown(r) for r in records))
