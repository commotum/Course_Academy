#!/usr/bin/env python3
"""Positive-even monic completing-square expression generator, basis1356.

Easy preserves whole-expression radios and supplied-binomial/constant blanks.
Moderate preserves p/q identification, with familiar half coefficients1..11.
Hard is authored p/q identification with half coefficients12..15: the same four
operative stages, larger familiar squares only. No odd/negative linear terms,
nonmonic coefficients, equations to solve, or adding to both sides.
Raw/ completed source banks are evidence-only: scalar distractor offsets do not
establish recovered error intent. Default banks derive complete method mistakes.
All sampling chooses family/profile before parameters and rejects a whole bank.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186068875
KP_UUID='366b36a5-c909-5ea5-a05d-a6052fcd41d7'
TITLE='Completing the Square on a Quadratic Expression'
VERSION='completing-expression-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# level, variable, half coefficient, constant, field kind, response shape
CONFIG={
'q-140221':('easy','y',6,15,'radio','expression'),
'q-250390':('moderate','x',7,31,'blank','pq'),
'q-141537':('easy','x',5,16,'radio','expression'),
'q-141548':('easy','y',7,45,'radio','expression'),
'q-250452':('easy','y',11,131,'blank','plus'),
'q-250454':('easy','y',4,13,'blank','minus'),
'q-25238':('moderate','x',2,5,'radio','pq'),
'q-3667':('easy','x',6,35,'radio','expression'),
'q-141539':('moderate','x',3,14,'radio','pq'),
}

def enum(v):return v[':db/ident'] if isinstance(v,dict) else v
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+str(v)))
def parameters_for(sid):
 _,v,a,c,_,_=CONFIG[sid];return {'variable':v,'a':a,'c':c}
def signterm(n,space=False):return (' + ' if n>=0 else ' - ')+str(abs(n)) if space else ('+' if n>=0 else '-')+str(abs(n))
def poly(p,spaced=False):
 v,a,c=p['variable'],p['a'],p['c']
 return f'{v}^{{2}} + {2*a}{v} + {c}' if spaced else f'{{{v}}}^{{2}}+{2*a}{v}+{c}'
def expression(v,a,q,style='normal'):
 if style=='space':return f'({v} {"+" if a>=0 else "-"} {abs(a)})^{{2}}'+signterm(q,True)
 return f'({v}'+signterm(a)+ ('{)}^{2}' if style=='capture' else ')^{2}')+signterm(q)
def pair(a,q):return f'p={a},'+r'\,'+f'q={q}'

def mask(s,sid):
 _,v,a,c,kind,shape=CONFIG[sid];q=c-a*a
 # Mask complete numerical components before changing the variable token.
 def part(m):
  t=m[0]
  # Both expanded polynomial spellings in observed prompt/layout.
  t=re.sub(r'(?:\{'+v+r'\}|'+v+r')\^\{2\}\s*\+\s*'+str(2*a)+v+r'\s*\+\s*'+str(c),lambda z:'POLYSP' if ' ' in z[0] else 'POLYC',t)
  t=t.replace(r'\cdot '+str(a)+v,r'\cdot ASLOT'+v)
  t=t.replace('{'+str(a)+'}^{2}','{ASLOT}^{2}')
  t=t.replace('('+v+'+'+str(a)+'{)}','('+v+'+ASLOT{)}')
  t=t.replace('('+v+' + '+str(a)+')','('+v+' + ASLOT)')
  t=t.replace('p='+str(a),'p=ASLOT').replace('q='+str(q),'q=QSLOT')
  # Terminal collected remainder, complete signed component.
  t=t.replace('^{2}'+signterm(q),'^{2}QTERMSLOT')
  t=re.sub(r'(?<![\w])'+str(c)+r'(?![\w])','CSLOT',t)
  t=t.replace('ASLOT'+v,'ASLOTVARSLOT')
  t=re.sub(r'(?<![A-Za-z\\])'+v+r'(?![A-Za-z])','VARSLOT',t)
  return t
 return re.sub(r'\$\$.*?\$\$|\$[^$]*\$',part,s,flags=re.S)
MASKS={sid:{k:mask(q[k],sid) for k in (':question/problem',':question/worked-solution') if k in q} for sid,q in QUESTIONS.items()}
def fill(s,p):
 for k,v in {'POLYSP':poly(p,True),'POLYC':poly(p),'ASLOT':str(p['a']),'CSLOT':str(p['c']),'QSLOT':str(p['c']-p['a']**2),'QTERMSLOT':signterm(p['c']-p['a']**2),'VARSLOT':p['variable']}.items():s=s.replace(k,v)
 return s

def solution(p,pq=False):
 v,a,c=p['variable'],p['a'],p['c'];q=c-a*a
 return ('First, we rewrite the coefficient of the linear term as a product with $2$ as a factor:\n\n$$\n'+f'{{{v}}}^{{2}}+2'+r'\cdot '+f'{a}{v}+{c}'+'\n$$\n\nNow, here\'s the trick. We *add* and *then subtract* $'+f'{{{a}}}^{{2}},$ writing the constant term ${c}$ last:\n\n$$\n'+r'\underbrace{'+f'{{{v}}}^{{2}}+2'+r'\cdot '+f'{a}{v}+{{{a}}}^{{2}}'+r'}-\,'+f'{{{a}}}^{{2}}+{c}'+'\n$$\n\nThe first three terms form a perfect square, which we factor as follows:\n\n$$\n'+f'({v}+{a})^{{2}}-{{{a}}}^{{2}}+{c}'+'\n$$\n\nFinally, evaluating the last two terms, we get\n\n$$\n'+expression(v,a,q)+'.\n$$'+(f'\n\nTherefore, $p={a}$ and $q={q}.$' if pq else ''))

# Historical evidence recipes: scale half coefficient and shift collected
# remainder by the observed signed offset. These patterns are parameterized but
# opaque; numerical reproduction alone does not establish mistake semantics.
BANKS={}
for sid,src in QUESTIONS.items():
 if CONFIG[sid][4]!='radio':continue
 _,v,a,c,_,shape=CONFIG[sid];q=c-a*a;recipes=[]
 for ans in src[':question/answer-fields'][0][':answer-field/choices']:
  val=ans[':answer/value'];compact=val.replace(' ','').replace('{','').replace('}','')
  nums=re.findall(r'-?\d+',compact)
  if shape=='pq':r,z=map(int,nums)
  else:
   m=re.search(r'\('+v+r'([+-]\d+)\)\^2([+-]\d+)',compact);r,z=int(m[1]),int(m[2])
  recipes.append((sp.Rational(r,a),z-q))
 BANKS[sid]=recipes

def guard(level,p,sid,evidence=False):
 if set(p)!={'variable','a','c'} or p['variable'] not in ('x','y','z') or type(p['a']) is not int or type(p['c']) is not int:raise ValueError('expected x/y/z variable, integer a,c')
 a,c=p['a'],p['c'];q=c-a*a
 if level=='hard':valid=12<=a<=15 and 1<=abs(q)<=25 and c>0
 else:valid=1<=a<=11 and 1<=abs(q)<=25 and 0<c<=140
 if not valid:raise ValueError('outside familiar even-positive completing-square bounds')
 shape=CONFIG[sid][5] if sid in CONFIG else 'pq'
 if shape=='plus' and q<=0:raise ValueError('plus blank requires positive remainder')
 if shape=='minus' and q>=0:raise ValueError('minus blank requires negative remainder')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard') or field_type not in (None,'radio','blank'):raise ValueError('unknown level/field')
 rng=random.Random(seed);observed=bool(profile and profile.startswith(('raw:','completed:')));raw=bool(profile and profile.startswith('raw:'))
 if observed:
  sid=profile.split(':',1)[1]
  if sid not in CONFIG or CONFIG[sid][0]!=level or (template and template!=sid):raise ValueError('source profile outside family/level')
 else:
  if profile not in (None,'method'):raise ValueError('unknown profile')
  options=[s for s,cfg in CONFIG.items() if cfg[0]==level and (not field_type or cfg[4]==field_type)] if level!='hard' else ['hard_radio','hard_blank']
  if level=='hard' and field_type:options=['hard_'+field_type]
  sid=template or rng.choice(options)
  if sid not in options:raise ValueError('template outside eligible families')
 kind,shape=(CONFIG[sid][4:6] if sid in CONFIG else (sid.split('_')[1],'pq'))
 if field_type and kind!=field_type:raise ValueError('field selector mismatch')
 # Select complete bank first. No option-by-option replacement after collision.
 recipes=BANKS[sid] if observed and kind=='radio' else 'method'
 for attempt in range(1000):
  if parameters is not None:p=dict(parameters)
  else:
   a=rng.randint(12,15) if level=='hard' else rng.randint(2 if shape=='minus' else 1,11)
   q=rng.choice([n for n in range(-25,26) if n and a*a+n>0 and (level=='hard' or a*a+n<=140) and (shape!='plus' or n>0) and (shape!='minus' or n<0)])
   p={'variable':rng.choice(['x','y','z']),'a':a,'c':a*a+q}
  guard(level,p,sid,observed);v,a,c=p['variable'],p['a'],p['c'];q=c-a*a
  tuples=[(a,q),(a,c),(a,c-a),(a,c+a*a),(2*a,c-4*a*a)] if recipes=='method' else [(sp.Rational(scale)*a,q+offset) for scale,offset in recipes]
  exprs=[sp.expand((sp.Symbol('v')+r)**2+z) for r,z in tuples]
  collision=len(set(exprs if shape!='pq' else tuples))!=5 if kind=='radio' else False
  if not collision:break
  if parameters is not None:raise ValueError('whole complete bank collision')
 else:raise ValueError('no valid instance')
 if sid in MASKS:
  prompt=fill(MASKS[sid][':question/problem'],p)
  sol=fill(MASKS[sid][':question/worked-solution'],p) if ':question/worked-solution' in MASKS[sid] else solution(p,shape=='pq')
 else:
  prompt=f'If the expression ${poly(p)}$ is written as $(x+p)^{{2}}+q$, then what are the values of $p$ and $q$?'.replace('(x+p)',f'({v}+p)')
  if kind=='blank':prompt+='\n\n$p =$\n{{field-1}},\n$q =$\n{{field-2}}'
  sol=solution(p,True)
 # Old expressions preserve their exact historical notation only in evidence.
 style='space' if sid==next(iter(CONFIG)) else ('capture' if observed else 'normal')
 values=[pair(r,z) if shape=='pq' else expression(v,r,z,style) for r,z in tuples] if kind=='radio' else []
 correct=pair(a,q) if shape=='pq' else expression(v,a,q,style)
 source=QUESTIONS.get(sid)
 qrec={':question/problem':prompt}
 if not raw or ':question/worked-solution' in source:qrec[':question/worked-solution']=sol
 if not raw or ':question/difficulty' in source:qrec[':question/difficulty']=':question.difficulty/'+level
 fields=source[':question/answer-fields'] if raw else [{':answer-field/key':k} for k in (['selection'] if kind=='radio' else ['field-1','field-2'])]
 specs=[]
 for f in fields:
  key=f[':answer-field/key'];val=str(a) if shape=='pq' and key=='field-1' else (v+'+'+str(a) if key=='field-1' else str(abs(q) if shape=='minus' else q))
  vals=values if kind=='radio' else [val];cv=correct if kind=='radio' else val
  specs.append((key,vals,cv,not raw or ':answer-field/choices' in f,not raw or ':answer-field/correct' in f))
 # Identity includes actual correct presence/value and every actual field shape,
 # but excludes aliases, seed and choice order. Missing raw banks remain absent.
 ident=digest([VERSION,qrec,kind,sorted((k,sorted(vals) if bank else None,cv if corr else None,bank,corr) for k,vals,cv,bank,corr in specs)])
 qrec[':question/id']=uid(ident);qrec[':question/answer-fields']=[]
 for key,vals,cv,bank,corr in specs:
  f={':answer-field/id':uid(ident+key),':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind}
  if bank:
   choices=[{':answer/id':uid(ident+key+val),':answer/type':':answer.type/math',':answer/value':val} for val in vals]
   if kind=='radio':rng.shuffle(choices)
   f[':answer-field/choices']=choices
  if corr:f[':answer-field/correct']=[':answer/id',uid(ident+key+cv)]
  qrec[':question/answer-fields'].append(f)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':qrec,'generation':{'version':VERSION,'seed':seed,'template':sid,'parameters':p,'bank_profile':profile or 'method','source':{k:SOURCE[k] for k in ('database','basis','lineage')},'mathematical_fingerprint':digest([a,c,shape]),'content_fingerprint':ident,'raw_replay':raw,'evidence_only':observed,'eligible_for_learning':not observed,'origin':'raw observed evidence' if raw else ('authored completion/evidence bank' if observed else ('authored hard' if level=='hard' else 'observed family; authored method bank')),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# Easy: observed whole-expression rewrite and supplied square fragments.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: observed p/q identification, same four component operations.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: authored larger familiar squares12..15, no extra algebra branch.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];parts=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):parts.append(f[':answer-field/key']+': '+', '.join('$'+a[':answer/value']+'$' for a in f.get(':answer-field/choices',[])))
 parts.append(q.get(':question/worked-solution','[Source omits worked solution.]'));return '\n\n'.join(parts)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type',choices=['radio','blank']);args=ap.parse_args()
 out=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(out,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
