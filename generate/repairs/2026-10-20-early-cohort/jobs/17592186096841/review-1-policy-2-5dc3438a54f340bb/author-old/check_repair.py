"""Executable regression for 1f66e48744758180770f; no runtime mutations."""
from test_support import *
from collections import Counter

OUT=E/'evidence'
OUT.mkdir(exist_ok=True)
def write(name,data):
 (OUT/name).write_text(json.dumps(data,indent=2,default=str))
def function(r):
 return parse(re.search(r'f\(x\)\s*=\s*(.*?)\$',r['question'][':question/problem'])[1].rstrip('.,'))
def verify(r):
 result=check_record(r)
 assert all(result[k] for k in ('key_correct','unique_correct','distinct')),result
 if r['generation']['template']=='quartic_radio':
  f=function(r);inner,n=f.args
  solution=r['question'][':question/worked-solution']
  inner_line=re.search(r'g=([^$]+)',solution)[1].strip()
  assert s.expand(parse(inner_line)-inner)==0
  di_line=re.search(r'\\frac\{\\text\{d\}g\}\{\\text\{d\}x\}=([^$]+)',solution)[1].strip().rstrip('.')
  assert s.expand(parse(di_line)-s.diff(inner,x))==0
  final=solution.split('&=')[-1].split(r'\end')[0].rstrip('.')
  assert s.expand(parse(final)-s.diff(f,x))==0
 return result

def coverage(records):
 groups={}
 for r in records:
  if r['generation']['template']!='quartic_radio':continue
  f=function(r);inner,n=f.args
  degree=min(m[0] for m,c in s.Poly(inner,x).terms())
  q=r['question'];choices=q[':question/answer-fields'][0][':answer-field/choices'];key=correct(q)
  factors=[int(re.match(r'\d+',a[':answer/value'])[0]) for a in choices]
  leads=[abs(s.Poly(s.cancel(parse(a[':answer/value'])/inner**(n-1)/o),x).coeff_monomial(x**3)) for a,o in zip(choices,factors)]
  idx=choices.index(key);sr=sorted(set(leads)).index(leads[idx]);orr=sorted(set(factors)).index(factors[idx])
  info=groups.setdefault(str(degree),{'count':0,'positions':Counter(),'leading_ranks':Counter(),'outer_ranks':Counter(),'shortest':0,'longest':0,'lex_first':0,'lex_last':0})
  info['count']+=1
  for k,v in [('positions',idx),('leading_ranks',sr),('outer_ranks',orr)]:info[k][str(v)]+=1
  values=[a[':answer/value'] for a in choices];v=key[':answer/value']
  lengths=list(map(len,values))
  info['shortest']+=len(v)==min(lengths) and lengths.count(len(v))==1;info['longest']+=len(v)==max(lengths) and lengths.count(len(v))==1
  info['lex_first']+=v==min(values);info['lex_last']+=v==max(values)
 for degree,info in groups.items():
  for k in ['positions','leading_ranks','outer_ranks']:assert len(info[k])>1,(degree,k,info)
  for k in ['shortest','longest','lex_first','lex_last']:assert info[k]<info['count'],(degree,k,info)
 return groups

def main():
 # Original seed and coefficients; the explicit degree slot repairs the missing input.
 pairs=[g.generate_moderate(99173,'quartic_radio',parameters=dict(a=3,b=1,n=5,second_power=k)) for k in (1,3)]
 assert s.expand(function(pairs[1])-(3*x**4+x**3)**5)==0
 assert s.expand(function(pairs[0])-(3*x**4+x)**5)==0
 assert pairs[0]['generation']['bank_design']==pairs[1]['generation']['bank_design']
 assert s.expand(expected(pairs[0]['question'])-expected(pairs[1]['question']))!=0
 # Legacy explicit parameters must continue to replay the linear family.
 legacy=g.generate_moderate(99173,'quartic_radio',parameters=dict(a=3,b=1,n=5))
 assert s.expand(function(legacy)-function(pairs[0]))==0
 # Reordering choices preserves the response (and is tested by native IDs).
 import copy
 reordered=copy.deepcopy(pairs[1]);reordered['question'][':question/answer-fields'][0][':answer-field/choices'].reverse()
 assert expected(reordered['question'])==expected(pairs[1]['question'])
 boundaries=[]
 for k in (1,3):
  for a,b,n in [(-3,-6,2),(1,6,6)]:
   for profile in ['authored_quartic','observed_48625']:
    boundaries.append(g.generate_moderate(42,'quartic_radio',parameters=dict(a=a,b=b,n=n,second_power=k),profile=profile))
 normal=[g.generate_moderate(seed,'quartic_radio') for seed in range(100,136)]
 assert set(coverage(normal))=={'1','3'}
 easy=[g.generate_easy(seed) for seed in range(810,815)]
 source_cases=list(g.SOURCE_CASES)+[('q-132770','quadratic_derivative',dict(a=1,b=3,n=2),None),('q-132994','quadratic_derivative',dict(a=1,b=1,n=3),None)]
 replay=[];source_results=[]
 for sid,name,p,profile in source_cases:
  r=g.generate(g.TEMPLATES[name][0],551,template=name,parameters=p,profile=profile);replay.append(r)
  orig=g.SOURCES[sid];of=orig[':question/answer-fields'][0]
  original=[str(s.expand(parse(a[':answer/value']))) for a in of[':answer-field/choices']]
  actual=[str(s.expand(parse(a[':answer/value']))) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  if sid=='q-340690':original=[str(s.expand(parse(of[':answer-field/correct'][':answer/value'])))]
  assert sorted(original)==sorted(actual),(sid,original,actual)
  source_results.append({'source':sid,'complete_bank':True,'choices':len(actual),'note':'Exclude documented incorrect extra blank alternative' if sid=='q-340690' else ''})
 all_records=pairs+[reordered]+boundaries+normal+easy+replay
 math_results=[verify(r) for r in all_records]
 write('counterfactual-records.json',pairs+[reordered]);write('quartic-records.json',normal)
 write('easy-records.json',easy);write('source-replays.json',replay)
 write('source-replay-results.json',source_results);write('math-results.json',math_results)
 write('coverage-before.json',coverage(normal))
 write('grader-input.json',[make_grading(r,str(i)) for i,r in enumerate(pairs+[reordered]+boundaries+easy+replay)])
 write('render-records.json',pairs+[boundaries[0],easy[0]])
 write('summary.json',{'finding':'1f66e48744758180770f','math_checks':len(all_records),'source_replays':len(replay),'normal_quartic_samples':len(normal),'canonical_replay':True,'controlled_degree_change':True,'legacy_linear_replay':True})
 print(json.dumps(json.loads((OUT/'summary.json').read_text())))

if __name__=='__main__':main()
