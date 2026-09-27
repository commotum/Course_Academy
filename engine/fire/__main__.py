"""Run with python -m engine.fire demo or python -m engine.fire replay FILE."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from .core import Edge, EncompassingGraph, Event, FireEngine, Policy, TopicState


def replay(data: dict) -> dict:
    engine = FireEngine(EncompassingGraph((Edge(**e) for e in data.get('edges', [])), data.get('topics', ())),
                        Policy(**data.get('policy', {})), data.get('difficulty_accuracy'), data.get('neighborhoods'))
    for seed in data.get('initial_states', []):
        engine.seed(seed['learner'], seed['topic'], TopicState(**seed['state']))
    receipts = []
    for raw in data.get('events', []):
        receipts.append(engine.apply(Event(**{**raw, 'question_results': tuple(raw.get('question_results', []))})))
    return {'assumptions': data.get('assumptions', []), 'receipts': receipts, 'snapshot': engine.snapshot()}


def demo() -> dict:
    """The author's multiplication example, with explicitly assumed parameters."""
    edges = [Edge('two-digit-multiplication', 'one-digit-multiplication', 1),
             Edge('two-digit-multiplication', 'addition', 1)]
    engine = FireEngine(EncompassingGraph(edges))
    for topic in engine.graph.topics:
        engine.seed('demo', topic, TopicState())
    before = engine.due('demo', 1)
    ranking = engine.rank('demo', 1, [
        {'topic': 'two-digit-multiplication', 'expected_minutes': 5},
        {'topic': 'one-digit-multiplication', 'expected_minutes': 4},
        {'topic': 'addition', 'expected_minutes': 4},
    ])
    receipt = engine.apply(Event('demo-review', 'demo', 'two-digit-multiplication', 1, True,
                                question_results=(True, True, True), source='student-selected'))
    slow = FireEngine(EncompassingGraph(edges))
    for topic in slow.graph.topics:
        slow.seed('demo', topic, TopicState(accuracy=.4 if topic == 'addition' else .8))
    slow_receipt = slow.apply(Event('slow-review', 'demo', 'two-digit-multiplication', 1, True))
    return {
        'description': 'Published encompassing example under our assumed numeric policy; not a fitted MA schedule.',
        'policy': asdict(engine.policy), 'edges': [asdict(e) for e in edges],
        'due_before': before, 'ranking': ranking, 'receipt': receipt,
        'due_after': engine.due('demo', 1),
        'slow_component': {'receipt': slow_receipt, 'due_after': slow.due('demo', 1)},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['demo', 'replay'])
    parser.add_argument('input', nargs='?', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.command == 'replay' and not args.input:
        parser.error('replay requires a JSON input file')
    result = demo() if args.command == 'demo' else replay(json.loads(args.input.read_text()))
    payload = json.dumps(result, indent=2, allow_nan=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
