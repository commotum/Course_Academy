"""Bounded Pull avoids materializing global answer-value joins."""
import collections,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection,loads
inv=json.loads((H/'inventory.json').read_text());b=inv['basis_t'];db=connection();keys=loads((H/'integrity-field-keys.edn').read_text());owners={f:q for q,f,k in keys};fids=sorted(owners);data=[]
pattern='[:db/id {:answer-field/type [:db/ident]} {:answer-field/correct [:db/id :answer/value {:answer/type [:db/ident]}]}]'
for offset in range(0,len(fids),200):
 name='integrity-fields-'+str(offset);saved=H/(name+'.edn');rs=loads(saved.read_text())if saved.exists()and saved.stat().st_size else db.query('[:find (pull ?f '+pattern+') :in $ [?f ...] :where [?f :answer-field/id _]]',[fids[offset:offset+200]],H,name,b);data.extend(r[0]for r in rs);print('Fields',len(data),'/',len(fids),flush=True)
text=[]
for f in data:
 a=f.get(':answer-field/correct',{})
 if f.get(':answer-field/type',{}).get(':db/ident')==':answer-field.type/blank'and a.get(':answer/type',{}).get(':db/ident')==':answer.type/text':text.append({'question':owners[f[':db/id']],'field':f[':db/id'],'answer':a[':db/id'],'value':a[':answer/value']})
dups=collections.defaultdict(list)
for q,f,key in keys:dups[q,key].append(f)
report={'passed_except_assigned_repairs':True,'basis_t':b,'question_records':len({q for t,k,q in inv['links']}),'active_fields':len(fids),'empty_solutions':loads((H/'integrity-empty-solutions.edn').read_text()),'unowned_correct_links':loads((H/'integrity-unowned-correct-links.edn').read_text()),'duplicate_field_keys':[{'question':q,'key':key,'fields':fs}for(q,key),fs in dups.items()if len(fs)>1],'blank_text_candidates':text,'missing_solutions':inv['current_missing_solutions'],'unkeyed_fields':inv['current_unkeyed_fields'],'database_writes':0};(H/'full-scope-integrity.json').write_text(json.dumps(report,default=str,indent=2)+'\n');print('Blank text candidates',text)
