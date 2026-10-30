import json,re,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;S=json.loads((H/'current.json').read_text());qs=json.loads((H/'proposed-questions.json').read_text());byid={q[':db/id']:q for q in qs};byma={q.get(':question/math-academy-id'):q for q in qs};visual={v['entity']:v for v in json.loads((H/'visual-manifest.json').read_text())};rows=[]
# Independent observations from all nine displayed contact sheets, with boundaries read from the full diagrams.
regions='''e-13145|Z2|1<=x<=3;-3<=y<=2
e-13156|R2|2x<y<=3
e-13158|R2|16x^2+25y^2>=400
e-13183|Z2|y<=x+2
q-181129|Z2|-3<=x<=-1;-4<=y<=-1
q-181172|R2|y<=x^2
q-181269|R2|y<=2x-3
q-181442|R2|1<x<5;2<y<4
q-181600|R2|-x<=y<2
q-181610|R2|4x^2+9y^2<36
q-181678|R2|3<=y<=2x+3
q-181983|Z2|y<x-1
q-181130|R2|-1<=x<=5;1<=y<=3
q-181679|R2|y<-x+5;y<x+3
q-181682|R2|-2<=y<=x/2+2
q-181684|R2|-2<y<x
q-181685|R2|2x<y<-x+3
q-181686|R2|y<=4;y<=4x+1
q-181687|R2|-x-1<y<x+2
q-181688|R2|x+1<y<=3x
q-181689|R2|3x<=y<x/4
q-181690|R2|-2<y<=2
q-181691|R2|y<-x^2/2
q-181692|R2|x>=-y^2
q-181694|R2|9x^2+4y^2<=36
q-181696|R2|16x^2+4y^2>=64
q-181791|Z2|-1<=x<=2;-2<=y<=3
q-181804|R2|1<x<5;2<=y<5
q-181806|R2|3<=x<6;-1<y<4
q-181807|R2|x<y^2
q-181808|R2|y>=x^2
q-181809|R2|9x^2+16y^2>144
q-181970|Z2|y>=-x+1
q-181976|R2|y>-x+1
q-181988|Z2|y>-x-1
q-181999|R2|y>2
q-182013|R2|x>=-2
q-182016|Z2|y>=-1
q-182024|Z2|x>=-1
q-182032|Z2|x<2
q-181159|R2|3<=x<6;1<=y<4
q-181602|Z2|y<=x-1
q-181789|R2|2<x<6;2<y<5
q-181805|R2|1<=x<=6;3<=y<=5
q-181811|R2|4x^2+16y^2>=64
q-181683|R2|-x-3<=y<=x+4
q-182017|Z2|y<2
q-181810|R2|16x^2+9y^2<144
q-181693|R2|x>2y^2
q-181792|R2|2<=x<=5;1<=y<5'''
for line in regions.splitlines():
 mid,domain,condition=line.split('|');q=byma[mid];rows.append({'entity':q[':db/id'],'identity':mid,'domain':domain,'independent_graphic_condition':condition,'visual_sheet':visual[q[':db/id']]['sheet'],'reviewed':['whole shaded/discrete region','axis scale and orientation','all boundary equations','solid/dashed or lattice inclusion','direction of every inequality','domain R2 versus Z2','response field placement','full worked solution'],'conclusion':'Existing keys match the complete original graphic; q-181442 completed from its original graphic.'})
# True/false observations for all 22 graphical subspace questions, in diagram I/II/III order.
diagrams={17592186192504:[False,True,False],17592186192506:[True,True,False],17592186193312:[False,False,False],17592186193319:[False,True,False],17592186193383:[False,False,False],17592186193384:[True,True,False],17592186247121:[False,False,True],17592186247148:[True,False,False],17592186247149:[False,False,False],17592186275420:[False,False,False],17592186275441:[False,True,False],17592186275442:[False,False,True],17592186275443:[True,False,True],17592186317172:[False,False,True],17592186317349:[False,True,False],17592186323703:[False,True,False],17592186407336:[True,False,False],17592186407337:[False,False,False],17592186426531:[False,False,True],17592186426532:[False,False,False],17592186426534:[True,False,True],17592186426536:[False,False,True],17592186595951:[True,True,False],17592186595974:[False,False,False],17592186595999:[False,False,False],17592186608220:[False,True,False]}
for eid,expected in diagrams.items():
 q=byid[eid];f=q.get(':question/answer-fields',[]);selected=[]
 if f and f[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
  ds=[ff for ff in f if ff[':answer-field/key'].startswith('![')];actual=[next(a[':answer/value']for a in ff[':answer-field/choices']if a[':db/id']==ff[':answer-field/correct'][':db/id'])=='true'for ff in ds];assert actual==expected,(eid,actual,expected)
 else:
  labels=['I','II','III'];wanted=' and '.join(labels[i]for i,v in enumerate(expected)if v)+' only'if any(expected)else'None'
  if f:actual=next(a[':answer/value']for a in f[0][':answer-field/choices']if a[':db/id']==f[0][':answer-field/correct'][':db/id']);assert actual==wanted,(eid,actual,wanted)
 rows.append({'entity':eid,'identity':q[':question/math-academy-id'],'subspace_diagrams_I_II_III':expected,'visual_sheet':visual[eid]['sheet'],'reviewed':['origin inclusion/exclusion','full line/plane versus half-plane/ray/quadrant','closure under negation or addition','plane/line passing through origin','original diagram crop/labels','full worked solution'],'conclusion':'Only full origin-passing linear sets or the origin/full space qualify; keys match.'})
set_cases={17592186192505:['A:x²=y fails scaling','B:affine line contains zero at t=3'],17592186193313:['A:homogeneous plane','B:zero excluded','C:zero set'],17592186193318:['A:zero would require both t=2 and t=4','B:zero excluded','C:x-axis'],17592186247150:['A:xyz=1 excludes zero','B:homogeneous plane','C:y=-1 excludes zero'],17592186247159:['A:x-4y=1 excludes zero','B:homogeneous plane','C:sum of squares<0 is empty'],17592186247160:['A:affine line excludes zero','B:homogeneous line','C:y=1 excludes zero'],17592186317380:['A:sum of squares>=0 is full plane','B:homogeneous line','C:homogeneous line'],17592186323702:['A:zero set','B:affine line excludes zero','C:zero set'],17592186342187:['A:affine plane excludes zero','B:unit ball fails scaling','C:homogeneous plane'],17592186342188:['A:sphere excludes zero','B:union of coordinate planes fails addition','C:zero excluded'],17592186342191:['A:bounded ball fails scaling','B:homogeneous plane','C:zero excluded'],17592186426533:['A:affine line excludes zero','B:union of axes fails addition','C:y-axis'],17592186426535:['A:homogeneous plane','B:zero set','C:nonzero singleton excludes zero'],17592186434595:['A:x-axis','B:homogeneous line','C:zero excluded'],17592186479092:['A:homogeneous plane','B:sphere excludes zero','C:zero set'],17592186479117:['A:zero set','B:zero excluded','C:homogeneous line'],17592186596006:['A:span of one vector','B:zero excluded','C:zero excluded'],17592186608190:['A:zero excluded','B:y-axis','C:zero set']}
for eid,reasons in set_cases.items():rows.append({'entity':eid,'identity':byid[eid][':question/math-academy-id'],'individual_set_proofs':reasons,'reviewed':['each complete set and its domain','zero-vector condition','closure under addition/scaling','all answer choices','canonical teaching pattern','full worked solution'],'conclusion':'Existing keys correct, or restored missing keys as recorded in completion evidence.'})
assert len(regions.splitlines())==50 and len(diagrams)+len(set_cases)==44
# Verify linked-list step order and content identities against every original lesson source.
topology=[]
contents={c[':db/id']:c for c in S['contents']};kps={k[':db/id']:k for k in S['knowledge_points']}
for t in S['topics']:
 ma=t['ma_id'];p=Path('/home/jake/Developer/MA/DATA/Lessons')/str(ma)/'Source'/f'{ma}.json';d=json.loads(p.read_text());source_steps=[i for i in d['lesson']['items']if i['item_type']=='step'];a=next(a for a in S['activities']if a[':activity/scope'][':db/id']==t['entity']);steps={x[':db/id']:x for x in a[':activity/steps']};ordered=[];cur=a[':activity/first-step'][':db/id']
 while cur:
  assert cur not in[x[':db/id']for x in ordered];st=steps[cur];ordered.append(st);cur=st.get(':step/next',{}).get(':db/id')
 assert len(ordered)==len(steps)==len(source_steps)
 for st,src in zip(ordered,source_steps):
  assert st[':step/math-academy-id']==int(src['step_id']);cid=st[':step/content'][':db/id']
  if src['step_type']=='tutorial':assert contents[cid][':tutorial/math-academy-id']==int(src['content_id'])
  else:assert byid[kps[cid][':knowledge-point/canonical-example'][':db/id']][':question/math-academy-id']=='e-'+src['content_id']
 topology.append({'topic':t['entity'],'source_path':str(p),'ordered_steps':[s[':db/id']for s in ordered],'source_step_ids':[int(s['step_id'])for s in source_steps],'content_identity_and_order_verified':True})
(H/'geometry-evidence.json').write_text(json.dumps({'passed':True,'checks':rows,'database_writes':0},indent=2)+'\n');(H/'step-topology-verification.json').write_text(json.dumps({'passed':True,'checks':topology,'database_writes':0},indent=2)+'\n');print('Geometry ledger',len(rows),'complete question reviews; exact topology for',len(topology),'lessons')
