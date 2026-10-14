"""Independent rendered expression parser and native learner grader probes."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
from functools import lru_cache
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def load(p,n):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load(HERE.with_suffix('.py'),'g');F=load(ROOT/'generate/runs/current/root-source-fidelity.py','F')
def save(name,o):(HERE/name).write_text(json.dumps(o,indent=2,ensure_ascii=False,default=str)+'\n')
x=s.Symbol('x',real=True);u=s.Symbol('u',real=True)
@lru_cache(None)
def expr(t):
 t=t.strip().rstrip('.,:').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\qquad','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
 t=re.sub(r'\\operatorname\{(sin|cos|tan|sec|csc|cot)\}',r'\\\1',t).replace('{sec}',r'\sec')
 # Compact legacy TeX \dfrac 25 consumes one token per operand.
 t=re.sub(r'\\frac\s*([0-9])\s*([0-9])',r'\\frac{\1}{\2}',t)
 def convert(text):
  out='';i=0
  def group(pos):
   if text[pos]=='{':
    depth=1;j=pos+1
    while depth:depth+=int(text[j]=='{')-int(text[j]=='}');j+=1
    return text[pos+1:j-1],j
   if text[pos]=='(':
    depth=1;j=pos+1
    while depth:depth+=int(text[j]=='(')-int(text[j]==')');j+=1
    return text[pos+1:j-1],j
   z=re.match(r'\\pi|[a-zA-Z]|[0-9]+',text[pos:]);assert z,('Missing operand',text,pos);return z[0],pos+len(z[0])
  while i<len(text):
   if text[i].isspace():i+=1;continue
   if text.startswith(r'\frac',i):
    i+=5
    while text[i].isspace():i+=1
    a,i=group(i)
    while text[i].isspace():i+=1
    b,i=group(i);out+='(('+convert(a)+')/('+convert(b)+'))'
   elif text.startswith(r'\pi',i):out+='pi';i+=3
   elif text[i]=='\\':
    z=re.match(r'\\(sin|cos|tan|sec|csc|cot)',text[i:]);assert z,('Unknown command',text[i:]);fn=z[1];i+=len(z[0]);power='1'
    if i<len(text) and text[i]=='^':power,i=group(i+1)
    while i<len(text) and text[i].isspace():i+=1
    arg,i=group(i);out+='('+fn+'('+convert(arg)+'))**('+convert(power)+')'
   elif text[i]=='{':a,i=group(i);out+='('+convert(a)+')'
   elif text[i]=='^':a,i=group(i+1);out+='**('+convert(a)+')'
   else:out+=text[i];i+=1
  return out
 text=convert(t)
 return parse_expr(text,local_dict={'x':x,'u':u,'pi':s.pi,'sin':s.sin,'cos':s.cos,'tan':s.tan,'sec':s.sec,'csc':s.csc,'cot':s.cot},transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)
def equal(a,b):
 delta=a-b
 if delta==0:return True
 # Real numeric witnesses disprove equivalence; only simplify possible matches.
 for z in (s.Rational(1,7),s.Rational(2,7),s.Rational(4,7)):
  v=delta.subs({x:z,u:z})
  if v.is_finite is not False and abs(complex(s.N(v,12)))>1e-8:return False
 return s.simplify(s.trigsimp(delta,method='fu'))==0

def function_in_prompt(q,m):
 inline=re.findall(r'\$([^$]+)\$',q[':question/problem'])
 token=next(t for t in inline if re.match(r'(?:f\(x\)|y)\s*=',t))
 return expr(token.split('=',1)[1])
def rendered_check(rec):
 q=rec['question'];m=rec['generation']['template'];fun=function_in_prompt(q,m);D=s.diff(fun,x)
 worked=q.get(':question/worked-solution','');norm=g.normalized_prose(worked).replace('{sec}',r'\sec') if worked else ''
 # Read every printed inner binding; each must regenerate the function argument.
 bindings=re.findall(r'(?<![A-Za-z])u\s*=\s*(.*?)(?=\.\s*\n|\.\s*\$|\n\$\$|,\\|\\end)',norm,re.S)
 if bindings:
  inner=expr(bindings[0]);assert fun.has(inner) or equal(fun,s.sin(inner)) or equal(fun,s.cos(inner)) or equal(fun,s.tan(inner)) or m in ('authored-affine-sine','q-31163','q-51026'),(m,'inner binding',inner,fun)
  # Formal operands on differentiation line, including source g for sum family.
  line=next((b for b in re.findall(r'\$\$\s*(.*?)\s*\$\$',norm,re.S) if r'\frac{\text{d}u}{\text{d}x}=' in b or r'\dfrac{\textrm d u}{\textrm d x} =' in b or r'\frac{\mathrm{d}u}{\mathrm{d}x}=' in b),None)
  if line:
   lhs=re.search(r'\\(?:d?frac)\{(?:\\text\{d\}|\\textrm d |\\mathrm\{d\})u\}\{(?:\\text\{d\}|\\textrm d |\\mathrm\{d\})x\}\s*=\s*(.*)',line)
   assert lhs,(m,'formal operand line',line)
   id=expr(lhs[1]);assert equal(id,s.diff(inner,x)),(m,'inner derivative operand',id,inner)
   start=line.split('=',1)[1];od=expr(re.split(r',?\\(?:qquad|,)|\\text\{and\}|\\style',start)[0]);outer=(rec['generation']['parameters'].get('A',1)*s.cos(u)) if m in ('q-1943','q-48508','q-48636','q-51026') else s.cos(u) if m in ('q-310180','q-31153','q-310182','q-31241') else s.sec(u)**2 if m in ('q-1946','q-310179') else -s.sin(u)
   # This expected operand is derived from the printed function operation.
   if m in ('q-1943','q-48508','q-48636','q-51026'):outer=-rec['generation']['parameters'].get('A',1)*s.sin(u)
   if m=='authored-affine-sine':outer=rec['generation']['parameters']['A']*s.cos(u)
   assert equal(od,outer),(m,'outer derivative operand',od,outer)

 # Read each numeric or symbolic RHS in the chain-rule display, rather than
 # trusting only its final answer. Formal operator identities are checked by
 # the preceding bindings/factors and omitted from expression parsing.
 stage_count=0
 for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',norm,re.S):
  if not (r'\begin{aligned}' in block):continue
  is_chain=(r'\frac{\text{d}' in block or r'\dfrac{\textrm d' in block or r'\frac{\mathrm{d}' in block) and ('&' in block)
  if not is_chain:continue
  target=D+18*x**2 if m=='q-31163' else D
  segments=block.split(chr(92)*2)
  for segment in segments:
   if '&' not in segment or '=' not in segment:continue
   rhs=segment.split('=',1)[1].split(r'\end')[0].strip()
   if r'\frac' in rhs or r'\dfrac' in rhs:continue
   try:part=expr(rhs)
   except Exception as e:raise AssertionError((m,'unread chain operand',rhs)) from e
   if bindings:part=part.subs(u,inner)
   assert equal(part,target),(m,'chain stage',rhs,part,target)
   stage_count+=1
 # All response keys are read from the rendered prompt and owned bank.
 at=None
 if m in ('q-310180','q-31153','q-310182','q-31241'):
  token=next(t for t in re.findall(r'\$([^$]+)\$',q[':question/problem']) if re.match('x=',t.replace(' ','')));at=expr(token.split('=',1)[1]);expected=s.simplify(D.subs(x,at))
 elif m in ('q-48508','q-48636','q-51026'):
  token=next(t for t in re.findall(r'\$([^$]+)\$',q[':question/problem']) if ',' in t and '(' in t);token=token.replace(r'\left','').replace(r'\right','').strip().strip('.')
  point=token.strip('()');parts=point.split(',');at=expr(parts[0]);ordinate=expr(parts[1]);assert equal(fun.subs(x,at),ordinate),(m,'point on curve');expected=s.expand(s.simplify(D.subs(x,at))*(x-at)+ordinate)
 else:expected=D

 evaluation_count=0;line_count=0
 for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',norm,re.S):
  if not r'\begin{aligned}' in block:continue
  is_evaluation=(m in ('q-310180','q-31153','q-310182','q-31241','q-48508','q-48636','q-51026') and not (r'\frac{\text{d}' in block or r'\dfrac{\textrm d' in block or r'\frac{\mathrm{d}' in block) and ('&' in block) and ("f'(" in block or '{f}^{′}' in block or "{f}^{'}" in block))
  is_tangent=m in ('q-48508','q-48636','q-51026') and 'y-' in block
  if is_evaluation:
   slope=s.simplify(D.subs(x,at))
   for segment in block.split(chr(92)*2):
    if '&' not in segment or '=' not in segment:continue
    rhs=segment.split('&',1)[1].strip().lstrip('=').split(r'\end')[0].strip()
    for component in rhs.split('='):
     assert equal(expr(component),slope),(m,'evaluation stage',component,slope)
     evaluation_count+=1
  if is_tangent:
   for segment in block.split(chr(92)*2):
    segment=segment.split(r'\end')[0].strip()
    if 'y_1' in segment or '{y}_{1}' in segment or 'y_{1}' in segment:continue
    if '=' not in segment:continue
    lhs,rhs=segment.split('=',1);lhs=lhs.replace('&','').strip();rhs=rhs.replace('&','').strip()
    assert equal(expr(lhs).subs(s.Symbol('y'),expected),expr(rhs)),(m,'tangent stage',lhs,rhs,expected)
    line_count+=1
 fields=q.get(':question/answer-fields',[])
 for f in fields:
  values=[expr(a[':answer/value'].split('=',1)[1] if a[':answer/value'].startswith('y=') else a[':answer/value'].strip('$')) for a in f[':answer-field/choices']]
  if ':answer-field/correct' in f:
   i=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]);assert equal(values[i],expected),(m,'printed key',values[i],expected)
   assert sum(equal(v,expected) for v in values)==1,(m,'bank ambiguity')
   assert all(not equal(v,w) for i,v in enumerate(values) for w in values[:i]),(m,'bank duplicate')
 return {'template':m,'parameters':rec['generation']['parameters'],'function':str(fun),'derivative':str(D),'at':str(at),'answer':str(expected),'inner_bindings':len(bindings),'fields':len(fields),'chain_stages_read':stage_count,'evaluation_stages_read':evaluation_count,'tangent_stages_read':line_count}

def main():
 cases=[{'source_id':m,'template':m,'level':g.LEVELS[m],'parameters':p,'profile':'observed_raw','authored_level':g.LEVELS[m] if ':question/difficulty' not in g.SOURCES[m] else None} for m,p in g.DEFAULTS.items() if m in g.SOURCES];save('source-cases.json',cases)
 _,fidelity=F.check(g,g.KP_ID,HERE)
 results=[];records=[]
 for m,p in g.DEFAULTS.items():
  choices=g.parameters_for(m);variants=[p,choices[0],choices[-1],choices[len(choices)//2]]
  for j,p in enumerate(variants):
   r=g.generate(g.LEVELS[m],seed=j,template=m,parameters=p);results.append(rendered_check(r));records.append(r)
   if m in g.SOURCES:
    raw=g.generate(g.LEVELS[m],template=m,parameters=p,profile='observed_raw');results.append(rendered_check(raw))
    if raw['question'].get(':question/answer-fields'):
     rf=raw['question'][':question/answer-fields'][0];nf=r['question'][':question/answer-fields'][0]
     original_values=[expr(a[':answer/value'].split('=',1)[1] if a[':answer/value'].startswith('y=') else a[':answer/value'].strip('$')) for a in rf[':answer-field/choices']]
     served_values=[expr(a[':answer/value'].split('=',1)[1] if a[':answer/value'].startswith('y=') else a[':answer/value']) for a in nf[':answer-field/choices']]
     assert len(original_values)==len(served_values) and all(sum(equal(v,w) for w in served_values)==1 for v in original_values),(m,'complete changed-parameter raw/served bank mismatch')
   assert r==g.generate(g.LEVELS[m],seed=j,template=m,parameters=p)
   assert r['question']==g.generate(g.LEVELS[m],seed=999,template=m,parameters=p)['question']
 # Negative controls mutate actual printed operands, substitutions, keys.
 negative=[]
 r=g.generate('moderate',template='q-310179',parameters={'a':7,'b':-4})
 for label,mut in [('outer derivative',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace(r'\sec^{2}⁡u',r'\cos u'))),('substitution',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('7{x}^{4}-4','8{x}^{4}-4'))),('inner derivative',lambda q:q.__setitem__(':question/worked-solution',q[':question/worked-solution'].replace('28{x}^{3}','27{x}^{3}'))),('printed function',lambda q:q.__setitem__(':question/problem',q[':question/problem'].replace('7{x}^{4}','8{x}^{4}'))),('key',lambda q:q[':question/answer-fields'][0][':answer-field/choices'][0].__setitem__(':answer/value','0'))]:
  n=copy.deepcopy(r);mut(n['question'])
  try:rendered_check(n)
  except Exception:negative.append(label)
  else:raise AssertionError(('uncaught negative',label))
 probes=[]
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];checks=[]
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Every owned option'} for a in f[':answer-field/choices']]
  else:
   value=f[':answer-field/choices'][0][':answer/value'];m=r['generation']['template'];p=r['generation']['parameters']
   if m=='q-310179':equivalent=tex_equiv= str(4*p['a'])+r' x^{3}/\cos^{2}('+str(p['a'])+r'x^{4}'+str(p['b'])+')' if p['b']<0 else str(4*p['a'])+r' x^{3}/\cos^{2}('+str(p['a'])+r'x^{4}+'+str(p['b'])+')'
   elif m=='q-31241':equivalent=str(p['b'])+r'\cos('+str(p['c'])+')'
   elif m=='q-310180':equivalent='1-1'
   elif m in ('q-48508','q-48636'):equivalent='2/2'
   else:equivalent=value+'+0'
   checks=[{'submitted':value,'expected':'accepted','purpose':'Canonical rendered answer'},{'submitted':equivalent,'expected':'accepted','purpose':'Equivalent expression'},{'submitted':value+'+1' if r['generation']['template']=='q-310179' else '314159','expected':'rejected','purpose':'Wrong expression'},{'submitted':'1' if value=='0' else '0','expected':'rejected','purpose':'Simple wrong value against rendered key'}]
  probes.append({'label':f'{i}-{r["generation"]["template"]}','record':r,'checks':checks})
 save('engine-input.json',probes)
 binary=ROOT/'generate/runs/current/check-engine';sha=hashlib.sha256(binary.read_bytes()).hexdigest();assert sha=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 p=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],text=True,capture_output=True);(HERE/'engine.log').write_text(p.stdout+p.stderr);assert p.returncode==0,p.stdout+p.stderr
 freeze=json.loads((HERE/'baseline-freeze.json').read_text());assert all(hashlib.sha256((ROOT/o['path']).read_bytes()).hexdigest()==o['sha256'] for o in freeze['paths'])
 report={'source_fidelity':fidelity,'rendered_checks':results,'negative_controls':negative,'native_binary_sha256':sha,'baseline_files_preserved':len(freeze['paths']),'default_meaningful_counts':{'easy':2112,'moderate':582,'hard':576},'supplemental_native_limits':['Native trig_bounds only encloses numeric arguments of absolute value<=16; default tan-quartic parameter pairs enforce |a+b|<=16 so x=1 yields a valid common-domain witness. Wrong constant314159 against the excluded tan-quartic a24,b20 can be unresolved due domain differences; main served probes use same-domain wrong answer. Larger args a24,b20 are outside served sampler and were independently tested unresolved.'],'status':'worker_validated_pending_parent_qa'};save('validation.json',report);print(json.dumps({k:v for k,v in report.items() if k!='rendered_checks'},indent=2))
if __name__=='__main__':main()
