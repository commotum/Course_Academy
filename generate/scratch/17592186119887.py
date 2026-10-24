#!/usr/bin/env python3
"""Fundamental vector product, immutable math basis 2275; local review only.

Easy vector tasks have at most one nonunit coordinate scale; moderate tasks
have exactly two, and hard tasks exactly three, with common nonunit band 2..4.
The observed easy norm family separately varies its already computed product. No new operators,
functions, geometric targets, normalization, or integration. These authored
labels are arithmetic policies, not recovered Math Academy levels.

The public observed:<source-id> profiles replay every original field and absence
at its anchor and apply a diagonal-coordinate recipe at changed parameters.
Opaque historical options are evidence-only; their error intent is unresolved.
Normal radio defaults use one complete method bank: ordered cross, reversed
cross, omitted j-cofactor sign, first tangent, second tangent. Norm defaults
supply the previously computed product and assess only its scalar magnitude.
Source layouts are parameterized expression masks, never literal-payload returns.
"""

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186119887-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, importlib.util, json, random, re, sys, uuid
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
HERE=Path(__file__).with_suffix(''); ROOT=HERE.parents[2]
SNAPSHOT=json.loads((HERE/'source.json').read_text()); REC=SNAPSHOT['record']
KP_ID=17592186119887; VERSION='fundamental-vector-product-draft-2'
GENERATOR_ID=str(uuid.uuid5(uuid.UUID(REC[':knowledge-point/id']), 'question-generator'))
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import normalize_prose, normalize_tex, validate_generated_record
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
TEMPLATES={q:'easy' for q in SOURCES}; CROSS=tuple(q for q in SOURCES if q!='q-167648')
TEMPLATES.update({'moderate:'+q:'moderate' for q in CROSS});TEMPLATES.update({'hard:'+q:'hard' for q in CROSS})
spec=importlib.util.spec_from_file_location('surface_display_parser',ROOT/'generate/runs/current/vector-math-parser.py');parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser)
u,v,x=parser.u,parser.v,parser.x;theta=sp.Symbol('theta',real=True)
def scalar(t):return parser.scalar(t.replace(r'\theta','t')).subs(parser.t,theta)
def vector(t):return sp.Matrix([scalar(s) for s in t.strip()[1:-1].replace(r'\,','').split(',')])
REGULARITY={'q-105606':'Singular exactly where cos(u)=0 and v=0; regular elsewhere', 'q-105607':'Singular exactly where v=u and 2u=cos(u); regular elsewhere','q-109904':'Regular for all real u,v','q-109909':'Regular for all real u,v','q-109911':'Singular exactly at u=v=0; regular elsewhere','q-109912':'Singular exactly where cos(u)=cos(v)=0; regular elsewhere','q-167648':'Regular for 0<x<=1; x=0 is a singular boundary, with algebraic norm still valid'}
BASE={
'q-105606':sp.Matrix([sp.sin(u),v**2,4*v*sp.cos(u)]),
'q-105607':sp.Matrix([u+v,v**2+sp.sin(u),u*v]),
'q-109904':sp.Matrix([u,v,u**2-v**2]),
'q-109909':sp.Matrix([u,v,u-sp.exp(v)]),
'q-109911':sp.Matrix([u**2+1,v**3+1,2*u+v]),
'q-109912':sp.Matrix([u,u*sp.sin(v),v*sp.cos(u)]),
'q-167648':sp.Matrix([x,2*x**2*sp.cos(theta),2*x**2*sp.sin(theta)])}
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(z):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+z))
def tex(z):return sp.latex(z).replace(r'\left','').replace(r'\right','')
def vec(z):return '⟨'+r'\,'.join([])+r',\,'.join(tex(t) for t in z)+'⟩'
def multiply(t,k):
 """A complete scalar slot; unit scale preserves exact source spelling."""
 if k==1 or scalar(t)==0:return t
 return str(k)+r'\left('+t+r'\right)'
def vec_scale(t,scales,expanded=False):
 parts=re.split(r'(?<!\\),',t[1:-1]);assert len(parts)==3
 # Retain each source's exact comma spacing and TeX fragments at unit parameters.
 out=[]
 for part,k in zip(parts,scales):
  prefix=re.match(r'(?:\s|\\,)*',part)[0];body=part[len(prefix):]
  if expanded and k!=1 and scalar(body)!=0:
   # Keep the source norm common-factor stage, while collecting its changed
   # leading coefficient; all other evaluated vectors distribute actual scales.
   if '({cos}^{2}' in body:
    m=re.match(r'(-?\d+)(.*)',body);assert m;value=str(int(m[1])*k)+m[2]
   else:value=tex(sp.expand(k*scalar(body)))
  else:value=multiply(body,k)
  out.append(prefix+value)
 return '⟨'+','.join(out)+'⟩'
def derivative_vec(t,scales):
 parts=re.split(r'(?<!\\),',t[1:-1]);out=[]
 for part,k in zip(parts,scales):
  m=re.search(r'(\\frac\{∂\}\{∂(?:u|v|x|\\theta )\}\()(.*)(\))',part)
  assert m,part
  out.append(part[:m.start()]+m[1]+multiply(m[2],k)+m[3]+part[m.end():])
 return '⟨'+','.join(out)+'⟩'
def matrices(text,scales):
 # Every determinant has derivative vectors as rows and coordinate columns.
 pat=r'\\begin\{aligned\}([^{}]*(?:\{[^{}]*\}[^{}]*)*)\\end\{aligned\}'
 # Scan innermost aligned blocks instead of assuming a flat regex grammar.
 spans=[];stack=[]
 for m in re.finditer(r'\\(?:begin|end)\{aligned\}',text):
  if m[0].startswith(r'\begin'):stack.append(m)
  else:
   begin=stack.pop();inside=text[begin.end():m.start()]
   if r'\begin{aligned}' not in inside and '=' not in inside and ' & ' in inside:spans.append((begin.end(),m.start(),inside))
 out=text
 # All three 2x2 cofactor matrices occur left-to-right, then 3x3 separately.
 minors=[s for s in spans if len(s[2].split(r' \\ '))==2]
 index={a:i for i,(a,b,z) in enumerate(sorted(minors))}
 for a,b,z in sorted(spans,reverse=True):
  rows=z.split(r' \\ ')
  if len(rows)==3:
   cols=(0,1,2);start=1
  else:cols=((1,2),(0,2),(0,1))[index[a]%3];start=0
  for j in range(start,len(rows)):
   cells=rows[j].split(' & ');assert len(cells)==len(cols)
   rows[j]=' & '.join(multiply(t,scales[col]) for t,col in zip(cells,cols))
  out=out[:a]+r' \\ '.join(rows)+out[b:]
 return out

def transform_solution(base,scales):
 source=SOURCES[base].get(':question/worked-solution')
 if source is None:return None
 co=(scales[1]*scales[2],scales[0]*scales[2],scales[0]*scales[1])
 spans=list(re.finditer('⟨[^⟨⟩]*⟩',source));eval_count=0; replacements=[]
 for m in spans:
  t=m[0]
  if r'\begin{aligned}' in t:continue # handled by determinant cell masks
  if r'\frac{∂x}' in t:continue # formal coordinate partials
  if r'\frac{∂}' in t:out=derivative_vec(t,scales)
  else:
   # Before derivative blocks: surface vector. After those blocks: cofactor result.
   before=source[:m.start()]
   if 'We first compute' not in before:out=vec_scale(t,scales)
   elif 'Therefore, the fundamental' not in before:out=vec_scale(t,scales,expanded=True)
   else:out=vec_scale(t,co,expanded=True)
  replacements.append((m.start(),m.end(),out))
 out=source
 for a,b,z in reversed(replacements):out=out[:a]+z+out[b:]
 out=matrices(out,scales)
 if base=='q-167648':
  # The scalar magnitude stages are separately parameterized: no vector-component
  # equivalence substitute is used for a scalar norm.
  norm=norm_solution(scales[0],scales[1],exact=True)
  out=out[:out.index('Finally, the corresponding norm is')]+norm
 return out

def transform_prompt(base,scales):
 t=SOURCES[base][':question/problem']
 if base=='q-167648':return t # faithful context-dependent original layout
 if '⟨' in t:
  m=re.search('⟨[^⟨⟩]*⟩',t);return t[:m.start()]+vec_scale(m[0],scales)+t[m.end():]
 # Whole coordinate RHS slots, never isolated variable-letter replacements.
 pat=r'([xyz])(\s*=\s*)(.*?)(?=,|\.|\$)'
 count=0
 def repl(m):
  nonlocal count
  k=scales['xyz'.index(m[1])];count+=1
  return m[1]+m[2]+multiply(m[3],k)
 t=re.sub(pat,repl,t);assert count==3,(base,t,count)
 return t

def norm_answer(a,b):return str(2*b)+r'{x}^{2}\sqrt{'+str(16*b*b)+r'{x}^{2}+'+str(a*a)+'}'

def norm_solution(a,b,exact=False):
 source=SOURCES['q-167648'][':question/worked-solution'];part=source[source.index('Finally, the corresponding norm is'):]
 # Exact source stage strings become scalar expression masks. The common factor
 # x^2 is nonnegative for all real x; sqrt(x^4)=x^2, never x or |x|.
 rhs=part.split(r' & =')[1:]; rows=[t.split(r' \\')[0].split(r'.\end')[0] for t in rhs]
 A=8*b*b;B=2*a*b
 values=[rf'\sqrt{{({A}{{x}}^{{3}})^{{2}}+(-{B}{{x}}^{{2}}\operatorname{{cos}}⁡\theta )^{{2}}+(-{B}{{x}}^{{2}}\operatorname{{sin}}⁡\theta )^{{2}}}}',
 rf'\sqrt{{{A*A}{{x}}^{{6}}+{B*B}{{x}}^{{4}}{{cos}}^{{2}}⁡\theta +{B*B}{{x}}^{{4}}{{sin}}^{{2}}⁡\theta }}',
 rf'\sqrt{{{A*A}{{x}}^{{6}}+{B*B}{{x}}^{{4}}({{cos}}^{{2}}⁡\theta +{{sin}}^{{2}}⁡\theta )}}',
 rf'\sqrt{{{A*A}{{x}}^{{6}}+{B*B}{{x}}^{{4}}}}',
 norm_answer(a,b)]
 for old,new in reversed(list(zip(rows,values))):
  # Work with full unique rows; no overlapping numeric token replacement.
  part=part.replace(old,new,1)
 return part

def authored_solution(surface,du,dv,cross,base):
 """Missing source q-105607: canonical formal/substitution/cofactor stages."""
 opening=r'For a surface with parametrization $r(u,v),$ the fundamental vector product is defined as ${r}_{u}^{′}\times {r}_{v}^{′}.$'
 formal=lambda t:rf'⟨\frac{{∂x}}{{∂{t}}},\,\frac{{∂y}}{{∂{t}}},\,\frac{{∂z}}{{∂{t}}}⟩'
 sub=lambda t:'⟨'+r',\,'.join(rf'\frac{{∂}}{{∂{t}}}({tex(z)})' for z in surface)+'⟩'
 sol=opening+'\n\nIn vector form, our surface has the equation \n\n$$\nr(u,v)='+vec(surface)+'.\n$$\n\nWe first compute the tangent vectors to the grid curves:\n\n$$\n'
 sol+=r'\begin{aligned}{r}_{u}^{′} & ='+formal('u')+r' \\  & ='+sub('u')+r' \\  & ='+vec(du)+r' \\ {r}_{v}^{′} & ='+formal('v')+r' \\  & ='+sub('v')+r' \\  & ='+vec(dv)+r'\end{aligned}'+'\n$$\n\nTherefore, the fundamental vector product is\n\n$$\n'
 matrix=r'|\begin{aligned}i & j & k \\ '+ ' & '.join(tex(z) for z in du)+r' \\ '+' & '.join(tex(z) for z in dv)+r'\end{aligned}|'
 minors=[]
 for i,(j,k) in enumerate(((1,2),(0,2),(0,1))):
  minors.append(('-' if i==1 else '')+r'|\begin{aligned}'+tex(du[j])+' & '+tex(du[k])+r' \\ '+tex(dv[j])+' & '+tex(dv[k])+r'\end{aligned}|')
 # Keep unevaluated two determinant products, including the outside minus on j.
 products=[rf'({tex(du[1])})({tex(dv[2])})-({tex(du[2])})({tex(dv[1])})',rf'-[({tex(du[0])})({tex(dv[2])})-({tex(du[2])})({tex(dv[0])})]',rf'({tex(du[0])})({tex(dv[1])})-({tex(du[1])})({tex(dv[0])})']
 sol+=r'\begin{aligned}{r}_{u}^{′}\times {r}_{v}^{′} & ='+matrix+r' \\  & =⟨'+r',\,'.join(minors)+'⟩'+r' \\  & =⟨'+r',\,'.join(products)+'⟩'+r' \\  & ='+vec(cross)+r'.\end{aligned}'+'\n$$'
 return sol

def parameter_domain(level,base,observed=False):
 """Finite assessed domains; evidence is exempt from authored level design.

 The norm is an observed easy scalar task supplied with its prior product, not a
 vector-partial task; a,b range 1..4 with c=b. Vector defaults share scales 1..4
 and distinguish exactly the number of independently nonunit coordinate scales.
 """
 import itertools
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if base=='q-167648':
  if level!='easy':raise ValueError('Existing norm remains easy')
  return tuple({'a':a,'b':b,'c':b} for a,b in itertools.product(range(1,5),repeat=2))
 def eligible(values):
  count=sum(z!=1 for z in values)
  return observed or (count<=1 if level=='easy' else count==2 if level=='moderate' else count==3)
 return tuple(dict(zip(('a','b','c'),values)) for values in itertools.product(range(1,5),repeat=3) if eligible(values))

def parameters_for(level,base,rng,parameters,observed=False):
 domain=parameter_domain(level,base,observed)
 p=dict(rng.choice(domain)) if parameters is None else dict(parameters)
 if base=='q-167648' and 'c' not in p and 'b' in p:p['c']=p['b']
 if set(p)!={'a','b','c'} or any(type(z)!=int for z in p.values()) or p not in domain:
  raise ValueError('Coordinate scales violate bounded domain or level bookkeeping count')
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 rng=random.Random(seed)
 choices=[t for t,l in TEMPLATES.items() if l==level and (field_type is None or (field_type.split('/')[-1]=='blank')==(t=='q-167648'))]
 if template is None:
  if profile=='norm:supplied-product':template='q-167648'
  elif profile and profile.startswith('observed:'):template=profile.split(':',1)[1]
  else:
   if not choices:raise ValueError('No eligible template/field type')
   template=rng.choice(choices)
 if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('Template level mismatch')
 base=template.split(':')[-1]
 if field_type is not None and (field_type.split('/')[-1]=='blank')!=(base=='q-167648'):raise ValueError('Explicit template/field contract mismatch')
 observed=profile is not None and profile.startswith('observed:')
 p=parameters_for(level,base,rng,parameters,observed);scales=(p['a'],p['b'],p['c'])
 if observed and profile!='observed:'+base:raise ValueError('Observed bank mismatch')
 if observed and level!='easy':raise ValueError('Raw evidence keeps observed labels')
 if profile is None:profile='norm:supplied-product' if base=='q-167648' else 'method:ordered-cross'
 if not observed and profile not in ('method:ordered-cross','norm:supplied-product'):raise ValueError('Unknown complete profile')
 if (profile=='norm:supplied-product')!=(base=='q-167648') and not observed:raise ValueError('Profile shape')
 surface=sp.diag(*scales)*BASE[base];s,t=(x,theta) if base=='q-167648' else (u,v)
 du=surface.diff(s);dv=surface.diff(t);cross=du.cross(dv).applyfunc(sp.expand);cross=cross.applyfunc(sp.trigsimp) if base=='q-167648' else cross;norm=sp.simplify(sp.sqrt(sp.trigsimp(cross.dot(cross)))) if base=='q-167648' else None
 prompt=transform_prompt(base,scales);solution=transform_solution(base,scales)
 if base=='q-105607' and not observed:solution=authored_solution(surface,du,dv,cross,base)
 if base=='q-167648' and not observed:
  prompt='The fundamental vector product computed in the preceding step is\n\n$$\n{r}_{x}^{′}'+r'\times {r}_{\theta }^{′}='+vec(cross)+r',\quad x\in[0,1],\quad\theta\in[0,2\pi).'+ '\n$$\n\nFind its norm.\n\n'+r'$‖{r}_{x}^{′}\times {r}_{\theta }^{′}‖=$ {{field-1}}'
  solution=norm_solution(p['a'],p['b'])
 fields=[];co=(p['b']*p['c'],p['a']*p['c'],p['a']*p['b'])
 if observed:
  for sf in SOURCES[base][':question/answer-fields']:
   vals=[norm_answer(p['a'],p['b']) if base=='q-167648' else a[':answer/value'] for a in sf[':answer-field/choices']]
   if base!='q-167648':vals=[vec_scale(z,co) for z in vals]
   correct=None
   if ':answer-field/correct' in sf:
    old=sf[':answer-field/correct'][':answer/id'];correct=next(i for i,a in enumerate(sf[':answer-field/choices']) if a[':answer/id']==old)
   fields.append((sf[':answer-field/key'],sf[':answer-field/type'][':db/ident'],vals,correct))
 elif base=='q-167648':fields=[('field-1',':answer-field.type/blank',[tex(norm)],0)]
 else:
  values=[cross,-cross,sp.Matrix([cross[0],-cross[1],cross[2]]),du,dv]
  if any(all(sp.expand(z)==0 for z in a-b) for i,a in enumerate(values) for b in values[:i]):raise ValueError('Whole method bank collides')
  fields=[('selection',':answer-field.type/radio',[vec(z) for z in values],0)]
 # Mathematical identity excludes offsets annihilated by derivatives, answer banks,
 # aliases, seed and order; norm uses its actual supplied product up to sign aliases.
 fp=digest(['supplied-product-norm' if base=='q-167648' else 'partial-cross', [sp.srepr(z) for z in (cross if base=='q-167648' else list(du)+list(dv))]])
 if not observed:
  prompt=normalize_prose(prompt);solution=normalize_prose(solution)
  fields=[(k,t,[normalize_tex(z) for z in vals],correct) for k,t,vals,correct in fields]
 content=digest([VERSION,level if not observed else SOURCES[base].get(':question/difficulty'),prompt,solution,[[k,t,sorted(vals),correct is not None] for k,t,vals,correct in fields]])
 outfields=[]
 for fi,(key,typ,vals,correct) in enumerate(fields):
  fid=uid(content+':field:'+str(fi));ans=[{':answer/id':uid(fid+':'+z),':answer/type':':answer.type/math',':answer/value':z} for z in vals]
  f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':typ,':answer-field/choices':ans}
  if correct is not None:f[':answer-field/correct']=[':answer/id',ans[correct][':answer/id']]
  if not observed and typ.endswith('/radio'):rng.shuffle(ans)
  outfields.append(f)
 q={':question/id':uid(content),':question/problem':prompt,':question/answer-fields':outfields}
 if solution is not None:q[':question/worked-solution']=solution
 if not observed or ':question/difficulty' in SOURCES[base]:q[':question/difficulty']=':question.difficulty/'+level
 return {'knowledge_point':{'db_id':KP_ID,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source_ids':[base],'source':{k:SNAPSHOT[k] for k in ('database','basis','lineage')},'evidence_only':observed,'eligible_for_learning':not observed,'domains':{'variables':'real','regularity':REGULARITY[base],'norm_context':'Recovered r=<x,2x² cos theta,2x² sin theta> from full captured original worked solution; no inference from scalar answer'},'bookkeeping_nonunit_coordinates':sum(z!=1 for z in scales),'authored_difficulty_uncertainty':'Number of nonunit coordinate scales is a conservative coefficient-bookkeeping policy, not recovered MA difficulty evidence; observed easy norms have their own supplied-product workload','mathematical_fingerprint':fp,'content_hash':content,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':{'rating':'none','references':[]},'grading_limitations':(['Native rules accept canonical and reordered factored norms but cannot establish uncollected square-root equivalence; recorded as unresolved'] if base=='q-167648' else []),'recipe_interpretation':('Complete observed bank diagonal-coordinate covariance; source error intent opaque, evidence only' if observed else 'cross; reversed operands; omit negative middle cofactor; first tangent; second tangent' if base!='q-167648' else 'Euclidean scalar norm of supplied product'), 'calculator_policy':'unknown in captured EDB; two local widgets have empty instruction blocks, not an inferred general prohibition'}}

# EASY: vector tasks have zero/one nonunit scales; observed norm workload is separate.
_generate=generate
def generate(*args,**kwargs):
 record=_generate(*args,**kwargs)
 if record['generation']['eligible_for_learning']:validate_generated_record(record)
 return record
def generate_easy(seed=0,**kwargs):return generate('easy',seed=seed,**kwargs)
# MODERATE: exactly two nonunit coordinate scales in 2..4; same fixed six partials.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed=seed,**kwargs)
# HARD: exactly three nonunit scales in 2..4; same cofactor stages, no new calculus.
def generate_hard(seed=0,**kwargs):return generate('hard',seed=seed,**kwargs)
def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  s+='Field '+f[':answer-field/key']+' ('+f[':answer-field/type']+')\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'
 return s+q.get(':question/worked-solution','[No captured worked solution]')

from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186119887-source-policy.json'))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template');p.add_argument('--profile');p.add_argument('--parameters',type=json.loads);a=p.parse_args()
 rows=[generate(l,a.seed+i,a.template,parameters=a.parameters,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(rows,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
