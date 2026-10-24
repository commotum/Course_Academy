"""Build isolated v4 packages; install repository entrypoints only after commit."""
import argparse
import importlib.util
import json
import re
from pathlib import Path
import shutil
import sys

H=Path(__file__).resolve().parent;ROOT=H.parents[3]
sys.path.insert(0,str(ROOT/'generate/scratch/17592186068915'))
sys.path.insert(0,str(ROOT/'generate'))
import trig_scaffold as engine


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--install',action='store_true');args=parser.parse_args()
    old=ROOT/'reference/edb-math/repairs/2026-10-24-trig-substitution-bands'
    sys.path.insert(0,str(old))
    spec=importlib.util.spec_from_file_location('prior_printed_checker',old/'check.py')
    reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
    for kp in engine.CASES:
        d=H/str(kp);source=json.loads((d/'source/source.json').read_text());inv=json.loads((d/'inventory/inventory.json').read_text())
        record=source['material']['kp'];excluded=[];failures=[]
        for q in inv['questions']+[inv['canonical_example']]:
            try:
                text=q[':question/problem'].replace(r'{\int }',r'\int').replace(r'\text{d}x',r'\mathrm{d}x').replace(r'\textrm d x',r'\mathrm{d}x')
                text=text.replace('y','x').replace('z','x').replace(r'\text{d}x',r'\mathrm{d}x')
                text=text.replace(r'\textrm{d}x',r'\mathrm{d}x').replace(r'\textrm dx',r'\mathrm{d}x')
                text=re.sub(r'(?<![A-Za-z])dx',lambda _:r'\mathrm{d}x',text)
                text=re.sub(r'\\dfrac\s+(\\pi|x|\d+)\s+(\d+)',lambda m:r'\frac{'+m[1]+'}{'+m[2]+'}',text)
                text=re.sub(r'\\int_(-?\d+)\^',lambda m:r'\int_{'+m[1]+'}^',text)
                text=text[text.index(r'\int'):]
                body,var,lo,hi,_=reader.integral(text)
                excluded.append(engine.task_key(body,lo,hi))
            except Exception as exc:failures.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'error':str(exc)})
        # A retired/generated task cannot be lost just because an old source
        # uses noncanonical imported TeX. Stored generated prompts are canonical.
        assert not any(not f['source'] for f in failures),failures
        origin={
            'easy':'Authored supplied-substitution transformation stage, modeled on imported q-49529/q-49532 scaffolding; own KP sources anchor the integrands.',
            'moderate':'Own imported integration methods with one small factor and provided primitive/endpoint facts; authored task support explicitly changes response demand.',
            'hard':{
                17592186068915:'Authored single negative-inner-derivative condition, with familiar endpoint values supplied; replaces the uncalibrated compound hard band.',
                17592186068916:'Authored negative affine derivative/decreasing-bounds condition across familiar reciprocal derivative families; no fractional slopes or radical evaluation.',
                17592186068917:'Reciprocal-inner hard source q-3038 and square-root moderate source q-2377; authored band uses recognition of the less obvious inner function with small coefficients.',
                17592186068918:'Source-supported single rational rearrangement (q-113997/q-113992), nested inner (q-73674/q-114004), or definite evaluation (q-350887/q-350901).'}[kp]}
        evidence={'kp':{'db_id':kp,'id':str(record[':knowledge-point/id']),'title':record[':knowledge-point/title']},
            'basis':source['basis'],'excluded_tasks':sorted(set(excluded)),'exclusion_parse_limitations':failures,
            'band_origin':origin,'pedagogical_reference':'reference/edb-math/audits/2026-10-24-difficulty-pedagogy/README.md',
            'benchmark_kp':17592186064172,'benchmark_sources':['q-66139','q-113887','q-113890','q-31249','q-113893','q-71910'],
            'source_counts':{band:sum(bool(q.get(':question/math-academy-id'))and q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/'+band for q in inv['questions'])for band in origin}}
        contract={'version':engine.VERSION,'families':{band:list(cases)for band,cases in engine.CASES[kp].items()},
            'easy':{'operation':'Choose the integral produced by the given substitution','provided_substitution':True,'response':'radio','outside_coefficient_maximum':3,'displayed_bank_coefficient_maximum':8},
            'moderate':{'operation':'Choose the substitution and complete the calculation','provided_primitive':True,'provided_endpoint_values':True,'response':'blank'},
            'hard':{'operation':origin['hard'],'provided_primitive':True,'provided_endpoint_values':True,'response':'blank','independent_extra_challenges':1},
            'parameter_policy':'Small integer amplitudes/slopes; at most one small reciprocal factor. No independently compounded fractional amplitude, fractional slope, phase and radical bounds.',
            'answer_policy':'Preserve trig arguments. Final solution exactly matches the answer fragment plus any externally displayed C. No unshown log conversion.',
            'sampling_policy':'Seeded family-first sampling; no amplitude-only padding; exclude existing/retired mathematical task fingerprints; unsupported/short requests fail explicitly.',
            'calibration':'Source-informed authored progression, not external psychometric calibration. Do not inherit difficulty from numeric magnitude or response shape alone.'}
        wrapper=f'''#!/usr/bin/env python3
"""KP {kp}: scaffolded substitution with controlled prerequisite work."""
import json
from pathlib import Path
import sys
LOCAL=Path(__file__).with_suffix('')
if not (LOCAL/'trig_scaffold.py').is_file():LOCAL=Path(__file__).resolve().parent
sys.path.insert(0,str(LOCAL))
import trig_scaffold as model
KP={kp}
EVIDENCE=json.loads((LOCAL/'source-evidence.json').read_text())
def generate(level,seed=0,template=None,**kwargs):
    return model.generate(KP,level,seed,template,evidence=EVIDENCE,**kwargs)
def batch(level,count=8,seed=0,template=None):
    return model.batch(KP,level,count,seed,evidence=EVIDENCE,template=template)
if __name__=='__main__':model.cli(KP,LOCAL)
'''
        targets=[d/'package']+([ROOT/f'generate/scratch/{kp}']if args.install else [])
        for target in targets:
            target.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/'generate/trig_scaffold.py',target/'trig_scaffold.py')
            shutil.copy2(ROOT/'generate/scratch/17592186068915/trig_format.py',target/'trig_format.py')
            (target/'source-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
            (target/'band-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
            (target/'generator.py'if target.name=='package'else ROOT/f'generate/scratch/{kp}.py').write_text(wrapper)
        if args.install:
            capabilities={'supported_levels':['easy','moderate','hard'],'implementation_version':engine.VERSION,
                'band_contract':'band-contract.json','imported_source_counts':evidence['source_counts'],'band_origin':origin,
                'maximum_records_per_call':100,'unsupported_levels_filled':False,'response_policy':'Supplied-substitution radio at easy; supported full calculation at moderate/hard.'}
            (ROOT/f'generate/scratch/{kp}/capabilities.json').write_text(json.dumps(capabilities,indent=2)+'\n')
            (ROOT/f'generate/scratch/{kp}/README.md').write_text(f'''# Scaffolded trig substitution — KP {kp}

Current implementation: `../{kp}.py`, using the bundled `trig_scaffold.py` helper.
Version: {engine.VERSION}. The registered immutable package is recorded in
`reference/edb-math/repairs/2026-10-24-trig-scaffolding/`.

Easy supplies u and assesses transformation. Moderate asks for the full calculation.
Hard adds one relevant condition while keeping arithmetic simple. Full calculations
provide the primitive and any required endpoint values. See `band-contract.json`.

Older extraction, capacity, validation, and replay files remain historical evidence;
they do not describe the current sampler. Imported questions and historical learner
work are preserved. Newly sampled banks are explicitly authored, not source replays.
''')
        print(kp,'package prepared; existing tasks excluded',len(excluded),'source parsing limitations',len(failures),flush=True)


if __name__=='__main__':main()
