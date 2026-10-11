# Capture principles

1. Prioritize progress: an unfinished activity can block Math Academy's queue. Never quit or defer activities because of uncertainty or errors; every failure needs a default next action, without asking Jake.
2. Make fault tolerance and resumability part of every phase. Save progress and decisions, recover automatically, and resume without repeating accepted actions. Respect manual stops.
3. Resolve every question within its activity through a competent agent. Record a final judgment even when the question is genuinely unanswerable. Override planned answer sequences when needed to continue.
4. Python runs the workflow and detects exceptions. Agents answer specific questions; Python checks their results before acting.
5. Keep each phase focused. Use explicit records between phases and share common operations. Add complexity only when the capture requires it.
6. Preserve Math Academy's originals and attribution, including errors. Keep our reasoning, corrections, and calculated values distinct. Never turn a guess into a confirmed answer.
7. Follow the schema's entities and terminology. Reuse existing UUIDs when content changes so its history stays together.
8. Keep capture evidence and learner observations under `reference/` for later use. Store original images once by hash in `math/images`, and reference those files from content.
9. Let Database Commit own writes. Preview, commit, and verify; make retries safe. Persist pending database work so a temporary outage cannot block further capture or be mistaken for a successful import.
