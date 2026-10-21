import sys
sys.dont_write_bytecode=True
import json,re,collections,hashlib,importlib.util
from pathlib import Path
from bs4 import BeautifulSoup,Tag
ROOT=Path('/home/jake/Developer/Course_Academy');OUT=Path(__file__).resolve().parent
BRACE=ROOT/'reference/edb-math/repairs/2026-10-17-brace-accent-repair'
AUDIT=ROOT/'reference/edb-math/audits/2026-10-17-underbrace-import'
HATS={'^','ˆ','̂'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
seed=json.loads((BRACE/'preexisting-render-findings.json').read_text())['unchanged_math_errors'];ids=sorted({x['entity']for x in seed})
links=json.loads((AUDIT/'source-trace/source-links.json').read_text());links={x['eid']:x for x in links if x['attribute']==':question/worked-solution'}
changes={x['entity']:x for x in json.loads((BRACE/'changes.json').read_text())if x['attribute']==':question/worked-solution'}
cache={};seeds=[]
for eid in ids:
 link=links[eid];src=link['sources'][0];sid=link['source_identity'];qid=sid.split('-')[1]
 captured=json.loads(Path(src['record_file']).read_text())[src['record_key']][src['record_index']]
 path=Path(captured['solution_evidence'])
 if path not in cache:cache[path]=BeautifulSoup(path.read_text(),'html.parser')
 soup=cache[path];q=soup
 occurrences=[]
 for mover in q.find_all('mover'):
  cs=mover.find_all(recursive=False)
  if len(cs)!=2 or cs[1].get_text().strip()not in HATS:continue
  occurrences.append({'mathml':str(mover),'mover_attrs':mover.attrs,'operator_tag':cs[1].name,'operator_attrs':cs[1].attrs,'glyph':cs[1].get_text().strip(),'base_mathml':str(cs[0]),'original_formula':str(mover.find_parent('math'))})
 captured=json.loads(Path(src['record_file']).read_text())[src['record_key']][src['record_index']]
 imported=captured['worked_solution'];assert imported==changes[eid]['before'],eid
 seeds.append({'entity':eid,'attribute':':question/worked-solution','source_identity':sid,'source_file':str(path),'source_sha256':sha(path),'selector':'complete saved solution modal','capture_record_file':src['record_file'],'capture_record_sha256':sha(Path(src['record_file'])),'capture_record_index':src['record_index'],'exact_saved_import_value_matches_prebrace_text':True,'current_hat_count':changes[eid]['after'].count(r'\overset{^}'),'source_hat_count':len(occurrences),'source_hats':occurrences})
(OUT/'seed-source-proofs.json').write_text(json.dumps(seeds,ensure_ascii=False,indent=2)+'\n')
print('seed',len(seeds),sum(x['source_hat_count']for x in seeds),flush=True)
# Archived lesson original HTML is a second import path: its converter flattens
# mover into base^(glyph). Preserve the source scope even where text lost it.
originals=[];stats=collections.Counter();candidate_pattern=re.compile(r'<mo\b[^>]*>\s*[\^ˆ̂]\s*</mo>',re.S)
for p in sorted(Path('/home/jake/Developer/MA/DATA/Lessons').glob('*/Source/*.html')):
 if p.stem!=p.parent.parent.name:continue
 stats['files_scanned']+=1;s=p.read_text()
 if not candidate_pattern.search(s):continue
 stats['files_with_hat_operator']+=1;soup=BeautifulSoup(s,'html.parser')
 for mover in soup.find_all('mover'):
  cs=mover.find_all(recursive=False)
  if len(cs)!=2 or cs[1].get_text().strip()not in HATS:continue
  owner=next((anc for anc in mover.parents if anc.get('id')and re.match(r'(?:question|step)-',anc['id'])),None)
  originals.append({'file':str(p),'file_sha256':hashlib.sha256(s.encode()).hexdigest(),'topic_id':p.stem,'selector':'#'+owner['id']if owner else None,'glyph':cs[1].get_text().strip(),'operator_tag':cs[1].name,'operator_attrs':cs[1].attrs,'mover_attrs':mover.attrs,'mathml':str(mover),'original_formula':str(mover.find_parent('math'))})
(OUT/'archived-hat-mathml.json').write_text(json.dumps(originals,ensure_ascii=False,indent=2)+'\n')
stats['hat_occurrences']=len(originals);stats['topics_with_hats']=len({x['topic_id']for x in originals});stats['items_with_hats']=len({(x['file'],x['selector'])for x in originals})
summary={'seed_fields':len(seeds),'seed_source_hat_occurrences':sum(x['source_hat_count']for x in seeds),'seed_stored_hat_occurrences':sum(x['current_hat_count']for x in seeds),'seed_all_exact_saved_import_matches':all(x['exact_saved_import_value_matches_prebrace_text']for x in seeds),'seed_all_source_counts_match_stored':all(x['source_hat_count']==x['current_hat_count']for x in seeds),'seed_operator_forms':dict(collections.Counter(json.dumps(x['operator_attrs'],sort_keys=True)+' '+x['glyph']for y in seeds for x in y['source_hats'])),'archive':dict(stats),'archive_operator_forms':dict(collections.Counter(json.dumps(x['operator_attrs'],sort_keys=True)+' '+x['glyph']for x in originals)),'archive_mover_forms':dict(collections.Counter(json.dumps(x['mover_attrs'],sort_keys=True)for x in originals))}
(OUT/'source-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
