#!/usr/bin/env python3
"""Read-only independent audit. Run with repo .venv Python, PYTHONDONTWRITEBYTECODE=1.
Optional --candidate-records FILE evaluates a prospective batch's bank-only cue.
"""
import sys
sys.dont_write_bytecode=True
import argparse, collections, copy, hashlib, importlib.util, json, pathlib, re, subprocess
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
E=pathlib.Path(__file__).resolve().parent
P=E.parent/'workspace'; R=pathlib.Path('/home/jake/Developer/Course_Academy')
def save(name,obj): (E/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def load(path): return json.loads(pathlib.Path(path).read_text())
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
sys.path.insert(0,str(P)); g=module('audited_generator',P/'generator.py')
f=module('shared_math_format',R/'scripts/question_capture/math_format.py')
x=s.Symbol('x')
# Restricted independent parser for the captured/emitted TeX vocabulary. Not a learner grader.
def parse(t):
 t=t.replace('\u2061','').replace(r'\operatorname{ln}','ln').replace(r'\ln','ln')
 t=t.replace(r'\left','').replace(r'\right','').replace(r'\cdot','*').replace(r'\,','').replace(' ', '')
 if t.startswith('y='):t=t[2:]
 def group(i):
  assert t[i]=='{', (t,i)
  depth=1;j=i+1
  while depth:
   depth+=(t[j]=='{')-(t[j]=='}');j+=1
  return t[i+1:j-1],j
 while r'\frac' in t:
  i=t.index(r'\frac'); a,j=group(i+5);b,k=group(j)
  t=t[:i]+'(('+a+')/('+b+'))'+t[k:]
 t=t.replace('{','(').replace('}',')')
 t=re.sub(r'ln(\d+)',r'ln(\1)',t)
 t=re.sub(r'(?<=[0-9x)])ln', '*ln',t)
 assert '\\' not in t,t
 return parse_expr(t,local_dict={'x':x,'ln':s.log},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))
def choices(rec):return rec['question'][':question/answer-fields'][0][':answer-field/choices']
def correct(rec):return rec['question'][':question/answer-fields'][0][':answer-field/correct'][1]
def expected(rec):
 # Read displayed function and point, not generation answer metadata.
 p=rec['question'][':question/problem']; expr=re.search(r'(?:y|f\(x\))\s*=\s*([^$]+)',p)[1].rstrip(',.')
 y=parse(expr);d=s.diff(y,x)
 if 'point where' in p:
  t=parse(re.search(r'point where \$x=([^$]+)',p)[1].rstrip('.'))
  return s.expand(d.subs(x,t)*(x-t)+y.subs(x,t)) if 'equation' in p else d.subs(x,t)
 if '{{field-1}}' in p and r'\cdot' in p.split('{{field-1}}')[1]:return s.simplify(d/(y))
 return d

def cue(rec):
 # DECLARED INPUT: complete bank ONLY. No target, key, source recipe, metadata,
 # bounds or derivative reasoning. Count slope signs; inspect repeated coefficients
 # and standalone rational constant. This is a recognizable bank-layout recipe.
 vals=[(a,parse(a[':answer/value'])) for a in choices(rec)]
 slopes=[s.expand(v).coeff(x) for a,v in vals]
 signs=[int(s.sign(v)) for v in slopes]; majority=collections.Counter(signs).most_common(1)[0][0]
 counts=collections.Counter(slopes)
 candidates=[]
 for (a,v),slope,sign in zip(vals,slopes,signs):
  rational_part=s.expand(v.subs(x,0)).as_coeff_Add()[0]
  if sign==majority and counts[slope]==2 and rational_part>0:candidates.append(a[':answer/id'])
 return candidates[0] if len(candidates)==1 else None

def probes(records):
 return {'allowed_information':'Bank-only: displayed option expressions, slope-sign counts, repeated x coefficients and sign of rational constant. No target, keys, parameters or correct-output catalog. Symbolic extraction recognizes these superficial bank roles; no differentiation or curve evaluation.',
  'total':len(records),'correct':sum(cue(r)==correct(r) for r in records),'random_baseline':0.2,
  'cases':[{'id':r['question'][':question/id'],'seed':r.get('generation',{}).get('seed'),'predicted':cue(r),'correct':correct(r),'success':cue(r)==correct(r),'point':r.get('generation',{}).get('parameters',{}).get('point')} for r in records]}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidate-records');args=ap.parse_args()
 if args.candidate_records:
  rs=load(args.candidate_records); report=probes(rs);save('prospective-probe.json',report);print(json.dumps({k:v for k,v in report.items() if k!='cases'}));return
 before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir() if p.is_file()};save('package-before.json',before)
 batch=load(E.parent/'samples.json');save('batch.json',batch)
 # Independent small sample, deliberately distinct seeds, plus controlled cases.
 fresh=[g.generate('hard',seed) for seed in range(800,824)]
 base={'b':3,'c':1,'a':2,'n':1,'k':0,'l':0,'d':1,'point':'-1'}
 params=[base,{**base,'point':'0'},{**base,'a':-2,'point':'0'},{**base,'d':-1,'point':'1'},{**base,'b':4}]
 controlled=[g.generate('hard',71+i,parameters=p) for i,p in enumerate(params)]
 # Irrelevant bank-order counterfactual: same mathematical instance, different seed.
 controlled.append(g.generate('hard',901,parameters=base))
 save('fresh.json',fresh);save('controlled.json',controlled)
 current=load(E.parent/'source/source.json')['material']['kp'];sources=current[':knowledge-point/questions']+[current[':knowledge-point/canonical-example']]
 replay=[];replay_tests=[]
 for q in sources:
  qid=q[':question/math-academy-id'];p=g.default_params(qid)
  r=g.generate(g.SPECS[qid]['level'],77,template=qid,parameters=p,profile='historical:'+qid)
  replay.append(r)
  # Full banks compared mathematically, with independent derivative check.
  observed=q.get(':question/answer-fields',[])
  actual=[parse(a[':answer/value']) for a in choices(r)]
  banks=[]
  for field in observed:
   old=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
   banks.append(len(old)==len(actual) and all(any(s.simplify(a-b)==0 for b in actual) for a in old))
  replay_tests.append({'source_id':qid,'question_id':q[':question/id'],'generated_id':r['question'][':question/id'],'complete_banks_match':banks,'missing_source_solution':not q.get(':question/worked-solution'),'fieldless_source':not observed,'prompt_equal_after_declared_typography':f.normalize_prose(g.normalized(q[':question/problem']))==r['question'][':question/problem'] if observed else 'fieldless prompt has authored matching blank'})
 save('source-replay.json',replay);save('source-replay-results.json',replay_tests)
 allrecords=batch+fresh+controlled+replay
 math=[];boundaries=[];grader=[]
 for i,r in enumerate(allrecords):
  exp=expected(r);cs=choices(r);matches=[a[':answer/id'] for a in cs if s.simplify(parse(a[':answer/value'])-exp)==0]
  # q-340969 captured aliases are identical accepted entries, not a radio ambiguity.
  keyed=next(a for a in cs if a[':answer/id']==correct(r)); ok=s.simplify(parse(keyed[':answer/value'])-exp)==0
  math.append({'index':i,'id':r['question'][':question/id'],'expected':str(exp),'keyed':keyed[':answer/value'],'correct':ok,'matching_choices':len(matches)})
  for k in [':question/problem',':question/worked-solution']:
   f.validate_math_boundaries(r['question'][k],strict=True);f.validate_prose(r['question'][k]);boundaries.append({'index':i,'field':k,'passed':True})
  for field in r['question'][':question/answer-fields']:
   for a in field[':answer-field/choices']:
    if a[':answer/type']==':answer.type/text':f.validate_math_boundaries(a[':answer/value'],strict=True)
    else:f.validate_tex(a[':answer/value'])
    if a.get(':answer/feedback'):f.validate_math_boundaries(a[':answer/feedback'],strict=True)
  typ=r['question'][':question/answer-fields'][0][':answer-field/type']
  if typ.endswith('/radio'):
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id'] in matches else 'rejected','purpose':'independent derivative/tangent calculation, all bank options'} for a in cs]
  else:
   checks=[{'submitted':s.latex(exp).replace(r'\log',r'\ln'),'expected':'accepted','purpose':'independent symbolic result'}, {'submitted':s.latex(2*exp).replace(r'\log',r'\ln'),'expected':'rejected','purpose':'plausible doubled coefficient'}]
  grader.append({'label':str(i)+':'+r['generation']['template'],'record':r,'checks':checks})
 save('math-results.json',math);save('boundary-results.json',{'passed':True,'checks':boundaries,'text_choices':0,'feedback_fields':0,'emphasis':'No Markdown emphasis wrappers occur in the emitted fields; no hints/labels require emphasis.','tables':'Source and hard records have no tables/matrices.','currency_percentage':'Absent from source and generated vocabulary.'});save('grader-input.json',grader)
 hard_source=next(r for r in replay if r['generation']['template']=='q-107463')
 save('shortcut-results.json',{'fresh':probes(fresh),'batch':probes(batch),'controlled':probes(controlled),'original_complete_bank':probes([hard_source]),'by_point':{t:probes([r for r in fresh if r['generation']['parameters']['point']==t]) for t in ['-1','0','1'] if any(r['generation']['parameters']['point']==t for r in fresh)}})
 save('render-records.json',batch+controlled+[hard_source])
 save('sampling-results.json',{'fresh_seeds':[800,823],'count':len(fresh),'signs':dict(collections.Counter('positive' if r['generation']['parameters']['a']>0 else 'negative' for r in fresh)),'points':dict(collections.Counter(r['generation']['parameters']['point'] for r in fresh)),'bases':dict(collections.Counter(r['generation']['parameters']['b'] for r in fresh)),'rejections':g.REJECTIONS,'replay_equal':g.generate('hard',800)==fresh[0],'source_eligibility':load(E.parent/'source/source.json')['material']['source_eligibility'],'repair_history_present':(E.parent/'repair-history.json').exists(),'repair_preflight_present':(E.parent/'repair-preflight.json').exists()})
 save('package-after.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir() if p.is_file()})
 print(json.dumps({'records':len(allrecords),'math_failed':[v for v in math if not v['correct']],'source_bank_mismatches':[v for v in replay_tests if not all(v['complete_banks_match'])],'shortcut_fresh':probes(fresh)['correct'],'shortcut_batch':probes(batch)['correct']}))
if __name__=='__main__':main()
