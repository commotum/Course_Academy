"""Root independent implicit conic banks/formal stages/prose and actual PNG geometry."""
import importlib.util,json,re,sys,math,hashlib
from pathlib import Path
from PIL import Image
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'implicit-conic-stages.py','p');x,y=p.x,p.y
geo={17592186166865:{'q-127359':(0,0,2,2),'q-127360':(1,-1,3,3),'q-127493':(0,0,4,4),'q-127497':(1,0,2,2),'q-127499':(-1,1,1,1),'q-127500':(-3,-2,2,2),'q-127502':(0,-2,3,3)},17592186166866:{'q-127362':(0,0,3,2),'q-127364':(2,-1,3,4),'q-127511':(0,0,1,2),'q-127512':(0,0,5,3),'q-127513':(0,0,2,5),'q-127514':(0,0,3,1),'q-127523':(-1,-1,2,1),'q-127525':(0,1,2,3),'q-127526':(3,0,3,2)}}
n=dict(records=0,choices=0,whole_banks=0,formal_inputs=0,printed_stages=0,complete_equations=0,raster_checks=0,blue_pixels=0,source_prompts=0,source_values=0,source_solutions=0,source_designations=0)
images=[]
def raster(path,expected):
 im=Image.open(path).convert('RGB');side=json.load(open(path.with_suffix('.json')))
 if 'axes_transform' in side:
  mat=side['axes_transform'];sx,sy=mat[0][0]*1.4,mat[1][1]*1.4;ox,oy=mat[0][2]*1.4,mat[1][2]*1.4
 else:
  t=side['pixel_transform'];factor=im.width/t['canvas_size'][0];sx=(t['unit_x'][0]-t['origin'][0])*factor;sy=(t['unit_y'][1]-t['origin'][1])*factor;ox,oy=[v*factor for v in t['origin']]
 assert math.isclose(sx,sy,rel_tol=1e-10)
 h,k,a,b=[float(z) for z in expected];cx,cy=ox+sx*h,im.height-(oy+sy*k);A,B=sx*a,sy*b
 blue=[]
 for i,c in enumerate(im.getdata()):
  if c[2]>120 and c[2]>1.5*c[0] and c[1]>1.4*c[0]:blue.append((i%im.width,i//im.width))
 assert blue
 bbox=[min(u for u,v in blue),max(u for u,v in blue),min(v for u,v in blue),max(v for u,v in blue)];wanted=[cx-A,cx+A,cy-B,cy+B];assert all(abs(v-w)<=4 for v,w in zip(bbox,wanted)),(path,bbox,wanted)
 for u,v in blue:
  dx,dy=u-cx,v-cy;q=(dx/A)**2+(dy/B)**2;grad=2*math.sqrt((dx/A**2)**2+(dy/B**2)**2);assert abs(q-1)/grad<=4,(path,u,v,q)
 n['raster_checks']+=1;n['blue_pixels']+=len(blue)
 return side

def check(r,kp):
 q=r['question'];m=r['generation'];assert m['eligible_for_learning']==(not m['evidence_only']);imgref=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1];path=Path(imgref);sid=m.get('source_id') or (re.search(r'q-\d+',m['bank_profile'])[0] if re.search(r'q-\d+',m['bank_profile']) else None);circle=kp==17592186166865
 if ':question/worked-solution' in q:
  data=p.parse_solution(q[':question/worked-solution']);h,k,a,b=[data[z] for z in ('h','k','a','b')];curve=data['curve'];answer=data['answer'];n['formal_inputs']+=data['formal_inputs'];n['printed_stages']+=data['stages'];n['complete_equations']+=data['equations']
 else:
  if imgref.startswith('images/'):h,k,a,b=map(s.sympify,geo[kp][sid])
  else:
   side=json.load(open(path.with_suffix('.json')));h,k=map(s.sympify,side['center']);a,b=(s.sympify(side['parameters']['r']),)*2 if circle else map(s.sympify,side['semiaxes'])
  curve=(x-h)**2/a**2+(y-k)**2/b**2-1;answer=p.p.slope(curve)
 if imgref.startswith('images/'):
  assert all(p.same(v,s.sympify(w)) for v,w in zip((h,k,a,b),geo[kp][sid]));path=Path('/media/jake/SSD/EDB/math')/imgref
 else:raster(path,(h,k,a,b))
 f=q[':question/answer-fields'][0];vs=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(vs)==5 and all(not p.p.same_on_curve(u,v,curve) for i,u in enumerate(vs) for v in vs[:i]);good=[i for i,v in enumerate(vs) if p.p.same_on_curve(v,answer,curve)];assert len(good)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][good[0]][':answer/id']==f[':answer-field/correct'][1]
 if not m['evidence_only']:
  U,V=x-h,y-k
  expected=[-U/V,U/V,-V/U,-2*U/V,-U/(2*V)] if circle else [-b*b/(a*a)*U/V,b*b/(a*a)*U/V,-a*a/(b*b)*U/V,-b/a*U/V,-a*a/(b*b)*V/U]
  assert all(sum(p.p.same_on_curve(v,e,curve) for v in vs)==1 for e in expected),'Whole implicit-derivative method bank differs'
 images.append({'kp':kp,'level':q.get(':question/difficulty','unrated'),'path':str(path),'parameters':[str(z) for z in (h,k,a,b)]});n['records']+=1;n['choices']+=5;n['whole_banks']+=1

if __name__=='__main__':
 kp=int(sys.argv[1]);D=ROOT/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'g');old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']};assert json.load(open(D/'source.json'))==json.load(open(R/'sources'/f'{kp}.json'))
 for c in json.load(open(D/'source-cases.json')):
  level=c.get('level',c.get('assigned_level',c.get('difficulty')));r=g.generate(level,template=c.get('template'),profile=c['bank_profile'],parameters=c['parameters']);check(r,kp);q=r['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   ov=next(z[':answer/value'] for z in of[':answer-field/choices'] if z[':answer/id']==of[':answer-field/correct'][':answer/id']);gv=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert ov==gv;n['source_designations']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for r in json.load(open(D/'review.json')):check(r.get('record',r),kp)
 for level in ('easy','moderate','hard'):
  for seed in range(5):
   r=g.generate(level,seed=32000+seed);check(r,kp);z=g.generate(level,seed=33000+seed,parameters=r['generation']['parameters']);assert r['question'][':question/id']==z['question'][':question/id']
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');(R/'qa'/f'{kp}-images.json').write_text(json.dumps(images,indent=2)+'\n');print(n)
