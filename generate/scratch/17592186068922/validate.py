"""Validate printed rational functions, complete banks, solutions and actual grading."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE))
import printed as p
spec=importlib.util.spec_from_file_location('partial_fractions',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def coefficients(prompt):
 # Read the actual response positions in the prompt, ignoring generator data.
 logs=re.findall(r'\\operatorname\{ln\}⁡\|([^|]+)\|',prompt)
 assert len(logs)==2
 return list(map(p.scalar,logs))
def check(rec):
 q=rec['question'];meta=rec['generation'];assert rec==g.generate(q[':question/difficulty'].split('/')[-1],meta['seed'],meta['template'],meta['parameters'])
 integrand,lo,hi=p.integral(q[':question/problem']);assert lo is None and hi is None
 num,den=sp.fraction(sp.cancel(integrand));poles=sp.solve(den,p.x);assert len(poles)==2
 assert sorted(map(str,poles))==sorted(meta['domains']['excluded_poles'])
 fs=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key']);kind=g.DATA[meta['template']][1]
 if kind in ('sum','coefficients'):
  factors=coefficients(q[':question/problem']);A,B=sp.symbols('A B')
  got=sp.solve(sp.Poly(sp.together(integrand-A*sp.diff(factors[0],p.x)/factors[0]-B*sp.diff(factors[1],p.x)/factors[1]).as_numer_denom()[0],p.x).all_coeffs(),[A,B]);assert set(got)=={A,B}
  targets=[sp.simplify(got[A]+got[B])] if kind=='sum' else [got[A],got[B]]
 for i,f in enumerate(fs):
  assert len(f[':answer-field/choices'])==(1 if kind=='coefficients' else 5)
  assert f[':answer-field/type']==(':answer-field.type/blank' if kind=='coefficients' else ':answer-field.type/radio')
  bank=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];matches=[]
  for j,value in enumerate(bank):
   valid=sp.cancel(sp.diff(value,p.x)-integrand)==0 if kind=='logs' else sp.simplify(value-targets[i])==0
   matches.append(valid);assert valid==(f[':answer-field/choices'][j][':answer/id']==f[':answer-field/correct'][1])
   for previous in bank[:j]:assert (sp.cancel(sp.diff(value-previous,p.x))!=0 if kind=='logs' else sp.simplify(value-previous)!=0)
  assert sum(matches)==1
  if kind=='coefficients':assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 # Independently check each rendered final primitive on its real pole-free intervals.
 logs=re.findall(r'([^\n]*?\\operatorname\{ln\}⁡\|[^\n]*?\+C)',q[':question/worked-solution'])
 assert logs
 final=logs[-1].split('&=')[-1].split('& =')[-1].strip()
 # Source rows may begin with an equals sign or include earlier equations.
 if '=' in final:final=final.rsplit('=',1)[1].strip()
 assert sp.cancel(sp.diff(p.scalar(final),p.x)-integrand)==0,(meta['template'],final)
 if meta['parameters']['k']>1:
  sol=q[':question/worked-solution'];first=re.search(r'\$\$\n(.*?)\n\$\$',sol,re.S)[1];left,right=first.rstrip('.').split('=');assert sp.expand(p.scalar(left)-p.scalar(right))==0
  A,B=sp.symbols('A B');lines=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
  # Partial fraction decomposition and multiplied identity are independently
  # reconstructed from printed equations, then checked at each pole.
  decomp=lines[1].rstrip('.');lhs,rhs=decomp.split('=');identity=lines[2].rstrip('.');il,ir=identity.split('=')
  rp=sp.solve(den,p.x);eq=sp.Poly(sp.expand(p.scalar(il)-p.scalar(ir)),p.x).all_coeffs();solved=sp.solve(eq,[A,B]);assert set(solved)=={A,B}
  assert sp.cancel((p.scalar(lhs)-p.scalar(rhs)).subs(solved))==0
  assert sp.cancel(p.scalar(lhs)-integrand)==0
  for j,symbol,root in [(3,B,rp[0]),(4,A,rp[1])]:
   line=lines[j].rstrip('.');parts=line.split(r'\qquad');assert len(parts)==2
   l,r=parts[0].rstrip(',').split('=');v=p.scalar(r).subs(solved);assert sp.simplify(p.scalar(l)-v)==0
   l,r=parts[1].split('=');assert sp.simplify(p.scalar(l).subs(solved)-p.scalar(r))==0
  rendered_integral=re.search(r'\\begin\{aligned\}(.*?)&=',sol,re.S)[1]
  assert sp.cancel(p.integral(rendered_integral)[0]-integrand)==0
  split=sol.split('&=',1)[1].split(r'\\',1)[0].replace(r'\int','').replace(r'\text{d}x','')
  assert sp.cancel(p.scalar(split)-integrand)==0
 assert fingerprint(q)==meta['mathematical_fingerprint']
 return rec

def native(label,rec):
 checks=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete selected bank option grading'} for a in f[':answer-field/choices'])
  else:
   c=f[':answer-field/choices'][0][':answer/value'];value=p.scalar(c)
   for v,e,purpose in [(c,'accepted','canonical LaTeX'),(str(value),'accepted','equivalent exact rational'),('('+c+')+0','accepted','equivalent zero offset'),('('+c+')+1','rejected','incorrect offset'),('-('+c+')','rejected','incorrect sign')]:checks.append({'field_index':i,'submitted':v,'expected':e,'purpose':purpose})
 return {'label':label,'record':rec,'checks':checks}
def main():
 replay=[];inputs=[];review=[];seen=set();counts={};matched=0;distractors=0
 for t,info in g.DATA.items():
  old=g.sources()[t];r=check(g.generate(info[0],0,t,{'k':1}));q=r['question'];assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  for f,of in zip(q[':question/answer-fields'],sorted(old[':question/answer-fields'],key=lambda f:f[':answer-field/key'])):
   assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident']
   assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
   correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct[':answer/value']==of[':answer-field/correct'][':answer/value']
   matched+=len(f[':answer-field/choices']);distractors+=len(f[':answer-field/choices'])-1
  replay.append({'source':t,'profile':t,'complete_bank_matched':True,'missing_extra':[],'prompt_solution_fields_exact':True});inputs.append(native('source '+t,r));review.append({'label':'source '+t,'record':r})
 for level in ('easy','moderate'):
  count=0
  for t,params in g.candidates(level):
   r=check(g.generate(level,1982,t,params));assert g.generate(level,999,t,params)['question']==r['question'];fp=fingerprint(r['question']);assert fp not in seen;seen.add(fp);count+=1;inputs.append(native(t+' '+str(params),r))
  counts[level]=count
 for level,t,k in [('hard','q-49903',2),('easy','q-49903',0),('easy','q-49903',10),('easy','q-49903',2.5),('moderate','q-49903',2)]:
  try:g.generate(level,0,t,{'k':k})
  except ValueError:pass
  else:raise AssertionError('invalid boundary accepted')
 for t,info in g.DATA.items():review.append({'label':'variant '+t,'record':check(g.generate(info[0],1982,t,{'k':2}))})
 previews=g.batch('easy',8,1982)+g.batch('moderate',8,1982);save('previews.json',previews);save('review.json',review);(HERE/'review.md').write_text('\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review)+'\n')
 save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('source-replay.json',{'passed':True,'source_results':replay,'complete_banks_matched':10,'complete_banks_total_supported':10,'matched_values':matched,'total_values_supported':matched,'matched_distractors':distractors,'total_distractors_supported':distractors,'excluded_sources':['q-49904','q-128339'],'fidelity':'Ten exact prompts/solutions, field layouts and complete banks. Variants use explicit numerator/bank transport and preserve factor/decompose/eliminate/integrate/answer sequence; algebra layout simplified.'})
 save('validation.json',{'passed':True,'exhaustive_distinct_instances':len(seen),'counts':counts,'printed_math':'Independent prompt rational function, coefficient matching, every option, distinctness modulo C, final printed primitives, factor/decomposition/elimination equations; domain poles','native_grading':'Every source and bounded variant, all radio choices and equivalent/wrong entries for every blank field','hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'validate.py',HERE/'printed.py',HERE/'check-engine.rs',HERE/'check-engine',HERE/'engine-build.json',*[ROOT/p for p in json.loads((HERE/'engine-build.json').read_text())['hashes']]]}})
 save('capabilities.json',{'supported_levels':['easy','moderate'],'bounded_distinct_tasks':counts,'policy':'k=2..9 positive integer numerator scaling; original replay k=1. Denominator fixed, every complete source bank transported by k. Genuine changed integrands, deduplicated by rational function; seed/UUID/order excluded. Finite policy intentionally preserves observed mathematical workload.','exceptions':[{'difficulty':'hard','status':'unsupported','unfilled_reserve':5,'evidence':'Twelve source practice questions at basis '+str(json.loads((HERE/'basis.json').read_text())['basis'])+': three easy, eight moderate (one underdefined improper-integral question excluded), one corrupt unrated bank. No hard workload/template/bank evidence. Implementation supports observed easy/moderate workload only; new evidence reopens classification.'}],'excluded_source_questions':{'q-49904':'Corrupt determinant/ln answer text, absent correct marker and solution, unrated; no complete faithful bank can be validated.','q-128339':'Prompt never defines f(x); solution splits a convergent improper integral into separately divergent integrals. Excluded without altering source.'},'unsupported_levels_filled':False})
 print('Validated',counts)
if __name__=='__main__':main()
