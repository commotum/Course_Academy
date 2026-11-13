#!/usr/bin/env python3
"""Semantic family audit of weak arrays from the captured EDB value (basis14355).

All input strings are read from the compressed immutable snapshot. No database
access, source mutation, or changes to the primary/completion repairs occur.
"""
import collections
import gzip
import hashlib
import json
from pathlib import Path
import re
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parents[2]/'audits/2026-11-11-imported-matrix-tables'
if not AUDIT.exists():
    AUDIT=HERE.parents[3]/'audits/2026-11-11-imported-matrix-tables'
rows=json.loads((AUDIT/'weak-array-candidates.json').read_text())
needed={(x['entity'],x['attribute']) for x in rows}
fields={};ma_topics={};step_contents={};activity_steps={};topic_activities={}
with gzip.open(AUDIT/'snapshot.jsonl.gz','rt') as f:
    for line in f:
        d=json.loads(line);e,a=d['e'],d['a']
        if (e,a) in needed: fields[(e,a)]=d['raw_string']
        if a=='topic/math-academy-id':ma_topics[e]=int(d['value_edn'])
        elif a=='step/content' and d['ref_eid'] is not None:step_contents[e]=d['ref_eid']
        elif a=='activity/steps':activity_steps.setdefault(e,[]).append(d['ref_eid'])
        elif a=='topic/activities':topic_activities.setdefault(e,[]).append(d['ref_eid'])
        elif a=='activity/scope':topic_activities.setdefault(d['ref_eid'],[]).append(e)
assert len(fields)==len(needed)
content_topics=collections.defaultdict(set)
for topic,activities in topic_activities.items():
    for activity in activities:
        for step in activity_steps.get(activity,[]):
            if step in step_contents:content_topics[step_contents[step]].add(topic)

families={
 'polynomial_division':(set([17592186048669,17592186050748,17592186050299,17592186050429,17592186051061,17592186048841,17592186050083,17592186048497,17592186050767,17592186050439,17592186048222,17592186051068]),
  'Coefficient/degree headings, divisor and product/remainder rows form synthetic or polynomial division work. Those arithmetic roles and horizontal rules are meaningful; no matrix operand is intended.'),
 'numerical_division':(set([17592186048953,17592186048981,17592186051073,17592186049207,17592186049278,17592186048488,17592186050939,17592186050815,17592186049343,17592186049211,17592186049143,17592186050177,17592186048145,17592186048153,17592186050556,17592186408188]),
  'Digit columns, division boxes/quotients and vertically aligned subtraction or remainder work represent numerical division. Empty cells align place value or partial quotients; they are not missing matrix brackets.'),
 'sign_and_slope_tables':(set([17592186048480,17592186048795,17592186048885]),
  'Rows and columns identify coordinate regions or x/y sample points; cells record signs, arrows or slopes. This is a sign chart or slope-field data table whose coordinate headings carry meaning.'),
 'probability_and_statistics_tables':(set([17592186050116,17592186048785,17592186048615,17592186048872,17592186050079,17592186051001,17592186050297,17592186049359,17592186049871,17592186050997,17592186049690,17592186050835,17592186050198]),
  'Variable values, probabilities, critical values, sample groups or distribution parameters label the rows/columns. The entries are table data, totals or probability lookup values, not a bracketed linear-algebra object.'),
 'function_and_ratio_tables':(set([17592186050138,17592186050948,17592186049659,17592186050633,17592186050063]),
  'Input/output, variable or ratio headings pair values across columns/rows. Blank entries and growth arrows belong to a function/ratio table; converting to a matrix would erase those roles.'),
 'boolean_truth_tables':(set([17592186050882,17592186048596,17592186049447,17592186049505]),
  'Boolean variable columns enumerate truth assignments and outputs or minterms/maxterms. These are truth-table rows with meaningful logical headings, not matrix entries.'),
 'fraction_area_models':(set([17592186050167]),
  'The table draws a rectangle with an area and side-length label. Its blank edge cells and phantom box represent an area model for division, not a matrix/vector.'),
 'euler_iteration_tables':(set([17592186049441]),
  'Columns x, y, derivative and delta-y describe successive Euler steps. The blank second row is an iteration table with column semantics.'),
 'scalar_fraction_layout':(set([17592186048191]),
  'The table places a derivative equality beside a numerator and denominator. It encodes a scalar quotient, not a rectangular matrix or vector; any fraction cleanup is outside this matrix audit.'),
 'sample_space_tree':(set([17592186620948]),
  'The prompt explicitly requests a sample-space tree; branch labels and ordered outcomes occupy tree positions. The unbalanced rows are tree geometry, not a matrix.'),
 'binomial_probability_layout':(set([17592186049354]),
  'Parentheses arrange binomial coefficients and a sum of probability quotients. Top/bottom numbers are binomial arguments or fraction components, not vector entries.'),
 'state_transition_table':(set(),
  'State and tape-symbol headings index Turing-machine transition tuples (next state, symbol, direction). This is a transition table whose headings must remain visible.'),
 'modular_addition_table':(set(),
  'The plus sign and residue row/column headers define a modular addition table. Its rectangular body is operation-table data, not a matrix operand.'),
}
topic_family={t:name for name,(topics,_) in families.items() for t in topics}
# Tutorial-only cases have no census topic IDs. Their complete captured prose
# and exact cell geometry were inspected; assign by the actual tutorial entity,
# not by generic section names such as Introduction.
tutorial_family={
17592186065438:'polynomial_division',17592186088935:'polynomial_division',17592186088995:'polynomial_division',17592186135065:'polynomial_division',
17592186069984:'function_and_ratio_tables',17592186120991:'function_and_ratio_tables',17592186121103:'function_and_ratio_tables',17592186148676:'function_and_ratio_tables',17592186148677:'function_and_ratio_tables',17592186218249:'function_and_ratio_tables',
17592186074956:'numerical_division',17592186144015:'numerical_division',17592186144016:'numerical_division',17592186189390:'numerical_division',17592186193819:'numerical_division',17592186232047:'numerical_division',17592186489385:'numerical_division',17592186489388:'numerical_division',
17592186130416:'sign_and_slope_tables',17592186168158:'sign_and_slope_tables',17592186173192:'sign_and_slope_tables',17592186173195:'sign_and_slope_tables',17592186180696:'sign_and_slope_tables',
17592186163174:'probability_and_statistics_tables',17592186189371:'probability_and_statistics_tables',
17592186205151:'boolean_truth_tables',17592186205156:'boolean_truth_tables',
17592186185289:'state_transition_table',17592186205247:'modular_addition_table',17592186232002:'fraction_area_models'}

source_cache={}
def source_info(topic):
    ma=ma_topics.get(topic)
    if ma is None:return {'topic_entity':topic,'source_scope':'No topic Math Academy ID in captured snapshot.'}
    if ma not in source_cache:
        base=Path(f'/home/jake/Developer/MA/DATA/Lessons/{ma}/Source/{ma}')
        info={'topic_entity':topic,'ma_topic_id':ma,'json_path':str(base.with_suffix('.json')),'html_path':str(base.with_suffix('.html'))}
        if base.with_suffix('.json').exists() and base.with_suffix('.html').exists():
            j=json.loads(base.with_suffix('.json').read_text());text=base.with_suffix('.html').read_text()
            soup=BeautifulSoup(text,'html.parser')
            info.update(topic_title=j.get('topic_title'),html_table_count=len(soup.select('table')),
              html_sha256=hashlib.sha256(text.encode()).hexdigest(),
              question_ids=[str(i['question_id']) for i in j.get('lesson',{}).get('items',[]) if i.get('question_id')],
              source_scope='Local source-family HTML and normalized lesson JSON inspected. Exact variant presence is stated separately; captured full field supplies decisive target semantics.')
        else:info['source_scope']='Local lesson source unavailable; captured full field supplies decisive target semantics.'
        source_cache[ma]=info
    return source_cache[ma]

reviews=[]
excluded=[]
for index,x in enumerate(rows):
    if set(x['topics']) & {17592186048637,17592186049409}:
        excluded.append(index);continue
    whole=fields[(x['entity'],x['attribute'])]
    start,end=x['span'];assert whole[start:end]==x['table'],(index,'span drift')
    family=(topic_family[x['topics'][0]] if x['topics'] else tutorial_family[x['entity']])
    # Every nontrivial family decision has its own exact stored geometry and
    # containing prose. Nested division/sign-table fragments inherit their
    # containing arithmetic/coordinate semantics, rather than being mistaken
    # for unlabeled matrices merely because their local cells are numeric.
    topicids=x['topics'] or sorted(content_topics.get(x['entity'],set()))
    source=[source_info(t) for t in topicids]
    exact_ids=[]
    for src in source:
        exact_ids+=sorted(set(src.get('question_ids',[])) & {i[2:] for i in x['imported_ids'] if i.startswith('q-')})
    reviews.append({'entity':x['entity'],'attribute':x['attribute'],'span':x['span'],
        'weak_index':index,'status':'disconfirmed','family':family,'rationale':families[family][1],
        'evidence':{'basis':14355,'full_field_sha256':hashlib.sha256(whole.encode()).hexdigest(),
                    'span_exact_match':True,'rows':x['rows'],'titles':x['titles'],
                    'context_before':x['context_before'],'context_after':x['context_after'],
                    'source_topics':topicids,'source_paths':[s.get('html_path') for s in source if s.get('html_path')],
                    'exact_source_question_ids_present':exact_ids,
                    'source_scope':'Family evidence plus exact captured full-field semantics; no claim that every historical variant was present in local sources.'}})

assert len(reviews)+len(excluded)==len(rows)
assert len({(x['entity'],x['attribute'],tuple(x['span'])) for x in reviews})==len(reviews)
for name,data in [('supplemental-reviews',reviews),('supplemental-proposals',[]),
                  ('supplemental-evidence',{'basis':14355,'queue_size':len(rows),'excluded_newton_indices':excluded,
                    'family_counts':dict(collections.Counter(x['family'] for x in reviews)),
                    'source_families':list(source_cache.values()),
                    'conclusion':'No weak-array candidate is an additional malformed matrix/vector layout. All tables retain meaningful arithmetic, lookup, sign, truth, area, tree, fraction or iteration semantics.'})]:
    (HERE/f'{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'reviewed':len(reviews),'excluded':len(excluded),'confirmed':0,'disconfirmed':len(reviews),'proposals':0,
                  'families':dict(collections.Counter(x['family'] for x in reviews))},indent=2))
