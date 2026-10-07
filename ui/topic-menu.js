// Only topic links registered by the assignment renderer can open this menu.
const topics = new WeakMap();
let menu;
let actions;
let opener;

export function attachTopicMenu(element, topic) {
  const id = String(topic.id ?? '');
  if (!/^[1-9]\d*$/.test(id)) return;
  topics.set(element, {
    title: topic.title || topic.name || 'Topic',
    urls: [
      '/learn?topicId=' + encodeURIComponent(id),
      '/topic?topic=' + encodeURIComponent(topic.uuid || topic.mathAcademyId || id),
      '/?course=all&topic=' + encodeURIComponent(id),
    ],
  });
  element.setAttribute('aria-haspopup', 'menu');
  element.setAttribute('aria-expanded', 'false');
  if (!menu) initialize();
}

function topicLinkAt(target) {
  for (let element = target instanceof Element ? target : target?.parentElement; element; element = element.parentElement) {
    if (topics.has(element)) return element;
  }
  return null;
}

function close(restoreFocus = false) {
  menu.hidden = true;
  if (opener?.isConnected) {
    opener.setAttribute('aria-expanded', 'false');
    if (restoreFocus) opener.focus({ preventScroll: true });
  }
  opener = null;
}

function open(link, x, y) {
  close();
  opener = link;
  const topic = topics.get(link);
  actions.forEach((action, index) => { action.href = topic.urls[index]; });
  menu.setAttribute('aria-label', 'Actions for ' + topic.title);
  link.setAttribute('aria-expanded', 'true');
  menu.hidden = false;
  menu.style.left = '0px'; menu.style.top = '0px';
  const bounds = menu.getBoundingClientRect();
  menu.style.left = `${Math.max(8, Math.min(x, document.documentElement.clientWidth - bounds.width - 8))}px`;
  menu.style.top = `${Math.max(8, Math.min(y, document.documentElement.clientHeight - bounds.height - 8))}px`;
  actions[0].focus({ preventScroll: true });
}

function initialize() {
  menu = document.createElement('div');
  menu.className = 'topic-context-menu'; menu.hidden = true;
  menu.setAttribute('role', 'menu');
  actions = ['Study now', 'Go to topic', 'View in graph'].map(label => {
    const action = document.createElement('a');
    action.textContent = label; action.setAttribute('role', 'menuitem');
    action.addEventListener('click', () => close());
    return action;
  });
  menu.append(...actions); document.body.append(menu);
  document.addEventListener('contextmenu', event => {
    const link = topicLinkAt(event.target);
    if (event.shiftKey || !link) { close(); return; }
    event.preventDefault(); event.stopPropagation();
    const bounds = link.getBoundingClientRect();
    open(link, event.clientX || bounds.left + 16, event.clientY || bounds.bottom + 5);
  }, true);
  document.addEventListener('keydown', event => {
    if (!menu.hidden) {
      if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); close(true); }
      else if (event.key === 'Tab') close(true);
      else if (['ArrowUp', 'ArrowDown', 'Home', 'End'].includes(event.key)) {
        event.preventDefault();
        const index = actions.indexOf(document.activeElement);
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? actions.length - 1
          : (index + (event.key === 'ArrowDown' ? 1 : -1) + actions.length) % actions.length;
        actions[next].focus({ preventScroll: true });
      } else if (event.key === ' ' && actions.includes(event.target)) {
        event.preventDefault(); event.target.click();
      }
      return;
    }
    if (!(event.key === 'ContextMenu' || event.shiftKey && event.key === 'F10')) return;
    const link = topicLinkAt(event.target);
    if (!link) return;
    event.preventDefault();
    const bounds = link.getBoundingClientRect();
    open(link, bounds.left + 16, bounds.bottom + 5);
  });
  document.addEventListener('pointerdown', event => { if (!menu.contains(event.target)) close(); }, true);
  document.addEventListener('scroll', () => close(), true);
  window.addEventListener('resize', () => close());
  window.addEventListener('blur', () => close());
  for (const event of ['course-academy:profile-changing', 'course-academy:developer-mode-changing']) {
    window.addEventListener(event, () => close());
  }
}
