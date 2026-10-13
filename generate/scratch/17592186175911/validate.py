"""Parse printed mathematics independently and use actual learner grading."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=sp.Symbol('x',real=True)
def save(name,v): (HERE/name).write_text(json.dumps(v,indent=2)+'\n')
def expression(t):
    t=t.replace(' ','')
    t=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
    t=re.sub(r'(\d|\))x',r'\1*x',t)
    t=re.sub(r'(\d|\))\(',r'\1*(',t)
    return sp.expand(sp.sympify(t,locals={'x':x}))
def fingerprint(q): return g.fingerprint(q)
def check(r):
    q=r['question'];meta=r['generation'];p=meta['parameters'];level=q[':question/difficulty'].split('/')[-1]
    assert g.allowed(level,p) and meta['version']==g.VERSION
    assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    expected=g.generate(level,meta['seed'],meta['template'],p,meta['replay'])
    assert r==expected,'Generator content/stable identity mismatch'
    pairs=[tuple(map(int,z)) for z in re.findall(r'\((-?\d+),\s*(-?\d+)\)',q[':question/problem'])]
    (u,v),(a,b),(c,d)=pairs;m=sp.Rational(d-b,c-a);intercept=v-m*u
    assert pairs==[(p['u'],p['v']),(p['a'],p['b']),(p['c'],p['d'])]
    assert len(q[':question/answer-fields'])==1 and q[':question/problem'].endswith('$y =$\n{{field-1}}')
    f=q[':question/answer-fields'][0];assert f[':answer-field/key']=='field-1' and f[':answer-field/type']==':answer-field.type/blank'
    assert len(f[':answer-field/choices'])==1
    ans=f[':answer-field/choices'][0];value=expression(ans[':answer/value'])
    assert '=' not in ans[':answer/value'] and '$' not in ans[':answer/value']
    assert ans[':answer/type']==':answer.type/math' and f[':answer-field/correct']==[':answer/id',ans[':answer/id']]
    assert value==m*x+intercept and value.subs(x,u)==v and sp.diff(value,x)==m
    sol=q[':question/worked-solution']
    slope=re.search(r'&= (.*?)\n\\end\{aligned\}',sol)[1]
    assert expression(slope)==m
    expanded=re.findall(r'y - \([^)]*\) &= ([^\n]+) \\\\',sol)
    assert len(expanded)==2 and all(expression(t)==m*(x-u) for t in expanded)
    final=re.search(r'y &= ([^\n]+)',sol)[1];assert expression(final)==value
    assert f'point $({u},{v})$' in sol and fingerprint(q)==meta['mathematical_fingerprint']
    return r
def native(label,r):
    p=r['generation']['parameters'];m=sp.Rational(p['d']-p['b'],p['c']-p['a']);b=p['v']-m*p['u']
    return {'label':label,'record':r,'checks':[
      {'submitted':r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'],'expected':'accepted','purpose':'canonical LaTeX RHS'},
      {'submitted':f'({m})*(x-({p["u"]}))+({p["v"]})','expected':'accepted','purpose':'equivalent point-slope RHS'},
      {'submitted':str(m*x+b+1),'expected':'rejected','purpose':'wrong intercept'},
      {'submitted':str(-m*x+b),'expected':'rejected','purpose':'wrong slope'}]}
def main():
    source=json.loads((HERE/'source.json').read_text());old={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
    replays=[];inputs=[];review=[]
    for sid,p in g.SOURCE_PARAMETERS.items():
        level='easy' if p['u']==0 else 'moderate';r=check(g.generate(level,parameters=p,replay=True));f=old[sid][':question/answer-fields'][0]
        assert r['question'][':question/problem']==old[sid][':question/problem']
        assert f[':answer-field/key']=='field-1' and f[':answer-field/type'][':db/ident']==':answer-field.type/blank'
        assert ':answer-field/correct' not in f and not f.get(':answer-field/choices') and ':question/worked-solution' not in old[sid]
        replays.append({'source':sid,'parameters':p,'prompt_exact':True,'field_contract_exact':True,'source_bank_empty':True,'source_difficulty_absent':True,'answer_and_solution':'authored from exact mathematics and canonical move sequence'})
        inputs.append(native(sid,r));review.append('## Source replay '+sid+'\n\n'+g.markdown(r))
    counts={};fps=set()
    for level in ('easy','moderate'):
        pool=list(g.candidates(level));counts[level]=len(pool)
        for p in pool:
            r=check(g.generate(level,parameters=p));inputs.append(native(level+str(p),r));fps.add(fingerprint(r['question']))
            assert g.generate(level,99,parameters=p)['question']==r['question'],'Seed cannot change identity or content'
    previews=g.batch('easy',5,1946)+g.batch('moderate',5,1946)
    for r in previews: check(r);review.append('## Variant\n\n'+g.markdown(r))
    for level,p in [('hard',g.SOURCE_PARAMETERS['q-214094']),('easy',dict(u=0,v=1,a=2,b=1,c=2,d=3)),('moderate',dict(u=1,v=1,a=2,b=1,c=3,d=1))]:
        try: g.generate(level,parameters=p)
        except ValueError: pass
        else: raise AssertionError('Unsupported/degenerate input accepted')
    save('source-replay.json',{'passed':True,'basis':source['basis'],'sources':replays,'source_choices_total':0,'source_choices_matched':0,'missing_or_extra_options':[],'complete_observed_choice_banks':0,'limits':'No source keys, solutions, or ratings exist. Authored additions are not claimed as recovered fidelity.'})
    save('previews.json',previews);save('native-input.json',inputs)
    subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json',{'passed':True,'exhaustive_instances':sum(counts.values()),'counts':counts,'distinct_bounded_lines':len(fps),'supported_levels':['easy','moderate'],'math':'Independently parsed printed points, slope, every answer RHS, expanded solution RHS, final RHS, incidence and parallelism. Complete finite domain checked.','native_grading':'Canonical LaTeX and equivalent point-slope RHS accepted, incorrect intercept/slope rejected at every bounded tuple.','source_fidelity':'Both prompts and field layouts exact; empty banks faithfully accounted for; all keys/solutions/difficulty labels explicitly authored.','hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'check-engine')}})
    print('Validated',counts,'distinct lines',len(fps))
if __name__=='__main__': main()
