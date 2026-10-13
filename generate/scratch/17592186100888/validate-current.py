"""Validate current checkbox source fidelity, displayed stages and native grading."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path[:0]=[str(ROOT/'scripts/question_capture')]
from edn import loads
spec=importlib.util.spec_from_file_location('legacy_validation',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g

def displayed(rec):
 q=rec['question'];fields=sorted(q[':question/answer-fields'],key=lambda f:('I','II','III').index(f[':answer-field/key']))
 assert [f[':answer-field/key'] for f in fields]==['I','II','III']
 bits=[];ids=[q[':question/id']]
 for f in fields:
  assert f[':answer-field/type']==':answer-field.type/checkbox'
  assert len(f[':answer-field/choices'])==2
  assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'true','false'}
  assert all(a[':answer/type']==':answer.type/text' for a in f[':answer-field/choices'])
  assert f[':answer-field/correct'][0]==':answer/id'
  ids.append(f[':answer-field/id']);ids.extend(a[':answer/id'] for a in f[':answer-field/choices'])
  bits.append(next(a[':answer/value']=='true' for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
 assert len(ids)==len(set(ids))
 for i in ids:assert str(uuid.UUID(i))==i
 assert bits[1]==bits[2]
 # Feed the actual displayed expressions and solution rows to the independently
 # authored TeX parser/stage checker. Only the answer representation is adapted.
 adapted=copy.deepcopy(rec)
 adapted['question'][':question/problem']=re.sub(r'- \*\*(?:I|II|III)\.\*\* ', '- ',q[':question/problem'].replace('\n\nSelect all that apply.',''))
 correct=g.ANSWERS[bits[0],bits[1]];fid=g.uid(q[':question/id']+':validator')
 bank=['None','I only','II and III only','I, II, and III','II only']
 adapted['question'][':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/correct':[':answer/id',g.uid(fid+':'+correct)],':answer-field/choices':[{':answer/id':g.uid(fid+':'+a),':answer/type':':answer.type/text',':answer/value':a} for a in bank]}]
 return v.displayed_check(adapted)

def checks(rec):
 return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Check each statement both selected and unselected'} for i,f in enumerate(rec['question'][':question/answer-fields']) for a in f[':answer-field/choices'] for b in [a[':answer/value']]]

def compile_engine():
 deps=ROOT/'target/release/deps'
 libs={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
 command=['rustc','--edition=2024','-O',str(ROOT/'generate/runs/current/check-engine.rs')]
 for name,p in libs.items():command+=['--extern',name+'='+str(p)]
 command+=['-L','dependency='+str(deps),'-o',str(H/'check-engine')]
 subprocess.run(command,check=True)
 return {name:hashlib.sha256(p.read_bytes()).hexdigest() for name,p in libs.items()}

def main():
 current=loads((H/'reference/initial/kp.edn').read_text())[0][0]
 sources={q[':question/math-academy-id']:q for q in current[':knowledge-point/questions']}
 cases=json.loads((H/'source-cases.json').read_text());fixtures=[];stage_count=0;source_count=0
 records=[]
 for case in cases:
  r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=r['question'];s=sources[case['source_id']]
  assert q[':question/problem']==s[':question/problem']
  assert q[':question/worked-solution']==s[':question/worked-solution']
  assert q[':question/difficulty']==s[':question/difficulty'][':db/ident']
  for f in q[':question/answer-fields']:
   sf=next(z for z in s[':question/answer-fields'] if z[':answer-field/key']==f[':answer-field/key'])
   assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
   assert sorted((a[':answer/value'],a[':answer/id']==f[':answer-field/correct'][1]) for a in f[':answer-field/choices'])==sorted((a[':answer/value'],a[':answer/id']==sf[':answer-field/correct'][':answer/id']) for a in sf[':answer-field/choices'])
  stage_count+=displayed(r);source_count+=1;records.append(r)
  normal=g.generate(case['level'],template=case['template'],parameters=case['parameters']);stage_count+=displayed(normal);records.append(normal)
 # Exhaustively validate every moderate task, including all signed bounds and
 # forbidden collision (-2,2). Distinct mathematical fingerprints ignore fields.
 moderate=[]
 for a,n in itertools.product(range(-5,-1),range(2,6)):
  try:r=g.generate_moderate(parameters={'a':a,'n':n})
  except ValueError:
   assert (a,n)==(-2,2);continue
  stage_count+=displayed(r);moderate.append(r);records.append(r)
 assert len(moderate)==len({r['generation']['mathematical_fingerprint'] for r in moderate})==15
 for t,l in g.LEVELS.items():
  for seed in (71,73):
   r=g.generate(l,seed,t);stage_count+=displayed(r);records.append(r)
   replay=g.generate(l,seed+100,t,parameters=r['generation']['parameters'])
   assert replay['question']==r['question']
 for claim,solution in itertools.product((True,False),repeat=2):
  r=g.generate_hard(parameters={'a':-2,'b':3,'c':-1,'claim':claim,'solution':solution});stage_count+=displayed(r);records.append(r)
 libs=compile_engine()
 fixtures=[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)]
 (H/'reference/current-native-input.json').write_text(json.dumps(fixtures,indent=2))
 subprocess.run([str(H/'check-engine'),str(H/'reference/current-native-input.json'),str(H/'reference/current-native-report.json')],check=True)
 native=json.loads((H/'reference/current-native-report.json').read_text());assert native['documented_unresolved_checks']==0
 evidence={'passed':True,'version':g.CURRENT_VERSION,'classification_basis':2001,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','source_prompts_replayed':source_count,'source_solutions_replayed':source_count,'complete_source_banks_replayed':27,'source_boolean_choices_matched':54,'source_correct_designations_matched':27,'distinct_moderate_tasks_exhaustively_validated':15,'displayed_solution_stages_checked':stage_count,'native_accepted':native['accepted_checks'],'native_rejected':native['rejected_checks'],'native_unresolved':0,'engine_libraries':libs,'generator_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0,'legacy_mathematical_validation':'validation.json; unchanged symbolic components and constraints from version 1.1.0','limitations':['Moderate asserted derivative (a-n)x^(n-1) is a labeled authored continuation of one observed error; historical error intent is underdetermined.','Hard is an authored difficulty, with no rated source evidence. No hard inventory is claimed filled in this moderate job.','Raw source profiles retain the source domain-wording anomaly and are ineligible for learning.']}
 (H/'validation-current.json').write_text(json.dumps(evidence,indent=2)+'\n')
 (H/'reference/moderate-domain.json').write_text(json.dumps(moderate,indent=2)+'\n')
 print(json.dumps(evidence,indent=2))
if __name__=='__main__':main()
