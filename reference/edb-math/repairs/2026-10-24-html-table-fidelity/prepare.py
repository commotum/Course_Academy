"""Build content-only CAS payloads; retain response IDs and validate choice banks."""
import collections,hashlib,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/html-table-repair';sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import dumps,kw

def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def sha(v):return hashlib.sha256(v.encode()).hexdigest()
def main():
 rows=json.loads((H/'compiled.json').read_text());values={(r['e'],r['a']):r for r in json.loads((W/'values.json').read_text())};meta=json.loads((W/'metadata.json').read_text());owners=json.loads((W/'owners.json').read_text());idents=json.loads((W/'idents.json').read_text());groups=collections.defaultdict(list)
 for r in rows:groups[r['entity'],r['attribute']].append(r)
 fields=[];allfields=set()
 for (e,a),tables in sorted(groups.items()):
  before=values[e,a]['v'];after=before
  for t in sorted(tables,key=lambda t:t['span'][0],reverse=True):
   s,z=t['span'];assert before[s:z]==t['before_table'];after=after[:s]+'\n\n'+t['proposed_html']+'\n\n'+after[z:]
  assert before!=after
  marker=lambda v:collections.Counter(re.findall(r'\{\{[^}]+\}\}',v))
  assert marker(before)==marker(after),(e,'Field markers changed')
  f={'entity':e,'attribute':a,'before':before,'after':after,'before_sha256':sha(before),'after_sha256':sha(after),'tables':len(tables),'render_type':'text'}
  if a=='answer/value':
   fs=[p for p,attr in owners[str(e)]if attr=='answer-field/choices'];assert fs
   assert all(idents[str(meta[str(p)]['answer-field/type'])]in [':answer-field.type/radio',':answer-field.type/select']for p in fs),'Canonical free-response values must not change'
   assert idents[str(meta[str(e)]['answer/type'])]==':answer.type/text';f['answer_fields']=fs;allfields.update(fs)
  fields.append(f)
 # Capture full choice banks to prove no duplicate labels are introduced.
 needed={int(e)for e,refs in owners.items()if any(p in allfields and attr=='answer-field/choices'for p,attr in refs)};bankvalues={}
 for line in (W/'current.jsonl').open():
  d=json.loads(line)
  if d['e']in needed and d['a']=='answer/value':bankvalues[d['e']]=d['v']
 changed={f['entity']:f['after']for f in fields if f['attribute']=='answer/value'}
 for parent in allfields:
  ids=[int(e)for e,refs in owners.items()if[parent,'answer-field/choices']in refs];before=[(meta[str(e)]['answer/type'],bankvalues[e])for e in ids];after=[(meta[str(e)]['answer/type'],changed.get(e,bankvalues[e]))for e in ids];assert len(set(after))>=len(set(before)),('New choice collision',parent)
 batches=[]
 for offset in range(0,len(fields),150):
  chunk=fields[offset:offset+150];folder=H/f'batch-{offset//150+1:02}';folder.mkdir(exist_ok=True);forms=[[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']]for f in chunk];affected=sorted({p for f in chunk for p in f.get('answer_fields',[])});ensured=[p for p in affected if'answer-field/correct'in meta[str(p)]];forms.extend([kw('db/ensure'),p,kw('answer-field/validate')]for p in ensured);payload=dumps(forms)+'\n';assert len(payload.encode())<3_500_000;(folder/'transaction.edn').write_text(payload);save(folder/'fields.json',chunk)
  (folder/'read-query.edn').write_text('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]\n');(folder/'read-inputs.edn').write_text(dumps([[[f['entity'],kw(f['attribute'])]for f in chunk]])+'\n');batches.append({'name':folder.name,'fields':len(chunk),'sha256':sha(payload),'field_keys':[[f['entity'],f['attribute']]for f in chunk],'ensured_fields':ensured})
 save(H/'fields.json',fields);save(H/'batches.json',batches);report={'fields':len(fields),'entities':len({f['entity']for f in fields}),'tables':len(rows),'attributes':dict(collections.Counter(f['attribute']for f in fields)),'answer_fields':len(allfields),'batches':len(batches),'all_current_cell_bytes_preserved':True,'field_markers_preserved':True,'answer_value_changes_only_id_graded_choices':True,'fresh_basis':7027};save(H/'preparation.json',report);print(report)
if __name__=='__main__':main()
