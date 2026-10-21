import importlib.util,sys,copy
from repair_read import *
sys.path.insert(0,str(HERE/'package'));spec=importlib.util.spec_from_file_location('all_three_repaired',HERE/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
if __name__=='__main__':
 kp=json.loads((HERE/'kp.json').read_text());ledger=[];updates=[];replacements=[]
 bad=[17592186608363,17592186608368,17592186608371]
 recipes={
  bad[0]:lambda:g.build('powers-expand',0,2,4,signs=(1,-1,1),perm=(1,2,0),base='5',order=(0,1,2)),
  bad[1]:lambda:g.build('powers-expand',0,3,5,signs=(1,-1,1),perm=(1,2,0),base='10',order=(1,0,2)),
  bad[2]:lambda:g.build_numeric(1,1,2,4,1,'3'),
 }
 for q in kp[':knowledge-point/questions']:
  eid=q[':db/id']
  if q.get(':question/math-academy-id'):ledger.append({'id':eid,'decision':'preserve_math_academy_source','math_academy_id':q[':question/math-academy-id']});continue
  if eid in bad:
   r=recipes[eid]();replacements.append(r);ledger.append({'id':eid,'decision':'withdraw_and_replace','reason':'One positive and two negative log terms permit two quotient-rule applications and the power rule, bypassing the required numerator product step.','replacement_uuid':r['question'][':question/id']});continue
  ledger.append({'id':eid,'decision':'retain','reason':'Two positive terms, one negative term, and non-unit powers; matches the source rule sequence.'})
  if eid==17592186608372:
   v=(-g.F(2),g.F(3),g.F(1,2));old=g.expanded('2',v,(0,2,1));ordered=g.expanded('2',v,(2,1,0))
   solution='First reorder the terms so the two positive logarithms are together:\n\n$$\n'+old+'='+ordered+'\n$$\n\n'+g.solution('2',v,'combine',(2,1,0))
   # Apply the package's narrow-screen equation reflow without changing its bank.
   dummy=g.record('Reorder terms.', ['1','2','3','4','5'],0,solution,{})
   updates.append({'entity':eid,'attribute':':question/worked-solution','before':q[':question/worked-solution'],'after':dummy['question'][':question/worked-solution']})
 assert len(replacements)==3 and len(updates)==1
 save('audit-ledger.json',ledger);save('solution-updates.json',updates);save('replacements.json',replacements)
 save('package/scope-contract.json',{'kp':KP,'source_ids':['e-4095','q-1102','q-1111','q-66923','q-79406'],'required':'Two numerator factors and one denominator factor, with at least one non-unit power. Condense positive pair before the negative term. Numeric canonical family has a positive powered constant plus log(variable) minus log(constant).','excluded':'One numerator factor over two denominator factors; one positive term with two negative terms; no nontrivial powers. These can bypass the product rule.','distractors':'May retain alternative sign partitions; these are never selected as an out-of-scope correct target.','source_replay':'Captured source prompts, banks, and existing solutions retained.'})
 print(json.dumps({'withdrawn':bad,'clarified':[17592186608372],'retained_unchanged':[17592186608364]}))
