#!/usr/bin/env python3
"""Live, blinded semantic controls; deliberately not a full publication review.

Two actual Codex turns checkpoint source-only accounts before exposing designs.
The production principles/reviewer prompt govern judgment, but native/UI/report
acceptance is exercised separately by run_offline_pipeline.py. Gold verdicts
never enter either prompt. No EDB transport or publication is available here.
"""
from pathlib import Path
import hashlib
import json
import os
import random
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def controls():
    # Each pair is (design, expected semantic verdict). Labels/order are shuffled
    # before the reviewer sees them. A verdict is not inferred from echoed prose.
    return [
        ('substitution_endpoint', 'Independent practice: choose a substitution and complete an indefinite integral, returning an antiderivative in x. The target includes recognizing the inner function and differential.', [
            ('Easy question: Given u=x² and du=2x dx, rewrite ∫2x cos(x²) dx as an integral in u. Key: ∫cos(u) du.', 'reject'),
            ('Question: Evaluate ∫2x cos(x²) dx. Blank key: sin(x²)+C. The worked solution introduces u and du only after submission.', 'accept')]),
        ('missing_easy_trig', 'Independent practice simplifies trig sum/difference expressions using previously learned identities. No easy examples were imported; numerical calibration may be authored without changing the operation.', [
            ('Easy question: Use sin(A−B)=sin A cos B−cos A sin B with A=θ+π/3 and B=π/6 to simplify sin(θ+π/3)cos(π/6)−cos(θ+π/3)sin(π/6). Key sin(θ+π/6).', 'reject'),
            ('Easy question: Simplify sin(θ+π/3)cos(π/6)−cos(θ+π/3)sin(π/6). No formula or substituted arguments are shown until the worked solution. Key sin(θ+π/6). Other bands retain that identity with different familiar angles.', 'accept')]),
        ('translated_bank_rank', 'Solve the displayed two-equation coefficient system, then give the coefficient sum. Example 2a+b=7, a−b=2 gives a+b=4. Radio answers are numerical.', [
            ('Every system is solved to get s. The implementation creates options [s,s+1,s+2,s+3] and shuffles their display order. Example key4 bank[6,4,7,5]; another key7 bank[8,10,7,9].', 'reject'),
            ('Banks come from different plausible elimination/sign errors, deduplicated without deleting a mathematical system. Examples include key4 bank[3,4,5,6], key7 bank[7,6,3,8], key2 bank[4,2,5,1]. The sampler varies the coefficient matrix and derives the key from each displayed system.', 'accept'),
            ('An independently sampled two-item fragment happens to have its key smallest twice. A reviewer searched many ranks/subgroups after observing the keys. No fixed offset construction, usable finite-pool mechanism or independent confirmation has been found; record this as a diagnostic concern without imposing a rank quota.', 'accept')]),
        ('independent_qualifiers', 'Inspect three matrices independently and choose every diagonal matrix. A=diag(1,2), B=[[1,1],[0,2]], C=diag(3,4) has answer A+C. Current checkbox contract requires at least one qualifying choice.', [
            ('The generator chooses whether A or C will be diagonal, then forcibly makes the other nondiagonal. This is mandatory for every generated item because a repair example showed A-only versus C-only. B is always nondiagonal.', 'reject'),
            ('Each matrix property is constructed independently; reject only the all-false case for the nonempty response contract. A-only, C-only and A+C occur. The concrete displayed source item keys A+C.', 'accept')]),
        ('bank_collision_valid_case', 'Determine rank from matrix dimensions and nonpivot count on feasible ordinary matrices. A 4×7 matrix with3 nonpivot columns has rank4; full-row-rank cases belong to the target.', [
            ('Reject every item whose rank equals the row count, because the original row-count distractor would duplicate the key. This excludes 4×7 with3 nonpivots.', 'reject'),
            ('Keep 4×7 with3 nonpivots and use distinct plausible choices3,4,7 instead of duplicating the rows recipe. Explain rank=7−3=4 in the solution. Retain the original bank separately as replay evidence.', 'accept')]),
        ('valid_cancellation', 'Evaluate definite linear-argument trig integrals using the taught antiderivative/bounds method or a justified efficient equivalent. Valid cancellations are within scope.', [
            ('Reject every non-easy item whose result is zero or has a zero endpoint contribution, including ∫₀^π 2cos(2x) dx, purely to protect the hard label.', 'reject'),
            ('Allow ∫₀^π 2cos(2x) dx=0 and ∫₀^(π/4) 2cos(2x) dx=1. Both use a blank determined by the family, not the answer; solutions evaluate sin(2x) at the bounds. No given intermediate setup.', 'accept')]),
        ('equivalent_unshown_form', 'Integrate cos(3−2x), practicing inner-derivative scaling. The source teaches the direct primitive and does not require argument reversal/parity conversion as an answer-recognition step.', [
            ('Solution ends at −sin(3−2x)/2+C. A separate CAS renderer keys sin(2x−3)/2+C in a radio bank. No conversion is shown or justified; author cites only algebraic equality and native acceptance.', 'reject'),
            ('Solution ends at −sin(3−2x)/2+C and the radio key has that form. Native equivalent entries, where free entry applies, remain allowed. No extra parity step is needed to match the displayed answer.', 'accept')]),
        ('graph_readability_without_giveaway', 'From x=t,y=t² and t=−1,0,1, calculate coordinates and choose the matching curve. The student must distinguish y=x² from y=x²+1 at the displayed answer-card size. Solution overlays may show calculated points after answering.', [
            ('Inspect graph-design-a.png. These two curves are shown on a shared very coarse scale; only the keyed curve has the three calculated table points marked before answering. The generator treats unique equations and these markers as sufficient readability evidence.', 'reject'),
            ('Inspect graph-design-b.png. Curves share a readable scale with no answer-only marks. Calculated point overlays are reserved for the worked solution after answering. This control concerns the pictured card design only; actual player validation is separate.', 'accept')]),
        ('heldout_orthogonal_subset', 'For u=(1,2), choose all perpendicular vectors among A=(2,−1),B=(1,1),C=(−4,2). Independently apply the dot-product criterion to each option.', [
            ('Render a radio field and key A alone. The generator deletes all but the first perpendicular vector in future cases because prior examples had one answer.', 'reject'),
            ('Render a checkbox field with A+C correct. Dot products are0,3,0; explanation checks each. Future choices derive independent truth from their components, conditioned only on the current nonempty response requirement.', 'accept')]),
        ('heldout_non_target_given', 'A newly invented unit blick equals24cm. Convert3 blick/min to cm/s. Assess choosing factors and calculation; minute-to-second recall is a prerequisite, while the invented unit definition is a necessary given.', [
            ('Question states blick=24cm, then gives the setup3×24/60 and asks the student to calculate the final cm/s value. Key1.2.', 'reject'),
            ('Question defines1 blick=24cm and asks to convert3 blick/min to cm/s, leaving factor selection and ordinary time recall to the learner. Key1.2; setup appears in the solution.', 'accept'),
            ('Remove the blick-to-cm definition because no eligible standalone source supplied that invented relation, but still ask for3 blick/min in cm/s and key1.2.', 'reject')]),
        ('heldout_calculator_progression', 'Find rectangle area from two supplied side lengths. Recall/select the area relationship; keep a consistent calculator and precision contract. Authored difficulty is not empirical calibration.', [
            ('Easy gives A=length×width and partial product for3×6; hard gives perimeter instead of one side and requires inverse perimeter algebra. Decimal answer banks use key±0.01 offsets without a precision objective.', 'reject'),
            ('Easy sides3cm and6cm, moderate6cm and7cm, hard2.5cm and5cm. All ask for area in cm² without a supplied formula; same operation, controlled numbers. Decimal bank12.5,7.5,15 reflects area/sum/perimeter errors, not arbitrary cents. Bands are explicitly authored calibration.', 'accept')]),
    ]


def main():
    directory = Path(sys.argv[1]).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault('MPLCONFIGDIR', str(directory / 'mpl'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    x = np.linspace(-2,2,300)
    for tag, upper in [('a',100),('b',5)]:
        fig, axes = plt.subplots(1,2,figsize=(5.2,2.6),dpi=120)
        for i, ax in enumerate(axes):
            ax.plot(x,x*x+i,color='#244d73',lw=2)
            ax.set(xlim=(-2,2),ylim=(-1,upper),title=chr(65+i))
            ax.set_xticks([-2,-1,0,1,2]); ax.set_yticks([0,50,100] if tag=='a' else [0,1,2,3,4,5]); ax.grid(alpha=.35)
            if tag=='a' and i==0: ax.scatter([-1,0,1],[1,0,1],color='#c54c36',s=40,zorder=3)
        fig.tight_layout(); fig.savefig(directory/f'graph-design-{tag}.png'); plt.close(fig)
    cases=controls(); randomizer=random.Random(20261105)
    sources=[{'id':name,'target_source':source} for name,source,_ in cases]
    candidates=[]; gold={}
    for name,_, designs in cases:
        designs=list(designs); randomizer.shuffle(designs)
        for index,(design,verdict) in enumerate(designs):
            key=f'{name}:{index+1}'; candidates.append({'id':key,'case':name,'design':design}); gold[key]=verdict
    (directory/'sources.json').write_text(json.dumps(sources,indent=2))
    # Kept outside the working directory and never named in prompts.
    gold_file=directory.parent/(directory.name+'-gold.json'); gold_file.write_text(json.dumps(gold,indent=2))
    account_schema={'type':'object','properties':{'accounts':{'type':'array','items':{'type':'object','properties':{'id':{'type':'string'},'required_work':{'type':'array','items':{'type':'string'}},'allowed_givens':{'type':'string'},'endpoint':{'type':'string'}},'required':['id','required_work','allowed_givens','endpoint'],'additionalProperties':False}}},'required':['accounts'],'additionalProperties':False}
    verdict_schema={'type':'object','properties':{'verdicts':{'type':'array','items':{'type':'object','properties':{'id':{'type':'string'},'verdict':{'type':'string','enum':['accept','reject','uncertain']},'remaining_work':{'type':'string'},'reason':{'type':'string'},'inspection':{'type':'string'}},'required':['id','verdict','remaining_work','reason','inspection'],'additionalProperties':False}}},'required':['verdicts'],'additionalProperties':False}
    for name,schema in [('accounts',account_schema),('verdicts',verdict_schema)]: (directory/f'{name}.schema.json').write_text(json.dumps(schema))
    def run(name,prompt,resume=None):
        (directory/f'{name}.prompt.txt').write_text(prompt)
        command=['codex','exec','--sandbox','read-only','-c','approval_policy="never"','-C',str(directory)]
        if resume: command+=['resume']
        command+=['--skip-git-repo-check','--model','gpt-6.1-sol','-c','model_reasoning_effort="high"','--output-schema',str(directory/f'{name}.schema.json'),'--output-last-message',str(directory/f'{name}.json'),'--json']
        command+=([resume,'-'] if resume else ['-'])
        with (directory/f'{name}.events.jsonl').open('w') as log:
            subprocess.run(command,input=prompt,text=True,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=1800)
        return json.loads((directory/f'{name}.json').read_text())
    first=f'''You are the generator verifier in a bounded offline evaluation. This phase is source-only: read {ROOT}/generate/principles.md and sources.json. Do not inspect candidates, evaluation scripts, prior reports or gold files. Independently state required learner work, permissible givens and endpoint for each target. Do not query/write a database or change any files. Return the account schema. These authored sources are controls, not imported Math Academy records.'''
    accounts=run('accounts',first)
    original=(directory/'accounts.json').read_bytes(); initial_sha=hashlib.sha256(original).hexdigest()
    thread=None
    for line in (directory/'accounts.events.jsonl').read_text().splitlines():
        try: row=json.loads(line)
        except ValueError: continue
        if row.get('type')=='thread.started': thread=row['thread_id']
    if not thread: raise ValueError('Source-only thread was not retained')
    (directory/'candidates.json').write_text(json.dumps(candidates,indent=2))
    second=f'''Continue your independent source accounts. Read {ROOT}/generate/pipeline/reviewer.md and {ROOT}/generate/principles.md, then candidates.json and the two graph images using an image-viewing tool. This is a bounded SEMANTIC control review, not a full native/UI/package acceptance; do not fabricate those reports or claim production certification. Evaluate each design against your checkpointed target account and actual learner work, including restrictions and gratuitous demands. Accept means the described instructional design preserves the task; reject means a concrete supported defect; uncertain means evidence genuinely insufficient. For graphs inspect actual pixels and state what you observed. Return every candidate verdict with concrete reasoning. Do not inspect gold, original failure reports, evaluation scripts or other filesystem materials. Do not change files, query EDB, or infer that every pair contains one bad design. Candidate order is arbitrary.'''
    result=run('verdicts',second,thread)
    if hashlib.sha256((directory/'accounts.json').read_bytes()).hexdigest()!=initial_sha: raise ValueError('Initial account changed')
    actual={item['id']:item['verdict'] for item in result['verdicts']}
    errors=[{'id':key,'expected':expected,'observed':actual.get(key)} for key,expected in gold.items() if actual.get(key)!=expected]
    if len(actual)!=len(gold): errors.append({'coverage':'duplicate or unexpected candidate IDs'})
    summary={'kind':'live-blinded-semantic-controls','cases':len(cases),'candidates':len(gold),'source_account_sha256':initial_sha,'thread_id':thread,'mismatches':errors,'scope':'Semantic judgment only; actual pipeline/native/player validation reported separately.'}
    (directory/'summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
    return bool(errors)


if __name__=='__main__': raise SystemExit(main())
