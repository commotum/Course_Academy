#!/usr/bin/env python3
"""Reciprocal-plus-power integral radios; faithful basis-2275 source banks.

Every profile is a complete observed bank. Unrated incomplete captures receive
an explicit authored easy calibration and a canonical-example solution repair.
No new question forms, operators, plots, field types or database writes.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,itertools,json,math,random,re,sys,uuid
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
HERE=Path(__file__).with_suffix('')
z=importlib.util.spec_from_file_location('reciprocal_sum_math_format',HERE/'math_format.py');fmt=importlib.util.module_from_spec(z);z.loader.exec_module(fmt)
KP_ID=17592186105716
VERSION='reciprocal-power-v1'
SOURCE=json.loads((HERE/'source.json').read_text())
Q={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
X=s.Symbol('x',positive=True)
L=s.log(X)
TEMPLATES={
'q-103374':dict(level='easy',original=dict(a=3,b=6,d=2),slots=dict(a=[2,3,4,5,6],b=[4,6,8,10],d=[2,3,4])),
'q-103593':dict(level='easy',original=dict(p='3/2',b='1/2'),slots=dict(p=['1/2','3/2','5/2'],b=['1/2','1/3','1/4'])),
'q-29885':dict(level='easy',original=dict(n=2,r=2),slots=dict(n=[1,2,4,5],r=[2,3,5])),
'q-29886':dict(level='easy',original=dict(a=2,n=7,d=3),slots=dict(a=[2,3,4],n=[4,5,7,8],d=[2,3,4])),
'q-29888':dict(level='easy',original=dict(a=3,b=3),slots=dict(a=[3,4,5],b=[2,3,4,5])),
'q-29836':dict(level='easy',original=dict(a=3,d=5,b=3),slots=dict(a=[2,3,4],d=[5,6,7],b=[2,3,4]),calibration='authored easy: unrated source, missing key and solution'),
'q-29857':dict(level='easy',original=dict(a=2,b=1),slots=dict(a=[2,3,4,5],b=[1,2,3]),calibration='authored easy: unrated source, missing key and solution'),
'q-49100':dict(level='moderate',original=dict(a=2,c=1),slots=dict(a=list(range(2,9)),c=[1,2,3,4,5])),
'q-29915':dict(level='hard',original=dict(m=3,a=1,b=5),slots=dict(m=[1,3,5,7],a=list(range(1,9)),b=list(range(2,26)))),
}
BANK_PROFILES={k:dict(template=k,source=k,origin='observed') for k in TEMPLATES}
def tex(v):return s.latex(s.sympify(v)).replace(r'\log',r'\ln')
def powtex(p):return '{x}^{'+str(p)+'}'
def coeff(v):return tex(v)
def clean(t):
 t=t.replace(r'\u2061','').replace('⁡','').replace(r'\operatorname{ln}',r'\ln')
 t=re.sub(r'(?<![A-Za-z\\])ln',r'\\ln',t)
 return t

def replace_tokens(text,mapping):
 # Simultaneous replacement avoids cascades when slot values equal old tokens.
 keys=sorted(mapping,key=len,reverse=True)
 return re.sub('|'.join(re.escape(k) for k in keys),lambda m:mapping[m[0]],text)
def block(t):return '$$\n'+t+'\n$$'
def aligned(rows):return block(r'\begin{aligned}'+r' \\  & ='.join(rows)+r'.\end{aligned}')
def build(name,p):
 v={k:s.Rational(t) for k,t in p.items()};a=v.get('a');b=v.get('b');d=v.get('d');n=v.get('n');r=v.get('r');power=v.get('p');m=v.get('m');c=v.get('c')
 mp={};source=Q[name]
 if name=='q-103374':
  f=(a*X**2-b)/(d*X);bank=[a*X**2+s.log(a*X),a/d*X**2-s.log(a*X),a/(2*d)*X**2-b/d*L,a/(2*d)*X**2-s.log(a*X),a/d*X**2+b/d*L];good=2
  mp={r'\frac{3{x}^{2}-6}{2x}':r'\frac{'+str(a)+'{x}^{2}-'+str(b)+'}{'+str(d)+'x}',r'\frac{3{x}^{2}}{2x}':r'\frac{'+str(a)+'{x}^{2}}{'+str(d)+'x}',r'\frac{3}{x}':r'\frac{'+tex(b/d)+'}{x}',r'\frac{3}{2}':tex(a/d),r'\frac{3}{4}':tex(a/(2*d)),r'-3\int':'-'+tex(b/d)+r'\int',r'-3ln':'-'+tex(b/d)+'ln'}
 elif name=='q-103593':
  f=X**power+b/X;bank=[(power+1)*X**power+b*L,(power+1)*X**(power+1)+L/b,X**(power+1)/(power+1)+b*L,power*X**power+L/b,power*X**(power+1)+L/b];good=2
  mp={'3/2+1':str(power)+'+1',r'\frac{3}{2}':tex(power),'{x}^{3/2}':powtex(power),'{x}^{5/2}':powtex(power+1),r'\frac{1}{2}':tex(b),r'\frac{2}{5}':tex(1/(power+1))}
 elif name=='q-29885':
  power=n/3;f=X**power+s.sqrt(r)/X;bank=[(n+9)/(n+3)*X**((n+9)/3)+s.sqrt(r+3)*L,(n+5)/(n+3)*X**((n+2)/3)+r*L,3/(n+3)*L*X**((n+3)/3)+L,(n+7)/(n+3)*X**((n+5)/3)+s.sqrt(r+1)*L,3/(n+3)*X**((n+3)/3)+s.sqrt(r)*L];good=4
  mp={'2/3+1':str(power)+'+1',r'\frac{2}{3}':tex(power),'{x}^{2/3}':powtex(power),'{x}^{5/3}':powtex(power+1),r'\sqrt{2}':r'\sqrt{'+str(r)+'}',r'\frac{3}{5}':tex(3/(n+3))}
 elif name=='q-29886':
  power=n/3;f=a*X**power-1/(d*X);bank=[3*a/(n+3)*X**((n+3)/3)-L/d,(n-2)/a*X**(n/3)-d*L,n/a*X**((n-5)/3)-L,X**((n-6)/3)/(n-2)-L/d,n/(n-2)*X**(n/3)-d*L];good=0
  mp={'2{x}^{7/3}':tex(a)+powtex(power),'7/3+1':str(power)+'+1',r'\frac{7}{3}':tex(power),'{x}^{10/3}':powtex(power+1),r'\frac{1}{3x}':r'\frac{1}{'+str(d)+'x}',r'\frac{1}{3}':tex(1/d),r'2\cdot':tex(a)+r'\cdot',r'\frac{3}{5}':tex(a/(power+1))}
 elif name=='q-29888':
  f=a*X+b/X;bank=[a/2*X**2+b*L,(a+1)/b*X**2+(b+2)*L,(a-2)/2*X**2+b*L,(a-1)/b*X**2+(b-1)*L,(a+2)/2*X**2+(b+1)*L];good=0
  mp={r'\frac{3}{{x}^{-1}}':r'\frac{'+str(a)+'}{{x}^{-1}}','+3{x}^{-1}':'+'+str(b)+'{x}^{-1}',r'3\int x':tex(a)+r'\int x',r'+3\int':'+'+tex(b)+r'\int',r'\frac{3}{2}':tex(a/2),'+3ln':'+'+tex(b)+'ln'}
 elif name=='q-49100':
  f=(a-c/X)**2;bank=[a*c*X*L,s.log(s.Abs(a-c/X)),a*X-c*L,a*a*X-2*a*c*L-c*c/X,(a*X-c*L)**2];good=3
  unit=lambda z,body:body if z==1 else tex(z)+body
  mp={r'2-\frac{1}{x}':tex(a)+r'-\frac{'+tex(c)+'}{x}',
      r'4-\frac{4}{x}+\frac{1}{{x}^{2}}':tex(a*a)+r'-\frac{'+tex(2*a*c)+r'}{x}+\frac{'+tex(c*c)+'}{{x}^{2}}',
      r'4\int \text{d}x-4\int \frac{1}{x}\,\text{d}x+\int \frac{1}{{x}^{2}}\,\text{d}x':tex(a*a)+r'\int \text{d}x-'+tex(2*a*c)+r'\int \frac{1}{x}\,\text{d}x+'+unit(c*c,r'\int \frac{1}{{x}^{2}}\,\text{d}x'),
      r'\int 4':r'\int '+tex(a*a),r'\frac{4}{x}':r'\frac{'+tex(2*a*c)+'}{x}',
      r'\frac{1}{{x}^{2}}':r'\frac{'+tex(c*c)+'}{{x}^{2}}',
      '4x':tex(a*a)+'x','-4ln':'-'+tex(2*a*c)+'ln',
      r'+\frac{{x}^{-2+1}}{-2+1}':'+'+unit(c*c,r'\frac{{x}^{-2+1}}{-2+1}'),
      r'-\frac{1}{x}':r'-\frac{'+tex(c*c)+'}{x}'}
 elif name=='q-29915':
  f=(a-b)/X;bank=[-b*L,(a-b)*L,(b-a)*L,-(a+b)*X,b*X];good=1
  unit=lambda z,body:body if z==1 else tex(z)+body
  mp={r'\frac{\sqrt{{x}^{3}}}{\sqrt{{x}^{5}}}':unit(a,r'\frac{\sqrt{'+powtex(m)+r'}}{\sqrt{'+powtex(m+2)+'}}'),
      r'\int \frac{1}{{x}^{5/2-3/2}}':unit(a,r'\int \frac{1}{{x}^{'+str((m+2)/2)+'-'+str(m/2)+'}}'),
      r'\int \frac{1}{x}\,\text{d}x-5\int':unit(a,r'\int \frac{1}{x}\,\text{d}x')+'-'+tex(b)+r'\int',
      '-5{x}^{-1}':'-'+tex(b)+'{x}^{-1}',r'-5\int':'-'+tex(b)+r'\int',
      r'-4\int':tex(a-b)+r'\int','-4ln':tex(a-b)+'ln'}
 elif name=='q-29836':
  f=a/(d*X)+b*X;bank=[L+(b+4)/2*X**2,a/d*L+b/2*X**2,(a+4)/d*L+d/2*X**2,d/a*L+X**2/2,a/d*L+d/2*X**2];good=1
  mp={r'\frac{3}{5x}':r'\frac{'+str(a)+'}{'+str(d)+'x}',' + 3x':' + '+tex(b)+'x'}
 elif name=='q-29857':
  f=a/X-b/s.sqrt(X);bank=[a*L-2*b/X,b*L-b*s.sqrt(X),X-2*b*s.sqrt(X),a*L-2*b*s.sqrt(X),b*L+2*b*s.sqrt(X)];good=3
  mp={r'\frac{2}{x}':r'\frac{'+str(a)+'}{x}',r'\frac{1}{\sqrt{x}}':r'\frac{'+str(b)+r'}{\sqrt{x}}'}
 else:raise ValueError(name)
 prompt=clean(replace_tokens(source[':question/problem'],mp))
 if ':question/worked-solution' in source:solution=clean(replace_tokens(source[':question/worked-solution'],mp))
 else:
  # Explicit authored completion, not claimed as observed source solution.
  if name=='q-29836':rows=[r'\int ('+r'\frac{'+str(a)+'}{'+str(d)+'x}+'+tex(b)+r'x)\,\text{d}x & =\int '+r'\frac{'+str(a)+'}{'+str(d)+r'x}\,\text{d}x+'+tex(b)+r'\int x\,\text{d}x',tex(a/d)+r'\int \frac{1}{x}\,\text{d}x+'+tex(b)+r'\int x\,\text{d}x',tex(a/d)+r'\ln|x|+'+tex(b)+r'\cdot\frac{x^{1+1}}{1+1}+C',canonical(bank[good])]
  else:rows=[r'\int ('+tex(a)+r'/x-'+tex(b)+r'/\sqrt{x})\,\text{d}x & ='+tex(a)+r'\int \frac{1}{x}\,\text{d}x-'+tex(b)+r'\int x^{-1/2}\,\text{d}x',tex(a)+r'\ln|x|-'+tex(b)+r'\cdot\frac{x^{-1/2+1}}{-1/2+1}+C',canonical(bank[good])]
  solution='Applying the sum and constant factor rules, we get\n\n'+aligned(rows)
 return prompt,solution,f,bank,good

def canonical(v,bare_log=False):
 t=tex(v)
 if not bare_log:
  t=re.sub(r'\\ln\{\\left\(([^()]*) \\right\)\}',lambda m:m[0] if '|' in m[1] else r'\ln|'+m[1].strip()+'|',t)
 return t+'+C' 
def derivative(e):
 e=e.replace(lambda z:z.func==s.log and z.args[0].func==s.Abs,lambda z:s.log(z.args[0].args[0]))
 return s.cancel(s.diff(e,X))

def domain(level,template=None):
 names=[template] if template else [k for k,t in TEMPLATES.items() if t['level']==level]
 rows=[]
 for name in names:
  spec=TEMPLATES[name]
  if spec['level']!=level:raise ValueError('template/level mismatch')
  keys=list(spec['slots'])
  for values in itertools.product(*spec['slots'].values()):
   p=dict(zip(keys,values))
   if name=='q-49100' and math.gcd(p['a'],p['c'])!=1:continue
   if name=='q-29915' and p['b']<=p['a']:continue
   if name=='q-103374' and p['b']==p['d']:continue
   if name=='q-29836' and p['a']==p['b'] and p['d']==p['a']+4:continue
   rows.append(p if template else {'template':name,'parameters':p})
 return rows
# Freeze bounded valid domains once; explicit callers cannot bypass these guards.
DOMAINS={k:domain(t['level'],k) for k,t in TEMPLATES.items()}
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+':'+v))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
@fmt.checked_math_content
def generate(level,seed=0,template=None,parameters=None,profile=None,field_type=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio'):raise ValueError('source uses radio fields only')
 if profile is not None:
  if template is not None and template!=profile:raise ValueError('profile belongs to another template')
  template=profile
 names=[k for k,t in TEMPLATES.items() if t['level']==level]
 if template is not None and template not in names:raise ValueError('template/level mismatch')
 name=template or names[seed%len(names)];spec=TEMPLATES[name]
 if parameters is None:p=dict(DOMAINS[name][(seed//len(names) if template is None else seed)%len(DOMAINS[name])])
 else:
  p=dict(parameters)
  if any(type(value) not in (int,str) for value in p.values()) or p not in DOMAINS[name]:raise ValueError('parameters outside bounded valid domain')
 prompt,solution,f,bank,good=build(name,p)
 prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution)
 values=[fmt.normalize_tex(canonical(e,bare_log=(name=='q-29836' and i in (0,4)) or (name=='q-29885' and i==2))) for i,e in enumerate(bank)]
 fingerprint=digest([name,p]);content=digest([prompt,solution,values])
 qid=uid(content);fid=uid(qid+':selection');answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct=answers[good][':answer/id'];random.Random(seed).shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':SOURCE['record'][':knowledge-point/id'],'title':SOURCE['record'][':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':name,'bank_profile':name,'parameters':p,'parameter_fingerprint':fingerprint,'mathematical_task_fingerprint':digest(s.srepr(s.expand(f))),'source_analysis':{'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'question_ids':[name]},'calibration':spec.get('calibration','observed difficulty'),'authored_solution':':question/worked-solution' not in Q[name],'domain':'x>0 for radicals/fractional powers; x!=0 for integer rational forms, on connected intervals avoiding poles','plot_rating':'none','dependency_versions':{'sympy':s.__version__}}}
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
GENERATORS={'easy':generate_easy,'moderate':generate_moderate,'hard':generate_hard}
def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
 rows=['## '+g['template']+' — '+q[':question/difficulty'].split('/')[-1],json.dumps(g['parameters']),q[':question/problem']]
 for a in f[':answer-field/choices']:rows.append('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else ''))
 return '\n\n'.join(rows+[q[':question/worked-solution']])
def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--difficulty',choices=['all',*GENERATORS],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['json','markdown'],default='markdown');a.add_argument('--template',choices=list(TEMPLATES));a.add_argument('--profile',choices=list(BANK_PROFILES));args=a.parse_args()
 if args.count<1 or args.difficulty=='all' and (args.template or args.profile):a.error('positive count and specific difficulty required for template/profile')
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (GENERATORS if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
