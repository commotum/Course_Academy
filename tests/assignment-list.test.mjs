import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = await readFile(new URL('../ui/assignments.js', import.meta.url), 'utf8');
const helpers = source.slice(source.indexOf('function el('), source.indexOf('function escapeHTML('));
const list = source.slice(source.indexOf('function assignmentSortPreference('), source.indexOf('function renderAssignment('));
const visibility = source.slice(source.indexOf('async function syncAfterVisibility()'), source.indexOf('async function leaveAssignment('));

// Exercise the real list renderer without opening the app or writing learner data.
function fixture(storage = new Map()) {
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.children = []; this.attrs = {}; this.className = ''; }
    append(...nodes) { for (const node of nodes) { node.parent = this; this.children.push(node); } }
    replaceChildren(...nodes) { this.children = []; this.text = ''; this.append(...nodes); }
    get textContent() { return (this.text || '') + this.children.map(node => node.textContent).join(''); }
    set textContent(value) { this.replaceChildren(); this.text = String(value); }
    setAttribute(key, value) { this.attrs[key] = String(value); }
    getAttribute(key) { return this.attrs[key] ?? null; }
    querySelectorAll(selector) {
      const matches = node => selector.startsWith('.') ? node.className.split(' ').includes(selector.slice(1)) : node.tagName === selector;
      return this.children.flatMap(child => [...(matches(child) ? [child] : []), ...child.querySelectorAll(selector)]);
    }
    querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
    focus() { document.activeElement = this; }
  }
  const main = new Element('main'), announcement = new Element('div');
  const document = { createElement: tag => new Element(tag), getElementById: id => ({ main, announcement })[id] };
  const f = { main, document, loads: 0, storage, location: { href: 'http://127.0.0.1:8765/assignments' } };
  const context = vm.createContext({ document, Event, URL, location: f.location, isDeveloperMode: () => false,
    localStorage: { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value) },
    load(options) { f.loads++; f.loadOptions = options; },
  });
  f.h = vm.runInContext(`(() => {
    const $ = id => document.getElementById(id);
    const modeChanging = false, assignmentData = null;
    ${helpers}
    ${list}
    ${visibility}
    return { renderList, assignmentGroups, syncAfterVisibility };
  })()`, context);
  f.render = assignments => { main.replaceChildren(); f.h.renderList({ assignments }); };
  return f;
}

const math = { id: 'math', title: 'Calculus' }, chemistry = { id: 'chemistry', title: 'Chemistry' };
const assignment = (id, course, due, status = null) => ({ id, title: id, course, due, status, problemCount: 2 });
const rows = node => node.querySelectorAll('.queue-card').map(row => row.querySelector('h2').textContent);

test('default list groups by activity course, then deadline, with unassigned and undated entries last', () => {
  const f = fixture();
  const entries = [
    assignment('Math later', math, '2026-10-06T00:00:00Z'),
    assignment('No course', null, '2026-10-01T00:00:00Z'),
    assignment('Math undated', math, null),
    assignment('Chemistry earlier', chemistry, '2026-10-02T00:00:00Z'),
    assignment('Math earlier', math, '2026-10-03T00:00:00Z'),
  ];
  const original = structuredClone(entries);
  f.render(entries);
  assert.equal(f.main.querySelector('select').value, 'course');
  assert.equal(f.main.querySelectorAll('button').some(node => /Refresh/.test(node.textContent)), false);
  assert.deepEqual(f.main.querySelectorAll('.assignment-course-heading').map(node => node.textContent), ['Calculus', 'Chemistry', 'No course']);
  assert.deepEqual(rows(f.main), ['Math earlier', 'Math later', 'Math undated', 'Chemistry earlier', 'No course']);
  assert.deepEqual(entries, original);
  assert.equal(f.main.querySelector('.queue-card').querySelector('a').href, '/assignments?assignment=Math%20earlier');
});

test('date selection changes only the list, keeps course context and completion separation, and persists', () => {
  const f = fixture();
  const entries = [assignment('Math', math, '2026-10-04T00:00:00Z'), assignment('Chemistry', chemistry, '2026-10-02T00:00:00Z'), assignment('Finished', chemistry, '2026-10-01T00:00:00Z', 'learner-task.status/completed')];
  f.render(entries);
  const select = f.main.querySelector('select'); select.focus();
  select.value = 'date'; select.dispatchEvent(new Event('change'));
  assert.equal(f.main.querySelector('select'), select);
  assert.equal(f.document.activeElement, select);
  assert.equal(f.main.querySelectorAll('.assignment-course-heading').length, 0);
  assert.deepEqual(rows(f.main), ['Chemistry', 'Math', 'Finished']);
  assert.deepEqual(rows(f.main.querySelector('.assignment-completed')), ['Finished']);
  assert.deepEqual(f.main.querySelectorAll('.assignment-course-name').map(node => node.textContent), ['Chemistry', 'Calculus', 'Chemistry']);
  assert.equal(f.loads, 0);
  const reload = fixture(f.storage); reload.render(entries);
  assert.equal(reload.main.querySelector('select').value, 'date');
  assert.deepEqual(rows(reload.main), ['Chemistry', 'Math', 'Finished']);
});

test('returning to the assignment list reloads in the background without interrupting a detail view', async () => {
  const f = fixture(); f.render([assignment('Math', math, null)]);
  const original = f.main.querySelector('.queue-card');
  f.document.hidden = true; await f.h.syncAfterVisibility();
  assert.equal(f.loads, 0);
  f.document.hidden = false; await f.h.syncAfterVisibility();
  assert.equal(f.loads, 1);
  assert.equal(f.loadOptions.preserve, true);
  assert.equal(f.main.querySelector('.queue-card'), original);
  f.location.href += '?assignment=math'; await f.h.syncAfterVisibility();
  assert.equal(f.loads, 1);
});

test('same-titled courses stay separate and empty or storage-blocked lists remain usable', () => {
  const f = fixture({ get() { throw new Error('Blocked'); }, set() { throw new Error('Blocked'); } });
  f.render([assignment('Z', { id: 'two', title: 'Math' }, null), assignment('B', { id: 'one', title: 'Math' }, 'invalid'), assignment('A', { id: 'one', title: 'Math' }, null)]);
  assert.equal(f.main.querySelectorAll('.assignment-course-heading').length, 2);
  assert.deepEqual(rows(f.main), ['A', 'B', 'Z']);
  const select = f.main.querySelector('select'); select.value = 'date'; select.dispatchEvent(new Event('change'));
  assert.deepEqual(rows(f.main), ['A', 'B', 'Z']);
  f.render([]);
  assert.match(f.main.textContent, /No assignments yet/);
  f.render([assignment('Done', math, null, 'completed')]);
  assert.match(f.main.textContent, /All assignments completed/);
  assert.deepEqual(rows(f.main.querySelector('.assignment-completed')), ['Done']);
});
