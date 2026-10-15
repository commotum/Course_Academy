"""Rendered math, source/profile fidelity, parameter slots and native grading."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
from functools import lru_cache
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE))
from math_parser import latex,clean,group,X as x,U as u,C,log_derivative
from math_format import normalize_tex,normalize_prose,validate_generated_record
spec=importlib.util.spec_from_file_location('g64227',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,z):(HERE/n).write_text(json.dumps(z,indent=2,ensure_ascii=False,default=str)+'\n')
@lru_cache(maxsize=60000)
def scalar(t):
 t=clean(t).replace('du','1');return sp.Integer(-1 if t=='-'else 1)if t in('','-','+')else latex(t)
@lru_cache(maxsize=30000)
def eq(a,b):
 d=a-b
 if d==0:return True
 # Exact reciprocal definitions keep complete arguments and avoid running
 # general trigonometric searches on every rational denominator.
 d=d.replace(lambda z:z.func in(sp.sec,sp.csc,sp.tan,sp.cot),lambda z:{sp.sec:lambda t:1/sp.cos(t),sp.csc:lambda t:1/sp.sin(t),sp.tan:lambda t:sp.sin(t)/sp.cos(t),sp.cot:lambda t:sp.cos(t)/sp.sin(t)}[z.func](z.args[0]))
 d=sp.cancel(d)
 if d==0:return True
 num,_=sp.fraction(d);num=sp.trigsimp(num)
 return num==0 or sp.simplify(num)==0

def read_integral(t):
 t=t.strip();m=re.search(r'(?:\{\\int \}|\\int)',t);assert m,('no integral',t)
 pre=scalar(t[:m.start()]+'{1}');i=m.end();L=R=None
 if i<len(t)and t[i]=='_':
  lo,j=group(t,i+1);assert t[j]=='^';hi,i=group(t,j+1);L,R=scalar(lo),scalar(hi)
 body=t[i:];v=x if any(z in body for z in(r'\text{d}x',r'\textrm{d}x'))else u
 return pre*scalar(body),v,L,R

def evalbar(t):
 m=re.search(r'(?:\{\|\}|\|)_',t)
 if not m:return None
 lo,j=group(t,m.end());assert t[j]=='^';hi,k=group(t,j+1)
 F=scalar(t[:m.start()]+t[k:]);return F,scalar(lo),scalar(hi)

def operands(sol):
 for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
  if r'\frac{\text{d}u}{\text{d}x}'in block:continue
  b=re.sub(r'\\(?:begin|end)\{aligned\}','',block).replace('&','')
  for row in b.split(r'\\'):
   for t in row.split('='):
    t=t.strip().rstrip('.')
    if t:yield t

def check(rec):
 validate_generated_record(rec);q=rec['question'];
 if rec['generation']['eligible_for_serving']:assert not g.has_operator_defect(q),'Unrepaired trig operator capture in normal output'
 sol=q[':question/worked-solution'];sid=rec['generation']['template'];p=rec['generation']['parameters'];t=g.PROFILES[sid]
 prompt=next(b for b in re.findall(r'\$(.*?)\$',q[':question/problem'],re.S)if r'\int'in b)
 target,var,L,R=read_integral(prompt.rstrip('.='));assert var==x
 # Preserve original expression domains before any cancellation in simplification.
 if sid in('q-49280','q-49281'):
  fi=prompt.index(r'\frac');_,j=group(prompt,fi+5);den,j=group(prompt,j);D=scalar(den)
  if sid=='q-49280':assert eq(D,sp.cos(4*p['a']*x)*sp.sin(4*p['a']*x)),(sid,'lost cancelled sine poles')
  else:assert D.has(sp.sec(2*p['a']*x)),(sid,'lost original secant poles')
 sm=re.search(r'Let\s+\$u=(.*?)\.\$',sol);assert sm,(sid,'missing substitution');S=scalar(sm[1]);dS=sp.diff(S,x)
 assert eq(S,g.sym(t['substitution']).subs(x,p['a']*x)),(sid,'stale substitution',S)
 # Every actual displayed trig identity is read with complete function operands.
 identities=0
 for b in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',sol):
  if '='not in b or b.startswith('u=')or r'\text{d}'in b:continue
  a,z=b.rstrip('.').split('=',1);assert eq(scalar(a),scalar(z)),(sid,'identity',b);identities+=1
 dm=re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(.*?)⟹(.*?)(?:\n|$)',sol)
 if dm:
  assert eq(scalar(dm[1]),dS),(sid,'du/dx',dm[1],dS)
  left,right=dm[2].rstrip('.').split('=');assert eq(scalar(left)*dS,scalar(right)),(sid,'differential',left,right)
 else:
  dm=re.search(r'\$(\\text\{d\}x=.*?)\$',sol);assert dm,(sid,'dx missing');a,b=dm[1].rstrip('.').split('=');assert eq(scalar(a),scalar(b)*dS)
 if t['bounds']:
  baseL,baseR=map(g.sym,t['bounds']);assert eq(L,baseL/p['a'])and eq(R,baseR/p['a']);assert L<R
  ul,ur=sp.simplify(S.subs(x,L)),sp.simplify(S.subs(x,R))
  table=re.search(r'\| \$x\$ \| \$(.*?)\$ \| \$(.*?)\$ \|\n\| --- \| --- \| --- \|\n\| \$u\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol);assert table,(sid,'table')
  assert all(eq(scalar(z),want)for z,want in zip(table.groups(),[L,R,ul,ur])),(sid,'table values')
  F=sp.Rational(p['k'],p['a'])*g.sym(t['u_primitive']);answer=sp.simplify(F.subs(u,ur)-F.subs(u,ul))
  # Every source definite interval stays inside its original trig continuity
  # component under a>0. Explicit source argument extrema lie in [0,pi/2],
  # denominators and radical arguments are positive including both endpoints.
  for node in sp.preorder_traversal(target):
   if node.func in(sp.tan,sp.sec):
    z=node.args[0];assert sp.N(z.subs(x,L))>=0 and sp.N(z.subs(x,R))<sp.pi/2
   if node.func in(sp.cot,sp.csc):
    z=node.args[0];assert sp.N(z.subs(x,L))>0 and sp.N(z.subs(x,R))<=sp.pi/2
 else:
  assert L is None and R is None;ul=ur=None;F=sp.Rational(p['k'],p['a'])*g.sym(t['u_primitive']);answer=F.subs(u,S)
 count={'identities':identities,'formal_integral_operands':0,'primitive_operands':0,'exact_endpoint_operands':0}
 for b in operands(sol):
  if r'\int'in b:
   f,v,lo,hi=read_integral(b);got=f if v==x else f.subs(u,S)*dS
   assert eq(got,target),(sid,'formal integral operand',b,got,target)
   if L is not None:
    assert lo is not None and hi is not None
    assert eq(lo,L if v==x else ul)and eq(hi,R if v==x else ur),(sid,'integral bounds',b)
   else:assert lo is None and hi is None
   count['formal_integral_operands']+=1
  elif evalbar(b):
   f,lo,hi=evalbar(b);assert eq(lo,ul)and eq(hi,ur),(sid,'primitive bounds',b)
   assert eq(log_derivative(f,u).subs(u,S)*dS,target),(sid,'primitive stage',b)
   assert eq(sp.simplify(f.subs(u,hi)-f.subs(u,lo)),answer),(sid,'primitive evaluation',b)
   count['primitive_operands']+=1
  else:
   f=scalar(b)
   if L is not None:assert eq(f,answer),(sid,'endpoint arithmetic',b,f,answer);count['exact_endpoint_operands']+=1
   else:
    assert f.has(C),(sid,'missing integration constant',b)
    got=log_derivative(f,u).subs(u,S)*dS if f.has(u)else log_derivative(f,x)
    assert eq(got,target),(sid,'primitive rewrite',b,got,target);count['primitive_operands']+=1
 assert count['formal_integral_operands']>0 and count['primitive_operands']>0
 for f in q[':question/answer-fields']:
  vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];ci=next(i for i,a in enumerate(f[':answer-field/choices'])if a[':answer/id']==f[':answer-field/correct'][1])
  equivalent=(lambda z:eq(z,answer))if L is not None else(lambda z:eq(log_derivative(z,x),target))
  assert equivalent(vals[ci]),(sid,'key math',vals[ci],answer)
  if f[':answer-field/type'].endswith('/radio'):
   assert len(vals)==5 and sum(equivalent(z)for z in vals)==1,(sid,'ambiguous bank')
   for i,z in enumerate(vals):
    for w in vals[:i]:assert not(eq(z,w)if L is not None else eq(log_derivative(z-w,x),0)),(sid,'duplicate options')
 return count

def native_checks(rec):
 out=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  correct=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/radio'):
   out.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a==correct else'rejected','mathematical_expected':'accepted'if a==correct else'rejected','purpose':'normal radio complete bank'}for a in f[':answer-field/choices'])
  else:
   v=correct[':answer/value'];z=scalar(v)
   for submitted,expect,purpose in[(v,'accepted','normal blank canonical'),(r'\frac{2('+v+r')}{2}','accepted','normal blank genuine uncollected equivalent'),(g.tex(z+1),'rejected','normal blank wrong additive shift'),(g.tex(-z),'rejected','normal blank wrong sign')]:out.append({'field_index':i,'submitted':submitted,'expected':expect,'mathematical_expected':expect,'purpose':purpose})
 return out

def native_probe(items):
 gaps=[]
 for item in items:
  for c in item['checks']:
   save('probe-input.json',[{'label':item['label'],'record':item['record'],'checks':[dict(c)]}]);expected=c['expected']
   proc=subprocess.run([str(HERE/'check-engine'),str(HERE/'probe-input.json'),str(HERE/'probe-report.json')],capture_output=True,text=True)
   if proc.returncode:
    m=re.search(r'expected (accepted|rejected|unresolved), got (accepted|rejected|unresolved)',proc.stderr);assert m,proc.stderr
    actual=m[2];c['expected']=actual;c['grading_gap']=actual!=expected
    gaps.append({'label':item['label'],'field_index':c['field_index'],'submitted':c.get('submitted',c.get('submitted_answer_id')),'mathematical_expected':expected,'native_outcome':actual,'purpose':c['purpose'],'qualification':'Actual normal generated field; mathematical entry retained. Native parser/equivalence gap is separate from generator fidelity.'})
 save('native-input.json',items);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('native-gaps.json',{'normal_generator_grading_gaps':gaps,'count':len(gaps),'diagnostic_blank_shape_probes_for_radio':0});return gaps

def main():
 assert(HERE/'source.json').read_bytes()==(HERE/'reference/sources.json').read_bytes()
 qs=g.SOURCE['record'][':knowledge-point/questions'];assert len(qs)==20 and all(q.get(':question/math-academy-id')for q in qs)
 originals=[];reviews=[];repairs=[];ledger=[];fidelity=[];stages=[];inputs=[];counts={n:0 for n in g.LEVELS}
 for sid,t in g.PROFILES.items():
  print('Checking',sid,flush=True);old=g.SOURCES[sid];rec=g.generate(t['difficulty'],0,sid,{'a':1,'k':1},raw_source=True);q=rec['question'];counts[t['difficulty']]+=1
  assert q[':question/problem']==normalize_prose(old[':question/problem'])and q[':question/worked-solution']==normalize_prose(old[':question/worked-solution'])
  for f,of in zip(q[':question/answer-fields'],old[':question/answer-fields']):
   assert f[':answer-field/key']==of[':answer-field/key']and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
   assert[a[':answer/value']for a in f[':answer-field/choices']]==[normalize_tex(a[':answer/value'])for a in of[':answer-field/choices']]
   ci=next(i for i,a in enumerate(of[':answer-field/choices'])if a[':answer/id']==of[':answer-field/correct'][':answer/id']);assert f[':answer-field/correct'][1]==f[':answer-field/choices'][ci][':answer/id']
   for i,a in enumerate(of[':answer-field/choices']):ledger.append({'source_id':sid,'field_key':of[':answer-field/key'],'source_answer_id':a[':answer/id'],'original_value':a[':answer/value'],'correct':i==ci,'complete_profile':t['bank_profile'],'recipe':"(k/a)*D(a*x) + C when indefinite; D is the exact following source expression with its C removed",'D':str(scalar(a[':answer/value'])-C if scalar(a[':answer/value']).has(C)else scalar(a[':answer/value'])),'original_replay_exact':True})
  stages.append({'source_id':sid,'original':check(rec)});originals.append(rec)
  normal=g.generate(t['difficulty'],0,sid,{'a':1,'k':1})
  assert normal['generation']['eligible_for_serving']
  if g.has_operator_defect(old):
   check(normal);repairs.append(normal)
   assert not rec['generation']['eligible_for_serving']
   assert normal['question'][':question/problem']==normalize_prose(g.repair_operators(old[':question/problem']))
   assert normal['question'][':question/worked-solution']==normalize_prose(g.repair_operators(old[':question/worked-solution']))
   for f,of in zip(normal['question'][':question/answer-fields'],old[':question/answer-fields']):assert [a[':answer/value']for a in f[':answer-field/choices']]==[normalize_tex(g.repair_operators(a[':answer/value']))for a in of[':answer-field/choices']]
  inputs.append({'label':'normal source '+sid,'record':normal,'checks':native_checks(normal)})
  fidelity.append({'source_id':sid,'complete_bank':True,'prompt_exact_after_format_normalization':True,'solution_exact_after_format_normalization':True,'fields_and_correct_designation_exact':True,'choices':len(q[':question/answer-fields'][0][':answer-field/choices']),'distractors':4 if q[':question/answer-fields'][0][':answer-field/type'].endswith('/radio')else 0})
  for a,k in[(2,3),(6,-6),(1,-1),(6,1)]:
   r=g.generate(t['difficulty'],42,sid,{'a':a,'k':k});c=check(r);reviews.append(r);stages.append({'source_id':sid,'parameters':{'a':a,'k':k},'changed':c})
   if(a,k)==(2,3):inputs.append({'label':'changed '+sid,'record':r,'checks':native_checks(r)})
  # All declared individual slot values, independent held-other-slot changes.
  for a,k in[(a,1)for a in range(1,7)]+[(1,k)for k in range(-6,7)if k]:
   r=g.generate(t['difficulty'],7,sid,{'a':a,'k':k});assert r==g.generate(t['difficulty'],7,sid,{'a':a,'k':k});assert g.PROFILES[r['generation']['template']]['bank_profile']==r['generation']['bank_profile']
  # Positive coordinate scaling and nonzero scalar multiplication are invertible;
  # every bank stays exactly as ambiguous/nonambiguous as its original profile.
 save('source-cases.json',[{'source_id':r['generation']['template'],'record':r}for r in originals]);save('review-cases.json',reviews+repairs);save('choice-ledger.json',ledger);save('source-replay.json',fidelity);save('rendered-stage-checks.json',stages)
 save('source-errors-and-repairs.json',{'ineligible_raw_cases':[{'source_id':r['generation']['template'],'record':r,'defect':'Captured bare brace-group trig names render as italic letter products; exact raw evidence is ineligible for serving.'}for r in originals if not r['generation']['eligible_for_serving']],'supported_repairs':[{'source_id':r['generation']['template'],'record':r,'correction':'Replace bare {sin}/{cos}/{tan}/{cot}/{sec}/{csc} function names with operatorname; all surrounding operands, prose, field banks and correct designation stay the same.','support':'The same source solutions use operatorname versions of these exact functions in adjacent identities and substitutions.'}for r in repairs],'notes':['q-352797 retains two distinct answer IDs with equivalent logarithm values, as blank collection permits equivalents.','q-49280 retains cancelled sine holes; q-49281 retains original secant holes.','q-49281 generic reciprocal identity in x is universal and valid.']})
 md=[]
 for i,r in enumerate(originals):md.extend(['## '+r['generation']['template']+' exact original'+(' (ineligible raw operator capture)'if not r['generation']['eligible_for_serving']else''),g.markdown(r),'### Changed a=2,k=3 (normal notation repair where needed)',g.markdown(reviews[4*i])])
 (HERE/'source-and-changed.md').write_text('\n\n'.join(md)+'\n')
 # Corrupt the actual displayed target/identity/du/primitive/bounds/key and require
 # rejection. The checks read rendered text independently of generator formulas.
 mutations=[]
 base=next(z for z in reviews if z['generation']['template']=='q-49278'and z['generation']['parameters']=={'a':2,'k':3})
 for name,old,new in [('identity',r'\operatorname{sec}⁡{6x}=\frac{1}{\operatorname{cos}⁡{6x}}',r'\operatorname{sec}⁡{6x}=\frac{1}{\operatorname{sin}⁡{6x}}'),('du',r'2\left(-3',r'2\left(3'),('primitive-constant','+C','')]:
  r=copy.deepcopy(base);s=r['question'][':question/worked-solution'];assert old in s,(name,old);r['question'][':question/worked-solution']=s.replace(old,new,1)
  try:check(r)
  except(AssertionError,ValueError):mutations.append({'mutation':name,'rejected':True})
  else:raise AssertionError(('mutation survived',name))
 r=copy.deepcopy(base);f=r['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id']for a in f[':answer-field/choices']if a[':answer/id']!=f[':answer-field/correct'][1])
 try:check(r)
 except AssertionError:mutations.append({'mutation':'key','rejected':True})
 else:raise AssertionError('key mutation survived')
 for sid,field,old,new,name in [
  ('q-49278',':question/problem',r'\operatorname{sin}⁡{6x}',r'\operatorname{sin}⁡{9x}','stale trig argument'),
  ('q-347941',':question/worked-solution','| $x$ | $\\frac{\\pi}{18}$','| $x$ | $\\frac{\\pi}{9}$','stale limit table'),
 ]:
  r=copy.deepcopy(next(z for z in reviews if z['generation']['template']==sid and z['generation']['parameters']=={'a':2,'k':3}));assert old in r['question'][field],(name,old);r['question'][field]=r['question'][field].replace(old,new,1)
  try:check(r)
  except(AssertionError,ValueError):mutations.append({'mutation':name,'rejected':True})
  else:raise AssertionError(('mutation survived',name))
 for sid,expr,name in [('q-49280',r'\sec^{2}(8x)','cancelled sine holes removed'),('q-49281',r'\cos(4x)','original secant holes removed')]:
  r=copy.deepcopy(next(z for z in reviews if z['generation']['template']==sid and z['generation']['parameters']=={'a':2,'k':3}));r['question'][':question/problem']='Calculate $3\\int '+expr+r'\,\text{d}x.$'
  try:check(r)
  except(AssertionError,ValueError):mutations.append({'mutation':name,'rejected':True})
  else:raise AssertionError(('domain mutation survived',name))
 save('mutation-checks.json',mutations)
 invalid=0
 for fun,kw in[(g.generate,{'seed':True}),(g.generate,{'seed':1.5}),(g.batch,{'count':True}),(g.batch,{'count':0}),(g.batch,{'count':-1}),(g.batch,{'seed':'1'}),(g.generate,{'parameters':{'a':0,'k':1}}),(g.generate,{'parameters':{'a':1,'k':0}}),(g.generate,{'parameters':{'a':True,'k':1}})]:
  try:fun(**kw)
  except ValueError:invalid+=1
  else:raise AssertionError(('invalid accepted',kw))
 assert len(g.batch('all',1,2275))==3
 cli=subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','all','--count','1','--seed','2275','--format','json'],capture_output=True,text=True,check=True);assert len(json.loads(cli.stdout))==3
 save('boundary-checks.json',{'profiles':20,'changed_rendered_instances':80,'a_values':list(range(1,7)),'k_values':list(range(-6,0))+list(range(1,7)),'independent_held_other_slot_checks_per_profile':18,'strict_invalid_inputs_rejected':invalid,'all_count_one_json_records':3,'source_values_0_1_preserved':True,'domain':'positive a maps each source interval bijectively; negative nonzero k changes neither poles nor radical domain','profile_selection':'Complete profile selected first; no pooled options or fallback profiles'})
 inventory={level:set()for level in g.LEVELS};profile_counts={level:0 for level in g.LEVELS}
 for sid,t in g.PROFILES.items():
  for a in range(1,7):
   for k in list(range(-6,0))+list(range(1,7)):
    r=g.generate(t['difficulty'],0,sid,{'a':a,'k':k});inventory[t['difficulty']].add(r['generation']['mathematical_task_fingerprint']);profile_counts[t['difficulty']]+=1
 inventory_counts={level:len(v)for level,v in inventory.items()}
 # Same hard task appears through two source aliases, while the moderate sec²
 # normalization templates retain different original hole contracts.
 A=g.generate('hard',0,'q-73371',{'a':3,'k':1});B=g.generate('hard',0,'q-347942',{'a':2,'k':1});assert A['generation']['mathematical_task_fingerprint']==B['generation']['mathematical_task_fingerprint']
 A=g.generate('moderate',0,'q-49256',{'a':4,'k':1});B=g.generate('moderate',0,'q-49280',{'a':3,'k':1});assert A['generation']['mathematical_task_fingerprint']!=B['generation']['mathematical_task_fingerprint']
 rs=g.batch('all',12,2275);assert len({r['generation']['mathematical_task_fingerprint']for r in rs})==len(rs)
 save('mathematical-inventory.json',{'actual_distinct_mathematical_tasks_by_difficulty':inventory_counts,'profile_parameter_instances_by_difficulty':profile_counts,'total_actual_distinct_mathematical_tasks':len(set().union(*inventory.values())),'method':'Every declared pair emitted by normal generate; canonical actual integrand/bounds + original hole contract; excludes profile/seed/bank/field shape/choice order','batch_dedup':'mathematical task only, inside requested batch; every original remains eligible','hard_alias_equal_checked':True,'original_hole_contract_distinction_checked':True})
 gaps=native_probe(inputs)
 report={'status':'ready for independent QA','source_counts':counts,'actual_distinct_mathematical_tasks_by_difficulty':inventory_counts,'MA_originals':20,'non_MA_inventory':0,'source_choices_matched':len(ledger),'source_distractors_matched':sum(z['distractors']for z in fidelity),'complete_source_banks':20,'review_cases':len(reviews)+len(repairs),'authored_parameter_variants':80,'supported_original_notation_repairs':len(repairs),'raw_ineligible_operator_captures':len(repairs),'rendered_math_checks':len(stages)+len(repairs),'native_normal_cases':len(inputs),'native_checks':sum(len(z['checks'])for z in inputs),'native_gap_count':len(gaps),'registered_artifacts':'absent before creation; no existing numeric artifact imported','database_edits':False,'native_engine_edits':False,'fidelity':'20/20 exact normalized raw prompts, solutions, full banks, field contracts and correct designations; 11 bare trig-name captures ineligible for serving, separately supported operator-name repairs checked','limitations':['Finite conservative coordinate/numerator scales only; source exponents, sums, radical structure, bounds in argument space and method are fixed.','Native mathematical parser outcomes are recorded separately in native-gaps.json; valid output is never pruned to hide gaps.']};save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
