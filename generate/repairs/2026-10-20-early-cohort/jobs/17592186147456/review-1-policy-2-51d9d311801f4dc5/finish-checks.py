# Additional independent assertions for complete source banks and normalization displays.
exec(open(__file__.replace('finish-checks.py','review.py')).read().split('# Source-guided decision coverage')[0])
source=load(J/'source/source.json')['material'];result=load(E/'source-replay.json');replays=load(E/'source-replay-records.json');extra=[]
for r in replays:
 q=next(q for q in source['kp'][':knowledge-point/questions'] if q[':question/math-academy-id']==r['generation']['template']);fs=q[':question/answer-fields'];gfs=r['question'][':question/answer-fields'];ok=True
 if fs[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
  ge=prompted_eqs(r)
  for sf in fs:
   if sf[':answer-field/key']=='None of the above':gf=next(f for f in gfs if f[':answer-field/key']=='None of the above')
   else:
    se=eq(sf[':answer-field/key']);gi=next(i for i,e in enumerate(ge) if all(s.simplify(u-v)==0 for u,v in zip(se,e)));gf=gfs[gi]
   ok=ok and fieldvalue(gf)==sf[':answer-field/correct'][':answer/value'] and sorted(a[':answer/value'] for a in gf[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
 else:ok=fieldvalue(gfs[0])==fs[0][':answer-field/correct'][':answer/value']
 extra.append({'source_id':q[':question/id'],'template':r['generation']['template'],'every_source_key_and_bank_value_matches':ok});assert ok
# Canonical has no captured bank; confirm its displayed mathematics separately, without inventing a bank.
canonical=source['kp'][':knowledge-point/canonical-example'];ces=[eq(t) for t in re.findall(r'\$(.*?)\$',canonical[':question/problem'])];cf=[independent(e)[0] for e in ces];assert cf==[True,True,False]
# Numeric source rendering cleanup does not change the classification algebra.
normalization=[]
rs=load(E/'samples.json')+load(E/'normal-samples.json')+load(E/'counterfactual-records.json')+load(E/'batch.json')
for ri,r in enumerate(rs):
 es=prompted_eqs(r);sections=re.split(r'- Equation [IV]+ is ',r['question'][':question/worked-solution'])[1:]
 for j,(e,sect) in enumerate(zip(es,sections)):
  if e[0]==1:continue
  displayed=re.search(r'we get\n\n\$\$\n(.*?)\n\$\$',sect,re.S);assert displayed
  norm=eq(displayed.group(1));correct=norm[0]==1 and all(s.simplify(a-b/e[0])==0 for a,b in zip(norm[1:],e[1:]));assert correct
  normalization.append({'record_index':ri,'question_id':r['question'][':question/id'],'row':j,'displayed':displayed.group(1),'correct':correct})
slots={}
for r in load(E/'samples.json')+load(E/'normal-samples.json'):
 t=r['generation']['template'];p=r['generation']['parameters'];d=slots.setdefault(t,{side:[set() for _ in range(3)] for side in ['left_scales','right_scales']})
 for side in d:
  for i,v in enumerate(p[side]):d[side][i].add(v)
slots={t:{side:[sorted(x) for x in lists] for side,lists in d.items()} for t,d in slots.items()}
save('source-bank-and-normalization.json',{'source_banks':extra,'canonical':{'source_id':canonical[':question/id'],'parsed_flags':cf,'bank_replay':'Not asserted: answer fields absent in capture. Public template unsupported and reported in source-replay.json.','normalization':'Independent coefficient-normalization check of all canonical equations; two qualifying rows and one nonpower.'},'normalized_solution_displays':normalization,'scalar_slot_coverage':slots,'boundary_proof':'All six coefficient slots tested at 1 and 5 for each feasible decision state. Interior values are supplementary random coverage; dependency is linear nonzero scaling, whose invariance is checked by controlled pairs.'})
print('source banks',len(extra),'normalized displays',len(normalization))
