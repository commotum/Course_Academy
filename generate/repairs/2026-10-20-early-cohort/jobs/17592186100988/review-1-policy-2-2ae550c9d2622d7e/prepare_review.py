import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parent; P=R.parent/'review-0-policy-2-cec2a81535a7c052'
for f in ['regression.py','packaging.py']:(R/f).write_bytes((P/f).read_bytes())
s=(P/'review.py').read_text().replace('range(720010,720130)','range(731100,731160)').replace('[(2,3),(3,2),(3,4),(5,4)]','[(2,4),(3,2)]')
s=s.replace("save('counterfactual-records.json',pairs);",'''# New fixed-layout tests for the changed existence rule.
for style in ['inline_radio','inline_no_entry_radio','display_radio','display_should_radio','display_noperiod_radio']:
 base=g.generate('easy',seed=1167,template=style,profile='location_no_entry',parameters=p)
 for kind,change,profile in [('relevant',{'i':3},'overflow_locations'),('relevant',{'j':4},'overflow_locations'),('relevant',{'i':2},'location_no_entry'),('irrelevant',{'matrix':[[1,2,8],[4,5,6]]},'location_no_entry')]:
  pp=copy.deepcopy(p);pp.update(change);after=g.generate('easy',seed=1167,template=style,profile=profile,parameters=pp)
  pairs.extend([base,after]);pair_checks.append({'profile':style,'kind':kind,'change':change,'before_index':len(pairs)-2,'after_index':len(pairs)-1,'before_answer':identify(base['question'])[3],'after_answer':identify(after['question'])[3]})
save('counterfactual-records.json',pairs);''')
s=s.replace("print(json.dumps({'source_replay':replay,'canonical':canonical_result,", "print(json.dumps({'source_replay':replay,'canonical':canonical_result['result'],")
(R/'review.py').write_text(s)
v=(P/'variation_checks.py').read_text().replace('range(720010,720130)','range(731100,731160)').replace('[720010,720129]','[731100,731159]')
v=v.replace('Code fixes absence to inline formatting.','Both existence cases are now supported in all radio layouts.')
v=v.replace('Candidate batch adds five valid-entry easy records; combined fresh eligible pool has ten valid and zero absent. Larger sample has absent cases and survives filtering.','Current candidate batch and its counts are recorded above; both existence cases survive filtering.')
(R/'variation_checks.py').write_text(v)
(R/'provenance.json').write_text(json.dumps({'prior_review':str(P),'reused_scripts':['review.py','regression.py','packaging.py','variation_checks.py'],'adaptations':'Fresh seeds731100..731159, boundary testing focused on2x4 and3x2, fixed-layout existence and irrelevant-value controls added. Selection-rule account reused under matched engine/inventory bindings.','prior_binding':json.load(open(P/'review-binding.json'))},indent=2))
