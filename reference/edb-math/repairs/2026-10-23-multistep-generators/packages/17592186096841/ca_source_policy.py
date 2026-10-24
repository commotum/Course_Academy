"""Standalone source eligibility and declared generated-question provenance."""
import copy
import re

POLICY_VERSION = 1

# Static EDB rule definitions follow :rules directly in the installed CLI.
MULTIPART_RULES = '''
 :rules [(multipart ?c) [?s :step/content ?c] [?m :multistep/steps ?s]]
        [(multipart ?c) [?p :assigned-problem/content ?c] (multipart ?p)]'''


def exclusion_query(*, bounded=False, legacy=False):
    inputs = ' :in $ [?q ...]' if bounded else ''
    rules = MULTIPART_RULES
    if legacy:
        rules += '\n [(multipart ?c) [?s :multistep-step/question ?c] [?m :multistep/steps ?s]]'
    return ('''[:find (pull ?q [:db/id :question/id :question/math-academy-id :question/retired])'''
            + inputs + ''' :where [?q :question/id _]
 (or-join [?q] [?q :question/retired true] (multipart ?q))''' + rules + ']')


def question_entities(material):
    found = set()
    def visit(value):
        if isinstance(value, dict):
            if ':question/id' in value and ':db/id' in value:
                found.add(value[':db/id'])
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(material)
    return sorted(found)


def filter_material(material, excluded):
    """Remove excluded question payloads, retaining a separate identity ledger."""
    excluded_ids = {r[':db/id'] for r in excluded}
    def visit(value):
        if isinstance(value, dict):
            if ':question/id' in value and value.get(':db/id') in excluded_ids:
                return None
            return {k: result for k, child in value.items() if (result := visit(child)) is not None}
        if isinstance(value, list):
            return [result for child in value if (result := visit(child)) is not None]
        return copy.deepcopy(value)
    result = visit(material)
    result['source_eligibility'] = {'policy_version': POLICY_VERSION,
        'excluded_questions': sorted([dict(r) for r in excluded], key=lambda r:r[':db/id'])}
    return result


def source_references(record):
    """Read explicit source references without mistaking seeds/bases for IDs."""
    generation = record.get('generation', {})
    refs = set()
    def add(value):
        if isinstance(value, (list, tuple)):
            for child in value:
                add(child)
        elif isinstance(value, dict):
            for key in (':db/id', 'db_id', 'question_id', 'source_id', 'id'):
                if key in value:
                    add(value[key])
        elif value is not None:
            refs.add(str(value))
    for key in ('source_id', 'source_ids', 'source_question_id', 'source_question_ids'):
        add(generation.get(key))
    template = generation.get('template')
    if isinstance(template, str) and re.fullmatch(r'[qe]-\d+', template):
        add(template)
    return refs


def reject_excluded_sources(records, excluded):
    blocked = {str(r[k]):r for r in excluded for k in (':db/id', ':question/id', ':question/math-academy-id') if k in r}
    for record in records:
        hits = source_references(record) & blocked.keys()
        if hits:
            raise ValueError('Generated question derives from excluded standalone source(s): ' + ', '.join(sorted(hits)))
