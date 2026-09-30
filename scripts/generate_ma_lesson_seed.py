#!/usr/bin/env python3
"""Generate staged EDB lesson imports from the captured MA JSON and Markdown."""

import collections
import argparse
import csv
import json
import re
import uuid
from pathlib import Path

import yaml


ROOT = Path("/home/jake/Developer/MA/DATA")
LESSONS = ROOT / "Lessons"
OUTPUT = Path(".local/edb/lesson-seed")
CHUNK_TOPICS = 75
QUESTION_MARKER = re.compile(r"^\*\*Question (\d+)(?::\*\*|\*\*)", re.M)
HEADING = re.compile(r"^## (.+)\n", re.M)
OPTION = re.compile(r"^- \[ \] ([A-Z])\.(.*)$", re.M)
UNDERLINE = re.compile(r"\$\s*\\underline\{\\hspace\{[^}]*\}\}\s*\$")
MATH_MARKER = re.compile(r"^\[MATH: (.*)\]$", re.S)
IMAGE_MARKER = re.compile(r"^\[IMG: (.*)\]$", re.S)


def source_rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def ident(kind, source):
    return uuid.uuid5(uuid.NAMESPACE_URL, f"course-academy:ma:{kind}:{source}")


def uuid_edn(value):
    return f'#uuid "{value}"'


def string(value):
    return json.dumps(value, ensure_ascii=False)


def ref(kind, source):
    return string(f"{kind}-{source}")


def image_path(topic, src):
    name = Path(src).name
    local = LESSONS / topic / "Source" / "Images" / f"{name}.png"
    return str(local) if local.exists() else src


def markdown_images(text, topic):
    return re.sub(
        r"\]\(Source/Images/([^)]+)\)",
        lambda match: "](" + str(LESSONS / topic / "Source" / "Images" / match[1]) + ")",
        text,
    )


def readable_value(text, topic):
    text = text.strip()
    image = IMAGE_MARKER.fullmatch(text)
    if image:
        return "image", image_path(topic, image[1])
    math = MATH_MARKER.fullmatch(text)
    if math:
        return "math", math[1].strip()
    text = re.sub(r"\[MATH: (.*?)\]", lambda match: "$" + match[1] + "$", text)
    text = re.sub(
        r"\[IMG: (.*?)\]",
        lambda match: "![](" + image_path(topic, match[1]) + ")",
        text,
    )
    return "text", text


def answer_value(source, markdown, topic):
    if source.get("content_type") == "image":
        images = source.get("images", [])
        assert len(images) == 1, (topic, source)
        return "image", image_path(topic, images[0]["src"])
    if markdown:
        markdown = markdown_images(markdown.strip(), topic)
        match = re.fullmatch(r"\$([^$]+)\$", markdown, re.S)
        if match:
            return "math", match[1].strip()
        return "text", markdown
    return readable_value(source["readable_text"], topic)


def question_blocks(markdown, questions):
    marks = list(QUESTION_MARKER.finditer(markdown))
    heads = list(HEADING.finditer(markdown))
    assert len(marks) == len(questions), (len(marks), len(questions))
    blocks = []
    for index, (mark, question) in enumerate(zip(marks, questions)):
        assert int(mark[1]) == question["question_number"]
        ends = [len(markdown)]
        if index + 1 < len(marks):
            ends.append(marks[index + 1].start())
        ends.extend(head.start() for head in heads if head.start() > mark.start())
        block = markdown[mark.end() : min(ends)].strip()
        block = re.sub(r"(?:\n\s*---\s*)+$", "", block).strip()
        blocks.append(block)
    return blocks


def question_parts(block, question, topic):
    quiz_blocks = re.findall(r"```quiz\n(.*?)\n```", block, re.S)
    if quiz_blocks:
        parsed = yaml.safe_load(quiz_blocks[0])
        problem = parsed["content"].strip()
        options = [option["content"].strip() for option in parsed.get("options", [])]
    else:
        boundaries = [
            match.start()
            for regex in (OPTION, re.compile(r"^#### (?:Choices|Select)\b", re.M))
            for match in regex.finditer(block)
        ]
        problem = block[: min(boundaries)].strip() if boundaries else block.strip()
        marks = list(OPTION.finditer(block))
        options = []
        for index, mark in enumerate(marks):
            end = marks[index + 1].start() if index + 1 < len(marks) else len(block)
            option = (mark[2] + block[mark.end() : end]).strip()
            options.append(re.sub(r"(?:\n\s*---\s*)+$", "", option).strip())
    if question["question_format"] == "multiple-choice":
        if len(options) != len(question["choices"]):
            options = []  # Tables and some other rich options use the JSON fallback.
    else:
        options = []
        expected = len(question["free_entry_blanks"] or question["select_lists"])
        assert len(UNDERLINE.findall(problem)) == expected, (topic, question["question_id"])
        number = iter(range(1, expected + 1))
        problem = UNDERLINE.sub(lambda _: "{{field-" + str(next(number)) + "}}", problem)
    problem = markdown_images(problem, topic)
    assert problem, (topic, question["question_id"])
    return problem, options


def answer_map(identity, representation, value):
    assert representation in {"math", "text", "image"} and value
    return (
        f'{{:answer/id {uuid_edn(identity)} :answer/type :answer.type/{representation} '
        f':answer/value {string(value)} :db/ensure :answer/validate}}'
    )


def question_form(question, markdown, topic, duplicates):
    qid = question["question_id"]
    qkey = f"{topic}:{qid}" if qid in duplicates else qid
    q_uuid = ident("question", qkey)
    problem, markdown_options = question_parts(markdown, question, topic)
    kind = question["question_format"]
    assert kind in {"multiple-choice", "free-response", "select-list"}
    fields = []
    if kind == "multiple-choice":
        sources = question["choices"]
        choices = []
        seen = set()
        for index, source in enumerate(sources, 1):
            md = markdown_options[index - 1] if markdown_options else None
            representation, value = answer_value(source, md, topic)
            if (representation, value) in seen:
                continue
            seen.add((representation, value))
            choices.append(answer_map(ident("answer", f"{qkey}:1:{index}"), representation, value))
        fields.append(
            f'{{:answer-field/id {uuid_edn(ident("field", f"{qkey}:1"))} '
            f':answer-field/key "selection" :answer-field/type :answer-field.type/radio '
            f':answer-field/choices [{" ".join(choices)}]}}'
        )
    elif kind == "free-response":
        for index, _ in enumerate(question["free_entry_blanks"], 1):
            fields.append(
                f'{{:answer-field/id {uuid_edn(ident("field", f"{qkey}:{index}"))} '
                f':answer-field/key "field-{index}" :answer-field/type :answer-field.type/blank}}'
            )
    else:
        for index, select in enumerate(question["select_lists"], 1):
            choices = []
            seen = set()
            for cindex, option in enumerate(select["options"], 1):
                representation, value = readable_value(option["readable_text"], topic)
                if (representation, value) in seen:
                    continue
                seen.add((representation, value))
                choices.append(answer_map(ident("answer", f"{qkey}:{index}:{cindex}"), representation, value))
            fields.append(
                f'{{:answer-field/id {uuid_edn(ident("field", f"{qkey}:{index}"))} '
                f':answer-field/key "field-{index}" :answer-field/type :answer-field.type/select '
                f':answer-field/choices [{" ".join(choices)}]}}'
            )
    assert fields, (topic, qid)
    pieces = [
        f':db/id {ref("question", qkey)}',
        f':question/id {uuid_edn(q_uuid)}',
        ':question/is-example false',
        f':question/problem {string(problem)}',
        f':question/answer-fields [{" ".join(fields)}]',
    ]
    if qid not in duplicates:
        pieces.insert(2, f':question/math-academy-id {string("q-" + qid)}')
    if question["calculator_instructions"]["readable_text"].strip():
        pieces.insert(-1, ':question/requires-calculator true')
    # The source does not establish correct answers, so field/question specs are
    # deliberately not ensured yet. Captured choice values are still stored.
    return " {" + " ".join(pieces) + "}"


def step_blocks(markdown, steps):
    parts = HEADING.split(markdown)
    blocks = [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]
    blocks = [(title, body) for title, body in blocks if title not in ("Table of Contents", "Prerequisites")]
    assert len(blocks) == len(steps), (len(blocks), len(steps))
    assert all(title == step["title"] for (title, _), step in zip(blocks, steps))
    return blocks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    sources = sorted(LESSONS.glob("*/Source/*.json"), key=lambda path: int(path.stem))
    assert len(sources) == 2964
    all_questions = source_rows("Lesson-Data/Questions.csv")
    question_counts = collections.Counter(row["question-id"] for row in all_questions)
    duplicate_questions = {qid for qid, count in question_counts.items() if count > 1}
    assert duplicate_questions == {"56649", "156726"}
    content_counts = collections.Counter()
    for path in sources:
        data = json.loads(path.read_text())
        content_counts.update((item["step_type"], item["content_id"]) for item in data["lesson"]["items"] if item["item_type"] == "step")
    duplicate_contents = {key for key, count in content_counts.items() if count > 1}
    assert len(duplicate_contents) == 4
    key_prereqs = collections.defaultdict(list)
    for row in source_rows("Lesson-Data/Key-Prerequisites.csv"):
        key_prereqs[row["step-id"]].append(row["requires"])
    totals = collections.Counter()
    chunk = []
    batches = []
    for position, path in enumerate(sources, 1):
        topic = path.stem
        data = json.loads(path.read_text())
        assert data["topic_id"] == topic
        markdown = (path.parent.parent / f"{topic}.md").read_text()
        items = data["lesson"]["items"]
        steps = [item for item in items if item["item_type"] == "step"]
        questions = [item for item in items if item["item_type"] == "question"]
        blocks = step_blocks(markdown, steps)
        qblocks = question_blocks(markdown, questions)
        bodies = dict(zip((item["step_id"] for item in steps), (body for _, body in blocks)))
        per_step_questions = collections.defaultdict(list)
        previous_step = None
        for item in items:
            if item["item_type"] == "step":
                previous_step = item
            else:
                assert previous_step and previous_step["step_type"] == "example"
                per_step_questions[previous_step["step_id"]].append(item)
        for step in steps:
            sid, cid = step["step_id"], step["content_id"]
            body = bodies[sid].split("\n---\n", 1)[0].strip()
            if step["step_type"] == "tutorial":
                content = markdown_images(body, topic)
                assert content
                key = sid if ("tutorial", cid) in duplicate_contents else cid
                fields = [f':db/id {ref("tutorial", key)}', f':tutorial/id {uuid_edn(ident("tutorial", key))}']
                if ("tutorial", cid) not in duplicate_contents:
                    fields.append(f":tutorial/math-academy-id {cid}")
                fields.extend([f':tutorial/title {string(step["title"])}', f':tutorial/content {string(content)}', ':db/ensure :tutorial/validate'])
                chunk.append(" {" + " ".join(fields) + "}")
                totals["tutorials"] += 1
            else:
                match = re.match(r"\*\*Example:\*\*\s*(.*?)\n\n\*\*Explanation\*\*\s*(.*)", body, re.S)
                assert match and match[1].strip() and match[2].strip(), (topic, sid)
                problem, explanation = (markdown_images(part.strip(), topic) for part in match.groups())
                key = sid if ("example", cid) in duplicate_contents else cid
                fields = [f':db/id {ref("example", key)}', f':question/id {uuid_edn(ident("example", key))}']
                if ("example", cid) not in duplicate_contents:
                    fields.append(f':question/math-academy-id {string("e-" + cid)}')
                fields.extend([':question/is-example true', f':question/problem {string(problem)}',
                               f':question/worked-solution {string(explanation)}', ':db/ensure :question/validate'])
                chunk.append(" {" + " ".join(fields) + "}")
                totals["examples"] += 1
        for question, block in zip(questions, qblocks):
            form = question_form(question, block, topic, duplicate_questions)
            chunk.append(form)
            totals["questions"] += 1
            totals["fields"] += 1 if question["question_format"] == "multiple-choice" else len(question["free_entry_blanks"] or question["select_lists"])
            totals["choices"] += len(question["choices"]) + sum(len(s["options"]) for s in question["select_lists"])
            totals["emitted_choices"] += form.count(':answer/id ')
        kp_refs = []
        for step in steps:
            if step["step_type"] != "example":
                continue
            sid, cid = step["step_id"], step["content_id"]
            key = sid if ("example", cid) in duplicate_contents else cid
            qrefs = []
            for question in per_step_questions[sid]:
                qid = question["question_id"]
                qkey = f"{topic}:{qid}" if qid in duplicate_questions else qid
                qrefs.append(ref("question", qkey))
            assert qrefs
            prereqs = " ".join(f"[:topic/math-academy-id {mid}]" for mid in sorted(set(key_prereqs[sid]), key=int))
            fields = [
                f':db/id {ref("knowledge-point", sid)}',
                f':knowledge-point/id {uuid_edn(ident("kp", sid))}',
                f':knowledge-point/title {string(step["title"])}',
                f':knowledge-point/canonical-example {ref("example", key)}',
                f':knowledge-point/questions [{" ".join(qrefs)}]',
                ':db/ensure :knowledge-point/identity-validate',
            ]
            if prereqs:
                fields.insert(-1, f":knowledge-point/key-prerequisites [{prereqs}]")
            chunk.append(" {" + " ".join(fields) + "}")
            kp_refs.append(ref("knowledge-point", sid))
            totals["knowledge_points"] += 1
        step_refs = []
        for index, step in enumerate(steps):
            sid, cid = step["step_id"], step["content_id"]
            if step["step_type"] == "tutorial":
                key = sid if ("tutorial", cid) in duplicate_contents else cid
                content = ref("tutorial", key)
            else:
                content = ref("knowledge-point", sid)
            fields = [f':db/id {ref("step", sid)}', f':step/id {uuid_edn(ident("step", sid))}', f':step/math-academy-id {sid}', f":step/content {content}"]
            if index + 1 < len(steps):
                fields.append(f':step/next {ref("step", steps[index + 1]["step_id"])}')
            fields.append(':db/ensure :step/validate')
            chunk.append(" {" + " ".join(fields) + "}")
            step_refs.append(ref("step", sid))
            totals["steps"] += 1
        assert step_refs and kp_refs
        chunk.append(
            f' {{:db/id {ref("lesson", topic)} :activity/id {uuid_edn(ident("lesson", topic))} :activity/title {string(data["topic_title"])} '
            f':activity/type :activity.type/lesson :activity/scope [:topic/math-academy-id {topic}] '
            f':activity/steps [{" ".join(step_refs)}] :activity/first-step {step_refs[0]} :db/ensure :activity/validate}}'
        )
        chunk.append(
            f' {{:db/id [:topic/math-academy-id {topic}] :topic/knowledge-points [{" ".join(kp_refs)}] :db/ensure :topic/validate}}'
        )
        totals["lessons"] += 1
        if position % CHUNK_TOPICS == 0 or position == len(sources):
            filename = f"lessons-{len(batches) + 1:04d}.edn"
            path_out = output / filename
            path_out.write_text(
                ";; Staged MA lesson import: answers are unverified; question/field specs are not ensured.\n[\n"
                + "\n".join(chunk)
                + "\n]\n",
                encoding="utf-8",
            )
            batches.append({"file": filename, "topics": min(CHUNK_TOPICS, len(sources) - (position // CHUNK_TOPICS) * CHUNK_TOPICS) if position == len(sources) else CHUNK_TOPICS, "bytes": path_out.stat().st_size})
            chunk = []
    assert totals["tutorials"] == 6016
    assert totals["examples"] == totals["knowledge_points"] == 9636
    assert totals["questions"] == 19646
    assert totals["steps"] == 15652 and totals["lessons"] == 2964
    (output / "manifest.json").write_text(json.dumps({"totals": totals, "batches": batches, "duplicate_content_ids": sorted(map(str, duplicate_contents)), "duplicate_question_ids": sorted(duplicate_questions)}, indent=2) + "\n")
    print(dict(totals), "batches", len(batches), "largest", max(batch["bytes"] for batch in batches))


if __name__ == "__main__":
    main()
