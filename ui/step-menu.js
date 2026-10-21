import { readTopicStudyAvailability } from './requests.js';

// Only app-registered content can supply an ID; rendered Markdown cannot spoof it.
const stepIds = new WeakMap();
let menu = null;
let copyButton;
let academyButton;
let notice;
let noticeTimer;
let topicActions;
let currentStep = null;
let returnFocus = null;
let openVersion = 0;

export function stepEntityId(value) {
  if (typeof value === 'number' && !Number.isSafeInteger(value)) return null;
  if (typeof value !== 'number' && typeof value !== 'string') return null;
  const id = String(value);
  return /^[1-9]\d*$/.test(id) ? id : null;
}

export function academyEntityId(value) {
  if (typeof value === 'string' && /^(?:q|e)-[1-9]\d*$/.test(value)) return value;
  return stepEntityId(value);
}

// The legacy function name is retained for callers; value must identify the
// displayed entity, not its authored step or learner-task presentation.
export function attachStepMenu(element, value, mathAcademyId = null, options = {}) {
  const id = stepEntityId(value);
  if (!id) return;
  stepIds.set(element, { kind: 'step', ...options, dbId: id, mathAcademyId: academyEntityId(mathAcademyId) });
  element.dataset.stepDbId = id;
  if (element.tabIndex == null || element.tabIndex < 0) element.tabIndex = 0;
  element.setAttribute('aria-haspopup', 'menu');
  element.setAttribute('aria-expanded', 'false');
  if (!menu) initialize();
}

function stepAt(target) {
  for (let element = target instanceof Element ? target : target?.parentElement; element; element = element.parentElement) {
    if (stepIds.has(element)) return element;
  }
  return null;
}

function close(restoreFocus = false) {
  openVersion++;
  menu.hidden = true;
  currentStep?.setAttribute('aria-expanded', 'false');
  if (restoreFocus && returnFocus?.isConnected) returnFocus.focus({ preventScroll: true });
  currentStep = null;
  returnFocus = null;
}

function open(step, x, y) {
  close();
  const version = openVersion;
  const metadata = stepIds.get(step);
  currentStep = step;
  const host = step.closest?.('dialog[open]') || document.body;
  if (menu.parentElement !== host) host.append(menu);
  if (notice.parentElement !== host) host.append(notice);
  step.setAttribute('aria-expanded', 'true');
  const kind = metadata.kind;
  menu.setAttribute('aria-label', kind[0].toUpperCase() + kind.slice(1) + ' actions' + (metadata.title ? ' for ' + metadata.title : ''));
  copyButton.textContent = `Copy ${kind} :db/id`;
  academyButton.textContent = `Copy ${kind} :ma/id`;
  topicActions.forEach((action, index) => {
    const link = metadata.links?.[index];
    action.hidden = !link;
    if (link) {
      action.textContent = link.label;
      const setAvailability = (available, reason = '') => {
        action.setAttribute('aria-disabled', String(!available));
        action.tabIndex = available ? 0 : -1;
        action.title = reason;
        if (available) action.href = link.href;
        else action.removeAttribute('href');
      };
      setAvailability(!link.studyTopicId, link.studyTopicId ? 'Checking lesson question availability…' : '');
      if (link.studyTopicId) {
        void readTopicStudyAvailability(link.studyTopicId).then(data => {
          if (openVersion === version && !menu.hidden) {
            action.textContent = data.resumable ? 'Resume Study' : link.label;
            setAvailability(data.available, data.reason || '');
          }
        }).catch(error => {
          if (openVersion === version && !menu.hidden) setAvailability(false, error.message);
        });
      }
    }
  });
  returnFocus = step.contains(document.activeElement) ? document.activeElement : step;
  academyButton.hidden = !stepIds.get(step).mathAcademyId;
  menu.hidden = false;
  menu.style.left = '0px'; menu.style.top = '0px';
  const bounds = menu.getBoundingClientRect();
  menu.style.left = `${Math.max(8, Math.min(x, document.documentElement.clientWidth - bounds.width - 8))}px`;
  menu.style.top = `${Math.max(8, Math.min(y, document.documentElement.clientHeight - bounds.height - 8))}px`;
  copyButton.focus({ preventScroll: true });
}

function initialize() {
  menu = document.createElement('div');
  menu.className = 'step-context-menu'; menu.hidden = true;
  menu.setAttribute('role', 'menu'); menu.setAttribute('aria-label', 'Lesson step');
  copyButton = document.createElement('button');
  copyButton.type = 'button'; copyButton.setAttribute('role', 'menuitem');
  copyButton.textContent = 'Copy step :db/id';
  academyButton = document.createElement('button');
  academyButton.type = 'button'; academyButton.setAttribute('role', 'menuitem');
  academyButton.textContent = 'Copy step :ma/id';
  topicActions = Array.from({ length: 3 }, () => {
    const action = document.createElement('a'); action.hidden = true;
    action.setAttribute('role', 'menuitem');
    const blockDisabled = event => {
      if (action.getAttribute('aria-disabled') === 'true') {
        event.preventDefault(); event.stopPropagation(); return true;
      }
      return false;
    };
    action.addEventListener('click', event => { if (!blockDisabled(event)) close(); });
    action.addEventListener('auxclick', blockDisabled);
    return action;
  });
  menu.append(copyButton, academyButton, ...topicActions);
  notice = document.createElement('div');
  notice.className = 'step-copy-notice'; notice.setAttribute('role', 'status');
  notice.setAttribute('aria-atomic', 'true');
  document.body.append(menu, notice);

  const copy = async (key, label) => {
    const metadata = stepIds.get(currentStep);
    const id = metadata?.[key];
    close(true);
    if (!id) return;
    await copyEntityId(id, label, metadata.kind);
  };
  copyButton.addEventListener('click', () => copy('dbId', ':db/id'));
  academyButton.addEventListener('click', () => copy('mathAcademyId', ':ma/id'));

  document.addEventListener('contextmenu', event => {
    if (event.shiftKey) { close(); return; }
    const step = stepAt(event.target);
    if (!step) { close(); return; }
    event.preventDefault(); event.stopPropagation();
    const bounds = step.getBoundingClientRect();
    open(step, event.clientX || bounds.left + 16, event.clientY || Math.max(8, bounds.top) + 16);
  }, true);
  document.addEventListener('keydown', event => {
    if (!menu.hidden) {
      if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); close(true); }
      else if (event.key === 'Tab') close(true);
      else if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
        event.preventDefault();
        const buttons = [copyButton, academyButton, ...topicActions].filter(button => !button.hidden && button.getAttribute('aria-disabled') !== 'true');
        const index = buttons.indexOf(document.activeElement);
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1
          : (index + (event.key === 'ArrowDown' ? 1 : -1) + buttons.length) % buttons.length;
        buttons[next].focus();
      } else if (event.key === ' ' && topicActions.includes(event.target)) {
        event.preventDefault(); event.target.click();
      }
      return;
    }
    if (!(event.key === 'ContextMenu' || event.shiftKey && event.key === 'F10')) return;
    const step = stepAt(event.target);
    if (!step) return;
    event.preventDefault();
    const bounds = step.getBoundingClientRect();
    open(step, bounds.left + 16, Math.max(8, bounds.top) + 16);
  });
  document.addEventListener('pointerdown', event => { if (!menu.contains(event.target)) close(); }, true);
  document.addEventListener('scroll', () => close(), true);
  window.addEventListener('resize', () => close());
  window.addEventListener('blur', () => close());
  for (const event of ['course-academy:profile-changing', 'course-academy:developer-mode-changing']) {
    window.addEventListener(event, () => close());
  }
}

export async function copyEntityId(value, label = ':db/id', kind = '') {
  const id = label === ':db/id' ? stepEntityId(value) : academyEntityId(value);
  if (!id) return;
  const copiedValue = label === ':db/id' ? `${label}=${id}` : id;
  if (!menu) initialize();
  clearTimeout(noticeTimer); notice.textContent = '';
  try {
    await navigator.clipboard.writeText(copiedValue);
    notice.textContent = `Copied ${kind ? kind + ' ' : ''}${label === ':db/id' ? copiedValue : `${label} ${id}`}`;
    noticeTimer = setTimeout(() => { notice.textContent = ''; }, 2500);
  } catch {
    window.prompt(`Clipboard unavailable. Copy this ${label}:`, copiedValue);
  }
}
