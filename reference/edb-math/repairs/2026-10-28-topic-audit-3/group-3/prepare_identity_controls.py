import copy,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from generator_publish import localize_record
H=Path(__file__).resolve().parent;R=json.loads((H/'identity-contract-samples.json').read_text());idents=dict(json.loads((H/'idents.json').read_text()));reverse={v:k for k,v in idents.items()};qs=[];mapping=[];proof=[]
for i,s in enumerate(R):
 raw=s['record'];localized=localize_record(raw,H/'identity-preview-math',H);q=copy.deepcopy(localized['question']);qid=90000000+i;q[':db/id']=qid;mapping.append({'render_fixture_entity':qid,'kp':s['kp'],'level':s['level'],'original_question_UUID':q[':question/id']});assets=localized.get('assets',{});proof.append({'kp':s['kp'],'band':s['level'],'question_UUID_unchanged':raw['question'][':question/id']==q[':question/id'],'assets':assets,'production_protocol':'scripts.generator_publish.localize_record with its ImageLibrary; isolated audit math_root only; no EDB writes'})
 for j,f in enumerate(q.get(':question/answer-fields',[])):
  f[':db/id']=qid*100+j;typ=f[':answer-field/type'];typ=typ[':db/ident']if isinstance(typ,dict)else typ;f[':answer-field/type']={':db/id':reverse[typ]};cid=f[':answer-field/correct'][1]
  for n,a in enumerate(f[':answer-field/choices']):
   a[':db/id']=qid*100000+j*100+n;typ=a[':answer/type'];typ=typ[':db/ident']if isinstance(typ,dict)else typ;a[':answer/type']={':db/id':reverse[typ]}
   if a[':answer/id']==cid:f[':answer-field/correct']={':db/id':a[':db/id']}
 qs.append(q)
for p in(H/'identity-preview-math/images').rglob('*'):
 if p.is_file():assert hashlib.sha256(p.read_bytes()).hexdigest()==p.stem
(H/'identity-controls-snapshot.json').write_text(json.dumps({'questions':qs},indent=2));(H/'identity-controls-identity-map.json').write_text(json.dumps(mapping,indent=2));(H/'identity-asset-publication-proof.json').write_text(json.dumps({'records':len(proof),'all_localized_assets_exact_content_hash':True,'isolated_math_root':str(H/'identity-preview-math'),'checks':proof},indent=2));print('identity controls prepared',len(qs))
