"""Independent checks of rendered coordinates, complete banks and all stages."""
import hashlib, importlib.util, itertools, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def expression(value): return g.parse_math(value.split('=')[-1])
def fingerprint(q): return g.fingerprint(q)
def check(r):
    q=r['question'];meta=r['generation'];p=meta['parameters'];profile=meta['profile']
    assert r==g.generate('easy',meta['seed'],profile,p,meta['replay'])
    prompt=q[':question/problem'];match=re.search(r'The \$(x|y)\$-coordinate of \$A\$ is \$(.+?)\$',prompt)
    known=match[1];given=expression(match[2].rstrip('.'));target='y' if known=='x' else 'x'
    assert known==p['known'] and sp.simplify(given**2)==sp.Rational(p['n'],p['d']**2)
    assert f'What is the ${target}$-coordinate' in prompt and 'first quadrant' in prompt and 'unit circle' in prompt
    assert given.is_positive and given<1
    fields=q[':question/answer-fields'];assert len(fields)==1
    f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
    assert len(f[':answer-field/choices'])==5
    choices=f[':answer-field/choices'];values=[expression(a[':answer/value']) for a in choices]
    for a in choices:
        assert a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value']
        assert (('=' in a[':answer/value'])==(profile in g.EQUATION_PROFILES))
        if '=' in a[':answer/value']: assert a[':answer/value'].split('=')[0]==target
    assert all(v.is_real and v.is_finite for v in values)
    assert all(sp.simplify(a-b)!=0 for a,b in itertools.combinations(values,2))
    correct=sp.sqrt(1-given**2);matches=[i for i,v in enumerate(values) if sp.simplify(v-correct)==0]
    assert len(matches)==1 and f[':answer-field/correct']==[':answer/id',choices[matches[0]][':answer/id']]
    assert sp.simplify(given**2+values[matches[0]]**2)==1 and values[matches[0]]>0
    sol=q[':question/worked-solution'];assert f'Substituting ${known}=' in sol and f'solving for ${target}$' in sol
    substitution=re.search(r'Substituting \$[xy]=(.+?)\$',sol)[1];assert expression(substitution)==given
    rows=sol.split('\\begin{aligned}')[1].split('\\end{aligned}')[0].split('\\\\')
    assert len(rows)==7
    rhs=[row.split('& =')[1].strip().rstrip('.') for row in rows]
    assert all(expression(v)==1 for v in rhs[:3])
    assert expression(rhs[3])==1-given**2 and expression(rhs[4])==1-given**2
    sqrt_rhs=rhs[5];assert sqrt_rhs.startswith('\\sqrt{')
    assert expression(sqrt_rhs)==correct and expression(rhs[6].replace('\\pm',''))==correct
    assert f'{{{target}}}^{{2}}' in rows[3] and f'{{{target}}}^{{2}}' in rows[4]
    assert target in rows[5].split('&')[0] and target in rows[6].split('&')[0]
    # Check the substituted left sides, not just the final key.
    lhs2=rows[1].split('&')[0].strip();lhs3=rows[2].split('&')[0].strip()
    assert f'{{{target}}}^{{2}}' in lhs2 and f'{{{target}}}^{{2}}' in lhs3
    assert g.tex(given) in lhs2 and g.tex(given**2) in lhs3
    assert f'Since $A$ lies in the first quadrant, ${target}$ must be positive' in sol
    final=re.search(r'final answer is \$[xy]=(.+?)\$',sol)[1];assert expression(final.rstrip('.'))==correct
    assert fingerprint(q)==meta['mathematical_fingerprint']
    return r
def native(label,r):
    f=r['question'][':question/answer-fields'][0]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],
        'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
        'purpose':'Every radio option through actual learner grader'} for a in f[':answer-field/choices']]}
def main():
    source=json.loads((HERE/'source.json').read_text());old=g.sources();replays=[];inputs=[];review=[]
    for sid,p in g.SOURCE_PARAMETERS.items():
        r=check(g.generate('easy',0,sid,p,True));f=old[sid][':question/answer-fields'][0]
        assert r['question'][':question/problem']==old[sid][':question/problem']
        original=f[':answer-field/choices'];rendered=r['question'][':question/answer-fields'][0][':answer-field/choices']
        match=[]
        for a in original:
            hits=[b for b in rendered if sp.simplify(expression(a[':answer/value'])-expression(b[':answer/value']))==0]
            assert len(hits)==1;match.append({'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'rendered_value':hits[0][':answer/value']})
        assert len(original)==len(rendered)==5 and len({m['rendered_value'] for m in match})==5
        sourcekey=f.get(':answer-field/correct')
        if sourcekey:
            rf=r['question'][':question/answer-fields'][0];key=next(a for a in rendered if a[':answer/id']==rf[':answer-field/correct'][1])
            assert expression(sourcekey[':answer/value'])==expression(key[':answer/value'])
        replays.append({'source':sid,'source_db_id':old[sid][':db/id'],'profile':sid,'bank_matched':True,'choices_matched':5,'choices_total':5,'mappings':match,'correct_designation':'matches source' if sourcekey else 'authored mathematically; source missing key',
            'source_difficulty':'easy' if old[sid].get(':question/difficulty') else 'unrated; easy classification authored for generator only',
            'source_solution':bool(old[sid].get(':question/worked-solution')),'missing_or_extra_options':[]})
        inputs.append(native(sid,r));review.append('## Source '+sid+'\n\n'+old[sid][':question/problem']+'\n\n'+(old[sid].get(':question/worked-solution') or 'No source worked solution.')+'\n\n### Parameter replay\n\n'+g.markdown(r))
    counts={};slots={};fps=set();pool=list(g.candidates('easy'))
    for entry in pool:
        profile=entry['profile'];p={k:v for k,v in entry.items() if k!='profile'}
        r=check(g.generate('easy',0,profile,p));counts[profile]=counts.get(profile,0)+1
        assert g.generate('easy',987,profile,p)['question']==r['question'],'Seed changed content/identity'
        inputs.append(native(str(entry),r));fps.add(fingerprint(r['question']))
        slots.setdefault(profile,{'n':set(),'d':set(),'known':set()})
        for k in p:slots[profile][k].add(p[k])
    assert set(counts)==set(g.SOURCE_PARAMETERS)
    for slot in slots.values(): assert slot['known']=={'x','y'} and slot['d']==set(range(3,9))
    changed=[]
    for profile,p in g.SOURCE_PARAMETERS.items():
        a=check(g.generate('easy',0,profile,p,True));other=dict(p,known='y' if p['known']=='x' else 'x')
        # Use the same numeric data at a normal-domain candidate for target checks.
        base=next(z for z in pool if z['profile']==profile);p={k:v for k,v in base.items() if k!='profile'};other=dict(p,known='y' if p['known']=='x' else 'x')
        a=check(g.generate('easy',0,profile,p));b=check(g.generate('easy',0,profile,other))
        assert a['question'][':question/problem']!=b['question'][':question/problem']
        assert a['question'][':question/worked-solution']!=b['question'][':question/worked-solution']
        assert fingerprint(a['question'])==fingerprint(b['question'])
        changed.append({'profile':profile,'parameters':p,'changed_target_parameters':other,'prompt_solution_key_verified':True,'counted_as_new_mathematics':False})
        review.append('## Changed target with fixed numbers: '+profile+'\n\n'+g.markdown(a)+'\n\n'+g.markdown(b))
    previews=g.batch('easy',5,2208)
    assert len({fingerprint(r['question']) for r in previews})==5
    for r in previews:check(r);review.append('## Fresh variant\n\n'+g.markdown(r))
    for level in ('moderate','hard'):
        try:g.batch(level,1)
        except ValueError:pass
        else:raise AssertionError('Unsupported band filled')
    save('source-replay.json',{'passed':True,'basis':source['basis'],'sources':replays,'source_choices_total':35,'source_choices_matched':35,'complete_banks_matched':7,'complete_banks_total':7,'missing_or_extra_options':[],'fidelity_limits':'Opaque distractor offsets are observed expression patterns; inferred recipes are not claimed as original author intent. Two source keys/ratings/solutions missing; derived only in new generator output.'})
    save('previews.json',previews);save('native-input.json',inputs)
    subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    evidence=(HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'check-engine',HERE/'check-engine.rs')
    save('validation.json',{'passed':True,'source_basis':source['basis'],'source_banks_matched':'7/7','source_choices_matched':'35/35','exhaustive_instances':len(pool),'counts_by_profile':counts,'distinct_bounded_mathematical_tasks':len(fps),
        'slot_coverage':{sid:{k:sorted(v) for k,v in slot.items()} for sid,slot in slots.items()},'changed_target_checks':changed,
        'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'math':'Independent printed-coordinate parsing; all complete banks, unique positive unit-circle key, substitution and seven solution stages; exact SymPy arithmetic.',
        'native_grading':'All five choices graded at every bounded instance; every generated question admitted by actual assessment_sampling::pool.',
        'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in evidence}})
    print('Validated',len(pool),'instances; distinct tasks',len(fps),'profiles',counts)
if __name__=='__main__':main()
