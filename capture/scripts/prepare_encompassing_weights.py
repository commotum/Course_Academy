"""Prepare initial encompassing forms from independent account estimates.

Consumes pinned EDB read exports; does not read or transact against live storage.
Run: PYTHONPATH=capture python3 -m scripts.prepare_encompassing_weights
"""
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import argparse
import hashlib
import heapq
import json
import math
from pathlib import Path
import uuid

from .analyze_encompassing import distances, read
from .config import Config
from .database.commit import connection_identity
from .database.edn import dumps, kw
from .storage import atomic_json, atomic_text

ACCOUNTS = ('foundations', 'linear', 'multivariable', 'differential')
SOURCE_IDENT = ':agent/codex'
SOURCE_TEMPID = 'codex-encompassing-fractions-contributor'
WEIGHT_FRACTIONS = tuple(Fraction(value) for value in
                         ('1/5', '1/4', '1/3', '2/5', '1/2', '3/5', '2/3', '3/4', '4/5', '1'))
DEFAULT_FOLDER = 'reference/edb-math/imports/encompassing-weights/2026-10-11-frequency-fractions-r2'
DEFAULT_EVIDENCE_FOLDER = 'reference/mathacademy/encompassing-analysis-2026-10-11/frequency-fractions'


def validate_fraction_estimate(estimate):
    """Keep the observed ratio exact until selecting the user's nearest fraction."""
    rises, total = estimate['rising_activities'], estimate['eligible_activities']
    assert isinstance(rises, int) and isinstance(total, int) and 0 < rises <= total
    frequency = Fraction(rises, total)
    expected = min(WEIGHT_FRACTIONS, key=lambda weight: (abs(weight-frequency), -weight))
    assert estimate['frequency_weight_estimate'] == float(frequency)
    assert estimate['weight_fraction'] == str(expected), 'Fraction does not match nearest raw K/N'
    assert estimate['proposed_starting_coverage_weight'] == float(expected), 'Stored weight differs from its fraction'
    return str(expected)


def graph_coverage(edges):
    """Mirror Graph::coverage in engine/rust/core.rs, including direct overrides.

    Returns positive effective coverage and the inferred value immediately before
    each explicit pair overwrites it. Zero-weight edges still participate in order.
    """
    nodes = {node for pair in edges for node in pair}
    out = {node: [] for node in nodes}
    indegree = dict.fromkeys(nodes, 0)
    for (source, target), weight in sorted(edges.items()):
        assert source != target and math.isfinite(weight) and 0 <= weight <= 1
        out[source].append((target, weight))
        indegree[target] += 1
    ready = [node for node in nodes if not indegree[node]]
    heapq.heapify(ready)
    order = []
    while ready:
        node = heapq.heappop(ready)
        order.append(node)
        for target, _ in out[node]:
            indegree[target] -= 1
            if not indegree[target]:
                heapq.heappush(ready, target)
    if len(order) != len(nodes):
        raise ValueError('Encompassing graph cycle')
    effective, inferred = {}, {}
    for source in sorted(nodes):
        weights = {source: 1.0}
        for node in order:
            if node != source and (source, node) in edges:
                inferred[source, node] = weights.get(node, 0.0)
                weights[node] = edges[source, node]
            for target, weight in out[node]:
                weights[target] = max(weights.get(target, 0.0), weights.get(node, 0.0)*weight)
        effective.update({(source, target): weight for target, weight in weights.items()
                          if target != source and weight > 0})
    return effective, inferred


def coverage_audit(existing, additions):
    """Show actual before/after reductions and lower direct overrides separately."""
    assert not set(existing).intersection(additions), 'Existing direct edges must be preserved'
    before, _ = graph_coverage(existing)
    after, inferred = graph_coverage({**existing, **additions})
    pairs = [dict(source=source, target=target, weight=weight,
                  previous_effective_coverage=before.get((source, target), 0.0),
                  prepared_effective_coverage=after.get((source, target), 0.0),
                  inferred_before_direct_override=inferred.get((source, target), 0.0),
                  overrides_higher_inferred_coverage=inferred.get((source, target), 0.0) > weight+1e-12)
             for (source, target), weight in sorted(additions.items())]
    reduced = [dict(source=source, target=target, previous_effective_coverage=weight,
                    prepared_effective_coverage=after.get((source, target), 0.0))
               for (source, target), weight in sorted(before.items())
               if after.get((source, target), 0.0)+1e-12 < weight]
    return dict(implementation='engine/rust/core.rs Graph::coverage: explicit pair replaces inferred coverage before propagation',
                prepared_pairs=pairs,
                added_direct_edges_overriding_higher_inference=sum(p['overrides_higher_inferred_coverage'] for p in pairs),
                actual_effective_coverage_decreases=len(reduced),
                decreased_pairs=reduced)


def choose_account_estimate(estimates):
    """Select a whole account estimate; never average account outcomes."""
    return min(estimates, key=lambda e: (-e['eligible_activities'],
                                       e['proposed_starting_coverage_weight'], e['account']))


def prepare(root, folder, evidence_folder):
    if (folder/'superseded.json').exists():
        raise ValueError('This prepared transaction was superseded after methodology review. Preserve its exact request; do not regenerate or submit it.')
    identity = read(folder/'database-identity.json')
    topic_rows = read(folder/'topics.json')
    topics = {str(r[0][':topic/math-academy-id']): r[0] for r in topic_rows
              if ':topic/math-academy-id' in r[0]}
    idents = {str(r[0][':db/ident']): r[0][':db/id'] for r in read(folder/'idents.json')}
    required = ['topic/math-academy-id', 'topic/encompasses', 'encompassing/topic',
                'encompassing/weight', 'encompassing/rationale', 'encompassing/validate']
    assert all(':'+name in idents for name in required), 'Required schema missing'
    by_pair = defaultdict(list)
    manifests = []
    for account in ACCOUNTS:
        path = evidence_folder/(account+'-frequency-estimates.json')
        content = path.read_bytes()
        report = json.loads(content)
        assert report['account'] == account
        original = Path(report['source_report'])
        assert hashlib.sha256(original.read_bytes()).hexdigest() == report['source_report_sha256']
        manifests.append({'account': account, 'path': str(path),
                          'sha256': hashlib.sha256(content).hexdigest(),
                          'source_report_sha256': report['source_report_sha256']})
        for estimate in report['proposals']:
            assert estimate['account'] == account
            assert all(e['account'] == account for e in estimate['sequence'])
            assert estimate['eligible_activities'] == len(estimate['sequence']) >= 1
            assert estimate['rising_activities'] == sum(e['after'] > e['before'] for e in estimate['sequence'])
            validate_fraction_estimate(estimate)
            by_pair[estimate['source'],estimate['target']].append(estimate)
    # Validate the proposed graph against the captured current topic dependency graph.
    upstream = defaultdict(set)
    existing = defaultdict(list)
    encompassing_graph = defaultdict(set)
    for source, topic in topics.items():
        assert topic.get(':topic/id'), ('Missing topic identity',source)
        for child in topic.get(':topic/next', []):
            if ':topic/math-academy-id' in child:
                upstream[str(child[':topic/math-academy-id'])].add(source)
        for edge in topic.get(':topic/encompasses', []):
            target = str(edge[':encompassing/topic'][':topic/math-academy-id'])
            existing[source,target].append(edge)
            encompassing_graph[source].add(target)
    ancestors = {}
    selected, skipped, conflicts = [], [], []
    new_by_source = defaultdict(list)
    for (source,target), estimates in sorted(by_pair.items(),key=lambda x:(int(x[0][0]),int(x[0][1]))):
        assert source in topics and target in topics, ('Unresolved topic',source,target)
        assert source != target
        if source not in ancestors:
            ancestors[source] = distances(source,upstream)
        assert target in ancestors[source], ('No longer a prerequisite',source,target)
        assert len(existing[source,target]) <= 1, ('Duplicate existing target',source,target)
        choice = choose_account_estimate(estimates)
        weight = choice['proposed_starting_coverage_weight']
        assert isinstance(weight,(float,int)) and not isinstance(weight,bool) and math.isfinite(weight) and 0 < weight <= 1
        item = dict(source=source,target=target,source_title=topics[source][':topic/title'],
                    target_title=topics[target][':topic/title'], selected_account=choice['account'],
                    weight=weight, weight_fraction=choice['weight_fraction'],
                    crossing_frequency=choice['frequency_weight_estimate'],
                    rising_activities=choice['rising_activities'], eligible_activities=choice['eligible_activities'],
                    crossing_activity_numbers=choice['crossing_activity_numbers'],
                    activities_to_each_crossing=choice['activities_to_each_crossing'],
                    cadence_has_intervening_target_updates=choice['cadence_has_intervening_target_updates'],
                    account_estimates=estimates)
        if len({e['proposed_starting_coverage_weight'] for e in estimates})>1:
            conflicts.append(item)
        if existing[source,target]:
            skipped.append({**item,'reason':'Existing encompassing relationship preserved',
                            'existing_records':existing[source,target]})
            continue
        selected.append(item)
        encompassing_graph[source].add(target)
        summary = '; '.join(f"{e['account']}={e['weight_fraction']} ({e['rising_activities']}/{e['eligible_activities']})"
                            for e in sorted(estimates,key=lambda e:e['account']))
        try:
            evidence_path = str((evidence_folder/(choice['account']+'-frequency-estimates.json')).relative_to(root))
        except ValueError:
            evidence_path = str(evidence_folder/(choice['account']+'-frequency-estimates.json'))
        rationale = (f"Initial Codex estimate from captured target-band crossing frequency. "
            f"Selected account {choice['account']}: {choice['rising_activities']} rises / {choice['eligible_activities']} "
            f"eligible passed source activities = {choice['frequency_weight_estimate']:.6f}; nearest selected fraction = {choice['weight_fraction']}. "
            f"Crossing activity numbers {choice['crossing_activity_numbers']}; waits {choice['activities_to_each_crossing']}. "
            f"Separate account estimates: {summary}. Selection: most observations, then lower weight, then account name; no averaging. "
            f"Single-activity estimates included. Intervening target updates: {choice['cadence_has_intervening_target_updates']}. "
            f"Crossing frequency is the chosen practical estimate of encompassing coverage; a multi-band rise counts once. "
            f"This does not interpret color steps as physical repetition units. "
            f"Method: encompassing-report.md. Evidence: {evidence_path}, pair {source}->{target}. "
            f"All account evidence retained in the prepared import's selected-relationships.json.")
        new_by_source[source].append({kw('db/id'):f'encompassing-{source}-{target}',
            kw('encompassing/topic'):[kw('topic/math-academy-id'),int(target)],
            kw('encompassing/weight'):weight, kw('encompassing/rationale'):rationale,
            kw('db/ensure'):kw('encompassing/validate')})
    def visit(node):
        if node in active:
            raise ValueError('Encompassing graph cycle at '+node)
        if node in done:
            return
        active.add(node)
        for target in encompassing_graph.get(node,()):
            visit(target)
        active.remove(node);done.add(node)
    active,done=set(),set()
    for node in list(encompassing_graph):
        visit(node)
    existing_weights = {pair: edges[0][':encompassing/weight'] for pair, edges in existing.items() if edges}
    coverage = coverage_audit(existing_weights, {(e['source'],e['target']):e['weight'] for e in selected})
    forms=[]
    source_argument=SOURCE_IDENT
    if SOURCE_IDENT not in idents:
        forms.append({kw('db/id'):SOURCE_TEMPID,kw('db/ident'):kw(SOURCE_IDENT),
            kw('db/doc'):'Codex assistant. Initial encompassing calibration prepared from captured per-account band changes at Jake\u2019s request; exact model/version is not asserted by this contributor identity.'})
        source_argument=dumps(SOURCE_TEMPID)
    for source, edges in sorted(new_by_source.items(),key=lambda x:int(x[0])):
        forms.append({kw('db/id'):[kw('topic/math-academy-id'),int(source)],
                      kw('topic/encompasses'):edges})
    transaction='[\n'+'\n'.join('  '+dumps(form) for form in forms)+'\n]\n'
    transaction_hash=hashlib.sha256(transaction.encode()).hexdigest()
    intent_path=folder/'request.json'
    if intent_path.exists():
        prior=read(intent_path)
        assert (prior['transaction_sha256'],prior['basis'],prior['database_lineage']) == (
            transaction_hash,identity['basis'],identity['lineage']), 'Existing exact request differs; retain it for review/recovery'
        request_key=prior['request_key']
    else:
        request_key='initial-encompassing-frequency-fractions-2026-10-11-'+str(uuid.uuid4())
    intent={**connection_identity(Config()),'database_lineage':identity['lineage'],
        'basis':identity['basis'],'source':source_argument,'source_ident':SOURCE_IDENT,
        'source_entity_at_read_basis':idents.get(SOURCE_IDENT),'request_key':request_key,
        'transaction':transaction,'transaction_sha256':transaction_hash,
        'status':'prepared; not submitted', 'source_bootstrap_included':SOURCE_IDENT not in idents,
        'account_selection_rule':'Most eligible observations; ties lower proposed weight; remaining ties account name. Select one complete account estimate, no pooling.',
        'weight_method':'Original per-account crossing frequency K/N, rounded to the nearest selected fraction; exact ties choose the higher fraction.',
        'allowed_weight_fractions':[str(value) for value in WEIGHT_FRACTIONS],
        'evidence_manifests':manifests,
        'expected_new_relationships':len(selected),'expected_updated_source_topics':len(new_by_source),
        'preserved_existing_pairs':len(skipped),'differing_account_weight_pairs':len(conflicts),
        'added_direct_edges_overriding_higher_inference':coverage['added_direct_edges_overriding_higher_inference'],
        'actual_effective_coverage_decreases':coverage['actual_effective_coverage_decreases']}
    atomic_text(folder/'transaction.edn',transaction)
    atomic_json(intent_path,intent)
    atomic_json(folder/'selected-relationships.json',selected)
    atomic_json(folder/'existing-preserved.json',skipped)
    atomic_json(folder/'account-conflicts.json',conflicts)
    atomic_json(folder/'coverage-override-audit.json',coverage)
    summary={k:v for k,v in intent.items() if k not in ('transaction','evidence_manifests')}
    summary['selected_account_counts']=dict(Counter(e['selected_account'] for e in selected))
    summary['selected_observation_counts']=dict(sorted(Counter(e['eligible_activities'] for e in selected).items()))
    summary['selected_weight_counts']=dict(sorted(Counter(e['weight'] for e in selected).items()))
    summary['selected_fraction_counts']=dict(sorted(Counter(e['weight_fraction'] for e in selected).items(), key=lambda pair:Fraction(pair[0])))
    summary['application_validation']={'topic_identities_resolved':True,'finite_weights_in_range':True,
        'each_new_target_is_current_prerequisite':True,'one_new_record_per_source_target':True,
        'existing_records_preserved':True,'combined_encompassing_graph_acyclic':True,
        'nearest_allowed_fraction_from_raw_frequency':True,'explicit_override_effects_audited':True}
    summary['prepared_at']=datetime.now(timezone.utc).isoformat()
    atomic_json(folder/'summary.json',summary)
    print(json.dumps({k:intent[k] for k in ['basis','source_ident','expected_new_relationships',
                                         'expected_updated_source_topics','differing_account_weight_pairs']}))
    return intent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--folder',type=Path,help='Pinned EDB exports and prepared bundle directory; relative paths resolve under --root')
    parser.add_argument('--evidence-folder',type=Path,help='Per-account fractional frequency estimates; relative paths resolve under --root')
    args=parser.parse_args();root=args.root.resolve()
    folder = args.folder or Path(DEFAULT_FOLDER)
    evidence_folder = args.evidence_folder or Path(DEFAULT_EVIDENCE_FOLDER)
    prepare(root,folder if folder.is_absolute() else root/folder,
            evidence_folder if evidence_folder.is_absolute() else root/evidence_folder)


if __name__=='__main__':
    main()
