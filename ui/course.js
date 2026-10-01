import { marked } from './vendor/marked/marked.esm.js';
import { createCoursePicker } from './navigation.js';

const $ = id => document.getElementById(id);
const palette = ['#000000', '#303030', '#5A5A5A', '#858585', '#AEAEAE', '#D6D6D6', '#FFFFFF'];
let currentCourseId = null;
let curriculumSnapshot = null;
let requestController = null;
let generation = 0;
let loadedRoute = null;
let mathLoader = null;
let typesetting = Promise.resolve();
let lastLoadedAt = 0;
let refreshNeeded = false;

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function button(text, className, action) {
  const node = el('button', className, text);
  node.type = 'button'; node.addEventListener('click', action);
  return node;
}
function link(text, href, className = '') {
  const node = el('a', className, text); node.href = href; return node;
}
function levelName(value) {
  const key = String(value || '').split('/').at(-1);
  return { 'early-math': 'Early Math', 'high-school-math': 'High School Math', 'university-math': 'University Math' }[key] || key.replaceAll('-', ' ').replace(/\b\w/g, c => c.toUpperCase());
}
function topicKey(topic) { return String(topic.uuid || topic.id); }
function uniqueTopics(topics) { return [...new Map(topics.map(topic => [topicKey(topic), topic])).values()]; }
function unitTopics(unit) { return uniqueTopics((unit.modules || []).flatMap(module => module.topics || [])); }
function repetition(topic) { return Number.isFinite(topic.repetitions) && topic.repetitions >= 0 ? topic.repetitions : null; }
function band(topic) { const n = repetition(topic); return n === null ? null : Math.min(6, Math.floor(n)); }
function formatNumber(n) { return n.toLocaleString(undefined, { maximumFractionDigits: 3 }); }
function bandLabel(n) { return n === null ? 'No data' : n === 6 ? '6+' : String(n); }
function statistics(topics) {
  const unique = uniqueTopics(topics);
  const bands = Array(7).fill(0);
  let unknown = 0;
  for (const topic of unique) { const value = band(topic); if (value === null) unknown++; else bands[value]++; }
  const completed = bands[6];
  return { total: unique.length, completed, tracked: unique.length - unknown, unknown, bands };
}
function completionLabel(stats) {
  // Round down to one decimal so only an entirely completed group shows 100%.
  const percent = stats.total ? Math.floor(stats.completed * 1000 / stats.total) / 10 : 0;
  return `${formatNumber(percent)}% complete`;
}
function completionSummary(stats) {
  return `${completionLabel(stats)} · ${formatNumber(stats.completed)} / ${formatNumber(stats.total)} topics`;
}
function swatch(value) {
  const node = el('span', 'band-swatch' + (value === null ? ' unknown' : ''));
  if (value !== null) node.style.backgroundColor = palette[value];
  node.setAttribute('aria-hidden', 'true');
  return node;
}
function bandEntries(stats) {
  return [...stats.bands.map((count, value) => ({ count, value })).reverse(), { count: stats.unknown, value: null }];
}
function distribution(stats) {
  const bar = el('span', 'distribution');
  const entries = bandEntries(stats);
  bar.setAttribute('role', 'img');
  bar.setAttribute('aria-label', stats.total ? 'Repetition bands: ' + entries.map(({ count, value }) => `${bandLabel(value)}: ${count} topics`).join('; ') : 'No topics');
  for (const { count, value } of entries) {
    if (!count) continue;
    const segment = el('span', 'distribution-segment' + (value === null ? ' unknown' : ''));
    segment.style.flexGrow = String(count);
    segment.style.flexBasis = '0';
    if (value !== null) segment.style.backgroundColor = palette[value];
    segment.title = `${bandLabel(value)}${value === null ? '' : ' repetitions'} · ${count} ${count === 1 ? 'topic' : 'topics'}`;
    bar.append(segment);
  }
  return bar;
}
function breakdown(stats, compact = false) {
  const host = el('div', compact ? 'unit-breakdown' : 'distribution-legend');
  for (const { count, value } of bandEntries(stats)) {
    if (compact) {
      const item = el('span'); item.append(swatch(value), document.createTextNode(`${bandLabel(value)}: ${count}`));
      item.title = `${count} topics · ${value === null ? 'no repetition data' : 'repetition band ' + bandLabel(value)}`;
      host.append(item);
    } else {
      const item = el('div', 'legend-item');
      const label = el('span', 'legend-band'); label.append(swatch(value), document.createTextNode(bandLabel(value)));
      item.append(label, el('span', 'legend-count', formatNumber(count)));
      host.append(item);
    }
  }
  return host;
}
function escapeHTML(text) { return String(text).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]); }
function markdown(value, className = 'prose') {
  const node = el('div', className);
  const math = [];
  const prefix = 'CAMATH' + crypto.randomUUID().replaceAll('-', '') + 'TOKEN';
  const source = String(value || '').replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g, match => {
    math.push(match); return prefix + (math.length - 1) + 'END';
  });
  let html = marked.parse(source, { async: false, gfm: true });
  html = html.replace(new RegExp(prefix + '(\\d+)END', 'g'), (_, i) => escapeHTML(math[Number(i)]));
  const fragment = DOMPurify.sanitize(html, {
    RETURN_DOM_FRAGMENT: true,
    USE_PROFILES: { html: true },
    FORBID_TAGS: ['style', 'form', 'input', 'button', 'textarea', 'select', 'iframe', 'object', 'embed', 'img', 'video', 'audio'],
    FORBID_ATTR: ['style', 'srcset', 'id', 'name'],
  });
  for (const anchor of fragment.querySelectorAll('a')) {
    const href = anchor.getAttribute('href') || '';
    if (!/^https?:\/\//i.test(href)) anchor.removeAttribute('href');
    else { anchor.target = '_blank'; anchor.rel = 'noopener noreferrer'; }
  }
  node.append(fragment);
  if (math.length) node.dataset.math = 'true';
  return node;
}
function loadMath() {
  if (window.MathJax?.startup?.promise) return MathJax.startup.promise;
  if (!mathLoader) mathLoader = new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = '/ui/vendor/mathjax/tex-svg.js'; script.async = true;
    script.onload = () => window.MathJax?.startup?.promise ? MathJax.startup.promise.then(resolve, reject) : reject(new Error('Math rendering could not start.'));
    script.onerror = () => { script.remove(); reject(new Error('Math rendering could not load.')); };
    document.head.append(script);
  }).catch(error => { mathLoader = null; throw error; });
  return mathLoader;
}
function typeset(host) {
  if (!host.querySelector('[data-math]') && !host.matches('[data-math]')) return;
  typesetting = typesetting.catch(() => {}).then(async () => {
    if (!host.isConnected) return;
    await loadMath();
    if (host.isConnected) await MathJax.typesetPromise([host]);
  }).catch(() => {
    if (host.isConnected && !host.querySelector('.math-note')) host.append(el('p', 'math-note', 'Math notation could not be rendered. Refresh the page to try again.'));
  });
}
async function api(path, signal) {
  const response = await fetch(path, { cache: 'no-store', signal });
  let result;
  try { result = await response.json(); } catch { throw new Error('The course server did not return a response. Check that it is running, then try again.'); }
  if (!response.ok || result.error) {
    const error = new Error(result.error || `The request failed (${response.status}).`);
    error.status = response.status; throw error;
  }
  return result;
}
function courseURL(id) { return '/course' + (id ? '?course=' + encodeURIComponent(id) : ''); }
function topicURL(topic, courseId) {
  return '/topic?topic=' + encodeURIComponent(topic.uuid || topic.mathAcademyId) + (courseId ? '&course=' + encodeURIComponent(courseId) : '');
}
function graphURL(courseId, topicId) {
  return '/?course=' + encodeURIComponent(courseId || 'all') + (topicId === undefined ? '' : '&topic=' + encodeURIComponent(topicId));
}
function courseLink(course, className = '') {
  const node = link(course.title, courseURL(course.id), className);
  if (course.id === currentCourseId) node.setAttribute('aria-current', 'page');
  node.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); void navigate(course.id);
  });
  return node;
}
async function navigate(id) {
  const url = courseURL(id);
  if (location.pathname + location.search !== url) history.pushState(null, '', url);
  await loadCourse(true);
}
function sidebar(data, unitIds) {
  const aside = el('aside', 'course-sidebar'); aside.setAttribute('aria-label', 'Course navigation');
  const content = el('div', 'sidebar-content');
  const matchingSequences = (data.sequences || []).filter(sequence => sequence.courses.some(course => course.id === data.course.id));
  if (matchingSequences.length) {
    const sequences = el('nav'); sequences.setAttribute('aria-label', 'Course sequences');
    sequences.append(el('h2', 'sidebar-label', 'Course sequences'));
    for (const sequence of matchingSequences) {
      const group = el('div', 'sequence');
      const list = el('ul', 'sequence-links');
      list.setAttribute('aria-label', sequence.title);
      for (const course of sequence.courses) { const item = el('li'); item.append(courseLink(course)); list.append(item); }
      group.append(list); sequences.append(group);
    }
    content.append(sequences);
  }
  if (data.course.units.length) {
    const nav = el('nav', 'unit-nav'); nav.setAttribute('aria-label', 'Units in this course');
    nav.append(el('h2', 'sidebar-label', 'In this course'));
    const list = el('ol');
    data.course.units.forEach((unit, index) => {
      const item = el('li');
      const anchor = link('', '#' + unitIds[index]);
      anchor.append(el('span', 'unit-number', String(index + 1).padStart(2, '0')), el('span', '', unit.title));
      anchor.addEventListener('click', () => {
        const filter = $('topicFilter');
        if (filter?.value) { filter.value = ''; filter.dispatchEvent(new Event('input')); }
        const target = $(unitIds[index]); if (target) target.open = true;
      });
      item.append(anchor); list.append(item);
    });
    nav.append(list); content.append(nav);
  }
  content.append(button('Browse all courses ↗', 'text-button sidebar-browse', () => picker.open()));
  content.append(link('Explore this course ↗', graphURL(data.course.id), 'sidebar-link'));
  aside.append(content); return aside;
}
function courseHeading(data, topicCount) {
  const course = data.course;
  const header = el('section', 'course-heading'); header.setAttribute('aria-labelledby', 'pageTitle');
  const eyebrow = el('div', 'eyebrow', levelName(course.level) || 'Course');
  if (course.id === data.learner?.courseId) eyebrow.append(el('span', 'study-course-tag', 'Your study course'));
  const heading = el('h1', '', course.title); heading.id = 'pageTitle';
  header.append(eyebrow, heading);
  if (course.description?.trim()) header.append(markdown(course.description, 'prose course-description'));
  const facts = el('div', 'course-facts');
  if (course.code) facts.append(el('span', '', course.code));
  facts.append(el('span', '', `${course.units.length} ${course.units.length === 1 ? 'unit' : 'units'}`), el('span', '', `${formatNumber(topicCount)} ${topicCount === 1 ? 'topic' : 'topics'}`), link('View in graph ↗', graphURL(course.id)));
  header.append(facts);
  return header;
}
function courseReading(course) {
  const outcomes = (course.outcomes || []).filter(outcome => outcome.text?.trim());
  if (!course.overview?.trim() && !outcomes.length) return null;
  const details = el('details', 'course-reading');
  details.append(el('summary', '', course.overview?.trim() && outcomes.length ? 'Overview & learning outcomes' : outcomes.length ? 'Learning outcomes' : 'Course overview'));
  const body = el('div', 'reading-body');
  if (course.overview?.trim()) body.append(el('h2', '', 'Course overview'), markdown(course.overview));
  if (outcomes.length) {
    body.append(el('h2', '', 'Learning outcomes'));
    const groups = new Map();
    for (const outcome of outcomes) {
      const category = outcome.category?.trim() || '';
      if (!groups.has(category)) groups.set(category, []);
      groups.get(category).push(outcome);
    }
    for (const [category, items] of groups) {
      const group = el('section', 'outcome-group');
      if (category) group.append(el('h3', '', category));
      const list = el('ul');
      for (const outcome of items) { const item = el('li'); item.append(markdown(outcome.text)); list.append(item); }
      group.append(list); body.append(group);
    }
  }
  details.append(body);
  details.addEventListener('toggle', () => { if (details.open) typeset(body); });
  return details;
}
function progressSection(stats) {
  const section = el('section', 'progress-section'); section.setAttribute('aria-labelledby', 'progressTitle');
  const heading = el('div', 'progress-heading');
  const title = el('h2', '', 'Your progress'); title.id = 'progressTitle';
  const completion = el('p', 'completion-summary');
  completion.append(el('strong', '', completionLabel(stats)), document.createTextNode(` · ${formatNumber(stats.completed)} / ${formatNumber(stats.total)} topics`));
  const actions = el('div', 'progress-actions');
  actions.append(completion, button('Refresh', 'text-button', () => loadCourse()));
  heading.append(title, actions);
  section.append(heading, distribution(stats), breakdown(stats), el('p', 'progress-note', 'A topic is complete at 6 or more repetitions. Completion is the share of topics completed. Shades show repetition bands; dashed markers mean no recorded value.'));
  return section;
}
function topicRow(topic, courseId) {
  const item = el('li'); item.dataset.topicKey = topicKey(topic);
  item.dataset.search = [topic.title, topic.mathAcademyId, topic.id, topic.uuid].filter(value => value != null).join(' ').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase();
  const anchor = link('', topicURL(topic, courseId), 'topic-link');
  const title = el('span', 'topic-title', topic.title);
  const arrow = el('span', 'topic-arrow', ' ↗'); arrow.setAttribute('aria-hidden', 'true'); title.append(arrow);
  anchor.append(title);
  const value = repetition(topic);
  const label = value === null ? 'No data' : `${formatNumber(value)} ${value === 1 ? 'rep' : 'reps'}`;
  anchor.setAttribute('aria-label', `${topic.title}. Read topic. ${value === null ? 'No repetition data' : formatNumber(value) + ' repetitions'}.`);
  anchor.title = 'Read tutorials and worked examples';
  const progress = el('span', 'topic-progress' + (value === null ? ' unknown' : ''));
  progress.append(swatch(band(topic)), document.createTextNode(label));
  progress.setAttribute('aria-label', value === null ? 'No repetition data' : `${formatNumber(value)} ${value === 1 ? 'repetition' : 'repetitions'}`);
  anchor.append(progress); item.append(anchor); return item;
}
function outline(course, unitIds, stats) {
  const section = el('section', 'course-outline'); section.setAttribute('aria-labelledby', 'outlineTitle');
  const heading = el('div', 'outline-heading');
  const title = el('h2', '', 'Course outline'); title.id = 'outlineTitle';
  const controls = el('div', 'outline-controls');
  const units = [];
  controls.append(button('Expand all', 'text-button', () => units.forEach(unit => { if (!unit.hidden) unit.open = true; })), button('Collapse all', 'text-button', () => units.forEach(unit => { unit.open = false; })));
  heading.append(title, controls); section.append(heading);
  const filterRow = el('div', 'filter-row');
  const input = el('input', 'topic-filter'); input.type = 'search'; input.id = 'topicFilter'; input.placeholder = 'Filter topics in this course…'; input.autocomplete = 'off';
  input.setAttribute('aria-label', 'Filter topics in this course'); input.setAttribute('aria-controls', 'courseUnits');
  const count = el('span', 'filter-count'); count.setAttribute('role', 'status');
  filterRow.append(input, count); section.append(filterRow);
  const unitHost = el('div'); unitHost.id = 'courseUnits';
  course.units.forEach((unit, index) => {
    const unitStats = statistics(unitTopics(unit));
    const details = el('details', 'unit'); details.id = unitIds[index]; details.open = index === 0;
    const summary = el('summary');
    const label = el('span');
    label.append(el('span', 'unit-title', unit.title), el('span', 'unit-stat', completionSummary(unitStats)), distribution(unitStats));
    const toggle = el('span', 'unit-toggle'); toggle.setAttribute('aria-hidden', 'true');
    summary.append(el('span', 'unit-number', String(index + 1).padStart(2, '0')), label, toggle);
    const content = el('div', 'unit-content'); content.append(breakdown(unitStats, true));
    for (const module of unit.modules || []) {
      const host = el('section', 'module');
      const moduleHeading = el('div', 'module-heading');
      const moduleStats = statistics(module.topics || []);
      moduleHeading.append(el('h3', '', module.title), el('span', 'module-progress', completionSummary(moduleStats)));
      host.append(moduleHeading);
      const list = el('ul', 'topic-list');
      for (const topic of module.topics || []) list.append(topicRow(topic, course.id));
      if (!list.children.length) host.append(el('p', 'empty-outline', 'No topics in this module.')); else host.append(list);
      content.append(host);
    }
    if (!unit.modules?.length) content.append(el('p', 'empty-outline', 'No modules in this unit.'));
    details.append(summary, content); unitHost.append(details); units.push(details);
  });
  const empty = el('p', 'empty-outline', course.units.length ? 'No topics match your filter.' : 'This course has no outline yet.');
  empty.hidden = Boolean(course.units.length);
  section.append(unitHost, empty);
  if (!stats.total) filterRow.hidden = true;
  if (!units.length) controls.hidden = true;
  let beforeFilter = null;
  input.addEventListener('input', () => {
    const query = input.value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').trim().toLocaleLowerCase();
    const tokens = query.split(/\s+/).filter(Boolean);
    if (query && !beforeFilter) beforeFilter = units.map(unit => unit.open);
    const matches = new Set();
    units.forEach((unit, index) => {
      let matching = 0;
      for (const module of unit.querySelectorAll('.module')) {
        let moduleMatches = 0;
        for (const row of module.querySelectorAll('[data-search]')) {
          row.hidden = !tokens.every(token => row.dataset.search.includes(token));
          if (!row.hidden) { matching++; moduleMatches++; matches.add(row.dataset.topicKey); }
        }
        module.hidden = Boolean(query) && moduleMatches === 0;
      }
      unit.hidden = Boolean(query) && matching === 0;
      if (query && matching) unit.open = true;
      else if (!query && beforeFilter) unit.open = beforeFilter[index];
    });
    if (!query) beforeFilter = null;
    count.textContent = query ? `${matches.size} / ${stats.total} topics` : '';
    empty.hidden = query ? matches.size > 0 : units.length > 0;
    if (query) empty.textContent = 'No topics match your filter.';
  });
  return section;
}
function revealHash() {
  if (!location.hash) return;
  const target = document.getElementById(location.hash.slice(1));
  if (target?.classList.contains('unit')) { target.open = true; target.scrollIntoView({ block: 'start' }); }
}
function captureView() {
  return {
    openUnits: [...document.querySelectorAll('.unit')].map(unit => unit.open),
    filter: $('topicFilter')?.value || '',
    readingOpen: document.querySelector('.course-reading')?.open || false,
    scrollY: window.scrollY,
  };
}
function renderCourse(data, focus, previousView) {
  const course = data.course;
  currentCourseId = course.id;
  $('courseTitle').textContent = course.title; $('courseTitle').title = course.title;
  $('courseLevel').textContent = levelName(course.level) || 'Course';
  $('learnerName').textContent = data.learner?.name || '';
  $('courseLink').href = courseURL(course.id); $('graphLink').href = graphURL(course.id);
  document.title = `${course.title} · Course Academy`;
  const stats = statistics(course.units.flatMap(unitTopics));
  const unitIds = course.units.map((unit, index) => 'unit-' + (index + 1));
  const layout = el('div', 'course-layout');
  const body = el('div', 'course-body');
  const header = courseHeading(data, stats.total); body.append(header);
  const reading = courseReading(course); if (reading) body.append(reading);
  body.append(progressSection(stats), outline(course, unitIds, stats));
  layout.append(sidebar(data, unitIds), body);
  $('main').replaceChildren(layout);
  if (previousView) {
    document.querySelectorAll('.unit').forEach((unit, index) => { unit.open = previousView.openUnits[index] ?? false; });
    const reading = document.querySelector('.course-reading'); if (reading) reading.open = previousView.readingOpen;
    const input = $('topicFilter'); if (input && previousView.filter) { input.value = previousView.filter; input.dispatchEvent(new Event('input')); }
    window.scrollTo({ top: previousView.scrollY });
  }
  typeset(header);
  if (focus) { $('main').focus({ preventScroll: true }); window.scrollTo({ top: 0 }); }
  if (!previousView) revealHash();
  $('announcement').textContent = `${course.title}. ${completionLabel(stats)}. ${stats.completed} of ${stats.total} topics completed.`;
}
function renderError(error) {
  const section = el('section', 'empty-state'); section.setAttribute('role', 'alert');
  section.append(el('h1', '', error.status === 404 || error.status === 400 ? 'Course not found' : 'Unable to load this course'), el('p', '', error.message));
  const actions = el('div', 'error-actions');
  if (error.status !== 400 && error.status !== 404) actions.append(button('Try again', 'small-button', () => loadCourse()));
  const ownCourse = link('Your study course', '/course', 'small-button');
  ownCourse.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); void navigate(null);
  });
  actions.append(ownCourse, button('Browse courses', 'small-button', () => picker.open()));
  section.append(actions); $('main').replaceChildren(section);
  $('announcement').textContent = error.message;
}
async function loadCourse(focus = false) {
  const route = location.pathname + location.search;
  const previousView = !focus && currentCourseId && loadedRoute === route ? captureView() : null;
  const request = ++generation;
  requestController?.abort(); requestController = new AbortController();
  loadedRoute = route;
  const id = new URL(location.href).searchParams.get('course');
  currentCourseId = null;
  $('main').setAttribute('aria-busy', 'true');
  if (window.MathJax?.typesetClear) MathJax.typesetClear([$('main')]);
  $('main').replaceChildren(el('p', 'loading', 'Loading course…'));
  $('courseTitle').textContent = 'Course Academy'; $('courseTitle').removeAttribute('title');
  $('courseLevel').textContent = 'Course'; $('graphLink').href = '/'; $('courseLink').href = '/course';
  document.title = 'Course · Course Academy';
  try {
    if (id !== null && !/^(?:[1-9]\d*|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$/i.test(id)) {
      const error = new Error('The course address is invalid. Choose a course below or search the curriculum.'); error.status = 400; throw error;
    }
    const data = await api('/api/course' + (id ? '?course=' + encodeURIComponent(id) : ''), requestController.signal);
    if (request !== generation) return;
    if (!data.course?.id || !Array.isArray(data.course.units)) throw new Error('The course data is unavailable. Try again.');
    renderCourse(data, focus, previousView);
    lastLoadedAt = Date.now(); refreshNeeded = false;
  } catch (error) {
    if (request === generation && error.name !== 'AbortError') renderError(error);
  } finally {
    if (request === generation) $('main').setAttribute('aria-busy', 'false');
  }
}
const picker = createCoursePicker({
  getSnapshot: async () => {
    if (!curriculumSnapshot) curriculumSnapshot = api('/api/graph-explorer').catch(error => { curriculumSnapshot = null; throw error; });
    return curriculumSnapshot;
  },
  getCourseId: () => currentCourseId,
  onSelectCourse: course => course.id ? navigate(course.id) : location.assign(graphURL(null)),
  onSelectTopic: async topic => {
    const snapshot = await curriculumSnapshot;
    const containing = snapshot.courses.filter(course => course.topicIds.includes(Number(topic.id)));
    const course = containing.find(course => course.id === currentCourseId) || containing.find(course => course.id === snapshot.learner?.courseId) || containing[0];
    location.assign(topicURL(topic, course?.id));
  },
});
window.addEventListener('popstate', () => {
  if (loadedRoute !== location.pathname + location.search) void loadCourse(true);
  else revealHash();
});
function refreshOnReturn() {
  if (!document.hidden && refreshNeeded && currentCourseId && Date.now() - lastLoadedAt > 5000) void loadCourse();
}
document.addEventListener('visibilitychange', () => {
  if (document.hidden) refreshNeeded = true;
  else refreshOnReturn();
});
window.addEventListener('blur', () => { refreshNeeded = true; });
window.addEventListener('focus', refreshOnReturn);
void loadCourse();
