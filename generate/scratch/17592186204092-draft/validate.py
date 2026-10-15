#!/usr/bin/env python3
"""Standalone draft audit: whole raw fidelity, exhaustive domain, mutations, actual native grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];SCRIPT=HERE.with_suffix('.py');ENGINE=ROOT/'generate/runs/current/check-engine'
spec=importlib.util.spec_from_file_location('draft04092',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2,default=str)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def independent(rec):
 g.fmt.validate_generated_record(rec);g.parser.validate_record(rec)
 q=rec['question'];p=g.parser.prompt_parameters(q[':question/problem']);x=sp.Symbol(p['variable']);k=sp.Symbol(p['parameter'])
 display=re.search(r'\$\$\s*(.*?)\s*\$\$',q[':question/problem'],re.S)[1];l,r=map(g.parser.expr,display.split('='));delta=sp.expand(l-r);coefficient=delta.coeff(x);roots=sp.solve(coefficient,k)
 assert len(roots)==1 and delta.subs(k,roots[0])!=0 and not delta.subs(k,roots[0]).has(x)
 assert sp.solveset(sp.Eq(l.subs(k,roots[0]),r),x,domain=sp.S.Reals)==sp.S.EmptySet
 f=q[':question/answer-fields'][0];correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert g.parser.expr(correct[':answer/value'])==roots[0]
 for a in f[':answer-field/choices'][1:]:assert g.parser.expr(a[':answer/value']) not in roots
 assert rec['generation']['parameters']==p
 return p

def checks(rec):
 f=rec['question'][':question/answer-fields'][0];a=f[':answer-field/choices'];root=g.parser.expr(a[0][':answer/value'])
 if f[':answer-field/type'].endswith('/radio'):return [{'field_index':0,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if i==0 else 'rejected','purpose':'Every field-owned option via actual grade_field'} for i,v in enumerate(a)]
 entries=[a[0][':answer/value'],str(root),str(root)+'+0',r'\frac{'+str(root.p*2)+'}{'+str(root.q*2)+'}','0','1',str(root+1)]
 return [{'field_index':0,'submitted':v,'expected':'accepted' if g.parser.expr(v)==root else 'rejected','purpose':'Canonical/equivalent and ordinary0/1/+1 via actual grade_field'} for v in entries]
def expect_fail(call):
 try:call()
 except (ValueError,TypeError,KeyError,AssertionError):return
 raise AssertionError('invalid public request accepted')
def main():
 base=json.loads((HERE/'baseline.json').read_text());assert sha(ENGINE)==base['root_engine_sha256']=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 current=[SCRIPT.with_name('17592186204092.py')]+[p for p in (HERE.with_name('17592186204092')).rglob('*') if p.is_file()]
 assert set(str(p.relative_to(ROOT)) for p in current)==set(base['paths']) and all(sha(Path(p))==h for p,h in base['paths'].items())
 source=g.SOURCE;assert source['basis']==2275;cases=[];replays=[];served=[];fidelity=[]
 for q in source['record'][':knowledge-point/questions']:
  mid=q.get(':question/math-academy-id')
  if mid is None:continue
  p=g.parser.prompt_parameters(q[':question/problem']);raw=g.observed_raw(mid,p);assert raw['question']==q and raw['generation']['evidence_only'] is True and raw['generation']['eligible'] is False
  cases.append({'source_id':mid,'parameters':p,'record':raw,'role':'observed MA source practice','eligible':':question/difficulty' in q})
  replays.append(raw);row={'source_id':mid,'whole_original_equal':True,'full_prompt':True,'full_solution':':question/worked-solution' in q,'all_fields_banks_correct_feedback_source_attrs':True,'original_parameters':p}
  if ':question/difficulty' in q:
   level=q[':question/difficulty'][':db/ident'].split('/')[-1];r=g.generate(level,parameters=p,template=raw['generation']['template']);independent(r);served.append(r)
   old=q[':question/answer-fields'][0];new=r['question'][':question/answer-fields'][0]
   assert old[':answer-field/type'][':db/ident']==new[':answer-field/type'];assert old[':answer-field/key']==new[':answer-field/key'];assert len(old[':answer-field/choices'])==len(new[':answer-field/choices'])
   ov=[g.parser.expr(a[':answer/value']) for a in old[':answer-field/choices']];nv=[g.parser.expr(a[':answer/value']) for a in new[':answer-field/choices']];assert set(ov)==set(nv)
   assert g.parser.expr(old[':answer-field/correct'][':answer/value'])==nv[0]
   assert g.fmt.normalize_prose(q[':question/problem'])==r['question'][':question/problem']
   assert g.fmt.normalize_prose(g.re_underbraces(q[':question/worked-solution']))==r['question'][':question/worked-solution']
   row.update(matched_values=len(ov),complete_bank_matched=True,normalized_served_prompt_solution_equal=True)
  fidelity.append(row)
 save('source-cases.json',cases);save('raw-replay.json',replays);save('raw-fidelity.json',fidelity);save('served-original-replays.json',served)
 independent_inventory=json.loads((HERE/'independent-inventory.json').read_text());assert len(independent_inventory['questions'])==5;assert all(':question/math-academy-id' not in v['record'] and v['relationship_to_source_templates'] for v in independent_inventory['questions'])
 records=[];capacity={};coverage={}
 for level in g.SUPPORTED_LEVELS:
  domain=list(g.CATALOG[level]);assert len(domain)==80 and len({g.fingerprint(p) for p in domain})==80
  originals=[c['parameters'] for c in cases if c['eligible'] and c['record']['question'][':question/difficulty'][':db/ident']==':question.difficulty/'+level]
  all_parameters=domain+[p for p in originals if p not in domain]
  capacity[level]={'finite_distinct_target_ratio_capacity':80,'catalog_cases':len(domain),'field':'radio' if level=='easy' else 'blank','evidence':'observed method with authored parameters' if level!='hard' else 'no observed hard; conservative same-method authored calibration'}
  templates=['right-constant'] if level=='easy' else ['both-constants','both-constants-ax-layout']
  for template in templates:
   for p in all_parameters:
    rec=g.generate(level,seed=173,parameters=p,template=template);independent(rec);records.append(rec)
  batch=g.batch(level,80,173);assert len({v['generation']['parameter_fingerprint'] for v in batch})==80 and batch==g.batch(level,80,173)
  assert g.generate(level,173)==g.generate(level,173)
  coverage[level]={'templates':templates,'profiles':['observed-ratio-bank' if level=='easy' else 'blank-rational'],'all_catalog_parameters_checked':80,'every_template_catalog_pair_checked':80*len(templates),'all_accepted_original_parameters_checked':len(originals),'every_public_parameter_template_pair_checked':len(all_parameters)*len(templates),'coefficient_values':{slot:sorted({p[slot] for p in domain}) for slot in 'abcd'},'target_role':'constant parameter making variable coefficient zero; fixed by instructional purpose'}
 save('capacity.json',capacity)
 # Mathematical data held fixed while changing cosmetic variable/parameter names at observed parameters.
 orig=served[1];p=orig['generation']['parameters'];other=next(r for r in served if r['generation']['parameters']['variable']!=p['variable']);save('target-role-review.json',{'fixed_target_role':'the parameter, never the equation variable; changing role changes the question','cosmetic_names':'source replay preserves all observed names; authored catalog fixes x,p to avoid claiming cosmetic diversity','same_givens_different_role':'ineligible by mathematical purpose'})
 # Independent mutation controls against actual displayed data, whole banks, keys and every intermediate.
 mutations=[]
 ref=served[0]
 for name,mut in [
 ('prompt coefficient',lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('3py=5y+8','3py=6y+8'))),
 ('parameter metadata',lambda r:r['generation']['parameters'].__setitem__('a',9)),
 ('correct key',lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/correct',[':answer/id',r['question'][':question/answer-fields'][0][':answer-field/choices'][1][':answer/id']])),
 ('distractor whole bank',lambda r:r['question'][':question/answer-fields'][0][':answer-field/choices'][1].__setitem__(':answer/value','999')),
 ('field type',lambda r:r['question'][':question/answer-fields'][0].__setitem__(':answer-field/type',':answer-field.type/blank')),
 ('intermediate solution',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('5y+8-5y','5y+9-5y'))),
 ('target reference',lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('factor $y$','factor $z$'))),
 ('answer type',lambda r:r['question'][':question/answer-fields'][0][':answer-field/choices'][0].__setitem__(':answer/type',':answer.type/text'))]:
  bad=copy.deepcopy(ref);mut(bad);assert bad!=ref;expect_fail(lambda:independent(bad));mutations.append(name)
 invalid=[lambda:g.generate('unknown'),lambda:g.generate('easy',True),lambda:g.generate('easy',template=''),lambda:g.generate('hard',profile='observed-ratio-bank'),lambda:g.generate('easy',parameters={}),lambda:g.generate('easy',parameters=dict(g.CATALOG['easy'][0],a=True)),lambda:g.generate('easy',parameters=dict(g.CATALOG['easy'][0],a=0)),lambda:g.batch('easy',81),lambda:g.batch('easy',-1),lambda:g.batch('easy',True),lambda:g.batch('hard',1,1.5),lambda:g.observed_raw('nope'),lambda:g.observed_raw('q-288662',dict(g.CATALOG['easy'][0]))]
 for call in invalid:expect_fail(call)
 engine_input=[{'label':str(i),'record':rec,'checks':checks(rec)} for i,rec in enumerate(records)];save('engine-input.json',engine_input)
 run=subprocess.run([str(ENGINE),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True);(HERE/'engine.log').write_text(run.stdout+run.stderr);assert run.returncode==0,run.stderr
 engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 # Diagnostic malformed/foreign responses are isolated from serving checks.
 diagnostics=[]
 for submitted in ['999999','not-an-answer']:
  item={'label':'foreign-'+submitted,'record':ref,'checks':[{'field_index':0,'submitted':submitted,'expected':'unresolved','purpose':'isolated foreign malformed diagnostic'}]}
  save('diagnostic-input.json',[item]);res=subprocess.run([str(ENGINE),str(HERE/'diagnostic-input.json'),str(HERE/'diagnostic-report.json')],capture_output=True,text=True)
  diagnostics.append({'submitted':submitted,'expected_diagnostic':'unresolved','exit_code':res.returncode,'output':res.stdout+res.stderr})
 save('foreign-malformed-diagnostics.json',diagnostics)
 reviews={'observed_raw':replays,'served_originals':served,'variants':{level:[g.generate(level,seed=i) for i in (11,44)] for level in g.SUPPORTED_LEVELS}}
 save('review.json',reviews);(HERE/'review.md').write_text('\n\n---\n\n'.join(['## Original '+v['generation']['source_id']+'\n\n'+v['question'][':question/problem']+'\n\n'+v['question'].get(':question/worked-solution','Incomplete source: no captured solution') for v in replays]+['## '+level+' authored variant\n\n'+g.markdown(v) for level,rows in reviews['variants'].items() for v in rows])+'\n')
 cli=[]
 for level in g.SUPPORTED_LEVELS+('all',):
  for format in ['json','markdown']:
   out=HERE/('cli-'+level+'.'+('json' if format=='json' else 'md'));res=subprocess.run([sys.executable,str(SCRIPT),'--difficulty',level,'--count','2','--seed','91','--format',format,'--output',str(out)],capture_output=True,text=True);assert res.returncode==0,res.stderr
   if format=='json':
    parsed=json.loads(out.read_text());assert len(parsed)==(6 if level=='all' else 2)
    if level=='all':assert all(sum(row['question'][':question/difficulty']==':question.difficulty/'+l for row in parsed)==2 for l in g.SUPPORTED_LEVELS)
    for row in parsed:independent(row)
   else:
    content=out.read_text();assert content.count('Worked solution')==(6 if level=='all' else 2) and '\n\n---\n\n' in content and content.count('\n\nWorked solution\n\n')==(6 if level=='all' else 2)
   cli.append(str(out.name))
 validation={'status':'pass','basis':2275,'lineage':source['lineage'],'database_writes':0,'registered_baseline_preserved':True,'baseline_file_count':len(base['paths']),'MA_practice_records':len(cases),'eligible_complete_MA':len(served),'ineligible_preserved_raw':len(cases)-len(served),'independent_captured_inventory':5,'source_complete_banks_matched':len(served),'source_values_matched':sum(v.get('matched_values',0) for v in fidelity),'all_public_domain_records':len(records),'coverage':coverage,'mutation_controls':mutations,'invalid_public_requests_rejected':len(invalid),'CLI':cli,'all_CLI_count_contract':'exact count per level','native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'limitations':['No observed hard practice; hard authored calibration conservative and unverified.','Easy bank interpretation unresolved: complete source profile retained, recipes explicitly inferred numerical patterns.','Two incomplete MA questions preserved raw, excluded from served generation.'],'private_runtime_dependencies':['source.json','catalog.json','display_parser.py','math_format.py']}
 save('validation.json',validation)
 freeze={str(p.relative_to(ROOT)):sha(p) for p in [SCRIPT,HERE/'source.json',HERE/'catalog.json',HERE/'display_parser.py',HERE/'math_format.py',HERE/'validate.py',ENGINE]};save('freeze-manifest.json',{'generator_version':g.VERSION,'basis':2275,'artifacts':freeze,'registered_baseline_verified':True,'parent_QA':'pending','status':'local validation pass; not registered'})
 print(json.dumps(validation,indent=2))
if __name__=='__main__':main()
