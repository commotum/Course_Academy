"""Independent source/prose/graph criterion checks plus native radio grading."""
import importlib.util,json,re,subprocess,sys,copy
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('gen',str(ROOT)+'.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((ROOT/'source.json').read_text())['record'][':knowledge-point/questions'];out=[];engine=[]
def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];meta=r['generation'];p=meta['parameters'];s=q[':question/problem'];sol=q.get(':question/worked-solution','')
 assert '{{' not in s and '{{' not in sol
 for text in [s,sol]+[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]:
  assert all(ord(c)>=32 or c in '\n\t' for c in text)
  assert text.count('$')%2==0
  # Brace balancing independent of command names.
  depth=0
  for c in text:
   if c=='{':depth+=1
   if c=='}':depth-=1
   assert depth>=0
  assert depth==0
 if meta['evidence_only']:return
 f=q[':question/answer-fields'][0];bank=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(bank)==5 and len(set(bank))==5
 for i,a in enumerate(bank):
  for b in bank[i+1:]:assert subset(a)!=subset(b),'all-pairs criterion equivalence'
 geom=meta['plot_geometry'];a=geom['targets'][0];xmin,xmax,ymin,ymax=geom['bounds'];assert xmin<0<xmax and ymin<0<ymax
 if meta['template'] in g.SPECS:
  sid=meta['template'];orig=g.SPECS[sid];sh=p['shift'];target=orig['a']+sh
  coords=re.findall(r'x\s*=\s*(-?\d+)',s)
  assert int(coords[0])==(orig['b']+sh if sid=='q-48068' else target)
  # Independent source mathematical facts from marker/limit transcription.
  v=orig['value'];l=orig['left'];rr=orig['right'];exists=l==rr and not isinstance(l,str);cont=exists and v is not None and l==v
  for coord in re.findall(r'f\((-?\d+)\)',sol):assert int(coord)==target,(sid,coord,target)
  for coord in re.findall(r'x\\to \\\\,(-?\{?\d+\}?)',sol):assert int(coord.replace('{','').replace('}',''))==target,(sid,coord,target)
  expected_prose=re.sub(r'\$\$.*?\$\$|\$.*?\$','',q_source(sid).get(':question/worked-solution',''),flags=re.S)
  if expected_prose:assert re.sub(r'\$\$.*?\$\$|\$.*?\$','',sol,flags=re.S)==expected_prose
  bits={'q-48042':[not isinstance(l,str),not isinstance(rr,str),not cont],'q-48064':[v is not None,exists,cont],'q-48063':[v is not None,not isinstance(l,str),cont],'q-104049':[v is not None,exists and l!=v,not cont],'q-104051':[v is not None,exists,not cont],'q-104052':[v is None,exists,cont],'q-104124':[v is None,exists and l==v,cont],'q-48040':[v is not None,exists,cont],'q-48062':[v is not None,exists,cont],'q-48065':[v is not None,exists and l==v,cont],'q-48067':[v is not None,exists and l==v,cont],'q-48068':[True,False,True]}[sid]
 else:
  # Read point/branch markers and plotted limit values independently from the printed graph data.
  markers=geom['markers'];at=[m for m in markers if m[0]==a];filled=[m[1] for m in at if m[2]];v=filled[0] if filled else None
  curves=geom['curves'];left_y=curves[0][1][0];right_y=curves[1][1][0]
  if meta['template']=='fractional_value':
   l=round(left_y);rr=round(right_y);bits=[v is not None,l==rr and v==l,False]
   assert r'\frac' in s and 'I.' in s
  else:
   left_inf=abs(left_y)>=9;right_inf=abs(right_y)>=9;b=geom['targets'][1];hole=any(m[0]==b and not m[2] for m in markers);bits=[not left_inf,right_inf,not hole]
   assert a!=b and r'\frac' in s
 correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==g.answer_name(bits),(correct,bits)
 for i,b in enumerate(bits):assert f'Statement {"I"*(i+1)} is {"true" if b else "false"}' in sol
 plot=Path(re.search(r'!\[\]\((.*?)\)',s)[1]);assert plot.exists()
 if plot.with_suffix('.json').exists():raster(plot,geom)
def q_source(sid):return next(q for q in source if q[':question/math-academy-id']==sid)
def subset(s):return set(re.findall(r'\bIII\b|\bII\b|\bI\b',s))
def raster(path,geom):
 m=json.loads(path.with_suffix('.json').read_text());im=np.array(Image.open(path).convert('RGB'));T=np.array(m['transform']);h=im.shape[0]
 assert np.allclose(T@np.array([0,0,1]),[*m['origin'],1])
 for x,y,filled in geom['markers']:
  xy=T@np.array([x,y,1]);cx=int(round(xy[0]));cy=int(round(h-xy[1]));patch=im[max(0,cy-2):cy+3,max(0,cx-2):cx+3];red=(patch[:,:,0]>180)&(patch[:,:,1]<150)&(patch[:,:,2]<150)
  if filled:assert red.mean()>.4,(path,x,y,'filled center')
  else:assert red.mean()<.25,(path,x,y,'open center')
def add_engine(r,label):
 for f in r['question'].get(':question/answer-fields',[]):
  if ':answer-field/correct' not in f:continue
  engine.append({'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native subset criterion selection'} for a in f[':answer-field/choices']]})
def main():
 coverage={'banks':0,'options':0,'correct_designations':0,'missing_correct':0,'fieldless':0,'raw_presence':0,'solutions':0};reviews=[]
 for q in source:
  sid=q[':question/math-academy-id'];r=g.generate('easy',template=sid,parameters={'shift':0},profile='observed');check(r);new=r['question'];asset=re.search(r'!\[\]\((.*?)\)',q[':question/problem'])[1]
  assert new[':question/problem']==q[':question/problem'].replace(asset,g.SPECS[sid]['image']),sid
  for k in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (k in q)==(k in new),(sid,k)
  coverage['raw_presence']+=1
  if ':question/worked-solution' in q:assert q[':question/worked-solution']==new[':question/worked-solution'];coverage['solutions']+=1
  for a,b in zip(q.get(':question/answer-fields',[]),new.get(':question/answer-fields',[])):
   assert sorted(c[':answer/value'] for c in a[':answer-field/choices'])==sorted(c[':answer/value'] for c in b[':answer-field/choices']);assert (':answer-field/correct' in a)==(':answer-field/correct' in b)
   coverage['banks']+=1;coverage['options']+=len(a[':answer-field/choices'])
   if ':answer-field/correct' in a:
    assert a[':answer-field/correct'][':answer/value']==next(c[':answer/value'] for c in b[':answer-field/choices'] if c[':answer/id']==b[':answer-field/correct'][1]);coverage['correct_designations']+=1
   else:coverage['missing_correct']+=1
  if ':question/answer-fields' not in q:coverage['fieldless']+=1
  reviews.append({'label':'Original '+sid,'record':r});add_engine(r,'observed/'+sid)
  for shift in [-3,2]:
   rr=g.generate('easy',template=sid,parameters={'shift':shift});check(rr);out.append(rr);add_engine(rr,sid+'/shift'+str(shift));reviews.append({'label':'Generated easy '+sid+' shift '+str(shift),'record':rr})
 for level in ['moderate','hard']:
  for seed in range(16):
   r=g.generate(level,seed);check(r);out.append(r);add_engine(r,level+'/'+str(seed))
   if seed<3:reviews.append({'label':'Generated authored '+level+'/'+str(seed),'record':r})
 # Exhaust finite hard structural topology catalog at one nonincidental grid.
 hard_tasks=set()
 for left,right in [('-inf',1),(1,'+inf'),('-inf','+inf')]:
  for orient in [-1,1]:
   for continuous in [False,True]:
    p={'a':.25,'left':left,'right':right,'value':2,'b':.25+orient,'b_continuous':continuous}
    r=g.generate('hard',parameters=p);check(r);out.append(r);add_engine(r,'hard/finite-catalog');hard_tasks.add(r['generation']['mathematical_fingerprint'])
 assert len(hard_tasks)==12
 # Default family coverage (selection precedes all source parameter sampling).
 seen={g.generate('easy',seed)['generation']['template'] for seed in range(128)}
 assert seen==set(g.SPECS)
 # Identity/order guard and explicit level bounds.
 for level in ['easy','moderate','hard']:
  a=g.generate(level,1);b=g.generate(level,99,template=a['generation']['template'],parameters=a['generation']['parameters'],profile=a['generation']['profile']);assert a['question'][':question/id']==b['question'][':question/id']
 for l,p in [('easy',{'shift':.5}),('moderate',{'a':1,'left':1,'right':1,'value':2}),('hard',{'a':.5,'left':'-inf','right':1,'value':2,'b':1.5,'b_continuous':True})]:
  try:g.generate(l,parameters=p)
  except ValueError:pass
  else:raise AssertionError('explicit workload guard absent')
 # Mutations prove marker and criterion checks reject actual wrong output.
 mutated=copy.deepcopy(out[0]);mutated['question'][':question/answer-fields'][0][':answer-field/correct'][1]=mutated['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']
 # Always select a genuinely incorrect option for the mutation.
 original_correct=out[0]['question'][':question/answer-fields'][0][':answer-field/correct'][1]
 mutated['question'][':question/answer-fields'][0][':answer-field/correct'][1]=next(a[':answer/id'] for a in mutated['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']!=original_correct)
 if True:
  try:check(mutated)
  except AssertionError:pass
  else:raise AssertionError('correct-choice mutation undetected')
 control=copy.deepcopy(out[0]);control['question'][':question/worked-solution']+='\x0c'
 try:check(control)
 except AssertionError:pass
 else:raise AssertionError('control character mutation undetected')
 collision=copy.deepcopy(out[0]);f=collision['question'][':question/answer-fields'][0];f[':answer-field/choices'][1][':answer/value']=f[':answer-field/choices'][0][':answer/value']
 try:check(collision)
 except AssertionError:pass
 else:raise AssertionError('whole-bank collision mutation undetected')
 (ROOT/'native-input.json').write_text(json.dumps(engine));subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True)
 native=json.loads((ROOT/'native-report.json').read_text());(ROOT/'review.json').write_text(json.dumps(reviews,indent=2));md=[]
 for item in reviews:
  q=item['record']['question'];md.extend(['## '+item['label'],q[':question/problem'],'Choices: '+', '.join(a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']),q.get(':question/worked-solution','Original omitted worked solution.'),''])
 (ROOT/'review.md').write_text('\n\n'.join(md));report={'status':'passed','source_coverage':coverage,'hard_structural_catalog':len(hard_tasks),'normal_records':len(out),'native':native,'dependencies':out[0]['generation']['dependencies'],'raw_designation_inference':'q-48064 absent; no designation fidelity claimed. Normal independent derivation I only.','semantic_tasks_sampled':{l:len({r['generation']['mathematical_fingerprint'] for r in out if r['question'][':question/difficulty']==':question.difficulty/'+l}) for l in ['easy','moderate','hard']},'default_easy_families':sorted(seen),'finite_variety':'Easy 12 source graph/statement presentations × 9 coordinate shifts. Moderate 3 local topologies × 4 signed half-grid targets × 5 labelled ordinate anchors. Hard 3 infinity arrangements × 8 quarter-grid targets × 2 second-neighborhood states × 2 relative target orientations. Coordinates/grid affect reading; canonical categorical tasks separately: easy11 (continuous equality sources65/67 deduplicate), moderate3, hard12; pure coordinate shifts and incidental ordinates are excluded from canonical task fingerprints.','concurrency':json.loads((ROOT/'concurrency-report.json').read_text()),'plot_method':'Matplotlib; native source traces retain unknown algebra uncertainty; independent markers and calibrations; marker-center pixel checks.','db_writes':0}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({'status':'passed','source_coverage':coverage,'hard_structural_catalog':len(hard_tasks),'normal_records':len(out),'native_accepted':native.get('accepted_checks'),'native_rejected':native.get('rejected_checks')}))
if __name__=='__main__':main()
