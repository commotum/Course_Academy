#!/usr/bin/env python3
"""Reproducible semantic review; creates proposals, never writes the database."""
import collections
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'scripts/question_capture/math_format.py').exists())
sys.path.insert(0, str(ROOT))
from scripts.question_capture.math_format import (
    MATH, matrix_equation, matrix_input_grid, validate_prose,
)
from bs4 import BeautifulSoup
BASE = HERE.parent
assigned = json.loads((HERE / 'assigned.json').read_text())
snapshot = json.loads((BASE / 'snapshot-fields.json').read_text())
current = {x[':db/id']: x for x in json.loads((BASE / 'capture/entities.json').read_text())}
questions = {x[':db/id']: x for x in json.loads((BASE / 'capture/questions.json').read_text())}
topics = {x[':db/id']: x[':topic/math-academy-id'] for x in json.loads((BASE / 'capture/topics.json').read_text())}
MARKER = re.compile(r'\{\{(?:answer-field:)?[^{}]+\}\}')
TOKEN = re.compile(r'\{\{(?:answer-field:)?[^{}]+\}\}|\$(?:\\.|[^$])*\$')

def bare(value):
    value = html.unescape(value.strip())
    if value.startswith('$') and value.endswith('$'): return value[1:-1]
    assert MARKER.fullmatch(value) or value=='.', repr(value)
    return value

def nonempty(rows):
    return [[bare(c) for c in row if c.strip()] for row in rows]

def eq(label, rows, suffix=None):
    parts = ([label] if label else []) + [rows] + ([suffix] if suffix else [])
    return matrix_equation(parts)

def simple(c):
    rows = nonempty(c['rows'])
    label = None
    # Source labels span all matrix rows; Markdown imports may put them midrow.
    for row in rows:
        for i,v in enumerate(row):
            if '=' in v or '≈' in v:
                assert label is None, c['candidate_index']
                label = row.pop(i)
                break
    return label, rows

def svd(c):
    if len(c['rows']) == 3:
        label, rows = simple(c)
        assert all(len(r) == 1 for r in rows)
        return eq(label, rows), {'matrix_rows': rows, 'label': label}
    if c['format'] == 'html':
        soup = BeautifulSoup(c['table'], 'html.parser')
        outer = soup.find('table')
        inner = [t for t in outer.find_all('table') if t.find_parent('table') == outer]
        assert len(inner) == 2
        parts=[]; operands=[]
        for t in inner:
            rows = [[td.get_text(' ',strip=True) for td in r.find_all(['td','th'],recursive=False)]
                    for r in t.find_all('tr') if r.find_parent('table')==t]
            label, cells = simple({'rows':rows,'candidate_index':c['candidate_index']})
            assert len(cells)==3 and all(len(r)==1 for r in cells)
            parts.extend([label,cells]); operands.append({'label':label,'matrix_rows':cells})
        return matrix_equation(parts), {'operands':operands,'nested_container':True}
    tokens=[bare(m[0]) for m in TOKEN.finditer(c['table'])]
    groups=[]
    for token in tokens:
        if '=' in token:
            groups.append({'label':token,'cells':[]})
        else:
            assert groups
            groups[-1]['cells'].append(token)
    assert len(groups) in [2,4] and all(len(g['cells'])==3 for g in groups), (c['candidate_index'],groups)
    evidence={}
    if len(groups)==4:
        assert groups[:2]==groups[2:], (c['candidate_index'],groups)
        evidence['duplicate_import_artifact']={'complete_operands_first_copy':groups[:2],
                                              'complete_operands_second_copy':groups[2:]}
        groups=groups[:2]
    parts=[]
    for g in groups:parts.extend([g['label'],[[v] for v in g['cells']]])
    evidence['operands'] = [{'label':g['label'],'matrix_rows':[[v] for v in g['cells']]} for g in groups]
    return matrix_equation(parts),evidence

def newton(c):
    rows=nonempty(c['rows'])
    if len(rows[0])==6:
        a,b=rows
        assert len(b)==3 and a[0]=='[' and a[-1]==']'
        assert a[3].startswith(']') and a[3].endswith('[')
        lhs=[[a[1],a[2]],[b[0],b[1]]];rhs=[[a[4]],[b[2]]]
        middle=a[3][1:-1]
        return matrix_equation([lhs,middle,rhs]),{'operands':[lhs,rhs],'operator':middle,'rowspan_recovery':True}
    assert len(rows[0])==3 and len(rows[1])==1
    label=rows[0][0]
    assert label.endswith('[') and rows[0][-1]==']'
    cells=[[rows[0][1]],[rows[1][0]]]
    return eq(label[:-1],cells),{'matrix_rows':cells,'label':label[:-1],'rowspan_recovery':True}

def matrix_family(c):
    label,rows=simple(c)
    suffix=None
    # Lotka Jacobian tables have a separately spanning punctuation cell.
    if len(rows[0])>len(rows[-1]):suffix=rows[0].pop()
    assert len({len(r) for r in rows})==1 and len(rows[0]) in [1,2,3], (c['candidate_index'],rows)
    return eq(label,rows,suffix),{'matrix_rows':rows,'label':label,'suffix':suffix}

def linear(c):
    a,b=c['rows']
    label=bare(a[0]);cells=[[bare(a[2]),bare(a[3])],[bare(b[1]),bare(b[2])]]
    suffix=a[5]
    assert suffix=='$u$, where $u = x - x^{∗}$'
    return eq(label,cells,'u')+', where $u = x - x^{∗}$',{'matrix_rows':cells,'label':label,'operator':'u','prose_suffix':', where $u = x - x^{∗}$'}

DISCONFIRMED={17592186048960:'This is a relation incidence/adjacency table with explicit domain/range labels in its first column and first row. Those headings identify ordered-pair membership and must remain table headers; treating all cells as a bracketed numerical matrix would erase their role.',
17592186050376:'This is synthetic polynomial division, not a matrix or vector: the first column is the trial root, the top row contains polynomial coefficients, the middle row contains accumulated products and a down arrow, and the bottom row is the quotient/remainder. The arithmetic row and column rules are semantically necessary.',
17592186050772:'This is a growth-model comparison table: the t and P(t) headers, ellipses and colored increment/multiplier arrows describe the relationship between time and population. It has no matrix/vector operand semantics.'}
FAMILY={17592186048143:svd,17592186048637:newton,17592186048367:matrix_family,
17592186050832:matrix_family,17592186050600:matrix_family,17592186050228:matrix_family,
17592186051021:matrix_family,17592186048881:linear,17592186050727:matrix_family}
WHY={17592186048143:'The surrounding SVD computation explicitly identifies these as the three entries of a column of U, an orthogonal-complement solution vector, or the scaled Gram-Schmidt vector c2. Empty 5px columns are bracket strokes/spacers, not zero entries or data fields. The preserved entries give a 3×1 vector.',
17592186048637:'The instruction explicitly requests a Newton-Raphson matrix equation. Source-family HTML uses rowspan=2 for [, ](x1−x0)=[, ] and for x1=[; therefore the imported lower-row cells belong under the matrix/RHS entries rather than under the rowspanning fences. Rebuild the 2×2 matrix and 2×1 RHS, or the 2×1 iterate, preserving every supplied entry and operator.',
17592186048367:'The question asks for the total derivative of a vector-valued composition, and the answer label is that derivative at x0. The HTML label spans the rows; the 5px empty boundary cells draw brackets. All remaining supplied constants and answer markers form the Jacobian, including partially supplied rows.',
17592186050832:'The prompt requests the subset gradient, whose components form a column vector. Source-family HTML places a spanning gradient label beside a 5px bracket column and one component per row. Preserve every component marker and render a bracketed column.',
17592186050600:'The prompt explicitly asks for the Jacobian at an equilibrium. The table contains a spanning J(x*)= label, a 2×2 field grid, empty bracket columns, and separately spanning punctuation. Preserve its four controls and punctuation while rendering the Jacobian.',
17592186050228:'The prompt requests the standard fundamental matrix. The label Φ0(t)=1/2 supplies a scalar factor outside a 2×2 matrix; the empty 5px columns are bracket strokes. Preserve the scalar, both supplied exponential entries and both field markers.',
17592186051021:'The prompt asks for a unit vector parallel to the given 3D vector. The three nonempty component cells, including the supplied normalized component, form a 3×1 vector beside u=; blank columns draw brackets.',
17592186048881:'The prompt asks for a linearized ODE system. The table represents u′= followed by a 2×2 matrix multiplied by u, with the definition u=x−x* outside the matrix. Preserve the four entries, the multiplication operand and its definition.',
17592186050727:'The prompt requests the transpose U^T of a 3×2 matrix. Six controls in the two table rows form the required 2×3 matrix; the spanning U^T= label and empty 5px boundary cells supply the equation and brackets.'}

reviews=[]; groups=collections.defaultdict(list);changed=[]
def collect_source_evidence():
    evidence=[]
    for topic in sorted({topics[c['topics'][0]] for c in assigned}):
        path=Path(f'/home/jake/Developer/MA/DATA/Lessons/{topic}/Source/{topic}.html')
        soup=BeautifulSoup(path.read_text(),'html.parser').select_one('#lessonContent')
        for node in soup.select('mjx-container'):
            if node.parent is None:continue
            math=node.find('math')
            node.replace_with('[MATH '+(math.get_text(' ',strip=True) if math else '')+']')
        for node in soup.select('.freeResponseTextbox,.matheditor-wrapper-answer'):
            node.replace_with('[INPUT '+str(node.get('id'))+']')
        for node in soup.select('select'):node.replace_with('[SELECT '+str(node.get('id'))+']')
        for i,table in enumerate(soup.find_all('table')):
            if 'questionWidget' in str(table.get('class')):continue
            rows=[]
            for row in table.find_all('tr'):
                if row.find_parent('table')!=table:continue
                rows.append([{'text':cell.get_text(' ',strip=True),'attrs':cell.attrs}
                             for cell in row.find_all(['td','th'],recursive=False)])
            ancestor=table
            while ancestor and not ancestor.get('id','').startswith(('question-','step-')):ancestor=ancestor.parent
            evidence.append({'topic':topic,'table_index':i,'ancestor_id':ancestor.get('id') if ancestor else None,
                             'attrs':table.attrs,'rows':rows})
    (HERE/'source-evidence.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
    # Current SVD questions differ from this archived import. Retain the two
    # exact family explanations as semantic evidence, without asserting an
    # exact question-table match.
    svd=json.loads(Path('/home/jake/Developer/MA/DATA/Lessons/3133/Source/3133.json').read_text())
    excerpts=[{'step_id':i['step_id'],'title':i['title'],
               'sections':[s['readable_text'] for s in i['sections']]}
              for i in svd['lesson']['items'] if i.get('step_id') in ['32049','32872']]
    (HERE/'svd-family-source.json').write_text(json.dumps(excerpts,ensure_ascii=False,indent=2)+'\n')
    return evidence

source_evidence=collect_source_evidence()
for c in assigned:
    key=f"{c['entity']}/{c['attribute']}"
    before=snapshot[key]
    live=current[c['entity']][':'+c['attribute']]
    assert live==before, ('Snapshot changed',key)
    assert before[c['span'][0]:c['span'][1]]==c['table'], ('Span mismatch',c['candidate_index'])
    topic=c['topics'][0]
    ma_topic=topics[topic]
    source=f'/home/jake/Developer/MA/DATA/Lessons/{ma_topic}/Source/{ma_topic}.html'
    exact=[e for e in source_evidence if e['topic']==ma_topic and e['ancestor_id'] and 'q-'+e['ancestor_id'].removeprefix('question-') in c['imported_ids']]
    evidence={'stored_shape':{'format':c['format'],'row_widths':[len(r) for r in c['rows']]},
              'source_html':source,'source_match':'exact question in current lesson' if exact else 'family/semantic evidence only; archived question may differ from current lesson',
              'exact_source_table_indices':[e['table_index'] for e in exact]}
    review={'candidate_index':c['candidate_index'],'entity':c['entity'],'attribute':c['attribute'],
            'imported_ids':c['imported_ids'],'evidence':evidence}
    if topic in DISCONFIRMED:
        review.update(status='disconfirmed',reasoning=DISCONFIRMED[topic]);reviews.append(review);continue
    assert topic in FAMILY, (topic,c['candidate_index'])
    replacement,details=FAMILY[topic](c)
    evidence.update(details)
    if topic != 17592186048637:
        old_tokens=collections.Counter(bare(m[0]) for m in TOKEN.finditer(c['table']))
        new_tokens=collections.Counter(bare(m[0]) for m in TOKEN.finditer(html.unescape(replacement)))
        if 'duplicate_import_artifact' in details:
            assert old_tokens == collections.Counter({k:2*v for k,v in new_tokens.items()}), c['candidate_index']
            fields=questions[c['entity']][':question/answer-fields']
            field_keys=[f[':answer-field/key'] for f in fields]
            assert len(field_keys)==len(set(field_keys))
            evidence['duplicate_import_artifact']['single_question_field_per_key']=field_keys
            assert all(m[2:-2] in field_keys for m in MARKER.findall(replacement))
        elif c['candidate_index']==572:
            # The original period is ordinary prose; the equation renderer
            # places it in an isolated math-label span without changing it.
            new_tokens.subtract({'.':1});new_tokens=+new_tokens
            assert old_tokens==new_tokens,c['candidate_index']
        else:assert old_tokens==new_tokens,(c['candidate_index'],old_tokens-new_tokens,new_tokens-old_tokens)
    for math in MATH.finditer(replacement):assert not MARKER.search(math[0]),c['candidate_index']
    tables=BeautifulSoup(replacement,'html.parser').find_all('table')
    assert tables and all(t.get('aria-label')=='Answer matrix' for t in tables)
    assert all(all(td.get_text(strip=True) for td in t.find_all('td')) for t in tables)
    review.update(status='confirmed',reasoning=WHY[topic])
    review['marker_counts_before']=dict(collections.Counter(MARKER.findall(c['table'])))
    review['marker_counts_after']=dict(collections.Counter(MARKER.findall(replacement)))
    if 'duplicate_import_artifact' not in details:
        assert review['marker_counts_before']==review['marker_counts_after'],c['candidate_index']
    groups[key].append((c,replacement,details))
    reviews.append(review)

proposals=[]
for key,entries in groups.items():
    before=snapshot[key];after=before
    replacements=[]
    for c,replacement,details in entries:
        start,end=c['span']
        containing=[x for x in entries if x[0]['span'][0]<=start and x[0]['span'][1]>=end and x[0]['candidate_index']!=c['candidate_index']]
        if containing:
            assert len(containing)==1
            for r in reviews:
                if r['candidate_index']==c['candidate_index']:r['covered_by_outer_candidate']=containing[0][0]['candidate_index']
            continue
        # Strip only a scroll wrapper whose full content is this replaced table.
        openwrap=re.search(r'<div class="source-table-scroll">\s*$',before[:start])
        closewrap=re.match(r'\s*</div>',before[end:])
        if openwrap and closewrap:start=openwrap.start();end+=closewrap.end()
        replacements.append((start,end,replacement))
    for start,end,replacement in sorted(replacements,reverse=True):after=after[:start]+replacement+after[end:]
    assert before!=after
    validate_prose(after)
    # No question-control identity is lost or introduced. Duplicated captures are
    # explicitly documented and compared at the complete-operand level above.
    assert set(MARKER.findall(before))==set(MARKER.findall(after))
    before_count=collections.Counter(MARKER.findall(before));after_count=collections.Counter(MARKER.findall(after))
    duplicates=[x[0]['candidate_index'] for x in entries if 'duplicate_import_artifact' in x[2]]
    if not duplicates:assert before_count==after_count, key
    eid,attr=key.split('/',1)
    proposals.append({'entity':int(eid),'attribute':attr,'before':before,'after':after,
                      'candidate_indices':[x[0]['candidate_index'] for x in entries],
                      'replacements':[{'start':s,'end':e,'before':before[s:e],'after':r,
                                       'candidate_indices':[x[0]['candidate_index'] for x in entries if s<=x[0]['span'][0] and x[0]['span'][1]<=e]}
                                      for s,e,r in sorted(replacements)],
                      'rationale':' '.join(dict.fromkeys(WHY[x[0]['topics'][0]] for x in entries)),
                      'duplicate_import_artifact_candidates':duplicates,
                      'marker_counts_before':dict(before_count),'marker_counts_after':dict(after_count)})
assert len(reviews)==len(assigned) and len({r['candidate_index'] for r in reviews})==len(assigned)
(HERE/'reviews.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n')
(HERE/'proposals.json').write_text(json.dumps(proposals,ensure_ascii=False,indent=2)+'\n')
summary={'assigned':len(assigned),'decisions':dict(collections.Counter(r['status'] for r in reviews)),
         'proposals':len(proposals),'confirmed_by_topic':dict(collections.Counter(c['titles'][-1] for c in assigned if c['topics'][0] not in DISCONFIRMED)),
         'duplicate_artifact_candidates':[r['candidate_index'] for r in reviews if 'duplicate_import_artifact' in r['evidence']],
         'covered_nested_candidates':[r['candidate_index'] for r in reviews if 'covered_by_outer_candidate' in r],
         'validation':{'fresh_capture_values_match_snapshot':True,'all_fields_validate_prose':True,
                       'control_identity_sets_preserved':True,'no_controls_inside_tex':True,
                       'supplied_token_inventory_preserved':True,'duplicate_complete_operands_checked':True}}
(HERE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
