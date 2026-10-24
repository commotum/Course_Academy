"""Enforce the reviewed topic478 contract on the actual delivered batch."""
from collections import defaultdict
import re

KPS = {17592186068916, 17592186068917, 17592186068918}
FAMILIES = {
    17592186068916: {level: {'sec2','csc2','sec_tan','csc_cot'} for level in ('easy','moderate','hard')},
    17592186068917: {
        'easy': {'sin','cos','sec2','csc2','sec_tan','csc_cot'},
        'moderate': {'sin','cos','sec2','csc2','sec_tan','csc_cot','sqrt_sin','sqrt_cos'},
        'hard': {'sin','cos','sec2','csc2','sec_tan','csc_cot','reciprocal_sec2','reciprocal_sin'}},
    17592186068918: {
        'easy': {'sin','cos','shift_sin','shift_cos'},
        'moderate': {'sin2','cos2','cos3','tan','sec','csc','cot2','tan2'},
        'hard': {'sin2','cos3','sec','csc','cot2','tan2','nested_tan','rearranged'}},
}


def validate_delivery_batch(records, kp_id):
    if int(kp_id) not in KPS:
        return
    groups = defaultdict(list)
    shapes = set()
    for record in records:
        q, meta = record['question'], record.get('generation', {})
        if meta.get('batch_contract') != 'trig-substitution-v3':
            raise ValueError('Trig substitution requires the reviewed structural batch contract')
        band = str(q[':question/difficulty']).rsplit('/', 1)[-1]
        if meta.get('family') not in FAMILIES[int(kp_id)].get(band, set()):
            raise ValueError('Unsupported trig substitution family or difficulty')
        fields = q[':question/answer-fields']
        if len(fields) != 1 or str(fields[0][':answer-field/type']) != ':answer-field.type/blank':
            raise ValueError('Reviewed trig substitution uses one exact-entry field')
        field = fields[0]
        if len(field[':answer-field/choices']) != 1:
            raise ValueError('Normalize accepted aliases; a canonical answer must not be duplicated')
        key = field[':answer-field/choices'][0][':answer/value']
        blocks = re.findall(r'\$\$\s*(.*?)\s*\$\$', q[':question/worked-solution'], re.S)
        external_c = bool(re.search(r'\{\{field-1\}\}\s*\$\+C\$',q[':question/problem']))
        expected_final = key + ('+C' if external_c else '')
        if not blocks or blocks[-1].strip().rstrip('.') != expected_final:
            raise ValueError('Worked solution must visibly reach the exact displayed canonical answer')
        m = meta['model']
        shape = (meta['family'],m['substitution'],m['lower'],m['upper'])
        if shape in shapes:
            raise ValueError('Amplitude-only repetition in delivered trig substitution practice')
        shapes.add(shape)
        if m['lower'] is not None and key.strip() in {'0','0.0'}:
            raise ValueError('Zero-result definite questions may not pad this pool')
        groups[band].append(record)
    for band, rows in groups.items():
        need = min(len(rows),len(FAMILIES[int(kp_id)][band]))
        if len({r['generation']['family'] for r in rows}) < need:
            raise ValueError('Delivered trig substitution batch lost structural family coverage')
