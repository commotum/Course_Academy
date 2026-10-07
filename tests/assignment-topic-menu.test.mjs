import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { attachTopicMenu } from '../ui/topic-menu.js';

test('assignment preparation links offer all three topic actions and preserve ordinary navigation', async () => {
  class Node extends EventTarget {
    constructor(tag = 'div') { super(); this.tagName = tag; this.children = []; this.attrs = {}; this.dataset = {}; this.style = {}; }
    append(...children) { for (const child of children) { child.parentElement = this; this.children.push(child); } }
    setAttribute(key, value) { this.attrs[key] = value; }
    contains(node) { for (; node; node = node.parentElement) if (node === this) return true; return false; }
    get isConnected() { return document.body.contains(this); }
    getBoundingClientRect() { return { left: 20, top: 40, bottom: 82, width: 180, height: 110 }; }
    focus() { document.activeElement = this; }
    click() { return this.dispatchEvent(new Event('click', { cancelable: true })); }
  }
  const doc = new Node(); doc.body = new Node('body');
  doc.documentElement = { clientWidth: 800, clientHeight: 600 }; doc.activeElement = doc.body;
  doc.createElement = tag => new Node(tag);
  const win = new Node();
  const originals = new Map();
  for (const [name, value] of Object.entries({ document: doc, window: win, Element: Node })) {
    originals.set(name, Object.getOwnPropertyDescriptor(globalThis, name));
    Object.defineProperty(globalThis, name, { value, configurable: true });
  }
  const fire = (receiver, type, values = {}) => {
    const event = new Event(type, { cancelable: true });
    for (const [key, value] of Object.entries(values)) Object.defineProperty(event, key, { value });
    receiver.dispatchEvent(event); return event;
  };
  try {
    const source = await readFile(new URL('../ui/assignments.js', import.meta.url), 'utf8');
    const coverage = source.slice(source.indexOf('function coverage('), source.indexOf('function contentView('));
    const context = vm.createContext({ attachTopicMenu,
      el: (tag, className, text) => { const node = new Node(tag); node.className = className; node.textContent = text; return node; },
      link: (text, href) => { const node = new Node('a'); node.textContent = text; node.href = href; return node; },
      topicURL: topic => '/topic?topic=' + encodeURIComponent(topic.uuid),
    });
    const render = vm.runInContext(coverage + '\ncoverage;', context);
    const section = render([{ id: 20, uuid: 'topic-one', title: 'First topic' }, { id: 25, uuid: 'topic-two', title: 'Second topic' }]);
    doc.body.append(section);
    const [first, second] = section.children[1].children.map(row => row.children[0]);
    assert.equal(first.href, '/topic?topic=topic-one');
    assert.equal(first.click(), true); // Menu registration does not intercept normal clicks.
    const nested = new Node('span'); first.append(nested); nested.dataset.topicId = '999';
    const menu = doc.body.children.find(node => node.className === 'topic-context-menu');
    assert.equal(fire(doc, 'contextmenu', { target: nested, clientX: 795, clientY: 595 }).defaultPrevented, true);
    assert.equal(menu.hidden, false);
    assert.equal(menu.style.left, '612px'); assert.equal(menu.style.top, '482px');
    assert.equal(menu.attrs['aria-label'], 'Actions for First topic');
    assert.deepEqual(menu.children.map(node => node.textContent), ['Study now', 'Go to topic', 'View in graph']);
    assert.deepEqual(menu.children.map(node => node.href), ['/learn?topicId=20', '/topic?topic=topic-one', '/?course=all&topic=20']);
    assert.equal(doc.activeElement, menu.children[0]);
    fire(doc, 'keydown', { target: menu.children[0], key: 'ArrowDown' });
    assert.equal(doc.activeElement, menu.children[1]);
    fire(doc, 'keydown', { target: menu.children[1], key: 'End' });
    assert.equal(doc.activeElement, menu.children[2]);
    fire(doc, 'keydown', { target: menu.children[2], key: 'Escape' });
    assert.equal(menu.hidden, true); assert.equal(doc.activeElement, first);
    assert.equal(first.attrs['aria-expanded'], 'false');
    fire(doc, 'keydown', { target: second, key: 'F10', shiftKey: true });
    assert.deepEqual(menu.children.map(node => node.href), ['/learn?topicId=25', '/topic?topic=topic-two', '/?course=all&topic=25']);
    assert.equal(menu.children[0].click(), true); // Navigation reaches the existing assignment pause handler.
    assert.equal(menu.hidden, true);
    fire(doc, 'contextmenu', { target: first, clientX: 40, clientY: 60 });
    fire(doc, 'scroll'); assert.equal(menu.hidden, true);
    fire(doc, 'contextmenu', { target: first, clientX: 40, clientY: 60 });
    fire(doc, 'pointerdown', { target: doc.body }); assert.equal(menu.hidden, true);
    for (const values of [{ target: first, shiftKey: true }, { target: doc.body }]) {
      assert.equal(fire(doc, 'contextmenu', values).defaultPrevented, false);
      assert.equal(menu.hidden, true);
    }
  } finally {
    for (const [name, descriptor] of originals) {
      if (descriptor) Object.defineProperty(globalThis, name, descriptor);
      else delete globalThis[name];
    }
  }
});
