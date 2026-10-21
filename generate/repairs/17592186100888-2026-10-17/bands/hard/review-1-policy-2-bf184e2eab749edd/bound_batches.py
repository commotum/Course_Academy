import json,hashlib,subprocess,sys,itertools
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT));from review_tests import check,truth
ctxs=json.loads((ROOT.parent/'review-contexts.json').read_text());tests=[];native=[]
manifest=json.loads((ROOT.parent/'workspace/package.json').read_text())
for ctx in ctxs:
 band=ctx['requested_difficulty'];batch=Path(ctx['batch_file']);source=Path(ctx['source_file']);inventory=Path(ctx['inventory_file']);binding=ctx['review_binding']
 for p,key in [(batch,'batch_hash'),(source,'source_hash'),(inventory,'inventory_hash')]:assert hashlib.sha256(json.dumps(json.loads(p.read_text()),sort_keys=True,separators=(',',':')).encode()).hexdigest()==binding[key],(band,key)
 for f in manifest['files']:assert (Path(ctx['package_root'])/f).read_bytes()==(ROOT.parent/'workspace'/f).read_bytes(),(band,f)
 records=json.loads(batch.read_text());out=ROOT/('bound-'+band+'.json');out.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');counts=Counter(check(r) for r in records);assert set(counts)=={'000','011','100','111'}
 for i,r in enumerate(records):
  vals=truth(r);checks=[]
  for tup in itertools.product((False,True),repeat=3):
   for j,v in enumerate(tup):
    field=r['question'][':question/answer-fields'][j];aid=next(a[':answer/id'] for a in field[':answer-field/choices'] if a[':answer/value']==str(v).lower());checks.append({'field_index':j,'submitted_answer_id':aid,'expected':'accepted' if v==vals[j] else 'rejected','purpose':'exact boundbatch exhaustive8 checkbox tuples'})
  native.append({'label':band+':'+str(i),'record':r,'checks':checks})
 command=[ctx['python'],str(Path(ctx['repo_root'])/'generate/pipeline/check_delivery.py'),'--input',str(out),'--source',ctx['source_file'],'--inventory',ctx['inventory_file'],'--difficulty',band,'--output',str(ROOT/('bound-delivery-'+band)),'--asset-root',ctx['workspace'],'--math-root',ctx['math_root']]
 result=subprocess.run(command,check=True,capture_output=True,text=True);accepted=json.loads((ROOT/('bound-delivery-'+band)/'accepted.json').read_text());post=Counter(check(r) for r in accepted);assert post==counts
 tests.append({'band':band,'binding':binding,'package_files_match_independent_tested_workspace':True,'source_basis':json.loads(source.read_text())['basis'],'input_count':len(records),'pre_cases':dict(counts),'post_cases':dict(post),'command':command,'summary':result.stdout.strip()})
(ROOT/'bound-batches.json').write_text(json.dumps(tests,indent=2)+'\n');(ROOT/'bound-grader-input.json').write_text(json.dumps(native,indent=2)+'\n');print(json.dumps([{'band':r['band'],'input_count':r['input_count'],'post_cases':r['post_cases']} for r in tests]))
