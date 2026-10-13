#!/usr/bin/env python3
"""Triple integral change-of-variables SETUP only, frozen draft v1.

Read-only snapshot: math basis1356. Five raw evidence profiles preserve absent
attributes and faulty mathematics; these are explicitly ineligible for learning.
Normal easy serves every observed family with independent method-derived banks;
moderate follows canonical variable Jacobian/product cancellation; hard follows
the observed square-root coordinate with a dependent limit. No integral evaluation
is requested. Full integrals are checked for value ambiguity before publication.
All APIs accept explicit parameters without silent mutation. No database writes.
"""
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/'17592186198397'
VERSION='triple-setup-1'
CAPTURE=json.loads((EVIDENCE/'source.json').read_text())
KP=CAPTURE['record']; KP_ID=KP[':db/id']
X,Y,Z=s.symbols('x y z', real=True)
U,V,W=s.symbols('u v w', real=True)
SOURCE_QUESTIONS=KP[':knowledge-point/questions']
FAMILIES={'easy':('exp','log','cos2','sin'), 'moderate':('product',), 'hard':('sqrt',)}
TEMPLATES={a:level for level,aa in FAMILIES.items() for a in aa}
RAW_TEMPLATES=json.loads((EVIDENCE/'raw-templates.json').read_text()) if (EVIDENCE/'raw-templates.json').exists() else {}

def tex(e):return s.latex(s.sympify(e)).replace(r'\log',r'\ln')
def block(e):return '\n\n$$\n'+e+'\n$$'
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,str(v)))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def matrix(m):return r'\begin{vmatrix}'+r'\\'.join(' & '.join(tex(v) for v in row) for row in m.tolist())+r'\end{vmatrix}'
def repeated(e,b):
 return ''.join(r'\int_{'+tex(lo)+'}^{'+tex(hi)+'}' for lo,hi in b)+r'\left('+tex(e)+r'\right)\,dw\,dv\,du'
def normalize(v):
 if isinstance(v,dict):
  if ':db/ident' in v:return v[':db/ident']
  return {k:normalize(x) for k,x in v.items() if k not in (':db/id', ':question/math-academy-id')}
 if isinstance(v,list):return [normalize(x) for x in v]
 return v

def raw_generate(template,p,seed):
 """Public opaque evidence replay: compiled component masks, no source payload return.

 Each primitive source component is a scale slot, with exact spelling at scale1.
 Whole displayed integrands/banks scale together, not arbitrary fitted errors.
 Region-height slots are incidental; source anomalies remain explicitly visible.
 """
 spec=RAW_TEMPLATES[template]; scale=s.Rational(str(p.get('scale',1)))
 height=p.get('height',spec['height'])
 if type(height)!=int:raise ValueError('raw height must be exact integer')
 if set(p)!={'scale','height'} or height!=spec['height'] or not 1<=scale<=4:raise ValueError('raw scale1..4; captured fixed height required')
 def render(mask):
  out=mask.replace('@@HEIGHT@@',str(height))
  for key,value in spec['components'].items():
   comp=value if scale==1 else tex(scale)+r'\left('+value+r'\right)'
   out=out.replace('@@'+key+'@@',comp)
  return out
 q={':question/problem':render(spec['problem'])}
 if 'solution' in spec:q[':question/worked-solution']=render(spec['solution'])
 if 'difficulty' in spec:q[':question/difficulty']=spec['difficulty']
 vals=[render(a) for a in spec['answers']]
 correct=spec.get('correct_index')
 f={':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio'}
 return finish(q,f,vals,correct,template,p,'raw',seed,evidence_only=True)

def parameters(level,template,rng):
 if template in ('exp','sin','log','cos2'):
  a=rng.choice((2,3,4,5));c=rng.choice((1,2,3,4));h=rng.choice((2,3,4,5))
  return {'a':a,'c':c,'height':h}
 if template=='product':
  return {'a':rng.choice((2,3,4)),'c':rng.choice((1,2,3,4)), 'd':rng.choice((1,2,3,4)), 'sign':rng.choice((-1,1)), 'height':rng.choice((1,2,3))}
 return {'a':rng.choice((1,2,3)), 'c':rng.choice((1,2,3,4)), 'upper':rng.choice((2,3,4))}

def derive(level,t,p):
 """Independent exact model; domain guards also apply to explicit API inputs."""
 required={'easy':{'a','c','height'},'moderate':{'a','c','d','sign','height'},'hard':{'a','c','upper'}}[level]
 if set(p)!=required:raise ValueError('Expected parameters '+str(sorted(required)))
 if any(type(v)!=int for v in p.values()):raise ValueError('integer parameters required')
 if not 1<=p['c']<=4:raise ValueError('c1..4')
 if level=='easy' and (not 2<=p['a']<=5 or not 2<=p['height']<=5):raise ValueError('easy a2..5, height2..5')
 if level=='moderate' and (not 2<=p['a']<=4 or not 1<=p['d']<=4 or p['sign'] not in (-1,1) or not 1<=p['height']<=3):raise ValueError('moderate bounds')
 if level=='hard' and (not 1<=p['a']<=3 or not 2<=p['upper']<=4):raise ValueError('hard bounds')
 a,c=p['a'],p['c']
 if t=='exp':
  coords=(X+a*Y,Y-X,Z);inv=((U-a*V)/(a+1),(U+V)/(a+1),W)
  f=c*(X+a*Y)*s.exp(Y-X);bounds=((1,2),(0,1),(0,p['height']))
 elif t=='sin':
  coords=(a*X+Y,Y+Z,Z);inv=((U-V+W)/a,V-W,W)
  f=c*s.sin(a*X+Y)*s.cos(Y+Z);bounds=((3*s.pi/4,s.pi),(0,s.pi/2),(-1,p['height']))
 elif t=='log':
  coords=(X**2+Y,a*X+Z,Z);inv=((V-W)/a,U-((V-W)/a)**2,W)
  f=c*(a*X+Z)*s.log(X**2+Y);bounds=((1,2),(-1,a+4),(1,p['height']))
 elif t=='cos2':
  coords=(X+a*Y,Z-a*Y,Z);inv=(U+V-W,(W-V)/a,W)
  f=c*s.cos(X+Z)**2*s.cos(Z-a*Y);bounds=((0,s.pi/2),(0,s.pi/2),(0,p['height']))
 elif t=='product':
  coords=(X*Y,Y,a*Z);inv=(U/V,V,W/a)
  f=c*X*Y**2+p['d']*Y*Z
  bounds=((1,2),(1,2) if p['sign']==1 else (-2,-1),(0,a*p['height']))
 elif t=='sqrt':
  coords=(X+a*Y,X-a*Y,s.sqrt(Z));inv=((U+V)/2,(U-V)/(2*a),W**2)
  f=c*s.sqrt(Z);bounds=((1,p['upper']),(1,p['upper']),(1,s.sqrt(U*V)))
 else:raise ValueError(t)
 J=s.Matrix(coords).jacobian((X,Y,Z));det=s.factor(J.det());dnew=s.simplify(det.subs(dict(zip((X,Y,Z),inv))))
 # z>0 and w>0 in sqrt region; y has a fixed explicit branch in product.
 if t=='sqrt':dnew=-a/W
 jd=s.simplify(1/dnew)
 if t=='product':absjd=s.Integer(p['sign'])/(a*V)
 elif t=='sqrt':absjd=W/a
 else:absjd=s.Abs(jd)
 transformed=s.simplify(f.subs(dict(zip((X,Y,Z),inv))))
 if t=='sqrt':transformed=c*W
 g=s.simplify(transformed*absjd)
 return coords,inv,f,bounds,J,det,dnew,jd,absjd,transformed,g

def bank(t,p,m):
 coords,inv,f,b,J,det,dn,jd,ab,ft,g=m;a,c=p['a'],p['c']
 if t=='exp':values=(g,ft,g.subs({U:V,V:U},simultaneous=True),c*s.exp(V)/(a+1),c*s.exp(U)/(a+1))
 elif t=='sin':values=(g,ft,ft*a, c*s.sin(V)*s.cos(U)/a,c*s.sin(U)*s.sin(V)/a)
 elif t=='log':values=(g,ft,ft*a,c*U*s.log(U)/a,-g)
 elif t=='cos2':values=(g,ft,ft*a,c*s.cos(U-V)**2*s.cos(V)/a,c*s.cos(U)**2*s.cos(V)/a)
 elif t=='product':values=(g,ft,s.simplify(ft*s.Integer(p['sign'])*a*V),s.simplify((c*U+p['d']*V*W/a)*ab),s.simplify((c*U*V+p['d']*V*W)*ab))
 else:
  # Whole-bank setup errors from coordinate/Jacobian/bound operations.
  return [(g,b),(ft,b),(g,((1,p['upper']),(1,p['upper']),(1,U*V))), (g,((1,p['upper']),(1,p['upper']),(1,s.sqrt(U+V)))), (c*W/(2*a),b)]
 return [(s.simplify(v),b) for v in values]

def unambiguous(options,whole):
 if not whole:
  return all(s.simplify(options[i][0]-options[j][0])!=0 for i in range(5) for j in range(i))
 # Complete integral values matter, including different displayed bounds.
 vals=[]
 for e,b in options:
  vals.append(s.simplify(s.integrate(s.integrate(s.integrate(e,(W,*b[2])),(V,*b[1])),(U,*b[0]))))
 return all(s.simplify(vals[i]-vals[j])!=0 for i in range(5) for j in range(i))

def normal_question(level,t,p,m):
 coords,inv,f,b,J,det,dn,jd,ab,ft,g=m
 a=p['a']
 cv=',\\quad '.join(tex(v)+'='+tex(e) for v,e in zip((U,V,W),coords))
 if t=='log':region=((1,2,coords[0]),(-1,a+4,coords[1]),(1,p['height'],Z))
 elif t=='sqrt':region=((1,p['upper'],coords[0]),(1,p['upper'],coords[1]),(1,coords[0]*coords[1],Z))
 elif t=='product':region=((1,2,coords[0]),(*b[1],Y),(0,p['height'],Z))
 else:region=tuple((lo,hi,e) for (lo,hi),e in zip(b,coords))
 rtex=r'R=\{(x,y,z): '+',\\quad '.join(tex(lo)+r'\le '+tex(e)+r'\le '+tex(hi) for lo,hi,e in region)+r'\}.'
 whole=level!='easy'
 prompt='Consider the finite region $R$ in the $xyz$-space, given by'+block(rtex)+'\n\nGiven the change of variables'+block(cv+',')
 if whole:prompt+='\n\nWrite the triple integral'+block(r'\iiint_R '+tex(f)+r'\,dV')+'\n\nas a repeated integral in terms of $u$, $v$, and $w$.'
 else:prompt+='\n\nWhich of the following could be the missing part of the expression below?'+block(r'\iiint_R '+tex(f)+r'\,dV='+repeated(s.Symbol('MISSING'),b).replace('MISSING',r'\boxed{?}'))
 solution="Let's define a transformation $T$ as follows:"+block(r'T:(u,v,w)\longmapsto (x(u,v,w),y(u,v,w),z(u,v,w)).')
 solution+='\n\nThis transformation maps some region $Δ$ in the $uvw$-space to our region $R$ in the $xyz$-space.\n\nTo find the required integral, we can use the change of variables formula'+block(r'\iiint_R f(x,y,z)\,dV=\iiint_Δ f(x(u,v,w),y(u,v,w),z(u,v,w))\left|\frac{\partial(x,y,z)}{\partial(u,v,w)}\right|\,du\,dv\,dw')
 solution+='\n\nwhere $\\frac{∂(x,y,z)}{∂(u,v,w)}$ is the Jacobian determinant corresponding to $T.$\n\nNote that the change of variables'+block(cv)+'\n\ngives us the *inverse* function ${T}^{-1}$.'+block(r'T^{-1}:(x,y,z)\longmapsto (u(x,y,z),v(x,y,z),w(x,y,z)).')
 solution+='\n\nTo find the required integral, we proceed in four steps:\n\n**Step 1**: Find $Δ,$ which is the image of $R$ under the action of ${T}^{-1}.$\n\nOur domain in the $uvw$-space is'+block(r'Δ=\{(u,v,w): '+',\\quad '.join(tex(lo)+r'\le '+tex(v)+r'\le '+tex(hi) for v,(lo,hi) in zip((U,V,W),b))+r'\}.')
 solution+='\n\n**Step 2**: Compute the Jacobian determinant corresponding to ${T}^{-1}:$\n\nThe Jacobian determinant corresponding to ${T}^{-1}$ is'
 symbols=s.Matrix(3,3,lambda i,j:s.Symbol('D'+str(i)+str(j)))
 formal=r'\begin{vmatrix}'+r'\\'.join(' & '.join(r'\frac{\partial '+tex(v)+r'}{\partial '+tex(x)+r'}' for x in (X,Y,Z)) for v in (U,V,W))+r'\end{vmatrix}'
 # Full first-row expansion including all three minors and signed factors.
 minor_terms=[]
 for j in range(3):minor_terms.append('('+tex(J[0,j])+')'+matrix(J.minor_submatrix(0,j)))
 expansion=minor_terms[0]+'-'+minor_terms[1]+'+'+minor_terms[2]
 solution+=block(r'\begin{aligned}\frac{∂(u,v,w)}{∂(x,y,z)} &='+formal+r'\\ &='+matrix(J)+r'\\ &='+expansion+r'\\ &='+tex(det)+r'\\ &='+tex(dn)+r'.\end{aligned}')
 solution+='\n\n**Step 3**: Compute the Jacobian determinant corresponding to $T:$\n\nThe Jacobian determinant corresponding to $T$ is'+block(r'\frac{∂(x,y,z)}{∂(u,v,w)}=\left(\frac{∂(u,v,w)}{∂(x,y,z)}\right)^{-1}='+tex(jd)+'.')
 solution+='\n\nNote that $\\frac{∂(x,y,z)}{∂(u,v,w)}\\ne 0$ everywhere inside $Δ.$ In other words, $T$ has no critical points inside $Δ.$'
 if t=='sqrt':solution+=' Since $z\\ge1$ and $w=\\sqrt z$, the branch is $w>0$.'
 if t=='product':solution+=' The sign of $v$ is fixed throughout $Δ$.'
 solution+='\n\n**Step 4**: Perform the change of variables:'+block(r'\begin{aligned}\iiint_R '+tex(f)+r'\,dV &=\iiint_Δ \left('+tex(ft)+r'\right)\left|\frac{∂(x,y,z)}{∂(u,v,w)}\right|\,du\,dv\,dw\\ &=\iiint_Δ \left('+tex(ft)+r'\right)\left|'+tex(jd)+r'\right|\,du\,dv\,dw\\ &='+repeated(g,b)+r'.\end{aligned}')
 return {':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level}

def finish(q,f,vals,correct,t,p,profile,seed,evidence_only=False):
 ident=digest({'version':VERSION,'question':q,'field':f,'bank':sorted(vals),'correct':None if correct is None else vals[correct]})
 qid=uid(ident);fid=uid(qid+'/selection')
 answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
 if len(set(a[':answer/id'] for a in answers))!=len(answers):raise ValueError('duplicate printed answer')
 if correct is not None:f[':answer-field/correct']=[':answer/id',answers[correct][':answer/id']]
 random.Random(seed).shuffle(answers)
 f.update({':answer-field/id':fid,':answer-field/choices':answers})
 q.update({':question/id':qid,':question/answer-fields':[f]})
 taskp={k:v for k,v in p.items() if k!='height'} if t in ('exp','sin','cos2','log') else p
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':t,'parameters':p,'seed':seed,'bank_profile':profile,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'evidence_only':evidence_only,'eligible_for_learning':not evidence_only,'mathematical_fingerprint':digest([t,taskp]),'content_identity':ident,'python':sys.version.split()[0],'sympy':s.__version__}}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in FAMILIES:raise ValueError('difficulty')
 if field_type not in (None,'radio'):raise ValueError('only observed radio supported')
 if profile=='raw':
  if template not in RAW_TEMPLATES:raise ValueError('raw source template required')
  return raw_generate(template,{'scale':1,'height':RAW_TEMPLATES[template]['height']} if parameters is None else parameters,seed)
 if profile not in (None,'method'):raise ValueError('profile raw or method')
 rng=random.Random(seed);t=template or rng.choice(FAMILIES[level])
 if t not in FAMILIES[level]:raise ValueError('template difficulty mismatch')
 # Family and COMPLETE method bank chosen before parameter sampling.
 for _ in range(100):
  p=dict(parameters) if parameters is not None else globals()['parameters'](level,t,rng)
  m=derive(level,t,p);opts=bank(t,p,m)
  if unambiguous(opts,level!='easy'):break
  if parameters is not None:raise ValueError('ambiguous complete bank')
 else:raise RuntimeError('could not sample eligible bank')
 q=normal_question(level,t,p,m);f={':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio'}
 vals=[repeated(e,b) if level!='easy' else tex(e) for e,b in opts]
 return finish(q,f,vals,0,t,p,'method',seed)

# EASY: supplied repeated-integral limits; direct substitutions, constant Jacobian.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (authored): product coordinate with fixed nonzero y sign, reciprocal
# variable Jacobian and two nonzero integrand terms; full setup, no evaluation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored label for observed unrated family): square-root third coordinate,
# a dependent bound and variable Jacobian; same setup demand at every parameter.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 label='Original evidence replay' if r['generation']['evidence_only'] else 'Generated variant'
 level=q.get(':question/difficulty','unrated').split('/')[-1]
 return '## '+label+' / '+level+' / '+r['generation']['template']+'\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '') for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','*No source worked solution.*')
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=(*FAMILIES,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('count positive')
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (FAMILIES if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
