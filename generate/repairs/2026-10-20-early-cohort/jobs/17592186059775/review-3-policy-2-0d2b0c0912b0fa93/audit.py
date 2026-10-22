import sys
sys.dont_write_bytecode=True
import json,re,subprocess,importlib.util,hashlib,pathlib,shutil,os,platform,copy
import sympy as S
E=pathlib.Path(__file__).resolve().parent; J=E.parent; W=J/'workspace'; PY='/home/jake/Developer/Course_Academy/.venv/bin/python'
def save(n,x): (E/n).write_text(json.dumps(x,indent=2,default=str)+'\n')
def loadmod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
sys.path.insert(0,str(W));g=loadmod('current',W/'17592186059775.py')
pat=re.compile(r'\\begin\{(?:array|bmatrix)\}(?:\{cc\|c\})?(.*?)\\end\{(?:array|bmatrix)\}',re.S)
num=r'-?(?:\\frac\{-?\d+\}\{\d+\}|\d+)'
def rat(x):
 x=x.strip();sgn=-1 if x.startswith('-') else 1
 if x.startswith('-'): x=x[1:]
 m=re.fullmatch(r'\\frac\{(-?\d+)\}\{(\d+)\}',x)
 return sgn*(S.Rational(*map(int,m.groups())) if m else S.Rational(x))
def mats(t):return [S.Matrix([[rat(c) for c in row.split('&')] for row in m.split(r'\\')]) for m in pat.findall(t)]
def xy(t):return [rat(z) for z in re.findall(r'\b[xy]\s*=\s*('+num+')',t)]
def q(r):return r['question']
def f(r):return q(r)[':question/answer-fields'][0]
def key(r):return next(a for a in f(r)[':answer-field/choices'] if a[':answer/id']==f(r)[':answer-field/correct'][1])
def rank(r):
 vals=[mats(a[':answer/value'])[0][1,2] for a in f(r)[':answer-field/choices']]
 return sorted(vals).index(mats(key(r)[':answer/value'])[0][1,2])
def normalize(m):
 first=m[0,:]/m[0,0]; second=m[1,:]-m[1,0]*first;second/=second[0,1]
 return first.col_join(second)
def verify(r):
 qq=q(r);a=mats(qq[':question/problem'])[0];ref=normalize(a);correct=[]
 for ch in f(r)[':answer-field/choices']:
  cm=mats(ch[':answer/value'])[0]; pair=xy(ch[':answer/value'])
  good=cm==ref
  if pair:good=good and len(pair)==2 and a[:,:2]*S.Matrix(pair)==a[:,2]
  if good:correct.append(ch[':answer/id'])
 assert correct==[key(r)[':answer/id']],(qq[':question/id'],correct)
 stages=mats(qq[':question/worked-solution']);assert stages[0]==a and stages[-1]==ref
 for z in stages:assert z[:,:2].det()!=0 and z.rref()[0]==a.rref()[0]
 # Check every explicit intermediate matrix is the next forward-elimination stage.
 expected=[a];z=a.copy()
 if z[0,0]!=1:z[0,:]=z[0,:]/z[0,0];expected.append(z.copy())
 z[1,:]=z[1,:]-z[1,0]*z[0,:];expected.append(z.copy())
 if z[1,1]!=1:z[1,:]=z[1,:]/z[1,1];expected.append(z.copy())
 # Some source traces omit already-normalized operations; no invented stages.
 assert stages==expected,(r['generation']['parameters'],'stages',stages,expected)
 tail=xy(qq[':question/worked-solution'])
 if 'and then solve' in qq[':question/problem']:
  assert tail[-2:]==[ref[0,2]-ref[0,1]*ref[1,2],ref[1,2]],tail
 return {'id':qq[':question/id'],'parameters':r['generation']['parameters'],'rank':rank(r),'answer':str(ref),'passed':True}
manifest=json.load(open(W/'package.json'));before={n:hashlib.sha256((W/n).read_bytes()).hexdigest() for n in manifest['files']};save('package-before.json',before)
# Exact complete source banks; missing source data is recorded separately.
src=json.load(open(J/'source/source.json'))['material']['kp'][':knowledge-point/questions'];replays=[];sr=[]
for old in src:
 sid=old[':question/math-academy-id']
 if sid not in g.CASES:
  sr.append({'id':old[':question/id'],'result':'Unsupported incomplete capture: no key, worked solution or rating; no data fabricated.'});continue
 r=g.source_replay(sid);replays.append(r)
 assert q(r)[':question/problem']==old[':question/problem']
 assert q(r)[':question/worked-solution']==old[':question/worked-solution']
 assert [a[':answer/value'] for a in f(r)[':answer-field/choices']]==[a[':answer/value'] for a in old[':question/answer-fields'][0][':answer-field/choices']]
 assert key(r)[':answer/value']==old[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
 a=mats(q(r)[':question/problem'])[0]
 equivalents=[i for i,c in enumerate(f(r)[':answer-field/choices']) if mats(c[':answer/value'])[0].rref()[0]==a.rref()[0]]
 sr.append({'id':old[':question/id'],'replay':'exact prompt, complete bank, key and solution','equivalent_option_indices':equivalents,'known_correction':sid=='q-10512'})
save('source-replays.json',replays);save('source-replay-results.json',sr)
records=[];pairs=[];renders=[]
for i,sid in enumerate(g.CASES):
 band=g.level(sid); ks=[p[1] for p in g.domain(sid)]
 bank=[g.generate(band,seed=81731+i,parameters=[sid,max(ks),t]) for t in range(5)]
 records+=bank
 assert len({tuple(a[':answer/value'] for a in f(r)[':answer-field/choices']) for r in bank})==1
 assert len({str(mats(q(r)[':question/problem'])[0][0,:]) for r in bank})==1
 assert len({key(r)[':answer/value'] for r in bank})==5
 perm=g.generate(band,seed=91557+i,parameters=[sid,max(ks),2]);records.append(perm)
 assert q(perm)[':question/problem']==q(bank[2])[':question/problem'] and key(perm)[':answer/value']==key(bank[2])[':answer/value']
 small=g.generate(band,seed=26391+i,parameters=[sid,min(ks),4]);records.append(small)
 pairs.append({'template':sid,'relevant_before':q(bank[0])[':question/id'],'relevant_after':q(bank[4])[':question/id'],'all_ranks':[rank(r) for r in bank], 'irrelevant_permutation':q(perm)[':question/id'],'response_preserved':True})
 if band=='easy':renders+=bank[:1]+bank[-1:]
# Distinct deterministic seeds normal samples rather than author-selected cases.
for band in ['easy','moderate']:
 for seed in [982451653,107,31073]:records.append(g.generate(band,seed))
batch=json.load(open(J/'samples.json'));save('runner-batch.json',batch);records+=batch
save('independent-records.json',records)
results=[verify(r) for r in records];save('math-results.json',results);save('counterfactual-results.json',pairs)
grades=[]
for r in records:
 grades.append({'label':str(r['generation']['parameters']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r)[':answer/id'] else 'rejected','purpose':'All five choices independently checked by parsed exact matrix and optional solution'} for a in f(r)[':answer-field/choices']]})
save('grader-input.json',grades)
renders+=[records[-1],records[2],records[5]];save('render-records.json',renders)
# Isolated runtime closure and exact original failures. Never execute author tests in package.
dest=E/'relocated';dest.mkdir(exist_ok=True)
for n in manifest['files']:
 p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/n,p)
cli=[]
for band,cnt,seed in [('easy',5,0),('easy',0,731),('easy',1,731),('moderate',5,982451653),('easy',65,0),('hard',1,0)]:
 cmd=[PY,'-E','-s','-B',str(dest/manifest['entrypoint']),'--format','json','--difficulty',band,'--count',str(cnt),'--seed',str(seed)]
 p=subprocess.run(cmd,cwd=dest,capture_output=True,text=True,env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'runtime-assets')})
 if band=='hard' or cnt==65:assert p.returncode!=0
 else:
  value=json.loads(p.stdout);assert isinstance(value,list) and len(value)==cnt
  assert subprocess.run(cmd,cwd=dest,capture_output=True,text=True).stdout==p.stdout
  save('cli-'+band+'-'+str(cnt)+'.json',value)
 cli.append({'command':cmd,'returncode':p.returncode,'count':None if p.returncode else len(value),'stderr':p.stderr[-1500:]})
# Show strict decoder rejects the actual pre-fix retained output, then accepts current.
oldfile=W/'evidence/before-cli.json';oldout=json.load(open(oldfile));
def decode(v):return v.get('records',v.get('questions',[v] if 'question' in v else None)) if isinstance(v,dict) else v
assert decode(oldout) is None;save('retained-count-counterexample.json',oldout)
cli.append({'retained_failure':'before-cli.json decodes to None (requested five)','current':'raw arrays above decode to exact counts','preflight':json.load(open(J/'repair-preflight.json')),'retained_findings':json.load(open(J/'repair-history.json'))['findings'],'history_events':json.load(open(J/'repair-history.json'))['events']})
legacy=loadmod('legacy',W/'evidence/legacy/17592186059775.py')
p=subprocess.run([PY,'-B',str(W/'evidence/legacy/17592186059775.py'),'--format','json'],capture_output=True,text=True)
assert p.returncode!=0 and 'unrecognized arguments: --format json' in p.stderr
cli.append({'original_format_failure_returncode':p.returncode,'stderr':p.stderr})
save('packaging-results.json',{'versions':{'python':platform.python_version(),'sympy':S.__version__},'manifest_dependencies':manifest['dependencies'],'cli':cli,'package_unchanged':before=={n:hashlib.sha256((W/n).read_bytes()).hexdigest() for n in manifest['files']}})
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':S.__version__}}
# Reproduce stored generated records with original archived metadata; originals remain source-only.
inv=json.load(open(J/'source/inventory.json'));arch=json.load(open(W/'17592186059775/reference/replenishment/basis-2480/generated.json'));affected=[];storedrecords=[];invr=[]
for stored in inv['questions']:
 if ':question/math-academy-id' in stored:continue
 saved=next(r for r in arch if q(r)[':question/id']==stored[':question/id']);meta=saved['generation'];sid,k=meta['parameters']
 rr=legacy.generate(stored[':question/difficulty'][':db/ident'].split('/')[-1],meta['seed'],sid,meta['parameters']);assert rr==saved
 for field in [':question/problem',':question/worked-solution']:assert q(rr)[field]==stored[field]
 sf=stored[':question/answer-fields'][0]
 for a in f(rr)[':answer-field/choices']:
  sa=next(x for x in sf[':answer-field/choices'] if x[':answer/id']==a[':answer/id'])
  assert mats(a[':answer/value'])==mats(sa[':answer/value']) and xy(a[':answer/value'])==xy(sa[':answer/value'])
  a[':answer/value']=sa[':answer/value']
 assert f(rr)[':answer-field/correct'][1]==sf[':answer-field/correct'][':answer/id']
 if 'and then solve' in stored[':question/problem']:
  valid=[a[':answer/id'] for a in f(rr)[':answer-field/choices'] if (lambda m:m[:,:2]*S.Matrix(xy(a[':answer/value']))==m[:,2])(mats(a[':answer/value'])[0])]
  assert valid==[key(rr)[':answer/id']];defect='Only keyed matrix/solution pair is internally consistent; ignore the input system.'
 else:
  ranks=[rank(legacy.generate(legacy.level(sid),meta['seed'],sid,p)) for p in legacy.domain(sid)];assert set(ranks)=={2};defect='Always choose median lower-right entry within this legacy profile; no input-system reasoning required.'
 storedrecords.append(rr);affected.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'finding':defect,'reproduction':f'{PY} -B audit.py # legacy.generate({legacy.level(sid)!r}, {meta["seed"]}, {sid!r}, {meta["parameters"]!r})','evidence_path':'generated-records.json'})
 invr.append({'id':stored[':question/id'],'metadata':meta,'defect':defect})
save('generated-records.json',storedrecords);save('affected-inventory.json',{'affected_questions':affected});save('inventory-results.json',{'basis':inv['basis'],'originals_not_marked_generated':12,'all_stored_generated_tested':invr,'limits':'Historical weaknesses reproduced; current authored banks separately checked. Inventory captured, no live DB.'})
(E/'session-state.md').write_text('Completed independent source reconstruction, complete-bank replay, 81 current mathematical checks, target/permutation counterfactuals, isolated CLI, historical failures and all three stored generated reproductions. Await delivery, native grading, actual UI and final decision report. Package unchanged.\n')
print(json.dumps({'math_cases':len(results),'sources':len(replays),'native_cases':len(grades),'render_cases':len(renders),'affected_inventory':len(affected)}))
