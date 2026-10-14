"""Root source feedback, concrete derivative/evaluation stages and full banks."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096614;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'logarithm-readback.py','root_nls_parser');x=p.x;g=load(D.with_suffix('.py'),'root_nls_g');f=load(R/'root-source-fidelity.py','root_nls_fid');originals,S=f.check(g,K,D)
def math(z):return p.scalar(z.replace(r'\,','').strip().rstrip('.,'))
def bar(raw):
 pos=raw.index('|');body=raw[:pos].removesuffix(r'\big');body=body[1:] if body.startswith('{') and body.count('{')==body.count('}')+1 else body;body=body[1:-1] if body.startswith('{(') and body.endswith(')}') else body;marked,_=p.group(raw,raw.index('_{x=')+1,'{','}');return math(body),math(marked[2:])
C=dict(records=0,actual_functions=0,derivative_rows=0,evaluation_rows=0,formal_derivative_inputs=0,point_prose=0,answer_values=0,radio_bank_pairs=0,source_feedback_derivatives=0,source_feedback_operands=0,source_shared_prose=0,authored_irrational_whole_banks=0)
records=json.load(open(R/f'qa/{K}-sampled.json'));records.extend(g.generate(d['level'],template=t,seed=n) for t,d in g.SPECS.items() for n in (631,917))
for rec in records:
 q=rec['question'];md=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];function=math(re.search(r'\$[fy](?:\(x\))?\s*=(.*?)\$',md)[1]);derivative=s.diff(function,x);point=re.search(r'instantaneous rate of change at \$x=(.*?)\$',md);point=math(point[1]) if point else None;answer=derivative.subs(x,point) if point is not None else derivative;C['actual_functions']+=1
 for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
  assert r'\begin{aligned}' in block;chain=block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0];evaluation='|' in block
  for part in chain.split(chr(92)*2):
   raw=part.split('&',1)[1].strip().lstrip('=').strip().rstrip('.,')
   if '|' in raw:value,target=bar(raw);assert p.eq(value,derivative) and p.eq(target,point);value=value.subs(x,target)
   else:value=math(raw)
   assert p.eq(value,answer if evaluation else derivative),(family,raw,value,answer,derivative);C['evaluation_rows' if evaluation else 'derivative_rows']+=1
   if r'\frac{\text{d}}{\text{d}x}(' in raw:C['formal_derivative_inputs']+=1
 if point is not None:
  prose=re.search(r'Therefore, the instantaneous rate of change at \$x=(.*?)\$',sol);assert prose and p.eq(math(prose[1]),point);C['point_prose']+=1
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];values=[math(a[':answer/value']) for a in choices];good=[p.eq(z,answer) for z in values];assert [a[':answer/id'] for a,v in zip(choices,good) if v]==[field[':answer-field/correct'][1]];C['answer_values']+=len(values)
 if field[':answer-field/type'].endswith('/radio'):assert len(values)==5 and all(not p.eq(a,b) for a,b in itertools.combinations(values,2));C['radio_bank_pairs']+=10
 else:assert len(values)==1 and '{{'+field[':answer-field/key']+'}}' in md
 if family=='q-339973':
  assert field[':answer-field/type'].endswith('/radio');a=s.simplify(s.expand(function).coeff(s.log(x)));terms=[z for z in s.Add.make_args(function) if z.has(x) and not z.has(s.log(x))];assert len(terms)==1;power=terms[0];r=power.as_powers_dict()[x];wanted=[derivative,1/x+r*x**(r-1),a/x+x**(r-1),a/x+r*x**r,-a/x+r*x**(r-1)];assert all(sum(p.eq(z,w) for w in wanted)==1 for z in values);C['authored_irrational_whole_banks']+=1
 for a in choices:
  feedback=a.get(':answer/feedback')
  if feedback is None:continue
  for operand,rhs in re.findall(r'd\[(.*?)\]/dx\s*=\s*([^,;.]+)',feedback):
   # Some captured arguments provide a second equal power-rule expansion.
   rhs=rhs.split('=')[0].strip();assert p.eq(s.diff(math(operand),x),math(rhs)),(family,feedback);C['source_feedback_derivatives']+=1;C['source_feedback_operands']+=2
 source=originals[family].get(':question/worked-solution')
 if source:
  clean=lambda z:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',z,flags=re.S)).strip();assert clean(sol)==clean(source);C['source_shared_prose']+=1
 C['records']+=1
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
