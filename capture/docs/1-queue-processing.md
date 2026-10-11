# 1. Queue Processing

- Open the account's activity queue.
- Read each activity's type, title, Math Academy IDs, links, and progress.
- Expand every activity in the queue, collect its links, and record any details.
- Record assessment question counts, time limits, requirements, retake labels, and any missing or unfamiliar details.
- Recover from read errors where possible and continue with the details available.
- Save the queue in its displayed order, with its HTML, for Activity Selection.

An empty or temporarily unreadable queue keeps the process alive: retry the read with backoff. Recover and resume any saved active activity before considering new work.

Save new queue evidence under `reference/mathacademy/capture/<account>/queue/`. Allow 1 second for queue content to settle, and use the shared minimum 500 ms browser latency and 0.8–2.5 second event waits when navigating and expanding cards. Preserve expansion errors with the details that were readable.

Empty-queue retries start at 30 seconds and double to a 180-second cap, plus up to 5 seconds of jitter. Save the retry count and due time so restarting does not restart the wait. Server rate limits use the account's persisted `Retry-After` cooldown. Manual stops interrupt waits; an already active activity takes precedence over planned queue waits and rests.
