"""Independent curl, displayed parameter, full source banks and actual grading."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('curl_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z,i,j,k=sp.symbols('x y z i j k')
def parse(text):
 text=text.replace(chr(92)*2,chr(92)).replace(r'\,','').replace(r'\text{k}','k').replace('{','(').replace('}',')')
 text=re.sub(r'(?<=[0-9)])(?=[ijk])','*',text)
 return parse_expr(text,local_dict={'x':x,'y':y,'z':z,'i':i,'j':j,'k':k,'e':sp.E},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def fingerprint(q):return g.fingerprint(q[':question/problem'])
def target(sid,p):
 fields={'q-105668':((p if isinstance(p,int) else 3)*z*z,2*y,1),'q-105672':(sp.exp(y+z),1,x*y*z),'q-131336':(x*sp.exp(y*z),y*z,sp.exp(y*z)),'q-105698':(sp.log(x+y),y*z*z,x-z),'q-131338':(x,2*y,3*z),'q-131340':(x*x,x*z,z*z),'q-131341':(2*x*y+2*z,y*y+1,x+y),'q-98894':(0,x*y*sp.exp(z),y*z*sp.exp(x))}
 P,Q,R=map(sp.sympify,fields[sid]);curl=[sp.diff(R,y)-sp.diff(Q,z),sp.diff(P,z)-sp.diff(R,x),sp.diff(Q,x)-sp.diff(P,y)]
 points={'q-105672':(2,1,-1),'q-105698':(2,-1,3),'q-131340':(p[0],-3,p[1]) if isinstance(p,list) else (-2,-3,1),'q-131341':(-3,0,-1),'q-98894':(0,2,1)}
 if sid in points:curl=[a.subs(dict(zip((x,y,z),points[sid]))) for a in curl]
 return sp.expand(sum(a*b for a,b in zip(curl,(i,j,k))))
def check(r, replay=True):
 m=r['generation'];sid=m['template'];p=m['parameter'];q=r['question'];
 if replay:assert r==g.generate(g.PROFILES[sid]['level'],m['seed'],sid,p)
 expected=target(sid,p);f=q[':question/answer-fields'][0];values=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 correct=[n for n,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]];assert len(correct)==1
 assert sp.simplify(values[correct[0]]-expected)==0,(sid,p,expected,values)
 assert len(values)==5 and len({sp.srepr(sp.expand(v)) for v in values})==5
 assert sum(sp.simplify(v-expected)==0 for v in values)==1
 problem=q[':question/problem'];sol=q[':question/worked-solution']
 if sid=='q-105668':
  assert int(re.search(r'=([0-9]+)\{z\}\^\{2\}',problem)[1])==p
  assert all(int(n)==p for n in re.findall(r'([0-9]+)\{z\}\^\{2\}',sol))
  final=re.findall(r' & =([^&]+?)\\end\{aligned\}',sol)[-1];assert sp.expand(parse(final.removesuffix('.'))-expected)==0
 if sid=='q-131340':
  point=tuple(map(int,re.search(r'point\s*\$\((-?\d+),(-?\d+),(-?\d+)\)',problem).groups()));assert point==(p[0],-3,p[1])
  assert set(re.findall(r'\((-?\d+),(-?\d+),(-?\d+)\)',sol))=={tuple(map(str,point))}
  substituted=re.search(r' & =-\((-?\d+)\)\\,i\+\((\d+)\)\\,k',sol);assert tuple(map(int,substituted.groups()))==tuple(p)
  final=re.findall(r' & =([^&]+?)\\end\{aligned\}',sol)[-1];assert sp.expand(parse(final.removesuffix('.'))-expected)==0
 assert ':question/math-academy-id' not in q and fingerprint(q)==m['mathematical_fingerprint']
 return r

def native(label,r):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Actual learner radio selection grading'} for a in f[':answer-field/choices']]}
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def main():
 rows=[];replay=[];review=[];slot_coverage={}
 for sid,t in g.PROFILES.items():
  r=check(g.generate(t['level'],0,sid,t['observed']));old=g.SOURCES[sid];q=r['question'];of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution']
  assert [a[':answer/value'] for a in of[':answer-field/choices']]==[a[':answer/value'] for a in nf[':answer-field/choices']]
  replay.append({'source':sid,'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'complete_bank_match':True,'missing_or_extra':[],'prompt_exact':True,'solution_exact':True})
  review.append('## '+sid+'\n\nOriginal / exact replay\n\n'+g.markdown(r)+'\n\nBound variant\n\n'+g.markdown(check(g.generate(t['level'],0,sid,t['domain'][-1]))))
  fps=set()
  for p in t['domain']:
   r=check(g.generate(t['level'],42,sid,p));assert r['question']==g.generate(t['level'],999,sid,p)['question'];assert fingerprint(r['question']) not in fps;fps.add(fingerprint(r['question']));rows.append(r)
  slot_coverage[sid]={'tested_parameters':t['domain'],'uncovered_parameters':[],'distinct_tasks':len(fps)}
 # Changing the target point with F fixed must change prompt, evaluation stage and key.
 a=check(g.generate('moderate',0,'q-131340',[-2,1]));b=check(g.generate('moderate',0,'q-131340',[-4,3]));assert a['question'][':question/problem']!=b['question'][':question/problem'];assert target('q-131340',[-2,1])!=target('q-131340',[-4,3])
 # Mutations must fail independent rendered-reference and key checks.
 import copy
 caught=[]
 for what in ('prompt','solution','key'):
  bad=copy.deepcopy(b)
  if what=='prompt':bad['question'][':question/problem']=a['question'][':question/problem']
  elif what=='solution':bad['question'][':question/worked-solution']=a['question'][':question/worked-solution']
  else:bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']=a['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
  try:check(bad, replay=False)
  except AssertionError:caught.append(what)
 assert len(caught)==3
 save('source-replay.json',{'passed':True,'complete_banks_matched':8,'complete_banks_total':8,'distractors_matched':32,'distractors_total':32,'profiles':replay,'excluded_incomplete_sources':['q-41883','q-41899','q-168621']})
 save('native-input.json',[native(str(n),r) for n,r in enumerate(rows)])
 subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 report=json.loads((HERE/'native-grading.json').read_text());assert report['documented_unresolved_checks']==0
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n');save('slot-coverage.json',{'profiles':slot_coverage,'same_field_changed_target':True,'stale_reference_mutations_caught':caught})
 save('validation.json',{'passed':True,'supported_levels':list(g.SUPPORTED_LEVELS),'exhaustive_instances':len(rows),'finite_tasks_by_level':{l:sum(len(t['domain']) for t in g.PROFILES.values() if t['level']==l) for l in g.SUPPORTED_LEVELS},'full_source_bank_replay':True,'grading':{k:report[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',HERE/'source.edn',HERE/'capabilities.json')}})
 print('Validated',len(rows),'distinct bounded instances; eight complete banks and actual grading.')
if __name__=='__main__':main()
