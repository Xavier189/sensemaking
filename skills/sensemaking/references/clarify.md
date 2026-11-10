# Clarify — Resolve Consequential Decisions

Use Clarify within the exploration loop when context or impact investigation exposes choices about intent, scope, resulting behavior, constraints, success evidence, terminology, or delegated decisions that admit materially different outcomes. The user need not have identified those choices before the skill starts.

Let established facts and safe inherited defaults resolve agent-owned details. Surface remaining choices whose realistic answers would change the outcome, scope, validation, risk, or external commitments. An easy implementation or detailed requirement can still conceal a consequential assumption. Check relevant relationships before deciding the work has no material forks.

If the starting point contains a visible contradiction, false assumption, or consequential defect, state the finding through Challenge instead of disguising it as a clarification question. Continue Clarify only for the owner decisions that remain after the defect is exposed.

## Evidence gate before a working hypothesis

Before prescribing a frame or asking for a commitment, test whether current-state evidence could materially change the diagnosis or option set. If it could, inspect that evidence first. Keep a dependent frame `candidate` while its evidence is unavailable; do not turn a reported symptom into an assumed cause or target design.

Examples of such evidence include recent change paths, actual wait stages, frequency and severity distributions, current exceptions, usage traces, and authoritative constraints. The list is illustrative: request only evidence with enough information value to change the next decision.

Once the evidence supports a useful question or assessment, return to the discussion. State the relevant finding and its limit, then expose the choice it creates. Further investigation can follow the answer; a complete source tour is not a prerequisite for an owner decision.

## The bar for a question

Ask only when at least two realistic answers would change the frame, deliverable, resulting behavior, validation, or hard-to-reverse decision. If likely answers lead to the same action, do not ask.

When the relevant evidence is not accessible, request the smallest pointer or source that would make it inspectable: a repository path, document, metric view, example record, or responsible source. Do not ask the user to manually reconstruct code paths, file inventories, current metrics, or process facts that an agent could inspect from such a source. Lived experience that is not encoded anywhere may still require user input; label it as experience, not verified current state.

## Build an attackable working hypothesis

Present a concise hypothesis only after there is enough evidence to choose a frame; an established goal needs no repeated discovery interview. Say the change the user is trying to create, not merely the requested mechanism, and a proportionate design with the choices that would change it. Mention a concrete way the current framing fails only when the evidence shows one; do not invent a trap to fill a slot. Tag consequential decisions internally as `confirmed`, `assumed`, or unresolved.

If the request is a solution (“add Redis”, “make a dashboard”, “book a villa”), trace it back to the problem and test whether the solution actually serves it. Do not spend the session tuning parameters on top of an unexamined premise.

Before favoring a solution, identify any unconfirmed goal or trade-off that would reverse the recommendation. Explain options conditionally until that premise is settled. Current behavior is evidence about the starting point, not proof of the behavior the user wants next.

Read [context-and-impact.md](context-and-impact.md) when a claim depends on current behavior, downstream effects, or knowledge the user needs to judge the choices.

Keep the hypothesis compact and easy to reject. A sentence that would survive unchanged in an unrelated task is filler.

## Find the material forks

Stress-test the hypothesis adaptively:

- desired outcome and stakeholder;
- scope and explicit exclusions;
- observable success evidence;
- failure modes and negative requirements;
- dependencies and constraints;
- terminology or domain boundaries;
- long-term fit and reversibility.

These are lenses, not required headings. Surface only what could reroute the result.

Pay attention to familiar words whose meaning may change: “success”, “complete”, “active”, or “available” can refer to different stages or audiences. Explain the observable difference before treating a technical change as behavior-preserving.

## Ask with dependency awareness

Order independent forks by impact; a small batch often helps the user compare their consequences.

Each question should make three things clear:

- what part of the working hypothesis it tests;
- how realistic answers would change the outcome;
- the recommended default and why, when the user has enough basis to evaluate it.

If only the recommendation changes based on another independent answer, keep both in the batch and make the recommendation conditional. If the question's existence or option set changes, defer it to the next turn.

For taste, wording, naming, interaction, or other recognition-based choices, show concrete alternatives the user can react to rather than asking them to invent a description.

## Follow the answer, not a checklist

After each answer set:

1. State only the delta in the shared model.
2. Admit a follow-up only when the new answer exposed it; name the answer and the fork it opened.
3. Update only the decisions the answer addresses, invalidating superseded assumptions and leaving unanswered recommendations provisional.
4. Converge when no material follow-up remains.

A useful dependent follow-up has this shape:

> “You said writes must be visible immediately. That rules out plain TTL, so the remaining decision is invalidate-on-write versus no cache for this query.”

Do not manufacture extra rounds to appear thorough. If new forks grow as fast as they close, the request contains multiple efforts; preserve the fog, propose a split, and clarify only the first meaningful unit.

For example, a user asks: “列表加个导出按钮，帮我看看有没有遗漏。” After checking the existing filters, ask whether export means the current filtered results or all accessible records, explaining how the outputs differ. If they choose filtered results, keep any unanswered format or size-limit recommendation provisional. “继续” continues that discussion; it does not authorize adding the button. If the user already asked to implement after resolving these choices, honor that authorization when the choices are settled.

## Completion

Clarify completes when every material fork is:

- `confirmed` by the user or an authoritative constraint;
- delegated as an `assumed` default the user can see;
- explicitly `deferred`; or
- converted into a research/prototype action because it is not yet answerable.

Completing a clarification pass does not by itself authorize implementation; the readiness check in the main Skill still applies.

Render the shared decisions only when that helps the user or a downstream consumer. Confirmation applies to the decisions, not to a document shape.
