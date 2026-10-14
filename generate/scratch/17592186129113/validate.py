"""Independent coefficient-matrix oracle, rendered witnesses, bank replay, slots and real grading."""
import hashlib,importlib.util,itertools,json,re,subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('augmented_echelon_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,value): (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def parse(text):
    return [[[int(v.strip()) for v in row.split('&')] for row in body.split(r'\\')] for body in re.findall(r'\\begin\{array\}\{c+\|c\}(.*?)\\end\{array\}',text,re.S)]
def oracle(m): return bool(sp.Matrix([r[:-1] for r in m]).is_echelon)
def check(r):
    q=r['question'];meta=r['generation']
    assert r==g.generate('easy',meta['seed'],meta['profile'],meta['parameters'],meta['replay'])
    assert q[':question/difficulty']==':question.difficulty/easy' and r['knowledge_point']['db_id']==g.KP_ID
    ms=parse(q[':question/problem']);assert ms==meta['parameters']['matrices'] and parse(q[':question/worked-solution'])==ms and len(ms)==3
    if not meta['replay']:
        assert 'have coefficient matrices' in q[':question/problem'] and 'Treat the final column' in q[':question/problem']
    assert q[':question/problem'].endswith('Select all that apply.')
    verdicts=re.findall(r'- The (?:coefficient matrix of|matrix) \$([ABC])\$\s+is (not in|in) row echelon form',q[':question/worked-solution'])
    assert verdicts==[(label,'in' if oracle(m) else 'not in') for label,m in zip('ABC',ms)],meta['profile']
    for label,m in zip('ABC',ms):
        c=[row[:-1] for row in m]
        sentence=re.search(r'- The (?:coefficient matrix of|matrix) \$'+label+r'\$.*?(?=\n\n)',q[':question/worked-solution'],re.S)[0]
        if 'row contains only zeros' in sentence:
            i=next(i for i,n in enumerate(['first','second','third','fourth','fifth']) if n+' row' in sentence)
            assert not any(c[i]) and any(any(row) for row in c[i+1:])
        w=re.search(r'\$\{([abc])\}_\{(\d)(\d)\}',sentence)
        if w:
            name,ri,ci=w.groups();i,j=int(ri)-1,int(ci)-1
            assert name==label.lower() and c[i][j]!=0 and not any(c[i][:j])
            above=[next(k for k,v in enumerate(row) if v) for row in c[:i] if any(row)]
            assert above and j<=above[-1]
        w=re.search(r'columns \$(\d)\$ and \$(\d),\$',sentence)
        if w:
            first,second=map(int,w.groups());assert first==next(j+1 for j,v in enumerate(c[0]) if v) and second==next(j+1 for j,v in enumerate(c[1]) if v) and second<=first
    fs=q[':question/answer-fields'];assert [f[':answer-field/key'] for f in fs]==list('ABC');ids=[q[':question/id']]
    for f,m in zip(fs,ms):
        assert f[':answer-field/type']==':answer-field.type/checkbox'
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==['false','true']
        correct=[a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]]
        assert len(correct)==1 and correct[0][':answer/value']==str(oracle(m)!=('**not**' in q[':question/problem'])).lower()
        ids+=[f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
    assert len(ids)==len(set(ids)) and meta['mathematical_fingerprint']==g.fingerprint(q)
    return r
def native(label,r):
    return {'label':label,'record':r,'checks':[{'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Field-owned Boolean bank'} for i,f in enumerate(r['question'][':question/answer-fields']) for a in f[':answer-field/choices']]}
def main():
    mapping=[];replays=[];inputs=[];review=[];coverage={}
    for profile in g.PROFILES:
        source=g.SOURCES[profile];r=check(g.generate('easy',0,profile,g.original(profile),True))
        assert r['question'][':question/problem']==source[':question/problem'] and r['question'][':question/worked-solution']==source[':question/worked-solution']
        for sf,gf in zip(source[':question/answer-fields'],r['question'][':question/answer-fields']):
            assert sf[':answer-field/key']==gf[':answer-field/key'] and sf[':answer-field/type'][':db/ident']==gf[':answer-field/type']
            for sa in sf[':answer-field/choices']:
                matches=[a for a in gf[':answer-field/choices'] if a[':answer/value']==sa[':answer/value']];assert len(matches)==1
                correct=sa[':answer/id']==sf[':answer-field/correct'][':answer/id'];assert correct==(matches[0][':answer/id']==gf[':answer-field/correct'][1])
                mapping.append({'source':profile,'source_db_id':source[':db/id'],'field':sf[':answer-field/key'],'source_answer_id':sa[':answer/id'],'value':sa[':answer/value'],'recipe':'Literal Boolean '+sa[':answer/value'],'correct':correct,'matched':True})
        replays.append({'source':profile,'matched_choices':6,'total_choices':6,'matched_distractors':3,'total_distractors':3,'exact_prompt':True,'exact_solution':True})
        inputs.append(native('source-'+profile,r));review.append('## Source '+profile+'\n\n'+g.markdown(r))
        domain=[g.pivot_domain(m) for m in g.original(profile)['matrices']];observed=[set(),set(),set()]
        for i,choices in enumerate(domain):
            for pivots in choices:
                p=g.original(profile);width=len(p['matrices'][i][0]);old=p['matrices'][i]
                p['matrices'][i]=[[0]*(width-1)+[old[k][-1]] if pivot is None else [0]*pivot+[1]+[2]*(width-pivot-2)+[old[k][-1]] for k,pivot in enumerate(pivots)]
                rr=check(g.generate('easy',0,profile,p));inputs.append(native(profile+'-'+str(i)+'-'+str(pivots),rr));observed[i].add(tuple(-1 if v is None else v for v in pivots))
            assert len(observed[i])==len(choices)
        for seed in range(30):
            rr=check(g.generate('easy',seed,profile));assert rr['question']==g.generate('easy',seed+1000,profile,rr['generation']['parameters'])['question'];inputs.append(native(profile+'-sample-'+str(seed),rr))
        coverage[profile]={'domains':domain,'observed':[sorted(v) for v in observed],'structural_product_upper_bound':int(sp.prod(map(len,domain))),'matrix_dimensions':[[len(m),len(m[0])] for m in g.original(profile)['matrices']]}
        review.append('## Variant '+profile+'\n\n'+g.markdown(rr))
    # Fixed mathematical data, moved zero row: catch stale ordinal witnesses and keys.
    p=g.original('q-72576');a=check(g.generate('easy',0,'q-72576',p));p['matrices'][0][0],p['matrices'][0][1]=p['matrices'][0][1],p['matrices'][0][0]
    b=check(g.generate('easy',0,'q-72576',p));assert g.fingerprint(a['question'])!=g.fingerprint(b['question']) and 'first row contains only zeros' in b['question'][':question/worked-solution'];inputs.append(native('changed-zero-target',b));review.append('## Changed target with other data fixed\n\n'+g.markdown(b))
    # Fixed matrices except constants: ensure separating bar controls the requested object.
    p=g.original('q-72575');a=check(g.generate('easy',0,'q-72575',p));p['matrices'][0][2][-1]=0;p['matrices'][0][3][-1]=0
    b=check(g.generate('easy',0,'q-72575',p));assert g.fingerprint(a['question'])==g.fingerprint(b['question']);inputs.append(native('constants-not-coefficients',b))
    p=g.original('q-42006');a=g.generate('easy',0,'q-42006',p);p['matrices']=[[[2*v for v in row] for row in m] for m in p['matrices']];b=g.generate('easy',0,'q-42006',p);assert g.fingerprint(a['question'])==g.fingerprint(b['question'])
    q=dict(a['question']);it=iter(reversed(parse(q[':question/problem'])));q[':question/problem']=g.MATRIX.sub(lambda _:g.latex(next(it)),q[':question/problem']);assert g.fingerprint(q)==g.fingerprint(a['question'])
    previews=[check(r) for r in g.batch('easy',5,12345)];assert len({g.fingerprint(r['question']) for r in previews})==5
    for level in ('moderate','hard'):
        try:g.batch(level,5,0)
        except ValueError:pass
        else:raise AssertionError('Unsupported level accepted')
    save('source-choice-mapping.json',mapping);save('source-replay.json',{'passed':True,'basis':g.S['basis'],'complete_banks_matched':len(replays),'complete_banks_total':len(replays),'matched_choices':len(mapping),'total_choices':len(mapping),'matched_distractors':len(mapping)//2,'total_distractors':len(mapping)//2,'profiles':replays,'missing_or_extra_options':[],'excluded':g.EXCLUDED,'variant_clarification':g.CORRECTIONS})
    save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True);assert json.loads((HERE/'native-report.json').read_text())['documented_unresolved_checks']==0
    save('previews.json',previews);save('domain-catalog.json',coverage);(HERE/'review.md').write_text('\n\n'.join(review)+'\n')
    save('validation.json',{'passed':True,'source_templates':3,'complete_source_profiles':len(replays),'source_fidelity':f'{len(mapping)}/{len(mapping)} choices, {len(mapping)//2}/{len(mapping)//2} incorrect options, {len(replays)}/{len(replays)} full banks; exact replay prompts and solutions','variant_fidelity':'Same source matrices, bar notation, three checkbox fields, polarity and ordered solution stages. Explicit coefficient wording clarifies source convention. Witness row/columns parameterized.','mathematics':'Independent rendered-matrix parsing and SymPy coefficient Matrix.is_echelon; rendered verdicts, zero-row witnesses, pivot indices, leading-column witnesses and Boolean keys checked.','actual_grading':'Every Boolean choice through current learning::grade_field; zero unresolved checks','checked_instances':len(inputs),'all_declared_slot_domains_checked':True,'changed_target_with_other_data_fixed':True,'semantic_duplicate_checks':True,'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'assets':[]})
    print('Validated',len(replays),'complete banks and',len(inputs),'instances.')
if __name__=='__main__':main()
