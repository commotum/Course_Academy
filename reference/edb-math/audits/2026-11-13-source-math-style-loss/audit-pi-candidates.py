"""Read-only source/current audit of every literal-Pi candidate in the export."""
import csv, hashlib, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
from bs4 import BeautifulSoup, Tag

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from import_historical_question_content import Renderer
from question_capture.math_format import normalize_source_tex

SOURCES = json.loads((HERE / 'pi-source-path-index.json').read_text())
CANDIDATES = json.loads((HERE / 'current-literal-pi-candidates.json').read_text())
STATE_CACHE = {}
FONT = {'mathrm': 'normal', 'mathit': 'italic', 'mathbf': 'bold',
        'mathbfit': 'bold-italic', 'mathsf': 'sans-serif', 'mathtt': 'monospace'}
MATH = re.compile(r'\$\$([\s\S]*?)\$\$|(?<!\\)\$([^$]*?)\$')

def canonical(tex):
    tex = normalize_source_tex(tex).replace(r'\Pi', 'Π')
    tex = re.sub(r'\\(?:mathrm|mathit|mathbf|mathbfit|mathbb|mathcal|mathfrak|mathsf|mathtt|boldsymbol)\b', '', tex)
    tex = re.sub(r'\\(?:color|hspace|kern|mkern)(?:\[[^\]]*\])?\{[^{}]*\}', '', tex)
    tex = re.sub(r'\\(?:quad|qquad|left|right|displaystyle|textstyle)\b|\\[,;:! ]', '', tex)
    tex = tex.replace(r'\dfrac', r'\frac').replace(r'\neq', r'\ne').replace(r'\not\in', r'\notin')
    tex = tex.replace(r'\langle', '⟨').replace(r'\rangle', '⟩')
    tex = re.sub(r'\s', '', tex)
    # Ignore redundant one-token font groups while retaining fraction, matrix
    # and other multi-token argument boundaries for formula correspondence.
    while re.search(r'\{[A-Za-z0-9Π]\}', tex):
        tex = re.sub(r'\{([A-Za-z0-9Π])\}', r'\1', tex)
    return tex.rstrip('.,;')

def literal_styles(tex):
    """Read explicit font arguments around literal Π; implicit math italic is default."""
    stack = ['implicit-italic']; pending = None; result = []
    for token in re.findall(r'\\[A-Za-z]+|\\.|[{}]|[^\\{}]', tex):
        if token.startswith('\\') and token[1:] in FONT:
            pending = FONT[token[1:]]
        elif token == '{':
            stack.append(pending or stack[-1]); pending = None
        elif token == '}':
            if len(stack) > 1: stack.pop()
            pending = None
        elif token == 'Π':
            result.append(pending or stack[-1]); pending = None
        elif not token.isspace():
            pending = None
    return result

def source_formulas(node, path, component):
    r = Renderer(0); result = []
    for math in node.select('math'):
        if 'Π' not in math.get_text(): continue
        variants = []
        for token in math.select('mi, mn, mo, mtext'):
            if 'Π' not in token.get_text(): continue
            variant = None
            for ancestor in [token, *token.parents]:
                if isinstance(ancestor, Tag) and ancestor.has_attr('mathvariant'):
                    variant = ancestor['mathvariant']; break
                if ancestor is math: break
            variants.extend([variant or 'implicit-source'] * token.get_text().count('Π'))
        result.append({'tex': normalize_source_tex(r.m(math)), 'variants': variants,
                       'source': path, 'component': component, 'mathml': str(math)})
    # Legacy source TeX titles without MathML also encode upright Pi directly.
    for title in node.select('svg title, annotation[encoding="application/x-tex"]'):
        if title.select_one('math'): continue
        tex = title.get_text()
        if 'Π' not in tex and r'\Pi' not in tex: continue
        variants = literal_styles(tex) + ['normal'] * len(re.findall(r'\\Pi\b', tex))
        result.append({'tex': tex, 'variants': variants, 'source': path,
                       'component': component, 'source_tex': tex})
    return result

def load_sources(num):
    paths = SOURCES.get(num, [])
    html = [p for p in paths if p.endswith('.html')]
    selected = [p for p in html if '/history-' in p or '-before-entry-' in p]
    selected += [p for p in paths if p.endswith('.json') and p[:-5] + '.html' not in paths
                 and ('/history-' in p or '-before-entry-' in p)]
    if not selected: selected = html or paths
    out = defaultdict(list); hashes = {}; seen = set(); documents = []
    for path in sorted(selected):
        data = (ROOT / path).read_bytes()
        if path.endswith('.json'):
            record = json.loads(data); raw = record.get('html', '')
            if not raw: continue
        else: raw = data.decode()
        documents.append((path, data, raw))
    for parent in sorted({str(Path(p).parent) for p in paths if '/question-capture' in p}):
        statepath = parent + '/state.json'
        if not (ROOT / statepath).exists(): continue
        if statepath not in STATE_CACHE:
            data = (ROOT / statepath).read_bytes(); STATE_CACHE[statepath] = (data, json.loads(data))
        data, state = STATE_CACHE[statepath]
        question = state.get('questions', {}).get('q-' + num, {})
        for stage in ('before', 'after', 'history'):
            raw = question.get(stage, {}).get('html', '')
            if raw: documents.append((statepath + '#questions.q-' + num + '.' + stage + '.html', data, raw))
    for path, data, raw in documents:
        digest = hashlib.sha256(raw.encode()).hexdigest()
        if digest in seen: continue
        seen.add(digest); hashes[path] = hashlib.sha256(data).hexdigest()
        soup = BeautifulSoup(raw, 'html.parser')
        prompt = soup.select_one('.questionWidget-text, .questionText, .exampleQuestion')
        solution = soup.select_one('.questionWidget-explanation, .questionExplanation, .exampleExplanation')
        if prompt: out['problem'] += source_formulas(prompt, path, 'problem')
        if solution: out['solution'] += source_formulas(solution, path, 'solution')
        for choice in soup.select('.questionWidget-choiceText, .choiceText, .selectListOption'):
            out['answer'] += source_formulas(choice, path, 'answer')
    return out, hashes

rows = []; identities = []; hashes = {}
for q in CANDIDATES:
    source, source_hashes = load_sources(q['ma_id'][2:]); hashes.update(source_hashes)
    question_rows = []
    for field in q['fields']:
        attr = field['attribute']
        kind = 'problem' if attr in ('question/problem', 'answer-field/key') else 'solution' if attr == 'question/worked-solution' else 'answer'
        formulas = [a or b for a, b in MATH.findall(field['value']) if 'Π' in (a or b)]
        if not formulas and 'Π' in field['value']: formulas = [field['value']]
        checks = []
        for tex in formulas:
            matches = [s for s in source[kind] if canonical(s['tex']) == canonical(tex)]
            unique = {(tuple(s['variants']), canonical(s['tex'])) for s in matches}
            styles = literal_styles(tex)
            if not matches:
                status = 'missing_source_component' if not source[kind] else 'unmatched_formula_review'
            elif len({v for v, _ in unique}) > 1:
                status = 'conflicting_source_variants'
            elif matches[0]['variants'] and all(v == 'normal' for v in matches[0]['variants']):
                status = 'already_correct_wrapped' if all(v == 'normal' for v in styles) else 'confirmed_upright_pi_loss'
            else:
                status = 'non_normal_source_review'
            checks.append({'current_formula': tex, 'current_literal_styles': styles, 'status': status,
                           'evidence': matches[:1], 'matching_capture_count': len(matches)})
        counts = Counter(c['status'] for c in checks)
        unresolved = sum(n for s, n in counts.items() if s not in ('confirmed_upright_pi_loss', 'already_correct_wrapped'))
        status = ('confirmed_loss_with_unresolved_formulas' if unresolved else 'confirmed_loss') if counts['confirmed_upright_pi_loss'] else 'review_needed' if unresolved else 'already_correct'
        row = {'question': q['entity'], 'ma_id': q['ma_id'], 'topics': q['topics'],
               'entity': field['entity'], 'attribute': attr, 'retired': q['retired'],
               'status': status, 'formula_counts': dict(counts), 'checks': checks}
        rows.append(row); question_rows.append(row)
    identities.append({'entity': q['entity'], 'ma_id': q['ma_id'], 'topics': q['topics'],
                       'source_documents': len(source_hashes),
                       'confirmed_fields': sum(r['status'].startswith('confirmed_loss') for r in question_rows),
                       'correct_fields': sum(r['status'] == 'already_correct' for r in question_rows),
                       'review_fields': sum(r['status'] == 'review_needed' or 'unresolved' in r['status'] for r in question_rows)})

summary = {'candidate_questions': len(CANDIDATES), 'candidate_fields': len(rows),
           'field_status_counts': dict(Counter(r['status'] for r in rows)),
           'formula_status_counts': dict(Counter(c['status'] for r in rows for c in r['checks'])),
           'confirmed_affected_questions': sum(q['confirmed_fields'] > 0 for q in identities),
           'questions_with_review_gaps': sum(q['review_fields'] > 0 for q in identities),
           'source_documents_read': len({path.split('#')[0] for path in hashes}),
           'source_components_indexed': len(hashes), 'database_writes': 0}
affected = [row for row in rows if row['status'].startswith('confirmed_loss')]
by_topic = defaultdict(set)
for row in affected:
    for topic in row['topics']: by_topic[topic['title']].add(row['question'])
summary['unique_affected_attributes'] = len({(r['entity'], r['attribute']) for r in affected})
summary['affected_questions_by_topic'] = {title: len(values) for title, values in by_topic.items()}
report = {'summary': summary,
          'scope': 'Complete check of the 164 exported literal-Pi candidates only. A source/current formula must match after removing presentation styling; source Pi must explicitly be normal. No repairs are performed.',
          'source_sha256': hashes, 'questions': identities, 'findings': rows}
(HERE / 'pi-findings.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
with (HERE / 'pi-findings.csv').open('w') as stream:
    writer = csv.DictWriter(stream, fieldnames=['question', 'ma_id', 'topics', 'entity', 'attribute', 'retired', 'status', 'formula_counts'])
    writer.writeheader()
    for row in rows:
        writer.writerow({key: json.dumps(row[key], ensure_ascii=False) if key in ('topics', 'formula_counts') else row[key] for key in writer.fieldnames})
print(json.dumps(summary, indent=2))
