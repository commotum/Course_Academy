"""Complete source-bank replay and bounded source-scaling release validation."""
from pathlib import Path
import json,hashlib,subprocess,sys,copy
import validation_support as v
H=v.H;g=v.g;ROOT=H.parents[2]
def save(n,x):(H/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
ledger=[];records=[];review=[];coverage={};stages=0
for name,source in g.Q.items():
    level=g.SPEC[name][-1];original=g.generate(level,template=name,profile='raw_'+name,parameters={'scale':1})
    normal=g.generate(level,template=name,parameters={'scale':1})
    v.independent(normal)
    fields=[]
    for a,b in zip(normal['question'][':question/answer-fields'],source[':question/answer-fields']):
        parse=g.tuple_math if a[':answer-field/type'].endswith('/radio') else lambda t:(g.parse(t),)
        av={tuple(map(str,parse(x[':answer/value']))) for x in a[':answer-field/choices']}
        bv={tuple(map(str,parse(x[':answer/value']))) for x in b[':answer-field/choices']}
        assert av==bv and len(av)==len(a[':answer-field/choices'])==len(b[':answer-field/choices'])
        if ':answer-field/correct' in b:
            chosen=next(x for x in a[':answer-field/choices'] if x[':answer/id']==a[':answer-field/correct'][1])
            assert parse(chosen[':answer/value'])==parse(b[':answer-field/correct'][':answer/value'])
        fields.append({'key':a[':answer-field/key'],'matched':len(av),'total':len(bv),'missing':[],'extra':[],'correct_source_key_present':':answer-field/correct' in b})
    ledger.append({'source':name,'profile':normal['generation']['profile'],'fields':fields,'prompt_exact':normal['question'][':question/problem']==source[':question/problem'],'solution':'axis prose correction' if name=='q-276838' else 'authored completion' if ':question/worked-solution' not in source else 'exact'})
    cases=[]
    for scale in range(1,17 if level=='hard' else 9):
        r=g.generate(level,template=name,parameters={'scale':scale});stages+=v.verify(r);v.independent(r);records.append(r);cases.append(v.fingerprint(r['question']))
        # Each complete option follows its source's whole-coordinate scaling recipe.
        for f,sf in zip(r['question'][':question/answer-fields'],source[':question/answer-fields']):
            parse=g.tuple_math if f[':answer-field/type'].endswith('/radio') else lambda t:(g.parse(t),)
            power=2 if g.SPEC[name][3]=='square' else 1
            want={tuple(str(v.s.simplify(x*scale**power)) for x in parse(a[':answer/value'])) for a in sf[':answer-field/choices']}
            got={tuple(map(str,parse(a[':answer/value']))) for a in f[':answer-field/choices']};assert got==want
    assert len(set(cases))==len(cases)
    coverage[name]={'scales':list(range(1,len(cases)+1)),'distinct_printed_tasks':len(set(cases)),'role':'positive similarity of A; B radius linear or squared; angular workload fixed'}
    review.append({'source_id':name,'source':source,'variants':[g.generate(level,template=name,parameters={'scale':x}) for x in (2,3)]})
# Authored easy family is unchanged from the exhaustively checked draft logic.
# Recheck all boundaries, every angle, every factor, both layouts and deterministic IDs.
for radius in (1,12):
    for factor in (2,3,4,5):
        for angle in ['1/6','1/3','2/3','5/6','7/6','4/3','5/3','11/6']:
            for field_type in ('radio','blank'):
                r=g.generate('easy',field_type=field_type,parameters={'radius':radius,'factor':factor,'angle':angle});stages+=v.verify(r);v.independent(r);records.append(r)
for level in g.SUPPORTED_LEVELS:
    for seed in range(20):
        a=g.generate(level,seed);assert a==g.generate(level,seed);v.independent(a)
        b=g.generate(level,seed+900,template=a['generation']['template'],profile=a['generation']['profile'],parameters=a['generation']['parameters'],field_type=a['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1]);assert a['question'][':question/id']==b['question'][':question/id']
# Print a changed mathematical instance alongside its source. A mutation of the final key must fail.
r=copy.deepcopy(records[0]);f=r['question'][':question/answer-fields'][0];f[':answer-field/correct'][1]=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1])
try:v.verify(r)
except AssertionError:pass
else:raise AssertionError('Incorrect key not detected')
fixtures=[{'label':str(i),'record':r,'checks':v.checks(r)} for i,r in enumerate(records)]
save('reference/release-native-input.json',fixtures)
engine=ROOT/'generate/runs/current/check-engine'
subprocess.run([str(engine),str(H/'reference/release-native-input.json'),str(H/'reference/release-native-report.json')],check=True)
e=json.loads((H/'reference/release-native-report.json').read_text());assert e['documented_unresolved_checks']==0
save('source-bank-replay.json',ledger);save('slot-coverage.json',coverage);save('release-review.json',review)
md=[]
for item in review:
    md+=['## '+item['source_id'],'### Original',item['source'][':question/problem'],item['source'].get(':question/worked-solution','Original solution absent')]
    for r in item['variants']:md+=['### Generated positive scale '+str(r['generation']['parameters']['scale']),g.markdown(r)]
(H/'release-review.md').write_text('\n\n'.join(md)+'\n')
paths=[H.with_suffix('.py'),H/'masks.json',H/'source.json',H/'validate.py',H/'validation_support.py',Path(__file__),engine]
report={'status':'pass','source_basis':1356,'current_confirmation_basis':json.loads((H/'reference/initial/source.json').read_text())['basis'],'source_banks':7,'source_choices_matched':35,'source_blank_answers_matched':6,'source_records_replayed':10,'source_key_omissions_retained':2,'source_scaling_domain_records':104,'easy_boundary_records':128,'independent_printed_stages':stages,'source_profiles_complete':True,'native':{k:e[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'limitations':['Source bank recipes are explicit positive whole-coordinate scaling. Historical error interpretation is unresolved and no learner-facing diagnosis is invented.','Two unrated incomplete sources remain unchanged; generated completions have explicit authored difficulty and solutions.','Easy is authored from the frozen curriculum and canonical radius-inference method; it is not an observed easy practice band.','q-276838 original axis/quadrant prose error is preserved in EDB; generated variants use positive x-axis.']}
save('release-validation.json',report);print(json.dumps(report,indent=2))
