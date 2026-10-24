"""Compile source-proven, cell-preserving table edits into guarded EDB batches."""
import collections,hashlib,json,re,sys,uuid
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/mathml-tables-work';sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(H))
from migrate_learner_history import dumps,kw
from layout import environment,cells,mathml_ruled_table,FENCES
from resolve_fields import clean_rows

def save(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')
def read_rows(tex):
 m=re.search(r'\\begin\{([^}]+)\}',tex);assert m
 b,e,end=environment(tex,m.start());body=tex[b:e]
 if m[1]=='array':
  spec=re.match(r'\s*\{[^{}]*\}',body);assert spec;body=body[spec.end():]
 return clean_rows(cells(body))
def render_target(item,text):
 rows=read_rows(text);new=mathml_ruled_table(rows,item['source']['source_attributes']);assert new
 actual=read_rows(new);assert len(rows)==len(actual),(item['e'],item['a'],repr(text),rows,repr(new),actual)
 for before,after in zip(rows,actual):assert before==after[:len(before)] and all(not x for x in after[len(before):]),(before,after)
 if item['span']['env'] in FENCES:
  f=item['source']['source_fences']
  if f:new=r'\left'+f[0]+new+r'\right'+f[1]
 return new

def main():
 resolved=json.loads((H/'resolved-layouts.json').read_text())+json.loads((H/'manual-layouts.json').read_text());grouped=collections.defaultdict(list)
 for item in resolved:grouped[item['e'],item['a']].append(item)
 source_values={(r['e'],r['a']):r for r in json.loads((W/'all-values.json').read_text())};fields=[];trace=[]
 for (e,a),items in sorted(grouped.items()):
  old=source_values[e,a]['v'];byspan={(r['span']['start'],r['span']['end']):r for r in items};items=list(byspan.values())
  def replacement(item):
   start,end=item['span']['start'],item['span']['end'];text=old[start:end];assert text==item['span']['tex']
   children=[r for r in items if start<r['span']['start'] and r['span']['end']<end]
   direct=[r for r in children if not any(q['span']['start']<r['span']['start'] and r['span']['end']<q['span']['end'] for q in children)]
   for child in sorted(direct,key=lambda r:r['span']['start'],reverse=True):
    s,t=child['span']['start']-start,child['span']['end']-start;text=text[:s]+replacement(child)+text[t:]
   result=render_target(item,text);trace.append({'entity':e,'attribute':a,'source_path':item['source']['path'],'source_identity':item['source']['identity'],'source_attributes':item['source']['source_attributes'],'source_fences':item['source']['source_fences'],'cell_bytes_preserved':True,'old_tex':item['span']['tex'],'new_tex':result,'confidence':item['confidence']});return result
  roots=[r for r in items if not any(q['span']['start']<r['span']['start'] and r['span']['end']<q['span']['end'] for q in items)]
  after=old
  for item in sorted(roots,key=lambda r:r['span']['start'],reverse=True):
   s,t=item['span']['start'],item['span']['end'];after=after[:s]+replacement(item)+after[t:]
  if after!=old:fields.append({'entity':e,'attribute':a,'before':old,'after':after,'before_sha256':hashlib.sha256(old.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'table_edits':len(items),'source_t':source_values[e,a]['t']})
 # Only radio choices are permitted to change values: their grader compares IDs.
 owners=json.loads((W/'owners.json').read_text());types={};idents={}
 for line in (W/'field-types.jsonl').read_text().splitlines():
  r=json.loads(line)
  if r['a']=='db/ident':idents[r['e']]=r['v']
  else:types[r['e']]=r['v']
 answer_fields={}
 for f in fields:
  if f['attribute']!='answer/value':continue
  fs={owner for owner,attr in owners.get(str(f['entity']),[]) if attr=='answer-field/choices'};assert fs
  assert all(idents[types[field]]==':answer-field.type/radio' for field in fs),(f['entity'],fs)
  answer_fields[f['entity']]=sorted(fs)
 extra=json.loads((H/'restored-choice.json').read_text());batches=[]
 for offset in range(0,len(fields),200):
  chunk=fields[offset:offset+200];folder=H/f'batch-{offset//200+1:02}';folder.mkdir(exist_ok=True)
  forms=[[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']] for f in chunk]
  ensured=set(field for f in chunk for field in answer_fields.get(f['entity'],[]))
  restore=any(f['entity']==extra['existing_choice_entity'] and f['attribute']=='answer/value' for f in chunk)
  if restore:
   forms += [{kw('db/id'):extra['answer_tempid'],kw('answer/id'):uuid.UUID(extra['answer_uuid']),kw('answer/type'):kw(extra['type']),kw('answer/value'):extra['value'],kw('db/ensure'):kw('answer/validate')},[kw('db/add'),extra['field_entity'],kw('answer-field/choices'),extra['answer_tempid']]]
   ensured.add(extra['field_entity'])
  forms += [[kw('db/ensure'),field,kw('answer-field/validate')] for field in sorted(ensured)]
  payload=dumps(forms)+'\n';assert len(payload.encode())<3_500_000
  (folder/'transaction.edn').write_text(payload);save(folder/'fields.json',chunk)
  (folder/'read-query.edn').write_text('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]\n');(folder/'read-inputs.edn').write_text(dumps([[[f['entity'],kw(f['attribute'])] for f in chunk]])+'\n')
  batches.append({'name':folder.name,'fields':len(chunk),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'field_keys':[[f['entity'],f['attribute']] for f in chunk],'ensured_fields':sorted(ensured),'restores_choice':restore})
 save(H/'fields.json',fields);save(H/'table-edits.json',trace);save(H/'batches.json',batches)
 report={'database':'math','basis_t':6244,'fields_scanned':535403,'fields_repaired':len(fields),'entities':len({f['entity'] for f in fields}),'table_edits':len(trace),'attributes':dict(collections.Counter(f['attribute'] for f in fields)),'batches':len(batches),'all_cell_bytes_preserved':True,'radio_answer_values_only':len(answer_fields),'restored_omitted_choices':1,'new_answer_uuid':extra['answer_uuid']};save(H/'preparation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
