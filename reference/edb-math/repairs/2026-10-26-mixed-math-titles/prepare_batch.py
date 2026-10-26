"""Compile reviewed formula restorations into a content-only guarded transaction."""
import collections,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/mixed-math-titles';sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import dumps,kw
from question_capture.math_format import MATH

def main():
 rows=json.loads((H/'resolved.json').read_text());values={(d['e'],d['a']):d for d in json.loads((W/'values.json').read_text())};groups=collections.defaultdict(list)
 for r in rows:groups[r['entity'],r['attribute']].append(r)
 fields=[];reviews=[]
 for (e,a),edits in sorted(groups.items()):
  assert a in ['tutorial/content','question/problem','question/worked-solution'];before=values[e,a]['v'];after=before;last=len(before)
  for row in sorted(edits,key=lambda r:r['span'][0],reverse=True):
   s,z=row['span'];assert z<=last and before[s:z]==row.get('before_formula',before[s:z]),(e,a,s);last=s;after=after[:s]+row['after_formula']+after[z:];reviews.append(row)
  assert collections.Counter(re.findall(r'\{\{[^}]*\}\}',MATH.sub('',before)))==collections.Counter(re.findall(r'\{\{[^}]*\}\}',MATH.sub('',after))),('Field marker changed',e,a)
  fields.append({'entity':e,'attribute':a,'before':before,'after':after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'restored_formulas':len(edits)})
 folder=H/'batch-001';folder.mkdir(exist_ok=True);assert not(folder/'commit-intent.json').exists();payload=dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in fields])+'\n';assert len(payload.encode())<3_500_000;(folder/'transaction.edn').write_text(payload);(folder/'fields.json').write_text(json.dumps(fields,indent=2)+'\n');report={'fields':len(fields),'entities':len({f['entity']for f in fields}),'formulas':len(reviews),'payload_bytes':len(payload.encode()),'attributes':dict(collections.Counter(f['attribute']for f in fields)),'canonical_answer_values_and_links_unchanged':True,'field_markers_unchanged':True,'source_snapshot_basis':8029};(folder/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
if __name__=='__main__':main()
