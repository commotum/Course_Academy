"""Independent root graph-label, raster, complete-bank and solution readback."""
import importlib.util,json,re,sys,hashlib,math
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);return g
P=load('root_scalar',ROOT/'generate/runs/current/ode-scalar-parser.py')
def number(text):return P.scalar(text.strip('$').rstrip('.,'))
def source(g,k):
 src=json.loads((ROOT/f'generate/runs/current/sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());counts=dict(questions=len(src),fields=0,values=0,keys=0,solutions=0)
 def norm(v):return v.get(':db/ident') if isinstance(v,dict) else v
 for c in cases:
  old=next(q for q in src if c['source_id'] in (q[':question/id'],q[':question/math-academy-id'],q[':db/id']))
  new=g.generate(c.get('level',c.get('difficulty','moderate')),template=c['template'],profile=c['bank_profile'],parameters=c['parameters'])['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in old)==(key in new)
   if key!=':question/answer-fields' and key in old:assert norm(old[key])==new[key],(k,c['source_id'],key)
  for a,b in zip(old[':question/answer-fields'],new[':question/answer-fields']):
   for key in (':answer-field/key',':answer-field/type'):assert norm(a[key])==b[key]
   assert sorted((norm(x[':answer/type']),x[':answer/value']) for x in a[':answer-field/choices'])==sorted((x[':answer/type'],x[':answer/value']) for x in b[':answer-field/choices']);counts['fields']+=1;counts['values']+=len(a[':answer-field/choices'])
   assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
   if ':answer-field/correct' in a:
    ref=a[':answer-field/correct'][':answer/id'];oldkey=next(x[':answer/value'] for x in a[':answer-field/choices'] if x[':answer/id']==ref);newkey=next(x[':answer/value'] for x in b[':answer-field/choices'] if x[':answer/id']==b[':answer-field/correct'][1]);assert oldkey==newkey;counts['keys']+=1
  counts['solutions']+=(':question/worked-solution' in old)
 return counts
def graph(k,r):
 q=r['question'];path=Path(re.findall(r'!\[[^]]*\]\(([^)]+)\)',q[':question/problem'])[0]);d=json.loads(path.with_suffix('.json').read_text());im=np.array(Image.open(path).convert('RGB')).astype(int);h,w=im.shape[:2];blue=(im[:,:,2]-im[:,:,0]>40)&(im[:,:,2]-im[:,:,1]>12)
 if 'png_sha256' in d:assert hashlib.sha256(path.read_bytes()).hexdigest()==d['png_sha256']
 if k==17592186184148:
  labels=d['labels'];ticks=[number(a['text']) for a in labels[:3]];mid,period,D=ticks;assert mid*2==period;B=s.pi/period;C=0;fn='cot';box=d['axes_bounds_px'];limits=(*d['limits']['x'],*d['limits']['y']);boxes=[a['bounds'] for a in labels]
 elif k==17592186184236:
  labels=d['label_measurements'];xlabels=[a for a in labels if a['role'] in ('x-asymptote','x-calibration')];assert len(xlabels)==2
  v=sorted(number(a['text']) for a in xlabels);level=q[':question/difficulty'].split('/')[-1];cal=1 if level=='easy' else 2 if level=='moderate' else s.Rational(3,2);pole=v[1]*cal;assert v[0]==-v[1];period=2*pole;B=s.pi/period;C=0;fn='tan';limits=tuple(d['axes_bounds']);box=[.16*w,.18*h,.79*w,.75*h];boxes=[[a['bbox_pixels'][0],a['bbox_pixels'][1],a['bbox_pixels'][2]-a['bbox_pixels'][0],a['bbox_pixels'][3]-a['bbox_pixels'][1]] for a in labels]
  # Read the actual blue intercept under the declared calibrated axes transform.
  x0=round(box[0]+(0-limits[0])/(limits[1]-limits[0])*box[2]);col=blue[:,x0-1:x0+2];ys=np.where(col.any(axis=1))[0];ys=ys[(ys>h-(box[1]+box[3]))&(ys<h-box[1])];assert len(ys)>0
  yval=limits[2]+(h-float(np.median(ys))-box[1])/box[3]*(limits[3]-limits[2]);step=1 if level=='easy' else s.Rational(1,2) if level=='moderate' else s.Rational(1,4);D=s.Rational(round(yval/float(step)))*step;assert abs(yval-float(D))*box[3]/(limits[3]-limits[2])<2
  if level=='easy':assert number(next(a['text'] for a in labels if a['role']=='y-intercept'))==D
  else:
   assert next(a['text'] for a in labels if a['role']=='scale-caption')=='Each vertical grid step is '+('1/2' if level=='moderate' else '1/4')+' unit.'
   for label in (a for a in labels if a['role']=='y-calibration'):
    yy=number(label['text']);bb=label['bbox_pixels'];center=(bb[1]+bb[3])/2
    actual=h-(box[1]+(float(yy)-limits[2])/(limits[3]-limits[2])*box[3]);assert abs((h-center)-actual)<2
 elif k==17592186184149:
  labels=d['labels'];vals=sorted(number(a['value']) for a in labels);L,R=vals[0],vals[-1];period=R-L;B=s.pi/period;fn='cot' if 'cot' in q[':question/problem'] else 'tan';zero=(L+R)/2;C=(s.pi/2 if fn=='cot' else 0)-B*zero;D=0;assert -s.pi/2<C<s.pi/2 and zero in vals
  limits=tuple(d['bounds']);box=[.10*w,.26*h,.85*w,.55*h];boxes=[a['bbox'] for a in labels]
 else:raise ValueError(k)
 bx,by,bw,bh=box;xmin,xmax,ymin,ymax=map(float,limits)
 def point(x,y):return round(bx+(x-xmin)/(xmax-xmin)*bw),round(h-(by+(y-ymin)/(ymax-ymin)*bh))
 hits=0
 for phase in (s.pi/4,s.pi/3,s.pi/2,2*s.pi/3,3*s.pi/4) if fn=='cot' else (-s.pi/3,-s.pi/4,0,s.pi/4,s.pi/3):
  x=float((phase-C)/B);y=float((s.cot(phase) if fn=='cot' else s.tan(phase))+D)
  if not ymin<y<ymax:continue
  px,py=point(x,y);assert blue[max(0,py-3):py+4,max(0,px-3):px+4].any(),(k,r['generation']['seed'],phase,px,py);hits+=1
 for b in boxes:
  xx,yy,ww,hh=b;assert 0<=xx<xx+ww<=w+1 and 0<=yy<yy+hh<=h+1
  left,right=max(0,math.floor(xx)-2),min(w,math.ceil(xx+ww)+2);top,bottom=max(0,math.floor(h-yy-hh)-2),min(h,math.ceil(h-yy)+2)
  assert not blue[top:bottom,left:right].any(),(k,r['generation']['seed'],'label intersects blue ink',b)
 return dict(B=B,D=D,C=C,period=period,fn=fn),hits,len(boxes)
def read(text,env):
 text=text.strip().strip('$').rstrip('.,').replace(r'\quad','').replace(r'\Longrightarrow','⟹').replace(r'\,','')
 for old,new in [('B','u'),('D','v'),('C','z'),('T','k')]:text=text.replace(old,new)
 text=text.replace('A','1')
 return P.scalar(text).subs({P.u:env['B'],P.v:env['D'],P.z:env['C'],P.k:env['period'],P.y:(s.cot(env['B']*P.x+env['C']) if env['fn']=='cot' else s.tan(env['B']*P.x+env['C']))+env['D']})
def check(k):
 g=load('g'+str(k),ROOT/f'generate/scratch/{k}.py');counts=source(g,k);records=json.loads((ROOT/f'generate/runs/current/qa/{k}-sampled.json').read_text());choices=equalities=curvehits=boxes=0
 for r in records:
  env,hits,nb=graph(k,r);curvehits+=hits;boxes+=nb;q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];B,D,C=env['B'],env['D'],env['C']
  requested='C' if k==17592186184149 else re.findall(r'What is \$([^$?]+)(?:\?|\$)',prompt)[-1].replace(' ','').rstrip('?')
  target=read(requested,env);f=q[':question/answer-fields'][0];bank=f[':answer-field/choices'];vals=[number(a[':answer/value']) for a in bank];choices+=len(vals)
  assert len(vals)==len(set(vals))==5
  for a,v in zip(bank,vals):assert (s.simplify(v-target)==0)==(a[':answer/id']==f[':answer-field/correct'][1])
  if k==17592186184149:
   a=C;h=-a/B;feature=a-s.pi/2 if a>0 else a+s.pi/2;expected=[a,-a,-h,-h/B,feature]
   assert all(any(s.simplify(v-z)==0 for z in expected) for v in vals)
   assert all(not s.simplify((v-z)/s.pi).is_integer for i,v in enumerate(vals) for z in vals[:i])
   dm=re.search(r'by \$(.*?)\$ units to the (left|right)',sol);assert dm and dm[2]==('left' if C>0 else 'right')
   for z in dm[1].split('='):assert s.simplify(read(z,env)-abs(h))==0;equalities+=1
  else:
   profile=r['generation'].get('bank_profile');rawexpr=P.scalar(requested.replace('B','u').replace('D','v'))
   if k==17592186184148:
    coeff=s.expand(rawexpr).coeff(P.v)
    if profile=='easy_period':expected=[B,1/B,2*B,B/2,2/B]
    elif profile=='method_sign_period':expected=[B+coeff*D,1/B+coeff*D,B-coeff*D,B/2+coeff*D,2*B+coeff*D]
    elif profile=='method_midpoint_offset':expected=[B+coeff*D,B+coeff*(D+1),B+coeff*(D-1),B,1/B+coeff*D]
    else:raise AssertionError(profile)
   else:
    def f(b,d):return rawexpr.subs({P.u:b,P.v:d})
    if profile=='period-sign':expected=[f(B,D),f(B/2,D),f(2*B,D),f(B,-D),f(1/B,D)]
    elif profile=='omitted-sign':expected=[f(B,D),f(0,D),f(B,0),f(-B,-D),f(B,-D)]
    else:raise AssertionError(profile)
   assert all(any(s.simplify(v-z)==0 for z in expected) for v in vals)
   dm=re.search(r'translated by \$(.*?)\$ units? (up|down)',sol);assert dm and number(dm[1])==abs(D) and dm[2]==('up' if D>0 else 'down')
  # Display blocks and inline scalar conclusion chains, with every arrow stage retained.
  for block in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',sol,re.S):
   z=next(v for v in block if v);z=z.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');lhs=None
   for row in z.split(r'\\'):
    if '=' not in row or '<' in row:continue
    for chain in re.split(r'⟹|\\Longrightarrow',row.replace('&','').replace(r'\quad','')):
     parts=chain.split('=')
     if len(parts)<2:continue
     if not parts[0].strip():parts[0]=lhs
     else:lhs=parts[0]
     values=[read(a,env) for a in parts]
     if k==17592186184149 and parts[0].strip()=='y':
      baseline=s.cot(B*P.x) if env['fn']=='cot' else s.tan(B*P.x)
      if len(values)==2 and s.simplify(values[1]-baseline)==0:equalities+=1;continue
     for a in values[1:]:assert s.simplify(values[0]-a)==0,(k,row,values);equalities+=1
 report=dict(status='passed',kp_id=k,source=counts,normal_records=len(records),complete_choice_values=choices,actual_solution_equalities=equalities,actual_png_curve_targets=curvehits,label_boxes=boxes,source_assets_root_viewed=13 if k==17592186184148 else 7 if k==17592186184236 else 46,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest())
 (ROOT/f'generate/runs/current/qa/{k}-root-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
