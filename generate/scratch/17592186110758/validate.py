"""Independent printed-coordinate, full-bank, solution and actual grader checks."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def expression(t):return g.parse_math(t.replace('\\cdot','*'))
def fingerprint(q):return g.fingerprint(q)
def check(r):
 q=r['question'];p=r['generation']['parameters'];profile=r['generation']['bank_profile'];text=q[':question/problem']
 m=re.search(r'Given that the \$([xy])\$-coordinate.*? is \$(.*?)(?:,\$|\$)',text);assert m
 given=expression(m[2]);assert 0<given<1
 assert m[1]==p['known'] and sp.simplify(given**2)==sp.Rational(p['n'],p['d']**2)
 assert re.search(r'(tan|cot)',text).group(1)==p['target']
 other=sp.sqrt(1-given**2);x,y=(given,other) if m[1]=='x' else (other,given)
 correct=sp.simplify(y/x if p['target']=='tan' else x/y)
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 bank=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(bank)==5 and all(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'] for a in f[':answer-field/choices'])
 assert (len(set(map(str,bank)))==5 or profile=='q-64730' and not r['generation']['eligible_for_learning']) and all(v.is_real and v.is_finite for v in bank)
 hits=[i for i,v in enumerate(bank) if sp.simplify(v-correct)==0];assert len(hits)==1
 if profile=='q-65072':
  expected=[1/other,given,other,correct,1/correct]
 elif profile=='q-124789':
  n,d=sp.Integer(p['n']),sp.Integer(p['d']);m=d*d-n
  expected=[sp.sqrt(n+40)/m,sp.sqrt(n+1)/m,1/correct,sp.sqrt(n)/m,correct]
 else:
  assert p==g.DATA[profile]
  expected=[expression(a[':answer/value']) for a in g.sources()[profile][':question/answer-fields'][0][':answer-field/choices']]
 assert len(expected)==len(bank) and all(sp.simplify(a-b)==0 for a,b in zip(expected,bank))
 if ':answer-field/correct' in f:assert f[':answer-field/correct']==[':answer/id',f[':answer-field/choices'][hits[0]][':answer/id']]
 if q.get(':question/worked-solution'):
  sol=q[':question/worked-solution'];assert 'Pythagorean identity' in sol and 'positive in the first quadrant' in sol
  assert given==expression(re.search(r"given that \$[xy]=(.+?)\$",sol)[1])
  conclusion=sol.split('=')[-1].split('\\end{aligned}')[0].split('$$')[0].strip().rstrip('.')
  assert expression(conclusion)==correct,(profile,conclusion,correct)
  if profile in g.PRIMARY.values():
   blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
   assert len(blocks)==(2 if p['level']=='easy' else 3)
   ratios=re.findall(r'\\frac\{(\d+)\}\{(\d+)\}',blocks[1]);assert len(ratios)>=2
   offset=1 if p['level']=='easy' else 0
   assert sp.Rational(*map(int,ratios[offset]))==given**2 and sp.Rational(*map(int,ratios[offset+1]))==1-given**2
   chosen=re.search(r'So, \$cos.*?=(.+?)\.\$',sol);assert chosen and expression(chosen[1])==other
   assert ('rationalize the denominator' in sol)==(p['level']=='moderate')
 if p['level'] and profile!='q-64730':
  assert r['generation']['eligible_for_learning'] and ':answer-field/correct' in f
 assert fingerprint(q)==r['generation']['mathematical_fingerprint']
 return r
def native(label,r):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'All five independently verified radio values'} for a in f[':answer-field/choices']]}
def main():
 src=g.sources();replays=[];inputs=[];review=[]
 for sid,p in g.DATA.items():
  r=check(g.generate(p['level'],0,profile=sid,parameters=p,replay=True));q=r['question'];old=src[sid];f=q[':question/answer-fields'][0];sf=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution')
  assert (':question/difficulty' in q)==(':question/difficulty' in old)
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in sf[':answer-field/choices']]
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  if ':answer-field/correct' in sf:
   canonical=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert canonical==sf[':answer-field/correct'][':answer/value']
   if r['generation']['eligible_for_learning']:inputs.append(native(sid,r))
  replays.append({'source':sid,'bank_profile':sid,'complete_bank_matched':True,'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'prompt_exact':True,'solution_exact':True if q.get(':question/worked-solution') else None,'correct_designation_preserved':True,'missing_or_extra_options':[]})
  review.append('## Source replay '+sid+'\n\n'+g.markdown(r))
 counts={};slots={};fps={};records=[]
 # Finite domains checked exhaustively; all printed math and owned radio choices.
 for level in g.SUPPORTED_LEVELS:
  counts[level]={};slots[level]={'n':set(),'d':set()};fps[level]=set()
  for entry in g.candidates(level):
   r=check(g.generate(level,0,profile=entry['profile'],parameters=entry['parameters']));records.append(r)
   assert g.generate(level,999,profile=entry['profile'],parameters=entry['parameters'])['question']==r['question']
   inputs.append(native(str(entry),r));fps[level].add(fingerprint(r['question']));counts[level][entry['profile']]=counts[level].get(entry['profile'],0)+1
   for k in slots[level]:slots[level][k].add(entry['parameters'][k])
  expected_d=({5,7,8,9,10,13,15,17,20,25,26,29,30} if level=='easy' else set(range(3,9)))
  assert slots[level]['d']==expected_d,slots[level]
 for r in records[:1]+[r for r in records if r['generation']['parameters']['level']=='moderate'][:1]:
  for what in ('prompt','key','solution','choice'):
   bad=copy.deepcopy(r);q=bad['question'];f=q[':question/answer-fields'][0]
   if what=='prompt':q[':question/problem']=q[':question/problem'].replace('Given that','Given that the $x$-coordinate is $999$. Given that',1)
   if what=='key':f[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])]
   if what=='solution':q[':question/worked-solution']=q[':question/worked-solution'].rsplit('=',1)[0]+'=999.\n$$'
   if what=='choice':f[':answer-field/choices'][0][':answer/value']='999'
   try:check(bad)
   except (AssertionError,ValueError,AttributeError):pass
   else:
    if what=='choice':
     # A distinct wrong distractor is mathematically possible, but violates bank fidelity.
     assert bad!=g.generate(bad['generation']['parameters']['level'],bad['generation']['seed'],profile=bad['generation']['bank_profile'],parameters=bad['generation']['parameters'])
    else:raise AssertionError('Undetected '+what)
 try:g.batch('hard',1)
 except ValueError:pass
 else:raise AssertionError('Unsupported hard emitted')
 # Previews intentionally span both n and d and source templates.
 previews=g.batch('easy',8,2209)+g.batch('moderate',12,2209)
 for r in previews:check(r);review.append('## Fresh '+r['generation']['parameters']['level']+' variant\n\n'+g.markdown(r))
 save('previews.json',previews);save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('source-replay.json',{'passed':True,'basis':json.loads((HERE/'source.json').read_text())['basis'],'complete_banks_matched':8,'complete_banks_total':8,'choices_matched':40,'choices_total':40,'distractors_matched':32,'distractors_total':32,'sources':replays,'incomplete_evidence_only':['q-64974'],'unresolved_author_intent':['q-124789 offsets +40 and +1 preserve observed full expressions; original misconceptions are unidentifiable']})
 save('review.json',previews);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 evidence=[HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'check-engine',HERE/'check-engine.rs',HERE/'previews.json']
 save('validation.json',{'passed':True,'source_banks_matched':'8/8','source_choices_matched':'40/40','counts_by_profile':counts,'exhaustive_instances':len(records),'distinct_bounded_mathematical_tasks':{l:len(v) for l,v in fps.items()},'slot_coverage':{l:{k:sorted(v) for k,v in s.items()} for l,s in slots.items()},'supported_levels':list(g.SUPPORTED_LEVELS),'unsupported_levels':['hard'],'native_grading':json.loads((HERE/'native-grading.json').read_text())|{'records':'Saved in native-grading.json'},'source_omissions_preserved':True,'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in evidence}})
 print(json.dumps({'passed':True,'instances':len(records),'finite_tasks':{l:len(v) for l,v in fps.items()}}))
if __name__=='__main__':main()
