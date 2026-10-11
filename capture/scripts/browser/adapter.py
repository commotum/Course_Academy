"""Sequential UI actions, durable action intents, and authenticated source reads.

Browser failures propagate to the activity's retry loop. This module never
changes a pinned task, answers mathematics, defers content, or writes EDB.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

from ..runtime import check_stop
from ..storage import atomic_json, atomic_text, read_json
from .assets import AssetCapture
from .entry import by_id, enter
from .parsing import (BASE, LEARN, activity_from_url, parse_dashboard, parse_history_metadata,
                      parse_lesson_structure, parse_progress, parse_queue, parse_xp, question_identity)

EXTRACT = (Path(__file__).parent / "extract.js").read_text()
VIEW = (Path(__file__).parent / "view.js").read_text()


class BrowserUnavailable(RuntimeError):
    """Retry this same activity after reconnecting or rereading its server state."""


class SourceUnavailable(BrowserUnavailable):
    """The source explicitly says a completed activity's content no longer exists."""


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:20]


class MathAcademyBrowser:
    def __init__(self, config, stop_event):
        self.config, self.stop_event = config, stop_event
        self.playwright = self.browser = self.context = self.page = None
        self.image_responses = {}
        self.activity = None
        self.directory = None
        self.state = {}
        self.assets = AssetCapture(self)

    def __enter__(self):
        from playwright.sync_api import sync_playwright
        check_stop(self.stop_event)
        self.playwright = sync_playwright().start()
        if self.config.browser_cdp_url:
            self.browser = self.playwright.chromium.connect_over_cdp(self.config.browser_cdp_url)
            self.context = self.browser.contexts[0]
        else:
            self.config.profile.mkdir(parents=True, exist_ok=True)
            self.context = self.playwright.chromium.launch_persistent_context(
                str(self.config.profile), headless=self.config.headless,
                viewport={"width": 1440, "height": 1000}, accept_downloads=False)
        self.context.set_default_timeout(self.config.timeout_ms)
        self.context.on("response", self._response)
        self.page = next((p for p in self.context.pages if "mathacademy.com" in p.url), None) or self.context.new_page()
        return self

    def __exit__(self, *args):
        try:
            # A connected browser belongs to its caller; do not close its tabs.
            if self.context and not self.config.browser_cdp_url:
                self.context.close()
        finally:
            if self.playwright:
                self.playwright.stop()
            self.playwright = self.context = self.browser = self.page = None

    def restart(self):
        activity, directory = self.activity, self.directory
        try:
            self.__exit__(None, None, None)
        except Exception:
            pass
        self.__enter__()
        if activity and directory:
            self.open(activity, directory, {})

    def _response(self, response):
        if response.ok and response.request.resource_type == "image":
            self.image_responses[response.url] = response

    def _check(self, page=None):
        check_stop(self.stop_event)
        page = page or self.page
        if page is None or page.is_closed():
            raise BrowserUnavailable("Browser page closed; reconnect to the pinned activity")
        if re.search(r"/(login|signin|session-expired)(?:/|\?|$)", page.url) or page.locator("input[type='password']").count():
            raise BrowserUnavailable("Account session unavailable; keep its activity checkpoint and retry authentication")
        if page.locator("iframe[src*='captcha'], #challenge-form, .cf-challenge").count():
            raise BrowserUnavailable("Account access challenge; keep checkpoint and retry when access returns")

    def _goto(self, url, page=None):
        page = page or self.page
        check_stop(self.stop_event)
        response = page.goto(url, wait_until="domcontentloaded", timeout=self.config.timeout_ms)
        if response and response.status in (404, 410):
            raise SourceUnavailable(f"Source page HTTP {response.status}: {url}")
        if response and response.status >= 400:
            raise BrowserUnavailable(f"Source page HTTP {response.status}: {url}")
        self._check(page)

    def _save(self):
        if self.directory:
            atomic_json(self.directory / "browser-state.json", self.state)

    def _evidence(self, page, directory, stem):
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        html = page.content()
        suffix = fingerprint({"url": page.url, "html": html})
        target = directory / f"{stem}-{suffix}.html"
        atomic_text(target, html)
        screenshot = target.with_suffix(".png")
        errors = []
        try:
            page.screenshot(path=str(screenshot), full_page=True, timeout=min(self.config.timeout_ms, 10000))
        except Exception as error:
            errors.append("Screenshot unavailable: " + str(error))
        return {"html_path": str(target.resolve()), "screenshot": str(screenshot.resolve()) if screenshot.exists() else None,
                "captured_at": time.time(), "source_url": page.url, "evidence_errors": errors}

    def queue(self, directory):
        self._goto(LEARN)
        active = activity_from_url(self.page.url)
        if active:
            active["course_id"] = self.config.course_id
            evidence = self._evidence(self.page, directory, "forced-active")
            active["details"].update(evidence)
            return [active]
        self.page.locator("#incompleteTasks").wait_for(state="attached")
        # Each card can close its siblings. Save each expanded card before the
        # next click, rather than assuming every card can stay open together.
        initial = parse_queue(self.page.content())
        records = []
        for initial_item in initial:
            self._check()
            item = initial_item
            card = by_id(self.page, item["details"]["card_id"])
            try:
                details = card.locator(".taskDetails, .testDetails").first
                if not details.count() or not details.is_visible():
                    heading = card.locator(".taskNameUnlocked, [id^='taskName-']").first
                    (heading if heading.count() else card).click()
                # Expansion asynchronously inserts its start link.
                card.locator("a.taskStartButton").first.wait_for(state="attached", timeout=min(self.config.timeout_ms, 5000))
                expanded = parse_queue("<div id='incompleteTasks'>" + card.evaluate("n=>n.outerHTML") + "</div>")
                if expanded:
                    item = expanded[0]
                    item["position"] = initial_item["position"]
                    item["course_id"] = initial_item["course_id"] or self.config.course_id
                atomic_text(Path(directory) / f"queue-card-{item['task_id']}.html", card.evaluate("n=>n.outerHTML"))
            except Exception as error:
                item["details"]["expansion_error"] = str(error)
            records.append(item)
        evidence = self._evidence(self.page, directory, "queue")
        atomic_json(Path(directory) / "queue.json", {"activities": records, **evidence})
        return records

    def open(self, activity, directory, checkpoint):
        previous_task = str((self.activity or {}).get("task_id", ""))
        if previous_task != str(activity["task_id"]):
            self.image_responses.clear()
        self.activity, self.directory = dict(activity), Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.state = read_json(self.directory / "browser-state.json", {}) or {}
        if self.state.get("task_id") not in (None, str(activity["task_id"])):
            raise ValueError("Browser checkpoint belongs to another activity")
        self.state["task_id"] = str(activity["task_id"])
        url = self.state.get("activity_url") or activity.get("url") or activity.get("href")
        if not url:
            queue = self.queue(self.directory / "recovered-queue")
            found = next((x for x in queue if str(x["task_id"]) == str(activity["task_id"])), None)
            url = found.get("url") if found else None
        if not url:
            raise BrowserUnavailable("Pinned task has no link yet; reread its queue")
        self._goto(urljoin(BASE, url))
        # Server state, not the previous click's success, decides what to do next.
        if self.state.get("assessment_filled"):
            self.state["assessment_filled_before_reload"] = self.state.pop("assessment_filled")
        self.state["restored"] = True
        self.state["activity_url"] = self.page.url
        self._save()

    def _read(self, scope, directory, label, prior=None):
        item = scope.evaluate(EXTRACT)
        item = self.assets.collect(item, scope, directory, label, prior=prior)
        key = fingerprint({"html": item.get("html"), "url": self.page.url})
        target = Path(directory) / "observations" / (re.sub(r"[^a-zA-Z0-9_-]", "-", label) + "-" + key)
        atomic_json(target.with_suffix(".json"), item)
        atomic_text(target.with_suffix(".html"), item.get("html", ""))
        screenshot = target.with_suffix(".png")
        try:
            scope.screenshot(path=str(screenshot), timeout=min(self.config.timeout_ms, 10000))
        except Exception as error:
            item.setdefault("errors", []).append("Screenshot unavailable: " + str(error))
        for field in item.get("fields", []):
            confirmed = field.get("source_correct")
            if confirmed and confirmed.get("value") is not None:
                field.update(correct_value=confirmed["value"], correct_origin="ma_answer",
                             correct_evidence={"kind": "ma_answer", "source_file": str(target.with_suffix(".html").resolve()),
                                               "value": confirmed["value"]})
        return {**item, "html_path": str(target.with_suffix(".html").resolve()),
                "screenshot": str(screenshot.resolve()) if screenshot.exists() else None,
                "source_url": self.page.url, "captured_at": time.time()}

    def _view(self):
        self._check()
        return self.page.evaluate(VIEW)

    def _remaining(self):
        value = self.page.locator("#timeRemaining, #timer, .testTimer, #testTimer, #remainingTime").first
        if not value.count():
            return None
        raw = value.inner_text().strip()
        match = re.search(r"(\d+):(\d{2})(?::(\d{2}))?", raw)
        if match:
            return int(match[1]) * (3600 if match[3] else 60) + int(match[2]) * (60 if match[3] else 1) + int(match[3] or 0)
        units = re.findall(r"(\d+)\s*(hours?|minutes?|seconds?)", raw, re.I)
        if units:
            return sum(int(amount) * (3600 if unit.lower().startswith("hour") else 60 if unit.lower().startswith("minute") else 1)
                       for amount, unit in units)
        return None

    def _assessment_view(self, view):
        filled = self.state.setdefault("assessment_filled", {})
        unanswered = [qid for qid in view["ids"] if qid not in filled]
        if not unanswered:
            return {"kind": "instructions", "key": "submit-assessment", "action": "submit_assessment", "selector": "body"}
        qid = unanswered[0]
        scope = by_id(self.page, qid)
        if not scope.is_visible():
            self.page.locator("#questionNavigator .questionButton").nth(view["ids"].index(qid)).click()
            scope.wait_for(state="visible")
        return {"kind": "question", "selector": "[id=" + json.dumps(qid) + "]", "key": qid,
                "sequence_position": view["ids"].index(qid) + 1, "accepted": False, "assessment": True}

    def observe(self, directory):
        view = self._view()
        if view["kind"] == "assessment":
            view = self._assessment_view(view)
        observation = {**view, "remaining_seconds": self._remaining(), "source_url": self.page.url, "observed_at": time.time()}
        if view["kind"] in ("question", "example", "tutorial"):
            scope = self.page.locator(view["selector"])
            item = self._read(scope, directory, view["key"])
            mid = question_identity(item.get("dom_id"), item.get("html", ""), self.activity.get("kind") == "diagnostic")
            item.update(math_academy_id=mid, topic_id=self.activity.get("topic_id"),
                        sequence_position=view.get("sequence_position"), source_step=view.get("source_step"))
            if view["kind"] == "example":
                self.state["current_example"] = {"math_academy_id": mid, "title": item.get("name")}
                self._save()
            elif view["kind"] == "question" and self.activity.get("kind") == "lesson":
                example = self.state.get("current_example", {})
                example_id = view.get("source_example_id") or example.get("math_academy_id")
                item.update(source_example_id=example_id,
                            knowledge_point=re.sub(r"^Example:\s*", "", view.get("knowledge_point") or example.get("title") or ""),
                            kp_id=example_id)
            # Staged proofs reveal additional fields before the question ends.
            if scope.locator(".proofSection, .questionWidget-healthFrame").count() and not observation.get("accepted"):
                active_keys = [f["key"] for f in item["fields"] if f.get("source_result") != "Correct"]
                observation["key"] += ":fields:" + ",".join(active_keys)
            observation.update(html_path=item["html_path"], screenshot=item["screenshot"],
                               grade=item.get("result") or view.get("grade"),
                               accepted=bool(item.get("result") or view.get("accepted")),
                               worked_solution=item.get("worked_solution", ""))
            observation["can_dont_know"] = scope.locator(".questionWidget-skipButton:visible").count() > 0
            observation["can_skip"] = observation["can_dont_know"]
            if item.get("proof_feedback") or any(f.get("source_result") for f in item["fields"]):
                self.state.pop("pending_action", None)
                self._save()
            if view["kind"] in ("question", "example"):
                observation["question"] = item
            else:
                observation["tutorial"] = {**item, "content": item["problem"], "title": item.get("name"),
                                           "math_academy_id": (view.get("source_step") or {}).get("content_id") or re.sub(r"^step-t", "", item.get("dom_id", ""))}
            if self.activity.get("kind") == "multistep":
                observation.update(self._multistep_context(directory))
                observation["shared_context"] = "\n\n".join(x["problem"] for x in observation["shared_contexts"])
                observation["multistep"] = self.state.get("multistep", {})
            if observation.get("accepted"):
                self.state.setdefault("accepted", {})[observation["key"]] = {"grade": observation.get("grade"), "html_path": item["html_path"]}
                if mid:
                    self.state.setdefault("live_records", {})[mid] = item
                self.state.pop("pending_action", None)
                self._save()
        else:
            observation.update(self._evidence(self.page, Path(directory) / "observations", view["key"]))
            if view["kind"] == "complete":
                body = self.page.locator(view["selector"]).inner_text()
                observation["completion"] = {**parse_xp(body), "text": body, "task_id": self.activity["task_id"]}
                self.state["completion"] = observation["completion"]
                self.state["completed"] = True
                self.state.pop("pending_action", None)
                self._save()
        return observation

    def _multistep_context(self, directory):
        result = {"shared_contexts": [], "part_order": []}
        for step in self.page.locator("#steps > .step").all():
            q = step.locator(".question").first
            if q.count():
                result["part_order"].append({"math_academy_id": question_identity(q.get_attribute("id")), "source_step": step.get_attribute("id")})
            else:
                item = self._read(step, directory, "context-" + str(step.get_attribute("id")))
                result["shared_contexts"].append({**item, "id": step.get_attribute("id")})
        self.state["multistep"] = result
        self._save()
        return result

    def _intent(self, observation, action, **details):
        self.state["pending_action"] = {"key": observation["key"], "action": action, "time": time.time(), **details}
        self.state["restored"] = False
        self._save()

    def respond(self, observation, responses, directory):
        check_stop(self.stop_event)
        action = responses.get("action") if isinstance(responses, dict) else None
        if action == "submit_assessment":
            return self._submit_assessment(observation, directory)
        current = self._view()
        if current.get("accepted") or current["kind"] == "complete":
            return  # A response already accepted by MA is never repeated.
        if current["kind"] == "assessment":
            current = self._assessment_view(current)
        if current.get("selector") != observation.get("selector"):
            return  # The site moved on; capture its new presentation first.
        pending = self.state.get("pending_action", {})
        if pending.get("action") in ("submit", "dont_know", "skip") and not self.state.get("restored"):
            # Read-only reload asks the server whether the earlier request took.
            # No submission is retried just because its response timed out.
            self._goto(self.page.url)
            self.state["restored"] = True
            self._save()
            return
        scope = self.page.locator(current["selector"])
        if action in ("dont_know", "skip"):
            button = scope.locator(".questionWidget-skipButton:visible").first
            if not button.count():
                button = self.page.get_by_text(re.compile(r"^(Don't Know|I Don't Know|Skip)$", re.I)).filter(visible=True).first
            self._intent(observation, action)
            button.click()
        else:
            fresh = self._read(scope, directory, observation["key"] + "-before-entry")
            answers = {a["key"]: a for a in (responses.get("responses", responses.get("answers", [])) if isinstance(responses, dict) else responses)}
            entered = []
            for field in fresh["fields"]:
                if field.get("source_result") == "Correct" or field.get("disabled"):
                    continue
                if field["key"] not in answers:
                    raise ValueError("Missing response for answer field " + field["key"])
                entered.append(enter(scope, field, answers[field["key"]]))
            # Blur the active math editor so its floating symbol palette cannot
            # cover Submit or sanitize an entry after its readback.
            prompt = scope.locator(".questionWidget-text,.questionText").first
            if prompt.count() and prompt.is_visible():
                prompt.click(position={"x": 1, "y": 1})
            self._intent(observation, "entered", responses=entered)
            self._evidence(self.page, Path(directory) / "observations", observation["key"] + "-entered")
            if self.activity.get("kind") == "assessment":
                qid = scope.get_attribute("id")
                self.state.setdefault("assessment_filled", {})[qid] = entered
                self.state.pop("pending_action", None)
                self._save()
                return
            submit = scope.locator(".questionWidget-submitButton:visible,.submitButton:visible").first
            if not submit.count() and current.get("step_id"):
                submit = by_id(self.page, current["step_id"].replace("step-", "submitButton-"))
            # MA's MathEditor polls changes every 200ms before enabling Submit.
            self.page.wait_for_function("n => !n.disabled && !n.classList.contains('disabledButton')", arg=submit.element_handle(), timeout=self.config.timeout_ms)
            self._intent(observation, "submit", responses=entered)
            submit.click()
        # Wait for evidence, never automatically click Submit twice after timeout.
        self.page.wait_for_function(r'''old => {
          const n=document.querySelector(old.selector);
          return !n || !!n.querySelector('.questionWidget-result,.correctAnswerText,.incorrectAnswerText')?.textContent.trim() ||
            !!n.querySelector('.questionWidget-feedback')?.textContent.trim() ||
            !!document.querySelector('#retryScreen-noButton')?.getClientRects().length ||
            !!document.querySelector('#finalScreen')?.getClientRects().length ||
            [...n.querySelectorAll('.correctSelection,.incorrectSelection')].length > old.graded;
        }''', arg={"selector": current["selector"], "graded": sum(bool(f.get("source_result")) for f in observation.get("question", {}).get("fields", []))})

    def _submit_assessment(self, observation, directory):
        view = self._view()
        if view["kind"] == "complete":
            return
        dialog = self.page.locator("#confirmationDialog:visible")
        if not dialog.count():
            self._intent(observation, "open_assessment_confirmation")
            by_id(self.page, "submitTestButton").click()
            dialog = by_id(self.page, "confirmationDialog")
            dialog.wait_for(state="visible")
        if not re.search(r"submit\s+this\s+test", dialog.inner_text(), re.I):
            raise BrowserUnavailable("Unexpected confirmation; retain the test and reread its page")
        self._intent(observation, "submit_assessment")
        dialog.get_by_text("Yes", exact=True).click()
        self.page.locator("#finalScreen").wait_for(state="visible")
        self.state.pop("pending_action", None)
        self._save()

    def advance(self, observation, directory):
        current = self._view()
        if current["kind"] == "complete" or current["kind"] == "assessment":
            return
        if current.get("reload_required"):
            self._goto(self.page.url)
            return
        if current["kind"] == "question" and not current.get("accepted"):
            return  # Capture and answer it; do not skip an unread question.
        button = current.get("button") or current.get("next")
        if not button:
            raise BrowserUnavailable("No supported continuation is visible; reread the same activity")
        # Re-observation can show a later step after an interrupted Continue click.
        if current.get("key") != observation.get("key") and not observation["key"].startswith(current.get("key", "") + ":fields:"):
            return
        self._intent(observation, "advance", button=button)
        self.page.locator(button).click()
        previous = current.get("key")
        self.page.wait_for_function("previous => (" + VIEW + ")().key !== previous", arg=previous)
        self.state["activity_url"] = self.page.url
        self.state.pop("pending_action", None)
        self._save()

    def recover(self, observation, decision, directory):
        """Execute only an agent-selected control that still exists on this page."""
        self._check()
        if decision.get("action") != "advance":
            raise ValueError("Unsupported page-recovery action")
        selector, label = decision.get("button_selector"), decision.get("button_text")
        if not selector or not label:
            raise ValueError("Recovery needs the observed button selector and text")
        forbidden = r"\b(quit|exit|defer|abandon|logout|log out|delete|cancel|pause)\b|back\s+to|return\s+to|dashboard|activity\s+queue"
        if re.search(forbidden, label, re.I):
            raise ValueError("Recovery must continue the pinned activity")
        proposed = {"selector": selector, "text": label}
        if proposed not in observation.get("buttons", []):
            raise ValueError("The selected control was not in the captured page")
        current = self._view()
        if current["kind"] != "unknown" or proposed not in current.get("buttons", []):
            return  # The site changed; observe its new state before acting.
        button = self.page.locator(selector)
        if button.count() != 1 or not button.is_visible() or button.inner_text().strip() != label:
            raise ValueError("Recovery control changed before its click")
        pending = self.state.get("pending_action", {})
        if pending.get("action") == "recover_control" and not self.state.get("restored"):
            self._goto(self.page.url)
            self.state["restored"] = True
            self._save()
            return
        self._evidence(self.page, Path(directory) / "observations", "before-recovery-control")
        self._intent(observation, "recover_control", button=selector, button_text=label,
                     reasoning=decision.get("reasoning"))
        button.click()
        # The caller observes after the click. Retain intent through timeouts so
        # the next recovery verifies server state instead of clicking twice.

    def history(self, activity, directory):
        directory = Path(directory)
        self.activity, self.directory = dict(activity), directory
        if self.state.get("task_id") != str(activity["task_id"]):
            self.state = read_json(directory / "browser-state.json", {}) or {}
        limitation = None
        try:
            self._goto(LEARN + "?taskId=" + str(activity["task_id"]))
        except SourceUnavailable as error:
            limitation = str(error)
        if not limitation:
            try:
                self.page.locator(".question[id^='question-']").first.wait_for(state="attached")
            except Exception:
                self._check()
                limitation = "Completed history page exposed no question records after loading"
        metadata = parse_history_metadata(self.page.content())
        questions = []
        for info in metadata:
            self._check()
            node = by_id(self.page, info["dom_id"])
            explanation = by_id(self.page, info["dom_id"].replace("question-", "questionExplanation-"))
            try:
                if not explanation.count() or not explanation.is_visible():
                    node.locator(".answerDetails").click()
                explanation.wait_for(state="visible")
                item = self._read(node, directory, "history-" + info["math_academy_id"])
                solution = self._read(explanation, directory, "history-solution-" + info["math_academy_id"],
                                      prior=self.state.get("live_records", {}).get(info["math_academy_id"]))
                item["worked_solution"] = solution["worked_solution"]
                item["assets"] = item.get("assets", []) + solution.get("assets", [])
                item["solution_evidence"] = solution["html_path"]
            except Exception as error:
                item = self._read(node, directory, "history-" + info["math_academy_id"])
                item.setdefault("errors", []).append("History expansion: " + str(error))
            questions.append({**item, **info, "result": info["grade"],
                              "topic_id": info.get("topic_id") or activity.get("topic_id")})
        evidence = self._evidence(self.page, directory, "history-expanded")
        content = {"task_id": str(activity["task_id"]), "task_type": activity["kind"],
                   "topic_id": activity.get("topic_id"), "questions": questions,
                   "canonical_examples": [], "tutorials": [], "completion": self.state.get("completion", {}), **evidence}
        if limitation:
            content["source_limitations"] = [{"reason": limitation, "source_file": evidence["html_path"]}]
        if activity["kind"] == "lesson" and activity.get("topic_id"):
            content.update(self._lesson(activity, directory))
        if activity["kind"] == "multistep":
            multistep = self.state.get("multistep", {})
            content.update(multistep_id=activity.get("details", {}).get("multistep_id"), title=activity.get("title"),
                           shared_contexts=multistep.get("shared_contexts", []),
                           question_order=[x["math_academy_id"] for x in multistep.get("part_order", [])],
                           multistep=multistep)
        atomic_json(directory / "history-content.json", content)
        return content

    def _lesson(self, activity, directory):
        page = self.context.new_page()
        previous = self.page
        try:
            try:
                self._goto(f"{BASE}/topics/{activity['topic_id']}", page)
            except SourceUnavailable as error:
                evidence = self._evidence(page, directory, "lesson-topic-unavailable")
                return {"lesson_definition": {"topic_id": activity["topic_id"], "complete": False, "steps": [],
                                               "issues": [{"reason": str(error), "source_file": evidence["html_path"]}]}}
            try:
                page.locator("div.step[stepid][steptype][contentid]").first.wait_for(state="attached")
            except Exception:
                self._check(page)
            definition = parse_lesson_structure(page.content(), activity["topic_id"])
            evidence = self._evidence(page, directory, "lesson-topic")
            definition.update(source_file=evidence["html_path"])
            examples, tutorials = [], []
            self.page = page
            for step in definition["steps"]:
                scope = page.locator(f'div.step[stepid="{step["math_academy_id"]}"]')
                item = self._read(scope, directory, "lesson-step-" + str(step["math_academy_id"]))
                if step["type"] == "tutorial":
                    tutorials.append({**item, "math_academy_id": step["content_id"], "title": step["title"], "content": item["problem"]})
                elif step["type"] == "example":
                    examples.append({**item, "math_academy_id": "e-" + str(step["content_id"]),
                                     "knowledge_point": step["title"], "topic_id": activity["topic_id"],
                                     "source_placement_id": step["math_academy_id"]})
            return {"lesson_definition": definition, "canonical_examples": examples, "tutorials": tutorials}
        finally:
            self.page = previous
            page.close()

    def postprocess(self, activity, directory):
        capture_directory = Path(directory)
        source_state = read_json(capture_directory / "browser-state.json", {}) or {}
        if source_state.get("task_id") != str(activity["task_id"]):
            source_state = self.state if self.state.get("task_id") == str(activity["task_id"]) else {}
        directory = capture_directory / "post-activity"
        page = self.context.new_page()
        result = {"task_id": str(activity["task_id"]), "account": self.config.account,
                  "completion": deepcopy(source_state.get("completion", {})), "courses": [], "pending_reads": [], "observed_at": time.time()}
        try:
            try:
                self._goto(LEARN, page)
                page.locator("#completedTasks").wait_for(state="attached")
                dashboard = parse_dashboard(page.content(), activity["task_id"])
                result.update(completed=dashboard["completed"], dashboard=self._evidence(page, directory, "dashboard"))
                if dashboard["activity"]:
                    result["completion"].update(dashboard["activity"])
                urls = dashboard["course_urls"]
            except Exception as error:
                result["pending_reads"].append({"url": LEARN, "error": str(error)})
                urls = [f"{BASE}/courses/{self.config.course_id}/progress"] if self.config.course_id else []
            for url in urls:
                try:
                    self._goto(url, page)
                    page.locator(".moduleTopics .topicLink").first.wait_for(state="attached")
                    course = parse_progress(page.content(), re.search(r"/courses/(\d+)", url)[1])
                    course.update(self._evidence(page, directory, "course-" + course["course_id"]))
                    result["courses"].append(course)
                except Exception as error:
                    result["pending_reads"].append({"url": url, "error": str(error), "failed_at": time.time()})
            result["completion"].update(task_id=str(activity["task_id"]), kind=activity["kind"], topic_id=activity.get("topic_id"))
            atomic_json(directory / "observations.json", result)
            return result
        finally:
            page.close()
