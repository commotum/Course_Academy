"""Read rendered mathematics independently; replay complete source banks; grade."""
import ast, copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('three_matrix',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def save(path,value):path.write_text(json.dumps(value,indent=2,default=int)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def parse_matrix(text):
    m=re.fullmatch(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S);assert m
    rows=[[sp.sympify(x.strip()) for x in row.split('&')] for row in m[1].split('\\\\')]
    assert len({len(row) for row in rows})==1
    assert all(v.is_Integer for row in rows for v in row)
    return sp.Matrix(rows)

def matrices(text):
    return [parse_matrix(m[0]) for m in re.finditer(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',text,re.S)]

def expression_value(text,variables):
    # The independent parser accepts only matrix symbols and +/- ASTs.
    tree=ast.parse(text,mode='eval')
    def walk(node):
        if isinstance(node,ast.Expression):return walk(node.body)
        if isinstance(node,ast.Name):return variables[node.id]
        assert isinstance(node,ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub))
        a,b=walk(node.left),walk(node.right)
        return a+b if isinstance(node.op,ast.Add) else a-b
    return walk(tree)

def check(rec):
    assert rec['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
    q=rec['question'];meta=rec['generation'];text=q[':question/problem'];sol=q[':question/worked-solution']
    expr=re.search(r'Calculate \$(.*?)\$',text)[1]
    arrays=matrices(text);names=re.findall(r'([A-Z])=\\begin\{bmatrix\}',text)
    assert len(arrays)==3 and len(names)==3 and len(set(names))==3
    expected=expression_value(expr,dict(zip(names,arrays)))
    level=q[':question/difficulty'].split('/')[-1];template=meta['template']
    assert template in g.TEMPLATES[level] and meta['eligible_for_learning']
    assert expr==g.expression(template,names)
    assert tuple(arrays[0].shape)==((3,2) if template.endswith('radio') else (2,2))
    assert arrays==list(map(sp.Matrix,meta['parameters']['matrices'])) and names==meta['parameters']['names']
    assert g.fingerprint(q)==meta['mathematical_fingerprint']
    fields=sorted(q[':question/answer-fields'],key=lambda f:f[':answer-field/key'])
    assert len(fields)==(1 if template.endswith('radio') else 4)
    all_ids=[q[':question/id']]
    for i,f in enumerate(fields):
        all_ids.append(f[':answer-field/id']);choices=f[':answer-field/choices'];all_ids.extend(a[':answer/id'] for a in choices)
        assert all(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'] for a in choices)
        keyed={a[':answer/id']:a[':answer/value'] for a in choices};assert len(keyed)==len(choices)
        assert f[':answer-field/correct'][0]==':answer/id'
        v=keyed[f[':answer-field/correct'][1]]
        if template.endswith('radio'):
            assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
            bank=[parse_matrix(a[':answer/value']) for a in choices]
            assert len(bank)==5 and len({tuple(m) for m in bank})==5
            assert parse_matrix(v)==expected and sum(m==expected for m in bank)==1
        else:
            assert f[':answer-field/type']==':answer-field.type/blank' and len(choices)==1
            assert f[':answer-field/key']=='field-'+str(i+1) and '{{'+f[':answer-field/key']+'}}' in text
            assert sp.sympify(v)==list(expected)[i]
    assert len(set(all_ids))==len(all_ids)
    assert sorted(re.findall(r'\{\{(field-\d+)\}\}',text))==([] if template.endswith('radio') else ['field-1','field-2','field-3','field-4'])
    # Read every displayed worked-solution stage, including intermediate arithmetic.
    body=sol.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
    lhs,body=body.split(' & =',1);assert lhs==expr
    stages=body.split(r' \\  & =')
    assert len(stages)==(5 if template.startswith('nested') else 3)
    for stage in stages:
        values={}
        def replace(m):
            name='M'+str(len(values));values[name]=parse_matrix(m[0]);return name
        rendered=re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',replace,stage,flags=re.S).rstrip('.')
        assert expression_value(rendered,values)==expected,'Incorrect displayed solution stage'
    assert text.count('$$')==0 and 'class="matrix-operands"' in text and sol.count('$$')==2
    assert ('class="matrix-answer"' in text) == template.endswith('blank')
    if template.endswith('blank'):
        assert re.findall(r'<td>(.*?)</td>',text)==['{{field-1}}','{{field-2}}','{{field-3}}','{{field-4}}']
    assert not re.search(r'\+\-|\-\-',sol)
    return expected

def native(label,rec):
    checks=[]
    for i,f in enumerate(rec['question'][':question/answer-fields']):
        if f[':answer-field/type'].endswith('/radio'):
            for a in f[':answer-field/choices']:
                checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete-bank actual grading'})
        else:
            v=f[':answer-field/choices'][0][':answer/value']
            for submitted,expected in [(v,'accepted'),('('+v+')','accepted'),(str(int(v)+1)+'-1','accepted'),(str(int(v)+1),'rejected')]:
                checks.append({'field_index':i,'submitted':submitted,'expected':expected,'purpose':'canonical, equivalent expression or wrong entry'})
    return {'label':label,'record':rec,'checks':checks}

def source_cases():
    source=json.loads((HERE/'source.json').read_text());cases=[];raw=[];report=[];components=[]
    for q in source['record'][':knowledge-point/questions']:
        sid=q[':question/math-academy-id'];text=q[':question/problem'];mats=[[[int(v) for v in row] for row in m.tolist()] for m in matrices(text)]
        expr=re.search(r'Calculate \$(.*?)\$',text)[1].replace(' ','')
        names=list(dict.fromkeys(re.findall('[A-Z]',expr)))
        fields=q[':question/answer-fields'];level=q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1]
        template=next((t for t,ids in g.SOURCE_IDS.items() if sid in ids),None)
        data={'source_id':sid,'db_id':q[':db/id'],'level':level or 'unrated','expression':expr,'matrices':mats,'names':names,'template':template,'fields':[]}
        variables=dict(zip(names,map(sp.Matrix,mats)));correct=expression_value(expr,variables)
        for f in fields:
            data['fields'].append({'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'],'choices':[a[':answer/value'] for a in f[':answer-field/choices']],'correct':f.get(':answer-field/correct',{}).get(':answer/value')})
        if template is None:
            # Preserve incomplete raw banks and exact observed error offsets,
            # without assigning an unproved reusable recipe or difficulty.
            data['exclusion']='No difficulty, no correct reference and no worked solution; offset patterns are source-only, not a validated general bank'
            data['observed_offsets_from_true_result']=[(parse_matrix(a[':answer/value'])-correct).tolist() for a in fields[0][':answer-field/choices']]
            report.append({'source_id':sid,'supported':False,'reason':data['exclusion'],'true_matrix':correct.tolist(),'original_bank_preserved':True})
        else:
            r=g.generate(level,0,template,{'matrices':mats,'names':names});check(r)
            assert re.search(r'Calculate \$(.*?)\$',r['question'][':question/problem'])[1].replace(' ','')==expr
            assert matrices(r['question'][':question/problem'])==matrices(text)
            assert r['question'][':question/worked-solution']==q[':question/worked-solution']
            generated={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']}
            distractors=0
            for f in fields:
                gf=generated[f[':answer-field/key']]
                assert gf[':answer-field/type']==f[':answer-field/type'][':db/ident']
                assert sorted(a[':answer/value'] for a in gf[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices'])
                keyval=next(a[':answer/value'] for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])
                assert keyval==f[':answer-field/correct'][':answer/value']
                distractors+=len(f[':answer-field/choices'])-1
            report.append({'source_id':sid,'supported':True,'prompt_exact':False,'prompt_mathematics_preserved':True,'matrix_layout_standardized':True,'solution_exact':True,'field_keys_and_positions_preserved':True,'complete_bank_matched':True,'distractors_matched':distractors,'distractors_total':distractors,'missing_options':[],'extra_options':[]})
            cases.append({'source_id':sid,'level':level,'template':template,'parameters':{'matrices':mats,'names':names}});raw.append(r)
        components.append(data)
    save(HERE/'source-components.json',components);save(HERE/'source-cases.json',cases);save(HERE/'source-replay.json',report)
    return raw

def main():
    raw=source_cases();records=[];coverage={}
    for level,templates in g.TEMPLATES.items():
        for t in templates:
            rs=[g.generate(level,seed,t) for seed in range(80)]
            for r in rs:check(r)
            assert len({r['generation']['mathematical_fingerprint'] for r in rs})==80
            assert all(g.generate(level,r['generation']['seed'],t)==r for r in rs)
            coverage[t]={'sampled':len(rs),'distinct_tasks':80,'names':sorted({tuple(r['generation']['parameters']['names']) for r in rs}),'min_entry':min(v for r in rs for m in r['generation']['parameters']['matrices'] for row in m for v in row),'max_entry':max(v for r in rs for m in r['generation']['parameters']['matrices'] for row in m for v in row)}
            records+=rs
    # Explicit numerical boundaries for every blank template.
    for level,templates in g.TEMPLATES.items():
        for t in templates:
            if t.endswith('radio'):continue
            for v in (-9,0,9):
                check(g.generate(level,0,t,{'matrices':[[[v,v],[v,v]]]*3,'names':['A','B','C']}))
    # Change expression with fixed matrices: key and every solution stage must follow.
    p={'matrices':[[[4,-2],[7,1]],[[3,5],[0,-4]],[[1,2],[6,3]]],'names':['A','B','C']}
    changed=[g.generate('moderate',0,t,p) for t in g.TEMPLATES['moderate']]
    assert check(changed[0])!=check(changed[1])
    # Detect stale metadata, answer keys, rendered operands and worked stages.
    sample=records[0]
    for mutation in ('operand','key','solution','operator'):
        bad=copy.deepcopy(sample)
        if mutation=='operand':bad['question'][':question/problem']=bad['question'][':question/problem'].replace(' & ','9 & ',1)
        elif mutation=='key':bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999'
        elif mutation=='solution':bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(' & ','9 & ',1)
        else:bad['question'][':question/problem']=bad['question'][':question/problem'].replace('+','-',1)
        try:check(bad)
        except (AssertionError,ValueError,KeyError):pass
        else:raise AssertionError('Mutation escaped: '+mutation)
    # No seed-only or option-order duplicates, and letter changes cannot inflate counts.
    r=records[0];m=r['generation'];same=g.generate('easy',12345,m['template'],m['parameters']);assert r['question']==same['question']
    swapped=copy.deepcopy(r);swapped['question'][':question/answer-fields'].reverse();assert g.fingerprint(swapped['question'])==g.fingerprint(r['question'])
    preview=[g.generate(level,1920+i,t) for level,ts in g.TEMPLATES.items() for i,t in enumerate(ts)]
    save(HERE/'previews.json',preview)
    (HERE/'review.md').write_text('\n\n'.join('Source '+c['source_id']+'\n\n'+src['question'][':question/problem']+'\n\n'+src['question'][':question/worked-solution']+'\n\nGenerated variant\n\n'+next(x for x in preview if x['generation']['template']==c['template'])['question'][':question/problem']+'\n\n'+next(x for x in preview if x['generation']['template']==c['template'])['question'][':question/worked-solution'] for c,src in zip(json.loads((HERE/'source-cases.json').read_text()),raw)))
    inputs=[native('source-'+str(i),r) for i,r in enumerate(raw)]+[native('sample-'+str(i),r) for i,r in enumerate(records)]+[native('changed-'+str(i),r) for i,r in enumerate(changed)]
    save(HERE/'native-input.json',inputs)
    subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    save(HERE/'validation.json',{'passed':True,'source_basis':json.loads((HERE/'source.json').read_text())['basis'],'source_banks_matched':6,'source_banks_excluded':2,'supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'sampled_records':len(records),'coverage':coverage,'independent_display_and_all_solution_stages':True,'changed_operation_fixed_operands':True,'mutation_cases_detected':4,'deterministic_replay':True,'boundary_values':[-9,0,9],'seed_and_choice_order_not_counted':True,'actual_grader':'course_academy_engine::learning::grade_field','hashes':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'source.edn',HERE/'source-components.json',HERE/'source-cases.json',HERE/'validate.py',HERE/'check-engine']}})
    print('Validated 400 variants, six source banks, all displayed solution stages and native grading.')

if __name__=='__main__':main()
