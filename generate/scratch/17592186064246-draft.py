#!/usr/bin/env python3
"""Trigonometric indefinite integration by parts; immutable math basis 2275.

Backbone: one affine linear factor, one observed trig primitive, one application
of parts, then the source's reduction/primitive/collection sequence. Hard keeps
its observed csc² -> cot -> cos/sin -> log substitution. No repeated parts,
definite bounds, exponential operators or new method branches. Explicit and
sampled inputs obey the same workload bounds. Empirical whole banks reproduce
historical expressions without claiming to know historical error intent.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,random,re,sys,uuid
from functools import lru_cache
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
D=Path(__file__).with_suffix('')
spec=importlib.util.spec_from_file_location('kp64246_math_format',ROOT/'scripts/question_capture/math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
CAPTURE=json.loads((D/'source.json').read_text());KP=CAPTURE['record'];KP_ID=17592186064246
VERSION='trig-parts-draft-1';X=s.Symbol('x',real=True);A,B,K,H=s.symbols('a b k h',real=True)
Z=K*X+H;U=A*X+B;S=s.sin(Z);T=s.cos(Z);SC=s.sin(A*X);TC=s.cos(A*X)
# Each tuple is the complete ordered two-component expression, never a pool.
# Empirical banks deliberately retain all source terms, including opaque patterns.
BANK_PARTS={
'q-12564':[(X*S/K**2,T/K),(-S/K,X*T/K**2),(U*S/K,A*T/K**2),(U*S/K**2,T/K),(U*S/K,-X*T/K)],
'q-14437':[(-A*X*s.sin(X),s.cos(X)),(A*X*s.cos(X),-X*s.sin(X)),(TC,X*SC),(-X*s.cos(X),-TC),(-A*X*s.cos(X),A*s.sin(X))],
'q-14449':[(TC,X*SC),(-A*X*s.sin(X),s.cos(X)),(-X*s.cos(X),-TC),(-A*X*s.cos(X),A*s.sin(X)),(A*X*s.cos(X),-X*s.sin(X))],
'q-114297':[(K*S,X*T/(2*K)),(S,-X*T/K),(2*A*X*S/K,A*T/K**2),(A*X*S/K,A*T/K**2),(X*S/K,-T/K**2)],
'q-114299':[(A*X*S/K,A*T/K**2),((A+1)*X*S/2,T/K),(X*S/K,-T/2),(-S/K,X*T/(K+A)),(-S/(2*K),X*T/2)],
'q-114309':[(-U*T/K,A*S/K**2),(-3*U*T/K,S/(3*K)),(-U*T/(2*K),S/(2*K**2)),(-U*T/(3*K),-S/K),(-U*T/(2*K),-S/K)],
'q-114311':[(-U*T,A*S),(X*T,-A*B*S),(U*T,-S),(A*X*T,A**2*S),(-U*T,-A**2*S)],
'q-114312':[(X*S/(3*K),T/K),(S/K**2,X*T/K),(X*S/K,-2*T/K**2),(A*X*S/K,A*T/K**2),(2*S/K,-X*T/(3*K))],
'q-114314':[(U*s.tan(Z),-A*s.log(s.Abs(s.cos(Z)))),(-U*s.cot(Z),A*s.log(s.Abs(s.sin(Z)))),(-U*s.cot(Z),-2*A*s.log(s.Abs(s.cos(Z)))),(U*s.tan(Z),-2*A*s.log(s.Abs(s.sin(Z)))),(-2*U*s.cot(Z),-A*s.log(s.Abs(s.sin(Z))))],
'q-14453':[(-A*X*s.sin(X),A*s.cos(X)),(X*TC,X*SC),(X*TC,-X*SC),(-A*X*s.cos(X),-s.cos(X)),(A*X*s.sin(X),A*s.cos(X))],
'q-74087':[(A*X*S,T),(A*X*S/K,A*T/K**2),(A*X*S,-T/K**2),(A*X*S,T/K),(A*X*S/K,-T)],
'q-74088':[(S,T),(U*S,T/A),(A*S,A*T),(U*S,A*T),(U*S/A,T)],
'q-74090':[(X*S/A,-T),(A*X*S,T/A),(A*X*S,A*T),(A*S,-A*X*T),(A*S,-T)],
'q-12565':[(-K*X*s.cos(X+H)/K,K*s.sin(X+H)/K**2),(T/K,X*S/K**2),(-A*X*T/K,A*S/K**2),(X*T/K**2,-S/K),(X*T/K**2,2*S/K**2)],
'q-14451':[(X*T/K**2,-S/K**2),(-A*X*T/K,A*S/K**2),(s.cos(A*K*X)/K**2,X*s.sin(A*K*X)/K**2),(-X*T/K,S/K**2),(X*T/K**2,S/K)]}
# level, trig family, representative source, optional explicit primitive row.
TEMPLATES={
 'sin_unit':('easy','sin','q-14437',False),
 'cos_frequency':('easy','cos','q-114297',False),
 'cos_frequency_expanded':('easy','cos','q-114299',True),
 'cos_unit_expanded':('easy','cos','q-14453',True),
 'cos_unit':('easy','cos','q-74090',False),
 'sin_frequency':('easy','sin','q-14451',False),
 'affine_cos':('moderate','cos','q-12564',False),
 'affine_sin':('moderate','sin','q-114309',False),
 'affine_sin_unit':('moderate','sin','q-114311',False),
 'phase_cos':('moderate','cos','q-74087',False),
 'affine_cos_unit':('moderate','cos','q-74088',False),
 'phase_sin':('moderate','sin','q-12565',False),
 'csc_log':('hard','csc','q-114314',False)}
SOURCE_CASES=[
 ('q-12564','affine_cos',dict(a=1,b=3,k=3,h=0)),('q-14437','sin_unit',dict(a=2,b=0,k=1,h=0)),
 ('q-114297','cos_frequency',dict(a=3,b=0,k=3,h=0)),('q-114299','cos_frequency_expanded',dict(a=2,b=0,k=4,h=0)),
 ('q-114309','affine_sin',dict(a=1,b=4,k=2,h=0)),('q-114311','affine_sin_unit',dict(a=2,b=3,k=1,h=0)),
 ('q-114312','cos_frequency',dict(a=1,b=0,k=5,h=0)),('q-114314','csc_log',dict(a=1,b=0,k=1,h=0)),
 ('q-14449','sin_unit',dict(a=5,b=0,k=1,h=0)),('q-14453','cos_unit_expanded',dict(a=6,b=0,k=1,h=0)),
 ('q-74087','phase_cos',dict(a=2,b=0,k=2,h=8)),('q-74088','affine_cos_unit',dict(a=6,b=1,k=1,h=0)),
 ('q-74090','cos_unit',dict(a=10,b=0,k=1,h=0)),('q-12565','phase_sin',dict(a=1,b=0,k=3,h=5)),
 ('q-14451','sin_frequency',dict(a=2,b=0,k=2,h=0))]
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
CASES={sid:(name,p) for sid,name,p in SOURCE_CASES};MATH=re.compile(r'\$\$.*?\$\$|\$(?!\$).*?\$',re.S)
def tex(v):
 t=s.latex(v).replace(r'\left', '').replace(r'\right','').replace(r'\log',r'\ln')
 for f in ['sin','cos','tan','cot','csc']:t=t.replace('\\'+f,r'\operatorname{'+f+'}')
 return t

def tr(f,z):return r'\operatorname{'+f+'}('+tex(z)+')'
def coeff(c,t):
 c=s.Rational(c)
 if c==1:return t
 if c==-1:return '-'+t
 if c<0:return '-'+coeff(-c,t)
 if c.q==1:return str(c)+t
 return r'\frac{'+('' if c.p==1 else str(c.p))+t+'}{'+str(c.q)+'}'
def add(a,b):return a+('' if b.startswith('-') else '+')+b
def integral(body,var='x'):return r'\int '+body+r'\,\text{d}'+var
def aligned(rows,wrap_products=False,wrap_chain=False):
 if wrap_chain:
  lines=[rows[0][0]+'=',rows[0][1],*[left+'='+right for left,right in rows[1:]]]
  return '$$\n'+r'\begin{gathered}'+r' \\ '.join(lines)+r'\end{gathered}'+'\n$$'
 if wrap_products:
  # Centered continuation: one complete equality, broken immediately after =.
  # Keeping its two sides on separate visual lines avoids a wide shared column.
  lines=[rows[0][0]+'='+rows[0][1],rows[1][0]+'=',rows[1][1]]
  lines.extend(left+'='+right for left,right in rows[2:])
  return '$$\n'+r'\begin{gathered}'+r' \\ '.join(lines)+r'\end{gathered}'+'\n$$'
 return '$$\n'+r'\begin{aligned}'+r' \\ '.join(left+' & ='+right for left,right in rows)+r'\end{aligned}'+'\n$$'

def validate_parameters(name,p):
 if name not in TEMPLATES:raise ValueError('Unknown template')
 if set(p)!=set('abkh') or any(type(v)!=int for v in p.values()):raise ValueError('Exact integer a,b,k,h keys required')
 a,b,k,h=(p[t] for t in 'abkh');level,f,*_=TEMPLATES[name]
 if not 1<=a<=10 or not 1<=k<=5 or abs(b)>8 or abs(h)>8:raise ValueError('Coefficient/shift bounds exceeded')
 if level=='easy' and (b or h):raise ValueError('Easy has no affine or phase shift')
 if name in ['sin_unit','cos_unit','cos_unit_expanded','affine_sin_unit','affine_cos_unit'] and k!=1:raise ValueError('Unit-frequency template requires k=1')
 if name in ['cos_frequency','cos_frequency_expanded','sin_frequency'] and k==1:raise ValueError('Frequency template requires k=2..5')
 if level=='moderate':
  if name.startswith('affine') and (b==0 or h!=0):raise ValueError('Affine moderate requires nonzero b, h=0')
  if name.startswith('phase') and (b!=0 or h==0 or k==1):raise ValueError('Phase moderate requires nonzero h, b=0, k=2..5')
  # Same source-scale arithmetic: products and reduced final denominators bounded.
  if abs(a*b)>64 or k*k>25:raise ValueError('Coupled moderate arithmetic bound')
 if level=='hard' and (b!=0 or k!=1):raise ValueError('Hard retains monomial u and unit inner slope')
 # All coefficients actually used in the source-shaped reduction fit source ceilings.
 for q in [s.Rational(a,k),s.Rational(a,k*k)]:
  if abs(q.p)>10 or q.q>25:raise ValueError('Reduced by-parts coefficient exceeds source workload')

def sample(name,rng):
 level,f,*_=TEMPLATES[name]
 p=dict(a=rng.randint(1,10),b=0,k=1,h=0)
 if name in ['cos_frequency','cos_frequency_expanded','sin_frequency','affine_cos','affine_sin','phase_cos','phase_sin']:p['k']=rng.randint(2,5)
 if name.startswith('affine'):p['b']=rng.choice([n for n in range(-8,9) if n])
 if name.startswith('phase') or level=='hard':p['h']=rng.choice(list(range(-8,9))) if level=='hard' else rng.choice([n for n in range(-8,9) if n])
 return p

def mathdata(name,p):
 a,b,k,h=(s.Integer(p[t]) for t in 'abkh');u=a*X+b;z=k*X+h;f=TEMPLATES[name][1]
 if f=='cos':vp=s.cos(z);v=s.sin(z)/k;correct=u*v+a*s.cos(z)/k**2
 elif f=='sin':vp=s.sin(z);v=-s.cos(z)/k;correct=u*v+a*s.sin(z)/k**2
 else:vp=s.csc(z)**2;v=-s.cot(z);correct=-u*s.cot(z)+a*s.log(s.Abs(s.sin(z)))
 return u,z,vp,v,correct

def presentation(name,p,sid):
 """Replace complete math components in source prose; no short-string substitutions.
 All source prose and math-block order survive; math slots are recomputed, with
 equivalent consistent trig argument parentheses and fraction placement.
 """
 src=SOURCES[sid];a,b,k,h=(s.Integer(p[t]) for t in 'abkh');f=TEMPLATES[name][1];u,z,vp,v,correct=mathdata(name,p)
 ut=tex(u);uf='('+ut+')' if b else ut;zt=tex(z);ft=tr(f,z) if f!='csc' else r'\operatorname{csc}^{2}('+zt+')'
 integrand=uf+ft;it=integral(integrand)
 if f=='cos':vt=coeff(1/k,tr('sin',z));comp=tr('sin',z);first=coeff(1/k,uf+comp);redsign=-1;second=coeff(a/k**2,tr('cos',z));primitive=coeff(-1/k,tr('cos',z))
 elif f=='sin':vt=coeff(-1/k,tr('cos',z));comp=tr('cos',z);first=coeff(-1/k,uf+comp);redsign=1;second=coeff(a/k**2,tr('sin',z));primitive=coeff(1/k,tr('sin',z))
 else:vt='-'+tr('cot',z);first='-'+uf+tr('cot',z);comp=r'\frac{'+tr('cos',z)+'}{'+tr('sin',z)+'}';redsign=1;second=coeff(a,r'\ln|'+tr('sin',z)+'|');primitive=''
 reduction=add(first,coeff(redsign*a/k,integral(comp)))
 final=add(first,second)+'+C'
 defs='$$\n'+r'\begin{aligned}u='+ut+r'\, & ⟹\,{u}^{′}='+str(a)+r' \\ {v}^{′}='+ft+r'\, & ⟹\,v='+vt+'.'+r'\end{aligned}'+'\n$$'
 vpgroup='('+vt+')' if vt.startswith('-') or sid in ['q-114297','q-114312','q-74090'] else vt
 rows=[(integral(r'u{v}^{′}'),r'uv-\int v{u}^{′}\,\text{d}x'),(integral(uf+r'\cdot '+ft),uf+r'\cdot '+vpgroup+r'-\int '+vpgroup+r'\cdot '+str(a)+r'\,\text{d}x'+('' if f=='csc' else '.'))]
 endrows=[(it,reduction)]
 if f=='csc':
  rows.append(('',reduction+'.'))
  endrows += [('',add(first,coeff(a,integral(r'\frac{1}{u}','u')))),('',add(first,coeff(a,r'\ln|u|'))+'+C'),('',final)]
 else:
  if TEMPLATES[name][3]:
   # Preserve primitive evaluation before collection, not a duplicate CAS final.
   endrows.append(('',add(first,coeff(redsign*a/k,'('+primitive+')'))+'+C'))
  endrows.append(('',final))
 parts=[m[0] for m in MATH.finditer(src[':question/worked-solution'])]
 replace={0:'$$\n'+r'\int u{v}^{′}\,\text{d}x=uv-\int v{u}^{′}\,\text{d}x.'+'\n$$',1:'$'+it+'$',2:'$'+r'\int u{v}^{′}\,\text{d}x.$',3:defs,4:aligned(rows,wrap_products=True),len(parts)-1:aligned(endrows,wrap_chain=True)}
 if f=='csc':replace[5]='$u='+tr('sin',z)+',$';replace[6]='$'+r'\text{d}u='+tr('cos',z)+r'\,\text{d}x,$'
 idx=iter(range(len(parts)));worked=MATH.sub(lambda m:replace[next(idx)],src[':question/worked-solution'])
 oldmath=MATH.search(src[':question/problem'])[0];ending='=$' if oldmath.endswith('=$') else '.$'
 prompt=MATH.sub(lambda m:'$'+it+ending,src[':question/problem'],count=1)
 return prompt,worked,final

@lru_cache(maxsize=20000)
def primitive_equivalent(a,b):
 d=s.expand(s.diff((a-b).replace(s.Abs,lambda x:x),X))
 return d==0 or s.trigsimp(d,method='fu')==0

def bank(name,p,profile):
 u,z,vp,v,correct=mathdata(name,p);a=s.Integer(p['a']);k=s.Integer(p['k']);f=TEMPLATES[name][1]
 if profile.startswith('observed:'):
  sid=profile.split(':',1)[1]
  if sid not in CASES or CASES[sid][0]!=name:raise ValueError('Profile/template mismatch')
  subs={A:p['a'],B:p['b'],K:p['k'],H:p['h']};parts=[tuple(t.subs(subs) for t in row) for row in BANK_PARTS[sid]]
  eligible=False;origin='empirical complete-bank expressions; historical intent unresolved'
 elif profile=='authored:parts-errors':
  # Correct computed first. Four complete method errors: sign of residual,
  # omitted residual, sign of uv, using u instead of u′ in residual coefficient.
  residual=correct-u*v
  parts=[(u*v,residual),(u*v,-residual),(u*v,s.Integer(0)),(-u*v,residual),(u*v,residual*u/a)]
  eligible=True;origin='authored complete by-parts operation bank'
 else:raise ValueError('Unknown complete bank profile')
 vals=[s.Add(*r) for r in parts]
 # Exact differential comparison models arbitrary constants on regular intervals.
 def local(e):return e.replace(s.Abs,lambda x:x)
 def eq(a,b):return primitive_equivalent(a,b)
 if any(e.has(s.zoo,s.nan,s.oo,s.I) for e in vals):raise ValueError('Invalid whole bank')
 if sum(eq(e,correct) for e in vals)!=1 or any(eq(a,b) for i,a in enumerate(vals) for b in vals[i+1:]):raise ValueError('Ambiguous whole bank')
 return parts,vals,eligible,origin

def fingerprint(name,p):
 u,z,vp,v,c=mathdata(name,p)
 # Source labels, profile, style and option order do not define a mathematical task.
 return hashlib.sha256(s.srepr(s.expand(u)*vp).encode()).hexdigest()
def uid(kind,data):return str(uuid.uuid5(uuid.NAMESPACE_URL,kind+json.dumps(data,sort_keys=True,ensure_ascii=False)))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Only observed radio response contract supported')
 rng=random.Random(seed);eligible=[n for n,t in TEMPLATES.items() if t[0]==level]
 if profile and profile.startswith('observed:'):
  sid=profile.split(':',1)[1]
  if sid not in CASES:raise ValueError('Unknown observed profile')
  inferred=CASES[sid][0]
  if template is not None and template!=inferred:raise ValueError('Template/profile mismatch')
  template=inferred
 name=template or rng.choice(eligible)
 if name not in eligible:raise ValueError('Template/difficulty mismatch')
 # Select whole profile before any parameters; no first-valid subset selection.
 profile=profile or 'authored:parts-errors';sid=profile.split(':',1)[1] if profile.startswith('observed:') else TEMPLATES[name][2]
 for attempt in range(1000):
  p=dict(parameters) if parameters is not None else sample(name,rng)
  try:
   validate_parameters(name,p);parts,vals,learning,origin=bank(name,p,profile)
  except (ValueError,ZeroDivisionError):
   if parameters is not None:raise
   continue
  break
 else:raise ValueError('No eligible whole instance')
 prompt,worked,final=presentation(name,p,sid);prompt=fmt.normalize_prose(prompt);worked=fmt.normalize_prose(worked)
 # No answer CAS collapse changes the supplied whole-primitive +C contract.
 values=[fmt.normalize_tex(add(tex(a),tex(b))+'+C') for a,b in parts]
 u,z,vp,v,correct=mathdata(name,p)
 def eq(e):return primitive_equivalent(e,correct)
 ci=next(i for i,e in enumerate(vals) if eq(e))
 identity={'version':VERSION,'difficulty':level,'prompt':prompt,'solution':worked,'bank':sorted(values)};qid=uid('question',identity);fid=uid('field',[qid,'selection'])
 answers=[{':answer/id':uid('answer',[fid,value]),':answer/type':':answer.type/math',':answer/value':value} for value in values]
 ref=[':answer/id',answers[ci][':answer/id']];rng.shuffle(answers)
 record={'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':ref}]},'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':profile,'bank_origin':origin,'parameter_fingerprint':fingerprint(name,p),'eligible_for_learning':learning,'evidence_only':not learning,'source_reference':sid,'source_provenance':{k:CAPTURE[k] for k in ['database','basis','lineage']},'domains':'real x; hard: sin(x+h) nonzero, each connected interval','runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'plots':'none'}}
 fmt.validate_generated_record(record)
 for text in [prompt,worked,*values]:
  if any(ord(c)<32 and c not in '\n\t' for c in text):raise ValueError('C0 control character')
 return record

# Easy: one monomial factor and unshifted sin/cos; observed primitive/reduction.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: exactly one affine-linear or phase shift; observed same one-parts chain.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed csc², cot ratio and logarithmic substitution, no new trig branch.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
 return '\n\n'.join(['Level: '+q[':question/difficulty'].split('/')[-1]+'; template: '+g['template']+'; profile: '+g['bank_profile']+'; field type: radio',q[':question/problem'],'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices']),q.get(':question/worked-solution','*Raw source has no worked-solution key.*')])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
