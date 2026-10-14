"""Root reads actual scalar-factor relations/permutations and each printed equality."""
import json,re,sys,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186105737;D=ROOT/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);sys.modules[name]=m;z.loader.exec_module(m);return m
b=load(R/'qa-parametric-scalar-line.py','property_base');p=load(R/'vector-math-parser.py','property_math')
def scalar(raw):return p.scalar(raw.strip().rstrip('.,').replace('[','(').replace(']',')'))
def parity(order):return (-1)**sum(order[i]>order[j] for i in range(3) for j in range(i+1,3))
def vf(raw):
 raw=raw.strip().replace('(','').replace(')','');name=raw[-1];assert name in 'abc';coeff=raw[:-1];return name,scalar(coeff) if coeff not in ('','-') else (s.Integer(1) if not coeff else s.Integer(-1))
def triple(raw):
 outer,inner=raw.strip().split(r'\cdot',1);inner=inner.strip();assert inner.startswith('(') and inner.endswith(')'),raw;left,right=inner[1:-1].split(r'\times',1);items=[vf(z) for z in (outer,left,right)];order=''.join(v for v,c in items);assert set(order)==set('abc');return parity(order)*s.prod(c for v,c in items),[c for v,c in items],order

def expression(raw,T):
 raw=raw.replace(r'\,','').strip().rstrip('.,').replace('&','')
 if '⟨' in raw:
  aa,dd=re.fullmatch(r'(⟨.*?⟩)\\cdot\s*(⟨.*?⟩)',raw).groups();return p.vector(aa).dot(p.vector(dd))
 if '[' in raw:
  raw=re.sub(r'\[([^\[\]]*\\times[^\[\]]*)\]',lambda m:'('+s.latex(triple(m[1])[0]*T)+')',raw)
 if r'\times' in raw:return triple(raw)[0]*T
 return scalar(raw)
C={k:0 for k in ('records','actual_relations','actual_dot_operands','equalities','source_blocks','choices','whole_banks','hard_guards')}
def check(rec):
 q=rec['question'];text=q[':question/problem'];target=re.search(r'Find \$(.*?)\$',text)[1].rstrip(',');mult,req,order=triple(target)
 if '⟨' in text:
  w=p.vector(re.search(r'b\\times c=(⟨.*?⟩)',text)[1]);a=p.vector(re.search(r'a=(⟨.*?⟩)',text)[1]);T=a.dot(w);dotterms=list(a.multiply_elementwise(w));factors=None;rhs=None
 else:
  given=re.search(r'if \$(.*?)\$',text)[1].rstrip('.');lhs,rs=given.split('=');gm,factors,go=triple(lhs);rhs=scalar(rs);T=s.simplify(rhs/gm)
 C['actual_relations']+=1;answer=s.simplify(mult*T);sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)>=2
 for block in blocks:
  previous=None
  for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').split(chr(92)*2):
   if '=' not in row:continue
   vals=[]
   for j,side in enumerate(row.split('=')):
    if not side.strip():assert j==0 and previous is not None;val=previous
    else:
     val=expression(side,T)
     if factors is None and r'\cdot' in side and '⟨' not in side and r'\times' not in side:
      raw=side.replace(r'\,','').strip().rstrip('.,');parts=[];depth=0;at=0
      for j,ch in enumerate(raw):
       depth+=(ch in '({')-(ch in ')}')
       if ch=='+' and depth==0:parts.append(raw[at:j]);at=j+1
      parts.append(raw[at:]);assert len(parts)==3
      for item,aa,ww in zip(parts,a,w):
       l,r=item.split(r'\cdot',1);assert scalar(l)==aa and scalar(r)==ww,(item,aa,ww)
      C['actual_dot_operands']+=3
    vals.append(val)
   assert all(s.simplify(val-vals[0])==0 for val in vals),(row,vals,T);previous=vals[-1];C['equalities']+=1
  C['source_blocks']+=1
 f=q[':question/answer-fields'][0];values=[scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(set(values))==len(values);ref=f[':answer-field/correct'][1];assert next(z[':answer/id'] for z,value in zip(f[':answer-field/choices'],values) if value==answer)==ref
 if f[':answer-field/type'].endswith('/radio'):
  fam=rec['generation']['template']
  if factors is None:bank=[answer,-answer]+[mult*(T-u) for u in dotterms]
  elif fam=='single_scale':bank=[answer,-answer,mult*rhs,-mult*rhs,mult*rhs*next(z for z in factors if z!=1)]
  elif fam=='double_scaling':bank=[answer,-answer,parity(order)*T,parity(order)*T*req[1],parity(order)*T*req[2]]
  else:
   nonunit=[z for z in factors if z!=1];bank=[answer,-answer,parity(order)*rhs,answer*nonunit[0],answer*nonunit[-1]]
  assert set(values)==set(bank),(fam,values,bank);C['whole_banks']+=1
 else:assert '{{'+f[':answer-field/key']+'}}' in text and values==[answer]
 if q[':question/difficulty'].endswith('/hard'):assert all(2<=abs(z)<=5 for z in factors) and req[0]==1 and all(2<=abs(z)<=4 for z in req[1:]) and T.is_Integer and 1<=abs(T)<=9;C['hard_guards']+=1
 C['choices']+=len(values);C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'root_prop_gen');source=b.raw(g,K,D);records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 for fam,cfg in g.TEMPLATES.items():records.append(g.generate(cfg['level'],template=fam,seed=496))
 for z in records:check(z)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
