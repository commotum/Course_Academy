function node(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

// Presentation order uses stable group IDs; titles and memberships come from the database.
const columnGroupIds = [
  [
    'f9bfb1f6-2f0d-4823-8c41-b0d6fae46cd1', // Elementary School
    '874e333e-54e0-578c-a497-bbb57a1e0f68', // Middle School
    '5ae78dec-46f8-40ad-b2f4-70f6c1b6a570', // High School - Traditional
    'cfaf6e8b-f402-4c5d-a690-3a4c7c818377', // High School - Integrated Math
    'eb022b36-d6be-40f3-9450-a4261d40f4b8', // High School - Integrated Math (Honors)
    '882dd844-5c2c-4238-bb73-f4b39a918906', // Test Prep
  ],
  [
    'ac4e59ea-b8a3-4675-95f4-c6d422d642fa', // Advanced Placement
    '4dfdb3b5-9088-4687-8b8e-3e6a83d67353', // Mathematical Foundations
    'd8c4b174-8797-4f4d-86b7-0f7b33df061b', // University
  ],
];

function catalogColumns(groups) {
  const remaining = new Map(groups.map(group => [group.id, group]));
  const columns = columnGroupIds.map(ids => ids.flatMap(id => {
    const group = remaining.get(id);
    remaining.delete(id);
    return group ? [group] : [];
  }));
  // Keep newly added database groups visible before they have a designated position.
  columns[1].push(...remaining.values());
  return columns;
}

// Single-column course selector for the profile. Course choices remain buttons
// because selecting one changes the learner's study course instead of navigating.
export function createCourseSelect({ loadGroups }) {
  const element = node('div', 'profile-course-select');
  const control = node('button', 'profile-course-trigger'); control.type = 'button'; control.id = 'profileCourse';
  control.setAttribute('aria-haspopup', 'listbox'); control.setAttribute('aria-expanded', 'false');
  const options = node('div', 'profile-course-options'); options.id = 'profileCourseOptions'; options.hidden = true;
  options.setAttribute('role', 'listbox'); options.setAttribute('aria-label', 'Selected course');
  control.setAttribute('aria-controls', options.id);
  element.append(control, options);
  let available = [], groups = null, loading = false;
  let buttons = [];
  let search = '', searchAt = 0;

  function close(focus = false) {
    options.hidden = true; control.setAttribute('aria-expanded', 'false');
    if (focus) control.focus();
  }
  function render() {
    options.replaceChildren(); buttons = [];
    const byId = new Map(available.map(course => [course.id, course]));
    const grouped = new Set();
    const ordered = catalogColumns(groups).flat().map(group => ({ ...group,
      courses: group.courses.filter(course => byId.has(course.id)).map(course => {
        grouped.add(course.id); return byId.get(course.id);
      }),
    })).filter(group => group.courses.length);
    const others = available.filter(course => !grouped.has(course.id));
    if (others.length) ordered.push({ id: 'other', title: 'Other courses', courses: others });
    for (const group of ordered) {
      const section = node('div', 'catalog-group'); section.setAttribute('role', 'group');
      const heading = node('div', 'catalog-group-title', group.title); heading.id = `profile-course-group-${group.id}`;
      section.setAttribute('aria-labelledby', heading.id); section.append(heading);
      for (const course of group.courses) {
        const option = node('button', 'catalog-course', course.title); option.type = 'button'; option.value = course.id; option.tabIndex = -1;
        option.setAttribute('role', 'option'); option.setAttribute('aria-selected', String(course.id === control.value));
        option.addEventListener('click', () => {
          const changed = control.value !== course.id;
          control.value = course.id; control.textContent = course.title;
          control.setAttribute('aria-label', `Selected course: ${course.title}`); close(true);
          if (changed) control.dispatchEvent(new Event('change'));
        });
        buttons.push(option); section.append(option);
      }
      options.append(section);
    }
  }
  async function open(last = false) {
    if (control.disabled || loading) return;
    options.hidden = false; control.setAttribute('aria-expanded', 'true');
    if (!groups) {
      loading = true; options.setAttribute('aria-busy', 'true');
      options.replaceChildren(node('p', 'catalog-message', 'Loading courses…'));
      try { groups = await loadGroups(); }
      catch (failure) {
        options.replaceChildren(node('p', 'catalog-message', failure.message || 'Unable to load courses. Close and reopen to retry.'));
        return;
      } finally { loading = false; options.removeAttribute('aria-busy'); }
    }
    if (options.hidden) return;
    render();
    const selected = buttons.find(button => button.value === control.value);
    (selected || (last ? buttons.at(-1) : buttons[0]))?.focus();
  }
  function update(course, courses) {
    available = courses;
    const selected = courses.find(item => item.id === course.id) || course;
    if (control.value !== course.id) control.value = course.id;
    if (control.textContent !== selected.title) control.textContent = selected.title;
    control.setAttribute('aria-label', `Selected course: ${selected.title}`);
    if (!options.hidden && groups) render();
  }
  control.addEventListener('click', () => { if (options.hidden) void open(); else close(); });
  control.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') { event.preventDefault(); void open(event.key === 'ArrowUp'); }
  });
  options.addEventListener('keydown', event => {
    if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); close(true); return; }
    if (event.key === 'Tab') { close(true); return; }
    const index = buttons.indexOf(document.activeElement);
    let next;
    if (event.key === 'ArrowDown') next = buttons[Math.min(index + 1, buttons.length - 1)];
    else if (event.key === 'ArrowUp') next = buttons[Math.max(index - 1, 0)];
    else if (event.key === 'Home') next = buttons[0];
    else if (event.key === 'End') next = buttons.at(-1);
    else if (event.key.length === 1 && event.key !== ' ' && !event.ctrlKey && !event.metaKey && !event.altKey) {
      const now = Date.now(); search = now - searchAt > 700 ? event.key : search + event.key; searchAt = now;
      next = buttons.find(button => button.textContent.toLocaleLowerCase().startsWith(search.toLocaleLowerCase()));
    }
    if (next) { event.preventDefault(); next.focus(); }
  });
  element.addEventListener('focusout', event => { if (!element.contains(event.relatedTarget)) close(); });
  return { element, control, update, close };
}

// Progress-page catalog, independent of the global Explore search.
export function createCourseCatalog({ getCourseId, getCourseURL, onSelectCourse }) {
  const dialog = node('dialog'); dialog.id = 'courseCatalog';
  dialog.setAttribute('aria-label', 'Browse all courses');
  const closeButton = node('button', 'catalog-close', '×');
  closeButton.type = 'button'; closeButton.setAttribute('aria-label', 'Close course catalog');
  const error = node('p', 'catalog-error'); error.setAttribute('role', 'alert'); error.hidden = true;
  const content = node('div', 'catalog-content');
  dialog.append(closeButton, error, content); document.body.append(dialog);
  let returnFocus = null;
  let selecting = false;

  function close() { if (dialog.open) dialog.close(); }
  async function choose(event, course) {
    // Preserve native link behavior for opening a course in another tab.
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (selecting) return;
    selecting = true; error.hidden = true; content.setAttribute('aria-busy', 'true');
    try { await onSelectCourse(course); close(); }
    catch (failure) { error.textContent = failure.message || String(failure); error.hidden = false; }
    finally { selecting = false; content.removeAttribute('aria-busy'); }
  }
  function open(groups) {
    if (dialog.open) return;
    returnFocus = document.activeElement;
    error.hidden = true; content.replaceChildren();
    // The source identifier distinguishes imported Math Academy courses. Keep
    // the reader's course/next ordering and alphabetical tie breaks intact.
    const catalogGroups = groups.map(group => ({
      ...group,
      courses: group.courses.filter(course => course.mathAcademyId != null),
    })).filter(group => group.courses.length);
    for (const columnGroups of catalogColumns(catalogGroups)) {
      const column = node('div', 'catalog-column');
      content.append(column);
      for (const group of columnGroups) {
        const section = node('section', 'catalog-group');
        const heading = node('h2', 'catalog-group-title', group.title);
        heading.id = `catalog-group-${group.id}`;
        section.setAttribute('aria-labelledby', heading.id);
        const courses = node('ul', 'catalog-courses');
        for (const course of group.courses) {
          const item = node('li');
          const link = node('a', 'catalog-course', course.title);
          link.href = getCourseURL(course);
          if (getCourseId() === course.id) link.setAttribute('aria-current', 'page');
          link.addEventListener('click', event => choose(event, course));
          item.append(link); courses.append(item);
        }
        section.append(heading, courses); column.append(section);
      }
    }
    if (!catalogGroups.length) content.append(node('p', '', 'No Math Academy courses are available yet.'));
    dialog.showModal(); dialog.scrollTop = 0; closeButton.focus({ preventScroll: true });
  }
  closeButton.addEventListener('click', close);
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) close();
  });
  dialog.addEventListener('close', () => { if (returnFocus?.isConnected) returnFocus.focus({ preventScroll: true }); });
  return { open, close };
}
