#!/usr/bin/env python3
"""
call-to-onepager · build_pdf.py · v1.3.1 (2026-10-13)

Renders a config JSON into a brand-compliant Xurrent one-pager PDF.

    python3 build_pdf.py config.json [-o output.pdf]

The page is sized to the content: one continuous sheet, no pagination.
Bundled logo and fonts are embedded. No network access required.

v1.3.1: comment update only. The register pointer now lives at the plugin path.

v1.3.0: `motion` ("itsm" or "imr") drives the section headings, the coverage
table's column headers, the page title and the PDF metadata title, which were
hardcoded to IMR alerting through v1.2.0. The coverage section is now emitted
whole and returns empty when there are no rows, so a call that named no systems
no longer renders a labelled empty table.
"""

import argparse
import base64
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
FONTS = ASSETS / "fonts"
TEMPLATE = HERE / "template" / "onepager.html"

# Page geometry. Width is fixed to the template's .page width; height is measured.
PX_PER_IN = 96.0          # WeasyPrint lays out in CSS pixels
PAGE_WIDTH_IN = 8.5       # must match .page width in template/onepager.html
PROBE_HEIGHT_IN = 400     # pass-1 sheet, tall enough that nothing paginates
MIN_HEIGHT_IN = 11.0      # floor, so a short build is not a receipt
WARN_HEIGHT_IN = 30.0     # replaces the old two-page ceiling as the length guard
HAIRLINE_IN = 0.02        # absorbs sub-pixel rounding on the second pass
REFLOW_STEP_IN = 0.25
MAX_REFLOW_RETRIES = 3

# Motion defaults. `motion` in the config selects a column; any key set explicitly in
# the config wins. ITSM's flow heading is deliberately generic because the process
# differs per deal (joiner/mover/leaver, change approval, email to self-service), so
# preflight warns when an ITSM build ships with the placeholder still in place.
MOTIONS = {
    "imr": {
        "product_label": "Xurrent IMR",
        "flow_heading": "How the alert path works",
        "stack_heading": "Your monitoring stack",
        "stack_columns": ["Tool", "How alerts reach IMR"],
        "version_prefix": "IMR",
    },
    "itsm": {
        "product_label": "Xurrent",
        "flow_heading": "How this works",
        "stack_heading": "Systems this connects to",
        "stack_columns": ["System", "How it connects"],
        "version_prefix": "ITSM",
    },
}
ITSM_PLACEHOLDER_HEADING = MOTIONS["itsm"]["flow_heading"]

# Mirror-block signals for money and headcount. Decision of 2026-09-29: volumes and
# time go in by default, money and headcount only when the rep confirms per account,
# and that confirmation has to reach the handover as a CONFIRM line.
MONEY_HEADCOUNT_SIGNALS = [
    "£", "$", "€", "salary", "salaries", "headcount", "head count", "redundan",
    "fte", "vacanc", "temp staff", "agency staff", "cost saving", "budget",
]

# Danny kill list plus brand avoid list. Checked against rendered copy.
BANNED = [
    "leverage", "empower", "seamless", "robust", "world-class", "best-in-class",
    "cutting-edge", "synergy", "transformative", "groundbreaking", "moving the needle",
    "4me", "Zorent", "Cera AI", "Easy. Advanced. Complete.",
]

# Phrases the Greg Claims Register excludes, flags, or does not cover. Presence is a
# warning, not proof of error, but every hit needs a human to confirm it first.
# Aligned to Greg-Claims Register-V3.1 (2026-07-28). Resolve the register through the
# CLAIMS-REGISTER-POINTER block in /mnt/skills/plugins/greg/SKILL.md, never a hardcoded ID.
REGISTER_FLAGS = [
    # Out of V3.1 scope entirely: no entry means not usable.
    ("150+", "integration counts are outside V3.1 scope; no register entry"),
    ("150 integrations", "integration counts are outside V3.1 scope"),
    ("more than 150", "integration counts are outside V3.1 scope"),
    ("70% MTTR", "product-level capability figures are outside V3.1 scope"),
    ("not a paid tier", "pricing and packaging are outside V3.1 scope"),
    ("included in every plan", "pricing and packaging are outside V3.1 scope"),
    ("no additional cost", "pricing and packaging are outside V3.1 scope"),
    ("99.9% availability", "not present in V3.1"),
    ("SOC 2", "certifications are outside V3.1 scope"),
    ("ISO 27001", "certifications are outside V3.1 scope"),
    # Internal inconsistencies: both figures or neither.
    ("4,300 hours", "SEAS: V3.1 shows 4,300 in summary vs 3,200+ in body; cite both or neither"),
    ("4300 hours", "SEAS: V3.1 shows 4,300 in summary vs 3,200+ in body; cite both or neither"),
    ("34,000 users", "Pima: V3.1 shows 31,000 students vs 34,000 users; cite both or neither"),
    ("44 seconds", "IndiaMart: appears only in page metadata, contradicted by body"),
    ("15,000 requests", "NEXE: V3.1 shows 'more than' and 'nearly' 15,000; qualifier required"),
    ("570 external customers", "SETCOR: V3.1 also shows ~600; cite both or neither"),
    # Competitor guardrails.
    ("PagerDuty and VictorOps", "V3.1 records VictorOps as displaced by GroundTruth; PagerDuty only evaluated"),
    ("cheaper", "guardrail: never 'we are cheaper'"),
    ("better than", "guardrail: never 'we are better than'"),
    ("4 week", "no fast go-live claim without a named story from V3.1"),
    ("4-week", "no fast go-live claim without a named story from V3.1"),
    # Excluded market assertions lifted from success story pages.
    ("hidden costs of any outage", "8x8: EXCLUDED, industry assertion not a customer outcome"),
    ("average cost of a support analyst", "SSP: EXCLUDED, third-party Gartner benchmark"),
    ("industry estimates of 21%", "SSP: EXCLUDED, industry benchmark not SSP's own figure"),
    # Brand: 4me.com-hosted case study PDFs must never be linked externally.
    ("storage.4me.com", "BRAND FLAG: 4me.com-hosted PDF; never link externally"),
]

APPROVED_HEX = {
    "#CFB2F5", "#A3B7F6", "#E4E4E4", "#7800D3", "#300352",
    "#E0FF25", "#FFB933", "#333333", "#FFFFFF", "#000000",
}


def esc(s):
    """Escape text but keep the small set of inline tags we allow in config."""
    out = html.escape(str(s), quote=False)
    for tag in ("br", "b", "/b"):
        out = out.replace(f"&lt;{tag}&gt;", f"<{tag}>")
    return out


def block_flow(items):
    return "\n".join(
        f'<div class="step"><div class="n">{esc(i["n"])}</div>'
        f'<div class="t">{esc(i["t"])}</div>'
        f'<div class="d">{esc(i["d"])}</div></div>'
        for i in items
    )


def block_stack_section(rows, heading, columns):
    """Whole coverage section, or empty string when there is nothing to list.

    Returning the section rather than just its rows is what lets a call that named
    no systems drop the block entirely. Through v1.2.0 the <section> lived in the
    template, so an empty `stack` still rendered a heading and a column header row
    with nothing under it.
    """
    if not rows:
        return ""
    col_a, col_b = columns
    out = [f'<tr><th>{esc(col_a)}</th><th>{esc(col_b)}</th></tr>']
    for r in rows:
        how = esc(r["how"])
        # First sentence renders as the status lead-in when it flags a prebuilt path.
        m = re.match(r"^(Prebuilt integration\.|Documented integration\.)(.*)$", how)
        if m:
            how = f'<span class="native">{m.group(1)}</span>{m.group(2)}'
        out.append(f'<tr><td>{esc(r["tool"])}</td><td>{how}</td></tr>')
    body = "\n".join(out)
    return f'  <section>\n    <h2>{esc(heading)}</h2>\n    <table>{body}</table>\n  </section>'


def block_cols(cols):
    parts = []
    for c in cols:
        lis = "\n".join(
            f'<li><span class="lbl">{esc(i["lbl"])}</span> {esc(i["d"])}</li>'
            for i in c["items"]
        )
        parts.append(f'<div><h2>{esc(c["h"])}</h2><ul>{lis}</ul></div>')
    return "\n".join(parts)


def block_proof(cards):
    return "\n".join(
        f'<div class="card"><div class="who">{esc(c["who"])}</div>'
        f'<div class="stat">{esc(c["stat"])}</div>'
        f'<div class="d">{esc(c["d"])}</div></div>'
        for c in cards
    )


def preflight(cfg, rendered_text):
    """Non-fatal warnings. Copy judgment stays with the operator."""
    warn = []
    low = rendered_text.lower()
    for w in BANNED:
        if w.lower() in low:
            warn.append(f"banned term present: {w!r}")
    if "\u2014" in rendered_text:
        warn.append("em dash present (Danny rule: remove)")
    for hexv in set(re.findall(r"#[0-9A-Fa-f]{6}", rendered_text)):
        if hexv.upper() not in APPROVED_HEX:
            warn.append(f"non-palette hex: {hexv}")
    if not cfg.get("version"):
        warn.append("no version string set")
    if not cfg.get("claims_version"):
        warn.append("no claims_version set: the PDF cannot be traced to a claim set")
    for phrase, why in REGISTER_FLAGS:
        if phrase.lower() in low:
            warn.append(f"register check: {phrase!r} present. {why}.")
    for placeholder in ("[title]", "[email]", "TODO", "TKTK", "XXX"):
        if placeholder in rendered_text:
            warn.append(f"placeholder survived into output: {placeholder}")
    flow_n = len(cfg.get("flow", []))
    if flow_n and flow_n != 4:
        warn.append(f"flow has {flow_n} steps; template is built for 4")
    cols = cfg.get("cols", [])
    if len(cols) == 2 and len(cols[0].get("items", [])) == len(cols[1].get("items", [])):
        warn.append("both columns have equal bullet counts (symmetry trap)")

    motion = cfg.get("motion", "")
    defaults = MOTIONS.get(motion, {})
    if motion == "itsm" and cfg.get("flow_heading", ITSM_PLACEHOLDER_HEADING) == \
            ITSM_PLACEHOLDER_HEADING:
        warn.append(
            f"flow_heading is still the generic {ITSM_PLACEHOLDER_HEADING!r}; name the "
            "process this deal is actually about"
        )
    prefix = defaults.get("version_prefix")
    version = cfg.get("version", "")
    if prefix and version and not version.upper().startswith(prefix):
        warn.append(
            f"version {version!r} does not start with {prefix!r} for motion {motion!r}"
        )
    if not cfg.get("stack"):
        warn.append("no coverage rows: the systems section was dropped from the output")
    mirror_low = cfg.get("mirror", "").lower()
    hits = [s for s in MONEY_HEADCOUNT_SIGNALS if s in mirror_low]
    if hits:
        warn.append(
            f"mirror carries money or headcount language ({', '.join(sorted(set(hits)))}). "
            "Confirm with the rep for this account and put it in the CONFIRM line."
        )
    return warn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("-o", "--out")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text())
    tpl = TEMPLATE.read_text()

    # Motion is required. Defaulting it would quietly reinstate the v1.2.0 bug where
    # every build stamped itself IMR regardless of what the call was about.
    motion = str(cfg.get("motion", "")).strip().lower()
    if not motion:
        sys.exit(
            "config has no 'motion'. Set it to 'itsm' or 'imr'; it drives the section "
            "headings, the page title and the PDF metadata."
        )
    if motion not in MOTIONS:
        sys.exit(f"unknown motion {motion!r}; expected one of {sorted(MOTIONS)}")
    defaults = MOTIONS[motion]

    product_label = cfg.get("product_label") or defaults["product_label"]
    stack_columns = cfg.get("stack_columns") or defaults["stack_columns"]
    if len(stack_columns) != 2:
        sys.exit("stack_columns must be exactly two headers")
    account = cfg.get("account", "")
    doc_title = cfg.get("doc_title") or f"{product_label} | Prepared for {account}"

    logo_b64 = base64.b64encode((ASSETS / "logo-full-color.png").read_bytes()).decode()

    subs = {
        "DOC_TITLE": esc(doc_title),
        "FLOW_HEADING": esc(cfg.get("flow_heading") or defaults["flow_heading"]),
        "STACK_SECTION": block_stack_section(
            cfg.get("stack", []),
            cfg.get("stack_heading") or defaults["stack_heading"],
            stack_columns,
        ),
        "LOGO_B64": logo_b64,
        "FONT_DIR": FONTS.as_posix(),
        "ACCOUNT": esc(cfg.get("account", "")),
        "DEPARTMENT": esc(cfg.get("department", "")),
        "DATE": esc(cfg.get("date", "")),
        "KICKER": esc(cfg.get("focus_kicker", "")),
        "HEADLINE": esc(cfg.get("headline", "")),
        "SUBHEAD": esc(cfg.get("subhead", "")),
        "MIRROR": esc(cfg.get("mirror", "")),
        "FLOW": block_flow(cfg.get("flow", [])),
        "COLS": block_cols(cfg.get("cols", [])),
        "PROOF": block_proof(cfg.get("proof", [])),
        "NEXT_LABEL": esc(cfg.get("next_label", "Next step:")),
        "NEXT_STEP": esc(cfg.get("next_step", "")),
        "FOOTNOTE": esc(cfg.get("footnote", "")),
        "REP_NAME": esc(cfg.get("rep", {}).get("name", "")),
        "REP_TITLE": esc(cfg.get("rep", {}).get("title", "")),
        "REP_EMAIL": esc(cfg.get("rep", {}).get("email", "")),
        "VERSION": esc(cfg.get("version", "")),
        "CLAIMS_VERSION": esc(cfg.get("claims_version", "claims-UNVERIFIED")),
    }
    for k, v in subs.items():
        tpl = tpl.replace("{{" + k + "}}", v)

    # PAGE_SIZE is filled per render pass below, not in the main substitution.
    leftover = [k for k in re.findall(r"\{\{([A-Z_]+)\}\}", tpl) if k != "PAGE_SIZE"]
    if leftover:
        sys.exit(f"unfilled template slots: {sorted(set(leftover))}")
    if "{{PAGE_SIZE}}" not in tpl:
        sys.exit("template has no {{PAGE_SIZE}} slot; it predates build v1.2.0")

    out = Path(args.out) if args.out else Path(
        f"Xurrent_{cfg.get('account','Account').replace(' ','')}_"
        f"{cfg.get('version','v0')}.pdf"
    )

    # Preflight on copy only, with the base64 logo stripped out.
    copy_only = re.sub(r"data:image/png;base64,[A-Za-z0-9+/=]+", "", tpl)
    for w in preflight(cfg, copy_only):
        print(f"  WARN  {w}")

    from weasyprint import HTML

    def render(height_in):
        page_size = f"{PAGE_WIDTH_IN}in {height_in}in"
        return HTML(string=tpl.replace("{{PAGE_SIZE}}", page_size),
                    base_url=str(HERE)).render()

    # Pass 1: lay the whole document out on a deliberately tall sheet so nothing
    # paginates, then read where the content actually ends.
    probe = render(PROBE_HEIGHT_IN)
    page_box = probe.pages[0]._page_box
    bottom_px = 0.0
    for box in page_box.descendants():
        # descendants() yields the page box first, and it is the probe sheet,
        # not content. Measuring it would just hand back PROBE_HEIGHT_IN.
        if box is page_box:
            continue
        try:
            edge = box.position_y + box.margin_height()
        except (AttributeError, TypeError):
            continue
        if edge > bottom_px:
            bottom_px = edge
    if bottom_px <= 0:
        sys.exit("could not measure content height; layout tree gave no box extents")

    # Pass 2: re-render at the measured height. HAIRLINE absorbs sub-pixel rounding
    # that would otherwise tip one line onto a second page.
    height_in = max(MIN_HEIGHT_IN, round(bottom_px / PX_PER_IN + HAIRLINE_IN, 2))
    doc = render(height_in)
    for _ in range(MAX_REFLOW_RETRIES):
        if len(doc.pages) == 1:
            break
        height_in = round(height_in + REFLOW_STEP_IN, 2)
        doc = render(height_in)

    doc.write_pdf(
        out,
        metadata={
            "title": f"{product_label}, prepared for {account}",
            "authors": [cfg.get("rep", {}).get("name", "Xurrent")],
            "description": cfg.get("version", ""),
        },
    )
    print(f"  SIZE  {PAGE_WIDTH_IN}in x {height_in}in, {len(doc.pages)} page")
    print(f"  OK    {out}")
    if len(doc.pages) > 1:
        print(f"  WARN  {len(doc.pages)} pages after {MAX_REFLOW_RETRIES} retries. "
              f"Something in the layout is forcing a break.")
    if height_in > WARN_HEIGHT_IN:
        print(f"  WARN  {height_in}in tall. Past about {WARN_HEIGHT_IN}in a leave-behind "
              f"stops being a leave-behind. Cut content rather than shipping it.")


if __name__ == "__main__":
    main()
