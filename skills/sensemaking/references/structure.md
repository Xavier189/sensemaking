# STRUCTURE — Preserve Shared Understanding

STRUCTURE preserves the evolving understanding across investigation, explanation, dialogue, and design. It prevents a polished final summary from erasing exact decisions, negative requirements, revised assumptions, or unresolved risk.

It does not discover, clarify, or challenge by itself. It records shared decisions already established by those methods, prior conversation, or an authoritative source.

STRUCTURE-only is intentionally narrow: use it to preserve, reconcile, or hand off shared understanding about directions, decisions, assumptions, boundaries, and risks after the thinking is already done. It is not a router for arbitrary rewriting, formatting, file organization, data conversion, summarization, or content transformation; clear requests for those results should be executed directly.

## Information model

Capture only dimensions that matter to the current work:

- **Intent** — the change being sought and why it matters.
- **Stakeholders** — users, decision owners, operators, approvers, and affected parties.
- **Scenarios** — concrete situations, actions, inputs, and expected outcomes.
- **Scope** — included capabilities and explicit exclusions.
- **Requirements** — observable behavior the result must exhibit.
- **Constraints** — limits, dependencies, policies, compatibility, time, or budget.
- **Decisions** — ratified choices and their rationale.
- **Assumptions & evidence** — provisional beliefs, the facts that support or refute them, and their effect on recommendations.
- **Impacts & knowledge gaps** — affected relationships, unresolved mechanisms, and concrete verification steps.
- **Risks & edge cases** — failure modes, negative requirements, and accepted trade-offs.
- **Success evidence** — observable or measurable proof that the result worked.
- **Open items** — unresolved, deferred, or not-yet-specifiable questions.

This is a model, not a form. Omit irrelevant dimensions; never fill headings to make the artifact look complete.

## State semantics

Every consequential item has one current state:

| State | Meaning |
|---|---|
| `candidate` | A possible direction; not yet chosen |
| `confirmed` | Explicitly ratified by the user or authoritative source |
| `assumed` | A visible provisional default chosen by the agent |
| `invalidated` | Superseded or disproved; retained only for traceability |
| `deferred` | Deliberately postponed with consequence/default recorded |
| `risk` | A known concern or accepted trade-off |

Never silently upgrade `candidate` or `assumed` to `confirmed`. When a decision changes, invalidate the old item rather than leaving contradictory versions active.

Record the basis for confirmation: a source can establish current behavior or an authoritative constraint; it does not establish the user's desired change. A user answer confirms only the choices it addresses. Preserve the requested activity and existing authorization alongside decisions when handing off, so agreement on a direction is not mistaken for permission to implement it.

## Incremental capture

For short conversations, maintain the model in working context and render only the final delta.

Use a lightweight decision ledger when any of these is true:

- the conversation spans several rounds;
- a decision has already been revised;
- exact numbers, ordering, negative requirements, or exceptions matter;
- another session or agent will consume the result;
- the user requests persistence or traceability.

Suggested record:

```markdown
- D-03 [confirmed] Retry preserves prior messages and unsent input.
  - Basis: user answer to “failed send behavior”
  - Replaces: D-01 [invalidated] clear composer after any send attempt
  - Consequence: acceptance tests must cover retry without state loss
```

Stable IDs are useful only when downstream artifacts need coverage checks. Do not burden a short conversation with ledger ceremony.

## Renderers

Choose the lightest artifact that serves the user.

### Direction Map

```markdown
## Starting point
## Candidate directions
## Comparison criteria
## Blind spots learned
## Current direction or next experiment
## Still open
```

### Clarity Memo

```markdown
## Intent
## Confirmed decisions
## Boundaries and constraints
## Success evidence
## Assumptions and open items
```

### Challenge Report

```markdown
## What holds up
## Blocking findings
## Material findings
## Recommended revisions
## Accepted risks and owner decisions
```

### Requirements Brief

Use the relevant information-model sections and include state labels wherever a reader might mistake an assumption for a requirement.

### Decision Brief

Use the relevant information-model sections when the work is not naturally expressed as product or software requirements. Preserve the same state semantics without forcing the result into PRD language.

### Handoff Snapshot

Use only when another agent, tool, session, or durable artifact must consume the result:

```markdown
## Ready state
## Carry forward
## Assumptions, deferred items, and accepted risks
## Boundaries
## Success evidence
```

`Ready state` says what can now happen, not which workflow must happen. It may indicate direct delivery, evidence gathering, prototype, design, coordination planning, domain review, or stop. Omit this renderer when the conversation itself is sufficient.

A PRD, spec, ADR, user-story set, or implementation-plan input is a renderer requested by the user or downstream harness. It is not the internal reasoning model and not an automatic sensemaking output.

## Persistence

Do not write files by default. Persist only when the user or an authorized harness asks.

Choose the carrier by the continuity need:

- same agent and session: keep the state in conversation context;
- another agent in the same session: include an inline Handoff Snapshot in the dispatch message;
- another session, a long-running effort, or an audit trail: persist the snapshot in the project's file, issue, or task-state convention.

Rendering a Handoff Snapshot and writing a file are separate actions. Never write a file merely because sensemaking ran. A narrow skill or a subagent is also not a persistence mechanism: a skill supplies reusable capability, an agent performs work, and a durable artifact carries state across time.

When resuming from a persisted snapshot, preserve its decisions and boundaries but verify drift-prone facts and current implementation state before acting.

Example locations for a code repository when no project convention overrides them:

- `docs/discovery/YYYY-MM-DD-<slug>.md`
- `docs/clarity/YYYY-MM-DD-<slug>.md`
- `docs/challenges/YYYY-MM-DD-<slug>.md`

For a notes vault, personal project, operations workspace, or ordinary folder, use its established organization instead of creating a `docs/` hierarchy merely because sensemaking ran.
