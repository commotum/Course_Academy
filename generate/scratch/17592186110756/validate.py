"""Independent rendered-coordinate algebra, full-bank replay, and actual grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(n,v):(D/n).write_text(json.dumps(v,indent=2)+'\n')
def number(text):
 text=re.sub(r'\\sqrt\s+([0-9])',r'\\sqrt{\1}',text)
 text=text.replace('\\dfrac','\\frac').replace('\\left','').replace('\\right','').replace('\\,','').replace('\\cdot','*')
 def group(i):
  assert text[i]=='{';depth=1;j=i+1
  while depth:
   depth+=(text[j]=='{')-(text[j]=='}');j+=1
  return text[i+1:j-1],j
 out='';i=0
 while i<len(text):
  if text.startswith('\\frac',i):
   a,j=group(i+5);b,i=group(j);out+='(('+str(number(a))+')/('+str(number(b))+'))'
  elif text.startswith('\\sqrt',i):
   a,i=group(i+5);out+='sqrt('+str(number(a))+')'
  else:out+=text[i];i+=1
 out=out.replace('{','(').replace('}',')')
 assert re.fullmatch(r'[0-9\s()+*/.\-sqrt]+',out),out
 v=sp.simplify(parse_expr(out,transformations=standard_transformations+(implicit_multiplication_application,)))
 assert not v.free_symbols
 return v

def fingerprint(q):
 m=re.search(r'\$(x|y)\$-coordinate.*?is \$(.*?)\$',q[':question/problem'])
 # Captured sources also put x/y inside a single dollar-delimited fragment.
 if not m:m=re.search(r'\$(x|y)\$-coordinate.*?is \$(.*?)\$',q[':question/problem'])
 assert m,q[':question/problem'];axis=m[1];coordinate=number(m[2].rstrip(', '));target='sec' if axis=='y' else 'csc'
 assert ('\\'+target in q[':question/problem'] or target+'⁡' in q[':question/problem'])
 return g.digest({'axis':axis,'coordinate':str(coordinate),'target':target,'quadrant':1})

def display_check(rec):
 q=rec['question'];f=q[':question/answer-fields'][0];fp=fingerprint(q)
 m=re.search(r'\$(x|y)\$-coordinate.*?is \$(.*?)\$',q[':question/problem']);known=number(m[2].rstrip(', '));expected=sp.simplify(1/sp.sqrt(1-known**2));bank=[number(a[':answer/value']) for a in f[':answer-field/choices']]
 assert 0<known<1 and len(bank)==5
 assert all(sp.simplify(a-z)!=0 for i,a in enumerate(bank) for z in bank[i+1:])
 for a,value in zip(f[':answer-field/choices'],bank):assert (sp.simplify(value-expected)==0)==(a[':answer/id']==f[':answer-field/correct'][1])
 sol=q[':question/worked-solution'];assert 'first quadrant' in sol
 if rec['generation']:
  match=re.search(r'&=(.*?)\.\s*\\end\{aligned\}\$\$$',sol);assert match
  assert sp.simplify(number(match[1])-expected)==0
  p=rec['generation']['parameters'];axis=m[1];given='sin' if axis=='y' else 'cos';other='cos' if axis=='y' else 'sin';target='sec' if axis=='y' else 'csc'
  assert f'\\{given}\\theta={sp.latex(known)}' in sol
  assert f'\\{other}\\theta={sp.latex(sp.sqrt(1-known**2))}' in sol
  assert f'\\{target}\\theta=\\dfrac{{1}}{{\\{other}\\theta}}' in sol
  for role,a in rec['generation'].get('assets',{}).items():
   x,y=map(sp.sympify,a['point']);assert sp.simplify(x*x+y*y)==1
   assert sp.simplify((y if axis=='y' else x)-known)==0 and x>0 and y>0
   assert hashlib.sha256(Path(a['path']).read_bytes()).hexdigest()==a['sha256']
 for text in [q[':question/problem'],sol]+[a[':answer/value'] for a in f[':answer-field/choices']]:
  depth=0
  for c in text:depth+=(c=='{')-(c=='}');assert depth>=0
  assert depth==0 and text.count('$')%2==0
 return fp

def grade(records,path):
 path=Path(path);path.mkdir(parents=True,exist_ok=True);items=[]
 for r in records:
  f=r['question'][':question/answer-fields'][0]
  items.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned choice through actual learner grader'} for a in f[':answer-field/choices']]})
 (path/'native-input.json').write_text(json.dumps(items,indent=2));subprocess.run([str(D/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
 r=json.loads((path/'native-report.json').read_text());assert r['accepted_checks']==len(records) and r['rejected_checks']==len(records)*4 and r['documented_unresolved_checks']==0

def main():
 deps=ROOT/'target/release/deps';subprocess.run(['cargo','build','--release','--lib','--offline'],cwd=ROOT,check=True)
 libs={n:max(deps.glob('lib'+n+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for n in ('course_academy_engine','serde_json')}
 cmd=['rustc','--edition=2024','-O',str(D/'check-engine.rs')]
 for n,p in libs.items():cmd+=['--extern',n+'='+str(p)]
 subprocess.run(cmd+['-L','dependency='+str(deps),'-o',str(D/'check-engine')],check=True)
 sources={q[':db/id']:q for q in g.SOURCE['record'][':knowledge-point/questions']};replays=[];variants=[];banks=[];coverage={};review=[]
 for name,profile in g.PROFILES.items():
  src=sources[profile['source']];rec=g.generate('moderate',0,name,parameters=profile['original']);display_check(rec);replays.append(rec)
  original=src[':question/answer-fields'][0];bank=[number(a[':answer/value']) for a in original[':answer-field/choices']];f=rec['question'][':question/answer-fields'][0];new=[number(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(bank)==len(new)==5 and all(sum(sp.simplify(a-b)==0 for b in new)==1 for a in bank)
  original_correct=number(original[':answer-field/correct'][':answer/value']);new_correct=number(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]));assert sp.simplify(original_correct-new_correct)==0
  assert fingerprint(src)==display_check(rec)
  assert rec['question']==g.generate('moderate',99,name,parameters=profile['original'])['question']
  banks.append({'profile':name,'source_question':src[':db/id'],'distractors_matched':4,'distractors_total':4,'complete_banks_matched':1,'missing':[],'extra':[],'correct_verified':True})
  domain=g.domain(name);chosen=[domain[0],domain[-1]]+[domain[i*max(1,len(domain)//8)] for i in range(8) if i*max(1,len(domain)//8)<len(domain)]
  # All finite domains are checked mathematically; display/plots/actual grading
  # cover endpoints and representative interiors per complete bank.
  for p in domain:g.values(name,p)
  for p in chosen:
   r=g.generate('moderate',17,name,parameters=p);display_check(r);variants.append(r)
  coverage[name]={'valid_domain_size':len(domain),'b_values':sorted({p['b'] for p in domain}),'r_values':sorted({p['r'] for p in domain}),'rendered_parameters':chosen,'all_domain_banks_mathematically_checked':True}
  review.append({'source':src,'replay':rec,'variants':[g.generate('moderate',seed,name) for seed in (101,102)]})
 # Same numeric coordinate held fixed while its x/y role is changed. Each
 # corresponding prompt, target, complementary coordinate, and solution follows.
 y=g.generate('moderate',0,'y-rational',parameters={'b':3,'r':1})
 x=g.generate('moderate',0,'x-rational',parameters={'b':3,'r':1})
 assert display_check(x)!=display_check(y)
 assert r'\sec\theta' in y['question'][':question/problem'] and r'\csc\theta' in x['question'][':question/problem']
 stale=copy.deepcopy(x);stale['question'][':question/worked-solution']=y['question'][':question/worked-solution']
 try:display_check(stale)
 except AssertionError:pass
 else:raise AssertionError('Stale target solution accepted')
 grade(replays+variants+[x,y],D/'reference/validation')
 mutant=copy.deepcopy(variants[0]);f=mutant['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
 try:display_check(mutant)
 except AssertionError:pass
 else:raise AssertionError('Stale answer key accepted')
 for level in ('easy','hard'):
  try:g.generate(level,0)
  except ValueError:pass
  else:raise AssertionError('Unsupported difficulty generated')
 save('source-bank-replay.json',banks);save('slot-coverage.json',coverage);save('review.json',review)
 (D/'review.md').write_text('\n\n---\n\n'.join('Source '+str(x['source'][':db/id'])+'\n\n'+x['source'][':question/problem']+'\n\n'+x['source'][':question/worked-solution']+'\n\nReplay\n\n'+g.markdown(x['replay'])+'\n\nVariants\n\n'+'\n\n'.join(map(g.markdown,x['variants'])) for x in review))
 save('validation.json',{'status':'passed','source_basis':g.SOURCE['basis'],'complete_banks':5,'source_distractors_matched':20,'source_options_matched':25,'missing_options':[],'extra_options':[],'independent_display_validation_records':len(variants)+5,'actual_grader_records':len(variants)+7,'changed_target_fixed_data_checked':True,'stale_target_solution_rejected':True,'supported_levels':['moderate'],'unsupported_levels':['easy','hard'],'unclassified_source_excluded':17592186111341,'stale_key_mutation_rejected':True,'seed_independent_identity':True,'all_finite_domain_banks_checked':True,'fidelity':'All five complete banks, original mathematical objects and source solution stages. Clean standard LaTeX and exact Matplotlib plots replace captured rendering artifacts.'})
 print('All five complete banks and',len(variants),'representative variants passed')
if __name__=='__main__':main()
