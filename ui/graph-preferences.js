// The server's JSON file is authoritative across devices and URL origins.
export function createGraphPreferences({ apply, onError, fetcher = fetch }) {
  let pending = {}, saving = null, reading = null, revision = 0;

  async function request(changes) {
    const response = await fetcher('/api/graph-preferences', {
      cache: 'no-store', credentials: 'same-origin',
      ...(changes ? { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ changes }) } : {}),
    });
    const value = await response.json();
    if (!response.ok) throw new Error(value.error || 'Could not sync display settings.');
    return value;
  }

  function flush() {
    if (saving) return saving;
    saving = (async () => {
      while (Object.keys(pending).length) {
        const changes = pending; pending = {};
        try {
          const value = await request(changes);
          apply({ ...value, ...pending });
          onError(null);
        } catch (error) {
          pending = { ...changes, ...pending };
          throw error;
        }
      }
    })().finally(() => { saving = null; });
    return saving;
  }

  async function refresh() {
    if (saving || Object.keys(pending).length) return flush();
    if (reading) return reading;
    const started = revision;
    reading = request().then(value => {
      // An older read must not undo a switch clicked while it was in flight.
      if (revision === started) { apply(value); onError(null); }
    }).finally(() => { reading = null; });
    return reading;
  }

  function save(changes) {
    revision++;
    pending = { ...pending, ...changes };
    void flush().catch(onError);
  }

  return { refresh, save };
}
