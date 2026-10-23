from audit_helpers import *
from shortcut_probe import probe

OLD=ROOT.parent/'review-0-policy-2-707c0c642d91a260'
samples=json.load(open(ROOT/'independent-samples.json'))
batch=json.load(open(ROOT/'batch-records.json'))
cf=json.load(open(ROOT/'counterfactual-records.json'))
accepted=json.load(open(ROOT/'delivery-batch/accepted.json'))
independent=json.load(open(ROOT/'delivery-independent/accepted.json'))

def coverage(records):
    out={}
    for r in records:
        name=r['generation']['template']; p=r['generation']['parameters']; a=expected(r)
        d=out.setdefault(name,{'count':0,'parameters':[],'answers':[],'ranks':[],'positions':[],'attempts':[]})
        d['count']+=1;d['parameters'].append(p);d['answers'].append(str(a));d['ranks'].append(r['generation']['bank_assignment']);d['attempts'].append(r['generation']['attempts'])
        if field(r)[':answer-field/type'].endswith('/radio'):
            d['positions'].append(next(i for i,c in enumerate(field(r)[':answer-field/choices']) if c[':answer/value']==correct(r)))
    return out

save('coverage-results.json',{'seeds':'842700+19*template_index+role; radio role 0..4; blank role 0', 'raw':coverage(samples),'batch':coverage(batch),'delivered_batch':coverage(accepted),'delivered_independent_easy':coverage(independent),'sampling_review':'Template and rank chosen before retrying bank construction, so rejecting banks does not preferentially replace these roles. Explicit parameter calls reject invalid inputs; sampled draws have bounded retries. Degree, perfect-square evaluation and sign pools are unchanged.'})

probes=[];details=[]
def examine(records,label,ref):
    for name in sorted({r['generation']['template'] for r in records}):
        rs=[r for r in records if r['generation']['template']==name]
        if not field(rs[0])[':answer-field/type'].endswith('/radio'):
            continue
        scores=collections.Counter(); n=len(rs)
        for r in rs:
            f=field(r); vals=[latex(a[':answer/value']) for a in f[':answer-field/choices']]
            key=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/value']==correct(r))
            # A positive-domain witness is used only to order symbolic choices.
            numeric=vals
            if any(v.has(X) for v in vals):
                for t in range(-100,101):
                    vs=[s.simplify(v.subs(X,t)) for v in vals]
                    if all(v.is_real and v.is_finite for v in vs):numeric=vs;break
                else:raise AssertionError('No real domain witness')
            lengths=[len(a[':answer/value']) for a in f[':answer-field/choices']]
            order=sorted(range(5),key=lambda i:float(numeric[i]))
            tests={'first option':key==0,'least numeric value':key==order[0],'greatest numeric value':key==order[-1],
                   'uniquely shortest TeX':lengths.count(min(lengths))==1 and lengths[key]==min(lengths),
                   'unique sign':sum(s.sign(v)==s.sign(numeric[key]) for v in numeric)==1}
            if all(v.is_Rational for v in vals):
                ds=[v.q for v in vals]
                tests['unique least denominator']=ds.count(min(ds))==1 and ds[key]==min(ds)
                tests['unique greatest denominator']=ds.count(max(ds))==1 and ds[key]==max(ds)
            p=probe(r)
            if p is not None:tests['coefficient times common spacing']=p['success']
            for cue,success in tests.items():scores[cue]+=int(success)
            details.append({'set':label,'template':name,'question_id':r['question'][':question/id'],'tests':tests})
        for cue,correct_n in scores.items():
            probes.append({'cue':cue,'subgroup':label+': '+name,'scope':'within_template','strategy':cue+' (abstain if uniqueness/common spacing fails)','correct':correct_n,'total':n,'baseline':0.2,'disposition':'not_predictive','conclusion':'One of five choices gives a 0.2 blind-choice baseline. Counts include abstentions as failures. Finite incidental hits are not evidence of a stable family rule; inspect alongside bank construction and rank coverage.','sample_refs':[ref,'shortcut-results.json']})
    return

examine(samples,'fresh independent','independent-samples.json')
examine(batch,'exact runner batch','batch-records.json')
examine(accepted,'delivered runner batch','delivery-batch/accepted.json')
examine(independent,'delivered independent easy','delivery-independent/accepted.json')
save('shortcut-results.json',{'commands':['python -B review_checks.py','python -B shortcut_probe.py prior-failing-batch.json'],'records_checked':details,'probes':probes})

# The retained regression must fail its historical witness, not just pass new banks.
sys.path.insert(0,str(ROOT/'author-check'))
import importlib.util
spec=importlib.util.spec_from_file_location('retained_regression',ROOT/'author-check/regression.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
failed=False
try:mod.check(json.load(open(ROOT/'prior-failing-batch.json')))
except AssertionError:failed=True
assert failed
current=mod.check(batch)
save('regression-verification.json',{'retained_finding_id':'a68a8999b8ec7f376999','preflight':json.load(open(ROOT.parent/'repair-preflight.json')),'old_example_assertion_failed':failed,'current_batch':current,'author_script_result':json.load(open(ROOT/'author-regression/spacing-regression.json')),'adaptation':'Copied check and helper scripts under evidence_root. Only package/output locations changed; package never executed with writable package output. Original regression inputs, assertions and sample seeds retained.'})

inv=json.load(open(ROOT.parent/'source/inventory.json'));src=json.load(open(ROOT/'source-extract.json'))
original={q[':question/id'] for q in src['kp'][':knowledge-point/questions']}
affected=json.load(open(OLD/'affected-inventory.json'))['affected_questions'];ids={q['question_id'] for q in affected}
rows=[q for q in inv['questions'] if q[':question/id'] not in original]
assert all(q.get(':question/retired') for q in rows if q[':question/id'] in ids)
assert len([q for q in rows if q[':question/id'] in ids])==3
eligible_radio=[q for q in rows if not q.get(':question/retired') and any(f[':answer-field/type'][':db/ident'].endswith('/radio') for f in q[':question/answer-fields'])]
assert not eligible_radio
save('inventory-results.json',{'basis':inv['basis'],'generated_records':rows,'prior_finding_id':'ab222f0376dcbf24176c','known_affected_ids':sorted(ids),'all_three_retired':True,'eligible_generated_radios':0,'status':'Verified no currently eligible generated radio has the demonstrated spacing defect. Two eligible generated blanks do not have option banks. Original source questions excluded from generated inventory findings. Other possible historical defects not exhaustively reaudited.','eligibility_code':'engine/rust/learning.rs:149-154 rejects retired questions before fresh practice; callers filter via validate_practice_question.'})
save('affected-inventory.json',{'affected_questions':[]})

selection=[];ordered=sorted(accepted,key=lambda r:r['question'][':question/id'])
for n in range(200):
    seed=f'independent-revision-{n}';d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/2**53;r=ordered[int(u*len(ordered))]
    selection.append({'seed':seed,'id':r['question'][':question/id'],'template':r['generation']['template'],'spacing_success':bool((p:=probe(r)) and p['success'])})
save('selection-results.json',{'basis':inv['basis'],'code_refs':['engine/rust/question_selection.rs:select','engine/rust/question_selection.rs:seen_before_task','engine/rust/learning.rs:validate_practice_question'],'records':selection,'counts':dict(collections.Counter(r['template'] for r in selection)),'spacing_successes':sum(r['spacing_success'] for r in selection),'scenario':'Read-only conditional scenario: fresh accepted easy candidates, positive easy band weight. SHA256 bytes 8..16 choose uniformly within sorted candidates. UUID order substitutes for unknown future database entity IDs.','limits':['Actual learner history, policy weights, task seed and future entity IDs unavailable. No exact future sequence claimed. Zero-weight band excludes all easy items; previous exposure can remove individual records.','Unconfigured policy chooses first eligible entity. This preserves an individual item rather than introducing an option-spacing filter. Retirement excludes the three historical radios.'],'publication_preparation_exists':(ROOT.parent/'publication/preparation.json').exists()})

before=json.load(open(OLD/'package-before.json'));now=json.load(open(ROOT/'package-before.json'));manifest=json.load(open(PKG/'package.json'))
unchanged={f:before.get(f)==now.get(f) for f in manifest['files']}
oldscope=json.load(open(OLD/'scope-results.json'))
save('scope-results.json',{'unchanged_manifest_files':unchanged,'reused_scope_evidence':oldscope,'fresh_scope':'Only radio bank construction and version/profile labels changed. Rational scalar distractors retain the existing function, task, five-choice contract and complete worked solution. Source banks remain available in replays. No new differentiation operator or workload stage.','prior_evidence_source':str(OLD/'scope-results.json')})
save('counterfactual-results.json',{'records':'counterfactual-records.json','quadratic_targets':{'targets':[1,5,9],'expected':['4/3','0','-4/3'],'observed':[correct(r) for r in cf[:3]],'verified':all(expected(r)==a for r,a in zip(cf[:3],[s.Rational(4,3),0,-s.Rational(4,3)]))},'irrelevant_seed_pair':{'same_prompt':cf[3]['question'][':question/problem']==cf[4]['question'][':question/problem'],'same_solution':cf[3]['question'][':question/worked-solution']==cf[4]['question'][':question/worked-solution'],'answers':[correct(r) for r in cf[3:5]],'options_changed':field(cf[3])[':answer-field/choices']!=field(cf[4])[':answer-field/choices']},'changed_radio_target':{'targets':[-4,-3],'expected':['7/6','7/8'],'observed':[correct(r) for r in cf[5:7]],'verified':all(expected(r)==a for r,a in zip(cf[5:7],[s.Rational(7,6),s.Rational(7,8)]))},'prompt_and_solution_targets_follow':all(f"x={r['generation']['parameters']['t']}" in r['question'][':question/problem'] and f"x={r['generation']['parameters']['t']}" in r['question'][':question/worked-solution'] for r in cf),'native_grader':'grader-results.json','actual_ui':'render/rendering.json'})
print(json.dumps({'fresh_samples':len(samples),'shortcut_probe_groups':len(probes),'inventory_generated':len(rows),'retired_known_defects':3,'batch_survivors':len(accepted),'independent_easy_survivors':len(independent),'universal_cues':[{k:v for k,v in p.items() if k in ['cue','subgroup','correct','total']} for p in probes if p['total']>1 and p['correct']==p['total']]}))
