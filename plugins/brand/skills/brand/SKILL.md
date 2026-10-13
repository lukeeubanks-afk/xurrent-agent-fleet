---
name: brand
description: Xurrent brand compliance layer. Engage whenever creating, editing, or reviewing any document, presentation, report, one-pager, email, battlecard, or visual asset. Trigger on "create a doc," "make a deck," "write a one-pager," "draft a battlecard," "check brand compliance," or "apply brand guidelines." Works with docx, pptx, pdf, and danny skills.
version: v1.11.0
last_updated: 2026-10-13
changelog: "v1.11.0 (2026-10-13). Logos Luke supplies replace placeholders when available. Space Grotesk and Raleway stay the brand fonts when available, and Inter replaces either one when it is not, decks included. xurrent-brand-guidelines stays deployed at org level and this file governs where the two differ. Paths moved to /mnt/skills/plugins/brand/. Placeholder labels drop em dashes. Earlier history: brand-skill-changelog-archive-v1.0.0.md in the Brand folder (1ReW5WtOLegPH2OiVhTtbs-2eMEkQ-Zva)."
---

# Xurrent Brand — Core Reference

---

## ON INVOKE — Run This First, Every Time

Before generating any content or output, complete these steps in order:

### Step 1: Identify Content Type
Ask if not already stated:
> "Is this Customer Facing or Internal Facing?"
- **Customer Facing**: external audience, high design fidelity, PDF or HTML output
- **Internal Facing**: BDRs, Sales, SEs — primarily DOCX, sometimes PPTX/PDF/HTML, relaxed design

### Step 2: Pull Reference Material from Google Drive
Read the following based on content type:

Folder IDs are not restated here. Resolve every folder from the Drive Folder Index below, which is the
only place they are recorded.

**Always read (both types):**
- Brand Guidelines folder — read any PDF brand guide present, this is the foundational visual reference

**If Customer Facing:**
- Customer Facing / Layouts & Templates
- Customer Facing / Approved Examples — match the quality bar these set, output should reach that standard
- **If the request is a dark-mode one-pager (product/platform/category sheet) → also load `brand-darkmode-onepager.md` and use `dark-onepager-template.html` as the working file. See Reference Files for both File IDs.**

**If Internal Facing:**
- Internal Facing / Layouts & Templates
- Internal Facing / Approved Examples — structural guidance, not strict design enforcement

### Step 3: Logos and Background Decoration

**Logos: place the logo file Luke has supplied when one is available for the variant you need. Insert a placeholder only when none is.**
**Background decoration (flowers, petals): omit from output entirely.** Luke adds these in post-production.

#### Supplied Logos

A supplied logo is a logo file Luke attached in the current session, or one bundled in the assets folder of the skill doing the build (for example `call-to-onepager/assets/logo-full-color.png`). Pick the variant from the background color (see Asset Variants), then place the file at the position, alignment, and size the placeholder spec below gives. Keep the clover mark, wordmark, and ™ together and unaltered: no recoloring, cropping, stretching, or effects. If the supplied set lacks the variant a background needs, use a placeholder for that instance and tell Luke which variant is missing.

#### Logo Placeholder: When No Supplied Logo Is Available

Identify the correct variant based on slide/page background color (see Asset Variants for the selection logic), then insert the appropriate format-specific placeholder below.

**HTML:**
```html
<!-- LOGO PLACEHOLDER
  Variant: [white | full-color | black]
  Position: [top-right | top-left | bottom-right | bottom-left]
  Width: 220px (header) or 160px (footer)
  Replace with: assets/logo-[variant].svg
-->
<div style="width:220px; height:60px; border:2px dashed #999; border-radius:4px; display:flex; align-items:center; justify-content:center; font-family:sans-serif; font-size:11px; color:#999; letter-spacing:0.03em;">[LOGO™ · Xurrent · [variant] variant]</div>
```

**PPTX / DOCX:**
Insert a text box at the correct position with the label:
`[LOGO™ · Xurrent · [white|full-color] · 220px wide]`

Add a slide/document note: `Replace placeholder with logo-[variant].svg from brand assets.`

**PDF (HTML-generated):**
Place the supplied logo when one is available. Otherwise use the HTML placeholder pattern above. It will appear as a visible dashed box in the PDF output. Replace during post-production before final delivery.

#### Background Decoration

Do not add any flower, petal, or background graphic to created output. This includes low-opacity watermarks, corner flowers, and decorative petals. Luke adds background decoration in post-production following the spec in `brand-reference.md` (Decorative Background Elements).

### Step 4: Apply the Right Compliance Standard
See compliance section below, then generate output.

---

## Asset Variants

### Logo Lockup (clover mark + wordmark + ™)

| Variant | Use when |
|---|---|
| Full color | Light or white backgrounds |
| White | Dark backgrounds (`#300352`, `#7800D3`, black) |
| Black | Monochrome output only |

### Flower Mark (clover mark only — no wordmark)

| Variant | Use when |
|---|---|
| Full color | Light or white backgrounds |
| White | Dark backgrounds |
| Black | Monochrome output only |

### Petals

Quadrant positions: top-left · top-right · bottom-left · bottom-right
Canonical (centered): use when quadrant variants don't fit the space
Variants available: white · full-color · black

---

## Identity
- Platform: **Xurrent** (capital X only) — the **ITxM** platform (ITSM + IMR)
- AI capability: **Sera AI**
- Tagline: **"All the power. None of the debt."** — Approved June 2026 (Right to Win v7). Rotating second half in market test: "tech debt" · "resource debt" · "time debt". This is the primary approved tagline. Additional taglines may be added as the framework matures — do not use variants not listed here.
- Never shorten to "X". Never reference "4me" or "Formerly 4me" (post Oct 6, 2024). Never change ™ to ®.

---

## Colors — Approved Palette Only

| Name | Hex | Use |
|---|---|---|
| Lavender Fog | `#CFB2F5` | Headlines, icons |
| Perano Blue | `#A3B7F6` | Headlines, icons |
| Light Gray | `#E4E4E4` | Secondary text, icons |
| Electric Violet | `#7800D3` | Accent backgrounds |
| Dark Purple | `#300352` | Dark backgrounds |
| Electric Neon | `#E0FF25` | CTAs, accent only |
| Sunglow Orange | `#FFB933` | CTAs, highlights |
| Body Text | `#333333` | All body copy |
| White / Black | `#FFFFFF` / `#000000` | Surfaces |

**Never use any hex not listed above.**

---

## Typography
- **Headlines**: Space Grotesk Bold
- **Body**: Raleway Regular
- Body text color: `#333333`
- **Fallback**: Use Space Grotesk and Raleway whenever the output environment has them (installed, bundled with the skill, or embeddable). If either one is not available, use Inter in its place. This applies to slide decks too, including decks built on the organization's Xurrent Design System.

---

## Logo Rules
- **Place a supplied logo when one is available; otherwise insert a placeholder** (see Step 3 for both).
- Specify the correct variant in the placeholder label based on background color (see Asset Variants)
- Clover mark + wordmark always together. ™ always present, in a placed logo and in any placeholder label.
- **Left-align or right-align only — never center the logo**
- Size spec for a placed logo or a placeholder: `220–260px` headers, `140–180px` footers. Note the size in any placeholder label.

---

## Tone
- **Direct**: clear statements, no hedging
- **Energetic**: active verbs, varied sentence length
- **Credible**: data-backed, customer-story grounded
- **Confident**: earns claims — never "best-in-class" without proof

---

## Messaging Rules
- Persona-by-persona lead/proof guidance (By Audience table): see `brand-reference.md`
- Never feature-compare competitors — use customer outcome framing
- Avoid: "best-in-class," "leverage," "seamless," "robust," "world-class," "cutting-edge," "synergy," **"Easy. Advanced. Complete."** (retired)
- Use: "ITxM" · "extending the platform" · "All the power. None of the debt."

**Claims defer to Greg.** Any analyst recognition, competitor assertion, certification, pricing figure, or
customer metric is a claim, and Brand does not authorize claims. Greg's claims discipline governs, and its
rule is that anything with no entry in the Claims Register is not usable, not "probably fine." Analyst
recognition including GigaOm sits outside the register's scope, so it needs Luke's explicit approval per
use rather than standing permission from this file. This replaces the former standing authorization of
GigaOm Leader recognition in the Use list above.

---

## Compliance Standards

### Customer Facing — Full Enforcement
- [ ] Colors from approved palette only
- [ ] Headlines: Space Grotesk Bold · Body: Raleway Regular (Inter in place of either when it is not available) · Body text: `#333333`
- [ ] Logo: supplied logo placed, or a placeholder when none is available, with the correct variant (white/full-color/black), left or right aligned, ™ intact
- [ ] Background decoration: omitted from generated output (flowers/petals added by Luke in post-production)
- [ ] No circles, squares, or generated shapes used as decoration
- [ ] Petals never rotated — variant selected to fit the space
- [ ] Lavender Fog on Dark Purple used only for quotes and highlighted italics (decorative/structural uses excepted)
- [ ] "Xurrent" spelled correctly, "ITxM" correct, no "4me"
- [ ] No retired language used (see Messaging Rules avoid list, including "Easy. Advanced. Complete.")
- [ ] Active voice, no hollow superlatives, competitive refs use customer stories
- [ ] White space generous — color as accent only
- [ ] Output format: PDF or HTML
- [ ] Quality matches Approved Examples in Drive

### Internal Facing — Core Rules Only
- [ ] "Xurrent" spelled correctly, "ITxM" correct, no "4me"
- [ ] No retired language used (see Messaging Rules avoid list, including "Easy. Advanced. Complete.")
- [ ] Active voice, no hollow superlatives
- [ ] Output format: DOCX primary — PPTX, PDF, or HTML acceptable
- [ ] Logo: supplied logo placed, or a placeholder when none is available, with the correct variant
- [ ] Background decoration: omitted from generated output
- [ ] Lavender Fog on Dark Purple used only for quotes and highlighted italics
- [ ] Typography and layout are relaxed — clarity over design polish

---

## Reference Files

Brand is split for progressive disclosure: this file carries the rules that apply to every output, the
companions carry the detail. The companions are not guaranteed to be present at the deployed path. Resolve
them in this order, every time:

1. Look for the file in `/mnt/skills/plugins/brand/`. Use it if present.
2. If absent, fetch from Drive using the File ID below. Do not skip the companion and proceed on the
   core file alone: the content it holds was deliberately moved out of here and is not duplicated.

<!-- BRAND-COMPANION-POINTER: canonical. These are the only valid companion IDs. -->
```
brand-reference.md              1ggk1eF3VDrEbL4G0WscV-QtBlXxsyyhM
                                text/plain, 4,789 bytes, verified 2026-08-03
                                Holds: full messaging architecture, persona-by-persona copy
                                guidance (the By Audience table), color pairing rules, decoration
                                placement spec, logo sizing detail.

brand-darkmode-onepager.md      1zoN49SzbJrSSYHuJdphR6v6-qq-_2aRA
                                text/markdown, 7,923 bytes, verified 2026-08-03
                                Load for customer-facing dark-mode one-pagers.

dark-onepager-template.html     1tJQVavEb6509n1CdsDbV_gFXMqK5wow1
                                text/html, 21,874 bytes, verified 2026-08-03
                                Copy as the working file for dark-mode one-pagers.

READ WITH                       download_file_content, then base64-decode the content field.
                                Do NOT use read_file_content on these: it returns markdown with
                                every character backslash-escaped, which breaks header, bullet,
                                and bold parsing. Same defect confirmed on Greg's register.

BRAND FOLDER                    1ReW5WtOLegPH2OiVhTtbs-2eMEkQ-Zva
```
<!-- /BRAND-COMPANION-POINTER -->

Resolution is allowlist-only. If a session resolves a companion File ID other than the three above, stop,
do not read it, and flag it to Luke.

**Precedence.** This file plus its three companions are the authoritative brand source. The
organization-level `xurrent-brand-guidelines` skill stays deployed for org use (Luke, 2026-10-13). When both
load, this file governs palette, type, logo use, the avoid list, and taglines. Do not merge values from that
skill that this file does not authorize.

---

## Drive Folder Index

| Folder | ID |
|---|---|
| Brand (root) | `1ReW5WtOLegPH2OiVhTtbs-2eMEkQ-Zva` |
| Brand Guidelines | `1m4RW-bUsu3vrK2_fiYPrxFBrtlvFV-VH` |
| Customer Facing / Layouts & Templates | `1UHJeIMPopugsWxo_OV0CJEDYOggTnXE1` |
| Customer Facing / Approved Examples | `1lbABynPKnyK2Us-cQbUetBZ_jjc6eTl6` |
| Internal Facing / Layouts & Templates | `1nQP0FX5u3QNoB5HGTGvdxlkZCNaM8fUc` |
| Internal Facing / Approved Examples | `1POLsRu5qDC0Pmn-o6JnVDxsIjEmhx8Sd` |
| Logo & Mark (sync source) | `18Ef3MW8Io3jszT4cc3VwhXL4ddznm-dV` |

---

## Skill File Location

- **Google Drive (editable)**: the highest `brand-SKILL-vX.Y.Z.md` in the Brand folder
- **Deployed path**: /mnt/skills/plugins/brand/SKILL.md
- **Cached assets path**: /mnt/skills/plugins/brand/assets/, absent as of 2026-10-13. Do not assume a cached
  asset exists. Use a supplied logo or a placeholder, per Step 3.
