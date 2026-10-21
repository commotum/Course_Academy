import pathlib,json,sys,hashlib,collections,subprocess,importlib.util,copy
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P=J/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(P))
from independent_math import *
def read(p):return json.load(open(E/p))
def dump(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load(P/'17592186115241.py','current_final');prior=J/'review-1-policy-2-64575e53a5a82ae1';old=load(prior/'relocated/17592186115241.py','previous_final')
# Same strict fraction regression actually exits nonzero on the bound prior executable.
s=(E/'reproduce_shortcut.py').read_text().replace("P=E.parent/'workspace'",f"P=pathlib.Path({str(prior/'relocated')!r})").replace("'strict-new-regression.json'","'strict-prior-regression.json'")
(E/'strict_prior_fraction.py').write_text(s)
a=subprocess.run([sys.executable,'-B',str(E/'strict_prior_fraction.py')],capture_output=True,text=True);b=subprocess.run([sys.executable,'-B',str(E/'reproduce_shortcut.py')],capture_output=True,text=True)
assert a.returncode!=0 and b.returncode==0
p={'free_coefficients':[0,-3],'constants':[0,4],'mix':[1,1]};zero=[]
for label,gg in [('previous',old),('current',g)]:
 try:r=gg.generate_easy(seed=71381,parameters=p);zero.append({'version':label,'accepted':True,'record':r})
 except ValueError as ex:zero.append({'version':label,'accepted':False,'error':str(ex)})
assert not zero[0]['accepted'] and zero[1]['accepted']
# Exercise the author's executable assertion itself on a known failing baseline record.
sys.path.insert(0,str(E/'author-check'));ar=load(E/'author-check/rational_support.py','author_rational')
try:ar.inspect([old.generate_easy(seed=71381,profile='q-32244')]);author_failed=False
except AssertionError as ex:author_failed=True;failure=str(ex)
assert author_failed;ar.inspect([g.generate_easy(seed=71381,profile='q-32244')])
dump('repair-verification.json',{'retained_findings':json.load(open(J/'repair-history.json'))['findings'],'preflight':json.load(open(J/'repair-preflight.json')),'original_three_findings':'strict-regressions.json records historical failures and current passes, including complete generated witnesses.','fraction_strict_before':{'command':a.args,'exit':a.returncode,'stderr':a.stderr},'fraction_strict_after':{'command':b.args,'exit':b.returncode,'stderr':b.stderr},'author_assertion_before':{'failed':author_failed,'message':failure},'author_assertion_after':'passed same inspect assertion on current seed71381','zero_constant_boundary':zero,'author_current_executables':{'validate_repair':(E/'author-check/validate-console.txt').read_text(),'rational_support':(E/'author-check/rational-console.txt').read_text()},'copy_adjustments':'Only root/output paths changed in copied author checks; originals were never run with package output directories.'})
# Correct the inherited selection narrative and retain executable formulas.
I=json.load(open(J/'source/inventory.json'));batches=read('delivery-batch/accepted.json');draws=[]
for i in range(30):
 seed='independent-review-v1.1.1-'+str(i);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);draws.append({'seed':seed,'candidate_rank':int(u*len(batches))})
bands=collections.defaultdict(list)
for q in I['questions']:
 d=q.get(':question/difficulty');bands[d[':db/ident'].split('/')[-1] if d else 'unrated'].append(q[':db/id'])
for key in bands:bands[key].sort()
dump('learner-selection.json',{'implementation':'engine/rust/question_selection.rs select() and seen_before_task(), directly inspected','implementation_sha256':hashlib.sha256((R/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'captured_basis':I['basis'],'captured_band_candidates':dict(bands),'examined_rules':['exclude prior tasks and current prefix','sort/deduplicate numeric entity candidates','nonempty positive-weight difficulty band, then uniform candidate rank','unconfigured policy selects first numeric ID','unrated fallback only when no positive-weight rated band remains'],'batch_easy_candidate_count':len(batches),'batch_rank_draws':draws,'pre_post_decision_coverage':'delivery-shortcuts.json','source_variant_candidates':55,'source_unique_fraction_cues':0,'result':'No normalization/dedup or difficulty losses. Easy-band selection does not favor a mathematical case within the surviving candidate pool. Every batch candidate was independently audited, including the first-candidate fallback. The same analysis applies to all source-support candidates.','limits':['Future numeric IDs, live learner histories and configured weights are unavailable; no claim about a particular learner draw or probability across difficulty bands.','Seen exclusions can reduce coverage; audited banks are unchanged by selection.','Captured moderate/hard historical component defects remain recorded in affected-inventory.json; they are outside the requested easy batch.']})
# Control measurements and notation signatures after actual delivery.
controls=read('cue-control-records.json');ac=read('delivery-controls/accepted.json');assert len(controls)==len(ac)==24
from probes import summary
stats=read('delivery-shortcuts.json');stats['cue-control-records.json']=summary(controls);stats['delivery-controls/accepted.json']=summary(ac);dump('delivery-shortcuts.json',stats)
cr=read('changed-probe-results.json');assert all(r['math']['pass'] for r in cr['rows'])
for template in ['authored_easy_equal_coordinates','authored_easy_free_y']:
 assert len(cr['summary'][template]['key_positions'])>1
# Verify the apparent minimum-intercept predictor against independently selected controls.
z=cr['summary']['authored_easy_equal_coordinates']['cues']['first_intercept_min'];assert z['correct']<z['total']
dump('controlled-validation.json',{'integer':read('counterfactual-results.json'),'rational':read('rational-counterfactual-results.json'),'native_controlled_outcomes':[r for r in read('grader-results.json')['records'] if 'controlled-previous-vector' in r['label']],'rendered_pairs':['render-all/question-012.png','render-all/question-013.png','render-all/question-014.png','render-all/question-018.png','render-all/question-019.png','render-all/question-020.png'],'conclusion':'Relevant coefficient changes alter the printed problem, worked solution and complete solution vector; actual grader rejects the old vector. Invertible row mixing changes evidence but preserves the solution, which the real grader accepts.'})
# Captured inventory's historical record conclusions are kept separate from current generation.
inv=read('inventory-results.json');inv['limits'].append('No new affected generated inventory records demonstrated for repaired rational cue. The captured 24-question inventory contains 14 original source records and 10 historical moderate/hard generated records. Other concerns were not exhaustively tested.');dump('inventory-results.json',inv)
# Scope and rendering inspection record.
dump('scope-review.json',{'source_refs':['tutorial 3eff050b-e4ba-52e5-aa10-7bba2feef2fc','dc6dd9b4-de7f-52d0-8ff9-a7a7f7a9abd7','cbdb5209-5ae6-5fea-a525-87f604e2410b'],'records':['batch.json','fresh.json','source-shortcut-records.json','cue-control-records.json'],'observations':['Same five-choice radio contract, linear equations and one free real parameter.','Both source-backed shapes retained: rank-two 2x3 and rank-one 3x2 coefficient matrices.','Rational answer pools match each coordinate coefficient denominator, preserving source arithmetic without a reserved key signature.','Zero coordinate may be fixed in all choices, an acceptable simplification because another coordinate still determines the solution line.','All-zero basic coordinates declare otherwise absent z as +0z; the ambient variable list remains visible.','Default cases use a few elementary row operations; explicit boundary workload remains comparable.'],'unsupported':'Requested easy only; historical moderate/hard source fidelity and difficulty are not recertified.'})
# Final integrity uses every file, including non-manifest evidence accidentally touched by an import.
before=read('package-before.json');after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()};assert before==after
dump('package-integrity.json',{'before_file_count':len(before),'after_file_count':len(after),'changed':[],'unchanged':before==after,'database_writes':0,'published_assets':0})
print(json.dumps({'strict_fraction_before_exit':a.returncode,'after_exit':b.returncode,'zero_boundary_repaired':True,'equal_coordinate_min_intercept_control':z,'package_unchanged':True}))
