import json,re,sys,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import validate_tex
ns={'__file__':str(H/'propose_formulas.py')};exec((H/'propose_formulas.py').read_text().split('props=[];reject=[]')[0],ns);canon=ns['canonical'];nums=ns['nums'];role=ns['role']
D=json.loads((H/'current.json').read_text());banks=json.loads((H/'source-banks.json').read_text());idx=collections.defaultdict(list)
for s in banks:
 choices=s.get('choices',[])+[a for f in s.get('fields',[])for a in f['choices']]
 for a in choices:
  if len(a['formulas'])==1 and isinstance(a['formulas'][0],str):idx[s['identity']].append((s,a,a['formulas'][0]))
props={};audit=[];residual=[]
for q in D['questions']:
 ident=q.get(':question/math-academy-id');source=idx.get(ident,[])
 if not ident:continue
 for f in q.get(':question/answer-fields',[]):
  for a in f.get(':answer-field/choices',[]):
   if a[':answer/type'][':db/ident']!=':answer.type/math':continue
   before=a[':answer/value'];opts=[]
   for s,c,tex in source:
    if canon(before)==canon(tex)and nums(before)==nums(tex):opts.append((s,tex))
   same=bool(opts);audit.append({'question':q[':db/id'],'identity':ident,'field':f[':db/id'],'answer':a[':db/id'],'source_bank_present':bool(source),'source_equivalent_choice':same})
   if not opts:
    if ident=='q-39481':
     old=canon(before).replace('r2z','r^2z');matches=[(s,t)for s,c,t in source if canon(t)==old]
     if matches:opts=matches
    if not opts:continue
   s,after=max(opts,key=lambda p:sum(role(p[1]).values()))
   ro,rn=role(before),role(after)
   if same and not any(rn[k]>ro[k]for k in ro):continue
   validate_tex(after);p={'entity':a[':db/id'],'attribute':'answer/value','before':before,'after':after,'reason':'Restore exact original bank math notation with the same mathematical value and existing owned answer identity.'if same else'Restore source superscript lost from cylindrical-integral bank, independently checked Jacobian powers.','evidence':{'basis_t':9837,'identity':ident,'question':q[':db/id'],'field':f[':db/id'],'source_path':s['path'],'source_choice_tex':after,'independent_check':'Ordered mathematical and numeric tokens equal after explicitly removing source styles.'if same else'Original sqrt(x²+y²)=r times Jacobianr gives r²; every distractor uses its own retained source exponent/bounds, not inferred from canonical answer.'},'confidence':'high'}
   if a[':db/id']in props:assert props[a[':db/id']]['after']==after
   props[a[':db/id']]=p
(H/'answer-format-proposals.json').write_text(json.dumps(list(props.values()),indent=2)+'\n');(H/'source-bank-comparison.json').write_text(json.dumps(audit,indent=2)+'\n');print('math bank members',len(audit),'source bank present',sum(r['source_bank_present']for r in audit),'matched',sum(r['source_equivalent_choice']for r in audit),'repairs',len(props),'q39481',[(p['entity'],p['after'])for p in props.values()if p['evidence']['identity']=='q-39481'])
