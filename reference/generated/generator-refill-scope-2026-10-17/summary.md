# Automatic refill scope: relevance-v5

The selection-completion gate now applies only to agent authoring, repair,
packaging, and review. Approved registered generators refill automatically
across topics, including prerequisites and downstream topics, while the build
worker finishes current targets and queued topics.

The former restriction on both lanes was an overly broad interpretation of
the requested priority policy. Routine refill does not use a Codex agent, so it
does not consume the author/reviewer capacity reserved for selected work.

The native first pass includes registered hashed-package KPs through the existing
script index and reverse references. It excludes unregistered and legacy sibling
KPs in outside topics before inventory annotation. The broader authoring population
still waits until selected supply is complete. No separate manual catalog query
was used to verify deployment.

Approval checks are unchanged. Missing or stale package/source/difficulty/policy
approval stops refill; an outside review remains deferred until the build scope
opens. Successful prior reviews can reopen automatic refill. Pending publication
recovery and saved draft workspaces remain intact.

Validation: 18 native finder tests, 47 Python finder tests, and 43 worker tests
passed (108 total). The running selected generator pipeline survived service
restart, normal shutdown settings were restored, and the application returned
HTTP 200. The live queue verification reads local metadata only and checks that
outside author/reviewer jobs cannot run while the selection gate is closed.

[Live queue evidence](queue-snapshot.json) · [Deployment](deployment.json) ·
[Current policy](../../../generate/scripts/README.md)
