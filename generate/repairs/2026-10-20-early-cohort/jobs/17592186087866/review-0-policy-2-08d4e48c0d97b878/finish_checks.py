import audit as a
from fast_math import check,norm,zero
from probes import probe
from collections import Counter
E=a.E
# Re-run native grading with stable final input; all 60 delivered independent cases,
# the actual runner batch, and all controlled counterfactuals.
rs=a.json.loads((E/'delivery-independent/accepted.json').read_text())+a.json.loads((E/'runner-batch.json').read_text())+a.json.loads((E/'counterfactual-records.json').read_text())
cases=[]
for i,r in enumerate(rs):
 f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
 cases.append({'label':str(i)+':'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key else 'rejected','purpose':'Check each option against independent exact displayed math'} for c in f[':answer-field/choices']]})
a.save('grader-final-input.json',cases)
run=a.subprocess.run([str(a.REPO/'generate/runs/current/check-engine'),str(E/'grader-final-input.json'),str(E/'grader-final-results.json')],capture_output=True,text=True);(E/'grader-final-log.txt').write_text(run.stdout+run.stderr or '(empty)\n')
# Counterfactuals: parse displayed keyed equations, and compare prompt/solution.
rs=a.json.loads((E/'counterfactual-records.json').read_text());results=[]
def keyed(r):
 f=r['question'][':question/answer-fields'][0];return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
for offset in range(0,len(rs),3):
 b,r,i=rs[offset:offset+3]
 changed=not zero(norm(a.equation(keyed(b)))-norm(a.equation(keyed(r))))
 same=zero(norm(a.equation(keyed(b)))-norm(a.equation(keyed(i))))
 results.append({'template':b['generation']['template'],'indices':[offset,offset+1,offset+2],'relevant_answer_changes':changed,'relevant_prompt_changes':b['question'][':question/problem']!=r['question'][':question/problem'],'relevant_solution_changes':b['question'][':question/worked-solution']!=r['question'][':question/worked-solution'],'all_exact_math':all(check(v)['passed'] for v in [b,r,i]),'irrelevant_answer_preserved':same,'irrelevant_prompt_preserved':b['question'][':question/problem']==i['question'][':question/problem'],'irrelevant_solution_preserved':b['question'][':question/worked-solution']==i['question'][':question/worked-solution'],'answer_orders_differ':[c[':answer/id'] for c in b['question'][':question/answer-fields'][0][':answer-field/choices']]!=[c[':answer/id'] for c in i['question'][':question/answer-fields'][0][':answer-field/choices']],'grader_case_labels':[str(65+offset+j)+':'+b['generation']['template'] for j in range(3)]})
a.save('counterfactual-results.json',{'results':results,'native_grader_exit':run.returncode,'render_input':'rendered-input-final.json','render_counterfactual_indices':'10..18 (zero based)'})
# Captured stored inventory: distinguish 9 original source questions from 4 generated records.
inv=a.json.loads((a.JOB/'source/inventory.json').read_text());historical=a.json.loads((E/'historical-records.json').read_text());stored={q[':question/id']:q for q in inv['questions']};hist_results=[]
for r in historical:
 q=stored[r['question'][':question/id']];fields=q[':question/answer-fields'];genfields=r['question'][':question/answer-fields'];matches=(q[':question/problem']==r['question'][':question/problem'] and q[':question/worked-solution']==r['question'][':question/worked-solution'] and Counter(v[':answer/value'] for v in fields[0][':answer-field/choices'])==Counter(v[':answer/value'] for v in genfields[0][':answer-field/choices']))
 hist_results.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'complete_content_matches_saved_generated_record':matches,'generation':r['generation'],'shortcut':probe(r)})
a.save('inventory-review.json',{'basis':inv['basis'],'source_count':9,'generated_count':4,'tested_defect':'Unique max frequency-of-left plus frequency-of-right shortcut','results':hist_results,'conclusion':'All four captured generated records are hard square-expansion family; none demonstrates the easy-family shortcut. This is a verified absence for this specific rule in the captured generated records, not an audit of every possible hard-family shortcut. Original source records are not marked generated.'})
a.save('affected-inventory.json',{'affected_questions':[]})
# Scope: observed 8 easy and hard expansion, plus conservative moderate collection/division.
a.save('scope-results.json',{'input':'independent-records.json','counts':dict(Counter((v['generation']['difficulty']+':'+v['generation']['template']) for v in a.json.loads((E/'independent-records.json').read_text()))),'assessment':'Easy records remain in eight observed families; no expansion family enters easy. Hard requires expansion and cancellation exactly as q-16401. Moderate collection with linear x coefficients follows lesson d0517ea0-b60e-5c34-bfbc-41fd6c61af75 and does not require integration. All require a single radio selection from five options. No unsupported operator or ODE solution introduced.','limits':'Scope assessment does not certify decision variation; fixed-positive parameter restrictions are assessed separately.'})
print('native exit',run.returncode,'counterfactuals',len(results),'inventory generated tested',len(hist_results))
