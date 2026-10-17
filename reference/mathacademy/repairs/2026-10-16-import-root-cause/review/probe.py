#!/usr/bin/env python3
"""Read-only import-chain evidence; writes only this report folder."""
import hashlib, importlib.util, json, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from activities import html_to_markdown
from math_format import validate_prose

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value

historical = module('historical_content_audit', ROOT / 'scripts/import_historical_question_content.py')
source_root = Path('/home/jake/Developer/MA/DATA/Lessons')
manifest_path = ROOT / 'reference/edb-math/imports/math-academy/lessons/manifest.json'
manifest = json.loads(manifest_path.read_text())
result = {'scope': 'Read-only source/code probes; counts are archive/import coverage, not current affected EDB entities.',
          'baseline_manifest': str(manifest_path.relative_to(ROOT)),
          'baseline_totals': manifest['totals'], 'baseline_batches': len(manifest['batches']),
          'source_inventory': {'html_files': len(list(source_root.glob('*/Source/*.html'))),
                               'json_files': len(list(source_root.glob('*/Source/*.json')))},
          'legacy_topic_page_list_probes': [], 'historical_fraction_probes': [],
          'source_fraction_fixture_checks': [], 'validator_limits': [], 'files': {}}
for key, html, expected in [
    ('default_decimal_control','<ol><li>First</li><li>Second</li></ol>', '1. First\n2. Second'),
    ('roman_start_reset','<ol type="I" start="3"><li>First</li><li value="7">Reset</li></ol>', 'III. First\nVII. Reset'),
    ('reversed','<ol reversed><li>Second</li><li>First</li></ol>', '2. Second\n1. First'),
    ('nested','<ol><li>Outer<ol type="a"><li>Inner</li></ol></li><li>Second</li></ol>', '1. Outer\n  a. Inner\n2. Second'),
    ('source_css_class','<ol class="questionStatements"><li>First</li><li>Second</li></ol>', 'I. First\nII. Second'),
]:
    actual = html_to_markdown(html)
    result['legacy_topic_page_list_probes'].append({'case':key,'source_html':html,'expected_visible_labels':expected,
                                                   'output':actual,'matches':actual==expected})
for name, attr in [('ordinary_control',''),('zero_rule',' linethickness="0"')]:
    html = '<math><mfrac'+attr+'><mn>7</mn><mn>2</mn></mfrac></math>'
    renderer = historical.Renderer(0)
    actual = renderer.m(BeautifulSoup(html, 'html.parser').find('math'))
    result['historical_fraction_probes'].append({'case':name, 'source_html':html,'output':actual,'errors':renderer.errors,
                                                'validator_accepts':validate_prose('$'+actual+'$')=='$'+actual+'$'})
fixture_path = ROOT / 'capture/scripts/tests/fixtures/zero-bar-fractions.json'
for row in json.loads(fixture_path.read_text()):
    assert hashlib.sha256(row['html'].encode()).hexdigest() == row['html_sha256']
    soup = BeautifulSoup(row['html'], 'html.parser')
    formulas = [n for n in soup.select('math mfrac[linethickness="0"]') if n.find_parent('mphantom') is None]
    renderer = historical.Renderer(0)
    outputs = [renderer.m(n) for n in formulas]
    result['source_fraction_fixture_checks'].append({'question_id':row['question_id'], 'source_file':row.get('source_file'),
        'html_sha256':row['html_sha256'],'visible_zero_rule_fractions':len(formulas),'historical_outputs':outputs,
        'historical_errors':renderer.errors})
for text in ['$n$', '$\\begin{bmatrix}1&2\\\\3&4\\end{bmatrix}$', '$\\frac{7}{2}$']:
    result['validator_limits'].append({'input':text,'accepted':validate_prose(text)==text,
                                     'note':'Syntactically valid without source correspondence; not inherently erroneous.'})
for rel in ['reference/edb-math/bin/generate-ma-lessons-json.py','scripts/question_capture/activities.py',
            'scripts/import_historical_question_content.py','capture/scripts/browser/extract.js',
            'scripts/question_capture/math_format.py', 'capture/scripts/tests/fixtures/zero-bar-fractions.json']:
    result['files'][rel] = hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
(OUT/'probe.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'source_inventory':result['source_inventory'],
                  'legacy_list_mismatches':sum(not r['matches'] for r in result['legacy_topic_page_list_probes']),
                  'zero_rule_source_questions':len(result['source_fraction_fixture_checks']),
                  'visible_zero_rule_source_fractions':sum(r['visible_zero_rule_fractions'] for r in result['source_fraction_fixture_checks']),
                  'output':str(OUT/'probe.json')}, indent=2))
