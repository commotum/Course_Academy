import { attachStepMenu, stepEntityId } from './step-menu.js';

export function attachTopicMenu(element, topic) {
  const id = stepEntityId(topic.id);
  if (!id) return;
  attachStepMenu(element, id, topic.mathAcademyId, {
    kind: 'topic',
    title: topic.title || topic.name || 'Topic',
    links: [
      { label: 'Study now', href: '/learn?topicId=' + encodeURIComponent(id), studyTopicId: id },
      { label: 'Go to topic', href: '/topic?topic=' + encodeURIComponent(topic.uuid || topic.mathAcademyId || id) },
      { label: 'View in graph', href: '/?course=all&topic=' + encodeURIComponent(id) },
    ],
  });
}
