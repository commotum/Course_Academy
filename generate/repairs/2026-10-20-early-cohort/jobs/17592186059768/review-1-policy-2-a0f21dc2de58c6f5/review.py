import sys
sys.dont_write_bytecode=True
import json,pathlib,hashlib,copy,importlib.util,re,platform,subprocess,shutil,collections
E=pathlib.Path(__file__).resolve().parent;JOB=E.parent;PKG=JOB/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy');PY=REPO/'.venv/bin/python';PREV=JOB/'review-0-policy-2-039ec9a7ea105bf9'
def save(n,x):
 p=E/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n');return p
def read(p):return json.loads(pathlib.Path(p).read_text())
def hashes():return {str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(PKG.rglob('*')) if p.is_file()}
def load(p,name):
 sys.path.insert(0,str(p.parent));s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
# Independent parser and witnesses reused with explicit provenance; no previous main executed.
exec((E/'independent-witnesses.py').read_text(),globals())
g=load(PKG/'17592186059768.py','current_generator')

def checks(records):return [check_math(r) for r in records]
def bank(r):return [matrix(a[':answer/value'])[0] for a in field(r)[':answer-field/choices']]
def run(cmd,out,cwd=E):
 p=subprocess.run(list(map(str,cmd)),cwd=cwd,capture_output=True,text=True);save(out,{'command':list(map(str,cmd)),'cwd':str(cwd),'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});return p

def main():
 save('package-before.json',hashes());source=read(JOB/'source/source.json');batch=read(JOB/'samples.json');save('runner-batch.json',batch)
 save('provenance.json',{'parser':str(PREV/'audit.py'),'parser_sha256':hashlib.sha256((PREV/'audit.py').read_bytes()).hexdigest(),'use':'Independent linear parser, matrix parser, key/bank/solution witnesses reused. Current source replay, samples, counterfactuals and results freshly executed.'})
 global SIGNATURES
 SIGNATURES={};replays=[];results=[];samples=[];bounds=[];boundary_results=[];controls=[];pair_results=[]
 for idx,src in enumerate(source['material']['kp'][':knowledge-point/questions']):
  name=src[':question/math-academy-id'];level=src[':question/difficulty'][':db/ident'].split('/')[-1]
  texts=[src[':question/problem'],src[':question/worked-solution']]+[a[':answer/value'] for a in src[':question/answer-fields'][0][':answer-field/choices']]
  params={str(v):v for v in sorted({int(n) for t in texts for n in re.findall(r'\d+',t) if int(n)>1})}
  r=g.generate(level,623981001,profile=name,parameters=params);check_math(r);replays.append(r)
  assert bank(r)==[matrix(a[':answer/value'],True)[0] for a in src[':question/answer-fields'][0][':answer-field/choices']]
  assert correct_matrix(r)==matrix(src[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],True)[0]
  assert re.sub(r'\s+','',r['question'][':question/problem'])==re.sub(r'\s+','',src[':question/problem'])
  assert matrix(r['question'][':question/worked-solution'])==matrix(src[':question/worked-solution'])
  source_eq=equation_blocks(src[':question/worked-solution']);replay_eq=equation_blocks(r['question'][':question/worked-solution']);assert len(source_eq)==len(replay_eq)
  if source_eq:assert expected(replay_eq[0])==expected(source_eq[0])
  results.append({'profile':name,'source_id':src[':question/id'],'prompt':'matched ignoring whitespace','complete_bank_choices':5,'key':'matched','solution_stages':'organized equations and both matrices matched; organizing/coefficient/augmentation prose inspected'})
  SIGNATURES[name]=sign(correct_matrix(r))
  group=[g.generate(level,623981101+idx*107+i,profile=name) for i in range(8)]
  checks(group);samples+=group
  for v in [-24,1]:
   ps={k:(v if i==0 else min(24,i+3)) for i,k in enumerate(params)}
   try:
    b=g.generate(level,623981901+idx,profile=name,parameters=ps);check_math(b);bounds.append(b);outcome='accepted and math verified'
   except Exception as ex:outcome=repr(ex)
   boundary_results.append({'profile':name,'parameters':ps,'outcome':outcome})
  invalid={**params,next(iter(params)):25}
  try:g.generate(level,623981902,profile=name,parameters=invalid);raise AssertionError('invalid accepted')
  except ValueError as ex:boundary_results.append({'profile':name,'parameters':invalid,'outcome':str(ex)})
  if name in ['q-71722','q-129122','q-1068']:
   base=group[0];m=correct_matrix(base);changed=copy.deepcopy(m);i,j=next((i,j) for i,row in enumerate(m) for j,v in enumerate(row[:-1]) if v);changed[i][j]*=-1
   opts={k:base['generation'][k] for k in ['row_order','variable_order']}
   related=g.generate(level,base['generation']['seed'],profile=name,instance={'matrix':changed,**opts});check_math(related)
   # Build a harmless commutative reorder fixture with original bank and solution.
   irrelevant=copy.deepcopy(base);q=irrelevant['question'];match=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S);rows=match[1].split('\\\\')
   row_index,side=next((i,s) for i,row in enumerate(rows) for s,expr in enumerate(row.replace('&','').split('=')) if len(re.findall(r'[+-]?[^+-]+',expr.strip()))>1)
   lhs,rhs=rows[row_index].split('&=');expr=[lhs.strip(),rhs.strip()][side];parts=re.findall(r'[+-]?[^+-]+',expr);rev=''.join(t if t.startswith(('+','-')) else '+'+t for t in reversed(parts)).lstrip('+')
   rows[row_index]=(rev if side==0 else lhs)+' &='+(rev if side==1 else rhs)
   q[':question/problem']=q[':question/problem'][:match.start(1)]+'\\\\'.join(rows)+q[':question/problem'][match.end(1):];irrelevant['review_fixture']={'change':'commutative term order only; original bank, key and worked solution retained'};check_math(irrelevant)
   assert base['question'][':question/problem']!=irrelevant['question'][':question/problem'];assert correct_matrix(irrelevant)==m;assert correct_matrix(related)!=m
   offset=len(controls);controls += [base,related,irrelevant]
   pair_results.append({'profile':name,'indices':[offset,offset+1,offset+2],'relevant_change':f'matrix entry {i},{j} sign reversed at fixed other entries, equation roles and seed','before':m,'after':changed,'irrelevant_change':'reorder terms on one side of one equation','math_and_solution_dependency':'passed','grader_and_render':'see grader-results.json and render/rendering.json'})
 save('source-replays.json',replays);save('source-replay-results.json',results);save('independent-samples.json',samples);save('boundaries.json',boundary_results);save('boundary-records.json',bounds)
 # Exact prior counterexample; negative-corner rule must fail now; signed assignment accepted.
 old=load(PREV/'relocated-package/17592186059768.py','old_generator');oldr=old.generate('easy',941713401,profile='q-71722',parameters={'2':2,'3':4});now=g.generate('easy',941713401,profile='q-71722',parameters={'2':2,'3':4});signed=g.generate('easy',941713401,profile='q-71722',parameters={'2':-2,'3':4})
 save('retained-counterexamples.json',[oldr,now,signed]);checks([oldr,now,signed]);assert negative_corner(oldr) and not negative_corner(now);assert correct_matrix(signed)!=correct_matrix(now)
 old_missing=[]
 for name in ['q-1068','q-1053','q-129128']:
  try:old.generate('moderate',941713201,template=name);outcome='unexpected accepted'
  except Exception as ex:outcome=repr(ex)
  old_missing.append({'profile':name,'old_failure':outcome,'current_supported':name in g.PROFILES})
 save('retained-regression-results.json',{'original_corner_witness_fails_old':negative_corner(oldr),'current_corner_witness_defeated':not negative_corner(now),'signed_assignment_changes_answer':True,'source_omissions':old_missing})
 # Variable target/role change with same signed multiset: swap coefficient columns.
 base=next(r for r in samples if r['generation']['template']=='q-129122');m=correct_matrix(base);swapped=[[row[1],row[0],row[2]] for row in m];opts={'row_order':base['generation']['row_order'],'variable_order':list(reversed(base['generation']['variable_order']))};target=g.generate('easy',base['generation']['seed'],profile='q-129122',instance={'matrix':swapped,**opts});check_math(target);assert correct_matrix(target)==swapped
 controls += [base,target,now,signed];save('counterfactual-records.json',controls);save('counterfactual-results.json',{'pairs':pair_results,'variable_role_pair':{'indices':[9,10],'change':'swap x/y coefficient columns, preserving signed entries and row order','before':m,'after':swapped,'passed':True},'literal_pair':{'indices':[11,12],'change':'2 -> -2 in exact old q-71722 witness','passed':True}})
 all_records=replays+samples+bounds+batch+controls;save('math-results.json',{'method':'Reused independent exact integer parser; reads visible prompt and verifies unique matrix key, distinct complete bank and organized equations/coefficient/augmented solution matrices','records':checks(all_records),'count':len(all_records)})
 assert all(g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],profile=r['generation']['template'])==r for r in samples)
 save('scope-results.json',{'count':len(all_records),'observed':'All equations linear, integer; x,y for easy (2 equations), x,y,z moderate (2 or 3 equations); one five-choice radio field; three source solution stages; no solving or row reduction. Banks permute signed values and positions rather than introduce new response format. Magnitudes at most 24.','easy_shape_counts':dict(collections.Counter(str((len(bank(r)[0]),len(bank(r)[0][0]))) for r in all_records if r['question'][':question/difficulty'].endswith('/easy')))})
 cases=[]
 for i,r in enumerate(all_records):
  f=field(r);cases.append({'label':f'independent-{i}-{r["generation"]["template"]}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct_id(f) else 'rejected','purpose':'independently parsed visible-equation response' if a[':answer/id']==correct_id(f) else 'distinct incorrect coefficient/constant assignment'} for a in f[':answer-field/choices']]})
 save('grader-input.json',cases)
 for level in ['easy','moderate']:save('independent-'+level+'.json',[r for r in samples if r['question'][':question/difficulty'].endswith('/'+level)])
 manifest=read(PKG/'package.json');runtime={'python':platform.python_version(),'dependencies':manifest['dependencies'],'runtime_imports':'stdlib plus bundled math_format.py; no third-party dependencies','deterministic_replay_count':len(samples)};assert runtime['python']==manifest['dependencies']['python'];assert manifest['dependencies']['packages']=={};save('runtime.json',runtime)
 reloc=E/'relocated-package';reloc.mkdir(exist_ok=True)
 for f in ['package.json']+manifest['files']:
  p=reloc/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PKG/f,p)
 for level in ['easy','moderate']:
  p=run([PY,'-B',reloc/manifest['entrypoint'],'--difficulty',level,'--seed',623982001,'--count',3],'relocation-'+level+'-command.json',reloc);assert p.returncode==0;rs=json.loads(p.stdout);save('relocated-'+level+'.json',rs);assert rs==[g.generate(level,623982001+i) for i in range(3)];checks(rs)
 save('packaging-results.json',{'relocation':'manifest files only, deterministic equality both difficulties','external_outputs':'stdout JSON only; no assets; bytecode disabled','package_unchanged':hashes()==read(E/'package-before.json')})
 # Do not run author's script in workspace: its writes target workspace/evidence.
 author=(PKG/'checks/regression.py').read_text();author=author.replace("W=pathlib.Path(__file__).resolve().parents[1]",'W=pathlib.Path('+repr(str(PKG))+')').replace("E=W/'evidence'","E=pathlib.Path("+repr(str(E/'author-check'))+")")
 (E/'author-regression.py').write_text(author);p=run([PY,'-B',E/'author-regression.py'],'author-regression-command.json');assert p.returncode==0
 # Same unchanged executable witness against old package, writing only here.
 author_old=author.replace(repr(str(PKG)),repr(str(PREV/'relocated-package'))).replace("(W.parent/'source/source.json')","(pathlib.Path("+repr(str(JOB/'source/source.json'))+"))").replace(repr(str(E/'author-check')),repr(str(E/'author-old-check')))
 (E/'author-old-regression.py').write_text(author_old);p=run([PY,'-B',E/'author-old-regression.py'],'author-old-regression-command.json');assert p.returncode!=0
 save('render-input.json',batch+controls+[next(r for r in samples if r['generation']['template']==name) for name in ['q-1068','q-1053','q-129128']])
 (E/'session-state.md').write_text('Milestone 2 complete: 10 complete source banks replay; fresh 80 sampled variants, boundary cases, counterfactuals and exact old witnesses checked with independent visible-equation parser. Author executable check rerun redirected here; same check fails old package. Manifest-only relocation and dependency contract pass. Native grading, delivery, shortcut analysis, inventory reconstruction and UI inspection pending. Package untouched.\n')
 print(json.dumps({'source_banks':len(replays),'fresh_samples':len(samples),'math_records':len(all_records),'counterfactual_records':len(controls),'boundary_records':len(bounds),'package_unchanged':hashes()==read(E/'package-before.json')}))
if __name__=='__main__':main()
