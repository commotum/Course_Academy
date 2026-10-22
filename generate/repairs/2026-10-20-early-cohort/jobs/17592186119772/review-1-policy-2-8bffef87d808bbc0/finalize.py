#!/usr/bin/env python3
"""Complete the required review evidence without changing the target package."""
import audit as a
import copy, hashlib, itertools, json, re, subprocess, sys
from collections import Counter,defaultdict
E,J,W,R,OLD=a.E,a.J,a.W,a.R,a.OLD
sys.dont_write_bytecode=True

def main():
    # Execute the exact supplied acceptance assertions with only I/O/import paths
    # redirected into evidence. First establish that the old executable fails.
    author_results=[]
    for label,target in [('old',OLD/'relocated-package/17592186119772.py'),('current',W/'17592186119772.py')]:
        folder=E/('author-check-'+label);folder.mkdir(exist_ok=True)
        out=folder/'evidence';out.mkdir(exist_ok=True)
        minimal=json.loads((OLD/'minimal-failing-case.json').read_text())
        (out/'minimal-failing-case.json').write_text(json.dumps(minimal,indent=2)+'\n')
        visible=(W/'checks/visible_records.py').read_text()
        visible=visible.replace("W=Path(__file__).resolve().parents[1];E=W/'evidence';E.mkdir(exist_ok=True)",f"W=Path({str(W)!r});E=Path({str(out)!r});E.mkdir(exist_ok=True)")
        visible=visible.replace("W/'17592186119772.py'",f"Path({str(target)!r})")
        (folder/'visible_records.py').write_text(visible)
        (folder/'repair_regressions.py').write_text((W/'checks/repair_regressions.py').read_text())
        cmd=[str(a.PY),'-B',str(folder/'repair_regressions.py')]
        result=subprocess.run(cmd,cwd=E,capture_output=True,text=True)
        author_results.append({'target':label,'command':cmd,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'assertions_unchanged':True,'path_changes_only':['W points at protected workspace','E points at author-check-'+label+'/evidence','generator module target switches between retained old executable and current']})
        assert (result.returncode!=0) if label=='old' else (result.returncode==0)
    a.save('author-preflight-verification.json',{'results':author_results,'independent_validation':'Author assertions are supplemental. audit.py independently parses visible matrices with Fraction, tests retained negative cases on old/current code, source fidelity, fresh seeds, all eligible roles and actual grading/rendering.'})

    records=a.load('independent-records.json');coverage=[];probes=a.load('probe-definitions.json')
    by=defaultdict(list)
    for r in records:by[r['generation']['profile']].append(r)
    slots=[]
    for profile,rs in by.items():
        st=[a.inspect(r) for r in rs]
        entries=[v for r in rs for mat in a.visible(r['question']).values() for row in mat for v in row]
        bad_positions=defaultdict(set)
        for r in rs:
            t=a.target(r['question'])
            for mat in a.visible(r['question']).values():
                for i,row in enumerate(mat):
                    for j,v in enumerate(row):
                        if v and (i>j if t=='upper' else i<j):bad_positions[str((t,len(mat)))].add((i+1,j+1))
        counts=Counter(tuple(s['good']) for s in st)
        slots.append({'profile':profile,'n':len(rs),'targets':dict(Counter(s['target'] for s in st)),'qualifying_sets':{','.join(k):v for k,v in counts.items()},'dimensions':list(st[0]['dimensions']),'forbidden_witness_coordinates':{k:sorted(v) for k,v in bad_positions.items()},'negative_positive_zero_all_present':all(any((v<0 if sign==-1 else v>0 if sign==1 else v==0) for v in entries) for sign in [-1,0,1]),'observed_min':str(min(entries)),'observed_max':str(max(entries)),'semantic_banks':len({s['semantic'] for s in st})})
        if not rs[0]['question'][':question/difficulty'].endswith('/easy'):
            # All six permitted subsets are separately controlled, so sparse
            # natural subgroups are not used as evidence of universal behavior.
            for labels in itertools.chain(itertools.combinations('ABC',1),itertools.combinations('ABC',2)):
                probes.append({'cue':'Fixed qualifying subset','subgroup':profile+' ordinary moderate draws','scope':'within_template','strategy':'Always select '+','.join(labels),'correct':counts[labels],'total':len(st),'baseline':1/6,'disposition':'not_predictive','conclusion':'Comparison baseline 1/6 is uniform among the six nonempty proper subsets of A-C, rather than among source-specific radio choices. Natural draws have multiple qualifying sets; independent controlled assignments exercise all six and grade every offered response. Four natural draws do not establish a population frequency.','sample_refs':['slot-coverage.json','independent-records.json','controlled-role-records.json','grader-report-final.json']})
    a.save('slot-coverage.json',slots)
    assert all(len(x['targets'])==2 for x in slots)
    assert all(len(x['qualifying_sets'])>1 for x in slots)
    cf=a.load('counterfactual-records.json');render=a.load('render/rendering.json')
    assert render['passed'] and len(render['cases'])==13
    # These files were visually inspected through view_image in this session.
    images=[1,2,3,4,5,7,9,10,11,12,13]
    a.save('visual-inspection.json',{'renderer':'Unmodified application Learning.html/learning.js via render_preview.py','screenshots_inspected':[f'render/question-{n:03d}.png' for n in images],'counterfactuals':'001 upper A; 002 same matrices lower B; 003 irrelevant diagonal/allowed-side edits retain upper A; 004 retained A/E swap now accepts A. Prompt targets, visible entries, selected radio answers, and explanations agree.','restored_families':'010 decimal 4x4/3x3 checkbox bank and nonzero witness; 011 subset radio with three matrices and complete five-choice bank; 012/013 restored easy families.','result':'Readable square brackets, correct rows/columns, signed/decimal values, complete radio and checkbox controls, and worked solutions. No clipping, raw TeX, missing labels or malformed notation seen in representative desktop screenshots.','limits':['Representative desktop screenshots; not every viewport tested.','Renderer selects correct choices for preview, independently checked against native learner grading.']})
    reports=['counterfactual-records.json','counterfactual-results.json','grader-input-final.json','grader-report-final.json','render-input.json','render/rendering.json','visual-inspection.json']
    counterfactuals=[
        {'kind':'relevant','change':'Change only target upper to lower on an unchanged bank: A=[[1,3],[0,2]], B=[[1,0],[4,2]], C,D,E have nonzeros on both sides. seed=93071, q-126354.','expected':'A is the sole upper answer; B is the sole lower answer. Target text, selected response and above/below explanation must all change.','observed':'Both records accepted; independent visible-matrix predicate gives A then B. Native grader accepts the respective IDs and rejects the other four; UI screenshots 001/002 show the changed target, selected matrix and solution.','status':'passed','justification':'Lesson Introduction defines opposite zero sides; source labels cannot fix qualification. No transposition or new learner operation is introduced.','sample_refs':reports},
        {'kind':'relevant','change':'Retained exact minimal A/E role swap, q-126354 seed=20261022, with fixed 2x2 dimensions, values and exactly-one constraint.','expected':'A becomes sole correct label, solution and grader follow membership.','observed':'Old executable raises complete profile support counts must be preserved. Revised executable generates A; concrete solution says Notice that A; native grader accepts A only and screenshot 004 displays it.','status':'passed','justification':'Equally sized candidates can exchange qualifying roles without changing the zero-side test or response workload.','sample_refs':['retained-minimal-case.json','retained-finding-regressions.json',*reports]},
        {'kind':'irrelevant','change':'At fixed upper target, set all diagonal entries to -11 and 0 and all allowed upper entries to -7, leaving forbidden lower evidence unchanged.','expected':'A remains the sole answer; changed entries must be visible, explanation retains below-diagonal condition, native grader preserves membership.','observed':'Independent predicate gives A before/after; all five native choices follow that truth set. Screenshot 003 shows changed diagonal/upper entries and the same upper A answer and zero-side explanation.','status':'passed','justification':'Introduction explicitly allows any number, including zero, on the diagonal and unconstrained side.','sample_refs':reports}
    ]
    # A direct skill simplification is not an incidental predictor.
    batch=a.load('delivery-batch/accepted.json');d_hits=0;d_total=0
    for r in batch:
        mats=a.visible(r['question']);diags=[l for l,mat in mats.items() if all(not v for i,row in enumerate(mat) for j,v in enumerate(row) if i!=j)]
        if len(diags)==1:d_total+=1;d_hits+=a.inspect(r)['good']==tuple(diags)
    if d_total:
        probes.append({'cue':'Only diagonal matrix','subgroup':'Delivered batch records containing exactly one diagonal candidate','scope':'other_recognizable_subgroup','strategy':'Select the diagonal candidate','correct':d_hits,'total':d_total,'baseline':.2,'disposition':'intended_skill','conclusion':'Uniform choice baseline is 0.2. A diagonal matrix has all zeros on BOTH forbidden sides, directly applying the lesson definition, and is therefore a valid simplification. This observation is not evidence of a label/layout bypass.','sample_refs':['delivery-batch/accepted.json','math-results.json']})
    a.save('pedagogical-variation.json',{
        'learner_operation':'Read upper/lower target; inspect every candidate entry strictly below/above the main diagonal; select exactly those square matrices with all inspected entries zero.',
        'fixed_features':[{'feature':'Square matrices and zero-side definition','justification':'Tutorial 658a47dc-4d32-5d9d-a04c-82d683e87739 Introduction defines these conditions. Diagonal values are arbitrary.'},{'feature':'Five easy matrix-radio choices, exactly one correct','justification':'All eight original easy sources ask for a single matrix from a complete five-option bank. This preserves response and inspection workload.'},{'feature':'Source-profile labeled dimensions at normal easy/moderate generation','justification':'Fixed dimensions preserve observed per-question inspection workload. They do not fix qualification: every eligible role is independently assigned at these same dimensions and all profiles have counterexamples to a constant-label rule.'},{'feature':'One or two qualifying matrices in moderate three-matrix families','justification':'Source checkbox and text-subset banks assess nonempty proper subsets with one/two qualifiers; this maintains that response scope. All six eligible assignments are tested.'}],
        'answer_roles':[{'role':'Qualifying candidate label / subset','eligible_variation':'Every A-E label in easy; every one/two-element A-C subset in moderate, at unchanged dimensions.','observed':'40 easy and 30 moderate controlled assignments all accepted and independently checked, including native grading. Ordinary samples vary qualifying sets in all 13 source profiles.'},{'role':'Target orientation','eligible_variation':'Upper/lower can vary; prompt, condition, matrices and explanation must agree.','observed':'Both orientations in all 13 ordinary source profiles; controlled unchanged-matrix target switch changes A to B in actual grading and rendering.'},{'role':'Forbidden-side nonzero positions and allowed-side zero patterns','eligible_variation':'Qualifiers require zero forbidden entries; foils may have a nonzero at any forbidden coordinate. Allowed entries including zero are independent of qualification.','observed':'Sampling inspected and measured by profile/dimension in slot-coverage.json; controlled irrelevant allowed-side/diagonal edits preserve membership.'},{'role':'Displayed choice position','eligible_variation':'Correct response may appear at any position independent of label.','observed':'All five positions occur once in the exact batch; control position counts are 13,15,15,21,16. Actual UI may independently reorder choices using stable IDs, so screenshot and field-order cues are reported separately.'}],
        'coverage':[{'case':'All current source families and complete banks','sample_refs':['source-replay.json','source-replay-records.json','retained-finding-regressions.json'],'result':'13/13 original cases and 69 choices replay with exact raw problem, worked solution, field types, correct values and full banks. Canonical e-4395 lacks a captured bank and is separately classified B only.'},{'case':'Every eligible qualifying role at each fixed source profile','sample_refs':['controlled-role-records.json','controlled-role-results.json','grader-report-final.json'],'result':'70 controlled valid assignments: 8 easy profiles x 5 labels and 5 moderate profiles x 6 subsets; independent math and actual learner grading agree.'},{'case':'Fresh ordinary distribution and response workload','sample_refs':['independent-records.json','sample-index.json','slot-coverage.json','scope-results.json'],'result':'100 fresh seed/profile calls: 80 easy, 20 moderate. Both target orientations, multiple qualifying sets, signed/zero values and source-sized matrices appear in every profile.'},{'case':'Exact runner batch','sample_refs':['batch-records.json','delivery-batch/accepted.json','stage-summary.json','shortcut-results.json'],'result':'All five survive; labels B,A,B,D,A and field-order positions 5,3,2,4,1. Four distinct unlabeled off-diagonal support banks; repetition includes more than numeric/sign changes. Neither batch profile has a fixed label answer.'}],
        'counterfactuals':counterfactuals,
        'shortcut_probes':probes,
        'delivery':{'stages_examined':['Qualifying-role/orientation sampling before compatible support and values','Whole-instance validation and bounded retry; independent invalid/boundary tests','Nonempty-checkbox policy and easy-radio applicability','Actual publisher normalization, question validation and stable identities','Captured basis5453 inventory and within-batch deduplication','Requested easy filtering','Difficulty-first selection rules, uniform within-band draw, history exclusion and exhausted pool'], 'sample_refs':['runtime-results.json','delivery-control/delivery.json','delivery-batch/delivery.json','stage-summary.json','shortcut-results.json','selection-results.json','affected-inventory.json','generated-records.json','inventory-audit.json'],'result':'80/80 easy controls and 5/5 batch records survive with identical decision distributions. Prior dimension lookup now succeeds 10/60 applicable controls and 0/5 batch records. Current fixed-label/position/dimension/profile/orientation/diagonal probes have counterexamples. Read-only selection reproduction exercises requested easy with positive weight, unconfigured-first and excluded-history branches; no new answer-binding rule appears. Three historically affected generated moderate records remain separately documented.'},
        'limitations':['Finite samples and listed cue probes do not prove absence of every possible shortcut. Post-hoc most-common answers are reported descriptively, not as evidence of a deterministic population rule.','Live policy weights, learner histories and concurrent publication state are unavailable. Selection conclusions are conditional on stated branches and captured basis5453; exact future question ordering is not claimed.','Historical inventory reproduction retains original captured question IDs with explicitly reconstructed generation parameters and null original seed. These are not outputs of the revised package.','Requested easy and all observed source contracts were reviewed. Unchanged authored hard extension has no original hard sources and is outside this certification.','Canonical example e-4395 has no captured answer fields; exact canonical answer-bank replay cannot be asserted.']})

    # Verify report schema and every referenced file before returning a verdict.
    schema=json.loads((R/'generate/pipeline/pedagogical-variation.schema.json').read_text());v=a.load('pedagogical-variation.json')
    try:
        import jsonschema
        jsonschema.validate(v,schema);schema_check='jsonschema.validate passed'
    except ImportError:
        def validate(x,s):
            typ=s.get('type')
            if typ=='object':
                assert isinstance(x,dict);assert all(k in x for k in s.get('required',[]))
                if s.get('additionalProperties') is False:assert set(x)<=set(s['properties'])
                for k,z in x.items():validate(z,s['properties'][k])
            elif typ=='array':
                assert isinstance(x,list) and len(x)>=s.get('minItems',0)
                for z in x:validate(z,s['items'])
            elif typ=='string':assert isinstance(x,str) and len(x)>=s.get('minLength',0)
            elif typ=='integer':assert type(x)==int
            elif typ=='number':assert type(x) in (int,float)
            if 'enum' in s:assert x in s['enum']
            if typ in ('integer','number'):assert x>=s.get('minimum',float('-inf')) and x<=s.get('maximum',float('inf'))
        validate(v,schema);schema_check='Full supplied schema subset recursively checked: types, required/additional fields, enums, min lengths/items, numeric bounds.'
    def refs(obj):
        if isinstance(obj,dict):
            for k,x in obj.items():
                if k=='sample_refs':yield from x
                else:yield from refs(x)
        elif isinstance(obj,list):
            for x in obj:yield from refs(x)
    for p in refs(v):assert not a.Path(p).is_absolute() and (E/p).is_file() and (E/p).stat().st_size>0,p
    a.save('package-after.json',a.hashes());assert a.hashes()==a.load('package-before.json')
    a.save('evidence-validation.json',{'pedagogical_schema':schema_check,'all_sample_refs_relative_and_nonempty':True,'package_unchanged':True,'no_database_or_publication_actions':True,'author_assertions_verified_fail_old_pass_current':True})
    (E/'session-state.md').write_text('Completed required review: original source verified; all retained findings independently fail old and pass current; supplied author assertions also fail old and pass current using path-only evidence copies. Source replay, exact math, eligible roles, delivery, native grading, actual UI screenshots, portability/dependencies and inventory evidence complete. 13 source cases/69 choices; 100 fresh samples; 70 controlled roles; 5/5 exact batch survive. 3 historical affected inventory entries retained separately. Pedagogical schema and evidence references verified; package hashes unchanged. Verdict ready: accepted for revised generator and requested easy batch, with snapshot/finite-audit limits recorded.\n')
    print(json.dumps({'schema':schema_check,'package_unchanged':True,'author_negative_positive':[x['exit_code'] for x in author_results],'probes':len(probes),'inventory_affected':len(a.load('affected-inventory.json')['affected_questions'])}))
if __name__=='__main__':main()
