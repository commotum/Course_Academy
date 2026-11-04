#!/usr/bin/env python3
"""Independent CLI/visible-TeX, choice and portability regressions for one package."""
from pathlib import Path
import collections,copy,hashlib,importlib.util,json,math,re,shutil,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
PKG=HERE.parent
REPO=HERE.parents[5]
sys.path.insert(0,str(HERE))
from numeric_audit import audit,field_key,nodes,Numeric
from solution_reader import check as check_solution
KP=PKG.name

def cli(band,count,seed,path=PKG):
    command=[sys.executable,str(path/'generator.py'),'--difficulty',band,'--count',str(count),'--seed',str(seed),'--format','json']
    p=subprocess.run(command,capture_output=True,text=True,check=True,cwd='/tmp')
    data=json.loads(p.stdout)
    assert len(data)==count
    return data,command

def verify(records,label,all_distinct=True):
    rows=[]
    for i,r in enumerate(records):
        q=r['question'];row=audit(q,label+'/'+str(i),KP)
        assert row['status']=='match',row
        assert not row['choice_ambiguities'],row
        for f in q[':question/answer-fields']:
            vals=[Numeric(nodes(x[':answer/value']),{}).evaluate() for x in f[':answer-field/choices']]
            assert all(math.isfinite(v) for v in vals),(label,i,vals)
            if all_distinct:assert all(abs(a-b)>1e-8*max(1,abs(a),abs(b)) for j,a in enumerate(vals) for b in vals[:j]),(label,i,vals)
        sol=check_solution(q,label+'/'+str(i),KP)
        assert not sol.get('suspected_bad_equalities'),sol
        assert not sol.get('unparsed_equalities'),sol
        row['solution_equalities']=sol['checks']
        rows.append(row)
    return rows

def main():
    results=[];commands=[];records=[];coverage={};math_checks=[]
    counts={'easy':4,'moderate':16,'hard':16} if KP=='17592186059672' else {'easy':24,'moderate':16,'hard':16} if KP=='17592186059674' else dict.fromkeys(('easy','moderate','hard'),24)
    for band in ('easy','moderate','hard'):
        for seed,count in ((47,4 if band=='easy' else 5),(83,4 if band=='easy' else 5),(109,counts[band])):
            data,cmd=cli(band,count,seed);commands.append(cmd)
            name=f'{band}-{seed}.json';(HERE/name).write_text(json.dumps(data,indent=2)+'\n')
            math_checks.extend(verify(data,name));records.extend(data)
            assert all(r['question'][':question/difficulty']==':question.difficulty/'+band for r in data)
            # The CLI batch does not count unit/bank/ordering changes as new mathematical instances.
            signature=[]
            for r in data:
                gen=r['generation'];params=gen['parameters']
                if KP=='17592186059671':sig=(gen['family'],params['a'],params['unit'],params['k'],params['sign'] if gen['family']=='square' else None)
                elif KP=='17592186059672':sig=(gen['template'],params['end_degrees'],params['coefficient'],gen['symbolic_terminal'])
                elif KP=='17592186059673':sig=(gen['template'],params['role'],params['sign'],params['k'],str(params['angle'])+'/'+params['unit'],params.get('product'))
                else:sig=(gen['template'],params['doubled_degrees'],params['multiplier'],params['square_sign'] if gen['template']=='square' else None)
                signature.append(sig)
                prompt=r['question'][':question/problem']
                if gen.get('symbolic_terminal'):
                    assert params['unit']=='radians',params
                    assert r'\circ' not in prompt,prompt
                assert not re.search(r'\b(?:Use|Recall|first with|then with|using the sine of twice)\b',prompt),prompt
                # A printed 1 function/product multiplier is not useful arithmetic.
                content=prompt+'\n'+r['question'][':question/worked-solution']
                assert not re.search(r'(?<![\d{])1(?:\\,)?\\(?:sin|cos|tan|sec|csc|cot|left\()',content),content
            assert len(signature)==len(set(signature)),(band,seed,'semantic repeats')
            coverage[f'{band}-{seed}']=dict(collections.Counter((r['generation'].get('family') or r['generation']['template'])+(':symbolic' if r['generation'].get('symbolic_terminal') else '') for r in data))
        # Check replay of the exact current seeded CLI, not internal make() alone.
        assert cli(band,4 if band=='easy' else 5,47)[0]==json.loads((HERE/f'{band}-47.json').read_text())
        assert cli(band,0,47)[0]==[]
    if KP=='17592186059671':
        assert all('hidden' not in key for c in coverage.values() for key in c)
        for band in ('moderate','hard'):assert {'square','quotient'}<=set(coverage[f'{band}-47'])
    if KP=='17592186059672':
        assert {'product','cancellation','product:symbolic'}<=set(coverage['moderate-109'])
        assert {'pair_over_sec','sec_over_pair'}<=set(coverage['hard-47'])
        assert all(r['generation']['parameters']['coefficient'] in ('4','8') for r in json.loads((HERE/'easy-109.json').read_text()))
        excess=subprocess.run([sys.executable,str(PKG/'generator.py'),'--difficulty','easy','--count','5','--seed','47','--format','json'],capture_output=True,text=True)
        assert excess.returncode and 'four distinct' in excess.stderr
        old=json.loads((REPO/'reference/edb-math/audits/2026-11-04-four-trig-lessons/kps'/KP/'samples/easy-7.json').read_text())
        assert any('Use $2\\sin' in r['question'][':question/problem'] for r in old)
    if KP=='17592186059673':
        assert {'direct','quotient'}<=set(coverage['easy-109'])
        assert {'complement','binomial'}<=set(coverage['hard-47'])
    if KP=='17592186059674':
        assert set(coverage['moderate-109'])=={'square'}
        assert set(coverage['hard-109'])=={'sin_sec','cos_csc'}
    # Independent mathematical reader must reject an actually wrong current key.
    bad=copy.deepcopy(next(r for r in records if len(r['question'][':question/answer-fields'][0][':answer-field/choices'])>1));f=bad['question'][':question/answer-fields'][0]
    key=field_key(f);other=next(a for a in f[':answer-field/choices'] if a[':answer/value']!=key)
    f[':answer-field/correct']=[':answer/id',other[':answer/id']]
    assert audit(bad['question'],'negative-control',KP)['status']=='mismatch'
    # Runtime relocation includes exactly the declared closure, with no repository Python path.
    manifest=json.loads((PKG/'runtime-manifest.json').read_text())
    with tempfile.TemporaryDirectory(prefix='sine-double-runtime-') as tmp:
        relocated=Path(tmp)
        for name in manifest['runtime_files']:shutil.copy2(PKG/name,relocated/name)
        for band in ('easy','moderate','hard'):
            actual,cmd=cli(band,4 if band=='easy' else 5,47,relocated)
            assert actual==json.loads((HERE/f'{band}-47.json').read_text())
    # Imported sources are retained as evidence, not silently completed or fixed.
    evidence=json.loads((PKG/'source-evidence.json').read_text());source_checks=[]
    for q in evidence['imported_practice']:
        row=audit(q,str(q[':db/id']),KP)
        assert row['status'] in ('match','no_response_key'),row
        assert not row.get('choice_ambiguities'),row
        source_checks.append(row)
    if KP=='17592186059672':
        source=json.loads((PKG/'source-replay.json').read_text())
        for item in source:
            cmd=[sys.executable,str(PKG/'generator.py'),'--replay-source',item['id'],'--format','json']
            d=json.loads(subprocess.run(cmd,capture_output=True,text=True,check=True,cwd='/tmp').stdout)
            math_checks.extend(verify(d,'source-replay/'+item['id'],all_distinct=False))
    elif KP=='17592186059673':
        d=json.loads(subprocess.run([sys.executable,str(PKG/'generator.py'),'--replay-source','--format','json'],capture_output=True,text=True,check=True,cwd='/tmp').stdout)
        math_checks.extend(verify(d,'source-replay'))
    elif KP=='17592186059674':
        for r in json.loads((PKG/'source-replays.json').read_text()):
            ident=r['generation']['source_question_ids'][0]
            d=json.loads(subprocess.run([sys.executable,str(PKG/'generator.py'),'--replay-source',ident,'--format','json'],capture_output=True,text=True,check=True,cwd='/tmp').stdout)
            # Source replay stores original solutions; mathematical source defects are reported separately.
            row=audit(d[0]['question'],'source-replay/'+ident,KP)
            assert row['status']=='match' and not row['choice_ambiguities'],row
            source_checks.append(row)
    (HERE/'numeric-results.json').write_text(json.dumps(math_checks,indent=2)+'\n')
    (HERE/'source-results.json').write_text(json.dumps(source_checks,indent=2)+'\n')
    report={'status':'passed','kp':KP,'cli_records_checked':len(records),'math_key_and_all_choice_checks':len(math_checks),'solution_equalities':sum(x.get('solution_equalities',0) for x in math_checks),'commands':commands,'coverage':coverage,'checks':['independent visible-TeX numeric keys','all pairwise choice distinctions','solution equality witnesses','no easy method leak','no neutral 1 multipliers','seed replay','zero count','semantic batch uniqueness','runtime closure relocation','source keys or partial-source retention','negative wrong-key control'],'limits':['Numeric witnesses do not prove symbolic equality for all possible generator inputs.','Root owner performs actual UI rendering, native learner grading and publication/inventory filtering.']}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','kp','cli_records_checked','math_key_and_all_choice_checks','solution_equalities')}))
if __name__=='__main__':main()
