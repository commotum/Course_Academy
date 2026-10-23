import sys,ast,pathlib,json,hashlib,collections,importlib.util
sys.dont_write_bytecode=True
from helpers import mats,ops,check
ROOT=pathlib.Path(__file__).resolve().parent;JOB=ROOT.parent;PKG=JOB/'workspace'
s=importlib.util.spec_from_file_location('subject',PKG/'17592186161967.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
a=ast.parse((ROOT/'review.py').read_text());exec(compile(ast.Module(body=[n for n in a.body if isinstance(n,ast.FunctionDef) and n.name in ['bank','analyze','metrics']],type_ignores=[]),'analysis-functions','exec'))
def save(n,x):(ROOT/n).write_text(json.dumps(x,indent=2)+'\n')
sel={};post={};grade=[]
for name in ['batch','fresh']:
 rr=json.load(open(ROOT/f'delivery-{name}/accepted.json'));post[name]=metrics(rr);picks=[]
 for i in range(40):
  seed=f'independent-review-1-{i}';digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();ix=int(((int.from_bytes(digest[8:16],'big')>>11)/(1<<53))*len(rr));z=analyze(rr[ix]);picks.append({'seed':seed,'candidate_rank':ix,'id':z['id'],'shortcut_success':z['success']})
 sel[name]={'eligible_count':len(rr),'draws':picks,'shortcut_successes':sum(z['shortcut_success'] for z in picks),'draw_count':len(picks)}
 if name=='batch':
  for r in rr:
   z=analyze(r);grade.append({'label':'normalized batch shortcut','record':r,'checks':[{'submitted_answer_id':z['guess_id'],'expected':'accepted','purpose':'Bypass first operation using outlier sign, after actual delivery normalization'}]})
sel['captured_basis']=5580
sel['selection_rules']='Actual engine/rust/question_selection.rs inspected. All candidates easy. With positive easy weight, SHA256 offset 8 chooses uniformly within that band; 40 fresh deterministic seed examples per set. No learner history captured: empty history modeled; removal of previously seen questions cannot rescue the batch because each remaining record has the cue. Candidate order uses file rank; future entity ranks unknown. With absent weights actual selector uses first eligible record, which also has cue in this batch; zero easy weight makes this all-rated easy pool unavailable.'
sel['limits']='This is read-only captured-state modeling, not a claim about live policy settings or database publication. Original stored questions are outside generated-batch shortcut count.'
save('selection.json',sel);save('post-delivery-shortcuts.json',post);save('delivered-grader-input.json',grade)
assert json.load(open('relocated-output.json'))==g.batch('easy',3,91643)
p=json.load(open('packaging.json'));p.pop('relocation_pending');p['relocation_equal']=True
now={str(x.relative_to(PKG)):hashlib.sha256(x.read_bytes()).hexdigest() for x in PKG.rglob('*') if x.is_file()};assert now==json.load(open('package-before.json'));p['package_unchanged']=True;save('packaging.json',p)
save('retained-finding-results.json',{'finding_id':'d02e8980f26ead535fe5','preflight_claim_confirmed':True,'author_check_old':'Fails specifically Retained 36-case failure persists','author_check_current':'Passes with 9/36 old-cue successes and 52 identical-bank groups','independent_retained_old':'36/36, expected exit 1','independent_retained_current':'9/36, expected exit 0','fresh_independent_quartets':'All ten profiles admit all four signed answers with the same ordered bank; 20/40 opposite-outlier successes','new_failure':'Current delivered five-question batch has opposite-outlier-first-sign relationship in 5/5; batch-selection failure, not universal generator defect'})
save('scope-review.json',{'basis':'source-analysis.json','observed':'151 independently checked records use 3x3 integer matrices, two additions from unchanged pivot row, one five-choice radio field, no additional operators or steps. Source replay of ten complete banks passes.','boundary':'All nine pivot/column combinations; pivot -3, target entries +/-12 and multipliers +/-4. Fresh sample signs and targets recorded in shortcut-results.json.','unsupported':'Moderate/hard explicitly rejected; no observed source families excluded. Neighboring 4x4/column-operation KPs outside scope.','construction_limits':'Swap magnitude profiles require unequal coefficient magnitudes; unit profiles require at least one magnitude >1 so five distinct source-type choices exist. Equal coefficients remain supported by unit profiles. This justified distinct-choice restriction does not fix signs.'})
print(json.dumps({'post':{k:v['groups'] for k,v in post.items()},'selection_batch':sel['batch']['shortcut_successes'],'package_unchanged':True}))
