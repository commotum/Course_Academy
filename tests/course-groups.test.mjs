import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = (await readFile(new URL('../ui/navigation.js', import.meta.url), 'utf8'))
  .replace(/^import .*;\n/, '').replaceAll('export ', '');
const { courseGroupLabel, indexCurriculum, searchCurriculum } = vm.runInNewContext(
  `(() => { ${source}; return { courseGroupLabel, indexCurriculum, searchCurriculum }; })()`,
  { document: { querySelector: () => null } },
);

test('course labels display group titles verbatim, including multiple memberships', () => {
  assert.equal(courseGroupLabel({ groups: [{ title: 'High School - Integrated Math (Honors)' }] }), 'High School - Integrated Math (Honors)');
  assert.equal(courseGroupLabel({ groups: [{ title: 'Advanced Placement' }, { title: 'University' }] }), 'Advanced Placement · University');
  assert.equal(courseGroupLabel({ groups: [] }), 'Course');
});

test('Explore course results use group labels with their topic counts', () => {
  const index = indexCurriculum({
    courses: [{ id: 'foundations', title: 'Mathematical Foundations II', groups: [{ id: 'group', title: 'Mathematical Foundations' }], topicIds: [1, 2] }],
    nodes: [],
  });
  const result = searchCurriculum(index, 'Foundations II');
  assert.equal(result.courses.length, 1);
  assert.equal(result.courses[0].meta, 'Mathematical Foundations · 2 topics');
});
