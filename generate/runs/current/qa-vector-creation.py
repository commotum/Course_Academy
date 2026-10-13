"""Root reads scalar requests, actual arrows and full image-choice banks."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;ROOT=R.parents[2];D=ROOT/'generate/scratch/17592186096649'
z=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(z);z.loader.exec_module(g)
n=dict(records=0,choices=0,prose_magnitudes=0,prose_signs=0,pngs=0,arrow_ink_targets=0,source_prompts=0,source_options=0);seen=set()
def scalar(t):
 t=t.strip().removesuffix('a');t=re.sub(r'\\frac\{(\d+)\}\{(\d+)\}',r'\1/\2',t)
 return s.Rational('1' if t=='' else '-1' if t=='-' else t)
def color(a,c):
 return np.max(a,axis=2)<90 if c=='black' else (a[:,:,2]>a[:,:,0]+40)&(a[:,:,2]>a[:,:,1]+10) if c=='#2c72ae' else (a[:,:,0]>200)&(a[:,:,1]>70)&(a[:,:,1]<210)&(a[:,:,2]<70)
def plot(path):
 p=ROOT/path;side=json.loads(p.with_suffix('.json').read_text());spec=side['spec']
 if p in seen:return spec
 a=np.asarray(Image.open(p).convert('RGB')).astype(int);assert a.shape[:2]==(600,600)
 xmin,xmax=spec['bounds'][0];ymin,ymax=spec['bounds'][1];assert abs((xmax-xmin)-(ymax-ymin))<1e-9
 unit=564/(xmax-xmin)
 for v,(tail,tip) in zip(spec['vectors'],side['arrow_tail_tip_pixels']):
  t=np.array(v['tail']);vv=np.array(v['vector']);expected_tail=np.array([18+unit*(t[0]-xmin),18+unit*(t[1]-ymin)]);expected_tip=expected_tail+unit*vv
  assert np.linalg.norm(expected_tail-tail)<1e-7 and np.linalg.norm(expected_tip-tip)<1e-7
  ink=color(a,v['color'])
  for frac in np.linspace(.13,.86,11):
   xy=np.array(tail)+frac*(np.array(tip)-tail);x,y=round(xy[0]),600-round(xy[1]);assert ink[max(y-3,0):y+4,max(x-3,0):x+4].any(),(p,frac)
   n['arrow_ink_targets']+=1
  norm=(np.array(tip)-tail)/np.linalg.norm(np.array(tip)-tail);perp=np.array([-norm[1],norm[0]])
  def flare(endpoint,sign):
   out=0
   for back in range(1,11):
    for off in (-5,-4,-3,3,4,5):
     xy=np.array(endpoint)+sign*back*norm+off*perp;x,y=round(xy[0]),600-round(xy[1])
     if 0<=x<600 and 0<=y<600:out+=int(ink[y,x])
   return out
  j=spec['vectors'].index(v);vertices=side['patch_vertices_pixels'][j];left,head,right=map(np.array,vertices[3:6]);assert np.dot(head-(left+right)/2,np.array(tip)-tail)>0
  assert np.linalg.norm(head-tip)<4
  centre=(left+head+right)/3;x,y=round(centre[0]),600-round(centre[1]);assert ink[max(y-2,0):y+3,max(x-2,0):x+3].any(),(p,'actual arrowhead triangle ink')
  if np.linalg.norm(np.array(tip)-tail)>45:assert flare(tip,-1)>flare(tail,1),(p,'actual head direction')
 assert side['minimum_text_arrow_clearance_px']>3 and not side['axes'] and not side['ticks']
 seen.add(p);n['pngs']+=1;return spec
def record(r):
 q=r['question'];gen=r['generation'];prompt=q[':question/problem'];f=q[':question/answer-fields'][0]
 text=prompt.split('Which of the following diagrams shows ')[1];ks=[scalar(t) for t in re.findall(r'\$(.*?)\$',text)];path=re.search(r'!\[\]\((.*?)\)',prompt)[1]
 if path.startswith('images/'):
  assert not gen['eligible_for_learning'];return
 pp=plot(path);a=np.array(pp['vectors'][0]['vector']);assert pp['vectors'][0]['label']=='a'
 valid=[];banks=[]
 for ans in f[':answer-field/choices']:
  p=plot(ans[':answer/value']);assert p['bounds']==pp['bounds'] and len(p['vectors'])==len(ks)
  assert [scalar(v['label']) for v in p['vectors']]==ks
  vecs=[np.array(v['vector']) for v in p['vectors']];banks.append(tuple(tuple(np.round(v,9)) for v in vecs));valid.append(all(np.linalg.norm(v-float(k)*a)<1e-8 for v,k in zip(vecs,ks)))
 assert len(set(banks))==5 and sum(valid)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][valid.index(True)][':answer/id']==f[':answer-field/correct'][1]
 sol=q.get(':question/worked-solution') or gen['inferred_worked_solution']
 for subject,amount in re.findall(r'The magnitude of \$(.*?)\$ is \$(.*?)\$ times the magnitude of \$a\$',sol):
  k=scalar(subject);assert k in ks and scalar(amount+'a')==abs(k);n['prose_magnitudes']+=1
 for subject,direction,k,sign in re.findall(r'Vectors \$a\$ and \$(.*?)\$ have (the same direction|opposite directions) since the factor \$(.*?)\$ is (positive|negative)',sol):
  v=scalar(subject);assert v in ks and scalar(k+'a')==v and (v>0)==(sign=='positive')==(direction=='the same direction');n['prose_signs']+=1
 assert len(re.findall(r'The magnitude of',sol))==len(ks) and '![]('+f[':answer-field/choices'][valid.index(True)][':answer/value']+')' in sol
 level=gen['actual_difficulty']
 if gen['eligible_for_learning']:
  assert len(ks)==(2 if level=='hard' else 1)
  assert all(k>0 and k.q==1 for k in ks) if level=='easy' else ks[0]<0 and ks[0].q>1 if level=='moderate' else ks[0]>0 and ks[0].q==1 and ks[1]<0 and ks[1].q>1
 n['records']+=1;n['choices']+=5
for item in json.loads((D/'native-input.json').read_text()):record(item['record'])
for level in ('easy','moderate','hard'):
 for seed in range(18):record(g.generate(level,seed))
for profile,(sid,t,p) in g.RAW.items():
 r=g.generate('hard' if t=='pair' else 'moderate',profile=profile,parameters=p);q=r['question'];o=g.SOURCES[sid]
 assert q[':question/problem']==o[':question/problem'] and set(q)==set(o)
 f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert set(f)==set(of) and sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
 assert ':answer-field/correct' not in f and ':question/worked-solution' not in q and ':question/difficulty' not in q and not r['generation']['eligible_for_learning'];n['source_prompts']+=1;n['source_options']+=5
out={'status':'passed','independent_readback':n,'finite_normal_tasks':{'easy':18,'moderate':24,'hard':72},'source_raster_review':'Root viewed all 12 original prompt/choice images and three canonical diagrams at full resolution. Relative lengths, directions, complete error patterns and labels agree with extraction; exact 30/60 degree models remain inferred from ungridded ink.'}
(R/'qa/17592186096649-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
