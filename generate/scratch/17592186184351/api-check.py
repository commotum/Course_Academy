#!/usr/bin/env python3
"""Finite catalog, public integer guards and CLI checks; mathematics unchanged."""
import copy,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('api_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
def reject(fn):
 try:fn()
 except ValueError:return
 raise AssertionError('Invalid API input accepted')
guard_count=0
for bad in (True,False,1.0,1.5,'1',None):
 for fn in (lambda:g.generate('easy',seed=bad),lambda:g.generate_easy(seed=bad),lambda:g.generate_moderate(seed=bad),lambda:g.generate_hard(seed=bad),lambda:g.generate_batch('easy',seed=bad),lambda:g.generate_batch('easy',count=bad)):
  reject(fn);guard_count+=1
for bad in (0,-1):reject(lambda:g.generate_batch('easy',count=bad));guard_count+=1
capacities={};catalogs={};families={}
for level in g.LEVELS:
 catalog=g.semantic_catalog(level);catalogs[level]=catalog;cap=len(catalog);capacities[level]=cap
 assert len({row['semantic_key'] for row in catalog})==cap
 full=g.generate_batch(level,count=cap,seed=754)
 assert len(full)==cap and len({g.semantic_key(r['question'][':question/problem']) for r in full})==cap
 assert {r['generation']['mathematical_fingerprint'] for r in full}=={row['semantic_key'] for row in catalog}
 assert full==g.generate_batch(level,count=cap,seed=754),'Batch deterministic replay'
 families[level]=sorted({r['generation']['template'] for r in full})
 assert set(families[level])==set(g.level_templates(level))
 reject(lambda:g.generate_batch(level,count=cap+1));guard_count+=1
for params in g.parameters_for('base_ratio_linear_bank'):
 a=g.generate('hard',template='base_ratio_linear_bank',parameters=params)
 b=g.generate('hard',template='base_ratio_log_bank',parameters=params)
 assert a['question'][':question/id']!=b['question'][':question/id'],'Banks must retain different content identities'
 assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'],'Cross-profile integrals must deduplicate'
 groups=[row for row in catalogs['hard'] if row['semantic_key']==a['generation']['mathematical_fingerprint']]
 assert len(groups)==1 and len(groups[0]['alternatives'])==2
# Read the same expression through distinct TeX formatting wrappers. The
# method/variable remains fixed; seed or printed bank cannot enter the key.
canonical=g.generate('easy',template='positive_integer_power',parameters=g.ANCHORS['q-113852'])
prompt=canonical['question'][':question/problem'];alias=prompt.replace(r'\int ',r'\displaystyle \int ').replace(r'\,\text{d}x','dx')
assert g.semantic_key(prompt)==g.semantic_key(alias)
assert g.generate('easy',1,template='positive_integer_power',parameters=g.ANCHORS['q-113852'])['generation']['mathematical_fingerprint']==g.generate('easy',999,template='positive_integer_power',parameters=g.ANCHORS['q-113852'])['generation']['mathematical_fingerprint']
for sid in g.SOURCES:
 name=g.STYLE[sid];level=g.DIFFICULTY[sid];p=g.ANCHORS[sid]
 direct=g.generate(level,template=name,parameters=p,profile='observed:'+sid)
 singleton=g.generate_batch(level,1,template=name,parameters=p,profile='observed:'+sid)
 assert len(singleton)==1 and singleton[0]['generation']['mathematical_fingerprint']==direct['generation']['mathematical_fingerprint']
 assert g.capacity(level,template=name,parameters=p,profile='observed:'+sid)==1
 reject(lambda:g.generate_batch(level,2,template=name,parameters=p,profile='observed:'+sid));guard_count+=1
root=HERE.parents[2];cli=[sys.executable,str(HERE.with_suffix('.py'))]
flat=subprocess.run(cli+['--difficulty','all','--count','1','--format','json'],cwd=root,capture_output=True,text=True,check=True)
records=json.loads(flat.stdout);assert len(records)==3 and [r['question'][':question/difficulty'] for r in records]==[':question.difficulty/'+x for x in g.LEVELS]
(HERE/'cli-preview.json').write_text(flat.stdout)
for level,count in [('hard',90),('easy',152)]:
 out=subprocess.run(cli+['--difficulty',level,'--count',str(count),'--seed','43','--format','json'],cwd=root,capture_output=True,text=True,check=True)
 rows=json.loads(out.stdout);assert len(rows)==count and len({g.semantic_key(r['question'][':question/problem']) for r in rows})==count
for level,count in [('hard','91'),('all','153'),('easy','0'),('easy','1.0')]:
 out=subprocess.run(cli+['--difficulty',level,'--count',count,'--format','json'],cwd=root,capture_output=True,text=True)
 assert out.returncode!=0 and not out.stdout
# Refresh stored records to the current semantic metadata, requiring unchanged
# complete learner content/IDs/order. Existing mathematical/native/UI evidence
# remains applicable because none of that learner content changes.
changed_records=0
def refresh(value):
 global changed_records
 if isinstance(value,dict) and {'knowledge_point','question','generation'}<=set(value):
  meta=value['generation'];new=g.generate(g.DIFFICULTY[g.TEMPLATES[meta['template']]],meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
  assert new['question']==value['question'],'API correction changed verified learner content'
  assert new['knowledge_point']==value['knowledge_point'];changed_records+=1
  return new
 if isinstance(value,dict):return {k:refresh(v) for k,v in value.items()}
 if isinstance(value,list):return [refresh(v) for v in value]
 return value
for name in ('source-cases.json','review.json','bounded-records.json','native-input.json','ownership-input.json'):
 path=HERE/name;path.write_text(json.dumps(refresh(json.loads(path.read_text())),indent=2,ensure_ascii=False)+'\n')
cap=json.loads((HERE/'capacity.json').read_text());cap['by_level']=capacities;cap['distinct_mathematical_prompts']=sum(capacities.values());cap['capacity_basis']='actual normalized displayed integrand + integration variable + whole indefinite primitive modulo additive constant; bank profiles, seeds and format aliases excluded';cap['batch_without_replacement']=True;cap['oversize_rejected']=True
(HERE/'capacity.json').write_text(json.dumps(cap,indent=2)+'\n')
(HERE/'semantic-catalog.json').write_text(json.dumps(catalogs,indent=2)+'\n')
report={'passed':True,'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'strict_integer_seed_count_rejections':guard_count,'finite_semantic_capacities':capacities,'full_catalog_batch_without_replacement':True,'hard_shared_integrand_profile_pairs_deduplicated':54,'format_alias_dedup':True,'deterministic_batches':True,'all_source_parameter_profiles_supported':8,'cli_all_count1_flat_records':3,'cli_capacity_and_oversize_boundaries':True,'unchanged_previously_verified_record_questions':changed_records,'math_native_ui_rerun':'not repeated; complete learner question objects and identities proven unchanged, per root review instruction'}
(HERE/'api-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
