"""Frozen draft QA: source fidelity, rendered calculus stages, banks, native grading."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,subprocess,re
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from parser import latex,integrand,displayed_stages,equivalent_derivatives,X,U,C,clean
spec=importlib.util.spec_from_file_location('arcsec_draft',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def dump(name,obj): (H/name).write_text(json.dumps(obj,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def normalized(q):
 q=copy.deepcopy(q)
 q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
 return q

def record(q):return {'knowledge_point':{'id':g.KP_UUID,'title':g.SOURCE['record'][':knowledge-point/title']},'question':normalized(q),'generation':{'template':'MA-original','source_basis':g.SOURCE['basis']}}

def check_question(q):
 fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 choices=f[':answer-field/choices'];assert len(choices)==5
 assert len({a[':answer/id'] for a in choices})==5
 assert all(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'] for a in choices)
 target=integrand(q);expressions=[latex(a[':answer/value']) for a in choices]
 derivs=[sp.diff(z,X) for z in expressions]
 hits=[i for i,d in enumerate(derivs) if equivalent_derivatives(d,target)]
 assert len(hits)==1 and choices[hits[0]][':answer/id']==f[':answer-field/correct'][1],('incorrect key',hits)
 # Constant shifts count as the same antiderivative, including on either component.
 for i,d in enumerate(derivs):
  for e in derivs[:i]:assert not equivalent_derivatives(d,e),'equivalent antiderivative options'
 stages=displayed_stages(q)
 assert equivalent_derivatives(sp.diff(expressions[hits[0]]+37,X),target)
 assert equivalent_derivatives(sp.diff(expressions[hits[0]]-11,X),target)
 return stages

def check(r):
 g.fmt.validate_generated_record(r);stages=check_question(r['question']);m=r['generation'];p=m['profile'];slots=m['parameters']
 assert r==g.generate(r['question'][':question/difficulty'].split('/')[-1],m['seed'],profile=p,parameters=slots)
 n=sp.sympify(m['derived']['slope']);c=sp.sympify(m['derived']['normalized_amplitude'])
 assert sp.sympify(stages['slope'])==n
 expected=c/(sp.Abs(X)*sp.sqrt(n*n*X*X-1))
 assert equivalent_derivatives(integrand(r['question']),expected)
 assert m['mathematical_key']==g.mathematical_key(n,c)
 assert 'Each connected component' in m['domain'] and '|slope*x|>1' in m['domain']
 return stages

def engine_item(label,r):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'All five radio answer identities through application learner grader'} for a in f[':answer-field/choices']]}

def fail_mutation(r,name,change):
 bad=copy.deepcopy(r);change(bad['question'])
 try:check_question(bad['question'])
 except Exception:return {'mutation':name,'caught':True}
 raise AssertionError('Mutation escaped '+name)

def prose_signature(s):
 s=re.sub(r'\$\$[\s\S]*?\$\$','<display>',s)
 return re.sub(r'\$[^$]*\$','<inline>',s)
def stage_signature(term):
 if r'\int' in term:
  return 'integral-'+re.findall(r'\\(?:text|textrm)\{d\}([ux])',term)[0]
 return 'primitive-u' if latex(clean(term)).has(U) else 'primitive-x'

def main():
 baseline=json.loads((H/'registered-baseline.json').read_text());registered=H.parent/'17592186064250'
 current={str(p.resolve()):sha(p) for p in [registered.with_suffix('.py'),*registered.rglob('*')] if p.is_file()};assert current==baseline
 source=[];rows=[];ledger=[];profiles=[];terms=0;changed=[]
 N,A,D=sp.symbols('n A D',positive=True)
 for p,v in g.PROFILES.items():
  print('Checking',p,flush=True);original=g.ORIGINALS[p];old=record(original);oldstage=check_question(old['question'])
  slots=g.source_parameters(p);r=g.generate(v[0],0,profile=p,parameters=slots);newstage=check(r)
  assert equivalent_derivatives(integrand(old['question']),integrand(r['question']))
  assert prose_signature(original[':question/problem'])==prose_signature(r['question'][':question/problem'].removesuffix('\n\n{{selection}}'))
  assert prose_signature(original[':question/worked-solution'])==prose_signature(r['question'][':question/worked-solution'])
  assert [stage_signature(t) for t in oldstage['terms']]==[stage_signature(t) for t in newstage['terms']]
  assert len(oldstage['terms'])==len(newstage['terms'])
  oldf=old['question'][':question/answer-fields'][0];newf=r['question'][':question/answer-fields'][0]
  oldvals=[latex(a[':answer/value']) for a in oldf[':answer-field/choices']];newvals=[latex(a[':answer/value']) for a in newf[':answer-field/choices']]
  matches=[[j for j,z in enumerate(newvals) if sp.simplify(w-z)==0] for w in oldvals]
  assert all(len(z)==1 for z in matches) and len({z[0] for z in matches})==5
  symbolic=g.recipe_values(p,N,A,D);choices=[]
  for i,a in enumerate(oldf[':answer-field/choices']):
   j=matches[i][0];oc=a[':answer/id']==oldf[':answer-field/correct'][1];nc=newf[':answer-field/choices'][j][':answer/id']==newf[':answer-field/correct'][1];assert oc==nc
   choices.append({'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'correct':oc,'parameterized_recipe':{'amplitude':str(symbolic[j][0]),'function':symbolic[j][1],'argument_slope':str(symbolic[j][2])},'original_recipe_value':r['generation']['answer_recipes'][j],'generated_value':newf[':answer-field/choices'][j][':answer/value'],'one_to_one_match':j})
  ledger.append({'source_id':original[':db/id'],'MA_id':p,'difficulty':v[0],'template':v[1],'profile':p,'original_parameters':slots,'prompt':original[':question/problem'],'worked_solution':original[':question/worked-solution'],'choices':choices,'original_rendered_stages':oldstage,'normalized_replay_stages':newstage})
  source.append(engine_item(p,old));eligible=[];rejected=[];local=[]
  for instance in g.all_parameters(p):
   if g.eligible(p,instance):
    row=g.generate(v[0],371,profile=p,parameters=instance);st=check(row);terms+=st['operative_terms_checked'];rows.append(row);local.append(row);eligible.append(instance)
   else:rejected.append(instance)
  # Change each role independently, keeping every other role fixed.
  slotcoverage={}
  for role in slots:
   slotcoverage[role]=sorted({x[role] for x in eligible})
   assert len(slotcoverage[role])>1
   pair=None
   for a in local:
    for b in reversed(local):
     x=a['generation']['parameters'];y=b['generation']['parameters']
     if x[role]!=y[role] and all(x[k]==y[k] for k in x if k!=role):pair=(a,b);break
    if pair:break
   assert pair,(p,role)
   a,b=pair;assert a['question'][':question/problem']!=b['question'][':question/problem']
   check(a);check(b);changed.append({'profile':p,'changed_role':role,'held_fixed':{k:z for k,z in a['generation']['parameters'].items() if k!=role},'before':a['generation']['parameters'],'after':b['generation']['parameters']})
  profiles.append({'profile':p,'difficulty':v[0],'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'complete_banks_matched':1,'eligible_instances':len(eligible),'rejected_instances':rejected,'slot_coverage':slotcoverage,'source_replay_math_stages':len(newstage['terms']),'presentation':'Shared prose unchanged; equivalent fraction placement, simplified radicals and one aligned environment canonicalized.'})
 for slots in g.all_parameters('authored-e-direct'):
  r=g.generate('easy',371,parameters=slots);st=check(r);terms+=st['operative_terms_checked'];rows.append(r)
 easy_rows=[r for r in rows if r['generation']['profile']=='authored-e-direct']
 for role in ['slope_numerator','slope_denominator']:
  pair=next((a,b) for a in easy_rows for b in reversed(easy_rows) if a['generation']['parameters'][role]!=b['generation']['parameters'][role] and all(a['generation']['parameters'][k]==b['generation']['parameters'][k] for k in a['generation']['parameters'] if k!=role))
  for z in pair:check(z)
  changed.append({'profile':'authored-e-direct','changed_role':role,'before':pair[0]['generation']['parameters'],'after':pair[1]['generation']['parameters']})
 # Hand-read requested role separation case: numerator fixed while inner slope changes.
 q69477=[g.generate('moderate',0,profile='q-69477',parameters={'numerator':3,'slope':n}) for n in [7,9,11]]
 for r in q69477:check(r)
 dump('independent-role-review.json',q69477)
 mutations=[];r=g.generate('moderate',0,profile='q-69476',parameters={'slope':8,'numerator':8})
 def replace(q,a,b):q[':question/worked-solution']=q[':question/worked-solution'].replace(a,b,1)
 mutations.append(fail_mutation(r,'stale substitution slope',lambda q:replace(q,'$u=8x.','$u=7x.')))
 mutations.append(fail_mutation(r,'wrong du/dx',lambda q:replace(q,r'\text{d}x}=8',r'\text{d}x}=7')))
 mutations.append(fail_mutation(r,'wrong formal inverse-secant input',lambda q:replace(q,r'\text{arcsec}(u)+C',r'\text{arcsec}(2u)+C')))
 mutations.append(fail_mutation(r,'lost absolute value',lambda q:q.update({':question/problem':q[':question/problem'].replace('|8x|','8x')})))
 mutations.append(fail_mutation(r,'wrong intermediate prefactor',lambda q:replace(q,r'=8\,\int',r'=7\,\int')))
 mutations.append(fail_mutation(r,'wrong answer key',lambda q:q[':question/answer-fields'][0].update({':answer-field/correct':[':answer/id',q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']]})))
 for fun,args in [(g.batch,('easy',True,1)),(g.batch,('all',1,True)),(g.batch,('easy',0,1)),(g.batch,('easy',-1,1)),(g.batch,('easy',1.0,1)),(g.generate,('easy',True)),(g.generate,('moderate',1.5))]:
  try:fun(*args)
  except ValueError:continue
  raise AssertionError('invalid API accepted')
 for count in ['0','-1','1.5']:
  z=subprocess.run([sys.executable,str(H.with_suffix('.py')),'--difficulty','all','--seed','1','--count',count,'--format','json'],capture_output=True);assert z.returncode!=0
 for form in ['json','markdown']:
  command=[sys.executable,str(H.with_suffix('.py')),'--difficulty','all','--seed','2718','--count','2','--format',form]
  a=subprocess.run(command,check=True,capture_output=True).stdout;b=subprocess.run(command,check=True,capture_output=True).stdout;assert a==b
  if form=='json':assert len(json.loads(a))==6
 for level in ['easy','moderate','hard']:
  b=g.batch(level,10,42);assert len({r['generation']['mathematical_key'] for r in b})==10
 normal={}
 for level in ['moderate','hard']:
  counts={p:0 for p,v in g.PROFILES.items() if v[0]==level}
  for seed in range(250):counts[g.batch(level,1,seed)[0]['generation']['profile']]+=1
  assert all(counts.values());normal[level]=counts
 dump('sampling-validation.json',{'actual_batch_profile_counts':normal,'seeds':list(range(250)),'policy':'Complete profile chosen before independent role sampling; whole bank rejected on collision'})
 dump('source-cases.json',source);dump('review-cases.json',[engine_item(str(i),r) for i,r in enumerate(rows)])
 dump('independent-inventory.json',{'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'questions':[],'counts':{'easy':0,'moderate':0,'hard':0},'reason':'Fresh read contains17 MA practice questions and no nonMA inventory entries.'})
 dump('choice-ledger.json',{'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'questions':ledger});dump('source-replay.json',profiles)
 for name in ['source','review']:subprocess.run([str(H/'check-engine'),str(H/(name+'-cases.json')),str(H/(name+'-engine-report.json'))],check=True)
 bounds={lev:len({r['generation']['mathematical_key'] for r in rows if r['question'][':question/difficulty'].endswith('/'+lev)}) for lev in ['easy','moderate','hard']}
 dump('capability.json',{'source_basis':g.SOURCE['basis'],'supported_levels':['easy','moderate','hard'],'source_counts':{'easy':0,'moderate':5,'hard':12},'finite_distinct_integrands':bounds,'role_bounds':{'numerator':list(g.NUMERATORS),'easy_reduced_positive_ratios':list(g.EASY_RATIONALS),'integer_slope':list(g.SLOPES),'denominator_scale':list(g.NUMERATORS),'nonsquare_radicand':list(g.RADICANDS)},'sampling':'Independent supplied numerator/inner slope; independent denominator scale/inner slope; independent numerator/radicand; complete source profiles with whole-bank rejection. Easy direct matched numerator=slope is essential to supplied du shape.','plots':'none','blank_fields':0})
 dump('validation.json',{'passed':True,'source_basis':g.SOURCE['basis'],'source_inventory':{'MA':17,'nonMA':0,'easy':0,'moderate':5,'hard':12},'source_banks_matched':17,'source_choices_matched':85,'source_distractors_matched':68,'instances_checked':len(rows),'operative_terms_checked':terms,'profiles':profiles,'changed_single_role_cases':changed,'mutations':mutations,'normal_sampling_profile_counts':normal,'registered_artifact':{'unchanged':True,'files':len(baseline)},'grading':'Separate native originals/variants reports; every radio answer identity; no blanks','math_checks':'Rendered integrand, u, du/dx, differential equality, every formal input and primitive; both real components, arbitrary C shifts, correct/wrong and wrong/wrong derivatives','source_fidelity':'Complete prompts/fields/banks/shared prose and operative stage order match at original parameters; canonical math presentation differs explicitly','source_errors':[]})
 md=[]
 for p,v in g.PROFILES.items():
  original=g.ORIGINALS[p];variant=next(r for r in reversed(rows) if r['generation']['profile']==p)
  md.append('## '+p+' — '+v[0]+'\n\n### Original\n\n'+g.markdown(record(original))+'\n\n### Independent-role variant\n\n'+g.markdown(variant))
 md.append('## q-69477: fixed numerator3, independently changed slope\n\n'+'\n\n'.join(map(g.markdown,q69477)))
 md.append('## Authored easy\n\n'+g.markdown(g.generate('easy',0,parameters={'slope_numerator':3,'slope_denominator':1}))+'\n\n'+g.markdown(g.generate('easy',0,parameters={'slope_numerator':2,'slope_denominator':3})))
 (H/'review.md').write_text('\n\n'.join(md));print(json.dumps({'passed':True,'instances':len(rows),'operative_terms':terms,'distinct_integrands':bounds,'mutations':len(mutations)}))
if __name__=='__main__':main()
