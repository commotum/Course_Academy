"""Root actual parabola point, full source banks/teaching stages and PNG readback."""
import sys,re,json,importlib.util,math
from pathlib import Path
import sympy as s
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent

def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','parent');x,y=p.x,p.y;P=s.Symbol('p',real=True);D=s.Symbol('D',real=True)
n=dict(records=0,choices=0,whole_banks=0,formal_inputs=0,substitution_rows=0,derivative_rows=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,known_raw_errors=0,raster_checks=0,blue_pixels=0)
geo={'q-127372':(1,2),'q-127374':(-2,2),'q-127510':(3,6),'q-127515':(-1,2),'q-127520':(-8,4),'q-312780':(5,7),'q-342215':(-3,-1),'q-342218':(-6,6),'q-342354':(8,-8),'q-342355':(6,-2)}
DY=r'\frac{\text{d}y}{\text{d}x}';DX=r'\frac{\text{d}}{\text{d}x}'
def read(z):
 z=z.strip().rstrip('.,');z=re.sub(r'\\[A-Za-z]+|[pD]',lambda m:m[0] if m[0].startswith('\\') else {'p':'u','D':'v'}[m[0]],z)
 return p.scalar(z).subs({p.u:P,p.v:D})
def eq(z):
 l,r=z.replace('&','').split('=');return read(l)-read(r)
def same(a,b):return s.simplify(a-b)==0

def raster(path,a,b):
 side=json.load(open(path.with_suffix('.json')));im=Image.open(path).convert('RGB');bounds=side['bounds'];width,height=im.size;sx=width*.88/(bounds[0][1]-bounds[0][0]);sy=height*.88/(bounds[1][1]-bounds[1][0]);ox=width*.06-bounds[0][0]*sx;oy=height*.94+bounds[1][0]*sy
 orange=[];blue=[]
 for idx,c in enumerate(im.getdata()):
  if c[0]>180 and 90<c[1]<210 and c[2]<80:orange.append((idx%width,idx//width))
  if c[2]>120 and c[2]>1.5*c[0] and c[1]>1.4*c[0]:blue.append((idx%width,idx//width))
 assert orange and blue
 want=(ox+a*sx,oy-b*sy);centroid=(sum(z[0] for z in orange)/len(orange),sum(z[1] for z in orange)/len(orange));assert max(abs(z-w) for z,w in zip(centroid,want))<2
 c=b*b/a
 for px,py in blue:
  X,Y=(px-ox)/sx,(oy-py)/sy;value=Y*Y-c*X;grad=math.sqrt((c/sx)**2+(2*Y/sy)**2);assert abs(value)/grad<4,(path,px,py,value,grad)
 n['raster_checks']+=1;n['blue_pixels']+=len(blue)

def check(rec):
 q=rec['question'];gen=rec['generation'];sid=gen.get('source_id');asset=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1];sol=q.get(':question/worked-solution')
 easy=q.get(':question/difficulty','').endswith('/easy')
 if easy:
  assert sol and gen['template'].startswith('equation_')
  side=json.load(open(Path(asset).with_suffix('.json')));a,b=[side['parameters'][z] for z in ('a','b')]
  promptblock=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/problem'],re.S);assert len(promptblock)==1
  actualF=eq(promptblock[0]);assert s.expand(actualF-(y*y-s.Rational(b*b,a)*x))==0
 elif sol:
  a,b=[int(v) for v in re.search(r'passes through the point \$\((-?\d+),(-?\d+)\)',sol).groups()]
 else:a,b=geo[sid]
 if asset.startswith('images/'):assert (a,b)==geo[sid]
 else:raster(Path(asset),a,b)
 c=s.Rational(b*b,a);answer=c/(2*y);F=y*y-c*x;f=q[':question/answer-fields'][0];vs=[read(z[':answer/value']) for z in f[':answer-field/choices']]
 assert all(not same((u-v).subs(x,y*y/c),0) for idx,u in enumerate(vs) for v in vs[:idx]);valid=[idx for idx,v in enumerate(vs) if same((v-answer).subs(x,y*y/c),0)];assert len(valid)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][valid[0]][':answer/id']==f[':answer-field/correct'][1]
 if gen['eligible_for_learning'] and len(vs)>1:
  want=[answer,-answer,c/y,2*y/c,c/2];assert all(sum(same(z-w,0) for z in vs)==1 for w in want)
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem'] and all(not z.has(x) for z in vs)
 if sol:
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
  if easy:
   assert len(blocks)==2 and same(eq(blocks[0]),F) and 'Substituting' not in sol and '4px' not in sol
   rowblock=blocks[1]
  else:
   vertex=re.search(r'vertex is at \$\((-?\d+),(-?\d+)\)',sol);assert vertex
   if vertex.groups()!=('0','0'):assert sid=='q-127510' and gen['bank_profile'].startswith('raw:');n['known_raw_errors']+=1
   assert len(blocks)==4 and same(eq(blocks[0]).subs(P,c/4),F)
   rows=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3
   assert '^' in rows[0] and 'p' in rows[1] and rows[2].strip().startswith('p')
   for row in rows:assert same(eq(row).subs(P,c/4),0)
   assert same(eq(blocks[2]),F);rowblock=blocks[3];n['substitution_rows']+=3
  rows=rowblock.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3
  m=re.fullmatch(re.escape(DX)+r'\((.*?)\)\s*&\s*='+re.escape(DX)+r'\((.*?)\)',rows[0].strip());assert m
  l,r=[read(z) for z in m.groups()];assert l==y*y and r==c*x
  assert s.expand(eq(rows[1].replace(DY,'D'))-(2*y*D-c))==0
  assert same(eq(rows[2].replace(DY,'D')).subs(D,answer),0)
  n['formal_inputs']+=2;n['derivative_rows']+=2
 n['records']+=1;n['choices']+=len(vs);n['whole_banks']+=1
if __name__=='__main__':
 kp=17592186166867;D0=R.parents[2]/'generate/scratch'/str(kp);g=load(D0.with_suffix('.py'),'generator');source=json.load(open(D0/'source.json'));assert source==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for c in json.load(open(D0/'source-cases.json')):
  z=g.generate(c['level'],parameters=c['parameters'],profile=c['bank_profile'],template=c['template']);check(z);q=z['question'];o=olds[c['source_id']]
  for k in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (k in q)==(k in o)
   if k in o:assert q[k]==(o[k][':db/ident'] if k.endswith('difficulty') else o[k])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   value=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert value==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=len(f[':answer-field/choices']);n['source_solutions']+=int(':question/worked-solution' in o)
 for z in json.load(open(D0/'review.json')):check(z.get('record',z))
 for lv in ('easy','moderate','hard'):
  for seed in range(12):check(g.generate(lv,seed=67000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
