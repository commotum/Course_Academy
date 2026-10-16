import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = (await readFile(new URL('../ui/requests.js', import.meta.url), 'utf8')).replaceAll('export ', '');
function client(fetch) {
  return vm.runInNewContext(`(() => { ${source}; return { readRequest, readCurrentLearner }; })()`, { fetch });
}

test('concurrent reads share one fetch with separately readable response bodies', async () => {
  let resolve, calls = 0;
  const api = client((_path, settings) => {
    calls++;
    assert.equal(settings.cache, 'no-cache');
    return new Promise(done => { resolve = done; });
  });
  const a = api.readCurrentLearner(), b = api.readCurrentLearner();
  assert.equal(calls, 1);
  resolve(new Response(JSON.stringify({ learner: { targets: [42] } })));
  assert.deepEqual(await a, { targets: [42] });
  assert.deepEqual(await b, { targets: [42] });
});

test('completed reads and failed reads are refreshed on the next request', async () => {
  let calls = 0;
  const api = client(async () => {
    if (++calls === 1) throw new Error('offline');
    return new Response(JSON.stringify({ learner: { revision: calls } }));
  });
  await assert.rejects(api.readCurrentLearner(), /offline/);
  assert.equal((await api.readCurrentLearner()).revision, 2);
  assert.equal((await api.readCurrentLearner()).revision, 3);
});

test('mutations and abortable reads keep independent requests', async () => {
  let calls = 0;
  const api = client(async () => { calls++; return new Response('{}'); });
  const controller = new AbortController();
  await Promise.all([
    api.readRequest('/api/learner', { signal: controller.signal }),
    api.readRequest('/api/learner', { signal: controller.signal }),
    api.readRequest('/api/target', { method: 'POST', body: '{}' }),
    api.readRequest('/api/target', { method: 'POST', body: '{}' }),
  ]);
  assert.equal(calls, 4);
});
