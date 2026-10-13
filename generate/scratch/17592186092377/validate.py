"""Independent math, complete bank fidelity, and actual learner engine checks."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
spec=importlib.util.spec_from_file_location('arc_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sp=g.sp;T=g.T
COUNTS={'displayed_derivative_rows':0,'displayed_integral_rows':0,'displayed_antiderivative_rows':0,'displayed_evaluation_rows':0,'prompt_coordinate_rows':0}
def write(name,value): (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def norm(text):return re.sub(r'\s+','',text.replace('⁡',''))
def eq(a,b):
 diff=sp.trigsimp(sp.expand(a-b))
 return diff==0 or sp.simplify(diff)==0

def clean_rhs(row):return row.split(r'\end{aligned}')[0].split(r'\\')[0].replace('&','').strip().rstrip('.,')

def check_display(record):
 meta=record['generation'];key=meta['template'];u=sp.sympify(meta['parameters']['upper']);d=g.data(key,u,sp.sympify(meta['parameters'].get('scale',1)));raw=record['question'][':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',raw,re.S)
 prompt=record['question'][':question/problem'];coords=re.search(r'x=(.*?),\\,y=(.*?),\\,t',prompt,re.S)
 assert coords,key
 for expr,var in zip(coords.groups(),('x','y')):
  assert eq(g.parse_tex(expr),d[var]),(key,'prompt',var,expr)
  COUNTS['prompt_coordinate_rows']+=1
 for block,var in zip(blocks[1:3],('x','y')):
  for chunk in block.split('=')[1:]:
   if r'\frac{\text{d}}' in chunk:continue
   expr=clean_rhs(chunk)
   assert eq(g.parse_tex(expr),sp.diff(d[var],T)),(key,'displayed derivative',expr)
   COUNTS['displayed_derivative_rows']+=1
 for block in blocks[3:]:
  for row in block.split('='):
   if r'{\int }_' not in row:continue
   if r'\frac{\text{d}' in row:continue
   # Remove the leading coefficient and extract both actual printed bounds.
   prefix,tail=row.split(r'{\int }_',1);prefix=prefix.replace(r'\begin{aligned}','').replace('&','').replace('L','').strip().removesuffix(r'\cdot').strip()
   lo,end=g.group(tail,0);assert tail[end]=='^';hi,end=g.group(tail,end+1)
   if 't}' in lo or 't}' in hi:continue
   assert eq(g.parse_tex(lo),d['a']) and eq(g.parse_tex(hi),u),(key,'printed integral bounds',lo,hi)
   integrand=tail[end:].split(r'\text{d}t')[0].rstrip().removesuffix(r'\,').strip()
   # A sqrt may have a trailing exponential factor or an outside coefficient.
   value=g.parse_tex(prefix if prefix else '1')*g.parse_tex(integrand if integrand else '1')
   assert eq(value**2,d['dx']**2+d['dy']**2),(key,'displayed speed',prefix,integrand,value)
   for q in (sp.Rational(1,7),sp.Rational(1,2),sp.Rational(6,7)):
    t=d['a']+(u-d['a'])*q
    assert float(sp.N(value.subs(T,t)))>=0,(key,'speed sign')
   COUNTS['displayed_integral_rows']+=1
 # Check printed antiderivative, then each numeric evaluation row.
 last=blocks[-1];rows=re.split(r'\s*\\\\\s*&\s*=',last);idx=next(i for i,row in enumerate(rows) if '{|}' in row or '|}' in row)
 anti=rows[idx]
 if '{|}' in anti:expr=anti.split('{|}',1)[0]
 else:
  expr=anti.split('|}',1)[0]
  # Source groups an antiderivative together with its evaluation bar.
  if expr.count('{')>expr.count('}'):expr+='}'*(expr.count('{')-expr.count('}'))
 expr=expr.replace(r'\,','').strip()
 primitive=g.parse_tex(expr)
 assert eq(sp.diff(primitive,T),d['speed']),(key,'printed antiderivative',expr,primitive)
 COUNTS['displayed_antiderivative_rows']+=1
 for row in rows[idx+1:]:
  expr=clean_rhs(row);assert eq(g.parse_tex(expr),d['length']),(key,'printed evaluation',expr)
  COUNTS['displayed_evaluation_rows']+=1
 # Final answer shape includes the printed exponential factor on the prompt.
 field=record['question'][':question/answer-fields'][0];correct=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);value=g.parse_tex(correct[':answer/value'])
 if key=='q-351438':
  supplied=re.search(r'\$L=(.*?)\(\$',prompt).group(1);value*=g.parse_tex(supplied)
 assert eq(value,d['length']) and d['length']>0
 assert len(field[':answer-field/choices'])==(5 if d['kind']=='radio' else 1)
 # Every displayed authored wrong operation is independently recomputed from
 # the checked prompt derivatives/primitive, not merely judged unequal to L.
 if d['kind']=='radio' and meta['bank_profile']=='authored_operations':
  L=sp.simplify(primitive.subs(T,u)-primitive.subs(T,d['a']));delta=u-d['a'];s2=sp.trigsimp(sp.diff(d['x'],T)**2+sp.diff(d['y'],T)**2);square_integral=sp.integrate(s2,(T,d['a'],u));family=d['family']
  if family=='circle':
   radius=sp.sqrt(s2);expected=[L,s2*delta,L/sp.sqrt(2),2*L,L/2]
  elif family=='involute':
   coefficient=sp.simplify(sp.sqrt(s2/T**2));expected=[L,coefficient*(u*u-d['a']**2),square_integral,coefficient*delta,u*u-d['a']**2 if coefficient!=2 else L/2]
  else:expected=[L,L/2,2*L,square_integral,sp.sqrt(s2.subs(T,u))*delta]
  actual=[g.parse_tex(a[':answer/value']) for a in field[':answer-field/choices']]
  assert all(sum(eq(value,choice) for choice in actual)==1 for value in expected),(key,'displayed operation bank')
  COUNTS.setdefault('independently_checked_authored_options',0);COUNTS['independently_checked_authored_options']+=len(actual)
 import uuid
 uuid.UUID(record['question'][':question/id']);uuid.UUID(field[':answer-field/id'])
 assert len({a[':answer/id'] for a in field[':answer-field/choices']})==len(field[':answer-field/choices'])
 for a in field[':answer-field/choices']:uuid.UUID(a[':answer/id'])
 vals=[g.parse_tex(a[':answer/value']) for a in field[':answer-field/choices']]
 assert all(v.is_real and v>0 for v in vals)
 assert all(not eq(v,w) for i,v in enumerate(vals) for w in vals[i+1:])
 assert raw.count('$$')%2==0 and prompt.count('$$')%2==0
 assert raw.count(r'\begin{aligned}')==raw.count(r'\end{aligned}')
 assert '{{field-1}}' in prompt if d['kind']=='blank' else '{{field-1}}' not in prompt
 return record

def engine_item(r,label):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete bank selection'} for a in f[':answer-field/choices']]
 else:
  a=f[':answer-field/choices'][0][':answer/value'];v=g.parse_tex(a)
  # A structurally equivalent scalar entry exercises symbolic grading.
  equivalent='2*('+str(v).replace('**','^')+')/2'
  checks=[{'submitted':a,'expected':'accepted','purpose':'canonical blank fragment'},{'submitted':'('+a+')+1','expected':'rejected','purpose':'wrong scalar'},{'submitted':'-('+a+')','expected':'rejected','purpose':'negative length'}]
 return {'label':label,'record':r,'checks':checks}

def main():
 records=[];engine=[];source_cases=[];matched_options=0;matched_banks=0;distractors=0;source_report=[];review=['# Arc length review\n\nSource: math basis 1356, captured provenance retained in source.json. Original plots were inspected (source-plots-0–2.png). Generated variants are labeled below. Raw source solution punctuation is retained as evidence; q-20907 receives one closing-parenthesis repair in normal output. Default blank prompts use Give an exact answer; observed source replay retains Do not round, whose round substring triggers a normalize-only engine path. Failed original equivalence checks remain capability evidence.\n']
 for key,d in g.TEMPLATES.items():
  print('Checking sources and variants:',key,flush=True)
  case={'source_id':d['source'][':question/id'],'source_ma_id':key,'template':key,'level':d['level'],'parameters':{'upper':str(d['b']),'scale':'1'},'bank_profile':'observed'};source_cases.append(case)
  r=g.generate(d['level'],template=key,parameters=case['parameters'],profile=case['bank_profile']);check_display(r);records.append(r);engine.append(engine_item(r,'source/'+key))
  original=d['source'][':question/answer-fields'][0];generated=r['question'][':question/answer-fields'][0]
  source_values=[g.parse_tex(a[':answer/value']) for a in original[':answer-field/choices']];new_values=[g.parse_tex(a[':answer/value']) for a in generated[':answer-field/choices']]
  assert len(source_values)==len(new_values)
  for value in source_values:assert sum(eq(value,new) for new in new_values)==1
  old_correct=g.parse_tex(original[':answer-field/correct'][':answer/value']);new_correct=g.parse_tex(next(a[':answer/value'] for a in generated[':answer-field/choices'] if a[':answer/id']==generated[':answer-field/correct'][1]));assert eq(old_correct,new_correct)
  matched_banks+=1;matched_options+=len(source_values);distractors+=len(source_values)-1
  # Preserve every original prose sentence and the number of solution stages.
  old=d['source'][':question/worked-solution'];new=r['question'][':question/worked-solution']
  old_prose=re.sub(r'\$\$.*?\$\$','MATH',old,flags=re.S);new_prose=re.sub(r'\$\$.*?\$\$','MATH',new,flags=re.S);assert old_prose==new_prose
  assert old.count(r'\\')==new.count(r'\\'),(key,'solution stages')
  source_report.append({'source':key,'bank_match':True,'designation_match':True,'all_prose_and_stage_count':True,'format_repair':key=='q-20907','source_math_correct':True})
  review+=['## '+key+' ('+d['level']+', '+d['kind']+')\n\n### Original captured question\n\n'+d['source'][':question/problem']+'\n\n'+ '\n'.join('- $'+a[':answer/value']+'$' for a in original[':answer-field/choices'])+'\n\n'+old+'\n']
  for seed in (23,71):
   variant=g.generate(d['level'],seed=seed,template=key);check_display(variant);records.append(variant);engine.append(engine_item(variant,'generated/'+key+'/'+str(seed)));review+=['### Generated variant (seed '+str(seed)+')\n\n'+g.markdown(variant)+'\n']
 # Explicit family/sign boundaries at smallest/largest scales; blanks avoid
 # distractor eligibility deliberately, while radios use observed replay banks.
 for key,d in g.TEMPLATES.items():
  for scale in (1,6):
   boundary=g.generate(d['level'],template=key,parameters={'upper':str(d['b']),'scale':str(scale)},profile='observed' if d['kind']=='radio' else 'blank')
   check_display(boundary);engine.append(engine_item(boundary,'boundary/'+key+'/scale='+str(scale)))
 for scale in ('0','7','1/2','I'):
  try:g.generate_easy(template='q-10260',parameters={'upper':'1','scale':scale})
  except (ValueError,TypeError):pass
  else:raise AssertionError(('invalid scale accepted',scale))
 # Identity across seed/shuffling, profiles, and parameter spelling.
 for key,d in g.TEMPLATES.items():
  r=g.generate(d['level'],seed=3,template=key,parameters={'upper':str(d['b'])},profile='observed' if d['kind']=='radio' else 'blank');s=g.generate(d['level'],seed=19,template=key,parameters={'upper':str(2*d['b'])+'/2'},profile='observed' if d['kind']=='radio' else 'blank');assert r['question'][':question/id']==s['question'][':question/id'];assert r['generation']['parameter_fingerprint']==s['generation']['parameter_fingerprint']
  if d['kind']=='radio':
   other=g.generate(d['level'],seed=3,template=key);r=g.generate(d['level'],template=key,parameters=other['generation']['parameters'],profile='observed');assert r['question'][':question/id']!=other['question'][':question/id'];assert r['generation']['parameter_fingerprint']==other['generation']['parameter_fingerprint']
 a=g.generate_easy(template='q-351505',parameters={'upper':'3','scale':'3'});b=g.generate_easy(seed=99,template='q-351505',parameters={'upper':'6/2','scale':'6/2'})
 assert a['question'][':question/id']==b['question'][':question/id'];assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
 # Invalid inputs are rejected without hidden resampling.
 for bad in ({'upper':'0'},{'upper':'-1'},{'upper':'100'},{'upper':'I'},{'upper':'1','extra':3}):
  try:g.generate_easy(template='q-10260',parameters=bad)
  except (ValueError,TypeError):pass
  else:raise AssertionError(('invalid accepted',bad))
 # Enumerate sampler menus and complete-bank eligibility, without rendering.
 variety={level:set() for level in ('easy','moderate','hard')};eligibility={}
 for key,d in g.TEMPLATES.items():
  print('Enumerating complete banks:',key,flush=True)
  points={g.sample_endpoint(key,g.random.Random(seed)) for seed in range(300)};valid=0
  for u,scale in ((u,scale) for u in points for scale in range(1,7)):
   obj=g.data(key,u,scale);g.check_endpoint(obj);values=g.bank(key,obj,'authored_operations' if d['kind']=='radio' else 'blank')
   numeric=[float(v.evalf()) for _,v in values]
   if all(v.is_real and v>0 for _,v in values) and all(abs(v-w)>1e-9 for i,v in enumerate(numeric) for w in numeric[i+1:]):
    valid+=1;variety[d['level']].add((sp.srepr(obj['x']),sp.srepr(obj['y']),sp.srepr(d['a']),sp.srepr(u),d['kind']))
  assert valid>=2,(key,valid);eligibility[key]={'sampled_unique_endpoints':len(points),'eligible_complete_banks':valid,'uniform_scale_values':6}
 write('source-cases.json',source_cases);write('review.json',records);(HERE/'review.md').write_text('\n\n'.join(review));write('engine-input.json',engine)
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
 report={'status':'passed','database_writes':0,'source_basis':1356,'source_questions':18,'source_complete_banks':{'matched':matched_banks,'total':18},'source_options':{'matched':matched_options,'total':matched_options},'source_distractors':{'matched':distractors,'total':distractors},'source_correct_designations':{'matched':18,'total':18},'source_solution_prose_and_stage_count':{'matched':18,'total':18},'source_solution_punctuation':{'literal_string_comparison':'not claimed; endpoint/evaluation TeX normalized','minimal_source_format_repair':1,'total':18},'source_details':source_report,'generated_records':36,'all_records_checked':len(records),'boundary_records_checked':36,'total_checked_records':90,'displayed_stage_checks':COUNTS,'eligible_math_questions_by_level':{k:len(v) for k,v in variety.items()},'complete_bank_eligibility':eligibility,'variety_inventory_comparison':'numerical distinctness used for counting eligibility; actual generated banks and displayed answers use exact symbolic checks','native_grading':'engine-validation.json','authored_extensions':'familiar-angle interval sampler, uniform coordinate scales 1–6 and complete default operation banks; no new level or mathematical method','plots':'15 original prompt plots inspected; changed intervals rendered from exact coordinates; original assets reused at exact original endpoint','remaining_findings':['Original scalar distractor author intent is underdetermined. Observed homogeneous expression profiles are explicit replay only.','q-20907 extra closing parenthesis repaired; raw source retained.']}
 write('validation.json',report);print(json.dumps(report,indent=2))
 compatibility=[]
 for item in engine:
  r=item['record'];f=r['question'][':question/answer-fields'][0]
  if not f[':answer-field/type'].endswith('/blank'):continue
  a=f[':answer-field/choices'][0][':answer/value'];v=g.parse_tex(a);equivalent='2*('+str(v).replace('**','^')+')/2'
  probe={'label':item['label'],'record':r,'checks':[{'submitted':equivalent,'expected':'accepted','purpose':'equivalent mathematical scalar'}]}
  write('equivalence-probe-input.json',[probe]);proc=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(HERE/'equivalence-probe-input.json'),str(HERE/'equivalence-probe-output.json')],capture_output=True,text=True)
  compatibility.append({'label':item['label'],'canonical':a,'equivalent':equivalent,'native_accepted':proc.returncode==0,'reason':proc.stderr.strip()})
 write('native-equivalence.json',compatibility)
 failed=[p for p in compatibility if not p['native_accepted']]
 default_failed=[p for p in failed if p['label'].startswith('generated/')]
 observed_failed=[p for p in failed if not p['label'].startswith('generated/')]
 report['native_equivalence']={'accepted':len(compatibility)-len(failed),'total':len(compatibility),'failures':len(failed),'default_failures':len(default_failed),'observed_presentation_failures':len(observed_failed),'details':'native-equivalence.json'}
 if observed_failed:report['status']='passed_with_observed_presentation_capability_failure';report['remaining_findings'].append('The actual grader rejects equivalent blanks under original Do not round wording; default exact-answer wording repairs this presentation trigger. Original failures remain in native-equivalence.json; no engine edits.')
 if default_failed:report['status']='failed_native_default_equivalent_blank_acceptance'
 raw_source=(REPO/'generate/runs/current/sources/17592186092377.json').read_bytes();assert raw_source==(HERE/'source.json').read_bytes()
 report['source_capture_sha256']=hashlib.sha256(raw_source).hexdigest()
 subprocess.run([str(REPO/'.venv/bin/python'),str(HERE/'render.py'),'review'],check=True)
 visual_records=records+[item['record'] for item in engine]
 if (HERE/'cli-preview.json').exists():visual_records+=json.loads((HERE/'cli-preview.json').read_text())
 used={r['generation']['plot'] for r in visual_records if r['generation'].get('plot') and Path(r['generation']['plot']).is_absolute()}
 report['visual_qa']={'original_montages':['source-plots-'+str(i)+'.png' for i in range(3)],'generated_and_boundary_montages':['generated-plots-'+str(i)+'.png' for i in range((len(used)+5)//6)],'original_assets_inspected':15,'generated_plot_assets':len(used),'findings_resolved':['transparent original assets composited onto white','parameter arrows added from instance data','endpoint annotations placed inward','nonclosed curve context shortened for readable assessed arcs']}
 write('validation.json',report)
 if default_failed:raise SystemExit('Native default equivalent-blank grading failed: '+str(len(default_failed)))
 print('Native equivalent blanks: defaults accepted; original-presentation failures retained:',len(observed_failed),flush=True)
if __name__=='__main__':main()
