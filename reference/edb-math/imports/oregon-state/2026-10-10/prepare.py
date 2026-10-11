#!/usr/bin/env python3
"""Prepare OSU layers from saved transactions. Reads files; never commits to EDB."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import sys
import uuid
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, '/home/jake/Developer/Course_Academy/capture')
from scripts.database.edn import kw, Keyword, Tagged, dumps, loads
from scripts.database.images import ImageLibrary

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'output'
def read(name): return json.loads((ROOT/name).read_text())
def save(name, value):
    (ROOT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

state = read('db/state.json')
attrs = {row[1]: (row[2], row[3]) for row in state['attributes']}
original = read('assignments-original.json')
additions = read('assignments-additions.json')
reference = read('assignments-merged-reference.json')
audit = read('assignment-layer-audit.json')
full = {e[':db/id']:e for e in reference}
base = {e[':db/id']:e for e in original}
patches = {e[':db/id']:e for e in additions}
ids = {uid: next((k, v['$uuid']) for k,v in e.items() if k != ':db/id' and k.endswith('/id')) for uid,e in full.items()}
changes = []

# Assumptions written by the study author belong only to that author's layer.
for uid in ('e1c86b2f-9af3-50b9-8209-64644c12c39a', 'b990240c-49ef-55fd-aa91-1ef51a672c6c'):
    text = base[uid][':question/problem']
    new, n = re.subn(r'\n\n\*\*Source gap:\*\*[^\n]+', '', text)
    assert n == 1 and ':question/problem' in patches[uid]
    base[uid][':question/problem'] = new
    changes.append({'id':uid,'change':'Keep authored density interpretation only in the agent layer.'})
uid = '060f02f4-487e-5f5b-8a1c-5f000f57d3c8'
sentence = ' Interpret counterclockwise as viewed from above (positive z).'
assert sentence in base[uid][':question/problem'] and ':question/problem' in patches[uid]
base[uid][':question/problem'] = base[uid][':question/problem'].replace(sentence, '')
changes.append({'id':uid,'change':'Keep authored orientation assumption only in the agent layer.'})

# Keep the linked source, title, and deadline in the baseline. The saved summaries
# and import notes are locally written prose and are restored by the agent layer.
for e in original:
    if ':tutorial/content' not in e: continue
    before = e[':tutorial/content']
    prefix = before.split('\n\n## Instructions', 1)[0]
    lines = [line for line in prefix.splitlines()
             if not line or line.startswith(('**', 'Date:', 'Due:', 'Source:', 'Textbook:', 'MTH '))]
    e[':tutorial/content'] = '\n'.join(lines).strip()
    assert ':tutorial/content' in patches[e[':db/id']]
    if e[':tutorial/content'] != before:
        changes.append({'id':e[':db/id'],'change':'Move condensed instructions and local import notes to author layer; preserve source links.'})

# The two corrected deadlines came from Jake, after the originals and study work.
deadlines = []
for change in audit['due_corrections']:
    uid = change['activity_id']
    e = base[uid]
    deadlines.append({':db/id':uid, ':activity/due':e.pop(':activity/due')})
    intro_id = base[e[':activity/first-step']][':step/content']
    deadlines.append({':db/id':intro_id, ':tutorial/content':full[intro_id][':tutorial/content']})
    for layer in (base, patches):
        layer[intro_id][':tutorial/content'] = layer[intro_id][':tutorial/content'].replace('Due: '+change['date'], 'Due: unknown')

merged = copy.deepcopy(base)
for e in additions + deadlines:
    merged.setdefault(e[':db/id'], {}).update(e)
assert merged == full, 'Final layers must restore the exact saved graph, before schema/image migration.'

images = ImageLibrary(OUT, ROOT)
asset_manifest = {}
def text_images(text):
    def localize(match):
        source = match[0]
        path = Path(parse_qs(urlsplit(source).query)['path'][0])
        assert path.is_file(), str(path)
        target = images.store(path.read_bytes(), source)
        asset_manifest[str(path)] = {'path':target, 'sha256':Path(target).stem}
        return target
    text = re.sub(r'/api/asset\?path=[^\s)"<>]+', localize, text)
    return images.text(text)

def lookup(uid):
    attr, value = ids[uid]
    return [kw(attr), uuid.UUID(value)]

def value(v, attr, new_ids):
    if isinstance(v, dict):
        if '$uuid' in v: return uuid.UUID(v['$uuid'])
        if '$inst' in v: return Tagged('inst', v['$inst'])
        if '$ref' in v:
            a, x = v['$ref']
            if a == ':topic/math-academy-id':
                assert int(x) in {int(row[0]) for row in state['topics']}, x
            return [kw(a), value(x, a, new_ids)]
        raise ValueError(v)
    if isinstance(v, list): return [value(x, attr, new_ids) for x in v]
    if isinstance(v, str):
        t = attrs.get(attr, ('', ''))[0]
        if attr == ':db/ensure' or t in (':db.type/ref', ':db.type/keyword'):
            if v.startswith(':'): return kw(v)
            if v in ids: return v if v in new_ids else lookup(v)
        if t == ':db.type/string': return text_images(v)
    return v

def convert(rows, existing):
    new_ids = {e[':db/id'] for e in rows} - existing
    result = []
    for e in rows:
        uid = e[':db/id']
        m = {kw('db/id'): uid if uid in new_ids else lookup(uid)}
        for k,v in e.items():
            if k in (':db/id', ':question/is-example'): continue
            if uid in existing and k.endswith('/id'): continue
            if k == ':activity/scope':
                assert v['$ref'][0] == ':course/id'
                k = ':activity/course'
            assert k in attrs or k == ':db/ensure', k
            m[kw(k)] = value(v, k, new_ids)
        result.append(m)
    return result

orig_edn = convert(original, set())
add_edn = convert(additions, set(base))
dates_edn = convert(deadlines, set(full))

course_rows = loads((ROOT/'prior-seeds/2-courses.edn').read_text())
courses = [e for e in course_rows if ':course/id' in e]
assert len(courses) == 6
group = loads((ROOT/'prior-seeds/1-course-groups.edn').read_text())[0]
group[kw('db/id')] = 'osu-mth'
group[kw('course-group/courses')] = [e[':db/id'] for e in courses]
group[kw('db/ensure')] = kw('course-group/validate')
core_courses, maps = [], []
for e in courses:
    core_courses.append({k:v for k,v in e.items() if k in (':db/id', ':course/id', ':course/title', ':course/code', ':course/school')})
    core_courses[-1][kw('db/ensure')] = kw('course/identity-validate')
    maps.append({kw('db/id'):[kw('course/id'),e[':course/id']],
                 **{k:v for k,v in e.items() if k in (':course/description',':course/overview',':course/outcomes')},
                 kw('db/ensure'):kw('course/identity-validate')})
assert sum(len(e[':course/outcomes']) for e in maps) == 62

transactions = []
def emit(path, source, rows, comments):
    target = OUT/'seeds'/path
    target.parent.mkdir(parents=True, exist_ok=True)
    header = ['Prepared only. Supply '+source+' as the transaction source.'] + comments
    target.write_text(''.join(';; '+line+'\n' for line in header)+'[\n'+''.join(' '+dumps(row)+'\n' for row in rows)+']\n')
    transactions.append({'path':'seeds/'+path,'source':source,'maps':len(rows),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})

emit('oregon-state/1-oregon-state.edn', ':person/jake',
     [{kw('db/id'):'Oregon-State',kw('db/ident'):kw('org/Oregon-State'),kw('db/doc'):'Oregon State University'}],
     ['Register the source for the OSU course catalog and assigned source material.'])
emit('oregon-state/2-courses.edn', ':org/Oregon-State', core_courses+[group],
     ['After 1-oregon-state.edn. Six course identities and membership in OSU-MTH.',
      'Names checked against https://catalog.oregonstate.edu/courses/mth/ (2026-10-10).',
      'Preserves historical MTH 251/252 codes and stable UUIDs; catalog lists their Z equivalents.',
      'Locally authored descriptions, overviews, and outcomes are in 5-course-maps.edn.'])
emit('oregon-state/3-assignments.edn', ':org/Oregon-State', orig_edn,
     ['After 2-courses.edn. All 19 assignments: 176 assigned problems, 241 questions, 38 multisteps.',
      'Saved transcriptions of assigned source material; original publisher/PDF links are retained.',
      'OSU is the assigning institution; publisher material is not claimed to be authored by OSU.',
      'No generated answers, worked solutions, topic mappings, or learner facts.',
      'Questions are initially fieldless; original choice content is displayed without a key.'])
emit('oregon-state/4-assignment-study-content.edn', ':agent/gpt-6-astra-high', add_edn,
     ['After 3-assignments.edn. Authorship verified from saved writing-session model/effort records.',
      'Adds answer fields, answer keys, worked solutions, reference graphics, topic mappings,',
      'response markup, local assumptions, and condensed assignment instructions.',
      'Preserves the original question, assignment, and step UUIDs.'])
emit('local/chatgpt-6-pro.edn', ':person/jake',
     [{kw('db/ident'):kw('agent/chatgpt-6-pro'),kw('db/doc'):'ChatGPT 6 Pro — course-map author identified from Jake\'s recollection; exact model not recorded in the saved export.'}],
     ['Register before oregon-state/5-course-maps.edn. Attribution supplied by Jake on 2026-10-10.'])
emit('oregon-state/5-course-maps.edn', ':agent/chatgpt-6-pro', maps,
     ['After 2-courses.edn and ../local/chatgpt-6-pro.edn.',
      'Six authored descriptions, six overviews, and 62 ordered outcomes from the saved course maps.',
      'Author attribution is based on Jake\'s recollection, not a model identifier in the export.'])
emit('oregon-state/6-deadline-corrections.edn', ':person/jake', dates_edn,
     ['After 4-assignment-study-content.edn. Two deadlines supplied directly by Jake on 2026-10-07.',
      'MTH 255 R-2: October 6. MTH 255 WHW-2: October 8. Both date-only deadlines use',
      '23:59:59 America/Los_Angeles, preserving the previously committed interpretation.',
      'Updates activity/due and its displayed assignment-information text.'])

# Graph validation is independent of the transactor's required-attribute checks.
owners = collections.defaultdict(list)
for uid,e in full.items():
    for attr in (':activity/steps',':multistep/steps',':question/answer-fields',':answer-field/choices'):
        for child in e.get(attr,[]):
            assert child in full, (uid,attr,child)
            owners[child].append((uid,attr))
    for prefix in ('activity','multistep'):
        if ':'+prefix+'/steps' not in e:continue
        expected = e[':'+prefix+'/steps']
        cursor, chain = e[':'+prefix+'/first-step'], []
        while cursor:
            assert cursor not in chain, ('cycle',uid)
            chain.append(cursor)
            assert full[cursor][':step/content'] in full
            cursor = full[cursor].get(':step/next')
        assert chain == expected, (uid,'step order')
    if ':answer-field/correct' in e:
        assert e[':answer-field/correct'] in e[':answer-field/choices']
    if ':question/answer-fields' in e:
        keys = [full[f][':answer-field/key'] for f in e[':question/answer-fields']]
        assert len(keys) == len(set(keys)), uid
assert all(len(v)==1 for v in owners.values()), 'Component sharing'
assert not any(k.startswith((':learner/', ':task/', ':task-item/')) for e in full.values() for k in e)
assert not any(k in e for e in original for k in (':question/worked-solution',':question/answer-fields',':assigned-problem/topic-coverage'))
for e in original:
    assert '**Source gap:**' not in e.get(':question/problem','')
assert not any('/api/asset?' in (OUT/t['path']).read_text() for t in transactions)
for p in (OUT/'images').rglob('*'):
    if p.is_file():assert hashlib.sha256(p.read_bytes()).hexdigest() == p.stem

save('image-map.json',asset_manifest)
save('migration-adjustments.json',changes)
save('prepared-manifest.json',{'basis_read':state['basis'],'committed':False,
     'transactions':transactions,'assignment_counts':audit['merged_counts'],
     'image_files':len(list((OUT/'images').rglob('*.*'))),'image_source_paths':len(asset_manifest),
     'topic_coverage_targets':len({r['$ref'][1] for e in additions for r in e.get(':assigned-problem/topic-coverage',[])}),
     'checks':{'exact_final_graph_before_schema_and_image_migration':True,'stable_uuid_preservation':True,
               'all_step_chains':True,'component_ownership':True,'correct_answer_membership':True,
               'no_learner_writes':True,'images_hash_verified':True}})

# Pull every entity in the final speculative database; independent verifier checks values.
all_ids = [lookup(uid) for uid in full]
all_ids += [[kw('course/id'),e[':course/id']] for e in courses]
all_ids += [[kw('course-group/id'),group[':course-group/id']]]
all_ids += [[kw('course-outcome/id'),o[':course-outcome/id']] for c in maps for o in c[':course/outcomes']]
(ROOT/'pull-identities.edn').write_text(dumps(all_ids)+'\n')
(ROOT/'pull-pattern.edn').write_text('[*]\n')
print(json.dumps({'files':len(transactions),'assignments':19,'questions':241,'images':len(list((OUT/'images').rglob('*.*')))}))
