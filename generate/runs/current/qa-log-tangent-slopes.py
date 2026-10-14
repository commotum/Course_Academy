"""Root actual slope function, every derivative/evaluation stage and conclusion."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096616;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'logarithm-readback.py','root_lts_parser');x=p.x;g=load(D.with_suffix('.py'),'root_lts_g');f=load(R/'root-source-fidelity.py','root_lts_fid');originals,S=f.check(g,K,D)
def actual_point(md):
 raw=re.search(r'\$x\s*=\s*(.*?)\$',md)[1].rstrip('.,');return p.scalar(raw)
def remove_bar(raw):
 pos=raw.index('|');body=raw[:pos].removesuffix(r'\big');body=body[1:] if body.startswith('{') and body.count('{')==body.count('}')+1 else body;body=body[1:-1] if body.startswith('{(') and body.endswith(')}') else body
 marked,_=p.group(raw,raw.index('_{x=')+1,'{','}');return p.scalar(body),p.scalar(marked[2:])
C=dict(records=0,actual_prompt_functions=0,actual_points=0,printed_derivative_rows=0,printed_evaluation_rows=0,formal_derivative_inputs=0,point_conclusions=0,answer_values=0,radio_bank_pairs=0,blank_aliases=0,source_shared_prose=0)
records=json.load(open(R/f'qa/{K}-sampled.json'));records.extend(g.generate('easy',template=t,seed=n) for t in g.TEMPLATES for n in (631,917))
for rec in records:
 q=rec['question'];md=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];function=p.scalar(re.search(r'\$y\s*=(.*?)\$',md)[1].rstrip(','));point=actual_point(md);assert point.is_positive;derivative=s.diff(function,x);answer=s.expand(derivative.subs(x,point));C['actual_prompt_functions']+=1;C['actual_points']+=1
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==2
 for index,block in enumerate(blocks):
  chain=block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0] if r'\begin{aligned}' in block else block;rows=[(z.split('&',1)[1].strip().lstrip('=') if '&' in z else z.split('=',1)[1]).strip().rstrip('.,') for z in chain.split(chr(92)*2)]
  for raw in rows:
   if '|' in raw:val,target=remove_bar(raw);assert p.eq(val,derivative) and p.eq(target,point);value=val.subs(x,target)
   else:value=p.scalar(raw)
   assert p.eq(value,answer if index else derivative),(family,index,raw,value,derivative,answer);C['printed_evaluation_rows' if index else 'printed_derivative_rows']+=1
   if r'\frac{\text{d}}{\text{d}x}(' in raw:C['formal_derivative_inputs']+=1
  source=originals[g.case(family)['source_id']].get(':question/worked-solution')
  if source and index==0:
   original_block=re.findall(r'\$\$(.*?)\$\$',source,re.S)[0];original_chain=original_block.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0] if r'\begin{aligned}' in original_block else original_block;original=original_chain.split(chr(92)*2);assert len(rows)==len(original)
   for a,b in zip(rows,original):assert a.count(r'\frac{\text{d}}{\text{d}x}')==b.count(r'\frac{\text{d}}{\text{d}x}') and a.count(r'\cdot')==b.count(r'\cdot')
 conclusion=re.search(r'Therefore, the slope\s+of the tangent at \$x=(.*?)\$',sol,re.S);assert conclusion and p.eq(p.scalar(conclusion[1]),point);C['point_conclusions']+=1
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];values=[p.scalar(a[':answer/value']) for a in choices];good=[p.eq(z,answer) for z in values];assert next(v for a,v in zip(choices,good) if a[':answer/id']==field[':answer-field/correct'][1]);C['answer_values']+=len(values)
 if field[':answer-field/type'].endswith('/radio'):assert len(values)==5 and sum(good)==1 and all(not p.eq(a,b) for a,b in itertools.combinations(values,2));C['radio_bank_pairs']+=10
 else:assert all(good) and '{{'+field[':answer-field/key']+'}}' in md;C['blank_aliases']+=len(values)
 if source:
  clean=lambda z:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',z,flags=re.S)).strip();assert clean(sol)==clean(source);C['source_shared_prose']+=1
 level=q[':question/difficulty'].split('/')[-1]
 if level=='moderate':assert family=='ln_quadratic_linear_radio' and point in (2,3,4) and len(s.Add.make_args(function))==3
 if level=='hard':assert family=='log_quadratic_linear_blank' and len(s.Add.make_args(function))==3 and rec['generation']['parameters']['s'] in (2,3,4)
 C['records']+=1
out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
