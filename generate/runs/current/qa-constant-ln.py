"""Root actual constant-ln operands, formal derivative inputs and answer aliases."""
import importlib.util,json,re,hashlib,sys,itertools
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186096613;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','root_cln_parser');x=s.Symbol('x',positive=True);g=load(D.with_suffix('.py'),'root_cln_g');f=load(R/'root-source-fidelity.py','root_cln_fid');originals,S=f.check(g,K,D)
def scalar(z):return p.scalar(re.sub(r'\\cdot\s*$','',z.strip().rstrip('.,')).replace(r'\operatorname{ln}',r'\ln')).subs(p.x,x)
def derivative(z):
 operator=r'\frac{\text{d}}{\text{d}x}';assert operator in z;before,body=z.split(operator,1);assert body.startswith('(') and body.endswith(')');argument=scalar(body[1:-1]);assert argument.has(x);return (scalar(before) if before.strip() else 1)*s.diff(argument,x),argument
def eq(a,b):return s.simplify(a-b)==0
C=dict(records=0,actual_prompt_functions=0,identity_derivatives=0,formal_derivative_inputs=0,pulled_constant_operands=0,reciprocal_product_rows=0,collected_derivative_rows=0,answer_values=0,radio_bank_pairs=0,equivalent_blank_entries=0,source_shared_prose=0,explicit_level_guards=0)
records=json.load(open(R/f'qa/{K}-sampled.json'))
for level,template,profile in [('easy','legacy-radio','integer'),('easy','legacy-radio','fraction'),('easy','radio-dot','integer'),('easy','radio-dot','euler'),('easy','blank','canonical'),('easy','blank','equivalent-entry'),('moderate','authored-rational-e','canonical'),('hard','authored-signed-rational-e-power','canonical')]:records.extend(g.generate(level,template=template,profile=profile,seed=n) for n in (631,917))
for rec in records:
 q=rec['question'];md=q[':question/problem'];sol=q[':question/worked-solution'];function=scalar(re.search(r'\$y\s*=\s*(.*?)\$',md)[1]);c=s.simplify(function/s.log(x));assert not c.free_symbols and c!=0 and eq(function,c*s.log(x));answer=s.diff(function,x);C['actual_prompt_functions']+=1
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==2;left,right=blocks[0].strip().split('=');d,arg=derivative(left);assert eq(arg,s.log(x)) and eq(d,scalar(right));C['identity_derivatives']+=1
 chain=blocks[1].split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0];rows=[z.split('=',1)[1].strip().rstrip('.,') for z in chain.split(chr(92)*2)];assert len(rows)==4
 d,arg=derivative(rows[0]);assert eq(arg,function) and eq(d,answer);C['formal_derivative_inputs']+=1
 operator=r'\frac{\text{d}}{\text{d}x}';constant=scalar(rows[1].split(operator,1)[0]);d,arg=derivative(rows[1]);assert eq(arg,s.log(x)) and eq(constant,c) and eq(d,answer);C['pulled_constant_operands']+=1
 assert r'\cdot' in rows[2] and r'\frac{1}{x}' in rows[2];assert eq(scalar(rows[2]),answer);C['reciprocal_product_rows']+=1
 assert operator not in rows[3] and eq(scalar(rows[3]),answer);C['collected_derivative_rows']+=1
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];values=[scalar(a[':answer/value']) for a in choices];matches=[eq(z,answer) for z in values];assert next(v for a,v in zip(choices,matches) if a[':answer/id']==field[':answer-field/correct'][1]);C['answer_values']+=len(values)
 if field[':answer-field/type'].endswith('/radio'):
  assert len(values)==5 and sum(matches)==1 and all(not eq(a,b) for a,b in itertools.combinations(values,2));C['radio_bank_pairs']+=10
 else:
  assert field[':answer-field/type'].endswith('/blank') and all(matches) and '{{'+field[':answer-field/key']+'}}' in md;C['equivalent_blank_entries']+=len(values)
 source=originals.get(rec['generation']['source_id'],{}).get(':question/worked-solution')
 if source:
  clean=lambda z:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',z,flags=re.S)).strip();assert clean(sol)==clean(source);C['source_shared_prose']+=1
 level=q[':question/difficulty'].split('/')[-1];numerator,denominator=s.fraction(c);rational,exponential=c.as_coeff_Mul();exponent=s.simplify(s.log(exponential))
 if level=='moderate':assert c>0 and denominator>1 and exponent==1
 if level=='hard':assert c<0 and denominator>1 and exponent in (2,3,4)
 C['explicit_level_guards']+=1;C['records']+=1
out=dict(status='passed',source=S,readback=C,authored_calibration='M rational Euler constant; H signed rational fixed Euler power; one constant-ln derivative method',script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
