#!/usr/bin/env python3
"""Offline retained-findings regression; mathematical oracle reads visible content."""
import importlib.util
import json
import math
from pathlib import Path
import random
import re
import sys
from fractions import Fraction

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import generator as g

OUT = ROOT / 'evidence'
OUT.mkdir(exist_ok=True)
ROMANS = ['I', 'II', 'III', 'IV']
# One representative of every atom distinguished by the taught predicates:
# (sign, integer, rational). This partition is complete for these set symbols.
ATOMS = [(s, True, True) for s in [-1,0,1]] + [(s,False,r) for s in [-1,1] for r in [True,False]]


def save(name, data):
    (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')


def value(field):
    ref=field[':answer-field/correct']
    aid=ref[':answer/id'] if isinstance(ref,dict) else ref[1]
    return next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==aid)


def symbol(key):
    if key in ('None','None of the above'): return None
    base=re.search('[NZQRC]',key).group()
    return base+('0' if '0' in key else '')+('+' if '+' in key else '-' if '-' in key else '')


def member(atom,s):
    sign,integer,rational=atom
    if s=='C': return True
    if s=='N': return sign>0 and integer
    if s=='N0': return sign>=0 and integer
    if s[0]=='Z' and not integer: return False
    if s[0]=='Q' and not rational: return False
    return {'':True,'+':sign>0,'-':sign<0,'0+':sign>=0,'0-':sign<=0}[s[1:]]


def targets(prompt):
    if 'do all the ' in prompt:
        group=re.search('do all the (.*?) belong',prompt)[1]
        return [v for v in ATOMS if {
            'natural numbers':v[0]>0 and v[1], 'positive integers':v[0]>0 and v[1],
            'negative integers':v[0]<0 and v[1], 'integers':v[1],
            'nonnegative integers':v[0]>=0 and v[1],
            'positive rational numbers':v[0]>0 and v[2],
            'negative rational numbers':v[0]<0 and v[2],
            'rational numbers':v[2], 'real numbers':True}[group]]
    expr=re.search(r'number \$(.*?)\$ belong',prompt)[1].strip()
    sign=-1 if expr.startswith('-') else 1
    if r'\pi' in expr: return [(sign,False,False)]
    if r'\sqrt' in expr:
        n=int(re.search(r'\{(\d+)\}',expr)[1]); k=math.isqrt(n)
        return [(0 if n==0 else sign,k*k==n,k*k==n)]
    if r'\frac' in expr:
        n,d=map(int,re.findall(r'\{(\d+)\}',expr)); v=Fraction(sign*n,d)
    else: v=Fraction(expr)
    return [(0 if not v else 1 if v>0 else -1, v.denominator==1,True)]


def selected(label):
    return {ROMANS.index(x) for x in re.findall(r'\b(?:IV|III|II|I)\b',label)}


def expected(record):
    q=record['question']; atoms=targets(q[':question/problem']); fields=q[':question/answer-fields']
    kind=fields[0][':answer-field/type']
    if isinstance(kind,dict):kind=kind[':db/ident']
    if kind.endswith('/radio'):
        items=re.findall(r'^(?:[1-4]|I|II|III|IV)\.\s*\$(.*?)\$',q[':question/problem'],re.M)
        assert len(items)==4, items
        chosen={i for i,x in enumerate(items) if all(member(v,symbol(x)) for v in atoms)}
        matches=[a[':answer/value'] for a in fields[0][':answer-field/choices'] if selected(a[':answer/value'])==chosen]
        assert len(matches)==1,(chosen,matches)
        return matches
    ordinary=[all(member(v,symbol(f[':answer-field/key'])) for v in atoms) for f in fields if symbol(f[':answer-field/key'])]
    it=iter(ordinary)
    return [str(next(it) if symbol(f[':answer-field/key']) else not any(ordinary)).lower() for f in fields]


def validate(record,conclusion=True):
    q=record['question']; fields=q[':question/answer-fields']; want=expected(record)
    assert [value(f) for f in fields]==want,q[':question/id']
    assert 'leave every box unchecked' not in q[':question/worked-solution']
    assert 'leave all boxes unchecked' not in q[':question/problem']
    if conclusion:
        end=q[':question/worked-solution'].split('\n\n')[-1]
        if fields[0][':answer-field/type'].endswith('/checkbox'):
            ordinary=[f[':answer-field/key'] for f,w in zip(fields,want) if w=='true' and symbol(f[':answer-field/key'])]
            if ordinary:
                assert all(x in end for x in ordinary),(end,ordinary)
                assert 'None of the above' not in end
            else: assert 'select "None of the above"' in end,end
        else: assert 'select "'+want[0]+'"' in end,end
    return want


def source_checks():
    sources=json.loads((ROOT.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']
    assert json.loads((ROOT/'source_cases.json').read_text())==sources
    replay=[g.replay_source(i) for i in range(len(sources))]
    for r,s in zip(replay,sources):
        assert r['generation']['source_id']==s[':question/id']
        def bank(q): return [(f[':answer-field/key'],[a[':answer/value'] for a in f[':answer-field/choices']]) for f in q[':question/answer-fields']]
        assert bank(r['question'])==bank(s),(s[':question/id'],'incomplete bank')
        want=validate(r,False)
        for f,w in zip(s[':question/answer-fields'],want):
            if ':answer-field/correct' in f: assert value(f)==w
        if ':question/difficulty' in s: assert r['generation']['source_difficulty']==s[':question/difficulty']
    save('source-replays.json',replay)
    return len(replay)


def counterexamples():
    # The seed is retained, but changed sampling support may change its sampled profile.
    seed_records=g.generate(count=1,seed=827461)
    r=g.make_record(g.number_instance('root',radicand=0,sign=1),['Z+','Q-','Z-','N'],seed=827461)
    validate(r); assert expected(r)==['false']*4+['true']
    historical=g.make_record({'profile':'universal','group':'real numbers'},['N','Z','Q-','R0-'])
    validate(historical); assert expected(historical)==['false']*4+['true']
    save('retained-counterexamples.json',seed_records+[r,historical])
    pairs=[]
    def pair(a,b,candidates,bank='checkbox',same=False):
        rs=[g.make_record(x,candidates,bank_profile=bank) for x in [a,b]]
        keys=[validate(x) for x in rs]
        assert (keys[0]==keys[1])==same
        assert rs[0]['question'][':question/problem']!=rs[1]['question'][':question/problem']
        pairs.extend(rs)
    root=lambda n:g.number_instance('root',radicand=n,sign=1)
    pair(root(0),root(1),['Z+','Q-','Z-','N'])
    pair(root(2),root(121),['Q+','R','Q','Z'],'radio-0')
    pair(root(121),root(144),['Q+','R','Q','Z'],'radio-0',True)
    pair(g.number_instance('decimal',value='0.0'),g.number_instance('decimal',value='0.25'),['Z','Q+','Q-','R'],'radio-10')
    pair({'profile':'universal','group':'natural numbers'},{'profile':'universal','group':'negative integers'},['Z+','Z-','Q+','Q-'],'radio-10')
    save('counterfactual-records.json',pairs)
    return len(pairs)//2


def ordinary_patterns():
    # Every ordinary truth mask, with zero-boundary target fixed. Role assignments
    # choose sets from independent sign membership, not generator classification.
    rs=[];symbols=['N','N0','C']+[b+s for b in 'ZQR' for s in ('','+','-','0+','0-')]
    yes=[s for s in symbols if member((0,True,True),s)]
    no=[s for s in symbols if not member((0,True,True),s)]
    semantic_banks=set()
    for mask in range(16):
        rng=random.Random(6421+mask)
        count=mask.bit_count()
        while True:
            positives=rng.sample(yes,count);negatives=rng.sample(no,4-count)
            signature=tuple(sorted(positives+negatives))
            if signature not in semantic_banks: break
        semantic_banks.add(signature)
        y=iter(positives);n=iter(negatives)
        cs=[next(y) if mask&(1<<i) else next(n) for i in range(4)]
        r=g.make_record(g.number_instance('root',radicand=0,sign=1),cs);validate(r);rs.append(r)
    save('truth-patterns.json',rs)
    return rs


def inventory_checks():
    # Reproduce all stored generated records with the pre-repair constructor.
    # This historical fixture is evidence only, never used by runtime sampling.
    spec=importlib.util.spec_from_file_location('legacy',OUT/'legacy-generator.py')
    legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
    repo=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(repo))
    from scripts.generator_publish import content_fingerprint,normalized_question
    import uuid
    inv=json.loads((ROOT.parent/'source/inventory.json').read_text())
    original={q[':question/id'] for q in json.loads((ROOT/'source_cases.json').read_text())}
    reproduced=[];affected=[];replacements=[]
    for q in inv['questions']:
        if q[':question/id'] in original: continue
        p=q[':question/problem'];cs=[symbol(x) for x in re.findall(r'- The set (\$.*?\$) contains',q[':question/worked-solution'])]
        assert len(cs)==4
        if 'do all the ' in p:inst={'profile':'universal','group':re.search('do all the (.*?) belong',p)[1]}
        elif r'\sqrt' in p:
            e=re.search(r'number \$(.*?)\$ belong',p)[1]
            inst=g.number_instance('root',radicand=int(re.search(r'\{(\d+)\}',e)[1]),sign=-1 if e.startswith('-') else 1)
        else:
            e=re.search(r'number \$(.*?)\$ belong',p)[1];n,d=map(int,re.findall(r'\{(\d+)\}',e))
            inst=g.number_instance('fraction',numerator=-n if e.startswith('-') else n,denominator=d)
        raw=legacy.make_record(inst,cs)
        fingerprint=content_fingerprint(raw['question'])
        assert fingerprint==content_fingerprint(q)
        assert str(uuid.uuid5(uuid.UUID(g.KP['id']),'generated-question:'+fingerprint))==q[':question/id']
        r={'knowledge_point':g.KP.copy(),'question':normalized_question(q),'generation':{
            'inventory_reproduction':{'entity_id':q[':db/id'],'basis':inv['basis'],'content_fingerprint':fingerprint,
                'seed':None,'seed_limit':'Historical seed not captured; parameters reproduce complete stored content and publisher UUID.'},
            'instance':inst,'candidates':cs,'evidence_only':True},'assets':[]}
        for f in r['question'][':question/answer-fields']:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct']]
        assert [value(f) for f in r['question'][':question/answer-fields']]==expected(r)
        reproduced.append(r)
        if not any(value(f)=='true' for f in r['question'][':question/answer-fields']):
            affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],
                'finding':'All four ordinary checkboxes are false with no explicit None; excluded by current fresh-practice source rule.',
                'reproduction':'python checks/repair_check.py; explicit instance='+json.dumps(inst,sort_keys=True)+'; candidates='+json.dumps(cs),
                'evidence_path':'../workspace/evidence/generated-records.json'})
            new=g.make_record(inst,cs);validate(new);replacements.append(new)
    assert len(reproduced)==5 and len(affected)==1
    assert affected[0]['question_id']=='6e7f7e59-12b8-5d8f-a27b-48f0bd02db19'
    save('generated-records.json',reproduced);save('replacement-proposals.json',replacements)
    (ROOT/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
    return {'captured_questions':len(inv['questions']),'original_source':len(original),'generated_reproduced':len(reproduced),'affected':len(affected),
        'evidence_path_base':'author-1 evidence_root; ../workspace is intentional because writes are authorized only in workspace',
        'limit':'Verified captured inventory only; no live inventory or learner history queried. Source questions are never marked generated.'}


def main():
    source_count=source_checks();pairs=counterexamples();patterns=ordinary_patterns()
    sample=g.generate(count=180,seed=827461)
    assert sample==g.generate(count=180,seed=827461)
    coverage={}
    for r in sample:
        validate(r)
        p=r['generation']['profile'];b=r['generation']['bank_profile']
        d=coverage.setdefault(p,{'count':0,'banks':{},'decimal_sign_integrality':[]})
        d['count']+=1;d['banks'].setdefault(b,[])
        response=expected(r)
        if response not in d['banks'][b]:d['banks'][b].append(response)
        if p=='decimal' and targets(r['question'][':question/problem'])[0] not in d['decimal_sign_integrality']:
            d['decimal_sign_integrality'].append(targets(r['question'][':question/problem'])[0])
    assert set(coverage)==set(g.PROFILES)
    assert all(b in {r['generation']['bank_profile'] for r in sample} for b in g.RADIO_BANKS)
    assert len(coverage['decimal']['decimal_sign_integrality'])==5
    for b,bank in g.RADIO_BANKS.items():
        assert {value(r['question'][':question/answer-fields'][0]) for r in sample if r['generation']['bank_profile']==b}==set(bank),(b,'unexercised correct choice')
    save('samples.json',sample);save('coverage.json',coverage)
    # The delivery input includes the new sample, every truth mask, all source banks,
    # and controlled interventions. Duplicates are left to the actual delivery tool.
    all_records=sample+patterns+json.loads((OUT/'counterfactual-records.json').read_text())+json.loads((OUT/'source-replays.json').read_text())+json.loads((OUT/'retained-counterexamples.json').read_text())
    save('delivery-input.json',all_records)
    # One process will grade all authored choice IDs, expected via independent oracle.
    cases=[]
    for i,r in enumerate(all_records):
        checks=[]
        for j,(f,want) in enumerate(zip(r['question'][':question/answer-fields'],expected(r))):
            for a in f[':answer-field/choices']:
                checks.append({'field_index':j,'submitted_answer_id':a[':answer/id'],
                    'expected':'accepted' if a[':answer/value']==want else 'rejected','purpose':'visible-content independent set-membership witness'})
        cases.append({'label':str(i),'record':r,'checks':checks})
    save('grader-input.json',cases)
    result={'source_complete_banks':source_count,'retained_seed':827461,'truth_patterns':16,'counterfactual_pairs':pairs,
        'sample_size':len(sample),'inventory':inventory_checks(),'grader_cases_prepared':len(cases),'status':'passed'}
    save('repair-results.json',result);print(json.dumps(result))


if __name__=='__main__':main()
