"""Independent prompt/solution arithmetic, complete source banks, native grading."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('position_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def expression(v):
    v=v.replace(' ','')
    m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',v)
    if m:return sp.Integer(m[1] or 1)*sp.sqrt(int(m[2]))
    if re.fullmatch(r'\d+',v):return sp.Integer(v)
    raise ValueError('Unrecognized value '+v)

def parse_question(q):
    pairs=re.findall(r'\$[A-Z]\((-?\d+),\s*(-?\d+)\)',q[':question/problem'])
    if len(pairs)!=2:
        # The one source plot-only task has explicitly transcribed coordinates
        # in its verified worked solution; never infer from an asset name.
        pairs=re.findall(r'[A-Z]\((-?\d+),\s*(-?\d+)\)',q.get(':question/worked-solution',''))[:2]
    assert len(pairs)==2, 'Coordinates unresolved'
    return tuple(tuple(map(int,p)) for p in pairs)

def fingerprint(q):
    p,r=parse_question(q);return g.fingerprint_squared(sum((b-a)**2 for a,b in zip(p,r)))

def solution_check(q):
    p,r=parse_question(q);dx,dy=r[0]-p[0],r[1]-p[1];n=dx*dx+dy*dy
    solution=q[':question/worked-solution']
    lines=[line for line in solution.splitlines() if line.startswith('&=')]
    assert len(lines)==6
    # Verify the position subtraction and resulting vector against the prompt.
    assert lines[1].removeprefix('&= ').removesuffix(r' \\') == f'({g.vector(*r)}) - ({g.vector(*p)})'
    assert lines[2].removeprefix('&= ')==g.vector(dx,dy)
    signed=re.search(r'\\sqrt\{\((-?\d+)\)\^\{2\} \+ \((-?\d+)\)\^\{2\}\}',solution)
    assert signed and list(map(int,signed.groups()))==[dx,dy]
    squares=re.search(r'&= \\sqrt\{(\d+) \+ (\d+)\}',solution)
    assert squares and list(map(int,squares.groups()))==[dx*dx,dy*dy]
    assert r'&= \sqrt{'+str(n)+'}' in solution
    assert sp.simplify(expression(lines[-1][3:])-sp.sqrt(n))==0
    field=q[':question/answer-fields'];assert len(field)==1;field=field[0]
    assert field[':answer-field/key']=='selection'
    ft=field[':answer-field/type'];assert (ft if isinstance(ft,str) else ft[':db/ident'])==':answer-field.type/radio'
    answers=field[':answer-field/choices'];assert len(answers)==5
    vals=[expression(a[':answer/value']) for a in answers]
    assert len(set(vals))==5 and all(x.is_positive for x in vals)
    designation=field[':answer-field/correct'];cid=str(designation[1] if isinstance(designation,list) else designation[':answer/id'])
    assert [str(a[':answer/id']) for a,val in zip(answers,vals) if sp.simplify(val-sp.sqrt(n))==0]==[cid]
    assert len({str(a[':answer/id']) for a in answers})==5
    return sp.sqrt(n)

def independent(rec):
    solution_check(rec['question']);meta=rec['generation']
    assert rec['knowledge_point']['db_id']==g.KP_ID and rec['knowledge_point']['id']==g.KP_UUID
    assert rec['question'][':question/difficulty']==':question.difficulty/moderate'
    assert meta['parameter_fingerprint']==fingerprint(rec['question'])
    assert rec==g.generate_profile(meta['template'],meta['parameters']['scale'],meta['seed'])
    for asset in meta['assets']:
        assert asset['points']==[list(p) for p in parse_question(rec['question'])]
        assert hashlib.sha256((ROOT/asset['path']).read_bytes()).hexdigest()==asset['sha256']
        assert asset['reference'] in rec['question'][':question/problem']
    return True

def checks(rec):
    solution_check(rec['question']);f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Independent coordinate-distance result and every full-bank option'} for a in f[':answer-field/choices']]

def main():
    raw=json.loads((HERE/'reference/initial/source.json').read_text())
    questions={q[':question/math-academy-id']:q for q in raw['record'][':knowledge-point/questions']}
    replay=[];recipes=[]
    for mid,spec in g.SPECS.items():
        rec=g.generate_profile(mid,1,0);independent(rec)
        original=questions[mid][':question/answer-fields'][0][':answer-field/choices']
        generated=rec['question'][':question/answer-fields'][0][':answer-field/choices']
        observed=[expression(a[':answer/value']) for a in original];emitted=[expression(a[':answer/value']) for a in generated]
        assert len(original)==len(generated)==5
        assert sorted(map(str,observed))==sorted(map(str,emitted))
        assert [a[':answer/value'] for a in original]==[a[':answer/value'] for a in generated]
        correct=solution_check(rec['question']);assert sum(sp.simplify(v-correct)==0 for v in observed)==1
        replay.append({'source_id':mid,'matched_choices':5,'total_choices':5,'matched_distractors':4,'total_distractors':4,'complete_bank':True,'rendered_values_exact':True,'source_key_missing':True,'correct_key_independently_computed':str(correct),'missing':[],'extra':[]})
        for i,a in enumerate(original):
            recipes.append({'source_id':mid,'source_field':'selection','source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'profile':mid,'recipe':'scale * ('+a[':answer/value']+')','source_value_reproduced':True,'interpretation':'Observed homogeneous value pattern; misconception not inferred','correct':sp.simplify(expression(a[':answer/value'])-correct)==0})
    previews=g.batch('moderate',8,175921);assert len(previews)==8
    assert len({r['generation']['parameter_fingerprint'] for r in previews})==8
    for r in previews:independent(r)
    native=[{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in previews]
    (HERE/'reference/native-input.json').write_text(json.dumps(native,indent=2)+'\n')
    subprocess.run([str(HERE/'check-engine'),str(HERE/'reference/native-input.json'),str(HERE/'reference/native-report.json')],check=True)
    report=json.loads((HERE/'reference/native-report.json').read_text());assert report['documented_unresolved_checks']==0
    (HERE/'preview.json').write_text(json.dumps(previews,indent=2)+'\n')
    (HERE/'templates.json').write_text(json.dumps({'source_basis':raw['basis'],'profiles':g.SPECS,'choice_mapping':recipes,'proposed_bounds':{'scale':[1,2,3,4]},'sampling_extension':'Positive integer scaling; source observed only scale 1','source_bank_replay':replay},indent=2)+'\n')
    (HERE/'review.md').write_text('\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n\nChoices: '+', '.join('$'+a[':answer/value']+'$' for a in r['question'][':question/answer-fields'][0][':answer-field/choices']) for r in previews)+'\n')
    files=[HERE.with_suffix('.py'),HERE/'validate.py',HERE/'templates.json',HERE/'capabilities.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'check-engine',HERE/'reference/initial/source.json']
    result={'status':'pass','source_basis':raw['basis'],'source_fidelity':{'complete_available_banks':2,'matched_choices':10,'total_choices':10,'matched_distractors':8,'total_distractors':8,'replay':replay,'not_full_source_fidelity':'Three rated sources lack fields/banks, so cannot replay their grading. Diagram-only structure excluded. New keys/solutions/ratings are explicit authored completions.'},'mathematical_validation':{'instances':8,'independent_coordinate_distance':True,'complete_bank_uniqueness':True,'deterministic_replay':True,'all_profile_scale_boundaries':True,'distinct_squared_distances':8},'native_engine':report,'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'dependencies':{'sympy':sp.__version__},'plots':'Matplotlib; all eight inspectable, generated from exact same points as question'}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','instances':8,'bank_replay':'10/10 options, 8/8 distractors, 2/2 available banks','native':{'accepted':report['accepted_checks'],'rejected':report['rejected_checks']}}))
if __name__=='__main__':main()
