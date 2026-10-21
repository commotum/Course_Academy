import sys,json,re,itertools,hashlib,subprocess,shutil
from pathlib import Path
from collections import Counter,defaultdict
import sympy as s
ROOT=Path(__file__).resolve().parent;WORK=ROOT.parent/'workspace';sys.path.insert(0,str(WORK));import generator as g
x=s.Symbol('x',positive=True);y=s.Symbol('y',real=True)
def write(name,data): (ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def truth(r):
 out=[]
 for field in sorted(r['question'][':question/answer-fields'],key=lambda a:a[':answer-field/key']):
  correct=field[':answer-field/correct'][1];out.append(next(a[':answer/value']=='true' for a in field[':answer-field/choices'] if a[':answer/id']==correct))
 return tuple(out)
def oracle(t,p):
 d,q=p['d'],p['q']
 if t.startswith('power_'):
  f=p.get('a',1)*x**p['n'];claim=d*x**(p['n']-1);rhs=q*y/x
 elif t=='inverse_none': f=-1/x**p['n'];claim=d/x**(p['n']+1);rhs=-q*y/x
 elif t in ('exp_true','exp_none'):
  a=p.get('a',1);rate=p['k']*(-1 if t=='exp_none' else 1);f=a*s.exp(rate*x);claim=a*d*(1 if rate>0 else -1)*s.exp(rate*x);rhs=q*(1 if rate>0 else -1)*y
 elif t=='sin_none':f=s.sin(p['k']*x)/p['b'];claim=s.Rational(d,p['b'])*s.cos(p['k']*x);rhs=s.Rational(q,p['b'])*s.cos(p['k']*x)
 elif t=='cos_i':f=s.cos(p['k']*x);claim=-d*s.sin(p['k']*x);rhs=-q*s.sin(p['k']*x)
 elif t=='log_all': f=s.log(p['k']*x+p['h']);claim=d/(p['k']*x+p['h']);rhs=q/s.exp(y)
 elif t=='log_scaled':f=2*p['m']*s.log(x);claim=d/x;rhs=q*x/s.exp(y/p['m'])
 elif t=='affine_log':f=p['a']*s.log(p['b']*x+p['c']);claim=p['a']*d/(p['b']*x+p['c']);rhs=p['a']*q/s.exp(y/p['a'])
 else:raise AssertionError(t)
 derivative=s.diff(f,x);sub=s.simplify(rhs.subs(y,f));expected=(s.simplify(derivative-claim)==0,s.simplify(derivative-sub)==0)
 return f,claim,rhs,derivative,sub,(expected[0],expected[1],expected[1])
def tex(e):return s.latex(e).replace(r'\log',r'\ln')
def check(r):
 t=r['generation']['template'];p=r['generation']['parameters'];f,claim,rhs,derivative,sub,expected=oracle(t,p);q=r['question'];actual=truth(r);assert actual==expected,(t,p,actual,expected)
 # Exact exposed mathematics must agree with independent expressions, not metadata alone.
 assert '$f(x)='+tex(f)+'.' in q[':question/problem'],(t,'function')
 assert r'$f\prime(x)='+tex(claim)+'.' in q[':question/problem'],(t,'claim')
 assert r'y\prime='+tex(rhs) in q[':question/problem'],(t,'equation')
 solution=q[':question/worked-solution']
 for key,val in zip(('I','II','III'),expected): assert 'Statement '+key+' is '+str(val).lower()+'.' in solution
 assert '&='+tex(derivative) in solution,(t,'derivative solution')
 assert tex(sub) in solution,(t,'substitution solution')
 return ''.join('1' if v else '0' for v in actual)
def main():
 records=[];counts=defaultdict(Counter);boundaries=[]
 for t,band in g.LEVELS.items():
  for case in itertools.product((False,True),repeat=2):
   for i in range(8):
    rec=g.generate(band,seed=81601+i*71,template=t,decision_case=case);key=check(rec);counts[t][key]+=1;records.append(rec)
 write('samples.json',records)
 # Source replay invokes code independently and compares original prompts/solutions and fullBooleanbank semantics.
 source=json.loads((ROOT.parent/'source/source.json').read_text());byid={q[':question/math-academy-id']:q for q in source['material']['kp'][':knowledge-point/questions']};replays=[]
 for t,defaults in g.DEFAULTS.items():
  r=g.source_replay(g.LEVELS[t],t,defaults,raw=True);src=byid[g.MASKS[t]['source_id']];q=r['question']
  assert q[':question/problem']==src[':question/problem'],(t,'raw prompt')
  assert q[':question/worked-solution']==src[':question/worked-solution'],(t,'raw solution')
  expected={f[':answer-field/key']:(f[':answer-field/type'][':db/ident'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),f[':answer-field/correct'][':answer/value']) for f in src[':question/answer-fields']}
  actual={f[':answer-field/key']:(f[':answer-field/type'],sorted(a[':answer/value'] for a in f[':answer-field/choices']),next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])) for f in q[':question/answer-fields']}
  assert actual==expected,(t,'banks')
  replays.append({'source_id':src[':db/id'],'record':r,'exact_problem':True,'exact_solution':True,'complete_bank':True})
 write('replay.json',replays)
 # Choose truth-preserving relevant/irrelevant controlled changes without sampler decision metadata.
 pairs=[];pair_records=[]
 for t,band in g.LEVELS.items():
  base=g.sample(t,__import__('random').Random(817),decision_case=(True,True));base_rec=g.generate(band,template=t,parameters=base)
  # Independent target coefficient derives from derivative; choose another allowed coefficient.
  target=base['d'];alt=next(v for v in ([base['a']*k for k in (2,3,4,5)] if t=='power_moderate' else (2,4,6,8) if t=='log_scaled' else (2,3,4) if t=='affine_log' else (2,3,4,5)) if v!=target)
  p=dict(base,d=alt);r=g.generate(band,template=t,parameters=p);assert truth(base_rec)==(True,True,True) and truth(r)==(False,True,True);assert base_rec['question'][':question/problem']!=r['question'][':question/problem'];check(r)
  pairs.append({'kind':'relevant','template':t,'change':'claim coefficient only','before':base,'after':p,'expected':'111->011','observed':[truth(base_rec),truth(r)]});pair_records.extend([base_rec,r])
  target=base['q'];alt=next(v for v in ((2,4,6,8) if t=='log_scaled' else (2,3,4) if t=='affine_log' else (2,3,4,5)) if v!=target);p=dict(base,q=alt);r=g.generate(band,template=t,parameters=p);assert truth(r)==(True,False,False);check(r)
  pairs.append({'kind':'relevant','template':t,'change':'ODE coefficient only','before':base,'after':p,'expected':'111->100','observed':[truth(base_rec),truth(r)]});pair_records.append(r)
 # Independent irrelevant amplitude scaling of same homogeneous power ODE and derivative.
 p={'a':-3,'n':2,'d':-6,'q':2};q=dict(p,a=-6,d=-12);a=g.generate('moderate',template='power_moderate',parameters=p);b=g.generate('moderate',template='power_moderate',parameters=q);assert truth(a)==truth(b)==(True,True,True);check(a);check(b);pairs.append({'kind':'irrelevant','template':'power_moderate','change':'scale function/claim by2 preserving derivative and homogeneous ODE identity','before':p,'after':q,'expected':'111->111','observed':[truth(a),truth(b)]});pair_records.extend([a,b]);write('counterfactuals.json',pairs);write('counterfactual-records.json',pair_records)
 # Exhaust all8 possibleBoolean responses to everyfamily/decision andcontrolledpair throughnative fieldgrader.
 reps=[records[i] for i in range(0,len(records),8)]+pair_records;grader=[]
 for i,r in enumerate(reps):
  vals=truth(r);checks=[]
  for submitted in itertools.product((False,True),repeat=3):
   for j,v in enumerate(submitted):
    answer_id=next(a[':answer/id'] for a in r['question'][':question/answer-fields'][j][':answer-field/choices'] if a[':answer/value']==str(v).lower())
    checks.append({'field_index':j,'submitted_answer_id':answer_id,'expected':'accepted' if v==vals[j] else 'rejected','purpose':'all8checkbox response patterns; actual correct tuple '+str(vals)})
  grader.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':checks})
 write('grader-input.json',grader)
 render=[next(r for r in records if r['generation']['template']==t and check(r)==case) for t,case in [('power_easy','000'),('power_moderate','011'),('exp_true','111'),('exp_none','100'),('sin_none','011'),('cos_i','111'),('inverse_none','100'),('log_all','000'),('log_scaled','011'),('affine_log','111')]]
 render+=pair_records[-2:];write('render-input.json',render)
 write('independent-tests.json',{'command':'.venv/bin/python '+str(Path(__file__).relative_to(Path.cwd())),'sample_count':len(records),'counts':{k:dict(v) for k,v in counts.items()},'replays':len(replays),'controlled_pairs':len(pairs),'native_grader_cases':len(grader),'render_records':len(render),'passed':True})
 print(json.dumps({'samples':len(records),'families':len(counts),'replays':len(replays),'pairs':len(pairs),'grader_records':len(grader),'render_records':len(render)}))
if __name__=='__main__':main()
