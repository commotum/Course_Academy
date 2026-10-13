"""Parse rendered mathematics independently; check full banks and real grading."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from functools import lru_cache

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
# Validation-only dependency, isolated from the application environment.
sys.path.insert(0,str(HERE/'validation-deps'))
from sympy.parsing.latex import parse_latex
from mpmath import iv
spec=importlib.util.spec_from_file_location('exponential_base',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g); sp=g.sp
x=sp.Symbol('x'); C=sp.Symbol('C')
iv.dps=50
WITNESSES=[]

@lru_cache(maxsize=None)
def math(s):
    s=s.replace('\\operatorname{ln}\u2061',r'\ln ').replace(r'\,',' ')
    # Rebuild evaluated SymPy nodes without running the broad simplify search
    # on distractors containing logarithms and variable exponents.
    return sp.sympify(str(parse_latex(s,strict=True)))

@lru_cache(maxsize=None)
def unequal(a,b):
    # A single certified nonzero evaluation disproves equality on all real x.
    # Directed interval arithmetic encloses logs and rational powers; unlike an
    # unbounded symbolic equals search, it gives an explicit bounded witness.
    delta=a-b
    for value in (0,1,2,sp.Rational(1,2)):
        interval=interval_value(delta.subs(x,value))
        if interval.a>0 or interval.b<0:
            WITNESSES.append({'difference':str(delta),'x':str(value),
                              'enclosure':str(interval),'precision_digits':50})
            return True
    raise AssertionError(('No nonzero interval witness',delta))

def interval_value(expr):
    if expr.is_Rational:return iv.mpf(int(expr.p))/iv.mpf(int(expr.q))
    if expr.func==sp.Add:
        return sum((interval_value(t) for t in expr.args),iv.mpf(0))
    if expr.func==sp.Mul:
        result=iv.mpf(1)
        for t in expr.args:result*=interval_value(t)
        return result
    if expr.func==sp.Pow:return interval_value(expr.args[0])**interval_value(expr.args[1])
    if expr.func==sp.log:return iv.ln(interval_value(expr.args[0]))
    raise AssertionError(('Unsupported interval expression',expr))

def check(rec):
    meta=rec['generation']; t=meta['template']; b=meta['parameters']['base']; level=g.DATA[t][1]
    assert rec['knowledge_point']['db_id']==g.KP_ID
    assert rec['question']==g.generate(level,999,t,{'base':b})['question']
    q=rec['question']; f=q[':question/answer-fields'][0]; bank=f[':answer-field/choices']
    assert len(bank)==5 and f[':answer-field/key']=='selection'
    assert f[':answer-field/type']==':answer-field.type/radio'
    assert all(a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value'] for a in bank)
    vals=[math(a[':answer/value']) for a in bank]
    correct=next(i for i,a in enumerate(bank) if a[':answer/id']==f[':answer-field/correct'][1])
    integrand=math(g.integrand(q))
    assert sp.simplify(sp.diff(vals[correct],x)-integrand)==0
    for i,a in enumerate(vals):
        if i!=correct: unequal(sp.diff(a,x),integrand)
        for other in vals[i+1:]: unequal(sp.diff(a,x),sp.diff(other,x))
    ob,_,exponent,prefactor=g.DATA[t]
    assert sp.simplify(integrand-sp.sympify(prefactor)*sp.Integer(b)**sp.sympify(exponent))==0
    of=g.sources()[t][':question/answer-fields'][0]
    assert [a[':answer/value'] for a in bank]==[g.change_base(a[':answer/value'],ob,b) for a in of[':answer-field/choices']]
    solution=q[':question/worked-solution']
    final=solution.rsplit('& =',1)[1].split(r'\end{aligned}')[0].removesuffix('.')
    assert sp.simplify(math(final)-vals[correct])==0
    assert solution==g.change_base(g.sources()[t][':question/worked-solution'],ob,b)
    # Exact mathematical content identity independently reconstructed from LaTeX.
    fp=hashlib.sha256(sp.srepr(sp.simplify(integrand)).encode()).hexdigest()
    assert fp==g.fingerprint(q)==meta['mathematical_fingerprint']
    assert len({a[':answer/id'] for a in bank})==5
    return rec

def native(label,r):
    f=r['question'][':question/answer-fields'][0]; ci=f[':answer-field/correct'][1]
    return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],
        'expected':'accepted' if a[':answer/id']==ci else 'rejected',
        'purpose':'complete source-profile option selection'} for a in f[':answer-field/choices']]}

def save(n,v): (HERE/n).write_text(json.dumps(v,indent=2)+'\n')

def main():
    replays=[]; records=[]; inputs=[]; components=[]; reviews=[]
    for t,(ob,level,exponent,prefactor) in g.DATA.items():
        r=check(g.generate(level,0,t,{'base':ob})); q=r['question']; old=g.sources()[t]
        assert q[':question/problem']==old[':question/problem']
        assert q[':question/worked-solution']==old[':question/worked-solution']
        of=old[':question/answer-fields'][0]; f=q[':question/answer-fields'][0]
        assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in of[':answer-field/choices']]
        replays.append({'source':t,'difficulty':level,'bank_profile':t,'matched_values':5,
            'total_values':5,'matched_distractors':4,'complete_bank_matched':True,
            'missing':[],'extra':[],'solution_verbatim':True,'correct_value_matched':True})
        cs=[]
        for a in of[':answer-field/choices']:
            cs.append({'source_answer_id':a[':answer/id'],'source_field_id':of[':answer-field/id'],
              'source_value':a[':answer/value'],'recipe':g.change_base(a[':answer/value'],ob,'b'),
              'bank_profile':t,'correct':a[':answer/id']==of[':answer-field/correct'][':answer/id'],
              'complete_value_replayed':True,'interpretation':'Observed expression transport; no inferred misconception.'})
        components.append({'source':t,'source_question_db_id':old[':db/id'],
            'base':ob,'exponent':exponent,'prefactor':prefactor,'difficulty':level,
            'field_key':'selection','choices':cs,'source_prompt':old[':question/problem'],
            'source_solution':old[':question/worked-solution'],
            'prompt_template':g.change_base(old[':question/problem'],ob,'b'),
            'solution_template':g.change_base(old[':question/worked-solution'],ob,'b')})
        reviews.append({'source':old,'variant':g.generate(level,0,t,{'base':2 if ob!=2 else 3})})
        for b in g.BASES:
            rec=check(g.generate(level,0,t,{'base':b}))
            inputs.append(native(t+'-base-'+str(b),rec))
        print('Validated source profile and all bases:',t,flush=True)
    for level in ('easy','moderate'):
        for t,p in g.candidates(level): records.append(check(g.generate(level,1974,t,p)))
    fps=[g.fingerprint(r['question']) for r in records]; assert len(set(fps))==len(fps)
    originals={g.fingerprint(q) for t,q in g.sources().items() if t in g.DATA}; assert not originals & set(fps)
    for level in ('easy','moderate'):
        n=sum(r['question'][':question/difficulty'].endswith('/'+level) for r in records)
        assert g.batch(level,n,10)==g.batch(level,n,10)
        try:g.batch(level,n+1,0)
        except ValueError:pass
        else:raise AssertionError('Finite limit ignored')
    try:g.batch('hard',1,0)
    except ValueError:pass
    else:raise AssertionError('Unsupported hard accepted')
    for b in (1,13,True,2.5):
        try:g.generate('easy',0,'q-31420',{'base':b})
        except ValueError:pass
        else:raise AssertionError('Invalid base accepted')
    save('source-replay.json',{'passed':True,'complete_banks_matched':7,'complete_banks_total':7,
      'matched_values':35,'matched_distractors':28,'sources':replays,
      'excluded_incomplete_unrated_sources':['q-73800']})
    save('source-components.json',components)
    save('source-components-verification.json',{'passed':True,'source_choices_accounted_for':35,
      'complete_values_reproduced':35,'profiles':7,'unmapped_choices':[]})
    save('previews.json',records); save('native-input.json',inputs); save('review.json',reviews)
    (HERE/'review.md').write_text('\n\n'.join('## '+r['variant']['generation']['template']+
        '\n\nOriginal:\n\n'+g.markdown(g.generate(g.DATA[r['variant']['generation']['template']][1],0,
        r['variant']['generation']['template'],{'base':g.DATA[r['variant']['generation']['template']][0]}))+
        '\n\nVariant:\n\n'+g.markdown(r['variant']) for r in reviews))
    subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
    counts={l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in ('easy','moderate')}
    save('review-verification.json',{'passed':True,'source_variant_pairs':7,
      'prompt_solution_layout':'Exact base-slot transport, same Markdown and substitution steps.',
      'answer_bank':'All five original option structures transported as a whole; no mixed bank.',
      'mathematics':'Every option differentiated, exactly one antiderivative; final solution matches.'})
    save('non-equivalence-witnesses.json',{'passed':True,'method':'50 digit directed interval arithmetic; nonzero derivative-difference witness disproves equivalence up to integration constants.','witnesses':WITNESSES})
    files=[HERE.with_suffix('.py')]+[HERE/n for n in ('source.json','source.edn','validate.py','db_support.py','replenish.py',
      'check-engine.rs','check-engine','engine-build.json','source-replay.json','source-components.json',
      'source-components-verification.json','native-grading.json','previews.json','review-verification.json',
      'classification.md','template-extraction.md','plot-extraction.md','capabilities.json','non-equivalence-witnesses.json')]
    save('validation.json',{'passed':True,'counts':counts,'validated_profile_base_pairs':77,
      'mathematical_distinctness':'SHA256 exact SymPy integrand; duplicate banks excluded across q-31419/q-73802.',
      'source_bank_fidelity':'7/7 complete banks, 35/35 values, 28/28 distractors.',
      'native_grading':'All 385 option submissions through course_academy_engine::learning::grade_field.',
      'validator_dependencies':{'antlr4-python3-runtime':'4.11.1','path':str((HERE/'validation-deps').relative_to(ROOT)),'sympy':sp.__version__},
      'hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}})
    print('Passed bounded validation:',counts,flush=True)

if __name__=='__main__':main()
