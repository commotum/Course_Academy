"""Post-delivery checks and relocation; writes evidence only."""
from check_repair import *
from shortcut_support import probe
import tempfile

def main():
 before=json.loads((OUT/'quartic-records.json').read_text())
 after=json.loads((OUT/'delivery-quartic/accepted.json').read_text())
 write('coverage-after.json',coverage(after))
 assert coverage(before)==coverage(after)
 probes=[]
 for stage,records in [('before',before),('after',after)]:
  for degree in (1,3):
   group=[r for r in records if min(m[0] for m,c in s.Poly(function(r).args[0],x).terms())==degree]
   rows=probe(group,f'{stage}: second_power={degree}','quartic-records.json' if stage=='before' else 'delivery-quartic/accepted.json')
   assert all(p['correct']<p['total'] for p in rows),rows
   probes+=rows
 write('shortcut-results.json',probes)
 inventory=json.loads((E.parent/'source/inventory.json').read_text())
 rows=[]
 for q in inventory['questions']:
  row={'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':':question/math-academy-id' in q,'retired':q.get(':question/retired',False),'has_correct_links':all(f.get(':answer-field/correct') for f in q[':question/answer-fields'])}
  row['eligible_from_captured_response_contract']=not row['retired'] and row['has_correct_links']
  if not row['original_source']:
   row['math']=check_record({'question':q,'generation':{'template':'captured_inventory'}})
   assert all(row['math'][k] for k in ['key_correct','unique_correct','distinct'])
  rows.append(row)
 write('inventory-inspection.json',{'basis':inventory['basis'],'records':rows,'affected_defect':'Unavailable second-term degree is a generator-domain omission, not a wrong stored question. No affected individual record demonstrated.','limits':'No stored generation metadata in capture; original source records remain sources. Eligibility here checks captured retirement and correct links only. Eight non-source records checked mathematically, not exhaustively graded or rendered. Live history, policy weights and current retirement status are not tested.'})
 write('affected-inventory.json',{'affected_questions':[]})
 manifest=json.loads((E/'package.json').read_text())
 actual={'python':platform.python_version(),'packages':{'sympy':s.__version__,'mpmath':__import__('mpmath').__version__}}
 assert manifest['dependencies']==actual
 results=[]
 with tempfile.TemporaryDirectory(dir=OUT,prefix='relocation-') as dest:
  dest=Path(dest)
  for name in manifest['files']:shutil.copyfile(E/name,dest/name)
  for difficulty,extra in [('easy',[]),('moderate',['--template','quartic_radio'])]:
   cmd=[sys.executable,'generator.py','--difficulty',difficulty,'--seed','104','--count','5','--format','json']+extra
   env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(OUT/'assets'))
   original=subprocess.run(cmd,cwd=E,env=env,capture_output=True,text=True,check=True)
   relocated=subprocess.run(cmd,cwd=dest,env=env,capture_output=True,text=True,check=True)
   assert original.stdout==relocated.stdout
   results.append({'command':cmd,'identical_output':True,'count':len(json.loads(relocated.stdout))})
 write('packaging-results.json',{'versions':actual,'relocation':results,'runtime_files':manifest['files']})
 write('selection-results.json',{'delivery_counts':{'quartic':len(after),'easy':len(json.loads((OUT/'delivery-easy/accepted.json').read_text()))},'sampled_second_degrees':coverage(after),'sampling_attempts':dict(Counter(r['generation']['sampling_attempts'] for r in before)),'captured_inventory_eligible':sum(r['eligible_from_captured_response_contract'] for r in rows),'retired_in_capture':sum(r['retired'] for r in rows),'selection_rule':'learning.rs excludes retired questions; question_selection.rs receives fresh usable candidates, samples positive-weight nonempty difficulty bands then uniformly within a band. Unknown ratings are fallback only when no weighted rated band remains. Unconfigured selection uses smallest entity ID.','limits':'No live learner history, policy weights or future entity IDs; no claim about future learner-specific frequencies. Moderate degree coverage is tested separately because the requested easy delivery band deliberately contains affine inners.'})
 print('Post-delivery shortcut probes passed; inventory and relocation checks passed.')

if __name__=='__main__':main()
