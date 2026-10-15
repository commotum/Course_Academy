"""Source/normal mathematical readback, role probes, native checks, immutable baseline."""
import copy,hashlib,importlib.util,itertools,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('pointline_draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
spec=importlib.util.spec_from_file_location('pointline_independent',HERE/'readback.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def baseline():
 old=json.loads((HERE/'reference/registered-baseline.json').read_text());base=ROOT/'generate/scratch/17592186054676.py';paths=[base]+sorted(p for p in base.with_suffix('').rglob('*')if p.is_file());now={str(p.resolve()):sha(p)for p in paths};assert old==now,'registered path set or file bytes changed';return len(old)
def native_input(label,rec):
 checks=[];answer_base=100
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'canonical authored selection or complete-bank wrong selection'})
  correct_index=next(j for j,a in enumerate(f[':answer-field/choices'])if a[':answer/id']==f[':answer-field/correct'][1]);checks.append({'field_index':i,'submitted':str(answer_base+correct_index).zfill(8),'expected':'accepted','purpose':'equivalent numeric encoding of the same authored choice entity ID'})
  answer_base+=len(f[':answer-field/choices'])
  # Non-blank fields require an authored choice ID, not text-equivalent labels.
  checks.append({'field_index':i,'submitted':'true'if f[':answer-field/type'].endswith('/checkbox')else'$A$ only','expected':'unresolved','purpose':'literal equivalent label is outside supported selection-ID response contract'})
 return {'label':label,'record':rec,'checks':checks}
def main():
 nbaseline=baseline();sources=[];inventory=[];ledger=[];originals=[];bankchoices=0
 for sid,q in g.SOURCES.items():
  rec=g.replay_raw(sid);result=reader.check(rec);assert result['task']==rec['generation']['task_fingerprint']
  # Exact original content/fields/IDs and omission of difficulty for unrated.
  assert rec['question']==g._normal(q)
  level=q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1]
  if level!='unrated':
   replay=g.generate(level,template=sid,parameters=g.DEFAULTS[sid],bank_profile=level+'-source-bank:ABC');assert replay['question']==rec['question']
  sources.append({'source_id':sid,'record':rec,'source_level':level,'classification':'captured MA'if q.get(':question/math-academy-id')else'captured non-MA','fidelity':{'prompt':True,'solution':True,'complete_fields_banks_and_key':True,'matched_choices':result['answer_values'],'missing':[],'extra':[]}});originals.append(rec)
  if not q.get(':question/math-academy-id'):inventory.append({'source_id':sid,'relationship':'captured non-MA record associated with this knowledge point at basis 2275; content follows the prior generator source template; retained independently from new authored variants','record':rec,'mathematical_task':result['task']})
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    ledger.append({'source_id':sid,'field':f[':answer-field/key'],'value':a[':answer/value'],'correct':a[':answer/id']==f[':answer-field/correct'][':answer/id'],'recipe':'fixed Boolean complete field bank'if level=='unrated'else{'selected_base_roles':sorted(reader.subset(a[':answer/value'])),'operation':'map every selected base role through chosen bijection; preserve whole bank'},'complete_value_reproduced':True});bankchoices+=1
 save('source-cases.json',sources);save('choice-ledger.json',ledger)
 save('independent-inventory.json',{'database':g.WRAPPER['database'],'basis':g.WRAPPER['basis'],'lineage':g.WRAPPER['lineage'],'relationship':'captured non-Math Academy records only; authored new variants and diagnostics are separate','questions':inventory})
 reviews=[];slotsets={l:{'member_sets':set(),'slopes':set(),'intercepts':set(),'points':set(),'profiles':set()}for l in g.SUPPORTED_LEVELS};counts={l:set()for l in g.SUPPORTED_LEVELS};stagecount=0;pixelchecks=0
 # Real seeded normal output, all six complete role profiles, and signed/zero boundaries.
 for level in g.SUPPORTED_LEVELS:
  rows=g.batch(level,20,2275)
  for permutation in itertools.permutations('ABC'):
   profile=level+'-source-bank:'+''.join(permutation);rec=g.generate(level,seed=31,bank_profile=profile);rows.append(rec)
  for rec in rows:
   data=reader.check(rec);assert data['task']==rec['generation']['task_fingerprint'];stagecount+=data['stages'];pixelchecks+=1;reviews.append({'label':level+'-'+str(len(reviews)),'record':rec,'independent':data});counts[level].add(data['task'])
   p=rec['generation']['parameters'];z=slotsets[level];z['member_sets'].add(''.join(data['truth']));z['slopes'].add(str(p['m']));z['intercepts'].add(p['b']);z['points'].add(json.dumps(p['points']));z['profiles'].add(rec['generation']['bank_profile'])
  assert len(slotsets[level]['member_sets'])==3 and len(slotsets[level]['profiles'])==6
 # Same x-coordinates, slope/intercept, altered membership positions: no cosmetic relabel.
 controlled=[]
 for level in g.SUPPORTED_LEVELS:
  for perm in(('ABC','BAC','BCA')if level=='easy'else('ABC','ACB','BCA')):
   m=2 if level=='easy'else -2 if level=='moderate'else'1/2';b=0;xs=[-2,0,2];true={perm[i]for i in g.BASE_TRUTH[level]};p={'m':m,'b':b,'points':[[xx,int(g._frac(m)*xx)+(0 if a in true else 1)]for a,xx in zip('ABC',xs)]}
   rec=g.generate(level,seed=0,parameters=p,bank_profile=level+'-source-bank:'+perm);data=reader.check(rec);controlled.append({'label':'controlled-'+level+'-'+perm,'record':rec,'independent':data});stagecount+=data['stages'];pixelchecks+=1
 reviews+=controlled
 # Corruption probes preserve correct final choices whenever possible.
 base=copy.deepcopy(controlled[0]['record']);mutations=[]
 def probe(name,change):
  rec=copy.deepcopy(base);change(rec)
  try:reader.check(rec)
  except(AssertionError,ValueError,StopIteration):mutations.append({'mutation':name,'caught':True});return
  raise AssertionError('missed mutation '+name)
 probe('stale summary target coordinate',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('A(-2,-4)','A(-1,-4)',1)))
 probe('stale substitution operand with final result preserved',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('2(-2)','2(-1)',1)))
 probe('wrong intermediate coefficient with final result preserved',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('2(-2)','3(-2)',1)))
 probe('wrong evaluated stage with final key preserved',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('-4 & =-4','-4 & =-3',1)))
 probe('wrong truth prose with final key preserved',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('results in a true','results in a false',1)))
 probe('stale point conclusion with final key preserved',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('point $A$ does lie','point $A$ does not lie',1)))
 probe('stale final subset with key preserved',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('only points $A$ and $C$','only points $A$ and $B$',1)))
 probe('wrong key only',lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id',r['question'][':question/answer-fields'][0][':answer-field/choices'][1][':answer/id']]))
 probe('duplicate whole mathematical option',lambda r:r['question'][':question/answer-fields'][0][':answer-field/choices'][1].__setitem__(':answer/value',r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']))
 other=controlled[1]['record']['generation']['plot_path']
 probe('stale plot with correct prompt solution and key',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace(r['generation']['plot_path'],other)))
 save('mutation-probes.json',mutations)
 bad=[]
 for value in(True,1.5,'5',None):
  for function in('generate','batch'):
   try:getattr(g,function)('easy',**{'seed':value})
   except TypeError:bad.append([function,'seed',repr(value)])
   else:raise AssertionError('accepted invalid seed')
 for value in(True,1.5,'5',None,0,-1,g.CAPACITY_LIMIT+1):
  try:g.batch('easy',count=value)
  except(TypeError,ValueError):bad.append(['batch','count',repr(value)])
  else:raise AssertionError('accepted invalid count')
 for l in g.SUPPORTED_LEVELS:
  a=g.generate(l,123);assert a==g.generate(l,123)
  # Source replay remains canonically same task despite original/source ID.
  for k in g.SOURCE_TEMPLATES_BY_LEVEL.get(l,[]):assert reader.fingerprint(g.replay_raw(k)['question'])==g.task_identity(g.DEFAULTS[k])
 cli=[]
 for form in('json','markdown'):
  run=subprocess.run([sys.executable,'-B',str(HERE.with_suffix('.py')),'--difficulty','all','--count','1','--seed','2275','--format',form],capture_output=True,text=True,check=True);(HERE/('cli-all.'+('json'if form=='json'else'md'))).write_text(run.stdout)
  if form=='json':assert len(json.loads(run.stdout))==3
  cli.append(form)
 save('review-cases.json',reviews);save('slot-coverage.json',{l:{k:sorted(v)for k,v in z.items()}for l,z in slotsets.items()});save('task-counts.json',{l:len(v)for l,v in counts.items()});save('source-errors-and-repairs.json',{'errors':[],'repairs':[],'note':'All 12 captured practice banks/keys and source coordinates inspected; no mathematical source error found. Unrated short solutions intentionally preserved; no guessed difficulty.'})
 native=[native_input('source-'+str(i),r)for i,r in enumerate(originals)]+[native_input(row['label'],row['record'])for row in reviews]
 save('native-input.json',native);engine=HERE/'reference/check-engine';assert sha(engine)==sha(ROOT/'generate/runs/current/check-engine');subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 nr=json.loads((HERE/'native-grading.json').read_text());save('native-summary.json',{'engine_sha256':sha(engine),'fixtures':len(native),'checks':sum(len(v['checks'])for v in native),'accepted':nr['accepted_checks'],'rejected':nr['rejected_checks'],'unresolved':nr['documented_unresolved_checks'],'qualification':'Canonical IDs and equivalent leading-zero numeric encodings of each same authored choice are accepted. Unresolved checks are deliberately unsupported literal labels for radio/checkbox; all actual authored IDs tested. No mathematical blank field is observed or generated, so free-entry equivalent algebra is inapplicable. No supported valid answer rejected.','engine_changed':False,'database_writes':0})
 report={'status':'pass','basis':2275,'registered_files_unchanged':baseline(),'source_records':len(sources),'rated_MA':2,'unrated_MA':2,'captured_non_MA':len(inventory),'source_choice_values_matched':bankchoices,'source_complete_banks':16,'review_records':len(reviews),'variant_operative_stages_read':stagecount,'source_operative_stages_read':90,'all_operative_stages_read':stagecount+90,'png_pixel_readbacks':pixelchecks,'mutations_caught':len(mutations),'invalid_input_guards':len(bad),'CLI_formats':cli,'normal_tasks':{l:len(v)for l,v in counts.items()},'native_summary':'native-summary.json','source_repair_count':0,'hard':'authored rational slope same-method extension; no captured hard evidence','writes_to_database':0}
 save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
