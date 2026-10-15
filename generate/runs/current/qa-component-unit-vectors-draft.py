"""Root recomputes 2D vector normalization from printed operands and every equation."""
import sys,json,re,hashlib,importlib.util,copy
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059716;D=R.parents[2]/f'generate/scratch/{K}-draft';SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_component_unit_scalar',R/'ode-scalar-parser.py');s=p.s;g=module('root_component_unit_gen',D.with_suffix('.py'));C=dict(records=0,source_MA_banks=0,source_MA_values=0,source_inventory_banks=0,source_inventory_values=0,existing_keys=0,source_prose=0,operative_equalities=0,choice_vectors=0);tasks={l:set()for l in g.SUPPORTED_LEVELS}
matpat=r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}'
def mats(text):
 def sub(m):
  vals=[p.scalar(z)for z in m[1].split(r'\\')];assert len(vals)==2;return '('+s.latex(vals[0])+r'\cdot i+('+s.latex(vals[1])+r')\cdot j)'
 return re.sub(matpat,sub,text,flags=re.S)
def scalar(raw,env):
 raw=mats(raw.strip().rstrip('.,').replace('&','').replace(r'\mid','|').replace(r'\,','').replace(r'\dfrac',r'\frac'));raw=re.sub(r'\\mathbf\{([^{}]+)\}',r'\1',raw)
 def norm(m):
  v=scalar(m[1],env);assert v.has(p.i,p.j);a,b=v.coeff(p.i),v.coeff(p.j);assert s.expand(v-a*p.i-b*p.j)==0;return '('+s.latex(s.sqrt(a*a+b*b))+')'
 raw=re.sub(r'\|([^|]+)\|',norm,raw)
 raw=''.join(z if z.startswith('\\')else re.sub(r'[abnu]',lambda m:'('+s.latex(env[m[0]])+')'if m[0]in env else m[0],z)for z in re.split(r'(\\[A-Za-z]+)',raw))
 return s.expand(p.scalar(raw))
def vector(value):
 a,b=value.coeff(p.i),value.coeff(p.j);assert s.expand(value-a*p.i-b*p.j)==0;return s.Matrix([a,b])
def givens(q):
 prompt=q[':question/problem'];env={}
 # Two nested captures require explicit match groups.
 for m in re.finditer(r'([abn])\s*=\s*('+matpat+r')',prompt,re.S):env[m[1]]=scalar(m[2],{})
 target=re.search(r'parallel to \$(.*?)\$',prompt)[1];target=re.sub(r'\\mathbf\{([^{}]+)\}',r'\1',target)
 if not env:
  # Canonical capture omits operand labels, supplied in its own worked first sum.
  ms=re.findall(matpat,prompt,re.S);assert len(ms)==2 and ':question/answer-fields'not in q
  env={label:scalar(r'\begin{bmatrix}'+body+r'\end{bmatrix}',{})for label,body in zip('ab',ms)}
 V=vector(scalar(target,env));length=s.sqrt(V.dot(V));assert length>0;env['u']=s.expand((V[0]*p.i+V[1]*p.j)/length);return env,V,length,target
def check(q,level=None):
 env,V,L,target=givens(q);sol=q.get(':question/worked-solution','')
 for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
  block=mats(block).replace(r'\begin{aligned}','').replace(r'\end{aligned}','');previous=None
  for row in block.split(r'\\'):
   parts=row.strip().split('=');assert len(parts)>=2;values=[]
   for i,part in enumerate(parts):
    if not part.replace('&','').strip():assert i==0 and previous is not None;v=previous
    else:v=scalar(part,env)
    values.append(v)
   assert all(s.simplify(v-values[0])==0 for v in values[1:]),(row,values);previous=values[-1];C['operative_equalities']+=len(values)-1
 fields=q.get(':question/answer-fields',[])
 if fields:
  assert len(fields)==1;f=fields[0];values=[vector(scalar(a[':answer/value'],env))for a in f[':answer-field/choices']];assert len(values)==len({tuple(v)for v in values})==5;same_direction='same direction'in q[':question/problem'];good=[i for i,v in enumerate(values)if s.simplify(v.dot(v)-1)==0 and s.simplify(v[0]*V[1]-v[1]*V[0])==0 and(not same_direction or s.simplify(v.dot(V))>0)];assert len(good)==1
  if f.get(':answer-field/correct'):
   ref=f[':answer-field/correct'];cid=ref[1]if isinstance(ref,list)else ref[':answer/id'];assert f[':answer-field/choices'][good[0]][':answer/id']==cid
  C['choice_vectors']+=len(values)
 if level:tasks[level].add(str((env.get('a'),env.get('b'),env.get('n'),target)))
 C['records']+=1;return V,L,env
specs=json.loads((D/'replay-specifications.json').read_text())
for spec in specs:
 old=spec['original_record'];check(old);gen=spec.get('generated_replay')
 if gen is None:continue
 level='hard'if spec['parameters']['mode']=='combination'else'moderate';r=g.generate(level,parameters=spec['parameters'],profile=spec['profile']);q=r['question'];check(q,level)
 if old.get(':question/answer-fields'):
  env,_,_,_=givens(old);oldvals={tuple(vector(scalar(a[':answer/value'],env)))for a in old[':question/answer-fields'][0][':answer-field/choices']};env,_,_,_=givens(q);newvals={tuple(vector(scalar(a[':answer/value'],env)))for a in q[':question/answer-fields'][0][':answer-field/choices']};assert oldvals==newvals
  is_ma=spec['source_id'].startswith('q-');C['source_MA_banks'if is_ma else'source_inventory_banks']+=1;C['source_MA_values'if is_ma else'source_inventory_values']+=5
  if old[':question/answer-fields'][0].get(':answer-field/correct'):C['existing_keys']+=1
 if old.get(':question/worked-solution'):
  prose=lambda t:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$(?:\\.|[^$])*?\$','<math>',t,flags=re.S)).strip();assert prose(old[':question/worked-solution'])==prose(q[':question/worked-solution']);C['source_prose']+=1
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r['question'],r['question'][':question/difficulty'].split('/')[-1])
for level in g.SUPPORTED_LEVELS:
 for r in g.batch(level,count=24 if level=='easy'else 36,seed=314):check(r['question'],level)
allbatch=g.batch('all',count=12,seed=314);assert len(allbatch)==36 and len({r['generation']['parameter_fingerprint']for r in allbatch})==36
for row in g.original_parameters():
 level='hard'if row['mode']=='combination'else'moderate';check(g.generate(level,row)['question'],level)
base=g.generate('hard',g.original_parameters()[0]);mutations=[(r'\sqrt{169}',r'\sqrt{170}'),(r'\frac{1}{13}',r'\frac{1}{14}'),('0+(5)','1+(5)')]
for old,new in mutations:
 bad=copy.deepcopy(base);text=bad['question'][':question/worked-solution'];assert old in text;bad['question'][':question/worked-solution']=text.replace(old,new,1)
 try:check(bad['question'])
 except AssertionError:pass
 else:raise AssertionError('bad operative stage passed')
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA
proof={'status':'passed','script_sha256':SCRIPT_SHA,'source_and_readback':C,'sampled_actual_tasks':{l:len(v)for l,v in tasks.items()},'negative_controls':3,'scope':'2D direct normalization and source scalar combination before normalization; E small integer-length authored, M direct integer/radical, H same supported combination roles. No3D/dot/angle branches.','database_writes':0};(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof)
