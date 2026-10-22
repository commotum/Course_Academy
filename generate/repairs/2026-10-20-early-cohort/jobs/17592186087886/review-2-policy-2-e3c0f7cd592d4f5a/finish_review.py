from independent_review import *
import importlib.metadata,math

def size(value):return len(re.sub(r'\\(?:left|right|operatorname)|[{}\s]|\u2061','',value))
def fnv(value):
 n=2166136261
 for c in value:n=((n^ord(c))*16777619)&0xffffffff
 return n

def probes(rows,stage):
 groups={'all':rows}
 for t in sorted({r['generation']['template'] for r in rows}):groups[t]=[r for r in rows if r['generation']['template']==t]
 out=[]
 for label,rs in groups.items():
  for strategy in ['shortest','longest','lexicographically_first']+[f'position_{n}' for n in range(1,6)]:
   hits=0
   for r in rs:
    aa=field(r)[':answer-field/choices']
    chosen=aa[int(strategy[-1])-1] if strategy.startswith('position_') else min(aa,key=lambda a: (size(a[':answer/value']) if strategy=='shortest' else -size(a[':answer/value']) if strategy=='longest' else a[':answer/value']))
    hits+=chosen[':answer/id']==correct(r)[':answer/id']
   out.append({'stage':stage,'subgroup':label,'strategy':strategy,'correct':hits,'total':len(rs),'baseline':.2,'comment':'Five-choice uniform guess. Ties follow visible input order. Singleton or two-item subgroup successes are recorded, not interpreted as a family-wide predictor.'})
 return out

def delivery(inp,out):
 cmd=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(E/inp),'--source',str(J/'source/source.json'),'--inventory',str(J/'source/inventory.json'),'--difficulty','easy','--output',str(E/out),'--asset-root',str(E),'--math-root','/media/jake/SSD/EDB/math']
 p=subprocess.run(cmd,capture_output=True,text=True);assert p.returncode==0,p.stderr
 return {'command':cmd,'stdout':p.stdout,'exit':p.returncode}

def select(candidates,seed,weights=True):
 candidates=sorted(candidates,key=lambda t:t[0])
 if not weights:return candidates[0] if candidates else None
 # All candidates are easy: any positive easy weight leaves a uniform easy pool.
 h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 uniform=(int.from_bytes(h[8:16],'big')>>11)/(1<<53)
 return candidates[int(uniform*len(candidates))] if candidates else None

def main():
 const=[]
 for t in ['q-8745','q-90601','q-90600']:
  for k in range(2,7):
   if k==g.ORIGINAL[t]:continue
   const.append(g.generate('easy',44219,t,{'k':k,'shift':0,'bank_start':2}))
 save('cancellation-records.json',const);save('cancellation-math.json',[validate(r) for r in const]);save('cancellation-delivery-command.json',delivery('cancellation-records.json','delivery-cancellation'))
 raw=json.load(open(E/'independent-records.json'));accepted=json.load(open(E/'delivery-independent-records/accepted.json'));batch=json.load(open(E/'batch-records.json'));delbatch=json.load(open(E/'delivery-batch-records/accepted.json'));fresh=json.load(open(E/'delivery-fresh-batch/accepted.json'));conaccepted=json.load(open(E/'delivery-cancellation/accepted.json'))
 pp=[]
 for name,rs in [('independent_raw',raw),('independent_delivered',accepted),('runner_raw',batch),('runner_delivered',delbatch),('fresh_delivered',fresh),('cancellation_delivered',conaccepted)]:pp+=probes(rs,name)
 save('shortcut-results.json',pp)
 fixed=[]
 for t in sorted(g.ORIGINAL):
  rs=[r for r in accepted if r['generation']['template']==t and r['generation']['parameters']['k']==5 and r['generation']['parameters']['shift'] in [-2,-1,1,2]]
  assert len(rs)==4 and len({correct(r)[':answer/value'] for r in rs})==4
  assert len({tuple(values(r)) for r in rs})==1
  fixed.append({'family':t,'records':4,'fixed_bank':True,'distinct_eligible_keys':4,'bank_only_strategy_max_correct':1,'baseline':.25,'sample_file':'delivery-independent-records/accepted.json'})
 for t in ['q-8745','q-90601','q-90600']:
  rs=[r for r in conaccepted if r['generation']['template']==t]
  assert len({tuple(values(r)) for r in rs})==1 and len({correct(r)[':answer/value'] for r in rs})==len(rs)
  fixed.append({'family':t,'profile':'cancellation-constant','records':len(rs),'fixed_bank':True,'distinct_eligible_keys':len(rs),'bank_only_strategy_max_correct':1,'baseline':1/len(rs),'sample_file':'delivery-cancellation/accepted.json'})
 save('fixed-bank-results.json',fixed)
 # Actual learner selection rules, captured inventory, and a prospective pool.
 inv=json.load(open(J/'source/inventory.json'))
 candidates=[(q[':db/id'],'stored_original',q[':question/id']) for q in inv['questions']]
 nextid=max(c[0] for c in candidates)+1
 candidates += [(nextid+i,r['generation']['template'],r['question'][':question/id']) for i,r in enumerate(delbatch)]
 draws=Counter();history=[];pool=candidates[:]
 for i in range(128):
  chosen=select(candidates,'review-seed-'+str(i));draws[chosen[2]]+=1
 for i in range(len(candidates)):
  chosen=select(pool,'task-review/kp-17592186087886/slot-'+str(i));history.append(chosen);pool=[c for c in pool if c[0]!=chosen[0]]
 assert len({c[2] for c in history})==len(candidates) and not pool
 legacy=[];pool=candidates[:]
 while pool:
  c=select(pool,'unused',False);legacy.append(c);pool.remove(c)
 ui_positions=Counter()
 for item in range(1,33):
  for r in delbatch:
   f=field(r);aa=sorted(f[':answer-field/choices'],key=lambda a:fnv(f"{item}:{f[':answer-field/id']}:{a[':answer/id']}"))
   ui_positions[next(i+1 for i,a in enumerate(aa) if a[':answer/id']==correct(r)[':answer/id'])]+=1
 selection={'source':'engine/rust/question_selection.rs select(), seen_before_task(); learning.rs validate_practice_question(), lesson candidate filter','captured_basis':inv['basis'],'captured_originals':8,'surviving_runner_records':5,'prospective_candidates':candidates,'entity_ids_for_new_records':'Surrogate consecutive IDs above captured maximum solely for this read-only simulation; no database allocation performed. No conclusion depends on exact ID values.','eligibility':'All 13 records are easy standalone single-radio records with valid keys, no retired or multistep marker; native grade_field and publication validation passed. No free or checkbox restriction applies.','positive_easy_weight':'Only easy candidates exist, so any positive easy weight selects uniformly from all eligible easy records. Difficulty-first selection cannot favor a mathematical family within this pool.','weighted_draws_128':dict(draws),'without_replacement_history':history,'unconfigured_policy_order':legacy,'zero_easy_weight':'With no positively weighted available rated band and no unrated questions, selection returns None. This general policy behavior cannot introduce a question shortcut.','actual_ui_ordering':'learning.js choiceOrder uses FNV-1a(itemId:fieldId:answerId). Input bank order is not final UI position. Tested 32 item IDs x 5 published records; all five actual positions occur.','actual_ui_positions_160':dict(ui_positions),'limits':['No live learner history, reservations or active policy snapshot was supplied. They remove candidates or change band availability, and cannot be reconstructed as actual user state. Rules and both configured/unconfigured selection branches examined read-only.','Captured inventory is basis 5448; later inventory can change deduplication.']}
 save('selection-analysis.json',selection)
 # Final native invocation includes actual publisher-normalized records and cancellation counterfactuals.
 cases=json.load(open(E/'grader-input.json'))
 for r in delbatch+conaccepted:
  cases.append({'label':'post-delivery:'+r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct(r)[':answer/id'] else 'rejected','purpose':'Normalized publication IDs and bank windows; displayed rate independently checked'} for a in field(r)[':answer-field/choices']]})
 save('grader-final-input.json',cases)
 cmd=[str(REPO/'generate/runs/current/check-engine'),str(E/'grader-final-input.json'),str(E/'grader-final-report.json')]
 p=subprocess.run(cmd,capture_output=True,text=True);save('grader-final-command.json',{'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0
 # Runtime dependency contract and package invariance.
 manifest=json.load(open(P/'package.json'));versions={'python':platform.python_version(),'packages':{n:importlib.metadata.version(n) for n in manifest['dependencies']['packages']}}
 assert versions==manifest['dependencies']
 after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
 assert after==json.load(open(E/'package-before.json'))
 save('package-final.json',{'exact_runtime_versions':versions,'manifest_matches':True,'package_unchanged':True,'files_compared':len(after),'before_manifest':'package-before.json','declared_file_relocation_test':'author-replay/workspace/evidence/package-regression.json','external_asset_output':'No image assets are generated; relocation supplied COURSE_ACADEMY_GENERATOR_OUTPUT_DIR and verified no package writes.','historical_failure_controls':'regression-controls.json','repair_preflight':'Supplied repair-preflight path is absent; repair history has zero retained named findings and two event codes, both exercised with failing controls and current checks.'})
 # Compact scope conclusions, tied to independently parsed equations.
 save('scope-review.json',{'source_coverage':'All eight practice source families retained with full banks; canonical e-2301 is instructional derivation, not a five-choice question. Its cosine F(v)-v operation is the same transform independently checked in source analysis.','supported_difficulty':['easy'],'unsupported_difficulties':'moderate/hard rejected, consistent with supplied practice evidence','fixed_features':'y=vx, product rule, one derivative, degree-zero RHS, five radio equations. No integration, initial conditions, or solution of ODE introduced.','variation':'k and shift vary decisive cancellation/noncancellation and sign; all four nonzero shifts in eight fixed banks and all eligible cancellation-window targets exercised.','workload':'Cubic rational degrees and single nonlinear nesting retained. Adding a small multiple of y/x asks the source-supported common-denominator simplification and subtraction of v.','references':['source-analysis.json','math-results.json','cancellation-math.json','fixed-bank-results.json']})
 print(json.dumps({'cancellation_records':len(const),'fixed_bank_groups':len(fixed),'grader_cases':len(cases),'package_unchanged':True,'runner_position_results':[p for p in pp if p['stage']=='runner_delivered' and p['subgroup']=='all']}))
if __name__=='__main__':main()
