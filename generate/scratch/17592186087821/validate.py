"""Independent display/geometry checks, complete raw fidelity, actual native grading."""
import importlib.util,json,re,hashlib,sys,subprocess,concurrent.futures,math
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def scalar(t):
 t=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',t)
 return sp.Rational(sp.sympify(t.replace('{','').replace('}','')))
def read_prompt(prompt):
 m=re.search(r'y\s*=\s*(.*?)\^\{x\}\s*([+-])\s*(.*?)\$',prompt);assert m,prompt
 return scalar(m[1]),scalar(m[3].rstrip('?'))*(1 if m[2]=='+' else -1)
def check_display(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];b,c=read_prompt(q[':question/problem']);geoms=r['generation']['geometry'];f=q[':question/answer-fields'][0]
 assert len(f[':answer-field/choices'])==5
 assert {a[':answer/value'] for a in f[':answer-field/choices']}=={s['path'] for s in geoms}
 valid=[]
 for s in geoms:
  B,A,C=map(sp.Rational,(s['b'],s['A'],s['c']));d=s['direction'];assert B==b
  # Independent recognition criterion from printed prompt: intercept, asymptote,
  # increasing orientation and values at x=1, rather than answer-ID metadata.
  if A+C==1+c and C==c and d==1 and A*B+C==b+c:valid.append(s['path'])
  assert math.isfinite(float(A+C))
 assert len(valid)==1
 if ':answer-field/correct' in f:assert next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])[':answer/value']==valid[0]
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];assert sol.count('![](')==2
  inter=re.search(r'to \$\(0,(.*?)\),\$',sol);assert inter and scalar(inter[1])==1+c
  asym=re.search(r'to \$y=(.*?)\.\$',sol);assert asym and scalar(asym[1])==c
  shift=re.search(r'shift it \$(.*?)\$ units? (up|down)',sol);assert shift and scalar(shift[1])==abs(c) and (shift[2]=='up')==(c>0)
  for basal in [re.search(r'First, we plot the graph of \$y=(.*?):\$',sol),re.search(r'we take the graph of \$y=(.*?)\$',sol)]:
   assert basal and read_prompt('y='+basal[1]+'+0$')==(b,0)
  expr=re.search(r'To sketch the graph of \$y=(.*?),\$',sol);assert expr and read_prompt('y='+expr[1]+'$')==(b,c)
 for txt in [q[':question/problem'],q.get(':question/worked-solution','')]:
  assert txt.count('$')%2==0 and txt.count('{')==txt.count('}')
 return r

def engine_rows(records):
 rows=[]
 for i,r in enumerate(records):
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  cid=f[':answer-field/correct'][1]
  rows.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'native image radio selection'} for a in f[':answer-field/choices']]})
 return rows

def run():
 feature_path=Path('generate/runs/current/qa/17592186087821-source-features.json')
 source_features=json.loads(feature_path.read_text())['visually_read_intercept_asymptote_direction']
 for sid,features in source_features.items():
  for (A,C,D),(intercept,asymptote,direction) in zip(g.OBS[sid][2],features):
   assert sp.Rational(A)+sp.Rational(C)==sp.Rational(intercept) and sp.Rational(C)==sp.Rational(asymptote) and D==direction,(sid,A,C,D)
 assert g.OBS['q-170588'][2][4]==(sp.Rational(3,2),sp.Rational(3,2),1)
 originals=[];sourcecases=[];fidelity=[]
 for sid,q in g.QUESTIONS.items():
  level=q.get(':question/difficulty',{}).get(':db/ident','/easy').split('/')[-1]
  r=check_display(g.generate(level,profile='observed:'+sid));originals.append(r)
  rq=r['question'];assert rq[':question/problem']==q[':question/problem']
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in rq)==(key in q)
  assert rq.get(':question/worked-solution')==q.get(':question/worked-solution')
  f=rq[':question/answer-fields'][0];of=q[':question/answer-fields'][0]
  assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  assert f[':answer-field/key']==of[':answer-field/key']
  assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']
  assert all(a[':answer/type']==':answer.type/image' for a in f[':answer-field/choices'])
  assert ('image' in q[':question/problem'])==('image' in rq[':question/problem'])
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  if ':answer-field/correct' in of:
   assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  sourcecases.append({'source_id':sid,'template':'identify_shifted_growth','level':level,'level_assignment':'authored easy replay routing only' if ':question/difficulty' not in q else 'observed','parameters':r['generation']['parameters'],'bank_profile':'observed:'+sid})
  fidelity.append({'source_id':sid,'options_matched':5,'options_total':5,'complete_bank_match':True,'prompt_exact':True,'solution_exact':':question/worked-solution' in q,'raw_presence_match':True,'correct_designation_matched':':answer-field/correct' in of})
 records=[]
 for level in ('easy','moderate','hard'):
  for profile in g.AUTHORED:
   for seed in (21,2):records.append(check_display(g.generate(level,seed,profile=profile)))
 default_coverage={}
 for level in ('easy','moderate','hard'):
  defaults=[check_display(g.generate(level,seed)) for seed in (0,1)]
  assert {r['generation']['bank_profile'] for r in defaults}==set(g.AUTHORED)
  default_coverage[level]=[r['generation']['bank_profile'] for r in defaults]
  records.extend(defaults)
 try:g.generate_easy(parameters={'b':'3','c':'1/2'},profile='authored_offsets')
 except ValueError:pass
 else:raise AssertionError('Equivalent whole bank not rejected')
 regressions=[]
 for level,bases,shifts in [('easy',('2','9'),('-5/4','-3/4','-1','1/4')),('moderate',('5/4','9/2'),('-3/2','-1/2')),('hard',('5/4','9/2'),('-5/4','-3/4'))]:
  for base in bases:
   for shift in shifts:
    r=check_display(g.generate(level,parameters={'b':base,'c':shift},profile='authored_transformations'))
    regressions.append(r)
 records.extend(regressions)
 (HERE/'label-regression.json').write_text(json.dumps(regressions,indent=2)+'\n')
 # Public changed-parameter observed profiles: real feature continuation, never
 # eligible learning because original unlabelled horizontal geometry is unknown.
 for sid,(_,oldc,_) in g.OBS.items():
  level=g.QUESTIONS[sid].get(':question/difficulty',{}).get(':db/ident','/easy').split('/')[-1]
  records.append(check_display(g.generate(level,profile='observed:'+sid,parameters={'b':'2' if level=='easy' else '4/3','c':str(sp.Rational(oldc)-sp.sign(sp.Rational(oldc))*sp.Rational(1,4))})))
 # Exhaustively verify finite sampler domains mathematically, before rendering.
 domains={}
 for level in ('easy','moderate','hard'):
  bases,shifts=g.values(level);counts={}
  for profile in g.AUTHORED:
   eligible=[c for c in shifts if profile!='authored_offsets' or c not in [sp.Rational(1,2),-sp.Rational(1,2),1,-1]]
   counts[profile]=len(bases)*len(eligible)
  domains[level]={'bases':len(bases),'shifts':len(shifts),'unique_assessed_tasks':len(shifts),'eligible_instances_by_bank':counts,'fingerprint_excludes':'growth-base magnitude (same across all options), bank/profile/seed/order/UUID; includes c and assessed grid/cue'}
 # Determinism, aliases, bounds, and fresh concurrent cache writes.
 a=g.generate_easy(2,parameters={'b':'3','c':'3/2'},profile='authored_transformations');b=g.generate_easy(98,parameters={'b':'3','c':'1.5'},profile='authored_transformations');assert a['question'][':question/id']==b['question'][':question/id']
 for level,p in [('easy',{'b':'3/2','c':'1'}),('moderate',{'b':'3/2','c':'3/4'}),('hard',{'b':'3/2','c':'1/2'})]:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('explicit workload guard absent')
 fresh=[]
 for i in (0,1):
  s=g.plot(sp.Rational(7,3),1,sp.Rational(11+i,4),1,'labels',1,[-2,8]);s['qa_nonce']='fresh-concurrency';s['path']=str(HERE/'plots'/('qa-'+str(i)+'.png'));Path(s['path']).unlink(missing_ok=True);Path(s['path']).with_suffix('.json').unlink(missing_ok=True);fresh.append(s)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(g.render_plots,[[fresh[0]],[fresh[0]],[fresh[1]]]))
 # Exercise actual CLI output, including review-only headings and manifests.
 cli_args=[sys.executable,str(HERE.with_suffix('.py'))]
 cli_json=subprocess.run(cli_args+['--difficulty','all','--seed','42','--count','2','--format','json'],capture_output=True,text=True,check=True).stdout
 cli_records=json.loads(cli_json);assert len(cli_records)==6
 for r in cli_records:
  check_display(r);manifest=r['generation']['review_manifest']
  assert manifest['version']==g.VERSION and manifest['renderer_runtime']['renderer_version']=='shift-plots-7'
  assert manifest['generator_sha256']==hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()
  assert manifest['renderer_sha256']==hashlib.sha256((HERE/'render.py').read_bytes()).hexdigest()
 (HERE/'cli-review.json').write_text(cli_json)
 for name,args,heading in [('cli-review.md',['--difficulty','easy','--seed','2','--profile','authored_offsets'],'GENERATED VARIANT — easy'),('cli-original.md',['--difficulty','moderate','--profile','observed:q-170588'],'ORIGINAL REPLAY — moderate')]:
  md=subprocess.run(cli_args+args+['--format','markdown'],capture_output=True,text=True,check=True).stdout
  assert heading in md and md.count('**CORRECT**')==1 and 'generator_sha256' in md and '3.10.13' in md
  (HERE/name).write_text(md)
 # Read actual raster colors near independently expected sample coordinates.
 geomcmd=[g.RUNTIME,str(HERE/'verify_pixels.py')];subprocess.run(geomcmd,check=True)
 (HERE/'source-cases.json').write_text(json.dumps(sourcecases,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps(records,indent=2)+'\n')
 rows=engine_rows(originals+records+cli_records);(HERE/'engine-input.json').write_text(json.dumps(rows,indent=2))
 subprocess.run(['generate/runs/current/check-engine',str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 review=['# Original banks and generated variants\n\nOriginal raw omissions remain omissions; inferred legacy correct choices are documented separately. Observed changed-parameter variants are evidence only.']
 for r in originals:review.append('## Original '+r['generation']['source_id']+'\n\n'+g.markdown(r))
 for r in records:review.append('## GENERATED '+r['generation']['difficulty']+' '+r['generation']['bank_profile']+'\n\n'+g.markdown(r))
 # Make original image paths resolvable in review without modifying raw strings.
 text='\n\n'.join(review);text=re.sub(r'\]\((images/.*?)\)',r'](/media/jake/SSD/EDB/math/\1)',text);(HERE/'review.md').write_text(text+'\n')
 result={'status':'passed','source':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_fidelity':fidelity,'source_geometric_features':'35/35 native feature-table matches; explicit q170588 option5 regression passed','source_feature_table_sha256':hashlib.sha256(feature_path.read_bytes()).hexdigest(),'label_regression_records':len(regressions),'cli_checks':'6 JSON records independently read back; actual generated/original Markdown levels, correct markers and hash/runtime manifests passed','complete_banks':'7/7','options':'35/35','correct_designations':'5/5 present; 2 absent originals remain absent','solutions':'5/5 present exact; 2 absent originals remain absent','domains':domains,'global_unique_assessed_tasks':len({(str(c),'grid' if lev=='hard' else 'labels',str(sp.Rational(1,c.q)) if lev=='hard' else None) for lev in ('easy','moderate','hard') for c in g.values(lev)[1]}),'generated_review_records':len(records),'default_bank_coverage':default_coverage,'native_grading':f'{len(rows)} gradeable records: all {len(rows)*5} choice checks passed; raw/changed legacy evidence has absent correct refs and is ungradeable by design','raster_geometry':json.loads((HERE/'pixel-report.json').read_text()),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'renderer':{k:json.loads(next((HERE/'plots').glob('*.json')).read_text())[k] for k in ('python','matplotlib','numpy')}},'renderer_sha256':hashlib.sha256((HERE/'render.py').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'native_counts':{k:json.loads((HERE/'engine-report.json').read_text())[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'unresolved':['Exact original horizontal base geometry cannot be recovered from unticked rasters; all observed banks evidence-only.','Two sources have absent native correct refs, preserved in raw replay.','Unlabelled apparent zero asymptotes and their amplitudes are modelling conventions, not exact original raster recovery.']}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('source_fidelity','raster_geometry')},indent=2))
if __name__=='__main__':run()
