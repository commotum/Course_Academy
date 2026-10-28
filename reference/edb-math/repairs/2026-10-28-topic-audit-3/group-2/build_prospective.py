import copy,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH,normalize_prose,validate_math_structure
sys.path.insert(0,str(R/'scripts/question_capture'));import source_notation
D=json.loads((H/'current.json').read_text());Q={q[':db/id']:copy.deepcopy(q)for q in D['questions']};original={q[':db/id']:q for q in D['questions']}
if not(H/'format-proposals.json').exists():(H/'format-proposals.json').write_text((H/'proposals.json').read_text())
P=json.loads((H/'format-proposals.json').read_text())+json.loads((H/'structural-proposals.json').read_text())+json.loads((H/'completion-cas.json').read_text())+json.loads((H/'source-extra-proposals.json').read_text())
q=Q[17592186073998];before=q[':question/problem'];after=before.replace('-6a + 6b',r'\phantom{-}6a + 6b');assert before!=after
P.append({'entity':q[':db/id'],'attribute':'question/problem','before':before,'after':after,'reason':'Restore positive6a whose alignment phantom minus was mistakenly made visible during older import','evidence':{'basis':9837,'identity':'q-12457','source_path':'/home/jake/Developer/MA/DATA/Lessons/487/Source/487.html','source_formula':r'\left\{\begin{aligned}-7a+2b &=18 \\ \phantom{-}6a+6b &=0\end{aligned}\right.','independent_proof':'Second equation implies b=−a. First then −9a=18, giving a=−2,b=2. Both equations hold and exactly one existing owned bank value matches. Negative6a would imply a=b=−18/5, which matches none.'},'confidence':'high'})
q=Q[17592186247071];before=q[':question/problem'];after=before.replace('for $0\\le u\\le 1$','for $0\\le u\\le 2$');assert before!=after
P.append({'entity':q[':db/id'],'attribute':'question/problem','before':before,'after':after,'reason':'Authored source correction: make prose parameter interval agree with the displayed formal domain D','evidence':{'basis':9837,'identity':'q-110019','original_source':'1790/Source/1790.html','source_defect':'Source itself contradicts displayed0≤u≤2 with prose0≤u≤1. Displayed D is the formal integration domain.','independent_proof':r'For r=(u²,2u sinv,u cosv), ru×rv=(-2u,2u²sinv,4u²cosv). Its norm is2u√(1+u²+3u²cos²v) on either stated nonnegative interval. All existing values and canonical key remain valid. No numerical area or additional boundary data occur in the full question/solution. Only prose scope is reconciled to its own formal D.'},'confidence':'high'})
# Merge overlapping scalar edits by replaying each explicitly reviewed change.
def flatten_evidence(value):
 if isinstance(value,dict):yield value
 elif isinstance(value,list):
  for child in value:yield from flatten_evidence(child)
merged={}
for p in P:
 key=(p['entity'],p['attribute'])
 if key in merged:
  prev=merged[key];assert p['before']==prev['before'],key
  if prev['after']==p['after']:continue
  # Structural corrections can coexist with independently source-restored fonts.
  new=p['after']
  if key[1]=='question/worked-solution'and any(x in prev['reason']for x in['number-domain-notation','visible-set-braces']):pass
  else:
   # Nonoverlapping exact source-math replacements from the initial proposal.
   for e in flatten_evidence(prev['evidence']):
    a,b=e.get('before_math'),e.get('after_math')
    if a and b:
     spans=list(MATH.finditer(new));changed=False
     for m in reversed(spans):
      edge=2 if m[0].startswith('$$')else 1;inner=m[0][edge:-edge]
      if inner.strip()==a.strip():new=new[:m.start()]+m[0][:edge]+b+m[0][-edge:]+new[m.end():];changed=True
     if not changed and 'math_index'in e:
      spans=list(MATH.finditer(new));idx=e['math_index']
      if idx<len(spans):
       roles=[''.join(x)for x in re.findall(r'\\mathbf\s*(?:\{([A-Za-z])\}|([A-Za-z]))',b)]
       if roles:
        source_notation.ROLES=roles;m=spans[idx];edge=2 if m[0].startswith('$$')else 1;inner=source_notation.styled_math(m[0][edge:-edge]);new=new[:m.start()]+m[0][:edge]+inner+m[0][-edge:]+new[m.end():]
  prev['after']=new;prev['reason']+='; '+p['reason'];prev['evidence']=[prev['evidence'],p['evidence']]
 else:merged[key]=copy.deepcopy(p)
P=list(merged.values());objects={};all_objects={}
def index(v):
 if isinstance(v,dict):
  if ':db/id'in v:objects[v[':db/id']]=v;all_objects.setdefault(v[':db/id'],[]).append(v)
  for z in v.values():index(z)
 elif isinstance(v,list):
  for z in v:index(z)
index(list(Q.values()));A=copy.deepcopy(D['activities']);index(A)
for p in P:
 obj=objects[p['entity']];assert obj.get(':'+p['attribute'])==p['before'],(p['entity'],p['attribute']);
 for occurrence in all_objects[p['entity']]:occurrence[':'+p['attribute']]=p['after']
 validate_math_structure(p['after'])if p['attribute']!='answer/value'else None
for k in json.loads((H/'key-proposals.json').read_text()):
 f=objects[k['entity']];assert not f.get(':answer-field/correct');f[':answer-field/correct']=copy.deepcopy(next(a for a in f[':answer-field/choices']if a[':db/id']==k['after']))
for n in json.loads((H/'new-answer-plan.json').read_text())['new_answers']:
 f=objects[n['field']];assert not f.get(':answer-field/choices');a={':db/id':-len(objects)-1,':answer/id':n['answer_id'],':answer/type':{':db/id':17592186045498,':db/ident':':answer.type/math'},':answer/value':n['value']};f[':answer-field/choices']=[a];f[':answer-field/correct']=copy.deepcopy(a)
# Prospective unique fields; actual detaches remain separately guarded by history evidence.
removed=[]
for q in Q.values():
 fs=q.get(':question/answer-fields',[]);seen={}
 for f in fs:
  if f.get(':answer-field/correct'):seen[f[':answer-field/key']]=f
 q[':question/answer-fields']=[f for f in fs if seen.get(f[':answer-field/key'],f) is f]
 removed.extend(f[':db/id']for f in fs if f not in q[':question/answer-fields'])
(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');(H/'proposed-questions.json').write_text(json.dumps(list(Q.values()),indent=2)+'\n');(H/'proposed-activities.json').write_text(json.dumps(A,indent=2)+'\n')
(H/'authored-correction-index.json').write_text(json.dumps({'basis':9837,'authored_completions':[{'math_academy_id':p['math_academy_id'],'question':p['question'],'proof_artifact':'completion-proofs.json','proof_key':p['math_academy_id']}for p in json.loads((H/'completion-proofs.json').read_text())],'mathematical_or_source_semantic_corrections':[{'math_academy_id':'q-12457','question':17592186073998,'proof_artifact':'proposals.json','scope':'Restore actual positive source coefficient; key/solution completion relies on restored prompt'},{'math_academy_id':'q-110019','question':17592186247071,'proof_artifact':'proposals.json','scope':'Authored source correction: prose parameter interval agrees with its own displayed formal domain D; integrand/key unchanged'},{'math_academy_id':'q-158589','question':17592186378815,'proof_artifact':'structural-proposals.json','scope':'Closed arccos endpoint domain in worked-solution intermediate'}]},indent=2)+'\n');print('CAS',len(P),'prospective',len(Q),'duplicateoldfields',removed)
