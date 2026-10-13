#!/usr/bin/env python3
"""Exact source replay and bounded, source-supported general identity variants."""
import argparse,hashlib,json,random,re,uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186110721
KP_UUID='4b1fd794-f42b-5316-80e9-0698cb1f8b87'
TITLE='Solving a General Equation With Infinitely Many Solutions For Unknown Parameters'
VERSION='general-identity-1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
# a*u+b=c, d*v+e=f. Source layout/field shape is preserved per template.
SOURCE_CASES={
 'q-288622':('easy','shift-scale','observed-easy-bank','m','n',[1,2,7,5,0,15]),
 'q-288583':('moderate','scale-negative','blank','t','m',[2,0,6,-1,1,4]),
 'q-288584':('moderate','negative-scale','blank','s','t',[-1,3,1,2,0,6]),
 'q-288623':('easy','scale-unit','literal-replay-only','k','r',[2,0,9,1,0,6]),
 'q-288627':('easy','division-unit','literal-replay-only','p','q',[sp.Rational(1,2),0,4,1,0,20]),
}
SOURCES={q[':question/math-academy-id']:q for q in json.loads((PACKAGE/'source.json').read_text())['record'][':knowledge-point/questions']}
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(obj):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(obj)))
def tex(v):return sp.latex(sp.Rational(v)).replace('- ','-')
def linear(a,b,var):
 s=var if a==1 else '-'+var if a==-1 else (r'\frac{'+var+'}{'+str(sp.denom(a))+'}' if sp.numer(a)==1 and sp.denom(a)>1 else tex(a)+var)
 return s+('+' if b>0 else '')+(tex(b) if b else '')
def fingerprint(p):
 a,b,c,d,e,f=map(sp.Rational,p)
 # Normalize nonzero equation scaling, variable naming, layout, bank and seed.
 return digest(['general-identity',*[str(z) for z in sorted([(c-b)/a,(f-e)/d])]])
def render(mid,p):
 level,family,profile,u,v,original=SOURCE_CASES[mid]
 a,b,c,d,e,f=map(sp.Rational,p);U=(c-b)/a;V=(f-e)/d;total=U+V
 left=linear(a,b,u);right=(tex(e)+'-'+v) if mid=='q-288583' else linear(d,e,v)
 eq=('('+left+')' if b else left)+'x+'+('('+right+')' if e else right)+'='+('x' if c==1 else tex(c)+'x')+'+'+tex(f)
 source=SOURCES[mid]
 oldeq=re.findall(r'\$\$\n(.*?)\n\$\$',source[':question/problem'],re.S)[0]
 prompt=source[':question/problem'].replace(oldeq,eq)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',source[':question/worked-solution'],re.S)
 coeff=left+'='+tex(c)+'.';constant=right+'='+tex(f)+'.'
 solved_u=(r'\begin{aligned}'+u+' & ='+tex(U)+r'.\end{aligned}') if level=='easy' else u+'='+tex(U)+'.'
 solved_v=(r'\begin{aligned}'+v+' & ='+tex(V)+r'.\end{aligned}') if mid=='q-288622' else v+'='+tex(V)+'.'
 add=lambda z:'('+tex(z)+')' if z<0 else tex(z)
 ending=u+'+'+v+'='+tex(U)+'+'+add(V)+'='+tex(total)+'.'
 replacements=[blocks[0],blocks[1],eq,coeff,solved_u,constant]
 if len(blocks)==8:replacements.append(solved_v)
 replacements.append(ending)
 it=iter(replacements)
 worked=re.sub(r'\$\$\n(.*?)\n\$\$',lambda m:'$$\n'+next(it)+'\n$$',source[':question/worked-solution'],flags=re.S)
 original_since=re.search(r'Finally, since .*?we have',worked).group()
 worked=worked.replace(original_since,'Finally, since $'+u+'='+tex(U)+'$ and $'+v+'='+tex(V)+',$ we have')
 return prompt,worked,U,V,total

def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty not in ('easy','moderate'):raise ValueError('hard unsupported: no validated source difficulty template')
 rng=random.Random(seed)
 template=template or ('q-288622' if difficulty=='easy' else rng.choice(['q-288583','q-288584']))
 level,family,profile,u,v,original=SOURCE_CASES[template]
 if level!=difficulty:raise ValueError('template difficulty mismatch')
 if profile=='literal-replay-only':
  if parameters is None:raise ValueError('Unresolved source distractor recipes: exact replay only')
  if list(map(sp.Rational,parameters))!=list(map(sp.Rational,original)):raise ValueError('Unsupported profile extension')
 elif parameters is None:
  for _ in range(1000):
   U=rng.randint(1,12);V=rng.randint(1,12)
   if template=='q-288622':
    b=rng.randint(1,8);d=rng.randint(2,8);parameters=[1,b,U+b,d,0,d*V]
    vals=[U+V,d*V,U,2*V,U+b]
    if len(set(vals))<5:continue
   elif template=='q-288583':
    a=rng.randint(2,8);e=rng.randint(1,8);V=-rng.randint(1,12);parameters=[a,0,a*U,-1,e,e-V]
   else:
    c=rng.randint(1,8);d=rng.randint(2,8);parameters=[-1,U+c,c,d,0,d*V]
   break
  else:raise ValueError('Finite bounded search exhausted')
 p=list(map(sp.Rational,parameters))
 if len(p)!=6 or any(z==0 for z in (p[0],p[3])):raise ValueError('nonzero coefficients required')
 a,b,c,d,e,f=p
 if profile!='literal-replay-only':
  assert all(z.q==1 for z in p) and max(abs(z) for z in p)<=96
  if template=='q-288622':assert a==1 and 1<=b<=8 and 2<=d<=8 and e==0 and c>b and f>0
  elif template=='q-288583':assert 2<=a<=8 and b==0 and d==-1 and 1<=e<=8 and c>0 and f>e
  else:assert a==-1 and b>c and 1<=c<=8 and 2<=d<=8 and e==0 and f>0
 prompt,worked,U,V,total=render(template,p)
 if profile=='observed-easy-bank':values=[total,f,U,2*V,c]
 elif profile=='blank':values=[total]
 else:values=[sp.Rational(z[':answer/value'].replace(r'\frac{','').replace('}{','/').replace('}','')) for z in SOURCES[template][':question/answer-fields'][0][':answer-field/choices']]
 if len(set(values))!=len(values) or values.count(total)!=1:raise ValueError('Ambiguous bank')
 fp=fingerprint(p);qid=ident(['question',VERSION,fp,template,[str(z) for z in p]]);key='selection' if level=='easy' else 'field-1';fid=ident([qid,'field',key])
 choices=[{':answer/id':ident([fid,tex(z)]),':answer/type':':answer.type/math',':answer/value':tex(z)} for z in values]
 correct=next(a[':answer/id'] for a,z in zip(choices,values) if z==total)
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/radio' if level=='easy' else ':answer-field.type/blank',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':worked,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':[int(z) if z.q==1 else str(z) for z in p],'domain':'x and both parameters real','source_ids':[template],'mathematical_fingerprint':fp,'sympy':sp.__version__}}
def markdown(rec):return rec['question'][':question/problem']+'\n\n'+rec['question'][':question/worked-solution']
def batch(difficulty,count,seed):
 if not 1<=count<=144:raise ValueError('bounded count requires 1..144; actual finite capacity may be lower')
 records=[];seen=set()
 for i in range(count*100+100):
  rec=generate(difficulty,seed+i);fp=rec['generation']['mathematical_fingerprint']
  if fp not in seen:records.append(rec);seen.add(fp)
  if len(records)==count:return records
 raise ValueError('finite bounded variants exhausted; shortage remains explicit')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();r=batch(a.difficulty,a.count,a.seed);print(json.dumps(r,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,r)))
