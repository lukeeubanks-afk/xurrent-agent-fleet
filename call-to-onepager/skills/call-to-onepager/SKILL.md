---
name: call-to-onepager
version: v3.4.1
last_updated: 2026-10-13
owner: Luke Eubanks, Sales Enablement
description: Turns a discovery or cold call transcript into a brand-compliant, account-tailored customer-facing one-pager PDF, for ITSM deals or IMR deals. Use when a BDR, AE, or SE has a call transcript (Nooks, Gong, Gemini, Zoom) and wants a leave-behind built from what the prospect actually asked for. Triggers on "one-pager from this call," "build a leave-behind," "prospect asked me to send something," "turn this transcript into a PDF," or any paste of a call transcript followed by a request for collateral. Produces a versioned PDF built only from approved claims.
changelog: "v3.4.1 (2026-10-13). Step 4 finds the Greg skill from its location in the available skills list, then tries the plugin and user paths, so a change in how plugins are mounted no longer breaks the run. Moved into the xurrent-agent-fleet repository. v3.4.0 (2026-10-13). The skills now deploy under /mnt/skills/plugins/, and v3.3.0 still read Greg at /mnt/skills/user/greg/SKILL.md, a path that no longer exists, so Step 4 would stop every run. Step 4 now reads /mnt/skills/plugins/greg/SKILL.md and falls back to the user path. The register read follows the pointer block's READ WITH line instead of read_file_content, which returns escaped markdown. Same path fix in reference/register-usage.md (v2.0.1), reference/build.md (v1.3.1), DEPLOY.md (v1.2.1), and a build_pdf.py comment (v1.3.1); the template comment (v1.3.1) cites Brand v1.11.0. No code or layout change. v3.3.0 (2026-09-29). ITSM deals are now supported alongside IMR. The template was hardcoded to alerting in five places and produced a mislabelled flow heading and an empty monitoring-stack table on any ITSM call. Section headings, the coverage table's column headers, the page title and the PDF metadata title are now driven by a required `motion` field, and the coverage section drops out of the document when a call named no systems instead of rendering a labelled empty table. intake.md gains step 0 for the motion, an ITSM branch on the problem and environment extractions, and a rule for naming the prospect's incumbent platform. Cost and headcount figures move from a flat exclusion to opt-in per account with a CONFIRM line, because on an ITSM displacement they are frequently the whole reason the deal exists. The per-account approval gate is retired: this is out of pilot and reviewed by the seller. Integration verification is unchanged and still routes to SE. Derived from six ITSM calls across five accounts. v3.2.1 (2026-08-06). Replaced the dead fallback in step 4. It told the model to ask Greg directly when the Greg skill was not on disk, which resolves to nothing, since with no skill there is no Greg. Now stops and names which of the three resolution steps failed. v3.2.0 (2026-08-06). Output is now one continuous sheet sized to the content instead of fixed Letter pages. The @page rule became a template slot and build_pdf.py went to v1.2.0 with a two-pass measure-then-render. Fixed pages were leaving a third of page one empty, because the two-column, proof and footer blocks carry break-inside:avoid and jumped wholesale rather than splitting. Screen and email only: a continuous sheet does not print onto one Letter sheet. The two-page ceiling was the skill's only length guard, so it is replaced by a 30in height warning. Also removed an em dash from the PDF metadata title, which broke the brand rule in document properties. v3.1.0 (2026-07-28). This skill no longer holds a register file ID. It resolves the register through the CLAIMS-REGISTER-POINTER block in the Greg skill, so a register change is a one-file edit in Greg. Register is now Greg-Claims Register-V3.1, which carries no status taxonomy: the seven-status gate is replaced by the source-and-flags gate. Folder-listing discovery retired, since the V3.1 title no longer matches greg-claims-register-v*.md. Cache fallback disabled until a V3.1 cache exists. Fixed Files table reference to reference/claims.md, which never existed. v3.0.0. Claims now load from the Greg Claims Register in the pinned Greg Drive folder, replacing the skill-local claim list. Status taxonomy enforced: only VERIFIED and VERIFIED-RESTRICTED reach a document, and restrictions are applied per claim. Product capability and integration counts removed from available claims because register Pass 2 is not complete. v2.0.0. Live claims folder with cache fallback; coaching removed; conversational Propose-Confirm-Build flow. v1.0.0. Initial release."
---

# Call to One-Pager

Turns a call transcript into a customer-facing PDF that answers what the prospect
actually asked for, using only claims Xurrent can defend.

**This skill does not review the call or coach the rep.** It builds the document.
Call quality is a separate skill.

---

## How to talk to the person using this

Most people running this are not prompt engineers. They want a document, not a
conversation about building a document. So:

**Propose, don't interview.** Never ask an open question you could answer from the
transcript. Read it first, form a recommendation, then offer it with the reasoning
in one line. "The prospect asked specifically about alerting and how it integrates
with their network monitoring, so I'd build it around that. Sound right?" beats
"What should the focus be?"

**Use tappable options, not prose questions.** When you need a choice, use the
interactive option picker if it is available. One question per turn, three at the
absolute most, each with a recommended option marked. Someone on a phone between
calls will tap. They will not type a paragraph.

**Show the plan before you build.** This is the single biggest thing that prevents
wasted work. Before generating anything, put four lines on screen:

```
BUILDING FOR   Insight Global, Network Operations
FOCUS          Alerting and alert noise
LEADING WITH   Their own words: threshold fires, ticket lands in ServiceNow, still noise
PROOF          Savaco 10K alerts, GroundTruth 5-10 min MTTA, Pima College 49% MTTR
```

Then ask for a yes. A person who sees that and says "actually make it about
on-call rotation" just saved you a full build.

**Say what you are doing in plain words.** "Pulling the current approved claims"
not "loading claims-v1.2.0 from the pinned parentId." No jargon: not preflight,
not fixture, not font instancing, not slots.

**Never show them JSON.** You build the config. They never see it, edit it, or
know it exists.

**When something is missing, say what you need and why in one sentence.** "I need
the transcript text rather than the recording, because I can't process audio."
Not an error dump.

---

## The flow

### 1. Get the transcript

**Audio does not work.** Do not ask them to upload the recording. A `.wav` or a
`recording.nooks.in` link produces nothing usable and neither does fetching it.

Ask for the transcript text. In Nooks, open the call and copy the transcript pane
beside the player. Gong, Gemini notes, and Zoom transcripts work the same way.
If they upload audio anyway, say it in one line and ask for the paste. Do not
attempt transcription and do not spend turns on it.

### 2. Read it and form a view

Load `reference/intake.md`. Settle the motion first, ITSM or IMR, because it changes
how you read everything after it. Then pull the things it lists: the verbatim ask,
the prospect's own description of their problem, their environment facts, and their
calendar reality. You are looking for the sentence you will mirror back at the top
of the page. It is almost always the prospect describing their own mess.

One primary motion per document. IMR gets mentioned on most ITSM calls without being
the deal. The secondary product, if it matters at all, gets a line in the two-column
block and no more than that.

### 3. Propose, then confirm

Come back with a recommendation, not a questionnaire. You should already know the
focus and the audience from the transcript. What you genuinely cannot know:

- **Attribution.** Rep name, title, email for the footer. Ask outright; never guess
  a title that will appear on customer-facing collateral.
- **Spelling of names.** Transcripts are speech-to-text and have no spelling
  authority. Confirm the rep's name and the account name.
- **Anything the transcript left ambiguous.** If two focuses are equally supported,
  offer both as options with your pick marked.

Then show the four-line plan and get a yes.

### 4. Load the approved claims

See "Claims" below. Every number and capability statement in the output must come
from that file. If they ask for something that is not on it, do not write it. Say
which claim is missing and route it per the escalation table.

### 5. Build and check

Load `reference/build.md` and run the build script. Do not hand-write CSS or
rebuild the layout.

Then look at the render. Rasterize it at low DPI and view it. A PDF that builds
without error can still carry a placeholder into the output or open a gap where the
layout faulted. Output is a single continuous sheet, so a second page means
something is wrong.

### 6. Hand it over

Give them the file and three lines:

```
BUILT      filename and version
CLAIMS     which register version was used
CONFIRM    anything the seller has to clear before it goes out
```

That is the whole handover. No document critique, no scoring, nothing about how
the call went.

---

## Claims

Claims come from the **Greg Claims Register**, the same source Greg validates against
before any number reaches a rep. This skill keeps no claim list of its own.

**This skill does not hold the register's file ID.** Greg holds it. Hardcoding it here
is what broke the last two versions of this skill: the ID went stale in Drive and every
run read a file that no longer existed.

**Resolve it like this, every run:**

1. Find the Greg skill's `SKILL.md`. Use the location the available skills list gives for `greg`. If it gives none,
   try `/mnt/skills/plugins/greg/SKILL.md`, then `/mnt/skills/user/greg/SKILL.md`. In that file, find the block delimited by
   `<!-- CLAIMS-REGISTER-POINTER -->`. Take `FILE ID` and `VERSION STAMP` from it.
2. Read that one ID with the method the block's `READ WITH` line names. Never keyword-search Drive, never list the
   folder hoping to guess the newest file by name.
3. If the Greg skill is not on disk, or the pointer block is missing, or Drive
   returns nothing for that ID: **stop and do not build.** Say which of the three
   failed. Do not guess an ID, do not fall back to a cached copy, and do not build
   from claims you already know. Greg is provisioned org-wide, so absence means a
   provisioning or Drive-permission fault that a person needs to fix.

Load `reference/register-usage.md` at this step for the gate and how to apply it.

The short version:

1. **Every claim in the register is usable as written, attributed to the named
   customer.** V3.1 has no status labels because every claim in it sits on that
   customer's own published Xurrent success story page.
2. **The `Flags` and `EXCLUDED from claims` blocks are the restriction layer.** Read
   both on every account you take a claim from. `EXCLUDED` means never. Ranges and
   qualifiers travel with the number. Superlatives stay inside the customer's quote.
   `BRAND FLAG` means that case study PDF is hosted on 4me.com; never send the link.
3. **`INTERNAL INCONSISTENCY` means use both figures or neither.** Never one alone.
4. **No cache fallback right now.** The only cache predates V3.1 and its statuses no
   longer map. If Drive is unreachable, **stop and do not build.**
5. **Stamp the version** from the pointer block into `claims_version` so the PDF footer
   traces back to the claim set that produced it.

### What is not available

V3.1's scope is customer success story pages only, by design: no supplementation from
any other source. That means **competitor claims, pricing, product-level capability
figures, integration counts, and certifications have no register entry at all.** No
entry means not usable. Capability statements have to be structural: how the alert path
behaves, what routes where, which channels exist.

This is usually not a loss. Someone asking how alerting fits their stack wants the
mechanism and whether their specific tools are covered, not a total.

V3.1 was also not run through the `enrich_draft` verification pass, because it exceeds
that tool's 50,000-character limit. It is source-traceable, not independently verified.

### Hard stops

Stop and route to a human. Do not generate the document.

| Situation | Route to |
|---|---|
| Claim absent from the register, or present with an unusable status | Enablement (Luke) |
| Integration not confirmed in Xurrent's public integration documentation | Solutions Engineering |
| Any price, discount, or contract term | AE, then Deal Desk |
| Roadmap or unreleased feature | Product (Phil) |
| Any competitor capability, price, or EOL assertion | Enablement. Use a customer-outcome framing instead. |
| Prospect under NDA or in active legal review | AE |

Never assert an integration exists because it is plausible. Name the ingest path,
mark it unverified, and send them to an SE.

### Review

This is out of pilot. **The seller reviews their own one-pager before sending it.**
There is no per-account enablement or SE gate any more.

What did not change is the CONFIRM line. It is now the only thing standing between a
draft and a prospect's director, so it has to be specific and it has to be short.
Two things always belong in it:

- **Any integration not confirmed in Xurrent's public documentation.** An SE saying a
  connector exists on a live call does not clear this. Name the ingest path, mark it
  unverified, send them to an SE. Telling a service desk manager an integration exists
  when it does not is the fastest way to lose a technical champion.
- **Cost or headcount figures in the mirror**, where the rep has confirmed they are
  safe for that account. Put it in writing so they own the call knowingly.

Say the CONFIRM line out loud in the handover rather than assuming they read it.

## Token budget

Target under 25k tokens per one-pager.

- **One Drive call, ever:** read the register at the ID the Greg pointer block gives
  you. Resolving the pointer is a local file read and costs nothing. No folder
  listings, no keyword searches, no browsing the seller library, no reading Greg
  context.
- **No web search** for integrations. The claims file is the source.
- **Load reference files at the step that needs them**, not upfront.
- **Read the transcript once.** Work from your extract after that.
- **Do not paste the draft into chat before building.** Build the PDF, present the
  file. A chat preview of a full one-pager doubles the cost for nothing.

---

## Model selection

Reasoned from task type, not benchmarked. Adjust from field results.

| Situation | Tier | Why |
|---|---|---|
| First one-pager for an account | **Opus** | Steps 2 and 3 are judgment. Reading what the prospect actually asked for, catching that a proposed follow-up date is a Sunday, knowing which proof point fits a 100,000-endpoint NOC. Cheaper tiers execute the format correctly and miss these. |
| Rebuilding with claims and structure already settled | **Sonnet** | Execution. |
| Filename and version hygiene, bulk reformatting | **Haiku** | Mechanical. |

Escalate to Opus when the transcript is long, the prospect is technical, or the
deal has executive visibility. The cost difference is a rounding error against one
wrong number in front of a director.

---

## Files

| File | Load when |
|---|---|
| `reference/intake.md` | Step 2, every run |
| `reference/register-usage.md` | Step 4, every run. How to read and apply the register. |
| Greg's `SKILL.md` (location from the available skills list) | Step 4, every run. Holds the register pointer. Read the block, take the ID. |
| Greg Claims Register in Drive | Step 4, every run. The authoritative claims source. |
| `reference/build.md` | Step 5, every run |
| `template/onepager.html` | Read by the build script, not by you |
| `build_pdf.py`, `assets/` | Step 5 |

---

## Gap log

After each run, append one line to `FIELD-LOG.md`: date, account, focus, any claim
that was requested but not available, any integration that needed SE verification.

This is a gap tracker for enablement, not a record of how anyone performed. It
shows which claims the field keeps needing that do not exist yet, and which
integrations keep surfacing unverified.
