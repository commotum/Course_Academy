"""Displayed arithmetic, complete banks, boundaries, and native radio grading."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sympy as s

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(name,obj):
    (HERE/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')

def expr(text):
    """Parse the small delimiter-free numeric answer language, not metadata."""
    text=text.strip().rstrip('.,').replace(' ','').replace('\\dfrac','\\frac')
    def group(t,i):
        assert t[i]=='{',t
        depth=1;j=i+1
        while depth:
            if t[j]=='{':depth+=1
            if t[j]=='}':depth-=1
            j+=1
        return t[i+1:j-1],j
    while '\\frac' in text:
        i=text.index('\\frac');num,j=group(text,i+5);den,k=group(text,j)
        text=text[:i]+'('+str(expr(num))+'/'+str(expr(den))+')'+text[k:]
    while '\\sqrt' in text:
        i=text.index('\\sqrt');num,j=group(text,i+5)
        text=text[:i]+'sqrt('+str(expr(num))+')'+text[j:]
    text=re.sub(r'(?<=\d)(?=sqrt|\()', '*',text)
    assert re.fullmatch(r'[0-9+*/().\-sqrt]+',text),text
    return s.simplify(s.sympify(text))

def displayed_task(q):
    text=q[':question/problem']
    coordinate=re.search(r'\$(x|y)\$-coordinate',text).group(1)
    given=expr(re.search(r'is \$([^$]+)\$',text).group(1))
    target='2cos2' if '2{cos}^{2}' in text else 'cos' if ('\\cos' in text or 'cos\u2061' in text) else 'sin'
    return coordinate,given,target

def fingerprint(q):
    coordinate,given,target=displayed_task(q)
    return hashlib.sha256((coordinate+'|'+s.srepr(given)+'|'+target+'|QI').encode()).hexdigest()

def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every bank option through actual learner radio grader'} for a in f[':answer-field/choices']]

def independent(rec):
    q=rec['question'];md=rec['generation'];m=md['template'];p=md['parameters']
    coordinate,given,target=displayed_task(q)
    assert 0<given<1
    expected=2*(1-given**2) if target=='2cos2' else s.sqrt(1-given**2)
    assert (coordinate,target)==(('y','2cos2') if m=='q-37915' else ('x','sin'))
    f=q[':question/answer-fields'][0]
    assert f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
    vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len(vals)==5 and len(set(vals))==5
    selected=next(expr(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
    assert s.simplify(selected-expected)==0
    assert sum(s.simplify(v-expected)==0 for v in vals)==1
    solution=q[':question/worked-solution']
    # Independently check the values actually rendered at every numerical stage.
    if m=='q-37915':
        a,b=p['a'],p['b'];assert given==s.sqrt(a)/b
        required=[g.tex(given),g.frac(a,b*b),g.frac(2*a,b*b),g.tex(expected)]
        assert '2-2' in solution and '2{cos}^{2}' in solution
    else:
        a,b=p['m'],p['n'];assert given==s.Rational(a,b)
        required=[g.frac(a,b),g.frac(a*a,b*b),g.frac(b*b-a*a,b*b),g.tex(expected)]
        assert 'select the positive answer' in solution and 'first quadrant' in solution
    assert all(t in solution for t in required),(m,p,required,solution)
    final=re.search(r'So our final answer is \$([^$]+)',solution).group(1)
    assert expr(final.split('=',1)[1])==expected
    for text in (q[':question/problem'],solution):
        assert text.count('$')%2==0 and text.count('{')==text.count('}')
        assert len(re.findall(r'!\[\]\([^)]+\)',text))==1
    assert all('$' not in a[':answer/value'] for a in f[':answer-field/choices'])
    assert len(set(a[':answer/id'] for a in f[':answer-field/choices']))==5
    # Published assets preserve original local files; verify their exact bytes.
    for asset in md['assets'].values():
        assert hashlib.sha256((ROOT/asset['path']).read_bytes()).hexdigest()==asset['sha256']
        x,y=map(s.sympify,asset['point']);assert s.simplify(x*x+y*y)==1 and x>0 and y>0
        assert (y if coordinate=='y' else x)==given
    replay=g.generate(q[':question/difficulty'].split('/')[-1],md['seed'],m,p,md['bank_profile'],md['source_replay'])
    def strip_assets(text):return re.sub(r'!\[\]\([^)]+\)','[diagram]',text)
    assert all(strip_assets(q[k])==strip_assets(replay['question'][k]) for k in (':question/problem',':question/worked-solution'))
    assert q[':question/answer-fields']==replay['question'][':question/answer-fields'] and q[':question/id']==replay['question'][':question/id']

def main():
    records=[];banks=[];review=[];coverage={}
    for m,p in g.DEFAULTS.items():
        level='moderate' if m=='q-37915' else 'easy'
        rec=g.generate(level,template=m,parameters=p,replay=True);independent(rec)
        old=g.SOURCES[m];q=rec['question'];f=q[':question/answer-fields'][0];oldf=old[':question/answer-fields'][0]
        assert all(q[k]==old[k] for k in (':question/problem',':question/worked-solution'))
        oldvals=[expr(a[':answer/value']) for a in oldf[':answer-field/choices']];newvals=[expr(a[':answer/value']) for a in f[':answer-field/choices']]
        assert len(oldvals)==len(newvals)==5 and set(oldvals)==set(newvals)
        assert expr(oldf[':answer-field/correct'][':answer/value'])==next(expr(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        banks.append({'source':m,'template':m,'profile':m,'matched_values':5,'total_values':5,'matched_distractors':4,'total_distractors':4,'missing':[],'extra':[],'exact_prompt':True,'exact_solution':True,'complete_bank':True,'mapping':[{'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'recipe_index':newvals.index(expr(a[':answer/value'])),'complete_value_replayed':True} for a in oldf[':answer-field/choices']]})
        records.append(rec);review.append('## Exact source replay '+m+'\n\n'+g.markdown(rec))
        ds=g.domain(m)
        # Cover the full bounded mathematical domain independently of rendering.
        for x in ds:
            given,correct,bank=g.values(m,x)
            assert s.simplify(correct-(2*(1-given**2) if level=='moderate' else s.sqrt(1-given**2)))==0
            assert len(set(bank))==5 and sum(s.simplify(v-correct)==0 for v in bank)==1
        selected=[ds[0],ds[-1]]+[ds[i*len(ds)//8] for i in range(8)]
        selected+=([{'m':2,'n':5},{'m':4,'n':5}] if m!='q-37915' else [{'a':3,'b':4},{'a':7,'b':4}])
        for x in selected:
            if not g.valid(m,x):continue
            r=g.generate(level,template=m,parameters=x);independent(r);records.append(r)
            assert r==g.generate(level,template=m,parameters=x)
        coverage[m]={'bounded_valid_parameters':len(ds),'rendered_cases':len(selected),'slot_values':{k:sorted({x[k] for x in ds}) for k in p},'no_unsampled_eligible_slot_values':True,'fixed_roles':'x to sin in QI' if level=='easy' else 'y to 2cos² in QI'}
        review.append('## Same-template variations '+m+'\n\n'+'\n\n---\n\n'.join(g.markdown(r) for r in records[-2:]))
    candidates=g.batch('easy',8,2210)+g.batch('moderate',8,2210)
    for r in candidates:independent(r)
    records+=candidates
    assert len({fingerprint(r['question']) for r in candidates})==len(candidates)
    save('engine-input.json',[{'label':str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)])
    binary=HERE/'check-engine'
    r=subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],capture_output=True,text=True)
    (HERE/'engine.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
    engine=json.loads((HERE/'engine-report.json').read_text());assert engine['documented_unresolved_checks']==0
    save('source-bank-replay.json',banks);save('slot-coverage.json',coverage);save('review.json',{'records':records});(HERE/'review.md').write_text('\n\n---\n\n'.join(review))
    save('validation.json',{'status':'pass','source_basis':g.CAPTURE['basis'],'complete_source_banks':len(banks),'matched_source_values':25,'matched_source_distractors':20,'missing_options':[],'extra_options':[],'excluded_sources':{'q-37821':'Unrated; no correct key or solution','q-64731':'Unrated; no correct key or solution'},'independent_display_checks':len(records),'fidelity':'Exact prompt, worked solution, complete mathematical banks and correct designation for every supported source profile. Unrated incomplete source banks preserved as evidence; not declared supported.','correctness':'Independently reconstructed target from displayed coordinate; all bounded bank domains, all numerical solution stages and first-quadrant plot points checked.','native_grading':{k:engine[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),Path(__file__),HERE/'source.json',binary)}})
    print('Passed exact replay of 5 banks, displayed mathematics, bounded slot domains, and native grading')

if __name__=='__main__':main()
