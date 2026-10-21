import sys,json,pathlib,importlib.util,collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'workspace';sys.path.insert(0,str(P))
spc=importlib.util.spec_from_file_location('current_generator',P/'17592186115241.py');g=importlib.util.module_from_spec(spc);spc.loader.exec_module(g)
from independent_math import vec,field,correct,mathcheck,sp

def dump(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def probe(r):
 cs=field(r)[':answer-field/choices'];indices=[i for i,c in enumerate(cs) if '\\frac' in c[':answer/value']]
 return {'cue':'only answer choice containing a printed fraction','candidate_positions':[i+1 for i in indices],'applicable':len(indices)==1,'selected_answer_id':cs[indices[0]][':answer/id'] if len(indices)==1 else None,'correct':len(indices)==1 and cs[indices[0]][':answer/id']==correct(r),'baseline':0.2}
# q-32244 is a captured rank-one source family with a half-integer intercept.
rr=[g.generate_easy(seed=seed,profile='q-32244') for seed in range(71380,71400)]
dump('source-shortcut-records.json',rr)
minimal=next(r for r in rr if probe(r)['applicable']);dump('minimal-fraction-shortcut.json',{'command':str(sys.executable)+' -B reproduce_shortcut.py','record':minimal,'probe':probe(minimal),'math':mathcheck(minimal),'construction':'generate_easy(seed=SEED, profile="q-32244"), no explicit parameters, uses ordinary source-variant bank.'})
dump('source-shortcut-results.json',{'command':str(sys.executable)+' -B shortcut_followup.py','profile':'q-32244','seeds':[71380,71399],'cases':[{'seed':r['generation']['seed'],'probe':probe(r),'math':mathcheck(r)} for r in rr],'total':len(rr),'conditional_attempts':sum(probe(r)['applicable'] for r in rr),'conditional_correct':sum(probe(r)['correct'] for r in rr),'rule':'When one choice has a printed fraction and the other four have none, select that choice without reading the equations.','reason':'candidate_bank pool only constructs Integer(c)+a*free; inserted correct source expression can be rational. Correct answer supplies unique representation cue.'})
print(json.dumps({'minimal_seed':minimal['generation']['seed'],'prompt':minimal['question'][':question/problem'],'choices':[(c[':answer/value'],c[':answer/id']==correct(minimal)) for c in field(minimal)[':answer-field/choices']],'total':len(rr),'conditional_attempts':sum(probe(r)['applicable'] for r in rr),'correct':sum(probe(r)['correct'] for r in rr)},indent=2))
