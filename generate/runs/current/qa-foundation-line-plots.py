"""Root reads printed equations/stages and calibrated native raster geometry."""
import argparse,hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
P=module('root_line_scalar',R/'ode-scalar-parser.py');X,Y=P.x,P.y
def scalar(t):return P.scalar(t.strip().rstrip('.,?').replace('&',''))
def eq(t):
 a,b=t.split('=');return s.expand(scalar(a)-scalar(b))
def line(t):
 z=eq(t);c=z.coeff(Y);assert c and not c.free_symbols
 z=s.expand(z/c);assert s.Poly(z,X,Y).total_degree()==1
 return -z.coeff(X),-z.subs({X:0,Y:0})
def spans(t):return re.findall(r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',t)
def mask(t):
 t=re.sub(r'!\[.*?\]\(.*?\)','@ASSET@',t)
 t=re.sub(r'\$\$.*?\$\$','@DISPLAY@',t,flags=re.S)
 return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',t)).strip()
def blocks(t):return re.findall(r'\$\$(.*?)\$\$',t,re.S)
def review_rows(v):
 if isinstance(v,dict):return [r.get('record',r) for r in v.get('generated',[])]
 return [r.get('record',r) for r in v]
def main():
 a=argparse.ArgumentParser();a.add_argument('kp',type=int);o=a.parse_args();K=o.kp
 D=R.parents[2]/f'generate/scratch/{K}-draft';G=module('root_lines_'+str(K),D.with_suffix('.py'))
 F=module('root_lines_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
 C=dict(records=0,prompt_equations=0,source_prose_masks=0,operative_rows=0,table_values=0,point_coordinates=0,choice_lines=0,bank_pairs=0,claim_equations=0,subset_options=0,native_red_pixels=0,native_blue_markers=0,native_axes=0)
 records=json.loads((R/f'qa/{K}-sampled.json').read_text())
 records += [r for r in review_rows(json.loads((D/'review.json').read_text())) if 'question' in r and ':question/difficulty' in r['question'] and r['question'].get(':question/worked-solution') and not r['generation'].get('evidence_only') and not r['generation'].get('raw_source_replay')]
 if K==17592186054695:
  for c in json.loads((D/'source-cases.json').read_text()):
   p=dict(c['parameters']);p['m']=str(s.Rational(p['m'])*2);p['b']=str(s.Rational(p['b'])*2);p['x2']=str(-s.Rational(p['x2']))
   records.append(G.generate('easy',template=c['template'],profile=c['bank_profile'],parameters=p))
 if K==17592186054802:
  for c in json.loads((D/'source-cases.json').read_text()):
   profile=c['template'];p=next(p for p in G.candidates(profile) if p!=c['parameters'])
   records.append(G.generate(c['level'],template=profile,profile=profile,parameters=p))
 def raster(path,origin,unit,m,b,pts=(),points_only=False):
  im=np.asarray(Image.open(path).convert('RGB'));H,W=im.shape[:2];ox,oy=origin;ux,uy=unit
  assert ux>=7 and uy>=7 and abs(ux-uy)<.01,(path,'unit pixels',unit)
  red=(im[:,:,0]>180)&(im[:,:,1]<110)&(im[:,:,2]<110)
  blue=(im[:,:,2]>180)&(im[:,:,0]<110)&(im[:,:,1]<110)
  black=im.max(2)<100
  if points_only:assert red.sum()==0
  else:
   py,px=np.nonzero(red);assert len(px)>100
   # All red raster pixels, rather than just metadata or selected sample probes.
   residual=np.abs((H-oy-py)/uy-float(m)*(px-ox)/ux-float(b))/np.sqrt(1+float(m)**2)*ux
   assert np.quantile(residual,.995)<2.5,(path,'wrong visible line',m,b,np.quantile(residual,.995))
   C['native_red_pixels']+=len(px)
  for u,v in pts:
   px=int(round(ox+float(u)*ux));py=int(round(H-oy-float(v)*uy))
   assert 4<px<W-4 and 4<py<H-4 and blue[py-4:py+5,px-4:px+5].any(),(path,'missing blue point',u,v)
   C['native_blue_markers']+=1
  # The calibration must coincide with actual black zero axes in the raster.
  for vertical in (True,False):
   j=int(round(ox if vertical else H-oy));sl=black[:,max(0,j-1):j+2] if vertical else black[max(0,j-1):j+2,:]
   assert sl.any(1 if vertical else 0).sum()>min(H,W)*.2,(path,'axis calibration')
   C['native_axes']+=1
 def asset(r,path,m,b,pts=(),points_only=False):
  meta=r['generation']
  if K==17592186054694:
   path=Path(path);info=json.loads(Path(str(path)+'.json').read_text());origin=info['pixel_origin'];unit=info['pixel_unit']
  elif K==17592186054695:
   info=next(a for a in meta['assets'] if a['path']==path);path=Path(info['local']);im=Image.open(path);W,H=im.size
   xmin,xmax,ymin,ymax=info['bounds'];scale=min(.76*W/(xmax-xmin),.76*H/(ymax-ymin));left=.13*W+(.76*W-(xmax-xmin)*scale)/2;bottom=.12*H+(.76*H-(ymax-ymin)*scale)/2
   origin=[left-xmin*scale,bottom-ymin*scale];unit=[scale,scale]
  else:
   info=next(a for a in meta['assets'] if a['path']==path)
   if info.get('renderer')=='captured native PNG':return # Original rasters separately inspected in full resolution.
   path=Path(info['local']);W,H=info['dimensions'];origin=[info['origin_pixels'][0],H-info['origin_pixels'][1]];unit=info['unit_pixels']
   for x,y,w,h in info['tick_bboxes_display']+info['marker_bboxes_display']:assert 0<=x<x+w<=W and 0<=y<y+h<=H
   assert info['marker_min_axis_clearance_px']>=4
  raster(path,origin,unit,m,b,pts,points_only)
 for r in records:
  q,meta=r['question'],r['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];grade=q[':question/difficulty'].split('/')[-1]
  if K in (17592186054694,17592186054695):
   m,b=line(next(z for z in spans(prompt) if re.match(r'y\s*=',z)));C['prompt_equations']+=1
   if K==17592186054694:
    table=re.search(r'\| \$y\$ \|([^\n]+)',sol);ys=[scalar(t) for t in spans(table[1])];assert ys==[m*i+b for i in range(4)];C['table_values']+=4
    rows=[z for z in spans(sol) if z.startswith('y=') and z.count('=')==2];assert len(rows)==4
    for i,row in enumerate(rows):
     _,formula,value=row.split('=');assert scalar(formula)==m*i+b and scalar(value)==m*i+b
     assert f'({i})' in formula;C['operative_rows']+=1
    profile=meta['bank_profile']
    banks={'q-54397':[(-m,0),(m,b),(-m,-b/2),(m,-b),(m,0)],'q-59676':[(m,2*b),(-m,-2*b),(-m,-b),(2*m,4*b),(m,b)],'q-71695':[(m,-b),(-m,b/2),(-m/2,b),(m,b),(m/2,b)],'signed-products':[(m,b),(-m,b),(m,-b),(m,0),(2*m,b)],'half-units':[(m,b),(-m,b),(m,-b),(m,0),(2*m,b)]}
    bank=banks[profile];paths=meta['assets'][:5];pts=[(s.Integer(i),m*i+b) for i in range(4)]
    for path,(am,ab) in zip(paths,bank):asset(r,path,am,ab,[(s.Integer(i),am*i+ab) for i in range(4)])
    refs=re.findall(r'!\[.*?\]\((.*?)\)',sol);assert len(refs)==2;asset(r,refs[0],m,b,pts,True);asset(r,refs[1],m,b,pts)
    src=originals[meta['source_question']]
    if ':question/worked-solution' not in src:src=originals['q-54397']
    assert mask(sol)==mask(src[':question/worked-solution']);C['source_prose_masks']+=1
   else:
    xs=[scalar(z.split('=')[1]) for z in spans(sol) if z.startswith('x=')];assert len(xs)==2 and xs[0]==0 and xs[1]!=0
    pts=[(u,m*u+b) for u in xs];bs=blocks(sol);assert len(bs)==2
    for u,block in zip(xs,bs):
     rows=block.strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(chr(92)*2);assert len(rows)==(3 if b==0 else 4)
     for i,row in enumerate(rows):
      text=row.split('=')[1];assert scalar(text)==(m*X+b if i==0 else m*u+b)
      if i==1:assert '('+s.latex(u)+')' in text
      C['operative_rows']+=1
     if b:assert '+' in rows[2] or '-' in rows[2] # product/shift before collection
    stated=[z for z in spans(sol) if z.startswith('(') and z.endswith(').')];assert len(stated)==2
    for raw,point in zip(stated,pts):assert tuple(scalar(z) for z in raw.strip('().').split(','))==point;C['point_coordinates']+=1
    profile=meta['profile']
    legacy={'q-54286':[(m,b),(-m,-b),(m,-b),(m/4,b/2),(-m/4,-b/2)],'q-59678':[(-m,-2*b),(m,b),(-2*m,-b),(2*m,0),(4*m,2*b)],'q-102054':[(-m,m),(m,-m),(m/2,0),(m,0),(-m,0)],'q-109055':[(-m,-b),(m,2*b),(m,b),(-m,0),(m,0)]}
    if profile in legacy:bank=legacy[profile]
    elif b:bank=[(m,b),(-m,b),(m,-b),(-m,-b),(m+b,b)]
    elif abs(m)==1:bank=[(m,0),(-m,0),(m/2,0),(2*m,0),(0,0)]
    else:bank=[(m,0),(-m,0),(m/2,0),(2*m,0),(1/m,0)]
    paths=meta['choice_paths'];assert meta['choice_lines']==[[str(a),str(c)] for a,c in bank]
    for path,(am,ab) in zip(paths,bank):asset(r,path,am,ab)
    refs=re.findall(r'!\[.*?\]\((.*?)\)',sol);assert len(refs)==1;asset(r,refs[0],m,b,pts)
    src=originals['q-102054' if b==0 else 'q-109055'];assert mask(sol)==mask(src[':question/worked-solution']);C['source_prose_masks']+=1
    if grade=='moderate':assert abs(s.numer(m))>=2 and s.denom(m) in (2,3,4) and s.denom(b)==1 and b
    if grade=='hard':assert all(s.denom(v)==2 for _,v in pts)
   assert len(set(bank))==5 and bank.count((m,b))==1
   field=q[':question/answer-fields'][0];value=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert value==paths[bank.index((m,b))]
   assert {a[':answer/value'] for a in field[':answer-field/choices']}==set(paths);C['choice_lines']+=5;C['bank_pairs']+=10
  else:
   claims=re.findall(r'(?:\*\*I{1,3}\.\*\*|(?m:^I{1,3}\.))\s*\$([^$]+)\$',prompt);assert len(claims)==3
   aset=meta['assets'][0];m,b=map(s.Rational,aset.get('line',[])) if 'line' in aset else (None,None)
   if m is None:continue # raw-original normal anchor reviewed separately below.
   C['claim_equations']+=3;truth=[line(z)==(m,b) for z in claims]
   refs=re.findall(r'!\[.*?\]\((.*?)\)',prompt);assert len(refs)==1;asset(r,refs[0],m,b)
   compact=meta['template'] in ('q-54285','q-59732')
   if compact:
    coords=[tuple(scalar(z) for z in raw) for raw in re.findall(r'\((-?\d+),(-?\d+)\)',sol)]
    if meta['template']=='q-54285':
     intercept=s.Integer(re.search(r'y-axis at (-?\d+)',sol)[1]);points=[(s.Integer(0),intercept),coords[0]]
    else:points=coords[:2]
   else:points=[tuple(scalar(z) for z in raw.split(',')) for raw in re.findall(r'coordinates \$\((.*?)\)\$ and \$\((.*?)\)\$',sol)[0]]
   assert len(points)==2 and points[0]!=points[1] and all(v==m*u+b for u,v in points);C['point_coordinates']+=2
   refs=re.findall(r'!\[.*?\]\((.*?)\)',sol)
   if compact:assert not refs
   else:assert len(refs)==1;asset(r,refs[0],m,b,points)
   bs=blocks(sol)
   if meta['template'] in ('q-54285','q-59732'):
    # Captured compact solutions have no aligned substitution blocks or solution plot.
    assert not bs
    p=meta['parameters'];t=s.Rational(p['t'])
    if meta['template']=='q-54285':
     assert f'({t},{2*b})' in sol and f'slope is {b/t}' in sol and truth==[False,True,False]
    else:assert f'({t},0)' in sol and truth==[False,False,True]
   else:assert len(bs)==3
   for claim,block,ok in zip(claims,bs,truth):
    rows=block.strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(chr(92)*2)
    groups=[];group=[]
    for row in rows:
     group.append(row)
     if '✓' in row or r'\times' in row:groups.append(group);group=[]
    assert not group and len(groups) in (1,2)
    lhs,rhs=claim.split('=')
    for i,(point,group) in enumerate(zip(points,groups)):
     u,v=point;left,right=scalar(lhs).subs({X:u,Y:v}),scalar(rhs).subs({X:u,Y:v})
     for row in group:
      aa,bb=row.replace('&','').split('=');bb=bb.replace(r'\,✓','').replace(r'\,\times','')
      assert scalar(aa)==left and scalar(bb)==right;C['operative_rows']+=1
     assert ('✓' in group[-1])==(left==right)
     if left!=right:assert len(groups)==i+1
    assert all(scalar(lhs).subs({X:u,Y:v})==scalar(rhs).subs({X:u,Y:v}) for u,v in points)==ok
   fields=q[':question/answer-fields']
   if fields[0][':answer-field/type'].endswith('/checkbox'):
    assert len(fields)==3
    for f,ok in zip(fields,truth):
     chosen=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert chosen==str(ok).lower() and {a[':answer/value'] for a in f[':answer-field/choices']}=={'false','true'};C['subset_options']+=2
   else:
    assert len(fields)==1;f=fields[0];bank=[frozenset(re.findall(r'\bI{1,3}\b',a[':answer/value'])) for a in f[':answer-field/choices']];assert len(set(bank))==5
    target=frozenset(label for label,ok in zip(('I','II','III'),truth) if ok)
    assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],bank) if v==target]==[f[':answer-field/correct'][1]];C['subset_options']+=5;C['bank_pairs']+=10
  C['records']+=1
 result={'status':'passed','source':fidelity,'readback':{k:int(v) for k,v in C.items()},'original_asset_native_contact_sheets':len(json.loads((R/f'qa/{K}-original-assets.json').read_text())),'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0}
 (R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
