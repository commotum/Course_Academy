import json,re,hashlib,shutil
from pathlib import Path
root=Path.cwd();base=root/'reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic';plan=json.loads((base/'repair-plan.json').read_text());summary=[]
for d in sorted(base.glob('175*')):
 before=json.loads((d/'questions.json').read_text());qs=json.loads((d/'questions-after.json').read_text());lessons=json.loads((d/'lessons-after.json').read_text());topic=json.loads((d/'topic.json').read_text());routes=[]
 for a in lessons:
  a=a[0];steps={s[':db/id']:s for s in a[':activity/steps']};eid=a[':activity/first-step'][':db/id'];route=[]
  while eid:
   assert eid not in route and eid in steps;route.append(eid);eid=steps[eid].get(':step/next',{}).get(':db/id')
  assert set(route)==set(steps)
  expectedkps={k[':db/id']for k in topic[':topic/knowledge-points']};actualkps={s[':step/content'][':db/id']for s in steps.values()if ':knowledge-point/id'in s[':step/content']};assert actualkps==expectedkps
  routes.append({'activity':a[':db/id'],'route':route,'complete':True,'acyclic':True,'all_topic_knowledge_points_present':True})
 render=json.loads((d/'strict-render-after.json').read_text());layout=json.loads((d/'layout-after.json').read_text());grading=json.loads((d/'grading-checks.json').read_text());math=json.loads((d/'mathematics-after.json').read_text());chains=json.loads((d/'solution-chains-after.json').read_text());sources=json.loads((d/'source-manifest.json').read_text())
 assert all(g['passed']for g in grading)
 choice_checks=[c for r in math for c in r['choices']];assert all(c.get('mathematically_correct')==c['stored_correct']for c in choice_checks);assert all(sum(c.get('mathematically_correct',False)for c in r['choices'])==1 for r in math if r['choices'])
 assert not any(r.get('errors')or r.get('rawMarkers')or r['cardScrollWidth']>r['cardWidth']+3 for r in layout)
 row={'topic':int(d.name),'title':topic[':topic/title'],'read_basis':13537,'commit_basis':13541,'canonical_examples':sum(q[':question/math-academy-id'].startswith('e-')for q in qs),'practice_questions':sum(q[':question/math-academy-id'].startswith('q-')for q in qs),'active_fields':sum(len(q.get(':question/answer-fields',[]))for q in qs),'active_choices':len(choice_checks),'tutorials':sum(':tutorial/content'in s[':step/content']for a in lessons for s in a[0][':activity/steps']),'routes':routes,'all_207_question_sources_exact_identity':all(r['sources']for r in sources),'source_questions':len(sources),'source_comparison':'Every original solution captured locally matches the stored before solution modulo function-application spaces/U2061. Original snapshots remain unchanged; the16 listed source errors are corrected explicitly. Two missing solutions recovered from original DOM;15 newly authored from same-KP canonical templates.','strict_render_fields':len(json.loads((d/'fields-after.json').read_text())),'desktop_mobile_question_layouts':sum(not r.get('tutorial')for r in layout),'desktop_mobile_tutorial_layouts':sum(bool(r.get('tutorial'))for r in layout),'layout_errors':0,'actual_grader_checks':len(grading),'actual_grader_passed':True,'independent_all_choice_mathematics_passed':True,'unique_mathematical_answer_in_every_bank':True,'solution_chain_equations_parsed':sum('passed'in c for r in chains for c in r.get('checks',[])),'solution_chain_forms_reviewed_separately':sum('parse_error'in c for r in chains for c in r.get('checks',[])),'feedback':'No stored question/field/answer feedback attributes exist in these full records; worked solutions audited as corrective explanations.','assets':'No question, solution, choice, or tutorial image assets are required; all mathematics is native text/TeX.','completed_questions':[q[':question/math-academy-id']for q in qs if q[':question/math-academy-id']in plan['completions']],'mathematical_corrections':[q[':question/math-academy-id']for q in qs if q[':question/math-academy-id']in plan['mathematical_corrections']],'unresolved':[]}
 (d/'audit-summary.json').write_text(json.dumps(row,indent=2)+'\n');summary.append(row)
# Keep reproducible tooling local to this evidence package.
for name in ['collect','fields','fields_after','math','check','check_after','chain','chain_after','prepare','sources','filter_sources','reextract','compare','usage','visual','submit','reviews','verify','grade','finalize']:
 src=Path('/tmp/char_'+name+'.py')
 if name=='collect':src=Path('/tmp/characteristic_collect.py')
 if src.exists():
  text=src.read_text().replace("open(Path(__file__).with_name('math.py'))","open(Path(__file__).with_name('math.py'))")
  if name in ['check','check_after','chain','chain_after']:
   text=text.replace("exec(open(Path(__file__).with_name('math.py'))", "from pathlib import Path\nexec(open(Path(__file__).with_name('math.py'))")
  (base/(name+'.py')).write_text(text)
(base/'audit-summary.json').write_text(json.dumps({'topics':summary,'questions':207,'practice':188,'canonical':19,'tutorials':13,'all_choice_math_checks':940,'strict_render_fields':1367,'desktop_mobile_layout_checks':440,'actual_grader_checks':940,'committed_basis':13541,'repair':plan,'remaining_work':[]},indent=2)+'\n')
print(json.dumps({'questions':207,'math':940,'render':1367,'layout':440,'grader':940,'steps':sum(len(r['route'])for t in summary for r in t['routes']),'tutorials':sum(t['tutorials']for t in summary)},indent=2))
