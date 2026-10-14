#!/usr/bin/env python3
"""Private fail-closed printed mathematics, source fidelity, scope/native validator."""
import copy,hashlib,importlib.util,itertools,json,platform,re,subprocess,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor,rationalize
ROOT=Path(__file__).parent
spec=importlib.util.spec_from_file_location('segment_generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,t,u=g.x,g.y,g.t,g.u

def group(s,start):
 if s[start]!='{':raise AssertionError('TeX group required '+s[start:])
 n=1;i=start+1
 while i<len(s) and n:
  if s[i]=='{':n+=1
  if s[i]=='}':n-=1
  i+=1
 if n:raise AssertionError('unclosed group')
 return s[start+1:i-1],i

def math(s):
 """Independent recursive TeX reader, with Euler e explicitly identified.

It consumes actual learner strings, not generator expressions, and refuses
unknown TeX commands or leftover math-layout syntax.
"""
 s=s.strip().rstrip('.,');s=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','(E)',s);s=s.replace('⁡','').replace('−','-').replace('′',"'")
 for old in [r'\left',r'\right',r'\,',r'\;',r'\!',r'\quad',r'\displaystyle']:s=s.replace(old,'')
 s=s.replace(r'\operatorname{tan}',r'\tan').replace(r'{sec}',r'\sec').replace(r'\pi','pi').replace(r'\cdot','*')
 for op in ['frac','sqrt']:
  marker='\\'+op
  while marker in s:
   at=s.index(marker);atgroup=at+len(marker)
   arg,end=group(s,atgroup)
   if op=='frac':arg2,end=group(s,end);rep='(('+str(math(arg))+')/('+str(math(arg2))+'))'
   else:rep='sqrt('+str(math(arg))+')'
   s=s[:at]+rep+s[end:]
 s=s.replace(r'\sec','sec').replace(r'\tan','tan')
 s=s.replace('{','(').replace('}',')').replace('^','**')
 s=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','E',s)
 if '\\' in s or '&' in s or '|' in s:raise AssertionError('unconsumed notation '+s)
 loc={'x':x,'y':y,'t':t,'u':u,'E':S.E,'pi':S.pi,'sqrt':S.sqrt,'exp':S.exp,'sec':S.sec,'tan':S.tan}
 try:v=parse_expr(s,local_dict=loc,transformations=standard_transformations+(implicit_multiplication_application,convert_xor,rationalize),evaluate=True)
 except Exception as e:raise AssertionError('unreadable '+s) from e
 # Determine sec² from original operator when no exponent survives normalization.
 return v

def scalar(s):
 s=s.replace('{sec}',r'\sec').replace('⁡','').replace(r'\left','').replace(r'\right','')
 pattern=re.compile(r'\\sec\s*\^\s*(?:\{2\}|2)\s*')
 while (m:=pattern.search(s)):
  start=m.end()
  if s[start]=='{':
   arg,j=group(s,start)
  elif s[start]=='(':
   n=1;j=start+1
   while j<len(s) and n:
    if s[j]=='(':n+=1
    elif s[j]==')':n-=1
    j+=1
   if n:raise AssertionError('trig argument balance')
   arg=s[start+1:j-1]
  else:raise AssertionError('sec argument missing')
  s=s[:m.start()]+r'(\sec('+arg+r'))^{2}'+s[j:]
 return math(s)

def eq(a,b,label):
 d=S.simplify(a-b)
 if d!=0:raise AssertionError(label+': '+str(d))

def formatting(q):
 for value in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in value),'control character'
  # Count TeX group braces; escaped visible brace glyphs are excluded.
  n=0
  for c in re.sub(r'\\[{}]','',value):
   if c=='{':n+=1
   elif c=='}':n-=1
   assert n>=0,'closing group'
  assert n==0,'brace balance'
  assert len(re.findall(r'(?<!\\)\$',value))%2==0,'math delimiter parity'
  assert not re.search(r'\{\{[A-Za-z_]+\}\}',value),'unfilled slot'

def prompt(r):
 q=r['question'];text=q[':question/problem'];f=r['generation']['template']
 coords=re.findall(r'\$\((-?\d+),\s*(-?\d+)\)(?:\.)?\$',text)
 assert len(coords)==2,'two printed endpoints'
 a,b=map(S.Integer,coords[0]);A,B=map(S.Integer,coords[1]);X=a+(A-a)*t;Y=b+(B-b)*t
 if 'f(x,y)=' in text:fn=text.split('f(x,y)=',1)[1].split('$',1)[0]
 elif 'f(x, y) = ' in text:fn=text.split('f(x, y) = ',1)[1].split('$',1)[0]
 else:
  s=text.split('$',1)[1];fn=re.split(r'\\(?:mathrm|text)\{d\}s',s)[0]
  fn=re.sub(r'^\{?\\int\s*\}?_\{?C\}?\s*','',fn).rstrip('\\,')
 fn=scalar(fn);speed=S.sqrt((A-a)**2+(B-b)**2);assert speed>0
 pulled=S.simplify(fn.subs({x:X,y:Y},simultaneous=True))
 # Reference antiderivative constructed from printed function. No instance metadata.
 if f=='matched_exponential':
  inner=S.expand(X*Y);fac=S.simplify(pulled/S.exp(inner));eq(fac,S.diff(inner,t),'printed quadratic derivative-matching')
  P=S.exp(inner)
 elif f=='secant':
  inner=list(fn.atoms(S.sec))[0].args[0].subs({x:X,y:Y},simultaneous=True);inner=S.expand(inner)
  L,H=inner.subs(t,0),inner.subs(t,1);assert min(L,H)>-S.pi/2 and max(L,H)<S.pi/2
  P=S.tan(inner)/S.diff(inner,t)
 elif f=='exponential':
  inner=list(fn.atoms(S.exp))[0].args[0].subs({x:X,y:Y},simultaneous=True);P=S.exp(inner)/S.diff(inner,t)
 elif f=='radical':
  # printed radicand and path include real t >= 0; endpoint zero is allowed.
  powers=[v for v in fn.atoms(S.Pow) if v.exp==S.Rational(1,2) and v.base.has(y)];assert len(powers)==1
  rad=powers[0].base.subs({x:X,y:Y},simultaneous=True);assert rad.subs(t,0)>=0 and rad.subs(t,1)>=0
  P=S.integrate(pulled,t)
 else:P=S.integrate(pulled,t)
 eq(S.diff(P,t),pulled,'reference primitive')
 value=S.simplify(speed*(P.subs(t,1)-P.subs(t,0)))
 return dict(a=a,b=b,dx=A-a,dy=B-b,X=X,Y=Y,fn=fn,pulled=pulled,speed=speed,P=P,value=value)

def normal_stages(r,z):
 sol=r['question'][':question/worked-solution'];f=r['generation']['template']
 # Read back prose x(t),y(t), the substituted and expanded pullback, every
 # definite-integral row, actual primitive, each signed endpoint, and conclusion.
 X=scalar(re.search(r'\$x=(.*?)\$',sol).group(1));Y=scalar(re.search(r'\$y=(.*?)\$',sol).group(1));eq(X,z['X'],'x prose');eq(Y,z['Y'],'y prose')
 blocks=re.findall(r'\$\$\n\\begin\{aligned\}([\s\S]*?)\\end\{aligned\}\n\$\$',sol)
 assert len(blocks)==(5 if f in ['secant','matched_exponential'] else 4),'family block count'
 rows=lambda b:re.split(r'\s*\\\\\s*',b)
 # parameter-vector last row and derivative-vector row read coefficients separately.
 def vector(v):
  v=v.split('& =')[-1].strip();m=re.fullmatch(r'(.*?)\\,i\+\((.*?)\)\\,j',v);assert m,'vector form '+v
  return scalar(m[1]),scalar(m[2])
 vx,vy=vector(rows(blocks[0])[-1]);eq(vx,X,'param vector x');eq(vy,Y,'param vector y')
 dr=rows(blocks[1]);vx,vy=vector(dr[2]);eq(vx,z['dx'],'derivative x');eq(vy,z['dy'],'derivative y')
 eq(scalar(dr[-1].split('& =')[-1]),z['speed'],'speed final')
 eq(scalar(dr[-2].split('& =')[-1]),z['speed'],'speed squared components')
 pull=rows(blocks[2]);assert len(pull)==2
 for row in pull:eq(scalar(row.split('& =')[-1]),z['pulled'],'actual pulled row')
 if f=='product':assert 't^{2}' in pull[-1] or 't^2' in pull[-1],'required quadratic expansion'
 if f=='matched_exponential':assert ')e^{' in pull[-1],'required derivative factor/exponent collection'
 ir=rows(blocks[3]);assert len(ir)>=3
 # Direct pulled integrand row and extracted common-factor row.
 for row in ir[1:3]:
  rhs=row.split('& =')[-1].strip()
  m=re.fullmatch(r'(.*?)\\int_0\^1\s*\((.*?)\)(?:\\cdot\s*(.*?))?\\,\\mathrm\{d\}t',rhs)
  assert m,'integral row unreadable '+rhs
  fac=scalar(m[1]) if m[1] else S.Integer(1);integrand=scalar(m[2]);extra=scalar(m[3]) if m[3] else 1
  eq(fac*integrand*extra,z['speed']*z['pulled'],'printed weighted integrand')
 if f in ['secant','matched_exponential']:
  sub=re.search(r'\$u=(.*?)\,\$.*?\$\\mathrm\{d\}u=\((.*?)\)\\,\\mathrm\{d\}t\$',sol)
  assert sub,'substitution prose'
  inner=scalar(sub[1]);du=scalar(sub[2]);eq(S.diff(inner,t),du,'substitution chain rule')
  evalrows=rows(blocks[4]);assert len(evalrows)==(5 if f=='secant' else 4)
  row=evalrows[0].split('& =')[-1]
  m=re.fullmatch(r'(.*?)\\int_\{(.*?)\}\^\{(.*?)\}(.*?)\\,\\mathrm\{d\}u',row)
  assert m,'substitution integral row'
  fac=scalar(m[1]);L,H=scalar(m[2]),scalar(m[3]);integrand=scalar(m[4]);eq(L,inner.subs(t,0),'sub lower');eq(H,inner.subs(t,1),'sub upper');eq(fac*integrand.subs(u,inner)*du,z['speed']*z['pulled'],'substitution integrand')
  primitive=evalrows[1].split('& =')[-1];m=re.fullmatch(r'(.*?)\[(.*?)\]_\{(.*?)\}\^\{(.*?)\}',primitive);assert m,'u primitive stage'
  pref=scalar(m[1]);Pu=scalar(m[2]);eq(S.diff(Pu,u),integrand,'displayed u primitive');eq(scalar(m[3]),L,'u primitive lower');eq(scalar(m[4]),H,'u primitive upper');eq(pref,fac,'u primitive factor')
  endpoint=scalar(evalrows[2].split('& =')[-1]);eq(endpoint,z['value'],'signed endpoint row')
  if f=='secant':eq(scalar(evalrows[3].split('& =')[-1]),z['value'],'tan endpoint exact values')
  eq(scalar(evalrows[-1].split('& =')[-1]),z['value'],'conclusion')
 else:
  assert len(ir)==6,'primitive family rows'
  row=ir[3].split('& =')[-1];m=re.fullmatch(r'(.*?)\[(.*?)\]_0\^1',row);assert m,'t primitive'
  fac=scalar(m[1]);P=scalar(m[2]);eq(fac*S.diff(P,t),z['speed']*z['pulled'],'actual displayed primitive')
  # Read plus and minus endpoint components independently before subtracting.
  row=ir[4].split('& =')[-1];assert '-' in row,'signed endpoint row'
  # rightmost minus separates the lower endpoint (all normal prefixes are nonnegative speeds).
  depth=0;cuts=[]
  for j,c in enumerate(row):
   if c in '({[':depth+=1
   elif c in ')}]':depth-=1
   elif c=='-' and depth==0:cuts.append(j)
  assert cuts,'top-level signed lower endpoint'
  cut=cuts[-1];upper=scalar(row[:cut]);lower=scalar(row[cut+1:]);eq(upper,fac*P.subs(t,1),'positive endpoint');eq(lower,fac*P.subs(t,0),'negative endpoint');eq(upper-lower,z['value'],'endpoint difference')
  eq(scalar(ir[-1].split('& =')[-1]),z['value'],'final answer')

def record(r,stages=True):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];formatting(q);z=prompt(r);field=q[':question/answer-fields'][0];assert field[':answer-field/type']==':answer-field.type/radio';assert len(field[':answer-field/choices'])==5
 values=[scalar(a[':answer/value']) for a in field[':answer-field/choices']]
 corrects=[i for i,v in enumerate(values) if S.simplify(v-z['value'])==0];assert len(corrects)==1,'unique semantic correct'
 for i,j in itertools.combinations(range(5),2):
  assert S.simplify(values[i]-values[j])!=0,'equivalent pair'
  d=S.N(values[i]-values[j],80);assert d.is_real and abs(d)>S.Float('1e-45'),'precision/domain separation'
 if ':answer-field/correct' in field:assert field[':answer-field/correct'][1]==field[':answer-field/choices'][corrects[0]][':answer/id'],'semantic key'
 else:assert r['generation']['evidence_only'],'normal missing key'
 if stages and not r['generation']['evidence_only']:normal_stages(r,z)
 return z

def dump(name,data):(ROOT/name).write_text(json.dumps(data,indent=2)+'\n')

def main():
 source=json.load(open(ROOT/'source.json'));assert source['basis']==2275
 qs=source['record'][':knowledge-point/questions'];originals=[];cases=[];source_counts={'questions':0,'banks':0,'choices':0,'designations':0,'available_solutions':0,'missing_designations':0,'raw_omission_checks':0}
 for q in qs:
  sid=q[':question/math-academy-id'];level,f,p=g.ANCHORS[sid];r=g.generate(level,17,parameters=p,profile='source:'+sid);record(r,False)
  assert r['question'][':question/problem']==q[':question/problem'],'raw prompt fidelity'
  assert r['question'].get(':question/worked-solution')==q.get(':question/worked-solution'),'full solution fidelity'
  ff=q[':question/answer-fields'][0];rr=r['question'][':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in ff[':answer-field/choices'])==sorted(a[':answer/value'] for a in rr[':answer-field/choices'])
  for key in [':question/difficulty',':question/worked-solution']:assert (key in q)==(key in r['question']);source_counts['raw_omission_checks']+=1
  assert (':answer-field/correct' in ff)==(':answer-field/correct' in rr);source_counts['raw_omission_checks']+=1
  source_counts['questions']+=1;source_counts['banks']+=1;source_counts['choices']+=5
  if ':answer-field/correct' in ff:
   cor=next(a for a in rr[':answer-field/choices'] if a[':answer/id']==rr[':answer-field/correct'][1]);assert cor[':answer/value']==ff[':answer-field/correct'][':answer/value'];source_counts['designations']+=1
  else:source_counts['missing_designations']+=1
  if ':question/worked-solution' in q:source_counts['available_solutions']+=1
  originals.append(r);cases.append({'source_id':sid,'template':f,'parameters':p,'bank_profile':'source:'+sid,'authored_level':level if ':question/difficulty' not in q else None})
 dump('source-cases.json',cases)
 # Sample every family explicitly and default routing; exercise actual printed
 # mathematics rather than compare the output against generation metadata.
 variants=[];coverage={};native=[];sample_count=0;fingerprints={};slot_values={}
 for level,fs in g.FAMILIES.items():
  fingerprints[level]=set();coverage[level]={};slot_values[level]={}
  for family in fs:
   coverage[level][family]=0
   for seed in range(35):
    r=g.generate(level,seed,template=family);record(r);sample_count+=1;fingerprints[level].add(r['generation']['mathematical_fingerprint']);coverage[level][family]+=1
    for k,v in r['generation']['parameters'].items():slot_values[level].setdefault(k,set()).add(v)
    if seed<2:variants.append(r)
    ff=r['question'][':question/answer-fields'][0];checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ff[':answer-field/correct'][1] else 'rejected','purpose':'native radio selection; separate printed scalar proof'} for a in ff[':answer-field/choices']]
    if seed<2:native.append({'label':level+'/'+family+'/'+str(seed),'record':r,'checks':checks})
  selected=set()
  for seed in range(100):
   r=g.generate(level,seed);selected.add(r['generation']['template'])
  assert selected==set(fs),'default family coverage'
 # Evidence raw replay native fixtures infer a key only in memory, retaining raw
 # public records and unknown-original-designation counts separately.
 for r in originals:
  fixture=copy.deepcopy(r);ff=fixture['question'][':question/answer-fields'][0];ff.setdefault(':answer-field/correct',[':answer/id',r['generation']['inferred_correct_id']])
  native.append({'label':'source/'+r['generation']['source_id'],'record':fixture,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ff[':answer-field/correct'][1] else 'rejected','purpose':'explicitly inferred memory-only fixture key where original absent'} for a in ff[':answer-field/choices']]})
 # Seed/order excluded from identity with fixed mathematics and profile.
 for r in variants:
  lev=r['question'][':question/difficulty'].split('/')[-1];p=r['generation']['parameters'];family=r['generation']['template']
  other=g.generate(lev,990,template=family,parameters=p)
  assert other['question'][':question/id']==r['question'][':question/id'];assert other['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
 # Deliberate regressions must fail closed, including final-only masking errors.
 mutation_tests=[]
 def mutation(name,r,edit):
  rr=copy.deepcopy(r);edit(rr)
  try:record(rr)
  except (AssertionError,ValueError,TypeError):mutation_tests.append(name);return
  raise AssertionError('mutation accepted '+name)
 mutation('stale x prose',variants[0],lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('$x=', '$x=1+',1)))
 mutation('wrong printed xy substitution',next(r for r in variants if r['generation']['template']=='product'),lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('f(r(t)) & =','f(r(t)) & =2+',1)))
 mutation('control character',variants[0],lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\x0c'))
 mutation('duplicate wrong/wrong',variants[0],lambda r:r['question'][':question/answer-fields'][0][':answer-field/choices'][1].__setitem__(':answer/value',r['question'][':question/answer-fields'][0][':answer-field/choices'][2][':answer/value']))
 # Hard explicit derivative/scope controls and zero segment rejection.
 bad=[]
 for level,f,p in [('hard','matched_exponential',dict(a=0,b=1,dx=0,dy=0)),('moderate','radical',dict(a=2,b=0,dx=0,dy=-2,k=2)),('hard','secant',dict(a=0,b=0,dx=1,dy=5,n=8)),('easy','linear',dict(a=0,b=0,dx=2,dy=2,c=10,d=2))]:
  try:g.generate(level,parameters=p,template=f)
  except ValueError:bad.append(f)
  else:raise AssertionError('invalid parameters accepted')
 dump('engine-input.json',native)
 result=subprocess.run([str(Path('generate/runs/current/check-engine')) ,str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],capture_output=True,text=True);assert result.returncode==0,result.stderr
 dump('review.json',{'originals':originals,'generated_variants':variants})
 review=['# Draft review\n\nBasis 2275. Raw source profiles are evidence-only. Generated method banks are authored. Parent QA remains pending.\n']
 for r in originals+variants:
  meta=r['generation'];review.append('\n## '+('Original '+meta['source_id'] if meta['source_id'] else 'Generated '+r['question'][':question/difficulty'].split('/')[-1]+' / '+meta['template'])+'\n\n'+g.markdown(r))
 (ROOT/'review.md').write_text('\n'.join(review))
 report={'status':'worker_verified_pending_parent_QA','source':source_counts,'normal_printed_math_samples':sample_count,'per_family_coverage':coverage,'sampled_mathematical_fingerprints':{k:len(v) for k,v in fingerprints.items()},'slot_coverage':{l:{k:sorted(v) for k,v in d.items()} for l,d in slot_values.items()},'native':json.load(open(ROOT/'engine-report.json')),'mutation_rejections':mutation_tests,'explicit_scope_rejections':bad,'runtime':{'python':platform.python_version(),'sympy':S.__version__},'source_wrapper_sha256':hashlib.sha256((ROOT/'source.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'native_binary_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'unresolved':['Two source keys/ratings/solutions absent; no matched designation or solution claimed.','Opaque scalar source-bank author intentions unresolved; evidence profiles ineligible for learning.','Hard exponential raw solution omits its linear factor in one integral label; raw preserved, normal label repaired.','Calculator flags not captured; unknown.']}
 dump('validation.json',report)
 print(json.dumps({k:v for k,v in report.items() if k not in ['slot_coverage','native']},indent=2))
if __name__=='__main__':main()
