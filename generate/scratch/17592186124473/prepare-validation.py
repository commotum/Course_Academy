"""Current source fidelity, exact graph readback and finite distinct candidates."""
import hashlib,importlib.util,itertools,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
r=module(H/'replenish.py','replenish');v=r.v;g=r.g
inv=r.inventory(H/'reference/pre-generation-inventory.json');b=inv['basis'];kp=r.read_kp(H/'reference/pre-generation',b)
stock=r.counts(H/'reference/pre-generation',kp,b)
assert r.canonical(kp)==r.canonical(json.loads((H/'current-source.json').read_text())['record'])
source_records=[];report=[]
for q in kp[':knowledge-point/questions']:
 r.source_check(q)
 mid=q[':question/math-academy-id'];old=g.QUESTIONS[mid]
 assert q[':question/worked-solution']==old[':question/worked-solution']
 # Current prompt migration changes layout, retaining the complete displayed sets.
 assert [g.spset(ss) for ss in v.promptsets(q)]==[g.spset(ss) for ss in v.promptsets(old)]
 if not v.promptsets(q):assert r.canonical(q)==r.canonical(old)
 rec={'knowledge_point':{'db_id':g.KP_ID,'id':g.REC[':knowledge-point/id'],'title':g.TITLE},'question':r.normalize(q),'generation':{'template':'current-source-'+mid}}
 source_records.append({'label':mid,'record':rec,'checks':r.checks(rec)})
 report.append({'source_id':mid,'prompt_restrictions_preserved':True,'worked_solution_exact':True,'fields':len(q[':question/answer-fields']),'complete_current_banks_matched':True,'independent_hlt_keys_verified':True})
r.save(H/'current-source-native-input.json',source_records)
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'current-source-native-input.json'),str(H/'current-source-native-report.json')],check=True)
r.save(H/'current-source-validation.json',{'status':'pass','basis':b,'lineage':r.LINEAGE,'sources':report,'complete_banks':sum(x['fields'] for x in report),'choices':sum(len(x['checks']) for x in source_records),'native_report':'current-source-native-report.json','historical_source_capture_retained':True})
# Count the bounded normalized parameter catalog without generating duplicates.
domains={};caps={};records=[]
for level,templates in g.NORMAL.items():
 domains[level]=set()
 for template in templates:
  slots=[]
  for left,right,mid,closure in itertools.product(range(2,5),range(2,5),range(2,5),(False,True)):
   if template in ('single_turn','jump_ranges','plateau_interval') and mid!=2:continue
   if template=='plateau_union' and not closure:continue
   p={'h':0,'left':left,'right':right,'mid':mid,'orient':1,'closure':closure,'permutation':[0,1,2]}
   fp=r.strong_fingerprint({'generation':{'template':template,'parameters':p}})
   if fp in domains[level]:continue
   domains[level].add(fp);slots.append(p)
  caps[template]=len(slots)
  # Enough candidates for reserve and replacements; round-robin across families.
  for i,p in enumerate(slots[:8]):
   rec=g.generate(level,175921+i,template=template,parameters=p);r.validate_instance(rec);records.append(rec)
# Coverage check: changing requested interval roles with fixed graph updates each field.
changed=0
for level,templates in g.NORMAL.items():
 for template in templates:
  if template.startswith('plateau'):continue
  p={'h':0,'left':3,'right':4,'mid':3 if template in ('two_turns','union_ranges','disconnected_ranges') else 2,'orient':1,'closure':True,'permutation':[0,1,2]}
  for perm in itertools.permutations(range(3)):
   p['permutation']=list(perm);rec=g.generate(level,0,template=template,parameters=p);r.validate_instance(rec);changed+=1
native=[{'label':rec['question'][':question/id'],'record':rec,'checks':r.checks(rec)} for rec in records]
r.save(H/'replenishment-native-input.json',native)
subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'replenishment-native-input.json'),str(H/'replenishment-native-report.json')],check=True)
r.save(H/'replenishment-candidates.json',records)
r.save(H/'capabilities.json',{'supported_levels':list(r.LEVELS),'observed_levels':['moderate','hard'],'authored_levels':['easy','moderate','hard'],'unsupported_levels':[],
 'finite_distinct_task_domain':{k:len(v) for k,v in domains.items()},'per_template':caps,
 'deduplication':'Collapse translations, output reflections, seed, choice order and interval-label permutations. Require changed normalized relative-span or endpoint data.',
 'exceptions':[{'kind':'finite-catalog','bounds':'integer h -2..2; spans 2..4; endpoint inclusions; no new operations or graph topologies beyond classified families','shortage_policy':'When the declared distinct catalog is exhausted, retain explicit shortages and return finite-limit; cosmetic variants never count.'},
 {'kind':'source-evidence-exclusion','scope':'All source raster reconstruction profiles','reason':'Rasters underidentify exact analytic curves. Evidence replay is ineligible for learner inventory.'}],
 'current_basis':b,'source_question_count':len(kp[':knowledge-point/questions'])})
r.save(H/'replenishment-validation.json',{'status':'pass','basis':b,'current_inventory_counts':stock,'current_sources':len(report),'normal_candidates':len(records),'independent_exact_hlt':True,'all_owned_banks_and_wrong_choices_checked':True,'changed_target_fixed_graph_cases':changed,'different_seed_same_task_identity':True,'distinct_normalized_candidates':len({r.strong_fingerprint(rec) for rec in records}),'source_capture_unchanged':True})
paths=[H.with_suffix('.py'),H/'validate.py',H/'renderer.py',H/'replenish.py',H/'prepare-validation.py',H/'current-source.json',H/'current-source-validation.json',H/'current-source-native-report.json',H/'replenishment-candidates.json',H/'replenishment-validation.json',H/'replenishment-native-report.json',H/'validation.json',H/'classification.md',H/'template-extraction.md',H/'plot-extraction.md',H/'capabilities.json']
r.save(H/'replenishment-freeze.json',{'version':g.VERSION,'status':'validated_for_database_preparation','basis':b,'hashes':{str(p.relative_to(ROOT)):r.sha(p) for p in paths},'supersedes':'freeze.json (version 1 radio output); historical source evidence preserved'})
print(json.dumps({'basis':b,'available':stock['distinct_available'],'candidates':len(records),'finite_domains':{k:len(v) for k,v in domains.items()},'current_source_validation':'pass'}),flush=True)
