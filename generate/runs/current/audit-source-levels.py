"""Narrow follow-up to the captured difficulty-value bug; no grading or DB writes."""
import importlib.util,json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def main():
 manifest=json.loads((R/'manifest.json').read_text());out={'checked':0,'mismatches':[],'unsupported_calls':[],'scripts':{}}
 for job in manifest['jobs']:
  if job['status']!='qa_passed':continue
  path=ROOT/job['script'];cases=json.loads((path.with_suffix('')/'source-cases.json').read_text());sources=json.loads((R/f"sources/{job['kp_id']}.json").read_text())['record'][':knowledge-point/questions'];todo=[]
  for c in cases:
   if c.get('level',c.get('difficulty')):continue
   alias=c.get('source_math_academy_id',c.get('math_academy_id',c.get('source_ma_id',c.get('source_id'))));q=next((q for q in sources if str(alias) in map(str,[q.get(':db/id'),q.get(':question/id'),q.get(':question/math-academy-id')])),None)
   if q is not None and ':question/difficulty' in q:todo.append((c,q))
  if not todo:continue
  name='difficulty_audit_'+str(job['kp_id']);spec=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(spec);sys.modules[name]=g
  try:spec.loader.exec_module(g)
  except Exception as e:out['unsupported_calls'].append({'kp_id':job['kp_id'],'error':repr(e)});continue
  out['scripts'][str(job['kp_id'])]=hashlib.sha256(path.read_bytes()).hexdigest()
  for c,q0 in todo:
   actual=q0[':question/difficulty'];actual=actual.get(':db/ident') if isinstance(actual,dict) else actual;level=next((c[key] for key in ('authored_generator_level','authored_working_level','assigned_level') if c.get(key)),actual);level=str(level).split('/')[-1]
   try:
    r=g.generate(level,template=c['template'],parameters=c['parameters'],profile=c.get('profile',c.get('bank_profile')));q=r['question'];out['checked']+=1
    if q.get(':question/difficulty')!=actual:out['mismatches'].append({'kp_id':job['kp_id'],'source_id':c['source_id'],'expected':actual,'actual':q.get(':question/difficulty')})
   except Exception as e:out['unsupported_calls'].append({'kp_id':job['kp_id'],'source_id':c['source_id'],'level':level,'error':repr(e)})
  (R/'qa/source-level-runtime-audit.json').write_text(json.dumps(out,indent=2)+'\n')
 (R/'qa/source-level-runtime-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='scripts'}))
if __name__=='__main__':main()
