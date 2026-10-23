"""Fails if a current generated item can be solved by the demonstrated option-only cue.
Run: /home/jake/Developer/Course_Academy/.venv/bin/python shortcut_regression.py
No prompt, solution, generation metadata or key is consulted by predict().
"""
import sys,collections,json,itertools
sys.dont_write_bytecode=True
import audit

def predict(record):
    pairs=audit.optionpairs(record)
    f=[collections.Counter(p[i] for p in pairs) for i in range(2)]
    modes=[[x for x,n in counts.items() if n==max(counts.values())] for counts in f]
    # A visible conditional signature: first operation has unique mode appearing twice;
    # second operation also has a unique mode. Select their combined pair if present.
    if max(f[0].values())!=2 or any(len(mode)!=1 for mode in modes):return None
    target=tuple(mode[0] for mode in modes)
    ix=[i for i,pair in enumerate(pairs) if pair==target]
    return audit.choices(record)[ix[0]][':answer/id'] if len(ix)==1 else None

def probes(records):
    out=[]
    for i,r in enumerate(records):
        prediction=predict(r)
        out.append({'index':i,'question_id':r['question'][':question/id'],'profile':r['generation']['bank_profile'],'seed':r['generation']['seed'],'prediction':prediction,'correct':prediction==audit.correctid(r) if prediction else None,'pairs':audit.optionpairs(r)})
    return {'count':len(out),'attempts':sum(x['prediction'] is not None for x in out),'correct':sum(x['correct'] is True for x in out),'records':out}

if __name__=='__main__':
    rec=audit.m.generate(seed=842,bank_profile='q-91189',parameters={'A':[[4,2,-6],[1,3,4],[5,-1,2]],'row':0,'pivot':1,'ks':[-2,0,3]})
    audit.save('minimal-failure.json',[rec])
    prediction=predict(rec)
    permutations=[]
    for order in itertools.permutations(range(5)):
        variant=__import__('copy').deepcopy(rec);variant['question'][':question/answer-fields'][0][':answer-field/choices']=[audit.choices(rec)[i] for i in order]
        permutations.append(predict(variant)==audit.correctid(rec))
    audit.save('minimal-failure-results.json',{'parameters':rec['generation']['parameters'],'predicted_id':prediction,'actual_id':audit.correctid(rec),'all_120_choice_permutations_succeed':all(permutations),'independent_math':audit.check(rec)})
    assert prediction!=audit.correctid(rec), 'INCIDENTAL SHORTCUT: unique most frequent component pair answers the question without reading matrices (all 120 option orders).'
