"""Root independently reads three actual vector fields and all partial stages."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186133895;D=R.parents[2]/f'generate/scratch/{K}'
def load(p,n):
 z=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','unitcurl_root_parser');x,y=p.x,p.y
fidelity=load(R/'root-source-fidelity.py','curl_source');g=load(D.with_suffix('.py'),'curl_generator');originals,S=fidelity.check(g,K,D)
def math(t):return p.scalar(t.strip().rstrip('.,').replace(r'\operatorname{atan}',r'\arctan'))
def eq(a,b):return s.simplify(s.trigsimp(a-b))==0
def selection(t):return tuple(i for i,label in enumerate(('I','II','III')) if re.search(r'\b'+label+r'\b',t))
C=dict(records=0,actual_field_components=0,held_partials=0,grouped_subtraction_components=0,distributed_components=0,collected_curls=0,choices=0,bank_pair_checks=0,field_equivalence_pairs=0,source_prose_masks=0)
records=json.load(open(R/f'qa/{K}-sampled.json'))
for family,level in g.LEVELS.items():records.extend(g.generate(level,seed=n,template=family) for n in (631,917))
for rec in records:
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template']
 if '- $P(x,y)=' in prompt:
  fields=[(math(a),math(b)) for a,b in re.findall(r'- \$P\(x,y\)=(.*?)\$ and \$Q\(x,y\)=(.*?)\$',prompt)]
 else:fields=[tuple(map(math,v.replace(r'\,','').split(','))) for v in re.findall(r'F\(x,y\)=⟨(.*?)⟩',prompt)]
 assert len(fields)==3 and all(len(f)==2 for f in fields);C['actual_field_components']+=6
 deriv=[(s.diff(a,y),s.diff(b,x)) for a,b in fields];curl=[s.simplify(b-a) for a,b in deriv];truth=tuple(i for i,c in enumerate(curl) if eq(c,1))
 py=re.findall(r'\$\\frac\{∂P\}\{∂y\}=(.*?)\$',sol);qx=re.findall(r'\$\\frac\{∂Q\}\{∂x\}=(.*?)\$',sol);assert len(py)==len(qx)==3
 for i,(a,b) in enumerate(deriv):assert eq(math(py[i]),a) and eq(math(qx[i]),b);C['held_partials']+=2
 chains=re.findall(r'\\frac\{∂Q\}\{∂x\}-\\frac\{∂P\}\{∂y\}=(.*?)\n',sol)[1:];assert len(chains)==3
 for i,(chain,(a,b)) in enumerate(zip(chains,deriv)):
  parts=chain.split('=');assert len(parts)==3
  m=re.fullmatch(r'\\left\((.*?)\\right\)-\\left\((.*?)\\right\)',parts[0]);assert m and eq(math(m[1]),b) and eq(math(m[2]),a);C['grouped_subtraction_components']+=2
  distributed=parts[1].replace(r'\left','').replace(r'\right','');terms=[];pos=0
  while pos<len(distributed):
   sign=''
   if distributed[pos] in '+-':sign=distributed[pos];pos+=1
   assert distributed[pos]=='(';start=pos+1;depth=1;pos+=1
   while depth:depth+=(distributed[pos]=='(')-(distributed[pos]==')');pos+=1
   terms.append((sign,distributed[start:pos-1]))
  assert terms
  expected=[(1,t) for t in s.Add.make_args(b)]+[(-1,t) for t in s.Add.make_args(a)];assert len(terms)==len(expected)
  actual=[(-1 if sign=='-' else 1,math(t)) for sign,t in terms];assert all(sgn==esgn and eq(t,et) for (sgn,t),(esgn,et) in zip(actual,expected));C['distributed_components']+=len(terms)
  final=parts[-1].replace(r'\ne 1','');assert eq(math(final),curl[i]) and (r'\ne 1' in parts[-1])==(i not in truth);C['collected_curls']+=1
 declared=re.findall(r'- (?:Pair|Vector field) (I{1,3})(.*?) the required area\.',sol);assert len(declared)==3
 for label,claim in declared:assert ('not' not in claim)==(('I','II','III').index(label) in truth)
 conclusion=re.search(r'Therefore, the correct answer is "(.*?)"',sol)[1];assert selection(conclusion)==truth
 f=q[':question/answer-fields'][0];bank=[selection(a[':answer/value']) for a in f[':answer-field/choices']];assert len(bank)==len(set(bank))==5
 assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],bank) if v==truth]==[f[':answer-field/correct'][1]];C['choices']+=5;C['bank_pair_checks']+=10
 for a,b in itertools.combinations(fields,2):assert not (eq(a[0],b[0]) and eq(a[1],b[1]));C['field_equivalence_pairs']+=1
 if family!='mixed':
  clean=lambda t:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',t,flags=re.S)).strip();assert clean(sol)==clean(originals[family][':question/worked-solution']);C['source_prose_masks']+=1
 C['records']+=1
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
