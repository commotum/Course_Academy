import assert from 'node:assert/strict';
import test from 'node:test';
import { attachStepMenu, stepEntityId } from '../ui/step-menu.js';

test('database IDs preserve exact digits and reject UUIDs or rounded numbers', () => {
  assert.equal(stepEntityId(17592186157459), '17592186157459');
  assert.equal(stepEntityId('18446744073709551615'), '18446744073709551615');
  for (const value of [null, undefined, '', 0, -1, 1.5, Number.MAX_SAFE_INTEGER + 1, 'abc', 'step-1', '1e3']) {
    assert.equal(stepEntityId(value), null);
  }
});

test('step menus copy the selected container ID and support keyboard, dismissal, and clipboard failure', async () => {
  class Node extends EventTarget {
    constructor(tag = 'div') {
      super(); this.tagName = tag; this.children = []; this.dataset = {}; this.style = {}; this.attrs = {};
    }
    append(...children) { for (const child of children) { child.parentElement = this; this.children.push(child); } }
    setAttribute(key, value) { this.attrs[key] = value; }
    contains(node) { for (; node; node = node.parentElement) if (node === this) return true; return false; }
    get isConnected() { return document.body.contains(this); }
    closest() { return ['input', 'textarea', 'select'].includes(this.tagName) ? this : null; }
    getBoundingClientRect() { return { left: 20, top: 40, width: 180, height: 42 }; }
    focus() { document.activeElement = this; }
  }
  const doc = new Node();
  doc.body = new Node('body'); doc.documentElement = { clientWidth: 800, clientHeight: 600 }; doc.activeElement = doc.body;
  doc.createElement = tag => new Node(tag);
  const win = new Node();
  const copied = [], prompted = [];
  win.prompt = (message, id) => prompted.push(id);
  const clipboard = { writeText: async id => { copied.push(id); } };
  const originals = new Map();
  for (const [name, value] of Object.entries({ document: doc, window: win, Element: Node, navigator: { clipboard } })) {
    originals.set(name, Object.getOwnPropertyDescriptor(globalThis, name));
    Object.defineProperty(globalThis, name, { value, configurable: true });
  }
  const fire = (receiver, type, values = {}) => {
    const event = new Event(type, { cancelable: true });
    for (const [key, value] of Object.entries(values)) Object.defineProperty(event, key, { value });
    receiver.dispatchEvent(event); return event;
  };
  const settle = () => new Promise(resolve => setImmediate(resolve));
  try {
    const first = new Node('section'), second = new Node('section'), nestedMath = new Node('svg'), input = new Node('input');
    first.append(nestedMath, input); doc.body.append(first, second);
    attachStepMenu(first, '17592186000101', '18446744073709551615'); attachStepMenu(second, '17592186000102');
    const menu = doc.body.children.find(node => node.className === 'step-context-menu');
    const action = menu.children[0];
    const academyAction = menu.children[1];
    assert.equal(action.textContent, 'Copy :db/id');
    assert.equal(academyAction.textContent, 'Copy :ma/id');
    nestedMath.dataset.stepDbId = '999'; // Content cannot spoof a registered step.
    nestedMath.dataset.mathAcademyId = '999';
    const rightClick = fire(doc, 'contextmenu', { target: nestedMath, clientX: 795, clientY: 595 });
    assert.equal(rightClick.defaultPrevented, true);
    assert.equal(menu.hidden, false);
    assert.equal(menu.style.left, '612px'); assert.equal(menu.style.top, '550px');
    assert.equal(doc.activeElement, action);
    assert.equal(academyAction.hidden, false);
    fire(action, 'click'); await settle();
    assert.deepEqual(copied, ['17592186000101']);
    assert.equal(menu.hidden, true); assert.equal(doc.activeElement, first);

    fire(doc, 'keydown', { target: first, key: 'ContextMenu' });
    fire(doc, 'keydown', { target: action, key: 'ArrowDown' });
    assert.equal(doc.activeElement, academyAction);
    fire(doc, 'keydown', { target: academyAction, key: 'ArrowDown' });
    assert.equal(doc.activeElement, action);
    fire(doc, 'keydown', { target: action, key: 'End' });
    assert.equal(doc.activeElement, academyAction);
    fire(doc, 'keydown', { target: academyAction, key: 'Home' });
    assert.equal(doc.activeElement, action);
    fire(academyAction, 'click'); await settle();
    assert.deepEqual(copied, ['17592186000101', '18446744073709551615']);

    fire(doc, 'keydown', { target: second, key: 'F10', shiftKey: true });
    assert.equal(menu.hidden, false);
    assert.equal(academyAction.hidden, true);
    fire(doc, 'keydown', { target: action, key: 'End' });
    assert.equal(doc.activeElement, action);
    fire(action, 'click'); await settle();
    assert.deepEqual(copied, ['17592186000101', '18446744073709551615', '17592186000102']);

    fire(doc, 'contextmenu', { target: first, clientX: 40, clientY: 60 });
    fire(doc, 'keydown', { target: action, key: 'Escape' });
    assert.equal(menu.hidden, true); assert.equal(doc.activeElement, first);
    fire(doc, 'contextmenu', { target: first, clientX: 40, clientY: 60 });
    fire(doc, 'scroll'); assert.equal(menu.hidden, true);
    fire(doc, 'contextmenu', { target: second, clientX: 40, clientY: 60 });
    fire(doc, 'pointerdown', { target: doc.body }); assert.equal(menu.hidden, true);

    for (const values of [{ target: input }, { target: first, shiftKey: true }, { target: doc.body }]) {
      assert.equal(fire(doc, 'contextmenu', values).defaultPrevented, false);
      assert.equal(menu.hidden, true);
    }
    clipboard.writeText = async () => { throw new Error('Permission denied'); };
    fire(doc, 'contextmenu', { target: second, clientX: 40, clientY: 60 });
    fire(action, 'click'); await settle();
    assert.deepEqual(prompted, ['17592186000102']);
    fire(doc, 'contextmenu', { target: first, clientX: 40, clientY: 60 });
    fire(academyAction, 'click'); await settle();
    assert.deepEqual(prompted, ['17592186000102', '18446744073709551615']);
    assert.equal(doc.body.children.find(node => node.className === 'step-copy-notice').textContent, '');
  } finally {
    for (const [name, descriptor] of originals) {
      if (descriptor) Object.defineProperty(globalThis, name, descriptor);
      else delete globalThis[name];
    }
  }
});
