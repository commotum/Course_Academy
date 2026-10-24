"""Verify printed math, support, bounded workload and actual delivery filtering."""
from collections import Counter,defaultdict
import copy
import importlib.util
import json
from pathlib import Path
import random
import re
import sys

import sympy as s

H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import prepare_records,content_fingerprint,validate_question
from scripts.trig_substitution_batch_policy import validate_delivery_batch
from read_math import check,scalar,equal,p


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n')


def load(kp):
    path=H/str(kp)/'package/generator.py'
    spec=importlib.util.spec_from_file_location('scaffold_'+str(kp),path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def grading(row,label):
    result=check(row);field=row['question'][':question/answer-fields'][0]
    if field[':answer-field/type']==':answer-field.type/radio':
        checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==field[':answer-field/correct'][1]else'rejected'}for a in field[':answer-field/choices']]
    else:
        key=result['key'];indef=result['lower']is None
        wrong=r'2\left('+key+r'\right)'if indef else s.latex(result['answer']+1).replace(r'\log',r'\ln')
        checks=[{'submitted':key,'expected':'accepted'},
                {'submitted':r'\frac{2\left('+key+r'\right)}{2}','expected':'accepted'},
                {'submitted':wrong,'expected':'rejected'}]
        if indef:checks.append({'submitted':'('+key+')+1','expected':'accepted','purpose':'Absorb a numeric constant into external C'})
        if row['generation']['family'].startswith('rearranged_'):
            params=row['generation']['parameters'];a=s.Integer(params['amplitude']);d=s.Integer(params['offset'])
            fn='tan'if row['generation']['family'].endswith('tan')else'sec'
            arg=getattr(s,fn)(p.x)
            alternate=s.latex(a*arg)+'-'+s.latex(a*d)+r'\ln\left|'+s.latex(arg+d)+r'\right|'
            checks.append({'submitted':alternate,'expected':'accepted','purpose':'Expand and absorb the back-substitution constant'})
    return {'label':label,'record':row,'checks':checks}


def main():
    summary={};render=[];all_banks=0
    for kp in (17592186068915,17592186068916,17592186068917,17592186068918):
        directory=H/str(kp);g=load(kp)
        pool=[];samples=[];coverage=defaultdict(Counter)
        for band in ('easy','moderate','hard'):
            pool.extend(g.batch(band,8,20261024))
            # An independent seed exercises the same declared cases under other
            # small values. Broad repeats are not a substitute for case coverage.
            samples.extend(g.batch(band,8,112358))
        for row in pool+samples:
            validate_question(row['question']);check(row)
            band=row['question'][':question/difficulty'].rsplit('/',1)[-1]
            coverage[band][row['generation']['family']]+=1
            validate_delivery_batch([row],kp)
            if band=='easy':all_banks+=1
        assert g.batch('easy',8,20261024)==pool[:8]
        inv=json.loads((directory/'inventory/inventory.json').read_text())
        fingerprints={content_fingerprint(q)for q in inv['questions']+[inv['canonical_example']]}
        accepted,duplicates=prepare_records(pool,kp,g.EVIDENCE['kp']['id'],fingerprints,ROOT,directory/'package')
        assert len(accepted)==24 and duplicates==0
        for row in accepted:check(row)
        # The author-supplied metadata cannot conceal an oversized rendered
        # coefficient, incorrect derivative, or missing prerequisite support.
        negatives=[]
        oversized=copy.deepcopy(pool[0]);oversized['question'][':question/problem']=oversized['question'][':question/problem'].replace('Use the substitution','Use the substitution (24)')
        unsupported=copy.deepcopy(pool[8]);unsupported['question'][':question/problem']=unsupported['question'][':question/problem'].replace('You may use $','Recall $')
        for label,bad in [('rendered large numbers',oversized),('missing primitive support',unsupported)]:
            try:validate_delivery_batch([bad],kp)
            except ValueError:negatives.append(label+' rejected')
            else:raise AssertionError(label+' passed')
        broken=copy.deepcopy(pool[8]);sol=broken['question'][':question/worked-solution']
        broken['question'][':question/worked-solution']=re.sub(r'(\\frac\{\\mathrm\{d\}u\}\{\\mathrm\{d\}x\}=).*?(\.\n\$\$)',lambda m:m[1]+'987'+m[2],sol,count=1,flags=re.S)
        try:check(broken)
        except AssertionError:negatives.append('incorrect printed derivative rejected')
        else:raise AssertionError('Incorrect derivative passed')
        try:validate_delivery_batch([pool[0],copy.deepcopy(pool[0])],kp)
        except ValueError:negatives.append('amplitude/task clone rejected')
        else:raise AssertionError('Clone passed')
        for level,count in [('easy',0),('hard',101),('unknown',1)]:
            try:g.batch(level,count,0)
            except ValueError:continue
            raise AssertionError('Unsupported request passed')
        grader=[grading(row,str(kp)+' '+str(i))for i,row in enumerate(accepted)]
        save(directory/'candidate-pool.json',pool);save(directory/'accepted-pool.json',accepted)
        save(directory/'regression-samples.json',samples);save(directory/'grader-input.json',grader)
        # Retirement evidence binds every exact UUID/entity to the current
        # generated pool. Original/canonical entries are excluded and protected.
        old=json.loads((directory/'retirement-candidates.json').read_text())
        save(directory/'retirement-evidence.json',[{'entity':q[':db/id'],'uuid':q[':question/id'],
            'finding':'Superseded pre-scaffolding generated question; replaced under the reviewed task/difficulty contract',
            'record_before':q}for q in old])
        report={'passed':True,'pool_counts':dict(Counter(r['question'][':question/difficulty']for r in pool)),
                'printed_records_checked':len(pool)+len(samples),'delivered_records_rechecked':len(accepted),
                'coverage':{b:dict(v)for b,v in coverage.items()},'negative_controls':negatives,
                'old_generated_questions_to_retire':len(old),'maximum_problem_numeral':max(int(n)for r in pool for n in re.findall(r'\d+',r['question'][':question/problem'])),
                'response_policy':'Supplied-u transformation radio at easy; full exact calculation with supplied primitive at moderate/hard',
                'difficulty_claim':'Reviewed authored progression with one target-specific hard condition; no external psychometric calibration'}
        save(directory/'generator-verification.json',report);summary[str(kp)]=report
        render.extend([accepted[0],accepted[8],accepted[16]])
        if kp==17592186068915:
            render.append(next(r for r in accepted[16:]if r['generation']['model']['lower']is not None))
        if kp==17592186068917:
            render.append(next(r for r in accepted[16:]if r['generation']['family']=='sqrt_cos'))
        if kp==17592186068918:
            for case in ('rearranged_tan','rearranged_sec','nested_tan','def_sin2'):
                render.append(next(r for r in accepted[16:]if r['generation']['family']==case))
        print(kp,'printed mathematics and support checked; delivered',len(accepted),flush=True)
    # Match the same numerical instance across the two assessed task stages.
    g=load(17592186068915);m=g.model.trig_instance(g.KP,'easy','def_sin',random.Random(918))
    easy=g.model.render(g.KP,'easy','def_sin',m,918,g.EVIDENCE,random.Random(918))
    moderate=g.model.render(g.KP,'moderate','def_sin',m,918,g.EVIDENCE,random.Random(918))
    a,b=check(easy),check(moderate)
    assert equal(a['body'],b['body'])and a['lower']==b['lower']and a['upper']==b['upper']
    assert easy['question'][':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio'
    assert moderate['question'][':question/answer-fields'][0][':answer-field/type']==':answer-field.type/blank'
    save(H/'matched-scaffolding-pair.json',[easy,moderate])
    save(H/'matched-grader-input.json',[grading(easy,'same instance: transform'),grading(moderate,'same instance: evaluate')])
    save(H/'render-input.json',render);save(H/'generator-verification.json',{'knowledge_points':summary,'easy_banks_independently_checked':all_banks,
        'matched_task_pair':'Same integrand and bounds; supplied-u transformation vs full evaluation','database_writes':0})


if __name__=='__main__':main()
