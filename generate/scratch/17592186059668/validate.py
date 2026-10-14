"""Independent rendered mathematics, full source-bank replay and native grading."""
import importlib.util, json, re, sys, subprocess, itertools
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
a,b,x=sp.symbols('a b x',real=True)

def expression(t):
 t=t.replace(' ','').rstrip('.').replace('{)}',')').replace(r'\left','').replace(r'\right','')
 t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
 t=t.replace('{','(').replace('}',')').replace('^','**').replace(r'\cdot','*')
 t=re.sub(r'\|([^|]+)\|',r'Abs(\1)',t)
 return parse_expr(t,local_dict={'a':a,'b':b,'x':x,'Abs':sp.Abs,'f':sp.Function('f')},transformations=standard_transformations+(implicit_multiplication_application,))
def vector(t):
 t=t.strip().rstrip('.').strip();assert t.startswith('(') and t.endswith(')'),t
 return tuple(expression(z) for z in t[1:-1].split(','))
def parsed_task(q):
 text=q[':question/problem'];parts=re.findall(r'\$([^$]+)\$',text)
 A,B=vector(parts[0]);base=parts[1].removeprefix('y=').rstrip('.');target=parts[2].removeprefix('y=').rstrip('?')
 T=expression(target);F=expression(base)
 if F.has(sp.Function('f')):
  if T.has(-sp.Function('f')(x)) or T.coeff(sp.Function('f')(x))==-1:
   t='numeric_reflection';p={'a':int(A),'b':int(B),'k':int(T+sp.Function('f')(x))}
  else:
   atom=next(iter(T.atoms(sp.Function)));t='numeric_shift';p={'a':int(A),'b':int(B),'h':int(x-atom.args[0]),'k':int(T-atom)}
 else:
  t='quadratic' if F==x**2 else 'exponential' if F==2**x else 'absolute' if F==sp.Abs(x) else 'horizontal_scale' if F==3**x else None
  assert t,t
  if t=='quadratic':h=-sp.expand(T).coeff(x)/2;k=sp.expand(T).subs(x,h)
  elif t=='absolute':atom=next(iter(T.atoms(sp.Abs)));h=sp.simplify(x-atom.args[0]);k=T-atom
  else:
   atom=next(z for z in T.atoms(sp.Pow) if z.base in [2,3]);exponent=atom.exp;k=T-atom
   if t=='exponential':h=sp.simplify(x-exponent)
   else:s=1/exponent.coeff(x)
  p={'s':int(s),'k':int(k)} if t=='horizontal_scale' else {'h':int(h),'k':int(k)}
 return t,p,(A,B,F,T)
def fingerprint(q):
 if not q.get(':question/answer-fields'):
  return g.digest({'unsupported_source_prompt':q[':question/problem']})
 try:t,p,_=parsed_task(q);return g.mathematical_fingerprint(t,p)
 except (AssertionError,StopIteration,ValueError,TypeError):
  # Incomplete templates are retained as source evidence, never generated here.
  return g.digest({'unsupported_source_prompt':q[':question/problem']})

def check(rec):
 q=rec['question'];meta=rec['generation'];t,p,objects=parsed_task(q);A,B,F,T=objects
 assert t==meta['template'] and p==meta['parameters'];assert fingerprint(q)==meta['mathematical_fingerprint']
 f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 answers=[(z[':answer/id'],vector(z[':answer/value'])) for z in f[':answer-field/choices']]
 assert len(answers)==5 and len({str(z[1]) for z in answers})==5 and sum(z[0]==correct for z in answers)==1
 # Use the given relation, not the generator's answer computation. For arbitrary f,
 # a free slope gives a counterexample for every unsupported x-coordinate.
 m=sp.Symbol('m',real=True)
 def residual(X,Y):
  if t.startswith('numeric'):
   transformed=T.replace(lambda z:z.func==sp.Function('f'),lambda z:B+m*(z.args[0]-A))
   return sp.simplify(Y-transformed.subs(x,X))
  return sp.simplify((Y-T.subs(x,X)).subs(b,F.subs(x,a)))
 right=next(z for z in answers if z[0]==correct)[1]
 assert residual(*right)==0,(t,p,right,residual(*right))
 for aid,point in answers:
  if aid==correct:continue
  r=residual(*point)
  assert r!=0,'extra necessarily correct option'
  # Concrete real-domain witness; rejects even tempting special-point coincidences.
  assert any(sp.simplify(r.subs({a:z,m:7}))!=0 for z in [1,2,3,4,5]),r
 if rec.get('source_evidence'):return True
 solution=q[':question/worked-solution']
 for value in [q[':question/problem'].split('$')[-2].removeprefix('y=').rstrip('?'),g.pair(*right)]:assert value in solution
 stages=re.findall(r'\$\$\s*(\([^\n]+\))\.\s*\$\$',solution)
 assert len(stages)==2;X,Y=right
 expected_intermediate=(X,-B) if t=='numeric_reflection' else (X,B)
 assert vector(stages[0])==expected_intermediate and vector(stages[1])==right
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)[1]
 expressions=[z.strip().removeprefix('y').strip().lstrip('&=').strip().rstrip('.') for z in block.split(r'\\')]
 parsed=[expression(z) for z in expressions]
 # Evaluate the printed substitution rows from the same given relation.
 def reduce(z):
  if t.startswith('numeric'):return sp.simplify(z.replace(lambda n:n.func==sp.Function('f'),lambda n:B+m*(n.args[0]-A)))
  return sp.simplify(z.subs(b,F.subs(x,a)))
 assert all(sp.simplify(reduce(z)-reduce(parsed[-1]))==0 for z in parsed)
 assert sp.simplify(parsed[-1]-Y)==0
 assert ':question/math-academy-id' not in q
 return True

def engine_item(rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':z[':answer/id'],'expected':'accepted' if z[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual owned radio ID selection'} for z in f[':answer-field/choices']]}

def main():
 sources={q[':question/math-academy-id']:q for q in g.SOURCE['record'][':knowledge-point/questions']}
 reports=[];records=[];banks=[]
 for t,(mid,level,p) in g.CASES.items():
  rec=g.generate(level,0,t,p,t);check(rec);records.append(rec)
  source=sources[mid]; f=source[':question/answer-fields'][0];new=rec['question'][':question/answer-fields'][0]
  old_values=[vector(z[':answer/value']) for z in f[':answer-field/choices']];new_values=[vector(z[':answer/value']) for z in new[':answer-field/choices']]
  assert len(old_values)==len(new_values)==5 and set(old_values)==set(new_values),(t,old_values,new_values)
  assert vector(f[':answer-field/correct'][':answer/value'])==next(vector(z[':answer/value']) for z in new[':answer-field/choices'] if z[':answer/id']==new[':answer-field/correct'][1])
  banks.append({'template':t,'source':mid,'matched_options':5,'total_options':5,'matched_distractors':4,'total_distractors':4,'correct_designation':True})
  if t=='quadratic':
   assert '^{2}+1' in source[':question/worked-solution'];assert '^{2}+2' in rec['question'][':question/worked-solution']
  variations=[]; rejected=0
  for seed in range(40):
   r=g.generate(level,seed,t);check(r);records.append(r);variations.append(r['generation']['parameters'])
  # Signed domain corners for each complete profile; invalid banks must be rejected.
  keys=list(p);bounds=[([2,5] if k=='s' else [-8,-1,1,8]) for k in keys]
  for values in itertools.product(*bounds):
   pp=dict(zip(keys,values))
   try:r=g.generate(level,999,t,pp)
   except (AssertionError,ValueError):rejected+=1;continue
   check(r);records.append(r)
  # Change every declared slot, holding the other slots fixed: stale references/key test.
  slot_checks={}
  for key in keys:
   for val in ([2,3,4,5] if key=='s' else [-8,-3,-1,1,3,8]):
    pp=dict(p);pp[key]=val
    try:r=g.generate(level,0,t,pp)
    except (AssertionError,ValueError):continue
    check(r)
    assert r['question']==g.generate(level,100,t,pp)['question'],'seed changes identity/content'
    records.append(r);slot_checks.setdefault(key,[]).append(val)
   assert len(set(slot_checks[key]))>=2
  reports.append({'template':t,'samples':40,'slot_coverage':{k:sorted({z[k] for z in variations}) for k in keys},'held_other_slots_fixed':slot_checks,'invalid_boundary_banks_rejected':rejected})
 # Grader binary is the existing generic application fixture, read-only and hash recorded.
 binary=ROOT/'generate/scratch/17592186059711/check-engine'
 (HERE/'engine-input.json').write_text(json.dumps([engine_item(r) for r in records],indent=2))
 subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 engine=json.loads((HERE/'engine-report.json').read_text());assert engine['accepted_checks']==len(records) and engine['rejected_checks']==4*len(records) and engine['documented_unresolved_checks']==0
 report={'status':'passed','source_basis':g.SOURCE['basis'],'mathematics':'independent rendered prompt/options and every aligned solution row checked','gradable_instances':len(records),'full_source_banks':banks,'complete_banks_matched':6,'complete_banks_total':6,'matched_distractors':24,'total_distractors':24,'fidelity':'Complete bank algebra and two-method solution backbone preserved; notation normalized; q-121220 opening +1 typo corrected to +2 only in new content.','templates':reports,'unsupported_levels':['hard'],'source_questions_without_fields':[q[':question/math-academy-id'] for q in sources.values() if not q.get(':question/answer-fields')],'plot_assets':[],'actual_grader':'course_academy_engine::learning::grade_field','grader_binary':str(binary.relative_to(ROOT))}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 examples=[g.generate(level,42,t) for t,(_,level,_) in g.CASES.items()]
 (HERE/'review.json').write_text(json.dumps(examples,indent=2)+'\n')
 (HERE/'review.md').write_text('\n\n---\n\n'.join('Source '+mid+'\n\n'+sources[mid][':question/problem']+'\n\n'+'\n'.join('- $'+z[':answer/value']+'$'+(' (correct)' if z[':answer/id']==sources[mid][':question/answer-fields'][0][':answer-field/correct'][':answer/id'] else '') for z in sources[mid][':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+sources[mid][':question/worked-solution']+'\n\nGenerated variant\n\n'+g.markdown(r) for r,(t,(mid,level,p)) in zip(examples,g.CASES.items()))+'\n')
 print(json.dumps({'status':'passed','instances':len(records),'complete_banks':'6/6','distractors':'24/24'}))
if __name__=='__main__':main()
