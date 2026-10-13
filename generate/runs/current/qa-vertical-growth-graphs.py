"""Root independent source-labelled features, complete graph banks/prose and PNGs."""
import sys,re,json,hashlib,importlib.util,math
from pathlib import Path
import sympy as s
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'spatial-jacobian-readback.py','scalar');x=p.x
n=dict(records=0,choices=0,solution_equations=0,solution_intercepts=0,solution_asymptotes=0,solution_shift_inputs=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,pngs=0,pixel_curve_samples=0,original_features=0,complete_method_banks=0)
features=json.load(open(R/'qa/17592186087821-source-features.json'))['visually_read_intercept_asymptote_direction'];seen=set()
def expression(raw):
 e=p.scalar(raw.strip().rstrip('.,?:'));pw=[a for a in s.preorder_traversal(e) if isinstance(a,s.Pow) and a.exp==x];assert len(pw)==1;B=pw[0].base;C=s.simplify(e-pw[0]);assert B>1 and C.is_Rational;return B,C
def raster(path,B,A,C,D,grid):
 path=Path(path)
 if path in seen:return
 side=json.load(open(path.with_suffix('.json')));spec=side['spec'];assert side['version']=='shift-plots-7';assert hashlib.sha256(path.read_bytes()).hexdigest()==side['png_sha256'];im=Image.open(path).convert('RGB');w,h=im.size;assert (w,h)==(540,456);rgb=im.load();black=lambda px,py:max(rgb[px,py])<100
 ox=max(range(w),key=lambda px:sum(black(px,py) for py in range(h)));oy=max(range(h),key=lambda py:sum(black(px,py) for px in range(w)));left,bottom,width,height=side['axes_bbox'];lo,hi=spec['ylim'];assert abs(ox-(left+width/2))<3 and abs(oy-(h-bottom+(lo/(hi-lo))*height))<3,(path,ox,oy,side['axes_bbox'],lo,hi)
 for tx in (-2,-1,0,1,2):
  ty=float(A)*float(B)**(D*tx)+float(C)
  if not lo+.2<ty<hi-.2:continue
  px,py=round(ox+tx*width/10),round(oy-ty*height/(hi-lo));colors=[rgb[a,b] for a in range(max(0,px-4),min(w,px+5)) for b in range(max(0,py-4),min(h,py+5))];assert any(b>110 and b>r*1.4 and g>r*1.1 for r,g,b in colors),(path,tx,ty);n['pixel_curve_samples']+=1
 assert p.same(p.scalar(spec['shift_tex']),C) and p.same(p.scalar(spec['intercept_tex'].split(',',1)[1].rstrip(')')),A+C)
 if spec['cue']=='grid':assert s.Rational(spec['grid'])==grid
 n['pngs']+=1;seen.add(path)
def check(rec):
 q=rec['question'];meta=rec['generation'];B,C=expression(re.search(r'\$y\s*=\s*(.*?)\$',q[':question/problem'])[1]);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];geoms=meta['geometry'];assert len(choices)==len(geoms)==5;assert {a[':answer/value'] for a in choices}=={a['path'] for a in geoms};forms=[]
 for a in geoms:
  b,A,c=[s.Rational(a[z]) for z in ('b','A','c')];d=a['direction'];assert b==B and d in (-1,1);forms.append((A,c,d))
  if '17592186087821/plots' in a['path']:raster(a['path'],b,A,c,d,s.Rational(1,C.q))
 assert len(set(forms))==5 and forms.count((1,C,1))==1;path=geoms[forms.index((1,C,1))]['path']
 if ':answer-field/correct' in f:assert next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1])==path
 else:assert meta['evidence_only'] and not meta['eligible_for_learning']
 if meta['eligible_for_learning']:
  expected=([(1,C,1),(1,-C,1),(1,C,-1),(1,0,1),(B,C,1)] if meta['bank_profile']=='authored_transformations' else [(1,C,1),(1,-C,1),(1,C+1,1),(1,C-1,1),(1,0,1)])
  assert set(forms)==set(expected);n['complete_method_banks']+=1
 if ':question/worked-solution' in q:
  text=q[':question/worked-solution'];assert len(re.findall(r'!\[\]\((.*?)\)',text))==2
  equations=[e for e in re.findall(r'\$y=(.*?)\$',text) if '^{x}' in e];assert len(equations)==3
  for i,e in enumerate(equations):assert expression(e)==(B,C if i==1 else s.Integer(0));n['solution_equations']+=1
  m=re.search(r'intercept moves from \$\(0,1\)\$ to \$\(0,(.*?)\),\$',text);assert m and p.same(p.scalar(m[1]),C+1);n['solution_intercepts']+=1
  m=re.search(r'asymptote moves from \$y=0\$ to \$y=(.*?)\.\$',text);assert m and p.same(p.scalar(m[1]),C);n['solution_asymptotes']+=1
  m=re.search(r'shift it \$(.*?)\$ units? (up|down)',text);assert m and p.same(p.scalar(m[1]),abs(C)) and (m[2]=='up')==(C>0);n['solution_shift_inputs']+=1
 n['records']+=1;n['choices']+=5
if __name__=='__main__':
 kp=17592186087821;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(rec);q=rec['question'];o=old[c['source_id']];expected=features[c['source_id']]
  for a,(intercept,asymptote,direction) in zip(rec['generation']['geometry'],expected):assert p.same(s.Rational(a['A'])+s.Rational(a['c']),s.Rational(intercept)) and s.Rational(a['c'])==s.Rational(asymptote) and a['direction']==direction;n['original_features']+=1
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 observations=json.load(open(D/'plot-observations.json'))['plots']
 for a in observations:assert hashlib.sha256(Path(a['absolute_path']).read_bytes()).hexdigest()==a['sha256']
 for rec in json.load(open(D/'review.json')):check(rec)
 for rec in json.load(open(R/'qa'/f'{kp}-sampled.json')):check(rec)
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
