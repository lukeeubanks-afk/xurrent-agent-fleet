# Using the Greg Claims Register
Version: register-usage-v2.0.2
Updated: 2026-10-13

Claims come from the **Greg Claims Register**, the same source Greg validates against
before supplying a number to Danny, Lynn, or a rep. This skill does not keep its own
claim list. One register, one truth, one place Luke edits.

---

## Where it lives

**This file does not record the register's ID. Greg does.**

Resolve it every run:

1. Read Greg's `SKILL.md` at the location the available skills list gives for `greg` (fallbacks: `/mnt/skills/plugins/greg/SKILL.md`, then `/mnt/skills/user/greg/SKILL.md`).
2. Find the block delimited by `<!-- CLAIMS-REGISTER-POINTER -->`.
3. Take `FILE ID` and `VERSION STAMP` from it.
4. Read that one ID with the method the block's `READ WITH` line names.

**Never hardcode the ID into this skill, a config, or a chat.** This is not
hypothetical. Two prior versions pinned a file ID, Luke published a new register, and
every run afterwards read a file that had been deleted from Drive. Greg is the only
place the ID lives, so a register change is a one-file edit.

**Do not list the folder to guess the newest file.** That pattern is retired. The V3.1
title does not match the old `greg-claims-register-v*.md` shape and the version scheme
changed, so name sorting produces the wrong answer or no answer.

If the Greg skill is not on disk, ask Greg directly: "Greg, what is the current claims
register?" If neither resolves, **stop and do not build.** There is no usable offline
cache. The only cached register predates V3.1 and its status labels no longer map to
anything.

---

## The gate: source and flags

V3.1 has no status labels, and does not need them. Every claim in it is published on
that customer's own Xurrent success story page, and the page URL is the locator. The
register's own rule: only claims appearing on each company's own success story page are
recorded, with no supplementation from any other source.

So the question is no longer "what status does this claim carry." It is "what do the
account's own blocks say about how I may use it."

| What the register shows | What you may do |
|---|---|
| A claim bullet under an account | Use as written, attributed to that named customer |
| `EXCLUDED from claims` | Never use. Market assertion or vendor boilerplate, not a customer outcome |
| `Flags: INTERNAL INCONSISTENCY` | Use both figures with both locations, or neither. Never one alone |
| `Flags:` range, or a `~` qualifier | The range or qualifier travels with the number |
| `Flags:` superlative quoted | Only inside the customer's quotation marks, never in Xurrent's voice |
| `Flags:` competitor mention | Only as the customer's own fact of displacement or evaluation |
| `Flags: BRAND FLAG` | That case study PDF is hosted on 4me.com. Never send or link it |
| `Measurement window` stated | It travels with the claim |
| `Case study PDF: Dead link` | Do not link it |

**Presence in the register is not blanket permission.** Read the account's `EXCLUDED`
and `Flags` blocks before you take any claim from it.

### Worked examples from V3.1

- **Pima Community College, 49% MTTR decrease.** Usable. Also carries a user-count
  inconsistency: 31,000 students in the headline against 34,000 users in the meta.
  If you cite population, cite both or cite neither.
- **SEAS annual hours saved.** `INTERNAL INCONSISTENCY`: 4,300 in the summary against
  3,200+ in the body. Do not use 4,300 alone, even though Greg context v2.2.0 carries
  it as canonical. Flagged to Luke and unresolved.
- **GroundTruth, ~33% cost reduction and 5-10 minute MTTA.** Usable. The `~` and the
  range both travel. VictorOps may be named because GroundTruth named it as the tool
  they replaced. PagerDuty may be named only as a tool they evaluated.
- **IndiaMart, 60% MTTR reduction.** Usable. The meta claims 3 years uptime and
  resolution under 44 seconds while the body says two years; that is flagged, so do
  not use the 44-second figure at all. It appears only in page metadata.
- **8x8, 10M status page views.** Usable with the qualifier. The "hidden costs of any
  outage" line is `EXCLUDED`: it is an industry assertion, not an 8x8 outcome.
- **SSP Group self-service adoption 40%.** Usable. The $15-per-request Gartner figure
  and the 21% industry benchmark are both `EXCLUDED`.

If you cannot apply a flag faithfully in the space available, drop the claim. A
restriction half-applied is worse than the claim omitted.

---

## What V3.1 does not cover

The scope is customer success stories, 42 accounts. Nothing else. That means **no
competitor claims, no pricing, no product-level capability figures, no integration
counts, no certifications.** There is no entry to check, and no entry means not usable.

What you can say about capability is structural, not numeric: how the alert path
behaves, what routes where, which channels exist. Naming the specific integrations a
prospect asked about, confirmed against Xurrent's public integration documentation and
marked as needing SE confirmation, serves them better than a count.

V3.1 also did not complete the `enrich_draft` verification pass, because the register
exceeds that tool's 50,000-character input limit. Every figure is reproduced verbatim
from its source page, which makes it source-traceable, not independently verified.

---

## Competitor mentions

The guardrails are absolute. Never "we are better than," never "we are cheaper," never
feature-compare, never state a competitor negative as Xurrent's own opinion, never
claim a fast go-live without a named story.

The one safe form is a **customer's own fact**: "Displaced VictorOps" is something
GroundTruth did, and V3.1 records the named displacement for 19 accounts. Any assertion
about a competitor's pricing or capability is ours, is out of V3.1's scope, and does
not go in a document.

---

## Stamping and traceability

Set `claims_version` in the build config to the `VERSION STAMP` from the Greg pointer
block, currently `greg-claims-register-v3.1.0`. It prints in the footer, so any
artifact in the field traces back to the claim set that produced it. That is what makes
a recall possible if a claim is later withdrawn.

---

## When a rep wants something that is not usable

Say which claim it is and why it is not usable, offer the closest alternative that is,
and log it in `FIELD-LOG.md`. Do not negotiate. The register exists because a rep
quoted two invented figures on a live call in July 2026.
