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

from ..courses import record_current_course
from ..runtime import StopRequested, check_stop
from ..storage import atomic_json, atomic_text, read_json
from ..timing import Pacer
from .assets import AssetCapture
from .entry import by_id, enter, verify_entered
from .safety import BrowserSafety
from .parsing import (BASE, LEARN, activity_from_url, parse_dashboard, parse_history_metadata,
                      parse_lesson_structure, parse_progress, parse_queue, parse_xp, question_identity)

EXTRACT = (Path(__file__).parent / "extract.js").read_text()
VIEW = (Path(__file__).parent / "view.js").read_text()
RESPONSE_STATE = r'''n => ({
  feedback:n.querySelector('.questionWidget-feedback')?.textContent.trim() || '',
  grades:[...n.querySelectorAll('.correctSelection,.correctSelectionMultipleAttempts,.incorrectSelection')]
    .map((f,i)=>[f.closest('.selectList')?.id || f.id || i,f.className])
})'''
RESPONSE_READY = r'''old => {
  const n=document.querySelector(old.selector);
  if(!n) return true;
  const visible=n=>!!n?.getClientRects().length && getComputedStyle(n).visibility!=='hidden';
  if(n.querySelector('.questionWidget-result,.correctAnswerText,.incorrectAnswerText')?.textContent.trim() ||
     visible(document.querySelector('#retryScreen-noButton')) || visible(document.querySelector('#finalScreen')))
    return true;
  const feedback=n.querySelector('.questionWidget-feedback');
  if(visible(feedback) && feedback.textContent.trim() && feedback.textContent.trim()!==old.before.feedback) return true;
  const grades=[...n.querySelectorAll('.correctSelection,.correctSelectionMultipleAttempts,.incorrectSelection')]
    .map((f,i)=>[f.closest('.selectList')?.id || f.id || i,f.className]);
  if(grades.length && JSON.stringify(grades)!==JSON.stringify(old.before.grades)) return true;
  // Another incorrect proof attempt may produce identical feedback/classes.
  // In that case wait until MA finishes its request and enables another try.
  const frames=[...n.querySelectorAll('.selectListFrame,.selectListFrameDisabled')];
  const submit=n.querySelector('.questionWidget-submitButton,.submitButton');
  return !!frames.length && frames.every(f=>f.matches('.correctSelection,.correctSelectionMultipleAttempts,.incorrectSelection')) &&
    !visible(n.querySelector('.questionWidget-spinner')) && !!submit && !submit.disabled && !submit.classList.contains('disabledButton');
}'''


class BrowserUnavailable(RuntimeError):
    """Retry this same activity after reconnecting or rereading its server state."""


class SourceUnavailable(BrowserUnavailable):
    """The source explicitly says a completed activity's content no longer exists."""


class SourceHTTPError(BrowserUnavailable):
    """A source read failed without establishing that its content is absent."""

    def __init__(self, status, url):
        self.http_status, self.request_url = status, url
        super().__init__(f"Source page HTTP {status}: {url}")


class SubmissionHTTPError(BrowserUnavailable):
    """An answer request failed; its learner outcome still needs reconciliation."""

    def __init__(self, status, url):
        self.http_status, self.request_url = status, url
        super().__init__(f"Math Academy answer submission returned HTTP {status}; outcome unconfirmed ({url})")


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
        self.pacer = Pacer(config, stop_event)
        self.deadline_at = None
        self.safety = BrowserSafety(self)

    def __enter__(self):
        from playwright.sync_api import sync_playwright
        check_stop(self.stop_event)
        self.playwright = sync_playwright().start()
        if self.config.browser_cdp_url:
            self.browser = self.playwright.chromium.connect_over_cdp(self.config.browser_cdp_url, slow_mo=max(500, getattr(self.config, "ui_delay_ms", 500)))
            self.context = self.browser.contexts[0]
        else:
            self.config.profile.mkdir(parents=True, exist_ok=True)
            self.context = self.playwright.chromium.launch_persistent_context(
                str(self.config.profile), headless=self.config.headless,
                viewport={"width": 1440, "height": 1000}, accept_downloads=False,
                slow_mo=max(500, getattr(self.config, "ui_delay_ms", 500)))
        self.context.set_default_timeout(self.config.timeout_ms)
        self.context.on("response", self._response)
        self.context.route("**/*", self.safety.repair_document)
        self.context.on("page", self._attach_page_events)
        for page in self.context.pages:
            self._attach_page_events(page)
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

    def _attach_page_events(self, page):
        page.on("pageerror", lambda error: self.safety.event("page_error", message=str(error)))
        page.on("console", lambda message: self.safety.event("console", level=message.type, message=message.text)
                if message.type in ("warning", "error") else None)
        page.on("requestfailed", lambda request: self.safety.event("request_failed", url=request.url,
                                                                  reason=request.failure))

    def set_deadline(self, deadline_at):
        self.deadline_at = float(deadline_at) if deadline_at is not None else None
        if self.context:
            self.context.set_default_timeout(self.timeout_ms())

    def remaining_seconds(self):
        return None if self.deadline_at is None else max(0.0, self.deadline_at - time.time())

    def read_remaining_seconds(self):
        """Read the visible countdown while retaining the saved absolute bound."""
        live, saved = self._remaining(), self.remaining_seconds()
        values = [value for value in (live, saved) if value is not None]
        return min(values) if values else None

    def timeout_ms(self, reserve=0):
        remaining = self.remaining_seconds()
        if remaining is None:
            return self.config.timeout_ms
        if remaining <= 0:
            # An expired saved timer must still allow reading server results.
            # Answer entry has a separate deadline guard; read-only recovery
            # remains possible after the test has ended remotely.
            return min(self.config.timeout_ms, 5000)
        return max(1, min(self.config.timeout_ms, int((remaining - reserve) * 1000)))

    def _pause(self, reason, reserve=0):
        deadline = self.deadline_at - reserve if self.deadline_at is not None else None
        self.pacer.wait("event", reason, deadline=deadline)
        if self.context:
            self.context.set_default_timeout(self.timeout_ms())

    def _wait_cooldown(self):
        delay = self.safety.remaining_cooldown()
        if delay:
            remaining = self.remaining_seconds()
            if remaining is not None and delay >= remaining:
                error = BrowserUnavailable("Rate-limit cooldown extends beyond the assessment deadline")
                error.retry_after = delay
                raise error
            self.pacer.sleep(delay, deadline=self.deadline_at)
        if self.safety.remaining_cooldown() > .01:
            error = BrowserUnavailable("Math Academy rate-limit cooldown is still active")
            error.retry_after = self.safety.remaining_cooldown()
            raise error

    def _response(self, response):
        self.safety.response(response)
        if response.ok and response.request.resource_type == "image":
            self.image_responses[response.url] = response

    def _check(self, page=None):
        check_stop(self.stop_event)
        self._wait_cooldown()
        if self.context:
            self.context.set_default_timeout(self.timeout_ms())
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
        self._wait_cooldown()
        self._pause("navigation")
        response = page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms())
        if response and response.status in (404, 410):
            raise SourceUnavailable(f"Source page HTTP {response.status}: {url}")
        if response and response.status >= 400:
            raise SourceHTTPError(response.status, url)
        self._check(page)
        self.safety.reconcile_required = False

    def _save(self):
        if self.directory:
            atomic_json(self.directory / "browser-state.json", self.state)

    def _screenshot(self, target, **kwargs):
        for attempt in range(3):
            try:
                return target.screenshot(timeout=min(self.timeout_ms(), 10000), **kwargs)
            except Exception as error:
                if attempt == 2 or not re.search(r"font", str(error), re.I):
                    raise
                self.safety.event("screenshot_font_retry", attempt=attempt + 1)
                self.pacer.sleep(min(1.0, (attempt + 1) * .5), deadline=self.deadline_at)

    def _settle_content(self, scope, kind="content"):
        """Wait for authored content and MathML, then a short stable DOM window."""
        self.page.wait_for_function(r'''({node,kind}) => {
          const content=n=>!!n && (!!n.textContent.trim() || !!n.querySelector('img,canvas,svg'));
          const math=[...node.querySelectorAll('mjx-container')].every(n=>n.querySelector('mjx-assistive-mml math,svg'));
          const prompt=node.querySelector('.exampleQuestion');
          const solution=node.querySelector('.exampleExplanation');
          let ready=math && (kind==='example' ? content(prompt)&&content(solution) : content(node));
          if(kind==='tutorial') {
            const clone=node.cloneNode(true);clone.querySelectorAll('button,.stepName,[id^="continueButton-"]').forEach(n=>n.remove());
            ready=math&&content(clone);
          }
          if(!ready) return false;
          const html=node.innerHTML, now=performance.now();
          if(node.__captureStable?.html!==html) node.__captureStable={html,at:now};
          return now-node.__captureStable.at>=500;
        }''', arg={"node": scope.element_handle(), "kind": kind}, timeout=self.timeout_ms())

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
            self._screenshot(page, path=str(screenshot), full_page=True)
        except StopRequested:
            raise
        except Exception as error:
            errors.append("Screenshot unavailable: " + str(error))
        return {"html_path": str(target.resolve()), "screenshot": str(screenshot.resolve()) if screenshot.exists() else None,
                "captured_at": time.time(), "source_url": page.url, "evidence_errors": errors,
                "original_document": self.safety.original_documents.get(page.url)}

    def queue(self, directory):
        self._goto(LEARN)
        record_current_course(self.config, self.page.content(), self.page.url)
        active = activity_from_url(self.page.url)
        if active:
            active["course_id"] = self.config.course_id
            evidence = self._evidence(self.page, directory, "forced-active")
            active["details"].update(evidence)
            return [active]
        self.page.locator("#incompleteTasks").wait_for(state="attached")
        self.pacer.sleep(getattr(self.config, "settle_ms", 1000) / 1000, deadline=self.deadline_at)
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
                    self._pause("expand queue card")
                    (heading if heading.count() else card).click()
                # Expansion asynchronously inserts its start link.
                card.locator("a.taskStartButton").first.wait_for(state="attached", timeout=min(self.config.timeout_ms, 5000))
                expanded = parse_queue("<div id='incompleteTasks'>" + card.evaluate("n=>n.outerHTML") + "</div>")
                if expanded:
                    item = expanded[0]
                    item["position"] = initial_item["position"]
                    item["course_id"] = initial_item["course_id"] or self.config.course_id
                atomic_text(Path(directory) / f"queue-card-{item['task_id']}.html", card.evaluate("n=>n.outerHTML"))
            except StopRequested:
                raise
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
        self.set_deadline((checkpoint.get("assessment_timing") or {}).get("deadline_at") if activity.get("kind") == "assessment" else None)
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
        record_current_course(self.config, self.page.content(), self.page.url)
        # Server state, not the previous click's success, decides what to do next.
        if self.state.get("assessment_filled"):
            self.state["assessment_filled_before_reload"] = self.state.pop("assessment_filled")
        self.state["restored"] = True
        self.state["activity_url"] = self.page.url
        self._save()

    def _read(self, scope, directory, label, prior=None, context=None):
        item = scope.evaluate(EXTRACT, context or {})
        item = self.assets.collect(item, scope, directory, label, prior=prior)
        # Asset failures retain the section identified by the source extractor.
        for asset in item.get('assets', []):
            identity = asset.get('source_url') or label + ':' + str(asset['index'])
            for prefix in ('Graphic rendering unavailable: ', 'Image unavailable: '):
                error = prefix + identity
                if error in item.get('errors', []) and asset.get('extraction_part'):
                    parts = item.setdefault('extraction_error_parts', {}).setdefault(error, [])
                    if asset['extraction_part'] not in parts:
                        parts.append(asset['extraction_part'])
        key = fingerprint({"html": item.get("html"), "url": self.page.url})
        target = Path(directory) / "observations" / (re.sub(r"[^a-zA-Z0-9_-]", "-", label) + "-" + key)
        atomic_json(target.with_suffix(".json"), item)
        atomic_text(target.with_suffix(".html"), item.get("html", ""))
        screenshot = target.with_suffix(".png")
        try:
            self._screenshot(scope, path=str(screenshot))
        except StopRequested:
            raise
        except Exception as error:
            item.setdefault("errors", []).append("Screenshot unavailable: " + str(error))
        for field in item.get("fields", []):
            confirmed = field.get("source_correct")
            if confirmed and confirmed.get("value") is not None:
                field.update(correct_value=confirmed["value"], correct_origin="ma_answer",
                             correct_evidence={"kind": "ma_answer", "source_file": str(target.with_suffix(".html").resolve()),
                                               "value": confirmed["value"]})
        atomic_json(target.with_suffix(".json"), item)
        return {**item, "html_path": str(target.with_suffix(".html").resolve()),
                "screenshot": str(screenshot.resolve()) if screenshot.exists() else None,
                "source_url": self.page.url, "captured_at": time.time()}

    def _view(self):
        self._check()
        view = self.page.evaluate(VIEW)
        if view['kind'] == 'unknown' and self.activity:
            # A final review answer can return directly to the queue without a
            # finalScreen. Only this pinned task's completed source card proves
            # completion; other completed activities are irrelevant.
            completed = parse_dashboard(self.page.content(), self.activity['task_id'])['activity']
            if completed:
                return {'kind': 'complete', 'selector': '#task-' + str(self.activity['task_id']),
                        'key': 'complete', 'accepted': True}
        return view

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
            seconds = sum(int(amount) * (3600 if unit.lower().startswith("hour") else 60 if unit.lower().startswith("minute") else 1)
                       for amount, unit in units)
            # MA rounds minute-only labels upward; use their lower bound.
            if not any(unit.lower().startswith("second") for _, unit in units):
                seconds = max(0, seconds - (60 if any(unit.lower().startswith("minute") for _, unit in units) else 3600))
            return seconds
        return None

    def _assessment_view(self, view):
        self.state["assessment_question_count"] = len(view["ids"])
        navigator = self.page.locator("#questionNavigator")
        if navigator.count():
            try:
                self.page.wait_for_function("count=>document.querySelectorAll('#questionNavigator .questionButton').length===count",
                                            arg=len(view["ids"]), timeout=self.timeout_ms())
            except Exception as error:
                check_stop(self.stop_event)
                self.state.setdefault("assessment_readiness_errors", []).append("Navigator readiness: " + str(error))
        if not self.state.get("assessment_initial_evidence"):
            # Save every initialized question's original DOM before any answer.
            try:
                self.page.wait_for_function("() => Object.values((" + VIEW + ")().question_ready || {}).every(Boolean)",
                                            timeout=self.timeout_ms())
            except Exception as error:
                check_stop(self.stop_event)
                self.state.setdefault("assessment_readiness_errors", []).append("Initial question rendering: " + str(error))
            if self.directory:
                self.state["assessment_initial_evidence"] = self._evidence(self.page, self.directory / "observations", "assessment-initial")
                self._save()
        filled = self.state.setdefault("assessment_filled", {})
        unanswered = [qid for qid in view["ids"] if qid not in filled]
        if not unanswered:
            return {"kind": "instructions", "key": "submit-assessment", "action": "submit_assessment", "selector": "body"}
        qid = unanswered[0]
        scope = by_id(self.page, qid)
        if not scope.is_visible():
            self._pause("assessment navigation", reserve=15)
            try:
                self.page.locator("#questionNavigator .questionButton").nth(view["ids"].index(qid)).click()
                scope.wait_for(state="visible")
                view = self._view()
            except Exception as error:
                check_stop(self.stop_event)
                return {"kind": "unknown", "key": "assessment-navigator", "selector": "body", "buttons": [],
                        "readiness_errors": ["Assessment navigator did not reveal its question: " + str(error)]}
        return {"kind": "question", "selector": "[id=" + json.dumps(qid) + "]", "key": qid,
                "sequence_position": view["ids"].index(qid) + 1, "accepted": False, "assessment": True,
                "ready": view.get("question_ready", {}).get(qid, True)}

    def _wait_diagnostic_transition(self, previous_key):
        # The retry overlay disappears before its asynchronous request supplies
        # the next question. The old grade/Next button are still visible then.
        self.page.wait_for_function("previous => {const v=(" + VIEW + ")(); return v.kind==='complete' || "
            "(v.kind==='question' && v.key!==previous && v.ready!==false);}",
            arg=previous_key, timeout=self.timeout_ms())

    def _ready_view(self):
        while True:
            view = self._view()
            pending = self.state.get("pending_action", {})
            if ("diagnostic_previous_key" in pending and pending["diagnostic_previous_key"] == view.get("key")
                    and pending.get("action") == "advance" and not self.state.get("restored")):
                self._wait_diagnostic_transition(pending["diagnostic_previous_key"])
                continue
            if view["kind"] == "assessment":
                view = self._assessment_view(view)
            if view.get("ready") is not False:
                return view
            # Source controls and MathJax finish asynchronously. Wait first;
            # preserve explicit rendering errors if the source never completes.
            try:
                self.page.wait_for_function("old => {const v=(" + VIEW + ")(); return "
                    "v.kind === 'assessment' ? v.question_ready?.[old.key] !== false : v.ready !== false;}",
                    arg={"key": view["key"]}, timeout=self.timeout_ms())
            except Exception as error:
                check_stop(self.stop_event)
                issue = "Source rendering remained incomplete: " + str(error)
                self.safety.event("readiness_timeout", key=view.get("key"), reason=issue)
                # Preserve imperfect source evidence and let the activity agent
                # judge it. A grade can advance while history recovers its math.
                item = self.page.locator(view["selector"]).evaluate(EXTRACT)
                if view.get("accepted") or (item.get("problem") and item.get("fields")):
                    return {**view, "readiness_errors": [issue]}
                buttons = self.page.locator("button,a,[role=button],.button").evaluate_all(r'''nodes => nodes
                  .filter(n=>n.id && n.getClientRects().length && !/submit|don't know|skip|quit|exit/i.test(n.textContent))
                  .filter(n=>n.localName!=='a' || !n.getAttribute('href') || n.getAttribute('href')==='#' || /^javascript:/i.test(n.getAttribute('href')))
                  .map(n=>({selector:'#'+CSS.escape(n.id),text:n.textContent.trim()})).filter(n=>n.text)''')
                return {"kind": "unknown", "key": "unready-" + view["key"], "selector": "body",
                        "buttons": buttons, "readiness_errors": [issue], "source_view_kind": view["kind"]}

    def observe(self, directory):
        view = self._ready_view()
        observed_at, remaining = time.time(), self._remaining()
        observation = {**view, "remaining_seconds": remaining, "source_url": self.page.url, "observed_at": observed_at,
                       "deadline_at": self.deadline_at, "question_count": self.state.get("assessment_question_count"),
                       "browser_events": self.safety.events[-20:]}
        if view["kind"] in ("question", "example", "tutorial"):
            scope = self.page.locator(view["selector"])
            item = self._read(scope, directory, view["key"])
            if view.get("readiness_errors"):
                item.setdefault("errors", []).extend(view["readiness_errors"])
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
                pending = self.state.get("pending_action", {})
                if (pending.get("action") not in ("submit", "dont_know", "skip") or self.state.get("restored")
                    or (pending.get("response_before") is not None and self.page.evaluate(RESPONSE_READY,
                        {"selector": view["selector"], "before": pending["response_before"]}))):
                    self.state.pop("pending_action", None)
                    self._save()
            if view["kind"] in ("question", "example"):
                observation["question"] = item
            else:
                # A multistep's step-1 is shared context, not a tutorial ID.
                # Only explicit content IDs or the lesson's step-t<ID> encode
                # tutorial identity; retain the DOM label as capture evidence.
                tutorial_id = (view.get("source_step") or {}).get("content_id")
                if tutorial_id is None:
                    match = re.fullmatch(r"step-t(\d+)", item.get("dom_id") or "")
                    tutorial_id = match[1] if match else None
                observation["tutorial"] = {**item, "content": item["problem"], "title": item.get("name"),
                                           "math_academy_id": tutorial_id}
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
        started = time.time()
        try:
            return self._respond(observation, responses, directory)
        except Exception as error:
            # A durable submit intent means the server may have accepted it.
            # Entry/readback failures before that point are not learner attempts.
            error.submitted = self.state.get("pending_action", {}).get("action") in (
                "submit", "dont_know", "skip", "submit_assessment")
            if error.submitted and type(error).__name__ == 'TimeoutError':
                topic_id = str((self.activity or {}).get('topic_id') or '')
                question_id = str((observation.get('question') or {}).get('math_academy_id') or '').removeprefix('q-')
                source_ids = {str((self.activity or {}).get('task_id') or ''), question_id} - {''}
                failure = next((event for event in reversed(self.safety.events)
                    if event.get('kind') == 'http_error' and event.get('at', 0) >= started
                    and event.get('method') == 'POST'
                    and event.get('url') in {f'https://mathacademy.com/api/tasks/{identifier}/lessons/{topic_id}/submit-answer'
                                             for identifier in source_ids}), None)
                if failure:
                    cause = SubmissionHTTPError(failure['status'], failure['url'])
                    cause.submitted = True
                    raise cause from error
            raise

    def _respond(self, observation, responses, directory):
        check_stop(self.stop_event)
        action = responses.get("action") if isinstance(responses, dict) else None
        if action == "submit_assessment":
            return self._submit_assessment(observation, directory)
        self._check()
        if self.safety.reconcile_required:
            self._goto(self.page.url)
            return {"unknown_outcome": True, "not_submitted": True, "reason": "Reloaded to reconcile browser safety state"}
        current = self._ready_view()
        if current.get("accepted") or current["kind"] == "complete":
            return {"unknown_outcome": True, "not_submitted": True, "reason": "Question already accepted or activity completed"}
        if (current.get("selector") != observation.get("selector") or
                current.get("key") != observation.get("key", "").split(":fields:")[0]):
            return {"unknown_outcome": True, "not_submitted": True, "reason": "Current question differs from the captured presentation"}
        pending = self.state.get("pending_action", {})
        if pending.get("action") in ("submit", "dont_know", "skip") and not self.state.get("restored"):
            # Read-only reload asks the server whether the earlier request took.
            # No submission is retried just because its response timed out.
            self._goto(self.page.url)
            self.state["restored"] = True
            self._save()
            return {"unknown_outcome": True, "not_submitted": True, "reason": "Reloaded to reconcile an earlier submission with unknown outcome"}
        scope = self.page.locator(current["selector"])
        expected = observation.get("question") or {}
        live = scope.evaluate(EXTRACT)
        if expected.get("problem") is not None and self._binding(expected) != self._binding(live):
            return {"unknown_outcome": True, "not_submitted": True, "reason": "Captured prompt or answer controls do not match the live source before entry"}
        if action in ("dont_know", "skip"):
            button = scope.locator(".questionWidget-skipButton:visible").first
            if not button.count():
                button = self.page.get_by_text(re.compile(r"^(Don't Know|I Don't Know|Skip)$", re.I)).filter(visible=True).first
            response_before = scope.evaluate(RESPONSE_STATE)
            self._intent(observation, action, response_before=response_before)
            button.click()
        else:
            fresh = self._read(scope, directory, observation["key"] + "-before-entry")
            if expected.get("problem") is not None and self._binding(expected) != self._binding(fresh):
                return {"unknown_outcome": True, "not_submitted": True, "reason": "Prompt or answer controls changed during the fresh entry read"}
            answers = {a["key"]: a for a in (responses.get("responses", responses.get("answers", [])) if isinstance(responses, dict) else responses)}
            entered = []
            for field in fresh["fields"]:
                if field.get("source_result") == "Correct" or field.get("disabled"):
                    continue
                if field["key"] not in answers:
                    raise ValueError("Missing response for answer field " + field["key"])
                if self.activity.get("kind") == "assessment" and self.remaining_seconds() is not None and self.remaining_seconds() <= 15:
                    return {"unknown_outcome": True, "not_submitted": True, "deadline_reached": True}
                self._pause("answer field selection", reserve=15 if self.activity.get("kind") == "assessment" else 0)
                visible = self._view()
                if ((visible.get("key") != current.get("key") and visible["kind"] != "assessment") or
                        (fresh.get("problem") is not None and self._binding(fresh) != self._binding(scope.evaluate(EXTRACT)))):
                    return {"unknown_outcome": True, "not_submitted": True, "reason": "Question changed during answer entry"}
                entered.append(enter(scope, field, answers[field["key"]]))
            self._intent(observation, "entered", responses=entered)
            if self.activity.get("kind") == "assessment":
                self._settle_entry(scope, fresh, entered)
                self._evidence(self.page, Path(directory) / "observations", observation["key"] + "-entered")
                verify_entered(scope, fresh, entered)
                visible = self._view()
                if (visible["kind"] != "assessment" or (fresh.get("problem") is not None and
                        self._binding(fresh) != self._binding(scope.evaluate(EXTRACT)))):
                    return {"unknown_outcome": True, "not_submitted": True, "reason": "Assessment question changed while entered values settled"}
                qid = scope.get_attribute("id")
                self.state.setdefault("assessment_filled", {})[qid] = entered
                self.state.pop("pending_action", None)
                self._save()
                return
            submit = scope.locator(".questionWidget-submitButton:visible,.submitButton:visible").first
            if not submit.count() and current.get("step_id"):
                submit = by_id(self.page, current["step_id"].replace("step-", "submitButton-"))
            # MA's MathEditor polls changes every 200ms before enabling Submit.
            self.page.wait_for_function("n => !n.disabled && !n.classList.contains('disabledButton')", arg=submit.element_handle(), timeout=self.timeout_ms())
            self._settle_entry(scope, fresh, entered)
            self._evidence(self.page, Path(directory) / "observations", observation["key"] + "-entered")
            verify_entered(scope, fresh, entered)
            if (self._view().get("key") != current.get("key") or (fresh.get("problem") is not None and
                    self._binding(fresh) != self._binding(scope.evaluate(EXTRACT)))):
                return {"unknown_outcome": True, "not_submitted": True, "reason": "Question changed before Submit"}
            if submit.evaluate("n => n.disabled || n.classList.contains('disabledButton')"):
                raise ValueError("Submit became disabled while answer fields settled")
            response_before = scope.evaluate(RESPONSE_STATE)
            self._intent(observation, "submit", responses=entered, response_before=response_before)
            submit.click()
        # Wait for evidence, never automatically click Submit twice after timeout.
        self.page.wait_for_function(RESPONSE_READY, arg={"selector": current["selector"], "before": response_before},
                                    timeout=self.timeout_ms())

    @staticmethod
    def _binding(item):
        # Asset paths are local evidence details; bind to the source prompt and
        # actual choices/field order, without result or editable current values.
        assets = item.get("assets", [])
        def image_identity(value, source_html=None, part=None):
            candidates = [asset for asset in assets if value in (
                asset.get("path"), f"@asset-{asset['index']}@")]
            # Identical image bytes can belong to distinct source occurrences.
            # A captured path alone cannot select the first matching asset.
            if len(candidates) > 1 and part:
                scoped = [asset for asset in candidates if asset.get('extraction_part') == part]
                if scoped:
                    candidates = scoped
            if len(candidates) > 1 and source_html:
                scoped = [asset for asset in candidates if asset.get('html') and asset['html'] in source_html]
                if scoped:
                    candidates = scoped
            identities = {fingerprint({k: asset.get(k) for k in
                ("tag", "source_url", "html")}) for asset in candidates}
            if not identities:
                return value
            if len(identities) != 1:
                return '<ambiguous-source-image:' + fingerprint(sorted(identities)) + '>'
            return "<source-image:" + next(iter(identities)) + ">"

        def clean(value, source_html=None, part=None):
            value = value or ""
            value = re.sub(r"!\[[^]]*\]\(([^)]+)\)",
                           lambda match: image_identity(match[1], source_html, part), value)
            # Tables retain HTML images so their layout survives extraction.
            # Compare their original source identity just like Markdown images;
            # collecting an asset changes its marker into a local file path.
            return re.sub(r'''(<img\b[^>]*?\s+src\s*=\s*)(["'])(.*?)\2''',
                          lambda match: match[1] + match[2] +
                          image_identity(match[3], source_html, part) + match[2],
                          value, flags=re.I | re.S)

        def choice_value(choice):
            value = choice.get("value")
            return (image_identity(value, choice.get('html'), 'fields') if choice.get("type") == "image"
                    else clean(value, choice.get('html'), 'fields'))
        return {"source_id": question_identity(item.get("dom_id"), item.get("html", "")),
                "problem": clean(item.get("problem"), item.get('html'), 'problem'),
                "fields": [{**{k: field.get(k) for k in ("key", "type", "tag", "dom_id")},
                            "choices": [{k: choice_value(choice) if k == "value" else choice.get(k)
                                         for k in ("option", "value", "type", "dom_id")} for choice in field.get("choices", [])]}
                           for field in item.get("fields", [])]}

    def _settle_entry(self, scope, fresh, entered):
        if any(field.get("tag") == "mathquill" and not field.get("disabled")
               and field.get("source_result") != "Correct" for field in fresh["fields"]):
            # Native blur dismisses the editor without MA's question-background
            # click handler, which clears radio choices. Let its initial 500ms
            # poll and a subsequent 200ms poll finish before readback.
            scope.locator('.mq-textarea textarea').evaluate_all('(editors) => editors.forEach(e => e.blur())')
            self.page.wait_for_function("() => [...document.querySelectorAll('[id=\"mathEditorToolbox\"]')].every(n => "
                "!n.getClientRects().length || ['hidden','collapse'].includes(getComputedStyle(n).visibility))",
                timeout=self.timeout_ms())
            self.pacer.sleep(.7, deadline=self.deadline_at)
        verify_entered(scope, fresh, entered)

    def _submit_assessment(self, observation, directory):
        self._check()
        view = self._view()
        if view["kind"] == "complete":
            return
        pending = self.state.get("pending_action", {})
        if pending.get("action") == "submit_assessment" and not self.state.get("restored"):
            self._goto(self.page.url)
            self.state["restored"] = True
            self._save()
            return {"unknown_outcome": True, "not_submitted": True}
        dialog = self.page.locator("#confirmationDialog:visible")
        if not dialog.count():
            self._intent(observation, "open_assessment_confirmation")
            by_id(self.page, "submitTestButton").click()
            dialog = by_id(self.page, "confirmationDialog")
            dialog.wait_for(state="visible")
        if not re.search(r"submit\s+this\s+test", dialog.inner_text(), re.I):
            raise BrowserUnavailable("Unexpected confirmation; retain the test and reread its page")
        self._pause("assessment confirmation", reserve=15)
        self._intent(observation, "submit_assessment")
        dialog.get_by_text("Yes", exact=True).click()
        self.page.locator("#finalScreen").wait_for(state="visible")
        self.state.pop("pending_action", None)
        self._save()

    def _select_continue_step(self, button):
        """Continue follows MA's selected step, which scrolling can change."""
        match = re.fullmatch(r"#continueButton-([teq]?\d+)", button)
        if not match:
            return
        token = match[1]
        step_button = self.page.locator("#stepButton-" + token)
        if not step_button.count():
            return  # Reviews and older lesson layouts need no step selection.
        control = self.page.locator(button)
        control.scroll_into_view_if_needed()
        self.pacer.sleep(getattr(self.config, "settle_ms", 1000) / 1000,
                         deadline=self.deadline_at)
        if "current" not in (step_button.get_attribute("class") or "").split():
            step_button.click()
            self.page.wait_for_function("id => document.getElementById(id)?.classList.contains('current')",
                                        arg="stepButton-" + token)

    def advance(self, observation, directory):
        current = self._view()
        pending = self.state.get("pending_action", {})
        if ("diagnostic_previous_key" in pending and pending["diagnostic_previous_key"] == current.get("key")
                and pending.get("action") == "advance" and not self.state.get("restored")):
            self._wait_diagnostic_transition(pending["diagnostic_previous_key"])
            self.state.pop("pending_action", None)
            self._save()
            return
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
        pending = self.state.get("pending_action", {})
        if (pending.get("action") == "advance" and pending.get("key") == observation.get("key")
                and not self.state.get("restored")):
            self._goto(self.page.url)
            self.state["restored"] = True
            self._save()
            return
        if current.get("action") == "decline_retry" and observation.get("retry_diagnostic"):
            retry = self.page.locator("#retryScreen-yesButton:visible")
            if retry.count():
                button = "#retryScreen-yesButton"
        transition = {}
        if current.get("action") == "decline_retry":
            title = self.page.locator("#questionContainer .questionWidget-title")
            number = re.search(r"Question\s+(\d+)", title.inner_text()) if title.count() else None
            transition["diagnostic_previous_key"] = "diagnostic-" + number[1] if number else None
        self._pause("continue activity")
        self._intent(observation, "advance", button=button, **transition)
        self._select_continue_step(button)
        self.page.locator(button).click()
        if transition:
            self._wait_diagnostic_transition(transition["diagnostic_previous_key"])
        else:
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
        if (current["kind"] != "unknown" and not (observation.get("source_view_kind") == current["kind"] and current.get("ready") is False)) or (current["kind"] == "unknown" and proposed not in current.get("buttons", [])):
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
        self._pause("recovery continuation")
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
                    self._pause("expand history explanation")
                    node.locator(".answerDetails").click()
                explanation.wait_for(state="visible")
                self._settle_content(explanation)
                item = self._read(node, directory, "history-" + info["math_academy_id"], context={"history_grade": info["grade"]})
                solution = self._read(explanation, directory, "history-solution-" + info["math_academy_id"],
                                      prior=self.state.get("live_records", {}).get(info["math_academy_id"]))
                item["worked_solution"] = solution["worked_solution"]
                item["assets"] = item.get("assets", []) + solution.get("assets", [])
                item["errors"] = list(dict.fromkeys(item.get("errors", []) + solution.get("errors", [])))
                error_history = deepcopy(item.get("extraction_error_history", []))
                for entry in solution.get("extraction_error_history", []):
                    if entry not in error_history:
                        error_history.append(deepcopy(entry))
                if error_history:
                    item["extraction_error_history"] = error_history
                item["extraction_parts"] = sorted(set(item.get("extraction_parts", [])) | set(solution.get("extraction_parts", [])))
                for error, parts in solution.get('extraction_error_parts', {}).items():
                    current = item.setdefault('extraction_error_parts', {}).get(error, [])
                    item['extraction_error_parts'][error] = sorted(set(current) | set(parts))
                item["solution_evidence"] = solution["html_path"]
            except StopRequested:
                raise
            except Exception as error:
                item = self._read(node, directory, "history-" + info["math_academy_id"], context={"history_grade": info["grade"]})
                message = "History expansion: " + str(error)
                item.setdefault("errors", []).append(message)
                item.setdefault('extraction_error_parts', {})[message] = ['solution']
            questions.append({**item, **info, "result": info["grade"],
                              "topic_id": info.get("topic_id") or activity.get("topic_id")})
        evidence = self._evidence(self.page, directory, "history-expanded")
        if any(not q.get('fields') for q in questions):
            from .history import HistoryChoices, task_answers
            renderer = None
            try:
                self._check()
                url = f"{BASE}/api/tasks/{activity['task_id']}/answers"
                response = self.context.request.get(url, timeout=self.timeout_ms())
                from ..storage import atomic_bytes
                raw = response.body()
                source = directory/'source'/('task-answers-'+hashlib.sha256(raw).hexdigest()+'.json')
                atomic_bytes(source,raw)
                atomic_json(source.with_suffix('.response.json'), {'url':url,'status':response.status,'observed_at':time.time()})
                if not response.ok:
                    raise BrowserUnavailable('Task answers source HTTP '+str(response.status))
                answers = task_answers(json.loads(raw),activity['task_id'])
                renderer = HistoryChoices(self.context,self.config.repo_root)
                for index, question in enumerate(questions):
                    if not question.get('fields') and question.get('math_academy_id') in answers:
                        try:
                            questions[index] = renderer.recover(question,answers[question['math_academy_id']],source,directory)
                        except ValueError as error:
                            question.setdefault('field_recovery_errors',[]).append(str(error))
            except StopRequested:
                raise
            except Exception as error:
                for question in questions:
                    if not question.get('fields'):
                        question.setdefault('field_recovery_errors',[]).append(str(error))
            finally:
                if renderer:
                    renderer.close()
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

    def lesson_source(self, topic_id, directory):
        """Read instructional source only; never start or submit an activity."""
        return self._lesson({'topic_id': str(topic_id), 'kind': 'lesson'}, directory)

    def _lesson(self, activity, directory):
        page = self.context.new_page()
        previous = self.page
        url = f"{BASE}/topics/{activity['topic_id']}"
        try:
            try:
                self._goto(url, page)
            except SourceHTTPError as error:
                # This supplementary read follows the completed task's history.
                # A persistently broken topic page must not replay that history
                # forever. Keep account/authentication/rate-limit failures on the
                # normal recovery path, and retain the missing source explicitly.
                if not 500 <= error.http_status < 600:
                    raise
                failures = self.state.setdefault('lesson_source_failures', {})
                previous_failure = failures.get(url, {})
                evidence = self._evidence(page, directory, 'lesson-topic-unavailable')
                failure = {'reason': str(error), 'source_url': url,
                           'source_file': evidence['html_path'], 'http_status': error.http_status,
                           'attempts': previous_failure.get('attempts', 0) + 1,
                           'first_failed_at': previous_failure.get('first_failed_at', time.time()),
                           'last_failed_at': time.time()}
                failures[url] = failure
                self._save()
                if failure['attempts'] < 3:
                    raise
                return {'lesson_definition': {'topic_id': activity['topic_id'], 'complete': False,
                                               'steps': [], 'issues': [deepcopy(failure)]}}
            except SourceUnavailable as error:
                evidence = self._evidence(page, directory, "lesson-topic-unavailable")
                return {"lesson_definition": {"topic_id": activity["topic_id"], "complete": False, "steps": [],
                                               "issues": [{"reason": str(error), "source_file": evidence["html_path"]}]}}
            if self.state.get('lesson_source_failures', {}).pop(url, None):
                self._save()
            try:
                page.locator("div.step[stepid][steptype][contentid]").first.wait_for(state="attached")
            except Exception:
                self._check(page)
            self.page = page
            try:
                self._settle_content(page.locator("#steps") if page.locator("#steps").count() else page.locator("body"))
            except Exception:
                check_stop(self.stop_event)
            definition = parse_lesson_structure(page.content(), activity["topic_id"])
            evidence = self._evidence(page, directory, "lesson-topic")
            definition.update(source_file=evidence["html_path"])
            examples, tutorials = [], []
            self.page = page
            for step in definition["steps"]:
                scope = page.locator(f'div.step[stepid="{step["math_academy_id"]}"]')
                readiness_error = None
                try:
                    self._settle_content(scope, step["type"])
                except Exception as error:
                    readiness_error = "Lesson source rendering: " + str(error)
                item = self._read(scope, directory, "lesson-step-" + str(step["math_academy_id"]))
                if readiness_error:
                    item.setdefault("errors", []).append(readiness_error)
                missing = not item.get("problem") or (step["type"] == "example" and not item.get("worked_solution"))
                if item.get("errors") or missing:
                    definition["complete"] = False
                    definition.setdefault("issues", []).append({"step": step["math_academy_id"],
                        "reason": "Incomplete lesson content or source extraction errors", "source_file": item["html_path"]})
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
        directory = capture_directory / "post-activity" / str(time.time_ns())
        page = self.context.new_page()
        result = {"task_id": str(activity["task_id"]), "account": self.config.account,
                  "completion": deepcopy(source_state.get("completion", {})), "courses": [], "pending_reads": [], "observed_at": time.time()}
        try:
            try:
                self._goto(LEARN, page)
                page.locator("#completedTasks").wait_for(state="attached")
                dashboard = parse_dashboard(page.content(), activity["task_id"])
                result.update(completed=dashboard["completed"],
                              dashboard={**self._evidence(page, directory, "dashboard"),
                                         "course_progress": dashboard["course_progress"]})
                if dashboard["activity"]:
                    result["completion"].update(dashboard["activity"])
                urls = dashboard["course_urls"]
            except StopRequested:
                raise
            except Exception as error:
                result["pending_reads"].append({"url": LEARN, "error": str(error)})
                urls = [f"{BASE}/courses/{self.config.course_id}/progress"] if self.config.course_id else []
            for url in urls:
                try:
                    self._goto(url, page)
                    page.locator(".moduleTopics .topicLink").first.wait_for(state="attached")
                    self.pacer.sleep(getattr(self.config, "settle_ms", 1000) / 1000, deadline=self.deadline_at)
                    course = parse_progress(page.content(), re.search(r"/courses/(\d+)", url)[1])
                    course.update(self._evidence(page, directory, "course-" + course["course_id"]))
                    result["courses"].append(course)
                except StopRequested:
                    raise
                except Exception as error:
                    result["pending_reads"].append({"url": url, "error": str(error), "failed_at": time.time()})
            result["completion"].update(task_id=str(activity["task_id"]), kind=activity["kind"], topic_id=activity.get("topic_id"))
            atomic_json(directory / "observations.json", result)
            return result
        finally:
            page.close()
