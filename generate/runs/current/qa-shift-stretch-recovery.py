"""Root reads actual prose, five substitution stages, full banks and graph pixels."""
import sys,re,json,hashlib,importlib.util,math
from pathlib import Path
import sympy as s
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','scalar');x=p.x;y=p.y;K=p.k
n=dict(records=0,choices=0,formal_rows=0,substitution_rows=0,conclusions=0,pngs=0,curve_pixels=0,whole_banks=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
sourcefeatures={'q-18518':(s.Integer(0),s.Integer(-2)),'q-18521':(s.Integer(2),s.Integer(-1)),'q-29233':(s.Integer(1),s.Integer(-2)),'q-7239':(s.Integer(2),s.Integer(-1)),'q-7241':(s.Rational(11,2),s.Integer(4)),'q-7243':(s.Integer(5),s.Integer(2)),'q-99778':(s.Integer(1),s.Integer(-2))};seen=set()
def same(a,b):return s.simplify(a-b)==0
def eq(raw):assert raw.strip().startswith('y');return p.scalar(raw.split('=',1)[1])
def raster(path,B,A,C,level,step):
 path=Path(path)
 if path in seen:return
 side=json.load(open(path.with_suffix('.json')));meta=side['parameters'];assert s.Rational(meta['b'])==B and s.Rational(meta['k'])==A and s.Rational(meta['c'])==C
 im=Image.open(path).convert('RGB');w,h=im.size;assert (w,h)==(756,588);rgb=im.load();left=.07*w;right=.97*w;top=.03*h;bottom=.93*h;lo=min(-1,float(C)-1);hi=max(2,float(A+C)+2);xmin=-4;xmax=math.log(1+5/float(A),float(B));px=lambda X:left+(right-left)*(X-xmin)/(xmax-xmin);py=lambda Y:bottom-(bottom-top)*(Y-lo)/(hi-lo)
 black=lambda X,Y:max(rgb[X,Y])<100
 ox=max(range(round(left)+2,round(right)-2),key=lambda X:sum(black(X,Y) for Y in range(round(top),round(bottom))));oy=max(range(round(top)+2,round(bottom)-2),key=lambda Y:sum(black(X,Y) for X in range(round(left),round(right))));assert abs(ox-px(0))<3 and abs(oy-py(0))<3
 row=round(py(float(C)));assert sum(any(black(X,Y) for Y in range(row-2,row+3)) for X in range(round(left)+5,ox-45))>.2*(ox-45-left)
 for X in (-3,-2,-1,0,1):
  Y=float(A)*float(B)**X+float(C)
  if Y>=hi-.2 or X>=xmax-.1:continue
  Xp,Yp=round(px(X)),round(py(Y));colors=[rgb[i,j] for i in range(Xp-4,Xp+5) for j in range(Yp-4,Yp+5)];assert any(b>100 and b>r+45 and g>r+25 for r,g,b in colors);n['curve_pixels']+=1
 if level=='hard':
  values=[step*i for i in range(math.ceil(lo/float(step)),math.floor(hi/float(step))+1) if i];assert [s.Rational(t['value']) for t in side['ticks']]==values
  named=[t for t in side['ticks'] if t['labeled']];assert len(named)>=2
  assert all(t['index']%t['regular_named_stride']==0 and t['regular_named_stride'] in (2,4,8,16) for t in named)
  wanted=[t['value'] for t in named];assert side['labels']==wanted and str(C) not in wanted and str(A+C) not in wanted
  for t in named:assert abs(t['text_position_data'][1]-float(s.Rational(t['value'])))<1e-8
 else:
  layouts=[l for l in side['label_layout'] if l['kind'] in ('intercept','asymptote')];assert len(layouts)==2
  point=next(l for l in layouts if l['kind']=='intercept')['text'];assert tuple(p.scalar(z) for z in point.strip('()').split(','))==(0,A+C)
  assert p.scalar(next(l for l in layouts if l['kind']=='asymptote')['text'].split('=',1)[1])==C
 # Measured actual text must clear curve, axis, asymptote and dot.
 curves=[(px(xmin+(xmax-xmin)*i/3999),h-py(float(A)*float(B)**(xmin+(xmax-xmin)*i/3999)+float(C))) for i in range(4000)]
 layouts=side['label_layout'];assert side['parameters']['version']=='shift-stretch-v5'
 for a in layouts:
  assert a['uses_background'] is False and a['collision'] is None
  l,b,r,t=a['bbox_pixels'];assert not l-4<=px(0)<=r+4 and not b-4<=h-py(0)<=t+4
  assert not b-4<=h-py(float(C))<=t+4
  assert not(l-7<=px(0)<=r+7 and b-7<=h-py(float(A+C))<=t+7)
  assert not any(l-4<=X<=r+4 and b-4<=Y<=t+4 for X,Y in curves)
 seen.add(path);n['pngs']+=1

def check(rec):
 q=rec['question'];g=rec['generation'];f=q[':question/answer-fields'][0];problem=q[':question/problem'];B=p.scalar(re.search(r'k\((.*?)\)\+\s*c',problem.replace(' ',''))[1]).subs(x,1);normal=g['eligible_for_learning'];path=re.search(r'!\[\]\((.*?)\)',problem)[1]
 sol=q.get(':question/worked-solution')
 if sol:
  C=p.scalar(re.search(r'so \$c=(.*?)\.\$',sol)[1]);U=p.scalar(re.search(r'point on the graph is \$\(0,(.*?)\),\$',sol)[1]);A=U-C
  assert p.scalar(re.search(r'horizontal asymptote is \$y=(.*?)\$ so',sol)[1])==C
  block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1];rows=[r.replace('&','').strip() for r in block.split(r'\\')];assert len(rows)==5
  sides=[tuple(p.scalar(z) for z in r.split('=')) for r in rows];assert sides[0]==(y,K*B**x+C) and same(sides[1][0],U) and same(sides[1][1],K+C) and same(sides[2][0],U) and same(sides[2][1],K+C) and same(sides[3][0],U) and same(sides[3][1],K+C) and sides[4]==(A,K)
  assert '^{0}' in rows[1] and 'k(1)' in rows[2] and not '(' in rows[3];n['formal_rows']+=1;n['substitution_rows']+=4
  assert p.scalar(re.search(r'substitute \$x=(.*?)\$',sol)[1])==0 and p.scalar(re.search(r'and \$y=(.*?)\$ into',sol)[1])==U
  if f[':answer-field/choices'][0][':answer/type'].endswith('/text'):
   assert p.scalar(re.search(r'Therefore, \$k=(.*?)\$',sol)[1])==A and p.scalar(re.search(r'and \$c=(.*?)\.\$',sol)[1])==C
  else:assert same(eq(re.search(r'Therefore, the curve is \$(.*?)\.\$',sol)[1]),A*B**x+C)
  n['conclusions']+=1
 else:
  assert g['evidence_only'];U,C=sourcefeatures[g['source_id']];A=U-C
 if '17592186087824/plots' in path:
  if not sol:
   side=json.load(open(Path(path).with_suffix('.json')));A=s.Rational(side['parameters']['k']);C=s.Rational(side['parameters']['c'])
  raster(path,B,A,C,q.get(':question/difficulty',':question.difficulty/'+g['generation_level'] if 'generation_level' in g else ':question.difficulty/easy').split('/')[-1],s.Rational(g['parameters']['step']))
 text=f[':answer-field/choices'][0][':answer/type'].endswith('/text')
 vs=[(p.scalar(re.search(r'\$k\s*=\s*(.*?)\$',a[':answer/value'])[1]),p.scalar(re.search(r'\$c\s*=\s*(.*?)\$',a[':answer/value'])[1])) if text else eq(a[':answer/value']) for a in f[':answer-field/choices']]
 equal=lambda a,b:a==b if text else same(a,b);correct=(A,C) if text else A*B**x+C
 assert len(vs)==5 and all(not equal(v,w) for i,v in enumerate(vs) for w in vs[:i]);assert sum(equal(v,correct) for v in vs)==1
 if ':answer-field/correct' in f:assert equal(vs[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])],correct)
 if normal:
  level=q[':question/difficulty'].split('/')[-1];step=s.Rational(g['parameters']['step']);assert 2<=B<=6 and B.q==1 and 1<=A<=6 and C!=0 and abs(C)<=6 and abs(U)<=10
  if level=='easy':assert A.q==C.q==1 and step==1 and text
  elif level=='moderate':assert A.q in (1,2) and C.q==1 and step==1 and not text
  else:assert level=='hard' and A.q>1 and C.q>1 and step in (s.Rational(1,2),s.Rational(1,4)) and (A/step).q==(C/step).q==1 and U!=0 and not text
  params=[(A,C),(U,C),(A,-C),(U,0),(C,A)] if g['bank_profile']=='intercept_shift' else [(A,C),(A-step,C+step),(A+step,C-step),(A+step,C),(U,C)]
  expected=params if text else [a*B**x+c for a,c in params];assert all(sum(equal(v,e) for v in vs)==1 for e in expected);n['whole_banks']+=1
 n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186087824;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(rec);q=rec['question'];o=old[c.get('ma_source_id',c.get('source_math_academy_id',rec['generation']['source_id']))]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for a in json.load(open(D/'plot-extraction.json')):assert hashlib.sha256((Path('/media/jake/SSD/EDB/math')/a['asset']).read_bytes()).hexdigest()==a['sha256']
 for rec in json.load(open(D/'review.json'))+json.load(open(R/'qa'/f'{kp}-sampled.json')):check(rec)
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
