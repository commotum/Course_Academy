import json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,validate_math_structure
D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());F=json.loads((H/'fields.json').read_text());src=json.loads((H/'sources.json').read_text());ns={'re':re};s=(H/'refine.py').read_text();exec(s[s.index('def set_fences(t):'):s.index('answer_proofs=[]')],ns);fences=ns['set_fences']
for q in D['questions']:
 for f in q.get(':question/answer-fields',[]):
  if not f[':answer-field/type'][':db/ident'].endswith('checkbox'):continue
  e=f[':db/id'];a='answer-field/key';v=f[':'+a];F.append([e,a,v,q.get(':question/math-academy-id'),False]);after=v
  for m in reversed(list(MATH.finditer(v))):
   body=m[0].strip('$');new=fences(body)
   if new!=body:after=after[:m.start()]+'$'+new+'$'+after[m.end():]
  if after!=v:P.append({'entity':e,'attribute':a,'before':v,'after':after,'reason':'display-only-visible-set-delimiters-checkbox-key','evidence':{'source_paths':sorted({s['path']for s in src if s['identity']==q.get(':question/math-academy-id')and s['attribute']=='question/problem'}),'proof':'Only visible outer set delimiters change; vector entries and sequence are identical.'}})
# q35346: unchanged first row was transcribed with the final entry sign flipped in three intermediate matrices.
q=next(q for q in D['questions']if q[':db/id']==17592186446047);a='question/worked-solution';before=q[':'+a];pr=next((x for x in P if x['entity']==q[':db/id']and x['attribute']==a),None);current=pr['after']if pr else before;needle='3 & 6 & 0 & -3 & 9';assert current.count(needle)==3;after=current.replace(needle,'3 & 6 & 0 & -3 & -9');proof={'identity':'q-35346','derivation':'Only R4 and then R3 and R4 change. R1 remains (3,6,0,−3,−9) throughout. R4−4/3 R1=(0,−5,2,−1,7); the remaining nonzero rows have rank 2 and nullity 5−2=3.','source_paths':sorted({x['path']for x in src if x['identity']=='q-35346'})}
if pr:pr['after']=after;pr['reason']+=',authored-mathematical-correction-row-sign';pr.setdefault('additional_evidence',[]).append(proof)
else:P.append({'entity':q[':db/id'],'attribute':a,'before':before,'after':after,'reason':'authored-mathematical-correction-row-sign','evidence':proof})
# Correct the duplicated question mark in the incomplete source prompt; no mathematical change.
q=next(q for q in D['questions']if q[':db/id']==17592186134221);p=next(p for p in P if p['entity']==q[':db/id']and p['attribute']=='question/problem');p['after']=p['after'].replace('?$?','?$');p['reason']+=',duplicate-question-mark'
F=list({(e,a):(e,a,v,i,b)for e,a,v,i,b in F}.values());(H/'fields.json').write_text(json.dumps(F,indent=2)+'\n');(H/'proposals.json').write_text(json.dumps(P,indent=2)+'\n');print('fields',len(F),'proposals',len(P))
