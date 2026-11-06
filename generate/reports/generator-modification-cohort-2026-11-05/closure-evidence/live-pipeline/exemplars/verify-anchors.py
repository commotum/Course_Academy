import hashlib,json,re,sys
from pathlib import Path
sys.path.insert(0,'/home/jake/Developer/Course_Academy')
from scripts.generator_evidence import record_sha256
from scripts.generator_native_build import build_inputs
r=Path(__file__).resolve().parent
solved=json.loads((r/'independent-solving.json').read_text())['cases']
requests=json.loads((r/'grading-input.json').read_text())
examples=json.loads(Path('/tmp/generator-live-pipeline/workspace/exemplars.json').read_text())
for n,band in enumerate(['easy','moderate','hard']):
    assert json.loads((r/f'{band}-anchor.json').read_text())==[examples[n]]
    for stage,filename in [('raw',f'{band}-anchor.json'),('delivered',f'delivery-{band}/accepted.json')]:
        record=json.loads((r/filename).read_text())[0]
        q=record['question'];text=q[':question/problem']
        cells=re.search(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}',text,re.S).group(1)
        matrix=[[int(x) for x in row.split('&')] for row in cells.split('\\\\')]
        i,j=map(int,re.search(r'find \$a_\{([12])([12])\}',text).groups())
        expected=matrix[i-1][j-1];reverse=matrix[j-1][i-1]
        evidence=next(c for c in solved if c['band']==band and c['stage']==stage)
        assert evidence['record_sha256']==record_sha256(record)
        assert evidence['matrix']==matrix and evidence['independently_computed']==expected
        assert evidence['reversed_index_error']==reverse and evidence['sign_error']==-expected
        f=q[':question/answer-fields'][0]
        key=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
        assert int(key)==expected
        c=re.search(r'\$a_\{([12])([12])\}=(-?\d+)\$',q[':question/worked-solution'])
        assert tuple(map(int,c.groups()))==(i,j,expected)
        controls=next(c for c in requests if c['label']==f'{band}-{stage}')
        assert controls['record']==record
        assert [(c['submitted'],c['expected']) for c in controls['checks']]==[(str(expected),'accepted'),(f'{expected}/1','accepted'),(str(reverse),'rejected'),(str(-expected),'rejected')]
        assert expected!=reverse and expected!=0
assert build_inputs('/tmp/generator-live-pipeline/workspace/evidence/native-root')==build_inputs('/home/jake/Developer/Course_Academy')
assert hashlib.sha256((r/'source-analysis.json').read_bytes()).hexdigest()=='f4e2cdd70726c82b96396236ac7094d8f74d21fac0ebb01521765e182285e82c'
assert hashlib.sha256(Path('/tmp/generator-live-pipeline/workspace/exemplars.json').read_bytes()).hexdigest()=='3d3d6f29a18986bf2fcf0eac3cfdc31e9292caec5ac9ff14a17b0963a85e13b1'
assert hashlib.sha256(Path('/tmp/generator-live-pipeline/workspace/investigation.md').read_bytes()).hexdigest()=='bac8ec1af94ab9e06f2a9ca04ac7e8578aad0fc10802722e81ef29df7338118d'
print(json.dumps({'independent_math_and_controls':'passed','raw_and_delivered_cases':6,'initial_account_and_mutable_input_hashes_unchanged':True,'native_sources_equal_production':True}))
