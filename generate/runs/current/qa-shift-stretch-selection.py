"""Root independently reads full transformation/intercept methods and banks."""
import sys,re,json,hashlib,importlib.util,math
from pathlib import Path
import sympy as s
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','scalar');x=p.x
n=dict(records=0,choices=0,graph_stages=0,intercept_stages=0,conclusions=0,whole_banks=0,pngs=0,curve_pixel_checks=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
seen=set()
def same(a,b):return s.simplify(a-b)==0
def formula(text):
 text=text.rstrip(',?.');m=re.fullmatch(r'y\s*=\s*(.*?)',text);assert m;return p.scalar(m[1])
def features(e):
 powers=[a for a in s.preorder_traversal(e) if isinstance(a,s.Pow) and a.exp.has(x)];assert len(powers)==1;power=powers[0];B=power.base;assert B>1;C=s.expand(e).coeff(power,0);A=s.simplify((e-C)/power);assert A.is_Rational and C.is_Rational and same(power.exp,x);return A,B,C

def raster(path,expected):
 path=Path(path)
 if path in seen:return
 side=json.load(open(path.with_suffix('.json')));assert hashlib.sha256(path.read_bytes()).hexdigest()==side['png_sha256'];o=side['spec']['curve'];A,B,C,H=[s.Rational(o[k]) for k in ('a','b','c','h')];sign=o['s'];assert same(A*B**(sign*(x-H))+C,expected);mx,my=map(s.Rational,o['mark']);assert same(expected.subs(x,mx),my)
 im=Image.open(path).convert('RGB');w,h=im.size;assert(w,h)==(480,400);rgb=im.load();left=.04*w;right=.93*w;bottom=.96*h;top=.07*h;lo=min(0,float(C),float(my))-max(1,abs(float(A))*.8);hi=max(0,float(C),float(my))+max(1,abs(float(A))*1.8);xmin=min(-3,float(H)-2);xmax=max(2.1,float(H)+3,float(mx)+3)
 px=lambda X:left+(right-left)*(X-xmin)/(xmax-xmin);py=lambda Y:bottom-(bottom-top)*(Y-lo)/(hi-lo);black=lambda X,Y:max(rgb[X,Y])<100
 ox=max(range(round(left)+2,round(right)-2),key=lambda X:sum(black(X,Y) for Y in range(round(top),round(bottom))));oy=max(range(round(top)+2,round(bottom)-2),key=lambda Y:sum(black(X,Y) for X in range(round(left),round(right))));assert abs(ox-px(0))<3 and abs(oy-py(0))<3
 for i in range(1,31):
  X=xmin+(xmax-xmin)*i/32;Y=float(expected.subs(x,X))
  if not lo+.08*(hi-lo)<Y<hi-.08*(hi-lo):continue
  xp,yp=round(px(X)),round(py(Y))
  # Current renderer is required to clear curves without hiding them.
  if abs(yp-py(0))<5 or abs(yp-py(float(C)))<5:continue
  colors=[rgb[a,b] for a in range(xp-4,xp+5) for b in range(yp-4,yp+5)];assert any(blue>100 and r<95 and g>65 for r,g,blue in colors);n['curve_pixel_checks']+=1
 # Actual renderer text bounds must clear actual modeled strokes and axes.
 curves=[(px(xmin+(xmax-xmin)*i/3999),h-py(float(A)*float(B)**(sign*(xmin+(xmax-xmin)*i/3999-float(H)))+float(C))) for i in range(4000)]
 layouts=side['label_layout'];assert len(layouts)==(2 if C else 1)
 for a in layouts:
  assert a['uses_background'] is False and a['collision'] is None
  l,b,r,t=a['bbox_pixels'];assert not l-4<=px(0)<=r+4 and not b-4<=h-py(0)<=t+4
  if C:assert not b-4<=h-py(float(C))<=t+4
  assert not(l-7<=px(float(mx))<=r+7 and b-7<=h-py(float(my))<=t+7)
  assert not any(l-4<=X<=r+4 and b-4<=Y<=t+4 for X,Y in curves)
  if a['kind']=='asymptote':assert p.scalar(a['text'].split('=',1)[1])==C
  else:assert tuple(p.scalar(z) for z in a['text'].strip('()').split(','))==(mx,my)
 seen.add(path);n['pngs']+=1

def check(rec):
 q=rec['question'];g=rec['generation'];A,B,C=features(formula(q[':question/problem'].split('$')[1]));U=A+C;kind='intercept' if g['template'].startswith('intercept') else 'graph';f=q[':question/answer-fields'][0];sol=q.get(':question/worked-solution');normal=g['eligible_for_learning']
 if sol:
  if kind=='graph':
   equations=re.findall(r'\$y=(.*?)\$',sol);assert len(equations)==6
   for z,e in zip(equations,[B**x,A*B**x,0,A*B**x+C,0,C]):assert same(p.scalar(z.rstrip(':.,')),e);n['graph_stages']+=1
   assert p.scalar(re.search(r'factor of \$(.*?)\.\$',sol)[1])==A
   points=re.findall(r'to \$\(0,(.*?)\),\$',sol);assert len(points)==2 and [p.scalar(z) for z in points]==[A,U]
   assert p.scalar(re.search(r'shift the above graph \$(.*?)\$',sol)[1])==abs(C) and (' units up' in sol or ' unit up' in sol)==(C>0)
   assert p.scalar(re.search(r'asymptote moves from \$y=0\$ to \$y=(.*?)\.\$',sol)[1])==C
   paths=re.findall(r'!\[\]\((.*?)\)',sol);assert len(paths)==3
   for path,e in zip(paths,[B**x,A*B**x,A*B**x+C]):
    if path.startswith('/'):raster(path,e)
  else:
   mathblocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(mathblocks)==3;first=mathblocks[0].strip().rstrip('.').split('=');assert first[0]=='y' and p.scalar(first[1])==A and p.scalar(first[2])==A
   second=mathblocks[1].strip().rstrip('.').split('=');assert second[0]=='y' and p.scalar(second[1])==U and p.scalar(second[2])==U
   block=mathblocks[2].strip().replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=[r.strip().replace('&','').rstrip('.') for r in block.split(r'\\')];assert len(rows)==4
   assert rows[0].split('=',1)[0].strip()=='y' and '^{0}' in rows[0] and p.scalar(rows[0].split('=',1)[1])==U
   assert r'\cdot 1' in rows[1];assert [p.scalar(r.split('=',1)[1]) for r in rows[1:]]==[U]*3;n['intercept_stages']+=7
   assert same(formula(re.search(r'Therefore, \$(.*?)\$',sol)[1]),A*B**x+C) and p.scalar(re.search(r'axis at \$\(0,(.*?)\)\.\$',sol)[1])==U;n['conclusions']+=1
 answers=f[':answer-field/choices'];vs=[]
 if kind=='intercept':
  vs=[tuple(p.scalar(z) for z in a[':answer/value'].strip('()').split(',')) for a in answers];equal=lambda a,b:a==b;correct=(s.Integer(0),U)
 else:
  geoms=g['bank_geometry'];byrecipe={o['recipe']:o for o in geoms};byvalue={}
  for recipe,a in zip(g['recipes'],geoms):
   e=s.Rational(a['a'])*s.Rational(a['b'])**(a['s']*(x-s.Rational(a['h'])))+s.Rational(a['c']);vs.append(e)
   if not g['original_asset_reuse']:byvalue[hashlib.sha256(json.dumps({'renderer_version':g['version'],'curve':a,'style':'source-ungridded-marked-features'},sort_keys=True,separators=(',',':')).encode()).hexdigest()+'.png']=e
  if byvalue:
   vs=[]
   for a in answers:e=byvalue[Path(a[':answer/value']).name];vs.append(e);raster(a[':answer/value'],e)
  else:
   rows=json.load(open(D/'source-geometry.json'))['plots'];mapping={o['path']:byrecipe[o['recipe']] for o in rows if o.get('profile')==g['bank_profile']};vs=[s.Rational(mapping[a[':answer/value']]['a'])*B**(mapping[a[':answer/value']]['s']*(x-s.Rational(mapping[a[':answer/value']]['h'])))+s.Rational(mapping[a[':answer/value']]['c']) for a in answers]
  equal=same;correct=A*B**x+C
 assert len(vs)==5 and all(not equal(v,w) for i,v in enumerate(vs) for w in vs[:i]) and sum(equal(v,correct) for v in vs)==1
 if ':answer-field/correct' in f:assert equal(vs[next(i for i,a in enumerate(answers) if a[':answer/id']==f[':answer-field/correct'][1])],correct)
 if normal:
  level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert kind=='graph' and A.q==C.q==1 and 2<=A<=8 and 0<abs(C)<=8
  elif level=='moderate':assert kind=='intercept' and A.q in (1,2) and C.q in (1,2) and s.Rational(3,2)<=A<=8 and abs(C)<=s.Rational(17,2)
  else:assert level=='hard' and kind=='graph' and A.q==C.q==2 and s.Rational(3,2)<=A<=s.Rational(13,2) and abs(C)<=s.Rational(17,2)
  wanted=[(0,U),(U,0),(0,A),(0,C),(0,A-C)] if kind=='intercept' else [A*B**x+C,A*B**(-x)+C,B**x+C,(A+2*C)*B**x-C,A*B**(x-A)+C];assert all(sum(equal(v,e) for v in vs)==1 for e in wanted);n['whole_banks']+=1
 n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186087823;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(rec);q=rec['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for a in json.load(open(D/'source-geometry.json'))['plots']:assert hashlib.sha256((Path('/media/jake/SSD/EDB/math')/a['path']).read_bytes()).hexdigest()==a['sha256']
 for rec in json.load(open(D/'review.json'))+json.load(open(D/'regressions.json'))+json.load(open(R/'qa'/f'{kp}-sampled.json')):check(rec)
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
