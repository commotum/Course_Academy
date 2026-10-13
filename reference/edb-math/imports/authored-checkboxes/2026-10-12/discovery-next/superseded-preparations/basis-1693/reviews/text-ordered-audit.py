import json,re,collections
from pathlib import Path
B=Path('reference/edb-math/imports/authored-checkboxes/2026-10-12/discovery-next');p=B/'reviews/text-cases.json';d=json.load(open(p));scope=d['questions'];phrase=re.compile(r'in (?:which|what) order|order (?:should|do)|left to right|going from|blank spaces|blanks',re.I);matches=[];collisions=[]
for q in scope:
 if phrase.search(q['source_problem']):matches.append(q['id'])
 groups=collections.defaultdict(list)
 for a in q['choice_mapping']:groups[tuple(sorted(a['labels']))].append(a)
 duplicate=[v for v in groups.values()if len(v)>1]
 if duplicate:collisions.append({'id':q['id'],'ma_id':q['ma_id'],'collisions':duplicate})
 if q['ma_id']=='q-48430':
  q['decision']='retain_radio';q['classification']='ordered_blank_completion';q['reason']='The prompt explicitly asks left-to-right placement of parts into two blank spaces. Ordered answers I,II and II,I encode distinct placements but collapse to one checkbox subset. Retain the keyed radio sequence and every ordered distractor.';q['proposed_prompt']=q['source_problem'];q['key_evidence']['independent_proof']='IVT first blank requires continuous; second blank requires f(a) and f(b) inclusively. The correct ordered sequence is I,II. Reversed II,I is different and incorrect. Membership selection cannot preserve this requested order.'
  for a in q['choice_mapping']:a['ordered_labels']=a['labels'];a['labels']=None
  q['correct_labels']=None;q['correct_ordered_labels']=['I','II'];q['atomic_options']=[]
 q['content_repairs']=[r for r in q['content_repairs']if 'before'not in r or r['before']!=r['after']]
d['counts']['decisions']=dict(collections.Counter(q['decision']for q in scope));d['counts']['classes']=dict(collections.Counter(q['classification']for q in scope));d['counts']['atomic_checkbox_fields']=sum(len(q['atomic_options'])for q in scope if q['decision']=='convert');d['counts']['old_choices_mapped']=sum(len(q['choice_mapping'])for q in scope if q['decision']=='convert');d['counts']['content_repair_cases']=sum(bool(q['content_repairs'])for q in scope);d['atomic_truth_semantics']='truth means satisfies the requested selection predicate, including false-statement or negative-property questions.'
audit={'scope':len(scope),'exact_placement_phrase_matches':matches,'colliding_unordered_subsets':collisions,'embedded_field_flags_reviewed':26,'retained_ordered_question_ids':matches,'conclusion':'Only q-48430 requests ordered placement. Remaining 26 embedded layout flags are nested set/derivative/operator mathematics, not multi-blank ordered-response fields.'};(B/'reviews/text-ordered-response-audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n');print(d['counts']);print(audit)
