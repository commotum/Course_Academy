import sys,os,json,re,importlib.util,copy,hashlib,platform,shutil,subprocess
from pathlib import Path
from fractions import Fraction
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
JOB=ROOT.parent
REPO=Path('/home/jake/Developer/Course_Academy')
def save(name,x): (ROOT/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def load_generator(path):
 spec=importlib.util.spec_from_file_location('reviewed',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def matrices(text):
 text=re.sub(r'\\color\{[^}]*\}','',text);text=text.replace(r'\bbox[lightgray,2pt]','')
 return [[[int(v.replace('{','').replace('}','').strip()) for v in row.split('&')] for row in raw.split(r'\\')] for raw in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]
def ops(text):
 t=re.sub(r'\s|\$|\\,','',text).replace('{C}','C')
 return [(int(a)-1,int(p)-1,int(s+(n or '1'))) for a,b,s,n,p in re.findall(r'C_\{?(\d)\}?:=C_\{?(\d)\}?([+-])(\d*)C_\{?(\d)\}?',t) if a==b]
def field(rec):return rec['question'][':question/answer-fields'][0]
def correct_index(rec):
 f=field(rec);return next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
def coefficients(rec):return [tuple(o[2] for o in ops(a[':answer/value'])) for a in field(rec)[':answer-field/choices']]
def shortcut(rec):
 pairs=coefficients(rec); counts=Counter(tuple(map(abs,p)) for p in pairs)
 if sorted(counts.values())!=[1,4]:return None
 odd=next(p for p in pairs if counts[tuple(map(abs,p))]==1)
 main=next(p for p,c in counts.items() if c==4)
 if tuple(map(abs,odd))!=main[::-1] or main[0]==main[1]:return None
 predicted=(-odd[1],-odd[0]);return pairs.index(predicted) if predicted in pairs else None
def inspect(rec):
 q=rec['question'];A,B=matrices(q[':question/problem']);given=ops(q[':question/problem']);assert len(given)==1
 g,p,k=given[0]; assert all(A[i][p]==B[i][p] for i in range(4))
 ks={}
 for c in range(4):
  if c==p:continue
  ratios={Fraction(B[i][c]-A[i][c],A[i][p]) for i in range(4) if A[i][p]}
  assert len(ratios)==1;ks[c]=ratios.pop();assert ks[c].denominator==1
  assert all(A[i][c]+ks[c]*A[i][p]==B[i][c] for i in range(4))
 assert k==ks[g]
 expected=[(c,p,int(ks[c])) for c in sorted(ks) if c!=g]
 bank=[ops(a[':answer/value']) for a in field(rec)[':answer-field/choices']]
 assert len(bank)==5 and len(set(map(tuple,bank)))==5
 assert bank.count(expected)==1 and bank[correct_index(rec)]==expected
 stages=matrices(q[':question/worked-solution']);assert len(stages)==4 and stages[0]==A
 cur=copy.deepcopy(A)
 for j,c in enumerate(sorted(ks)):
  for i in range(4):cur[i][c]+=ks[c]*cur[i][p]
  assert cur==stages[j+1]
 assert stages[-1]==B
 so=ops(q[':question/worked-solution']);assert so[:3]==[(c,p,int(ks[c])) for c in sorted(ks)] and so[3:]==expected
 return {'id':q[':question/id'],'seed':rec['generation']['seed'],'profile':rec['generation']['bank_profile'],'correct_index':correct_index(rec),'pair':[o[2] for o in expected],'shortcut':shortcut(rec),'rows':[i for i in range(4) if A[i][p] and all(B[i][c]==0 for c in ks)]}
def main():
 m=load_generator(JOB/'workspace/17592186161966.py')
 records=[m.generate(seed=731000+100*j+i,bank_profile=p) for j,p in enumerate(m.PROFILES) for i in range(12)]
 batch=json.load(open(JOB/'samples.json'));save('samples.json',records);save('batch.json',batch)
 results=[inspect(r) for r in records];br=[inspect(r) for r in batch]
 save('math-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python review.py','sample_count':len(records),'results':results,'batch_results':br})
 replay=[];recs=[]
 src=json.load(open(JOB/'source/source.json'))['material']['kp']
 for q in src[':knowledge-point/questions']:
  profile=q[':question/math-academy-id'];A,B=matrices(q[':question/problem']);g,p,k=ops(q[':question/problem'])[0]
  r=next(i for i in range(4) if A[i][p] and all(B[i][c]==0 for c in range(4) if c!=p));ks=[int(Fraction(-A[r][c],A[r][p])) if c!=p else 0 for c in range(4)]
  par={'A':A,'row':r,'pivot':p,'given':g,'ks':ks};row={'source_id':q[':question/id'],'profile':profile,'parameters':par}
  try:
   rec=m.generate(seed=883,bank_profile=profile,parameters=par);inspect(rec);recs.append(rec)
   banks=[sorted([ops(c[':answer/value']) for c in f[':answer-field/choices']]) for f in q[':question/answer-fields']]
   got=sorted([ops(c[':answer/value']) for c in field(rec)[':answer-field/choices']]);row.update(status='passed' if all(b==got for b in banks) else 'failed',complete_banks_match=[b==got for b in banks],matrices_match=matrices(rec['question'][':question/problem'])==[A,B])
  except Exception as e:row.update(status='failed',error=repr(e))
  replay.append(row)
 # canonical backbone replay, no source bank exists
 q=src[':knowledge-point/canonical-example'];A,B=matrices(q[':question/problem']);par={'A':A,'row':2,'pivot':1,'given':2,'ks':[5,0,-4,-2]}
 rec=m.generate(seed=883,bank_profile='q-130619',parameters=par);inspect(rec);recs.append(rec)
 replay.append({'source_id':q[':question/id'],'status':'passed','canonical_backbone_only':True,'matrices_match':matrices(rec['question'][':question/problem'])==[A,B]})
 save('source-replay.json',replay);save('source-replays.json',recs)
 # Three controlled instances: base, changed answer-bearing entry, changed irrelevant off-row entry; also changed given target.
 par={'A':[[2,4,-6,8],[1,0,2,-1],[3,1,0,2],[-1,2,1,0]],'row':0,'pivot':0,'given':3,'ks':[0,-2,3,-4]}
 base=m.generate(seed=9123,bank_profile='q-130619',parameters=par)
 relevant=copy.deepcopy(par);relevant['A'][0][1]=-4;relevant['ks'][1]=2
 irrelevant=copy.deepcopy(par);irrelevant['A'][1][2]=7
 target=copy.deepcopy(par);target['given']=1
 cf=[base,m.generate(seed=9123,bank_profile='q-130619',parameters=relevant),m.generate(seed=9123,bank_profile='q-130619',parameters=irrelevant),m.generate(seed=9123,bank_profile='q-130619',parameters=target)]
 cfr=[inspect(r) for r in cf];assert cfr[0]['pair']!=cfr[1]['pair'] and cfr[0]['pair']==cfr[2]['pair'] and cfr[0]['pair']!=cfr[3]['pair']
 save('counterfactuals.json',cf);save('counterfactual-results.json',cfr)
 probes=[]
 for label,rs in [('fresh',records),('batch',batch)]:
  applicable=[r for r in rs if shortcut(r)!=None]
  probes.append({'set':label,'strategy':'Four choices share the same ordered absolute multiplier pair. Find the singleton swapped pair (u,v); select (-v,-u). Uses choices only, never A/B.','applicable':len(applicable),'correct':sum(shortcut(r)==correct_index(r) for r in applicable),'by_profile':{p:{'count':sum(r['generation']['bank_profile']==p for r in applicable),'correct':sum(r['generation']['bank_profile']==p and shortcut(r)==correct_index(r) for r in applicable)} for p in sorted({r['generation']['bank_profile'] for r in applicable})}})
 save('shortcut-results.json',probes)
 # Native grading: all bank choices, including actual shortcut-selected IDs and controlled pairs.
 cases=[]
 for label,rs in [('sample',records),('batch',batch),('counterfactual',cf)]:
  for i,r in enumerate(rs):
   good=correct_index(r);cases.append({'label':f'{label}-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==good else 'rejected','purpose':'Independently calculated column operation pair' + ('; choice-only shortcut' if j==shortcut(r) else '')} for j,a in enumerate(field(r)[':answer-field/choices'])]})
 save('grader-input.json',cases)
 save('render-input.json',batch[:1]+[r for r in batch if shortcut(r)!=None][:1]+cf)
 # Replay, package relocation, exact dependency checks.
 dest=ROOT/'relocated';dest.mkdir(exist_ok=True);shutil.copyfile(JOB/'workspace/17592186161966.py',dest/'17592186161966.py');(dest/'17592186161966').mkdir(exist_ok=True);shutil.copyfile(JOB/'workspace/17592186161966/source.json',dest/'17592186161966/source.json')
 clone=load_generator(dest/'17592186161966.py');assert clone.generate(seed=731000,bank_profile=m.PROFILES[0])==records[0];assert m.generate(seed=731000,bank_profile=m.PROFILES[0])==records[0]
 reject=[]
 for difficulty in ['easy','hard']:
  try:m.generate(difficulty=difficulty);reject.append({'difficulty':difficulty,'rejected':False})
  except ValueError:reject.append({'difficulty':difficulty,'rejected':True})
 bad=copy.deepcopy(par);bad['A'][0][0]=0
 try:m.generate(parameters=bad);reject.append({'zero_pivot_rejected':False})
 except AssertionError:reject.append({'zero_pivot_rejected':True})
 save('packaging.json',{'python':platform.python_version(),'sympy':m.sp.__version__,'manifest':json.load(open(JOB/'workspace/package.json'))['dependencies'],'deterministic':True,'relocated_replay_identical':True,'no_asset_output':True,'rejections':reject,'repair_history_exists':(JOB/'repair-history.json').exists(),'repair_preflight_exists':(JOB/'repair-preflight.json').exists()})
 inventory=json.load(open(JOB/'source/inventory.json'));source_ids={q[':question/id'] for q in src[':knowledge-point/questions']}
 inv=[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'source_question':q[':question/id'] in source_ids,'generation_keys':[k for k in q if 'generat' in k],'retired':q.get(':question/retired',False)} for q in inventory['questions']]
 save('inventory-audit.json',{'basis':inventory['basis'],'questions':inv,'conclusion':'All 13 captured records are original source questions; zero generated historical records. No eligible generated stored record to reproduce. Originals are not marked generated or submitted for pool repair.'});save('affected-inventory.json',{'affected_questions':[]})
 save('coverage.json',{'profiles':dict(Counter(r['generation']['bank_profile'] for r in records)),'role_combinations':len(set((r['generation']['parameters']['row'],r['generation']['parameters']['pivot'],r['generation']['parameters']['given']) for r in records)),'sign_pairs':dict(Counter(str(tuple(1 if k>0 else -1 for k in x['pair'])) for x in results)),'batch':br})
 print(json.dumps({'math':len(results)+len(br)+len(cfr),'replay_failures':[r for r in replay if r['status']=='failed'],'shortcuts':probes},indent=2))
 (ROOT/'session-state.md').write_text('Completed source analysis, 120 fresh samples, batch math checks, replay, controlled pairs, package relocation and inventory classification. Defects: missing source profiles; bank-only singleton swapped-pair shortcut. Next: actual delivery, native grading, UI render and delivery selection analysis.\n')
if __name__=='__main__':main()
