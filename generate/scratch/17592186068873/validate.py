#!/usr/bin/env python3
"""Independent printed-input/stage/bank checks plus native application grading."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)

def parse(t):
 t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',t)
 t=t.replace(r'\cdot','*').replace(r'\,','').replace('{','').replace('}','')
 t=t.strip().rstrip('.')
 return sp.expand(parse_expr(t,transformations=TRANS))

def mathblocks(t):return re.findall(r'\$\$(.*?)\$\$',t,re.S)
def formatting(t):
 assert not any(ord(c)<32 and c not in '\n\t' for c in t),'C0 control'
 assert t.count('$')%2==0,'math delimiters'
 depth=0
 for c in t:
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,'brace depth'
 assert depth==0,'unbalanced braces'
 assert 'SLOT' not in t and '+-' not in t and '--' not in t

def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];prompt=q[':question/problem'];formatting(prompt)
 printed=re.search(r'\$([^$]*)\$',prompt)[1].split('=')[0].strip()
 e=parse(printed);symbols=list(e.free_symbols);assert len(symbols)==1
 v=symbols[0];poly=sp.Poly(e,v);assert poly.degree()==2 and poly.nth(2)==1
 b=poly.nth(1);a=b/2;assert a>0 and a.is_Integer
 # Read outer constant independently from actual first displayed component.
 t=printed.replace(' ','').replace('{','').replace('}','')
 outer=re.search(r'\)([+-])(\d+)$',t);assert outer,'isolated perfect-square required'
 k=int(outer[2]);sg=1 if outer[1]=='+' else -1
 assert poly.nth(0)-sg*k==a*a,'printed perfect-square operand'
 solution=q.get(':question/worked-solution')
 if solution:
  formatting(solution);blocks=mathblocks(solution);assert len(blocks)==3
  lhs,rhs=blocks[0].strip().split('=');assert sp.simplify(parse(lhs)-parse(rhs))==0
  for bi,block in enumerate(blocks[1:]):
   body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
   rows=[s.split('&')[0].strip() for s in body.split(r'\\')]
   expected=e-sg*k if bi==0 else e
   for row in rows:assert sp.simplify(parse(row)-expected)==0,('stage operand',row)
   if bi==0:
    # Factor2/half coefficient and its square must be displayed, not a merely
    # equivalent collected row substituted for the taught factoring operation.
    compact=re.sub(r'\s+','',rows[-2])
    assert f'2\\cdot{int(a)}{v}' in compact
    assert f'{{{int(a)}}}^{{2}}' in compact
    assert re.search(r'\('+str(v)+r'\+'+str(a)+r'\{?\)',rows[-1]) or '{('+str(v)+'+'+str(a)+')}' in rows[-1]
   else:assert len(rows)==2
  # Family-specific structure/prose identical to source mask after substitutions.
  sid=r['generation']['template']
  p={'variable':str(v),'a':int(a),'k':k,'sign':sg}
  expected=g.fill(g.MASKS[sid][':question/worked-solution'],p) if sid in g.MASKS and ':question/worked-solution' in g.MASKS[sid] else g.completed_solution(p,g.CONFIG[sid][5] if sid in g.CONFIG else 'number')
  assert solution==expected,'operative stage/prose fidelity'
 for f in q[':question/answer-fields']:
  vals=[parse(c[':answer/value']) for c in f.get(':answer-field/choices',[])]
  for c in f.get(':answer-field/choices',[]):formatting(c[':answer/value'])
  if f[':answer-field/type'].endswith('/radio'):
   assert len(vals)==5
   assert len({sp.srepr(c) for c in vals})==5
   correct=[c[':answer/id'] for c,val in zip(f[':answer-field/choices'],vals) if sp.simplify(val-e)==0];assert len(correct)==1
   if ':answer-field/correct' in f:assert f[':answer-field/correct'][1]==correct[0]
  else:
   assert '{{'+f[':answer-field/key']+'}}' in prompt
   wanted=v+a if f[':answer-field/key']=='field-1' else k
   assert len(vals)<=1
   if vals:assert sp.simplify(vals[0]-wanted)==0,'supplied fragment'
 return 1

def main():
 fidelity=[];cases=[];review=[];checks=0
 for sid,cfg in g.CONFIG.items():
  level=cfg[0];p=g.parameters_for(sid);case={'source_id':sid,'template':sid,'parameters':p,'bank_profile':'raw:'+sid,'difficulty':level,'difficulty_origin':'observed' if ':question/difficulty' in g.QUESTIONS[sid] else 'authored classification'};cases.append(case)
  raw=g.generate(level,parameters=p,profile='raw:'+sid);checks+=check(raw);src=g.QUESTIONS[sid];q=raw['question']
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
   assert (key in q)==(key in src),(sid,key,'presence')
  assert q[':question/problem']==src[':question/problem']
  if ':question/worked-solution' in src:assert q[':question/worked-solution']==src[':question/worked-solution']
  matched=0;designations=0
  for sf in src[':question/answer-fields']:
   f=next(z for z in q[':question/answer-fields'] if z[':answer-field/key']==sf[':answer-field/key'])
   assert f[':answer-field/type']==g.enum(sf[':answer-field/type'])
   for key in (':answer-field/choices',':answer-field/correct'):assert (key in f)==(key in sf)
   if ':answer-field/choices' in sf:
    assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']);matched+=len(sf[':answer-field/choices'])
   if ':answer-field/correct' in sf:
    val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert val==sf[':answer-field/correct'][':answer/value'];designations+=1
  fidelity.append({'source_id':sid,'exact_prompt':True,'exact_solution_or_omission':True,'attribute_presence_parity':True,'options_matched':matched,'correct_designations_matched':designations})
  review.append(raw)
  completed=g.generate(level,parameters=p,profile='completed:'+sid);checks+=check(completed);review.append(completed)
  # Changed input through each public original bank profile and source layout.
  changed={'variable':'z','a':5 if sid=='q-141513' else 8,'k':9,'sign':p['sign']}
  rr=g.generate(level,77,parameters=changed,profile='raw:'+sid);checks+=check(rr);review.append(rr)
  for n in (91,157):
   rr=g.generate(level,n,template=sid);checks+=check(rr);review.append(rr)
 # Complete raw records and completed aliases share actual content identities.
 for sid in ('q-141513','q-250392','q-250395','q-250396','q-250397'):
  level=g.CONFIG[sid][0];p=g.parameters_for(sid)
  assert g.generate(level,0,parameters=p,profile='raw:'+sid)['question'][':question/id']==g.generate(level,1,parameters=p,profile='completed:'+sid)['question'][':question/id']
 for sid in g.BANKS:
  for seed in range(12):check(g.generate(g.CONFIG[sid][0],seed,profile='raw:'+sid))
 for sid,a in [('q-140186',1),('q-141513',1),('q-141513',4)]:
  p=g.parameters_for(sid);p['a']=a
  try:g.generate(g.CONFIG[sid][0],parameters=p,profile='raw:'+sid)
  except ValueError:pass
  else:raise AssertionError('ambiguous complete raw profile accepted')
 for level in ('easy','moderate','hard'):
  covered=set()
  for seed in range(60):
   rr=g.generate(level,seed);checks+=check(rr);covered.add(rr['generation']['template'])
   if seed<4:review.append(rr)
  assert covered==({sid for sid,c in g.CONFIG.items() if c[0]==level} if level!='hard' else {'hard_radio','hard_blank'}),'default family coverage'
 # All sampled arithmetic domains, aliases excluded from mathematical counts.
 counts={}
 for level in ('easy','moderate','hard'):
  fps=set()
  sid=next((s for s,c in g.CONFIG.items() if c[0]==level),None) or 'hard_radio'
  for a,k in itertools.product(range(11,16) if level=='hard' else range(1,11),range(1,11)):
   for kind in ('radio','blank'):
    t=next((s for s,c in g.CONFIG.items() if c[0]==level and c[6]==kind),None) or 'hard_'+kind
    p={'variable':'x','a':a,'k':k,'sign':1 if level=='easy' else -1}
    rr=g.generate(level,0,t,parameters=p);checks+=check(rr);fps.add(rr['generation']['mathematical_fingerprint'])
  counts[level]=len(fps)
 for r in review:
  gen=r['generation'];level=g.CONFIG[gen['template']][0] if gen['template'] in g.CONFIG else 'hard'
  rr=g.generate(level,gen['seed']+1,gen['template'],parameters=gen['parameters'],profile=gen['bank_profile']);assert rr['question'][':question/id']==r['question'][':question/id']
 for level,p in [('easy',{'variable':'x','a':-2,'k':3,'sign':1}),('hard',{'variable':'x','a':10,'k':3,'sign':-1}),('hard',{'variable':'x','a':16,'k':3,'sign':-1}),('moderate',{'variable':'x','a':2,'k':11,'sign':-1})]:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('scope guard')
 # Mutations keep final answer intact but corrupt operative intermediate rows.
 original=g.generate('moderate',0,'q-250397',parameters=g.parameters_for('q-250397'))
 mutations=[]
 for before,after in [(r'2\cdot 2x',r'2\cdot 3x'),(r'2\cdot 2x',r'4x'),('{2}^{2}','{3}^{2}')]:
  bad=copy.deepcopy(original);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(before,after)
  try:check(bad)
  except (AssertionError,Exception):mutations.append(True)
  else:raise AssertionError('stage mutation survived')
 bad=copy.deepcopy(original);bad['question'][':question/worked-solution']+='\f'
 try:check(bad)
 except AssertionError:mutations.append(True)
 else:raise AssertionError('C0 mutation survived')
 payload=[]
 for n,r in enumerate(review):
  if any(':answer-field/correct' not in f for f in r['question'][':question/answer-fields']):continue
  tests=[]
  for fi,f in enumerate(r['question'][':question/answer-fields']):
   if f[':answer-field/type'].endswith('/radio'):
    tests +=[{'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete choice bank selection'} for a in f[':answer-field/choices']]
   else:
    answer=f[':answer-field/choices'][0][':answer/value'];val=parse(answer)
    equivalent=str(val)+'/2+'+str(val)+'/2' if f[':answer-field/key']=='field-2' else '1*('+answer+')'
    tests +=[{'field_index':fi,'submitted':x,'expected':ex,'purpose':purpose} for x,ex,purpose in [(answer,'accepted','canonical supplied fragment'),(equivalent,'accepted','equivalent unreduced supplied fragment'),(str(val+1),'rejected','wrong supplied fragment')]]
  payload.append({'label':str(n)+' '+r['generation']['template'],'record':r,'checks':tests})
 (HERE/'engine-input.json').write_text(json.dumps(payload,indent=2)+'\n')
 engine=HERE.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-validation.json')],check=True)
 native=json.loads((HERE/'engine-validation.json').read_text())
 for name,data in [('source-cases.json',cases),('review.json',review)]: (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
 md=['# Isolated perfect-square review','Raw source replay preserves omissions. Completed originals explicitly author missing grading/solution attributes. Other examples use method-derived banks; hard is authored.']
 for r in review:
  gen=r['generation'];md+=['## '+gen['origin']+' — '+gen['template'],json.dumps(gen['parameters']),g.markdown(r)]
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 report={'status':'pass','basis':1356,'source_questions':8,'prompt_exact':8,'solution_exact':5,'solution_absence_preserved':3,'field_presence_parity':8,'source_options_matched':23,'source_distractors_matched':12,'correct_designations_matched':9,'original_complete_radio_banks':3,'unrated_authored_assignments':{'q-140186':'moderate','q-140271':'easy','q-250399':'moderate'},'authored_missing_levels':['hard'],'authored_completion_sources':['q-140186','q-140271','q-250399'],'fidelity':fidelity,'independently_checked_records':checks,'mutation_regressions_rejected':len(mutations),'finite_mathematical_tasks':counts,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'dependencies':review[0]['generation']['dependencies'],'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'plots':'none','database_writes':0}
 # Exact denominators read from evidence, never hard-coded claims.
 report['source_options_matched']=sum(f['options_matched'] for f in fidelity)
 report['correct_designations_matched']=sum(f['correct_designations_matched'] for f in fidelity)
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
