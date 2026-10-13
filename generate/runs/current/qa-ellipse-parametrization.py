"""Root independently reads whole ellipse banks and rendered coordinate recipes."""
import sys,re,json,hashlib,importlib.util
from pathlib import Path
import sympy as s
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','scalar');I=p.i
n=dict(records=0,choices=0,formal_coordinates=0,final_coordinates=0,prose_parameters=0,full_banks=0,pngs=0,pixel_targets=0,source_prompts=0,source_values=0,source_exact_values=0,source_solutions=0,source_refs=0)
seen=set()
def scalar(raw):return p.scalar(raw.replace(r'\theta','i').replace('θ','i').replace('⁡',''))
def same(a,b):return s.trigsimp(s.expand_trig(a-b))==0
def pair(raw):
 chunks=re.split(r',\s*(?:\\,|\\quad)?\s*y\s*=\s*',raw);assert len(chunks)==2,raw;assert chunks[0].strip().startswith('x');return scalar(chunks[0].split('=',1)[1]),scalar(chunks[1])
def valid(V,A,B,H,K,oriented):
 X,Y=V;locus=s.trigsimp(((X-H)/A)**2+((Y-K)/B)**2-1)==0
 return bool(locus and (not oriented or (same(X.subs(I,0),H+A) and same(Y.subs(I,0),K) and s.diff(Y,I).subs(I,0)>0)))
def raster(path,A,B,H,K,origin):
 path=Path(path)
 if path in seen:return
 side=json.load(open(path.with_suffix('.json')));a=np.asarray(Image.open(path).convert('RGB')).astype(int);h,w=a.shape[:2];blue=(a[:,:,2]>a[:,:,0]+50)&(a[:,:,2]>a[:,:,1]+15)&(a[:,:,0]<140);ys,xs=np.where(blue);assert len(xs)>50
 if origin:
  assert(w,h)==(700,700) and side['renderer_version']=='ellipse-v7';ox,oy=side['origin_pixel'];oy=h-oy;scale=616/(float(max(A,B))*3.4);assert side['a']==str(A) and side['b']==str(B)
  texts=[l['text'] for l in side['labels']]
  if side['hard']:assert set(str(i) for i in range(-int(max(A,B)),int(max(A,B))+1) if i and i%2==0).issubset(texts)
  else:
   assert set(map(str,[-int(A),int(A),-int(B),int(B)])).issubset(texts)
   # Signed y labels remain beside their y-axis endpoints, not detached far left.
   for l in side['labels']:
    if l['text'] in (str(int(B)),str(-int(B))):assert abs(l['data_position'][0])<.1*float(max(A,B))
 else:
  assert side['png_sha256']==hashlib.sha256(path.read_bytes()).hexdigest();ox,oy=side['origin_pixels'];sx,sy=side['scale_pixels'];assert abs(sx-sy)<1e-8;scale=sx
  assert tuple(side['parameters'][k] for k in ('a','b','h','k'))==tuple(map(int,[A,B,H,K]))
 black=np.max(a,axis=2)<100;assert abs(int(np.argmax(black.sum(axis=0)))-ox)<=3 and abs(int(np.argmax(black.sum(axis=1)))-oy)<=3
 # All actual blue extents must agree with printed/source-read ellipse parameters.
 expected=[ox+float(H-A)*scale,ox+float(H+A)*scale,oy-float(K+B)*scale,oy-float(K-B)*scale];actual=[xs.min(),xs.max(),ys.min(),ys.max()];assert max(abs(float(a)-b) for a,b in zip(actual,expected))<=4,(path,actual,expected)
 for j in range(32):
  t=2*np.pi*j/32;xp=round(ox+(float(H)+float(A)*np.cos(t))*scale);yp=round(oy-(float(K)+float(B)*np.sin(t))*scale);
  if origin and side['marked'] and j==0:assert black[max(0,yp-4):yp+5,max(0,xp-4):xp+5].sum()>30,(path,'marked endpoint')
  else:assert blue[max(0,yp-4):yp+5,max(0,xp-4):xp+5].any(),(path,j)
  n['pixel_targets']+=1
 seen.add(path);n['pngs']+=1

def check(rec):
 rec=rec.get('record',rec);q=rec['question'];g=rec['generation'];prompt=q[':question/problem'];oriented='counterclockwise' in prompt;sol=q.get(':question/worked-solution');raw=g.get('raw_replay',g.get('evidence_only'));sid=g.get('source_id') or (g.get('profile','').split(':',1)[1] if g.get('profile','').startswith('observed:') else None)
 if sol:
  if origin:
   m=re.search(r'In our case, \$a=(.*?)\$ and \$b=(.*?)\.\$',sol);assert m;A,B=map(scalar,m.groups());H=K=s.Integer(0);n['prose_parameters']+=2
  else:
   m=re.search(r'In our case, the ellipse is centered at the point \$\((-?\d+),(-?\d+)\),\$ \$a=(\d+)\$ and \$b=(\d+)\.\$',sol);assert m;H,K,A,B=map(s.Integer,m.groups());n['prose_parameters']+=4
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==2
  def normalize_generic(text):
   constants={'a':A,'b':B,'h':H,'k':K};return re.sub(r'\\[A-Za-z]+|[abhk]',lambda m:m[0] if m[0].startswith('\\') else '('+s.latex(constants[m[0]])+')',text)
  first=blocks[0].split(r',\,\theta')[0].split(r', \quad \theta')[0].split(r',\quad \theta')[0].strip();last=blocks[1].split(r',\,\theta')[0].split(r', \quad \theta')[0].split(r',\quad \theta')[0].strip()
  for V in (pair(normalize_generic(first)),pair(last)):
   assert same(V[0],A*s.cos(I)+H) and same(V[1],B*s.sin(I)+K)
  n['formal_coordinates']+=2;n['final_coordinates']+=2
  if oriented:assert 'counterclockwise' in sol and 'starting from' in sol
 else:
  sid=sid if isinstance(sid,str) else id_to_ma[sid];f=features[sid];A,B=s.Integer(f[0]),s.Integer(f[1]);H,K=(s.Integer(0),s.Integer(0)) if origin else (s.Integer(f[2]),s.Integer(f[3]))
 if not sol:
  plotted=re.search(r'!\[\]\((.*?)\)',prompt)
  if plotted and 'generate/scratch' in plotted[1]:
   side=json.load(open(Path(plotted[1]).with_suffix('.json')))
   if origin:A,B=s.Rational(side['a']),s.Rational(side['b'])
   else:A,B,H,K=[s.Integer(side['parameters'][z]) for z in ('a','b','h','k')]
 # Given quantities and start coordinates must agree with the actual solution.
 if origin:
  m=re.search(r'horizontal radius \$(.*?)\$ and vertical radius \$(.*?)',prompt)
  if m:
   first=m[1];second=re.search(r'vertical radius \$(.*?)\$',prompt)[1].rstrip(',.');assert scalar(first)==A and scalar(second)==B
  starts=re.findall(r'[AJ]\(([^,]+),([^)]*)\)',prompt)
  for X,Y in starts:assert scalar(X)==A and scalar(Y.rstrip('?.'))==0
 else:
  m=re.search(r'centered at \$\((-?\d+),(-?\d+)\)\$ with horizontal radius \$(\d+)\$ and vertical radius \$(\d+)',prompt)
  if m:assert tuple(map(s.Integer,m.groups()))==(H,K,A,B)
  starts=re.findall(r'A\((-?\d+),(-?\d+)\)',prompt)
  for X,Y in starts:assert (int(X),int(Y))==(H+A,K)
 if ':question/difficulty' in q and g['eligible_for_learning']:
  level=q[':question/difficulty'].split('/')[-1]
  if origin:
   assert H==K==0 and 2<=A<=9 and 2<=B<=9 and A!=B
   if level in ('easy','moderate'):assert A.q==B.q==1 and oriented==(level=='moderate')
   else:assert level=='hard' and (A.q==2 or B.q==2) and A.q in (1,2) and B.q in (1,2) and oriented
  else:assert A.is_Integer and B.is_Integer and 1<=A<=8 and 1<=B<=8 and A!=B and (H or K) and abs(H)<=6 and abs(K)<=6 and oriented==(level=='hard')
 for f in q[':question/answer-fields']:
  answers=f[':answer-field/choices'];radio=f[':answer-field/type'].endswith('/radio')
  if radio:
   vals=[pair(a[':answer/value']) for a in answers];assert len(vals)==5 and sum(valid(v,A,B,H,K,oriented) for v in vals)==1;assert all(not(same(v[0],w[0]) and same(v[1],w[1])) for i,v in enumerate(vals) for w in vals[:i]);n['full_banks']+=1
   if ':answer-field/correct' in f:assert valid(vals[next(i for i,a in enumerate(answers) if a[':answer/id']==f[':answer-field/correct'][1])],A,B,H,K,oriented)
  else:
   assert len(answers)==1 and '{{'+f[':answer-field/key']+'}}' in prompt;expected=A*s.cos(I)+H if f[':answer-field/key']=='field-1' else B*s.sin(I)+K;assert same(scalar(answers[0][':answer/value']),expected)
  n['choices']+=len(answers)
 path=re.search(r'!\[\]\((.*?)\)',prompt)
 if path and 'generate/scratch' in path[1]:raster(path[1],A,B,H,K,origin)
 n['records']+=1
if __name__=='__main__':
 kp=int(sys.argv[1]);assert kp in [17592186152187,17592186152189];origin=kp==17592186152187;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']};id_to_ma={q[':db/id']:q[':question/math-academy-id'] for q in old.values()};features=json.load(open(R/'qa'/f'{kp}-source-features.json'))['features']
 for c in json.load(open(D/'source-cases.json')):
  sourcekey=c['source_id'];sq=old[id_to_ma.get(sourcekey,sourcekey)];level=c.get('level',c.get('difficulty',sq.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]))
  rec=g.generate(level,template=c['template'],profile=c.get('bank_profile',c.get('profile')),parameters=c['parameters']);check(rec);q=rec['question'];sid=c.get('math_academy_id',c.get('source_ma_id',c['source_id']));sid=id_to_ma.get(sid,sid);o=old[sid]
  for key in [':question/problem',':question/worked-solution',':question/difficulty']:
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  assert len(q[':question/answer-fields'])==len(o[':question/answer-fields'])
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];new=[a[':answer/value'] for a in f[':answer-field/choices']];prev=[a[':answer/value'] for a in of[':answer-field/choices']]
   if f[':answer-field/type'].endswith('/radio'):assert all(sum(same(pair(v)[0],pair(w)[0]) and same(pair(v)[1],pair(w)[1]) for w in new)==1 for v in prev)
   else:assert all(sum(same(scalar(v),scalar(w)) for w in new)==1 for v in prev)
   assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:
    value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);oval=of[':answer-field/correct'][':answer/value'];assert value==oval;n['source_refs']+=1
   n['source_values']+=len(prev);n['source_exact_values']+=sum(v in new for v in prev)
  n['source_prompts']+=1;n['source_solutions']+=int(':question/worked-solution' in o)
 review=json.load(open(D/'review.json'));items=review if isinstance(review,list) else [item for v in review.values() if isinstance(v,list) for item in v]
 for rec in items+json.load(open(R/'qa'/f'{kp}-sampled.json')):check(rec)
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
