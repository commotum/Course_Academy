#!/usr/bin/env python3
import os,sys,json,re,copy,subprocess,hashlib,importlib.util,itertools
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)
def write(name,data): (D/name).write_text(json.dumps(data,indent=2)+'\n')
def expr(s):
 s=s.replace('&','').strip();s=re.sub(r'\\cancel\{([^{}]*)\}',r'\1',s)
 s=re.sub(r'\\(?:left|right|bigl|bigr|,|;|!)','',s)
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 assert '\\' not in s,s
 return sp.expand(parse_expr(s,local_dict={c:sp.Symbol(c) for c in 'xyabuvst'},transformations=TRANS))
def eq(s):
 a,b=s.split('=');return expr(a),expr(b)
def pair(s): return tuple(expr(v) for v in s.strip()[1:-1].split(','))
def value(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def inners(text):return re.findall(r'\\begin\{aligned\}((?:(?!\\begin\{aligned\}).)*?)\\end\{aligned\}',text,re.S)
def lines(block):return [s.strip() for s in block.split('\\\\')]
def system(text):return [eq(s) for s in lines(inners(text)[0])]
COUNTS={'records':0,'system_rows':0,'operative_equations':0,'complete_radio_banks':0,'tuple_substitutions':0,'blank_fields':0,'prose_conclusions':0,'scalings':0,'cancellations':0,'substitution_recovery_stages':0}
def check(r,source=False,count=True):
 q=r['question'];text=q[':question/worked-solution'];p=r['generation']['parameters'];x,y=map(sp.Symbol,p['variables']);rows=system(q[':question/problem'])
 solved=sp.solve([a-b for a,b in rows],(x,y));X,Y=solved[x],solved[y]
 assert all((a-b).subs(solved)==0 for a,b in rows)
 assert rows==[(expr(g.lhs(p['a1'],p['b1'],str(x),str(y))),sp.Integer(p['c1'])),(expr(g.lhs(p['a2'],p['b2'],str(x),str(y))),sp.Integer(p['c2']))]
 for f in q[':question/answer-fields']:
  if f[':answer-field/type'].endswith('/radio'):
   choices=[pair(a[':answer/value']) for a in f[':answer-field/choices']]
   assert len(choices)==len(set(choices))==5
   valid=[z for z in choices if all((a-b).subs({x:z[0],y:z[1]})==0 for a,b in rows)]
   assert valid==[(X,Y)] and pair(value(f))==(X,Y)
   if count:COUNTS['complete_radio_banks']+=1;COUNTS['tuple_substitutions']+=10
  else:
   assert expr(value(f))==({'field-1':X,'field-2':Y}[f[':answer-field/key']])
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
   if count:COUNTS['blank_fields']+=1
 # Check all real equations in every innermost aligned display. Scaling-marked
 # rows are checked separately as before/after objects, not misread as equations.
 blocks=inners(text);checked=0
 for block in blocks:
  for line in lines(block):
   if r'\times' in line:continue
   a,b=eq(line)
   assert sp.simplify((a-b).subs(solved))==0,(line,solved)
   checked+=1
 # Independently derive operation from prose, and read AFTER system.
 m=re.search(r'multiply the (first|second) equation by \$([^$]+)\$',text);assert m
 row=0 if m[1]=='first' else 1;mult=expr(m[2].strip().rstrip(','));assert mult.is_integer and 2<=abs(mult)<=7
 expected=[(sp.expand(a*(mult if i==row else 1)),b*(mult if i==row else 1)) for i,(a,b) in enumerate(rows)]
 assert [eq(s) for s in lines(blocks[1])]==expected
 assert sum(a.coeff(x) for a,b in expected)==0
 cancellation=next(b for b in blocks if r'\cancel' in b)
 stages=[eq(s) for s in lines(cancellation)]
 assert stages[:2]==expected
 total=(sp.expand(sum(a for a,b in expected)),sum(b for a,b in expected))
 assert stages[2]==total
 # Source easy combines term collection and solving because y coefficient is1.
 assert stages[-1]==(y,Y)
 if len(stages)==5:assert stages[3]==total
 # Every supplied recovery row and substitution operand must match its chosen
 # original row, not merely have the same final key.
 recovery=blocks[-1];back=[eq(s) for s in lines(recovery)]
 chosen=re.search(r"choose the (first|second) equation",text);assert chosen
 i=0 if chosen[1]=='first' else 1;a,b=rows[i];aa=a.coeff(x);bb=a.coeff(y)
 assert back[0]==rows[i]
 assert back[1]==back[2]==(sp.expand(aa*x+bb*Y),b)
 assert back[-1]==(x,X)
 if len(back)==5:assert back[3]==(aa*x,b-bb*Y)
 assert re.search(r'\('+re.escape(str(Y))+r'\)',re.sub(r'\\(?:left|right)','',lines(recovery)[1]))
 conclusion=text[text.index('Therefore,'):]
 tupletext=re.search(r'expressed as \$([^$]+)\$',conclusion);assert tupletext
 assert pair(tupletext[1].rstrip('.'))==(X,Y)
 g.validate_generated_record(r)
 if count:
  COUNTS['records']+=1;COUNTS['system_rows']+=2;COUNTS['operative_equations']+=checked;COUNTS['prose_conclusions']+=1;COUNTS['scalings']+=1;COUNTS['cancellations']+=2;COUNTS['substitution_recovery_stages']+=len(back)
 return (X,Y)

def main():
 cases=json.loads((D/'source-cases.json').read_text());source=[];repairs=[];replays=[]
 for c in cases:
  sid=c['source_id'];assert c['record']==g.ORIGINALS[sid]
  r=g.replay_source(sid,True);check(r,True);replays.append(r)
  before=c['record'];after=r['question']
  for original_field,served_field in zip(before[':question/answer-fields'],after[':question/answer-fields']):
   if ':answer-field/choices' in original_field:
    assert [a[':answer/value'] for a in original_field[':answer-field/choices']]==[a[':answer/value'] for a in served_field[':answer-field/choices']]
    assert original_field[':answer-field/correct'][':answer/id']==served_field[':answer-field/correct'][1]
  if ':question/worked-solution' in before:assert g.normalize_prose(before[':question/worked-solution'])==after[':question/worked-solution']
  repairs.append({'source_id':sid,'raw_record_preserved':True,'changes':[{'attribute':k,'raw':before.get(k),'supported':after[k],'reason':'Mathematical formatting repair only' if k in before else 'Explicitly authored completion; absent in capture'} for k in (':question/problem',':question/worked-solution',':question/difficulty') if before.get(k)!=after.get(k)],'missing_raw_field_values':sid=='q-208816','supported_solution':list(map(str,g.values(g.ANCHORS[sid])))})
  source.append({'source_id':sid,'raw_content_and_omissions_exact':True,'source_options_matched':sum(len(f.get(':answer-field/choices',[])) for f in before[':question/answer-fields']),'source_complete_banks_matched':1 if sid=='q-18787' else 0,'source_distractors_matched':4 if sid=='q-18787' else 0,'source_distractors_total':4 if sid=='q-18787' else 0,'source_designations_matched':sum(':answer-field/correct' in f for f in before[':question/answer-fields']),'prose_and_operative_stages_preserved':sid!='q-208816','omitted_solution_authored':sid=='q-208816'})
 write('source-repairs.json',repairs);write('source-fidelity.json',source);write('source-replays.json',replays)
 samples=[];variety={};slot={}
 for level in ('easy','moderate','hard'):
  tasks=set();orient=set();signs=set();labels=set();templates=set()
  for template in g.TEMPLATES:
   for seed in range(40):
    r=g.generate(level,seed,template);check(r);tasks.add(r['generation']['mathematical_fingerprint']);templates.add(template)
    p=r['generation']['parameters'];row,m=g.operation(p);orient.add(row);signs.add(int(sp.sign(m)));labels.add(p['variables'])
    if seed<4:samples.append(r)
  assert orient=={0,1} and signs=={-1,1} and labels=={'xy','ab','uv','st'}
  variety[level]={'checked':120,'unique_mathematical_tasks':len(tasks),'templates':sorted(templates),'scaled_rows':sorted(orient),'multiplier_signs':sorted(signs),'variable_pairs':sorted(labels),'finite_supported_batch_capacity':g.CAPACITY[level]}
 # Retain same mathematical fingerprint for alias and independent row scales.
 r=g.generate('moderate',99,template='blank_solution');p=copy.deepcopy(r['generation']['parameters']);p['variables']='xy';alias=g.canonical_task(p)
 for k in ('a1','b1','c1'):p[k]*=2
 assert g.canonical_task(p)==alias==r['generation']['mathematical_fingerprint']
 # Explicit controls retain correct fields and final prose but corrupt a real stage.
 controls=[];r=next(r for r in samples if r['generation']['template']=='moderate_blank_solution')
 text=r['question'][':question/worked-solution']
 replacements=[('scaling',r'\Longrightarrow',r'\Longrightarrow\, 99'),('cancellation',r'\cancel{',r'\cancel{9'),('collection',None,None),('recovery',None,None)]
 # Target exact printed constants in the stage, avoiding the final answer.
 bs=inners(text);cancel=next(b for b in bs if '\\cancel' in b);ls=lines(cancel);back=lines(bs[-1])
 edits=[('scaling',bs[1],bs[1].replace('=', '=1+',1)),('cancellation',ls[0],ls[0].replace('=', '=1+',1)),('term_collection',ls[3],ls[3].replace('=', '=1+',1)),('recovered_variable',back[2],back[2].replace('=', '=1+',1))]
 for name,old,new in edits:
  bad=copy.deepcopy(r);bad['question'][':question/worked-solution']=text.replace(old,new,1)
  try:check(bad,count=False)
  except (AssertionError,ValueError):controls.append({'name':name,'same_final_key':True,'rejected':True})
  else:raise AssertionError(name)
 bad=copy.deepcopy(r);fs=bad['question'][':question/answer-fields'];fs[0][':answer-field/key'],fs[1][':answer-field/key']='field-2','field-1'
 try:check(bad,count=False)
 except AssertionError:controls.append({'name':'blank_order','same_final_key':True,'rejected':True})
 else:raise AssertionError('blank order')
 write('negative-controls.json',controls)
 # Native learner grader: full prompt context, every option ID and blank math.
 inputs=[]
 for i,r in enumerate(replays+samples):
  checks=[]
  for fi,f in enumerate(r['question'][':question/answer-fields']):
   if f[':answer-field/type'].endswith('/radio'):
    checks += [{'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'entire supplied tuple option in native radio control'} for a in f[':answer-field/choices']]
   else:
    n=expr(value(f));equiv=r'\frac{'+str(2*n)+'}{2}'
    for s,expected,purpose in [(value(f),'accepted','exact coordinate fragment'),(equiv,'accepted','equivalent rational entry with full provided tuple context'),(str(n+1),'rejected','wrong mathematics'),(str(-n),'rejected','wrong sign')]:checks.append({'field_index':fi,'submitted':s,'expected':expected,'purpose':purpose})
  inputs.append({'label':str(i),'record':r,'checks':checks})
 write('engine-input.json',inputs)
 subprocess.run([str(D/'check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 # Full tuple math diagnostics use the native blank evaluator, preserving the
 # original complete system context. This fixture does not change served fields.
 diagnostics=[]
 for i,r in enumerate(samples):
  if r['generation']['template']!='radio_solution':continue
  probe=copy.deepcopy(r);f=probe['question'][':question/answer-fields'][0];correct=value(f);f[':answer-field/type']=':answer-field.type/blank'
  probe['question'][':question/problem']+='\n\nThe ordered pair is {{selection}}.'
  good=pair(correct);equivalent='('+','.join(r'\frac{'+str(2*n)+'}{2}' for n in good)+')'
  for submission,expected in [(correct,'accepted'),(equivalent,'accepted'),('('+str(good[0]+1)+','+str(good[1])+')','rejected')]:
   inp=[{'label':'tuple-'+str(i),'record':probe,'checks':[{'field_index':0,'submitted':submission,'expected':expected,'purpose':'full tuple mathematics diagnostic'}]}];write('tuple-probe.json',inp)
   out=D/'tuple-probe-report.json';result=subprocess.run([str(D/'check-engine'),str(D/'tuple-probe.json'),str(out)],text=True,capture_output=True)
   diagnostics.append({'sample':i,'submission':submission,'expected':expected,'passed':result.returncode==0,'report':json.loads(out.read_text()) if result.returncode==0 else None,'diagnostic':result.stderr if result.returncode else None})
 write('tuple-diagnostics.json',diagnostics)
 # Full tuples are not a served blank contract. Retain unsupported parser outcomes.
 assert all(d['passed'] or 'got unresolved' in d['diagnostic'] for d in diagnostics)
 write('samples.json',samples);write('variety.json',variety)
 # Strict API and CLI contracts.
 for value_ in (True,1.0,'1',None):
  try:g.generate('easy',value_)
  except TypeError:pass
  else:raise AssertionError('seed strictness')
  try:g.generate_batch('easy',count=value_)
  except TypeError:pass
  else:raise AssertionError('count strictness')
 for count in (0,-1,2001):
  try:g.generate_batch('easy',count=count)
  except ValueError:pass
  else:raise AssertionError('count bounds')
 command=[sys.executable,str(D.with_suffix('.py')),'--difficulty','all','--count','1','--seed','17']
 output=subprocess.check_output(command+['--format','json'],text=True);assert len(json.loads(output))==3
 assert subprocess.check_output(command+['--format','markdown'],text=True).count('Therefore,')==3
 assert output==subprocess.check_output(command+['--format','json'],text=True)
 write('cli-review.json',json.loads(output))
 write('validation.json',{'mathematics':COUNTS,'negative_controls':len(controls),'source_originals':len(cases),'non_ma_inventory':len(json.loads((D/'independent-inventory.json').read_text())['questions']),'native_tuple_probes':len(diagnostics),'native_false_accepts':0,'native_false_rejects':0,'native_unresolved_served_fields':0,'native_unresolved_tuple_diagnostics':sum(not d['passed'] for d in diagnostics),'strict_api_cli':True,'database_writes':0,'registered_imports':0})
 print(COUNTS)
if __name__=='__main__':main()
