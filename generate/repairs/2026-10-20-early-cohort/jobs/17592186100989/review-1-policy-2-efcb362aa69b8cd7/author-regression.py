"""Current-package regression for ad7e55b230ca82a0d63b; no DB or service access."""
import collections, copy, importlib.util, json, os, pathlib, platform, re, subprocess, sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100989/workspace')
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
OUT=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186100989/review-1-policy-2-efcb362aa69b8cd7/author-checks'); OUT.mkdir(exist_ok=True)
SOURCE=ROOT.parent/'source/source.json'; INVENTORY=ROOT.parent/'source/inventory.json'
ENTRY=ROOT/'17592186100989.py'; COMMANDS=[]
spec=importlib.util.spec_from_file_location('candidate',ENTRY);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj):
 (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
def read(path):return json.loads(path.read_text())
def run(args,output=None):
 args=list(map(str,args)); p=subprocess.run(args,text=True,capture_output=True,cwd=ROOT,env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(OUT/'assets')})
 COMMANDS.append({'command':args,'exit_code':p.returncode,'stderr':p.stderr})
 save('commands.json',COMMANDS)
 if output:(OUT/output).write_text(p.stdout)
 assert p.returncode==0, (args,p.stdout[-2000:],p.stderr[-2000:])
 return p.stdout

def parsed(r):
 q=r.get('question',r); s=q[':question/problem']
 m=re.search(r'\\begin\{(?:bmatrix|aligned)\}(.*?)\\end\{(?:bmatrix|aligned)\}',s,re.S)
 a=[[v.strip() for v in row.split('&')] for row in m[1].split('\\\\')]
 i,j=map(int,re.search(r'_\{(\d)(\d)\}',s).groups())
 return a,i,j

def expected(r):
 a,i,j=parsed(r);return a[i-1][j-1] if i<=len(a) and j<=len(a) else 'No such entry'
def field(r):return r.get('question',r)[':question/answer-fields'][0]
def ident(v):return v.get(':db/ident') if isinstance(v,dict) else v

def key(r):
 f=field(r);c=f[':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid)
def bank(r):return sorted(a[':answer/value'] for a in field(r)[':answer-field/choices'])
def norm(s):return re.sub(r'\s+','',s.replace(r'[\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}'))

def inspect(rs,label,require_cases=True):
 groups=collections.defaultdict(list); failures=[];semantics=set()
 for r in rs:
  q=r.get('question',r);a,i,j=parsed(r);n=len(a);want=expected(r);f=field(r);sol=q[':question/worked-solution']
  checks={'key':key(r)==want,'square':all(len(row)==n for row in a),'unique_bank':len(bank(r))==len(set(bank(r))),
   'solution_indices':all(t==f'{i}{j}' for t in re.findall(r'_\{(\d\d)\}',sol)),
   'solution_row_column':re.search(rf'\${i}\$(?:st|nd|rd|th) row and \${j}\$(?:st|nd|rd|th) column',sol) is not None}
  if want=='No such entry':
   axis='row' if i>n else 'column';index=i if i>n else j
   checks['absence_explanation']=f'${n}\\times {n}$' in sol and re.search(rf'does not have the \${index}\$(?:st|nd|rd|th) {axis}',sol) is not None
  else:
   checks['value_explanation']=re.search(rf'_\{{{i}{j}\}}='+re.escape(want)+r'\.\$',sol) is not None
   checks['matrix_explanation']=parsed(q|{':question/problem':sol})[0]==a
  if not all(checks.values()):failures.append({'id':q[':question/id'],'checks':checks})
  semantics.add((n,i,j,want))
  if ident(f[':answer-field/type']).endswith('/radio'):
   layout='display' if '$$' in q[':question/problem'] else 'inline'
   name=re.search(r'matrix \$([A-Z])\$',q[':question/problem'])[1]
   pos=next(k for k,c in enumerate(f[':answer-field/choices']) if c[':answer/value']==want)
   groups[(n,layout,len(bank(r)))].append((want=='No such entry',pos,name,want,(i,j)))
 reports=[]
 for group,rows in groups.items():
  outcomes={x[0] for x in rows}
  if require_cases and outcomes!={True,False}:failures.append({'group':group,'missing_case':list(outcomes)})
  positions=collections.Counter(x[1] for x in rows)
  reports.append({'group':group,'count':len(rows),'missing':sum(x[0] for x in rows),'existing':sum(not x[0] for x in rows),'position_counts':dict(positions),'best_fixed_position_success':max(positions.values()),'random_choice_baseline':0.2,'target_coordinates':sorted(set(x[4] for x in rows)), 'names':sorted(set(x[2] for x in rows))})
 report={'records':len(rs),'semantic_instances':len(semantics),'groups':reports,'failures':failures}
 save(label+'.json',report); assert not failures,report
 return report

def delivery(name):
 run([sys.executable,REPO/'generate/pipeline/check_delivery.py','--input',OUT/(name+'.json'),'--source',SOURCE,'--inventory',INVENTORY,'--difficulty','easy','--output',OUT/('delivery-'+name),'--asset-root',OUT/'assets','--math-root','/media/jake/SSD/EDB/math'])
 return read(OUT/('delivery-'+name)/'accepted.json')

# Exact previously failing public-API counterfactual, before any broad check.
run([sys.executable,ROOT/'reproduce_restriction.py',ENTRY], 'boundary-result.txt')
# Actual current CLI, exact retained seed/count, never the historical samples file.
cmd=[sys.executable,ENTRY,'--difficulty','easy','--count','5','--seed','3302362091','--format','json']
run(cmd,'prospective-batch.json');batch=read(OUT/'prospective-batch.json')
assert json.loads(run(cmd))==batch,'Deterministic replay failed'
for name,rs in [('prospective-batch',batch),('delivered-batch',delivery('prospective-batch'))]:
 inspect(rs,name+'-coverage');save(name+'.json',rs)
 run([sys.executable,ROOT/'shortcut_regression.py','--candidate-records',OUT/(name+'.json'),'--output',OUT/(name+'-shortcut.json')])
# Small deterministic CLI sample and several finite batches, independent of reported seed.
run([sys.executable,ENTRY,'--difficulty','easy','--count','48','--seed','11','--format','json'],'sample.json')
sample=read(OUT/'sample.json');inspect(sample,'sample-coverage')
assert 'all_four' in {r['generation']['bank_profile'] for r in sample},'Need nonvacuous 2x2 sample'
assert {r['generation']['bank_profile'] for r in sample}=={'all_four','transpose_neighbors','right_up_left','local_neighbors','inline_diagonal'}
accepted=delivery('sample');inspect(accepted,'delivered-sample-coverage')
for name,rs in [('sample',sample),('delivered-sample',accepted)]:
 save(name+'.json',rs); run([sys.executable,ROOT/'shortcut_regression.py','--candidate-records',OUT/(name+'.json'),'--output',OUT/(name+'-shortcut.json')])
finite=[]
for seed in range(6):
 for count in (2,3,5):
  rs=json.loads(run([sys.executable,ENTRY,'--difficulty','easy','--count',str(count),'--seed',str(seed),'--format','json']))
  inspect(rs,f'finite-{seed}-{count}');finite.extend(rs)
save('finite-batches.json',finite)
# Source replay with all complete banks, observed flags and noted source omissions.
sources=read(SOURCE)['material']['kp'][':knowledge-point/questions'];replay=[];results=[]
for q in sources:
 a,i,j=parsed(q);name=re.search(r'matrix \$([A-Z])\$',q[':question/problem'])[1];sid=q[':question/math-academy-id']
 p={'name':name,'matrix':a,'i':i,'j':j}
 if sid=='q-13490':p['opaque']=['5','4']
 raw=g.generate_easy(seed=47,profile='raw_'+sid,parameters=p)
 r=raw if sid=='q-13490' else g.generate_easy(seed=47,profile=sid,parameters=p)
 checks={'prompt':norm(q[':question/problem'])==norm(r['question'][':question/problem']),'complete_bank':bank(q)==bank(r),'key':key(r)==expected(q)}
 if ':answer-field/correct' in field(q):checks['observed_key']=key(r)==key(q)
 if ':question/worked-solution' in q:checks['solution']=norm(q[':question/worked-solution'])==norm(r['question'][':question/worked-solution'])
 if sid=='q-13506':checks['raw_omissions']=all(k not in raw['question'] for k in (':question/difficulty',':question/worked-solution')) and ':answer-field/correct' not in field(raw)
 if sid=='q-125593':checks['historical_name_preserved']='E=' in raw['question'][':question/worked-solution']
 assert all(checks.values()),(sid,checks)
 results.append({'source_id':q[':question/id'],'profile':sid,'choices_matched':len(bank(q)),'checks':checks});replay.append(r)
save('source-replay.json',results);save('source-replay-records.json',replay)
# Controlled witnesses for every changed bank and applicable size. Hold all displayed
# data and alternatives constant; alter only row/column boundary, or another target.
controlled=[];cf=[]
profiles={'all_four':[(2,1,2),(2,2,1)],'transpose_neighbors':[(3,3,2),(4,3,2)],'right_up_left':[(3,2,2),(4,3,2)],'local_neighbors':[(3,2,2),(4,3,2)],'inline_diagonal':[(3,1,1),(4,1,1)]}
for profile,cases in profiles.items():
 for n,i,j in cases:
  a=[[str(row*n+col-n*n//2) for col in range(n)] for row in range(n)]
  p={'name':'B','matrix':a,'i':i,'j':j}
  base=g.generate_easy(seed=11,profile=profile,parameters=p);controlled.append(base)
  for axis in ('i','j'):
   altered=p|{axis:n+1}
   if profile!='all_four':altered['bank_anchor']=[i,j]
   missing=g.generate_easy(seed=11,profile=profile,parameters=altered)
   assert bank(missing)==bank(base) and expected(base)!='No such entry' and key(missing)=='No such entry'
   controlled.append(missing);cf.append({'profile':profile,'n':n,'axis':axis,'old_key':key(base),'new_key':key(missing),'same_bank':True})
  # Rename preserves the response, relevant cell edits change it (all other values fixed).
  renamed=g.generate_easy(seed=17,profile=profile,parameters=p|{'name':'R'})
  assert key(renamed)==key(base);controlled.append(renamed)
  changed=copy.deepcopy(p);changed['matrix'][i-1][j-1]=r'\sqrt{2}'
  r=g.generate_easy(seed=11,profile=profile,parameters=changed);assert key(r)==r'\sqrt{2}';controlled.append(r)
  # A non-target offered entry may change; it must not change the key.
  changed=copy.deepcopy(p);rr,cc=next((rr,cc) for rr in range(n) for cc in range(n) if (rr+1,cc+1)!=(i,j));changed['matrix'][rr][cc]=r'\sqrt{3}'
  r=g.generate_easy(seed=11,profile=profile,parameters=changed);assert key(r)==key(base);controlled.append(r)
p={'name':'B','matrix':[['1','-3'],['0','5']],'i':1,'j':1}
for i,j in ((1,1),(1,2),(2,1),(2,2)):
 r=g.generate_easy(seed=11,profile='all_four',parameters=p|{'i':i,'j':j});controlled.append(r);assert key(r)==p['matrix'][i-1][j-1]
# Blank equivalents and boundaries remain meaningful.
rad=g.generate_easy(seed=19,profile='blank',parameters={'name':'G','matrix':[['0',r'\sqrt{2}'],['-1','2']],'i':1,'j':2});controlled.append(rad)
for change in ({'i':0},{'j':-1},{'matrix':[['1','2','3'],['4','5','6']]},{'i':3}):
 try:g.generate_easy(seed=11,profile='blank',parameters=p|change)
 except ValueError:pass
 else:raise AssertionError(('Invalid blank accepted',change))
save('counterfactuals.json',cf);save('controlled-records.json',controlled);inspect(controlled,'controlled-math',False)
# Every sampled radio size/layout/name must defeat constant absence and position cues.
for suffix,rs in [('raw',sample),('delivered',accepted)]:
 groups=collections.defaultdict(list)
 for r in rs:
  q=r.get('question',r);a,i,j=parsed(r);f=field(r);name=re.search(r'matrix \$([A-Z])\$',q[':question/problem'])[1]
  group=(len(a),'display' if '$$' in q[':question/problem'] else 'inline',name)
  groups[group].append((expected(r)=='No such entry',next(k for k,c in enumerate(f[':answer-field/choices']) if c[':answer/value']==key(r))))
 report=[]
 for group,rows in groups.items():
  assert {r[0] for r in rows}=={True,False},('name cue',group,rows)
  assert len({r[1] for r in rows})>1,('fixed position cue',group,rows)
  report.append({'group':group,'count':len(rows),'missing':sum(r[0] for r in rows),'positions':sorted(set(r[1] for r in rows))})
 save('conditional-cues-'+suffix+'.json',report)
# Native engine: expected answers come solely from displayed matrix/indices.
cases=[]
for idx,r in enumerate(batch+controlled+replay):
 f=field(r);e=expected(r)
 if ident(f[':answer-field/type']).endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==e else 'rejected','purpose':'independent prompt lookup, including stale answers and missing-choice distractors'} for a in f[':answer-field/choices']]
 else:
  forms=[(e,True),('sqrt(2)',True),('2^(1/2)',True),('2',False)] if e==r'\sqrt{2}' else [(e,True),(f'{int(e)*2}/2',True),(str(int(e)+1),False)]
  checks=[{'submitted':v,'expected':'accepted' if ok else 'rejected','purpose':'equivalent scalar or wrong entry'} for v,ok in forms]
 cases.append({'label':f'case-{idx}','record':r,'checks':checks})
save('grader-input.json',cases)
run([REPO/'generate/runs/current/check-engine',OUT/'grader-input.json',OUT/'grader-report.json'],'grader-stdout.txt')
# Inventory: only original source records in the capture; no inferred generated repairs.
inv=read(INVENTORY);source_ids={q[':question/id'] for q in sources}
assert all(q[':question/id'] in source_ids for q in inv['questions'])
assert not any(':question/generation' in q for q in inv['questions'])
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-analysis.json',{'basis':inv['basis'],'total':len(inv['questions']),'generated_records':0,'source_ids':[q[':question/id'] for q in inv['questions']],'conclusion':'Verified six captured records are original source questions. No stored generated records to reproduce; not a claim about live database state. Original unrated q-13506 lacks its correct reference and is not an eligible practice record.','selection_limit':'Captured fresh pool only. Runtime history and policy weights can remove/reweight candidates. No guarantee about an arbitrary learner-specific subset; no live DB access or publication.'})
# Runtime relocation uses only manifest files and explicit output directory.
import tempfile, shutil
with tempfile.TemporaryDirectory(dir=OUT) as d:
 dest=pathlib.Path(d)
 manifest=read(ROOT/'package.json')
 for file in manifest['files']:
  target=dest/file;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/file,target)
 relocated=json.loads(run([sys.executable,dest/manifest['entrypoint'],'--difficulty','easy','--count','5','--seed','3302362091','--format','json']))
 assert relocated==batch
 assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':g.sp.__version__}}
save('packaging.json',{'relocation':True,'deterministic_cli':True,'runtime_files':manifest['files'],'dependencies':manifest['dependencies']})
# Render exact original defect and its repaired counterpart, plus new larger missing case.
render=[g.generate_easy(seed=11,profile='all_four',parameters=p|{'i':3,'j':2}),g.generate_easy(seed=11,profile='all_four',parameters=p|{'i':2,'j':2})]
render.append(next(r for r in controlled if r['generation']['bank_profile']=='inline_diagonal' and expected(r)=='No such entry'))
save('render-records.json',render)
save('validation-summary.json',{'status':'passed','finding':'ad7e55b230ca82a0d63b','batch_count':len(batch),'batch_accepted':5,'sample_count':len(sample),'sample_accepted':len(accepted),'source_cases':len(replay),'source_choices_matched':sum(x['choices_matched'] for x in results),'controlled_records':len(controlled),'finite_batch_checks':18,'grading_cases':len(cases),'rendering':'input ready; run shared renderer and inspect screenshots separately'})
print(json.dumps(read(OUT/'validation-summary.json')))
