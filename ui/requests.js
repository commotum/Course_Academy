// Share concurrent reads, then let HTTP validators check the current database
// response. Mutations and independently abortable route loads stay separate.
const pending = new Map();

export function readRequest(path, options = {}) {
  const settings = { cache: 'no-cache', credentials: 'same-origin', ...options };
  if (settings.signal || settings.headers || settings.body || (settings.method || 'GET').toUpperCase() !== 'GET') return fetch(path, settings);
  const key = JSON.stringify([path, settings]);
  let request = pending.get(key);
  if (!request) {
    request = fetch(path, settings).finally(() => {
      if (pending.get(key) === request) pending.delete(key);
    });
    pending.set(key, request);
  }
  return request.then(response => response.clone());
}

export async function readCurrentLearner() {
  const response = await readRequest('/api/learner');
  const data = await response.json();
  if (!response.ok || !data.learner) throw new Error(data.error || 'Unable to refresh learner settings.');
  return data.learner;
}

export async function readTopicStudyAvailability(topicId) {
  const response = await readRequest('/api/topic-study-availability?topicId=' + encodeURIComponent(topicId));
  const data = await response.json();
  if (!response.ok || typeof data.available !== 'boolean' || String(data.topicId) !== String(topicId)) {
    throw new Error(data.error || 'Unable to check lesson availability. Reopen the menu to try again.');
  }
  return data;
}
