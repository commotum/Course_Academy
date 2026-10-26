import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

test('assignment preparation links register the topic rather than the surrounding problem', async () => {
  const source = await readFile(new URL('../ui/assignments.js', import.meta.url), 'utf8');
  const registrations = [];
  const el = (tag, className, text) => ({ tag, className, text, children: [], append(...nodes) { this.children.push(...nodes); } });
  const context = vm.createContext({ el, link: (text, href) => ({ text, href }), topicURL: topic => '/topic?topic=' + topic.uuid,
    attachTopicMenu: (node, topic) => registrations.push({ node, topic }) });
  const render = vm.runInContext(source.slice(source.indexOf('function coverage('), source.indexOf('function contentView(')) + '\ncoverage;', context);
  const topic = { id: 20, uuid: 'topic-one', title: 'First topic' };
  render([topic]);
  assert.equal(registrations.length, 1);
  assert.equal(registrations[0].topic, topic);
  assert.equal(registrations[0].node.href, '/topic?topic=topic-one');
});
