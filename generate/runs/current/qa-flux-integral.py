"""Root calculus readback from actual field/region, including each endpoint."""
import importlib.util,json,re,hashlib,itertools,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186133931;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'divergence-readback.py','parent_flux_integral');x,y,z=p.variables
def math(t):return p.scalar(t.strip().rstrip('.,'))
def equal(a,b):return s.simplify(a-b)==0
def group(t,pos,op='{',cl='}'):
 assert t[pos]==op;start=pos+1;depth=1;pos+=1
 while depth:depth+=(t[pos]==op)-(t[pos]==cl);pos+=1
 return t[start:pos-1],pos
def bounds(t,pos):
 assert t[pos]=='_';lo,pos=group(t,pos+1);assert t[pos]=='^';hi,pos=group(t,pos+1);return lo,hi,pos
def integral(t):
 t=t.strip().rstrip('.');pairs=[];pos=0
 while t[pos:].startswith(r'{\int }'):
  a,b,pos=bounds(t,pos+len(r'{\int }'));pairs.append((math(a),math(b)))
 diffs=list(re.finditer(r'\\text\{d\}([xyz])',t[pos:]));assert len(diffs)==len(pairs)
 integrand=math(t[pos:pos+diffs[0].start()].replace(r'\,','').strip() or '1');axes=[dict(zip('xyz',(x,y,z)))[m[1]] for m in diffs];pairs=tuple((v,a,b) for v,(a,b) in zip(reversed(axes),pairs));value=integrand
 for v,a,b in reversed(pairs):value=s.integrate(value,(v,a,b))
 return integrand,pairs,s.simplify(value)
def primitive(t):
 t=t.strip()
 if t.startswith('{['):t=t[1:].replace(']}',']',1)
 body,pos=group(t,0,'[',']');P=math(body);a,b,pos=bounds(t,pos);assert pos==len(t);axis,a=a.split('=');other,b=b.split('=');assert axis==other;v=dict(zip('xyz',(x,y,z)))[axis];a,b=math(a),math(b);return P,v,a,b,s.simplify(P.subs(v,b)-P.subs(v,a))
def split(t,separator='+'):
 depth=0;start=0;out=[]
 for i,c in enumerate(t):
  depth+=(c in '({[')-(c in ')}]')
  if c==separator and depth==0 and i>start:out.append(t[start:i]);start=i+(1 if separator=='+' else 0)
 return out+[t[start:]]
def endpoint(t):
 assert t.startswith('(') and t.endswith(')');body=t[1:-1];depth=0;positions=[]
 for i,c in enumerate(body):
  depth+=(c in '({')-(c in ')}')
  if c=='-' and depth==0 and i>0:positions.append(i)
 assert len(positions)==1,(t,positions);i=positions[0];return math(body[:i]),math(body[i+1:])
def products(t):return t.split(r'\cdot ')
C={k:0 for k in ('records','actual_components','actual_bounds','held_operands','individual_partials','collected_divergence','triple_integrands','repeated_integrals','separated_integrands','primitive_derivatives','primitive_bound_pairs','individual_endpoints','complete_calculation_rows','affine_component_endpoints','choices','complete_method_banks','operative_source_sequences')}
def check(rec,old):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];cs=p.field(prompt);assert cs is not None;ds=[s.diff(c,v) for c,v in zip(cs,(x,y,z))];div=s.expand(sum(ds));C['actual_components']+=3
 equations=re.findall(r'\$([xyz])\s*=\s*(.*?)\$',prompt);assert len(equations)==6 and [a for a,b in equations]==list('xxyyzz');B=tuple((v,math(equations[i*2][1]),math(equations[i*2+1][1])) for i,v in enumerate((x,y,z)));assert all(b>a for v,a,b in B);C['actual_bounds']+=6
 def I(f):
  for v,a,b in reversed(B):f=s.integrate(f,(v,a,b))
  return s.simplify(f)
 answer=I(div);blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==(3 if family=='affine' else 2)
 der=blocks[0].split(' & =')[1:];assert len(der)==3;_,ops=p.derivative_inputs(der[0]);assert len(ops)==3
 for c,var,(axis,arg,*_) in zip(cs,(x,y,z),ops):assert axis==str(var) and equal(math(arg),c);C['held_operands']+=1
 substituted=der[1].split(chr(92)*2)[0].strip();contributions=split(substituted);assert len(contributions)==3
 for t,v in zip(contributions,ds):assert equal(math(t),v);C['individual_partials']+=1
 assert equal(math(der[-1]),div);C['collected_divergence']+=1
 rows=blocks[1].split(' & =')[1:];rows=[t.split(chr(92)*2)[0].strip().rstrip('.') for t in rows];assert len(rows)==(7 if family in ('cos','log','exp') else 6)
 assert rows[0].startswith(r'{∭}_{R}') and equal(math(rows[0][len(r'{∭}_{R}'):].removesuffix(r'\,\text{d}V')),div);C['triple_integrands']+=1
 f,bounds0,val=integral(rows[1]);assert equal(f,div) and bounds0==B and equal(val,answer);C['repeated_integrals']+=1
 factors=[integral(t) for t in products(rows[2])];assert len(factors)==3 and [a[1] for a in factors]==[(b,) for b in B] and equal(s.prod(a[0] for a in factors),div);C['separated_integrands']+=3
 primitives=products(rows[3]);evaluated=products(rows[4]);assert len(primitives)==len(evaluated)==3
 for raw,end,(f,bs,val) in zip(primitives,evaluated,factors):
  v,a,b=bs[0]
  if raw.startswith('[') or raw.startswith('{['):
   P,axis,lo,hi,value=primitive(raw);assert (axis,lo,hi)==(v,a,b) and equal(s.diff(P,v),f);C['primitive_derivatives']+=1;C['primitive_bound_pairs']+=1
   upper,lower=endpoint(end);assert equal(upper,P.subs(v,b)) and equal(lower,P.subs(v,a));C['individual_endpoints']+=2
  else:
   assert f==1;hi,lo=endpoint(raw);assert (hi,lo)==(b,a) and equal(math(end),b-a);C['individual_endpoints']+=2
 def rowvalue(t):
  if t.startswith(r'{∭}_{R}'):return I(math(t[len(r'{∭}_{R}'):].removesuffix(r'\,\text{d}V')))
  values=[]
  for raw in products(t):
   values.append(integral(raw)[2] if raw.startswith(r'{\int }') else primitive(raw)[4] if raw.startswith('[') or raw.startswith('{[') else math(raw))
  return s.prod(values)
 for row in rows:assert equal(rowvalue(row),answer);C['complete_calculation_rows']+=1
 if family=='affine':
  extra=blocks[2].rstrip('.').split(chr(92)*2);assert len(extra)==2
  for row,a in zip(extra,(B[0][2],B[0][1])):
   lhs,rhs=row.split('&=');terms=split(rhs.strip());assert len(terms)==2 and equal(math(lhs),a*a+2*a) and [math(t) for t in terms]==[a*a,2*a];C['affine_component_endpoints']+=2
 choices=q[':question/answer-fields'][0][':answer-field/choices'];vals=[math(a[':answer/value']) for a in choices];assert len(vals)==5 and all(not equal(a,b) for a,b in itertools.combinations(vals,2));assert [a[':answer/id'] for a,t in zip(choices,vals) if equal(t,answer)]==[q[':question/answer-fields'][0][':answer-field/correct'][1]]
 bx,by,bz=[(a,b) for _,a,b in B];wx,wy,wz=[b-a for _,a,b in B]
 if family in ('xy_a','xy_b','cancel_x','cancel_x2','cancel_z','canonical'):
  nonzero=[a for a in ds if a!=0];wrong=I(sum(-a if a.could_extract_minus_sign() else a for a in ds)) if family.startswith('cancel_') else I(nonzero[0]);wanted=[answer,-answer,wrong,I(sum(s.diff(c,v,2) for c,v in zip(cs,(x,y,z)))),answer/wz]
 elif family=='cos':wanted=[answer,-answer,I(x*s.cos(z)),I(2*x*s.sin(z)),(bx[1]**2-bx[0]**2)*wy*wz]
 elif family=='log':wanted=[answer,-answer,(s.log(bx[1])-s.log(bx[0]))*wy*wz,I(y),(s.log(bx[1])-s.log(bx[0]))*(by[1]**2-by[0]**2)*wz]
 elif family=='exp':wanted=[answer,-answer,(bx[1]**3-bx[0]**3)*wy*wz,(bx[1]**3-bx[0]**3)*wy*s.exp(bz[1]),(bx[1]**2-bx[0]**2)*wy*(s.exp(bz[1])-s.exp(bz[0]))]
 elif family=='affine':wanted=[answer,-answer,I(2*x),I(2),(bx[1]**2+2*bx[1])*wy*wz]
 elif family=='xz':wanted=[answer,-answer,I(z),I(2),wx*wy*bz[1]**2]
 else:wanted=[answer,-answer,answer/wx,answer/wy,answer/wz]
 assert all(sum(equal(v,w) for w in wanted)==1 for v in vals);C['choices']+=5;C['complete_method_banks']+=1
 if old and ':question/worked-solution' in old:
  prose=lambda t:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',t,flags=re.S)).strip();normal=sol.split('\n\nThe individual endpoint terms are')[0];assert prose(normal)==prose(old[':question/worked-solution']);oldrows=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',old[':question/worked-solution'],re.S)[1].split(' & =')[1:];assert len(oldrows)==len(rows);C['operative_source_sequences']+=1
 C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'parent_closed_flux_generator');frozen=json.load(open(R/f'sources/{K}.json'));assert json.load(open(D/'source.json'))==frozen;originals={str(q[':db/id']):q for q in frozen['record'][':knowledge-point/questions']};S=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0,unrated=0,unrecoverable_context=1)
 for case in json.load(open(D/'source-cases.json')):
  o=originals[str(case['source_id'])];q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];assert q[':question/problem']==o[':question/problem'];assert (':question/difficulty' in q)==(':question/difficulty' in o) and (':question/worked-solution' in q)==(':question/worked-solution' in o);S['prompts']+=1;S['unrated']+=(':question/difficulty' not in o)
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];S['solutions']+=1
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);S['fields']+=1;S['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];S['refs']+=1
   else:S['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for family,c in g.FAMILIES.items():
  level='easy' if family=='constant' else 'hard' if family=='canonical' else 'moderate';records.extend(g.generate(level,seed=seed,template=family) for seed in (631,917))
 for rec in records:check(rec,originals.get(str(g.FAMILIES[rec['generation']['template']]['source'])))
 out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
