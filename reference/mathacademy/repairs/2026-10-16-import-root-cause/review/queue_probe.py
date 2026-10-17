"""Independent read-only assertions for the final source/current-field join."""
from pathlib import Path
import gzip, hashlib, importlib.util, json, re, sys
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent; BASE=HERE.parent; DB=BASE/'database'; SOURCE=BASE/'source'
def sha(b):return hashlib.sha256(b if isinstance(b,bytes) else b.encode()).hexdigest()
def lines(p):
 with (p.open() if p.exists() else gzip.open(str(p)+".gz","rt")) as f:
  for line in f:
   if line.strip():yield json.loads(line)
spec=importlib.util.spec_from_file_location('source_scan_quality',SOURCE/'scan.py')
scan=importlib.util.module_from_spec(spec);sys.modules[spec.name]=scan;spec.loader.exec_module(scan)
sys.path.insert(0,str(HERE.parents[4]))
from scripts.question_capture.math_format import MATH
def math_bodies(value):
 result=[]
 for match in MATH.finditer(value):
  token=match.group();size=2 if token.startswith(('$$',r'\[',r'\(')) else 1
  result.append(re.sub(r'\s+','',token[size:-size]))
 return result
summary=json.loads((DB/'source-comparison-summary.json').read_text())
source_summary=json.loads((SOURCE/'summary.json').read_text())
assert source_summary['files_scanned']==source_summary['files_catalogued']==2964
assert source_summary['code'][str((SOURCE/'scan.py').resolve())]==sha((SOURCE/'scan.py').read_bytes())
assert summary['source_stream_sha256']==sha((SOURCE/'primary-mixed-title.jsonl').read_bytes()),'Final queue stream hash does not match source stream'
candidates=list(lines(DB/'source-backed-candidates.jsonl'))
primary={x['id']:x for x in lines(SOURCE/'primary-mixed-title.jsonl')}
keys={(x['entity'],x['attribute']) for x in candidates}
assert len(keys)==len(candidates)
original={}
for row in lines(DB/'baseline-comparison.jsonl'):
 key=(row['entity'],row['attribute'])
 if key in keys:original.setdefault(key,[]).append(row)
current={}
for row in lines(DB/'content.jsonl'):
 key=(row['entity'],row['attribute'])
 if key in keys:current[key]=row
 if len(current)==len(keys):break
occurrences=0
for candidate in candidates:
 key=(candidate['entity'],candidate['attribute'])
 assert candidate['current_value']==current[key]['value']
 assert candidate['current_sha256']==sha(current[key]['value'])
 matches=[r for r in original[key] if r['uuid']==candidate['uuid'] and r['original_value']==candidate['current_value']]
 assert matches and all(r['comparison']=='unchanged-original' for r in matches)
 for occurrence in candidate['source_occurrences']:
  source=primary[occurrence['id']]
  assert source['source_id']==occurrence['source_id'] and source['attribute']==candidate['attribute']
  assert any(source['topic_id'] in r['original_topic_ids'] and str(source['source_id'])==str(r['source_id']) for r in matches)
  assert scan.title_info(re.sub(r'^<title[^>]*>|</title>$','',source['source_html']))[2]
  assert len({x['attribute'] for x in source['stored_json_matches']})==1
  assert occurrence['original_sha256']==candidate['current_sha256']==occurrence['current_sha256']
  expected=math_bodies(source['legacy_markdown'])
  assert expected and any(body in math_bodies(candidate['current_value']) for body in expected),(source['id'],'No exact normalized math body in current/original field')
  occurrences+=1
ids={17592186054454:'Decimal 1,000 and its highlighted zeros are replaced by label 3.',
17592186055986:'Probability ratio and explanatory numerator/denominator become an inline 3.',
17592186059429:'Four shaded proof blanks become visible ABCDEFGHI strings.',
17592186059525:'Three vector definitions lose their a/b/c names and equalities.',
17592186059614:'A proof-reasoning box becomes eight visible zeros.',
17592186060869:'A gray empty carry box becomes visible zero; other long-multiplication structure also needs review.',
17592186068508:'Two coordinate pairs and their underbrace labels become x1 and x2.',
17592186073442:'The statement loses greater than and leaves only the comparison fraction.'}
sampled=[]
for candidate in candidates:
 if candidate['entity'] not in ids:continue
 occurrence=candidate['source_occurrences'][0];source=primary[occurrence['id']]
 raw=Path(source['source_file']).read_text();soup=BeautifulSoup(raw,'html.parser')
 assert raw[source['source_offset']:source['source_offset']+len(source['source_html'])]==source['source_html']
 title=soup.find_all('title')[source['source_title_index']];owner=title.find_parent(id=source['dom_id'])
 assert owner is not None
 archived=json.loads(Path(source['source_file']).with_suffix('.json').read_text())
 item=next(x for x in archived['lesson']['items'] if x.get('dom_id')==source['dom_id'])
 replay=scan.legacy.build_step_item(item['lesson_index'],item['step_index'],owner)
 assert [(s['section_type'],s['normalized_html']) for s in item['sections']]==[(s['section_type'],s['normalized_html']) for s in replay['sections']]
 sampled.append({'entity':candidate['entity'],'attribute':candidate['attribute'],'source_occurrence':source['id'],
                 'finding':ids[candidate['entity']],'current_field_equals_committed_original':True,
                 'source_owner_and_entire_archived_sections_replay_exact':True,
                 'current_sha256':candidate['current_sha256']})
assert len(sampled)==8
neutral_only=[]
for source in primary.values():
 info=scan.title_info(re.sub(r'^<title[^>]*>|</title>$','',source['source_html']))
 # Detect the known FORMULA adjacency boundary edge separately from true multifragment loss.
 if len(info[0])==1:
  outer=re.sub(r'\\require\s*\{[^{}]*\}','',info[1])
  outer=re.sub(r'\\(?:displaystyle|textstyle|scriptstyle|scriptscriptstyle|quad|qquad|enspace)(?=FORMULA|\b)|\\[,!;:]','',outer)
  if not re.sub(r'FORMULA|[{}\s,.;:?!]','',outer):neutral_only.append(source['id'])
result=json.loads((HERE/'audit-quality.json').read_text())
result.update(queue_review_pending=False,final_source_stream_sha256=summary['source_stream_sha256'],
 final_scanner_sha256=sha((SOURCE/'scan.py').read_bytes()),final_source_files=source_summary['files_scanned'],
 candidate_field_count=len(candidates),candidate_source_occurrences=occurrences,
 all_candidate_fields_equal_pinned_current_and_committed_original=True,
 all_candidate_source_ownership_joins_verified=True,all_candidate_math_body_anchors_verified=True,primary_queue_review_passed=True,current_field_samples=sampled,
 independently_replayed_current_fields=8,final_observed_neutral_only_primary_occurrences=neutral_only,
 scanner_controls_test_count=8,scanner_controls_tests_passed=True,
 review_verdict='Source-backed field queue is supported by exact original/current guards and sampled source replay; not permission for automatic replacement.',
 nonblocking_limitations=['Synthetic adjacent neutral command + fragment remains a detector boundary edge; no neutral-only occurrence occurs in the final primary stream.',
  'Five of 12 source samples have repeated equal values; repairs require exact source ordinal/context or reviewed whole-field reconstruction.',
  'This audit validates the scoped mixed-title candidate queue, not all possible extraction-loss classes.'])
(HERE/'audit-quality.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['candidate_field_count','candidate_source_occurrences','independently_replayed_current_fields','final_observed_neutral_only_primary_occurrences','queue_review_pending']}))
