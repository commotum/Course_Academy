"""Read-only, fixed-basis inventory of Triangular Matrices instructional images."""
from pathlib import Path
import json
import re
import sys
sys.dont_write_bytecode = True
ROOT = next(path for path in Path(__file__).resolve().parents if (path / 'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps

HERE = Path(__file__).resolve().parent
db = Publisher.from_environment(source=':agent/gpt-6.1-sol-high').client
status = db.status()
basis = status['basis']
out = HERE / f'capture-{basis}'
out.mkdir(parents=True, exist_ok=True)
pull = (ROOT / 'reference/mathacademy/repairs/2026-10-14-linear-algebra-latex/lesson-pull.edn').read_text().strip()
result = db.query('[:find (pull ?topic ' + pull + ') :in $ ?topic :where [?topic :topic/id _]]', [17592186050283], out, 'topic', basis)
topic = result[0][0]
(out / 'snapshot.edn').write_text(dumps({**status, 'topic': topic}) + '\n')
(out / 'snapshot.json').write_text(json.dumps({**status, 'topic': topic}, indent=2, default=str) + '\n')
fields = {}
def walk(value):
    if isinstance(value, list):
        for item in value:
            walk(item)
    elif isinstance(value, dict):
        for attr in (':tutorial/content', ':question/problem', ':question/worked-solution', ':answer/value', ':answer/feedback'):
            if isinstance(value.get(attr), str):
                fields[(value[':db/id'], attr)] = {'entity': value[':db/id'], 'attribute': attr, 'value': value[attr],
                                                 'source_id': value.get(':question/math-academy-id', value.get(':tutorial/math-academy-id')),
                                                 'images': re.findall(r'!\[[^\]]*\]\(([^)]+)\)', value[attr])}
        for item in value.values():
            walk(item)
walk(topic)
images = [field for field in fields.values() if field['images']]
save = {'basis': basis, 'topic': topic[':db/id'], 'title': topic[':topic/title'], 'fields': len(fields), 'image_fields': images}
(out / 'image-fields.json').write_text(json.dumps(save, indent=2) + '\n')
(HERE / 'capture-directory.txt').write_text(str(out.relative_to(ROOT)) + '\n')
print(json.dumps({'basis': basis, 'topic': save['title'], 'knowledge_points': len(topic[':topic/knowledge-points']),
                  'fields': len(fields), 'image_fields': [{key: item[key] for key in ('entity', 'attribute', 'source_id', 'images')} for item in images]}, indent=2))
