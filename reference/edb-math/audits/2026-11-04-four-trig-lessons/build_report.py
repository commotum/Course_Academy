"""Bind the critical findings to every captured question and generator."""
import collections,json,re
from pathlib import Path
H=Path(__file__).resolve().parent
rows=json.loads((H/'question-ledger.json').read_text());kps=json.loads((H/'kps.json').read_text());capture=json.loads((H/'capture.json').read_text())
reviews={
17592186059665:('repair','Keep unhinted shift simplification. Easy gives away both identity and exact values; moderate includes full-turn and near-duplicate variants. Non-axis hard is substantially source-aligned.',[17592186714557,17592186714906,17592186714886]),
17592186059666:('repair','Easy/moderate decomposition hints match the imports. Hard reverses an expanded identity, removes the decomposition, then expands again; no imported hard anchor supports that synthesis task.',[17592186715337,17592186233854]),
17592186059821:('repair','Easy axis shifts and moderate non-axis shifts match imports. Hard invents weighted pairs of cosine expansions; some phase-equivalent pairs collapse to one ordinary shift. Also avoid negative entries after a printed minus.',[17592186715695,17592186715668,17592186272274]),
17592186059662:('repair','Easy/moderate are largely aligned. Hard invents sums/differences of two shifted sines and mixed-radical coefficient collection without imported hard anchors. One moderate frame adds unnecessary double negation.',[17592186701660,17592186701793,17592186304991]),
17592186059663:('retain_with_checks','Good distinction: supplied decomposition in easy/moderate, independent decomposition in hard is directly supported by imported hard q-119007. Preserve one forward identity application; do not add the cosine hard wrapper.',[17592186253530,17592186705148,17592186233846]),
17592186059820:('repair','Easy supplies the identity and both exact values although no easy import does so. Moderate axis and hard non-axis tasks are mostly appropriate. Renaming-only repeats and one imported solution angle typo need attention.',[17592186701792,17592186705223,17592186272322]),
17592186059671:('review_extension','Direct easy practice is useful. Moderate sometimes names the resulting sine/doubled angle in the prompt. Quartic hard requires factoring/Pythagorean recognition: plausible transfer, but no hard imported anchor establishes its calibration.',[17592186695676,17592186695694,17592186253624]),
17592186059672:('repair','Easy states the identity and both substitutions in sequence, giving away the skill. Moderate drops the reciprocal-cancellation family (five of six moderate imports) even though a constructor branch exists. Reciprocal hard families are source-supported.',[17592186696011,17592186696466,17592186233282,17592186696009]),
17592186059673:('retain_with_checks','Strongest alignment: students must independently select the doubled-angle rewrite, cancel/rewrite ratios, and use source-supported factoring in hard. Difficulty overlap between a source easy cotangent quotient and generated moderate deserves calibration, not a blanket reduction.',[17592186696490,17592186253633,17592186335851]),
17592186059674:('retain_with_source_repair','Generated product/square/reciprocal families match the source progression; guidance stays in the solution. One partial imported question ends its worked solution with the wrong sign in the original expression.',[17592186696379,17592186696501,17592186233281]),
17592186087669:('review_extension_and_source_repair','Easy direct and moderate common-factor recognition are aligned. Quartic hard adds difference-of-squares/Pythagorean work without imported hard anchors. Bank-first angle ladders create clustered variants. Two imported radio banks have valid alternatives marked wrong.',[17592186698882,17592186703441,17592186088094,17592186290550]),
17592186087670:('repair','Easy/moderate alternatives and common-factor recognition match imports. Hard invents quartic regrouping and a second double-angle application, anchored to a generated prototype. A source bank is ambiguous and another needs a response-form caveat.',[17592186698910,17592186703559,17592186598566,17592186345265]),
17592186087671:('retain_with_sampling_guard','The expanded-perfect-square hard family is genuinely imported. However, the only stored generated hard question uses a known 135-degree angle and evaluates directly to zero, bypassing the target identity; exclude or deliberately limit these cases. Source operator notation also needs repair.',[17592186702810,17592186292878,17592186304990,17592186304985]),
}

findings=[
('F01','high','Method and prerequisite values supplied in ordinary easy practice',lambda r:r['origin']=='generated' and r['band']=='easy' and r['kp'] in [17592186059665,17592186059820,17592186059672]),
('F02','high','Hard exact-cosine family adds reverse recognition and unsupplied decomposition',lambda r:r['origin']=='generated' and r['band']=='hard' and r['kp']==17592186059666),
('F03','high','Unanchored two-expansion degree-shift hard families',lambda r:r['origin']=='generated' and r['band']=='hard' and r['kp'] in [17592186059662,17592186059821]),
('F04','high','Alternative-cosine hard invents quartic regrouping and repeated application',lambda r:r['origin']=='generated' and r['band']=='hard' and r['kp']==17592186087670),
('F05','review','Unanchored factoring extensions require explicit calibration, not automatic rejection',lambda r:r['origin']=='generated' and r['band']=='hard' and r['kp'] in [17592186059671,17592186087669]),
('F06','medium','Response frame requires a negative coefficient after a printed minus',lambda r:r['entity'] in [17592186715668,17592186701793]),
('F07','medium','Hard cosine pair is phase-equivalent and reduces to one shift',lambda r:r['entity']==17592186715695),
('F08','high','Stored generated hard question bypasses the target identity at a known angle',lambda r:r['entity']==17592186702810),
('F09','medium','Moderate prompt supplies the resulting sine/doubled-angle form',lambda r:r['entity'] in [17592186695676,17592186696247]),
('F10','critical','Imported radio bank marks another valid single-cosine answer incorrect',lambda r:r['entity'] in [17592186088094,17592186290550,17592186598566]),
('F11','high','Imported solution contains a false sign/angle equality',lambda r:r['entity'] in [17592186233281,17592186272322]),
('F12','review','Imported value-equivalent distractors require interpreting the single-ratio response contract',lambda r:r['entity']==17592186345265),
]
clusters=json.loads((H/'renaming-only-clusters.json').read_text())['groups'];duplicates={eid for g in clusters for eid in g}
findings.append(('F13','medium','Repeated mathematical inputs after variable renaming',lambda r:r['entity'] in duplicates))
notation={r['question'] for r in json.loads((H/'notation-findings.json').read_text()) if 'question' in r}
findings.append(('F14','medium','Residual imported named-function notation loss',lambda r:r['entity'] in notation))
ledger=[];summary=[]
for r in rows:
    marks=[{'finding':fid,'severity':severity,'description':title} for fid,severity,title,rule in findings if rule(r)]
    ledger.append({**{k:v for k,v in r.items() if k not in ('prompt','solution','keys')},'findings':marks,'response_key_status':'complete' if r['key_complete'] else 'not_applicable_to_canonical' if r['role']=='canonical' else 'partial_import','review_scope':'Stored prompt, answer field/key/choices, worked solution when present; evaluated against imported task and registered generator construction.'})
for kid,k in kps.items():
    subset=[r for r in rows if r['kp']==int(kid) and r['role']=='practice'];state,note,evidence=reviews[int(kid)]
    summary.append({'kp':int(kid),'title':k[':knowledge-point/title'],'disposition':state,'analysis':note,'evidence_questions':evidence,'practice_count':len(subset),'imported':sum(r['origin']=='imported' for r in subset),'generated':sum(r['origin']=='generated' for r in subset),'imported_by_band':dict(collections.Counter(r['band'] for r in subset if r['origin']=='imported')),'generated_by_band':dict(collections.Counter(r['band'] for r in subset if r['origin']=='generated'))})
out=[{'id':fid,'severity':severity,'title':title,'affected_stored_questions':[r['entity'] for r in rows if rule(r)]} for fid,severity,title,rule in findings]
out.append({'id':'F15','severity':'medium','title':'Multiple-times moderate sampler never schedules the cancellation family','kp':17592186059672,'source_examples':[17592186233282,17592186253642,17592186290562,17592186345243,17592186345244],'affected_stored_questions':[]})
(H/'question-review.json').write_text(json.dumps(ledger,indent=2)+'\n');(H/'kp-review.json').write_text(json.dumps(summary,indent=2)+'\n');(H/'findings.json').write_text(json.dumps(out,indent=2)+'\n')
numeric=json.loads((H/'numeric-results.json').read_text());sol=json.loads((H/'solution-results.json').read_text());probes=json.loads((H/'generator-probes.json').read_text());renders=json.loads((H/'renders/rendering.json').read_text())
assert len(reviews)==len(kps)==13 and all(r['ok'] for r in probes) and renders['passed']
assert not any(r['status'] in ('mismatch','unparsed') for r in numeric)
assert not any(r.get('unparsed_equalities') for r in sol)
completion={'audit_complete':True,'basis':capture['basis'],'lessons':4,'kps_and_registered_generators':13,'practice_questions':346,'imported_practice':186,'generated_practice':160,'canonical_examples':13,'tutorial_sections':9,'all_stored_questions_and_examples_reviewed':len(ledger),'runtime_cli_calls':len(probes),'runtime_records_checked':sum(r.get('records',0) for r in probes),'runtime_failures':0,'stored_complete_keys_checked':sum(r['status']=='match' and r['label'].isdigit() for r in numeric),'runtime_keys_checked':sum(r['status']=='match' and not r['label'].isdigit() for r in numeric),'solution_equality_numeric_checks':sum(r['checks'] for r in sol),'manually_confirmed_wrong_source_solutions':2,'source_radio_banks_with_live_rejected_valid_alternative':3,'ui_cases_rendered':len(renders['cases']),'overscaffolded_stored_easy_questions':sum(len(f['affected_stored_questions']) for f in out if f['id']=='F01'),'imported_easy_anchor_gaps':[s['kp'] for s in summary if not s['imported_by_band'].get('easy')],'imported_hard_anchor_gaps':[s['kp'] for s in summary if not s['imported_by_band'].get('hard')],'source_evidence_limitations':{'practice_without_complete_key':sum(r['role']=='practice' and not r['key_complete'] for r in rows),'missing_stored_solutions':sum(not r['solution_present'] for r in rows),'canonical_response_fields_not_required':True},'no_retired_or_multistep_fragments_in_captured_membership':not json.loads((H/'source-exclusions.json').read_text()),'database_writes':0,'generators_modified':0,'qualification':'Numeric witnesses and representative UI renders supplement construction/pedagogy review; they are not exhaustive symbolic proofs of every possible future generator output.'}
(H/'completion.json').write_text(json.dumps(completion,indent=2)+'\n');print(json.dumps(completion,indent=2))
