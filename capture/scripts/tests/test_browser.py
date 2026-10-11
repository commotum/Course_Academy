"""Saved MA source fragments plus offline action/recovery tests.

Question/history: reference/mathacademy/question-capture/14085116.
Lesson: reference/edb-math/imports/math-academy/newer-captures/source-evidence/topic-3178.html.
Assessment: reference/mathacademy/question-capture-workers/linear/14097922.
Multistep: reference/mathacademy/question-capture/14039183.
Diagnostic/queue regressions: scripts/question_capture/fixtures.
"""
import hashlib
import json
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace

from scripts.browser.adapter import EXTRACT, MathAcademyBrowser
from scripts.browser.assets import AssetCapture, image_extension, replace_markers
from scripts.browser.entry import enter, normalized_math, pick_choice, validated_keys, write_math
from scripts.browser.parsing import (activity_from_url, parse_history_metadata, parse_lesson_structure,
                                    parse_queue, parse_xp, question_identity)

FIXTURES = Path(__file__).parent / "fixtures"


class SourceParsingTests(unittest.TestCase):
    def test_queue_retains_source_details_and_start_link(self):
        rows = parse_queue((FIXTURES / "quiz-6-required-card.html").read_text())
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["kind"], "assessment")
        self.assertFalse(row["started"])
        self.assertTrue(row["url"].endswith("/start"))
        self.assertTrue(row["details"]["source_fields"])
        self.assertTrue(row["details"]["links"])

    def test_forced_diagnostic_is_started_without_guessing_question_id(self):
        row = activity_from_url("https://mathacademy.com/tasks/22/diagnostics/31")
        self.assertEqual(row["kind"], "diagnostic")
        self.assertTrue(row["started"])
        self.assertIsNone(question_identity("questionContainer", "Question 12", diagnostic=True))

    def test_history_uses_kp_source_link_and_observed_difficulty(self):
        [row] = parse_history_metadata((FIXTURES / "review-history-question.html").read_text())
        self.assertEqual(row["math_academy_id"], "q-1396")
        self.assertEqual(row["topic_id"], "245")
        self.assertEqual(row["knowledge_point_source_id"], 4341)
        self.assertEqual(row["difficulty"], "easy")
        self.assertEqual(row["grade"], "Correct")

    def test_lesson_content_and_placement_are_distinct(self):
        html = '<h1 id="topicName">Vectors</h1><div class="step" id="step-t8" stepid="51" steptype="tutorial" contentid="8"><span class="stepName">Start</span></div><div class="step" stepid="52" steptype="example" contentid="19"><span class="stepName">Example: Add</span></div>'
        record = parse_lesson_structure(html, 3)
        self.assertTrue(record["complete"])
        self.assertEqual([(s["math_academy_id"], s["content_id"]) for s in record["steps"]], [(51, 8), (52, 19)])
        self.assertEqual(record["steps"][1]["title"], "Add")

    def test_semantic_choice_survives_shuffle(self):
        field = {"key": "selection", "choices": [{"value": "B", "option": "a"}, {"value": "A", "option": "b"}]}
        self.assertEqual(pick_choice(field, {"value": "A", "option": "a"})["option"], "b")
        with self.assertRaises(ValueError):
            pick_choice(field, {"value": "absent", "option": "a"})

    def test_original_svg_bytes_are_saved_and_source_html_is_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            original = '<svg xmlns="http://www.w3.org/2000/svg"><circle r="4"/></svg>'
            item = {"problem": "![](@asset-0@)", "html": "@asset-0@", "assets": [{"index": 0, "tag": "svg", "html": original}]}
            captured = AssetCapture(SimpleNamespace()).collect(item, None, directory, "step")
            asset = captured["assets"][0]
            self.assertEqual(Path(asset["path"]).read_bytes(), original.encode())
            self.assertEqual(asset["sha256"], hashlib.sha256(original.encode()).hexdigest())
            self.assertEqual(captured["html"], "@asset-0@")
            self.assertIn(asset["path"], captured["problem"])

    def test_html_error_page_is_not_stored_as_an_image(self):
        with self.assertRaises(ValueError):
            image_extension(b"<html>Sign in</html>", "image/png")

    def test_xp_denominator_and_penalty_are_source_values(self):
        self.assertEqual(parse_xp("8 of 13 XP")["base_xp"], 13)
        self.assertEqual(parse_xp("-5 / 13")["earned_xp"], -5)

    def test_math_editor_notation_changes_do_not_change_scope(self):
        self.assertEqual(normalized_math("x/2"), normalized_math(r"\frac{x}{2}"))
        self.assertEqual(normalized_math("x^2"), normalized_math("x^{2}"))
        self.assertEqual(normalized_math(r"\left(x\right)"), normalized_math("(x)"))
        self.assertNotEqual(normalized_math("x/2y"), normalized_math(r"\frac{x}{2y}"))
        self.assertNotEqual(normalized_math("x+1/2"), normalized_math(r"\frac{x+1}{2}"))
        with self.assertRaises(ValueError):
            validated_keys([{"text": None, "key": "Enter"}])


class OfflineBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise unittest.SkipTest("Playwright is required for offline DOM tests")
        cls.pw = sync_playwright().start()
        try:
            cls.browser = cls.pw.chromium.launch(headless=True)
        except Exception:
            cls.pw.stop()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.pw.stop()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.directory = Path(self.temporary.name)
        self.context = self.browser.new_context()
        self.context.route("**/*", lambda route: route.abort())  # No live websites.
        self.page = self.context.new_page()
        config = SimpleNamespace(timeout_ms=1000, course_id="55", account="test")
        self.adapter = MathAcademyBrowser(config, threading.Event())
        self.adapter.page = self.page
        self.adapter.context = self.context
        self.adapter.directory = self.directory
        self.adapter.activity = {"task_id": "1", "kind": "review", "topic_id": "245", "details": {}}

    def tearDown(self):
        self.context.close()
        self.temporary.cleanup()

    def test_saved_radio_keeps_math_and_all_choices(self):
        self.page.set_content((FIXTURES / "q-1396-before.html").read_text())
        item = self.page.locator("#step-q1396").evaluate(EXTRACT)
        self.assertIn("a\\times b", item["problem"])
        self.assertEqual(len(item["fields"][0]["choices"]), 5)
        self.assertTrue(item["fields"][0]["choices_complete"])
        self.assertEqual(item["errors"], [])

    def test_saved_diagnostic_selects_are_not_lost_after_skip(self):
        counts = []
        for name in ("diagnostic-skipped-select-before.html", "diagnostic-skipped-select-after.html"):
            self.page.set_content((FIXTURES / name).read_text())
            scope = self.page.locator("#questionContainer")
            if not scope.count():
                scope = self.page.locator("body")
            item = scope.evaluate(EXTRACT)
            counts.append(len(item["fields"]))
            self.assertTrue(all(f["choices"] for f in item["fields"]))
        self.assertTrue(counts[0])
        self.assertEqual(counts[0], counts[1])

    def test_saved_lesson_preserves_tutorial_and_example_placement_ids(self):
        html = (FIXTURES / "lesson-3178-fragment.html").read_text()
        definition = parse_lesson_structure(html, 3178)
        self.assertEqual([(x["math_academy_id"], x["content_id"]) for x in definition["steps"]], [(657075, 7725), (657079, 12356)])
        self.page.set_content(html)
        tutorial = self.page.locator('div.step[stepid="657075"]').evaluate(EXTRACT)
        example = self.page.locator('div.step[stepid="657079"]').evaluate(EXTRACT)
        self.assertTrue(tutorial["problem"])
        self.assertTrue(example["problem"])
        self.assertTrue(example["worked_solution"])
        self.assertNotIn("Continue", tutorial["problem"])

    def test_saved_assessment_and_multistep_keep_field_structure(self):
        for filename, expected in [("assessment-105178-question.html", "q-105178"),
                                   ("multistep-128186-question.html", "q-128186")]:
            self.page.set_content((FIXTURES / filename).read_text())
            scope = self.page.locator('.question').first
            item = scope.evaluate(EXTRACT)
            self.assertEqual(question_identity(item["dom_id"]), expected)
            self.assertTrue(item["problem"])
            self.assertTrue(item["fields"])
        self.page.set_content((FIXTURES / "multistep-128186-context.html").read_text())
        context = self.page.locator('.step').evaluate(EXTRACT)
        self.assertIn("initial value problem", context["problem"])
        self.assertFalse(context["fields"])

    def test_graded_question_is_not_submitted_again(self):
        self.page.set_content('''<div class="step questionWidget" id="step-q1">
          <div class="questionWidget-text">What is 2+2?</div><input id="answer"/>
          <div class="questionWidget-result"></div>
          <button class="questionWidget-submitButton" onclick="window.submissions=(window.submissions||0)+1;this.parentNode.querySelector('.questionWidget-result').textContent='Correct';this.style.display='none';document.getElementById('continueButton-q1').style.display='block'">Submit</button>
          <button id="continueButton-q1" style="display:none">Continue</button></div>''')
        before = self.adapter.observe(self.directory)
        self.assertFalse(before["accepted"])
        self.adapter.respond(before, [{"key": "field-1", "value": "4"}], self.directory)
        after = self.adapter.observe(self.directory)
        self.assertTrue(after["accepted"])
        self.adapter.respond(before, [{"key": "field-1", "value": "4"}], self.directory)
        self.assertEqual(self.page.evaluate("window.submissions"), 1)

    def test_unknown_submission_outcome_is_reloaded_before_any_retry(self):
        self.page.set_content('''<div class="step questionWidget" id="step-q1"><div class="questionWidget-text">What is 2+2?</div><input id="answer"/><button class="questionWidget-submitButton" onclick="window.submissions=(window.submissions||0)+1">Submit</button></div>''')
        observation = self.adapter.observe(self.directory)
        self.adapter.state["pending_action"] = {"key": observation["key"], "action": "submit"}
        self.adapter.state["restored"] = False
        reloads = []
        self.adapter._goto = lambda url: reloads.append(url)
        self.adapter.respond(observation, [{"key": "field-1", "value": "4"}], self.directory)
        self.assertEqual(len(reloads), 1)
        self.assertIsNone(self.page.evaluate("window.submissions"))
        self.assertTrue(self.adapter.state["restored"])

    def test_assessment_minutes_label_supplies_actual_timer_budget(self):
        self.page.set_content('<span id="timeRemaining">15 minutes remaining</span>')
        self.assertEqual(self.adapter._remaining(), 900)

    def test_assessment_entry_is_not_a_grade_and_whole_submit_is_separate(self):
        self.adapter.activity["kind"] = "assessment"
        self.page.set_content('''<div id="questions"><div class="question" id="question-4"><div class="questionText">First</div><input id="a"/></div><div class="question" id="question-5"><div class="questionText">Second</div><input id="b"/></div></div>
          <button id="submitTestButton" onclick="document.getElementById('confirmationDialog').style.display='block'">Submit test</button>
          <div id="confirmationDialog" style="display:none">Submit this test?<button onclick="document.getElementById('finalScreen').style.display='block'">Yes</button></div>
          <div id="finalScreen" style="display:none">8 of 13 XP</div>''')
        first = self.adapter.observe(self.directory)
        self.assertFalse(first["accepted"])
        self.adapter.respond(first, [{"key": "field-1", "value": "4"}], self.directory)
        second = self.adapter.observe(self.directory)
        self.assertEqual(second["question"]["math_academy_id"], "q-5")
        self.adapter.respond(second, [{"key": "field-1", "value": "5"}], self.directory)
        submit = self.adapter.observe(self.directory)
        self.assertEqual(submit["action"], "submit_assessment")
        self.adapter.respond(submit, {"action": "submit_assessment"}, self.directory)
        done = self.adapter.observe(self.directory)
        self.assertEqual(done["kind"], "complete")
        self.assertEqual(done["completion"]["base_xp"], 13)

    def test_queue_expands_each_card_even_when_previous_one_collapses(self):
        self.page.set_content('''<div id="incompleteTasks">
          <div id="task-1" class="taskUnlocked" progress="0"><span class="taskTypeUnlocked">Lesson</span><span id="taskName-1" onclick="expand(1)">One</span><div class="taskDetails" style="display:none"></div></div>
          <div id="task-2" class="taskUnlocked" progress="0.5"><span class="taskTypeUnlocked">Review</span><span id="taskName-2" onclick="expand(2)">Two</span><div class="taskDetails" style="display:none"></div></div></div>
          <script>function expand(id){document.querySelectorAll('.taskDetails').forEach(n=>n.style.display='none');let n=document.querySelector('#task-'+id+' .taskDetails');n.style.display='block';n.innerHTML='<a class="taskStartButton" href="/tasks/'+id+'/topics/245/'+(id===1?'lesson':'review')+'">Start</a>';}</script>''')
        self.adapter._goto = lambda *args: None
        queue = self.adapter.queue(self.directory)
        self.assertEqual(len(queue), 2)
        self.assertTrue(all(item["url"] for item in queue))
        self.assertTrue(queue[1]["started"])
        self.assertTrue((self.directory / "queue-card-1.html").exists())

    def test_multistep_shared_context_is_not_prepended_to_local_problem(self):
        self.adapter.activity["kind"] = "multistep"
        self.page.set_content('''<div id="steps"><div class="step" id="step-1"><p>A shared setup.</p></div><div class="step" id="step-2"><div class="question" id="question-7"><div class="questionText">Find x.</div><input id="x"/></div><button class="submitButton" id="submitButton-2">Submit</button></div></div>''')
        item = self.adapter.observe(self.directory)
        self.assertEqual(item["question"]["problem"], "Find x.")
        self.assertEqual(item["shared_context"], "A shared setup.")
        self.assertEqual(item["part_order"][0]["math_academy_id"], "q-7")

    def test_late_postprocessing_never_borrows_newer_activity_xp(self):
        self.adapter.state = {"task_id": "2", "completion": {"earned_xp": 99, "base_xp": 100}}
        (self.directory / "browser-state.json").write_text(json.dumps({"task_id": "1", "completion": {"earned_xp": 3, "base_xp": 5}}))
        def dashboard(url, page=None):
            page.set_content('<div id="completedTasks"></div>')
        self.adapter._goto = dashboard
        result = self.adapter.postprocess(self.adapter.activity, self.directory)
        self.assertEqual(result["completion"]["earned_xp"], 3)
        self.assertEqual(self.adapter.state["completion"], {"earned_xp": 99, "base_xp": 100})

    def test_unknown_page_agent_can_choose_a_current_idless_continue(self):
        self.page.set_content('''<div><button onclick="this.remove();document.getElementById('finalScreen').style.display='block';window.recoveryClicks=(window.recoveryClicks||0)+1">Continue</button></div><div id="finalScreen" style="display:none">Done</div>''')
        observation = self.adapter.observe(self.directory)
        [button] = observation["buttons"]
        self.assertTrue(button["selector"])
        decision = {"action": "advance", "button_selector": button["selector"], "button_text": button["text"]}
        self.adapter.recover(observation, decision, self.directory)
        self.adapter.recover(observation, decision, self.directory)
        self.assertEqual(self.page.evaluate("window.recoveryClicks"), 1)
        self.assertEqual(self.adapter.observe(self.directory)["kind"], "complete")

    def test_unknown_page_recovery_rejects_unobserved_or_abandon_controls(self):
        self.page.set_content('<button id="continue">Continue</button><button id="quit">Quit</button>')
        observation = self.adapter.observe(self.directory)
        with self.assertRaises(ValueError):
            self.adapter.recover(observation, {"action": "advance", "button_selector": "#quit", "button_text": "Quit"}, self.directory)
        with self.assertRaises(ValueError):
            self.adapter.recover(observation, {"action": "advance", "button_selector": "#unseen", "button_text": "Continue"}, self.directory)

    def test_math_editor_uses_validated_keys_when_write_cannot_enter_value(self):
        self.page.set_content('''<div class="matheditor-wrapper-answer"><span class="mq-editable-field"><textarea></textarea></span></div><script>
          window.calls=[];window.output='';window.MathQuill=()=>({focus(){},select(){},write(){throw Error('unsupported direct write')},keystroke(key){calls.push(['key',key]);if(key==='Backspace')output='';},cmd(value){calls.push(['command',value]);output+=value;},typedText(value){calls.push(['text',value]);output+=value;},latex(){return output;}});
        </script>''')
        observed = write_math(self.page.locator('.matheditor-wrapper-answer'), r"\pi", [{"text": r"\pi", "key": None}])
        self.assertEqual(observed, r"\pi")
        self.assertIn(["command", r"\pi"], self.page.evaluate("window.calls"))
        self.assertNotIn(["text", r"\pi"], self.page.evaluate("window.calls"))

    def test_image_response_cache_is_scoped_to_the_current_activity(self):
        self.adapter._goto = lambda *args: None
        activity = {**self.adapter.activity, "url": "https://mathacademy.com/tasks/1/topics/245/review"}
        sentinel = object()
        self.adapter.image_responses["current-image"] = sentinel
        self.adapter.open(activity, self.directory, {})
        self.assertIs(self.adapter.image_responses["current-image"], sentinel)
        following = {**activity, "task_id": "2", "url": "https://mathacademy.com/tasks/2/topics/245/review"}
        self.adapter.open(following, self.directory / "next", {})
        self.assertEqual(self.adapter.image_responses, {})

    def test_custom_dropdown_can_reparent_its_menu_to_body(self):
        self.page.set_content('''<div id="question"><div class="selectList" id="select"><div class="selectListFrame" style="padding:8px;border:1px solid black" onclick="let m=document.querySelector('.selectListOptions');document.body.appendChild(m);m.style.display='block';">Choose</div><div class="selectListOptions" style="display:none"><div class="selectListOption" id="one" onclick="document.querySelector('.selectListFrame').textContent=this.textContent;this.parentNode.style.display='none'">One</div></div></div></div>''')
        field = {"key": "field-1", "type": "select", "tag": "custom-select", "dom_id": "select", "choices": [{"value": "One", "type": "text", "option": "0", "dom_id": "one"}]}
        response = enter(self.page.locator('#question'), field, {"value": "One"})
        self.assertEqual(response["value"], "One")
        self.assertEqual(self.page.locator('.selectListFrame').inner_text(), "One")


if __name__ == "__main__":
    unittest.main()
