"""Read actual dependent systems, operative stages, and full affine answer images."""
import json,re,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186073778
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'qa-line-intersections.py','familyparser');expr=p.expr;eq=p.eq;x,y=p.symbols['x'],p.symbols['y']
def tuple_value(t):return tuple(expr(z) for z in t.replace(r'\left','').replace(r'\right','').strip()[1:-1].split(','))
def family(t):
 A,B=tuple_value(t);v=A.free_symbols|B.free_symbols;assert len(v)<=1
 if not v:return ('point',A,B)
 z=next(iter(v));dA=s.diff(A,z);dB=s.diff(B,z);assert not dA.has(z) and not dB.has(z) and (dA!=0 or dB!=0)
 normal=(dB,-dA,-dB*A.subs(z,0)+dA*B.subs(z,0));pivot=next(v for v in normal if v!=0);return tuple(s.simplify(v/pivot) for v in normal)
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','familygenerator');raw=load(R/'qa-elimination-solution.py','familyraw');source=raw.raw(g,K);C=dict(records=0,systems=0,multipliers=0,transformed_rows=0,ordered_constant_components=0,isolation_stages=0,conclusions=0,choices=0,whole_banks=0)
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];t=q[':question/problem'];matches=re.search(r'lines \$(.*?)\$ and \$(.*?)\$',t);assert matches;E=list(map(eq,matches.groups()));coeff=[(L.coeff(x),L.coeff(y),D) for L,D in E];a,b,c=coeff[0];d,e,f=coeff[1];ratio=d/a;assert e==ratio*b and f==ratio*c;m=-a/b;h=c/b;level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert m.q==h.q==1 and 2<=abs(m)<=6 and 1<=abs(h)<=8
  elif level=='moderate':assert (m.q>1)+(h.q>1)==1 and max(m.q,h.q)<=4
  else:assert 3<=m.q<=6 and 3<=h.q<=6
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==5;assert list(map(eq,blocks[0].replace(r'\{','').split(';')))==E;C['systems']+=1
  op=blocks[1].replace(r'\{','').split(';');assert eq(op[1])==E[1];z=re.fullmatch(r'(.*?)\s*\\mid\s*\\mid\s*\\cdot\s*\((.*?)\)\s*',op[0]);assert z and eq(z[1])==E[0] and expr(z[2])==-ratio;C['multipliers']+=1
  stages=p.aligned(blocks[2]);assert list(map(eq,stages))==[(-d*x-e*y,-f),(d*x+e*y,f),(s.Integer(0),s.Integer(0)),(s.Integer(0),s.Integer(0))];C['transformed_rows']+=2
  rhs=stages[2].split('=')[1];tokens=re.findall(r'[+-]?\s*\d+',rhs);assert [expr(v) for v in tokens]==[-f,f];C['ordered_constant_components']+=2
  assert p.rows(blocks[3])==[(a*x+b*y,c),(b*y,c-a*x),(y,(c-a*x)/b),(y,h+m*x)];C['isolation_stages']+=4
  # The quotient is an operative node, even where the easy divisor is one.
  assert r'\frac{' in p.aligned(blocks[3])[2]
  end=tuple_value(blocks[4]);v=end[0];assert v in (p.symbols['x'],p.symbols['t'],p.symbols['u']);assert end==(v,h+m*v);assert 'where $'+str(v)+'$ is any number' in sol;C['conclusions']+=1
  if v!=x:assert 'Let $'+str(v)+'=x$ be the free coordinate' in sol
  field=q[':question/answer-fields'][0];radio=field[':answer-field/type'].endswith('/radio');target=family('('+str(v)+','+str(m*v+h)+')');seen=[]
  if radio:
   want=[family('('+str(v)+','+str(mm*v+hh)+')') for mm,hh in ((m,h),(-m,h),(m,-h),(-b/a,c/a),(0,h))]
   for choice in field[':answer-field/choices']:
    F=family(choice[':answer/value']);assert (F==target)==(choice[':answer/id']==field[':answer-field/correct'][1]);seen.append(F);C['choices']+=1
   assert len(set(seen))==5 and set(seen)==set(want);C['whole_banks']+=1
  else:
   assert '{{'+field[':answer-field/key']+'}}' in t and len(field[':answer-field/choices'])==1;choice=field[':answer-field/choices'][0];assert expr(choice[':answer/value'])==m*v+h and choice[':answer/id']==field[':answer-field/correct'][1];C['choices']+=1
  C['records']+=1
 # Explicit affine-image equivalence check, independent of same parameter spelling.
 assert family('(x,3x+2)')==family('(2t+1,6t+5)') and family('(x,3x+2)')!=family('(2t+1,6t+2)')
 out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
