"""Read rendered matrices/targets independently, replay banks, test actual grader."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as sp

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('entry_removal',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(s);s.loader.exec_module(g)

def save(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')

def parse(text):
    return [[[int(x.strip()) for x in row.split('&')] for row in body.split(r'\\')]
      for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)]

def entries(text):
    return [(int(i)-1,int(j)-1) for i,j in re.findall(r'\{a\}_\{(\d)(\d)\}',text)]

def remove(m,targets):
    copy=sp.Matrix(m)
    for i,j in targets:copy[i,j]=0
    return copy

def check(r):
    q=r['question'];meta=r['generation'];m=parse(q[':question/problem'])[0]
    assert m==meta['parameters']['matrix']
    assert len(m)==4 and all(len(row)==4 for row in m)
    assert not sp.Matrix(m).is_echelon
    assert q[':question/difficulty']==':question.difficulty/moderate'
    f=q[':question/answer-fields'][0]
    assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection'
    assert f[':answer-field/type']==':answer-field.type/radio'
    assert len(f[':answer-field/choices'])==5
    correct=[a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]]
    assert len(correct)==1
    bs=[entries(a[':answer/value']) for a in f[':answer-field/choices']]
    assert len({tuple(sorted(b)) for b in bs})==5
    for a,b in zip(f[':answer-field/choices'],bs):
        assert bool(remove(m,b).is_echelon)==(a[':answer/id']==correct[0][':answer/id'])
    b=entries(correct[0][':answer/value']);assert len(b) in (2,3)
    assert all(m[i][j]!=0 for i,j in b)
    assert entries(q[':question/worked-solution'])==b
    assert parse(q[':question/worked-solution'])==[m,[list(row) for row in remove(m,b).tolist()]]
    assert meta['mathematical_fingerprint']==g.fingerprint(q)
    assert r==g.generate('moderate',meta['seed'],meta['profile'],meta['parameters'],meta['replay'])
    return r

def native(label,r):
    f=r['question'][':question/answer-fields'][0]
    return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],
      'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every choice through actual radio grader'} for a in f[':answer-field/choices']]}

def main():
    mapping=[];replays=[];inputs=[];coverage={};reviews=[];eligible=[];target_case=None
    for profile in g.PROFILES:
        source=g.SOURCES[profile];r=check(g.generate('moderate',0,profile,g.original(profile),True))
        assert r['question'][':question/problem']==source[':question/problem']
        assert r['question'][':question/worked-solution']==source[':question/worked-solution']
        sf=source[':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0]
        for sa in sf[':answer-field/choices']:
            matches=[a for a in gf[':answer-field/choices'] if a[':answer/value']==sa[':answer/value']]
            assert len(matches)==1
            assert (sa[':answer/id']==sf[':answer-field/correct'][':answer/id'])==(matches[0][':answer/id']==gf[':answer-field/correct'][1])
            mapping.append({'source':profile,'source_db_id':source[':db/id'],'source_answer_id':sa[':answer/id'],
              'original_value':sa[':answer/value'],'recipe':{'operation':'set specified entries to zero','positions':entries(sa[':answer/value']),'mapping':'old column j -> index of j in columns'},
              'correct':sa[':answer/id']==sf[':answer-field/correct'][':answer/id'],'matched':True})
        replays.append({'source':profile,'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'exact_prompt':True,'exact_solution':True,'complete_bank':True})
        inputs.append(native('source-'+profile,r));reviews.append('## Original '+profile+'\n\n'+g.markdown(r))
        tested=[];valid_cols=[];target_sets=[]
        for cols in itertools.permutations(range(4)):
            p={'matrix':[[row[j] for j in cols] for row in g.original(profile)['matrix']],'columns':list(cols)}
            bs=g.bank(profile,list(cols)); verdict=[bool(remove(p['matrix'],b).is_echelon) for b in bs]
            accepted=verdict==[i==g.correct_index(profile) for i in range(5)] and not sp.Matrix(p['matrix']).is_echelon and all(p['matrix'][i][j] for i,j in bs[g.correct_index(profile)])
            assert accepted==g.valid(profile,p)
            tested.append({'columns':list(cols),'accepted':accepted,'bank_echelon_verdicts':verdict})
            if accepted:
                variant=check(g.generate('moderate',0,profile,p));eligible.append(variant);inputs.append(native(profile+'-'+str(cols),variant))
                valid_cols.append(list(cols));target_sets.append(bs[g.correct_index(profile)])
        coverage[profile]={'tested':tested,'eligible_columns':valid_cols,'sampled_correct_targets':target_sets,'all_24_permutations_tested':True}
    # Controlled validator fixture: every matrix entry stays fixed while the
    # target SET changes, rather than only its order. This fixture is not added
    # to the public source-support catalog or available inventory.
    fixture=json.loads((HERE/'target-test-parameters.json').read_text())
    first=check(g.generate('moderate',0,fixture['profile'],fixture['first']))
    second=check(g.generate('moderate',0,fixture['profile'],fixture['second']))
    assert first['question'][':question/problem']==second['question'][':question/problem']
    b1=entries(first['question'][':question/worked-solution']);b2=entries(second['question'][':question/worked-solution'])
    assert sorted(b1)!=sorted(b2)
    target_case={'source':fixture['profile'],'matrix':fixture['first']['matrix'],'original_targets':b1,'changed_targets':b2,
      'first_record':first,'changed_record':second,'rendered_prompt_solution_key_checked':True,'test_fixture_only':True}
    inputs.extend([native('fixed-matrix-first-target',first),native('fixed-matrix-changed-target',second)])
    catalog=g.structural_catalog();assert len(catalog)==len({r['fingerprint'] for r in catalog})
    for x in catalog:
        if x['parameters']['columns']!=g.IDENTITY:
            reviews.append('## Changed target variant '+x['profile']+'\n\n'+g.markdown(check(g.generate('moderate',0,x['profile'],x['parameters']))))
            break
    # Signed and endpoint values cannot affect echelon status; validate output.
    for n in (-9,-1,1,9):
        for profile in g.PROFILES:
            p=g.original(profile);p['matrix']=[[n if x else 0 for x in row] for row in p['matrix']]
            r=check(g.generate('moderate',n,profile,p));inputs.append(native(profile+'-boundary-'+str(n),r))
    for seed in range(60):
        r=check(g.generate('moderate',seed));assert r==g.generate('moderate',seed)
        assert r['question']==g.generate('moderate',seed+1000,r['generation']['profile'],r['generation']['parameters'])['question']
        inputs.append(native('seed-'+str(seed),r))
    for level in ('easy','hard'):
        try:g.generate(level,0)
        except ValueError:pass
        else:raise AssertionError('Unsupported level accepted')
    save('source-choice-mapping.json',mapping);save('source-replay.json',replays);save('slot-coverage.json',coverage);save('changed-target.json',target_case)
    save('domain-catalog.json',catalog);save('native-input.json',inputs)
    subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
    native_report=json.loads((HERE/'native-report.json').read_text());assert native_report['documented_unresolved_checks']==0
    previews=[check(g.generate('moderate',i)) for i in range(5)];save('previews.json',previews)
    (HERE/'review.md').write_text('\n\n---\n\n'.join(reviews)+'\n')
    save('validation.json',{'passed':True,'basis':g.S['basis'],'source_replay':{'banks':10,'choices':50,'distractors':40,'all_matched':True},
      'independent_oracle':'SymPy Matrix.is_echelon on rendered prompt and each parsed option','structural_domain':len(catalog),
      'profiles':10,'column_cases':240,'eligible_cases':len(eligible),'fixed_matrix_changed_targets':True,'native_grading':{'accepted':native_report['accepted_checks'],'rejected':native_report['rejected_checks'],'unresolved':0},
      'boundary_values':[-9,-1,1,9],'deterministic_seeds':60,'supported_levels':['moderate'],'unsupported_levels':['easy','hard'],
      'fidelity':'Exact source prompt, solution and complete banks on original parameters; normal variants normalize list punctuation and correct malformed q-73151 distractor conjunction.'})
    print((HERE/'validation.json').read_text())

if __name__=='__main__':main()
