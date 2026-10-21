import pathlib,json,sys,copy,shutil,hashlib,subprocess,os
E=pathlib.Path(__file__).resolve().parent;B=E.parent;P=B/'workspace'
sys.dont_write_bytecode=True
qid='0dbda9ea-eb5b-5de0-b271-e71696078d9a'
archive=json.loads((P/'17592186172039/reference/replenishment/basis-2772/generated.json').read_text());original=next(r for r in archive if r['question'][':question/id']==qid)
old=P/'evidence/historical-generator.py';dest=E/'historical-generator.py';shutil.copyfile(old,dest)
namespace={'__file__':str(dest),'__name__':'independent_historical_replay'};exec(compile(dest.read_text().split('# Every learner-facing checkbox question')[0],str(dest),'exec'),namespace)
assets=E/'historical-assets';namespace['HERE']=assets
for ext in ['png','json']:
 rel=pathlib.Path('images/generated/signs-nppn-zero-x.'+ext);target=assets/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/'17592186172039'/rel,target)
gen=original['generation'];r=namespace['generate'](gen['level'],seed=gen['seed'],template=gen['template'],parameters=gen['parameters'],profile=gen['legacy_bank_profile'])
assert r['question'][':question/id']==qid;assert json.loads(json.dumps(r['generation']))==gen
q=r['question'];claims=[line[line.index('At every point'):] for line in q[':question/problem'].splitlines() if 'At every point' in line];q[':question/problem']=q[':question/problem'].splitlines()[0]+'\n\nSelect all that apply.'
for roman,claim,f in zip(['I','II','III'],claims,q[':question/answer-fields']):
 f[':answer-field/key']=claim;q[':question/worked-solution']=q[':question/worked-solution'].replace('Statement '+roman+' is','Statement “'+claim+'” is')
for old,a in original.get('assets',{}).items():q[':question/worked-solution']=q[':question/worked-solution'].replace(old,a['path'])
inv=json.loads((B/'source/inventory.json').read_text());stored=next(q for q in inv['questions'] if q[':question/id']==qid)
def normalize(v):
 if isinstance(v,list):return [normalize(x) for x in v]
 if isinstance(v,dict):
  if ':db/ident' in v:return v[':db/ident']
  return {k:normalize(x) for k,x in v.items() if k!=':db/id'}
 return v
normal=normalize(stored)
for f in normal[':question/answer-fields']:
 f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']];f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
for o in [normal,q]:o[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
assert normal==q
r['reproduction']={'command':'/home/jake/Developer/Course_Academy/.venv/bin/python inventory_replay.py','historical_generator_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'stored_entity_id':stored[':db/id'],'exact_generation_metadata':True,'complete_stored_question_match_after_documented_presentation_migration':True,'historical_asset_inputs':'historical-assets/','parameters':gen['parameters'],'seed':gen['seed']}
(E/'generated-records.json').write_text(json.dumps([r],indent=2)+'\n');(E/'affected-inventory.json').write_text(json.dumps({'affected_questions':[{'question_id':qid,'entity_id':stored[':db/id'],'finding':'All three claims are false, with no None checkbox. The UI cannot submit the mathematically correct empty subset. Current generator adds correctly keyed None.','reproduction':'/home/jake/Developer/Course_Academy/.venv/bin/python inventory_replay.py; historical easy seed=3504342439 c=-6 a=1 b=0 quadrants=[1,3,2] claims=[1,-1,-1]','evidence_path':'generated-records.json'}]},indent=2)+'\n')
legacy=E/'legacy';legacy.mkdir(exist_ok=True);entry=legacy/'17592186172039.py';shutil.copyfile('/home/jake/Developer/Course_Academy/generate/scratch/17592186172039.py',entry)
proc=subprocess.run([sys.executable,str(entry),'--difficulty','moderate','--count','1','--format','json'],capture_output=True,text=True,cwd=E,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=''))
assert proc.returncode!=0 and 'StopIteration' in proc.stderr
(E/'legacy-failure.json').write_text(json.dumps({'command':[sys.executable,str(entry),'--difficulty','moderate','--count','1','--format','json'],'exit_code':proc.returncode,'stderr':proc.stderr,'current_counterexample_result':'Current manifest-only relocated CLI succeeds, see packaging.json.'},indent=2))
print('Exact stored question and generation metadata reproduced; legacy relocated import failure reproduced.')
