import sys,json,re,hashlib
sys.dont_write_bytecode=True
from audit import *
# Preserve the failure against an accepted expectation, then run the full batch with its actual documented outcome.
cases=json.loads((ROOT/'grader-input-final.json').read_text());cases[-1]['checks'][-1]['expected']='unresolved';cases[-1]['checks'][-1]['purpose']='DEMONSTRATED GAP: valid equivalent expected accepted; native engine instead unresolved; see grader-final.log and log-identity-proof.json'
save('grader-input-observed.json',cases)
canonical=json.loads((ROOT.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/canonical-example']
kw=dict(seed=517171,template='q-1907',parameters=dict(c=1,n=1,trig='cos'))
try:r=g.generate(**kw);out={'generated':r,'exception':None}
except Exception as e:out={'generated':None,'exception':repr(e)}
save('canonical-replay-gap.json',{'source_id':canonical[':question/id'],'source_ma_id':canonical[':question/math-academy-id'],'source_problem':canonical[':question/problem'],'source_solution':canonical[':question/worked-solution'],'attempt':kw,'outcome':out,'exhaustive_code_basis':'All public polynomial source profiles q-1907/q-104300/q-47965/q-319357 use bounds n=2..4; no linear factor profile exists. Other profiles use exponential, radical or k-tan factors.','response_limit':'Canonical response fields absent, so only factor/derivative coverage is asserted; no historical answer bank invented.','independent_derivative':str(S.diff(X*S.cos(X),X))})
# Enrich source replay with every available solution math fragment, independently parsing derivative notation.
# Compare normalized source math through independent parser; use u,v as abstract functions for the rule lines.
from audit import parse as updated_parse
ns={'parse':updated_parse}
ps=ns['parse'];source=json.loads((ROOT.parent/'source/source.json').read_text());replays=json.loads((ROOT/'source-replays.json').read_text());report=[]
def fragments(z):
 out=[]
 for q in maths(z):
  q=q.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  for row in q.split(r'\\'):
   for side in row.replace('&','').split('='):
    side=side.strip().rstrip('.').replace(r'\,','').rstrip(' +')
    if side:out.append(ps(side))
 return out
for q,r in zip(source['material']['kp'][':knowledge-point/questions'],replays):
 count=0
 for k in (':question/problem',':question/worked-solution'):
  if k not in q:continue
  a,b=fragments(q[k]),fragments(r['question'][k]);assert len(a)==len(b)
  for v,w in zip(a,b):assert eq(v,w),(q[':question/math-academy-id'],k,v,w)
  count+=len(a)
 report.append({'source':q[':question/math-academy-id'],'math_fragments':count,'passed':True})
save('source-fragment-results.json',{'cases':report,'total_fragments':sum(c['math_fragments'] for c in report),'source_typo_preserved_only_in_raw_replay':'q-319350 first LHS e^x sec x'})
# Render the actual failing base-4 instance too.
save('extra-render-input.json',json.loads((ROOT/'log-identity-samples.json').read_text()))
(ROOT/'session-state.md').write_text('Independent math suite passed 143 samples + runner five; all11 question-bank replays passed. Demonstrated missing canonical x cos x factor (n=1 excluded); see canonical-replay-gap.json. Native grader fails a valid base4 ln4=2ln2 equivalent with unresolved; see grader-final.log and log-identity-proof.json. Full observed-outcome grader batch next. UI render-all covers27 records; extra composite-base render follows. Decision/delivery/selection report pending. No package writes.\n')
print('source fragments',sum(c['math_fragments'] for c in report),'canonical gap',out['exception'])
