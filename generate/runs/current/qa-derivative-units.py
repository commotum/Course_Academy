"""Root declared-unit algebra, scale fidelity and full printed stage audit."""
import importlib.util,itertools,json,re
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186064271;D=R.parents[2]/f'generate/scratch/{K}'
sp=importlib.util.spec_from_file_location('root_unit_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
m,t,l,d,e,f,pt=s.symbols('mass time length dollar euro fahrenheit point',positive=True)
UNITS={'gram':m,'kilogram':1000*m,'ton':10**6*m,'meter':l,'centimeter':l/100,'liter':l**3/1000,'milliliter':l**3/10**6,'second':t,'minute':60*t,'hour':3600*t,'dollar':d,'euro':e,'degree fahrenheit':f,'point':pt}
for word in ('cupcake','visitor','visit','item','package','student','ticket'):UNITS[word]=s.Symbol(word,positive=True)
def unit(raw):
 raw=raw.lower().strip().strip(' ."').removeprefix('metric ')
 if ' per ' in raw:
  a,b=raw.split(' per ',1);return s.cancel(unit(a)/unit(b))
 power=1
 for prefix,n in [('squared ',2),('cubic ',3)]:
  if raw.startswith(prefix):power=n;raw=raw[len(prefix):]
 for suffix,n in [(' squared',2),(' cubed',3)]:
  if raw.endswith(suffix):power=n;raw=raw[:-len(suffix)]
 if raw=='degrees fahrenheit':raw='degree fahrenheit'
 elif raw.endswith('s'):raw=raw[:-1]
 assert raw in UNITS,raw;return UNITS[raw]**power
def same(a,b):return s.cancel(a-b)==0
def group(text,start):
 assert text[start]=='{';depth=0
 for n in range(start,len(text)):
  if text[n]=='{':depth+=1
  elif text[n]=='}':
   depth-=1
   if not depth:return text[start+1:n],n+1
 raise AssertionError(text)
def ratio(raw):
 raw=raw.strip().rstrip('.,').replace(r'\dfrac',r'\frac')
 if raw.startswith(r'\text{'):
  body,end=group(raw,5);assert end==len(raw);return unit(body)
 assert raw.startswith(r'\frac'),raw
 a,end=group(raw,5);b,end2=group(raw,end);assert end2==len(raw),raw;return s.cancel(ratio(a)/ratio(b))
def printed(prompt):
 def match(pattern):
  z=re.search(pattern,prompt);assert z,prompt;return z.groups()
 if 'farmer' in prompt:
  out,inp=match(r'\$w\(p\)\$ metric (.*?) of crops at a price of \$p\$ (.*?)\.');return 'w','p',unit(out),unit(inp)
 if 'pail' in prompt:
  inp,out=match(r'\$t\$ (.*?) after.*?\$V\(t\)\$ (.*?)\.');return 'V','t',unit(out),unit(inp)
 if 'website' in prompt:
  out,inp=match(r'\$v\(h\)\$ (.*?) every \$h\$ (.*?)\.');return 'v','h',unit(out),unit(inp)
 if 'parents' in prompt:
  out,inp=match(r'\$R\(p\)\$ (.*?) if.*?\$p\$ (.*?) in');return 'R','p',unit(out),unit(inp)
 if 'bakes' in prompt:
  inp,out=match(r'\$c\$ (.*?) using \$f\(c\)\$ (.*?) of flour');return 'f','c',unit(out),unit(inp)
 if 'dairy' in prompt:
  out,inp=match(r'\$p\(v\)\$ (.*?), where.*?number of (.*?) of milk');return 'p','v',unit(out),unit(inp)
 if 'battery' in prompt:
  out,inp=match(r'\$L\(t\)\$ (.*?) when.*?\$t\$ (.*?)\.');return 'L','t',unit(out),unit(inp)
 if 'bank exchanges' in prompt:
  inp,out=match(r'\$D\$ (.*?) for \$E\(D\)\$ (.*?)\.');return 'E','D',unit(out),unit(inp)
 if 'coffee' in prompt:
  inp,out=match(r'\$t\$ (.*?) after.*?\$F\(t\)\$ (.*?)\.');return 'F','t',unit(out),unit(inp)
 if 'production' in prompt:
  out,inp=match(r'\$Q\(x\)\$ (.*?) of material to make \$x\$ (.*?)\.');assert 'student' not in inp;return 'Q','x',unit(out),unit(inp)
 out,inp=match(r'\$Q\(x\)\$ (.*?) of a product at a price of \$x\$ (.*?)\.');return 'Q','x',unit(out),unit(inp)
C=dict(instances=0,values=0,unit_stages=0,source_questions=0,source_values=0,source_banks=0,source_existing_refs=0,source_missing_refs=0,source_fieldless=0,source_exact_prompts=0,source_exact_solutions=0,raw_invalid_banks=0,raw_visit_unit_defects=0)
def check(r):
 q=r['question'];dep,ind,out,inp=printed(q[':question/problem']);target=s.cancel(out/inp);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];vv=[unit(z[':answer/value']) for z in choices];assert len(vv)==5
 assert all(not same(a,b) for n,a in enumerate(vv) for b in vv[:n]);good=[same(z,target) for z in vv];raw=r['generation']['profile']=='raw_observed'
 if raw:assert sum(good)==0 and ':answer-field/correct' not in f;C['raw_invalid_banks']+=1
 else:assert sum(good)==1 and good[next(n for n,z in enumerate(choices) if z[':answer/id']==f[':answer-field/correct'][1])]
 worked=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',worked,re.S);assert len(blocks)==2
 raw_visit='website' in q[':question/problem'] and r['generation']['profile']=='observed'
 expected_out=UNITS['visitor'] if raw_visit else out
 first=blocks[0].split(chr(92)*2);assert len(first)==2
 for row in first:
  name,body=row.split(':',1);actual=ratio(body.replace('&','').strip());expected=expected_out if '(' in name else inp;assert same(actual,expected),(row,actual,expected);C['unit_stages']+=1
 actual_derivatives=re.findall(r'\\frac\{d([A-Za-z])\}\{d([A-Za-z])\}',worked.replace(r'\text{d}','d'));assert actual_derivatives and all(z==(dep,ind) for z in actual_derivatives)
 for part in blocks[1].split('&',1)[1].strip().split('='):
  assert same(ratio(part),expected_out/inp),(part,target);C['unit_stages']+=1
 quoted=re.search(r'is measured in "([^"]+)"',worked);assert quoted and same(unit(quoted[1]),expected_out/inp)
 if raw_visit:C['raw_visit_unit_defects']+=1
 level=q[':question/difficulty'].split('/')[-1]
 if level=='hard':assert same(inp*out, next(z for z in (d,e) if same(inp*out,z)))
 C['instances']+=1;C['values']+=len(vv);return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];q=check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile'))));assert q[':question/problem']==old[':question/problem'];C['source_exact_prompts']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_exact_solutions']+=1
 if not old.get(':question/answer-fields'):C['source_fieldless']+=1;C['source_missing_refs']+=1
 for of,nf in zip(old.get(':question/answer-fields',[]),q[':question/answer-fields']):
  assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in nf[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(of[':answer-field/choices'])
  if of.get(':answer-field/correct'):
   actual=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]);assert actual==of[':answer-field/correct'][':answer/value'];C['source_existing_refs']+=1
  else:C['source_missing_refs']+=1
 C['source_questions']+=1
review=json.loads((D/'review.json').read_text())
for r in review if isinstance(review,list) else review['generated']:check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for template,definition in g.DEFS.items():
 keys=list(definition['eligible'])
 for values in itertools.product(*(definition['eligible'][key] for key in keys)):
  parameters=dict(definition['parameters']);parameters.update(zip(keys,values))
  if template=='cupcake':parameters['alt']='kilogram' if parameters['u']=='gram' else 'gram'
  if template=='milk':parameters['alt']='milliliter' if parameters['v']=='liter' else 'liter'
  check(g.generate(g.TEMPLATES[template]['level'],template=template,parameters=parameters,profile='authored_default'))
for u,v,power in itertools.product(('centimeter','meter'),('item','package','ticket','cupcake'),(2,3)):
 check(g.generate('moderate',template='non_time_power',parameters={'u':u,'v':v,'power':power}))
for u,v in itertools.product(('ton','kilogram','liter','meter','item','package','ticket','cupcake'),('dollar','euro')):
 check(g.generate('hard',template='price_rate',parameters={'u':u,'v':v,'power':1}))
C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
