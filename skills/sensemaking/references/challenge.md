# Challenge — Stress-Test Proposals and Decisions

Use Challenge to test assumptions and effects during exploration or design, for requested critique or review, and when evidence exposes a material defect. A defect need not already be visible before examining a clear-looking proposal.

The same starting point may contain unsettled choices, untested claims, and defects revealed by investigation. Use Clarify for the former and Challenge for contradictions, invalid assumptions, untestable claims, or unsafe boundaries. Source, format, domain, lifecycle phase, and size do not determine validity.

Challenge is not a software architecture ceremony. It applies to product ideas, policies, meetings, writing structures, operating procedures, technical designs, and any other consequential proposal.

## Start from the claim, not a questionnaire

Understand the proposal, its intended outcome, and the evidence or constraints it relies on. Read relevant sources before judging. Then lead with concrete findings; do not turn every flaw you can already explain into a question.

For a tentative idea, test its claims while clarifying the premises that would change the recommendation. Do not treat the supplied mechanism as an accepted direction. A finding supported independently of the user's preferences can be stated directly; a preferred repair that depends on an unconfirmed goal or risk tolerance should remain conditional.

Name the behavior a recommendation changes and the evidence supporting its expected benefit. Guarantees require evidence for their preconditions and failure cases. Follow relevant relationships using [context-and-impact.md](context-and-impact.md); assess enough of the current design to discover effects the user has not named.

Use questions only when:

- the finding depends on the user's intent or risk tolerance;
- multiple repairs embody different values;
- an assumption cannot be verified externally;
- the user must accept an external commitment or irreversible consequence.

## Select what could change the conclusion

Test only the claims that could change the conclusion: whether the proposal solves the actual problem or a proxy, whether its parts contradict, what must be true and what supports it, what it excludes and what happens at the limits, how it fails and who notices, who benefits or can undermine it, whether important terms match reality, how anyone would agree it worked, what is costly to undo, and whether a simpler approach differs in consequences.

A failure story, a reversed assumption, a counterexample, a check of an inherited premise, a look at conflicting incentives, or a small simulation is useful only when it exposes something the direct reading missed. Describe what you found.

## Communicate findings

Make each material finding's defect, basis, consequence, and smallest useful correction or experiment clear. Include an owner decision only when a trade-off needs one. These are content requirements, not mandatory headings or a five-part form.

Say what breaks if a finding is ignored, and whether proceeding would contradict the goal, change the outcome, or only be worth remembering.

Connect each proposed correction to the requested outcome. Separate necessary corrections, trade-offs for the user, and independent improvements; do not promote a legacy weakness into mandatory scope without showing why this change depends on fixing it.

Do not mistake stylistic preference for a defect. Do not overstate an inference as fact; label it and say what evidence would resolve it.

## Adversarial pass without adversarial tone

Attack the proposal, not the user. Preserve good choices and explain why they survive. A useful review identifies strengths, not only flaws, because retained strengths constrain the repair.

When proposing alternatives, compare what each optimizes and sacrifices. Do not replace the user's design with the agent's preferred design without exposing the trade-off.

## Completion

Completion depends on what the user requested:

- **Assessment or recommendations:** complete when the relevant claims have been examined and supported findings, consequences, recommendations, and evidence limits have been delivered. Owner choices may remain open and recommendations conditional; user acceptance of each finding is not required. If no material defect is found, state the scope and basis of that conclusion.
- **Resolve or revise the proposal together:** continue until material findings are corrected, rejected with rationale, delegated, explicitly deferred with their consequences, or accepted as risks. A decision outside the agent's authority remains open until its owner resolves or defers it.
- **Review followed by authorized execution:** resolve findings that would make proceeding contradict the goal, violate a hard constraint, or create an unacceptable irreversible risk, and resolve owner choices, then complete the authorized work and its necessary verification. Preserve the other concerns without turning them into additional approval gates.

Delivering an assessment does not mark its recommendations as confirmed or its risks as accepted. Render a report or revised proposal only when it serves the requested deliverable.
