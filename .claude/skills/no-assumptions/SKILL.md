---
name: no-assumptions
description: Enforces exact-scope execution on any code change, fix, or feature request. Use this skill whenever the user asks to change, fix, add, remove, refactor, or check anything in a codebase — including small or obvious-seeming requests. It prevents three failure modes: silently filling spec gaps with guesses, doing extra unrequested work that tangles the codebase, and reporting success when the requested change did not actually land. Trigger it even when the task looks trivial, and especially when the user says "taxmin?", "3 savol", "faqat shuni qil", "nima o'zgardi", "KOD YOZMA", or expresses frustration that a previous change had no effect.
---

# No Assumptions — Exact Scope Execution

## Why this exists

Three failure modes compound into weeks of lost work. Each feels harmless in the moment:

1. **Silent gap-filling.** The spec has a hole. You fill it with something reasonable and keep going. The user never learns a decision was made on their behalf — until it surfaces three versions later as a bug they have to debug themselves.

2. **Scope creep.** While in the file you notice something else worth fixing, so you fix it. Now the diff contains changes nobody asked for. The codebase gets tangled, and a later bug cannot be traced back to any request.

3. **Phantom completion.** You do a lot of adjacent work and report success, but the one concrete thing the user asked for did not change. This is the worst one, because it looks like progress.

The user's time then goes to undoing these instead of building. Slower and correct beats fast and tangled.

---

## Before writing any code

### 1. The one-line diff test

Write the request as one concrete sentence: `<what> currently <X> → will become <Y>`.

If you cannot write that sentence without inventing a detail, you do not understand the request. Stop and ask. Do not start coding and figure it out on the way.

- Good: "kassa panel currently renders 2 columns → will render 3 columns × 2 rows, always, regardless of value"
- Not good: "improve the kassa panel" — no concrete before/after exists. Ask first.

### 2. The assumption block (Taxmin bloki)

Output this before any code, every time — even when the user did not ask for it:

```
TAXMIN BLOKI

1. ANIQ BILMAYOTGAN JOYLARIM
   - <gaps in the spec; decisions not explicitly stated>

2. TAXMINLARIM
   - [MEN] <if I fill that gap, here is how — this decision came from me>
   - [USER] <this one was explicitly stated by the user>

3. TA'SIR QILADIGAN JOYLAR
   - <grep result: every place that reads this field / function / screen>
```

Rules for the block:

- **Part 1 must never be left empty out of convenience.** If it is genuinely empty, say so explicitly rather than omitting the section.
- **Part 2 must label each line `[USER]` or `[MEN]`.** Anything marked `[MEN]` is a decision you made — the user gets to overrule it before it becomes code. Unlabeled assumptions are how a user's project silently becomes someone else's design.
- **Part 3 is a grep result, not a recollection.** Search for the field name, then search for every function that touches it. Knowing the variable name is not enough — find every read site, including string keys, receipt labels, PDF templates, and save/serialize functions.

Then wait. "ha" / "to'g'ri" / "shunaqa qil" is the go signal. Silence is not.

---

## While writing

**Change only what the one-line diff says.** Nothing else.

Forbidden without being asked:

- Renaming variables or functions you happened to touch
- Refactoring "while I'm in here"
- Adding error handling, validation, or defensive checks nobody requested
- Adding features that seem like natural companions to the requested one
- Reformatting, reordering, or tidying unrelated lines
- Copying an approach from an older version of the file because it looks similar

That last one deserves emphasis: **old code is evidence, not documentation.** A previous version's decision solved a previous problem under previous constraints. Reusing existing *code* (calling a function that already works) is good. Inheriting an old *decision* is not. Implement what was specified now.

**Line budget.** Before starting, estimate roughly how many lines will change. If the actual diff exceeds about twice that estimate, stop and report before continuing. A ballooning diff means the scope drifted.

**One change per turn.** Do not bundle a second improvement into the same edit, however small it seems.

---

## After writing — verification

A change is not done because you wrote it. It is done when you can prove it landed.

Output this before claiming completion:

```
TEKSHIRUV
So'ralgan: <the one-line diff>
Qilingan:  <what actually changed>
Dalil:     <file>:<line>   <before>  →  <after>
Grep:      <field/function> o'qiladigan joylar: <list>
           — hammasi yangilandi / <which were not, and why>
```

If you cannot fill the `Dalil` line with a real line number and a real before/after, the change did not happen. Say that plainly instead of reporting success.

Common ways phantom completion happens — check each before reporting done:

- The edit went to the wrong file, or to a copy of the file
- A second code path still reads the old value; the grep missed it
- The change sits behind a condition that never fires
- You described the change in prose but never actually applied the edit
- The file was written but the syntax check was never run

---

## When the user pushes back

If the user says the change did not work, or that something they never asked for appeared:

- Do not defend the previous output.
- Do not immediately write a second fix on top of the first.
- Re-read what was actually asked. Re-read what was actually written. Report the gap between them.
- Then propose one targeted fix and wait for approval.

Layering unverified fixes onto unverified fixes is how a codebase stops being traceable.

---

## Logic vs cosmetic

**Treat as logic — always surface the Taxmin bloki and wait:**
calculations, data fields, control flow, storage schema, sync, state, money, anything that persists.

**Treat as cosmetic — may proceed, but ask in one line first and report what was touched:**
colors, text strings, spacing, typos, label wording.

The one-line ask: "Bu vizual o'zgarish, mockupsiz yozaman — rozimisan?"

**When unsure which side a change falls on, treat it as logic.** The cost of asking is one message. The cost of a wrong silent change is a debugging session.

---

## Trigger phrases

| Phrase | Required response |
|---|---|
| `taxmin?` / `3 savol` | Output the Taxmin bloki immediately, before anything else |
| `faqat shuni qil` | Exact scope, zero extras, no companions |
| `nima o'zgardi?` | Output the TEKSHIRUV block with real line numbers |
| `KOD YOZMA` | Analysis or mockup only. Do not edit any file. |
| `mockup qil` | Visual before/after proposal as a separate file. No code. |
| `chigallashib ketdi` | Stop. List every change made since the last confirmed-good state, and which ones were not requested. |
