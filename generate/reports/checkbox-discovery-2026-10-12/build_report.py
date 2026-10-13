"""Adjudicate structural signals without changing questions or their keys."""
import collections,csv,importlib.util,json,re
from pathlib import Path
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('screen',OUT/'screen.py');screen=importlib.util.module_from_spec(spec);spec.loader.exec_module(screen)
s=json.loads((OUT/'screening.json').read_text());inventory=json.loads((OUT/'inventory.json').read_text())
strong=[];secondary=[];review=[];excluded=[]
canonical={row[0]for row in json.loads((OUT/'canonical-membership.json').read_text())}if (OUT/'canonical-membership.json').exists()else set()
solution_checked=set(json.loads((OUT/'solution-checked.json').read_text()))if (OUT/'solution-checked.json').exists()else set()
solution_ids=set(json.loads((OUT/'solution-presence.json').read_text()))if (OUT/'solution-presence.json').exists()else None
def comparison_shortcut(p):
 bodies=re.findall(r'(?m)^\s*(?:-\s+|[1-9][.)]\s+|(?:III|II|I)[.)]\s+)([^\n]+)',p)
 bodies=[v.strip().strip('$').strip()for v in bodies]
 return len(bodies)==3 and set(bodies)=={'>','<','='}
def flags(q):
 fs=q['fields'];out=[]
 if q['id']in canonical:out.append('also_used_as_canonical_example')
 if solution_ids is not None and q['id']in solution_checked and q['id']not in solution_ids:out.append('no_stored_worked_solution')
 if len(fs)!=1:out.append('missing_answer_fields'if not fs else 'duplicate_or_multiple_fields')
 if any(':answer-field/correct'not in f for f in fs):out.append('missing_stored_key')
 if q['image']:out.append('image_based_case_list_requires_inspection')
 if any(isinstance(v,list)and len(v)!=len(set(v))for v in q['parsed_subsets']):out.append('repeated_label_in_source_option')
 if any(screen.subset(a.get(':answer/value','')) is None for f in fs for a in f.get(':answer-field/choices',[])):out.append('not_all_options_are_label_subsets')
 if any(f.get(':answer-field/correct',{}).get(':db/id')not in {a[':db/id']for a in f.get(':answer-field/choices',[])}for f in fs if ':answer-field/correct'in f):out.append('correct_ref_outside_owned_bank')
 return out
for bucket,qs in s['buckets'].items():
 for original in qs:
  q=dict(original);p=q['problem'];q['review_flags']=flags(q)
  parsed=q['parsed_subsets'];is_combo=any(isinstance(v,list)and len(v)>1 for v in parsed)
  generic_none_all=re.search(r'\b(?:none|all|not continuous on any)\b',' '.join(v for v,parsed_value in zip(q['values'],parsed)if parsed_value is None),re.I)
  if re.search(r'\bin which quadrant|\bwhich quadrant does',p,re.I):
   q['decision_reason']='One mutually exclusive quadrant classification, not a set of selections.';excluded.append(q);continue
  if comparison_shortcut(p):
   q['decision_reason']='The three displayed relations >, = and < are mutually exclusive; radio is suitable.';excluded.append(q);continue
  if bucket=='subset_banks' or (bucket=='combined_prose'and is_combo and sum(v is not None for v in parsed)>=len(parsed)-2 and generic_none_all):
   q['recommendation']='checkbox';q['confidence']='strong structural candidate';q['decision_reason']='Response bank encodes subsets of independently labeled statements or objects.'
   if re.search(r'\{\{[^}]+\}\}',p):q['review_flags'].append('embedded_field_layout_requires_review')
   strong.append(q);continue
  if bucket=='set_values':
   keyvals=[f.get(':answer-field/correct',{}).get(':answer/value','')for f in q['fields']]
   if any(re.search(r'^Any\b|\ball (?:real )?(?:values|numbers)|\bevery (?:real )?(?:value|number)',v,re.I)for v in keyvals):
    q['decision_reason']='Stored correct answer denotes an unrestricted set; retain radio.';excluded.append(q);continue
   titles=' '.join(k['title']for k in q['kps'])
   finite=re.search(r'\broots?\b|\bcritical points?\b|\bstationary points?\b|\bpoints of discontinuity\b|\basymptotes?\b|\bpoints.*(?:not differentiable|gradient vanishes|horizontal|vertical|perpendicular)|\b(?:like terms|prime|composite)\b',titles,re.I)
   numeric_solutions=re.search(r'\b(?:solve|solving|solutions|possible values)\b',titles+' '+p,re.I) and re.search(r'\b(?:equation|unknown|polynomial|absolute value|determinant|minor)\b',titles+' '+p,re.I)
   ordered=re.search(r'from (?:left to right|top to bottom)|quotient.*remainder|lengths? of (?:the )?(?:major|minor)',p,re.I)
   assigned={v for value in keyvals for v in re.findall(r'\b([a-z])\s*(?:=|\\approx)',value)}
   ordered=ordered or len(assigned)>1
   if (finite or numeric_solutions) and not re.search(r'inequalit|ranges? of|intervals?|multiplicit|coefficient|completing|negating|conditional|conjunction|disjunction|general solution|fundamental solution|inhomogeneous|matrix differential equation|BVP|Classifying the Equilibrium',titles,re.I) and not ordered:
    q['recommendation']='consider checkbox with authored atomic options';q['confidence']='secondary';q['decision_reason']='Finite values, points or objects are bundled into radio alternatives; atomic options must be constructed and checked.';secondary.append(q);continue
   # Explicitly named case labels sometimes contain subscripts, e.g. P_1/P_2.
   if re.search(r'which of (?:the |these )?(?:following|given)|to which of',p,re.I) and (len(q['listed_labels'])>=2 or re.search(r'\$[A-Z]_(?:\{)?[1-9]', ' '.join(q['values']))):
    q['recommendation']='possible checkbox';q['confidence']='requires semantic review';q['decision_reason']='Selection over listed cases, but option atoms need extraction.';review.append(q);continue
   q['decision_reason']='A conjunction alone does not establish a subset response; ordinary formula/tuple/classification may be appropriate.';excluded.append(q);continue
  if bucket=='listed_or_selection'and not q['fields'] and (len(q['listed_labels'])>=2 or len(re.findall(r'(?m)^\s*-\s+',p))>=2) and re.search(r'which.*(?:true|false|satisf|following)|identify.*(?:following|all)',p,re.I|re.S):
   q['recommendation']='likely checkbox; recover source fields/key first';q['confidence']='requires semantic review';q['decision_reason']='Fieldless question explicitly lists independently assessable cases.';review.append(q);continue
  q['decision_reason']='Broad wording signal only; not enough evidence to recommend a format change.';excluded.append(q)
def grouped(qs):
 groups=collections.defaultdict(list);metadata={}
 for q in qs:
  for k in q['kps']:groups[k['id']].append(q);metadata[k['id']]=k
 return [{**metadata[kid],'candidate_questions':len(rows),'question_ids':[q['id']for q in rows],'ma_ids':[q['ma_id']for q in rows]}for kid,rows in sorted(groups.items(),key=lambda kv:(-len(kv[1]),kv[0]))]
report={**inventory,'scope':'All KP-attached practice questions, not only scheduler-selected KPs. Canonical-only examples and already-all-checkbox questions are excluded. Existing blank formats are retained.',
 'method':'Read-only structural screen at one EDB basis. Combination banks provide strong answer-format evidence. This is not independent mathematical verification of all stored keys or inspection of every image; flags identify work needed before a migration.',
 'counts':{'strong_candidates':len(strong),'strong_candidate_kps':len(grouped(strong)),'secondary_finite_set_candidates':len(secondary),'secondary_candidate_kps':len(grouped(secondary)),'additional_semantic_review':len(review),'screened_false_positive_or_insufficient_signals':len(excluded),'already_checkbox_questions':s['field_shapes'].get(':answer-field.type/checkbox',0)},
 'strong_candidates':strong,'strong_kps':grouped(strong),'secondary_candidates':secondary,'secondary_kps':grouped(secondary),'additional_review':review,'excluded_screen_matches':excluded,'field_shapes':s['field_shapes']}
report['source_review_flags']={flag:sum(flag in q['review_flags']for q in strong)for flag in sorted({f for q in strong for f in q['review_flags']})}
previous=json.loads((OUT.parents[1]/'runs/checkbox-audit-2026-10-12/report.json').read_text())
previous_kps={k['db/id']for k in previous['direct_candidates']}|{k['db/id']for k in previous['secondary_candidates']}
report['previous_audit_overlap']={'remaining_strong_candidates_in_previously_audited_kps':sum(any(k['id']in previous_kps for k in q['kps'])for q in strong)}
(OUT/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
with (OUT/'candidates.csv').open('w')as f:
 writer=csv.writer(f);writer.writerow(['tier','question_eid','ma_id','kp_eid','kp_title','topic_eids','topic_titles','current_field_types','correct_values','review_flags'])
 for tier,qs in (('strong',strong),('secondary',secondary),('review',review)):
  for q in qs:
   for k in q['kps']:
    writer.writerow([tier,q['id'],q['ma_id'],k['id'],k['title'],';'.join(str(t[':db/id'])for t in k['topics']),';'.join(t[':topic/title']for t in k['topics']),';'.join(f[':answer-field/type'][':db/ident']for f in q['fields']),';'.join(f.get(':answer-field/correct',{}).get(':answer/value','MISSING')for f in q['fields']),';'.join(q['review_flags'])])
md=['# Checkbox candidates at math basis 1534','',f"Read-only scan of {inventory['practice_questions']:,} practice questions across {inventory['knowledge_points']:,} KPs. {report['counts']['already_checkbox_questions']} questions already use checkbox fields. No database changes.",'',f"Found {len(strong):,} strong structural candidates across {len(grouped(strong))} KPs, plus {len(secondary):,} secondary finite-set candidates and {len(review):,} cases needing semantic/source review.",'','Strong candidates use combination banks such as I and III only. Secondary candidates bundle roots/points/objects and need authored atomic options. These counts are a discovery shortlist, not a transaction-ready or independently mathematically verified migration. Image case lists, missing keys, duplicate fields and malformed labels require review. Database keys take precedence over local study keys. Ordered tuples, unrestricted all-values answers and mutually exclusive classifications are excluded.','', 'Review flags on strong candidates: '+', '.join(flag+'='+str(n)for flag,n in report['source_review_flags'].items())+'. No strong candidates remain on KPs included in our previous audit.','', 'Full question IDs, prompts, field structures, keys, KP/topic membership and exclusions: report.json. Flat membership listing: candidates.csv. Original bounded EDB reads: evidence/ and sources/.','','## Strong candidates by KP','','| KP ID | Knowledge point | Questions | Topic |','|---|---|---:|---|']
for k in report['strong_kps']:md.append(f"| {k['id']} | {k['title'].replace('|','/')} | {k['candidate_questions']} | {', '.join(t[':topic/title']for t in k['topics']).replace('|','/')} |")
md+=['','## Secondary finite-set candidates by KP','','| KP ID | Knowledge point | Questions |','|---|---|---:|']
for k in report['secondary_kps']:md.append(f"| {k['id']} | {k['title'].replace('|','/')} | {k['candidate_questions']} |")
(OUT/'report.md').write_text('\n'.join(md)+'\n');print(json.dumps(report['counts'],indent=2))
