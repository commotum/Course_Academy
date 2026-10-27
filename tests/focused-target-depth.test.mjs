import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { projectTargetScope } from '../ui/target-scope.js';

test('target projection defaults to focused depth zero and preserves explicit depth controls', () => {
  const snapshot = {
    nodes: Array.from({ length: 33 }, (_, id) => ({ id, name: `Topic ${id}` })),
    links: Array.from({ length: 32 }, (_, id) => ({ source: id, target: id + 1 })),
    learner: { targets: [32], queue: [] }, courses: [],
  };
  assert.deepEqual([...projectTargetScope(snapshot).nodeIds].sort(), [30, 31, 32]);
  snapshot.studyDefaults = { targetPrerequisiteDepth: 0 };
  assert.deepEqual([...projectTargetScope(snapshot).nodeIds], [32]);
  assert.deepEqual([...projectTargetScope(snapshot, { prerequisiteDepth: 1 }).nodeIds].sort(), [31, 32]);
});

test('actual graph initialization uses the server code policy for the targets overview', async () => {
  const html = await readFile(new URL('../ui/Math-Academy-Graph-Explorer.html', import.meta.url), 'utf8');
  const source = html.slice(html.indexOf('  async function loadData()'), html.indexOf("  $('retryLoad').onclick=loadData;"));
  for (const depth of [undefined, 0, 2]) {
    const data = { learner: { courseId: 'course', name: 'Learner' },
      ...(depth === undefined ? {} : { studyDefaults: { targetPrerequisiteDepth: depth } }) };
    const elements = new Map(), calls = [];
    const context = vm.createContext({
      URL, loading: false, focusedModeRefresh: false, snapshot: null,
      location: { protocol: 'http:', href: 'http://example.test/?view=targets' },
      $: id => { if (!elements.has(id)) elements.set(id, {}); return elements.get(id); },
      readRequest: async () => ({ ok: true, json: async () => data }),
      installSnapshot: value => { context.snapshot = value; },
      changeCourse: (...args) => calls.push(args), nodeById: new Map(),
      renderTargetCourseFilters() {}, renderTargetWeekStrip() {},
    });
    await vm.runInContext(`${source}\nloadData()`, context);
    assert.equal(calls.length, 1);
    assert.deepEqual([...calls[0]], ['course', false, 'targets', String(depth ?? 2)]);
  }
});
