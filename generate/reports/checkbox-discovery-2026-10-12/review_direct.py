"""Select straightforward format conversions; preserve the database answer key."""
import collections,importlib.util,json,re,csv
from pathlib import Path
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('screen',OUT/'screen.py');screen=importlib.util.module_from_spec(spec);spec.loader.exec_module(screen)
qs=json.loads((OUT/'direct-format-provisional.json').read_text())
solutions={q[':db/id']:q[':question/worked-solution']for q in json.loads((OUT/'direct-worked-solutions.json').read_text())}
LABEL=r'(?:VIII|VII|VI|IV|III|II|IX|X|V|I|[A-Z])'
LIST=LABEL+r'(?:\s*(?:,\s*(?:and\s+)?|and\s+|&\s*)'+LABEL+r')*'
VERDICT=re.compile(r'\bstatements?\s+('+LIST+r')\s+(?:is|are)\s+(true|false)\b',re.I)
accepted=[];held=[]
for q in qs:
 sol=solutions[q['id']];normal=re.sub(r'\*|\$','',sol)
 labels={a['label']for a in q['atomic_options']};key=set(q['correct_labels']);reasons=[]
 verdicts=collections.defaultdict(set);evidence=[]
 for match in VERDICT.finditer(normal):
  # "Not both statements I and II are true" is not a verdict that each is true.
  if re.search(r'\bnot\s+(?:both\s+|all\s+)?$',normal[max(0,match.start()-30):match.start()],re.I):continue
  named=re.findall(r'\b'+LABEL+r'\b',match.group(1))
  for label in named:verdicts[label].add(match.group(2).lower()=='true')
  evidence.append(match.group(0))
 if set(verdicts)-labels:reasons.append('worked solution names a statement outside the source list')
 if any(len(v)!=1 or (label in key)not in v for label,v in verdicts.items()):reasons.append('worked solution statement verdict conflicts with stored key')
 conclusions=[]
 for match in re.finditer(r'correct answer is\s*,?\s*["\u201c\u2018\']([^"\u201d\u2019\'\n]+)["\u201d\u2019\']',normal,re.I):
  parsed=screen.subset(match.group(1).strip().rstrip('.'))
  if isinstance(parsed,list):conclusions.append((set(parsed),match.group(0)))
 if any(answer!=key for answer,_ in conclusions):reasons.append('worked solution final answer conflicts with stored key')
 complete_verdict=set(verdicts)==labels and all(len(v)==1 for v in verdicts.values())
 # An explicit final subset is sufficient; otherwise require every listed statement to have a verdict.
 if not conclusions and not complete_verdict:reasons.append('worked solution lacks a complete explicit key confirmation')
 if reasons:held.append({'id':q['id'],'ma_id':q['ma_id'],'reasons':reasons,'key':q['correct_labels'],'source_verdicts':{k:list(v)for k,v in verdicts.items()},'solution_tail':sol[-800:]});continue
 bank=[{'answer_eid':a[':db/id'],'value':a[':answer/value'],'labels':screen.subset(a[':answer/value'])}for a in q['fields'][0][':answer-field/choices']]
 assert len({tuple(sorted(a['labels']))for a in bank})==len(bank)
 assert all(not re.search(r'\bor\b',a['value'],re.I)for a in bank)
 accepted.append({**q,'source_key_confirmation':[text for _,text in conclusions]or evidence,'source_choice_to_checked_labels':bank,'worked_solution':sol})
assert len(accepted)+len(held)==len(qs)
report={'database':'math','basis':1534,'database_writes':0,'scope':'Conservative subset of strong practice-question candidates; easy means conversion effort, not difficulty rating.','criteria':['No discovery review flags; exactly one owned, keyed radio field; easy/moderate/hard rating; stored worked solution.','Prompt explicitly asks which statements are true; two to five extractable text statements.','Every radio choice and correct answer map to a finite subset of those statements. No all/none special alternatives or authored mathematical options.','Worked solution explicitly confirms the stored answer or supplies matching verdicts for all statements; no detected conflicting or unknown-label verdict.'], 'verification_limit':'Verifies format and source-key agreement, not independent mathematical correctness of every stored solution. Existing database keys are preserved.','counts':{'selected_questions':len(accepted),'knowledge_points':len({k['id']for q in accepted for k in q['kps']}),'difficulty':dict(collections.Counter(q['difficulty'].split('/')[-1]for q in accepted)),'provisional_questions':len(qs),'held_for_source_review':len(held)},'questions':accepted,'held':held}
(OUT/'direct-candidates.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
with (OUT/'direct-candidates.csv').open('w')as f:
 w=csv.writer(f);w.writerow(['question_eid','ma_id','difficulty','field_eid','correct_labels','kp_eids','kp_titles','topic_titles'])
 for q in accepted:w.writerow([q['id'],q['ma_id'],q['difficulty'].split('/')[-1],q['fields'][0][':db/id'],','.join(q['correct_labels']),';'.join(str(k['id'])for k in q['kps']),';'.join(k['title']for k in q['kps']),';'.join(t[':topic/title']for k in q['kps']for t in k['topics'])])
md=['# Straightforward checkbox conversions','',f"Selected {len(accepted)} questions across {report['counts']['knowledge_points']} KPs at math basis 1534. No database changes.",'','Easy refers to conversion effort; all source difficulty ratings are retained.','',*['- '+x for x in report['criteria']],'',report['verification_limit'],'',f"Held {len(held)} of {len(qs)} provisional questions for source review.",'','## Examples','','| Question ID | MA ID | Knowledge point | Checked labels |','|---|---|---|---|']
for q in accepted[:10]:md.append(f"| {q['id']} | {q['ma_id']} | {q['kps'][0]['title']} | {', '.join(q['correct_labels'])} |")
md+=['','All IDs and memberships: direct-candidates.csv. Exact option text, keys, source choice mappings, and solution confirmation: direct-candidates.json. This is a reviewed format-conversion list, not a transaction.']
(OUT/'direct-candidates.md').write_text('\n'.join(md)+'\n')
print(json.dumps(report['counts'],indent=2))
print('Held reasons:',dict(collections.Counter(reason for q in held for reason in q['reasons'])))
for q in held:
 if any('conflict'in x or 'outside'in x for x in q['reasons']):print(json.dumps(q,ensure_ascii=False))
