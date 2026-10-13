# Gap Log: call-to-onepager

Claims come from the Greg Claims Register. This log records what the field needed
that the register could not supply.

One line per run. This tracks **gaps in what the field can say**, not how anyone
performed. Call quality lives in a separate skill.

Format: `DATE | ACCOUNT | FOCUS | CLAIM REQUESTED BUT UNAVAILABLE | NEEDS SE VERIFICATION`

---

2026-07-24 | Insight Global | Alerting and alert noise | Fleet-average alert-noise and MTTR figures | Cisco Meraki ingest path, no prebuilt connector
2026-07-27 | (register integration) | Alerting | Integration count. 150+ is PENDING-EXTERNAL, so no total can be stated. | Named connectors need confirming against Xurrent public integration docs

## Standing items for enablement

- **RESOLVED 2026-07-27.** The register quarantined the 70% MTTR product claim as
  UNSOURCED and Greg v2.2.0 now says MTTR reduction is customer-specific. The field
  has verified per-customer figures instead: Book My Show 80 to 90%, Chalo 90%,
  Electrum 60%, Cactus Comms 50%. No general figure is needed.
- **Product capability claims are still unverified.** Register Pass 2 has not covered
  integration counts, certifications, or competitor claims. One-pagers currently
  cannot state an integration total. This is the largest remaining gap for technical
  audiences, who ask about integrations constantly.
- **Cisco Meraki** surfaced twice in the first week with no prebuilt connector. Worth
  asking Product whether one is planned.
- **Danny SKILL.md points at a dead Greg file ID** (`1UwrMBGGJ04lvrZ87bn27BY-0NwHJTs-1`).
  Live file is `greg-context-v2.1.1` at `1m-gLmPO9gIfMJnG7qnQng-Ma5_zZZNTS`.

## Reading this log

Two reps asking for the same missing number in a week means one of two things: the
claim exists and is not documented, or the field has found a real gap in what we can
prove. Both are worth acting on. Neither is a rep problem.
2026-08-06 | Ansira (Carlos Arias, SRE Manager) | post-incident RCA and postmortem automation, three variants | MISSING CLAIM: rep asserted 'up to 80% alert noise reduction' on the call; no 80% alert-noise figure exists in register v3.1.0 (nearest published: Chalo 95%, Razorpay unquantified) | UNVERIFIED INTEGRATION: New Relic has no register entry and no published customer story; routed to SE | NOTE: Datadog covered only via Chalo's page, not as a product-level integration claim

2026-09-29 | Barking, Havering and Redbridge NHS Trust (Mark Archer / Angelina, ICT Site Service Managers) | ITSM displacement off Ivanti Neurons v22: password-reset deflection, JML automation, reporting | MISSING CLAIM: UCL cited twice on the calls (9% to 38% self-service, 118,000 additional tickets a year, 7 business functions to 19). UCL is in register v3.1.0 Section C with no published page and all claims removed. CONFLICT: Vitality stated as a nine-week migration on the call; the published page says 90 days from signature. CONFLICT: Sera AI accuracy stated as 97% and adoption as 91%; register has SETCOR above 90% email classification and AXSOS at 60%, no 97% and no adoption figure. Also unavailable: 400-plus reports, 100-plus integrations, 165 languages, 35-day average implementation, 600-plus enterprise customers | UNVERIFIED INTEGRATIONS: ESR, OpenScape via Mitel CTI, Qlik. Lansweeper named as live on two published pages (Claraspital, NAFTA) but not confirmed against public integration docs; an SE asserting it on the call does not clear the bar

## Standing items for enablement

- **ITSM capability claims are the same gap as IMR, and worse.** Across six ITSM calls the field stated at least eight product-level figures with no register entry, because capability figures and integration counts are outside register scope by design. ITSM buyers ask about module inclusion, report counts, and integration totals constantly. Two reps also gave different out-of-the-box percentages on different calls, 85% at Riverside and 75% at Benevis.
- **Pointer conflict between Greg and this skill.** Greg's CLAIMS-REGISTER-POINTER block states that other skills must not resolve the File ID or read the register, and should ask Greg for a validated claim instead. This skill's step 4 and Files table instruct the opposite. Both are current. Needs one of them corrected.
