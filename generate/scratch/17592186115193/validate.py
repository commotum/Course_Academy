"""Independent calculus/choice checks, full observed-bank replay and native grading."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('slope_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x',real=True)
def parse(text):
 text=re.sub(r'\\operatorname\{([^{}]+)\}',r'\1',text).replace('⁡','').replace(r'\pi','pi').replace(r'\cdot','*')
 while r'\frac' in text or r'\sqrt' in text:
  new=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',text)
  new=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',new)
  assert new!=text,(text,new);text=new
 text=text.replace('{','(').replace('}',')')
 return parse_expr(text,local_dict={'pi':sp.pi,'e':sp.E,'sin':sp.sin,'cos':sp.cos,'sec':sp.sec,'csc':sp.csc,'tan':sp.tan,'cot':sp.cot,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def fingerprint(q):return g.fingerprint(q[':question/problem'])
def function(sid,n):
 return {'q-1886':(n*sp.cos(x)-sp.sec(x)+1/x,sp.sqrt(3)), 'q-1905':(2*x-sp.sqrt(2)*sp.sec(x),sp.pi/4),'q-104442':(sp.sec(x)/sp.sqrt(3)+3*x*x/sp.pi,sp.pi/3),'q-1904':(-x*x+n*sp.csc(x),sp.pi/6),'q-340630':(sp.exp(x)+3*sp.sec(x),sp.pi),'q-340660':(n*x/sp.sec(x),0),'q-340642':(sp.csc(x)*sp.cot(x),sp.pi/2),'q-70874':(sp.log(x)+3*sp.csc(x),sp.pi/3)}[sid]
def check(r):
 m=r['generation'];sid=m['template'];n=m['parameter'];q=r['question'];assert r==g.generate(g.PROFILES[sid]['level'],m['seed'],sid,n)
 f,point=function(sid,n);target=sp.simplify(sp.diff(f,x).subs(x,point));assert target.is_finite
 fields=q[':question/answer-fields'];assert len(fields)==1;field=fields[0];bank=field[':answer-field/choices'];values=[parse(a[':answer/value']) for a in bank]
 correct=[i for i,a in enumerate(bank) if a[':answer/id']==field[':answer-field/correct'][1]];assert len(correct)==1
 assert sp.simplify(values[correct[0]]-target)==0,(sid,n,target,values)
 for i in range(len(values)):
  for j in range(i):assert abs(complex(sp.N(values[i]-values[j],35)))>1e-7,(sid,n,'bank collision')
 for i,v in enumerate(values):
  if i!=correct[0]:assert abs(complex(sp.N(v-target,35)))>1e-7
 # Independently read parameter from the displayed function and final solution.
 problem=q[':question/problem'];sol=q[':question/worked-solution']
 if sid=='q-1886':
  assert int(re.search(r'f\(x\)=(\d+)\\operatorname\{cos\}',problem)[1])==n
  final=re.findall(r' & =([^&]+?)\\end\{aligned\}',sol)[-1];assert sp.simplify(parse(final.removesuffix('.'))-target)==0
 elif sid=='q-1904':
  assert int(re.search(r'\+(\d+)csc',problem)[1])==n
  final=re.findall(r' & =([^&]+?)\\end\{aligned\}',sol)[-1];assert sp.simplify(parse(final.removesuffix('.'))-target)==0
 elif sid=='q-340660':
  assert int(re.search(r'\\frac\{(\d+)x\}',problem)[1])==n
  final=re.findall(r' & =(\d+)\\end\{aligned\}',sol)[-1];assert int(final)==target
 assert ':question/math-academy-id' not in q and fingerprint(q)==m['mathematical_fingerprint']
 assert len({a[':answer/id'] for a in bank})==len(bank)
 return r

def native(label,r):
 field=r['question'][':question/answer-fields'][0]
 if field[':answer-field/type']==':answer-field.type/radio':
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'Actual radio ID grading'} for a in field[':answer-field/choices']]
 else:
  value=field[':answer-field/choices'][0][':answer/value'];v=parse(value)
  checks=[{'submitted':value,'expected':'accepted','purpose':'Canonical blank'}, {'submitted':'('+value+')','expected':'accepted','purpose':'Equivalent grouping'}, {'submitted':sp.latex(v+1),'expected':'rejected','purpose':'Wrong value'}]
  if v.is_Integer:checks.append({'submitted':r'\frac{'+str(2*v)+'}{2}','expected':'accepted','purpose':'Equivalent fraction'})
 return {'label':label,'record':r,'checks':checks}
def main():
 rows=[];replay=[];review=[]
 for sid,t in g.PROFILES.items():
  r=check(g.generate(t['level'],0,sid,t['observed']));old=g.SOURCES[sid];q=r['question'];of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices'])
  assert next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  replay.append({'source':sid,'profile':sid+'-observed-bank','matched_choices':len(of[':answer-field/choices']),'matched_distractors':len(of[':answer-field/choices'])-1,'complete_bank_match':True,'prompt_exact':True,'solution_exact':True})
  review.append('## '+sid+'\n\nOriginal and exact replay\n\n'+g.markdown(r)+'\n\nBound variant\n\n'+g.markdown(check(g.generate(t['level'],0,sid,t['domain'][-1]))))
  for n in t['domain']:
   r=check(g.generate(t['level'],42,sid,n));assert r['question']==g.generate(t['level'],999,sid,n)['question'];rows.append(r)
 save('source-replay.json',{'passed':True,'complete_banks_matched':len(replay),'complete_banks_total':len(replay),'distractors_matched':sum(z['matched_distractors'] for z in replay),'distractors_total':sum(z['matched_distractors'] for z in replay),'profiles':replay,'excluded_incomplete_sources':['q-104437']})
 save('native-input.json',[native(str(i),r) for i,r in enumerate(rows)]);subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 report=json.loads((HERE/'native-grading.json').read_text());assert report['documented_unresolved_checks']==0
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n');save('previews.json',g.batch('moderate',5,1939))
 save('validation.json',{'passed':True,'supported_levels':['easy','moderate'],'exhaustive_instances':len(rows),'finite_tasks_by_level':{l:sum(len(t['domain']) for t in g.PROFILES.values() if t['level']==l) for l in ['easy','moderate']},'full_source_bank_replay':True,'grading':{k:report[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',HERE/'source.edn',HERE/'capabilities.json']}})
 print('Validated',len(rows),'instances; eight complete banks and all native grading checks passed.')
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
if __name__=='__main__':main()
