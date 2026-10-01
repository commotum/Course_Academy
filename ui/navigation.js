// Keep sticky sidebars and anchor targets below the header, including when
// its navigation wraps onto another row on narrow screens.
const siteHeader = document.querySelector('.site-header');
if (siteHeader) {
  const measureHeader = () => document.documentElement.style.setProperty('--site-header-height', `${Math.ceil(siteHeader.getBoundingClientRect().height)}px`);
  measureHeader();
  if ('ResizeObserver' in window) new ResizeObserver(measureHeader).observe(siteHeader);
  else window.addEventListener('resize', measureHeader);
}

function node(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}
function levelLabel(value) {
  const key = String(value || '').split('/').at(-1);
  return { 'early-math': 'Early Math', 'high-school-math': 'High School Math', 'university-math': 'University Math' }[key] || '';
}
function normalize(value) { return String(value ?? '').toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').trim(); }

export function topicReferenceURL(snapshot, topic, preferredCourseId) {
  const containing = snapshot.courses.filter(course => course.topicIds.some(id => String(id) === String(topic.id)));
  const course = containing.find(course => course.id === preferredCourseId) || containing.find(course => course.id === snapshot.learner?.courseId) || containing[0];
  return '/topic?topic=' + encodeURIComponent(topic.uuid || topic.mathAcademyId || topic.id) + (course ? '&course=' + encodeURIComponent(course.id) : '');
}

// Normalize and join memberships once per immutable curriculum snapshot, rather
// than scanning every course's membership and sorting names on each keystroke.
const indexes = new WeakMap();
export function indexCurriculum(snapshot) {
  if (indexes.has(snapshot)) return indexes.get(snapshot);
  const memberships = new Map();
  for (const course of snapshot.courses) for (const topic of course.topicIds) {
    if (!memberships.has(topic)) memberships.set(topic, []);
    memberships.get(topic).push(course.title);
  }
  const courses = snapshot.courses.map((course, index) => ({
    value: course, index: String(index + 1).padStart(2, '0'), values: [course.title, course.id, course.code].map(normalize),
    meta: `${levelLabel(course.level) || 'Course'} · ${course.topicIds.length.toLocaleString()} topics`,
  }));
  const coursesById = new Map(courses.map(course => [course.value.id, course]));
  const sequences = (snapshot.sequences || []).map((sequence, index) => ({
    value: sequence, index: String(index + 1).padStart(2, '0'), values: [sequence.title, sequence.id].map(normalize),
    courses: sequence.courseIds.map(id => coursesById.get(id)).filter(Boolean),
    meta: `Sequence · ${sequence.courseIds.length} courses · ${sequence.topicIds.length.toLocaleString()} topics`,
  }));
  const topics = snapshot.nodes.map(topic => {
    const names = memberships.get(topic.id) || [];
    const details = [topic.mathAcademyId != null ? `Topic ${topic.mathAcademyId}` : 'Topic'];
    if (names.length) details.push(names.slice(0, 2).join(' · ') + (names.length > 2 ? ` · +${names.length - 2} courses` : ''));
    return { value: topic, name: normalize(topic.name), values: [topic.name, topic.id, topic.uuid, topic.mathAcademyId].map(normalize), meta: details.join(' · ') };
  }).sort((a, b) => a.value.name.localeCompare(b.value.name));
  const index = { courses, sequences, topics };
  indexes.set(snapshot, index);
  return index;
}
export function searchCurriculum(index, text) {
  const query = normalize(text), tokens = query.split(/\s+/).filter(Boolean);
  const matches = entry => tokens.every(token => entry.values.some(value => value.includes(token)));
  const courses = query ? index.courses.filter(matches) : [];
  const sequences = query ? index.sequences.filter(matches) : [];
  const buckets = [[], [], []];
  if (query) for (const topic of index.topics) if (matches(topic)) {
    buckets[topic.values.includes(query) ? 0 : topic.name.startsWith(query) ? 1 : 2].push(topic);
  }
  return { courses, sequences, topics: buckets.flat() };
}

// Every page shares this curriculum browser. Sequences expand in place;
// browsing courses and reference topics never changes the learner's study course.
export function createCoursePicker({ getSnapshot, getCourseId, onSelectCourse, onSelectTopic }) {
  const trigger = document.getElementById('courseBrowse');
  const dialog = node('dialog'); dialog.id = 'coursePicker'; dialog.setAttribute('aria-labelledby', 'coursePickerTitle');
  const head = node('div', 'course-picker-head');
  const heading = node('div'); heading.append(node('span', 'picker-kicker', 'Explore the curriculum'));
  const title = node('h2', '', 'Sequences, courses & topics'); title.id = 'coursePickerTitle'; heading.append(title);
  const closeButton = node('button', 'picker-close', '×'); closeButton.id = 'closeCoursePicker'; closeButton.type = 'button'; closeButton.setAttribute('aria-label', 'Close search');
  head.append(heading, closeButton);
  const input = node('input'); input.id = 'courseFilter'; input.type = 'search'; input.placeholder = 'Find any sequence, course or topic…'; input.autocomplete = 'off';
  input.setAttribute('aria-label', 'Find a sequence, course or topic across the entire curriculum'); input.setAttribute('aria-controls', 'courseList'); input.setAttribute('autofocus', '');
  const error = node('p', 'picker-error'); error.setAttribute('role', 'alert'); error.hidden = true;
  const list = node('div', 'course-list'); list.id = 'courseList';
  const foot = node('div', 'course-picker-foot');
  const count = node('span'); count.id = 'courseCount'; count.setAttribute('aria-live', 'polite'); count.setAttribute('aria-atomic', 'true');
  foot.append(count, node('span', '', 'View only · study selection unchanged'));
  dialog.append(head, input, error, list, foot); document.body.append(dialog);
  const shortcut = /Mac|iPhone|iPad/.test(navigator.platform) ? '⌘ K' : 'Ctrl K';
  if (trigger) {
    trigger.setAttribute('aria-keyshortcuts', 'Meta+K Control+K');
    trigger.setAttribute('aria-controls', dialog.id);
    trigger.setAttribute('aria-label', `Explore sequences, courses and topics (${shortcut})`);
  }
  let snapshot = null;
  let loading = false;
  let selecting = false;
  let returnFocus = null;
  const expandedSequences = new Set();

  function message(text) { list.replaceChildren(node('p', 'picker-message', text)); }
  function close() { if (dialog.open) dialog.close(); }
  function options() { return [...list.querySelectorAll('.course-option:not(:disabled)')].filter(button => !button.closest('[hidden]')); }
  async function choose(action, value) {
    if (selecting) return;
    selecting = true; error.hidden = true; list.setAttribute('aria-busy', 'true');
    for (const button of options()) button.disabled = true;
    try { await action(value); close(); }
    catch (failure) { error.textContent = failure.message || String(failure); error.hidden = false; }
    finally { selecting = false; list.removeAttribute('aria-busy'); for (const button of list.querySelectorAll('button')) button.disabled = false; }
  }
  function option({ title, meta, index, current = false, action, value, host = list, expand }) {
    const button = node('button', 'course-option'); button.type = 'button';
    if (current) button.setAttribute('aria-current', 'true');
    const label = node('span'); label.append(node('span', 'course-option-title', title), node('span', 'course-option-meta', meta));
    const arrow = node('span', 'course-arrow', expand ? '+' : current ? '•' : '↗'); arrow.setAttribute('aria-hidden', 'true');
    const number = node('span', 'course-index', index); number.setAttribute('aria-hidden', 'true');
    button.append(number, label, arrow);
    button.addEventListener('click', () => expand ? expand(button, arrow) : choose(action, value));
    host.append(button);
    return button;
  }
  function render() {
    list.replaceChildren(); error.hidden = true;
    const query = normalize(input.value);
    count.textContent = '';
    if (!query || !snapshot || loading) return;
    const { courses: courseMatches, sequences: sequenceMatches, topics: topicMatches } = searchCurriculum(indexCurriculum(snapshot), query);
    if (sequenceMatches.length) {
      list.append(node('h3', 'picker-group-title', 'Sequences'));
      sequenceMatches.forEach(({ value: sequence, courses, meta, index }) => {
        const group = node('div', 'picker-sequence');
        const children = node('div', 'sequence-courses');
        children.id = 'sequence-courses-' + sequence.id;
        children.setAttribute('role', 'group'); children.setAttribute('aria-label', sequence.title + ' courses');
        children.hidden = !expandedSequences.has(sequence.id);
        const toggle = option({
          title: sequence.title, meta, index, host: group,
          expand: (button, arrow) => {
            children.hidden = !children.hidden;
            if (children.hidden) expandedSequences.delete(sequence.id); else expandedSequences.add(sequence.id);
            button.setAttribute('aria-expanded', String(!children.hidden));
            arrow.textContent = children.hidden ? '+' : '−';
          },
        });
        toggle.setAttribute('aria-expanded', String(!children.hidden));
        toggle.setAttribute('aria-controls', children.id);
        toggle.querySelector('.course-arrow').textContent = children.hidden ? '+' : '−';
        courses.forEach(({ value: course, meta }, courseIndex) => option({
          title: course.title, meta, index: String(courseIndex + 1).padStart(2, '0'), host: children,
          current: getCourseId() === course.id, action: onSelectCourse, value: course,
        }));
        if (!courses.length) children.append(node('p', 'picker-message', 'No courses in this sequence.'));
        group.append(children); list.append(group);
      });
    }
    if (courseMatches.length) {
      list.append(node('h3', 'picker-group-title', 'Courses'));
      courseMatches.forEach(({ value: course, meta, index }) => option({
        title: course.title,
        meta, index,
        current: (getCourseId() || null) === course.id,
        action: onSelectCourse, value: course,
      }));
    }
    // No selected-course filter belongs here: topic search is always global.
    if (topicMatches.length) {
      list.append(node('h3', 'picker-group-title', 'Topics · all courses'));
      topicMatches.slice(0, 80).forEach(({ value: topic, meta }) => {
        option({ title: topic.name, meta, index: '↳', action: onSelectTopic, value: topic });
      });
      if (topicMatches.length > 80) list.append(node('p', 'picker-message', `Showing the first 80 of ${topicMatches.length.toLocaleString()} topics. Keep typing to narrow your search.`));
    }
    if (!courseMatches.length && !sequenceMatches.length && !topicMatches.length) message('No sequences, courses or topics match your search.');
    count.textContent = `${sequenceMatches.length} sequences · ${courseMatches.length} courses · ${topicMatches.length.toLocaleString()} topics`;
  }
  async function refresh() {
    loading = true; error.hidden = true; count.textContent = ''; list.replaceChildren();
    if (normalize(input.value)) { count.textContent = 'Loading curriculum…'; message('Loading sequences, courses and topics…'); }
    try {
      const data = await getSnapshot();
      if (!Array.isArray(data?.courses) || !Array.isArray(data?.nodes)) throw new Error('The curriculum data is unavailable. Close search and try again.');
      snapshot = data;
    } catch (failure) {
      snapshot = null; error.textContent = failure.message || String(failure); error.hidden = false;
      message('Close search and reopen it to try again.'); count.textContent = 'Unable to load curriculum';
    } finally { loading = false; if (snapshot) render(); }
  }
  async function open() {
    if (dialog.open) { input.focus(); return; }
    returnFocus = document.activeElement;
    expandedSequences.clear();
    input.value = ''; error.hidden = true; dialog.showModal(); input.focus();
    await refresh();
  }
  input.addEventListener('input', render);
  dialog.addEventListener('keydown', event => {
    if (!['ArrowDown', 'ArrowUp', 'Enter', 'Home', 'End'].includes(event.key)) return;
    const buttons = options(); if (!buttons.length) return;
    const index = buttons.indexOf(document.activeElement);
    if (event.key === 'Enter' && document.activeElement === input) { event.preventDefault(); buttons[0].click(); }
    else if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
      if (document.activeElement !== input && index === -1) return;
      event.preventDefault();
      if (event.key === 'ArrowUp' && index === 0) input.focus();
      else buttons[index === -1 ? (event.key === 'ArrowDown' ? 0 : buttons.length - 1) : (index + (event.key === 'ArrowDown' ? 1 : -1) + buttons.length) % buttons.length].focus();
    } else if (index !== -1 && (event.key === 'Home' || event.key === 'End')) {
      event.preventDefault(); buttons[event.key === 'Home' ? 0 : buttons.length - 1].focus();
    }
  });
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) close();
  });
  dialog.addEventListener('close', () => { if (returnFocus?.isConnected) returnFocus.focus({ preventScroll: true }); });
  closeButton.addEventListener('click', close);
  trigger?.addEventListener('click', open);
  document.addEventListener('keydown', event => {
    if ((event.metaKey || event.ctrlKey) && !event.altKey && event.key.toLowerCase() === 'k') {
      event.preventDefault(); if (dialog.open) close(); else void open();
    }
  });
  return { open, close, refresh };
}
