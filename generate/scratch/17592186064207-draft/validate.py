"""Independent exact QA of rendered prompt, substitution, every integration and C/K stage."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,re,subprocess,time
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('draft64207',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);p=g.parser

def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def normal(e):return p.log_normal(e)
def eq(a,b):return s.simplify(normal(a)-normal(b))==0
def integral(term,d):
 term=term.strip().rstrip('.')
 coef,tail=term.split(r'\int',1);m=re.search(r'\\text\{d\}([xu])',tail);assert m,term
 expression=tail[:m.start()].rstrip(' ,').removesuffix(r'\,');assert not tail[m.end():].strip(),term
 coef=coef.strip();factor=1 if not coef or coef=='+' else -1 if coef=='-' else p.scalar(coef)
 return s.cancel(factor*p.scalar(expression).subs(p.u,d)*(s.diff(d,p.x) if m[1]=='u' else 1))
def check(z,allow_bank_ambiguity=False):
 q=z['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];f=p.integral_operands(prompt)[0]
 # Independently read uncancelled task denominator and numerator; metadata is checked after parsing.
 n,den=s.fraction(f);a=s.diff(den,p.x);b=den.subs(p.x,0);assert a!=0 and not a.has(p.x)
 match=re.search(r'First, let \$u=([^$]+)\$',sol);assert match
 d=p.scalar(match[1]);assert s.cancel(d-den)==0
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==4
 differential=blocks[0].rstrip('.');left,right=differential.split('⟹');aa=p.scalar(left.split('=')[1].removesuffix(r'\,'));assert aa==s.diff(d,p.x)
 jj=right.split('=')[1].removesuffix(r'\text{d}u').rstrip(' ,').removesuffix(r'\,');jj=1 if jj=='' else -1 if jj=='-' else p.scalar(jj);assert aa*jj==1
 alpha=s.cancel(f*d/a);assert not alpha.has(p.x);mapping=alpha*s.log(p.K)
 prosemap=re.search(r'writing \$C\s*=\s*([^$]+)\$',sol);assert prosemap
 assert eq(p.scalar(prosemap[1]),mapping),('wrong prose C mapping',prosemap[1],alpha)
 counts={'formal_integral_terms':0,'primitive_terms':0,'constant_equalities':0}
 for bi in (1,2,3):
  body=blocks[bi].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').rstrip('.')
  for row in body.split(r'\\'):
   for term in re.split(r'&\s*=?|=',row):
    term=term.strip()
    if not term:continue
    if r'\int' in term:
     assert s.cancel(integral(term,d)-f)==0,('wrong integral stage',term,f);counts['formal_integral_terms']+=1
    else:
     e=p.scalar(term).subs(p.u,d);assert s.cancel(p.derivative(e)-f)==0,('wrong primitive stage',term,f)
     assert eq(e.subs(p.C,mapping),alpha*s.log(p.K*s.Abs(d))),('wrong C/K equality',term,alpha)
     counts['primitive_terms']+=1;counts['constant_equalities']+=1
 assert counts['primitive_terms']>=6 and counts['formal_integral_terms']>=4,counts
 field=q[':question/answer-fields'][0];bank=field[':answer-field/choices'];assert len(bank)==5
 vals=[p.scalar(c[':answer/value']) for c in bank];ds=[p.derivative(v) for v in vals]
 key=field[':answer-field/correct'][1];assert len({c[':answer/id'] for c in bank})==5
 for c,der in zip(bank,ds):
  if not allow_bank_ambiguity:assert (s.cancel(der-f)==0)==(c[':answer/id']==key),(c,der,f)
  elif c[':answer/id']==key:assert s.cancel(der-f)==0
 if not allow_bank_ambiguity:
  for i,j in itertools.combinations(range(5),2):assert s.cancel(ds[i]-ds[j])!=0,'ambiguous bank modulo arbitrary constant'
 assert z['generation']['mathematical_fingerprint']==g.digest(str(s.cancel(f)))
 assert z['generation']['domain']['excluded_poles']==[str(-b/a)]
 return counts

def main():
 started=time.time();sourcecases=[];rawcases=[];reviewcases=[];replay=[];ledger=[];native=[];reviews=[];stats=[]
 for sid,t in g.ANCHORS.items():
  raw=g.raw(sid);case=g.source_case(sid);assert case['raw']==raw;rawcases.append(case)
  prompt,solution=g.render(sid,t['parameters']);assert prompt==g.fmt.normalize_prose(raw[':question/problem']);assert solution==g.fmt.normalize_prose(raw.get(':question/worked-solution',''))
  vals=[g.fmt.normalize_tex(g.recipe(r,t['parameters'])) for r in t['recipes']];fields=raw.get(':question/answer-fields',[]);choices=[c for f in fields for c in f.get(':answer-field/choices',[])]
  assert len(vals)==len(choices)
  # Compare complete functions at the same K (stronger than derivative); exactly one match per choice.
  matches=[]
  for c in choices:
   match=[i for i,v in enumerate(vals) if eq(p.scalar(v),p.scalar(c[':answer/value']))];assert len(match)==1,(sid,c,match);matches+=match
  assert len(set(matches))==len(choices)
  key=next((f.get(':answer-field/correct') for f in fields),None)
  designated=None
  if key:
   designated=next(i for i,c in enumerate(choices) if c[':answer/id']==key[':answer/id']);assert eq(p.scalar(vals[designated]),p.scalar(key[':answer/value']))
  replay.append({'source_id':sid,'MA':':question/math-academy-id' in raw,'complete_bank':True,'matched_choices':len(choices),'total_choices':len(choices),'correct_designation_preserved':bool(key),'missing_key_preserved':not bool(key),'prompt':True,'solution_or_omission':True,'eligible':case['public_replay_eligible'],'issues':case['issues']})
  # Every observed recipe is also exercised at changed parameters, even excluded source banks.
  n,a,b=t['parameters'];changed=[n if n==1 else n+1,a if a==-1 else a+(1 if a>0 else -1),b+2]
  for i,r in enumerate(t['recipes']):ledger.append({'source_id':sid,'field':'selection','choice_index':i,'original_value':choices[i][':answer/value'],'correct':None if not key else i==designated,'recipe':r,'original_rendered':vals[i],'original_exact_function_match':True,'changed_parameters':changed,'changed_rendered':g.recipe(r,changed),'interpretation':'observed algebraic expression; error interpretation not asserted'})
  item={'source_id':sid,'basis':2275,'raw':raw,'replay':case,'parameters':t['parameters'],'rendered_prompt':prompt,'rendered_solution':solution,'rendered_values':vals}
  replayq=copy.deepcopy(raw);replayq[':question/problem']=prompt
  if ':question/worked-solution' in replayq:replayq[':question/worked-solution']=solution
  if ':question/difficulty' in replayq:replayq[':question/difficulty']=replayq[':question/difficulty'][':db/ident']
  for f in replayq.get(':question/answer-fields',[]):
   f[':answer-field/type']=f[':answer-field/type'][':db/ident']
   for c in f.get(':answer-field/choices',[]):c[':answer/type']=c[':answer/type'][':db/ident'];c[':answer/value']=g.fmt.normalize_tex(c[':answer/value'])
   if f.get(':answer-field/correct'):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  item['public_replay_eligible']=case['public_replay_eligible'];item['record']={'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':replayq,'generation':{'template':'exact-source-replay','source_id':sid,'origin':'raw_source_evidence','public_replay_eligible':case['public_replay_eligible'],'source_basis':2275}}
  if ':question/math-academy-id' in raw:sourcecases.append(item)
  reviews.append('## '+sid+'\n\nOriginal frozen prompt\n\n'+raw[':question/problem']+'\n\nOriginal bank\n\n'+'\n'.join('- $'+c[':answer/value']+'$' for c in choices)+'\n\nStatus: '+('; '.join(case['issues']) or 'eligible')+'\n')
 # Context ordered chain, using first/next rather than assuming array order.
 lesson=g.json.loads((HERE/'lessons.json').read_text())['record'][0];steps={v[':db/id']:v for v in lesson[':activity/steps']};chain=[];cursor=lesson[':activity/first-step'][':db/id']
 while cursor is not None:
  z=steps[cursor];c=z[':step/content'];chain.append({'step':cursor,'content_id':c[':db/id'],'title':c.get(':tutorial/title',c.get(':knowledge-point/title'))});cursor=z.get(':step/next',{}).get(':db/id')
 save('ordered-context.json',{'basis':2275,'chain':chain,'hard':'Conservative larger nonunit numerator and signed slope (7..15), signed nonzero intercept; exactly the same substitution and single-log constant stages; no subsequent combined-integral KP skill used.','prerequisite_topics':g.json.loads((HERE/'topics.json').read_text())['record'][':topic/_next']})
 for difficulty in g.LEVELS:
  for sid in g.profiles(difficulty):
   rows=[]
   # Original observed anchors, plus signed and boundary parameter variation.
   if not sid.startswith('authored:'):
    anchor=g.ANCHORS[sid.split(':')[-1]]['parameters']
    if g.eligible(sid,anchor,difficulty) and g.valid_bank(sid,anchor):rows.append(g.generate(difficulty,0,sid,anchor))
   for seed in range(200):
    z=g.generate(difficulty,seed+100,sid)
    if any(v['generation']['mathematical_fingerprint']==z['generation']['mathematical_fingerprint'] for v in rows):continue
    rows.append(z)
    if len(rows)==6:break
   assert len(rows)==6
   for z in rows:
    result=check(z);stats.append({'difficulty':difficulty,'profile':sid,'parameters':z['generation']['parameters'],**result});reviewcases.append(z)
    assert z['question']==g.generate(difficulty,-15,sid,z['generation']['parameters'])['question']
    field=z['question'][':question/answer-fields'][0];key=field[':answer-field/correct'][1]
    checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key else 'rejected','purpose':'owned correct option' if c[':answer/id']==key else 'owned option with wrong derivative'} for c in field[':answer-field/choices']]
    checks.extend([{'submitted':v,'expected':'unresolved','purpose':'foreign or malformed radio input'} for v in ('foreign-answer-id','','99999999')]);native.append({'label':sid+' '+str(z['generation']['parameters']),'record':z,'checks':checks})
   reviews.append('## '+sid+' normal original/variant comparison\n\n'+g.markdown(rows[0])+'\n\n---\n\n'+g.markdown(rows[-1]))
 # Validate actual frozen solution prose/stages independently, including non-MA and the fieldless source.
 sourceverification=[]
 for sid,t in g.ANCHORS.items():
  raw=g.raw(sid)
  if not raw.get(':question/worked-solution'):continue
  q=copy.deepcopy(raw);q[':question/problem']=g.fmt.normalize_prose(q[':question/problem']);q[':question/worked-solution']=g.fmt.normalize_prose(q[':question/worked-solution'])
  if not q.get(':question/answer-fields'):
   q[':question/answer-fields']=g.generate('moderate',0,'complete:q-49515',t['parameters'])['question'][':question/answer-fields']
  else:
   for f in q[':question/answer-fields']:
    f[':answer-field/type']=f[':answer-field/type'][':db/ident']
    for c in f[':answer-field/choices']:c[':answer/type']=c[':answer/type'][':db/ident'];c[':answer/value']=g.fmt.normalize_tex(c[':answer/value'])
    f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  ff=p.integral_operands(q[':question/problem'])[0];n,a,b=t['parameters']
  z={'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'question':q,'generation':{'template':'frozen-source-stage-verification','origin':'exact_frozen_source_with_separate_fieldless_validation_fixture' if sid=='q-49515' else 'exact_frozen_source','source_id':sid,'mathematical_fingerprint':g.digest(str(s.cancel(ff))),'domain':{'excluded_poles':[str(-s.Rational(b,a))]}}}
  result=check(z,sid=='q-113533');sourceverification.append({'source_id':sid,'counts':result,'fieldless_fixture':sid=='q-49515','ambiguous_bank_explicitly_qualified':sid=='q-113533'})
  if g.source_case(sid)['public_replay_eligible']:
   field=q[':question/answer-fields'][0];key=field[':answer-field/correct'][1];checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==key else 'rejected','purpose':'exact eligible frozen source ID selection'} for c in field[':answer-field/choices']];native.append({'label':'source '+sid,'record':z,'checks':checks})
 save('source-stage-verification.json',sourceverification)
 # Exercise declared parameter endpoints and signs with full rendered-stage verification.
 boundaries=[]
 for difficulty in g.LEVELS:
  for sid in g.profiles(difficulty):
   n0,a0,b0=([7,7 if sid.endswith('positive') else -7,1] if difficulty=='hard' else g.ANCHORS[sid.split(':')[-1]]['parameters']);ns=([7,15] if difficulty=='hard' else [1] if n0==1 else [2,6]);av=([7,15] if difficulty=='hard' else [1] if a0==-1 else [2,6]);bs=([-15,15] if difficulty=='hard' else [-9,9]);sign=1 if a0>0 else -1
   for nn,aa,bb in itertools.product(ns,av,bs):
    par=[nn,aa*sign,bb]
    if g.eligible(sid,par,difficulty) and g.valid_bank(sid,par):
     z=g.generate(difficulty,0,sid,par);result=check(z);boundaries.append({'difficulty':difficulty,'profile':sid,'parameters':par,**result})
 save('boundary-cases.json',boundaries)
 # Broader independent task and slot diversity; each instance has independent rendered math checks.
 diversity={}
 for level in g.LEVELS:
  rows=g.batch(level,75,1700);assert rows==g.batch(level,75,1700);assert len({z['generation']['mathematical_fingerprint'] for z in rows})==75
  for z in rows:check(z)
  diversity[level]={'distinct_tasks':75,'slot_values':{k:sorted({z['generation']['parameters'][i] for z in rows}) for i,k in enumerate(['n','a','b'])},'profiles':sorted({z['generation']['profile'] for z in rows})};save('preview-'+level+'.json',rows[:3]);(HERE/('preview-'+level+'.md')).write_text('\n\n---\n\n'.join(g.markdown(z) for z in rows[:3]))
 strict=[]
 for name,fn in [('bool seed',lambda:g.generate(seed=True)),('float seed',lambda:g.generate(seed=1.0)),('bool count',lambda:g.batch('easy',True)),('float count',lambda:g.batch('easy',1.0)),('zero count',lambda:g.batch('easy',0)),('bool parameter',lambda:g.generate('easy',template='q-113532',parameters=[True,2,3])),('float parameter',lambda:g.generate('easy',template='q-113532',parameters=[1,2.0,3])),('zero slope',lambda:g.generate('easy',template='q-113532',parameters=[1,0,3])),('wrong difficulty',lambda:g.generate('hard',template='q-113532')),('colliding full bank',lambda:g.generate('easy',template='q-113532',parameters=[1,2,2]))]:
  try:fn()
  except ValueError:strict.append(name)
  else:raise AssertionError('accepted '+name)
 mutations=[];sample=g.generate('moderate',7,'q-113537',[4,5,3]);text=sample['question'][':question/worked-solution']
 changes={'stale_prose_constant':text.replace(r'C=\frac{4}{5}',r'C=\frac{1}{5}',1),'stale_expanded_constant':text.replace(r'+\frac{4}{5}\operatorname{ln}⁡K',r'+\frac{1}{5}\operatorname{ln}⁡K',1),'wrong_differential':text.replace(r'=\frac{1}{5}\text{d}u',r'=\frac{1}{4}\text{d}u',1),'wrong_integrand_stage':text.replace(r'4\int \frac{1}{5x+3}',r'3\int \frac{1}{5x+3}',1),'wrong_intermediate_primitive':text.replace(r'\frac{4}{5}\operatorname{ln}⁡|u|',r'\frac{3}{5}\operatorname{ln}⁡|u|',1)}
 for name,value in changes.items():
  assert value!=text,name;z=copy.deepcopy(sample);z['question'][':question/worked-solution']=value
  try:check(z)
  except (AssertionError,ValueError):mutations.append({'name':name,'rejected':True})
  else:raise AssertionError('mutation survived '+name)
 # Exact same-K inequality and family equivalence are distinguished.
 A=p.scalar(r'\frac{1}{3}\ln(K|3x+4|)');B=p.scalar(r'\frac{1}{3}\ln(\frac{|3x+4|}{K})');assert not eq(A,B);assert eq(A,B.subs(p.K,1/p.K));assert s.cancel(p.derivative(A)-p.derivative(B))==0
 save('independent-inventory.json',{'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'questions':[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Existing nonMA inventory, not counted as observed MA practice templates.'} for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]})
 save('source-cases.json',sourcecases);save('raw-replay.json',rawcases+[g.source_case('e-450')]);save('source-replay.json',replay);save('recipe-ledger.json',ledger);save('review-cases.json',reviewcases);save('native-input.json',native);save('strict-inputs.json',strict)
 engine=ROOT/'generate/runs/current/check-engine';sha=hashlib.sha256(engine.read_bytes()).hexdigest();assert sha=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea';subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 cli=json.loads(subprocess.check_output([sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--count','2','--seed','-7']));assert len(cli)==6
 base=json.load(open(HERE/'numeric-baseline.json'));root=ROOT/'generate/scratch/17592186064207';now={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() if x.is_file() else 'directory' for x in [root,*sorted(root.rglob('*')),root.with_suffix('.py')]};assert base==now
 save('numeric-integrity.json',{'unchanged':True,'path_count':len(base),'file_count':sum(v!='directory' for v in base.values())})
 (HERE/'review.md').write_text('\n\n'.join(reviews)+'\n')
 report={'passed':True,'basis':2275,'source_records':14,'MA_originals':10,'independent_inventory_records':4,'MA_original_choices_matched':45,'MA_original_banks':9,'independent_choices_matched':20,'independent_banks':4,'raw_replay_eligible_MA':6,'normal_profiles':12,'profile_cases_checked':len(stats),'actual_source_solution_checks':len(sourceverification),'boundary_checks':len(boundaries),'additional_distinct_tasks':diversity,'cases':stats,'mutations':mutations,'constant_equivalence':{'same_K_functions_unequal':True,'positive_K_reciprocal_family_equivalent':True,'source_q113533_excluded_and_separate_repair':True},'native_engine_sha256':sha,'numeric_tree_unchanged':True,'limitations':['No observed hard source: authored larger-coefficient workload preserves identical method.','q49513/q49516 missing key/solution/difficulty; q49515 missing fields: exact ineligible raw replay and separate authored completions.','q113533 contains equivalent distractor; exact ineligible raw replay and separate derivative-wrong replacement.','No blank source fields exist; no invented blank learner contract.','65 observed source choices fully replayed, including independent inventory; no DB or engine mutations.'],'duration_seconds':time.time()-started};save('validation.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ('cases','additional_distinct_tasks')},indent=2))
if __name__=='__main__':main()
