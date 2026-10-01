import { marked } from './vendor/marked/marked.esm.js';
import { createCoursePicker } from './navigation.js';

const $ = id => document.getElementById(id);
let currentCourseId = null;
let curriculumSnapshot = null;
let requestController = null;
let generation = 0;
let mathLoader = null;
let typesetting = Promise.resolve();
let sectionObserver = null;

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function link(text, href, className = '') {
  const node = el('a', className, text); node.href = href; return node;
}
function button(text, className, action) {
  const node = el('button', className, text);
  node.type = 'button'; node.addEventListener('click', action); return node;
}
function short(value) { return String(value || '').split('/').at(-1); }
function levelName(value) {
  return { 'early-math': 'Early Math', 'high-school-math': 'High School Math', 'university-math': 'University Math' }[short(value)] || 'Course';
}
function courseURL(id) { return '/course' + (id ? '?course=' + encodeURIComponent(id) : ''); }
function topicURL(topic, courseId) {
  return '/topic?topic=' + encodeURIComponent(topic.uuid || topic.mathAcademyId || topic.id) + (courseId ? '&course=' + encodeURIComponent(courseId) : '');
}
function graphURL(courseId, topicId) {
  return '/?course=' + encodeURIComponent(courseId || 'all') + (topicId == null ? '' : '&topic=' + encodeURIComponent(topicId));
}
function escapeHTML(text) { return String(text).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]); }
function assetURL(value) {
  if (!value) return '';
  if (String(value).startsWith('/api/asset?')) return value;
  return '/api/asset?path=' + encodeURIComponent(String(value).replace(/^file:\/\//, ''));
}
function fieldLabel(key, index) {
  if (!key || key === 'selection') return 'Answer';
  const numbered = /^field-(\d+)$/.exec(key);
  return numbered ? `Answer ${numbered[1]}` : `Answer ${index + 1}`;
}
function markdown(value, className = 'prose', fields = []) {
  const container = el('div', className);
  // Protect TeX before Markdown handles backslashes, underscores and table pipes.
  const math = [];
  const prefix = 'CAMATH' + crypto.randomUUID().replaceAll('-', '') + 'TOKEN';
  const placeholder = /\{\{(?:answer-field:)?([^}]+)\}\}/g;
  const fieldIndex = key => fields.findIndex(field => field.key === key);
  let source = String(value || '').replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g, match => {
    math.push(match.replace(placeholder, (whole, key) => fieldIndex(key) < 0 ? whole : `\\underbrace{\\qquad}_{\\text{answer ${fieldIndex(key) + 1}}}`));
    return prefix + (math.length - 1) + 'END';
  });
  source = source.replace(placeholder, (whole, key) => fieldIndex(key) < 0 ? whole : `<span class="field-location">${escapeHTML(fieldLabel(key, fieldIndex(key)))}</span>`);
  let html = marked.parse(source, { async: false, gfm: true, breaks: false });
  html = html.replace(new RegExp(prefix + '(\\d+)END', 'g'), (_, i) => escapeHTML(math[Number(i)]));
  const fragment = DOMPurify.sanitize(html, {
    RETURN_DOM_FRAGMENT: true,
    USE_PROFILES: { html: true },
    FORBID_TAGS: ['style', 'form', 'input', 'button', 'textarea', 'select', 'iframe', 'object', 'embed', 'video', 'audio'],
    FORBID_ATTR: ['style', 'srcset', 'id', 'name'],
  });
  for (const image of fragment.querySelectorAll('img')) {
    image.src = assetURL(image.getAttribute('src'));
    image.referrerPolicy = 'no-referrer'; image.loading = 'lazy';
    image.addEventListener('error', () => image.replaceWith(el('span', 'image-note', `Image unavailable${image.alt ? ': ' + image.alt : '.'}`)), { once: true });
  }
  for (const anchor of fragment.querySelectorAll('a')) {
    const href = anchor.getAttribute('href') || '';
    if (!/^https?:\/\//i.test(href)) anchor.removeAttribute('href');
    else { anchor.target = '_blank'; anchor.rel = 'noopener noreferrer'; }
  }
  container.append(fragment);
  if (math.length) container.dataset.math = 'true';
  return container;
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
  if (!host.querySelector('[data-math]')) return Promise.resolve();
  typesetting = typesetting.catch(() => {}).then(async () => {
    if (!host.isConnected) return;
    await loadMath();
    if (host.isConnected) await MathJax.typesetPromise([host]);
  }).catch(() => {
    if (host.isConnected && !host.querySelector('.math-note')) host.append(el('p', 'math-note', 'Math notation could not be rendered. Refresh the page to try again.'));
  });
  return typesetting;
}
async function api(path, signal) {
  const response = await fetch(path, { cache: 'no-store', signal });
  let result;
  try { result = await response.json(); } catch { throw new Error('The topic server did not return a response. Check that it is running, then try again.'); }
  if (!response.ok || result.error) {
    const error = new Error(result.error || `The request failed (${response.status}).`);
    error.status = response.status; throw error;
  }
  return result;
}
function sidebar(data, sections, course) {
  const aside = el('aside', 'topic-sidebar'); aside.setAttribute('aria-label', 'Topic navigation');
  const content = el('div', 'sidebar-content');
  if (sections.length) {
    const nav = el('nav'); nav.setAttribute('aria-label', 'In this topic');
    nav.append(el('h2', 'sidebar-label', 'In this topic'));
    const list = el('ol', 'topic-toc');
    sections.forEach(section => {
      const item = el('li'); const anchor = link(section.title, '#' + section.anchor);
      item.append(anchor); list.append(item);
    });
    nav.append(list); content.append(nav);
  }
  if (data.prerequisites?.length) {
    const nav = el('nav', 'prerequisites'); nav.setAttribute('aria-label', 'Prerequisites');
    nav.append(el('h2', 'sidebar-label', 'Prerequisites'));
    const list = el('ul', 'prerequisite-list');
    for (const prerequisite of data.prerequisites) {
      const item = el('li'); item.append(link(prerequisite.title, topicURL(prerequisite, course?.id))); list.append(item);
    }
    nav.append(list); content.append(nav);
  }
  const links = el('div', 'sidebar-links');
  if (course) links.append(link('← ' + course.title, courseURL(course.id), 'sidebar-link'));
  links.append(link('View topic in graph ↗', graphURL(course?.id, data.topic.id), 'sidebar-link'));
  content.append(links); aside.append(content); return aside;
}
function canonicalAnswers(fields) {
  const answers = el('div', 'canonical-answers');
  fields.forEach((field, index) => {
    if (field.correct == null) return;
    const choice = (field.choices || []).find(choice => String(choice.id) === String(field.correct));
    if (!choice) return;
    const value = choice.value;
    const type = short(choice.type);
    const row = el('div', 'canonical-answer');
    row.append(el('p', 'section-label', fieldLabel(field.key, index)));
    if (type === 'image') {
      row.append(markdown(`![Answer](${assetURL(value)})`));
    } else {
      const text = String(value);
      row.append(markdown(type === 'math' && !/^\s*(\$|\\\[|\\\()/.test(text) ? '$' + text + '$' : text));
    }
    answers.append(row);
  });
  return answers.children.length ? answers : null;
}
function instructionalSection(section) {
  const article = el('section', 'topic-section'); article.id = section.anchor;
  article.setAttribute('aria-labelledby', section.anchor + '-title');
  const header = el('div', 'section-heading');
  const label = el('div');
  if (section.kind === 'example') label.append(el('div', 'section-label', 'Worked example ' + section.exampleNumber));
  const heading = el('h2', '', section.title); heading.id = section.anchor + '-title';
  label.append(heading); header.append(label);
  if (section.requiresCalculator) header.append(el('span', 'calculator-note', 'Calculator example'));
  article.append(header);
  const fields = section.fields || [];
  if (section.markdown?.trim()) article.append(markdown(section.markdown, 'prose', fields));
  if (section.workedSolution?.trim()) {
    const solution = el('div', 'worked-solution');
    solution.append(el('h3', 'section-label', 'Worked solution'), markdown(section.workedSolution, 'prose', fields));
    article.append(solution);
  }
  if (section.kind === 'example') {
    const answers = canonicalAnswers(fields); if (answers) article.append(answers);
  }
  return article;
}
function revealHash() {
  const target = document.getElementById(location.hash.slice(1));
  if (target?.classList.contains('topic-section')) target.scrollIntoView({ block: 'start' });
}
function observeSections(sections) {
  sectionObserver?.disconnect();
  if (!sections.length) return;
  const links = [...document.querySelectorAll('.topic-toc a')];
  const visible = new Set();
  const select = id => {
    for (const anchor of links) {
      if (anchor.hash === '#' + id) anchor.setAttribute('aria-current', 'location');
      else anchor.removeAttribute('aria-current');
    }
  };
  select(sections[0].anchor);
  if (!('IntersectionObserver' in window)) return;
  sectionObserver = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (entry.isIntersecting) visible.add(entry.target.id); else visible.delete(entry.target.id);
    }
    const active = sections.find(section => visible.has(section.anchor));
    if (active) select(active.anchor);
  }, { rootMargin: '-10% 0px -55% 0px' });
  for (const section of sections) sectionObserver.observe($(section.anchor));
}
function renderTopic(data) {
  const requestedCourse = new URL(location.href).searchParams.get('course');
  const courses = data.courses || [];
  const course = courses.find(course => course.id === requestedCourse) || courses.find(course => course.id === data.learner?.courseId) || courses[0];
  currentCourseId = course?.id || null;
  $('courseTitle').textContent = course?.title || 'Course Academy'; $('courseTitle').title = course?.title || 'Course Academy';
  $('courseLevel').textContent = course ? levelName(course.level) : 'Topic';
  $('learnerName').textContent = data.learner?.name || '';
  $('courseLink').href = courseURL(currentCourseId); $('graphLink').href = graphURL(currentCourseId);
  document.title = `${data.topic.title} · Course Academy`;
  let exampleNumber = 0;
  const sections = data.sections.filter(section => ['tutorial', 'example'].includes(section.kind)).map((section, index) => {
    if (section.kind === 'example') exampleNumber++;
    return { ...section, anchor: 'section-' + (index + 1), exampleNumber, title: section.title?.trim() || (section.kind === 'example' ? 'Example ' + exampleNumber : 'Introduction') };
  });
  const layout = el('div', 'topic-layout'); const body = el('article', 'topic-body');
  const header = el('header', 'topic-heading');
  header.append(el('p', 'eyebrow', 'Topic'), el('h1', '', data.topic.title));
  const facts = el('div', 'topic-facts');
  const tutorials = sections.filter(section => section.kind === 'tutorial').length;
  if (tutorials) facts.append(el('span', '', `${tutorials} ${tutorials === 1 ? 'tutorial' : 'tutorials'}`));
  if (exampleNumber) facts.append(el('span', '', `${exampleNumber} worked ${exampleNumber === 1 ? 'example' : 'examples'}`));
  if (course) facts.append(link(course.title, courseURL(course.id)));
  header.append(facts); body.append(header);
  if (sections.length) sections.forEach(section => body.append(instructionalSection(section)));
  else {
    const empty = el('section', 'empty-state');
    empty.append(el('h2', '', 'No lesson content available'), el('p', '', 'Tutorials and worked examples have not been added for this topic yet. You can explore its prerequisites or return to the course.'));
    body.append(empty);
  }
  layout.append(sidebar(data, sections, course), body); $('main').replaceChildren(layout);
  observeSections(sections);
  revealHash();
  const initialHash = location.hash;
  void typeset(body).then(() => { if (body.isConnected && initialHash && location.hash === initialHash) revealHash(); });
  $('announcement').textContent = `${data.topic.title}. ${tutorials} tutorials and ${exampleNumber} worked examples.`;
}
function renderError(error) {
  const section = el('section', 'empty-state'); section.setAttribute('role', 'alert');
  section.append(el('h1', '', error.status === 400 || error.status === 404 ? 'Topic not found' : 'Unable to load this topic'), el('p', '', error.message));
  const actions = el('div', 'error-actions');
  if (error.status !== 400 && error.status !== 404) actions.append(button('Try again', 'small-button', () => loadTopic()));
  actions.append(link('Your study course', '/course', 'small-button'), button('Browse topics', 'small-button', () => picker.open()));
  section.append(actions); $('main').replaceChildren(section);
  $('announcement').textContent = error.message;
}
async function loadTopic() {
  const request = ++generation;
  requestController?.abort(); requestController = new AbortController();
  sectionObserver?.disconnect(); currentCourseId = null;
  $('main').setAttribute('aria-busy', 'true');
  if (window.MathJax?.typesetClear) MathJax.typesetClear([$('main')]);
  $('main').replaceChildren(el('p', 'loading', 'Loading topic…'));
  try {
    const id = new URL(location.href).searchParams.get('topic');
    if (!id || !/^(?:[1-9]\d*|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$/i.test(id)) {
      const error = new Error('Choose a topic from your course or search the curriculum.'); error.status = 400; throw error;
    }
    const data = await api('/api/topic?topic=' + encodeURIComponent(id), requestController.signal);
    if (request !== generation) return;
    if (!data.topic?.title || !Array.isArray(data.sections)) throw new Error('The topic data is unavailable. Try again.');
    renderTopic(data);
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
  onSelectCourse: course => location.assign(course.id ? courseURL(course.id) : graphURL(null)),
  onSelectTopic: async topic => {
    const snapshot = await curriculumSnapshot;
    const containing = snapshot.courses.filter(course => course.topicIds.some(id => String(id) === String(topic.id)));
    const course = containing.find(course => course.id === currentCourseId) || containing.find(course => course.id === snapshot.learner?.courseId) || containing[0];
    location.assign(topicURL(topic, course?.id));
  },
});
window.addEventListener('hashchange', revealHash);
void loadTopic();
