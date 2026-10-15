"""Parent reads prompt equation, all actual substitution stages and point pixels."""
import sys,json,re,importlib.util,hashlib,copy
from pathlib import Path
from PIL import Image
import numpy as np
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186054676;D=R.parents[2]/f'generate/scratch/{K}-draft';SCRIPT_SHA=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_point_scalar',R/'ode-scalar-parser.py');s=p.s;x=p.x;g=module('root_point_generator',D.with_suffix('.py'))
C=dict(records=0,substitution_rows=0,png_coordinates=0,source_records=0,source_fields=0,source_values=0,MA_originals=0,nonMA_inventory=0);targets={k:set() for k in ('easy','moderate','hard')};tasks={k:set() for k in targets}
def subset(text):return frozenset(re.findall(r'\$([ABC])\$',text))
def plotcheck(path,points):
 im=np.array(Image.open(path).convert('RGB'));black=np.max(im,axis=2)<80;ox=int(black.sum(axis=0).argmax());oy=int(black.sum(axis=1).argmax());gray=(np.ptp(im.astype(int),axis=2)<3)&(im[:,:,0]>175)&(im[:,:,0]<215)
 def step(counts):
  ids=np.where(counts>max(35,counts.max()*.6))[0];groups=[]
  for i in ids:
   if groups and i-groups[-1][-1]<3:groups[-1].append(i)
   else:groups.append([i])
  centers=[sum(a)/len(a) for a in groups];gaps=np.diff(centers);assert len(gaps)>=2;return float(sum(gaps)/sum(np.rint(gaps/np.median(gaps))))
 sx,sy=step(gray.sum(axis=0)),step(gray.sum(axis=1));assert abs(sx-sy)<1,(path,sx,sy)
 red=(im[:,:,0]>180)&(im[:,:,1]<100)&(im[:,:,2]<100)
 for xx,yy in points.values():
  px,py=round(ox+xx*sx),round(oy-yy*sy);assert red[max(0,py-4):py+5,max(0,px-4):px+5].sum()>5,(path,xx,yy,px,py);C['png_coordinates']+=1
 assert np.count_nonzero(red)>15
 return True
def check(record):
 r=record.get('record',record);q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];eq=p.scalar(re.search(r'\$y\s*=\s*([^$?]+)',prompt)[1]);pts={a:(int(b),int(c)) for a,b,c in re.findall(r'([ABC])=?\((-?\d+),(-?\d+)\)',sol.split('\n\n')[0])};assert set(pts)==set('ABC');truth={a for a,(xx,yy) in pts.items() if eq.subs(x,xx)==yy};fields=q[':question/answer-fields']
 if fields[0][':answer-field/type'].endswith('/checkbox'):
  assert len(fields)==3 and {f[':answer-field/key'] for f in fields}==set('ABC') and truth=={'B'} and 'Only B satisfies' in sol
  for f in fields:
   assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'true','false'};selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert(selected=='true')==(f[':answer-field/key'] in truth)
 else:
  assert len(fields)==1;f=fields[0];bank=[subset(a[':answer/value']) for a in f[':answer-field/choices']];assert len(set(bank))==len(bank)==5;assert next(subset(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==truth
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==3
  for a,block in zip('ABC',blocks):
   xx,yy=pts[a];ok=a in truth;rows=[z.strip() for z in block.split(r'\\')];assert len(rows)==3
   l0,r0=rows[0].split('&');assert l0.strip()=='y' and p.scalar(r0.strip().lstrip('='))==eq
   l1,r1=rows[1].split('&');assert p.scalar(l1)==yy;expr=r1.strip().lstrip('=');m=re.fullmatch(r'(.*?)\((-?\d+)\)(.*)',expr);assert m and p.scalar(m[1])==eq.coeff(x) and int(m[2])==xx and p.scalar(m[3]or'0')==eq.subs(x,0)
   l2,r2=rows[2].split('&');assert p.scalar(l2)==yy and p.scalar(r2.strip().lstrip('=').replace('✓','').replace(r'\times',''))==eq.subs(x,xx);assert ('✓' in r2)==ok
   assert re.search(r'Substituting the point \$'+a+r'\('+str(xx)+','+str(yy)+r'\)\$ results in (?:a )?'+('true'if ok else'false')+' statement:',sol)
   assert 'Therefore, the point $'+a+'$ does '+(''if ok else ('*not* ' if 'Therefore, the point $'+a+'$ does *not* ' in sol else'not '))+'lie on the line.' in sol;C['substitution_rows']+=3
  final=re.search(r'Finally, only points? (.*?) lie(?:s)? on the line\.',sol);assert final and subset(final[1])==truth
 path=Path(re.search(r'!\[\]\((.*?)\)',prompt)[1])
 if path.is_absolute():plotcheck(path,pts)
 level=q.get(':question/difficulty','unrated').split('/')[-1]
 if level in tasks:targets[level].add(''.join(sorted(truth)));tasks[level].add(str((eq,sorted(pts.values()))))
 if level=='hard':assert s.denom(eq.coeff(x)) in (2,3) and len(truth)==1
 C['records']+=1;return q
source=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']
for old in source:
 key=old.get(':question/math-academy-id') or old[':question/id'];q=check(g.replay_raw(key));expected=copy.deepcopy(old);expected.pop(':db/id',None)
 if ':question/difficulty' in expected:expected[':question/difficulty']=expected[':question/difficulty'][':db/ident']
 for f in expected[':question/answer-fields']:
  f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f[':answer-field/choices']:a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident']
  C['source_fields']+=1;C['source_values']+=len(f[':answer-field/choices'])
 assert q==expected;C['source_records']+=1;C['MA_originals'if ':question/math-academy-id'in old else'nonMA_inventory']+=1
for r in json.loads((D/'review-cases.json').read_text())+json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
assert targets['easy']=={'AB','AC','BC'} and targets['moderate']==targets['hard']=={'A','B','C'}
assert hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest()==SCRIPT_SHA
proof={'status':'passed','script_sha256':SCRIPT_SHA,'source_and_readback':C,'sampled_actual_tasks':{k:len(v)for k,v in tasks.items()},'member_role_coverage':{k:sorted(v)for k,v in targets.items()},'scope':'Read supplied integer grid coordinates, substitute into given linear equation, select complete membership subset. Rational-slope authored hard retains same three substitution tests; no line fitting or systems.','visual_review':'Root inspected original/controlled graph contact and full rendered hard52 player screenshot; point labels, axes and all operative fractions legible.','database_writes':0};(R/'qa'/f'{K}-root-readback.json').write_text(json.dumps(proof,indent=2)+'\n');print(proof)
