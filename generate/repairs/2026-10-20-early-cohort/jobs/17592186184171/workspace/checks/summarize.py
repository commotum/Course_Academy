"""Summarize completed, saved checks without regenerating questions."""
import collections,hashlib,json,pathlib,re
W=pathlib.Path(__file__).resolve().parents[1];E=W/'evidence'
def load(p):return json.loads((E/p).read_text())
def save(p,x):(E/p).write_text(json.dumps(x,indent=2)+'\n')
r=load('regression-results.json');grade=load('grader-report.json');ui=load('render/rendering.json');scroll=load('scroll-results.json')
assert r['passed'] and ui['passed'] and scroll['passed']
assert grade['accepted_checks']==18 and grade['rejected_checks']==72 and grade['database_writes']==0
positions=[]
for c in ui['cases']:
 markers=re.findall(r'(Incorrect choice left unselected\.|Correct choice selected\.)',c['text']);assert len(markers)==5
 positions.append({'case':c['index']+1,'correct_display_position':markers.index('Correct choice selected.')+1,'passed':c['passed']})
assert len({c['correct_display_position']for c in positions[:5]})>1
save('ui-position-results.json',{'cases':positions,'batch_display_position_counts':dict(collections.Counter(c['correct_display_position']for c in positions[:5])),'limitations':'Actual UI shuffles authored choices. This finite eight-record sample varies answer positions; mathematical bank-role witnesses independently cover numeric-order strategies.'})
m=json.loads((W/'package.json').read_text());assert all((W/p).is_file()for p in m['files'])
save('runtime-hashes.json',{p:hashlib.sha256((W/p).read_bytes()).hexdigest()for p in m['files']})
source=load('source-replay.json');a=load('retained-bank-strategy.json')
save('final-validation.json',{'fidelity':{'passed':source['complete_banks']==15,'complete_banks':source['complete_banks'],'choices':source['matched_choices'],'distractors':source['matched_distractors']},'correctness':{'passed':r['passed'],'independent_visible_record_math_checks':r['math_checks']},'grading':{'accepted':grade['accepted_checks'],'rejected':grade['rejected_checks'],'unresolved':grade['documented_unresolved_checks']},'decision_variation':{'passed':load('shortcut-results.json')['after']['all_tested_shape_groups_vary'],'exact_old_bank_correct_values':[2,3],'old_rule_regenerated_batch':a['stages']['batch_delivered'],'same_pool_before_after_delivery':'shortcut-results.json','normal_semantic_coverage':load('pedagogical-variation.json')['coverage']},'rendering':{'passed':ui['passed'],'cases':len(ui['cases']),'visual_inspection':'visual-inspection.json','wide_math_scroll_verified':scroll['passed']},'packaging':load('packaging.json'),'inventory':load('inventory-audit.json'),'limitations':['No live learner policy/history or future generated entity IDs supplied; no particular learner sequence is asserted.','Wide three-vector solution displays use the existing horizontal math scroll container.','Finite shortcut probes do not exhaust every possible strategy. No tested template or bank shape fixes the correct numeric position.'],'database_writes':0,'published':False})
print(json.dumps({'source_banks':source['complete_banks'],'math_checks':r['math_checks'],'grader_checks':grade['accepted_checks']+grade['rejected_checks'],'rendered_cases':len(ui['cases']),'passed':True}))
