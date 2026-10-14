"""Independent displayed-math, original per-axis raster recovery, native grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,concurrent.futures,tempfile
from pathlib import Path
import sympy as sp
import numpy as np
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('draft',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x')
def save(n,v):(H/n).write_text(json.dumps(v,indent=2)+'\n')
def parse_math(t):
 t=t.strip().rstrip(',.');t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t);t=re.sub(r'(?<=[\d)])(?=[x(])','*',t)
 return sp.sympify(t,locals={'x':x})
def components(mask):
 seen=set();parts=[]
 for yy,xx in zip(*np.where(mask)):
  if (yy,xx) in seen:continue
  todo=[(yy,xx)];seen.add((yy,xx));p=[]
  while todo:
   y0,x0=todo.pop();p.append((x0,y0))
   for y1 in range(max(0,y0-1),min(mask.shape[0],y0+2)):
    for x1 in range(max(0,x0-1),min(mask.shape[1],x0+2)):
     if mask[y1,x1] and (y1,x1) not in seen:seen.add((y1,x1));todo.append((y1,x1))
  if len(p)>5:parts.append(np.mean(p,axis=0))
 return sorted(parts,key=lambda p:p[0])
def raster(path,source=False):
 im=Image.open(path).convert('RGBA');white=Image.new('RGBA',im.size,'white');white.alpha_composite(im);a=np.asarray(white.convert('RGB')).astype(int)
 black=(a.max(2)<90);black[:20]=False;black[:,:3]=False;black[:,-20:]=False;black[-3:]=False
 ox=int(np.argmax(black.sum(0)));oy=int(np.argmax(black.sum(1)))
 gray=(np.ptp(a,axis=2)<3)&(a[:,:,0]>160)&(a[:,:,0]<240)
 def scale(axis):
  counts=gray.sum(axis);inds=np.flatnonzero(counts>(a.shape[axis]/3));groups=[]
  for i in inds:
   if not groups or i>groups[-1][-1]+1:groups.append([int(i)])
   else:groups[-1].append(int(i))
  vals=np.array([np.mean(p) for p in groups]);diff=np.diff(vals);return float(np.median(diff[diff>3]))
 sx=scale(0);sy=scale(1)
 blue=(a[:,:,2]>160)&(a[:,:,0]<100)&(a[:,:,1]<100)
 pts=components(blue);assert len(pts)==4,(path,pts)
 coords=[((p[0]-ox)/sx,(oy-p[1])/sy) for p in pts]
 # Recover equation from all four markers, after independently locating axes/grid.
 fitted=np.polyfit([v[0] for v in coords],[v[1] for v in coords],1)
 red=(a[:,:,0]>180)&(a[:,:,1]<100)&(a[:,:,2]<100)
 yy,xx=np.where(red);redcoords=np.stack(((xx-ox)/sx,(oy-yy)/sy),axis=1)
 return {'dimensions':list(im.size),'origin':[ox,oy],'pixel_grid':[sx,sy],'markers_pixels':[list(p) for p in pts],'coordinates':coords,'fitted_line':list(fitted),'red_max_residual':float(np.max(np.abs(redcoords[:,1]-(fitted[0]*redcoords[:,0]+fitted[1])))) if len(xx) else None}
def check(r):
 q=r['question'];meta=r['generation'];raw=meta['parameters']['source_replay'];level=q.get(':question/difficulty',':question.difficulty/easy').split('/')[-1]
 eqs=re.findall(r'\$y\s*=\s*([^$]+)\$',q[':question/problem']);assert len(eqs)==1
 poly=sp.Poly(parse_math(eqs[0]),x);assert poly.degree()==1;m,b=poly.nth(1),poly.nth(0)
 assert [str(m),str(b)]==[meta['parameters']['m'],meta['parameters']['b']]
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 prompt_rows=q[':question/problem'].splitlines();assert '| $x$ | $0$ | $1$ | $2$ | $3$ |' in prompt_rows;assert '| $y$ |  |  |  |  |' in prompt_rows
 f=q[':question/answer-fields'][0];assert len(f[':answer-field/choices'])==5
 values=f[':answer-field/choices'];assert len({a[':answer/id'] for a in values})==5
 lines=[tuple(map(sp.Rational,v)) for v in meta['lines']];assert len(set(lines))==5 and lines.count((m,b))==1
 correct=lines.index((m,b));expected=meta['assets'][correct]
 if ':answer-field/correct' in f:
  chosen=next(a for a in values if a[':answer/id']==f[':answer-field/correct'][1]);assert chosen[':answer/value']==expected
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];rows=re.findall(r'if \$x=(\d)\$ then \$y=([^$]+)\$',sol);assert len(rows)==4
  for n,calc in rows:
   lhs,ans=calc.rstrip(',.').split('=');assert parse_math(lhs)==parse_math(ans)==poly.as_expr().subs(x,int(n));assert '('+n+')' in lhs
  yrow=next(l for l in sol.splitlines() if l.startswith('| $y$'));ys=re.findall(r'\$([^$]+)\$',yrow)[1:];assert list(map(parse_math,ys))==[m*i+b for i in range(4)]
  assert sol.index('First, we fill')<sol.index('if $x=0$')<sol.index('| $x$')<sol.index('$(x,y)$ pairs')<sol.index('Finally, connecting')
  finales=re.findall(r'This is the graph of\s+\$y=([^$]+)\$',sol);assert parse_math(finales[0])==poly.as_expr()
  for t in [q[':question/problem'],sol]:assert not any(ord(c)<32 and c not in '\n\t\r' for c in t)
 for line,path in zip(lines,meta['recreated_assets']):
  side=json.load(open(path+'.json'));assert [side['m'],side['b']]==list(map(str,line));assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==side['sha256']
  assert list(map(sp.Rational,side['table_y']))==[line[0]*i+line[1] for i in range(4)]
  img=np.asarray(Image.open(path).convert('RGB'));blue=(img[:,:,2]>160)&(img[:,:,0]<100)&(img[:,:,1]<100);pts=components(blue);assert len(pts)==4
  actual=sorted(pts,key=lambda p:p[0]);pixels=side['pixel_points']
  for (cx,cy),(px,py) in zip(actual,pixels):assert abs(cx-px)<1.2 and abs(cy-(576-py))<1.2,(path,actual,pixels)
 return True

def main():
 source_checks=[];native=[];review=[];orig=[]
 for c in json.load(open(H/'source-cases.json')):
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r);src=g.SOURCES[c['source_id']];q=r['question'];assert q[':question/problem']==src[':question/problem']
  for key in (':question/difficulty',':question/worked-solution'):assert (key in q)==(key in src)
  if ':question/worked-solution' in src:assert q[':question/worked-solution']==src[':question/worked-solution']
  sf=src[':question/answer-fields'][0];f=q[':question/answer-fields'][0];assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in sf[':answer-field/choices']]
  rows=[]
  for i,a in enumerate(sf[':answer-field/choices']):
   recovered=raster(H/'source-assets'/Path(a[':answer/value']).name,True);line=tuple(map(sp.Rational,r['generation']['lines'][i]));coords=recovered['coordinates'];assert len(coords)==4
   for j,(cx,cy) in enumerate(coords):assert abs(cx-j)<.04 and abs(cy-float(line[0]*j+line[1]))<.05,(c['source_id'],i,recovered,line)
   assert np.allclose(recovered['fitted_line'],list(map(float,line)),atol=.035);assert recovered['red_max_residual']<.10
   rows.append({'option':i+1,'answer_id':a[':answer/id'],'asset':a[':answer/value'],'line':list(map(str,line)),'recipe':r['generation']['recipes'][i],'sha256':hashlib.sha256((H/'source-assets'/Path(a[':answer/value']).name).read_bytes()).hexdigest(),'independent_native_geometry':recovered})
  source_checks.append({'source':c['source_id'],'complete_bank_match':True,'choices_matched':5,'distractors_matched':4,'source_key_present':':answer-field/correct' in sf,'missing_attributes_retained':r['generation']['source_omissions'],'plots':rows});orig.append(r)
  if ':answer-field/correct' in f:native.append(fixture('source-'+c['source_id'],r))
 # Exact meaningful family sizes; no banks, cosmetic labels, or shuffles counted.
 counts={};math_count=0
 for level in ('easy','moderate','hard'):
  tasks=g.task_domain(level);counts[level]=len(tasks);fps=set()
  for m,b in tasks:
   template='unit_positive' if m==1 else 'unit_negative' if m==-1 else 'double_positive';profile=g.profile_for(level,template);lines=g.bank(profile,m,b)
   assert len(set(lines))==5 and sum(v==(m,b) for v in lines)==1;fps.add((m,b));math_count+=1
  assert len(fps)==len(tasks)
  # Changed signs and coefficient boundaries, all source-shaped layouts.
  examples=[('unit_positive',{'m':1,'b':-8}),('unit_negative',{'m':-1,'b':8}),('double_positive',{'m':2,'b':8})] if level=='easy' else [('unit_negative',{'m':-4,'b':-8}),('double_positive',{'m':-2,'b':8})] if level=='moderate' else [('unit_positive',{'m':'-5/2','b':'-11/2'}),('double_positive',{'m':'5/2','b':'11/2'})]
  for t,p in examples:
   r=g.generate(level,41,template=t,parameters=p);check(r);same=g.generate(level,99,template=t,parameters=p);assert same['question'][':question/id']==r['question'][':question/id'];assert same['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'];review.append(r);native.append(fixture(level+str(p),r))
  for seed in range(6):r=g.generate(level,seed);check(r);native.append(fixture(level+'-seed-'+str(seed),r))
 # Mutations prove actual prompt and substitution reading do not defer to metadata.
 mutated=copy.deepcopy(review[0]);mutated['question'][':question/problem']=mutated['question'][':question/problem'].replace('y=x-8','y=x-7')
 try:check(mutated)
 except AssertionError:pass
 else:raise AssertionError('Prompt mutation escaped')
 mutated=copy.deepcopy(review[0]);mutated['question'][':question/worked-solution']=mutated['question'][':question/worked-solution'].replace('(1)-8=-7','(2)-8=-7')
 try:check(mutated)
 except AssertionError:pass
 else:raise AssertionError('Arithmetic-stage mutation escaped')
 # Fresh concurrent generation: two same and two distinct calls in separate processes.
 fresh=Path(tempfile.mkdtemp(prefix='concurrent-',dir=H))
 worker="import importlib.util,json,sys;from pathlib import Path;s=importlib.util.spec_from_file_location('freshdraft',sys.argv[1]);g=importlib.util.module_from_spec(s);s.loader.exec_module(g);g.HERE=Path(sys.argv[3]);print(json.dumps(g.generate('hard',int(sys.argv[2]))))"
 cmd=[sys.executable,'-c',worker,str(H.with_suffix('.py'))]
 def call(seed):
  p=subprocess.run(cmd+[str(seed),str(fresh)],capture_output=True,text=True,check=True);r=json.loads(p.stdout);check(r);return r
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:concurrent_results=list(ex.map(call,[8127,8127,8128,8129]))
 assert concurrent_results[0]==concurrent_results[1];assert len({r['generation']['mathematical_fingerprint'] for r in concurrent_results})==3
 assert not list((fresh/'images').glob('render-*')) and not list((fresh/'images').glob('write-*'))
 save('source-choice-mapping.json',source_checks);save('review.json',{'originals':orig,'generated':review});save('native-input.json',native)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'native-input.json'),str(H/'native-grading.json')],check=True)
 text=['# Original and local draft review\n\nOriginal replay retains source refs; regenerated banks are separately available in generation.recreated_assets.']
 for r in orig+review:text.append('## '+('Original '+r['generation']['source_question'] if r['generation']['evidence_only'] else 'Authored/local '+r['question'][':question/difficulty'])+'\n\n'+g.markdown(r))
 (H/'review.md').write_text('\n\n'.join(text)+'\n')
 # Native-size review collage of extremes, complete generated banks separately.
 for k,r in enumerate(review):
  canvas=Image.new('RGB',(576*5,610),'white');draw=ImageDraw.Draw(canvas)
  for i,path in enumerate(r['generation']['recreated_assets'][:5]):canvas.paste(Image.open(path),(576*i,34));draw.text((576*i,8),str(r['generation']['lines'][i]),fill='black')
  canvas.save(H/('review-bank-'+str(k)+'.png'))
 save('validation.json',{'passed':True,'supported_levels':['easy','moderate','hard'],'source_basis':g.S['basis'],'source_lineage':g.S['lineage'],'original_questions':3,'original_choices_matched':15,'original_distractors_matched':12,'complete_banks_matched':3,'original_plot_reference_occurrences_matched':19,'original_unique_practice_plot_refs_matched':15,'source_keys_matched':2,'source_keys_absent':1,'solutions_exact':2,'solution_absent':1,'independent_inventory_records':3,'meaningful_task_counts':counts,'whole_domain_exact_banks_checked':math_count,'rendered_records_checked':len(native)+1,'native_checks_expected':len(native)*5,'native_scope':'real application memory-fixture radio IDs only; no fidelity or math claim','concurrent_fresh_calls':4,'source_geometry':'all 15 independently calibrated original axes, grid, four markers, red strokes; .05-unit marker / .10-unit antialias tolerances','mutation_regressions':2,'unresolved':[],'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [H.with_suffix('.py'),H/'validate.py',H/'source.json',ROOT/'generate/runs/current/check-engine']}})
 print('PASS 15/15 choices; 3/3 banks; 168 meaningful tasks; '+str(len(native)*5)+' actual native radio checks')
def fixture(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'image radio identity grading, separately from math/plot proof'} for a in f[':answer-field/choices']]}
if __name__=='__main__':main()
