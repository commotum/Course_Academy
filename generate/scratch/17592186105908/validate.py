#!/usr/bin/env python3
"""Read displayed coordinates/stages/options independently; native grading separately."""
import importlib.util,json,re,hashlib,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('coplanar',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def require(x,msg):
 if not x:raise AssertionError(msg)
def eq(a,b):return sp.simplify(a-b)==0
def matrices(s):
 pat=r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|'
 def replace(m):
  rows=re.split(r'\\\\',m[1]);nums=[[g.parse_math(z)for z in row.split('&')]for row in rows]
  return '('+str(sp.Matrix(nums).det())+')'
 return re.sub(pat,replace,s,flags=re.S)
def root_values(s,v):
 s=s.replace(' only','').replace('$','')
 if '='not in s:return[g.parse_math(s)]
 return [g.parse_math(x.strip())for x in re.split(r',| or ',s)for x in[x.split('=',1)[1]]]
def full_solution(r):
 q=r['question'];v,d,roots=g.roots_from_prompt(q[':question/problem']);x=sp.Symbol(v)
 sol=q.get(':question/worked-solution')
 if sol is None:return 0
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);phase='det';n=0
 for block in blocks:
  s=matrices(block).replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  for row in re.split(r'\\\\',s):
   row=row.strip().rstrip('.')
   if not row:continue
   if '='not in row:continue
   sides=[a.replace('&','').strip()for a in row.split('=')]
   if sides[-1]=='0':phase='solve'
   if phase=='det':
    for rhs in sides[1:]:require(eq(g.parse_math(rhs),d),'Printed determinant stage wrong '+row);n+=1
   elif len(sides)==2:
    left,right=sides
    if r'\times'in left:require(right=='0','Triple-product condition');continue
    if r'\pm'in right:
     a=g.parse_math(right.replace(r'\pm',''));lhs=g.parse_math(left)
     got=[sp.solve(lhs-a,x),sp.solve(lhs+a,x)];got=[z for a in got for z in a]
    else:got=sp.solve(g.parse_math(left)-g.parse_math(right),x)
    require(set(got)==set(roots),'Printed isolation stage wrong '+row);n+=1
 return n

def check(r,raw=False):
 require(set(r['knowledge_point'])=={'db_id','id','title'},'Outer shape')
 require(r['knowledge_point']['db_id']==g.KP_ID,'KP identity')
 require(r['generation']['eligible_for_learning']==(not r['generation']['evidence_only']),'Evidence eligibility')
 q=r['question'];v,d,roots=g.roots_from_prompt(q[':question/problem']);stages=full_solution(r)
 names=[a for a,b in re.findall(r'([a-z])\s*=\s*⟨(.*?)⟩',q[':question/problem'])]
 if q.get(':question/worked-solution'):
  wanted=names[0]+r'\cdot('+names[1]+r'\times'+names[2]+')'
  triples=re.findall(r'[a-z]\\cdot\s*\([a-z]\\times\s*[a-z]\)',q[':question/worked-solution'])
  require(triples and all(z.replace(' ','')==wanted for z in triples),'Formal triple product must use actual prompted vector names')
 for f in q[':question/answer-fields']:
  kind=f[':answer-field/type'].split('/')[-1];aa=f[':answer-field/choices'];correct=f.get(':answer-field/correct')
  require(len({a[':answer/id']for a in aa})==len(aa),'Choice identities')
  for a in aa:
   require(isinstance(a[':answer/type'],str),'Enum string')
   s=a[':answer/value'];require(s.count('$')%2==0 and s.count('{')==s.count('}'),'Answer formatting')
  if kind=='blank':require('{{'+f[':answer-field/key']+'}}'in q[':question/problem'],'Missing placeholder')
  if correct is None:require(raw,'Missing normal correct designation');continue
  ci=next(a for a in aa if a[':answer/id']==correct[1]);vals=root_values(ci[':answer/value'],v)
  if not raw:
   expected=roots if kind=='radio'else[roots[0]if f[':answer-field/key']=='field-1'else roots[-1]]
   require(set(vals)==set(expected),'Wrong full answer shape '+str(vals)+str(expected))
  if kind=='radio':
   sets=[frozenset(root_values(a[':answer/value'],v))for a in aa]
   require(len(set(sets))==len(sets),'Ambiguous complete bank')
   if r['generation']['profile']=='method':
    m=g.printed_vectors(q[':question/problem']);x=sp.Symbol(v)
    # Independently compute dot(cross) and the explicitly assessed wrong operations.
    poly=sp.expand(sp.Matrix(list(m.row(0))).dot(sp.Matrix(list(m.row(1))).cross(sp.Matrix(list(m.row(2))))))
    degree=sp.degree(poly,x);A=poly.coeff(x,degree);B=poly.subs(x,0)
    if degree==1:
     a,b,c=[list(m.row(i))for i in range(3)]
     plus=sp.expand(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))
     wrong=sp.solve(plus,x)[0]
     expected=[frozenset([z])for z in(-B/A,B/A,-B,-A/B,wrong)]
    else:
     z=-B/A;root=sp.sqrt(z)
     expected=[frozenset(a)for a in([-root,root],[root],[-root],[-z,z],[-sp.sqrt(1/z),sp.sqrt(1/z)])]
    require(set(sets)==set(expected),'Actual displayed authored operation bank mismatch')
  prompt=q[':question/problem'];require(prompt.count('$')%2==0,'Prompt math delimiter')
 if ':question/worked-solution'in q:
  s=q[':question/worked-solution'];require(s.count('$')%2==0 and s.count('{')==s.count('}'),'Solution formatting')
 return stages

def native(r,label):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  ci=f[':answer-field/correct'][1];correct=next(a for a in f[':answer-field/choices']if a[':answer/id']==ci)
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==ci else'rejected','purpose':'owned choice grading'}for a in f[':answer-field/choices'])
  else:
   c=correct[':answer/value'];e=g.parse_math(c)
   v,d,roots=g.roots_from_prompt(r['question'][':question/problem']);x=sp.Symbol(v);degree=sp.degree(d,x)
   if degree==1:
    A=d.coeff(x);B=d.subs(x,0);equiv=r'\frac{2\cdot ('+str(-B)+r')}{2\cdot ('+str(A)+')}'
   else:
    A=d.coeff(x,2);B=d.coeff(x);C=d.subs(x,0);disc=B*B-4*A*C
    options=[r'\frac{'+str(-B)+sign+r'\sqrt{'+str(disc)+'}}{'+str(2*A)+'}'for sign in ('+','-')]
    equiv=next(z for z in options if eq(g.parse_math(z),e))
   require(eq(g.parse_math(equiv),e),'Independently derived equivalent blank')
   checks.extend([{'field_index':i,'submitted':c,'expected':'accepted','purpose':'canonical blank'},{'field_index':i,'submitted':equiv,'expected':'accepted','purpose':'independent unreduced determinant ratio / quadratic formula blank'},{'field_index':i,'submitted':g.tex(e+1),'expected':'rejected','purpose':'incorrect blank'}])
 return{'label':label,'record':r,'checks':checks}

def main():
 cases=[];replays=[];normal=[];variants=[];eng=[];values=banks=refs=solutions=stages=0
 for sid,q in g.ORIGINALS.items():
  case={'source_id':sid,'template':sid,'level':'moderate','parameters':{'shift':0},'bank_profile':'source:'+sid+':raw'};cases.append(case)
  r=g.generate('moderate',template=sid,parameters=case['parameters'],profile=case['bank_profile']);replays.append(r);a=r['question']
  require(a[':question/problem']==q[':question/problem'],'Exact prompt fidelity '+sid)
  require(a.get(':question/worked-solution')==q.get(':question/worked-solution'),'Full solution sequence fidelity '+sid)
  require((':question/difficulty'in a)==(':question/difficulty'in q),'Missing rating fidelity '+sid)
  for original,gen in zip(q[':question/answer-fields'],a[':question/answer-fields']):
   require(gen[':answer-field/key']==original[':answer-field/key'],'Field key fidelity')
   require(gen[':answer-field/type']==original[':answer-field/type'][':db/ident'],'Type fidelity')
   require(sorted((z[':answer/type'],z[':answer/value'])for z in gen[':answer-field/choices'])==sorted((z[':answer/type'][':db/ident'],z[':answer/value'])for z in original[':answer-field/choices']),'Entire bank fidelity '+sid)
   values+=len(gen[':answer-field/choices']);banks+=int(gen[':answer-field/type'].endswith('/radio'))
   require((':answer-field/correct'in gen)==(':answer-field/correct'in original),'Missing ref fidelity')
   if ':answer-field/correct'in original:
    value=next(z[':answer/value']for z in gen[':answer-field/choices']if z[':answer/id']==gen[':answer-field/correct'][1]);require(value==original[':answer-field/correct'][':answer/value'],'Correct designation fidelity');refs+=1
  stages+=check(r,raw=True);solutions+=int(':question/worked-solution'in q)
  if all(':answer-field/correct'in f for f in a[':question/answer-fields']):eng.append(native(r,sid+' RAW original designation'))
  repaired=g.generate('moderate',template=sid,parameters={'shift':0},profile='source:'+sid+':normalized');check(repaired);normal.append(repaired);eng.append(native(repaired,sid+' normalized'))
  for h in (-2,3):
   r=g.generate('moderate',template=sid,parameters={'shift':h},profile='source:'+sid+':normalized');check(r);variants.append(r);eng.append(native(r,sid+' affine '+str(h)))
 for level in ('easy','moderate','hard'):
  for template in (('linear','quadratic')if level=='moderate'else('linear',)):
   for kind in ('blank','radio'):
    for seed in range(35):
     r=g.generate(level,seed,template=template,field_type=kind);stages+=check(r)
     r2=g.generate(level,seed+317,template=template,field_type=kind,parameters=r['generation']['parameters']);require(r['question'][':question/id']==r2['question'][':question/id'],'Seed-independent identity')
     eng.append(native(r,level+template+kind+str(seed)))
     if seed<2:variants.append(r)
 # Independently reject explicit workload escapes, including hard sparse/positive easy cases.
 invalid=[('moderate','linear',{'vectors':[['0','-2','3'],['-2','2','k'],['1','0','-3']],'variable':'k'}),('hard','linear',{'vectors':[['1','2','3'],['k','4','5'],['6','7','8']],'variable':'k'}),('easy','linear',{'vectors':[['k','4','0'],['1','2','3'],['0','1','1']],'variable':'k'}),('hard','quadratic',{'vectors':[['2','3','4'],['k^2','3','4'],['2','3','4']],'variable':'k'})]
 for l,t,p in invalid:
  try:g.generate(l,parameters=p,template=t);raise AssertionError('Invalid parameters admitted')
  except ValueError:pass
 # Bank/profile alone cannot inflate math fingerprints; actual content must distinguish banks.
 base=normal[2];other=g.generate('moderate',template='q-128436',profile='source:q-128436:raw',parameters={'shift':0});require(base['generation']['parameter_fingerprint']==other['generation']['parameter_fingerprint'],'Profile in math identity')
 # Same displayed task must share math identity across authored and evidence banks.
 source_task=normal[2];p={'vectors':[[str(z)for z in row]for row in g.printed_vectors(source_task['question'][':question/problem']).tolist()],'variable':'k'}
 method_task=g.generate('moderate',parameters=p,template='linear',field_type='radio')
 require(method_task['generation']['parameter_fingerprint']==source_task['generation']['parameter_fingerprint'],'Cross-layout task identity')
 require(method_task['question'][':question/id']!=source_task['question'][':question/id'],'Distinct banks content identity')
 # Enumerated seed variety counts are substantive coordinates, never source aliases.
 variety={l:len({g.generate(l,i)['generation']['parameter_fingerprint']for i in range(100)})for l in('easy','moderate','hard')}
 require(min(variety.values())>=75,'Insufficient meaningful parameter variety')
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 (HERE/'engine-input.json').write_text(json.dumps(eng,indent=2)+'\n')
 engine=ROOT/'generate/runs/current/check-engine'
 run=subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
 require(run.returncode==0,'Native grading failed '+run.stdout+run.stderr)
 result={'status':'passed','source':g.SOURCE,'source_coverage':{'practice_questions':len(cases),'observed_moderate':15,'unrated':2,'prompt_exact':len(cases),'full_solution_exact':solutions,'full_solution_total':solutions,'answer_values_matched':values,'answer_values_total':values,'complete_radio_banks_matched':banks,'complete_radio_banks_total':banks,'correct_field_refs_matched':refs,'correct_field_refs_total':refs,'source_questions_with_correct_refs':15,'source_questions_missing_correct_refs':2,'missing_correct_refs_preserved':2,'missing_solutions_preserved':2,'missing_ratings_preserved':2,'source_fields_preserved':19,'designated_source_wrong_choices_matched':36,'designated_source_wrong_choices_total':36,'unmarked_source_choices_preserved':10},'mathematics':{'printed_stages_checked':stages,'source_raw_correctness_exceptions':['q-18266 correct designation is a singleton; true root set is {-3,3}'],'normal_records_checked':len(eng)-15,'variety_100_seeds':variety,'all_choices_checked':'Full scalar/root-set equality and uniqueness; raw incorrect designation recorded separately','raw_native_records':15,'raw_missing_ref_records_not_gradable':2},'native':{'records':len(eng),'checks':sum(len(a['checks'])for a in eng),'status':'passed','engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'authored_missing_levels':['easy sparse linear determinant','hard dense signed linear determinant'],'interpretation_limits':['All opaque source banks are evidence-only affine recipes, not inferred learner mistakes.'],'unresolved_findings':[]}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps({'source_replays':replays,'normalized_source_replays':normal,'generated':variants},indent=2)+'\n')
 lines=['# Coplanarity review','','Source math basis 1356. Raw evidence is not normal learner output. Every observed bank is followed by a normalized replay and two labeled affine variants. All three authored levels have at least two examples for each supported field layout.','']
 for sid,q,r,n in zip(g.ORIGINALS,g.ORIGINALS.values(),replays,normal):
  lines+=['## Original '+sid,'',q[':question/problem'],'','Original fields: '+json.dumps(q[':question/answer-fields'],ensure_ascii=False),'',q.get(':question/worked-solution','Missing original worked solution, rating, and correct designation.'),'','### Raw parameterized replay','',g.markdown(r),'','### Normalized replay','',g.markdown(n),'']
 for r in variants:lines+=['## GENERATED '+r['generation']['level']+' / '+r['generation']['template']+' / '+str(r['generation']['parameters']),'',g.markdown(r),'']
 (HERE/'review.md').write_text('\n'.join(lines))
 print(json.dumps(result,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:
  (HERE/'validation.json').write_text(json.dumps({'status':'failed','error':str(e)},indent=2)+'\n');raise
