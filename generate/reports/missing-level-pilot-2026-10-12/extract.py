#!/usr/bin/env python3
"""Extract and audit the three-KP pilot from its frozen EDB export.

Run with .venv/bin/python. This is an evidence extractor, not a question generator.
"""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('source_math', ROOT / 'generate/scratch/17592186198379/math_parser.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)


def scalar(text):
    # The audited parser supports i,j,k; this bijective renaming extends it to
    # the source's r,s,u without changing expressions or conflating variables.
    text = re.sub(r'(\\[a-zA-Z]+)|([rsu])', lambda m:
        m[1] if m[1] else {'r':'i','s':'j','u':'k'}[m[2]], text)
    return parser.scalar(text)


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=str) + '\n')


# Literal prompt components, recorded separately from proposed sampling bounds.
DETERMINANTS = {
    'q-1088': ('unrated-radical-radio', [r'\sqrt{2}','5','1','3']),
    'q-1089': ('E1-named-symbolic-root-radio', [r'\sqrt{x}','y',r'{y}^{2}',r'\sqrt{x}']),
    'q-1083': ('E2-bare-symbolic-radio', ['2x',r'{y}^{2}','z','-3']),
    'q-1087': ('E3-numeric-rational-radio', [r'\frac{1}{2}','17','1','10']),
    'q-275595': ('E4-root-blank', [r'\sqrt{3}','y','2',r'\sqrt{3}']),
    'q-317374': ('E4-root-blank', [r'\sqrt{6}','y','4',r'\sqrt{6}']),
    'q-69649': ('E5-bare-root-monomial-radio', [r'3\sqrt{x}',r'{z}^{2}','2y',r'-\sqrt{x}']),
    'q-127601': ('M1-fraction-cancellation-radio', ['-x','-2y',r'\frac{x}{2}','5y']),
    'q-127603': ('M2-polynomial-factor-radio', ['2x','y','-5','xy']),
    'q-69650': ('M3-four-symbols-factor-radio', ['-2r','3s','-2t','3u']),
    'q-317367': ('M4-numeric-rational-blank', [r'\frac{2}{5}','-3',r'-\frac{1}{2}','2']),
    'q-317368': ('M4-numeric-rational-blank', [r'-\frac{3}{4}','5','2','-1']),
    'q-317372': ('M5-symbolic-polynomial-blank', ['3x','2y','-5','x']),
}
MATRICES = {
    'q-13488': ('unrated-inline-in-bounds-radio', [[1,1,2],[-1,1,3]], 1,3),
    'q-13496': ('unrated-out-of-bounds-radio', [[0,1,2,4],[-1,2,-3,5],[2,1,-3,4]],4,3),
    'q-279260': ('E1-lookup-radio', [[1,-2,6],[-2,-1,7]],2,2),
    'q-279539': ('E2-lookup-blank', [[-5,-2,0,9],[3,-8,-2,5],[-2,2,5,-8],[6,6,-6,0],[-6,4,2,5]],5,3),
    'q-279540': ('E2-lookup-blank', [[4,5,-2,0],[-2,-1,2,5],[3,4,0,-3]],3,2),
    'q-13497': ('E1-lookup-radio', [[0,1,2,4],[-1,2,-3,5],[2,1,-3,4]],2,4),
    'q-125561': ('E1-lookup-radio', [[1,2],[-1,5],[-3,4]],3,1),
}
TRIG = {
    'q-124750': ('M1-rational-y-sec-radio','y','1','5'),
    'q-124743': ('M2-rational-x-csc-radio','x','1','3'),
    'q-65062': ('M3-radical-y-sec-radio','y',r'\sqrt{3}','3'),
    'q-85234': ('M3-radical-y-sec-radio','y',r'\sqrt{2}','3'),
    'q-65064': ('M4-radical-x-csc-radio','x',r'\sqrt{15}','5'),
    'q-65066': ('unrated-rational-y-perfect-square','y','3','5'),
}


def components(q):
    qid = q[':question/math-academy-id']
    if qid in DETERMINANTS:
        template, raw = DETERMINANTS[qid]
        a,b,c,d = map(scalar,raw)
        values = dict(zip('abcd', (a,b,c,d)))
        pattern = dict(correct=a*d-b*c, plus=a*d+b*c, reversed=b*c-a*d,
            main_diagonal_only=a*d, subtract_off_diagonal_only=-b*c,
            omit_c=a*d-b, omit_b=a*d-c, top_right_minus_bottom_right=b-d)
        return template, dict(entries=raw, ad=str(a*d), bc=str(b*c),
            symbol_aliases={'r':'i','s':'j','u':'k'} if qid=='q-69650' else {},
            domains='Real variables; x >= 0 in templates containing sqrt(x).',
            expected_answer=s.latex(s.expand(a*d-b*c))), s.simplify(a*d-b*c), values, pattern
    if qid in MATRICES:
        template, matrix, i,j = MATRICES[qid]
        expected = matrix[i-1][j-1] if i<=len(matrix) and j<=len(matrix[0]) else 'No such entry'
        return template, dict(matrix=matrix, rows=len(matrix),columns=len(matrix[0]),row=i,column=j,
            domains='One-based integer indices; allow absent entry only for the observed out-of-bounds family.',
            expected_answer=str(expected)), expected, dict(A=matrix,i=i,j=j), {}
    template, axis,n,b = TRIG[qid]
    n,b = scalar(n),scalar(b)
    K = s.sqrt(b*b-n*n)
    answer = s.simplify(b/K)
    pattern = dict(correct=b/K, missing_reciprocal=K/b, missing_denominator_scale=1/K,
        opposite_sign=-b/K, numerator_instead_of_denominator=n/K,
        negative_numerator_instead_of_denominator=-n/K,
        known_denominator_only=b, radicand_divided_by_denominator=(b*b-n*n)/b,
        other_ratio_squared=(b*b-n*n)/(n*n), root_over_known_numerator_squared=K/(n*n))
    return template, dict(given_axis=axis,given_numerator=str(n),given_denominator=str(b),
        given_coordinate=s.latex(n/b),missing_coordinate=s.latex(K/b),
        reciprocal='sec' if axis=='y' else 'csc',
        radicand=str(b*b-n*n),perfect_square_complement=bool(K.is_Rational),
        domains='0 < coordinate < 1, first quadrant, positive root, reciprocal denominator nonzero.',
        expected_answer=s.latex(answer)), answer, dict(n=n,b=b,K=K), pattern


def observed_pattern(value):
    """Retain the whole value as a descriptive expression, never infer a cause."""
    expr = scalar(value)
    if expr.free_symbols:
        return dict(kind='observed_symbolic_expression', expression=str(expr),
            parameters={str(v):'source symbol '+{'i':'r','j':'s','k':'u'}.get(str(v),str(v))
                        for v in sorted(expr.free_symbols,key=str)},
            generalization='Numeric coefficients remain source-profile constants; error mechanism unresolved.')
    coefficient, remaining = expr.as_coeff_Mul()
    if remaining.is_Pow and remaining.exp == s.Rational(1,2):
        p,q = coefficient.as_numer_denom()
        return dict(kind='observed_radical_value_pattern', expression='p * sqrt(d) / q',
            parameters=dict(p=str(p),d=str(remaining.base),q=str(q)),
            generalization='Source-profile constants; how these change with new prompt parameters is unresolved.')
    if not expr.is_Rational:
        return dict(kind='observed_constant_expression',expression=str(expr),parameters={},
            generalization='Complete fixed source expression; prompt-dependent generation and error mechanism unresolved.')
    p,q = expr.as_numer_denom()
    return dict(kind='observed_rational_value_pattern', expression='p / q',
        parameters=dict(p=str(p),q=str(q)),
        generalization='Source-profile constants; no computational mistake is inferred.')


def main():
    source = read(HERE/'source.json')
    scores = {r['kp_entity']:r for r in read(ROOT/'generate/reports/kp-absence-2026-10-12/scores.json')['kps']}
    cases, assets = [], []
    asset_folder=HERE/'assets';asset_folder.mkdir(exist_ok=True)
    for kp in source['records']:
        folder=HERE/str(kp[':db/id']);folder.mkdir(exist_ok=True)
        canonical=kp.get(':knowledge-point/canonical-example',{})
        for attr in (':question/problem',':question/worked-solution'):
            for path in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',canonical.get(attr,'')):
                asset=Path('/media/jake/SSD/EDB/math')/path
                assert asset.is_file(),asset
                shutil.copyfile(asset,asset_folder/asset.name)
                assets.append(dict(question=canonical[':question/math-academy-id'],context='canonical',
                    role=attr.split('/')[-1],source_path=str(asset),local_path='assets/'+asset.name,
                    sha256=hashlib.sha256(asset.read_bytes()).hexdigest(),
                    inspection='Visually inspected in 12-asset contact sheet; first-quadrant unit circle and angle.'))
        rendered=['# Complete source practice questions', '',
            f"EDB math basis {source['database']['basis']}; KP {kp[':db/id']}. "
            'Original prompts, every choice, and one original worked solution are retained. '
            'Missing source attributes remain explicitly missing.', '']
        for q in kp[':knowledge-point/questions']:
            qid=q[':question/math-academy-id']
            template, features, expected, params, candidates=components(q)
            fields=[]
            for f in q.get(':question/answer-fields',[]):
                field_type=f[':answer-field/type'][':db/ident'].split('/')[-1]
                profile=None if field_type=='blank' else 'bank-'+qid
                choices=[]
                for a in f.get(':answer-field/choices',[]):
                    value=a[':answer/value']
                    marked=a[':db/id']==f.get(':answer-field/correct',{}).get(':db/id')
                    if a[':answer/type'][':db/ident']==':answer.type/text':
                        math_correct=value==expected
                        recipe=dict(kind='fixed_text',expression=value,parameters={},
                            generalization='Offer exactly this source text for an absent-entry option.')
                        matches=[]
                    else:
                        expr=scalar(value)
                        math_correct=not isinstance(expected,str) and s.simplify(expr-expected)==0
                        matches=[name for name,formula in candidates.items() if s.simplify(expr-formula)==0]
                        recipe=observed_pattern(value)
                        if qid in MATRICES:
                            A=features['matrix']
                            locations=[(i+1,j+1) for i,row in enumerate(A) for j,v in enumerate(row) if s.simplify(expr-v)==0]
                            recipe=dict(kind='matrix_entry_candidates' if locations else 'fixed_source_scalar',
                                expression='A[r-1][c-1]' if locations else 'k',
                                parameters=dict(candidate_positions=locations) if locations else dict(k=str(expr)),
                                generalization='Multiple matching cells do not identify which was sampled; preserve ambiguity.'
                                    if len(locations)>1 else 'Observed location; original author sampling rule unresolved.')
                    if marked:
                        assert math_correct,(qid,value,expected)
                        recipe=dict(kind='correct',expression='ad - bc' if qid in DETERMINANTS else
                            'b / sqrt(b**2 - n**2)' if qid in TRIG else 'A[i-1][j-1]',
                            parameters={k:str(v) for k,v in params.items()},generalization='Computed from prompt components.')
                    choices.append(dict(answer_entity=a[':db/id'],answer_id=a.get(':answer/id'),
                        source_field=f[':answer-field/key'],source_value=value,source_type=a[':answer/type'][':db/ident'],
                        source_marked_correct=marked if ':answer-field/correct' in f else None,
                        mathematically_correct=bool(math_correct),bank_profile=profile,recipe=recipe,
                        candidate_prompt_based_recipes=matches,
                        recipe_intent='unresolved' if not marked and not math_correct else 'correct computation',
                        complete_value_retained=True))
                assert sum(c['mathematically_correct'] for c in choices)==1,qid
                fields.append(dict(key=f[':answer-field/key'],type=field_type,
                    correct_reference_present=':answer-field/correct' in f,bank_profile=profile,choices=choices))
            for attr in (':question/problem',':question/worked-solution'):
                for path in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',q.get(attr,'')):
                    asset=Path('/media/jake/SSD/EDB/math')/path
                    assert asset.is_file(),asset
                    shutil.copyfile(asset,asset_folder/asset.name)
                    assets.append(dict(question=qid,context='practice',role=attr.split('/')[-1],source_path=str(asset),
                        local_path='assets/'+asset.name,sha256=hashlib.sha256(asset.read_bytes()).hexdigest(),
                        inspection='Visually inspected in 12-asset contact sheet; first-quadrant unit circle and angle.'))
            cases.append(dict(kp_entity=kp[':db/id'],source_question=qid,question_entity=q[':db/id'],
                difficulty=q.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1],
                template=template,features=features,fields=fields,
                problem=q[':question/problem'],worked_solution=q.get(':question/worked-solution'),
                worked_solution_status='present' if ':question/worked-solution' in q else 'missing in database',
                missing_attributes=[v for v in ('difficulty','worked-solution') if ':question/'+v not in q]
                    +(['correct answer reference'] if any(not f['correct_reference_present'] for f in fields) else [])))
            def image_paths(text):
                return re.sub(r'!\[([^\]]*)\]\((images/[^)]+)\)',lambda m:
                    '!['+m[1]+'](../assets/'+Path(m[2]).name+')',text)
            rendered += [f'## {qid} — {cases[-1]["difficulty"]}', '',
                '**Specific components:** '+json.dumps(features,ensure_ascii=False), '',
                '**Template:** `'+template+'`', '', image_paths(q[':question/problem']), '',
                '| Field | Type | Bank profile | Source answer entity | Original value | Source correct | Value recipe |',
                '|---|---|---|---:|---|---|---|']
            for field in fields:
                for choice in field['choices']:
                    recipe=choice['recipe']
                    value=choice['source_value']
                    value='$'+value+'$' if choice['source_type']==':answer.type/math' else value
                    flag='unrecorded' if choice['source_marked_correct'] is None else str(choice['source_marked_correct'])
                    rendered.append(f"| {field['key']} | {field['type']} | {field['bank_profile'] or 'none'} | "
                        f"{choice['answer_entity']} | {value} | {flag} | `{recipe['expression']}`; "
                        +json.dumps(recipe['parameters'],ensure_ascii=False)+' |')
            rendered += ['', '**Original worked solution:**', '',
                image_paths(q.get(':question/worked-solution','**Missing in database. No source solution was invented.**')), '']
        (folder/'source-questions.md').write_text('\n'.join(rendered))
        write(folder/'source-cases.json',[c for c in cases if c['kp_entity']==kp[':db/id']])
        write(folder/'absence-scores.json',scores[kp[':db/id']])
    write(HERE/'source-cases.json',cases)
    write(HERE/'plot-assets.json',assets)
    options=[choice for c in cases for f in c['fields'] for choice in f['choices']]
    verification=dict(database=source['database'],practice_questions=len(cases),
        rated_questions=sum(c['difficulty']!='unrated' for c in cases),
        source_answers=len(options),retained_complete_values=sum(c['complete_value_retained'] for c in options),
        rated_marked_correct_verified=sum(c['source_marked_correct'] is True for c in options),
        incomplete_questions=[c['source_question'] for c in cases if c['missing_attributes']],
        field_type_counts=dict(Counter(f['type'] for c in cases for f in c['fields'])),
        source_bank_profiles=sum(f['bank_profile'] is not None for c in cases for f in c['fields']),
        source_asset_occurrences=sum(a['context']=='practice' for a in assets),
        canonical_asset_occurrences=sum(a['context']=='canonical' for a in assets),all_source_assets_present=True,
        generator_fidelity_claimed=False,engine_grading_tested=False,
        recipes_note='Observed expression patterns and candidate prompt-based matches are retained. '
            'Distractor causes and extrapolation remain unresolved where not established by source evidence.')
    write(HERE/'verification.json',verification)
    print(json.dumps(verification,indent=2))


if __name__=='__main__':
    main()
