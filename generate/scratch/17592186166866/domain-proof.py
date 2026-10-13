"""Targeted metadata QA: parse displayed slope denominators; no plot rerender or regrade."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json,re
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('qa',HERE/'validate.py');qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)
proof=[]
for previous in json.loads((HERE/'domain-before.json').read_text()):
 r=g.generate(**previous['call']);assert g.digest(r['question'])==previous['question_sha256'];assert r['question'][':question/id']==previous['question_id'];assert r['generation']['content_fingerprint']==previous['content_fingerprint']
 gen=r['generation'];assert gen['source']['database']=='math' and gen['source']['basis']==1356 and gen['source']['lineage']==g.SOURCE['lineage']
 expected_ids=[gen['bank_profile'].split('-',1)[1]] if gen['bank_profile'].startswith(('observed-','completed-')) else [c['source_id'] for c in g.CASES.values() if c['template']==gen['template']]
 assert gen['source']['source_ids']==expected_ids;assert gen['dependencies']==g.dependency_metadata()
 proof.append({'question_id':previous['question_id'],'question_and_content_identity_unchanged':True,'source_and_dependency_metadata_valid':True})
records=json.loads((HERE/'review.json').read_text());parsed=[]
for r in records:
 old_q_hash=g.digest(r['question']);p=r['generation']['parameters'];domain=g.domain_metadata(p);r['generation']['domain']=domain;r['generation']['source']=g.source_metadata(p,r['generation']['bank_profile']);r['generation']['dependencies']=g.dependency_metadata()
 assert g.digest(r['question'])==old_q_hash
 assert domain['variable_domains']=={'x':'real','y':'real'}
 lhs,rhs=domain['real_locus_equation_tex'].split('=');F=qa.expr(lhs)-qa.expr(rhs)
 expected=(qa.x-p['h'])**2/p['a']**2+(qa.y-p['k'])**2/p['b']**2-1
 assert sp.cancel(F-expected)==0
 assert p['a']>0 and p['b']>0 and p['a']!=p['b']
 derivative=sp.cancel(-sp.diff(F,qa.x)/sp.diff(F,qa.y))
 field=r['question'][':question/answer-fields'][0]
 candidates=[a for a in field[':answer-field/choices'] if sp.cancel(qa.expr(a[':answer/value'])-derivative)==0];assert len(candidates)==1
 answer=candidates[0]
 if ':answer-field/correct' in field:assert field[':answer-field/correct'][1]==answer[':answer/id']
 # The actual displayed answer string, not generation parameters, provides the denominator.
 denominator=sp.denom(sp.cancel(qa.expr(answer[':answer/value'])))
 roots=sp.solve(denominator,qa.y);assert roots==[p['k']]
 factor=domain['finite_slope_condition_tex'].split(r'\ne')[0];assert sp.cancel(qa.expr(factor)-(qa.y-p['k']))==0
 assert domain['finite_slope_excluded_line']=={'y':roots[0]}
 for point in domain['vertical_tangent_points']:assert sp.cancel(F.subs(dict(zip((qa.x,qa.y),point))))==0
 solution=r['question'].get(':question/worked-solution')
 if solution:
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',solution,re.S);printed=blocks[0].split('⟹')[1].replace(r'\,','').rstrip('.')
  ll,rr=printed.split('=');assert sp.cancel(qa.expr(ll)-qa.expr(rr)-F)==0
 else:assert r['generation']['evidence_only']
 if 'spec' in r['generation']['plot']:
  plot=json.loads(Path(r['generation']['plot']['spec']).read_text());assert plot['parameters']==p;assert plot['semiaxes']==[p['a'],p['b']];assert plot['center']==[p['h'],p['k']]
 parsed.append({'question_id':r['question'][':question/id'],'actual_displayed_correct':answer[':answer/value'],'parsed_denominator':str(denominator),'only_finite_slope_exclusion':{'y':p['k']},'real_locus_matches_printed_equation_and_plot':True,'question_unchanged':True})
(HERE/'review.json').write_text(json.dumps(records,indent=2)+'\n')
# Keep native fixtures current while retaining their exact learner questions and grading checks.
fixtures=json.loads((HERE/'engine-input.json').read_text())
for f in fixtures:
 gen=f['record']['generation'];gen['domain']=g.domain_metadata(gen['parameters']);gen['source']=g.source_metadata(gen['parameters'],gen['bank_profile']);gen['dependencies']=g.dependency_metadata()
(HERE/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n')
report={'status':'passed','metadata_only':True,'records':len(records),'fixed_call_question_identity_checks':proof,'source_and_dependency_checks':proof,'dependencies':g.dependency_metadata(),'displayed_domain_checks':parsed,'plots_rerendered':0,'native_regrading_required':False,'reason':'Question JSON, choice IDs/values and native grading checks are unchanged; only generation metadata was added.'}
(HERE/'domain-proof.json').write_text(json.dumps(report,indent=2)+'\n')
v=json.loads((HERE/'validation.json').read_text());v['source_and_dependency_metadata']={'status':'passed','fixed_call_question_identities_unchanged':len(proof),'source_basis':1356,'runtime':g.dependency_metadata(),'native_regrade_required':False};v['domain_metadata']={'status':'passed','records':len(records),'displayed_denominators_parsed':len(parsed),'question_identities_unchanged':len(proof),'plots_rerendered':0,'proof':'domain-proof.json'};(HERE/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
print('Domain metadata: '+str(len(records))+' displayed denominators and unchanged fixed-call questions/IDs passed; no plot rerenders.')
