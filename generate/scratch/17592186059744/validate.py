"""Parse rendered tasks, check transpose entry-by-entry, replay entire banks, grade through application."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('transpose',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def check(r):
 q=r['question'];m=r['generation'];level=q[':question/difficulty'].split('/')[-1]
 assert r==g.generate(level,m['seed'],m['template'],m['parameters'],m['replay'])
 given=g.matrix_object(q[':question/problem']);expected=tuple(zip(*given));assert g.fingerprint(q)==m['mathematical_fingerprint']
 # Parse the printed solution, not metadata, and check every cell's original row/column index.
 out=g.matrix_object(q[':question/worked-solution']);assert len(out)==len(given[0]) and len(out[0])==len(given)
 for i,row in enumerate(out):
  for j,value in enumerate(row):assert sp.simplify(value-given[j][i])==0
 keys=set();ids={q[':question/id']};fields=q[':question/answer-fields'];blanks='{{field-' in q[':question/problem']
 assert q[':question/worked-solution'].startswith('To find the transpose, we interchange the rows and columns')
 if len(fields)==1 and fields[0][':answer-field/type'].endswith('radio'):
  phrase='single row, so it becomes a single column' if len(given)==1 else 'single column, so it becomes a single row'
  if m['template']!='q-1048':assert phrase in q[':question/worked-solution']
 for f in fields:
  assert f[':answer-field/key'] not in keys;keys.add(f[':answer-field/key']);assert f[':answer-field/id'] not in ids;ids.add(f[':answer-field/id'])
  choices=f[':answer-field/choices'];correct=[a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]];assert len(correct)==1
  for a in choices:assert a[':answer/id'] not in ids;ids.add(a[':answer/id']);assert '$' not in a[':answer/value']
  if f[':answer-field/type'].endswith('radio'):
   objects=[g.matrix_object(a[':answer/value']) for a in choices];assert len(choices)==len(set(objects))==5
   assert g.matrix_object(correct[0][':answer/value'])==expected
   assert sum(z==expected for z in objects)==1
  else:
   assert blanks and len(choices)==1
   i=int(f[':answer-field/key'].split('-')[-1])-1
   assert sp.simplify(g.expression(correct[0][':answer/value'])-list(sum((list(row) for row in expected),[]))[i])==0
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 assert len(re.findall(r'\{\{field-\d+\}\}',q[':question/problem']))==len(fields) if blanks else True
 return r

def native(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('radio'):
   checks += [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every complete radio option'} for a in f[':answer-field/choices']]
  else:
   value=g.expression(f[':answer-field/choices'][0][':answer/value'])
   for z,outcome,purpose in [(g.tex(value),'accepted','Canonical fragment'),('('+str(value)+')+0','accepted','Algebraically equivalent fragment'),(str(value+1),'rejected','Wrong entry'),(str(-value) if value!=0 else '1','rejected','Sign error')]:
    checks.append({'field_index':i,'submitted':z,'expected':outcome,'purpose':purpose})
 return {'label':label,'record':r,'checks':checks}

def build():
 sys.path.insert(0,str(ROOT/'scripts'));from serve_graph_explorer import build_learning
 binary=build_learning(ROOT.parent/'EDB');deps=ROOT/'target/release/deps';edbdeps=ROOT.parent/'EDB/target/release/deps';libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')}
 for name in ('check-engine','inspect-inventory'):
  cmd=['rustc','--edition=2024','-O',str(HERE/(name+'.rs'))]
  for n,p in libs.items():cmd+=['--extern',n+'='+str(p)]
  subprocess.run(cmd+['-L','dependency='+str(deps),'-L','dependency='+str(edbdeps),'-o',str(HERE/name)],check=True)
 save('native-build.json',{'libraries':{n:{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for n,p in libs.items()},'executables':{str(HERE/n):hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('check-engine','inspect-inventory')},'application_inventory':str(binary)})

def main():
 build();inputs=[];mapping=[];replays=[];samples=[];coverage={};review=[]
 for t,spec in g.SPECS.items():
  src=g.SOURCES[t];r=check(g.generate(spec['difficulty'],0,t,g.original(t),True));profile=spec['profile'];gf=r['question'][':question/answer-fields'];bykey={f[':answer-field/key']:f for f in gf};bank_count=0;matched=0;distractors=0
  for sf in src[':question/answer-fields']:
   f=bykey[sf[':answer-field/key']];blank=profile=='blank';obj=g.expression if blank else g.matrix_object
   original=[obj(a[':answer/value']) for a in sf[':answer-field/choices']];produced=[obj(a[':answer/value']) for a in f[':answer-field/choices']]
   assert len(original)==len(produced) and set(original)==set(produced),(t,original,produced)
   correct=sf.get(':answer-field/correct')
   if correct:assert obj(correct[':answer/value'])==obj(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]))
   for a in sf[':answer-field/choices']:
    i=produced.index(obj(a[':answer/value']));recipe='entry '+sf[':answer-field/key'] if blank else 'recipes('+profile+')[ '+str(i)+' ]'
    mapping.append({'source':t,'source_db_id':src[':db/id'],'field_id':sf[':db/id'],'field':sf[':answer-field/key'],'answer_id':a[':answer/id'],'source_value':a[':answer/value'],'profile':profile,'recipe':recipe,'recipe_object':str(produced[i]),'complete_value_reproduced':True})
   bank_count+=1;matched+=len(original);distractors+=len(original)-1 if not blank else 0
  replays.append({'source':t,'profile':profile,'complete_banks':bank_count,'matched_choices':matched,'matched_distractors':distractors,'correct_designation':'matched' if t!='q-1048' else 'absent source key; independently inferred only in evidence replay','source_complete':t not in ('q-1045','q-1048'),'source_errors':('Duplicate legacy field has no correct key and repeats selection; generated practice uses only the valid captured field.' if t=='q-1045' else 'Unrated, missing key and solution; excluded from normal generation and inventory.' if t=='q-1048' else None)})
  inputs.append(native('replay-'+t,r));review.append('## '+t+' source\n\n'+src[':question/problem']+'\n\n'+src.get(':question/worked-solution','[Source solution absent]')+'\n\nReplay:\n\n'+g.markdown(r))
  if t not in g.TEMPLATES:continue
  params=[set() for _ in spec['entries']];fps=set()
  for seed in range(16):
   try:r=check(g.generate(spec['difficulty'],seed,t))
   except ValueError:continue
   for i,z in enumerate(r['generation']['parameters']['entries']):params[i].add(z)
   fps.add(g.fingerprint(r['question']));samples.append(r);inputs.append(native(t+'-'+str(seed),r))
   assert r['question']==g.generate(spec['difficulty'],seed+1000,t,r['generation']['parameters'])['question']
  assert len(fps)>1 and all(len(v)>1 for v in params)
  coverage[t]={'orientation':spec['orientation'],'parameter_values_by_entry':[sorted(v) for v in params],'distinct_tasks':len(fps),'bank_profile':profile}
  review.append('Sample:\n\n'+g.markdown(r))
 # Change just one entry. Original data and orientation fixed; verify prompt, solution and that field's key change together.
 t='q-282775';a=check(g.generate('moderate',0,t,g.original(t)));p=g.original(t);p['entries'][0]='2*a-b';b=check(g.generate('moderate',0,t,p));assert a['generation']['parameters']['entries'][1]==b['generation']['parameters']['entries'][1];assert a['question']!=b['question'];inputs += [native('changed-entry-before',a),native('changed-entry-after',b)]
 try:g.batch('hard',5,0)
 except ValueError:pass
 else:raise AssertionError('Unsupported hard accepted')
 save('source-choice-mapping.json',mapping);save('source-replay.json',{'passed':True,'basis':g.S['basis'],'sources':replays,'matched_choices':len(mapping),'missing_or_extra_options':[],'excluded_normal_generation':['q-1048'],'legacy_field_correction':'q-1045 redundant unkeyed historical field omitted from new instances only'})
 save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 report=json.loads((HERE/'native-report.json').read_text());assert report['documented_unresolved_checks']==0
 save('previews.json',samples);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 save('validation.json',{'passed':True,'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'sample_count':len(samples),'source_questions':len(replays),'matched_choices':len(mapping),'correctness':'Independently parse displayed vector and solution, check each transposed cell; all radio matrices pairwise distinct with exactly one correct; every blank matches indexed target entry','fidelity':'Complete source banks replayed including malformed legacy fields; correct keys match wherever present; prompt/solution structure and field layout retained, with explicit legacy duplicate-field correction','actual_grading':{'entry_point':report['entry_point'],'accepted':report['accepted_checks'],'rejected':report['rejected_checks'],'unresolved':0},'coverage':coverage,'changed_entry_with_other_data_fixed':True,'deterministic_identity_ignores_seed':True,'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'source-specs.json',HERE/'source-query.edn')}})
 print('Validated',len(replays),'sources,',len(mapping),'source choices,',len(samples),'variants.')
if __name__=='__main__':main()
