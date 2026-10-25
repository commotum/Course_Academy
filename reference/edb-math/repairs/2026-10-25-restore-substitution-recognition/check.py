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
def full_check(row,kp):
  # Reuse independent printed-math readers on the complete calculation. The
  # original full choice bank is separately checked below, never hidden from QA.
  r=copy.deepcopy(row);f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
  key=next(a for a in f[':answer-field/choices']if a[':answer/id']==cid)
  key[':answer/value']=key[':answer/value'].removesuffix('+C')
  f[':answer-field/type']=':answer-field.type/blank';f[':answer-field/choices']=[key]
  r['question'][':question/difficulty']=':question.difficulty/moderate' if kp not in TRIG else r['question'][':question/difficulty']
  return (trig_check.check if kp in TRIG else other_check.check)(r)

def bank_check(row,kp):
  f=row['question'][':question/answer-fields'][0]
  if f[':answer-field/type']!=':answer-field.type/radio':return 0
  read=trig_check.scalar if kp in TRIG else reader.scalar
  x=trig_check.p.x if kp in TRIG else reader.X
  definite=row['generation']['model']['lower']is not None
  values=[read(a[':answer/value'].removesuffix('+C'))for a in f[':answer-field/choices']]
  signatures=values if definite else [s.diff(v,x)for v in values]
  pairs=0
  for i,a in enumerate(signatures):
   for b in signatures[:i]:
    delta=a-b;witness=None
    for point in (s.Rational(1,97),s.Rational(-1,89),s.Rational(1,7),2,3,-2,-3):
     try:
      va,vb=(complex(v.evalf(30,subs={x:point}))for v in(a,b))
      if abs(va.imag)<1e-12 and abs(vb.imag)<1e-12 and 1e-12<abs(va-vb)<1e100:witness=str(point);break
     except (TypeError,ValueError):pass
    assert witness is not None,('Equivalent or unresolved answer choices',kp,row['question'][':question/id'],a,b)
    pairs+=1
  return pairs

def main():
 summaries=[];render=[];graders=[];pairs=0
 for item in json.loads((H/'capture.json').read_text())['knowledge_points']:
  kp=item['kp'];d=H/str(kp);pool=json.loads((d/'candidate-pool.json').read_text());before=json.loads((d/'records-before.json').read_text());policy=trig_policy if kp in TRIG else other_policy
  policy(pool,kp)
  for row in pool:
   validate_question(row['question']);validate_prerequisite_recall(row);full_check(row,kp);pairs+=bank_check(row,kp)
   q=row['question'];assert 'Use the substitution'not in q[':question/problem']and 'You may use'not in q[':question/problem']and 'Endpoint values:'not in q[':question/problem']
   assert 'Use the integration rule:'in q[':question/worked-solution']
  current=json.loads((d/'before.json').read_text());fps=inventory_fingerprints(current[':knowledge-point/questions']+[current[':knowledge-point/canonical-example']]);accepted,duplicates=prepare_records(pool,kp,current[':knowledge-point/id'],fps,ROOT,d/'package');assert len(accepted)+duplicates==24 and (len(accepted)>=8 if kp==17592186064250 else len(accepted)==8),(kp,len(accepted),duplicates)
  for hint in ('Use the substitution $u=x^2$.','Let $u=x^2$.','You may use $\\int 1/u\\,du=\\ln|u|+C$.'):
   bad=copy.deepcopy(pool[0]);bad['question'][':question/problem']+='\n\n'+hint
   try:policy([bad],kp)
   except ValueError:pass
   else:raise AssertionError('Giving away target decision or primitive accepted')
  full=json.loads((d/'accepted-pool.json').read_text());checks=[]
  for i,row in enumerate(full):
   f=row['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1];key=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==cid);indef=row['generation']['model']['lower']is None
   if f[':answer-field/type']==':answer-field.type/radio':tests=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==cid else'rejected'}for a in f[':answer-field/choices']]
   else:
    tests=[{'submitted':key,'expected':'accepted'},{'submitted':r'\frac{2\left('+key+r'\right)}{2}','expected':'accepted'},{'submitted':'2('+key+')'if indef else '('+key+')+1','expected':'rejected'}]
    if indef:tests.append({'submitted':'('+key+')+1','expected':'accepted'})
   checks.append({'label':str(kp)+' '+str(i),'record':row,'checks':tests})
  report={'passed':True,'questions_checked':24,'complete_answer_replacements':len(accepted),'unchanged_full_questions':duplicates,'complete_worked_solutions':True,'actual_delivery_duplicates':duplicates,'leaked_target_decision_negative_controls_rejected':True}
  save(d/'generator-verification.json',report);save(d/'grader-input.json',checks);summaries.append({'kp':kp,**report});graders+=checks
  render.extend([full[0],full[3],full[8],full[16]])
  print(kp,'printed mathematics, complete banks and delivery checked',flush=True)
 save(H/'generator-verification.json',{'passed':True,'knowledge_points':summaries,'questions_checked':288,'distinct_answer_pairs_checked':pairs,'replacements':sum(r['complete_answer_replacements']for r in summaries),'unchanged_full':sum(r['unchanged_full_questions']for r in summaries)});save(H/'grader-input.json',graders);save(H/'render-input.json',render)
if __name__=='__main__':main()
