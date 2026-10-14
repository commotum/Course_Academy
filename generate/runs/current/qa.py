"""Parent-run independent structural, replay, grading and variety checks; no EDB access."""
from __future__ import annotations
import argparse,importlib.util,json,subprocess,sys,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]

def load(path):return json.loads(path.read_text())
def dump(path,x):path.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def record_checks(rec):
 q=rec['question'];meta=rec['generation'];errors=[]
 for text in [q.get(':question/problem',''),q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])]:
  assert all(ord(c)>=32 or c in ('\n','\t','\r') for c in text),'unintended control byte in learner display'
 assert q[':question/difficulty'] in [':question.difficulty/'+s for s in ('easy','moderate','hard')]
 assert q[':question/problem'].strip() and q[':question/worked-solution'].strip()
 assert ':question/math-academy-id' not in q
 qid=str(uuid.UUID(q[':question/id']));assert qid==q[':question/id']
 fs=q[':question/answer-fields'];assert fs
 assert len({f[':answer-field/key'] for f in fs})==len(fs)
 owner_ids={qid};checks=[]
 for i,f in enumerate(fs):
  fid=str(uuid.UUID(f[':answer-field/id']));assert fid==f[':answer-field/id'] and fid not in owner_ids;owner_ids.add(fid)
  kind=f[':answer-field/type'];assert kind in [':answer-field.type/'+x for x in ('radio','select','checkbox','blank')]
  bank=f[':answer-field/choices'];assert bank
  ref=f[':answer-field/correct'];assert len(ref)==2 and ref[0]==':answer/id'
  assert sum(a[':answer/id']==ref[1] for a in bank)==1
  for a in bank:
   aid=str(uuid.UUID(a[':answer/id']));assert aid==a[':answer/id'] and aid not in owner_ids;owner_ids.add(aid)
   assert isinstance(a[':answer/value'],str) and a[':answer/value'].strip()
   if kind==':answer-field.type/blank':
    if aid==ref[1]:checks.append({'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'parent canonical blank'})
   else:checks.append({'field_index':i,'submitted_answer_id':aid,'expected':'accepted' if aid==ref[1] else 'rejected','purpose':'parent owned option selection'})
  if kind==':answer-field.type/blank':assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 assert 'parameter_fingerprint' in meta or 'parameters' in meta
 return checks

def main():
 parser=argparse.ArgumentParser();parser.add_argument('kp',type=int);parser.add_argument('--samples',type=int,default=12)
 parser.add_argument('--finite-domain',action='append',default=[],metavar='LEVEL=COUNT',help='Root-reviewed finite semantic catalog; excludes cosmetic variants')
 parser.add_argument('--script',type=str,help='Separate scratch draft when preserving a registered baseline')
 args=parser.parse_args();kp=args.kp;sample_count=args.samples
 finite={}
 for value in args.finite_domain:
  level,count=value.split('=',1);assert level in ('easy','moderate','hard') and level not in finite and int(count)>0;finite[level]=int(count)
 assert sample_count>=12
 script=Path(args.script).resolve() if args.script else REPO/'generate/scratch'/f'{kp}.py'
 assert script.parent==REPO/'generate/scratch'
 folder=script.with_suffix('');qa=ROOT/'qa';qa.mkdir(exist_ok=True)
 spec=importlib.util.spec_from_file_location('parent_kp_'+str(kp),script);g=importlib.util.module_from_spec(spec);sys.modules[spec.name]=g;spec.loader.exec_module(g)
 records=[];by_level={};checks=[]
 for level in ('easy','moderate','hard'):
  ids=set();params=set();tasks=set();examples=[]
  for seed in range(sample_count):
   rec=g.generate(level,seed=seed);record_checks(rec)
   assert rec==g.generate(level,seed=seed),'nondeterministic replay'
   assert rec['knowledge_point']['db_id']==kp
   ids.add(rec['question'][':question/id']);params.add(json.dumps(rec['generation']['parameters'],sort_keys=True))
   meta=rec['generation'];task=next((meta[k] for k in ('mathematical_task_fingerprint','mathematical_fingerprint','parameter_fingerprint') if k in meta),None)
   tasks.add(str(task) if task is not None else json.dumps([meta['template'],meta['parameters']],sort_keys=True))
   examples.append(rec);records.append(rec)
   checks.append({'label':f'parent/{level}/seed={seed}','record':rec,'checks':record_checks(rec)})
  assert len(tasks)>=min(6,finite.get(level,6)),(level,'insufficient sampled mathematical variation',len(tasks))
  if level in finite:assert len(tasks)<=finite[level],(level,'finite domain exceeded',len(tasks),finite[level])
  by_level[level]={'sampled_questions':sample_count,'unique_content':len(ids),'unique_parameters':len(params),'unique_mathematical_tasks':len(tasks),'templates':sorted({x['generation']['template'] for x in examples})}
  if level in finite:by_level[level]['root_reviewed_finite_semantic_domain']=finite[level]
 # Use the actual CLI once, independently of module helper execution.
 cli=subprocess.run([sys.executable,str(script),'--difficulty','all','--seed','91','--count','1','--format','json'],cwd=REPO,text=True,capture_output=True,timeout=60,check=True)
 cli_records=json.loads(cli.stdout);assert isinstance(cli_records,list) and len(cli_records)==3
 for rec in cli_records:record_checks(rec)
 dump(qa/f'{kp}-engine-input.json',checks)
 subprocess.run([str(ROOT/'check-engine'),str(qa/f'{kp}-engine-input.json'),str(qa/f'{kp}-engine.json')],check=True,timeout=60)
 dump(qa/f'{kp}-sampled.json',records)
 source=load(ROOT/'sources'/f'{kp}.json')['record'];casefile=folder/'source-cases.json'
 evidence=load(folder/'source.json')
 assert evidence==load(ROOT/'sources'/f'{kp}.json'),'worker source evidence changed from immutable capture'
 cases=load(casefile);qids={q.get(':question/math-academy-id',str(q[':db/id'])) for q in source.get(':knowledge-point/questions',[])}
 aliases={str(q[':db/id']):q.get(':question/math-academy-id',str(q[':db/id'])) for q in source.get(':knowledge-point/questions',[])}
 aliases.update({q[':question/id']:q.get(':question/math-academy-id',str(q[':db/id'])) for q in source.get(':knowledge-point/questions',[]) if ':question/id' in q})
 caseids={aliases.get(str(case.get('source_math_academy_id',case.get('math_academy_id',case.get('source_ma_id',case['source_id'])))),str(case.get('source_math_academy_id',case.get('math_academy_id',case.get('source_ma_id',case['source_id']))))) for case in cases}
 assert caseids==qids,'source case coverage gap'
 result={'kp_id':kp,'automated_parent_checks':'passed','source_case_coverage':len(qids),'levels':by_level,'native_grading':str(qa/f'{kp}-engine.json'),'database_writes':0,
  'manual_review_required':['source-bank mathematical equivalence and correctness designation','shared worked-solution fidelity and intermediate math','curriculum scope of observed and authored levels','plots and source repairs where present']}
 dump(qa/f'{kp}.json',result);print(json.dumps(result))
if __name__=='__main__':main()
