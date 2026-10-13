"""Parent independently derives special-chain-rule stages from printed prompts."""
import importlib.util,re,json,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186166748
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
p=load(R/'ode-scalar-parser.py','specialrootparser');xp=s.Symbol('x',positive=True);y=p.y
FX=r'\frac{∂f}{∂x}';FY=r'\frac{∂f}{∂y}';YD=r'\frac{\text{d}y}{\text{d}x}';D=r'\frac{\text{d}f}{\text{d}x}'
def scalar(z):return p.scalar(z.strip().rstrip('.,').replace(r'\ln',r'\operatorname{ln}'))
def same(a,b):
 d=s.cancel(s.expand(a-b))
 if d==0:return True
 for at in (1,2,3):
  value=d.subs(p.locals_['x'],at)
  if value.is_finite is not False and value.is_zero is False:return False
 return s.simplify(s.trigsimp(d))==0
def task(q):
 x=xp if 'Assume $x>0.$' in q[':question/problem'] else p.x;p.locals_['x']=x
 prompt=q[':question/problem'];m=re.search(r'\$f\(x,y\)=(.*?)\$ and \$y=(.*?)\$',prompt);assert m,prompt
 F=scalar(m[1]);h=scalar(m[2]);assert h.free_symbols<={x} and F.free_symbols<={x,y}
 A=s.diff(F,x);B=s.diff(F,y);C=s.diff(h,x);aa=A.subs(y,h);bb=B.subs(y,h);answer=s.diff(F.subs(y,h),x);assert same(answer,aa+bb*C);return x,F,h,A,B,C,aa,bb,answer

def check(k=K):
 g=load(ROOT/f'generate/scratch/{k}.py','specialg');source=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());src=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,mathematically_valid_original_keys=0,source_domain_errors=0)
 for c in cases:
  original=next(q for q in source if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));q=g.generate('easy',template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question'];assert q[':question/problem']==original[':question/problem'];assert q[':question/worked-solution']==original[':question/worked-solution'];src['prompts']+=1;src['solutions']+=1
  x,F,h,A,B,C,aa,bb,answer=task(q)
  for f,f0 in zip(q[':question/answer-fields'],original[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);src['fields']+=1;src['values']+=len(f[':answer-field/choices'])
   selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert selected==f0[':answer-field/correct'][':answer/value'];src['keys']+=1
   if c['template']=='radial_power':
    assert not same(scalar(selected).subs(x,-1),answer.subs(x,-1));src['source_domain_errors']+=1
   else:assert same(scalar(selected),answer),(c,selected,answer);src['mathematically_valid_original_keys']+=1
 records=json.loads((R/f'qa/{k}-sampled.json').read_text());stats=dict(records=0,partial_stages=0,substitution_stages=0,dependency_stages=0,formal_dependency_derivatives=0,final_stages=0,choices=0,complete_method_banks=0)
 for r in records:
  q=r['question'];x,F,h,A,B,C,aa,bb,answer=task(q);sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==5
  rule=blocks[0].strip();assert rule==D+'='+FX+'+'+FY+r'\cdot '+YD,rule
  for bi,block in enumerate(blocks[1:],1):
   body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=body.split(r'\\');current=None
   for row in rows:
    # A single formal-partials row has both ordered components separated by ,\,.
    for piece in re.split(r',\\,',row):
     parts=[z.strip().rstrip('.,') for z in piece.replace('&','').split('=')];lhs=parts[0]
     if lhs:current=lhs
     assert current
     if current in (FX,FY,YD,D):
      want={FX:A if bi==1 else aa,FY:B if bi==1 else bb,YD:C,D:answer}[current]
     elif current.startswith(r'\frac{\text{d}}{\text{d}x}'):
      raw=current[len(r'\frac{\text{d}}{\text{d}x}'):];assert raw.startswith('(') and raw.endswith(')');want=s.diff(scalar(raw[1:-1]),x);stats['formal_dependency_derivatives']+=1
     else:raise AssertionError(('unknown displayed derivative',current))
     for expr in parts[1:]:
      if expr in (FX,FY,YD,D):got={FX:A if bi==1 else aa,FY:B if bi==1 else bb,YD:C,D:answer}[expr]
      else:got=scalar(expr)
      assert same(got,want),(r['generation']['template'],bi,piece,want,got)
      stats[{1:'partial_stages',2:'substitution_stages',3:'dependency_stages',4:'final_stages'}[bi]]+=1
  field=q[':question/answer-fields'][0];vals=[]
  for option in field[':answer-field/choices']:
   v=scalar(option[':answer/value']);assert same(v,answer)==(option[':answer/id']==field[':answer-field/correct'][1]);assert not any(same(v,w) for w in vals);vals.append(v);stats['choices']+=1
  expected=[aa+bb*C,aa,aa-bb*C,aa+bb,bb*C if r['generation']['template']=='reciprocal_exp' else aa+bb*h]
  assert all(any(same(v,w) for w in expected) for v in vals);stats['complete_method_banks']+=1;stats['records']+=1
 out=dict(status='passed',kp_id=k,source=src,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
