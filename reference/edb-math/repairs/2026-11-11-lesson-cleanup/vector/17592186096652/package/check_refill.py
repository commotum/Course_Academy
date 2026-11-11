"""Independent survivor checks for the two-scalar grid-vector task."""
import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from pathlib import Path

CHECK_IDS = ['vector-geometry-and-endpoints', 'independent-two-blank-task', 'target-provenance']

def enum(x):
    return x.get(':db/ident') if isinstance(x, dict) else x

def selected(field):
    ref = field[':answer-field/correct']
    aid = ref[-1] if isinstance(ref, list) else ref.get(':answer/id') if isinstance(ref, dict) else ref
    return next(x for x in field[':answer-field/choices'] if x[':answer/id'] == aid)

def fingerprint(q):
    # Native publisher content identity for this deliberately two-blank task.
    result = {k: q[k] for k in [':question/problem', ':question/requires-calculator'] if k in q}
    result[':question/answer-fields'] = sorted([
        {':answer-field/key': f[':answer-field/key'], ':answer-field/type': enum(f[':answer-field/type']),
         ':answer-field/correct': {':answer/type': enum(selected(f)[':answer/type']), ':answer/value': selected(f)[':answer/value']}}
        for f in q[':question/answer-fields']], key=lambda f: f[':answer-field/key'])
    return hashlib.sha256(json.dumps(result, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()

def scalar(text):
    match = re.fullmatch(r'(-?)\\frac\{(\d+)\}\{(\d+)\}', text.strip())
    return (-1 if match[1] else 1) * F(int(match[2]), int(match[3])) if match else F(text)

def assess(record):
    q = record['question'];g = record['generation'];s = g['instance']
    u,v,t = [tuple(map(F, s[k])) for k in ['u','v','target']]
    det = u[0]*v[1]-u[1]*v[0]
    assert det, 'Known arrows must be nonparallel.'
    a = (t[0]*v[1]-t[1]*v[0])/det
    b = (u[0]*t[1]-u[1]*t[0])/det
    assert a and b, 'This reviewed sampler uses two nonzero scale readings.'
    assert (a,b) == (F(s['a']),F(s['b'])), 'Declared factors contradict exact geometry.'
    corner = tuple(map(F, s['corner']))
    assert corner == tuple((a*u[i] if s['first']==0 else b*v[i]) for i in range(2)), 'Solution route has wrong corner.'
    assert all(x.denominator==1 for p in [u,v,t,corner] for x in p), 'Unmarked non-grid endpoint.'
    fields=q[':question/answer-fields']
    assert len(fields)==2 and {f[':answer-field/key'] for f in fields}=={'field-1','field-2'}
    prompt=q[':question/problem']
    assert r'\mathbf{c}=\lambda\mathbf{a}+\mu\mathbf{b}' in prompt
    assert prompt.count('{{field-1}}')==1 and prompt.count('{{field-2}}')==1
    stripped=re.sub(r'!\[[^\]]*\]\([^)]*\)|\{\{field-[12]\}\}', '', prompt)
    assert not re.search(r'\d|construct|first parallel|hence|move|trace|coefficient formula', stripped, re.I), 'Prompt supplies intermediate work.'
    assert 'Matching coefficients gives' in q[':question/worked-solution']
    endpoint=q[':question/worked-solution'].split('Matching coefficients gives',1)[1]
    match=re.fullmatch(r'\s*\$\\lambda=(.+?)\$ and \$\\mu=(.+?)\$\.',endpoint)
    assert match and (scalar(match[1]),scalar(match[2]))==(a,b), 'Displayed solution endpoint disagrees with geometry.'
    checks=[]
    for index,f in enumerate(fields):
        assert enum(f[':answer-field/type'])==':answer-field.type/blank'
        assert len(f[':answer-field/choices'])==1
        answer=selected(f);value=a if f[':answer-field/key']=='field-1' else b
        assert enum(answer[':answer/type'])==':answer.type/math' and scalar(answer[':answer/value'])==value
        checks += [
            {'field_index':index,'submitted':f'{2*value.numerator}/{2*value.denominator}', 'expected':'accepted','control':'equivalent','purpose':'Exact geometry determines this rational value; unreduced quotient is equivalent and no simplest-form restriction is displayed.'},
            {'field_index':index,'submitted':str(-value),'expected':'rejected','control':'wrong','purpose':'Opposite signed scalar is wrong because this geometry has a unique nonzero coefficient for the named vector.'}]
    assert g['source_basis']==14174, 'Wrong captured source basis.'
    assert set(g['source_ids']) <= {'q-326018','q-326022','q-326014','q-327074','q-326016'} and g['source_ids']
    return checks

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--records',type=Path,required=True);p.add_argument('--inventory',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    records=json.loads(a.records.read_text());json.loads(a.inventory.read_text())
    checked=[];native=[]
    for record in records:
        controls=assess(record);identity=fingerprint(record['question']);checked.append(identity);native.append({'fingerprint':identity,'checks':controls})
    checked=sorted(checked)
    a.output.write_text(json.dumps({'status':'passed','checked_fingerprints':checked,'check_results':[{'id':key,'status':'passed','checked_fingerprints':checked} for key in CHECK_IDS],'native_checks':native},indent=2)+'\n')
