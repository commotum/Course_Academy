"""Root three-path actual-display verification, including coefficient responses."""
import importlib.util,json,re,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186166750
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
T=load(R/'qa-two-independent-chain.py','threeparser');p=T.p;scalar0=T.scalar;axes=(p.x,p.y,p.z);cs=(p.i,p.j,p.k)
def scalar(z):
 z=re.sub(r'\{?c\}?_\{?([123])\}?',lambda m:'ijk'[int(m[1])-1],z);return scalar0(z)
same=T.same

def task(q):
 text=q[':question/problem'];f=re.search(r'\$f\(x,y,z\)=(.*?)\$',text);assert f,text;F=scalar(f[1]);maps=[]
 for a in 'xyz':
  m=re.search(r'\$'+a+r'=(.*?)\$',text);assert m,text;maps.append(scalar(m[1]))
 assert F.free_symbols<=set(axes) and all(e.free_symbols<={T.u,T.v} for e in maps)
 vars=re.findall(r'\\frac\{∂f\}\{∂([st])\}',text);assert len(vars)==1;textvar=vars[0];var=T.u if textvar=='s' else T.v;other=T.v if var==T.u else T.u
 partials=[s.diff(F,a) for a in axes];sub=dict(zip(axes,maps));components=[a.subs(sub,simultaneous=True) for a in partials];coords=[s.diff(a,var) for a in maps];products=[a*b for a,b in zip(components,coords)];D=s.diff(F.subs(sub,simultaneous=True),var);assert same(D,sum(products));coeff=None
 if 'Given that' in text:
  block=re.search(r'\$\$(.*?)\$\$',text,re.S);assert block;_,form=block[1].split('=',1);signature=scalar(form)
  delta=s.together(D-signature).as_numer_denom()[0];delta=s.expand(s.trigsimp(delta));poly=s.Poly(delta,T.u,T.v);solution=s.solve(poly.coeffs(),cs,dict=True);assert len(solution)==1 and set(solution[0])==set(cs);coeff=[s.simplify(solution[0][a]) for a in cs];assert all(not e.free_symbols for e in coeff);assert same(signature.subs(dict(zip(cs,coeff))),D);answer=sum(coeff)
 else:answer=D
 return F,maps,textvar,var,other,partials,components,coords,products,D,coeff,answer

def stages(q,n):
 F,maps,textvar,var,other,P,C,M,products,D,coeff,answer=task(q);Dtag=r'\frac{∂f}{∂'+textvar+'}';ptags=[r'\frac{∂f}{∂'+a+'}' for a in 'xyz'];mtags=[r'\frac{∂'+a+'}{∂'+textvar+'}' for a in 'xyz'];rule='+'.join(a+r'\cdot '+b for a,b in zip(ptags,mtags))
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',q[':question/worked-solution'],re.S);assert blocks[0].strip().rstrip('.')==Dtag+'='+rule
 seen_partial=False
 for block in blocks[1:]:
  body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=body.split(r'\\');first=re.split(r'&?\s*=',rows[0],maxsplit=1)[0].strip()
  if first in ptags:mode='substitution_stages' if seen_partial else 'formal_partial_stages';seen_partial=True;values=dict(zip(ptags,C if mode=='substitution_stages' else P))
  elif first in mtags:mode='held_coordinate_stages';values=dict(zip(mtags,M))
  elif first==Dtag:mode='product_reduction_stages';values={Dtag:D,**dict(zip(ptags,C)),**dict(zip(mtags,M))}
  else:
   assert coeff is not None;mode='coefficient_sum_stages';values={}
  if mode=='product_reduction_stages' and (F*p.x).free_symbols<={p.y,p.z}:
   # Detect the quotient family from its actual printed outer function.
   slots=[row.split('=',1)[1].strip().rstrip('.,') for row in rows]
   assert len(slots)==3 and slots[0].count(r'\frac')==3
   def fraction(raw):
    assert raw.startswith(r'\frac{'),raw
    def group(start):
     assert raw[start]=='{';depth=1;end=start+1
     while depth:depth+=(raw[end]=='{')-(raw[end]=='}');end+=1
     return raw[start+1:end-1],end
    numerator,end=group(5);denominator,end=group(end);assert not raw[end:].strip()
    return scalar(numerator),scalar(denominator)
   common,den=fraction(slots[1]);collected,den2=fraction(slots[2])
   assert same(den,(T.u+T.v)**2) and same(den2,den)
   assert T.u+T.v in common.atoms(s.Add) and T.u+T.v not in collected.atoms(s.Add)
   n['common_denominator_chains']=n.get('common_denominator_chains',0)+1
  current=None;want=None
  for row in rows:
   for piece in re.split(r',\\,',row):
    parts=[a.strip().rstrip('.,') for a in piece.replace('&','').split('=')]
    if parts[0]:
     current=parts[0]
     if current in values:want=values[current]
     else:assert coeff is not None and mode=='coefficient_sum_stages';want=scalar(current).subs(dict(zip(cs,coeff)))
    assert current and want is not None
    for expr in parts[1:]:
     for tag,val in values.items():expr=expr.replace(tag,'('+s.latex(val,ln_notation=True)+')')
     got=scalar(expr)
     if coeff is not None:got=got.subs(dict(zip(cs,coeff)))
     assert same(got,want),(mode,piece,got,want);n[mode]+=1
 if coeff is not None:
  declared=set()
  for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/worked-solution']):
   for piece in re.split(r'(?<!\\),',inline):
    bits=piece.strip().rstrip('.,').split('=')
    if len(bits)<2 or not re.search(r'\{?c\}?_\{?([123])\}?',bits[0]):continue
    want=scalar(bits[-1])
    for lhs in bits[:-1]:
     actual=scalar(lhs).subs(dict(zip(cs,coeff)));assert same(actual,want)
     declared.update(int(z) for z in re.findall(r'\{?c\}?_\{?([123])\}?',lhs))
  assert declared=={1,2,3},(declared,q[':question/worked-solution']);n['coefficient_declarations']+=len(declared)
 return task(q)

def check():
 g=load(ROOT/f'generate/scratch/{K}.py','threeg');orig=json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{K}/source-cases.json').read_text());src=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,missing_legacy_keys=0,coefficient_response_sources=0)
 for c in cases:
  q0=next(q for q in orig if q[':question/math-academy-id']==c['source_id']);q=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question'];assert q[':question/problem']==q0[':question/problem'] and q[':question/worked-solution']==q0[':question/worked-solution'];src['prompts']+=1;src['solutions']+=1;F,maps,tv,var,other,P,C,M,prod,D,coeff,answer=task(q0);src['coefficient_response_sources']+=coeff is not None;assert len(q[':question/answer-fields'])==len(q0[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);src['fields']+=1;src['values']+=len(f[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0);assert sum(same(scalar(a[':answer/value']),answer) for a in f0[':answer-field/choices'])==1
   if ':answer-field/correct' in f:
    a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert a[':answer/value']==f0[':answer-field/correct'][':answer/value'];assert same(scalar(a[':answer/value']),answer);src['keys']+=1
   else:src['missing_legacy_keys']+=1
 records=json.loads((R/f'qa/{K}-sampled.json').read_text());n=dict(records=0,formal_partial_stages=0,substitution_stages=0,held_coordinate_stages=0,product_reduction_stages=0,coefficient_sum_stages=0,coefficient_declarations=0,choices=0,complete_method_banks=0,normal_anchor_cases=0)
 n['colliding_method_anchors']=[]
 for c in cases:
  try:records.append(g.generate(c['level'],template=c['template'],parameters=c['parameters']));n['normal_anchor_cases']+=1
  except ValueError as exc:
   assert str(exc)=='whole-bank collision'
   original_profile=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='observed-repaired')
   stages(original_profile['question'],n)
   n['colliding_method_anchors'].append(c['source_id'])
 for rec in records:
  q=rec['question'];F,maps,tv,var,other,P,C,M,prod,D,coeff,answer=stages(q,n);kind=rec['generation']['template'];vals=[];f=q[':question/answer-fields'][0]
  for option in f[':answer-field/choices']:
   got=scalar(option[':answer/value']);assert same(got,answer)==(option[':answer/id']==f[':answer-field/correct'][1]);assert not any(same(got,z) for z in vals);vals.append(got);n['choices']+=1
  if coeff is not None:
   A,B,H=coeff
   if kind=='q-94589':expected=[answer,A,H,A+H,-answer]
   elif kind=='q-170675':expected=[answer,-answer,A,A+H,-A+B+H]
   elif kind=='q-37208':expected=[answer,A,B,H,A+B]
   else:expected=[answer,-answer,A,B+H,-B-H]
  else:
   active=[z for z in prod if not same(z,0)];a,b=active[:2];whole=F.subs(dict(zip(axes,maps)),simultaneous=True);expected=[D,D-a,D-b,s.diff(whole,other),D+a]
  assert all(any(same(got,w) for w in expected) for got in vals);n['complete_method_banks']+=1;n['records']+=1
 out=dict(status='passed',kp_id=K,source=src,readback=n,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
