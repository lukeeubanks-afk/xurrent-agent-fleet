# Build: PDF pipeline
Version: build-v1.3.1
Updated: 2026-10-13

## One command

```bash
pip install weasyprint --break-system-packages -q   # first run only
python3 build_pdf.py config.json
```

`build_pdf.py` reads a JSON config, fills `template/onepager.html`, embeds the
bundled logo and fonts, and writes a versioned PDF. Do not hand-write CSS. Do not
rebuild the layout. The template is already brand-compliant and every edit to it
risks reintroducing a failure that was already caught once.

## Config shape

```json
{
  "motion": "imr",
  "account": "Insight Global",
  "department": "Network Operations",
  "focus_kicker": "Xurrent IMR · Incident Management and Response",
  "headline": "Alerting that filters before<br>it wakes anyone up",
  "subhead": "How Xurrent IMR ingests alerts from the network monitoring you already run.",
  "mirror": "Prospect's own description of their current path, in their words.",
  "flow": [{"n":"01 INGEST","t":"Short title","d":"Two sentences."}],
  "stack": [{"tool":"ThousandEyes","how":"Prebuilt integration. ..."}],
  "cols": [{"h":"Section heading","items":[{"lbl":"Lead-in.","d":"Detail."}]}],
  "proof": [{"who":"Savaco","stat":"10K daily alerts","d":"One line."}],
  "next_label": "Next step:",
  "footnote": "Optional small line under the CTA. Leave empty rather than filling it.",
  "next_step": "The ask, sized to the prospect's actual availability.",
  "rep": {"name":"Bryan Obioha","title":"Business Development Representative",
          "email":"bryan.obioha@xurrent.com"},
  "version": "IMR-ALERTING-ONEPAGER-IG-v1.0.0",
  "claims_version": "greg-claims-register-v3.1.0",
  "date": "24 July 2026"
}
```

Keep `flow` at 4, `proof` at 3, `stack` at 5 or 6 rows where the call supports it.
Vary bullet counts between the two columns. Equal counts everywhere reads as
machine-generated.

## `motion` is required

`"itsm"` or `"imr"`. The build exits if it is missing, on purpose: defaulting it is
how every build through v1.2.0 stamped itself IMR no matter what the call was about.

It sets four things you would otherwise have to write by hand. Any of them can be
overridden in the config, and `flow_heading` on an ITSM build usually should be.

| Field | `imr` | `itsm` |
|---|---|---|
| `product_label` | Xurrent IMR | Xurrent |
| `flow_heading` | How the alert path works | How this works |
| `stack_heading` | Your monitoring stack | Systems this connects to |
| `stack_columns` | Tool / How alerts reach IMR | System / How it connects |
| `version` prefix | `IMR` | `ITSM` |

`product_label` also drives the page title and the PDF document properties. Set
`doc_title` only if you need something other than "<product_label> | Prepared for
<account>".

**Name the process in `flow_heading` on ITSM builds.** The default is deliberately
bland because the process differs per deal: joiner, mover and leaver at one account,
change approval at another, moving email traffic to self-service at a third.
Preflight warns if the generic default survives into the output.

## The coverage section disappears when it is empty

`stack` is what the platform connects to. On an ITSM build those are integration
targets, not alert sources, and the incumbent platform is not one of them.

Pass no rows and the whole section is omitted: heading, column headers and table.
Through v1.2.0 the section lived in the template, so an empty `stack` still rendered
a heading above an empty table, which is the defect that surfaced in the field. The
build prints a warning so you know a block left the document.

Do not invent rows to fill it. If the transcript named nothing, ask the rep; if the
rep has nothing either, let it drop.

Config values are escaped before they reach the template. Do not put HTML in them.
Use `next_label` for the bolded lead-in rather than a `<span>` in `next_step`.

`claims_version` is required. Use the `VERSION STAMP` value from the
CLAIMS-REGISTER-POINTER block in `/mnt/skills/plugins/greg/SKILL.md`, currently
`greg-claims-register-v3.1.0`. Do not type it from memory and do not invent a version.
It prints in the footer so any PDF traces back to the claim set that produced it. There
is no cache fallback: if you could not read the register, you should not have built.

`footnote` is optional and empty by default. Nothing is hardcoded into the template,
because the line that used to sit there ("included in every plan, not a paid tier")
turned out to be an INTERNAL claim needing sign-off. Leave it empty unless you have a
verified line to put in it.

## The preflight checks the register, not just the brand

`build_pdf.py` warns on phrases the register quarantines or restricts: integration
counts, the 70% MTTR product claim, the AI-included-at-no-cost line, competitor
overstatements, and go-live claims without a named story. A warning is not proof of
error, but every hit needs a human to confirm the status before the file goes out.

## The page is sized to the content

As of build v1.2.0 there is no pagination. The output is always one continuous
sheet, 8.5in wide, as tall as the copy needs. This replaced fixed Letter pages,
where the three `break-inside:avoid` blocks (the two-column section, the proof
cards, the footer) refused to split and jumped wholesale to a second page, leaving
a third of page one empty.

How it works: the script renders once onto a 400in probe sheet so nothing
paginates, walks the layout tree for the lowest content edge, then re-renders at
that height. The page box itself is skipped during measurement, since it reports
the probe height rather than the content. A 0.02in hairline absorbs sub-pixel
rounding, and if a second page appears anyway the script grows the sheet by 0.25in
and retries up to three times.

Height floors at 11in so a thin build does not come out looking like a receipt.
Typical full builds land between 15in and 17in.

**Screen and email only.** A continuous sheet reads correctly in every PDF viewer
and in email previews. It does not print onto one sheet of Letter. If a print
leave-behind is ever needed, that is a different output, not a tweak to this one.

**Length discipline moved.** The old two-page ceiling was the only thing stopping a
rep generating something enormous. The script now warns above 30in instead. A
warning there means cut content; it does not mean raise the threshold.

## Why fonts are bundled

Space Grotesk Bold and Raleway Regular are mandatory under the brand skill. The
Google Fonts CDN is unreachable from this environment, so a CDN `<link>` silently
falls back to a generic sans-serif and fails brand compliance without erroring.

`assets/fonts/` holds four static instances cut from the upstream variable fonts
(SIL Open Font License, redistribution permitted). The template references them
by absolute path via `@font-face`. Never swap in a CDN link.

## Renderer

WeasyPrint. `wkhtmltopdf` is present on the box but its engine predates CSS Grid
and will collapse the layout to a single vertical column without warning.

## Verify before delivering

```bash
pdftotext -layout out.pdf - | head -40    # text and reading order
pdfinfo out.pdf | grep -i "page size"     # confirm one page, expected height
pdftoppm -png -r 46 out.pdf page          # then view page-1.png
```

Use a low DPI. A 16in sheet at 80dpi produces an image too tall to read in one
view; 46 fits the whole document on screen.

Look at the render. Check: exactly one page, logo top-right and not centered, no
placeholder text surviving into the output, and no unexplained gap in the flow
(a gap now means a real layout fault, not pagination).

## Brand checks the template already handles

Approved palette only · Space Grotesk Bold headlines · Raleway body at #333333 ·
logo right-aligned, never centered · background decoration omitted for
post-production · no generated shapes as decoration · no em dashes · version
stamped in the footer.

## Brand checks it cannot handle

Copy quality. Run the Danny kill list yourself: no leverage, empower, seamless,
robust, world-class, best-in-class, cutting-edge, synergy. No hollow intensifiers.
No em dashes anywhere including the document title. Bold once per section. Active
voice throughout.
