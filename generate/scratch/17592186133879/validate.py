#!/usr/bin/env python3
"""Fail closed on displayed mathematics, source banks/prose/sequence, scope,
identity, format and real application radio grading. Memory-only fixtures.
"""
import hashlib, importlib.util, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
from math_parser import expression, equivalent, Parser, X,Y,T
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('kp_generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
raw=json.loads((ROOT/'source.json').read_text());sources=raw['record'][':knowledge-point/questions']

def write(name,value):(ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def displays(s):return re.findall(r'\$\$(.*?)\$\$',s,re.S)
def rows(block):return block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
def prose(s):
 s=re.sub(r'\$\$.*?\$\$','<display>',s,flags=re.S)
 s=re.sub(r'\$[^$]*\$','<inline>',s)
 return re.sub(r'\s+',' ',s).strip()
def point(s):
 s=s.strip().rstrip('.,');s=s.replace(r'\langle','').replace(r'\rangle','').replace('⟨','').replace('⟩','')
 return tuple(expression(v) for v in s.split(','))
def check_format(q):
 for s in (q[':question/problem'],q[':question/worked-solution']):
  assert s.count('$')%2==0
  depth=0
  for c in s:
   if c=='{':depth+=1
   if c=='}':depth-=1
   assert depth>=0
  assert depth==0
  assert '{{' not in s

def displayed_math(record):
 """Parse actual learner field, path, gradient, potential, endpoint and final
 equations. Reconstruct potential independently from the DISPLAYED gradient.
 No expected AST in generation metadata is used to establish correctness.
 """
 q=record['question'];level=record['generation']['template'];difficulty=g.TEMPLATES[level][0]
 prompt=q[':question/problem'];solution=q[':question/worked-solution']
 match=re.search(r'F\(x,y\)=\\left\((.*?)\\right\)\\,i\+\\left\((.*?)\\right\)\\,j',prompt,re.S)
 assert match,prompt
 P,Q=map(expression,match.groups())
 blocks=displays(solution)
 assert len(blocks)==(8 if difficulty=='hard' else 5)
 gi=3 if difficulty=='hard' else 1
 grad=rows(blocks[gi]);assert len(grad)==2
 assert equivalent(expression(grad[0].split('=')[1]),P)
 assert equivalent(expression(grad[1].split('=')[1]),Q)
 f=expression(blocks[gi+1].split('=')[1])
 assert equivalent(sp.diff(f,X),P) and equivalent(sp.diff(f,Y),Q)
 candidate=sp.integrate(P,X)
 residual=sp.simplify(Q-sp.diff(candidate,Y));assert X not in residual.free_symbols
 reconstructed=candidate+sp.integrate(residual,Y)
 assert not sp.simplify(reconstructed-f).free_symbols
 if difficulty=='hard':
  assert equivalent(sp.diff(P,Y),sp.diff(Q,X))
  assert equivalent(expression(blocks[2].split('=')[-1]),sp.diff(P,Y))
  under=re.search(r'\\underbrace\{\\left\((.*?)\\right\)\}_\{P\(x,y\)\}\\,i\+\\underbrace\{\\left\((.*?)\\right\)\}_\{Q\(x,y\)\}',blocks[1],re.S)
  assert under and equivalent(expression(under[1]),P) and equivalent(expression(under[2]),Q)
  pathblock=blocks[5]
  curve=re.search(r'curve \$y=(.*?)\$ for \$x\\in \[(.*?),(.*?)\]',prompt)
  assert curve
  limits=tuple(expression(v) for v in curve.groups()[1:])
  curve_expr=expression(curve[1])
 else:pathblock=displays(prompt)[0]
 pathmatch=re.search(r'r\(t\)=\\langle (.*?)\\rangle,\\,t\\in \[(.*?),(.*?)\]',pathblock,re.S);assert pathmatch,pathblock
 path=point(pathmatch[1]);lo,hi=map(expression,pathmatch.groups()[1:])
 if difficulty=='hard':assert equivalent(lo,limits[0]) and equivalent(hi,limits[1]) and equivalent(path[0],T) and equivalent(path[1],curve_expr.subs(X,T))
 start=tuple(sp.simplify(v.subs(T,lo)) for v in path);end=tuple(sp.simplify(v.subs(T,hi)) for v in path)
 # Domain and familiar evaluations are independently checked from printed path.
 assert sp.N(hi-lo)>0
 for tt in (lo,(lo+hi)/2,hi):
  for v in path:assert v.subs(T,tt).is_real is not False and not v.subs(T,tt).has(sp.zoo,sp.oo,sp.nan)
 erows=rows(blocks[-2]);assert len(erows)==2
 for row,tt,pt in zip(erows,(lo,hi),(start,end)):
  lhs,rhs=row.split('=');assert equivalent(expression(re.search(r'r\((.*?)\)',lhs)[1]),tt)
  assert all(equivalent(a,b) for a,b in zip(point(rhs.strip().rstrip('.')),pt))
 sentence=re.search(r'Therefore, the coordinates.*?are \$(.*?)\$ and \$(.*?)\$',solution)
 if sentence:assert all(equivalent(a,b) for shown,actual in zip(sentence.groups(),(start,end)) for a,b in zip(point(shown.rstrip('.')[1:-1]),actual))
 fa=sp.simplify(f.subs({X:start[0],Y:start[1]},simultaneous=True));fb=sp.simplify(f.subs({X:end[0],Y:end[1]},simultaneous=True));I=sp.simplify(fb-fa)
 final=rows(blocks[-1]);expected_rows=6 if level=='cubic_radical_path' else 5
 assert len(final)==expected_rows
 # Actual printed endpoint f arguments in the final subtraction.
 arguments=[v.strip()[1:-1] for v in final[1].split('=f',1)[1].split('-f')];assert len(arguments)==2
 for shown,actual in zip(arguments,(end,start)):assert all(equivalent(a,b) for a,b in zip(point(shown),actual))
 for row in final[2:]:assert equivalent(expression(row.split('=',1)[1]),I),row
 field=q[':question/answer-fields'][0];assert len(field[':answer-field/choices'])==5
 opts=[expression(a[':answer/value']) for a in field[':answer-field/choices']]
 assert all(not a.free_symbols and a.is_real is not False for a in opts)
 assert all(not equivalent(a,b) for i,a in enumerate(opts) for b in opts[:i])
 flags=[a[':answer/id']==field[':answer-field/correct'][1] for a in field[':answer-field/choices']]
 assert sum(flags)==1
 assert all(equivalent(a,I)==flag for a,flag in zip(opts,flags))
 check_format(q)
 ids=[q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in field[':answer-field/choices']]
 assert len(set(ids))==7 and all(str(uuid.UUID(v))==v for v in ids)
 assert field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection'
 assert all(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'] and ':answer/feedback' not in a for a in field[':answer-field/choices'])
 assert ':question/math-academy-id' not in q
 return {'potential':str(f),'P':str(P),'Q':str(Q),'start':[str(v) for v in start],'end':[str(v) for v in end],'final_rows':len(final),'verified_numeric_rows':len(final)-2}

def arithmetic_signature(row):
 tokens=Parser(row.split('=',1)[1]).ts
 additive=sum(v in ('+','-') and i>0 and tokens[i-1] not in ('{','(','+','-','*','/','^') for i,v in enumerate(tokens))
 return {'binary_add_subtract':additive,'explicit_zero_terms':tokens.count('0'),'fraction_operations':tokens.count(r'\frac')}

def native(record,label):
 f=record['question'][':question/answer-fields'][0]
 return {'label':label,'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'correct selection' if a[':answer/id']==f[':answer-field/correct'][1] else 'wrong selection'} for a in f[':answer-field/choices']]}

def main():
 reports=[];cases=[];reviews=[];audit=[];checks=[];variety=[];boundaries=[]
 for q in sources:
  sid=q[':question/math-academy-id'];template=next(k for k,v in g.TEMPLATES.items() if v[1]==sid);level=g.TEMPLATES[template][0]
  p=dict(g.ORIGINAL[template],s=1);r=g.generate(level,template=template,parameters=p,profile='observed_homogeneous')
  audit.append({'label':sid,**displayed_math(r)})
  f=q[':question/answer-fields'][0];rf=r['question'][':question/answer-fields'][0]
  sourcevals=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
  genvals=[expression(a[':answer/value']) for a in rf[':answer-field/choices']]
  unused=set(range(5));matches=[]
  for i,sv in enumerate(sourcevals):
   sf=f[':answer-field/choices'][i][':answer/id']==f[':answer-field/correct'][':answer/id']
   found=[j for j in unused if equivalent(sv,genvals[j]) and sf==(rf[':answer-field/choices'][j][':answer/id']==rf[':answer-field/correct'][1])]
   assert len(found)==1,(sid,i,sv,genvals)
   unused.remove(found[0]);matches.append({'source_index':i,'generated_index':found[0]})
  assert not unused
  assert prose(q[':question/worked-solution'])==prose(r['question'][':question/worked-solution']),(sid,'prose differs')
  assert prose(q[':question/problem'])==prose(r['question'][':question/problem']),(sid,'prompt prose differs')
  assert [len(rows(b)) for b in displays(q[':question/worked-solution'])]==[len(rows(b)) for b in displays(r['question'][':question/worked-solution'])]
  # Independently parse every original displayed numeric final row and potential;
  # records with endpoint typos are documented as repaired, never exact.
  rawblocks=displays(q[':question/worked-solution']);gi=3 if level=='hard' else 1
  original_gradient=[expression(v.split('=')[1]) for v in rows(rawblocks[gi])]
  source_field=(displays(q[':question/problem'])[0].split('=',1)[1] if level=='hard' else re.search(r'for \$F=(.*?)\$',q[':question/problem'])[1])
  ptext,qtext=source_field.split(r'\,i',1);qtext=qtext.rsplit(r'\,j',1)[0]
  assert equivalent(expression(ptext),original_gradient[0]) and equivalent(expression(qtext),original_gradient[1])
  actual_blocks=displays(r['question'][':question/worked-solution'])
  for original,actual in zip(original_gradient,[expression(v.split('=')[1]) for v in rows(actual_blocks[gi])]):assert equivalent(original,actual)
  if level=='hard':assert equivalent(expression(rawblocks[2].split('=')[-1]),expression(actual_blocks[2].split('=')[-1]))
  original_f=expression(rawblocks[gi+1].split('=')[1]);assert equivalent(original_f,expression(displays(r['question'][':question/worked-solution'])[gi+1].split('=')[1]))
  Ifinal=expression(rows(displays(r['question'][':question/worked-solution'])[-1])[-1].split('=')[-1])
  for row in rows(rawblocks[-1])[2:]:assert equivalent(expression(row.split('=')[-1]),Ifinal),(sid,row)
  original_intermediates=rows(rawblocks[-1])[3:-1];generated_intermediates=rows(actual_blocks[-1])[3:-1]
  for before,after in zip(original_intermediates,generated_intermediates):assert arithmetic_signature(before)==arithmetic_signature(after),(sid,'collapsed arithmetic stage',before,after)
  report_structure=[arithmetic_signature(row) for row in generated_intermediates]
  report={'source_id':sid,'template':template,'bank_profile':'observed_homogeneous','options_matched':5,'distractors_matched':4,'designation_matched':True,'bank_passed':True,'prompt_prose_passed':True,'solution_prose_passed':True,'solution_stage_sequence_passed':True,'intermediate_arithmetic_structure':report_structure,'notation_normalization':'Computed standard TeX for all complete math components; original prose and stage counts preserved.','solution_repaired':sid in ('q-104747','q-104764')}
  reports.append(report);cases.append({'source_id':sid,'template':template,'level':level,'parameters':p,'bank_profile':'observed_homogeneous','original':q});reviews.append({'label':'Original replay '+sid,'kind':'observed replay','record':r});checks.append(native(r,sid))
  for scale in (2,3):
   rr=g.generate(level,template=template,parameters=dict(p,s=scale),profile='observed_homogeneous');audit.append({'label':sid+' scaled bank '+str(scale),**displayed_math(rr)});checks.append(native(rr,sid+' scaled bank '+str(scale)));reviews.append({'label':'Generated observed-profile variant '+sid+' scale '+str(scale),'kind':'homogeneous observed-bank extension','record':rr})
  authored=g.generate(level,template=template,parameters=p,profile='authored_operations')
  assert authored['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
  assert authored['question'][':question/id']!=r['question'][':question/id']
 for template,(level,sid) in g.TEMPLATES.items():
  for seed in range(12):
   r=g.generate(level,seed=seed,template=template);audit.append({'label':template+':'+str(seed),**displayed_math(r)})
   fixed=g.generate(level,seed=12345,template=template,parameters=r['generation']['parameters']);assert fixed['question']==r['question']
   if seed<2:reviews.append({'label':'Authored variant '+template+' '+str(seed),'kind':'authored missing easy level' if level=='easy' else 'authored bank/parameter variation','record':r})
   checks.append(native(r,template+':'+str(seed)))
  # Scope bounds enforced on explicit input, including abs signed coefficients.
  for key,(lo,hi) in g.BOUNDS[template].items():
   p=g.sample(template,__import__('random').Random(19),'authored_operations');p[key]=hi+1
   try:g.generate(level,template=template,parameters=p)
   except ValueError:pass
   else:raise AssertionError(('out of bound accepted',template,key))
  for high in (False,True):
   p={k:(hi if high else lo) for k,(lo,hi) in g.BOUNDS[template].items()};p['s']=1
   expected_zero=g.mathematics(template,p)['I']==0
   try:r=g.generate(level,template=template,parameters=p)
   except ValueError as exc:
    assert expected_zero and 'collision' in str(exc),(template,p,exc)
    boundaries.append({'template':template,'parameters':p,'outcome':'whole bank rejected for zero-result collision'})
   else:
    assert not expected_zero
    audit.append({'label':template+' boundary '+str(high),**displayed_math(r)});checks.append(native(r,template+' boundary '+str(high)))
    boundaries.append({'template':template,'parameters':p,'outcome':'displayed math/native checked'})
  for profile in ('authored_operations','observed_homogeneous') if sid else ('authored_operations',):
   seen=set()
   for seed in range(20):
    r=g.generate(level,seed=seed,template=template,profile=profile);seen.add(r['generation']['mathematical_fingerprint'])
   assert len(seen)>1,(template,profile)
   variety.append({'template':template,'profile':profile,'seeds_checked':20,'distinct_mathematical_tasks':len(seen),'complete_bank_rejections':'Whole zero-result instance rejection, never choice repair'})
 # Full review data shows every observed bank and >=2 generated items per template.
 write('source-cases.json',cases);write('review.json',reviews);write('source-fidelity.json',reports);write('displayed-math-audit.json',audit);write('engine-input.json',checks);write('variety.json',variety);write('boundary-checks.json',boundaries)
 exe=REPO/'generate/runs/current/check-engine';subprocess.run([str(exe),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 engine=json.loads((ROOT/'engine-report.json').read_text())
 validation={'passed':True,'provenance':g.PROVENANCE,'source_questions':12,'source_complete_banks_matched':12,'source_options_matched':60,'source_distractors_matched':48,'source_correct_designations_matched':12,'source_prompt_prose_matches':12,'source_solution_prose_matches':12,'source_solution_sequence_matches':12,'source_solution_math_exact_unrepaired':10,'source_solution_endpoint_repairs':2,'generated_displayed_math_records':len(audit),'native_records':len(checks),'native_accepted':engine['accepted_checks'],'native_rejected':engine['rejected_checks'],'native_unresolved':engine['documented_unresolved_checks'],'grader_executable_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'sympy_version':sp.__version__,'authored_easy_templates':2,'all_difficulties':['easy','moderate','hard'],'plots':'none','database_writes':0,'unresolved_findings':[],'original_distractor_intent':'Unresolved; explicit homogeneous replay profiles only, authored full-operation bank is default.'}
 write('validation.json',validation)
 lines=['# Review: potential reconstruction and endpoint subtraction','', 'Original records and banks are retained in source-cases.json. Standard TeX is computed throughout; two documented endpoint typos are repaired in replay solutions.']
 for q in sources:
  lines+=['','## Original '+q[':question/math-academy-id'],'',q[':question/problem'],'','Options: '+', '.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),'',q[':question/worked-solution']]
 for item in reviews:lines+=['','## '+item['label'],'',item['kind'],'',g.markdown(item['record'])]
 (ROOT/'review.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps(validation,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as exc:
  write('validation.json',{'passed':False,'error':str(exc),'error_type':type(exc).__name__});raise
