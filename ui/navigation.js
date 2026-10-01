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
  const courses = [{ id: null, title: 'All topics', topicIds: snapshot.nodes.map(topic => topic.id) }, ...snapshot.courses].map((course, index) => ({
    value: course, index: String(index).padStart(2, '0'), values: [course.title, course.id, course.code].map(normalize),
    meta: `${course.id === null ? 'Entire knowledge graph' : levelLabel(course.level) || 'Course'} · ${course.topicIds.length.toLocaleString()} topics`,
  }));
  const topics = snapshot.nodes.map(topic => {
    const names = memberships.get(topic.id) || [];
    const details = [topic.mathAcademyId != null ? `Topic ${topic.mathAcademyId}` : 'Topic'];
    if (names.length) details.push(names.slice(0, 2).join(' · ') + (names.length > 2 ? ` · +${names.length - 2} courses` : ''));
    return { value: topic, name: normalize(topic.name), values: [topic.name, topic.id, topic.uuid, topic.mathAcademyId].map(normalize), meta: details.join(' · ') };
  }).sort((a, b) => a.value.name.localeCompare(b.value.name));
  const index = { courses, topics };
  indexes.set(snapshot, index);
  return index;
}
export function searchCurriculum(index, text) {
  const query = normalize(text), tokens = query.split(/\s+/).filter(Boolean);
  const matches = entry => tokens.every(token => entry.values.some(value => value.includes(token)));
  const courses = index.courses.filter(matches);
  const buckets = [[], [], []];
  if (query) for (const topic of index.topics) if (matches(topic)) {
    buckets[topic.values.includes(query) ? 0 : topic.name.startsWith(query) ? 1 : 2].push(topic);
  }
  return { courses, topics: buckets.flat() };
}

// Both pages share one picker. Its snapshot always contains the complete graph;
// changing the viewed course never writes the learner's designated study course.
export function createCoursePicker({ getSnapshot, getCourseId, onSelectCourse, onSelectTopic }) {
  const trigger = document.getElementById('courseBrowse');
  const dialog = node('dialog'); dialog.id = 'coursePicker'; dialog.setAttribute('aria-labelledby', 'coursePickerTitle');
  const head = node('div', 'course-picker-head');
  const heading = node('div'); heading.append(node('span', 'picker-kicker', 'Explore the curriculum'));
  const title = node('h2', '', 'Courses & topics'); title.id = 'coursePickerTitle'; heading.append(title);
  const closeButton = node('button', 'picker-close', '×'); closeButton.id = 'closeCoursePicker'; closeButton.type = 'button'; closeButton.setAttribute('aria-label', 'Close search');
  head.append(heading, closeButton);
  const input = node('input'); input.id = 'courseFilter'; input.type = 'search'; input.placeholder = 'Find any course or topic…'; input.autocomplete = 'off';
  input.setAttribute('aria-label', 'Find a course or topic across the entire curriculum'); input.setAttribute('aria-controls', 'courseList'); input.setAttribute('autofocus', '');
  const error = node('p', 'picker-error'); error.setAttribute('role', 'alert'); error.hidden = true;
  const list = node('div', 'course-list'); list.id = 'courseList';
  const foot = node('div', 'course-picker-foot');
  const count = node('span'); count.id = 'courseCount'; count.setAttribute('aria-live', 'polite'); count.setAttribute('aria-atomic', 'true');
  foot.append(count, node('span', '', 'View only · study course unchanged'));
  dialog.append(head, input, error, list, foot); document.body.append(dialog);
  const shortcut = /Mac|iPhone|iPad/.test(navigator.platform) ? '⌘ K' : 'Ctrl K';
  if (trigger) {
    const hint = trigger.querySelector('kbd'); if (hint) hint.textContent = shortcut;
    trigger.setAttribute('aria-keyshortcuts', 'Meta+K Control+K');
    trigger.setAttribute('aria-controls', dialog.id);
    trigger.setAttribute('aria-label', `Search all courses and topics (${shortcut})`);
  }
  let snapshot = null;
  let loading = false;
  let selecting = false;
  let returnFocus = null;

  function message(text) { list.replaceChildren(node('p', 'picker-message', text)); }
  function close() { if (dialog.open) dialog.close(); }
  function options() { return [...list.querySelectorAll('.course-option:not(:disabled)')]; }
  async function choose(action, value) {
    if (selecting) return;
    selecting = true; error.hidden = true; list.setAttribute('aria-busy', 'true');
    for (const button of options()) button.disabled = true;
    try { await action(value); close(); }
    catch (failure) { error.textContent = failure.message || String(failure); error.hidden = false; }
    finally { selecting = false; list.removeAttribute('aria-busy'); for (const button of list.querySelectorAll('button')) button.disabled = false; }
  }
  function option({ title, meta, index, current = false, action, value }) {
    const button = node('button', 'course-option'); button.type = 'button';
    if (current) button.setAttribute('aria-current', 'true');
    const label = node('span'); label.append(node('span', 'course-option-title', title), node('span', 'course-option-meta', meta));
    const arrow = node('span', 'course-arrow', current ? '•' : '↗'); arrow.setAttribute('aria-hidden', 'true');
    const number = node('span', 'course-index', index); number.setAttribute('aria-hidden', 'true');
    button.append(number, label, arrow); button.addEventListener('click', () => choose(action, value));
    list.append(button);
  }
  function render() {
    if (!snapshot || loading) return;
    list.replaceChildren(); error.hidden = true;
    const query = normalize(input.value);
    const { courses: courseMatches, topics: topicMatches } = searchCurriculum(indexCurriculum(snapshot), query);
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
    if (!courseMatches.length && !topicMatches.length) message('No courses or topics match your search.');
    count.textContent = query ? `${courseMatches.length} ${courseMatches.length === 1 ? 'course' : 'courses'} · ${topicMatches.length.toLocaleString()} ${topicMatches.length === 1 ? 'topic' : 'topics'}` : `${snapshot.courses.length} courses · ${snapshot.nodes.length.toLocaleString()} topics`;
  }
  async function refresh() {
    loading = true; error.hidden = true; count.textContent = 'Loading curriculum…'; message('Loading courses and topics…');
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
