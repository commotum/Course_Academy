"""Root reads printed equations/prose, whole banks and actual graph pixels."""
import sys,re,json,hashlib,importlib.util,math
from pathlib import Path
import sympy as s
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'spatial-jacobian-readback.py','scalar');x=p.x
n=dict(records=0,choices=0,solution_equations=0,pngs=0,curve_pixel_checks=0,ticks=0,whole_banks=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
seen=set();sourceC={'q-26807':-4,'q-7228':1,'q-170593':s.Rational(-3,2),'q-26804':10,'q-99774':-5,'q-99775':-3,'q-7230':-2,'q-7232':-3}
def eq(v):
 assert v.strip().startswith('y');return p.scalar(v.split('=',1)[1].strip().rstrip('.'))
def raster(path,B,C,level,step):
 path=Path(path)
 if path in seen:return
 side=json.load(open(path.with_suffix('.json')));a=side['parameters'];assert a['version']=='shift-asymptote-1.2';assert s.Rational(a['b'])==B and s.Rational(a['c'])==C and a['level']==level
 im=Image.open(path).convert('RGB');w,h=im.size;assert (w,h)==(756,588);rgb=im.load();left=.07*w;right=.97*w;top=.03*h;bottom=.93*h;lo,hi=float(C-2 if C-2<-2 else -2),float(C+4 if C+4>3 else 3);xmin=-4;xmax=max(1.5,math.log(hi-float(C),float(B)));px=lambda x:left+(right-left)*(x-xmin)/(xmax-xmin);py=lambda y:bottom-(bottom-top)*(y-lo)/(hi-lo)
 black=lambda X,Y:max(rgb[X,Y])<100
 ox=max(range(round(left)+2,round(right)-2),key=lambda X:sum(black(X,Y) for Y in range(round(top),round(bottom))));oy=max(range(round(top)+2,round(bottom)-2),key=lambda Y:sum(black(X,Y) for X in range(round(left),round(right))));assert abs(ox-px(0))<3 and abs(oy-py(0))<3
 # Dashed level must occupy many actual dark pixels across the left half.
 row=round(py(float(C)));assert sum(any(black(X,Y) for Y in range(row-2,row+3)) for X in range(round(left),round(px(-1))))>30
 for X in [-3,-2,-1,0,1]:
  Y=float(B)**X+float(C)
  if Y>=hi-.2 or X>=xmax-.1:continue
  Xp,Yp=round(px(X)),round(py(Y));colors=[rgb[i,j] for i in range(Xp-4,Xp+5) for j in range(Yp-4,Yp+5)];assert any(b>100 and b>r*1.4 and g>r*1.2 for r,g,b in colors),(path,X,Y);n['curve_pixel_checks']+=1
 if level=='hard':
  values=[step*k for k in range(math.ceil(lo/float(step))+1,math.floor(hi/float(step))) if k];assert [s.Rational(t['value']) for t in side['ticks']]==values
  wanted=[str(v) for v in values if (v/step)%2==0 and v!=C];assert side['labels']==wanted and str(C) not in wanted
  for v in values:
   Y=round(py(float(v)));assert any(black(X,Z) for X in range(ox-6,ox+7) for Z in range(Y-1,Y+2));n['ticks']+=1
 else:
  assert side['labels']==['y='+str(C)];boxes=side['feature_label_boxes'];assert len(boxes)==1 and boxes[0]['text']=='y='+str(C)
  l,b,r,t=boxes[0]['bounds'];assert not b-4<=h-py(0)<=t+4 and not b-4<=h-py(float(C))<=t+4
  assert not l-4<=px(0)<=r+4
  for X in [-4+i*(xmax+4)/1199 for i in range(1200)]:
   Y=float(B)**X+float(C)
   if Y<hi-.15:assert not (l-4<=px(X)<=r+4 and b-4<=h-py(Y)<=t+4)
 assert not side['intercept_marked'];seen.add(path);n['pngs']+=1

def check(rec):
 q=rec['question'];g=rec['generation'];normal=g['eligible_for_learning'];f=q[':question/answer-fields'][0];vs=[eq(a[':answer/value']) for a in f[':answer-field/choices']]
 if normal:
  braw=re.search(r'curve \$y=(.*?)\+c\.\$',q[':question/problem'])[1];B=p.scalar(braw).subs(x,1);assert B>1
  sol=q[':question/worked-solution'];cs=re.findall(r'\$c=(.*?)\.\$',sol);assert len(cs)==1;C=p.scalar(cs[0]);assert p.same(eq(re.search(r'horizontal asymptote is \$(y=.*?)\.\$',sol)[1]),C)
  bases=re.findall(r'\$y=(.*?)\$',sol);assert len(bases)==5 and p.same(p.scalar(bases[0]),B**x) and bases[1]=='0.' and p.same(p.scalar(bases[2].replace('+c','')),B**x) and bases[3]=='c.' and p.same(p.scalar(bases[4].rstrip('.')),C);n['solution_equations']+=5
  level=q[':question/difficulty'].split('/')[-1];step=s.Rational(g['parameters']['step']);assert C!=0 and abs(C)<=12
  if level=='easy':assert C.q==B.q==1 and step==1
  elif level=='moderate':assert 2<=C.q<=6 and step==1
  else:assert level=='hard' and C.q>1 and step in [s.Rational(1,2),s.Rational(1,3),s.Rational(1,4)] and (C/step).q==1 and abs(C/step)<=8
  profile=g['bank_profile'];base=B**x
  expected={'signed_intercept':[base+C,base+C+1,base-C+1,base-C-1,base-C],'confuse_shift_stretch':[base+C,base-C,base,C*base,-C*base],'intercept_offset':[base+C,base+C+1,base+C-1,C*base,(C-1)*base],'axis_reading':[base+C,base+C+step,base+C-step,base-C,base]}[profile]
  assert all(sum(p.same(v,e) for v in vs)==1 for e in expected);n['whole_banks']+=1;raster(re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1],B,C,level,step)
 else:
  sid=g['source_id'];C=sourceC[sid];prompt=q[':question/problem'];chunk=re.search(r'\$y\s*=\s*(.*?)\+\s*c[.$]',prompt)[1];B=p.scalar(chunk).subs(x,1)
  assert g['evidence_only']
  asset=re.search(r'!\[\]\((.*?)\)',prompt)[1]
  if '17592186087822/plots' in asset:
   C=s.Rational(json.load(open(Path(asset).with_suffix('.json')))['parameters']['c']);raster(asset,B,C,q.get(':question/difficulty',':question.difficulty/easy').split('/')[-1],s.Integer(1))
   if ':question/worked-solution' in q:assert p.same(p.scalar(re.findall(r'\$c=(.*?)\.\$',q[':question/worked-solution'])[0]),C)
 assert len(vs)==5 and all(not p.same(v,w) for i,v in enumerate(vs) for w in vs[:i]);correct=B**x+C;assert sum(p.same(v,correct) for v in vs)==1
 if ':answer-field/correct' in f:assert p.same(vs[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])],correct)
 n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186087822;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(rec);q=rec['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for a in json.load(open(D/'plot-source-inventory.json')):assert hashlib.sha256(Path(a['asset']).read_bytes()).hexdigest()==a['sha256']
 for rec in json.load(open(D/'review.json'))+json.load(open(R/'qa'/f'{kp}-sampled.json')):check(rec)
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
