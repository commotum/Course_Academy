#!/usr/bin/env python3
"""Volumes from three supplied vectors; local review generator, no DB writes.

Source: math basis1356. See 17592186105907/ for full source extraction/QA.
Source-layout templates replay every complete prompt and worked-solution stage.
Observed scalar radio banks are opaque evidence-only proportional catalogs; they
are NEVER default banks or claims about the original author's error operations.
Normal radios choose one whole authored bank: omit each cofactor term, or reverse
the middle cofactor sign. Exact rational arithmetic; reject the whole instance.
All levels compute |a dot (b cross c)| from supplied vectors. Moderate and hard
are explicitly authored scopes; neither asks for vertices or coplanarity.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186105907
KP_UUID='fe9711f6-e2ad-5eed-8ded-a6153b0322bd'
TITLE='Calculating the Volume of a Parallelepiped Spanned by Three Vectors'
VERSION='parallelepiped-volume-1'
EVIDENCE=Path(__file__).with_suffix('')
CAPTURE=json.loads((EVIDENCE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in CAPTURE['record'][':knowledge-point/questions']}
PROVENANCE={k:CAPTURE[k] for k in ('database','basis','lineage')}
# (substitution coefficient styles, commute second minor products, zero-term omissions,
#  direct evaluated minor row). All are extracted layout choices, not distractors.
STYLES={
 'q-128421':(('full','full','full'),True,(),False),
 'q-128433':(('zero','omit','full'),True,(0,),False),
 'q-18259':(('full','full','omit'),True,(),False),
 'q-280670':(('full','full','full'),False,(),False),
 'q-280671':(('full','full','full'),False,(),False),
 'q-280712':(('full','full','full'),False,(),True),
 'q-280716':(('full','omit','full'),False,(),False),
 'q-40221':(('full','full','zero'),True,(2,),False),
 'q-42050':(('omit','full','omit'),True,(),False),
 'q-40214':(('full','full','full'),False,(),False),
 'q-42052':(('full','full','full'),False,(),False),
}
SOURCE_FAMILIES={sid:('radio_missing_solution' if sid in ('q-40214','q-42052') else
 'blank_compute_evaluated_minors' if sid=='q-280712' else
 'blank_compute_products' if sid=='q-280716' else
 'blank_calculate_products' if sid in ('q-280670','q-280671') else
 'radio_calculate_products') for sid in SOURCES}
TEMPLATES={sid.replace('q-','source_'):{'level':'easy','source_id':sid,
 'field_type':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]} for sid,q in SOURCES.items()}
for level in ('easy','moderate','hard'):
 for kind in ('blank','radio'):
  TEMPLATES[level+'_'+kind]={'level':level,'source_id':None,'field_type':kind}

class Rejected(ValueError): pass

def scalar(x):
 if isinstance(x,bool): raise ValueError('Boolean coordinate')
 if isinstance(x,float): raise ValueError('Use exact integers or rational strings')
 v=sp.Rational(x)
 return v

def canonical(p):
 if set(p)!= {'vectors'}: raise ValueError('Parameters must contain only vectors')
 v=p['vectors']
 if len(v)!=3 or any(len(row)!=3 for row in v): raise ValueError('Three three-dimensional vectors required')
 return [[scalar(x) for x in row] for row in v]

def serialized(v):return {'vectors':[[str(x) for x in row] for row in v]}
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(x): return sp.latex(sp.Rational(x))
def atom(x): return '('+tex(x)+')' if x<0 else tex(x)
def matrix(rows):return r'\begin{aligned}'+r' \\ '.join(' & '.join(tex(x) for x in row) for row in rows)+r'\end{aligned}'
def determinant(rows):return '|'+matrix(rows)+'|'
def math_data(v):
 a,b,c=v
 mins=[b[1]*c[2]-b[2]*c[1],b[0]*c[2]-b[2]*c[0],b[0]*c[1]-b[1]*c[0]]
 terms=[a[0]*mins[0],-a[1]*mins[1],a[2]*mins[2]]
 return mins,terms,sum(terms)

def plus_terms(items):
 s=''
 for value,body in items:
  s+=('-' if value<0 else '+' if s else '')+body
 return s

def rendered_rows(v,labels,style):
 a,b,c=v; modes,commute,omissions,direct=style
 minors,terms,d=math_data(v)
 indices=((1,2),(0,2),(0,1))
 cof=[]; sub=[]
 for i,(j,k) in enumerate(indices):
  cofm=determinant([[b[j],b[k]],[c[j],c[k]]])
  # Formal cofactor signs stay visible, grouping every signed coefficient.
  cof.append(('' if i==0 else '-' if i==1 else '+')+atom(a[i])+r'\cdot '+cofm)
  coeff=a[i]*(1 if i!=1 else -1)
  if modes[i]=='zero':
   if a[i]!=0:raise ValueError('Source zero substitution mode requires zero coordinate')
   body='0'
  else:
   if direct: inside=tex(minors[i])
   else:
    second=(c[j],b[k]) if commute else (b[k],c[j])
    inside=atom(b[j])+r'\cdot '+atom(c[k])+'-'+atom(second[0])+r'\cdot '+atom(second[1])
   if modes[i]=='omit':
    if abs(coeff)!=1:raise ValueError('Source omitted-unit mode requires unit coefficient')
    prefix=''
   else:prefix=tex(abs(coeff))
   body=prefix+'('+inside+')'
  sub.append((coeff,body))
 evaluated=[]
 for i,t in enumerate(terms):
  if i in omissions:
   if t!=0:raise ValueError('Source zero omission requires a zero term')
   continue
  sign=t
  # q-280712 retains the formal -0 stage.
  if t==0 and i==1: sign=-1
  evaluated.append((sign,tex(abs(t))))
 rows=[labels[0]+r'\cdot ('+labels[1]+r'\times '+labels[2]+') & ='+determinant(v),
       ' & ='+''.join(cof),' & ='+plus_terms(sub),' & ='+plus_terms(evaluated),' & ='+tex(d)]
 return rows

def source_vectors(q):
 return [[scalar(x.replace(' ','')) for x in s.split(',')] for s in re.findall('⟨(.*?)⟩',q[':question/problem'])]

def source_prompt(sid,v):
 q=SOURCES[sid]; original=q[':question/problem']; tuples=re.findall('⟨(.*?)⟩',original)
 it=iter(zip(tuples,v))
 def substitute(_):
  raw,row=next(it)
  # Individual numeric slots retain exact comma/space and spaced-minus style.
  n=iter(row)
  def number(m):
   x=next(n); spelling=tex(x)
   if ' ' in m.group() and x<0:spelling=spelling.replace('-', '- ')
   return spelling
  return '⟨'+re.sub(r'-\s*\d+|\d+',number,raw)+'⟩'
 return re.sub('⟨(.*?)⟩',substitute,original)

def labels_for(sid):return re.findall(r'\$([a-z])\s*=',SOURCES[sid][':question/problem'])

def solution(v,labels,sid=None):
 style=STYLES[sid] if sid else (('full','full','full'),False,(),False)
 rows=rendered_rows(v,labels,style)
 block=r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
 d=math_data(v)[2]
 if sid and ':question/worked-solution' in SOURCES[sid]:
  original=SOURCES[sid][':question/worked-solution']
  # Complete aligned component is one slot, never substring digit replacement.
  start=original.index(r'\begin{aligned}')
  end=original.index('\n$$',start)
  out=original[:start]+block+original[end:]
  out=re.sub(r'V=\|[-\d]+\|=[\d]+\.',lambda _: 'V=|'+tex(d)+'|='+tex(abs(d))+'.',out)
  return out
 return ('The volume of the parallelepiped spanned by three vectors is given by the absolute value of their triple product.\n\nFirst, we compute the triple product:\n\n$$\n'+block+'\n$$\n\nFinally, we take the absolute value. So the volume of the corresponding parallelepiped is\n\n$$\nV=|'+tex(d)+'|='+tex(abs(d))+'.\n$$')

def allowed(level,v,sid=None):
 _,terms,d=math_data(v)
 if not d: raise Rejected('Nonzero volume required')
 if sid:
  # Source replay preserves all original integers and per-layout zero/unit structure.
  if any(x.q!=1 or abs(x)>9 for row in v for x in row):raise ValueError('Observed integer-coordinate bounds exceeded')
  rendered_rows(v,labels_for(sid),STYLES[sid])
  return
 flat=sum(v,[])
 if level=='easy':
  if any(x.q!=1 or abs(x)>9 for x in flat) or not 1<=flat.count(0)<=3:raise Rejected('Easy requires integer coordinates <=9 and 1..3 zero coordinates')
 elif level=='moderate':
  if any(x==0 or x.q!=1 or abs(x)>5 for x in flat) or any(t==0 for t in terms):raise Rejected('Moderate requires nonzero integer coordinates <=5 and three nonzero cofactor terms')
 elif level=='hard':
  if any(x==0 or x.q not in (1,2,3) or abs(x)>5 for x in flat) or sum(x.q>1 for x in flat)<3 or any(t==0 for t in terms):raise Rejected('Hard requires bounded integer/half/third coordinates, >=3 reduced fractions and three nonzero cofactor terms')
 else:raise ValueError('Unknown difficulty')

def source_profile(sid):
 q=SOURCES[sid]; volume=abs(math_data(source_vectors(q))[2])
 return [scalar(a[':answer/value'])/volume for a in q[':question/answer-fields'][0][':answer-field/choices']]

def bank(v,profile,sid,kind):
 _,t,d=math_data(v);volume=abs(d)
 if kind=='blank':return [volume]
 if profile and profile.startswith('observed_'):
  return [r*volume for r in source_profile(sid)]
 vals=[volume,abs(t[0]+t[1]),abs(t[0]+t[2]),abs(t[1]+t[2]),abs(t[0]-t[1]+t[2])]
 if len(set(vals))!=5 or any(x<=0 for x in vals):raise Rejected('Whole authored cofactor bank collides or has an ineligible zero volume')
 return vals

def sample(level,rng,sid=None):
 if sid:
  v=source_vectors(SOURCES[sid])
  # Positive common scale preserves omitted-zero/unit constraints by scaling only
  # the SECOND supplied vector: a's source unit/zero coefficients remain fixed.
  scale=rng.choice((1,2,-1))
  if max(abs(x*scale) for x in v[1])<=9:v[1]=[x*scale for x in v[1]]
  return v
 if level=='easy':
  v=[[sp.Integer(rng.randint(-5,5)) for _ in range(3)] for _ in range(3)]
  for index in rng.sample(range(9),rng.randint(1,3)):v[index//3][index%3]=sp.Integer(0)
  return v
 if level=='moderate':return [[sp.Integer(rng.choice((-5,-4,-3,-2,-1,1,2,3,4,5))) for _ in range(3)] for _ in range(3)]
 return [[sp.Rational(rng.choice((-5,-4,-2,-1,1,2,4,5)),rng.choice((1,2,3))) for _ in range(3)] for _ in range(3)]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Invalid difficulty')
 if profile and profile.startswith('observed_'):
  raw=profile[len('observed_'):].removesuffix('_repaired')
  if raw not in SOURCES:raise ValueError('Unknown observed profile')
  implied=raw.replace('q-','source_')
  if template and template!=implied:raise ValueError('Profile/template mismatch')
  template=implied
 elif profile not in (None,'authored_cofactor'):raise ValueError('Unknown bank profile')
 template=template or level+'_'+(field_type or 'radio')
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level:raise ValueError('Template/difficulty mismatch')
 spec=TEMPLATES[template];sid=spec['source_id'];kind=spec['field_type']
 if field_type and field_type!=kind:raise ValueError('Field type mismatch')
 if kind=='blank' and profile is not None:raise ValueError('Blank fields have no bank profile')
 profile=profile or ('authored_cofactor' if kind=='radio' else None)
 raw_profile=bool(profile and profile.startswith('observed_') and not profile.endswith('_repaired'))
 rng=random.Random(seed)
 for _ in range(1000):
  v=canonical(parameters) if parameters is not None else sample(level,rng,sid)
  try:
   allowed(level,v,sid)
   vals=bank(v,profile,sid,kind)
   break
  except Rejected:
   if parameters is not None:raise
 else:raise Rejected('No eligible whole bank found')
 labels=labels_for(sid) if sid else ['a','b','c']
 prompt=source_prompt(sid,v) if sid else ('Calculate the volume'+(' $V$' if kind=='blank' else '')+' of the parallelepiped spanned by '+', '.join('$'+l+'=⟨'+','.join(tex(x) for x in row)+'⟩$' for l,row in zip(labels,v))+'.'+('\n\n$V=${{field-1}}' if kind=='blank' else ''))
 solved=solution(v,labels,sid)
 missing_solution=sid and ':question/worked-solution' not in SOURCES[sid]
 missing_correct=sid and ':answer-field/correct' not in SOURCES[sid][':question/answer-fields'][0]
 missing_rating=sid and ':question/difficulty' not in SOURCES[sid]
 qcontent={':question/problem':prompt,':question/answer-values':sorted(tex(x) for x in vals),'kind':kind}
 if not(raw_profile and missing_solution):qcontent[':question/worked-solution']=solved
 if not(raw_profile and missing_rating):qcontent[':question/difficulty']=':question.difficulty/'+level
 # Identity binds actual learner content, bank and correct designation availability.
 qcontent['correct']=None if raw_profile and missing_correct else tex(abs(math_data(v)[2]))
 cf=digest({'version':VERSION,'content':qcontent})
 qid=str(uuid.uuid5(uuid.NAMESPACE_URL,KP_UUID+'/'+cf)); key='selection' if kind=='radio' else 'field-1';fid=str(uuid.uuid5(uuid.UUID(qid),key))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'math:'+tex(x))),':answer/type':':answer.type/math',':answer/value':tex(x)} for x in vals]
 correct=next(a[':answer/id'] for a in answers if a[':answer/value']==tex(abs(math_data(v)[2])))
 rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
 if not(raw_profile and missing_correct):field[':answer-field/correct']=[':answer/id',correct]
 question={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if ':question/difficulty' in qcontent:question[':question/difficulty']=qcontent[':question/difficulty']
 if ':question/worked-solution' in qcontent:question[':question/worked-solution']=solved
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
 'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':serialized(v),'bank_profile':profile,
 'bank_origin':'observed-opaque-evidence-only' if raw_profile else 'observed-opaque-repaired' if profile and profile.startswith('observed_') else 'authored-method' if kind=='radio' else 'observed' if sid else 'authored',
 'evidence_only':bool(profile and profile.startswith('observed_')),
 'eligible_for_learning':not bool(profile and profile.startswith('observed_')),
 'parameter_fingerprint':digest({'vectors':serialized(v)['vectors']}),'content_fingerprint':cf,'provenance':PROVENANCE,
 'source_id':sid,'observed_template_family':SOURCE_FAMILIES.get(sid),'authored_difficulty':missing_rating or not sid,'authored_extension':not sid,
 'source_repairs':{'inferred_correct':bool(missing_correct and not raw_profile),'authored_solution':bool(missing_solution and not raw_profile),'authored_easy_rating':bool(missing_rating and not raw_profile)},
 'plot_rating':'none','domain':'Exact rational supplied vectors, nonzero determinant; positive volume options',
 'bank_recipes': ['volume','omit_third_cofactor','omit_second_cofactor','omit_first_cofactor','reverse_middle_cofactor'] if profile=='authored_cofactor' else ['evidence-only ratio '+str(r) for r in source_profile(sid)] if profile else []}}

# EASY — observed integer vectors, 1..3 zero coordinates, exact determinant.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Observed source styles and normal integer/zero-coordinate workload."""
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — authored nonzero integer vectors; all three terms contribute.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Three nonzero cofactor terms, signed integer coordinates of magnitude <=5."""
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored reduced half/third coordinates; same scalar triple product.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """At least three reduced fractions, denominator <=3 and magnitude <=5."""
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return (q[':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[No source worked solution]'))
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=('markdown','json'),default='markdown');p.add_argument('--template',choices=TEMPLATES);p.add_argument('--profile');p.add_argument('--field-type',choices=('blank','radio'));args=p.parse_args()
 if args.count<1:p.error('Positive count required')
 records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
