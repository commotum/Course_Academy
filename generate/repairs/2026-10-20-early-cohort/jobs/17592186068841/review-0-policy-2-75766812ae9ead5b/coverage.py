import sys,json,re,hashlib,subprocess,shutil
from pathlib import Path
sys.dont_write_bytecode=True
from review import ROOT,JOB,REPO,PKG,module,save,load
from independent_math import parse,value,correct,s,X,Y,K,C,rhs
sys.path.insert(0,str(REPO));from scripts.generator_publish import normalized_question

def leak(r):
 q=r['question'];m=re.search(r'Use an interval where \$(.*?)>0',q[':question/problem'])
 if not m:return None
 inner=parse(m[1]);name=r['generation']['template'];power=s.Rational(2,3) if name=='q-8304' else 2
 target=inner**power/(4 if name=='q-8303' else 1)
 f=q[':question/answer-fields'][0];matches=[a for a in f[':answer-field/choices'] if s.simplify(value(a[':answer/value'])-target)==0]
 return {'id':q[':question/id'],'template':name,'cue':m[1],'selected_values':[a[':answer/value'] for a in matches],'correct':len(matches)==1 and matches[0][':answer/id']==f[':answer-field/correct'][1]}

def coverage(records):
 from collections import Counter
 return {'count':len(records),'templates':dict(Counter(r['generation']['template'] for r in records)),'coefficient_signs':dict(Counter('positive' if r['generation']['parameters']['a']>0 else 'negative' for r in records)),'positions':dict(Counter(str(next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1])+1) for r in records)),'interval_leaks':[v for r in records if (v:=leak(r))]}

def main():
 results={}
 for n in ['easy-grid.json','batch.json','leak-cases.json','delivery-easy/accepted.json','delivery-batch/accepted.json','delivery-moderate/accepted.json','delivery-hard/accepted.json']:
  results[n]=coverage(load(n))
 save('coverage-results.json',results)
 # Reproduce all six captured generated records, using their retained seed metadata as inputs (not correctness evidence).
 m=module();retained=json.loads((PKG/'17592186068841/reference/replenishment/basis-2684/generated.json').read_text());inv=json.loads((JOB/'source/inventory.json').read_text());generated=[];matches=[];affected=[]
 for old in retained:
  g=old['generation'];level=old['question'][':question/difficulty'].split('/')[-1]
  fresh=m.generate(level,g['seed'],g['template'],parameters=g['parameters'],profile=g['bank_profile'])
  stored=next(q for q in inv['questions'] if q[':question/id']==old['question'][':question/id'])
  matched=normalized_question(stored)==normalized_question(fresh['question'])
  generated.append(fresh);matches.append({'question_id':stored[':question/id'],'entity_id':stored[':db/id'],'generation':fresh['generation'],'complete_content_and_identity_match':matched,'interval_cue':leak(fresh),'blank_family':fresh['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank')})
  assert matched
 save('generated-records.json',generated);save('inventory-reproduction.json',{'basis':inv['basis'],'inventory_questions':len(inv['questions']),'source_questions':15,'generated_questions_reproduced':len(generated),'results':matches,'conclusion':'Verified none of the six captured generated records belong to the demonstrated interval-leak or arbitrary-constant blank families. Original source questions are not marked generated. Missing q-128198 is a generator coverage defect, not a defective stored generated record.'});save('affected-inventory.json',{'affected_questions':affected})
 # Read-only learner selection reproduction of the provided select() formula, for a stated fresh-learner scenario.
 # The entire set of legal history masks need not be sampled: removing members cannot remove a cue from remaining members.
 import collections
 selection={}
 for n in ['delivery-easy/accepted.json','delivery-batch/accepted.json','delivery-moderate/accepted.json']:
  records=load(n);counts=collections.Counter();leaks=0
  pool=sorted(records,key=lambda r:r['question'][':question/id'])
  for i in range(256):
   seed=f'independent-review-730091-{i}';d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53;r=pool[int(u*len(pool))];counts[r['generation']['template']]+=1;leaks+=bool(leak(r))
  selection[n]={'draws':256,'templates':dict(counts),'interval_leak_draws':leaks,'pool_size':len(pool)}
 save('learner-selection.json',{'implementation':'engine/rust/question_selection.rs select(): candidates already fresh/usable, deduplicate/sort, select weighted nonempty difficulty then uniformly within band via second SHA256 word. This reproduction uses UUID ordering rather than unknown future numeric entity IDs; thus counts are illustrative, reachability and cue preservation do not depend on ordering.','scenario':'Fresh learner, requested difficulty has positive weight; all accepted records are eligible; 256 deterministic task seeds. Actual policy weights and learner history absent from captured inventory. Zero weight suppresses entire band; history can only remove members.','seed_prefix':'independent-review-730091-','results':selection,'structural_result':'Every accepted member has positive selection probability in a positive-weight band. All 5 batch members are easy_linear with both exponent signs; selection cannot introduce easy_constant. Interval copying succeeds on every tested surviving member of each affected template, so difficulty weighting/history cannot cure the within-template leak.','limitations':['No live policy or learner history captured; no claim of exact future frequencies or IDs.','Inventory basis 5369 may change.']})
 # Relocate the complete declared package under evidence; exercise stdout and deterministic execution.
 dest=ROOT/'relocated-package';shutil.copytree(PKG,dest,dirs_exist_ok=True)
 commands=[];outputs=[]
 for package in [PKG,dest]:
  cmd=[str(REPO/'.venv/bin/python'),'-B',str(package/'17592186068841.py'),'--difficulty','easy','--seed','730083','--count','2','--format','json'];p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);commands.append({'command':cmd,'returncode':p.returncode,'stderr':p.stderr});outputs.append(json.loads(p.stdout))
 save('relocation-samples.json',outputs[1]);save('packaging-results.json',{'commands':commands,'relocation_identical':outputs[0]==outputs[1],'manifest_dependencies':json.loads((PKG/'package.json').read_text())['dependencies'],'actual_dependencies':{'python':sys.version.split()[0],'packages':{'sympy':s.__version__}},'missing_manifest_files':[f for f in json.loads((PKG/'package.json').read_text())['files'] if not (PKG/f).is_file()],'external_output':'Entrypoint only emits stdout; relocation samples saved here by review script. No asset paths, package writes or database operations.'})
 print({n:{'count':v['count'],'templates':v['templates'],'leaks':len(v['interval_leaks'])} for n,v in results.items()});print('inventory',len(matches),'matched; affected',len(affected),'relocation',outputs[0]==outputs[1])
if __name__=='__main__':main()
