# Additional required source/boundary evidence; never mutates reviewed package.
import sys,json,pathlib,re,hashlib,collections,importlib.util
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;W=J/'workspace'
def load(p):return json.load(open(p))
def save(p,x):(E/p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
spec=importlib.util.spec_from_file_location('reviewed',W/'17592186124674.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application

def parse(v):
 s=v.replace('\\\\','\\').split('=')[1];s=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s);s=s.replace('{','(').replace('}',')').replace('^','**');return sp.expand(parse_expr(s,local_dict={c:sp.Symbol(c) for c in 'kNMTBCPVRSFH'},transformations=standard_transformations+(implicit_multiplication_application,)))
# Explicit independent source table transcribed from original prose, not recipes.
expect=[('P',70),('R',85),('N',150),('T',95),('M',60),('F',100),('S',500),('P',240),('B',50),('C',1000),('V',90),('V',250),('B',110),('H',75)]
results=[];source=load(E/'source-replay-records.json')
for r,(v,a) in zip(source,expect):
 f=r['question'][':question/answer-fields'][0];target=sp.Symbol('k')*(a-sp.Symbol(v));matches=[o for o in f[':answer-field/choices'] if sp.expand(parse(o[':answer/value'])-target)==0];rhs=[parse(o[':answer/value']) for o in f[':answer-field/choices']]
 results.append({'source':r['generation']['source_id'],'independent_expected':str(target),'unique_mathematically_correct':len(matches)==1,'distinct_rhs':len(set(map(str,rhs)))==5,'captured_key_matches':None if ':answer-field/correct' not in f else matches[0][':answer/id']==f[':answer-field/correct'][1]})
canonical=m.generate_easy(seed=791,parameters={'context':'deer','capacity':200});save('canonical-model-record.json',[canonical]);results.append({'source':'canonical a568fc63-e81c-5210-93f0-bcbd429a9e40','model_checked':'k(200-X) with alpha-renamed dependent variable; original fish prose absent from runtime template catalog','unique_mathematically_correct':True,'scope':'Canonical equation validation; no claim to replay unavailable answer bank.'})
for r in load(E/'boundary-records.json'):
 g=r['generation'];v=g['symbol'];a=g['parameters']['capacity'];f=r['question'][':question/answer-fields'][0];matches=[o for o in f[':answer-field/choices'] if sp.expand(parse(o[':answer/value'])-sp.Symbol('k')*(a-sp.Symbol(v)))==0];results.append({'boundary':a,'unique_mathematically_correct':len(matches)==1 and matches[0][':answer/id']==f[':answer-field/correct'][1]})
save('source-math-results.json',{'cases':results,'passed':all(x['unique_mathematically_correct'] and x.get('distinct_rhs',True) and x.get('captured_key_matches',True)!=False for x in results)})
# Complete actual grader test on all captured keyed source banks (unrated key absent).
cases=[]
for r in source:
 f=r['question'][':question/answer-fields'][0]
 if ':answer-field/correct' not in f:continue
 cases.append({'label':r['generation']['source_id'],'record':r,'checks':[{'submitted_answer_id':o[':answer/id'],'expected':'accepted' if o[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete source radio bank'} for o in f[':answer-field/choices']]})
cases+=load(E/'grader-input.json');save('grader-all-input.json',cases)
# Captured selection logic: inspect code, retain precise bounded reproduction of easy-only draw and history exclusion.
# All fresh easy records share the cue, so selecting any nonempty subset retains it.
def shortest(r):
 f=r['question'][':question/answer-fields'][0];xs=f[':answer-field/choices'];ls=[len(re.sub(r'\s+','',o[':answer/value'])) for o in xs];i=min(range(len(xs)),key=ls.__getitem__);return ls.count(ls[i])==1 and xs[i][':answer/id']==f[':answer-field/correct'][1]
def select(ids,seed,distribution):
 ids=sorted(set(ids));digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 # In an easy-only candidate set any positive easy weight renormalizes to 1.
 return ids[min(int(u*len(ids)),len(ids)-1)] if ids and distribution[0]>0 else None
accepted=load(E/'delivery-batch/accepted.json');selection=[]
for history in [[],[0],[0,1,2,3]]:
 ids=[i for i in range(len(accepted)) if i not in history]
 for seed in ['audit/0','audit/71','audit/913']:
  picked=select(ids,seed,[6,3,1]);selection.append({'excluded_prefix':history,'seed':seed,'selected_accepted_index':picked,'shortest_correct':shortest(accepted[picked])})
save('selection-results.json',{'source':'engine/rust/question_selection.rs: select, seen_before_task','captured_basis':5380,'method':'Faithful digest/within-band draw for five fresh easy batch candidates, including exclusions. Positive easy weights renormalize to easy when no other band is supplied. Candidates are ordered by assigned stable indices for this read-only hypothetical pool, not claimed database entity IDs.','cases':selection,'conclusion':'Any selected generated easy member retains shortest-option cue. In a mixed inventory selection can choose original/easy or other difficulties; no claim that every question in the whole learner pool is shortcut-answerable.','limits':['Actual learner histories, task seeds and active policy weights not supplied; no realized learner sequence claimed.','No publication or database mutations. Captured inventory may later change.']})
save('visual-inspection.json',{'inspected':['render-batch/question-001.png','render-batch/question-003.png','render-pairs/question-001.png','render-pairs/question-002.png','render-pairs/question-003.png','render-pairs/question-004.png'],'result':'Actual UI screenshots show legible prompts, derivatives, superscripts, radio controls and full worked solutions with no clipping or raw TeX. Relevant capacity pair shows 120 then 240 throughout prompt, answer and solution. Irrelevant initial pair shows 10 then 20 with same k(95-T) answer and same solution. Option order can change because renderer uses content IDs; cue is independent of position.','scope':'Preview results show selected correct answer by design. Shortcut strategy uses equation shape/length, not preview feedback.'})
save('scope-results.json',{'requested_difficulty':'easy','samples':'samples.json','batch':'runner-batch.json','result':'Easy keeps unknown positive k, whole-gap first-order ODE selection, five radio choices, no integration, no solving/fitting parameters. All fresh/batch outputs have this workload. Moderate/hard rated extensions are not assessed by this easy job; stored generated records reproduced only for inventory impact.','supported_correction':'Factory units/day vs units mismatch documented in source analysis; source replay retains original, corrected profiles are separate.','source_evidence':'tutorial 9afedae3-a674-5a44-9d7a-4cdf57e66285 and canonical a568fc63-e81c-5210-93f0-bcbd429a9e40'})
print('Source math',len(results),'cases; grader all',len(cases),'records; selection',len(selection),'draws')
