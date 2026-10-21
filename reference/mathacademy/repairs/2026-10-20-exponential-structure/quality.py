"""Independent printed-equation algebra, role variation, source replay, delivery and grading."""
import importlib.util,sys,itertools,copy,re,random
from collections import Counter
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from read import *
from scripts.generator_publish import validate_question,answer_id,enum,prepare_records,content_fingerprint
sys.path.insert(0,str(HERE/'package'))
spec=importlib.util.spec_from_file_location('expanded_generator',HERE/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
h=g.hard
V={s:sp.Symbol(s,real=True)for s in ('x','y','t')};V['e']=sp.E
TRANS=standard_transformations+(implicit_multiplication_application,)
def group(text,pos):
 assert text[pos]=='{';depth=1;j=pos+1
 while depth:
  if text[j]=='{':depth+=1
  elif text[j]=='}':depth-=1
  j+=1
 return text[pos+1:j-1],j
def expr(text):
 text=text.strip().rstrip('.?').strip().replace('⁡','').replace(r'\operatorname{ln}',r'\ln')
 while (m:=re.search(r'\\(d?frac|sqrt)(?:\[([^]]+)\])?\{',text)):
  first,pos=group(text,m.end()-1)
  if m[1]=='sqrt':replacement='(('+str(expr(first))+')**(1/'+(m[2]or'2')+'))'
  else:
   second,end=group(text,pos);pos=end;replacement='(('+str(expr(first))+')/('+str(expr(second))+'))'
  text=text[:m.start()]+replacement+text[pos:]
 text=text.replace(r'\left','').replace(r'\right','').replace(r'\ln','log').replace(r'\cdot','*').replace('^','**').replace('{','(').replace('}',')')
 return parse_expr(text,local_dict=V,transformations=TRANS)
def equivalent(a,b):return sp.simplify(sp.expand_log(a-b,force=True))==0
def check(q):
 inline=re.findall(r'\$(.*?)\$',q[':question/problem'],re.S);equation=next(m for m in inline if ('e^'in m or '{e}^'in m)and'='in m);lhs,rhs=equation.split('=');lhs,rhs=expr(lhs),expr(rhs);variables=(lhs-rhs).free_symbols;assert len(variables)==1;v=next(iter(variables));linear=sp.expand_log(sp.log(lhs)-sp.log(rhs),force=True);expected=sp.solve(linear,v);assert len(expected)==1;expected=expected[0]
 f=q[':question/answer-fields'][0];correct=answer_id(f[':answer-field/correct']);options=[]
 for a in f[':answer-field/choices']:
  raw=a[':answer/value'].split('=')[-1];val=expr(raw);options.append(val);assert equivalent(val,expected)==(str(a[':answer/id'])==correct),(q[':question/id'],raw,expected)
 assert all(not equivalent(a,b)for a,b in itertools.combinations(options,2))
 steps=0
 for display in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
  display=re.sub(r'\\(?:begin|end)\{aligned\}','',display).replace('&','')
  for line in display.split(r'\\'):
   sides=line.split('=')
   for left,right in zip(sides,sides[1:]):
    assert equivalent(expr(left).subs(v,expected),expr(right).subs(v,expected)),(q[':question/id'],line,expected);steps+=1
 return steps
def coverage(records):
 return {'count':len(records),'sign_cases':dict(Counter(r['generation']['decision_case']for r in records)),'coefficients':sorted({r['generation']['parameters']['a']for r in records}),'offsets':sorted({r['generation']['parameters']['b']for r in records}),'variables':dict(Counter(r['generation']['parameters']['variable']for r in records)),'orders':dict(Counter(r['generation']['parameters']['order']for r in records)),'root_indices':sorted({r['generation']['parameters']['r']for r in records}),'radicands':sorted({r['generation']['parameters']['n']for r in records}),'answer_positions':dict(Counter(next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices'])if a[':answer/id']==answer_id(r['question'][':question/answer-fields'][0][':answer-field/correct']))for r in records)),'fixed_minus_unit_template':sum(r['generation']['parameters']['a']==-1 and r['generation']['parameters']['b']>0 for r in records)}
def main():
 all_records=[];checked=[];steps=0
 for seed in range(20):
  batch=g.generate(100,seed,'hard');assert batch==g.generate(100,seed,'hard');all_records+=batch
  for r in batch:validate_question(r['question']);p=r['generation']['parameters'];assert p['a']!=0 and p['b']!=0 and p['r']>=2 and p['n']>1
  if seed<1:
   for r in batch:steps+=check(r['question']);checked.append(r)
 raw=coverage(all_records);assert len(raw['sign_cases'])==4 and raw['coefficients']==list(h.COEFFICIENTS)and raw['offsets']==list(h.OFFSETS)and set(raw['answer_positions'])==set(range(5))
 # Vary the assessed role while keeping every option and RHS root fixed.
 roles=[(-2,3),(2,3),(-2,-3),(2,-3),(3,4)];counterfactuals=[]
 for key in range(5):
  for variable,order in itertools.product(('x','y','t'),('constant-first','variable-first')):
   r=h.build(roles,key,7,4,variable,order);steps+=check(r['question']);checked.append(r);counterfactuals.append(r)
 assert len({r['question'][':question/answer-fields'][0][':answer-field/correct'][1]for r in counterfactuals})==30
 # Correct answer IDs differ by question ownership; the mathematical values cover all five roles.
 values=[h.value(*roles[k],7,4)for k in range(5)];assert len(set(values))==5
 # Invalid explicit paths must not remove the target logarithm/root/linear skill.
 invalid=0
 for kwargs in ({'n':1},{'r':1},{'roles':[(0,3)]+roles[1:]},{'roles':[(2,0)]+roles[1:]},{'roles':[roles[0]]*5},{'order':'invalid'}):
  args=dict(roles=roles,key=0,n=7,r=4);args.update(kwargs)
  try:h.build(**args);raise AssertionError('Invalid domain accepted')
  except ValueError:invalid+=1
 # Previous moderate generator and its source replay retain identical learner content.
 oldspec=importlib.util.spec_from_file_location('old_generator',HERE/'original/generator.py');old=importlib.util.module_from_spec(oldspec);oldspec.loader.exec_module(old)
 oldbatch=old.generate(40,17);newbatch=g.generate(40,17)
 assert [r['question']for r in oldbatch]==[r['question']for r in newbatch]
 assert old.build(-5,4,21,replay=True)['question']==g.build(-5,4,21,replay=True)['question']
 for r in newbatch:steps+=check(r['question']);checked.append(r)
 sources=h.replay_sources();source_data=json.loads((HERE/'package/hard-sources.json').read_text())
 for r in sources:
  q=r['question'];source=next(s for s in source_data if s[':question/id']==r['generation']['source_question_id']);f=source[':question/answer-fields'][0];new=q[':question/answer-fields'][0]
  assert q[':question/problem']==h.normalize_prose(source[':question/problem']) and q[':question/worked-solution']==h.normalize_prose(source[':question/worked-solution'])
  assert {a[':answer/value']for a in new[':answer-field/choices']}=={h.normalize_tex(a[':answer/value'])for a in f[':answer-field/choices']}
  correct=next(a[':answer/value']for a in new[':answer-field/choices']if a[':answer/id']==answer_id(new[':answer-field/correct']));assert correct==h.normalize_tex(f[':answer-field/correct'][':answer/value']);steps+=check(q);checked.append(r)
 kp=json.loads((HERE/'kp.json').read_text())
 existing_authored=[q for q in kp[':knowledge-point/questions']if not q.get(':question/math-academy-id')]
 for q in existing_authored:steps+=check(q);checked.append({'question':q})
 # Reproduce publication normalization and duplicate filtering against actual inventory.
 fingerprints={content_fingerprint(q)for q in kp[':knowledge-point/questions']};delivered,duplicates=prepare_records(all_records,17592186087689,h.KP_ID,fingerprints,Path(DB.config.math_root),HERE/'delivery-assets',localizer=lambda r,*args:copy.deepcopy(r));delivered_coverage=coverage(delivered);assert len(delivered_coverage['sign_cases'])==4 and delivered_coverage['coefficients']==raw['coefficients']
 # Add one question for each coefficient/offset sign case and variable name.
 additions=[]
 for sa,sb,variable in itertools.product((-1,1),(-1,1),('x','y','t')):
  candidate=next(r for r in delivered if (1 if r['generation']['parameters']['a']>0 else -1)==sa and (1 if r['generation']['parameters']['b']>0 else -1)==sb and r['generation']['parameters']['variable']==variable and abs(r['generation']['parameters']['a'])>1 and r['question'][':question/id']not in {x['question'][':question/id']for x in additions})
  additions.append(candidate);steps+=check(candidate['question']);checked.append(candidate)
 assert len(additions)==12 and len(coverage(additions)['sign_cases'])==4 and len(coverage(additions)['orders'])==2
 save('additions.json',additions);save('grading-records.json',checked);save('pedagogical-variation.json',{'passed':True,'raw':raw,'after_publication_filter':delivered_coverage,'duplicates_removed':duplicates,'published_additions':coverage(additions),'controlled_fixed_bank_target_roles':5,'controlled_names_and_orders':6,'option_only_shortcut_bound':'For the same bank and RHS, each of five eligible roles can be selected; any fixed option-only rule succeeds on at most one of the five counterfactuals.','source_backbone':'Base e, isolated exponential, linear real unknown, exact logarithmic answer; hard roots add fractional-power conversion. Approximation and external rearrangement belong to sibling KPs.','limitations':'Finite samples do not rule out every conceivable shortcut. Fresh selection is checked from the committed native pool; learner histories and configured difficulty weights govern actual scheduling.'})
 questions=[]
 for record in checked:
  q=record['question'];fs=[]
  for f in q[':question/answer-fields']:
   correct=f[':answer-field/correct'];value=correct.get(':answer/value')if isinstance(correct,dict)else next(a[':answer/value']for a in f[':answer-field/choices']if str(a[':answer/id'])==answer_id(correct))
   fs.append({'key':f[':answer-field/key'],'type':enum(f[':answer-field/type']).split('/')[-1],'correct_value':value,'choices':[{'type':enum(a[':answer/type']).split('/')[-1],'value':a[':answer/value']}for a in f[':answer-field/choices']]})
  questions.append({'math_academy_id':str(q[':question/id']),'problem':q[':question/problem'],'knowledge_point':'Exact exponential equations using ln','answer_fields':fs})
 out=HERE/'native-grading';out.mkdir(exist_ok=True);(out/'input.json').write_text(json.dumps({'questions':questions})+'\n');binary=ROOT/'reference/mathacademy/repairs/2026-10-20-log-product-quotient/native-grading/grader';subprocess.run([str(binary),str(out/'input.json'),str(out/'results.json')],check=True);result=json.loads((out/'results.json').read_text());assert result['current_engine_ready_count']==len(questions)
 save('quality-verification.json',{'passed':True,'seeded_hard_questions':len(all_records),'deterministic':True,'source_hard_banks_replayed':len(sources),'moderate_regression_records':40,'existing_authored_questions_retained':len(existing_authored),'invalid_paths_rejected':invalid,'counterfactuals':len(counterfactuals),'native_grading_questions':len(questions),'new_questions':len(additions),'delivery_filter_tested':True});save('algebra-verification.json',{'passed':True,'printed_equations_checked':steps,'independently_checked_questions':len(checked),'method':'Parse printed prompt equations, solve independently with SymPy, compare every answer and worked-solution equation under the solution.'});print((HERE/'quality-verification.json').read_text())
if __name__=='__main__':main()
