"""Independent rendered mathematics, bank replay and counterexample checks.

The reader does not use the generator's expected expressions or parameters.
It differentiates actual displayed primitives, compares every original and
transformed operand and bound, and checks separate signed endpoint components.
"""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
H=Path(__file__).parent
z=importlib.util.spec_from_file_location('kp00818_generator',H.with_suffix('.py'));G=importlib.util.module_from_spec(z);z.loader.exec_module(G);R=G.R;x,u=R.x,R.u

def write(n,z):(H/n).write_text(json.dumps(z,indent=2,ensure_ascii=False)+'\n')
def check(r):
 G.fmt.validate_generated_record(r);q=r['question'];expect,counts=R.stages(q);f=q[':question/answer-fields'][0];answers=f[':answer-field/choices'];blank=f[':answer-field/type'].endswith('/blank')
 c,F,_,lo,hi,end=R.integral(next(b for b in R.blocks(q[':question/problem'])if r'\int'in b).rstrip('= .?('));assert not end;canon=s.cancel(s.expand_log((c*F).subs(x,s.Symbol('positive_x',positive=True)),force=False));actualfp=G.digest({'integrand':s.srepr(canon),'bounds':list(map(s.srepr,[s.simplify(lo),s.simplify(hi)])),'domain':'positive x; real logarithm; original continuous u-interval, convergent endpoint allowed'});assert r['generation']['math_fingerprint']==actualfp,('stale mathematical fingerprint',r['generation'])
 # Read supplied notation, so a coefficient blank is graded against precisely
 # its fragment rather than the full definite integral value.
 last=R.blocks(q[':question/problem'])[-1];mult=R.scalar(last.lstrip(')').strip())if last.startswith(')')else s.Integer(1)
 vals=[R.scalar(a[':answer/value'])for a in answers];good=[a[':answer/id']for a,v in zip(answers,vals)if R.equal(v*mult,expect)]
 assert f[':answer-field/correct'][1]in good,(q[':question/problem'],vals,expect,mult)
 if not blank:
  assert len(good)==1,('multiple correct answers',good)
  for i,v in enumerate(vals):
   for w in vals[:i]:assert not R.equal(v,w),('equivalent choices',v,w)
 else:assert len(good)==len(vals),('incorrect supported blank expression',vals,expect,mult)
 return counts,expect/mult

source=[];ledger=[];reviews=[];native=[];coverage={};stats={};alltasks=set();sourceerrors=[]
for sid in G.QS:
 print('checking '+sid,flush=True);r=G.generate(G.CONFIG[sid],template=sid,parameters=G.original(sid));cc,expected=check(r);source.append({'source_id':sid,'record':r,'raw_source_eligible':sid not in G.REPAIRS,'repair':G.REPAIRS.get(sid,[])})
 sf=G.QS[sid][':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0];unused=set(range(len(gf[':answer-field/choices'])));mappings=[]
 for a in sf[':answer-field/choices']:
  matches=[i for i in unused if R.equal(R.scalar(a[':answer/value']),R.scalar(gf[':answer-field/choices'][i][':answer/value']))];assert len(matches)>=1,(sid,a,matches)
  i=matches[0];unused.remove(i);mappings.append({'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'generated_value':gf[':answer-field/choices'][i][':answer/value'],'recipe':'t * observed expression(x/k)','interpretation':'complete opaque observed pattern, no inferred misconception','matched':True,'source_correct':a[':answer/id']==sf.get(':answer-field/correct',{}).get(':answer/id'),'generated_correct':gf[':answer-field/choices'][i][':answer/id']==gf[':answer-field/correct'][1]})
 assert not unused
 if sid!='q-49607':assert all(a['source_correct']==a['generated_correct']for a in mappings)
 ledger.append({'source_id':sid,'profile':sid,'matched':len(mappings),'total':len(mappings),'choices':mappings,'prompt_equal_normalized':r['question'][':question/problem']==G.fmt.normalize_prose(G.QS[sid][':question/problem']),'solution_equal_normalized':sid not in G.REPAIRS and r['question'][':question/worked-solution']==G.fmt.normalize_prose(G.QS[sid].get(':question/worked-solution',''))})
 if sid in G.REPAIRS:sourceerrors.append({'source_id':sid,'raw_eligible':False,'supported_repair':G.REPAIRS[sid],'raw_question':G.QS[sid],'corrected_record':r})
 rows=[r];reviewseen={r['generation']['math_fingerprint']};tasks=set();slots={k:set()for k in G.original(sid)}
 for seed in range(12):
  v=G.generate(G.CONFIG[sid],seed=seed,template=sid);counts,key=check(v);rows.append(v);tasks.add(v['generation']['math_fingerprint']);alltasks.add(v['generation']['math_fingerprint'])
  for k,z in counts.items():stats[k]=stats.get(k,0)+z
  for k,z in v['generation']['parameters'].items():slots[k].add(z)
  if len(reviewseen)<4 and v['generation']['math_fingerprint']not in reviewseen:
   reviews.append({'source_id':sid,'seed':seed,'record':v});reviewseen.add(v['generation']['math_fingerprint'])
 coverage[sid]={'actual_distinct_math_tasks_in_12':len(tasks),'slots':{k:sorted(z)for k,z in slots.items()}}
 # Freeze native full-bank grading on originals and 3 normal variants/profile.
 selected=[r]+[z['record']for z in reviews if z['source_id']==sid];assert len(selected)==4
 for j,v in enumerate(selected):
  f=v['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];checks=[]
  if f[':answer-field/type'].endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'full observed bank ID selection'}for a in f[':answer-field/choices']]
  else:
   _,key=check(v);canonical=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==correct);equivalent=G.tex(s.expand(key));equivalent='('+equivalent+')+0';wrong=G.tex(key+1)
   checks=[{'submitted':canonical,'expected':'accepted','purpose':'canonical normal blank fragment'},{'submitted':equivalent,'expected':'accepted','purpose':'genuinely equivalent normal blank fragment'},{'submitted':wrong,'expected':'rejected','purpose':'wrong normal blank fragment'}]
  native.append({'label':sid+' '+('original'if j==0 else'normal-'+str(j)),'record':v,'checks':checks})
# Failures aimed at a correct-result-only validator.
mutations=[]
base=next(z['record']for z in source if z['source_id']=='q-49605')
for label,old,new in [
 ('derivative false operand',r'=\frac{1}{x}',r'=\frac{2}{x}'),
 ('original integral wrong operand',r'\frac{8\operatorname{ln}⁡x}{x}',r'\frac{9\operatorname{ln}⁡x}{x}'),
 ('transformed integral wrong operand',r'_{2}^{4}u\,',r'_{2}^{4}u^{2}\,'),
 ('transformed bounds stale',r'_{2}^{4}u\,',r'_{1}^{4}u\,'),
 ('invalid primitive unchanged endpoint result',r'4\cdot {u}^{2}{|}_{2}^{4}',r'4\cdot {u}^{2}+(u-2)(u-4){|}_{2}^{4}'),
 ('compensating endpoint arithmetic',r'(16-4)',r'(17-5)'),
]:
 q=copy.deepcopy(base);sol=q['question'][':question/worked-solution'];assert old in sol,(label,old);q['question'][':question/worked-solution']=sol.replace(old,new,1)
 try:check(q)
 except Exception as e:mutations.append({'mutation':label,'caught':True,'reason':str(e)[:400]})
 else:raise AssertionError(('undetected mutation',label))
# Supplied blank suffix must participate in validation.
b=copy.deepcopy(next(z['record']for z in source if z['source_id']=='q-351286'));b['question'][':question/problem']=b['question'][':question/problem'].replace(r')\operatorname{ln}⁡2',r')\operatorname{ln}⁡3')
try:check(b)
except Exception as e:mutations.append({'mutation':'stale supplied blank factor','caught':True,'reason':str(e)[:400]})
else:raise AssertionError('undetected blank suffix')
# CLI list contract and builtin integer guards.
for level in ('easy','moderate','hard'):
 for key,val in [('seed',True),('count',True),('count',101)]:
  try:G.generate_batch(level,**{key:val})
  except ValueError:pass
  else:raise AssertionError(('invalid builtin integer/count',key,val))
p=subprocess.run([sys.executable,str(H.with_suffix('.py')),'--difficulty','all','--count','1'],capture_output=True,text=True);assert p.returncode==0,p.stderr;assert len(json.loads(p.stdout))==3
p=subprocess.run([sys.executable,str(H.with_suffix('.py')),'--difficulty','all','--count','1','--format','markdown'],capture_output=True,text=True);assert p.returncode==0 and r'\int'in p.stdout
write('source-cases.json',source);write('choice-ledger.json',ledger);write('source-errors-and-repairs.json',sourceerrors);write('review-cases.json',reviews);write('native-input.json',native)
write('independent-inventory.json',{'basis':2275,'description':'Captured non-MA inventory only. The frozen source contains34MA questions and zero non-MA questions; authored native fixtures are separate.','count':0,'entries':[]})
write('validation.json',{'status':'mathematics passed; native grading pending','basis':2275,'raw_source_questions':34,'raw_source_eligible':30,'raw_source_ineligible':4,'supported_repaired_originals':4,'rated_complete_source_banks':33,'authored_completed_bank':1,'replayed_banks':34,'matched_source_answers':sum(z['matched']for z in ledger),'total_source_answers':sum(z['total']for z in ledger),'source_originals_suppressed':0,'normal_sample_records':34*12,'actual_distinct_math_tasks_in_normal_samples':len(alltasks),'coverage':coverage,'operative_stage_checks':stats,'mutation_checks':mutations,'capacity':'23 reduced positive ratios from numerator/denominator1..6 times6 x-scales =138 mathematical tasks per profile before cross-profile equivalence; batch cap100 and task dedup, no bank/seed-only variety','limits':['Coefficient and positive x-rescaling only; base, log exponent, transformed endpoints and field fragment role fixed per observed source profile.','Opaque distractors preserve exact whole expressions under scaling; no unobserved misconception recipes.','q-49607 completion is authored, not rated observed evidence.','q-31643 improper lower endpoint has exponent-1/2 and finite primitive limit.']})
print('Mathematics checks passed; originals34, normal408, actualdistinct'+str(len(alltasks)),flush=True)
