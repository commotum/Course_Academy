import sys
sys.dont_write_bytecode=True
import json,pathlib,importlib.util,ast,re,collections,hashlib,platform,shutil
import sympy as sp
R=pathlib.Path(__file__).resolve().parent;J=R.parent;P=J/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(n,d):(R/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def read(n):return json.loads((R/n).read_text())
def load(p):
 s=importlib.util.spec_from_file_location('candidate',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
# Independent mathematical parser and shortcut carried forward from original independent review.
for n in ast.parse((R/'review_checks.py').read_text()).body:
 if isinstance(n,ast.FunctionDef) and n.name in ['key','pars','ex','shortcut'] or isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='EX' for x in n.targets):exec(compile(ast.Module(body=[n],type_ignores=[]),'<prior independent helpers>','exec'))
m=load(P/'17592186229181.py'); t=sp.Symbol('t',real=True)
source=json.loads((J/'source/source.json').read_text());batch=json.loads((J/'samples.json').read_text());save('batch.json',batch)
# Fresh bounded sample, exact prior seed and physical counterexample, both arithmetic boundaries.
samples=[m.generate('easy',seed) for seed in range(519401,519421)]
samples+=[m.generate('easy',81031),m.generate('easy',81031,parameters=read('previous-minimal-failure.json')['record']['generation']['parameters'])]
for p in [dict(V=300,r=10,c='.01',q0=1,context='salt'),dict(V=1000,r=50,c='.06',q0=25,context='dye')]:samples.append(m.generate('easy',7443,parameters=p))
extras=[m.generate(level,519401+i) for level in ['moderate','hard'] for i in range(2)]
save('easy-samples.json',samples);save('extra-samples.json',extras)
bank={'c':['.02','.04'],'q0':[5,16],'r':[15,30]};corners=((0,0,0),(0,1,1),(1,0,1),(1,1,0),(1,1,1));cf=[];inputs=[]
for role,bits in enumerate(corners):
 p=dict(V=600,context='coolant',**{k:bank[k][bits[j]] for j,k in enumerate(('c','q0','r'))});cf.append(m.generate('easy',75493,parameters=p,bank=bank,role=role));inputs.append(dict(seed=75493,parameters=p,bank=bank,role=role))
p=dict(inputs[4]['parameters'],context='pollutant');cf.append(m.generate('easy',75493,parameters=p,bank=bank,role=4));inputs.append(dict(seed=75493,parameters=p,bank=bank,role=4))
save('counterfactual-records.json',cf);save('counterfactual-inputs.json',inputs)
allgroups=[('sample',samples),('extra',extras),('batch',batch),('counterfactual',cf)]
math=[];grades=[]
def cv(q):return next(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==key(q))
for group,records in allgroups:
 for i,rec in enumerate(records):
  q=rec['question'];V,q0,c,r,time=pars(q);E=V*c;expected=E+(q0-E)*sp.exp(-r*t/V);opts=q[':question/answer-fields'][0][':answer-field/choices'];truth=[]
  for a in opts:
   if time is None:
    e,b,k=ex(a[':answer/value']); f=e+b*sp.exp(-k*t); good=sp.expand(sp.diff(f,t)-(r*c-r*f/V))==0 and e+b==q0
   else:good=abs(float(re.match(r'[0-9.]+',a[':answer/value'])[0])-float(expected.subs(t,time)))<.005
   if good:truth.append(a[':answer/id'])
  sol=q[':question/worked-solution'];eqs=list(EX.finditer(sol));e,b,k=ex(eqs[-1][0]);solgood=sp.expand(e+b*sp.exp(-k*t)-expected)==0
  # Verify source-derived intermediate rates, IC and time constant rather than only final key.
  ns=lambda n:format(float(n),'.10f').rstrip('0').rstrip('.')
  intermediates=(r'\frac{Q}{'+ns(V)+'}' in sol and r'\frac{dQ}{dt}+\frac{1}{'+ns(V/r)+'}Q=' in sol and sol.count('**Step ')==4)
  ic=re.search(r'A & =(-?[\d.]+)\\end',sol);intermediates &= bool(ic) and sp.Rational(ic[1])==q0-E
  row={'group':group,'index':i,'seed':rec['generation']['seed'],'id':q[':question/id'],'prompt_parameters':list(map(str,(V,q0,c,r,time))),'unique_correct':truth==[key(q)],'solution_final':solgood,'intermediate_solution':bool(intermediates),'passed':truth==[key(q)] and solgood and bool(intermediates)};math.append(row)
  grades.append({'label':group+'-'+str(i),'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id'] in truth else 'rejected','purpose':'independent prompt-derived ODE and initial condition oracle'} for a in opts]})
save('math-results.json',{'cases':math,'passed':all(x['passed'] for x in math)})
# Exact full source replay; key values as well as presence.
replay=[];rs=[]
for q in source['material']['kp'][':knowledge-point/questions']:
 level='moderate' if 'rounded' in q[':question/problem'] else 'easy';rec=m.generate(level,61829,template='source_'+str(q[':db/id']));rq=rec['question'];errs=[]
 for f in [':question/problem',':question/worked-solution']:
  if rq.get(f)!=q.get(f) or (f in rq)!=(f in q):errs.append(f)
 if rq.get(':question/difficulty')!=q.get(':question/difficulty',{}).get(':db/ident'):errs.append('difficulty')
 bankvalues=lambda a:sorted(o[':answer/value'] for o in a[':question/answer-fields'][0][':answer-field/choices'])
 if bankvalues(q)!=bankvalues(rq):errs.append('complete bank')
 if bool(key(q))!=bool(key(rq)) or (key(q) and cv(q)!=cv(rq)):errs.append('key')
 rs.append({'source_id':q[':question/id'],'entity':q[':db/id'],'differences':errs,'passed':not errs});replay.append(rec)
 if key(rq):grades.append({'label':'source-'+q[':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(rq) else 'rejected','purpose':'replay original bank whose unique mathematics is checked in source-math.json'} for a in rq[':question/answer-fields'][0][':answer-field/choices']]})
save('source-replay-records.json',replay);save('source-replay.json',{'cases':rs,'passed':all(x['passed'] for x in rs),'source_math_reused':'source-math.json; matching source hash, all unique source keys already independently verified'})
# Fixed visible bank under all five eligible target assignments, then irrelevant noun change.
values=lambda rec:[a[':answer/value'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]
cvs=[cv(rec['question']) for rec in cf];pairs=[]
for coordinate,first in [('flow',3),('initial_amount',2),('feed_concentration',1),('context',4)]:
 last=5 if coordinate=='context' else 4
 before=pars(cf[first]['question']);after=pars(cf[last]['question']);diff=[j for j,(a,b) in enumerate(zip(before,after)) if a!=b]
 pairs.append({'coordinate':coordinate,'before_index':first,'after_index':last,'changed_prompt_coordinates':diff,'ordered_bank_same':values(cf[first])==values(cf[last]),'answer_changed':cvs[first]!=cvs[last],'expected':'preserve' if coordinate=='context' else 'change','passed':(cvs[first]==cvs[last])==(coordinate=='context') and values(cf[first])==values(cf[last]),'native_case_refs':['counterfactual-'+str(first),'counterfactual-'+str(last)]})
save('counterfactual-results.json',{'pairs':pairs,'all_five_target_values_distinct':len(set(cvs[:5]))==5,'all_banks_identical':all(values(x)==values(cf[0]) for x in cf),'correct_values':cvs,'passed':all(x['passed'] for x in pairs) and len(set(cvs[:5]))==5,'render_file':'render/rendering.json','grader_file':'grader-report.json'})
# Invalid inputs and exact runtime/relocation. Only declared runtime files copied.
manifest=json.loads((P/'package.json').read_text());rel=R/'relocated';rel.mkdir(exist_ok=True)
for fn in manifest['files']:
 target=rel/fn;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/fn,target)
reloc=load(rel/manifest['entrypoint']);base=dict(V=500,r=25,c='.02',q0=7,context='coolant');rej=[]
for label,p in [('zero flow',dict(base,r=0)),('zero volume',dict(base,V=0)),('unknown context',dict(base,context='unknown')),('equilibrium',dict(base,q0=10)),('zero concentration',dict(base,c=0)),('outside arithmetic',dict(base,V=299))]:
 try:m.generate('easy',75493,parameters=p);ok=False;error='accepted'
 except ValueError as e:ok=True;error=str(e)
 rej.append(dict(case=label,rejected=ok,error=error,parameters=p))
save('packaging.json',{'runtime':{'python':platform.python_version(),'packages':{'sympy':sp.__version__}},'declared':manifest['dependencies'],'exact_version_match':manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':sp.__version__}},'deterministic':m.generate('easy',519401)==samples[0],'relocation':reloc.generate('easy',519401)==samples[0],'rejections':rej,'external_outputs':'No asset, network or database output code. stdout CLI only.','boundaries':'Samples 22 and 23 cover V=300,r=10,c=.01,q0=1 and V=1000,r=50,c=.06,q0=25.'})
save('grader-input.json',grades);save('render-input.json',batch+cf+[extras[0]])
# In current bank equal coordinate multiplicities are shared 2/3; initial value+equilibrium/rate matching is intended mathematics.
def probes(records,group):
 out=[]
 for cue in ['position-first','shortest','largest-leading-constant','smallest-leading-constant','old-intersection']:
  correct=0;abstain=0
  for rec in records:
   q=rec['question'];opts=q[':question/answer-fields'][0][':answer-field/choices']
   if cue=='old-intersection':pick=shortcut(q)
   elif cue=='position-first':pick=opts[0][':answer/id']
   elif cue=='shortest':pick=min(opts,key=lambda o:len(o[':answer/value']))[':answer/id']
   else:pick=sorted(opts,key=lambda o:ex(o[':answer/value'])[0],reverse=cue.startswith('largest'))[0][':answer/id']
   correct+=pick==key(q);abstain+=pick is None
  out.append(dict(cue=cue,subgroup=group,correct=correct,total=len(records),abstained=abstain,baseline=.2))
 return out
out=probes(samples,'raw easy')+probes(batch,'exact runner batch')+probes(cf[:5],'fixed-bank all five targets')
for context in sorted({r['generation']['parameters']['context'] for r in samples}):out+=probes([r for r in samples if r['generation']['parameters']['context']==context],'context '+context)
for sign in [True,False]:out+=probes([r for r in samples if (pars(r['question'])[1]<pars(r['question'])[0]*pars(r['question'])[2])==sign], 'increasing' if sign else 'decreasing')
save('shortcut-results.json',out)
save('independent-summary.json',{'math_cases':len(math),'math_passed':all(x['passed'] for x in math),'source_replay_passed':all(x['passed'] for x in rs),'counterfactual_passed':all(x['passed'] for x in pairs),'fresh_seeds':list(range(519401,519421)),'retained_counterexamples':[81031],'command':sys.executable+' '+str(R/'independent_checks.py')})
(R/'session-state.md').write_text('Source account reused with confirmed passages. Current and negative retained regressions run. Fresh bounded math/source replay, controlled bank-target changes, boundary/rejection and relocation complete. Pending delivery/grader/renderer and final report.\n')
print(json.dumps(read('independent-summary.json')))
