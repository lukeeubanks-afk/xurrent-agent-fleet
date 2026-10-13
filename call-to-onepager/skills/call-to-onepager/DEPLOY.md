# Deploying this to the team
Version: deploy-v1.2.1
Updated: 2026-10-13

## Skill or project? Skill.

Build it as a **standalone skill provisioned to the organization.** Three reasons, in
order of how much they matter:

**1. The PDF pipeline needs files on disk.** Space Grotesk Bold, Raleway, and the logo
have to exist as real files for the renderer to embed them. A skill ships a folder, so
they do. Project knowledge is document context, not a filesystem, and a `.ttf` is
useless there. Without the bundled fonts the output silently falls back to a generic
face and fails brand compliance without raising an error.

**2. Skills require code execution, and this needs it.** That dependency is explicit in
a skill. In a project it is an assumption.

**3. Org provisioning is one upload for the whole team.** An owner adds the zip once in
Organization settings and it appears for everyone, enabled by default, with no
per-person install. Personal skill uploads stay private to the uploader, which is the
wrong shape for a team tool.

Progressive disclosure is a fourth, smaller reason: the skill loads reference files only
at the step that needs them, where project knowledge loads into every conversation.

### When a project would earn its place

Add one **on top of** the skill, not instead of it, if you want a shared workspace where
the team can see each other's builds and find the quickstart without hunting. The
project instructions then do one job: point Claude at the skill. Instructions are at the
bottom of this file.

Be aware of the maintenance cost. Two artifacts drift. If you add a project, the skill
stays the single source of logic and the project holds nothing but a pointer.

---

## Part 1: provision the skill

You need to be an organization **owner** for steps 1 and 2. Xurrent is on a Team or
Enterprise plan, and you already have `xurrent-brand-guidelines` provisioned org-wide,
so this path is already open.

**Step 1. Turn on the prerequisites.**
Organization settings → Skills. Enable both:
- Code execution and file creation
- Skills

Skills do not function without code execution. If it is off, nothing else works.

**Step 2. Upload the skill.**
Organization settings → Skills → Organization skills → **+ Add**.
Select `call-to-onepager-v3.2.0.zip`. The zip must contain the folder with `SKILL.md`
at its root, which this one does.

It provisions immediately to everyone, enabled by default. Members can toggle it off
individually if they want.

**Step 3. Confirm it landed.**
Open a new chat as yourself and ask: *"What skills do you have available?"* You should
see `call-to-onepager`. Then check Customize → Skills and confirm it shows as an
organization skill rather than a personal upload.

**Step 4. Check Drive access, because this is where it will break.**
The skill reads the Greg folder at build time. Every rep who runs it needs the Google
Drive connector enabled **and** read access to folder `1cZqUAN-CcNFToCqYGw_NyQfZjQbnN5Ht`.

Test with one rep before you announce it. Have them paste a short transcript and watch
whether the register loads. There is no cache fallback as of v3.1.0: the only cached
copy predates the current register and its statuses no longer map, so a rep without
Drive access gets a refusal to build rather than a stale document. That is the intended
behaviour. Fix the permission; do not re-enable the cache.

**Step 5. Test end to end yourself.**
Paste a real transcript, run it through, open the PDF. Check the fonts are Space Grotesk
and Raleway rather than a fallback, the logo is top-right, and the footer carries both
version stamps. Output is one continuous sheet sized to the content as of v3.2.0, so a
second page means the layout faulted.

**Step 6. Announce it with the quickstart, not the SKILL.md.**
Send the team `QUICKSTART.md`. It is written for someone between calls who does not care
how it works. `SKILL.md` is for Claude and for you.

---

## Part 2: updating claims later

You do not touch the skill. Publish a new register version into the Greg folder and the
skill picks it up on the next run.

You do not touch this skill. You update **Greg**, and this skill follows.

1. Publish the new register into the Greg folder `1cZqUAN-CcNFToCqYGw_NyQfZjQbnN5Ht`.
   Keep it as `text/markdown`. Do not upload it as a Google Doc: conversion escapes
   every markdown character and the parser fails on it.
2. Open `/mnt/skills/plugins/greg/SKILL.md` and edit the `CLAIMS-REGISTER-POINTER` block:
   new title, new `FILE ID`, new `VERSION STAMP`, new byte count and date.
3. Bump Greg's `version` and add a changelog line.
4. Move the old register out of the folder or suffix it `OBSOLETE`.

That is the whole update. The pointer lives in exactly one file, so this skill,
Danny, Lynn, and anything else built later all pick up the change with no edits.

**If the new register changes shape, not just content**, the gate needs revisiting too.
V3.1 dropped the seven-status taxonomy, so `reference/register-usage.md` had to change
with it. A register that reintroduces status labels, or that widens scope past customer
success stories, is a shape change. Content-only updates are not.

The only reason to re-upload this skill is a change to the template, the build script,
the bundled assets, or the gate.

---

## Part 3: optional project wrapper

Only if you want the shared workspace. Create a project, share it with the team, and
paste this into the custom instructions field verbatim. Nothing else goes in that field.

```
This project is for building customer-facing one-pagers from sales call transcripts.

Use the call-to-onepager skill for every request in this project. Follow it exactly.
Do not build a one-pager without it, and do not substitute your own judgement for the
claims register it reads.

When someone starts a conversation here, assume they have a call transcript and want a
one-pager. If they have not pasted one, ask for the transcript text. Do not accept audio
files or recording links; you cannot process audio.

Before building anything, show the four-line plan the skill describes and get a yes.

Every number in the finished document must come from the Greg Claims Register, and the
register is resolved through the pointer block in the Greg skill, never from a
hardcoded ID. Read each account's EXCLUDED and Flags blocks before using its claims. If
someone asks for a figure that is not usable, say why, offer the closest alternative
that is, and route them to Luke. Do not talk yourself into using it.

Keep responses short. The people in this project are between calls.
```

**Project knowledge:** add `QUICKSTART.md` and nothing else. Do not add the fonts, the
logo, the template, or the register. The fonts and logo cannot work as project knowledge
and the register must stay live in Drive rather than frozen as an uploaded copy.

---

## What is in the skill

| File | What it is for |
|---|---|
| `SKILL.md` | The instructions Claude follows. Start here if you are editing behaviour. |
| `QUICKSTART.md` | The team-facing guide. This is what you send reps. |
| `DEPLOY.md` | This file. |
| `FIELD-LOG.md` | Gap log: claims the field needed that were not usable. |
| `reference/intake.md` | How to read a transcript. Loaded at step 2. |
| `reference/register-usage.md` | How to resolve, load, and apply the claims register. Step 4. |
| `reference/build.md` | The PDF pipeline and its constraints. Step 5. |
| `template/onepager.html` | The layout. Brand-compliant. Do not rewrite it. |
| `build_pdf.py` | Renders config to PDF, with a compliance preflight. |
| `assets/logo-full-color.png` | The logo, embedded at build time. |
| `assets/fonts/*.ttf` | Space Grotesk Bold and Medium, Raleway Regular and SemiBold. |
| `cache/register-cache-v1.1.0-SUPERSEDED.md` | Historical only. Predates V3.1 and is not a usable fallback. |
| `examples-alerting.json` | A worked config, used as a regression test. |
