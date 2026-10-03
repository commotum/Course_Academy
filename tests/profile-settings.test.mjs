import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

// Exercise the actual controllers with a local server stand-in. No learner
// preferences or study attempts are changed by these tests.
async function fixture(theme = 'dark') {
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.children = []; this.attrs = {}; this.dataset = {}; }
    append(...children) {
      for (const child of children) {
        if (child.parent) child.parent.children = child.parent.children.filter(node => node !== child);
        child.parent = this; this.children.push(child);
      }
    }
    replaceChildren(...children) { this.children = []; this.append(...children); }
    setAttribute(key, value) { this.attrs[key] = String(value); }
    getAttribute(key) { return this.attrs[key] ?? null; }
    hasAttribute(key) { return key in this.attrs; }
    removeAttribute(key) { delete this.attrs[key]; }
    contains(element) { for (let current = element; current; current = current.parent) if (current === this) return true; return false; }
    click() {
      for (let node = this; node; node = node.parent) if (node.disabled) return;
      this.dispatchEvent(new Event('click'));
    }
    focus() { document.activeElement = this; }
    showModal() { this.open = true; }
    close() { this.open = false; this.dispatchEvent(new Event('close')); }
  }
  const document = new Element('document'); document.body = new Element('body');
  document.documentElement = new Element('html'); document.documentElement.dataset.theme = theme;
  document.createElement = tag => new Element(tag);
  const find = (predicate, node = document.body) => predicate(node) ? node : node.children.map(child => find(predicate, child)).find(Boolean);
  document.getElementById = id => find(node => node.id === id);
  const trigger = new Element('button'); trigger.id = 'learnerName'; document.body.append(trigger);
  const window = new EventTarget();
  const profile = { learner: { name: 'Test learner', selfDirected: true }, course: { id: 'one' }, courses: [{ id: 'one', title: 'One' }, { id: 'two', title: 'Two' }] };
  const state = { enabled: false, fail: null, calls: [], events: [], stored: new Map() };
  for (const name of ['developer-mode-changing', 'developer-mode-settled', 'profile-changing', 'profile-changed']) {
    window.addEventListener(`course-academy:${name}`, event => state.events.push({ name, detail: event.detail }));
  }
  const storage = {
    setItem(key, value) { if (state.storageBlocked) throw new Error('Storage blocked'); state.stored.set(key, value); },
    removeItem(key) { state.stored.delete(key); },
  };
  const context = vm.createContext({ document, window, Event, CustomEvent, crypto, JSON, sessionStorage: storage, localStorage: storage,
    location: { reload() { assert.fail('Settings must not reload the document'); }, replace() { assert.fail('Settings must not navigate the document'); } },
    fetch: async (path, options) => {
      const body = options.body ? JSON.parse(options.body) : null;
      state.calls.push({ path, body });
      if (body) {
        if (state.hold?.path === path) await state.hold.promise;
        if (path === '/api/developer-mode') state.enabled = body.enabled;
        else { profile.learner.selfDirected = body.selfDirected; profile.course.id = body.courseId; }
        if (state.fail === path) { state.fail = null; throw new Error('Reply lost after commit'); }
      }
      return { ok: true, json: async () => structuredClone(path === '/api/developer-mode' ? { enabled: state.enabled } : path === '/api/course' ? {
        courseGroups: [{ id: 'group', title: 'Example group', courses: [profile.courses[1], profile.courses[0]] }],
      } : profile) };
    },
  });
  const dev = (await readFile(new URL('../ui/developer-mode.js', import.meta.url), 'utf8')).replaceAll('export ', '');
  const controls = vm.runInContext(`(() => { ${dev}; return { developerModeControl, developerModeNotice, developerModeReady, isDeveloperMode }; })()`, context);
  context.controls = controls;
  await controls.developerModeReady;
  const catalog = (await readFile(new URL('../ui/course-catalog.js', import.meta.url), 'utf8')).replaceAll('export ', '');
  context.createCourseSelect = vm.runInContext(`(() => { ${catalog}; return createCourseSelect; })()`, context);
  const source = (await readFile(new URL('../ui/profile.js', import.meta.url), 'utf8')).replace(/^import .*;\n/gm, '').replaceAll('export ', '');
  const themeControls = vm.runInContext(`(() => { const { developerModeControl, developerModeNotice } = controls; ${source}; return { themeColor, setColorTheme, isLightTheme }; })()`, context);
  const settle = () => new Promise(resolve => setImmediate(resolve));
  const hold = path => {
    let release;
    state.hold = { path, promise: new Promise(resolve => { release = resolve; }) };
    return () => { state.hold = null; release(); };
  };
  trigger.click(); await settle();
  return { document, window, state, profile, controls, themeControls, find, settle, hold, get: document.getElementById };
}

test('switches save in place, preserve the other switch, and keep the same dialog and controls', async () => {
  const f = await fixture();
  const dialog = f.get('userProfile'), dev = f.get('developerModeToggle'), directed = f.get('selfDirectedToggle');
  directed.click(); await f.settle();
  assert.equal(directed.getAttribute('aria-checked'), 'false');
  assert.equal(dev.getAttribute('aria-checked'), 'false');
  assert.equal(dialog.open, true);
  dev.click(); await f.settle();
  assert.equal(dev.getAttribute('aria-checked'), 'true');
  assert.equal(directed.getAttribute('aria-checked'), 'false');
  assert.equal(f.controls.isDeveloperMode(), true);
  dev.click(); await f.settle();
  assert.equal(f.controls.isDeveloperMode(), false);
  assert.equal(f.get('userProfile'), dialog);
  assert.equal(f.get('selfDirectedToggle'), directed);
  assert.equal(f.state.events.filter(e => e.name === 'developer-mode-settled').length, 2);
  f.get('profileCourse').value = 'two'; f.get('profileCourse').dispatchEvent(new Event('change')); await f.settle();
  assert.equal(f.state.events.at(-1).detail.changedCourse, true);
});

test('light mode switches immediately, preserves the open profile and settings, and makes no API request', async () => {
  const f = await fixture();
  const toggle = f.get('lightModeToggle'), dialog = f.get('userProfile');
  const calls = f.state.calls.length;
  toggle.click();
  assert.equal(f.document.documentElement.dataset.theme, 'light');
  assert.equal(toggle.getAttribute('aria-checked'), 'true');
  assert.equal(f.state.stored.get('course-academy.theme'), 'light');
  assert.equal(f.get('selfDirectedToggle').getAttribute('aria-checked'), 'true');
  assert.equal(f.get('developerModeToggle').getAttribute('aria-checked'), 'false');
  assert.equal(f.get('userProfile'), dialog);
  assert.equal(dialog.open, true);
  assert.equal(f.state.calls.length, calls);
  toggle.click();
  assert.equal(f.document.documentElement.dataset.theme, 'dark');
  assert.equal(f.state.stored.get('course-academy.theme'), 'dark');
  assert.equal(f.state.calls.length, calls);
});

test('theme follows other tabs and remains usable during settings saves or blocked storage', async () => {
  const f = await fixture('light');
  const toggle = f.get('lightModeToggle');
  assert.equal(toggle.getAttribute('aria-checked'), 'true');
  const release = f.hold('/api/profile-settings');
  f.get('selfDirectedToggle').click();
  f.state.storageBlocked = true;
  toggle.click();
  assert.equal(f.document.documentElement.dataset.theme, 'dark');
  assert.equal(toggle.getAttribute('aria-checked'), 'false');
  const remote = new Event('storage');
  Object.assign(remote, { key: 'course-academy.theme', newValue: 'light' });
  f.window.dispatchEvent(remote);
  assert.equal(f.document.documentElement.dataset.theme, 'light');
  assert.equal(toggle.getAttribute('aria-checked'), 'true');
  release(); await f.settle();
  assert.equal(toggle.getAttribute('aria-checked'), 'true');
  assert.equal(f.get('selfDirectedToggle').getAttribute('aria-checked'), 'false');
});

test('lost responses freeze recording and retry the same operation without resetting switch state', async () => {
  const f = await fixture();
  const dev = f.get('developerModeToggle'), directed = f.get('selfDirectedToggle');
  f.state.fail = '/api/developer-mode'; dev.click(); await f.settle();
  assert.equal(f.controls.isDeveloperMode(), true);
  assert.equal(dev.getAttribute('aria-checked'), 'false'); // Last confirmed state, not a fake reset.
  assert.equal(directed.getAttribute('aria-checked'), 'true');
  dev.click(); await f.settle();
  const devWrites = f.state.calls.filter(call => call.path === '/api/developer-mode' && call.body);
  assert.deepEqual(devWrites[0].body, devWrites[1].body);
  assert.equal(dev.getAttribute('aria-checked'), 'true');
  f.state.fail = '/api/profile-settings'; directed.click(); await f.settle();
  assert.equal(directed.getAttribute('aria-checked'), 'true');
  f.find(node => node.className === 'profile-retry').click(); await f.settle();
  const writes = f.state.calls.filter(call => call.path === '/api/profile-settings');
  assert.deepEqual(writes[0].body, writes[1].body);
  assert.equal(directed.getAttribute('aria-checked'), 'false');
  assert.equal(dev.getAttribute('aria-checked'), 'true');
});

test('changes from another tab refresh controls and notify the page without navigating', async () => {
  const f = await fixture();
  const dialog = f.get('userProfile');
  const storageEvent = key => {
    const event = new Event('storage'); Object.defineProperty(event, 'key', { value: key });
    f.window.dispatchEvent(event);
  };
  f.state.enabled = true;
  storageEvent('course-academy-developer-mode-changed'); await f.settle();
  assert.equal(f.get('developerModeToggle').getAttribute('aria-checked'), 'true');
  assert.equal(f.get('selfDirectedToggle').getAttribute('aria-checked'), 'true');
  f.profile.learner.selfDirected = false;
  storageEvent('course-academy-profile-changed'); await f.settle();
  assert.equal(f.get('selfDirectedToggle').getAttribute('aria-checked'), 'false');
  assert.equal(f.get('developerModeToggle').getAttribute('aria-checked'), 'true');
  assert.equal(f.get('userProfile'), dialog);
  assert.equal(dialog.open, true);
  assert.equal(f.state.events.at(-1).name, 'profile-changed');
});

test('switches move before slow saves finish, without confirmation UI or premature recording', async () => {
  const f = await fixture();
  const dev = f.get('developerModeToggle'), directed = f.get('selfDirectedToggle'), courses = f.get('profileCourse');
  assert.equal(f.find(node => node.className === 'profile-status'), undefined);
  let release = f.hold('/api/profile-settings');
  directed.click();
  assert.equal(directed.getAttribute('aria-checked'), 'false');
  assert.equal(directed.dataset.animate, 'true');
  assert.equal(f.profile.learner.selfDirected, true); // The server has not responded yet.
  assert.equal(dev.getAttribute('aria-checked'), 'false');
  assert.equal(f.get('profileCourse'), courses);
  release(); await f.settle();
  assert.equal(directed.getAttribute('aria-checked'), 'false');

  release = f.hold('/api/developer-mode');
  dev.click();
  assert.equal(dev.getAttribute('aria-checked'), 'true');
  assert.equal(dev.dataset.animate, 'true');
  assert.equal(f.state.enabled, false);
  assert.equal(directed.getAttribute('aria-checked'), 'false');
  release(); await f.settle();

  release = f.hold('/api/developer-mode');
  dev.click();
  assert.equal(dev.getAttribute('aria-checked'), 'false');
  assert.equal(f.state.enabled, true);
  assert.equal(f.controls.isDeveloperMode(), true); // Recording stays blocked until confirmed.
  release(); await f.settle();
  assert.equal(f.controls.isDeveloperMode(), false);
});

test('grouped course picker preserves server order and only saves an explicit changed selection', async () => {
  const f = await fixture();
  const control = f.get('profileCourse'), list = f.get('profileCourseOptions');
  const key = value => {
    const event = new Event('keydown', { cancelable: true });
    Object.defineProperty(event, 'key', { value }); list.dispatchEvent(event);
  };
  control.click(); await f.settle();
  assert.equal(control.getAttribute('aria-expanded'), 'true');
  const group = list.children[0], choices = group.children.slice(1);
  assert.equal(group.children[0].textContent, 'Example group');
  assert.deepEqual(choices.map(choice => choice.textContent), ['Two', 'One']);
  assert.equal(f.document.activeElement, choices[1]);
  key('Home'); assert.equal(f.document.activeElement, choices[0]);
  key('Escape'); assert.equal(list.hidden, true);
  assert.equal(f.document.activeElement, control);
  assert.equal(f.state.calls.filter(call => call.path === '/api/profile-settings').length, 0);

  control.click(); await f.settle();
  list.children[0].children[2].click(); // Already-selected course.
  assert.equal(f.state.calls.filter(call => call.path === '/api/profile-settings').length, 0);
  control.click(); await f.settle();
  list.children[0].children[1].click(); await f.settle();
  assert.equal(list.hidden, true);
  assert.equal(control.textContent, 'Two');
  assert.equal(f.profile.course.id, 'two');
  assert.equal(f.profile.learner.selfDirected, true);
  assert.equal(f.state.calls.filter(call => call.path === '/api/course').length, 1);
  assert.equal(f.state.events.at(-1).detail.changedCourse, true);
});
