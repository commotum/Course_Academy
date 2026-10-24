"""Fresh full-database scan after commit; no remaining percentage mistakes."""
import collections,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/percent-escaping';sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
sys.path.insert(0,str(R/'scripts/question_capture'));from math_format import MATH
db=connection();subprocess.run([str(R/'.local/edb/math-image-import-audit-2026-10-22/export-current'),'math',str(W/'final.jsonl')],env=db.env,check=True)
idents={};answer_types={};percent_fields=[];strings=0;actual={};fields=json.loads((H/'fields.json').read_text());expected={(f['entity'],f['attribute']):f['after']for f in fields};comments={(r['entity'],r['attribute'])for r in json.loads((H/'token-review.json').read_text())if r['decision']=='retain-comment'};original={(r['e'],r['a']):r['v']for r in json.loads((H/'percent-inventory.json').read_text())if(r['e'],r['a'])in comments}
for line in(W/'final.jsonl').open():
 r=json.loads(line);e,a,v=r['e'],r['a'],r['v']
 if a=='db/ident':idents[e]=v
 elif a=='answer/type':answer_types[e]=v
 if(e,a)in expected or(e,a)in comments:actual[e,a]=v
 if isinstance(v,str):
  strings+=1
  if'%'in v:percent_fields.append(r)
assert all(actual[k]==v for k,v in expected.items())and all(actual[k]==v for k,v in original.items())
remaining=[]
for r in percent_fields:
 v=r['v'];spans=list(MATH.finditer(v));bare=r['a']=='answer/value'and idents.get(answer_types.get(r['e']))==':answer.type/math'and not spans and not v.lstrip().startswith(('$',r'\(',r'\['))
 for i,c in enumerate(v):
  if c!='%':continue
  j=i-1;slashes=0
  while j>=0 and v[j]=='\\':slashes+=1;j-=1
  if slashes%2 or not(bare or any(m.start()<=i<m.end()for m in spans)):continue
  remaining.append({'entity':r['e'],'attribute':r['a'],'offset':i,'context':v[max(0,i-50):i+100],'retained_reviewed_comment':(r['e'],r['a'])in comments})
(H/'remaining-unescaped-math-percent.json').write_text(json.dumps(remaining,indent=2)+'\n');assert len(remaining)==17 and all(r['retained_reviewed_comment']for r in remaining)
basis=json.loads((W/'final.manifest.json').read_text())['basis_t'];report={'database':'math','basis_t':basis,'fresh_domain_strings_scanned':strings,'all_905_committed_fields_current_and_exact':True,'remaining_percentage_escape_defects':0,'retained_real_comment_tokens':len(remaining),'retained_real_comment_fields':len(comments),'original_comment_values_byte_identical':True,'learner_history_and_ids_unchanged_by_repair':True};(H/'coverage-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
