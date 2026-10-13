#!/usr/bin/env python3
"""Exact nontrigonometric parameter elimination, steps 3–7 only.

Observed templates are compiled from the immutable basis-1356 capture. Every
mathematical fragment is evaluated as a coordinate-substitution recipe: old
x=(x-h)/a, a positive integer. The same invertible substitution transforms the
parameter equations, every solution stage and complete observed banks. a=1,h=0
is normal recipe replay, not a literal-question branch. Canonical Cartesian
relations are independently derived from the parameterization, never correct IDs.

Three native coefficient families additionally sample easy quadratic, moderate
factored quadratic and hard fractional-linear substitution at source workloads.
The two empirical banks q15653/q6828 are explicit raw replay profiles only;
authored default banks use complete, method-based operations. Raw source-error
profiles are evidence, never random learner output. See evidence README.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json, random, re, sys, uuid
import sympy as sp
HERE=Path(__file__).resolve().with_suffix('')
sys.path.insert(0,str(HERE))
from math_parser import expression, X, Y, T
KP=17592186100889
SNAPSHOT=json.loads((HERE/'source.json').read_text())
RECORD=SNAPSHOT['record']; TITLE=RECORD[':knowledge-point/title'];VERSION='algebra-cartesian-1'
SOURCE={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions']}
# Input parametrizations and exact real domains are independent of choice IDs.
# Tuples: x(t), y(t), parameter domain, exact x image, isolation target.
def complement(a,b):return sp.Complement(a,b,evaluate=False)
SPECS={
'q-15678':(1/(T-2),T**2,complement(sp.S.Reals,sp.FiniteSet(2)),complement(sp.S.Reals,sp.FiniteSet(0)),1),
'q-15755':(T-2,T**2,sp.S.Reals,sp.S.Reals,1),
'q-102664':(1-2*T,(T-2)**2*(T+1),sp.S.Reals,sp.S.Reals,1),
'q-102668':((T-5)/2,(T**2-25)*(T-4),sp.S.Reals,sp.S.Reals,1),
'q-15653':(5-T,T**2-1,sp.S.Reals,sp.S.Reals,1),
'q-15654':(sp.sqrt(T),T*(9-T),sp.Interval(0,sp.oo),sp.Interval(0,sp.oo),1),
'q-15677':(1/(T+1),1/(T-2),complement(sp.S.Reals,sp.FiniteSet(-1,2)),complement(sp.S.Reals,sp.FiniteSet(0,sp.Rational(1,3))),1),
'q-276277':(T+1,T**2+4,sp.S.Reals,sp.S.Reals,1),
'q-276284':(1/(T-4),T/(2*T+1),complement(sp.S.Reals,sp.FiniteSet(4,-sp.Rational(1,2))),complement(sp.S.Reals,sp.FiniteSet(0,-sp.Rational(2,9))),1),
'q-320871':(T-2,T**2-4,sp.S.Reals,sp.S.Reals,1),
'q-320926':(1/(T+3),T/(-2*T+1),complement(sp.S.Reals,sp.FiniteSet(-3,sp.Rational(1,2))),complement(sp.S.Reals,sp.FiniteSet(0,sp.Rational(2,7))),1),
'q-321074':((T+1)/3,(T**2-4)*(1-T)**2,sp.S.Reals,sp.S.Reals,1),
'q-321075':((1-T)/4,(T**2-1)*(1+T)**2,sp.S.Reals,sp.S.Reals,1),
'q-321084':(sp.sqrt(T+1),T*(4-T),sp.Interval(0,sp.oo),sp.Interval(1,sp.oo),1),
'q-321090':(sp.sqrt(T**2-9),3*T**2,sp.Interval(3,sp.oo),sp.Interval(0,sp.oo),2),
'q-321141':(1/(2*T+1),(T+1)**2,complement(sp.S.Reals,sp.FiniteSet(-sp.Rational(1,2))),complement(sp.S.Reals,sp.FiniteSet(0)),1),
'q-321410':(-3*T+2,-1/T,complement(sp.S.Reals,sp.FiniteSet(0)),complement(sp.S.Reals,sp.FiniteSet(2)),1),
'q-6828':(T**2+5,1/T**2,complement(sp.S.Reals,sp.FiniteSet(0)),sp.Interval.open(5,sp.oo),2),
'q-6830':(sp.sqrt(T**2-4),2*T**2,sp.Interval(2,sp.oo),sp.Interval(0,sp.oo),2),
'q-276278':(2*T+5,(T-2)*(T+1),sp.S.Reals,sp.S.Reals,1),
'q-320878':(3*T-1,(T+5)*(T-2),sp.S.Reals,sp.S.Reals,1),
}
# Same Markdown/value layout pairs; retained source profiles remain distinct.
GROUP={'q-320871':'q-276277','q-320878':'q-276278'}
TEMPLATES={}
for sid,q in SOURCE.items():
 name=GROUP.get(sid,sid).replace('q-','observed_');level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]
 TEMPLATES.setdefault(name,{'level':level,'sources':[],'origin':'observed','field_type':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].split('/')[-1]})['sources'].append(sid)
for name,level in [('native_quadratic','easy'),('native_factors','moderate'),('native_fractional','hard')]:TEMPLATES[name]={'level':level,'sources':[],'origin':'authored native coefficient extension','field_type':'blank'}
EMPIRICAL={'q-15653','q-6828'}
RAW_UNSAFE={'q-15678','q-6828'}
# Shared exact mathematics, Markdown compilation and identity helpers.
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+digest(v)))
def tex(e):return sp.latex(e).replace(r'\left','').replace(r'\right','')
def coordinate(p):
 n=X-p['h'];return tex(n) if p['a']==1 else r'\frac{'+tex(n)+'}{'+str(p['a'])+'}'
def transform(text,p):
 """Compile each math island; prose/layout stays fixed, x is an actual operand."""
 u=coordinate(p)
 def sub(m):
  body=m.group(2)
  # Group a nontrivial substitution so powers/implicit products remain correct.
  replacement='x' if p['a']==1 and p['h']==0 else '('+u+')'
  return m.group(1)+re.sub(r'(?<![A-Za-z])x(?![A-Za-z])',lambda _:replacement,body)+m.group(1)
 return re.sub(r'(\$\$|\$)(.*?)(?:\1)',sub,text,flags=re.S)
def transform_value(value,p):
 return transform('$'+value+'$',p)[1:-1]
def derive(xt,yt,power,p):
 z=sp.Symbol('z',real=True);xb=(X-p['h'])/p['a']
 if power==2:
  xe=xt.subs(T**2,z);ye=yt.subs(T**2,z)
  # Generic radical and quadratic source equations.
  if xt.is_Pow and xt.exp==sp.Rational(1,2):inverse=sp.solve(sp.Eq(xb**2,xt.base.subs(T**2,z)),z)[0]
  else:inverse=sp.solve(sp.Eq(xb,xe),z)[0]
  return sp.factor(ye.subs(z,inverse)),inverse
 roots=sp.solve(sp.Eq(xb,xt),T)
 if len(roots)!=1:raise ValueError('Template does not have one supported inverse')
 return sp.factor(yt.subs(T,roots[0])),roots[0]
def image(base,p):
 if base==sp.S.Reals:return base
 if isinstance(base,sp.Interval):return sp.Interval(p['a']*base.start+p['h'],p['a']*base.end+p['h'],base.left_open,base.right_open)
 excluded=base.args[1];return complement(sp.S.Reals,sp.FiniteSet(*[p['a']*v+p['h'] for v in excluded]))
def rhs_value(value):
 # Complete equations include comma-separated domain; a fragment never does.
 return expression(re.split(r',|\\,',value.split('=',1)[1] if '=' in value else value,maxsplit=1)[0].strip())
def repaired_source(sid,profile):
 q=SOURCE[sid];problem=q[':question/problem'];solution=q.get(':question/worked-solution')
 fields=[{'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'values':[a[':answer/value']for a in f[':answer-field/choices']],'source_correct':f.get(':answer-field/correct',{}).get(':answer/id'),'source_ids':[a[':answer/id']for a in f[':answer-field/choices']]} for f in q[':question/answer-fields']]
 if solution is None:
  solution='To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$\n\n$$\nx=t-2\\,⇒\\,t=x+2\n$$\n\nNow, substituting $t=x+2$ into our expression for $y,$ we get\n\n$$\ny=(x+2)^{2}\n$$\n\nSo, the complete Cartesian equation is $y=(x+2)^{2},\\,x\\in (-\\infty,\\infty).$'
 if profile!='raw_observed':
  if sid=='q-15678':fields[0]['values']=[v.replace(r'{(\frac{-1-2x}{x})}^{2}',r'(\frac{-1-2x}{x})')for v in fields[0]['values']]
  if sid=='q-6828':
   solution=solution.replace(r'x\ne 5',r'x>5').replace('we must have $x>5.$','we must have $x>5$ because $t^{2}>0.$')
   fields[0]['values']=[v.replace(r'x\ne 5',r'x>5')for v in fields[0]['values']]
 return problem,solution,fields

def assemble(level,template,profile,p,problem,solution,fields,math,seed):
 identity_fields=sorted([{'key':f['key'],'type':f['type'],'values':sorted(f['values']),'correct_value':f['values'][f['correct_index']]}for f in fields],key=lambda f:f['key'])
 content={'version':VERSION,'prompt':problem,'solution':solution,'fields':identity_fields};fp=digest(content);qid=uid(content)
 owned=[]
 for i,f in enumerate(fields):
  fid=uid([qid,'field',f['key']]);answers=[];seen={}
  for v in f['values']:
   occurrence=seen.get(v,0);seen[v]=occurrence+1;answers.append({':answer/id':uid([fid,'answer',v,occurrence]),':answer/type':':answer.type/math',':answer/value':v})
  owned.append({':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':f['type'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[f['correct_index']][':answer/id']]})
 response=sorted([(f['key'],f['type'],str(sp.cancel(sp.expand(rhs_value(f['values'][f['correct_index']])))) if f['type'].endswith('/blank') else 'whole_equation')for f in fields])
 task={'relation':str(sp.factor(math['relation'])),'domain':str(math['x_domain']),'response':response,'parameterization':{'x_t':str(sp.cancel(sp.expand(math['x_t']))),'y_t':str(sp.cancel(sp.expand(math['y_t']))),'t_domain':str(math['t_domain'])}}
 # Coefficient-normalized y-RHS is canonical across factor/expanded templates.
 task['relation']=str(sp.cancel(sp.expand(math['relation'])))
 outmath={k:str(v)for k,v in math.items()}
 return {'knowledge_point':{'db_id':KP,'id':RECORD[':knowledge-point/id'],'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':owned},'generation':{'version':VERSION,'provenance':{k:SNAPSHOT[k]for k in ('database','basis','lineage')},'seed':seed,'dependency_versions':{'python':sys.version.split()[0],'sympy':sp.__version__},'template':template,'profile':profile,'bank_profile':profile,'parameters':p,'mathematics':outmath,'content_fingerprint':fp,'parameter_fingerprint':digest(task),'origin':TEMPLATES[template]['origin'],'plot_rating':'none','raw_evidence_only':profile=='raw_observed' and p.get('source_id') in RAW_UNSAFE}}

def observed(level,template,seed,p,profile):
 sid=p['source_id'];xt,yt,td,xd,power=SPECS[sid];relation,inverse=derive(xt,yt,power,p)
 problem,solution,fields=repaired_source(sid,profile)
 if profile=='authored_method' and sid in EMPIRICAL:
  xb=X
  if sid=='q-15653':bank=[(5-xb)**2-1,-((5-xb)**2-1),(5+xb)**2-1,xb**2+24,xb**2-10*xb+25];dom=r'x\in (-\infty,\infty)'
  else:bank=[1/(xb-5),1/(xb+5),-1/(xb-5),1/(xb-5)**2,1/xb];dom=r'x>5'
  fields[0]['values']=['y='+tex(v)+r',\,'+dom for v in bank];fields[0]['source_ids']=[];fields[0]['source_correct']=None
 for f in fields:
  vals=[transform_value(v,p)for v in f['values']]
  if f['type'].endswith('/radio'):
   indices=[i for i,v in enumerate(vals)if sp.simplify(rhs_value(v)-relation)==0]
   if profile=='raw_observed' and sid=='q-15678':index=f['source_ids'].index(f['source_correct'])
   elif len(indices)==1:index=indices[0]
   else:raise ValueError('Whole bank has nonunique correct value')
  else:
   # Domain blanks expect source-coordinate endpoint because prompt explicitly
   # transforms the coordinate expression too. Derive that point from exclusions.
   if f['key']=='field-1':expected=relation
   else:
    den=sp.denom(sp.cancel(xt));excluded=[]
    for bad_t in td.args[1]:
     if den.subs(T,bad_t)!=0:excluded.append(sp.simplify(xt.subs(T,bad_t)))
    if sp.degree(den,T)>0:excluded.append(sp.limit(xt,T,sp.oo))
    excluded=list(set(excluded));expected=next(v for v in excluded if v!=0)if len(excluded)>1 else excluded[0]
   assert sp.simplify(rhs_value(vals[0])-expected)==0;index=0
  f.update(values=vals,correct_index=index);f.pop('source_ids');f.pop('source_correct')
 return assemble(level,template,profile,p,transform(problem,p),transform(solution,p),fields,{'relation':relation,'inverse':inverse,'x_t':p['a']*xt+p['h'],'y_t':yt,'t_domain':td,'x_domain':image(xd,p),'isolation_power':power},seed)

# Easy native coefficients: one affine isolation and quadratic substitution.
# Moderate native coefficients: same isolation, two factor substitutions, denominator square.
# Hard native coefficients: reciprocal inverse, rational simplification, two exclusions.
def native(level,template,seed,p):
 # EASY: affine isolation followed by one quadratic substitution.
 if template=='native_quadratic':
  b,c=p['b'],p['c'];xt=T+b;yt=T**2+c;inv=X-b;rel=sp.expand(inv**2+c);td=xd=sp.S.Reals
  stages=[tex(inv**2+c),tex(rel)];param='x='+tex(xt)+r',\,y='+tex(yt)+r',\,t\in(-\infty,\infty)'
  suffix='.';fields=[{'key':'field-1','type':':answer-field.type/blank','values':[tex(rel)],'correct_index':0}]
 # MODERATE: substitute into both factors and retain factored form.
 elif template=='native_factors':
  a,b,u,v=(p[k]for k in ('a','b','u','v'));xt=a*T+b;yt=(T-u)*(T-v);inv=(X-b)/a;rel=sp.factor((inv-u)*(inv-v));td=xd=sp.S.Reals
  stages=['('+tex(inv-u)+')('+tex(inv-v)+')',tex(rel)];param='x='+tex(xt)+r',\,y=('+tex(T-u)+')('+tex(T-v)+r'),\,t\in(-\infty,\infty)'
  suffix='.';fields=[{'key':'field-1','type':':answer-field.type/blank','values':[tex(rel)],'correct_index':0}]
 # HARD: reciprocal inverse, rational simplification and two exclusions.
 else:
  h,c,d=(p[k]for k in ('h','c','d'));xt=1/(T-h);yt=T/(c*T+d);inv=h+1/X;rel=sp.cancel(yt.subs(T,inv));bad=-sp.Rational(c,c*h+d);td=complement(sp.S.Reals,sp.FiniteSet(h,-sp.Rational(d,c)));xd=complement(sp.S.Reals,sp.FiniteSet(0,bad))
  stages=[r'\frac{'+tex(inv)+'}{'+str(c)+'('+tex(inv)+')+'+tex(d)+'}',tex(rel)];param='x='+tex(xt)+r',\,y='+tex(yt)+r',\,t\ne '+tex(h)+r',\,t\ne '+tex(-sp.Rational(d,c))
  suffix=r'$,\,x\ne $'+'\n{{field-2}}'+r'$,\,x\ne 0.$';fields=[{'key':'field-1','type':':answer-field.type/blank','values':[tex(rel)],'correct_index':0},{'key':'field-2','type':':answer-field.type/blank','values':[tex(bad)],'correct_index':0}]
 problem='Consider the curve defined parametrically as\n\n$$\n'+param+'.\n$$\n\nThe Cartesian equation of this curve is\n\n$y=$\n{{field-1}}'+suffix
 solution='To find the Cartesian equation, we eliminate $t.$ First, we use the $x$ equation to solve for $t:$\n\n$$\n'+tex(xt)+'=x\\,⇒\\,t='+tex(inv)+'\n$$\n\nNow, substituting $t='+tex(inv)+'$ into our expression for $y,$ we get\n\n$$\n'+r'\begin{aligned}y & ='+(r' \\ & ='.join(stages))+r'\end{aligned}'+'\n$$'
 if template=='native_fractional':solution+='\n\nFinally, the excluded values of $t$ give $x\\ne 0$ and $x\\ne '+tex(bad)+'$. Therefore, the complete Cartesian equation is $y='+tex(rel)+r',\,x\ne '+tex(bad)+r',\,x\ne 0.$'
 return assemble(level,template,'authored_native',p,problem,solution,fields,{'relation':rel,'inverse':inv,'x_t':xt,'y_t':yt,'t_domain':td,'x_domain':xd,'isolation_power':1},seed)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 rng=random.Random(seed);eligible=[k for k,s in TEMPLATES.items()if s['level']==level and (field_type is None or s['field_type']==field_type)]
 if profile is not None:
  if profile=='authored_native':eligible=[k for k in eligible if not TEMPLATES[k]['sources']]
  elif profile=='authored_method':eligible=[k for k in eligible if any(sid in EMPIRICAL for sid in TEMPLATES[k]['sources'])]
  elif profile in ('raw_observed','repaired_observed'):
   eligible=[k for k in eligible if TEMPLATES[k]['sources'] and (parameters is not None or not any(sid in EMPIRICAL for sid in TEMPLATES[k]['sources']))]
  else:raise ValueError('Unknown bank profile')
 if not eligible:raise ValueError('No eligible template for level/field/profile')
 if template is None:template=rng.choice(eligible)
 if template not in eligible:raise ValueError('Template/level/field mismatch')
 spec=TEMPLATES[template]
 if spec['sources']:
  if parameters is None:
   sid=rng.choice(spec['sources']);p={'source_id':sid,'a':rng.randint(1,7),'h':rng.randint(-9,9)}
  else:p=dict(parameters)
  if set(p)!={'source_id','a','h'}or p['source_id']not in spec['sources']or type(p['a'])is not int or not 1<=p['a']<=12 or type(p['h'])is not int or not -20<=p['h']<=20:raise ValueError('Invalid explicit source parameters')
  sid=p['source_id'];profile=profile or ('authored_method'if sid in EMPIRICAL else'repaired_observed')
  if profile not in ('raw_observed','repaired_observed','authored_method'):raise ValueError('Unknown source profile')
  if profile=='raw_observed'and sid in EMPIRICAL and (p['a']!=1 or p['h']!=0):raise ValueError('Underdetermined empirical source banks are explicit original-parameter replay only')
  if profile=='repaired_observed'and sid in EMPIRICAL:raise ValueError('Empirical source bank requires raw_observed replay or authored_method')
  if profile=='authored_method'and sid not in EMPIRICAL:raise ValueError('Profile not eligible')
  return observed(level,template,seed,p,profile)
 if profile not in (None,'authored_native'):raise ValueError('Unknown native profile')
 if parameters is None:
  if template=='native_quadratic':p={'b':rng.choice([i for i in range(-8,9)if i]),'c':rng.randint(-12,12)}
  elif template=='native_factors':
   u,v=rng.sample(range(-5,6),2);p={'a':rng.choice([-4,-3,-2,2,3,4]),'b':rng.randint(-8,8),'u':u,'v':v}
  else:
   p={'h':rng.choice([-5,-4,-3,-2,2,3,4,5]),'c':rng.choice([-3,-2,-1,1,2,3]),'d':rng.choice([-3,-2,-1,1,2,3])}
   while p['c']*p['h']+p['d']==0:p['d']=rng.choice([-3,-2,-1,1,2,3])
 else:p=dict(parameters)
 keys={'native_quadratic':{'b','c'},'native_factors':{'a','b','u','v'},'native_fractional':{'h','c','d'}}[template]
 if set(p)!=keys or any(type(v)is not int or abs(v)>20 for v in p.values()):raise ValueError('Invalid native parameters')
 if template=='native_quadratic'and p['b']==0:raise ValueError('Native quadratic requires a nonzero shift')
 if template=='native_factors'and (p['a']==0 or p['u']==p['v']):
  raise ValueError('Noninvertible or duplicate native factors')
 if template=='native_fractional'and (p['c']==0 or p['d']==0 or p['c']*p['h']+p['d']==0):raise ValueError('Degenerate fractional template')
 return native(level,template,seed,p)
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];out=q[':question/problem']+'\n\n'
 for f in q[':question/answer-fields']:
  out+='Field '+f[':answer-field/key']+' ('+f[':answer-field/type'].split('/')[-1]+')\n'
  for a in f[':answer-field/choices']:out+='- $'+a[':answer/value']+'$'+(' **correct**'if a[':answer/id']==f[':answer-field/correct'][1]else'')+'\n'
 return out+'\n'+q[':question/worked-solution']+'\n'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile)for level in (['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty])for i in range(args.count)]
 print(json.dumps(records,indent=2)if args.format=='json'else'\n\n---\n\n'.join(markdown(r)for r in records))
if __name__=='__main__':main()
