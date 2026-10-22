exec(open('audit.py').read().split('initial=digest()')[0])
# One-item CLI reproduction retained separately.
cmd=[sys.executable,str(PKG/'generator.py'),'--seed','827461','--count','1','--format','json']
p=subprocess.run(cmd,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,check=True)
save('minimal-cli.json',json.loads(p.stdout));save('minimal-command.json',{'command':cmd,'returncode':p.returncode,'same_question_as_fresh_first':json.loads(p.stdout)[0]['question'][':question/id']==load(ROOT/'minimal-failure.json')[0]['question'][':question/id']})
sys.path.insert(0,'/home/jake/Developer/Course_Academy')
from scripts.generator_publish import content_fingerprint, normalized_question
import uuid
inv=load(JOB/'source/inventory.json');known={q[':question/id'] for q in load(JOB/'source/source.json')['material']['kp'][':knowledge-point/questions']}
rebuilt=[]
for q in inv['questions']:
 if q[':question/id'] in known:continue
 p=q[':question/problem']; candidates=[sym(x) for x in re.findall(r'- The set (\$.*?\$) contains',q[':question/worked-solution'])]
 if 'do all the ' in p:inst={'profile':'universal','group':re.search(r'do all the (.*?) belong',p)[1]}
 elif '\\sqrt' in p:
  expr=re.search(r'number \$(.*?)\$ belong',p)[1];inst=g.number_instance('root',radicand=int(re.search(r'\{(\d+)\}',expr)[1]),sign=-1 if expr.startswith('-') else 1)
 else:
  expr=re.search(r'number \$(.*?)\$ belong',p)[1];n,d=map(int,re.findall(r'\{(\d+)\}',expr));inst=g.number_instance('fraction',numerator=-n if expr.startswith('-') else n,denominator=d)
 r=g.make_record(inst,candidates)
 assert content_fingerprint(r['question'])==content_fingerprint(q)
 published_id=str(uuid.uuid5(uuid.UUID(g.KP['id']),'generated-question:'+content_fingerprint(r['question'])))
 assert published_id==q[':question/id']
 r['question']=normalized_question(q)
 for f in r['question'][':question/answer-fields']:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct']]
 assert r['question'][':question/problem']==q[':question/problem']
 assert r['question'][':question/worked-solution']==q[':question/worked-solution']
 r['generation']['inventory_reproduction']={'entity_id':q[':db/id'],'basis':inv['basis'],'method':'Raw make_record mathematical parameters reproduce content fingerprint and publisher UUID exactly; captured normalized fields retained; original sampling seed absent in captured inventory; null seed is not an asserted historical seed.'}
 rebuilt.append(r)
save('generated-records.json',rebuilt)
validation=[]
for n in ['delivery-samples/accepted.json','delivery-batch/accepted.json']:
 for i,r in enumerate(load(ROOT/n)):validation.append({'label':n+':'+str(i),'record':r,'expected_usable':True})
for r in rebuilt:validation.append({'label':'inventory:'+r['question'][':question/id'],'record':r,'expected_usable':any(truth(f)=='true' for f in r['question'][':question/answer-fields'])})
save('selection-input.json',validation)
# Keep original shared fixture adapter, substitute the public native eligibility call.
src=(JOB.parents[4]/'unused') if False else pathlib.Path('/home/jake/Developer/Course_Academy/generate/runs/current/check-engine.rs')
s=src.read_text();s=s[:s.index('  let snapshot=EntitySnapshot::new')]+'''  let snapshot=EntitySnapshot::new(entities,0)?;
  let result=learning::validate_practice_question(&snapshot,10);
  let usable=result.is_ok();
  if usable != item["expected_usable"].as_bool().ok_or("expected usability required")? { return Err(format!("Unexpected usability {}: {:?}",item["label"],result).into()); }
  reports.push(json!({"label":item["label"],"question_id":q[":question/id"],"usable":usable,"reason":result.err()}));
 }
 fs::write(&args[1],serde_json::to_string_pretty(&json!({"database_writes":0,"entry_point":"course_academy_engine::learning::validate_practice_question","records":reports}))?+"\\n")?;
 Ok(())
}
'''
(ROOT/'check-selection.rs').write_text(s)
print('Reproduced',len(rebuilt),'stored generated question IDs exactly; native eligibility cases',len(validation))
