import assert from 'node:assert/strict';
import test from 'node:test';
import { createGraphPreferences } from '../ui/graph-preferences.js';

const defaults = () => ({ colorCode: true, courses: ['255', '256', '341'], includeQueue: true,
  splitByCourse: false, weeks: { kind: 'all' } });
const reply = value => ({ ok: true, json: async () => structuredClone(value) });

test('two independent origins share saved display choices and send only changed fields', async () => {
  let saved = defaults();
  const posts = [], errors = [], views = [{}, {}];
  const fetcher = async (_url, options) => {
    if (options.body) {
      const changes = JSON.parse(options.body).changes; posts.push(changes);
      saved = { ...saved, ...changes };
    }
    return reply(saved);
  };
  const clients = views.map((_, index) => createGraphPreferences({ fetcher,
    apply: value => { views[index] = value; }, onError: error => { if (error) errors.push(error); } }));
  await Promise.all(clients.map(client => client.refresh()));
  clients[0].save({ colorCode: false }); await clients[0].refresh();
  clients[1].save({ courses: ['341'], includeQueue: false }); await clients[1].refresh();
  await Promise.all(clients.map(client => client.refresh()));
  assert.deepEqual(views[0], views[1]);
  assert.equal(views[0].colorCode, false);
  assert.deepEqual(views[0].courses, ['341']);
  assert.deepEqual(posts, [{ colorCode: false }, { courses: ['341'], includeQueue: false }]);
  assert.deepEqual(errors, []);
});

test('a stale read cannot reverse a newer local change', async () => {
  let resolveRead, shown;
  const client = createGraphPreferences({ apply: value => { shown = value; }, onError() {},
    fetcher: async (_url, options) => options.body ? reply({ ...defaults(), colorCode: false }) :
      new Promise(resolve => { resolveRead = resolve; }) });
  const reading = client.refresh();
  client.save({ colorCode: false }); await client.refresh();
  resolveRead(reply(defaults())); await reading;
  assert.equal(shown.colorCode, false);
});

test('failed saves retain the latest changes for retry without reverting a rapid toggle', async () => {
  let rejectSave, shown, writes = 0;
  const client = createGraphPreferences({ apply: value => { shown = value; }, onError() {},
    fetcher: async (_url, options) => {
      writes++;
      if (writes === 1) return new Promise((_resolve, reject) => { rejectSave = reject; });
      return reply({ ...defaults(), ...JSON.parse(options.body).changes });
    } });
  client.save({ colorCode: false });
  client.save({ colorCode: true, splitByCourse: true });
  rejectSave(new Error('Disconnected'));
  await assert.rejects(client.refresh());
  await client.refresh();
  assert.equal(shown.colorCode, true);
  assert.equal(shown.splitByCourse, true);
});
