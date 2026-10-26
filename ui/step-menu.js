import { attachEntityMenu, attachMenuButton, copyText } from './entity-menu.js';

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

export function entityIdActions(value, mathAcademyId, kind = 'entity') {
  const id = stepEntityId(value), academyId = academyEntityId(mathAcademyId);
  return [
    { id: 'copy-db-id', label: `Copy ${kind} :db/id`, hidden: !id, run: () => copyEntityId(id, ':db/id', kind) },
    { id: 'copy-ma-id', label: `Copy ${kind} :ma/id`, hidden: !academyId, run: () => copyEntityId(academyId, ':ma/id', kind) },
  ];
}

// Compatibility adapter: callers identify the displayed content, not its
// authored placement or learner-task presentation unless that is the subject.
export function attachStepMenu(element, value, mathAcademyId = null, options = {}) {
  const id = stepEntityId(value); if (!id) return;
  const kind = options.kind || 'step';
  attachEntityMenu(element, {
    kind, title: options.title,
    actions: context => [...entityIdActions(id, mathAcademyId, kind), ...(options.actions?.(context) || [])],
  });
  element.dataset.stepDbId = id;
  if (options.actionsButton) attachMenuButton(element, `${kind[0].toUpperCase() + kind.slice(1)} actions`);
}

export async function copyEntityId(value, label = ':db/id', kind = '') {
  const id = label === ':db/id' ? stepEntityId(value) : academyEntityId(value);
  if (!id) return;
  const text = label === ':db/id' ? `${label}=${id}` : id;
  await copyText(text, `${kind ? kind + ' ' : ''}${label === ':db/id' ? text : `${label} ${id}`}`);
}
