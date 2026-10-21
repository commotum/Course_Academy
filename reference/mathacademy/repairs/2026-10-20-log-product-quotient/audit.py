"""Classify every existing authored question and build source-faithful replacements."""
import importlib.util,random,re,copy
from read import *
sys.path.insert(0,str(HERE/'package'));spec=importlib.util.spec_from_file_location('log_scope_generator',HERE/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
if __name__=='__main__':
 kp=json.loads((HERE/'kp.json').read_text());ledger=[];updates=[];replacements=[]
 oldspec=importlib.util.spec_from_file_location('old_log_generator',HERE/'original/generator.py');old=importlib.util.module_from_spec(oldspec);oldspec.loader.exec_module(old)
 parameters={
  17592186608285:dict(template='combine',base='e',c=9,u='q',v='p',signs=[-1,1,-1],order=[1,2,0]),
  17592186608296:dict(template='combine',base='e',c=5,u='x',v='z',signs=[-1,1,-1],order=[0,2,1]),
  17592186608299:dict(template='expand',base='e',c=2,u='q',k=1,signs=[-1,1,1],order=[2,1,0]),
  17592186608300:dict(template='expand',base='e',c=3,u='p',k=1,signs=[-1,-1,1],order=[2,0,1]),
  17592186608308:dict(template='combine',base='10',c=9,u='z',v='x',signs=[1,1,-1],order=[0,1,2]),
 }
 for q in kp[':knowledge-point/questions']:
  if q.get(':question/math-academy-id'):ledger.append({'id':q[':db/id'],'decision':'preserve_math_academy_source','math_academy_id':q[':question/math-academy-id']});continue
  p=parameters[q[':db/id']];assert all(s in q[':question/problem']for s in ([str(p['c']),p['u']]if p['template']=='combine'else[p['u']]))
  reconstructed=old.make_record(p,random.Random(0))['question'][':question/problem'];assert reconstructed==q[':question/problem'],(q[':db/id'],reconstructed,q[':question/problem'])
  try:g.validate_scope(p);decision='retain_and_clarify_solution'
  except ValueError as e:decision='withdraw_and_replace'
  if decision=='retain_and_clarify_solution':
   solution=g.normalize_prose(g.solution(p));updates.append({'entity':q[':db/id'],'attribute':':question/worked-solution','before':q[':question/worked-solution'],'after':solution});ledger.append({'id':q[':db/id'],'decision':decision,'parameters':p});continue
  fixed=copy.deepcopy(p)
  if p['template']=='combine':fixed['signs']=[1,1,-1];fixed['order']=[0,1,2]
  else:fixed['signs']=[1,-1,1];fixed['order']=[0,2,1]
  rec=g.make_record(fixed,random.Random(q[':db/id']),seed=q[':db/id']);replacements.append(rec);ledger.append({'id':q[':db/id'],'decision':decision,'reason':'One positive and two subtracted logarithms; outside the saved source factor roles and two-positive/one-negative presentation.','old_parameters':p,'new_parameters':fixed,'replacement_uuid':rec['question'][':question/id']})
 assert len(ledger)==9 and len(parameters)==5 and len(replacements)==3 and len(updates)==2
 save('audit-ledger.json',ledger);save('solution-updates.json',updates);save('replacements.json',replacements)
 save('package/scope-contract.json',{'kp':KP,'sources':['e-4085','q-47200','q-47203','q-100242','q-66781'],'combine':'log(constant)+log(variable)-log(other variable); the positive pair may be interchanged','expand':'log((known base power times variable)/constant) or log((constant times variable)/(known base power)); expand quotient then numerator product, then evaluate known logarithm','excluded':'one positive with two subtracted logarithms; negative leading term; variable moved to denominator of expand template; non-unit variable log coefficients in combine','evidence':'Saved EDB source examples and original source_cases.json; no web sources'})
 print(json.dumps({'questions_audited':len(ledger),'authored_questions':len(parameters),'withdraw_and_replace':len(replacements),'retain_with_clearer_solutions':len(updates),'source_questions_preserved':4}))
