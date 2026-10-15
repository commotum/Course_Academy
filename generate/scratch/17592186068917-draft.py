"""Private all-level generator; immutable registered package is never imported.

Source basis 2275. Source prose and ordered math cells are frozen per-family
masks, each rendered by the same parameter recipe, including original inputs.
Observed scalar banks have no recovered error interpretation: raw profiles are
ineligible evidence. Normal complete banks are method-derived. Easy is authored
from the immediately preceding nonlinear-product tutorial (exact derivative).
"""
import argparse,copy,hashlib,importlib.util,json,random,re,sys,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('');KP_ID=17592186068917
KP_UUID='d359337c-4ec2-5100-bdac-d0858619db3b';TITLE='Integrating Products Containing Trigonometric Functions Using Substitution'
VERSION='trig-products-private-2.0.0'
def load(file,name):
 spec=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=load(HERE/'frozen_math_format.py','trigproducts_format');printed=load(HERE/'printed.py','trigproducts_printed')
x=printed.x;u=printed.u;C=printed.C
SOURCE=json.loads((HERE/'source.json').read_text());SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
LEVELS={'q-13461':'moderate','q-13474':'moderate','q-13464':'moderate','q-13533':'hard','q-13537':'hard','q-3038':'hard','q-350202':'hard','q-350203':'hard','authored-easy':'easy'}
# A, inner coefficient k, power, trig family, transformed lower and upper / pi.
ANCHORS={'q-13461':(1,1,2,'sin',None,None),'q-13474':(4,1,3,'sec2',None,None),'q-13464':(1,1,2,'csc2',None,None),'q-13533':(5,2,2,'cos','0','1'),'q-13537':(3,2,2,'sin','0','2'),'q-3038':(1,1,-1,'sec2',None,None),'q-350202':(8,4,2,'sectan','0','1/3'),'q-350203':(12,6,2,'cos','1/2','1')}
OPS={'sin':s.sin(u),'cos':s.cos(u),'sec2':s.sec(u)**2,'csc2':s.csc(u)**2,'sectan':s.sec(u)*s.tan(u)}
PRIMS={'sin':-s.cos(u),'cos':s.sin(u),'sec2':s.tan(u),'csc2':-s.cot(u),'sectan':s.sec(u)}
SUPPORTED_LEVELS=('easy','moderate','hard');PROFILES=('observed_raw','authored_method')
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def tex(e):return s.latex(e)
def defaults(t):
 if t=='authored-easy':return dict(A=2,k=1,kind='cos')
 a,k,n,f,lo,hi=ANCHORS[t];return dict(A=a,k=k)
def domain(t,raw=False):
 if t=='authored-easy':return [dict(A=2*k,k=k,kind=f) for f in ('sin','cos') for k in range(1,13)]
 a,k,n,f,lo,hi=ANCHORS[t]
 # Evidence transport varies only the observed outer-amplitude slot. Keeping
 # its inner coefficient fixed avoids claiming recovered historical designs.
 if raw:return [dict(A=A,k=k) for A in range(1,13)]
 # Moderate always requires a nonunit adjustment; easy has exact derivative.
 return [dict(A=A,k=K) for A in range(1,13) for K in range(1,7) if raw or n<0 or lo is not None or s.Rational(A,n*K)!=1]
def model(t,p,raw=False):
 if t=='authored-easy':a,k,n,f,lo,hi=p['A'],p['k'],2,p['kind'],None,None
 else:
  _,_,n,f,lo,hi=ANCHORS[t];a=p['A'];k=p['k']
  # Same definite-integral method, nonzero endpoint difference; raw observed
  # banks retain original endpoints and are evidence-only.
  if not raw and t=='q-13533':lo='1/6';hi='1/2'
  if not raw and t=='q-13537':hi='1'
 inner=k*x**n;outer=a*x**(n-1) if n>0 else a/x**2
 h=OPS[f];H=PRIMS[f];ratio=s.cancel(outer/s.diff(inner,x));integrand=outer*h.subs(u,inner);F=ratio*H.subs(u,inner)
 ulo=None if lo is None else s.Rational(lo)*s.pi;uhi=None if hi is None else s.Rational(hi)*s.pi
 xl=None if lo is None else s.sqrt(ulo/k);xh=None if hi is None else s.sqrt(uhi/k)
 ans=F if lo is None else s.simplify(ratio*(H.subs(u,uhi)-H.subs(u,ulo)))
 return dict(a=a,k=k,n=n,f=f,inner=inner,outer=outer,h=h,H=H,r=ratio,I=integrand,F=F,ans=ans,lo=xl,hi=xh,ul=ulo,uh=uhi)
def intval(integrand,lo=None,hi=None,var='x'):
 limits='' if lo is None else '_{'+tex(lo)+'}^{'+tex(hi)+'}'
 return r'\int'+limits+' '+tex(integrand)+r'\,\text{d}'+var
def wrap(v):return r'\left('+tex(v)+r'\right)'
def general_cells(d,t):
 """Actual operative stages, including separated derivative factors/endpoints."""
 a,k,n,h,H,r,z=d['a'],d['k'],d['n'],d['h'],d['H'],d['r'],d['inner'];lo,hi,ul,uh=d['lo'],d['hi'],d['ul'],d['uh']
 I=intval(d['I'],lo,hi);differential_factor=s.cancel(x**(n-1)/s.diff(z,x)) if n>0 else -1/s.Integer(k)
 outside=x**(n-1) if n>0 else 1/x**2
 split=intval(s.Integer(1),lo,hi).replace(' 1', ' '+tex(a*h.subs(u,z))+r'\cdot '+tex(outside))
 # split is constructed as a product, not eagerly simplified by the CAS.
 transformed=intval(h,ul,uh,'u')
 substituted=(tex(a)+r'\int '+tex(h)+r'\cdot '+wrap(differential_factor)+r'\,\text{d}u') if lo is None else ('\\int_{'+tex(ul)+'}^{'+tex(uh)+'} '+tex(a*h)+r'\cdot '+wrap(differential_factor)+r'\,\text{d}u')
 extracted=tex(r)+r'\int'+('' if lo is None else '_{'+tex(ul)+'}^{'+tex(uh)+'}')+' '+tex(h)+r'\,\text{d}u'
 if lo is None:return [I,split,substituted,extracted,tex(r*H)+'+C',tex(d['ans'])+'+C']
 evaluated=tex(r*H)+r'\big|_{'+tex(ul)+'}^{'+tex(uh)+'}'
 endpoint=tex(r)+r'\left('+tex(H.subs(u,uh,simultaneous=True).func(uh,evaluate=False) if False else H.subs(u,uh,simultaneous=True))+r'-\left('+tex(H.subs(u,ul,simultaneous=True))+r'\right)\right)'
 # Keep function-at-endpoint notation separately from evaluated components.
 def at(q):return tex(H).replace('u',r'\left('+tex(q)+r'\right)')
 endpoint=tex(r)+r'\left('+at(uh)+r'-\left('+at(ul)+r'\right)\right)'
 values=tex(r)+r'\left('+tex(H.subs(u,uh))+r'-\left('+tex(H.subs(u,ul))+r'\right)\right)'
 final=tex(d['ans'])
 if t=='q-13533':return [I,split,substituted,extracted,evaluated,endpoint,tex(r)+r'\left('+tex(s.simplify(H.subs(u,uh)-H.subs(u,ul)))+r'\right)',final]
 if t=='q-13537':return [I,split,substituted,extracted,evaluated,endpoint,values,tex(r)+r'\cdot '+wrap(s.simplify(H.subs(u,uh)-H.subs(u,ul))),final]
 # Matching-derivative source blanks omit the redundant coefficient-extraction
 # row. Under changed coefficients keep the coefficient in its substituted row.
 return [I,split,extracted,evaluated,endpoint,values,final]
def source_cells(t):
 sol=SOURCES[t].get(':question/worked-solution','');m=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
 if not m:return []
 body=m[1].replace(r'\begin{aligned}','');rows=re.split(r'\\\\\s*',body)
 return [rows[0].split('&')[0].strip()]+[row.split('=',1)[1].strip() for row in rows]
def lexical(expression,reference,lexeme):
 """Reuse source typography for an unchanged *component*; never a payload.

 Math cells have independent parameterized masks. This preserves source number
 forms and conventions without an anchor branch around the generator.
 """
 return lexeme if expression==reference else expression
def solution(t,d,raw):
 if t=='authored-easy' or t=='q-13461':
  prefix='Let $u='+tex(d['inner'])+'.$ Differentiating, we have\n\n$$\n'+r'\frac{\text{d}u}{\text{d}x}='+tex(s.diff(d['inner'],x))+r'\,⟹\,'+tex(1/s.Integer(d['n']*d['k']))+r'\text{d}u='+tex(x**(d['n']-1))+r'\,\text{d}x.'+'\n$$\n\nUsing the above, we can write the integral in terms of $u$ and evaluate:\n\n'
  cells=general_cells(d,t)
  return prefix+'$$\n'+r'\begin{aligned}'+cells[0]+''.join((' &=' if i==1 else r' \\ &=')+cell for i,cell in enumerate(cells[1:],1))+r'\end{aligned}'+'\n$$'
 src=SOURCES[t][':question/worked-solution'];base=model(t,defaults(t),True)
 # Keep every original prose sentence and the entire ordered stage sequence.
 # Each full displayed math component is a slot, not a token-wide digit edit.
 cells=general_cells(d,t);bcells=general_cells(base,t);oldcells=source_cells(t)
 assert len(cells)==len(oldcells),(t,len(cells),len(oldcells))
 # Replace aligned expression cells simultaneously; source separators survive.
 oldblock=re.search(r'\\begin\{aligned\}.*\\end\{aligned\}',src,re.S).group()
 body=oldblock
 # Duplicate lexemes can appear in more than one slot, so replace by position.
 pattern=re.compile(r'\\begin\{aligned\}|\\end\{aligned\}')
 nested=oldblock.count(r'\begin{aligned}')
 inn=oldblock.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
 pieces=re.split(r'(\\\\\s*)',inn);row0=pieces[0];lhs,rest=row0.split('&',1)
 pieces[0]=lhs.replace(oldcells[0],lexical(cells[0],bcells[0],oldcells[0]))+'&'+rest.replace(oldcells[1],lexical(cells[1],bcells[1],oldcells[1]))
 for j in range(2,len(pieces),2):
  idx=j//2+1;pieces[j]=pieces[j].replace(oldcells[idx],lexical(cells[idx],bcells[idx],oldcells[idx]))
 block=r'\begin{aligned}'*nested+''.join(pieces)+r'\end{aligned}'*nested
 src=src.replace(oldblock,block)
 # First math block is the derivative and differential relation.
 oldder=re.search(r'\$\$\n(.*?)\n\$\$',src,re.S).group(1)
 if d['n']>0:
  derivative=tex(s.diff(d['inner'],x));outside=tex(x**(d['n']-1));dr=tex(s.Rational(1,d['n']*d['k']))
  der=r'\frac{\text{d}u}{\text{d}x}='+derivative+r'\,⟹\,'+dr+r'\text{d}u='+outside+r'\,\text{d}x.'
 else:der=r'\frac{\text{d}u}{\text{d}x}='+tex(s.diff(d['inner'],x))+r'\,⟹\,'+tex(-s.Rational(1,d['k']))+r'\text{d}u=\frac{1}{x^{2}}\,\text{d}x.'
 refd=general_derivative(base)
 der=lexical(der,refd,oldder);src=src.replace(oldder,der,1)
 # Entire initial u definition, including source typography at unchanged inner.
 initial=re.search(r'\$u=(.*?)\$',src).group(1);punct='.' if initial.endswith('.') else ','
 oldinner=initial[:-1] if initial[-1:] in '.,' else initial
 src=src.replace('$u='+initial+'$','$u='+lexical(tex(d['inner']),tex(base['inner']),oldinner)+punct+'$',1)
 if d['lo'] is not None:
  for row,key1,key2 in [('x','lo','hi'),('u','ul','uh')]:
   pat=re.compile(r'\| \$'+row+r'\$ \| \$(.*?)\$ \| \$(.*?)\$ \|')
   match=pat.search(src);vals=[lexical(tex(d[k]),tex(base[k]),match[i+1]) for i,k in enumerate((key1,key2))]
   src=src[:match.start()]+'| $'+row+'$ | $'+vals[0]+'$ | $'+vals[1]+'$ |'+src[match.end():]
 return src
def general_derivative(d):
 if d['n']>0:return r'\frac{\text{d}u}{\text{d}x}='+tex(s.diff(d['inner'],x))+r'\,⟹\,'+tex(s.Rational(1,d['n']*d['k']))+r'\text{d}u='+tex(x**(d['n']-1))+r'\,\text{d}x.'
 return r'\frac{\text{d}u}{\text{d}x}='+tex(s.diff(d['inner'],x))+r'\,⟹\,'+tex(-s.Rational(1,d['k']))+r'\text{d}u=\frac{1}{x^{2}}\,\text{d}x.'
def observed_bank(t,d):
 old=SOURCES[t][':question/answer-fields'][0];base=model(t,defaults(t),True);scale=s.cancel(d['r']/base['r']);out=[]
 for a in old[':answer-field/choices']:
  original=printed.scalar(a[':answer/value']).subs(C,0)
  changed=original.subs(x,(d['k']/s.Integer(base['k']))**s.Rational(1,base['n'])*x)*scale if base['n']>0 else original.subs(x,s.Rational(base['k'],d['k'])*x)*scale
  # Reconstruct with exact original function spelling when component unchanged.
  text=lexical(tex(changed)+('+C' if d['lo'] is None else ''),tex(original)+('+C' if d['lo'] is None else ''),a[':answer/value'])
  out.append(text)
 return out
def method_bank(d):
 r,H,z=d['r'],d['H'],d['inner']
 if d['lo'] is None:
  # Correct primitive; missed sign; missed derivative adjustment; applied inner
  # derivative twice; substituted a different primitive function.
  substitute={'sin':s.sin(u),'cos':s.cos(u),'sec2':s.sec(u),'csc2':-s.csc(u),'sectan':s.tan(u)}[d['f']]
  vals=[r*H,-r*H,d['a']*H,r*H/(abs(d['n'])*d['k']),r*substitute]
  vals=[v.subs(u,z) for v in vals]
 else:
  hu=H.subs(u,d['uh']);hl=H.subs(u,d['ul']);delta=s.simplify(hu-hl)
  # Endpoint reversal; omit derivative scale; apply derivative factor twice;
  # differentiate the basic trig primitive instead of integrating it.
  vals=[r*delta,-r*delta,d['a']*delta,r*delta/(d['n']*d['k']),r*s.simplify(d['h'].subs(u,d['uh'])-d['h'].subs(u,d['ul']))]
 return [tex(s.simplify(v))+('+C' if d['lo'] is None else '') for v in vals]
def exact_zero(expr):
 # Exact rational trig normalization on every supplied expression. Groebner
 # reduction uses sin²+cos²=1 independently per printed argument.
 expr=expr.replace(s.tan,lambda z:s.sin(z)/s.cos(z)).replace(s.cot,lambda z:s.cos(z)/s.sin(z)).replace(s.sec,lambda z:1/s.cos(z)).replace(s.csc,lambda z:1/s.sin(z))
 num=s.fraction(s.cancel(expr))[0]
 if num==0:return True
 args=sorted({v.args[0] for v in num.atoms(s.sin,s.cos)},key=str)
 if not args:return s.simplify(num)==0
 symbols=[s.Dummy('T'+str(i)) for i in range(2*len(args))]
 mapping={fn(z):symbols[2*i+j] for i,z in enumerate(args) for j,fn in enumerate((s.sin,s.cos))}
 polynomial=num.xreplace(mapping)
 try:
  gb=s.groebner([symbols[2*i]**2+symbols[2*i+1]**2-1 for i in range(len(args))],*symbols)
  return gb.reduce(polynomial)[1]==0
 except (s.PolynomialError,s.CoercionFailed):return s.simplify(num)==0
def valid_bank(values,indefinite):
 expr=[printed.scalar(v).subs(C,0) for v in values]
 for i,a in enumerate(expr):
  for b in expr[:i]:
   diff=s.diff(a-b,x) if indefinite else a-b
   if exact_zero(diff):return False
 return True
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS or type(seed) is not int:raise ValueError('level/seed')
 profile='authored_method' if profile is None else profile
 if profile not in PROFILES:raise ValueError('profile')
 rng=random.Random(seed);templates=[t for t in LEVELS if LEVELS[t]==level and (profile!='observed_raw' or t in SOURCES)]
 if template is not None and template not in templates:raise ValueError('template/difficulty')
 t=template or rng.choice(templates);raw=profile=='observed_raw'
 if parameters is not None:
  expected={'A','k','kind'} if t=='authored-easy' else {'A','k'}
  if not isinstance(parameters,dict) or set(parameters)!=expected or any(type(parameters[z]) is not int for z in ('A','k')) or 'kind' in parameters and type(parameters['kind']) is not str or parameters not in domain(t,raw):raise ValueError('parameters outside documented finite domain')
 candidates=[parameters] if parameters is not None else domain(t,raw);candidates=candidates.copy();rng.shuffle(candidates)
 for p in candidates:
  d=model(t,p,raw);blank=t in ('q-350202','q-350203')
  kind='blank' if blank else 'radio'
  if field_type is not None and field_type not in (kind,':answer-field.type/'+kind):raise ValueError('field_type')
  vals=observed_bank(t,d) if raw else ([tex(d['ans'])+('+C' if d['lo'] is None else '')] if blank else method_bank(d))
  if not valid_bank(vals,d['lo'] is None):
   if parameters is not None:raise ValueError('whole-bank ambiguity')
   continue
  break
 else:raise ValueError('no eligible complete bank')
 I=intval(d['I'],d['lo'],d['hi']);sol=solution(t,d,raw);key='field-1' if blank else 'selection'
 if raw:
  old=SOURCES[t];prompt=old[':question/problem'];base=model(t,defaults(t),True)
  # Entire integral is a single component slot; prose/layout is frozen.
  start=prompt.index('$');stop=prompt.rfind('$');math=prompt[start+1:stop]
  trailing='=' if math.endswith('=') else '.' if math.endswith('.') else ''
  new=I+trailing
  prompt=prompt[:start+1]+lexical(new,intval(base['I'],base['lo'],base['hi'])+trailing,math)+prompt[stop:]
  if ':question/worked-solution' not in old:sol=None
 else:
  prompt=('Evaluate the following integral. Give an exact answer.\n\n$'+I+'=$\n{{'+key+'}}') if blank else ('Calculate $'+I+'.$')
  sol=sol.replace('Do not round the answer.','Give an exact answer.')
  prompt=fmt.normalize_prose(prompt);sol=fmt.normalize_prose(sol)
  vals=[fmt.normalize_tex(v.replace(r'\u2061','⁡')) for v in vals]
 canonical=digest([s.srepr(d['I']),None if d['lo'] is None else s.srepr(d['lo']),None if d['hi'] is None else s.srepr(d['hi']),kind])
 identity=digest([VERSION,level,prompt,sol,sorted(vals)]);uid=lambda a:str(uuid.uuid5(uuid.UUID(KP_UUID),a))
 qid=uid(identity);fid=uid(identity+':field:'+key);answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
 target=d['ans'];matches=[a for a in answers if exact_zero(printed.scalar(a[':answer/value']).subs(C,0)-target)];assert len(matches)==1,(t,p,vals,target)
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
 if not raw or ':answer-field/correct' in SOURCES[t][':question/answer-fields'][0]:field[':answer-field/correct']=[':answer/id',matches[0][':answer/id']]
 rng.shuffle(answers);q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if sol is not None:q[':question/worked-solution']=sol
 if not raw or ':question/difficulty' in SOURCES[t]:q[':question/difficulty']=':question.difficulty/'+level
 rec={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':profile,'parameters':p,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'mathematical_fingerprint':canonical,'content_identity':identity,'evidence_only':raw,'eligible_for_learning':not raw,'authored_level':t=='authored-easy' or t=='q-13461','domain':'Connected real intervals avoiding trig poles; x != 0 in reciprocal substitution. Definite transformed intervals avoid poles.','dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}}
 if not raw:fmt.validate_generated_record(rec)
 return rec
# EASY: exact derivative factor, sin/cos of k*x^2; no coefficient isolation.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: sin/csc^2 quadratic or sec^2 cubic; nonunit ratio required.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: reciprocal with negative differential, or exact definite endpoints.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def batch(level,count,seed=0,template=None,profile=None):
 if level not in SUPPORTED_LEVELS or type(count) is not int or count<1 or type(seed) is not int:raise ValueError('batch')
 profile=profile or 'authored_method'
 if profile not in PROFILES:raise ValueError('profile')
 pool=[]
 for t in LEVELS:
  if LEVELS[t]!=level or template is not None and t!=template or profile=='observed_raw' and t not in SOURCES:continue
  pool.extend((t,p) for p in domain(t,profile=='observed_raw'))
 random.Random(seed).shuffle(pool);records=[];seen=set()
 for t,p in pool:
  try:r=generate(level,seed,t,parameters=p,profile=profile)
  except ValueError as e:
   if str(e)=='whole-bank ambiguity':continue
   raise
  fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:seen.add(fp);records.append(r)
  if len(records)==count:return records
 raise ValueError('finite unique domain capacity '+str(len(records)))
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[No captured worked solution.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=(*SUPPORTED_LEVELS,'all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=('markdown','json'),default='json');ap.add_argument('--template');ap.add_argument('--profile',choices=PROFILES);a=ap.parse_args()
 records=[r for level in (SUPPORTED_LEVELS if a.difficulty=='all' else [a.difficulty]) for r in batch(level,a.count,a.seed,a.template,a.profile)]
 print(json.dumps(records,ensure_ascii=False,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
