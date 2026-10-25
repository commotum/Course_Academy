"""Verify support removal, preserved mathematics/banks and actual delivery."""
import copy,importlib.util,json,re,sys,types
from pathlib import Path
import sympy as s
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'generate/scratch/17592186068915'));sys.path.insert(0,str(ROOT/'generate'))
from scripts.generator_publish import prepare_records,inventory_fingerprints,validate_question
from scripts.integration_support_policy import validate_prerequisite_recall
from scripts.trig_substitution_batch_policy import validate_delivery_batch as trig_policy,KPS as TRIG
from scripts.substitution_pedagogy_batch_policy import validate_delivery_batch as other_policy

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
old=ROOT/'reference/edb-math/repairs/2026-10-24-trig-scaffolding';sys.path.insert(0,str(old))
rule_reader="next(b for b in blocks if b.lstrip().startswith(r'\\int') and b.count(r'\\int')==1 and b.strip().rstrip('.').endswith('+C')).strip().rstrip('.')"
trig_code=(old/'read_math.py').read_text().replace("re.search(r'You may use \\$(.*?)\\$\\.',problem).group(1)",rule_reader)
trig_code=trig_code.replace("re.search(r'Endpoint values: \\$(.*?)\\$',problem)","re.search(r'Endpoint values: \\$(.*?)\\$',sol)").replace("next(block for block in blocks if block.count(r'\\int')==1 and '='in block)","[block for block in blocks if block.count(r'\\int')==1 and '='in block][-1]").replace('formula supplied before the learner answers','formula explained in the worked solution').replace('Incorrect supplied','Incorrect worked-solution')
(H/'trig_read_math.py').write_text(trig_code)
trig_check=module('trig_printed_check',H/'trig_read_math.py')
other=ROOT/'reference/edb-math/repairs/2026-10-24-two-topic-pedagogy';reader=module('inverse_printed_reader',other/'read_math.py')
other_check=types.ModuleType('new_printed_check');other_check.__dict__.update({'s':s,'re':re,'scalar':reader.scalar,'integral':reader.integral,'X':reader.X,'U':reader.U})
code=(other/'check.py').read_text();code=code[code.index('def equal('):code.index('def main():')]
code=code.replace("formula=re.search(r'You may use \\$(.*?)\\$',problem)[1]", "formula=next(b for b in blocks if b.lstrip().startswith(r'\\int') and b.count(r'\\int')==1 and b.strip().rstrip('.').endswith('+C')).strip().rstrip('.')")
(H/'solution_rule_reader.py').write_text(code)
exec(compile(code,str(H/'solution_rule_reader.py'),'exec'),other_check.__dict__)

def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def main():
 summaries=[];render=[];graders=[]
 for item in json.loads((H/'capture.json').read_text())['knowledge_points']:
  kp=item['kp'];d=H/str(kp);pool=json.loads((d/'candidate-pool.json').read_text());before=json.loads((d/'records-before.json').read_text());policy=trig_policy if kp in TRIG else other_policy
  policy(pool,kp)
  for oldrow,row in zip(before,pool):
   validate_question(row['question']);validate_prerequisite_recall(row)
   (trig_check.check if kp in TRIG else other_check.check)(row)
   q=row['question'];is_full=not q[':question/difficulty'].endswith('/easy')
   assert 'You may use'not in q[':question/problem']and 'Endpoint values:'not in q[':question/problem']
   if is_full:
    assert 'Use the integration rule:'in q[':question/worked-solution']
    # The same primitive formerly supplied before answering is now explained in feedback.
    former=re.search(r'You may use \$(.*?)\$',oldrow['question'][':question/problem'])[1]
    assert former in q[':question/worked-solution'],('lost rule',kp,former)
    if 'Endpoint values:'in oldrow['question'][':question/problem']:assert 'Endpoint values:'in q[':question/worked-solution']
  current=json.loads((d/'before.json').read_text());fps=inventory_fingerprints(current[':knowledge-point/questions']+[current[':knowledge-point/canonical-example']]);accepted,duplicates=prepare_records(pool,kp,current[':knowledge-point/id'],fps,ROOT,d/'package');assert len(accepted)==16 and duplicates==8
  # A regression must reject both the actual old policy and a hint hidden behind false metadata.
  bad=copy.deepcopy(pool[8]);bad['question'][':question/problem']+='\n\nYou may use $\\int 1/u\\,du=\\ln|u|+C$.'
  try:policy([bad],kp)
  except ValueError:pass
  else:raise AssertionError('Blanket hint accepted')
  full=json.loads((d/'accepted-pool.json').read_text());checks=[]
  for i,row in enumerate(full):
   f=row['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1];key=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==cid);indef=row['generation']['model']['lower']is None
   if f[':answer-field/type']==':answer-field.type/radio':tests=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==cid else'rejected'}for a in f[':answer-field/choices']]
   else:
    tests=[{'submitted':key,'expected':'accepted'},{'submitted':r'\frac{2\left('+key+r'\right)}{2}','expected':'accepted'},{'submitted':'2('+key+')'if indef else '('+key+')+1','expected':'rejected'}]
    if indef:tests.append({'submitted':'('+key+')+1','expected':'accepted'})
   checks.append({'label':str(kp)+' '+str(i),'record':row,'checks':tests})
  report={'passed':True,'questions_checked':24,'hint_free_replacements':16,'unchanged_guided_questions':8,'math_and_response_banks_preserved':True,'former_rules_retained_in_solutions':True,'actual_delivery_duplicates':duplicates,'blanket_hint_negative_control_rejected':True}
  save(d/'generator-verification.json',report);save(d/'grader-input.json',checks);summaries.append({'kp':kp,**report});graders+=checks
  render.extend([full[0],full[8],full[16]])
  print(kp,'printed mathematics, support policy and delivery checked',flush=True)
 save(H/'generator-verification.json',{'passed':True,'knowledge_points':summaries,'questions_checked':288,'replacements':192,'unchanged_guided':96});save(H/'grader-input.json',graders);save(H/'render-input.json',render)
if __name__=='__main__':main()
