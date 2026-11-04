import copy
import json
from pathlib import Path
import unittest
import uuid

from generate.trig_question_pedagogy import KPS, validate_delivery_batch
from scripts.generator_publish import prepare_records

ROOT = Path(__file__).resolve().parents[1]


def record(prompt, kp=17592186059665, choices=('1', '2')):
    answer_ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, 'trig-guard-answer:'+value)) for value in choices]
    return {'knowledge_point': kp, 'question': {
        ':question/id': str(uuid.uuid4()), ':question/difficulty': ':question.difficulty/easy',
        ':question/problem': prompt,
        ':question/worked-solution': 'Use the identity in the solution: $1\\cdot\\cos x=\\cos x$.',
        ':question/answer-fields': [{':answer-field/id': str(uuid.uuid4()),
            ':answer-field/key': 'selection', ':answer-field/type': ':answer-field.type/radio',
            ':answer-field/choices': [{':answer/id': aid, ':answer/type': ':answer.type/math', ':answer/value': value}
                                    for aid, value in zip(answer_ids, choices)],
            ':answer-field/correct': [':answer/id', answer_ids[0]]}]}}


class TrigQuestionPedagogyTests(unittest.TestCase):
    def rejects(self, kp, prompt, message):
        with self.assertRaisesRegex(ValueError, message):
            validate_delivery_batch([record(prompt, kp)], kp)

    def test_actual_audited_method_reminders_are_rejected(self):
        # Historical 17592186714557 and 17592186696011, before repair.
        prompts = [
            (17592186059665, r'Simplify $\cos(t-\pi)$ in terms of $\sin t$ or $\cos t$.'
             '\nUse the difference formula\n'
             r'$$\cos(u-v)=\cos u\cos v+\sin u\sin v$$'
             r' and the exact values $\cos\pi=-1$ and $\sin\pi=0$.'),
            (17592186059672, 'Without using a calculator, find the exact value of '
             r'$4\sin(\pi/16)\cos(\pi/16)\cos(\pi/8)$.'
             r' Use $2\sin x\cos x=\sin(2x)$, first with $x=\pi/16$ and then with $x=\pi/8$.'),
            (17592186059820, r'Express $\sin(x+\pi/2)$ in terms of $\sin x$ and $\cos x$.'
             '\nUse the sum formula\n'
             r'$$\sin(u+v)=\sin u\cos v+\cos u\sin v$$'),
            (17592186059671, r'Express $6\sin(17^\circ)\cos(17^\circ)$ using the sine of twice the angle.'),
        ]
        for kp, prompt in prompts:
            with self.subTest(kp=kp): self.rejects(kp, prompt, 'formula|equality')

    def test_source_supported_angle_split_hints_are_preserved(self):
        for kp, fn in [(17592186059666, 'cos'), (17592186059663, 'sin')]:
            prompt = 'Find the exact value of $\\'+fn+r'(75^\circ)$.'
            prompt += '\n*Hint: Use the fact that*\n$$75^\\circ=30^\\circ+45^\\circ.$$'
            validate_delivery_batch([record(prompt, kp)], kp)

    def test_literal_unit_products_rejected_but_entry_one_and_solution_steps_allowed(self):
        kp = 17592186059671
        for expr in [r'1\sin(17^\circ)\cos(17^\circ)', r'{1}\cdot\sin(17^\circ)',
                     r'\sin(17^\circ)\cdot1', r'11\sin(17^\circ)+1\cos(17^\circ)']:
            with self.subTest(expr=expr): self.rejects(kp, 'Express $'+expr+'$.', 'unit multiplication')
        prompt = r'Express $2\sin(17^\circ)\cos(17^\circ)$ as a single ratio.'
        validate_delivery_batch([record(prompt, kp, ('1', '-1', '11'))], kp)
        with self.assertRaisesRegex(ValueError, 'unit multiplication'):
            validate_delivery_batch([record(prompt, kp, (r'1\sin(34^\circ)',))], kp)
        validate_delivery_batch([record(r'Express $11\sin(17^\circ)\cos(17^\circ)$.', kp)], kp)
        validate_delivery_batch([record(r'Express $\cos(1)\sin(x)$.', kp)], kp)
        validate_delivery_batch([record(r'Express $\cos 1\sin x$.', kp)], kp)
        # Genuine constant 1 in an alternative form is not a coefficient 1.
        validate_delivery_batch([record(r'Express $1-2\sin^2(17^\circ)$.', 17592186087670)], 17592186087670)

    def test_actual_zero_full_turn_and_weighted_shift_wrappers_are_rejected(self):
        # Original audit sample moderate-31/2 and generated 17592186715695.
        for kp, expr in [(17592186059820, r'\sin(x-2\pi)'),
                         (17592186059662, r'\sin(x-360^\circ)'),
                         (17592186059665, r'\cos(x+0)'),
                         (17592186059821, r'\cos(x-300^\circ)-2\cos(x+60^\circ)'),
                         (17592186059662, r'2\sin(x+25^\circ)+\sin(x-35^\circ)')]:
            with self.subTest(expr=expr): self.rejects(kp, 'Express $'+expr+'$.', 'shift|wrapper')
        # A source-supported response frame may repeat the same single target.
        prompt = r'Express $\sin(x+180^\circ)$ in terms of $\sin x$ or $\cos x$.'
        prompt += '\n'+r'$\sin(x+180^\circ)=$ {{field-1}}'
        validate_delivery_batch([record(prompt, 17592186059662)], 17592186059662)
        validate_delivery_batch([record(r'Express $\cos(x+\frac{5\pi}{3})$.')], 17592186059665)

    def test_actual_invented_quartics_rejected_and_genuine_exact_square_allowed(self):
        cases = [
            (17592186087669, r'2\cos^4(19^\circ)-2\sin^4(19^\circ)'),  # 17592186698882
            (17592186087670, r'8\cos^4(18^\circ)-8\cos^2(18^\circ)+1'),  # 17592186698910
            (17592186059671, r'-3\sin^3(\frac{2\pi}{11})\cos(\frac{2\pi}{11})'
             r'-3\sin(\frac{2\pi}{11})\cos^3(\frac{2\pi}{11})'),  # old hard-7/0
        ]
        for kp, expr in cases:
            with self.subTest(kp=kp): self.rejects(kp, 'Express $'+expr+'$.', 'quartic')
        # Imported 17592186292878 really does ask this expanded perfect square.
        expr = r'\cos^4(15^\circ)-2\cos^2(15^\circ)\sin^2(15^\circ)+\sin^4(15^\circ)'
        validate_delivery_batch([record('Find the exact value of $'+expr+'$.', 17592186087671)], 17592186087671)
        # A binomial square has independent source support in the sine products KP.
        validate_delivery_batch([record(r'Simplify $(\sin(\pi/6)+\cos(\pi/6))^2$.', 17592186059671)], 17592186059671)

    def test_original_standard_angle_bypasses_rejected_but_doubled_special_angles_allowed(self):
        for kp in (17592186087669, 17592186087670, 17592186087671):
            for angle in (r'45^\circ', r'135^\circ', r'\pi', r'\frac{5\pi}{3}'):
                with self.subTest(kp=kp, angle=angle):
                    self.rejects(kp, r'Express $\cos^2('+angle+r')-\sin^2('+angle+')$.', 'standard-angle')
            validate_delivery_batch([record(r'Express $\cos^2(15^\circ)-\sin^2(15^\circ)$.', kp)], kp)

    def test_old_exact_cosine_reverse_product_task_is_rejected(self):
        # Generated 17592186715337 changed a forward exact-value task into synthesis.
        self.rejects(17592186059666,
                     r'Find the exact value of $\cos(-345^\circ)\cos(60^\circ)-\sin(-345^\circ)\sin(60^\circ)$.',
                     'reverse product')

    def test_all_thirteen_kps_and_unrelated_scope(self):
        for kp in KPS:
            with self.subTest(kp=kp):
                self.rejects(kp, r'Find $\sin(17^\circ)$. Recall the double-angle identity.', 'formula')
        validate_delivery_batch([{'question': {}}], 101)

    def test_publication_prepare_records_rejects_before_any_database_operation(self):
        kp, kp_uuid = 17592186087669, '5ec37c5e-8a40-58a7-8af3-4457cd5da43f'
        bad = record(r'Express $2\cos^4(19^\circ)-2\sin^4(19^\circ)$.', kp)
        with self.assertRaisesRegex(ValueError, 'quartic'):
            prepare_records([bad], kp, kp_uuid, set(), '/tmp', '/tmp',
                            localizer=lambda r, *_: copy.deepcopy(r))
        good = record(r'Express $2\cos^2(19^\circ)-2\sin^2(19^\circ)$.', kp)
        accepted, duplicates = prepare_records([good], kp, kp_uuid, set(), '/tmp', '/tmp',
                                               localizer=lambda r, *_: copy.deepcopy(r))
        self.assertEqual((len(accepted), duplicates), (1, 0))

    def test_final_generated_repair_batches_when_present(self):
        base = ROOT/'generate/repairs/2026-11-04-four-trig-lessons'
        if not base.exists(): self.skipTest('Repair evidence is not present in this checkout')
        covered, bands = set(), set()
        for path in base.rglob('*.json'):
            if path.parent.name not in ('evidence', 'validation') or not path.name.startswith(('easy-', 'moderate-', 'hard-')):
                continue
            records = json.loads(path.read_text())
            if not isinstance(records, list) or not records or 'question' not in records[0]: continue
            kp = records[0].get('knowledge_point')
            kp = kp.get('db_id') if isinstance(kp, dict) else kp
            if kp not in KPS: continue
            with self.subTest(path=str(path)):
                validate_delivery_batch(records, kp)
            covered.add(kp)
            for r in records:
                band = r['question'][':question/difficulty']
                if isinstance(band, dict): band = band[':db/ident']
                bands.add((kp, band.rsplit('/', 1)[-1]))
        self.assertEqual(covered, KPS)
        self.assertEqual(bands, {(kp, band) for kp in KPS for band in ('easy', 'moderate', 'hard')})


if __name__ == '__main__': unittest.main()
