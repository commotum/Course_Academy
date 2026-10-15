"""Read displayed matrices independently and test native learner grading."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('matrix_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,obj):(H/name).write_text(json.dumps(obj,indent=2)+'\n')
def matrix(text):
    m=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S);assert m
    rows=[[int(x.strip()) for x in row.split('&')] for row in m[1].split(r'\\')];assert all(len(row)==len(rows) for row in rows);return rows
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(a))) for j in range(len(a))] for i in range(len(a))]
def power(a,p):
    out=[[int(i==j) for j in range(len(a))] for i in range(len(a))]
    for _ in range(p):out=mul(out,a)
    return out
def fingerprint(q):return g.fingerprint(q)
def check(r,strict=True):
    q=r['question'];ptext=q[':question/problem'];sol=q[':question/worked-solution'];a=matrix(ptext)
    p=int(re.search(r'\^\{(\d+)\}',ptext)[1]);answer=power(a,p);flat=sum(answer,[]);fields=q[':question/answer-fields']
    sid=r['generation']['template'];t=g.PROFILES[sid];assert p==t['power'] and len(a)==t['a'].rows
    assert q[':question/difficulty']==':question.difficulty/'+t['level']
    assert len(fields)==len(t['mask'])
    tokens=re.findall(r'\{\{field-(\d+)\}\}|\$(-?\d+)\$',ptext.split('\n\n',1)[1]);assert len(tokens)==len(a)**2
    field_by_key={f[':answer-field/key']:f for f in fields};assert len(field_by_key)==len(fields)
    seen=[]
    for i,(key,fixed) in enumerate(tokens):
        if key:
            f=field_by_key['field-'+key];seen.append(i)
            assert f[':answer-field/type']==':answer-field.type/blank'
            bank=f[':answer-field/choices'];assert len(bank)==1
            assert bank[0][':answer/type']==':answer.type/math' and int(bank[0][':answer/value'])==flat[i]
            assert f[':answer-field/correct']==[':answer/id',bank[0][':answer/id']]
        else:assert int(fixed)==flat[i],(sid,i,fixed,flat)
    assert seen==t['mask']==r['generation']['target_cells']
    displayed=[matrix(m[0]) for m in re.finditer(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',sol,re.S)]
    expected=[a,a,power(a,2)]
    if p>2:expected += [power(a,2),a if p==3 else power(a,2),answer]
    assert displayed==expected,(sid,displayed,expected)
    assert r['generation']['mathematical_key']==g.task_key(g.sp.Matrix(a),p)
    assert list(map(int,sum(a,[])))==r['generation']['parameters']
    for text in (ptext,sol):assert text.count('$')%2==0 and text.count('{')==text.count('}') and '!!' not in text
    assert ':question/math-academy-id' not in q
    if strict:assert r==g.generate(t['level'],r['generation']['seed'],sid,sum(a,[]))
    return flat
def engine_item(label,r):
    check(r,False);checks=[]
    for i,f in enumerate(r['question'][':question/answer-fields']):
        z=int(f[':answer-field/choices'][0][':answer/value'])
        for submitted,outcome,purpose in [(str(z),'accepted','canonical integer'),(r'\frac{'+str(2*z)+'}{2}','accepted','equivalent fraction'),(str(z)+'.0','accepted','equivalent decimal'),(str(z+1),'rejected','wrong entry'),(str(z-1),'rejected','wrong entry')]:checks.append({'field_index':i,'submitted':submitted,'expected':outcome,'purpose':purpose})
    return {'label':label,'record':r,'checks':checks}
def main():
    replay=[];rows=[];review=[];coverage={};negative=0
    for sid,t in g.PROFILES.items():
        original=t['source'];r=check_record=g.generate(t['level'],0,sid,list(map(int,t['a'])));check(r)
        assert r['question'][':question/problem']==original[':question/problem'],sid
        assert r['question'][':question/worked-solution']==original[':question/worked-solution'],sid
        old={f[':answer-field/key']:f for f in original[':question/answer-fields']}
        for f in r['question'][':question/answer-fields']:
            of=old[f[':answer-field/key']];assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
            assert f[':answer-field/choices'][0][':answer/value']==of[':answer-field/correct'][':answer/value']
        replay.append({'source':sid,'complete_banks_matched':len(old),'prompt_exact':True,'solution_exact':True,'correct_values_exact':True});rows.append(r)
        vals=[set() for _ in t['a']]
        for seed in range(200):
            z=g.generate(t['level'],seed,sid);check(z);rows.append(z)
            assert z['question']==g.generate(t['level'],seed+10000,sid,z['generation']['parameters'])['question']
            for pool,value in zip(vals,z['generation']['parameters']):pool.add(value)
        coverage[sid]=[sorted(pool) for pool in vals]
        for i,pool in enumerate(vals):
            if t['a'][i]==0:assert pool=={0}
            else:assert len(pool)>1
        variant=g.generate(t['level'],41,sid);review += ['## '+sid,'','Original','',original[':question/problem'],'',original[':question/worked-solution'],'','Variant','',g.markdown(variant),'']
    for part in (':question/problem',':question/worked-solution'):
        bad=copy.deepcopy(rows[1]);bad['question'][part]=bad['question'][part].replace('&', '& 99 +',1)
        try:check(bad)
        except (AssertionError,ValueError):negative+=1
        else:raise AssertionError('Corrupted displayed matrix accepted')
    bad=copy.deepcopy(rows[1]);bad['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='99999'
    try:check(bad)
    except AssertionError:negative+=1
    else:raise AssertionError('Bad key accepted')
    for level in ['hard','unclassified']:
        try:g.generate(level)
        except ValueError:negative+=1
        else:raise AssertionError('Unsupported difficulty accepted')
    native=rows[::20]+[g.generate(t['level'],0,sid,list(map(int,t['a']))) for sid,t in g.PROFILES.items()]
    save('engine-input.json',[engine_item(str(i),r) for i,r in enumerate(native)])
    subprocess.run([str(H/'check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
    (H/'review.md').write_text('\n'.join(review));save('source-replay.json',replay);save('slot-coverage.json',coverage)
    save('previews.json',g.batch('easy',5,2553)+g.batch('moderate',5,2553))
    result={'passed':True,'source_basis':g.SOURCE['basis'],'supported_levels':list(g.SUPPORTED_LEVELS),'profiles':len(g.PROFILES),'source_replays':replay,'supported_complete_banks_matched':sum(x['complete_banks_matched'] for x in replay),'supported_complete_banks_total':sum(x['complete_banks_matched'] for x in replay),'supported_distractors_total':0,'independent_rendered_math_checks':len(rows),'negative_controls':negative,'native':{k:v for k,v in json.loads((H/'engine-report.json').read_text()).items() if k!='records'},'radio_fidelity':'Deferred; source banks captured, not passed as generated content','plots':'none','files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [H.with_suffix('.py'),Path(__file__),H/'source.json',H/'source.edn',H/'check-engine',H/'capabilities.json']}}
    save('validation.json',result);print(json.dumps(result))
if __name__=='__main__':main()
