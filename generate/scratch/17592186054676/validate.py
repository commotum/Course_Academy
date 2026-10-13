"""Validate visible equations, coordinates, entire subset banks and native grading."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def selected(value):return set(re.findall(r'\$([ABC])\$',value))
def fingerprint(q):
    text=q[':question/problem'];eq=re.search(r'y\s*=\s*([^$?]+)',text)[1].rstrip('.')
    x=s.Symbol('x');expr=s.sympify(eq.replace('x','*x').lstrip('*'))
    coords=re.findall(r'([ABC])=?\((-?\d+),(-?\d+)\)',q.get(':question/worked-solution',''))
    if not coords:return hashlib.sha256(text.encode()).hexdigest()
    points={a:(int(b),int(c)) for a,b,c in coords}
    task=json.dumps({'equation':[int(expr.coeff(x)),int(expr.subs(x,0))],'points':[list(points[a]) for a in 'ABC'],'response':'point-subset'},sort_keys=True)
    return hashlib.sha256(task.encode()).hexdigest()
def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every complete source-bank choice through native learner grader'} for a in f[':answer-field/choices']]
def independent(rec):
    q,md=rec['question'],rec['generation'];p=md['parameters'];level=q[':question/difficulty'].split('/')[-1]
    assert rec==g.generate(level,md['seed'],md['template'],p,md['bank_profile'])
    assert fingerprint(q)==md['task_fingerprint']
    x=s.Symbol('x');eq=re.search(r'y\s*=\s*([^$?]+)',q[':question/problem'])[1].rstrip('.')
    expr=s.sympify(eq.replace('x','*x').lstrip('*'))
    truth={a for a,(xx,y) in zip('ABC',p['points']) if expr.subs(x,xx)==y}
    f=q[':question/answer-fields'][0];banks=[selected(a[':answer/value']) for a in f[':answer-field/choices']]
    correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    assert selected(correct[':answer/value'])==truth and sum(v==truth for v in banks)==1
    assert len({tuple(sorted(v)) for v in banks})==5
    for (xx,y),block in zip(p['points'],re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)):
        last=block.split(r'\\')[-1];match=re.search(r'(-?\d+) & =(-?\d+)',last)
        assert match and int(match[1])==y and int(match[2])==expr.subs(x,xx)
        assert ('✓' in block)==(y==expr.subs(x,xx))
    for text in (q[':question/problem'],q[':question/worked-solution']):assert text.count('$')%2==0 and text.count('{')==text.count('}')
    assert not any('$' in a[':answer/id'] for a in f[':answer-field/choices'])
    if p!=g.DEFAULTS[md['template']]:assert Path(md['plot_path']).is_file()
def main():
    records=[];cases=[]
    for level,m in g.TEMPLATES.items():
        rec=g.generate(level,template=m,parameters=g.DEFAULTS[m]);independent(rec)
        old=g.SOURCES[m];q=rec['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
        assert q[':question/problem']==old[':question/problem']
        assert q[':question/worked-solution']==old[':question/worked-solution'],(m,q[':question/worked-solution'])
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
        assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
        cases.append({'source':m,'complete_bank':True,'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'missing':[],'extra':[],'exact_prompt':True,'exact_solution':True})
        records.append(rec)
        for variant in g.batch(level,30,2027):independent(variant);records.append(variant)
        # Explicit boundary cases include zero shifts, both signs and sampler extrema.
        for slope,b,xs in itertools.product(([1,4] if level=='easy' else [-2,-5]),[-4,0,6],[[-3,-1,0],[0,1,3]]):
            points=[[x,slope*x+b+(0 if (i in (0,2) if level=='easy' else i==2) else 1)] for i,x in enumerate(xs)]
            if all(-10<=y<=10 for x,y in points):
                r=g.generate(level,parameters={'m':slope,'b':b,'points':points});independent(r);records.append(r)
    save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    save('source-cases.json',cases);save('review.json',{'source_replays':[r for r in records if r['generation']['parameters']==g.DEFAULTS[r['generation']['template']]],'variants':records})
    (HERE/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records[:4]))
    script=str(HERE.with_suffix('.py').relative_to(ROOT))
    save('validation.json',{'status':'pass','source_basis':2027,'complete_source_banks':2,'matched_source_choices':10,'total_source_choices':10,'matched_source_distractors':8,'total_source_distractors':8,'exact_source_prompt_and_solution':True,'independent_checks':len(records),'grading':{k:engine[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'supported_levels':['easy','moderate'],'unrated_sources_excluded':['q-22405','q-44504'],'hashes':{script:hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest()}})
    print('Passed exact source replay, full bank coverage, independent substitution and native grading.')
if __name__=='__main__':main()
