import { developerModeControl, developerModeNotice } from './developer-mode.js';
import { createCourseSelect } from './course-catalog.js';

const themeKey = 'course-academy.theme';
export function isLightTheme() { return document.documentElement.dataset.theme === 'light'; }

// Canvas colors must be resolved values; CSS and SVG use the shared theme variables.
export function themeColor(darkColor) {
  if (!isLightTheme()) return darkColor;
  const hex = /^#([\da-f]{3,4}|[\da-f]{6}|[\da-f]{8})$/i.exec(darkColor);
  if (hex) {
    const value = hex[1].length <= 4 ? [...hex[1]].map(c => c + c).join('') : hex[1];
    return '#' + [0, 2, 4].map(i => (255 - parseInt(value.slice(i, i + 2), 16)).toString(16).padStart(2, '0')).join('') + value.slice(6);
  }
  return darkColor.replace(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(,\s*[\d.]+)?\)$/, (_match, r, g, b, alpha) =>
    `${alpha ? 'rgba' : 'rgb'}(${255 - Number(r)},${255 - Number(g)},${255 - Number(b)}${alpha || ''})`);
}

export function setColorTheme(value, persist = true) {
  const theme = value === 'light' ? 'light' : 'dark';
  const changed = document.documentElement.dataset.theme !== theme;
  document.documentElement.dataset.theme = theme;
  if (persist) {
    try { localStorage.setItem(themeKey, theme); } catch { /* The switch still works without storage. */ }
  }
  if (changed) window.dispatchEvent(new CustomEvent('course-academy:theme-changed', { detail: { theme } }));
}
window.addEventListener('storage', event => {
  if (event.key === themeKey || event.key === null) setColorTheme(event.newValue, false);
});

const trigger = document.getElementById('learnerName');
const changeKey = 'course-academy-profile-changed';

function node(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

if (trigger) {
  const dialog = node('dialog'); dialog.id = 'userProfile';
  dialog.setAttribute('aria-labelledby', 'profileTitle');
  const head = node('div', 'profile-head');
  const heading = node('h2', '', 'Your profile'); heading.id = 'profileTitle';
  const close = node('button', 'profile-close', '×'); close.type = 'button';
  close.setAttribute('aria-label', 'Close profile');
  head.append(heading, close);
  const name = node('p', 'profile-name');
  const fields = node('fieldset'); fields.disabled = true;
  const courseLabel = node('label', 'profile-label', 'Selected course'); courseLabel.htmlFor = 'profileCourse';
  const courseSelect = createCourseSelect({ loadGroups: async () => {
    const response = await fetch('/api/course', { cache: 'no-store', credentials: 'same-origin' });
    const data = await response.json();
    if (!response.ok || !Array.isArray(data.courseGroups)) throw new Error('Unable to load courses. Close and reopen the list to retry.');
    return data.courseGroups;
  } });
  const courses = courseSelect.control;
  const help = node('p', 'profile-help', 'Choose the course shown in Study.');
  help.id = 'profileCourseHelp'; courses.setAttribute('aria-describedby', help.id);
  fields.append(courseLabel, courseSelect.element, help);

  function modeRow(label, description, control) {
    const row = node('div', 'profile-mode');
    const copy = node('div');
    const title = node('label', 'profile-label', label); title.htmlFor = control.id;
    const detail = node('p', 'profile-help', description); detail.id = `${control.id}Help`;
    control.setAttribute('aria-describedby', detail.id);
    copy.append(title, detail); row.append(copy, control);
    return row;
  }
  const directed = node('button', 'profile-switch'); directed.type = 'button'; directed.id = 'selfDirectedToggle';
  directed.setAttribute('role', 'switch'); directed.setAttribute('aria-label', 'Self-directed mode');
  directed.setAttribute('aria-checked', 'false');
  fields.append(
    modeRow('Developer mode', 'Inspect lessons without recording answers, time, or progress.', developerModeControl),
    modeRow('Self-directed mode', 'Choose target topics to guide your study queue.', directed),
  );
  const themeSwitch = node('button', 'profile-switch'); themeSwitch.type = 'button'; themeSwitch.id = 'lightModeToggle';
  themeSwitch.setAttribute('role', 'switch'); themeSwitch.setAttribute('aria-label', 'Light mode');
  const renderTheme = () => themeSwitch.setAttribute('aria-checked', String(isLightTheme()));
  renderTheme();
  themeSwitch.addEventListener('click', () => {
    themeSwitch.dataset.animate = 'true';
    setColorTheme(isLightTheme() ? 'dark' : 'light');
  });
  window.addEventListener('course-academy:theme-changed', renderTheme);
  const appearance = modeRow('Light mode', 'Light backgrounds with darker mastery bands.', themeSwitch);
  const error = node('p', 'profile-error'); error.setAttribute('role', 'alert'); error.hidden = true;
  const retry = node('button', 'profile-retry', 'Retry'); retry.type = 'button'; retry.hidden = true;
  dialog.append(head, name, fields, appearance, error, retry); document.body.append(dialog);

  let profile = null;
  let operation = null;
  let busy = false;
  let frozen = false;
  let refreshNeeded = false;
  function freeze() {
    frozen = true;
    window.dispatchEvent(new Event('course-academy:profile-changing'));
  }
  async function request(body) {
    const response = await fetch(body ? '/api/profile-settings' : '/api/profile', {
      method: body ? 'POST' : 'GET', cache: 'no-store', credentials: 'same-origin',
      headers: body ? { 'Content-Type': 'application/json' } : {},
      body: body ? JSON.stringify(body) : undefined,
    });
    const result = await response.json();
    if (!response.ok) {
      const failure = new Error(result.error || 'Unable to load your profile.'); failure.code = result.code; throw failure;
    }
    return result;
  }
  function render() {
    name.textContent = profile.learner.name || 'Learner';
    trigger.textContent = profile.learner.name || 'Profile';
    courseSelect.update(profile.course, profile.courses);
    const checked = String(profile.learner.selfDirected);
    if (directed.getAttribute('aria-checked') !== checked) directed.setAttribute('aria-checked', checked);
  }
  function applyProfile(result, notify = false) {
    const changedCourse = profile?.course.id !== result.course.id;
    profile = result; frozen = false; render();
    if (notify) window.dispatchEvent(new CustomEvent('course-academy:profile-changed', {
      detail: { ...result, changedCourse },
    }));
  }
  function fail(failure) {
    if (failure.code === 'basis-conflict' && operation) operation.requestId = crypto.randomUUID();
    error.textContent = failure.message + (operation ? ' Retry to finish saving, or reload before studying.' : '');
    error.hidden = false; retry.hidden = false;
  }
  async function load(notify = frozen) {
    if (busy || operation) { refreshNeeded ||= notify; return; }
    busy = true; fields.disabled = true; fields.setAttribute('aria-busy', 'true'); error.hidden = true; retry.hidden = true;
    try {
      applyProfile(await request(), notify); fields.disabled = false;
    } catch (failure) { fail(failure); }
    finally {
      busy = false; fields.setAttribute('aria-busy', 'false');
      if (refreshNeeded) { refreshNeeded = false; void load(true); }
    }
  }
  async function save() {
    if (busy || !operation) return;
    busy = true; fields.disabled = true; fields.setAttribute('aria-busy', 'true'); retry.hidden = true; error.hidden = true;
    if (directed.getAttribute('aria-checked') !== String(operation.selfDirected)) {
      directed.dataset.animate = 'true';
      directed.setAttribute('aria-checked', String(operation.selfDirected));
    }
    freeze();
    try {
      const result = await request(operation);
      try {
        sessionStorage.removeItem('course-academy.study-header');
        localStorage.setItem(changeKey, crypto.randomUUID());
      } catch { /* Settings are persisted on the server. */ }
      operation = null; applyProfile(result, true); fields.disabled = false;
    } catch (failure) { render(); fail(failure); }
    finally {
      busy = false; fields.setAttribute('aria-busy', 'false');
      if (refreshNeeded) { refreshNeeded = false; void load(true); }
    }
  }
  function change(selfDirected) {
    if (!profile || busy || frozen || operation) return;
    operation = { courseId: courses.value, selfDirected, requestId: crypto.randomUUID() };
    void save();
  }
  courses.addEventListener('change', () => change(profile.learner.selfDirected));
  directed.addEventListener('click', () => change(!profile.learner.selfDirected));
  retry.addEventListener('click', () => { if (operation) void save(); else void load(); });
  trigger.addEventListener('click', () => {
    dialog.append(developerModeNotice);
    dialog.showModal(); trigger.setAttribute('aria-expanded', 'true');
    if (!operation) void load();
  });
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
  });
  dialog.addEventListener('close', () => {
    courseSelect.close();
    document.body.append(developerModeNotice);
    trigger.setAttribute('aria-expanded', 'false'); trigger.focus();
  });
  window.addEventListener('course-academy:developer-mode-changing', () => {
    fields.disabled = true;
  });
  // A failed developer-mode request remains retryable inside the profile.
  window.addEventListener('course-academy:developer-mode-changed', () => { if (!busy && profile && !frozen) fields.disabled = false; });
  window.addEventListener('storage', event => {
    if (event.key !== changeKey) return;
    freeze();
    try { sessionStorage.removeItem('course-academy.study-header'); } catch { /* Optional cache. */ }
    void load(true);
  });
}
