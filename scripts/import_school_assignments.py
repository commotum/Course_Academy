#!/usr/bin/env python3
"""Prepare the four reviewed F26 assignments as deterministic EDB transactions.

This writes a reviewable EDN file and a source audit; it never transacts or changes
the vault. The reviewed coverage below is per problem, not every linked lesson.
Rerunning the same source produces the same identities and transaction content.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import uuid
from datetime import date, datetime, time, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT.parent / "study/vault"
DEFAULT_LEARNER = "59d5cf13-351c-4114-be19-4c3bb64ee051"
LINK = re.compile(r'(!?)\[([^\]]*)\]\((?:<([^>]+)>|([^\s)]+))\)')
PROBLEM = re.compile(r'^## Problem (\d+)\s*$', re.M)
PART = re.compile(r'^\*\*\(([a-z])\)\*\*\s*', re.M)
MATCH_LINE = re.compile(r'^\*\*(?:Math Academy match|Supporting prerequisite|Supporting lessons for long-term behavior):\*\*.*(?:\n|$)', re.M)

# These decisions come from each assignment's Math Academy Matches.md. Supporting
# skills do not claim that an unmatched proof or drawing task is fully covered.
SOURCES = [
    {
        "path": "F26/255/W1 09-27/R1 09-29/R1 09-29.md",
        "problems": {
            "1": {"direct": [1938], "supporting": [1939], "coverage": "partial", "note": "Directional derivatives covers (a)-(c). Gradient normals supports (d), but constructing two mutually orthogonal zero-change directions is not fully covered."},
            "2": {"direct": [1837], "supporting": [], "coverage": "direct", "note": "3D differentiation, speed, and arc length are covered. The worksheet also isolates differential notation."},
            "3": {"direct": [2835], "supporting": [2030], "coverage": "partial", "note": "Polar conversion and evaluation in (a) are covered. Polar integration supports (b), but the Gaussian-integral deduction has no verified equivalent."},
            "4": {"direct": [1936, 3173], "supporting": [], "coverage": "direct", "note": "Vector chain rule for the helix; general multivariable chain rule for the cone. Preserve the reflection prompts."},
            "5": {"direct": [3173], "supporting": [1942], "coverage": "direct", "note": "General chain-rule computation, with spherical-coordinate formulas supplied by the polar-coordinate lesson."},
            "6": {"direct": [2059], "supporting": [], "coverage": "partial", "note": "Cylindrical bounds in (a) are covered. The general shell-formula proof in (b) has no verified equivalent."},
        },
    },
    {
        "path": "F26/256/W1 09-27/OHW-1/OHW-1.md",
        "problems": {
            "1": {"direct": [6679], "supporting": [], "coverage": "direct", "note": "Nonresonant exponential-forcing IVP."},
            "2": {"direct": [6679], "supporting": [], "coverage": "direct", "note": "Two forcing exponentials, including a resonant term, with an initial condition."},
            "3": {"direct": [1179], "supporting": [], "coverage": "direct", "note": "Separable trigonometric IVP; integrating factors are an alternative rather than another required target."},
            "4": {"direct": [877], "supporting": [], "coverage": "direct", "note": "Integrating factor, general solution, and IVP on an interval containing x=1 but excluding x=0."},
            "5": {"direct": [877], "supporting": [], "coverage": "direct", "note": "Linear IVP with shifted reciprocal coefficient and rational forcing; retain both singularities."},
            "6": {"direct": [877], "supporting": [], "coverage": "direct", "note": "Integrating factor cancels an exponential of the independent variable squared."},
        },
    },
    {
        "path": "F26/256/W1 09-27/R1 09-29/R1 09-29.md",
        "problems": {
            "1": {"direct": [1109, 1007], "supporting": [308], "coverage": "partial", "note": "Product rule and exponential chain rule cover (a)-(c). The antiderivative relation supports (d), but its combined symbolic task has no verified equivalent exercise."},
            "2": {"direct": [1061], "supporting": [], "coverage": "direct", "note": "Direct-integration IVPs for all four subparts."},
            "3": {"direct": [877], "supporting": [], "coverage": "direct", "note": "Reverse product rule and integrating-factor IVP workflow; the product factor is already supplied."},
        },
    },
    {
        "path": "F26/256/W1 09-27/WHW-1/WHW-1.md",
        "problems": {
            "1": {"direct": [1181], "supporting": [], "coverage": "direct", "note": "Verify a supplied solution by differentiation and substitution. Preserve x>c for real powers."},
            "2": {"direct": [6700], "supporting": [1924, 649], "coverage": "direct", "note": "Constant input minus proportional removal, solved symbolically. Growth/decay models support the limit without assuming G0 is below equilibrium."},
            "3": {"direct": [], "supporting": [3352], "coverage": "supporting-only", "shared_images": True, "note": "Reading the direction field is supported. No complete equivalent found for drawing integral, solution, and nonintegral curves; preserve the supplied equation and diagram."},
            "4": {"direct": [], "supporting": [3352], "coverage": "supporting-only", "shared_images": True, "note": "Reading the direction field is supported. No complete equivalent found for the three sketches; no differential equation is supplied and none is inferred from the image."},
        },
    },
]


def stable_id(relative_path: str, local_key: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"course-academy:school:{relative_path}#{local_key}"))


def tidy(value: str) -> str:
    value = re.sub(r'^---\s*$', '', value, flags=re.M)
    return re.sub(r'\n{3,}', '\n\n', value).strip()


def edn(value) -> str:
    if isinstance(value, dict):
        if "$uuid" in value:
            return '#uuid ' + json.dumps(value["$uuid"])
        if "$inst" in value:
            return '#inst ' + json.dumps(value["$inst"])
        if "$ref" in value:
            return '[%s %s]' % (value["$ref"][0], edn(value["$ref"][1]))
        return '{' + '\n  '.join(f'{key} {edn(item)}' for key, item in value.items()) + '}'
    if isinstance(value, list):
        return '[' + ' '.join(edn(item) for item in value) + ']'
    if isinstance(value, str):
        return value if value.startswith(':') else json.dumps(value, ensure_ascii=False)
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, int):
        return str(value)
    raise TypeError(value)


class Import:
    def __init__(self, vault: Path, due_dates: dict):
        self.vault = vault.resolve()
        self.due_dates = due_dates
        self.entities = []
        self.assets = {}
        self.audit = []

    def entity(self, source: str, key: str, kind: str, **attributes) -> str:
        identity = stable_id(source, key)
        record = {":db/id": identity, f":{kind}/id": {"$uuid": identity}}
        record.update({':' + k.replace('__', '/').replace('_', '-'): v for k, v in attributes.items()})
        record[':db/ensure'] = f':{kind}/validate'
        self.entities.append(record)
        return identity

    def links(self, value: str, source: Path) -> str:
        def replace(match):
            image, label, angled, plain = match.groups()
            path = angled or plain
            if urlsplit(path).scheme or path.startswith('#'):
                return match.group()
            file = (source.parent / unquote(path)).resolve()
            if not file.is_relative_to(self.vault) or not file.is_file():
                raise ValueError(f'Missing or external asset: {source}: {path}')
            if image and file.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'}:
                raise ValueError(f'Unsupported image: {file}')
            if not image and file.suffix.lower() != '.pdf':
                raise ValueError(f'Unexpected source link in assignment content: {file}')
            route = '/api/asset?path=' if image else '/api/source?path='
            self.assets[str(file)] = {"path": str(file), "sha256": hashlib.sha256(file.read_bytes()).hexdigest(), "kind": "image" if image else "pdf"}
            return f'{image}[{label}]({route}{quote(str(file), safe="")})'
        return LINK.sub(replace, value)

    def sequence(self, source: str, keys: list[str], contents: list[str]) -> list[str]:
        assert len(keys) == len(contents)
        ids = [stable_id(source, key) for key in keys]
        for i, content in enumerate(contents):
            attrs = {'step__content': content}
            if i + 1 < len(contents):
                attrs['step__next'] = ids[i + 1]
            self.entity(source, keys[i], 'step', **attrs)
        return ids

    def build_assignment(self, spec: dict) -> str:
        relative = spec['path']
        path = self.vault / relative
        text = path.read_text(encoding='utf-8')
        markers = list(PROBLEM.finditer(text))
        expected = list(spec['problems'])
        if [m[1] for m in markers] != expected:
            raise ValueError(f'Problem list changed in {relative}; review coverage before importing')
        if '```' in text:
            raise ValueError(f'Quiz/code blocks need a dedicated reviewed conversion: {relative}')
        title = re.match(r'^# (.+)$', text, re.M)[1]
        intro = text[:markers[0].start()]
        intro = re.sub(r'^# .+\n', '', intro, count=1)
        intro = re.sub(r'^\[Math Academy lesson matches\].*\n', '', intro, flags=re.M)
        intro = re.sub(r'^## (?:Prerequisites|Lessons)\n.*?(?=^## |\Z)', '', intro, flags=re.M | re.S)
        intro = self.links(tidy(intro), path)
        tutorial = self.entity(relative, 'instructions', 'tutorial', tutorial__title='Assignment information', tutorial__content=intro)
        contents = [tutorial]
        problem_audit = []
        for i, marker in enumerate(markers):
            number = marker[1]
            raw = text[marker.end():markers[i + 1].start() if i+1 < len(markers) else len(text)]
            body = tidy(MATCH_LINE.sub('', raw))
            body = self.links(body, path)
            parts = list(PART.finditer(body))
            mapping = spec['problems'][number]
            if parts:
                # Move a trailing shared diagram only after a source review says
                # it applies to every part. Other images retain their positions.
                images = [m[0] for m in LINK.finditer(body) if m[1] == '!'] if mapping.get('shared_images') else []
                if images:
                    body = LINK.sub(lambda m: '' if m[1] == '!' else m[0], body)
                parts = list(PART.finditer(body))
                context = tidy(body[:parts[0].start()])
                if images:
                    context = tidy(context + '\n\n' + '\n\n'.join(images))
                questions = []
                for j, part in enumerate(parts):
                    statement = tidy(body[part.end():parts[j+1].start() if j+1 < len(parts) else len(body)])
                    questions.append(self.entity(relative, f'problem-{number}/part-{part[1]}', 'question', question__is_example=False, question__problem=f'**({part[1]})** {statement}'))
                inner = self.sequence(relative, [f'problem-{number}/part-{p[1]}/step' for p in parts], questions)
                attrs = {'multistep__steps': inner, 'multistep__first_step': inner[0]}
                if context:
                    attrs['multistep__context'] = context
                content = self.entity(relative, f'problem-{number}/multistep', 'multistep', **attrs)
            else:
                content = self.entity(relative, f'problem-{number}/question', 'question', question__is_example=False, question__problem=body)
            topics = sorted(set(mapping['direct'] + mapping['supporting']))
            attrs = {'assigned_problem__content': content}
            if topics:
                attrs['assigned_problem__topic_coverage'] = [{'$ref': [':topic/math-academy-id', t]} for t in topics]
            assigned = self.entity(relative, f'problem-{number}', 'assigned-problem', **attrs)
            contents.append(assigned)
            problem_audit.append({"number": int(number), "assigned_problem_id": assigned, "content_id": content, "parts": [p[1] for p in parts], "topics": topics, **mapping})
        steps = self.sequence(relative, ['instructions/step'] + [f'problem-{n}/step' for n in expected], contents)
        attrs = dict(activity__title=title, activity__type=':activity.type/assignment', activity__steps=steps, activity__first_step=steps[0])
        supplied_due = self.due_dates.get(relative)
        due = None
        if supplied_due:
            if re.fullmatch(r'\d{4}-\d{2}-\d{2}', supplied_due):
                parsed = datetime.combine(date.fromisoformat(supplied_due), time(23, 59, 59), ZoneInfo('America/Los_Angeles'))
            else:
                parsed = datetime.fromisoformat(supplied_due.replace('Z', '+00:00'))
                if parsed.tzinfo is None:
                    raise ValueError('Deadline timestamps require an explicit timezone')
            due = parsed.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
            attrs['activity__due'] = {'$inst': due}
        activity = self.entity(relative, 'activity', 'activity', **attrs)
        self.audit.append({"source": relative, "sha256": hashlib.sha256(text.encode()).hexdigest(), "title": title, "activity_id": activity, "due": due, "due_evidence": f"Explicit supplied deadline: {supplied_due}; date-only values mean 23:59:59 America/Los_Angeles." if supplied_due else "No deadline in assignment Markdown, source PDF, or adjacent course notes. Date/imported date retained only as labeled source information.", "match_report": str(path.parent / 'Math Academy Matches.md'), "problems": problem_audit})
        return activity

    def validate(self):
        records = {r[':db/id']: r for r in self.entities}
        if len(records) != len(self.entities):
            raise ValueError('Duplicate identities')
        owners = collections.defaultdict(list)
        for eid, row in records.items():
            for attr in (':activity/steps', ':multistep/steps'):
                for child in row.get(attr, []):
                    owners[child].append(eid)
            if ':question/id' in row:
                assert row[':question/problem'].strip()
                assert row[':question/is-example'] is False
                assert ':question/answer-fields' not in row
                assert ':question/math-academy-id' not in row
        for eid, row in records.items():
            if ':step/id' in row:
                assert len(owners[eid]) == 1
                assert row[':step/content'] in records
                if ':step/next' in row:
                    assert owners[row[':step/next']] == owners[eid]
            if ':assigned-problem/id' in row:
                child = records[row[':assigned-problem/content']]
                assert ':question/id' in child or ':multistep/id' in child
            for prefix in ('activity', 'multistep'):
                if f':{prefix}/steps' not in row:
                    continue
                owned = set(row[f':{prefix}/steps'])
                visited = set()
                cursor = row[f':{prefix}/first-step']
                while cursor:
                    assert cursor in owned and cursor not in visited
                    visited.add(cursor)
                    cursor = records[cursor].get(':step/next')
                assert visited == owned

    def transaction(self, snapshot: dict, learner: str, activities: list[str]):
        """Emit only new facts; refuse silent reconciliation of changed imports."""
        rows = snapshot['entities']
        identities = {}
        for eid, row in rows.items():
            for attr, value in row.items():
                if attr.endswith('/id') or attr in ('db/ident', 'topic/math-academy-id'):
                    identities[(attr, json.dumps(value, sort_keys=True))] = int(eid)

        def lookup(attr, value):
            return identities.get((attr.lstrip(':'), json.dumps(value, sort_keys=True)))

        present = {}
        generated_identity = {}
        for row in self.entities:
            identity_attr = next(k for k in row if k.endswith('/id') and k != ':db/id')
            present[row[':db/id']] = lookup(identity_attr, row[identity_attr])
            generated_identity[row[':db/id']] = {'$ref': [identity_attr, row[identity_attr]]}

        def resolved(value):
            if isinstance(value, dict) and '$inst' in value:
                parsed = datetime.fromisoformat(value['$inst'].replace('Z', '+00:00'))
                return {'$instant': int(parsed.timestamp() * 1000)}
            if isinstance(value, dict) and '$ref' in value:
                eid = lookup(*value['$ref'])
                if eid is None:
                    raise ValueError(f'Unresolved existing reference: {value}')
                return eid
            if isinstance(value, list):
                return sorted((resolved(v) for v in value), key=str)
            if isinstance(value, str) and value.startswith(':'):
                eid = lookup('db/ident', {'$keyword': value[1:]})
                if eid is None:
                    raise ValueError(f'Uninstalled enum: {value}')
                return eid
            if isinstance(value, str) and value in present:
                return present[value]
            return value

        forms = []
        optional_managed = (':step/next', ':multistep/context', ':assigned-problem/topic-coverage')
        for row in self.entities:
            existing = present[row[':db/id']]
            # Resolve external topics even for newly created records.
            for value in row.values():
                if isinstance(value, (dict, list)):
                    resolved(value)
            if existing is None:
                forms.append(row)
                continue
            stored = rows[str(existing)]
            for attr, value in row.items():
                if attr in (':db/id', ':db/ensure'):
                    continue
                actual = stored.get(attr[1:])
                if isinstance(actual, dict) and '$instant' in actual and isinstance(actual['$instant'], str):
                    parsed = datetime.fromisoformat(actual['$instant'].replace('Z', '+00:00'))
                    actual = {'$instant': int(parsed.timestamp() * 1000)}
                if isinstance(actual, list):
                    actual = sorted(actual, key=str)
                if actual != resolved(value):
                    raise ValueError(f'Existing imported content differs at {row[":db/id"]} {attr}. Review a targeted reconciliation; no transaction written.')
            for attr in optional_managed:
                if attr not in row and attr[1:] in stored:
                    raise ValueError(f'Removed managed attribute {attr} on {row[":db/id"]}; review its retraction before importing.')
        learner_eid = lookup('learner/id', learner)
        if learner_eid is None:
            raise ValueError(f'Unknown learner: {learner}')
        assigned = rows[str(learner_eid)].get('learner/assignments', [])
        for activity in activities:
            if present[activity] not in assigned:
                ref = {"$ref": [":activity/id", {"$uuid": activity}]} if present[activity] else activity
                forms.append([":db/add", {"$ref": [":learner/id", learner]}, ":learner/assignments", ref])

        def existing_refs(value):
            if isinstance(value, dict):
                if any(k.startswith('$') for k in value):
                    return value
                return {k: existing_refs(v) for k, v in value.items()}
            if isinstance(value, list):
                return [existing_refs(v) for v in value]
            if isinstance(value, str) and value in present and present[value] is not None:
                return generated_identity[value]
            return value

        return [existing_refs(form) for form in forms]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', type=Path, default=VAULT)
    parser.add_argument('--output', type=Path, default=ROOT / '.local/edb/school-assignments')
    parser.add_argument('--learner', default=DEFAULT_LEARNER)
    parser.add_argument('--snapshot', type=Path, required=True, help='Current EDB entity snapshot; validates topic refs and prevents duplicate or conflicting imports')
    parser.add_argument('--manifest', type=Path, help='Reviewed JSON source list with path and per-problem direct/supporting/coverage/note mappings; defaults to the four reviewed F26 assignments')
    parser.add_argument('--due-dates', type=Path, help='Optional JSON object mapping vault-relative paths to confirmed ISO dates or timezone-qualified timestamps')
    args = parser.parse_args()
    sources = json.loads(args.manifest.read_text()) if args.manifest else SOURCES
    due_dates = json.loads(args.due_dates.read_text()) if args.due_dates else {}
    unknown_deadlines = set(due_dates) - {source['path'] for source in sources}
    if unknown_deadlines:
        parser.error(f'Deadline paths do not match selected assignments: {sorted(unknown_deadlines)}')
    model = Import(args.vault, due_dates)
    activities = [model.build_assignment(spec) for spec in sources]
    model.validate()
    snapshot = json.loads(args.snapshot.read_text())
    forms = model.transaction(snapshot, args.learner, activities)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    transaction = '[\n' + '\n '.join(edn(row) for row in forms) + '\n]\n'
    (output / 'assignments.edn').write_text(transaction, encoding='utf-8')
    (output / 'entities.json').write_text(json.dumps(model.entities, indent=2, ensure_ascii=False) + '\n')
    counts = collections.Counter(next(k[1:-3] for k in row if k.endswith('/id') and k != ':db/id') for row in model.entities)
    audit = {"basis": snapshot['basis_t'], "counts": dict(counts), "learner": args.learner, "activities": model.audit, "assets": list(model.assets.values()), "transaction_sha256": hashlib.sha256(transaction.encode()).hexdigest(), "source_answer_fields": 0, "source_answer_keys": 0, "source_feedback": 0, "notes": ["Original numbered problems and labeled subparts preserved; worksheet diagrams become shared multipart context.", "No due dates, Math Academy content IDs, difficulty ratings, time estimates, answer keys, or solutions fabricated.", "Only explicit per-problem mappings enter topic-coverage. Supporting-only and partial matches remain identified in this audit.", "Prerequisite and lesson navigation lists are omitted from prompts; original source links and instructions remain.", "Prepared only; this script does not connect to the database.", "Unchanged imports produce no transaction forms. Changed managed content stops for reviewed reconciliation, preserving authored keys/solutions and learner records."]}
    (output / 'audit.json').write_text(json.dumps(audit, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({"output": str(output), "counts": dict(counts), "forms": len(forms), "sha256": audit['transaction_sha256']}, indent=2))


if __name__ == '__main__':
    main()
