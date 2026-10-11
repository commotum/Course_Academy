"""Read source identities and metadata without making answer judgments."""
from __future__ import annotations

import re
from urllib.parse import urljoin

BASE = "https://mathacademy.com"
LEARN = BASE + "/learn"


def soup(html):
    from bs4 import BeautifulSoup
    return BeautifulSoup(html, "html.parser")


def text(node):
    return node.get_text(" ", strip=True) if node else ""


def number(value):
    match = re.search(r"\d+", str(value or ""))
    return int(match[0]) if match else None


def activity_from_url(url):
    """Use a forced active route when Learn redirects into an unfinished exam."""
    match = re.search(r"/tasks/(\d+)/(topics|tests|diagnostics|multisteps)/(\d+)(?:/(lesson|review))?", url)
    if not match:
        return None
    task, section, identifier, subtype = match.groups()
    kind = {"tests": "assessment", "diagnostics": "diagnostic", "multisteps": "multistep"}.get(section, subtype)
    if not kind:
        return None
    detail_key = {"assessment": "test_id", "diagnostic": "diagnostic_id", "multistep": "multistep_id"}.get(kind)
    return {"task_id": task, "kind": kind, "title": "", "url": urljoin(BASE, url),
            "started": True, "topic_id": identifier if section == "topics" else None,
            "course_id": None, "position": 0,
            "details": {detail_key: identifier} if detail_key else {}}


def parse_queue(html):
    page = soup(html)
    enrolled = page.select_one("a#courseNameLink, a.courseNameLink")
    course = re.search(r"/courses/(\d+)", enrolled.get("href", "")) if enrolled else None
    result = []
    cards = page.select("#incompleteTasks .taskUnlocked") or page.select(".taskUnlocked[id^='task-']")
    for position, card in enumerate(cards):
        start = card.select_one("a.taskStartButton")
        url = urljoin(BASE, start.get("href", "")) if start else ""
        route = activity_from_url(url) or {}
        kind = text(card.select_one(".taskTypeUnlocked")).lower() or route.get("kind", "unknown")
        values = {}
        for row in card.select(".testDetails tr"):
            name = text(row.select_one(".testFieldName")).rstrip(":")
            if name:
                values[name] = text(row.select_one(".testFieldValue"))
        try:
            progress = float(card.get("progress", 0))
        except (ValueError, TypeError):
            progress = None
        details = {**route.get("details", {}), "card_id": card.get("id"),
                   "start_id": start.get("id") if start else None,
                   "progress": progress, "source_fields": values,
                   "text": text(card), "html": str(card),
                   "links": [{"title": text(a), "url": urljoin(BASE, a["href"])} for a in card.select("a[href]")]}
        if kind == "assessment":
            details.update(question_count=number(values.get("Questions")), time_limit=values.get("Time Limit"),
                           requirement=values.get("Requirement") or values.get("Required"),
                           retake=bool(re.search(r"retake", text(card), re.I)))
        task_id = route.get("task_id") or str(number(card.get("id")) or "")
        result.append({"task_id": task_id, "kind": kind,
                       "title": text(card.select_one("[id^='taskName-'], .taskNameUnlocked")),
                       "url": url, "started": bool(progress and progress > 0) or bool(re.search(r"resume|continue", text(start), re.I)),
                       "topic_id": route.get("topic_id"), "course_id": course[1] if course else None,
                       "position": position, "details": details})
    return result


def question_identity(dom_id, html="", diagnostic=False):
    match = re.fullmatch(r"step-([qe])(\d+)", dom_id or "")
    if match:
        return match[1] + "-" + match[2]
    if not diagnostic:
        match = re.fullmatch(r"question-(\d+)", dom_id or "")
        if match:
            return "q-" + match[1]
    # Diagnostic questionContainer has no permanent ID; field IDs sometimes do.
    match = re.search(r'(?:questionWidget-choiceLetterCircle-|selectList-)(\d+)-', html)
    return "q-" + match[1] if match else None


def parse_history_metadata(html):
    page = soup(html)
    result = []
    for position, node in enumerate(page.select(".question[id^='question-']"), 1):
        match = re.fullmatch(r"question-(\d+)", node.get("id", ""))
        if not match:
            continue
        kp = node.select_one(".questionKP")
        parent = node.find_parent(class_="kp")
        kp_title = text(kp) or text(parent.select_one(".kpTitle") if parent else None)
        href = kp.get("href", "") if kp else ""
        source = re.search(r"/topics/(\d+)#(\d+)", href)
        grade = text(node.select_one(".answerResult"))
        result.append({"math_academy_id": "q-" + match[1], "dom_id": node["id"],
                       "sequence_position": number(text(node.select_one(".questionNumber"))) or position,
                       "difficulty": {"E": "easy", "M": "moderate", "H": "hard"}.get(text(node.select_one(".questionDifficulty"))),
                       "knowledge_point": re.sub(r"^KP\s+\d+\.\s*", "", kp_title),
                       "topic_id": source[1] if source else None,
                       "knowledge_point_source_id": int(source[2]) if source else None,
                       "kp_href": href, "grade": "Correct" if grade == "Full Credit" else grade,
                       "source_grade": grade, "raw_html": str(node)})
    return result


def parse_lesson_structure(html, topic_id):
    page = soup(html)
    steps = []
    issues = []
    for position, node in enumerate(page.select("div.step[stepid][steptype][contentid]")):
        kind = node["steptype"]
        name = re.sub(r"^Example:\s*", "", text(node.select_one(".stepName")))
        placement, content = number(node["stepid"]), number(node["contentid"])
        if not placement or not content or kind not in ("tutorial", "example"):
            issues.append({"reason": "unknown_source_step", "html": str(node)})
        steps.append({"math_academy_id": placement, "type": kind, "content_id": content,
                      "title": name, "position": position, "dom_id": node.get("id"), "html": str(node)})
    title = text(page.select_one("#topicName"))
    if not title or not steps:
        issues.append({"reason": "lesson_definition_missing"})
    ids = [x["math_academy_id"] for x in steps]
    if len(set(ids)) != len(ids):
        issues.append({"reason": "duplicate_placement_identity"})
    return {"topic_id": str(topic_id), "title": title, "steps": steps,
            "complete": not issues, "issues": issues, "source_url": f"{BASE}/topics/{topic_id}"}


def parse_xp(value):
    match = re.search(r"(-?\d+)\s*(?:/|of)\s*(\d+)(?:\s*XP)?", value, re.I)
    if match:
        return {"earned_xp": int(match[1]), "base_xp": int(match[2]), "source_text": value}
    match = re.search(r"(-?\d+)\s*XP", value, re.I)
    return {"earned_xp": int(match[1]) if match else None, "base_xp": None, "source_text": value}


def parse_dashboard(html, task_id):
    page = soup(html)
    rows = []
    for node in page.select("#completedTasks .taskCompleted"):
        tid = str(number(node.get("id")) or "")
        topic = node.select_one("a[id^='taskTopicLink-']")
        rows.append({"task_id": tid, "kind": text(node.select_one(".taskTypeLocked")).lower(),
                     "topic_id": str(number(topic.get("href"))) if topic else None,
                     **parse_xp(text(node.select_one(".taskPoints"))), "html": str(node)})
    selected = next((row for row in rows if row["task_id"] == str(task_id)), {})
    urls = []
    for link in page.select("a#courseNameLink[href], a.courseNameLink[href], #sequenceUnits a.courseUnitLink[href]"):
        match = re.search(r"/courses/(\d+)/progress", link["href"])
        if match:
            url = f"{BASE}/courses/{match[1]}/progress"
            if url not in urls:
                urls.append(url)
    return {"completed": rows, "activity": selected, "course_urls": urls}


def parse_progress(html, course_id):
    page = soup(html)
    topics = []
    for row in page.select(".moduleTopics tr"):
        link = row.select_one(".topicLink")
        match = re.search(r"/topics/(\d+)", link.get("href", "")) if link else None
        if not match:
            continue
        circle = row.select_one(".topicCircle")
        topics.append({"topic_id": match[1], "title": text(link), "href": link["href"],
                       "circle_style": circle.get("style") if circle else None,
                       "displayed_progress": text(row.select_one(".topicProgress"))})
    return {"course_id": str(course_id), "topics": topics,
            "displayed_progress": text(page.select_one("#courseProgress, .courseProgress, #courseCompletion"))}
