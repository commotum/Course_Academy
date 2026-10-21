"""Prepare the precise fence additions and deduplicate changed TeX witnesses."""
import importlib,json,hashlib
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
analysis=importlib.import_module('reference.mathacademy.repairs.2026-10-19-fraction-fences-corpus.analyze')
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False,default=str)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run():
    candidates=json.loads((HERE/'candidate-changes.json').read_text());types={e[':db/id']:e[':answer/type'][':db/ident'] for [e] in json.loads((HERE/'answer-types.json').read_text())};owners=defaultdict(set)
    for a,q,f in json.loads((HERE/'answer-owners.json').read_text()):owners[a].add(q)
    questions=json.loads((HERE/'questions.json').read_text());tutorials=json.loads((HERE/'tutorials.json').read_text());answers=json.loads((HERE/'answers.json').read_text());current={e[':db/id']:e for e in tutorials+questions+answers}
    for q in questions:
        for f in q.get(':question/answer-fields',[]):
            for a in f.get(':answer-field/choices',[])+[f.get(':answer-field/correct',{})]:
                if ':db/id' in a:current[a[':db/id']]=a
    changes=[];excluded=[];witnesses={};by_witness=defaultdict(list)
    for c in candidates:
        e,a=c['entity'],c['attribute'];bare=a==':answer/value' and types[e]==':answer.type/math'
        assert e in current and current[e][a]==c['before'],('Snapshot mismatch',e,a)
        after=analysis.scale(c['before'],bare)
        if after==c['before']:excluded.append({'entity':e,'attribute':a,'reason':'Answer is text; no matching delimited math span.'});continue
        assert after==c['after'] or a==':answer/value'
        assert analysis.signature(c['before'])==analysis.signature(after)
        c={**c,'after':after,'bare_tex':bare,'owning_questions':sorted(owners[e]) if a.startswith(':answer/') else [e] if a.startswith(':question/') else []}
        change_index=len(changes);changes.append(c)
        old_spans=[c['before']] if bare else [m[0] for m in analysis.fmt.MATH.finditer(c['before'])]
        new_spans=[after] if bare else [m[0] for m in analysis.fmt.MATH.finditer(after)]
        assert len(old_spans)==len(new_spans)
        for old,new in zip(old_spans,new_spans):
            if old==new:continue
            size=0 if bare else 2 if old.startswith(('$$',r'\[',r'\(')) else 1
            before_tex=old[size:-size] if size else old;after_tex=new[size:-size] if size else new
            display=bare or old.startswith(('$$',r'\['));key=before_tex,after_tex,display
            if key not in witnesses:witnesses[key]=len(witnesses)
            by_witness[witnesses[key]].append(change_index)
    save('changes.json',changes);save('excluded.json',excluded)
    cases=[{'index':index,'before':before,'after':after,'display':display,'change_indices':by_witness[index]} for (before,after,display),index in witnesses.items()];save('math-cases.json',cases)
    summary={'passed':True,'fields':len(changes),'entities':len({c['entity'] for c in changes}),'by_attribute':dict(Counter(c['attribute'] for c in changes)),'affected_questions':len({q for c in changes for q in c['owning_questions']}),'tutorials':sum(c['attribute']==':tutorial/content' for c in changes),'unique_changed_math_spans':len(cases),'excluded_non_math_answers':len(excluded),'only_scalable_parentheses_added':True,'changes_sha256':sha(HERE/'changes.json'),'math_cases_sha256':sha(HERE/'math-cases.json')};save('preparation-summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
