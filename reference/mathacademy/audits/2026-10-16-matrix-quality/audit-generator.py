from pathlib import Path
import hashlib,importlib.util,json,sys,traceback
sys.dont_write_bytecode=True
from scripts.question_capture.math_format import validate_generated_record
x=json.loads(sys.argv[1]);path=Path(x['generator'][':question-generator/script']);path=path if not str(path).startswith('generators/') else Path('/media/jake/SSD/EDB/math')/path
sys.path.insert(0,str(path.parent.resolve()));sha=hashlib.sha256(path.read_bytes()).hexdigest();spec=importlib.util.spec_from_file_location('matrix_quality_gen_'+str(x['kp']),path);g=importlib.util.module_from_spec(spec);sys.modules[spec.name]=g;spec.loader.exec_module(g)
out=dict(kp=x['kp'],path=str(path),sha256=sha,samples=[],unsupported=[],failures=[],formatFindings=[],samplingRejections=[],finiteLimits=[]);records=[]
for level in ['easy','moderate','hard']:
 supported=getattr(g,'SUPPORTED_LEVELS',None)
 if supported is not None and level not in supported:out['unsupported'].append(level);continue
 for seed in [404,917]:
  try:
   r=g.generate(level,seed=seed)
   assert r==g.generate(level,seed=seed),'Nondeterministic same-seed replay'
   if r.get('outcome') in ['finite-limit','unsupported']:
    out['finiteLimits'].append(dict(level=level,outcome=r['outcome'],reason=r.get('exception')));break
   q=r['question'];kp=r['knowledge_point'];assert kp.get('db_id',kp.get('id'))==x['kp']
   fs=q[':question/answer-fields'];assert fs and len({f[':answer-field/key'] for f in fs})==len(fs)
   for f in fs:
    ids=[a[':answer/id'] for a in f[':answer-field/choices']];assert f[':answer-field/correct'][1] in ids
    assert len(ids)==len(set(ids))
    if f[':answer-field/type'].endswith(('/blank','/select')):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
   try:validate_generated_record(r)
   except ValueError as ex:out['formatFindings'].append(dict(level=level,seed=seed,error=str(ex)))
   out['samples'].append(dict(level=level,seed=seed,legacyTable='| ---' in q[':question/problem'],unstackedMultiMatrix=q[':question/problem'].count(r'\begin{bmatrix}')>1 and 'matrix-operands' not in q[':question/problem']))
   records.append(r)
  except Exception as ex:
   if any(z in str(ex).lower() for z in ['unsupported','only easy','only hard','only moderate','not certified','not implemented','no observed','not supported','easy only','moderate/hard','requested moderate','unknown level']):out['unsupported'].append(dict(level=level,reason=str(ex)));break
   if any(z in str(ex).lower() for z in ['workload','outside bounded','entire source profile rejected']):out['samplingRejections'].append(dict(level=level,seed=seed,error=str(ex)));continue
   out['failures'].append(dict(level=level,seed=seed,error=repr(ex),traceback=traceback.format_exc()[-1500:]));break
out['unchanged']=sha==hashlib.sha256(path.read_bytes()).hexdigest();print(json.dumps(dict(report=out,records=records)))
