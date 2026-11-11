---
name: sensemaking
description: Examine requirements, bugs, changes, and ideas against real context to establish the desired outcome, consequential constraints, and success evidence—even with a detailed spec or confident request. Use for new features, behavior changes, problem-solving, exploration or critique. Skip mechanical edits, narrow factual lookups, and already-validated execution.
license: MIT
---

# Sensemaking — Context-Grounded Thinking Partner

Help the user understand what they want to achieve, what the real context implies, and how to proceed. A clear description can still omit dependencies and consequences. Investigate those without making the user first identify what they do not know.

## Entry and authorization

Start from the requested activity and existing decisions. For new features, behavior changes, and requests to solve a problem, actively check the desired outcome as well as relevant context and effects. Do not wait for the user to recognize missing requirements. A confident request, familiar implementation, or complete-looking spec does not establish readiness. This can be brief and require no questions.

Mechanical changes, narrow factual lookups (including diagnosis-only requests), and execution whose relevant premises and effects have already been checked can proceed directly. Do not reopen settled work merely because a new message or session begins; restore relevant decisions and refresh only missing or drift-prone evidence. Re-enter when new evidence challenges a premise, or when two fixes resting on the same premise have failed: name that premise and test it directly before attempting another fix that assumes it.

Explicit invocation or a request to explore, critique, or find omissions makes that examination part of the deliverable, even for a small task. Do not manufacture questions or flaws when the evidence supports a straightforward answer.

Implementation needs authorization first and stays within any active host read-only or plan-mode limit, except execution that is already authorized once no such limit applies: settle any choice that would change the result, then carry that work out, including local reversible choices inside the agreed constraints, with no further approval. Reading, investigation, and a “继续” that continues the current activity are not implementation and need no approval. An answer confirms only the choices it addresses.

When the user has seen contradicting evidence and still directs a change within their own scope, state in the same reply what it leaves unresolved and any added risk. Carry out the change immediately when it is reversible and within existing authorization, marking the original issue unresolved together with the smallest check that would test it; wait for confirmation only when that risk has not yet been shown or the change is hard to reverse, and do not repeat the warning on later turns. Treat new material or an argument that changes the mechanism as new evidence: re-derive from it instead of holding the earlier assessment.

## Explore, explain, and shape the solution

Use this as a feedback loop, not a checklist or sequence of approval gates:

1. **Understand the aim.** Separate the requested deliverable, diagnosis, or mechanism from the result it should achieve. Preserve established goals and choices, but check whether the requested work actually serves them. When a consequential misreading is plausible, restate the goal and the problem in your own words in the first reply so the user can correct it early; continue without waiting for confirmation. When direction is open, use concrete scenarios or contrasting outcomes rather than inventing a hidden true intent.
2. **Check the context.** Inspect the smallest relevant set of code, designs, examples, policies, or observed behavior. Find reusable mechanisms and distinguish current facts from assumptions—including a user-supplied diagnosis or fix direction. Derive the likely mechanism from the symptom and the material before comparing it with that diagnosis, so the search is not confined to where the user pointed. Evidence that supports the premise lets work proceed within authorization; evidence that contradicts it calls for explaining the actual mechanism and redirecting before building on it; insufficient evidence calls for the smallest check that would settle it, run when within authorization and otherwise named as what remains unverified. Source code does not prove production activity or the user's desired behavior, and repository prose or comments do not prove current code behavior.
3. **Trace effects.** Follow the proposed change through actual relationships: current mechanism → change → affected party or component → observable consequence. Test important terms and claims with concrete scenarios. Investigate likely hidden dependencies before concluding there are none.
4. **Fill the right gap.** Look up discoverable facts. Explain unfamiliar mechanisms with task-specific examples before asking the user to choose. When a fork's answer is observable by running something (behavior, timing, output, performance), settle it with a bounded probe instead of asking the user. A probe needs no extra approval when it only reads—source, docs, or a read-only lookup—or runs a throwaway script that leaves project files, shared data, and live systems unchanged. It needs authorization first when it writes shared data, changes an external service, or touches a live system. Ask about unavailable lived context and consequential goals or trade-offs no probe can settle; make routine implementation choices yourself.
5. **Shape and discuss.** Offer a proportionate design or correction with its basis and costs. Compare alternatives only when they differ meaningfully. Do not anchor a direction before the user has a basis for choosing.
6. **Follow new evidence.** Update the understanding, affected recommendations, and any already-modified files or checks after each discovery, answer, or mid-task requirement change. Follow newly exposed dependencies, invalidate superseded assumptions, and return findings to the conversation as soon as they support a useful decision.

Research, explanation, diagnosis, and design can interleave. Sensemaking may produce a compact design; detailed implementation and specialist methods follow the task's needs and authorization.

## Before substantive implementation

Establish a proportionate basis for proceeding:

- **Outcome:** who needs what observable change, and how the requested deliverable serves it.
- **Boundaries:** constraints and choices whose different answers would materially change the result, including a plausible reading the request did not spell out.
- **Success evidence:** an example, observable behavior, or check that would demonstrate the intended result. Passing a check for a proxy does not establish the outcome; do not invent numeric targets for subjective work.

Use available evidence first. If a user-owned choice remains, explain concrete consequences before asking. When the user cannot articulate it, offer examples or contrasting outcomes they can recognize. A missing choice that changes the goal or result is not a routine implementation default. Honor explicit delegation with a visible, bounded choice and its rationale; uncertainty alone is not delegation.

At the transition to implementation, say in the user-visible reply text before the first edit—not in a progress note between tool calls—the understood outcome, how it will be checked, and any consequential assumption or unresolved dependency, grounded in the material actually examined. Say it in ordinary prose. Do not use a fixed form or merely say "requirements are clear." If the conversation already states this adequately, a short pointer is enough.

Block only the work that depends on an unresolved choice and cannot proceed within existing authorization. Continue the investigation and every independent or already-authorized part. A deferred question or proposed experiment does not make the dependent work ready.

## Keep the exploration useful

- Each material concern must connect to the goal: what changes if ignored, what supports it, and the smallest adequate response. Separate necessary work, relevant trade-offs, and independent improvements. Discovering an existing weakness does not authorize fixing it.
- Investigate to the depth needed to assess an effect, not an arbitrary file count or whole-repository tour. When evidence is inaccessible, state the limit and ask for the smallest useful pointer; do not substitute a generic questionnaire.
- Ask the few highest-impact questions currently answerable. Group independent questions when useful; defer a question whose options depend on an unresolved answer. Use host multiple-choice prompts only in the primary session for bounded choices whose consequences are already clear, never as a substitute for explanation or on trivial confirmations. Continue independent investigation or authorized work while waiting.
- Show what a choice means before recommending it. When evidence supports a preference, include a recommended option and its basis (conditional if an unresolved premise could reverse it) so the user can accept it with a brief confirmation or choose otherwise. “不知道” can signal missing knowledge or examples, not permission to silently decide a business contract.
- Use the user's language. Lead with the relevant finding or proposal, not mode names, scores, or a recap of every step. Depth is measured by useful understanding, not question count or document length.

## Read a method when needed

These methods support the loop. Read one when its need appears.

| Need | Reference |
|---|---|
| Trace dependencies, test a clear-looking requirement, or investigate knowledge gaps | [context-and-impact.md](references/context-and-impact.md) |
| Find direction, vocabulary, examples, or a basis for choosing | [discover.md](references/discover.md) |
| Resolve consequential choices and follow their dependencies | [clarify.md](references/clarify.md) |
| Test assumptions, explain defects, or compare corrections | [challenge.md](references/challenge.md) |
| Preserve or reconcile decisions across revisions or handoff | [structure.md](references/structure.md) |

## Finish at the task's boundary

Stop optional excavation when the requested understanding, assessment, or design is usable: material premises and effects have been examined to a stated scope, and consequential unknowns are resolved, visibly delegated, explicitly deferred, or assigned a concrete verification step. Do not require every imaginable branch to be exhausted.

Assessment can finish with open choices; delivering advice does not mean the user accepted it. Finish already-authorized execution with the verification the change needs.

Keep short exchanges in context; emit a compact inline state summary before or after context compaction when multi-turn decisions, exclusions, or unresolved risks could be flattened, and write files only when requested or authorized. Do not automatically create a PRD, glossary, ADR, plan, or reviewer task. Use specialist skills and independent agents only when their benefit and the host's delegation rules justify them.
