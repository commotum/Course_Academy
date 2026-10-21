import sys,json,re,collections
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
O=Path(__file__).resolve().parent
read=lambda x:json.loads((O/x).read_text())
def save(x,v):(O/x).write_text(json.dumps(v,indent=2)+'\n')
T,k=sp.symbols('T k')
def expr(v):
 rhs=v.split('=')[1].replace(' ','').replace('kT','k*T').replace('k(','k*(').replace('T(','T*(')
 return sp.sympify(re.sub(r'(\d)([Tk(])',r'\1*\2',rhs),locals={'T':T,'k':k})
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):
 x=field(r)[':answer-field/correct'];return x[1] if isinstance(x,list) else x[':answer/id']
records=read('normal-easy-records.json')+read('initial-endpoint-records.json')+read('samples.json')+read('batch.json')+read('counterfactual-records.json')+read('changed-counterfactual-records.json')+read('delivery-batch/accepted.json')+read('delivery-moderate/accepted.json')
cases=[]
for i,r in enumerate(records):
 q=r['question'];S=int(re.findall(r'\$\{(\d+)\}\^',q[':question/problem'])[-1]);target=-k*(T-S);choices=field(r)[':answer-field/choices'];hits=[a for a in choices if sp.expand(expr(a[':answer/value'])-target)==0]
 assert len(hits)==1 and hits[0][':answer/id']==key(r)
 assert f'-k(T-{S})' in q[':question/worked-solution']
 cases.append({'label':f'fresh-native-{i}','record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a in hits else 'rejected','purpose':'Equation independently derived from ambient in visible prompt'} for a in choices]})
save('all-grader-input.json',cases)
# All exact delivered batch items, both cake ambient cases, and turkey/soup relevant and irrelevant triples.
render=read('delivery-batch/accepted.json')+read('changed-counterfactual-records.json');save('actual-ui-records.json',render)
# Independent cue probes, per recognizable template and exact delivery set.
probes=[]
for dataset in ['samples.json','batch.json','delivery-easy/accepted.json','delivery-moderate/accepted.json','delivery-batch/accepted.json']:
 rows=read(dataset);groups={'ALL':rows}
 for r in rows:groups.setdefault(r['generation']['template'],[]).append(r)
 for group,rs in groups.items():
  for name in ['unique_shortest','unique_longest','first_position','last_position','one_minus','two_minus','no_plus','lexicographically_first']:
   correct=eligible=0
   for r in rs:
    choices=field(r)[':answer-field/choices'];rhs=[a[':answer/value'].split('=')[1] for a in choices]
    if name=='unique_shortest':sel=[i for i,s in enumerate(rhs) if len(s)==min(map(len,rhs))]
    elif name=='unique_longest':sel=[i for i,s in enumerate(rhs) if len(s)==max(map(len,rhs))]
    elif name=='first_position':sel=[0]
    elif name=='last_position':sel=[4]
    elif name=='one_minus':sel=[i for i,s in enumerate(rhs) if s.count('-')==1]
    elif name=='two_minus':sel=[i for i,s in enumerate(rhs) if s.count('-')==2]
    elif name=='no_plus':sel=[i for i,s in enumerate(rhs) if '+' not in s]
    else:sel=[rhs.index(min(rhs))]
    eligible+=len(sel)==1
    correct+=len(sel)==1 and choices[sel[0]][':answer/id']==key(r)
   probes.append({'dataset':dataset,'subgroup':group,'cue':name,'correct':correct,'total':len(rs),'unique_candidate':eligible,'baseline':0.2,'interpretation':'A tie/abstention counts as failure. Minus-count and no-plus use partial intended sign/form knowledge; inspect any perfect predictor before calling it incidental.'})
save('conditional-cue-probes.json',probes)
print(json.dumps({'records_math_checked':len(records),'native_responses':sum(len(x['checks']) for x in cases),'render_count':len(render),'perfect_probes':[p for p in probes if p['correct']==p['total']]}))
