"""Root independently reads operand matrices, all printed arithmetic cells and whole banks."""
import copy,hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=R.parents[2]/f'generate/scratch/{K}-draft';sigma=-1 if K==17592186054649 else 1

def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
G=mod('root_entrywise_generator'+str(K),D.with_suffix('.py'));P=mod('root_entrywise_scalar'+str(K),R/'ode-scalar-parser.py');F=mod('root_entrywise_fidelity'+str(K),R/'root-source-fidelity.py')
originals,fidelity=F.check(G,K,D)
C=dict(records=0,printed_operand_cells=0,unevaluated_arithmetic_cells=0,collected_result_cells=0,whole_matrix_values=0,scalar_values=0,bank_pairs=0,complete_method_banks=0,level_checks=0,prose_masks=0,source_keys=0)
M=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def matrix(body):return s.Matrix([[P.scalar(v.replace(r'\,','').strip()) for v in row.split('&')] for row in body.split(chr(92)*2)])
def textmatrix(text):
 blocks=M.findall(text);assert len(blocks)==1;return matrix(blocks[0])
def mask(text):return re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$','@DISPLAY@',text,flags=re.S)).strip()
def check(r,raw=False):
 q,m=r['question'],r['generation'];prompt=q[':question/problem'];operands=M.findall(prompt);assert len(operands)==2
 a,b=map(matrix,operands);assert a.shape==b.shape;c=a+sigma*b;n=len(a);C['printed_operand_cells']+=2*n
 t=m['template'];profile=m.get('profile',m.get('bank_profile'));targets=m.get('parameters',{}).get('targets',list(range(n)))
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=M.findall(sol);assert len(blocks)==4
  aa,bb,ops,cc=map(matrix,blocks);assert aa==a and bb==b and ops==c and cc==c
  # Read the operative nodes before simplification: each cell must still show
  # actual corresponding operands and the assessed + or - operation.
  bodies=[[v.strip().replace(r'\,','') for row in body.split(chr(92)*2) for v in row.split('&')] for body in blocks]
  for actual,x,y in zip(bodies[2],a,b):
   op='+' if sigma==1 else '-';found=re.fullmatch(r'\(?(-?\d+)\)?\s*'+re.escape(op)+r'\s*\(?(-?\d+)\)?',actual);assert found and tuple(map(int,found.groups()))==(x,y),(K,t,actual,x,y)
   C['unevaluated_arithmetic_cells']+=1
  C['collected_result_cells']+=n
  assert ('We subtract the corresponding entries:' if sigma==-1 else 'We add the corresponding entries:') in sol
  sid=m.get('source_id',m.get('source_question'))
  if isinstance(sid,int):old=next((q for q in originals.values() if q[':db/id']==sid),None)
  else:old=originals.get(sid or t)
  if old is None and K==17592186054648:old=next(o for o in originals.values() if ':question/worked-solution' in o)
  if old and ':question/worked-solution' in old:assert mask(sol)==mask(old[':question/worked-solution']);C['prose_masks']+=1
 fields=q[':question/answer-fields'];radio=fields[0][':answer-field/type'].endswith('/radio')
 if radio:
  for f in fields:
   vals=[textmatrix(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5 and all(v.shape==c.shape for v in vals) and sum(v==c for v in vals)==1
   for v,w in itertools.combinations(vals,2):assert v!=w;C['bank_pairs']+=1
   if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if v==c]==[f[':answer-field/correct'][1]];C['source_keys']+=int(raw)
   if not raw:
    if sigma==-1:
     first=c.copy();first[0]=a[0]+b[0];second=c.copy();second[1]=b[1]-a[1];expected=[c,a+b,-c,first,second]
    elif K==17592186054648:
     if profile=='authored-correspondence':expected=[c,a-b,b-a,a,c.T]
     else:assert profile=='authored-signs';expected=[c,a+b.applyfunc(abs),a.applyfunc(abs)+b,-c,a+b.T]
    else:
     if profile=='method-omission':expected=[c,a,b,a-b,b-a]
     else:assert profile=='method-sign';expected=[c,-c,a-b,b-a,a.applyfunc(abs)+b.applyfunc(abs)]
    assert all(v in vals for v in expected);C['complete_method_banks']+=1
   C['whole_matrix_values']+=5
 else:
  assert len(fields)==len(targets)
  for j,f in enumerate(fields):
   key=f[':answer-field/key'];assert re.fullmatch(r'field-\d+',key) and len(f[':answer-field/choices'])==1;j=int(key.split('-')[-1])-1;assert 0<=j<len(targets)
   v=P.scalar(f[':answer-field/choices'][0][':answer/value']);assert v==c[targets[j]]
   if ':answer-field/correct' in f:assert f[':answer-field/correct'][1]==f[':answer-field/choices'][0][':answer/id'];C['source_keys']+=int(raw)
   C['scalar_values']+=1
  if K==17592186054649 and t=='q-319625':
   table=prompt.split('\n\n|',1)[1];entries=[]
   for line in table.splitlines():
    for cell in line.split('|'):
     cell=cell.strip()
     if re.fullmatch(r'\{\{field-\d+\}\}|\$-?\d+\$',cell):entries.append(cell)
   assert len(entries)==9
   for i,token in enumerate(entries):
    if i in targets:assert token=='{{field-'+str(targets.index(i)+1)+'}}'
    else:assert P.scalar(token.strip('$'))==c[i]
 if not raw:
  level=q[':question/difficulty'].split('/')[-1];av=list(a);bv=list(b)
  if K==17592186054648:
   if level=='easy':assert all(abs(x)<=12 for x in av+bv)
   elif level=='moderate':assert all(1<=abs(x)<=25 for x in av+bv) and sum(bool(x*y<0) for x,y in zip(av,bv))==2 and sum(bool(abs(x)>=10) for x in av+bv)>=2
   else:assert all(10<=abs(x)<=99 for x in av+bv) and all(x*y<0 for x,y in zip(av,bv)) and sum(bool(x>0) for x in c)==2 and sum(bool(x<0) for x in c)==2
  elif K==17592186054650:
   opposite=sum(bool(x*y<0) for x,y in zip(av,bv))
   if level=='easy':assert all(abs(x)<=9 for x in av+bv) and opposite<=2
   elif level=='moderate':assert all(1<=abs(x)<=16 for x in av+bv) and opposite==3 and sum(bool(x<0 and y<0) for x,y in zip(av,bv))==3
   else:assert all(10<=abs(x)<=16 for x in av+bv) and opposite==6 and all(x!=0 for x in c) and min(c)<0<max(c)
  else:
   assert all(abs(v)<=12 for v in av+bv)
   if level=='easy':assert all(0<=v<=9 for v in av+bv)
   elif level=='moderate':assert sum(bool(bv[i]<0) for i in targets)==1 and any(av[i]<0 for i in targets) and any(bv[i]>0 for i in targets)
   else:assert any(av[i]<0 and bv[i]<0 for i in targets) and any(av[i]>0 and bv[i]<0 for i in targets) and any(av[i]<0 and bv[i]>0 for i in targets)
  C['level_checks']+=1
 C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for template in G.TEMPLATES:
  for seed in (38,91):check(G.generate(level,seed,template=template))
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c.get('level','easy'),template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile'))),True)
regressions={}
if K==17592186054649:
 base=G.generate('easy',38,template='q-319625');p=copy.deepcopy(base['generation']['parameters']);unqueried=next(i for i in range(9) if i not in p['targets']);p['a'][unqueried]=p['a'][unqueried]+1 if p['a'][unqueried]<9 else p['a'][unqueried]-1;changed=G.generate('easy',38,template='q-319625',parameters=p)
 assert changed['generation']['mathematical_fingerprint']==base['generation']['mathematical_fingerprint'] and changed['question'][':question/id']!=base['question'][':question/id'];check(changed);regressions['unqueried_operand_and_given_cell_not_assessed']=True
 p=copy.deepcopy(base['generation']['parameters']);p['targets']=sorted([unqueried]+p['targets'][1:]);targetchange=G.generate('easy',38,template='q-319625',parameters=p);assert targetchange['generation']['mathematical_fingerprint']!=base['generation']['mathematical_fingerprint'];check(targetchange);regressions['changed_requested_target_actual_prompt_fields_solution']=True
result={'regressions':regressions,'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
