#!/usr/bin/env python3
"""Source-backed bounded line-integral generator; see the adjacent package.

The sole sampled slot is the positive integrand multiplier c=2..9. Paths,
orientation, requested differential, response contract, and solution stages stay
fixed. Diagrams show only paths and are reused byte-for-byte. c=1 is evidence.
"""
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).with_suffix('')
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import normalize_prose,normalize_tex,checked_math_content
KP_ID=17592186133893
CAPTURE=json.loads((HERE/'source.json').read_text());SOURCE=CAPTURE['kp']
SOURCE_BY_ID={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
EXCLUDED={mid:'Rational integrand undefined on the path; an explicit improper-integral convention is absent. This bounded smooth-path generator preserves and excludes this source.' for mid in ['q-124123','q-124173','q-124177','q-124212']}
TEMPLATES={mid:{'level':q[':question/difficulty'][':db/ident'].split('/')[-1],'profile':'source-bank:'+mid,'source_db_id':q[':db/id']} for mid,q in SOURCE_BY_ID.items() if mid not in EXCLUDED}
VERSION='line-integral-smooth-scale-v1';SCALES=tuple(range(2,10))
x,y,t=sp.symbols('x y t',real=True)
# The supplied field, oriented parametrization, bounds, requested differential.
DATA={
 'q-124120':(x+sp.pi*sp.cos(sp.pi*y),(1+t,t),(0,1),'x'),
 'q-124175':(sp.sqrt(x-1)+y,(1+t,2-t),(0,1),'x'),
 'q-124217':(sp.pi*sp.sin(sp.pi*y/2)+x**2,(2,2*t),(0,1),'y'),
 'q-124278':(x+sp.sqrt(3*y),(2-2*t,3*t),(0,1),'y'),
 'q-124172':(y**2-2*x,(2*t,1+2*t),(0,1),'y'),
 'q-124167':(x*y/2,(2*sp.cos(t),2*sp.sin(t)),(0,sp.pi),'y'),
 'q-124268':(x**2*y,(sp.cos(t),2*sp.sin(t)),(sp.pi,3*sp.pi/2),'y'),
 'q-124273':(x*sp.exp(1-y**2),(3*sp.cos(t),sp.sin(t)),(sp.pi/2,2*sp.pi),'x')}

def clean(s):
 s=s.replace('⁡','').replace(r'\u2061','')
 s=re.sub(r'(?<![a-z])\{(sin|cos)\}(?=\^)',lambda m:r'\operatorname{'+m[1]+'}',s)
 s=re.sub(r'(?<!\\)\\\\(?=(?:frac|pi))',lambda m:'\\',s)
 return s

def scale(s,c):return s if c==1 else str(c)+r'\left('+s.strip().rstrip('.,')+r'\right)'

def base_integrand(src):return re.search(r'Now, since \$f\(x,y\)=(.*?)\$',src[':question/worked-solution'],re.S)[1].rstrip(',')

def corrected_solution(src):
 s=clean(src[':question/worked-solution']);d=DATA[src[':question/math-academy-id']][3]
 # Correct only the LHS label in source integral formulas, never geometric data.
 s=re.sub(r'(\{\\int \}_\{C\}f\(x,y\)\\,\\text\{d\})[xy]',lambda m:m[1]+d,s)
 return s

def solution(src,c):
 s=corrected_solution(src)
 if c==1:return normalize_prose(s)
 original=clean(base_integrand(src));s=s.replace('f(x,y)='+original,'f(x,y)='+scale(original,c))
 def block(m):
  body=m[1];rows=body.split(r'\\');out=[]
  field=body.startswith('f(r(t))');integral=r'{\int }' in body
  if not(field or integral):return m[0]
  for k,row in enumerate(rows):
   lhs,rhs=row.split('& =',1)
   if field:rhs=scale(rhs,c)
   elif k==0 and 'f(r(t))' in rhs:pass
   else:rhs=scale(rhs,c)
   if k==0 and integral and 'f(x,y)' not in lhs:lhs=scale(lhs,c)
   out.append(lhs+'& ='+rhs)
  return r'\begin{aligned}'+r'\\'.join(out)+r'\end{aligned}'
 s=re.sub(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',block,s,flags=re.S)
 return normalize_prose(s)

def exact(template,c):
 f,path,bounds,d=DATA[template];path=tuple(map(sp.sympify,path))
 value=sp.simplify((c*f).subs({x:path[0],y:path[1]},simultaneous=True))
 integrand=sp.trigsimp(value*sp.diff(path[0 if d=='x' else 1],t))
 return sp.simplify(sp.integrate(integrand,(t,*bounds)))

@checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None):
 if level not in ('moderate','hard'):raise ValueError('Unsupported band: '+level+'; see capabilities.json')
 rng=random.Random(seed);templates=sorted(mid for mid,z in TEMPLATES.items() if z['level']==level)
 template=template or rng.choice(templates)
 if template not in templates:raise ValueError('Template/level mismatch')
 c=(parameters or {}).get('c',rng.choice(SCALES))
 if type(c)!=int or c not in (1,*SCALES):raise ValueError('Outside validated integer multiplier domain')
 if profile not in (None,TEMPLATES[template]['profile']):raise ValueError('Unknown complete bank profile')
 src=SOURCE_BY_ID[template];ans=exact(template,c);sf=src[':question/answer-fields'][0];original=clean(base_integrand(src))
 problem=clean(src[':question/problem'])
 # Source integrand is the only variable part of the prompt; preserve its path.
 if c!=1:
  m=re.search(r'(Evaluate \$\{\\int \}_\{C\})(.*?)(\\,\\text\{d\}[xy])',problem)
  assert m
  body=m[2]
  if body.startswith('(') and body.endswith(')'):body=body[1:-1]
  problem=problem[:m.start(2)]+scale(body,c)+problem[m.end(2):]
 problem=normalize_prose(problem)
 # Content identity has no seed, bank order, source identity, or generated UUID.
 identity=json.dumps([problem,level],separators=(',',':'))
 qid=str(uuid.uuid5(uuid.UUID(SOURCE[':knowledge-point/id']),identity));fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+sf[':answer-field/key']))
 choices=[];correct=None
 for a in sf[':answer-field/choices']:
  val=normalize_tex(scale(clean(a[':answer/value']),c));aid=str(uuid.uuid5(uuid.UUID(fid),val))
  choices.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':val})
  if a[':answer/id']==sf[':answer-field/correct'][':answer/id']:correct=aid
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution(src,c),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':sf[':answer-field/key'],':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',correct],':answer-field/choices':choices}]}
 return {'question':q,'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'generation':{'version':VERSION,'seed':seed,'parameters':{'c':c},'template':template,'bank_profile':TEMPLATES[template]['profile'],'source_question':src[':question/id'],'source_db_id':src[':db/id'],'source_basis':CAPTURE['basis'],'source_lineage':CAPTURE['lineage'],'exact_answer':sp.sstr(ans),'domain':'Real-valued continuous field along the complete smooth source path; endpoint square roots remain continuous.','sympy_version':sp.__version__,'python_version':sys.version.split()[0],'eligible_for_learning':c!=1,'evidence_only':c==1}}

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard'],required=True);p.add_argument('--count',type=int,default=1);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
 if a.difficulty=='easy':p.error('easy is unsupported; see capabilities.json')
 slots=[(mid,c) for mid,z in sorted(TEMPLATES.items()) if z['level']==a.difficulty for c in SCALES];random.Random(a.seed).shuffle(slots)
 if a.count<0 or a.count>len(slots):p.error('count outside finite capacity: '+str(len(slots)))
 out=[generate(a.difficulty,a.seed,mid,{'c':c}) for mid,c in slots[:a.count]]
 print(json.dumps(out,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
