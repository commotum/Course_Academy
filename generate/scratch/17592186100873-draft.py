#!/usr/bin/env python3
"""Selected entry of a product: source-faithful matrix/target recipes, E/M/H.

Registered numeric sibling is immutable and is never imported. Evidence profiles
retain opaque historical banks without claiming to recover their wrong operations.
Normal radio banks use complete method-derived profiles selected before sampling.
"""
import argparse,copy,hashlib,json,random,re,sys,uuid
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).with_suffix('')
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import matrix_tex,normalize_prose,normalize_tex,validate_prose,validate_tex,checked_math_content
import sympy as sp
CAPTURE=json.loads((HERE/'source.json').read_text()); SOURCE=CAPTURE['record']
KP_ID=17592186100873; VERSION='selected-entry-v2'; LEVELS=('easy','moderate','hard')
SOURCES={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
MAT=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
TARGET=re.compile(r'\{?([a-z])\}?_\{([1-5])([1-5])\}')
def matrices(text):
 return [[[int(x.strip()) for x in row.split('&')] for row in body.split(r'\\')] for body in MAT.findall(text)]
def params(q):
 a,b=matrices(q[':question/problem']); _,i,j=TARGET.search(q[':question/problem']).groups()
 return {'A':a,'B':b,'row':int(i),'column':int(j)}
def typename(f):return f[':answer-field/type'][':db/ident'].split('/')[-1]
TEMPLATES={s:{'field_type':typename(q[':question/answer-fields'][0]),'terms':len(params(q)['B'])} for s,q in SOURCES.items()}
PROFILES=('method-omit-sign','method-reverse-column')
def ordinal(n):return str(n)+{1:'st',2:'nd',3:'rd'}.get(n,'th')
def factor(n):return '('+str(n)+')' if n<0 else str(n)
def hashof(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(SOURCE[':knowledge-point/id']),x))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def validate_parameters(p,level,evidence=False):
 if set(p)!={'A','B','row','column'}:raise ValueError('Exact parameter keys A,B,row,column required')
 a,b,i,j=p['A'],p['B'],p['row'],p['column']
 if not (isinstance(a,list) and isinstance(b,list) and 2<=len(a)<=5 and 2<=len(b)<=3):raise ValueError('Source-shaped dimensions')
 if any(not isinstance(r,list) for r in a+b):raise ValueError('Rows required')
 n=len(b);m=len(b[0])
 if not 2<=m<=5 or any(len(r)!=n for r in a) or any(len(r)!=m for r in b):raise ValueError('Conformable rectangular matrices')
 if any(type(x)is not int or abs(x)>20 for r in a+b for x in r):raise ValueError('Integer operand bound 20')
 if type(i)is not int or type(j)is not int or not 1<=i<=len(a) or not 1<=j<=m:raise ValueError('Eligible target required')
 row=a[i-1];col=[r[j-1] for r in b];terms=[x*y for x,y in zip(row,col)]
 if max(map(abs,row+col))>10:raise ValueError('Selected operand source ceiling 10')
 if max(map(abs,terms))>30 or sum(map(abs,terms))>58:raise ValueError('Product/L1 source ceiling')
 if not evidence:
  if sum(x!=0 for x in terms)<2:raise ValueError('At least two substantive products')
  if level=='easy':
   if n==3 and not any(abs(x)<=1 or abs(y)<=1 for x,y in zip(row,col)):raise ValueError('Easy three-term unit/zero support')
  else:
   if n!=3 or any(not 2<=abs(x)<=6 for x in row+col):raise ValueError('Three substantive nonunit products')
   l1=sum(map(abs,terms))
   if level=='moderate' and (max(map(abs,terms))>16 or not 12<=l1<=36):raise ValueError('Moderate bounds')
   if level=='hard' and (not 37<=l1<=58 or not(min(terms)<0<max(terms))):raise ValueError('Hard signed collection bounds')
 return row,col,terms

def bank_values(row,col,profile):
 t=[x*y for x,y in zip(row,col)];answer=sum(t)
 if profile=='method-omit-sign':return [answer,sum(t[:-1]),sum(map(abs,t)),-answer,sum(row)+sum(col)]
 if profile=='method-reverse-column':return [answer,dot(row,list(reversed(col))),t[0],sum(t[1:]),dot(row,row)]
 raise ValueError('Unknown complete profile')

def render_problem(src,p):
 text=src[':question/problem'];ms=list(MAT.finditer(text))
 for match,value in reversed(list(zip(ms,(p['A'],p['B'])))):text=text[:match.start()]+matrix_tex(value)+text[match.end():]
 return TARGET.sub(lambda m: ('{'+m[1]+'}' if m[0].startswith('{') else m[1])+'_{'+str(p['row'])+str(p['column'])+'}',text)

def render_solution(src,p):
 a,b,i,j=p['A'],p['B'],p['row'],p['column'];row=a[i-1];col=[r[j-1] for r in b];terms=[x*y for x,y in zip(row,col)];letter=TARGET.search(src[':question/problem'])[1]
 old=src.get(':question/worked-solution')
 if old:
  intro=old.split('\n\n$$')[0]
  intro=re.sub(r'\$[1-5]\$(?:st|nd|rd|th) row',lambda _: '$'+str(i)+'$'+ordinal(i)[-2:]+' row',intro)
  intro=re.sub(r'\$[1-5]\$(?:st|nd|rd|th) column',lambda _: '$'+str(j)+'$'+ordinal(j)[-2:]+' column',intro)
 else:
  labels=re.search(r'Let \$([A-Z])\s*=\s*([A-Z])([A-Z])',src[':question/problem']).groups()
  intro=f'Multiplying the ${i}$'+ordinal(i)[-2:]+f' row in ${labels[1]}$ by the ${j}$'+ordinal(j)[-2:]+f' column in ${labels[2]}$, we get'
 implicit=bool(old and r'\cdot' not in old)
 expansion='+'.join(factor(x)+'('+str(y)+')' if implicit else factor(x)+r'\cdot '+factor(y) for x,y in zip(row,col))
 signed=''.join(('+' if k and x>=0 else '')+str(x) for k,x in enumerate(terms))
 stages=[matrix_tex(a)+matrix_tex(b),matrix_tex([row])+matrix_tex([[x] for x in col]),expansion,signed,str(sum(terms))+'.']
 return intro+'\n\n$$\n'+r'\begin{aligned}{'+letter+'}_{'+str(i)+str(j)+r'} & ='+(r' \\  & ='.join(stages))+r'\end{aligned}'+'\n$$'

@checked_math_content
def normal_checked(record):return record

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Raw profiles `observed:<source-id>` preserve absent attributes; evidence only.
 Normal profiles are method-derived complete banks. Invalid explicit inputs fail.
 """
 if level not in LEVELS:raise ValueError('Unsupported difficulty')
 rng=random.Random(seed);evidence=bool(profile and profile.startswith('observed:'))
 if evidence:
  sid=profile.split(':',1)[1]
  if template not in (None,sid):raise ValueError('Profile/template mismatch')
  template=sid
 choices=[s for s,t in TEMPLATES.items() if (field_type in (None,t['field_type'])) and (level=='easy' or t['terms']==3)]
 if template is None:template=rng.choice(choices)
 if template not in choices:raise ValueError('Unsupported template/field/level')
 src=SOURCES[template];ft=TEMPLATES[template]['field_type']
 if evidence and level!='easy':raise ValueError('All originals easy or unrated')
 if profile is None:profile=rng.choice(PROFILES) if ft=='radio' else 'blank'
 if not evidence and profile not in (PROFILES if ft=='radio' else ('blank',)):raise ValueError('Profile incompatible with field')
 explicit=parameters is not None
 for attempt in range(10000):
  if explicit:p=copy.deepcopy(parameters)
  elif evidence:p=params(src)
  else:
   anchor=params(src);n=len(anchor['B']);m=len(anchor['B'][0]);h=len(anchor['A']);p={'A':[[rng.randint(-6,6) for _ in range(n)] for _ in range(h)],'B':[[rng.randint(-6,6) for _ in range(m)] for _ in range(n)],'row':rng.randint(1,h),'column':rng.randint(1,m)}
  try:
   row,col,terms=validate_parameters(p,level,evidence)
   anchor=params(src)
   if (len(p['A']),len(p['B']),len(p['B'][0]))!=(len(anchor['A']),len(anchor['B']),len(anchor['B'][0])):raise ValueError('Preserve source-shaped dimensions per family')
   answer=int((sp.Matrix(p['A'])*sp.Matrix(p['B']))[p['row']-1,p['column']-1])
   if answer!=sum(terms):raise AssertionError('Independent exact product disagreement')
   if evidence:
    sf=src[':question/answer-fields'][0];key=sf.get(':answer-field/correct',{}).get(':answer/id')
    vals=[answer if a[':answer/id']==key else int(a[':answer/value']) for a in sf[':answer-field/choices']]
   else:vals=[answer] if ft=='blank' else bank_values(row,col,profile)
   if len(vals)!=len(set(vals)) or max(map(abs,vals))>58:raise ValueError('Whole bank ambiguous or outside bound')
   break
  except ValueError:
   if explicit or evidence:raise
 else:raise ValueError('No eligible whole instance')
 problem=normalize_prose(render_problem(src,p));solution=normalize_prose(render_solution(src,p));sf=src[':question/answer-fields'][0]
 q={':question/problem':problem}
 if not evidence or ':question/worked-solution' in src:q[':question/worked-solution']=solution
 if not evidence or ':question/difficulty' in src:q[':question/difficulty']=':question.difficulty/'+level
 # Mathematical task identity excludes irrelevant entries, labels, bank aliases.
 fp=hashof(['selected-entry',level,p['row'],p['column'],row,col])
 qid=uid(hashof([VERSION,q,ft,sf[':answer-field/key'],sorted(vals)]));q[':question/id']=qid
 fid=uid(qid+':field:'+sf[':answer-field/key']);answers=[];correct=None
 for k,v in enumerate(vals):
  aid=uid(fid+':'+str(v));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':normalize_tex(str(v))})
  if evidence:
   if sf[':answer-field/choices'][k][':answer/id']==sf.get(':answer-field/correct',{}).get(':answer/id'):correct=aid
  elif k==0:correct=aid
 if ft=='radio':rng.shuffle(answers)
 f={':answer-field/id':fid,':answer-field/key':sf[':answer-field/key'],':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers}
 if correct is not None:f[':answer-field/correct']=[':answer/id',correct]
 q[':question/answer-fields']=[f]
 r={'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'mathematical_fingerprint':fp,'source_basis':CAPTURE['basis'],'source_lineage':CAPTURE['lineage'],'evidence_only':evidence,'eligible_for_learning':not evidence,'difficulty_evidence':'observed/inferred-unrated' if level=='easy' else 'authored missing-level extension','python_version':sys.version.split()[0],'sympy_version':sp.__version__,'bank_recipes':('opaque historical constants; computed designated key' if evidence else profile)}}
 if evidence:
  validate_prose(problem)
  if ':question/worked-solution' in q:validate_prose(solution)
  for a in answers:validate_tex(a[':answer/value'])
  r['generation']['math_format']='course-academy-tex-v1';return r
 return normal_checked(r)

# Easy: observed two-/three-term selected dot product, with unit/zero support in3.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate authored: three nonzero nonunit products, each <=16, L1<=36.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard authored: same three products/stages; mixed signs, L1 37..58, products<=30.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];g=r['generation'];out=[f"Level: {q.get(':question/difficulty','MISSING (raw source)')} | template: {g['template']} | profile: {g['bank_profile']}",q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  out.append('Field '+f[':answer-field/key']+' ('+f[':answer-field/type']+')')
  key=f.get(':answer-field/correct',[None,None])[1]
  if key is None:out.append('Correct designation: MISSING (raw source)')
  out.extend(('* [correct] ' if a[':answer/id']==key else '* ')+a[':answer/value'] for a in f[':answer-field/choices'])
 out.append('Worked solution:\n'+q.get(':question/worked-solution','MISSING (raw source)'));return '\n\n'.join(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='json');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 records=[generate(l,a.seed+k,template=a.template,profile=a.profile) for l in (LEVELS if a.difficulty=='all' else (a.difficulty,)) for k in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
