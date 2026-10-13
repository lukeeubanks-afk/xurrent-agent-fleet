# Build a one-pager from a call
Version: quickstart-v1.1.0 (2026-09-29)

For BDRs, AEs, and SEs. You do not need to know anything about how this works.
Works for ITSM deals and IMR deals.

---

## The short version

Paste your call transcript into the chat and say **"build a one-pager from this
call."** Answer a couple of questions. You get a PDF.

That is it. Everything below is for when something goes sideways.

---

## Getting your transcript

**Do not upload the recording.** Claude cannot listen to audio. A `.wav` file or a
Nooks recording link will not work, and neither will pasting the link.

What you want is the **text** of the call:

- **Nooks:** open the call, find the transcript pane next to the player, select all,
  copy, paste into the chat.
- **Gong:** open the call, Transcript tab, copy.
- **Gemini or Zoom notes:** they usually land in your email. Copy the body.

Paste the whole thing. It does not need cleaning up. Speaker labels, filler words,
misspelled company names are all fine.

---

## What you will be asked

A few things, usually with tappable options and a recommendation already marked. Tap
the recommendation if it looks right.

**ITSM or IMR.** Claude reads the call and proposes one, with the reason. Most ITSM
calls have a couple of minutes of IMR in them without being IMR deals, so if the
prospect spent the call on their service desk and the rep mentioned incident
management in passing, the answer is ITSM. Pick one. The other product still gets a
mention in the document if it came up.

**The focus.** Claude reads the transcript and works out what the prospect actually
asked you to send. It will propose that back to you. If the prospect said "definitely
alerting" at minute nine, the focus is alerting and you just confirm.

**Your details.** Name, title, email. These print in the footer as the person who
prepared it, so they have to be right. Spell your own name; the transcript is
speech-to-text and gets names wrong constantly.

**Anything genuinely ambiguous.** If the call supported two directions equally,
you will get both as options.

Then you get a four-line summary of what is about to be built. **Read it.** If it
says the wrong thing, say so now. Changing it here takes a sentence. Changing it
after takes a rebuild.

---

## What you get

A PDF, one or two pages, brand-compliant, with your name in the footer. Ready to
attach to an email.

You also get up to three lines back:

- **BUILT** the filename
- **CLAIMS** which version of the claims register was used
- **CONFIRM** anything that needs a second pair of eyes before you send

If there is a CONFIRM line, deal with it before sending. It is usually an
integration that needs an SE to sanity-check.

---

## Things that will come up

**"That claim is not usable."**
You asked for a number that either is not in the claims register or is in there with a
status that blocks external use. This is not the skill being
difficult. Every figure in the document has to trace to something we can defend if a
prospect's director pushes back. Two options: use the verified figure it offers
instead, or ping Luke to get the status changed. Do not talk it into using the number
anyway.

**"No prebuilt connector for that tool."**
The prospect named a tool we do not have a documented integration for. The document
will describe an honest ingest path and flag it as needing SE confirmation. Get that
confirmation before you send. Telling a NOC manager an integration exists when it
does not is the fastest way to lose a technical champion.

**It asks for a price.**
It will not answer. Pricing goes to your AE and Deal Desk. Nothing in this document
should carry a number you cannot source.

**"Which systems does this need to connect to?"**
The transcript did not name any, or named one. That happens when the prospect did not
know what they run, or nobody asked. Tell Claude what you know about the account. If
you do not know either, say so and the section comes out of the document. An empty
table under a heading looks worse than no table.

**"Can I use the cost figures they mentioned?"**
Ticket counts and hours go in without asking. Money and headcount do not, because
these documents get forwarded. If the prospect told you they want to cut three roles
or save ninety grand, that is real and it may belong in there, but you decide per
account and it lands in the CONFIRM line so the decision is yours on the record.

**It came out two pages.**
Fine. Prospects who ask for a leave-behind usually say "one or two pages." Two pages
of the technical detail they asked for beats one page with the detail stripped out.

**It got my company or contact name wrong.**
Tell it the correct spelling. Transcripts have no spelling authority.

---

## You review it before it goes out

No sign-off queue. Read it before you send it. It carries your name and it usually
gets forwarded to someone more senior than the person you spoke to.

If there is a CONFIRM line, deal with that first. It is the one thing nobody else is
checking for you now.

---

## When to just ask for help

If you have gone three rounds and the document still is not right, the transcript is
probably missing the thing you need, or the ask is bigger than a one-pager. Grab
Luke. That is a faster path than a fourth round.
