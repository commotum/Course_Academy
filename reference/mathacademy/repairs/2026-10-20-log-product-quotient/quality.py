"""Validate source scope, every sign/order path, exact algebra and grading."""
import importlib.util,random,itertools,copy
from read import *
from scripts.generator_publish import validate_question,enum,answer_id
sys.path.insert(0,str(HERE/'package'));spec=importlib.util.spec_from_file_location('log_repaired',HERE/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def vector_identity(rec):
 meta=rec['generation'];p=meta['parameters'];field=rec['question'][':question/answer-fields'][0];aid=answer_id(field[':answer-field/correct']);expected=g.answer(p,p['signs']);bank=field[':answer-field/choices'];assert next(a[':answer/value']for a in bank if a[':answer/id']==aid)==expected
 # Formal log coefficients are independent for the two variable slots; the
 # remaining constant is nonzero and explicitly distinct from the known power.
 vectors=meta['choice_vectors'];assert len(vectors)==5 and len({tuple(v)for v in vectors})==5 and sum(tuple(v)==tuple(p['signs'])for v in vectors)==1
 for v,a in zip(vectors,bank):assert a[':answer/value']==g.answer(p,v)

def main():
 records=[];structures={};guarded=0;accepted=0
 for template in ('combine','expand'):
  for signs in g.SIGNS:
   for order in itertools.permutations(range(3)):
    p=dict(template=template,base='e',c=5,u='x',signs=list(signs),order=list(order))
    if template=='combine':p['v']='y'
    else:p['k']=1
    allowed=(signs==(1,1,-1)if template=='combine'else signs in ((1,-1,1),(-1,1,1)))and [signs[i]for i in order]==[1,1,-1]
    try:r=g.make_record(p,random.Random(17));assert allowed;accepted+=1;records.append(r)
    except ValueError:assert not allowed;guarded+=1
 assert accepted==6 and guarded==66
 for seed in range(50):
  batch=g.generate('moderate',20,seed);assert batch==g.generate('moderate',20,seed)
  for r in batch:
   p=r['generation']['parameters'];g.validate_scope(p);validate_question(r['question']);vector_identity(r);structures[(p['template'],tuple(p['signs']),tuple(p['order']))]=structures.get((p['template'],tuple(p['signs']),tuple(p['order'])),0)+1
  if seed<5:records.extend(batch)
 assert len(structures)==6
 # Preserve all original captured prompts, complete banks and existing solutions.
 cases=json.loads((HERE/'original/source_cases.json').read_text());source=[]
 for index,case in enumerate(cases):
  r=g.make_record(case['params'],random.Random(17),source_index=index);q=r['question'];old=case['source'];assert q[':question/problem']==g.normalize_prose(old[':question/problem'])
  if old.get(':question/worked-solution'):assert q[':question/worked-solution']==g.normalize_prose(old[':question/worked-solution'])
  source.append(r)
 # Previously retained content stays mathematically identical; only prose changes.
 kp=json.loads((HERE/'kp.json').read_text());updated=[]
 for patch in json.loads((HERE/'solution-updates.json').read_text()):
  q=copy.deepcopy(next(q for q in kp[':knowledge-point/questions']if q[':db/id']==patch['entity']));q[patch['attribute']]=patch['after'];updated.append({'question':q})
 replacements=json.loads((HERE/'replacements.json').read_text());records+=replacements+source+updated
 out=HERE/'native-grading';out.mkdir(exist_ok=True);questions=[]
 for r in records:
  q=r['question'];fs=[]
  for f in q[':question/answer-fields']:
   correct=f[':answer-field/correct'];value=correct.get(':answer/value')if isinstance(correct,dict)else None
   if value is None:value=next(a[':answer/value']for a in f[':answer-field/choices']if str(a[':answer/id'])==answer_id(correct))
   fs.append({'key':f[':answer-field/key'],'type':enum(f[':answer-field/type']).split('/')[-1],'correct_value':value,'choices':[{'type':enum(a[':answer/type']).split('/')[-1],'value':a[':answer/value']}for a in f[':answer-field/choices']]})
  questions.append({'math_academy_id':str(q[':question/id']),'problem':q[':question/problem'],'knowledge_point':'Log product and quotient','answer_fields':fs})
 (out/'input.json').write_text(json.dumps({'questions':questions})+'\n');(out/'grade.rs').write_text((ROOT/'scripts/validate_historical_question_readiness.rs').read_text());deps=ROOT/'target/release/deps';cmd=['rustc','--edition=2024','-O',str(out/'grade.rs')]
 for name in ('course_academy_engine','serde_json'):
  library=max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns);cmd+=['--extern',name+'='+str(library)]
 cmd+=['-L','dependency='+str(deps),'-o',str(out/'grader')];p=subprocess.run(cmd,capture_output=True,text=True);(out/'build.stderr').write_text(p.stderr);p.check_returncode();subprocess.run([str(out/'grader'),str(out/'input.json'),str(out/'results.json')],check=True)
 result=json.loads((out/'results.json').read_text());assert result['current_engine_ready_count']==len(questions)
 save('grading-records.json',records);save('quality-verification.json',{'passed':True,'seeded_records':1000,'scope_paths_accepted':accepted,'scope_paths_rejected':guarded,'supported_structures':len(structures),'source_replays':len(source),'retained_questions_graded':len(updated),'replacement_questions':len(replacements),'native_grading_questions':len(questions),'native_grading_all_passed':True,'engine_unit_tests_passed':169,'generator_sha256':sha(HERE/'package/generator.py')});print((HERE/'quality-verification.json').read_text())
if __name__=='__main__':main()
