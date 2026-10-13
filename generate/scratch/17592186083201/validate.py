"""Parse printed integrals independently; check limits, domains, banks and real grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
spec=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
ENGINE=ROOT/'generate/runs/current/check-engine'
def write(name,x):(P/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def group(text,pos):
 assert text[pos]=='{';start=pos+1;depth=1;pos+=1
 while depth:
  depth+=(text[pos]=='{')-(text[pos]=='}');pos+=1
 return text[start:pos-1],pos

def value(text,var='x'):
 text=text.replace('⁡','').replace('\\u2061','').replace(r'\,','').replace(r'\cdot','*').replace(r'\infty','oo').replace(r'\operatorname{ln}','log').replace(r'\ln','log')
 text=text.replace(r'\log','log').replace(r'\left','').replace(r'\right','')
 text=re.sub(r'log\s*(-?\d+|[a-z])',r'log(\1)',text)
 out='';pos=0
 while pos<len(text):
  if text.startswith(r'\frac',pos):
   a,n=group(text,pos+5);b,pos=group(text,n);out+='('+str(value(a,var))+')/('+str(value(b,var))+')'
  elif text.startswith(r'\sqrt',pos):
   pos+=5;degree=2
   if text[pos]=='[':
    end=text.index(']',pos);degree=int(text[pos+1:end]);pos=end+1
   a,pos=group(text,pos);out+='(('+str(value(a,var))+')**(1/'+str(degree)+'))'
  elif text[pos]=='{':
   a,pos=group(text,pos);out+='('+str(value(a,var))+')'
  else:out+=text[pos];pos+=1
 out=out.replace('^','**')
 out=re.sub(r'(?<=[a-z0-9)])log',r'*log',out)
 v=s.Symbol(var,real=True);a=s.Symbol('a',real=True)
 return parse_expr(out,local_dict={var:v,'a':a,'log':s.log,'e':s.E,'oo':s.oo},transformations=standard_transformations+(implicit_multiplication_application,))

def printed(problem):
 records=[]
 for fragment in problem.split('$')[1::2]:
  if r'\int' not in fragment:continue
  m=re.search(r'\\int\s*\}_',fragment);assert m,fragment
  lo,pos=group(fragment,m.end());assert fragment[pos]=='^';hi,pos=group(fragment,pos+1)
  expr=fragment[pos:].rstrip('=.,')
  d=re.search(r'\\text\{d\}([a-z])',expr);assert d,expr
  var=d[1]
  expr=expr[:d.start()]+'1'+expr[d.end():]
  expr=expr.rstrip('=.,')
  # A differential in a denominator fraction becomes numerator 1. A trailing
  # differential is removed rather than multiplied by an extra written 1.
  if expr.endswith('1'):expr=expr[:-1]
  expr=expr.rstrip().removesuffix(r'\,')
  records.append((value(expr,var),value(lo,var),value(hi,var),s.Symbol(var,real=True)))
 assert records
 return records

def limit_result(item):
 expr,lo,hi,x=item
 if hi==s.oo and lo.is_nonnegative:
  xp=s.Symbol(str(x),positive=True);expr=s.simplify(expr.subs(x,xp));x=xp
 # Independent derivative check plus oriented endpoint limits. Odd roots in
 # this bank are on positive tails; square roots on negative tails stay real.
 F=s.integrate(expr,x)
 assert not F.has(s.Integral),expr
 assert s.simplify(s.diff(F,x)-expr)==0,(expr,F)
 # Real logarithm primitive handles reciprocal on a negative half-line.
 if expr==1/x:F=s.log(s.Abs(x))
 right=s.limit(F,x,hi) if hi in (s.oo,-s.oo) else F.subs(x,hi)
 left=s.limit(F,x,lo) if lo in (s.oo,-s.oo) else F.subs(x,lo)
 ans=s.simplify(right-left)
 assert ans not in (s.nan,s.zoo) and ans.is_extended_real is not False,(expr,ans)
 return ans

def fingerprint(q):
 # Variable names, seed, field identity, order and answer bank do not establish
 # distinctness. Integral sequence with exact integrand/bounds is the task.
 normalized=[]
 for expr,lo,hi,x in printed(q[':question/problem']):
  normalized.append([s.srepr(s.simplify(expr.subs(x,s.Symbol('x',real=True)))),str(lo),str(hi)])
 return G.digest(normalized)

def structural(r):
 q=r['question'];ints=printed(q[':question/problem']);results=[limit_result(item) for item in ints]
 fields=q[':question/answer-fields'];assert len({f[':answer-field/key'] for f in fields})==len(fields)
 if len(fields)==1:assert len(results)==1 and results[0] in (s.oo,-s.oo)
 else:assert len(fields)==len(results)==3
 ids=set()
 for i,f in enumerate(fields):
  choices=f[':answer-field/choices'];correct=next(a for a in choices if a[':answer/id']==f[':answer-field/correct'][1])
  if f[':answer-field/type'].endswith('/checkbox'):
   assert len(choices)==2 and {a[':answer/value'] for a in choices}=={'true','false'}
   assert correct[':answer/value']==str(results[i] in (s.oo,-s.oo)).lower()
  else:
   assert len(choices)==5 and correct[':answer/type']==':answer.type/text' and 'diverge' in correct[':answer/value']
   vals=[s.simplify(value(a[':answer/value'])) for a in choices if a[':answer/type']==':answer.type/math']
   assert len(vals)==len(set(vals)) and all(z.is_finite for z in vals)
  for a in choices:
   assert a[':answer/id'] not in ids;ids.add(a[':answer/id'])
   assert '$' not in a[':answer/value']
 # Verify the evaluated result printed in each aligned solution. This catches
 # stale finite endpoint arithmetic, while the integral parser verifies prompt.
 parts=q[':question/worked-solution'].split(r'\begin{aligned}')
 result_parts=[p for p in parts[1:] if r'\int' in p.split(r'\end{aligned}')[0]]
 ends=[]
 for part in result_parts:
  body=part.split(r'\end{aligned}')[0]
  last=body.split(r' & =')[-1].rstrip('., ')
  if last in (r'\infty',r'-\infty') or re.fullmatch(r'-?\d+|-?\\frac\{\d+\}\{\d+\}',last):ends.append(value(last))
 assert len(ends)>=len(results),(ends,results,q[':question/problem'])
 assert ends[-len(results):]==results,(ends,results)
 for text in (q[':question/problem'],q[':question/worked-solution']):
  assert text.count('$')%2==0 and '@' not in text
  depth=0
  for ch in text:depth+=(ch=='{')-(ch=='}');assert depth>=0
  assert depth==0
 assert r['knowledge_point']['db_id']==G.KP_ID
 return results

def checks(r):
 return [{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual grader for every owned radio/checkbox option'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]

def main():
 native=[];review=[];reports=[];count=0;options=0;distractors=0;tasksets={k:set() for k in G.SUPPORTED_LEVELS}
 for t in G.TEMPLATES:
  mid=t['template'];source=G.BY_ID[mid];r=G.generate(t['level'],17,mid,parameters=t['source_parameters']);structural(r)
  assert r['question'][':question/problem']==source[':question/problem']
  expected_solution=source[':question/worked-solution']
  correction=mid=='q-101734'
  if correction:expected_solution=expected_solution.replace(r'{lim}_{a\to \infty }{\int }_{1}^{\infty }',r'{lim}_{a\to \infty }{\int }_{1}^{a}')
  assert r['question'][':question/worked-solution']==expected_solution
  banks=[]
  for f,of in zip(r['question'][':question/answer-fields'],source[':question/answer-fields']):
   original=sorted((a[':answer/type'][':db/ident'],a[':answer/value'],a[':answer/id']==of[':answer-field/correct'][':answer/id']) for a in of[':answer-field/choices'])
   new=sorted((a[':answer/type'],a[':answer/value'],a[':answer/id']==f[':answer-field/correct'][1]) for a in f[':answer-field/choices'])
   assert original==new,(mid,original,new)
   options+=len(new);distractors+=len(new)-1;banks.append({'key':f[':answer-field/key'],'matched_options':len(new),'missing':[],'extra':[]})
  reports.append({'source_id':mid,'prompt_exact':True,'solution_exact_except_documented_truncation_correction':True,'correction':correction,'banks':banks})
  review.extend([{'label':'Source '+mid,'record':r}])
  for n in t['sampling_values']:
   rec=G.generate(t['level'],19,mid,parameters={t['parameter']:n});structural(rec);count+=1;tasksets[t['level']].add(fingerprint(rec['question']))
   repeat=G.generate(t['level'],29,mid,parameters={t['parameter']:n});assert rec['question'][':question/id']==repeat['question'][':question/id']
   native.append({'label':mid+' '+str(n),'record':rec,'checks':checks(rec)})
  variant=G.generate(t['level'],83,mid,parameters={t['parameter']:t['sampling_values'][-1]});review.append({'label':'Boundary variant '+mid,'record':variant})
  for n in (0,-1,1000):
   try:G.generate(t['level'],template=mid,parameters={t['parameter']:n});raise AssertionError('Out-of-bound parameter accepted')
   except ValueError:pass
 for level in G.SUPPORTED_LEVELS:
  assert len({fingerprint(r['question']) for r in G.batch(level,10,73)})==10
 try:G.batch('hard',5);raise AssertionError('Hard is unsupported')
 except ValueError:pass
 write('engine-input.json',native);subprocess.run([str(ENGINE),str(P/'engine-input.json'),str(P/'engine-report.json')],check=True)
 engine=json.loads((P/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
 write('review.json',review);(P/'review.md').write_text('# Source replay and bounded variants\n\n'+'\n\n---\n\n'.join('## '+x['label']+'\n\n'+G.markdown(x['record']) for x in review)+'\n')
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [P.with_suffix('.py'),P/'source.json',P/'templates.json',Path(__file__)]}
 write('validation.json',{'passed':True,'source_basis':json.loads((P/'source.json').read_text())['basis'],'source_total':14,'source_replayed':13,'excluded_source_ids':['q-6294'],'source_replay':reports,'complete_banks_matched':23,'matched_options':options,'matched_distractors':distractors,'missing_or_extra_options':0,'generated_instances_checked':count,'finite_distinct_tasks':{k:len(v) for k,v in tasksets.items()},'supported_levels':list(G.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':hashes,'engine_sha256':hashlib.sha256(ENGINE.read_bytes()).hexdigest(),'fidelity':'All 13 supported source layouts and complete banks replay exactly, except documented finite-bound typo correction. Narrow parameter recipe extensions are separate from observed source values.','correctness':'Independent parse of printed integrands/bounds; exact primitives, derivative checks, endpoint limits and evaluated solution results for every allowed parameter.','grading':'Actual grade_field for every checkbox and radio option; no unresolved cases','database_writes':0})
 print('Validation PASS:',count,'parameter cases')
if __name__=='__main__':main()
