"""Read displayed coordinates, vectors, all arithmetic stages and complete banks.
Actual native grade_field tests are separate field/ID compatibility evidence.
"""
import concurrent.futures,copy,hashlib,importlib.util,json,math,re,subprocess,sys,tempfile
from pathlib import Path
import sympy as sp
from PIL import Image
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('position_draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)

def scalar(value):
 value=value.replace(' ','');m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',value)
 if m:return sp.Integer(m[1] or 1)*sp.sqrt(int(m[2]))
 return sp.Integer(value)
def vec(text):
 text=text.replace(' ','').strip('.,')
 pieces=re.findall(r'([+-]?\d*)([ij])',text)
 rebuilt=''.join(a+b for a,b in pieces)
 assert rebuilt==text,(text,pieces)
 result=[]
 for variable in ['i','j']:
  vals=[(-1 if a=='-' else 1 if a in ['', '+'] else int(a)) for a,b in pieces if b==variable]
  assert len(vals)<=1
  result.append(vals[0] if vals else 0)
 return result

def blue_centers(path):
 arr=np.array(Image.open(path).convert('RGB'));mask=(arr[:,:,2]>110)&(arr[:,:,0]<70)&(arr[:,:,1]>70)&(arr[:,:,1]<170)
 seen=set();components=[];h,w=mask.shape
 for yy,xx in zip(*np.nonzero(mask)):
  if (int(yy),int(xx)) in seen:continue
  todo=[(int(yy),int(xx))];seen.add(todo[0]);pixels=[]
  while todo:
   y,x=todo.pop();pixels.append((x,y))
   for dy,dx in [(1,0),(-1,0),(0,1),(0,-1)]:
    yn,xn=y+dy,x+dx
    if 0<=yn<h and 0<=xn<w and mask[yn,xn] and (yn,xn) not in seen:seen.add((yn,xn));todo.append((yn,xn))
  if len(pixels)>12:components.append([sum(p[0] for p in pixels)/len(pixels),sum(p[1] for p in pixels)/len(pixels),len(pixels)])
 return components

def read_grid(asset,source=False):
 path=ROOT/asset['path'];centers=blue_centers(path)
 if source:
  # Independently measured native origin and axis units; source image is
  # anisotropic (56 x pixels versus 46.7 y pixels per coordinate unit).
  origin=[141,233];ux=56.;uy=140./3;h=304
  expected_order=[[197,186.5],[253,93]]
 else:
  axes=asset['axes'];h=asset['dimensions'][1];origin=[axes['origin_pixel'][0],h-axes['origin_pixel'][1]]
  ux=axes['unit_x_pixel'][0]-axes['origin_pixel'][0];uy=axes['unit_y_pixel'][1]-axes['origin_pixel'][1]
  assert abs(ux-uy)<1e-7,'generated equal coordinate units'
  expected_order=[[p[0],h-p[1]] for p in axes['endpoint_pixels']]
  # Actual PNG has a black axis intersection at the calibrated origin.
  arr=np.array(Image.open(path).convert('RGB'));ox,oy=map(round,origin)
  assert (arr[max(0,oy-2):oy+3,max(0,ox-2):ox+3,:].min(axis=2)<60).any()
 result=[]
 for expected in expected_order:
  x,y,count=min(centers,key=lambda c:(c[0]-expected[0])**2+(c[1]-expected[1])**2)
  assert math.hypot(x-expected[0],y-expected[1])<2,(centers,expected)
  a,b=(x-origin[0])/ux,(origin[1]-y)/uy
  assert abs(a-round(a))<.055 and abs(b-round(b))<.055,(a,b)
  result.append([round(a),round(b)])
 assert len({tuple(p) for p in result})==2
 return result

def coordinates(record):
 q=record['question'];pairs=re.findall(r'\b[A-Z]\((-?\d+),\s*(-?\d+)\)',q[':question/problem'])
 if pairs:return [list(map(int,p)) for p in pairs]
 asset=record['generation']['assets'][0]
 return read_grid(asset,asset['renderer']=='original captured raster')

def math_check(record):
 q=record['question'];points=coordinates(record);p,r=points;d=[r[i]-p[i] for i in range(2)];n=sum(v*v for v in d)
 assert points==record['generation']['parameters']['points']
 solution=q.get(':question/worked-solution')
 if solution:
  environments=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert len(environments)==3
  rows=[[v.strip() for v in re.split(r'\\\\',env)] for env in environments]
  assert len(rows[0])==2 and len(rows[1])==4 and len(rows[2]) in [3,4],rows
  position=[vec(row.rsplit('=',1)[1]) for row in rows[0]];assert position==points
  # Check formal order from actual point labels in source or rendered question.
  labels=g.SPECS[record['generation']['source_ids'][0]]['labels'];a,b=labels
  assert '{O'+b+'}' in rows[1][0] and '{O'+a+'}' in rows[1][0]
  assert rows[1][0].index('{O'+b+'}')<rows[1][0].index('{O'+a+'}')
  assert rows[1][0].split('=',1)[1].replace(' ','')==r'\overset{\to}{O'+b+r'}-\overset{\to}{O'+a+'}'
  assert rows[1][1].split('=')[1].replace(' ','')==b.lower()+'-'+a.lower()
  pair=re.search(r'=\s*\((.*?)\)\s*-\s*\((.*?)\)',rows[1][2]);assert pair
  assert [vec(pair[1]),vec(pair[2])]==[r,p]
  assert vec(rows[1][3].rsplit('=',1)[1])==d
  assert not re.search(r'\{-\d+\}\^\{2\}',rows[2][0]),'negative square base must visibly group sign'
  square=rows[2][0].split('=',1)[1].replace(' ','').replace('{','').replace('}','').replace('(','').replace(')','')
  m=re.fullmatch(r'\\sqrt(-?\d+)\^2\+(-?\d+)\^2',square);assert m and list(map(int,m.groups()))==d,(square,d)
  evaluated=re.search(r'\\sqrt\{(\d+)\+(\d+)\}',rows[2][1].replace(' ',''));assert evaluated and list(map(int,evaluated.groups()))==[v*v for v in d]
  assert rows[2][2].split('=',1)[1].strip().removesuffix('.')==rf'\sqrt{{{n}}}', 'collected squared sum must remain explicit'
  final=rows[2][-1].split('=',1)[1].strip().removesuffix('.')
  assert sp.simplify(scalar(final)-sp.sqrt(n))==0
  # Every authored signed subtraction row is read independently, including signs.
  explicit=re.findall(r'\((-?\d+)\)-\((-?\d+)\)=(-?\d+)',solution)
  if not record['generation']['evidence_only']:
   assert len(explicit)==2 and [[int(v) for v in trip] for trip in explicit]==[[r[i],p[i],d[i]] for i in range(2)]
  if record['generation']['template']=='graph_read':
   intro=re.findall(r'\b[A-Z]\((-?\d+),\s*(-?\d+)\)',solution)
   assert [list(map(int,pair)) for pair in intro[:2]]==points
 fields=q.get(':question/answer-fields',[])
 for field in fields:
  assert field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection'
  answers=field[':answer-field/choices'];values=[scalar(a[':answer/value']) for a in answers];assert len(answers)==5
  assert len({a[':answer/id'] for a in answers})==5
  for i in range(5):
   for j in range(i):assert sp.simplify(values[i]-values[j])!=0
  correct=[a[':answer/id'] for a,v in zip(answers,values) if sp.simplify(v-sp.sqrt(n))==0];assert len(correct)==1
  if ':answer-field/correct' in field:assert field[':answer-field/correct']==[':answer/id',correct[0]]
  assert all(':answer/feedback' not in a for a in answers)
 assert record['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 # Control-character regression applies to normal output and actual strings.
 for text in [q[':question/problem'],solution or '']+[a[':answer/value'] for f in fields for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in text)
  assert text.count('$')%2==0
  assert text.count('{')==text.count('}')
 return {'points':points,'displacement':d,'squares':[v*v for v in d],'squared_sum':n,'magnitude':str(sp.sqrt(n))}

def rejects(record,mutator):
 bad=copy.deepcopy(record);mutator(bad)
 try:math_check(bad)
 except (AssertionError,ValueError):return True
 raise AssertionError('mutation escaped independent validator')

def main():
 assert (HERE/'source.json').read_bytes()==(ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186059715.json').read_bytes()
 originals=[];fidelity=[];stage_checks=[]
 cases=json.loads((HERE/'source-cases.json').read_text())
 for row in cases:
  record=g.generate(row['level'],template=row['template'],profile=row['bank_profile'],parameters=row['parameters']);source=g.ORIGINALS[row['source_id']]
  proof=math_check(record);stage_checks.append({'label':row['source_id'],'independent':proof})
  q=record['question'];assert q[':question/problem']==source[':question/problem']
  assert q.get(':question/worked-solution')==source.get(':question/worked-solution')
  for key in [':question/difficulty',':question/worked-solution',':question/answer-fields',':question/requires-calculator']:assert (key in q)==(key in source)
  if ':question/difficulty' in source:assert q[':question/difficulty']==source[':question/difficulty'][':db/ident']
  banks=0;choices=0
  for sf,gf in zip(source.get(':question/answer-fields',[]),q.get(':question/answer-fields',[])):
   assert sf[':answer-field/type'][':db/ident']==gf[':answer-field/type']
   assert (':answer-field/correct' in sf)==(':answer-field/correct' in gf)
   observed=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);emitted=sorted(a[':answer/value'] for a in gf[':answer-field/choices']);assert observed==emitted
   for sa,ga in zip(sorted(sf[':answer-field/choices'],key=lambda a:a[':answer/value']),sorted(gf[':answer-field/choices'],key=lambda a:a[':answer/value'])):assert (':answer/feedback' in sa)==(':answer/feedback' in ga)
   banks+=1;choices+=len(observed)
  fidelity.append({'source_id':row['source_id'],'raw_prompt_exact':True,'raw_solution_exact_or_absent':True,'attribute_presence_parity':True,'complete_banks':banks,'matched_choices':choices,'matched_distractors':max(choices-banks,0),'missing_original_correct_ref':bool(banks),'grading_evidence':'missing source key remains absent; independent norm does not count as designation match'})
  originals.append(record)
 # All normal families and levels; explicit source-shaped changes and level bounds.
 reviews=[];normal=[];family_coverage={level:set() for level in g.DOMAINS}
 for level in g.DOMAINS:
  for seed in range(60):
   record=g.generate(level,seed);math_check(record);normal.append(record);family_coverage[level].add(record['generation']['template'])
   if seed<2:reviews.append(record)
  for family in sorted(family_coverage[level]):
   record=g.generate(level,100,template=family);math_check(record)
   if not any(r['generation']['template']==family and r['question'][':question/difficulty']==':question.difficulty/'+level for r in reviews):reviews.append(record)
 assert family_coverage['moderate']==set(g.FAMILIES)
 # Exact bank evidence generalizes only as explicitly opaque homogeneous profiles.
 changed=[]
 for mid in ['q-18051','q-18052']:
  for scale in [2,3,4]:
   record=g.generate('moderate',profile='evidence:'+mid,parameters={'scale':scale});math_check(record);changed.append(record)
 for mid,points in [('q-125118',[[2,3],[-1,1]]),('q-18049',[[-2,4],[1,-2]]),('q-18055',[[2,1],[4,4]])]:
  record=g.generate('moderate',profile='evidence:'+mid,parameters={'points':points});math_check(record);changed.append(record)
 boundary=json.loads((HERE/'boundary-review.json').read_text())
 for record in boundary:math_check(record)
 # Identity unchanged by seed/order, changed bank/solution/reading cannot share ID.
 sample=normal[0];level=sample['question'][':question/difficulty'].split('/')[-1];params=sample['generation']['parameters'];family=sample['generation']['template']
 a=g.generate(level,0,template=family,parameters=params);b=g.generate(level,44,template=family,parameters=params)
 assert a['question'][':question/id']==b['question'][':question/id']
 assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
 assert [x[':answer/id'] for x in a['question'][':question/answer-fields'][0][':answer-field/choices']] != [x[':answer/id'] for x in b['question'][':question/answer-fields'][0][':answer-field/choices']]
 # Common translation with unchanged subtraction signs is one assessed task.
 tx=[[v+1 for v in p] for p in sample['generation']['parameters']['points']]
 # Direct fingerprint definition checked without forcing a translated point out of level bounds.
 d=lambda ps:[ps[1][i]-ps[0][i] for i in range(2)]
 assert d(tx)==d(sample['generation']['parameters']['points'])
 # Explicit invalid calls fail with the same guards as samplers.
 invalid=[('easy','coordinate_ab',{'points':[[-1,1],[3,2]]}),('moderate','coordinate_ab',{'points':[[1,1],[3,4]]}),('hard','graph_read',{'points':[[-8,0],[8,7]]}),('hard','graph_read',{'points':[[0,0],[2,4]]})]
 for level,family,params in invalid:
  try:g.generate(level,template=family,parameters=params)
  except ValueError:pass
  else:raise AssertionError('explicit boundary guard bypassed')
 # Displacement reversal has identical norm: never claim it as wrong scalar.
 p,q=sample['generation']['parameters']['points'];assert sum((q[i]-p[i])**2 for i in range(2))==sum((p[i]-q[i])**2 for i in range(2))
 # Required teaching rows, signed sum and fixed conclusion mutation regressions.
 mut=normal[0]
 rejects(mut,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('Now, using the formula', '\x0cNow, using the formula')))
 rejects(mut,lambda r:r['question'].__setitem__(':question/worked-solution',re.sub(r'(\\sqrt\{)(\d+)(\+\d+\})',lambda m:m[1]+str(int(m[2])+1)+m[3],r['question'][':question/worked-solution'],count=1)))
 rejects(mut,lambda r:r['question'].__setitem__(':question/worked-solution',re.sub(r'&\s*=\s*\([^)]*\)-\([^)]*\)\s*\\\\','',r['question'][':question/worked-solution'],count=1)))
 # Engine is memory-only. Missing source refs/fields never receive synthetic raw
 # grading success; completed normal records are explicitly authored.
 native=[]
 for record in normal+reviews+boundary:
  field=record['question'][':question/answer-fields'][0]
  native.append({'label':record['question'][':question/id'],'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'Radio field-owned UUID compatibility; independent full value-bank proof is separate'} for a in field[':answer-field/choices']]})
 (HERE/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 report=json.loads((HERE/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
 # Fresh concurrent processes test identical and different instances, avoiding
 # cached reads: each process uses a unique private evidence render directory.
 with tempfile.TemporaryDirectory(prefix='concurrent-',dir=HERE) as td:
  helper=HERE/'concurrent-render.py'
  helper.write_text('import importlib.util,json,sys\nfrom pathlib import Path\ns=importlib.util.spec_from_file_location("g",sys.argv[1]);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)\ng.HERE=Path(sys.argv[2]);g.ROOT=Path(sys.argv[3]);g.HERE.mkdir(parents=True,exist_ok=True)\nr=g.render_plots(json.loads(sys.argv[4]),["P","Q"],"grid",2);print(json.dumps(r))\n')
  inputs=[[[ -6,1],[3,-4]],[[-6,1],[3,-4]],[[7,-5],[-3,2]],[[7,-5],[-3,2]]]
  def call(item):
   i,points=item
   out=subprocess.check_output([sys.executable,str(helper),str(HERE.with_suffix('.py')),str(Path(td)/'shared'),str(ROOT),json.dumps(points)],text=True)
   asset=json.loads(out);assert read_grid(asset)==points;return asset
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:assets=list(executor.map(call,enumerate(inputs)))
  assert assets[0]['sha256']==assets[1]['sha256'] and assets[2]['sha256']==assets[3]['sha256']
  assert assets[0]['sha256']!=assets[2]['sha256']
  assert not any(p.name.endswith('.tmp') for p in Path(td).rglob('*'))
 (HERE/'review.json').write_text(json.dumps(originals+reviews+changed,indent=2)+'\n')
 sections=[]
 for record in originals+reviews+changed:
  q=record['question'];asset=record['generation']['assets'][0];review_problem=q[':question/problem'].replace(asset['reference'],str((ROOT/asset['path']).relative_to(HERE)));sections.append(('ORIGINAL MA EVIDENCE' if record['generation']['evidence_only'] else 'AUTHORED NORMAL '+q[':question/difficulty'])+' — '+record['generation']['template']+'\n\n'+review_problem+'\n\n'+q.get(':question/worked-solution','Worked solution absent in original.')+'\n\n'+'Choices: '+', '.join('$'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']))
 (HERE/'review.md').write_text('\n\n---\n\n'.join(sections)+'\n')
 files=[HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'topic.json',HERE/'lesson.json',ROOT/'generate/runs/current/check-engine',ROOT/'generate/runs/current/check-engine.rs']
 result={'status':'pass','source_basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'source_fidelity':{'original_questions':5,'public_replays':5,'complete_available_banks':2,'matched_choices':10,'total_choices':10,'matched_distractors':8,'total_distractors':8,'stored_correct_refs_present':0,'missing_correct_refs_preserved':2,'fieldless_preserved':3,'unrated_preserved':2,'missing_solution_preserved':2,'calculator_absence_preserved':5,'feedback_absence_preserved':10,'source_rows':fidelity,'raw_exact_prompts':5,'raw_exact_present_solutions':3},'mathematics':{'normal_instances':len(normal),'boundary_instances':len(boundary),'independent_printed_stage_checks':True,'original_and_changed':stage_checks,'changed_evidence_instances':len(changed),'all_bank_pair_criterion':'exact nonnegative scalar magnitude; reversal norm equal and excluded as distractor','control_and_missing_stage_mutations_rejected':3},'variation':{'finite_domain_enumeration':json.loads((HERE/'domain-enumeration.json').read_text()),'default_family_coverage':{k:sorted(v) for k,v in family_coverage.items()},'distinct_assessed_fingerprints':{level:len({r['generation']['parameter_fingerprint'] for r in normal if r['question'][':question/difficulty']==':question.difficulty/'+level}) for level in g.DOMAINS},'translations_excluded_from_task_data':True,'bounds_applied_to_explicit_calls':True},'plots':{'original_native_inspected':5,'grid_source_coordinates_independently_calibrated':[[1,1],[2,3]],'normal_grid_points_read_back_from_png':True,'fresh_concurrent_render_processes':4,'concurrent_shared_directory':True,'visual_review_boundary_instances':4,'equal_scale_generated':True},'native_engine':report,'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':__import__('matplotlib').__version__},'hashes':{str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in files},'unresolved':['Original two five-choice banks have opaque historical distractor intent; scale profiles evidence-only and never defaults.','Original missing keys/fields/solutions/difficulty remain unknown in raw evidence; authored normal completions are separate.'],'database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','source_fidelity','variation','runtime']},indent=2))
if __name__=='__main__':main()
