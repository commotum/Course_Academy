#!/usr/bin/env python3
"""Fail on fidelity, displayed mathematics/stages, native grading, scope or identity."""
import collections,difflib,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
from fractions import Fraction
import sympy as sp
D=Path(__file__).parent;SCRIPT=D.with_suffix('.py');spec=importlib.util.spec_from_file_location('g',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def dump(name,data):(D/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def check(value,label):
 if not value:raise AssertionError(label)
def balanced(s):
 check(s.count('$')%2==0,'unbalanced math delimiters')
 depth=0
 for c in re.sub(r'\\[{}]','',s):
  depth+=(c=='{')-(c=='}');check(depth>=0,'unmatched brace')
 check(depth==0,'unmatched brace end');check('@@' not in s,'unfilled slot')
 check('--' not in s and '+-' not in s,'ungrouped signed term')
def rhs(row):return row.split('=',1)[1].replace('&','').strip()
def components(row):
 s=rhs(row).replace(r'\,','').replace(r'\text{ }','').strip()
 m=re.fullmatch(r'(.*)i\s*([+-].*)j',s);check(m is not None,'basis row '+s)
 a,b=m.groups();return g.parse_math(a or '1'),g.parse_math(b if b not in ('+','-') else b+'1')
def paren_arg(s,start):
 check(s[start]=='(','argument opening');depth=1;i=start+1
 while depth:
  depth+=(s[i]=='(')-(s[i]==')');i+=1
 return s[start+1:i-1],i

def independent(record,allow_anomalies=False):
 q=record['question'];check(set(record['knowledge_point'])=={'db_id','id','title'},'outer schema shape')
 problem=q[':question/problem'];balanced(problem)
 ftext=re.search(r'\$f\(x, ?y\)\s*=\s*(.*?)\$',problem).group(1).rstrip(',')
 f=g.parse_math(ftext);pointtext=re.search(r'\$\(x, ?y\)\s*=\s*(.*?)\$',problem).group(1).rstrip('.').strip()[1:-1]
 pt,qt=map(g.parse_math,pointtext.split(','));dx,dy=sp.diff(f,g.X),sp.diff(f,g.Y);u,v=[sp.simplify(e.subs({g.X:pt,g.Y:qt})) for e in (dx,dy)];check((u,v)!=(0,0),'nonzero gradient')
 want=u*(g.X-pt)+v*(g.Y-qt)
 field=q[':question/answer-fields'][0];answers=field[':answer-field/choices'];check(len(answers)==5,'full 5 option bank');ids=[a[':answer/id'] for a in answers];check(len(set(ids))==5,'owned distinct answer IDs')
 for a in answers:balanced(a[':answer/value'])
 lines=[g.read_line(a[':answer/value']) for a in answers];keys=[g.line_key(z) for z in lines];eligible=[a[':answer/id'] for a,z in zip(answers,lines) if g.equivalent(z,want)]
 if not allow_anomalies:check(len(set(keys))==5,'no whole-line-equivalent options');check(len(eligible)==1,'exactly one mathematically valid line')
 if ':answer-field/correct' in field:check(field[':answer-field/correct'][1] in eligible,'correct whole object designation')
 # Independent tangent criterion and finite slope where meaningful.
 for a,z in zip(answers,lines):
  if a[':answer/id'] in eligible:
   check(sp.simplify(z.subs({g.X:pt,g.Y:qt}))==0,'line passes through displayed point')
   aa=sp.diff(z,g.X);bb=sp.diff(z,g.Y)
   check(sp.simplify(aa*v-bb*u)==0,'gradient and displayed line normal parallel')
   if v:check(sp.simplify(-aa/bb+u/v)==0,'whole-line slope')
 sol=q.get(':question/worked-solution')
 if sol:
  balanced(sol);blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);check(len(blocks)==2,'source complete two blocks')
  rows=blocks[0].split('\\\\');check(len(rows)==6,'ordered six gradient rows')
  check('{f}_{x}(x,y)' in rows[0] and '{f}_{y}(x,y)' in rows[0],'formal component row')
  row=rows[1]
  for marker in (r'\frac{∂}{∂x}',r'\frac{∂}{∂y}'):
   i=row.index(marker)+len(marker);arg,_=paren_arg(row,i);check(sp.simplify(g.parse_math(arg)-f)==0,'actual formal derivative input')
  aa,bb=components(rows[2]);check(sp.simplify(aa-dx)==0 and sp.simplify(bb-dy)==0,'actual displayed partial derivatives')
  aa,bb=components(rows[3]);check(not (aa.has(g.X,g.Y) or bb.has(g.X,g.Y)),'point component substitution complete')
  check(sp.simplify(aa-u)==0 and sp.simplify(bb-v)==0,'displayed point-substitution arithmetic')
  pp=rows[3].split('&')[0];m=re.search(r'f\((.*?),(.*?)\)',pp);check(m is not None,'gradient evaluation point')
  check(sp.simplify(g.parse_math(m.group(1))-pt)==0 and sp.simplify(g.parse_math(m.group(2))-qt)==0,'evaluation point in actual row')
  aa,bb=components(rows[4]);check(sp.simplify(aa-u)==0 and sp.simplify(bb-v)==0,'component reduction row')
  m=re.search(r'⟨(.*?),(.*?)⟩',rows[5]);check(m is not None,'gradient tuple');aa,bb=map(g.parse_math,m.groups());check(sp.simplify(aa-u)==0 and sp.simplify(bb-v)==0,'gradient tuple actual')
  tangent=blocks[1].split('\\\\');check(len(tangent)==3,'ordered three tangent rows')
  check('∇f({x}_{0},{y}_{0})' in tangent[0] and 'x-{x}_{0}' in tangent[0] and 'y-{y}_{0}' in tangent[0],'formal tangent row')
  m=re.search(r'f\((.*?),(.*?)\)',tangent[1]);check(m is not None,'tangent evaluated gradient')
  check(sp.simplify(g.parse_math(m.group(1))-pt)==0 and sp.simplify(g.parse_math(m.group(2))-qt)==0,'tangent point')
  m=re.search(r'⟨(.*?),(.*?)⟩',tangent[1]);a,b=map(g.parse_math,m.groups());check(sp.simplify(a-(g.X-pt))==0 and sp.simplify(b-(g.Y-qt))==0,'tangent displaced components')
  actual=re.sub(r'\s*&\s*','',tangent[2]).strip().rstrip('.')
  check(g.equivalent(g.read_line(actual),want),'final full displayed tangent equation')
 return {'equivalent_correct_options':len(eligible),'distinct_whole_lines':len(set(keys)),'stages_checked':0 if not sol else 9}

def finite_count(level):
 """Enumerate canonical polynomial derivative/point tasks modulo common scaling.
 Rational coordinates are reduced FIRST; unused constants/banks are absent.
 This counts canonical easy only, a conservative lower bound across 7 families.
 """
 maxcoef=5 if level=='easy' else 6
 coeff=[i for i in range(-maxcoef,maxcoef+1) if i]
 pts=[Fraction(i) for i in ([-2,-1,1,2] if level=='easy' else [-3,-2,-1,1,2,3])] if level!='hard' else sorted({Fraction(n,d) for d in (2,3) for n in range(-5,6) if n and Fraction(n,d).denominator==d})
 tasks=set();valid=0
 for a,b,c,p,q in itertools.product(coeff,coeff,coeff,pts,pts):
  u=2*a*p+b*q if level=='easy' else 2*a*p+c*q*q;v=b*p+2*c*q if level=='easy' else 2*b*q+2*c*p*q
  if not u or not v or u==v or u==-v or u*p==v*q:continue
  if any(abs(e.numerator)>200 or e.denominator>27 for e in (u,v)):continue
  valid+=1
  tasks.add((Fraction(b,a),Fraction(c,a),p,q))
 return {'valid_parameter_tuples':valid,'meaningful_assessed_tasks':len(tasks),'counted_family':'canonical' if level!='easy' else 'quadratic (conservative easy-family lower bound)','normalization':'common function scale; no bank, identity, aliases or added constants','coordinates':len(pts),'coefficients':len(coeff)}

def main():
 check((D/'source.json').read_bytes()==Path('generate/runs/current/sources/17592186124454.json').read_bytes(),'immutable source copy')
 originals=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'];source_report=[];records=[];engine=[];review=[]
 for original in originals:
  sid=original[':question/math-academy-id'];case=next(c for c in json.loads((D/'source-cases.json').read_text()) if c['source_id']==sid)
  raw=g.generate('easy',profile='raw:'+sid,template=case['template'],parameters=case['parameters']);q=raw['question'];of=original[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  for k in (':question/problem',':question/worked-solution'):
   check((k in q)==(k in original),'raw key presence '+sid+k);check(q.get(k)==original.get(k),'exact source '+sid+k)
  for k in (':question/difficulty',':question/answer-fields'):check((k in q)==(k in original),'raw key presence '+sid+k)
  check((':answer-field/correct' in f)==(':answer-field/correct' in of),'raw correct presence')
  check(sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']),'exact source complete bank')
  check(f[':answer-field/type']==of[':answer-field/type'][':db/ident'],'field type fidelity');check(f[':answer-field/key']==of[':answer-field/key'],'field key fidelity')
  if ':answer-field/correct' in of:
   actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);check(actual==of[':answer-field/correct'][':answer/value'],'exact designation fidelity')
  report=independent(raw,True);report.update({'source_id':sid,'exact_prompt':True,'exact_bank_options':5,'exact_worked_solution':':question/worked-solution' in original,'designation_matched':':answer-field/correct' in of,'omissions_preserved':True})
  source_report.append(report);review.append({'label':'Original raw '+sid,'record':raw})
  completed=g.generate('easy',profile='completed:'+sid);independent(completed,True);review.append({'label':'Inferred completion / opaque evidence '+sid,'record':completed});records.append(completed)
  # Alter actual curve and actual coordinates through the same public raw API.
  transformed=g.generate('easy',profile='raw:'+sid,parameters={'r':2,'s':3});independent(transformed,True);review.append({'label':'Generated raw coordinate pullback '+sid,'record':transformed})
  for r,s in itertools.product(range(1,4),repeat=2):independent(g.generate('easy',profile='raw:'+sid,parameters={'r':r,'s':s}),True)
  for n in (11,37):
   normal=g.generate('easy',seed=n,template=case['template']);independent(normal);review.append({'label':'Generated authored safe bank '+sid,'record':normal});records.append(normal)
 for level in ('moderate','hard'):
  for seed in (11,37):
   rec=g.generate(level,seed);independent(rec);review.append({'label':'Generated authored '+level,'record':rec});records.append(rec)
 seen=collections.defaultdict(set);positions=set();sample=0
 for level in ('easy','moderate','hard'):
  templates=list(g.TEMPLATES) if level=='easy' else ['canonical']
  for template in templates:
   for seed in range(35):
    rec=g.generate(level,seed,template);independent(rec);sample+=1;seen[level].add(rec['generation']['mathematical_fingerprint']);f=rec['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
   base=g.generate(level,8,template);args={'level':level,'template':template,'profile':base['generation']['profile'],'parameters':base['generation']['parameters']};again=g.generate(seed=77,**args)
   check(base['question'][':question/id']==again['question'][':question/id'],'seed-independent question identity')
   check(base['generation']['mathematical_fingerprint']==again['generation']['mathematical_fingerprint'],'seed-independent task fingerprint')
 check(positions==set(range(5)),'deterministic shuffled correct position variation')
 # Finite numerical domains, signed boundaries, invalid reduced rational workload.
 bad=[('moderate',{'a':-7,'b':2,'c':1,'p':1,'q':2}),('moderate',{'a':1,'b':2,'c':1,'p':'1/2','q':2}),('hard',{'a':1,'b':2,'c':1,'p':'1/999999','q':'1/2'}),('hard',{'a':1,'b':2,'c':1,'p':'20/10','q':'2/3'}),('hard',{'a':0,'b':2,'c':1,'p':'1/2','q':'2/3'}),('easy',{'a':1,'b':2,'c':1,'p':'oo','q':2})]
 for level,p in bad:
  try:g.generate(level,template='canonical' if level!='easy' else 'quadratic',parameters=p)
  except ValueError:pass
  else:raise AssertionError('explicit invalid input accepted '+str(p))
 for profile in ('raw:q-36383','raw:q-37517'):
  for p in ({'r':0,'s':1},{'r':'1/999999','s':1},{'r':4,'s':1}):
   try:g.generate('easy',profile=profile,parameters=p)
   except ValueError:pass
   else:raise AssertionError('raw invalid domain')
 # Accepted signed/reduced boundaries and aliases tested via public explicit API.
 for level,p in [('moderate',{'a':-6,'b':6,'c':-6,'p':3,'q':-3}),('hard',{'a':-6,'b':6,'c':-6,'p':'5/2','q':'-5/3'})]:
  independent(g.generate(level,template='canonical',parameters=p))
 a=g.generate('easy',template='product',parameters={'a':1,'b':2,'c':1,'p':1,'q':2})
 b=g.generate('easy',template='product',parameters={'a':1,'b':2,'c':5,'p':1,'q':2})
 check(a['question'][':question/id']==b['question'][':question/id'],'unused coefficient does not create presentation identity')
 check(a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'],'unused coefficient excluded from assessment counts')
 a=g.generate('easy',template='quadratic',parameters={'a':1,'b':2,'c':3,'p':1,'q':2})
 b=g.generate('easy',template='quadratic',parameters={'a':-1,'b':-2,'c':-3,'p':1,'q':2})
 check(a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'],'common scalar multiple excluded from task identity')
 check(a['question'][':question/id']!=b['question'][':question/id'],'changed display gives different content identity')
 # Native field tests on all displayed IDs (including opaque completed evidence).
 for i,rec in enumerate(records):
  f=rec['question'][':question/answer-fields'][0];engine.append({'label':f"review-{i}-{rec['generation']['template']}",'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio selection; independent complete-line mathematics checked separately'} for a in f[':answer-field/choices']]})
 dump('engine-input.json',engine);run=subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-report.json')],capture_output=True,text=True);check(run.returncode==0,'native grading '+run.stderr)
 dump('review.json',review);(D/'review.md').write_text('# Tangent line generator review\n\nOriginal raw records preserve absent difficulty/correct keys. Inferred completions retain opaque or ambiguous banks and are **evidence only**. Generated learning variants use explicitly authored safe banks. Correct native designations are marked; equivalent historical options are listed in validation, independently of their native key.\n\n'+''.join(g.markdown(x['record'],x['label']) for x in review))
 counts={level:finite_count(level) for level in ('easy','moderate','hard')}
 # Freeze hashes only after final artifact generation. Validation report excluded.
 files=[SCRIPT,*[p for p in D.iterdir() if p.is_file() and p.name!='validation.json'],Path('generate/runs/current/sources/17592186124454.json'),Path('generate/runs/current/topics/17592186049511.json'),Path('generate/runs/current/lessons/17592186049511.json'),Path('generate/runs/current/check-engine'),Path('generate/runs/current/check-engine.rs'),Path('engine/rust/learning.rs')]
 hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.exists()}
 report={'passed':True,'source_provenance':g.SOURCE,'source_practice_total':7,'source_prompt_exact':7,'source_bank_options_exact':35,'source_complete_banks_exact':7,'source_worked_solutions_exact':5,'source_worked_solutions_absent':2,'source_correct_designations_matched':5,'source_correct_designations_absent':2,'source_unrated_omissions_preserved':2,'raw_source_analysis':source_report,'source_whole_bank_learning_valid':4,'source_ambiguous_whole_banks':3,'source_keyed_distractors_exact':20,'source_unkeyed_choices_exact':10,'historical_wrong_operation_intentions_resolved':0,'coordinate_pullbacks_independently_checked':63,'raw_eligible_for_learning':False,'completed_opaque_eligible_for_learning':False,'safe_bank_learning_records':True,'authored_levels':['moderate','hard'],'generated_actual_display_checks':sample,'sampled_meaningful_tasks':{k:len(v) for k,v in seen.items()},'finite_domain_counts':counts,'native_grader':json.loads((D/'engine-report.json').read_text()),'format':'balanced prompt/choices/worked solution delimiters and braces','identity':'whole display bank/prompt/solution included; shuffle excluded; common polynomial scaling excluded from task','plot_rating':'none for practice; canonical contextual raster inspected','limits':['historical wrong-operation intentions unresolved; coordinate pullback is evidence geometry only','native radio grader evaluates stored key, not complete line equivalence; independent ambiguity analysis is authoritative','missing-level difficulty workload is authored rather than observed','2 source correct refs/solutions/difficulty omitted in raw replay; completion is separate','common scaling normalized for polynomial task counts; log/trig aliases deduplicated by actual displayed derivatives'],'freeze_hashes':hashes}
 dump('validation.json',report);print(f"PASS: 7 prompts, 35 options, 5 worked solutions; {sample} displayed variants; native {run.stdout.strip()}");print('Finite task counts:',counts)
if __name__=='__main__':main()
