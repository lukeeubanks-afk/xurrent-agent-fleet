# Intake: reading the transcript
Version: intake-v1.1.0 (2026-09-29)

v1.1.0 adds step 0, the motion, and the ITSM branches that follow from it. Derived
from six ITSM calls: Riverside Health System, Benevis, NC Department of IT, Ligeti
Partners, and two with Barking, Havering and Redbridge NHS Trust.

Transcripts are speech-to-text. They mangle proper nouns. "Xurrent" comes through
as Zorent, Current, or Zurich. "Sera AI" becomes Cera, Sierra, or Sarah. Correct
silently. Never carry an ASR spelling into the document, and never trust a
transcript for the spelling of a person's name.

---

## 0. Settle the motion first

Before anything else, work out whether this is an **ITSM** deal or an **IMR** deal.
It changes how you read the ask, so it cannot wait until the build.

Do not ask cold. Read the transcript, form a view, and offer it back with the one
line of evidence that decided it:

```
Motion: ITSM  (ServiceNow replacement, renewal in June, no alerting discussion)
Options: ITSM · IMR
```

**One primary motion per document.** IMR turns up inside most ITSM calls without
being the deal. At Benevis the rep pitched Zenduty for two minutes and the prospect
declined it on maturity grounds. At Riverside IMR seats were bundled into the quote
while both prospects said their incident management was already strong. At Ligeti it
was floated for P1s and not picked up. None of those are IMR one-pagers.

When both products genuinely matter, as at NC DIT where the rep laid out status
pages, major incidents and traditional ITSM on one call, still pick the primary. The
secondary product gets a mention in the two-column block and nothing more. It does
not get its own flow block or its own coverage table.

Read the motion from what the prospect is trying to replace or add, not from what
the rep pitched.

---

## Pull these three things

### 1. The verbatim ask
What did the prospect say to send? Use their words, not the rep's summary.

> "Definitely alerting. Understanding how your alerting works and how that
> integrates with different major manufacturers."

That sentence is the brief. Everything in the document either serves it or gets cut.

Look for the ask near the end. It usually arrives after the rep asks what to
highlight, and it is usually more specific than the rep realizes.

### 2. The problem in their own words
The prospect will describe their actual problem somewhere, usually in concrete
operational detail rather than in vendor categories.

> "We've got thresholds set up to create alerts that'll send us tickets in
> ServiceNow, which will populate an email, but that's still noise, right?"

That is the best opening line the document will ever have. It is specific, it is
theirs, and it proves someone listened. Mirror it back near the top. It beats
anything written about the platform.

**On ITSM calls the pain is usually quantified, and some of it cannot go in.**

Volumes and time go in by default. Ticket counts, tickets per agent, minutes per
task, hours lost to a manual report. At the NHS trust that is 500 tickets a day
across 14 agents, three minutes per leaver across 135 of them, and two to four
hours a day rebuilding reports in Excel. All usable.

Money and headcount do not go in by default. Contractor cost, salary lines,
efficiency targets, roles the prospect wants to remove. Ask the rep whether it is
safe for this account, and if they say yes, put it in the CONFIRM line at handover
so they own that decision knowingly. The NHS trust is the live example: the deal
runs on £90,000 of temp staff and three first-line roles they want to lose, and one
of the prospects said on the call that they might be putting themselves out of jobs.
That document goes to their director. It can travel further.

**Naming the incumbent.** Name it when the prospect named it, in their framing, and
never as a migration they have not declared. The five ITSM calls sat all over this
range. Benevis called RemedyForce abandoned by both its parents and Ligeti called
their tool half baked, so their own words are fair to reflect. The NHS trust has
procurement engaged and a contract ending in March, so the move is real. Riverside
said the opposite: very happy with ServiceNow, no need to move, looking only because
renewal is due. NC DIT said they are not actively looking to leave, and the document
is going to the director who owns their ServiceNow instance.

Writing "replacing ServiceNow" for either of those last two misstates their position
back to them, in a document their colleague will read. Never assert a comparison
either way. The register holds no competitor claims at all.

### 3. Environment facts
Scale, current tools, timelines, constraints, calendar reality.

- Sites, endpoints, users, alert volume
- Tools named, and whether they are current, being replaced, or already gone
- Contract and go-live timing
- Who else reads the document
- How much of the prospect's time actually exists

**On ITSM calls, the coverage table lists integration targets, not alert sources.**
The systems that matter are the ones the platform has to connect to: HR and payroll
feeds, identity, asset discovery, telephony, reporting. At the NHS trust that is
Lansweeper, IT Health, ESR, OpenScape through Mitel, Entra ID and Qlik. At Benevis
it is iSIMS, ADP Lyric and Active Directory. The incumbent platform is not a row in
this table. It belongs in the mirror, if it belongs anywhere.

**When the transcript names one system or none, ask the rep.** They were on the call
and know the account. Riverside is the case that forces this: the rep asked what
monitoring they run and the prospect did not know, then raised SolarWinds and could
not recall what replaced it. Nothing confirmed, nothing to tabulate. Ask, and if the
rep has nothing either, the section drops out of the document. The build reports that
it was dropped. Do not pad it to reach a row count.

**Who the document is actually for.** ITSM leave-behinds brief someone who was not on
the call far more often than IMR ones do. NC DIT wanted material for two directors
ahead of the next meeting. The NHS trust wanted something to forward to an assistant
director and the ICT director. Benevis wanted the module list and the recording. Size
the ask at the end for the reader, not only for the person you spoke to.

Use these to size the ask at the end. A prospect whose calendar runs six weeks out
and who is dual-rolling between managing and architecting should not be asked for
a working session. Offer an asynchronous first step and earn the meeting.

---

## Sanity checks: cheap, high value

Run these every time.

- **Dates.** Compute the day of week for any date the rep proposed. A follow-up
  offered for a Sunday has happened. Flag it.
- **Company and person spelling.** Confirm against the rep, not the transcript.
- **Tenses matter.** "We moved away from PagerDuty" and "we're moving away from
  ServiceNow" have different implications. Read carefully.
- **Tool status.** If a replacement is already signed and deploying, the document
  should not read as a rip-and-replace pitch. Position around the gap the new tool
  has not closed yet.

---

## What not to put in the document

The prospect forwards this to their directors. Keep out:

- Their internal vendor decisions stated as fact, especially migrations their
  leadership may not have finalized publicly
- Anything the prospect said about being unable to get calendar time
- Anything that reads as though the call was transcribed and mined

Two of these moved in v1.1.0 rather than disappearing. Cost pressure and headcount
are no longer a flat exclusion, because on an ITSM displacement they are frequently
the whole reason the deal exists. They are now opt-in per account: excluded unless
the rep confirms, and named in the CONFIRM line when they go in. Read the ITSM
branch under extraction 2 before using either.

Operational strain stated as workload, meaning volumes and hours, is usable. The
same strain stated as people you plan to remove is not, unless the rep has confirmed
it for that account.

Reflecting their technical environment shows listening. Reflecting their internal
politics reads as surveillance. The line matters.
