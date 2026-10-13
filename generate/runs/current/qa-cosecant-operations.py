"""Root reads given function values, shifted expressions and every equality."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','csc_operations_p');V=load(R/'qa-vector-line-stages.py','csc_operations_source');CS=s.Function('Cosecant');p.functions['csc']=CS;n=s.Symbol('n',integer=True);p.locals_['u']=n

def read(z):
 z=z.strip().strip('$').rstrip('.,?=').replace(r'\theta','x')
 z=re.sub(r'(?<![A-Za-z])theta(?![A-Za-z])','x',z)
 for var,target in [('a','x'),('t','x'),('n','u')]:z=re.sub(r'(?<![A-Za-z])'+var+r'(?![A-Za-z])',target,z)
 return p.scalar(z)
def normal(expr,value):
 mapping={p.y:value}
 for atom in expr.atoms(CS):
  arg=s.expand(atom.args[0]);coefficient=arg.coeff(p.x);constant=s.expand(arg-coefficient*p.x);assert coefficient in (1,-1) and (constant/(2*s.pi)).is_integer is True,(arg,constant)
  mapping[atom]=coefficient*value
 return s.simplify(expr.xreplace(mapping))
def physics(prompt):
 spans=re.findall(r'\$([^$]+)\$',prompt);assert len(spans)==2,(prompt,spans);left,value=spans[0].rstrip(',').split('=');given=read(left);value=read(value);assert given==CS(p.x) and abs(value)>1
 asked=read(spans[1]);atoms=sorted(asked.atoms(CS),key=s.default_sort_key);assert atoms
 return value,asked,atoms
def source_readback(g,k):
 sources=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());counts=dict(prompts=0,solutions=0,fields=0,values=0,keys=0)
 enum=lambda v:v[':db/ident'] if isinstance(v,dict) else v
 def correct(field):
  v=field[':answer-field/correct']
  return v[':answer/value'] if isinstance(v,dict) else next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==v[1])
 for case in cases:
  original=next(q for q in sources if case['source_id']==q[':question/math-academy-id']);q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in original)==(key in q)
   if key in original:assert enum(original[key])==enum(q[key])
  counts['prompts']+=1;counts['solutions']+=(':question/worked-solution' in original)
  assert len(original[':question/answer-fields'])==len(q[':question/answer-fields'])
  for a,b in zip(original[':question/answer-fields'],q[':question/answer-fields']):
   assert a[':answer-field/key']==b[':answer-field/key'] and enum(a[':answer-field/type'])==enum(b[':answer-field/type']);assert sorted((enum(v[':answer/type']),v[':answer/value']) for v in a[':answer-field/choices'])==sorted((enum(v[':answer/type']),v[':answer/value']) for v in b[':answer-field/choices']);assert (':answer-field/correct' in a)==(':answer-field/correct' in b);counts['fields']+=1;counts['values']+=len(a[':answer-field/choices'])
   if ':answer-field/correct' in a:assert correct(a)==correct(b);counts['keys']+=1
 return counts

def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','g'+str(k));source=source_readback(g,k);records=json.loads((R/f'qa/{k}-sampled.json').read_text());counts=dict(records=0,choices=0,solution_equalities=0,period_argument_checks=0,prose_substitutions=0)
 for q0 in json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions']:
  value,asked,atoms=physics(q0[':question/problem']);answer=normal(asked,value);key=q0[':question/answer-fields'][0].get(':answer-field/correct');assert key is None or V.same(read(key[':answer/value']),answer)
 for rec in records:
  q=rec['question'];value,asked,atoms=physics(q[':question/problem']);answer=normal(asked,value);sol=q[':question/worked-solution'];f=q[':question/answer-fields'][0];values=[read(v[':answer/value']) for v in f[':answer-field/choices']];assert len(values)==5
  for choice,actual in zip(f[':answer-field/choices'],values):assert V.same(actual,answer)==(choice[':answer/id']==f[':answer-field/correct'][1]);counts['choices']+=1
  if k==17592186176060:
   assert len(atoms)==1;atom=atoms[0];a=s.expand(asked).coeff(atom);b=s.expand(asked-a*atom);delta=s.expand(atom.args[0]+p.x)
   if q[':question/difficulty'].endswith('/hard'):expected=[answer,a*value+b,-a*value-b,-value+b,-a/value+b]
   elif q[':question/difficulty'].endswith('/moderate'):expected=[-value+delta,value+delta,value,0,-value]
   elif rec['generation']['template']=='easy_radical':expected=[-value,value,1,-value*value,value*value]
   else:expected=[value,0,-value,1/value,-1/value]
  else:
   b=s.expand(asked-sum(s.expand(asked).coeff(atom)*atom for atom in atoms));coeff=[s.expand(asked).coeff(atom) for atom in atoms];delta=[s.expand(atom.args[0]-p.x) for atom in atoms];template=rec['generation']['template']
   if len(atoms)==2:
    a,d=coeff;expected=[answer,a*value+b,d*value+b,(a-d)*value+b,(a+d)*value-b]
    # Error 'reverse second sign' refers to the prompt's displayed term order.
    ordered=re.findall(r'\\operatorname\{csc\}⁡\((.*?)\)',re.findall(r'\$([^$]+)\$',q[':question/problem'])[1]);assert len(ordered)==2
    first=next(atom for atom in atoms if atom.args[0]==read(ordered[0]));a=s.expand(asked).coeff(first);d=sum(coeff)-a;expected=[answer,a*value+b,d*value+b,(a-d)*value+b,(a+d)*value-b]
   else:
    a=coeff[0];shift=delta[0]
    if template in ('legacy_integer','legacy_fraction','direct_radical'):expected=[value,1/value,-value,value+shift,shift/s.pi*value]
    elif template=='scaled_integer':expected=[a*value,value,a+value,a/value,a*(value+shift)]
    elif template.startswith('reciprocal'):expected=[answer,value+b,a*value,b-a*value,a*value-b]
    elif template=='affine_radical':expected=[answer,value+b,a*value,a*(value+b),a*value-b]
    else:raise AssertionError(template)
  remaining=list(map(s.sympify,expected))
  for actual in values:
   matches=[i for i,want in enumerate(remaining) if V.same(actual,want)];assert len(matches)==1,(k,actual,remaining);remaining.pop(matches[0])
  # Every actual equality, including first distributed arithmetic and final
  # prose, is read from its rendered string, without generation parameters.
  blocks=re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',sol,re.S)
  for double,inline in blocks:
   block=double or inline
   if block.strip().startswith('n=') or '=' not in block:continue
   block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');lhs=None
   for row in block.split(r'\\'):
    terms=row.replace('&','').split('=')
    if len(terms)<2:continue
    lhs=terms[0].strip() or lhs;terms[0]=lhs
    actuals=[normal(read(t),value) for t in terms]
    assert all(V.same(actuals[0],v) for v in actuals[1:]),(k,rec['generation']['template'],row,actuals);counts['solution_equalities']+=len(actuals)-1
  if k==17592186176054:
   offsets=sorted(int(s.expand(atom.args[0]-p.x)/(2*s.pi)) for atom in atoms);substitutions=list(map(int,re.findall(r'Substituting \$n=(-?\d+)\$',sol)));assert sorted(substitutions)==offsets;counts['prose_substitutions']+=len(offsets)
   reduction_blocks=[a for a,b in blocks if a and r'\begin{aligned}' in a and a.lstrip().startswith(r'\begin{aligned}\operatorname{csc}')]
   assert len(reduction_blocks)==len(offsets)
   for block,index in zip(reduction_blocks,substitutions):
    exprs=[read(v) for v in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split('=')];assert len(exprs)==3 and exprs[0]==CS(p.x)
    assert exprs[1].args[0]==exprs[2].args[0]==p.x+2*index*s.pi;counts['period_argument_checks']+=2
  elif q[':question/difficulty'].endswith(('/moderate','/hard')):
   first=next(a for a,b in blocks if a and r'\begin{aligned}' in a);rows=first.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');firstexpr=read(rows[0].replace('&','').split('=')[0]);expanded=read(rows[0].replace('&','').split('=')[1]);reduced=read(rows[1].replace('&','').split('=')[1]);assert firstexpr==expanded==atoms[0] and reduced==CS(-p.x);counts['period_argument_checks']+=3
  counts['records']+=1
 report=dict(status='passed',kp_id=k,source=source,readback=counts,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
