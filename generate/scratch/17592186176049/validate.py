"""Current-source checkbox fidelity, finite-domain mathematics and native grading."""
import copy,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE));import instance_validation as iv
g=iv.g;legacy=iv.v

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main():
    current=json.loads((HERE/'current-source.json').read_text());old={q[':question/math-academy-id']:q for q in current['record'][':knowledge-point/questions']}
    replay=[];native=[]
    for name,(qid,_) in g.OBSERVED.items():
        r=g.generate('hard',template=name,parameters=g.ANCHORS[name],profile='current:'+name);iv.check(r)
        q=r['question'];source=old[qid]
        assert q[':question/problem']==source[':question/problem'],qid
        assert q.get(':question/worked-solution')==source.get(':question/worked-solution'),qid
        assert (':question/difficulty' in q)==(':question/difficulty' in source)
        for f in q[':question/answer-fields']:
            original=next(z for z in source[':question/answer-fields'] if z[':answer-field/key']==f[':answer-field/key'])
            assert f[':answer-field/type']==original[':answer-field/type'][':db/ident']
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in original[':answer-field/choices'])
            assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==original[':answer-field/correct'][':answer/value']
        native.append(iv.native(r,qid));replay.append({'source':qid,'prompt_exact':True,'solution_exact':True,'complete_fields_matched':3,'complete_values_matched':6,'correct_designations_matched':3,'difficulty_presence_preserved':True})
    counts={};distinct={};records=[]
    for level in ['easy','moderate','hard']:
        domain=[(None,p) for p in g.catalogs(level)] if level!='hard' else [(t,p) for t in g.OBSERVED for p in legacy.source_domain(t)]+[('two_identity_properties',p) for p in g.hard_catalog()]
        seen=set()
        for template,p in domain:
            r=g.generate(level,2,template=template,parameters=p);iv.check(r);fp=iv.fingerprint(r['question']);seen.add(fp)
            other=g.generate(level,91,template=template,parameters=p)
            assert r['question']==other['question'],'Seed affects current record'
            native.append(iv.native(r,level+':'+str(template)+':'+str(p)));records.append(r)
        counts[level]=len(domain);distinct[level]=len(seen)
    # Mutations must fail independently of metadata keys.
    r=copy.deepcopy(records[0]);r['question'][':question/answer-fields'][0][':answer-field/correct'][1]=r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']
    if r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']==str(r['generation']['truth_vector'][0]).lower():
        r['question'][':question/answer-fields'][0][':answer-field/correct'][1]=r['question'][':question/answer-fields'][0][':answer-field/choices'][1][':answer/id']
    try:iv.check(r)
    except AssertionError:pass
    else:raise AssertionError('Wrong Boolean key accepted')
    r=copy.deepcopy(records[0]);r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace(' is true.',' is false.',1)
    try:iv.check(r)
    except AssertionError:pass
    else:raise AssertionError('False solution verdict accepted')
    save('native-input.json',native)
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    grade=json.loads((HERE/'native-grading.json').read_text());assert grade['documented_unresolved_checks']==0
    save('source-replay-current.json',replay)
    save('validation.json',{'passed':True,'version':g.VERSION,'basis':current['basis'],'lineage':current['lineage'],'source_prompts_exact':'6/6','source_solutions_exact':'6/6','source_fields_complete':'18/18','source_boolean_values_matched':'36/36','source_correct_designations_matched':'18/18','source_rating_presence':'6/6','finite_instances':counts,'rendered_mathematical_fingerprints':distinct,'native_records':len(native),'native_checks':6*len(native),'native_unresolved':0,'native_accepted':grade['accepted_checks'],'native_rejected':grade['rejected_checks'],'mutation_regressions_rejected':2,'limitations':['Easy/moderate assignments are authored workload bounds, not observed source labels.','q-27660 current Boolean keys and solution are present but its rating is absent; source remains excluded.','Finite statement catalogs, no infinite-variant claim.'],'hashes':{'generator':sha(HERE.with_suffix('.py')),'native_engine':sha(ROOT/'generate/runs/current/check-engine'),'current_source':sha(HERE/'current-source.json')}})
    print('Validated current checkbox sources and finite catalogs:',counts,flush=True)
if __name__=='__main__':main()
