"""Materialize private source descriptions and review cases; no shared writes."""
from pathlib import Path
import importlib.util,json,re,hashlib,collections
import numpy as np
from PIL import Image
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',str(D)+'.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def dump(name,v):(D/name).write_text(json.dumps(v,indent=2)+'\n')
DESC={
'e-3961': ['horizontal constant segment','smooth even bell with a peak at the vertical axis','three visible peaks with intervening troughs','strictly decreasing smooth curve across the entire visible segment'],
'q-36000':['strictly decreasing reciprocal-like branch entirely right of the vertical axis','strictly increasing LEFT branch terminating at the vertical axis; no right-hand falling branch is shown','symmetric two-sided trough/cusp at the origin; both sides have the same positive output levels','short symmetric downward arch touching the horizontal axis at its vertex'],
'q-36897':['strictly increasing log-like branch right of the vertical axis','two turning points, one trough touching the horizontal axis and a subsequent peak','left side decreases to a negative local minimum before rising through the origin and flattening on the right','symmetric downward arch with vertex above the horizontal axis'],
'q-108581':['asymmetric four-turn smooth curve','symmetric two peaks separated by a local minimum at the origin; both outer tails turn upward near the frame','two increasing straight segments joined at the origin, with different slopes','two disconnected curved branches: left branch ends at a CLOSED dot at pixel (521,443); right branch starts at an OPEN circle at (521,511). Their output interiors overlap; the horizontal witness through the closed dot also meets the rising right branch'],
'q-108605':['curved hump, corner to an increasing line, then a descending line: repeated levels','two disconnected increasing branches. Left S-like branch ends at CLOSED dot (479,182), entirely below the horizontal axis. Right square-root-like branch starts CLOSED at (563,140) and remains on/above the axis. Their output ranges are disjoint','upward parabola with vertex below the horizontal axis','left decreasing line to a corner at the axis, followed by a hump then a valley on the right'],
'q-36063':['isolated CLOSED dot at (127,98) plus increasing square-root-like branch from the origin. The dot height also occurs on the branch','decreasing curved left segment joined at the origin to a decreasing straight right segment','decreasing left curved branch joined at the origin to an increasing straight right segment','symmetric two-sided cusp/trough at the origin'],
'q-66510':['increasing straight segment','smooth oscillatory curve with central peak, two troughs and rising outer portions','strictly increasing exponential-like curve','downward arch with a sharp-looking top at the vertical axis'],
'q-36905':['increasing line followed by a short falling curved portion and then a rising curved portion','negative bell/trough centered on the vertical axis','two visible sine-like peaks and troughs','upward parabola with vertex below the horizontal axis'],
'q-66508':['strictly increasing exponential-like curve','symmetric bell with peak at the vertical axis','cosine-like curve with central peak and two visible troughs','strictly decreasing exponential-like curve across the entire shown segment'],
'q-66509':['V-shaped absolute-value-like graph at the origin','four visible sine-like cycles','symmetric pointed bell centered on the vertical axis','strictly increasing concave-down log-like curve over the shown segment'],
'q-66514':['downward outer curved pieces, two symmetric corner peaks and a shallow central trough above the horizontal axis','four visible sine-like cycles','strictly increasing exponential-like curve','steep increasing left line to a corner peak at the vertical axis, falling line to a corner minimum on the horizontal axis, and rising right line']}
VISUAL={'e-3961':8,'q-36000':3,'q-36897':1,'q-108581':4,'q-108605':2,'q-36063':2,'q-66510':5,'q-36905':0,'q-66508':9,'q-66509':8,'q-66514':4}
ex=[];cases=[]
for q in [m.R[':knowledge-point/canonical-example']]+list(m.SOURCES.values()):
 name=q[':question/math-academy-id'];plots=[]
 for role in [':question/problem',':question/worked-solution']:
  for ref in re.findall(r'images/[^)]+',q.get(role,'')):
   p=D/'originals'/Path(ref).name;im=Image.open(p).convert('RGBA');a=np.asarray(im);alpha=a[:,:,3:4]/255;rgb=a[:,:,:3]*alpha+255*(1-alpha)
   blue=(rgb[:,:,2]>100)&(rgb[:,:,0]<100)&(rgb[:,:,2]>rgb[:,:,0]+30)&(rgb[:,:,1]>50)
   black=rgb.max(2)<80;h,w=blue.shape
   # Fit each panel's own origin from the long black axis shafts.
   xp=[int(np.argmax(black[:,:w//2].sum(0))),w//2+int(np.argmax(black[:,w//2:].sum(0)))]
   yp=[int(np.argmax(black[:h//2,:].sum(1))),h//2+int(np.argmax(black[h//2:,:].sum(1)))]
   panels=[]
   for i in range(4):
    x0,x1=(0,w//2) if i%2==0 else (w//2,w);y0,y1=(0,h//2) if i<2 else (h//2,h)
    ys,xs=np.nonzero(blue[y0:y1,x0:x1]);panels.append({'roman':m.ROMANS[i],'origin_pixel':[xp[i%2],yp[i//2]],'blue_bbox_pixel':[int(xs.min()+x0),int(ys.min()+y0),int(xs.max()+x0),int(ys.max()+y0)],'blue_pixel_count':len(xs),'source_ticks':[],'coordinate_scale':'unlabelled; only pixel coordinates recovered, no integer-coordinate claim'})
   plots.append({'role':role,'source_ref':ref,'private_asset':str(p),'width':w,'height':h,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'panels':panels,'curve_arrows':False,'axis_arrows':'positive x and positive y only','grid':False,'pixel_recipe':'complete ink coordinate cloud, composited on white; diagonal positive affine map','opaque_geometry':True})
 f=q.get(':question/answer-fields',[{}])[0]
 ex.append({'source_id':name,'source_db_id':q[':db/id'],'difficulty':q.get(':question/difficulty'),'difficulty_observed':':question/difficulty' in q,'prompt':q[':question/problem'],'worked_solution':q.get(':question/worked-solution'),'original_key_presence':sorted(q),'graph_descriptions':DESC[name],'visual_horizontal_line_mask':VISUAL[name],'inferred_only':':answer-field/correct' not in f,'graph_domain':'actual visible curve segments and individually marked points only; no unshown continuation inferred','choice_bank':[{'value':a[':answer/value'],'mask':m.mask(a[':answer/value']),'id':a[':answer/id'],'correct_observed':a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id')} for a in f.get(':answer-field/choices',[])],'plots':plots,'learning_eligible':False,'geometry_limit':'ink recipe reproduces bounded visible geometry; exact smooth equations and unlabeled finite endpoint inclusion cannot be recovered'})
 if name in m.SOURCES:cases.append({'source_id':name,'template':'captured-graph-bank','level':q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1],'level_authored_if_unrated':':question/difficulty' not in q,'profile':'raw:'+name,'bank_profile':name,'parameters':{'order':[0,1,2,3],'scale':[1,1]}})
dump('extraction.json',ex);dump('source-cases.json',cases)
review=[];md=['# Graph-invertibility review\n\nAll originals are raw captured evidence. Generated affine ink variants are evidence-only. Exact authored E/M/H examples are eligible practice. The hard label is authored, never observed.']
for case in cases:
 name=case['source_id'];q=m.SOURCES[name];r=m.generate(case['level'],profile=case['profile'],parameters=case['parameters'])
 md+=['\n## Original '+name+' (observed '+('unrated' if ':question/difficulty' not in q else q[':question/difficulty'][':db/ident'].split('/')[-1])+')',m.markdown(r)]
 for ref,path in r['generation']['assets'].items():md[-1]=md[-1].replace(ref,path)
 # Original reconstruction independently checked against full raster, not just
 # unchanged replay identity. Both prompt and all solution assets reconstructed.
 for ref,path in r['generation']['assets'].items():
  rec=m.asset({'mode':'raw','asset':path,'scale':[1,1]})
  md+=['\nParameterized raw ink reconstruction (full original scale):\n\n![]('+rec+')']
 rr=m.generate(case['level'],profile=case['profile'],parameters={'order':[0,1,2,3],'scale':[.9,.9]},seed=11)
 review.append(rr);md+=['\nGenerated evidence-only affine variant '+name,m.markdown(rr)]
for level in ['easy','moderate','hard']:
 for j,bank in enumerate(sorted(m.BANKS)):
  r=m.generate(level,100+j,profile=bank);review.append(r)
  md+=['\n## Generated '+level+' (authored), complete bank '+bank,m.markdown(r)]
extra=m.generate('easy',111,profile='q-36000',parameters={'correct_mask':3,'graphs':[{'kind':'exponential','orientation':1},{'kind':'logarithm','orientation':-1},{'kind':'absolute','orientation':1},{'kind':'wave','orientation':1}]})
review.append(extra);md+=['\n## Generated easy (authored): additional logarithmic/exponential shape coverage',m.markdown(extra)]
dump('review.json',review);(D/'review.md').write_text('\n\n'.join(md)+'\n')
masks=sorted({m.mask(v) for bank in m.BANKS.values() for v in bank})
counts={'eligible_correct_subset_masks':masks,'easy_structural_task_count':len(masks)*5**4,'moderate_structural_task_count':len(masks)*32**4,'hard_structural_task_count':sum(1536**z.bit_count()*768**(4-z.bit_count()) for z in masks),'count_convention':'Ordered panels; bank profiles, axis letters, source affine scales and easy vertical reflection do not increase counts. Moderate and hard direction/range-order/curve-kind/open-circle patterns are structural parameters; no unlimited diversity claim.'}
dump('catalog.json',counts)
print('Saved',len(ex),'original records,',len(cases),'practice cases,',len(review),'review variants')
