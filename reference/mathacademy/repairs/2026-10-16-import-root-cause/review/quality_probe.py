"""Focused independent scanner QA. Does not run/modify the global scanner."""
import hashlib, importlib.util, json, sys
from pathlib import Path
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'source'
spec=importlib.util.spec_from_file_location('reviewed_source_scan',SOURCE/'scan.py')
scan=importlib.util.module_from_spec(spec);sys.modules[spec.name]=scan;spec.loader.exec_module(scan)
rows={r['id']:r for line in (SOURCE/'primary-mixed-title.jsonl').read_text().splitlines() if (r:=json.loads(line))}
samples=[
 ('29:step-16079:42999','two-matrix definition','loss','Assignment labels and second matrix are outside the retained first fragment.'),
 ('36:step-2595:235911','series label-only','loss','The full series expansion was reduced to the n inside an underbrace label.'),
 ('36:step-2595:252203','repeated same-value fragment','loss','Derivative series also became n; its replacement differs from the previous n in this same solution.'),
 ('49:step-152907:58056','ordered pairs and matrix tuple','loss','Other ordered-pair examples and the second matrix disappear; parentheses carry tuple structure.'),
 ('60:step-153495:103948','logical proposition/nonmatrix','loss','Proposition label S and divisibility statement are outside the first 14 fragment.'),
 ('68:step-5178:124054','nonvisual package directive','not_mixed_title_loss','Only require{cancel} surrounds the complete first equation; no visible cancellation exists here.'),
 ('68:step-5178:135383','cancellation steps','other_structural_loss','Require-only wrapper is not mixed-title loss, but explicit strike marks and multirow layout are lost by MathML conversion.'),
 ('110:step-174239:246439','decorated decimal label','loss','Value 1,000 and the highlighted underbrace are replaced with label digit3.'),
 ('148:step-17169:45467','outer system fence','loss','The left system brace surrounding a multirow equation fragment is omitted.'),
 ('155:step-16480:103370','three-matrix product','loss','Two further matrix factors/results and equality are omitted.'),
 ('254:step-182699:403486','proof blank/decorated phantom','loss','Source fbox around invisible-width sample becomes eight visible zeros; this is not an authored numeric answer.'),
 ('1358:step-20040:394842','punctuation-only wrapper','punctuation_only','Full matrix survives; only a trailing question mark is omitted. Exclude from mathematical truncation count.'),
]
# Keep review examples once selected, even if corrected final scanner drops them.
cache=HERE/'sample-records.json'
if cache.exists():
 rows={**{r['id']:r for r in json.loads(cache.read_text())},**rows}
selected=[]
for ident,category,verdict,note in samples:
 r=rows[ident]
 raw=Path(r['source_file']).read_text()
 assert raw[r['source_offset']:r['source_offset']+len(r['source_html'])]==r['source_html']
 assert hashlib.sha256(r['source_html'].encode()).hexdigest()==r['source_sha256']
 soup=BeautifulSoup(raw,'html.parser')
 title=soup.find_all('title')[r['source_title_index']]
 owner=title.find_parent(id=r['dom_id'])
 assert owner is not None, (ident,'wrong DOM owner')
 wrapper=title.find_parent(class_='mjpage') or title.find_parent('mjx-container')
 # Use the outer formula container when nested CHTML appears in its SVG title.
 archived=json.loads(Path(r['source_file']).with_suffix('.json').read_text())
 archived_owner=next(x for x in archived['lesson']['items'] if x.get('dom_id')==r['dom_id'])
 replayed_owner=scan.legacy.build_step_item(archived_owner['lesson_index'],archived_owner['step_index'],owner)
 archived_sections=[(x['section_type'],x['normalized_html']) for x in archived_owner['sections']]
 replayed_sections=[(x['section_type'],x['normalized_html']) for x in replayed_owner['sections']]
 assert archived_sections==replayed_sections,(ident,'whole owner JSON replay mismatch')
 actual=scan.legacy.extract_math_from_node(wrapper)[0]
 assert actual==r['legacy_text'], (ident,'legacy replay mismatch',actual,r['legacy_text'])
 actual_attr=':tutorial/content'
 if r['kind']=='question':
  actual_attr=':question/worked-solution' if title.find_parent(class_='exampleExplanation') else ':question/problem'
 assert r['attribute']==actual_attr,(ident,'field attribution mismatch',actual_attr,r['attribute'])
 alternatives=[x for x in r['stored_json_matches'] if x['attribute']==actual_attr]
 assert alternatives,(ident,'no archived field match')
 selected.append({'id':ident,'category':category,'verdict':verdict,'finding':note,'source_hash_verified':True,
                  'actual_dom_owner_verified':True,'whole_owner_archived_sections_replay_exact':True,'actual_legacy_extractor_replay_verified':True,
                  'source_attribute':actual_attr,'archived_same_value_matches_in_attribute':len(alternatives),
                  'occurrence_to_json_position_unique':len(alternatives)==1,
                  'outer_template':next(x['discarded_outer_template'] for x in r['mechanisms'] if x['code']=='mixed-title-first-fragment')})
cache.write_text(json.dumps([rows[x[0]] for x in samples],indent=2)+'\n')
one='<mjx-container><mjx-assistive-mml><math><mn>7</mn></math></mjx-assistive-mml></mjx-container>'
controls=[]
for key,content,expected in [
 ('complete_pure_tex',r'A=\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}',False),
 ('single_html_punctuation','<span> , '+one+'</span>.',False),
 ('single_question_punctuation',one+'?',False),
 ('require_only',r'\require{cancel}'+one,False),
 ('neutral_spacing',r'\qquad'+one,False),
 ('actual_assignment','A='+one,True),
 ('two_independent_fragments',one+' '+one,True),
 ('literal_fence','('+one+')',True),
]:
 actual=scan.title_info(content)[2]
 controls.append({'case':key,'expected_mixed_loss':expected,'actual_mixed_loss':actual,'passed':actual==expected})
result={'read_only':True,'reviewed_occurrences':len(selected),'samples':selected,'negative_and_positive_controls':controls,
        'scanner_sha256':hashlib.sha256((SOURCE/'scan.py').read_bytes()).hexdigest(),
        'controls_passed':all(x['passed'] for x in controls),
        'queue_review_pending':True,
        'critical_findings':['Nonvisual require-only wrappers and punctuation-only wrappers must not be confirmed mathematical truncation.',
         'Exact value matches identify candidate fields, not unique formula positions. Multiple occurrences need source ordinal/context before repair.'],
        'repair_boundary':'Do not globally replace a legacy formula string; regenerate a reviewed whole field or bind each exact source occurrence/ordinal.',
        'scan_run_boundary':'Review samples may originate from checkpoint stream. Final queue must use final code-hashed stream after controls settle.'}
(HERE/'audit-quality.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'reviewed_occurrences':len(selected),'ambiguous_same_value_samples':sum(not x['occurrence_to_json_position_unique'] for x in selected),
                  'controls_passed':result['controls_passed'],'failed_controls':[x['case'] for x in controls if not x['passed']]}))
