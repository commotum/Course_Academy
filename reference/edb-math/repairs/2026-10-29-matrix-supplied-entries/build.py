"""Replace presentation markers only; calculate every cell from the operands."""
import copy,importlib.util,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(H/'package'))
spec=importlib.util.spec_from_file_location('distributive_repair',H/'package/generator.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
from generate.matrix_product_prompt_policy import validate_delivery_batch,SUPPLIED_ENTRIES_KP

def product(prompt):
    expr=re.search(r'\$([ABC]{2}[+-][ABC]{2})\$',prompt)[1]
    env=dict(zip('ABC',g.matrices(prompt)[:3]));left,op,right=re.fullmatch(r'([ABC]{2})([+-])([ABC]{2})',expr).groups()
    first=env[left[0]]*env[left[1]];second=env[right[0]]*env[right[1]]
    return first+second if op=='+' else first-second

def patch_question(q):
    assert not q.get(':question/math-academy-id')
    before=q[':question/problem'];result=product(before);row_index=0;changed=0
    def row(match):
        nonlocal row_index,changed
        i=row_index;row_index+=1;column=0
        def cell(m):
            nonlocal column,changed
            j=column;column+=1
            if m[1].strip()=='$\\ast$':
                changed+=1;return '<td>$'+g.s.latex(result[i,j])+'$</td>'
            assert re.fullmatch(r'\{\{field-\d+\}\}',m[1]);return m[0]
        updated=re.sub(r'<td>(.*?)</td>',cell,match[1]);assert column==3
        return '<tr>'+updated+'</tr>'
    after=re.sub(r'<tr>(.*?)</tr>',row,before)
    assert row_index==3 and changed==9-len(q[':question/answer-fields'])
    legend='Fill in the input cells. An asterisk $\\ast$ marks an entry that is not requested.'
    assert after.count(legend)==1
    after=after.replace(legend,'Fill in the missing entries.')
    out=copy.deepcopy(q);out[':question/problem']=after
    assert {k:v for k,v in out.items() if k!=':question/problem'}=={k:v for k,v in q.items() if k!=':question/problem'}
    return out

def verify(q):
    result=product(q[':question/problem']);fields={f[':answer-field/key']:f for f in q[':question/answer-fields']}
    requested=supplied=0
    rows=re.findall(r'<tr>(.*?)</tr>',q[':question/problem']);assert len(rows)==3
    seen=set()
    for i,row in enumerate(rows):
        cells=re.findall(r'<td>(.*?)</td>',row);assert len(cells)==3
        for j,cell in enumerate(cells):
            if m:=re.fullmatch(r'\{\{(field-\d+)\}\}',cell):
                key=m[1];assert key not in seen;seen.add(key);f=fields[key];correct=f[':answer-field/correct']
                if isinstance(correct,dict):value=correct[':answer/value']
                else:value=next(a[':answer/value'] for a in f[':answer-field/choices'] if str(a[':answer/id'])==str(correct[1]))
                requested+=1
            else:
                assert cell.startswith('$') and cell.endswith('$');value=cell[1:-1];supplied+=1
            assert g.s.simplify(g.scalar(value)-result[i,j])==0,(i,j,value,result)
    assert seen==set(fields) and requested+supplied==9
    assert g.matrices(q[':question/worked-solution'])[-1]==result
    validate_delivery_batch([{'question':q}],SUPPLIED_ENTRIES_KP)
    return {'requested':requested,'supplied':supplied}

def main():
    before=json.loads((H/'before.json').read_text());affected=[q for q in before[':knowledge-point/questions'] if '\\ast' in q.get(':question/problem','')]
    assert len(affected)==9
    repaired=[patch_question(q) for q in affected];checks=[{'entity':q[':db/id'],**verify(q)} for q in repaired]
    fresh=[]
    for level,profiles in g.PROFILES.items():
        for profile in profiles:
            for seed in (19,20261029):
                r=g.generate(level,seed,profile);verify(r['question']);fresh.append(r)
    # Fresh sampling retains the old arithmetic and targets under identical seeds.
    original=H/'original-generator.py';original.write_text((ROOT/'reference/edb-math/repairs/2026-10-27-linear-algebra-audit/group-2/generator-17592186115226.py.txt').read_text())
    spec=importlib.util.spec_from_file_location('old_distributive',original);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    for r in fresh:
        m=r['generation'];previous=old.generate(r['question'][':question/difficulty'].split('/')[-1],m['seed'],m['profile'])
        for key in ('seed','profile','expression','side','targets','matrices','intermediate','source_ids'):assert m[key]==previous['generation'][key]
        assert r['question'][':question/worked-solution']==previous['question'][':question/worked-solution']
        assert [[a[':answer/value'] for a in f[':answer-field/choices']] for f in r['question'][':question/answer-fields']]==[[a[':answer/value'] for a in f[':answer-field/choices']] for f in previous['question'][':question/answer-fields']]
    (H/'repairs.json').write_text(json.dumps([{'entity':a[':db/id'],'before':a[':question/problem'],'after':b[':question/problem']} for a,b in zip(affected,repaired)],indent=2)+'\n')
    (H/'render-input.json').write_text(json.dumps([{'question':q} for q in repaired],indent=2)+'\n')
    (H/'fresh-samples.json').write_text(json.dumps(fresh,indent=2)+'\n')
    report={'passed':True,'repaired_questions':checks,'fresh_records':len(fresh),'all_profiles':list(g.PROFILES.values()),'unchanged_arithmetic_targets_solutions_and_correct_values':True}
    (H/'generator-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
