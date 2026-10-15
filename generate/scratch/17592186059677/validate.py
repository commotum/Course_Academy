#!/usr/bin/env python3
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
ROOT=Path(__file__).parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from readback import X,parse,derivative_input,blocks,rows,expression_parts,check_original_solution
ENGINE=REPO/'generate/runs/current/check-engine'
assert hashlib.sha256(ENGINE.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'

def equal(a,b):return sp.simplify(a-b)==0

def check(record):
 q=record['question'];m=record['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 if m['profile']=='source_faithful':
  question=copy.deepcopy(q);question[':question/math-academy-id']=m['source_id'];audit=check_original_solution(question)
  supplied=parse(re.search(r'[fg]\(x\)\s*=\s*([^$]+)',prompt)[1]);result=sp.diff(supplied,X,2)
  point=m['original_parameters'].get('t');result=sp.simplify(result.subs(X,point)) if point is not None else result
  field=q[':question/answer-fields'][0];values=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
  assert all(not equal(values[i],values[j]) for i in range(len(values)) for j in range(i));assert sum(equal(v,result) for v in values)==1
  original=g.ORIGINALS[m['source_id']];scale=m['parameters']['scale'];of=original[':question/answer-fields'][0]
  for i,a in enumerate(field[':answer-field/choices']):assert equal(parse(a[':answer/value']),scale*parse(of[':answer-field/choices'][i][':answer/value']))
  assert len(field[':answer-field/choices'])==len(of[':answer-field/choices'])
  assert field[':answer-field/key']==of[':answer-field/key']
  if scale==1:
   assert prompt==g._fmt.normalize_prose(original[':question/problem']);assert sol==g._fmt.normalize_prose(original[':question/worked-solution'])
   assert [a[':answer/value'] for a in field[':answer-field/choices']]==[g._fmt.normalize_tex(a[':answer/value']) for a in of[':answer-field/choices']]
  # Shared prose and ordered math-stage count cannot be replaced by generic stages.
  prose=lambda text:re.sub(r'\$\$.*?\$\$','<math>',text,flags=re.S)
  assert prose(sol)==prose(g._fmt.normalize_prose(original[':question/worked-solution']))
  assert len(blocks(sol))==len(blocks(original[':question/worked-solution']))
  return audit['printed_rows'],result
 kind=q[':question/answer-fields'][0][':answer-field/type'].split('/')[-1]
 name='g' if '$g' in prompt else 'f';known=prompt.startswith('Given')
 inline=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S)
 given=next(v for v in inline if '=' in v and v.split('=')[1].strip())
 supplied=parse(given.split('=',1)[1].rstrip('.'))
 target=next(v for v in inline if r'\prime\prime' in v)
 tm=re.search(r'([fg])\^\{\\prime\\prime\}\((x|[-0-9]+)\)',target);assert tm,('target shape',target)
 assert tm[1]==name;point=None if tm[2]=='x' else int(tm[2]);assert point==m['parameters'].get('t')
 d1=supplied if known else sp.diff(supplied,X);d2=sp.diff(d1,X);result=d2 if point is None else sp.simplify(d2.subs(X,point))
 stage_blocks=blocks(sol);expected_count=(1 if known else 2)+(point is not None);derivative_blocks=stage_blocks[1:] if known else stage_blocks
 if known:
  assert len(stage_blocks)==expected_count+1
  first=expression_parts(stage_blocks[0])[0];assert first[0]==name+r'^{\prime}(x)';assert equal(parse(first[1]),supplied)
 else:assert len(stage_blocks)==expected_count
 number=0
 for order,(block,input_expr,output) in enumerate(zip(derivative_blocks,[d1] if known else [supplied,d1],[d2] if known else [d1,d2]),start=2 if known else 1):
  parts=expression_parts(block);lhs=parts[0][0].strip();expected_label=name+r'^{'+(r'\prime' if order==1 else r'\prime\prime')+'}(x)';assert lhs==expected_label,('derivative order/name',lhs,expected_label)
  operand,op_order=derivative_input(parts[0][1]);assert op_order==1 and equal(operand,input_expr),('formal derivative input',operand,input_expr)
  assert equal(sp.diff(operand,X,op_order),output);number+=1
  for _,rhs in parts[1:]:
   if r'\prime' in rhs:
    operand,op_order=derivative_input(rhs);assert op_order==1 and equal(operand,input_expr);assert equal(sp.diff(operand,X),output)
   else:assert equal(parse(rhs),output),('incorrect printed intermediate',rhs,output)
   number+=1
 if point is not None:
  assert 'evaluating the second derivative at $x='+str(point)+'$' in sol
  parts=expression_parts(stage_blocks[-1]);assert parts[0][0].strip()==name+r'^{\prime\prime}('+str(point)+')'
  for _,rhs in parts:assert equal(parse(rhs),result),('printed evaluation',rhs,result)
  number+=len(parts)
 field=q[':question/answer-fields'][0];values=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
 assert len(values)==(5 if kind=='radio' else 1)
 assert all(not equal(values[i],values[j]) for i in range(len(values)) for j in range(i))
 assert sum(equal(v,result) for v in values)==1
 correct=field[':answer-field/correct'][1];matches=[a for a in field[':answer-field/choices'] if a[':answer/id']==correct];assert len(matches)==1 and equal(parse(matches[0][':answer/value']),result)
 assert m['evidence_only'] is False and m['eligible_for_learning'] is True
 assert m['domain']==('x>0' if supplied.has(sp.sqrt(X)) or any(t.as_coeff_exponent(X)[1].q!=1 for t in supplied.as_ordered_terms()) else 'all real x')
 g._fmt.validate_generated_record(record)
 return number,result

def native_checks(record,result):
 field=record['question'][':question/answer-fields'][0]
 if field[':answer-field/type'].endswith('/radio'):
  return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'complete owned choice bank'} for a in field[':answer-field/choices']]
 canonical=field[':answer-field/choices'][0][':answer/value']
 equivalent=g.tex(2*result)+'/'+ '2' if result.is_number else g.tex(result)+r'+0x'
 # Parentheses are necessary to divide the complete numeric result.
 equivalent='('+canonical+')+0' if result.is_number else canonical+r'+0x'
 return [{'submitted':s,'expected':expected,'purpose':purpose} for s,expected,purpose in [(canonical,'accepted','canonical displayed answer'),(equivalent,'accepted','equivalent entered expression'),('0','accepted' if equal(result,sp.Integer(0)) else 'rejected','zero probe matched to mathematics'),('1','accepted' if equal(result,sp.Integer(1)) else 'rejected','one probe matched to mathematics'),(g.tex(result+1),'rejected','wrong answer plus one')]]

def main():
 source_cases=[];extraction=[];review=[];source_matched=0;original_options=0;source_worked=0;original_keys=0;source_math={}
 for sid,original in g.ORIGINALS.items():
  raw=g.generate(profile='observed_raw',source_id=sid);assert raw['question']==original;source_matched+=1;review.append(raw)
  source_math[sid]=check_original_solution(original)
  source_cases.append({'source_id':sid,'parameters':copy.deepcopy(g.SOURCE_PARAMETERS[sid]),'record':raw,'role':'MA-only source evidence','relationship_to_source_templates':'Exact full Pull original; omissions, identifiers, all choices, keys, and prose remain unchanged; evidence-only.'})
  original_options+=sum(len(f.get(':answer-field/choices',[])) for f in original.get(':question/answer-fields',[]))
  source_worked+=(':question/worked-solution' in original);original_keys+=sum(':answer-field/correct' in f for f in original.get(':question/answer-fields',[]))
  fields=[]
  for f in original.get(':question/answer-fields',[]):
   values=[a[':answer/value'] for a in f[':answer-field/choices']]
   for i,v in enumerate(values):
    for other in values[:i]:assert not equal(parse(v),parse(other)),(sid,'equivalent original options')
   fields.append({'field_key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'complete_profile':sid+'_complete_observed_bank','correct_ref_present':':answer-field/correct' in f,'choices':[{'value':a[':answer/value'],'id':a[':answer/id'],'recipe':('scale * ('+a[':answer/value']+'); exact whole-value linear-differentiation mask, no guessed error intention' if sid in g._faithful.SOURCES.values() else 'exact observed complete mathematical value; incomplete original remains raw-only'),'feedback':a.get(':answer/feedback'),'feedback_present':':answer/feedback' in a} for a in f[':answer-field/choices']]})
  extraction.append({'source_id':sid,'prompt':original[':question/problem'],'worked_solution':original.get(':question/worked-solution'),'worked_solution_present':':question/worked-solution' in original,'difficulty':original.get(':question/difficulty'),'fields':fields,'role':('raw evidence plus served faithful scalar profile' if sid in g._faithful.SOURCES.values() else 'raw evidence only'),'served_faithful_template':next((t for t,s in g._faithful.SOURCES.items() if s==sid),None),'omissions':[k for k in [':question/answer-fields',':question/difficulty',':question/worked-solution'] if k not in original]})
 native=[];diagnostics=[];counts={};ids=set();fingerprints=set();stages=0;enum_total=0;invalid=0;points={};template_counts={}
 for template,(level,kind,bounds,sources) in g.SPECS.items():
  count=0;points[template]=set();all_params=g.parameters(template)
  for p in all_params:
   try:record=g.generate(level,template=template,parameters=p)
   except ValueError:
    assert p not in g.valid_parameters(template);invalid+=1;continue
   count+=1;number,result=check(record);stages+=number;enum_total+=1
   assert record==g.generate(level,template=template,parameters=p)
   id=record['question'][':question/id'];assert id not in ids;ids.add(id)
   fp=record['generation']['mathematical_fingerprint'];assert fp not in fingerprints;fingerprints.add(fp)
   counts[level]=counts.get(level,0)+1
   if 't' in p:points[template].add(p['t'])
   native.append({'label':template+' '+json.dumps(p,sort_keys=True),'record':record,'checks':native_checks(record,result)})
   if count in [1,len(g.valid_parameters(template))]:review.append(record)
  template_counts[template]=count;assert count==len(g.valid_parameters(template))
  record=g.generate(level,41,template=template);number,result=check(record)
  field=record['question'][':question/answer-fields'][0]
  if kind=='radio':diag=[{'submitted':'999999','expected':'unresolved','purpose':'foreign numeric choice does not belong to field'},{'submitted':'malformed','expected':'unresolved','purpose':'malformed choice diagnostic'}]
  else:diag=[{'submitted':'','expected':'unresolved','purpose':'empty answer diagnostic'},{'submitted':'\\bad{','expected':'unresolved','purpose':'malformed math diagnostic'}]
  diagnostics.append({'label':template+' diagnostics','record':record,'checks':diag})
  # Hold math input constant and mutate only evaluation target; read every operator.
  if 't' in bounds:
   p=dict(g.valid_parameters(template)[0]);other=next(candidate for candidate in g.valid_parameters(template) if candidate['t']!=p['t'] and all(candidate[k]==p[k] for k in p if k!='t'))
   r1=g.generate(level,template=template,parameters=p);r2=g.generate(level,template=template,parameters=other)
   check(r1);check(r2);assert r1['question'][':question/problem']!=r2['question'][':question/problem'];assert r1['question'][':question/worked-solution']!=r2['question'][':question/worked-solution'];review.extend([r1,r2])
   # Negative mutation must be detected even when numeric key remains unchanged.
   bad=copy.deepcopy(r2);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('evaluating the second derivative at $x='+str(other['t'])+'$','evaluating the second derivative at $x='+str(p['t'])+'$')
   try:check(bad)
   except AssertionError:pass
   else:raise AssertionError('stale evaluation target escaped readback')
  bad=copy.deepcopy(record);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(r'\right)^{\prime}',r'\right)^{\prime\prime}',1)
  try:check(bad)
  except ValueError:pass
  else:raise AssertionError('wrong formal operator order escaped readback')
 # Faithful source masks are served profiles, separate from authored extensions.
 faithful_reports=[]
 for template,(level,kind) in g.FAITHFUL_SPECS.items():
  sid=g._faithful.SOURCES[template]
  for scale in g._faithful.SCALES:
   record=g.generate(level,template=template,parameters={'scale':scale});n,result=check(record);stages+=n
   assert record==g.generate(level,template=template,parameters={'scale':scale})
   native.append({'label':template+' scalar'+str(scale),'record':record,'checks':native_checks(record,result)})
   if scale in [1,3]:review.append(record)
  for kwargs in [{'parameters':{'scale':0}},{'parameters':{'scale':7}},{'parameters':{'scale':True}},{'parameters':{'scale':1,'order':3}},{'parameters':{'scale':1},'field_type':'checkbox'}]:
   try:g.generate(level,template=template,**kwargs)
   except ValueError:pass
   else:raise AssertionError('invalid faithful API input accepted')
  by_id=g.generate(level,profile='source_faithful',source_id=sid,parameters={'scale':1});by_name=g.generate(level,template=template,parameters={'scale':1});assert by_id==by_name
  faithful_reports.append({'source_id':sid,'template':template,'original_parameters':{'scale':1},'original_bank_choices':len(g.ORIGINALS[sid][':question/answer-fields'][0][':answer-field/choices']),'matched_complete_banks':1,'all_permitted_scales_checked':list(g._faithful.SCALES),'shared_prose_and_full_ordered_source_solution_matched':True})
 for source_case in source_cases:
  sid=source_case['source_id'];template=next((t for t,s in g._faithful.SOURCES.items() if s==sid),None)
  source_case['served_faithful_anchor']={'level':g.FAITHFUL_SPECS[template][0],'template':template,'profile':'source_faithful','parameters':{'scale':1}} if template else None
 authored_counts=dict(counts)
 counts={level:len(g.inventory_entries(level)) for level in ['easy','moderate','hard']}
 # CLI exact counts, types, basis and fail-closed capacity, including both field types.
 cli=[]
 for level in ['easy','moderate','hard']:
  package=g.inventory(level,seed=39,count=counts[level]);assert len(package['questions'])==counts[level]
  assert len({i['record']['generation']['mathematical_fingerprint'] for i in package['questions']})==counts[level]
  for item in package['questions']:assert item['role']=='independently authored inventory';check(item['record'])
  for fmt in ['json','markdown']:
   run=subprocess.run([sys.executable,str(ROOT.with_suffix('.py')),'--difficulty',level,'--count','7','--format',fmt],capture_output=True,text=True);assert run.returncode==0,run.stderr
   if fmt=='json':assert len(json.loads(run.stdout))==7
   else:assert run.stdout.count('### ')==7
   cli.append({'level':level,'format':fmt,'count':7,'status':'pass'})
  run=subprocess.run([sys.executable,str(ROOT.with_suffix('.py')),'--difficulty',level,'--count',str(counts[level]+1)],capture_output=True,text=True);assert run.returncode!=0 and not run.stdout
 run=subprocess.run([sys.executable,str(ROOT.with_suffix('.py')),'--difficulty','all','--count','1','--format','json'],capture_output=True,text=True);assert run.returncode==0,run.stderr
 assert [r['generation']['level'] for r in json.loads(run.stdout)]==['easy','moderate','hard']
 for template,(level,kind,_,_) in g.SPECS.items():
  assert len(g.inventory(level,count=1,template=template,field_type=kind)['questions'])==1
  for kwargs in [{'field_type':'checkbox'},{'parameters':{**g.valid_parameters(template)[0],'order':3}},{'parameters':{**g.valid_parameters(template)[0],'a':0}}]:
   try:g.generate(level,template=template,**kwargs)
   except ValueError:pass
   else:raise AssertionError('invalid public API input accepted')
 (ROOT/'source-cases.json').write_text(json.dumps({'database':g.SOURCE['database'],'basis':g.SOURCE['basis'],'lineage':g.SOURCE['lineage'],'questions':source_cases},indent=2,ensure_ascii=False)+'\n')
 (ROOT/'extraction.json').write_text(json.dumps(extraction,indent=2,ensure_ascii=False)+'\n')
 (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n');(ROOT/'review.md').write_text('# Source evidence and independent authored review\n\n'+'\n\n'.join(g.markdown(r) for r in review)+'\n')
 for file,data in [('native-input.json',native),('native-diagnostics-input.json',diagnostics)]:
  (ROOT/file).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
  report=file.replace('-input','-report');run=subprocess.run([str(ENGINE),str(ROOT/file),str(ROOT/report)],capture_output=True,text=True);assert run.returncode==0,run.stderr
  print(run.stdout)
 grading=json.loads((ROOT/'native-report.json').read_text());diagnostic=json.loads((ROOT/'native-diagnostics-report.json').read_text())
 assert grading['documented_unresolved_checks']==0
 result={'status':'worker validated; awaiting root QA','basis':2275,'database_writes':0,'source_fidelity':{'exact_records':source_matched,'total_records':13,'complete_banks':sum(bool(q.get(':question/answer-fields')) for q in g.ORIGINALS.values()),'all_original_choices':original_options,'existing_correct_designations':original_keys,'exact_existing_worked_solutions':source_worked,'omissions_and_feedback_presence_preserved':True,'printed_original_math':source_math},'capacity':counts,'authored_extension_capacity':authored_counts,'served_faithful_source_profiles':faithful_reports,'served_fidelity':{'complete_original_profiles_matched':5,'total_supported_complete_original_profiles':5,'supported_original_choices_matched':21,'excluded_incomplete_source_records':8,'raw_retained_source_records':13},'template_capacity':template_counts,'enumerated_bounded_cases':enum_total+len(g.FAITHFUL_SPECS)*len(g._faithful.SCALES),'authored_bounded_cases':enum_total,'faithful_bounded_cases':len(g.FAITHFUL_SPECS)*len(g._faithful.SCALES),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'invalid_whole_bank_collisions':invalid,'displayed_operator_and_intermediate_checks':stages,'evaluation_target_coverage':{k:sorted(v) for k,v in points.items() if v},'native_grading':{k:grading[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'separate_diagnostics':{k:diagnostic[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'cli':cli,'baseline':'No registered generator at frozen inventory; no numeric script existed before imports.','limits':['Five complete originals have served faithful scalar templates preserving source bank/prose/all ordered rows. Eight incomplete originals remain raw-only, with omissions documented. Opaque distractor intentions are not inferred.','q-10907 and q-1852 have no answer fields and remain raw-only; no missing field type is invented.','Four easy blank prompts omit function context. Authoring explicitly supplies the derivative or function supported by their full worked solutions.','Second derivative order stays fixed at two; higher-order derivative variation belongs to KP17592186059679.','Coefficient domains and square evaluation points are finite and conservative; no independent progression within a level.']}
 (ROOT/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
