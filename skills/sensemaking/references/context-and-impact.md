# Context and Impact — Examine What the Request Leaves Unsaid

Use this method when a requirement or proposed solution needs to be understood in its actual environment, including when the user has described it precisely. Aim to discover consequential relationships, not to reopen all decisions.

## Establish a working view

Separate what the user requests, what sources establish, what you provisionally infer, and what is not yet known. Reuse accepted context; do not equate existing behavior with the desired change.

Start at the affected behavior and trace the relevant inputs, callers, consumers, state transitions, and failure paths. For non-code work, use the equivalent people, materials, procedures, incentives, and dependencies. Inspect neighboring boundaries only when they could change the result. Lack of accessible evidence is a limit, not proof of absence.

A useful finding connects:

> Current mechanism → proposed change → affected relationship → observable consequence → evidence or missing premise.

This is a reasoning aid, not a required output table. An impact may justify retaining an existing mechanism or doing less, not just adding work.

## Choose relevant lenses

- **Meaning and lifecycle:** Do words such as accepted, active, complete, or missing mean the same thing to every participant? Distinguish observable stages rather than relabeling them.
- **Inputs and dependencies:** Where does required information come from? What must happen before it is available? Check existing capabilities before proposing new ones.
- **Consumers and commitments:** Who relies on current outputs, timing, errors, or side effects? Would the requested change preserve those expectations?
- **Exceptions and recovery:** Use concrete failure, absence, delay, retry, or partial-success scenarios when relevant. Trace their effects instead of listing generic reliability concerns.
- **Fit and verification:** Does the approach solve the stated problem? What observation would discriminate competing explanations or show the result is correct?

Do not mechanically apply every lens. Be specific about which effects are established, plausible, or unexamined. Code presence, configured enablement, and live behavior are different evidence levels.

When a change's safety rests on one or two facts, name them and push each as far as is cheap along this ladder: asserted → pointed at the exact line or library source → failure path walked step by step → exercised by a script or test against the real code → reproduced in the running system. State where each fact stopped; an asserted fact is unproven.

## Turn gaps into the appropriate next move

- **Discoverable fact:** inspect or research it, including authoritative documentation for unfamiliar behavior.
- **Uncertain mechanism:** state competing hypotheses and choose a small discriminating probe, using the main skill's rule for when a probe needs no extra approval.
- **Missing knowledge:** explain the mechanism using this task's consequences. A comparison or counterexample often gives the user a better basis than more questions.
- **User-owned choice:** describe realistic outcomes and ask for the value, business rule, or commitment that distinguishes them.
- **Routine implementation detail:** use established constraints and reversible defaults; disclose assumptions when they affect interpretation.

Recommendations should expose the premise that would change them. If the user cannot choose, help them understand or propose a reversible experiment; do not treat unfamiliarity as blanket delegation.

## Shape a proportionate design

Include only what explains feasibility or a consequential choice: changed behavior, integration with the current system, relevant data or state flow, failure behavior, and suitable verification. Compare multiple designs only when there is a real trade-off. Keep useful existing decisions and patterns.

For each concern, distinguish:
- necessary for the requested outcome;
- a relevant cost or risk to choose or accept;
- an independent improvement outside the current scope.

The discovery of a cross-cutting weakness does not make system-wide repair a prerequisite. Explain why any proposed scope increase is necessary before treating it as part of the task.

## Examples

A request to add an off-by-default limiter flag is precise. Inspect the current switches and whether enforcing limits is separate from counting activity. An existing enforcement flag may already be the right mechanism. “Off” need not mean removing statistics; show the actual difference before asking the user to choose.

Adding report fields may depend on two events arriving at different times. Check their association, when the report is emitted, and whether missing means unknown or definitely absent. Distinguish a stage that never happened from a missing record. Explain the minimum waiting/fallback behavior needed for correct fields without silently introducing an exactly-once platform redesign.

Replacing direct submission with a queue can change what accepted means and when capacity is occupied. Follow the acknowledgement, registration, retry, and completion paths. Explain supported consequences; do not assume a broker feature or a new architecture automatically fixes them.

A proposal to replace a meeting with written updates needs the same scrutiny: check which parts communicate status and which make decisions or resolve blockers. Preserve the time-saving goal while exploring those consequences, rather than adding a generic meeting policy.
