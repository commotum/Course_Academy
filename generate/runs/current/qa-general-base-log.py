"""Root actual functions, source chains, separated evaluation operands/banks."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096615;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'logarithm-readback.py','root_gbl_parser');x=p.x;g=load(D.with_suffix('.py'),'root_gbl_g');f=load(R/'root-source-fidelity.py','root_gbl_fid')
def check():
 originals,S=f.check(g,K,D);C=dict(records=0,actual_prompt_functions=0,actual_evaluation_points=0,formal_derivative_inputs=0,printed_derivative_rows=0,printed_evaluation_rows=0,separate_evaluation_components=0,choices=0,radio_bank_pairs=0,source_shared_prose=0)
 records=json.load(open(R/f'qa/{K}-sampled.json'));records.extend(g.generate(d[0],template=t,seed=n) for t,d in g.TEMPLATES.items() for n in (631,917))
 for rec in records:
  q=rec['question'];md=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];match=re.search(r'\$[fy](?:\(x\))?\s*=(.*?)\$',md);assert match;function=p.scalar(match[1]);derivative=s.diff(function,x);C['actual_prompt_functions']+=1
  point=re.search(r'instantaneous rate of change at \$x=(.*?)\$',md);point=p.scalar(point[1]) if point else None;answer=derivative.subs(x,point) if point is not None else derivative;C['actual_evaluation_points']+=int(point is not None)
  field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];values=[p.scalar(a[':answer/value']) for a in choices];assert [a[':answer/id'] for a,z in zip(choices,values) if p.eq(z,answer)]==[field[':answer-field/correct'][1]];C['choices']+=len(values)
  if field[':answer-field/type'].endswith('/radio'):assert len(values)==5 and all(not p.eq(a,b) for a,b in itertools.combinations(values,2));C['radio_bank_pairs']+=10
  else:assert len(values)==1 and '{{'+field[':answer-field/key']+'}}' in md
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S)
  for block in blocks:
   if r'\begin{aligned}' not in block:continue
   chain=block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0];rows=[z.split('&',1)[1].strip().lstrip('=').strip().rstrip('.,') for z in chain.split(chr(92)*2) if '&' in z];evaluation='|' in block
   for raw in rows:
    if '|' in raw:
     token=raw.replace(r'\left','').replace(r'\right','');pos=token.index('|');operand=token[:pos].strip();operand=operand.removesuffix(r'\big');operand=operand[1:] if operand.startswith('{') and operand.count('{')==operand.count('}')+1 else operand;operand=operand[1:-1] if operand.startswith('{(') and operand.endswith(')}') else operand;assert p.eq(p.scalar(operand),derivative),(family,raw);marked,_=p.group(token,token.index('_{x=')+1,'{','}');assert marked.startswith('x=') and p.eq(p.scalar(marked[2:]),point);value=p.scalar(operand).subs(x,point);C['separate_evaluation_components']+=len(s.Add.make_args(p.scalar(operand)))
    else:value=p.scalar(raw)
    assert p.eq(value,answer if evaluation else derivative),(family,raw,value,derivative,answer)
    C['printed_evaluation_rows' if evaluation else 'printed_derivative_rows']+=1
    if r'\frac{\text{d}}{\text{d}x}(' in raw:C['formal_derivative_inputs']+=1
  mid=g.TEMPLATES[family][1];source=originals.get(mid,{}).get(':question/worked-solution')
  if source:
   clean=lambda z:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',z,flags=re.S)).strip();assert clean(sol)==clean(source);C['source_shared_prose']+=1
  if q[':question/difficulty'].endswith('/moderate'):assert point is None and family=='log-ln-exp-derivative' and len(s.Add.make_args(function))==3
  if q[':question/difficulty'].endswith('/hard'):assert point==1 and len(s.Add.make_args(function))==3
  C['records']+=1
 out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
