"""Check printed mathematics, band workload, variation, delivery, and grader fixtures."""
from collections import Counter, defaultdict
import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

H = Path(__file__).resolve().parent;ROOT = H.parents[3]
sys.path.insert(0,str(H));sys.path.insert(0,str(ROOT))
from read_math import X, scalar, check, source_prompt, key
from generate.pipeline.check_delivery import audit
from scripts.generator_publish import normalized_question

KPS = (17592186064218,17592186064219,17592186064250,17592186064220)
SEED = 864218


def save(path, value):
    path = H/path;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,default=str,indent=2)+'\n')


def module(kp):
    path = H/'packages'/str(kp)/'generator.py';s = importlib.util.spec_from_file_location('checked_'+str(kp),path)
    m = importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def main():
    pool = [];samples = [];equalities = 0;coverage = {};delivery = [];grader = [];render = [];controls = []
    for kp in KPS:
        g = module(kp);source = json.loads((H/'source'/f'{kp}.json').read_text());inventory = json.loads((H/'source'/str(kp)/'inventory.json').read_text())
        evidence = g._generator.evidence
        assert len(evidence['originals']) == len(source['material']['kp'][':knowledge-point/questions'])+1
        for original in evidence['originals']:
            assert g.source_original(original[':question/math-academy-id']) == original
            body,lo,hi = source_prompt(original[':question/problem']);assert key(body,lo,hi) in g._generator.excluded
        per_band = {}
        count = 10 if kp == 17592186064220 else 8
        full_batch = g.batch('all',count,SEED)
        assert full_batch == g.batch('all',count,SEED)
        assert len({r['generation']['mathematical_fingerprint'] for r in full_batch}) == len(full_batch)
        for band in ('easy','moderate','hard'):
            rows = [r for r in full_batch if r['question'][':question/difficulty'].endswith('/'+band)]
            assert len({r['generation']['mathematical_fingerprint'] for r in rows}) == count
            members = []
            for case in g.CASES[band]:
                # Explicit coverage is independent of the final batch size.
                for seed in (17,181,1907): members.append(g.generate(band,seed,case))
            coverage_rows = members+rows
            cov = defaultdict(set);positions = defaultdict(set)
            for r in coverage_rows:
                result = check(r,r['generation']['inverse_function']);equalities += result['equalities']
                meta = r['generation'];p = meta['parameters'];case = meta['template'];cov['case'].add(case)
                for name in ('A','B','N','D','lower_u','upper_u'):cov[name].add(p[name])
                cov['response'].add(meta['response']);cov['inverse_function'].add(meta['inverse_function'])
                if meta['family'] == 'definite':
                    if band == 'hard':assert p['lower_u'] != '0' and p['upper_u'] != '0' and scalar(p['A'])>1 and scalar(p['B'])>1
                    cov['interval'].add((p['lower_u'],p['upper_u']))
                f = r['question'][':question/answer-fields'][0]
                if f[':answer-field/type'].endswith('/radio'):
                    index = next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id'] == f[':answer-field/correct'][1]);positions[case].add(index)
            assert cov['case'] == set(g.CASES[band])
            assert len(cov['B' if band == 'easy' else 'A']) > 1 or kp == 17592186064250
            for case, found in positions.items():assert len(found)>1, (kp,band,case,'constant keyed position',found)
            if kp == 17592186064220:assert cov['response'] == {'radio','blank'}
            per_band[band] = {k:sorted(v,key=str) for k,v in cov.items()} | {'key_positions_per_case':{k:sorted(v) for k,v in positions.items()}}
            samples += members
            out = H/'delivery'/str(kp)/band
            report = audit(rows,inventory,source,band,out,H/'packages'/str(kp),Path('/media/jake/SSD/EDB/math'))
            accepted = json.loads((out/'accepted.json').read_text())
            assert len(accepted) == count and report['duplicate_count'] == 0
            for before,after in zip(rows,accepted):
                assert normalized_question(before['question'],identity=False) == normalized_question(after['question'],identity=False)
                check(after,after['generation']['inverse_function'])
            delivery.append(report);pool += accepted
            save(Path('pools')/f'{kp}-{band}.json',accepted)
            # One actual UI case for every KP/band; add definite blank fragments below.
            render.append(accepted[0])
        coverage[str(kp)] = per_band
        # A changed numerator must update the answer while leaving the substitution fixed.
        band,case = {17592186064218:('moderate','integer-numerator'),17592186064219:('moderate','independent-numerator'),
                     17592186064250:('hard','radical-normalization'),17592186064220:('hard','sine-two-positive')}[kp]
        a = g.generate(band,89,case);params = dict(a['generation']['parameters'])
        for delta in (2,3,4,5):
            params['N'] = str(scalar(a['generation']['parameters']['N'])+delta)
            try:b = g.build(band,case,params)
            except ValueError:continue
            break
        else:raise AssertionError('No fresh numerator counterfactual')
        left = check(a,a['generation']['inverse_function']);right = check(b,b['generation']['inverse_function'])
        assert left['slope'] == right['slope'] and scalar(params['N'])>0
        assert left['answer'] != right['answer'];controls.append({'kp':kp,'check':'independent numerator changes answer, not substitution','passed':True})
        same = g.build(band,case,a['generation']['parameters'],seed=123456789,bank_profile=a['generation']['bank_profile'])
        assert normalized_question(a['question']) == normalized_question(same['question']);controls.append({'kp':kp,'check':'seed-only option reordering preserves question identity, mathematical content, and key','passed':True})
        broken = copy.deepcopy(a)
        broken['question'][':question/worked-solution'] = re.sub(r'\\mathrm\{d\}x=\(.*?\)',lambda _:r'\mathrm{d}x=(123)',broken['question'][':question/worked-solution'],count=1)
        assert broken != a
        try:check(broken,a['generation']['inverse_function'])
        except AssertionError:controls.append({'kp':kp,'check':'incorrect printed reciprocal factor rejected','passed':True})
        else:raise AssertionError('Printed-math checker accepted corrupt differential')
        if kp in (17592186064218,17592186064219,17592186064220):
            hard = g.generate('hard',65,next(iter(g.CASES['hard'])));params = dict(hard['generation']['parameters']);params['A']='1'
            try:g.build('hard',hard['generation']['template'],params)
            except ValueError:controls.append({'kp':kp,'check':'hard band rejects easy normalization workload','passed':True})
            else:raise AssertionError('Easy workload accepted as hard')
        if kp == 17592186064220:
            singular = g.generate('hard',67,'sine-cross-zero');params = dict(singular['generation']['parameters']);params.update(lower_u='-1',upper_u='1')
            try:g.build('hard','sine-cross-zero',params)
            except ValueError:controls.append({'kp':kp,'check':'both singular arcsine endpoints rejected','passed':True})
            else:raise AssertionError('Singular endpoint profile accepted')
        save(Path('verification')/f'{kp}-coverage.json',per_band)
    for i,r in enumerate(pool):
        checks = []
        for index,f in enumerate(r['question'][':question/answer-fields']):
            if f[':answer-field/type'].endswith('/radio'):
                checks += [{'field_index':index,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected'} for a in f[':answer-field/choices']]
            else:
                value = scalar(f[':answer-field/choices'][0][':answer/value'])
                checks += [{'field_index':index,'submitted':f[':answer-field/choices'][0][':answer/value'],'expected':'accepted'},
                           {'field_index':index,'submitted':str(value),'expected':'accepted'},
                           {'field_index':index,'submitted':str(value+1),'expected':'rejected'}]
        grader.append({'label':'published-'+str(i),'record':r,'checks':checks})
    render += [next(r for r in pool if r['generation']['response']=='blank' and len(r['question'][':question/answer-fields'])==2),
               next(r for r in pool if r['generation']['template']=='sine-cross-zero' and r['generation']['response']=='blank')]
    save(Path('candidate-pool.json'),pool);save(Path('regression-samples.json'),samples);save(Path('grader-input.json'),grader);save(Path('render-input.json'),render)
    report = {'passed':True,'printed_records_checked':len(samples)+len(pool),'printed_equalities_checked':equalities,
              'candidate_pool_counts':dict(Counter(str(r['knowledge_point']['db_id'])+'/'+r['question'][':question/difficulty'].split('/')[-1] for r in pool)),
              'new_questions':len(pool),'delivery_accepted':sum(r['accepted_count'] for r in delivery),'delivery_duplicates':sum(r['duplicate_count'] for r in delivery),
              'coverage':coverage,'controls':controls,'source_fidelity':'All 79 original practice/canonical records archived exactly; new banks are explicitly authored, not claimed exact source-bank parameterizations.',
              'difficulty_calibration':'Sine/tangent hard, secant easy, and the uniform definite-hard contract are authored compositions, not externally calibrated labels.'}
    save(Path('generator-verification.json'),report);save(Path('delivery-verification.json'),delivery)
    print(json.dumps({k:v for k,v in report.items() if k not in ('coverage','controls')},indent=2),flush=True)


if __name__ == '__main__':main()
