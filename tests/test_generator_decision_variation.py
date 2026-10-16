"""Adversarial controls for the review mandate, not an automated validity oracle."""
from collections import Counter, defaultdict
import importlib.util
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "decision_variation", ROOT / "generate/pipeline/fixtures/decision_variation.py")
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)


def question(item):
    return item["question"]


def key(item):
    field = question(item)[":question/answer-fields"][0]
    answer_id = field[":answer-field/correct"][1]
    return next(answer[":answer/value"] for answer in field[":answer-field/choices"]
                if answer[":answer/id"] == answer_id)


def matrices(item):
    # Parse what learners actually see; never inspect generation parameters.
    return {label: [[int(cell) for cell in row.split("&")] for row in raw.split(r"\\")]
            for label, raw in re.findall(r"([A-Z])=\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}",
                                         question(item)[":question/problem"])}


def template(item):
    return re.search(r"Collection (I+)\.", question(item)[":question/problem"])[1]


def selection(item):
    return frozenset(re.findall("[FHM]", key(item)))


def cue_accuracy(training, held_out, cue, response):
    """Fit only a cue-to-response lookup and measure held-out exact accuracy.

    This is diagnostic evidence, deliberately not a pass/fail validity rule.
    Whether a cue bypasses the intended skill requires an independent objective.
    """
    counts = defaultdict(Counter)
    for item in training:
        counts[cue(item)][response(item)] += 1
    predictions = {signature: values.most_common(1)[0][0] for signature, values in counts.items()}
    return sum(predictions.get(cue(item)) == response(item) for item in held_out) / len(held_out)


class DecisionVariationControls(unittest.TestCase):
    def assert_distribution_correct(self, items):
        for item in items:
            displayed = matrices(item)
            prompt = question(item)[":question/problem"]
            scale, left, right, first_coefficient, first, second_coefficient, second = re.search(
                r"evaluate \$(\d+)\(([ABC])\+([ABC])\)-(\d+)([ABC])-(\d+)([ABC])\$", prompt).groups()
            # Independently evaluate the emitted expression entry by entry.
            result = [[int(scale) * (displayed[left][r][c] + displayed[right][r][c])
                       - int(first_coefficient) * displayed[first][r][c]
                       - int(second_coefficient) * displayed[second][r][c]
                       for c in range(2)] for r in range(2)]
            chosen = key(item).split("=", 1)[0]
            self.assertEqual(result, displayed[chosen])
            self.assertIn("=" + key(item), question(item)[":question/worked-solution"])

    def assert_classification_correct(self, items):
        for item in items:
            displayed = matrices(item)
            expected = frozenset(label for label, value in displayed.items()
                                 if value[0][1] == value[1][0] == 0)
            self.assertEqual(selection(item), expected)
            solution = question(item)[":question/worked-solution"]
            self.assertIn(f"Select ${key(item)}$", solution)
            for label, value in displayed.items():
                self.assertIn(f"{label}: off-diagonal entries are {value[0][1]} and {value[1][0]}.", solution)

    def test_different_numeric_answers_and_shuffled_options_hide_fixed_survivor(self):
        broken = [controls.distributivity(seed) for seed in range(120)]
        repaired = [controls.distributivity(seed, repaired=True) for seed in range(120)]
        for items in (broken, repaired):
            self.assert_distribution_correct(items)
            self.assertGreater(len({key(item) for item in items}), 100)
            self.assertEqual(len({question(item)[":question/problem"] for item in items}), 120)
            self.assertGreater(len({tuple(answer[":answer/value"][0]
                                         for answer in question(item)[":question/answer-fields"][0][":answer-field/choices"])
                                    for item in items}), 1)
        response = lambda item: key(item)[0]
        self.assertEqual(cue_accuracy(broken[:60], broken[60:], lambda item: "same family", response), 1)
        self.assertAlmostEqual(cue_accuracy(repaired[:60], repaired[60:], lambda item: "same family", response), 1 / 3)
        self.assertEqual({response(item) for item in repaired}, set("ABC"))
        first_label = lambda item: re.search(r"evaluate \$\d+\(([ABC])", question(item)[":question/problem"])[1]
        self.assertEqual(sum(first_label(item) == response(item) for item in broken), 120)
        self.assertEqual(sum(first_label(item) == response(item) for item in repaired), 60)

    def test_globally_balanced_labels_hide_per_template_fixed_subsets(self):
        broken = [controls.classification(seed) for seed in range(120)]
        repaired = [controls.classification(seed, repaired=True) for seed in range(120)]
        for items in (broken, repaired):
            self.assert_classification_correct(items)
            self.assertEqual(Counter(label for item in items for label in selection(item)),
                             Counter({"F": 60, "H": 60, "M": 60}))
        self.assertEqual(cue_accuracy(broken[:60], broken[60:], template, selection), 1)
        self.assertAlmostEqual(cue_accuracy(repaired[:60], repaired[60:], template, selection), 1 / 6)
        for signature in ("I", "II"):
            self.assertEqual(len({selection(item) for item in repaired if template(item) == signature}), 6)

    def test_counterfactuals_change_relevant_evidence_key_and_solution_together(self):
        data = {"A": [[1, 2], [3, 4]], "B": [[5, 6], [7, 8]], "C": [[9, 10], [11, 12]]}
        before = controls.distributivity(0, repaired=True, matrices=data, survivor="A")
        after = controls.distributivity(0, repaired=True, matrices=data, survivor="B")
        self.assertEqual(matrices(before), matrices(after))
        self.assertNotEqual(key(before), key(after))
        self.assertNotEqual(question(before)[":question/worked-solution"], question(after)[":question/worked-solution"])
        self.assert_distribution_correct([before, after])
        # C is absent from the first expression, so changing C cannot change its answer.
        irrelevant = controls.distributivity(0, matrices={**data, "C": [[90, 80], [70, 60]]}, survivor="A")
        self.assertEqual(key(before), key(irrelevant))
        self.assert_distribution_correct([irrelevant])

        data = {"F": [[1, 0], [0, 2]], "H": [[3, 4], [0, 5]], "M": [[6, 0], [0, 7]]}
        before = controls.classification(matrices=data, collection="I")
        after = controls.classification(matrices={**data, "H": [[3, 0], [0, 5]]}, collection="I")
        irrelevant = controls.classification(matrices={**data, "H": [[30, 4], [0, 50]]}, collection="I")
        self.assertEqual(selection(after) - selection(before), {"H"})
        self.assertNotEqual(question(before)[":question/worked-solution"], question(after)[":question/worked-solution"])
        self.assertEqual(key(before), key(irrelevant))
        self.assert_classification_correct([before, after, irrelevant])

    def test_delivered_filter_and_coarse_dedup_can_erase_raw_role_coverage(self):
        raw = [controls.classification(seed, repaired=True) for seed in range(120)]
        # A hypothetical downstream case filter, followed by exact-text dedup.
        filtered = [item for item in raw if selection(item) == {"F"}]
        delivered = list({question(item)[":question/problem"]: item for item in filtered + filtered}.values())
        self.assertEqual(len(delivered), 20)
        self.assert_classification_correct(delivered)
        self.assertAlmostEqual(cue_accuracy(raw[:60], raw[60:], template, selection), 1 / 6)
        self.assertEqual(cue_accuracy(delivered[:10], delivered[10:], template, selection), 1)
        # A dedup key that collapses every numeric variant to its visible template
        # can independently retain only the first role assignment in each family.
        coarse = {}
        for item in raw:
            coarse.setdefault(template(item), item)
        self.assertEqual(len({selection(item) for item in coarse.values()}), 1)

    def test_intended_identity_is_not_rejected_for_having_an_invariant_answer(self):
        items = [controls.equal_row_identity(seed) for seed in range(60)]
        for item in items:
            prompt = question(item)[":question/problem"]
            self.assertIn("Use the equal-row determinant identity", prompt)
            raw = re.search(r"\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}", prompt)[1]
            (a, b), (c, d) = [[int(cell) for cell in row.split("&")] for row in raw.split(r"\\")]
            self.assertEqual(a * d - b * c, int(key(item)))
            self.assertEqual((a, b), (c, d))
        self.assertEqual(cue_accuracy(items[:30], items[30:], lambda item: "equal rows", key), 1)
        # A score of 1 is evidence to interpret against this narrow objective,
        # not proof of a defect or evidence of general determinant mastery.


if __name__ == "__main__":
    unittest.main()
