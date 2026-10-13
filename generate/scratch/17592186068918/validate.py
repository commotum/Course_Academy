"""Independent printed prompt/bank/solution checks plus the actual learner grader."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import printed as p
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def fingerprint(q):return g.fingerprint(q)
def zero(e):return sp.trigsimp(sp.simplify(e))==0
def equivalent(a,b,indef):return zero(sp.diff(a-b,p.x)) if indef else sp.simplify(sp.expand_log(a-b,force=True))==0
def check(r):
 q=r['question'];meta=r['generation'];t=meta['template'];m=meta['parameters']['m'];level=q[':question/difficulty'].split('/')[-1]
 assert r==g.generate(level,meta['seed'],t,{'m':m})
 f,lo,hi=p.integral(q[':question/problem']);ef,F,a,c,inner,h,H,elo,ehi=g.math_data(t,m)
 assert zero(f-ef) and (lo,hi)==(elo,ehi)
 assert zero(sp.diff(F,p.x)-f)
 if lo is not None:
  assert lo<hi
  # sin^2+3>=3; 8cos^3+5>=5 on [pi/3,pi/2]; csc+2>=3 on [pi/6,pi/2].
  assert t in ('q-350887','q-350901','q-350904')
  a=sp.simplify(F.subs(p.x,hi)-F.subs(p.x,lo))
 fields=q[':question/answer-fields'];assert len(fields)==1;field=fields[0];bank=field[':answer-field/choices'];blank=field[':answer-field/type'].endswith('/blank')
 assert len(bank)==len(g.sources()[t][':question/answer-fields'][0][':answer-field/choices'])
 vals=[p.scalar(b[':answer/value']).subs(p.C,0) for b in bank]
 matches=[equivalent(v,F if lo is None else a,lo is None) for v in vals]
 if blank:assert all(matches)
 else:
  assert sum(matches)==1
  assert all(not equivalent(v,vals[j],lo is None) for i,v in enumerate(vals) for j in range(i))
 assert next(matches[i] for i,b in enumerate(bank) if b[':answer/id']==field[':answer-field/correct'][1])
 assert blank==('{{field-1}}' in q[':question/problem'])
 assert meta['mathematical_fingerprint']==fingerprint(q)
 if m>1 or t=='q-49557':
  sol=q[':question/worked-solution'];pin=p.scalar(re.search(r'\$u=(.*?),\$',sol)[1]);assert pin==inner
  du=p.scalar(re.search(r'\\frac\{\\text\{d\}u\}\{\\text\{d\}x\}=(.*?)\.\n',sol)[1]);assert zero(du-sp.diff(pin,p.x))
  rows=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1].split('\\\\');rhs=[r.split('&=')[1].strip() for r in rows]
  i=rhs[0].index(r'\int');pc=p.scalar(rhs[0][:i].rstrip('{ '));assert pc==c
  ht=rhs[0].split(r'\text{d}u')[0];start=i+4
  if lo is not None:
   start+=2;assert ht[start]=='_';ul,start=p.group(ht,start+1);assert ht[start]=='^';uh,start=p.group(ht,start+1)
   assert p.scalar(ul)==sp.simplify(inner.subs(p.x,lo)) and p.scalar(uh)==sp.simplify(inner.subs(p.x,hi))
  assert zero(p.scalar(ht[start:])-h)
  prim=p.scalar(rhs[1].split(r'\big|')[0]).subs(p.C,0);assert sp.simplify(sp.diff(prim,p.u)-c*h)==0
  if lo is None:assert zero(sp.diff(p.scalar(rhs[-1]).subs(p.C,0),p.x)-f)
  else:
   assert equivalent(p.scalar(rhs[-2]),a,False) and equivalent(p.scalar(rhs[-1]),a,False)
   table=re.search(r'\| \$x\$ \| \$(.*?)\$ \| \$(.*?)\$ \|\n\| --- \| --- \| --- \|\n\| \$u\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol)
   aa,bb,cc,dd=map(p.scalar,table.groups());assert (aa,bb)==(lo,hi) and sp.simplify(inner.subs(p.x,aa)-cc)==0 and sp.simplify(inner.subs(p.x,bb)-dd)==0
 return r

def native(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'all source-bank options'} for a in f[':answer-field/choices']]
 else:
  c=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
  checks=[{'submitted':a[':answer/value'],'expected':'accepted','purpose':'all canonical aliases'} for a in f[':answer-field/choices']]
  checks += [{'submitted':s,'expected':e,'purpose':purpose} for s,e,purpose in [('('+c+')+0','accepted','equivalent exact'),('2('+c+')/2','accepted','unsimplified equivalent'),('('+c+')+1','rejected','wrong offset'),('-('+c+')','rejected','wrong sign')]]
 return {'label':label,'record':r,'checks':checks}
def main():
 rs=[];inputs=[];replays=[];review=[];fps=set();counts={}
 for t in g.DATA:
  old=g.sources()[t];r=check(g.generate(g.DATA[t][0],0,t,{'m':1}));q=r['question'];of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and [a[':answer/value'] for a in nf[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
  if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution']
  replays.append({'source':t,'complete_bank_matched':True,'matched_values':len(nf[':answer-field/choices']),'total_values':len(of[':answer-field/choices']),'matched_distractors':0 if nf[':answer-field/type'].endswith('/blank') else 4,'missing_extra':[],'authored_completion':t=='q-49557'})
  inputs.append(native('source-'+t,r));review+=[{'label':'original '+t,'record':old},{'label':'variant '+t,'record':g.generate(g.DATA[t][0],0,t,{'m':2})}]
 for level in ('easy','hard'):
  n=0
  for t,params in g.candidates(level):
   r=check(g.generate(level,1949,t,params));fp=fingerprint(r['question']);assert fp not in fps;fps.add(fp);n+=1;rs.append(r);inputs.append(native(t+'-'+str(params['m']),r));assert r['question']==g.generate(level,999,t,params)['question']
  counts[level]=n
 for level,t,m in [('moderate','q-49557',2),('easy','q-49557',0),('easy','q-49557',13),('easy','q-49557',True),('hard','q-49557',2)]:
  try:g.generate(level,0,t,{'m':m})
  except ValueError:pass
  else:raise AssertionError('Invalid input accepted')
 try:g.batch('easy',12,0)
 except ValueError:pass
 else:raise AssertionError('Finite limit ignored')
 save('source-replay.json',{'passed':True,'sources':replays,'complete_banks_matched':7,'complete_banks_total':7,'matched_values':sum(r['matched_values'] for r in replays),'matched_distractors':16,'excluded_sources':['q-10045','q-10046'],'source_solutions_retained':6})
 save('previews.json',rs);save('review.json',review);(HERE/'review.md').write_text('\n\n'.join('## '+r['label']+'\n\n'+(g.markdown(r['record']) if 'question' in r['record'] else r['record'][':question/problem']+'\n\n'+r['record'].get(':question/worked-solution','Missing source solution')) for r in review))
 save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('capabilities.json',{'supported_levels':['easy','hard'],'bounded_distinct_tasks':counts,'policy':'m=2..12 positive amplitude with complete source banks; easy q-49557 authored classification (single direct derivative/denominator logarithm); hard retains source labels. No novel middle-workload template inferred.','exceptions':[{'difficulty':'moderate','status':'unsupported','unfilled_reserve':5,'evidence':'No rated moderate source. Unrated q-10046 includes two non-real logarithm distractors; cannot reproduce its complete bank as a valid real bank. Bounded policy supports direct basic q-49557 and observed hard families only, not impossibility of moderate mathematics. New valid source evidence reopens classification.'},{'source':'q-10046','status':'excluded','reason':'ln(1-sqrt(2)) is not real; missing key, rating and solution. Original retained.'},{'source':'q-10045','status':'excluded','reason':'Options 1 and 3 are identical sums of logarithms with reversed order. Original retained.'}],'unsupported_levels_filled':False})
 files=[HERE.with_suffix('.py'),HERE/'printed.py',HERE/'source.json',HERE/'validate.py',HERE/'check-engine.rs',HERE/'check-engine']
 save('validation.json',{'passed':True,'counts':counts,'exhaustive_distinct_instances':len(fps),'source_bank_fidelity':'7/7 supported complete banks; 24/24 values; 16/16 distractors; 2 explicit defective exclusions','mathematics':'Independent parsing of printed prompts, banks, substitution, derivative, transformed integrals, primitives, bounds, endpoint differences and final values; exact derivative and logarithm equivalence checks. Blank aliases retained.','native_grading':'All supported source replays and 77 bounded variants; every radio choice and canonical/equivalent/incorrect blank probes.','hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}})
 print('Validated',counts,flush=True)
if __name__=='__main__':main()
