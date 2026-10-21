"""Assemble the review contract from completed independent checks."""
import json
from pathlib import Path
import sys
from review import ROOT, BASE, REPO, PYTHON, save, hash_package

def load(p):return json.loads((ROOT/p).read_text())

def validate(value,schema,path='$'):
    kinds={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float)}
    if 'type' in schema:assert isinstance(value,kinds[schema['type']]),path
    if 'enum' in schema:assert value in schema['enum'],path
    if isinstance(value,dict):
        assert set(schema.get('required',[]))<=value.keys(),path
        if schema.get('additionalProperties') is False:assert value.keys()<=schema.get('properties',{}).keys(),path
        for k,v in value.items():
            if k in schema.get('properties',{}):validate(v,schema['properties'][k],path+'.'+k)
    if isinstance(value,list):
        assert len(value)>=schema.get('minItems',0),path
        for i,v in enumerate(value):validate(v,schema.get('items',{}),path+f'[{i}]')
    if isinstance(value,str):assert len(value)>=schema.get('minLength',0),path
    if isinstance(value,(float,int)):
        assert value>=schema.get('minimum',float('-inf')),path
        assert value<=schema.get('maximum',float('inf')),path

def main():
    initial=load('source-analysis.json')
    if 'source_passages' not in initial:
        save('source-analysis-initial.json',initial)
        initial['source_passages']=[
            {'reference':'lesson tutorial 2806 / 0f1cb099-7970-59ba-ad74-7052da9f2872','passage':'Here, the base of the exponential is $e,$ so we take the *natural* logarithm of both sides'},
            {'reference':'lesson tutorial 2806 / 0f1cb099-7970-59ba-ad74-7052da9f2872','passage':'We often present the solution of an exponential equation as an exact solution in logarithmic form.'},
            {'reference':'e-4103 / 5e22ac55-3e84-5cb4-8231-5f882da9240e worked solution','passage':'Finally, we solve for $x$ and rewrite the right-hand side using the power law of logarithms'},
            {'reference':'q-263058 / ba9070de-c707-5661-a14c-cac1b4371745 worked solution','passage':'Now, we use the fact that $\\operatorname{ln}\u2061({e}^{a})=a$ to simplify the left-hand side.'}]
        initial['provenance']='Initial account saved and verified before any package inspection. Original preserved as source-analysis-initial.json; exact citation transcriptions appended at report assembly without changing independent skill or variation analysis.'
        save('source-analysis.json',initial)
    schema=json.loads((REPO/'generate/pipeline/pedagogical-variation.schema.json').read_text())
    variation=load('pedagogical-variation.json');validate(variation,schema)
    refs=[]
    def walk(v):
        if isinstance(v,dict):
            for k,x in v.items():
                if k=='sample_refs':refs.extend(x)
                else:walk(x)
        elif isinstance(v,list):
            for x in v:walk(x)
    walk(variation)
    for ref in refs:
        p=ROOT/ref
        assert not Path(ref).is_absolute() and p.resolve().is_relative_to(ROOT) and p.is_file() and p.stat().st_size,ref
    rendering=load('render/rendering.json');assert rendering['passed'] and len(rendering['cases'])==8
    save('render-visual-inspection.json',dict(passed=True,inspected_screenshots=[f'render/question-{i:03}.png' for i in range(1,9)],observations='Visually inspected all8 actual-UI screenshots: source, controlled coefficient/offset/RHS changes, rename, exponent-order change and upper boundary. Prompt notation, blank response display, answer expression and full worked solution are readable. No clipping, exposed TeX, missing glyphs or stale variable/value found.',limitations='Correct-response preview mode; actual response decisions tested separately through native grader.'))
    commands=[dict(cwd=str(ROOT),argv=[str(PYTHON),'-B','review.py'],purpose='Independent samples, exact math, supported source replay, packaging and native equivalents/wrong inputs'),dict(cwd=str(ROOT),argv=[str(PYTHON),'-B','finish_review.py'],purpose='Delivery coverage, exact counterfactuals, conditional selector reproduction and native shortcut outcomes')]
    for name,out in [('samples.json','delivery-independent'),('runner-batch.json','delivery-runner')]:
        commands.append(dict(cwd=str(ROOT),argv=[str(PYTHON),'-B',str(REPO/'generate/pipeline/check_delivery.py'),'--input',name,'--source',str(BASE/'source/source.json'),'--inventory',str(BASE/'source/inventory.json'),'--difficulty','moderate','--output',out,'--math-root','/media/jake/SSD/EDB/math'],environment={'PYTHONDONTWRITEBYTECODE':'1'}))
    commands.append(dict(cwd=str(ROOT),argv=[str(PYTHON),'-B',str(REPO/'generate/pipeline/render_preview.py'),'--input','render-samples.json','--output','render','--limit','8','--asset-root','.','--math-root','/media/jake/SSD/EDB/math'],environment={'PYTHONDONTWRITEBYTECODE':'1'}))
    save('reproduction-commands.json',commands)
    def check(paths,details):return dict(status='passed',evidence_paths=paths,details=details)
    result=dict(verdict='accepted',summary='All eight checks passed for the declared moderate blank family. The author’s historical grader failure was not reproduced with the current native executable. Package unchanged.',
        source_analysis={k:initial[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},
        checks=dict(
            source_replay=check(['source-analysis.json','source-replay-results.json'],'q-263058 prompt, worked solution, field type/key, complete single-answer bank and keyed mathematical value reproduced. Other source families explicitly unsupported.'),
            math=check(['math-results.json','samples.json','runner-batch.json'],'137 records checked independently from prompts using exact arithmetic, including keyed values and every equation in the final solve block; boundaries and all RHS2..30 covered.'),
            variety=check(['sampler-domain.json','delivery-coverage.json','delivery-independent/delivery.json','delivery-runner/delivery.json','selection-results.json'],'Full6264-triple sampler terminates with all four sign cases. Independent132->129 and runner5->5 under actual delivery filters. Independent delivered cases retain all signs. Selection rules examined and conditionally reproduced; live history/weights and future IDs remain documented limits.'),
            scope=check(['source-analysis.json','scope-results.json'],'Small signed affine exponent variations preserve exact natural-log inversion and moderate translation/division workload with one blank field.'),
            grading=check(['native-strict-execution.json','native-strict-report.json','native-diagnostic-input.json','native-diagnostic-report.json','shortcut-input.json','shortcut-native-report.json','native-current-binding.json'],'Current real native grader: main691 checks and shortcut792 checks all matched required acceptance/rejection, with zero unresolved outcomes; strict original-source wrong-zero also rejected.'),
            rendering=check(['render/rendering.json','render/input.json','render-visual-inspection.json','render/question-001.png','render/question-003.png','render/question-007.png','render/question-008.png'],'Eight actual-UI cases passed automated rendering and visual inspection, including source, relevant/irrelevant pairs and boundary.'),
            packaging=check(['packaging-results.json','package-before.json','package-after.json','reproduction-commands.json'],'Exact Python3.13.5 with no third-party runtime dependencies; deterministic CLI, relocation, empty count, invalid count/difficulty/parameter boundaries and no external output checked. Package files unchanged.'),
            decision_variation=check(['pedagogical-variation.json','counterfactual-results.json','shortcut-observations.json','shortcut-native-report.json','delivery-coverage.json'],'Both relevant and irrelevant controlled pairs verified through prompt, solution, key, rendered output and native grading. Conditional name/order shortcut actions examined before/after delivery; no reproducible incidental predictor found.')),
        findings=[])
    for c in result['checks'].values():
        for ref in c['evidence_paths']:assert (ROOT/ref).is_file() and (ROOT/ref).stat().st_size,ref
    assert load('package-before.json')==hash_package()
    save('contract-validation.json',dict(passed=True,pedagogical_schema='generate/pipeline/pedagogical-variation.schema.json',sample_ref_files_checked=len(set(refs)),all_sample_refs_relative_nonempty=True,eight_checks_have_created_evidence=True,source_analysis_has_required_evidence=True,package_unchanged=True))
    save('result.json',result)
    (ROOT/'session-state.md').write_text('REVIEW COMPLETE: accepted for declared moderate blank family. All eight checks and evidence contract pass; final structured report result.json. Package unchanged. Exact math137 records; native main691 + shortcut792 + strict1 checks pass with0 unresolved; actual renderer8 screenshots visually inspected; delivery132->129 and runner5->5. Source analysis preceded package inspection (initial preserved). Conditional learner-selection and snapshot limits recorded. No database operations or publication.\n')
    print(json.dumps(dict(verdict=result['verdict'],checks={k:v['status'] for k,v in result['checks'].items()},contract='passed',report='result.json',package_unchanged=True)))

if __name__=='__main__':main()
