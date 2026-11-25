# 01. Requirements and acceptance criteria

**Document date:** 25 November 2026
**Note on timing:** This document was written after the analysis and dashboard were complete, so that the project package is consistent and mentor-ready. The stakeholder, scope and success metrics below are stated as the intended goals of the project. They were not written before work started. Earlier drafts did not include them.

## 1. Scenario

Build a KPI dashboard for revenue, return rate, profit, average order value, and category and region performance, with actionable insights.

## 2. Stakeholder and decision

| Item | Definition |
|---|---|
| Primary stakeholder | E-commerce category and sales lead (assumed role; to be confirmed by mentor) |
| Decision supported | Where to focus margin and return-reduction effort across categories, and whether to change the minimum order value or shipping policy in low-margin categories |
| Measurable benefit | Identify categories where revenue and profit diverge, and quantify the revenue at stake from return-rate reduction |
| Frequency of use | Monthly review |

## 3. Scope

**In scope:**
- Revenue, net revenue, returns, net profit and margin, AOV
- Category, region and monthly breakdowns
- Data validation on all 17 source columns
- Interactive filters: date range, category, region
- Executive summary with three actions

**Out of scope (documented limitations):**
- Conversion rate (no session or visitor data; see README L1)
- Product-level performance (product_id is near-unique; see README L2)
- Customer-level age and gender analysis (attributes vary per order; see README L3)
- Causal explanation of losses (no cost or return-reason data; see README L5)

## 4. Success metrics

| # | Metric | Target | Result |
|---|---|---|---|
| M1 | Dashboard totals reconcile to source | Revenue and order counts match the independent Excel calculation to $0.01 | Met (see `KPI_Summary`, `Validation_Log` checks 15 to 18) |
| M2 | Every KPI has a written definition | 100% of headline KPIs in the dictionary | Met (`KPI_Dictionary`, 15 entries including 2 not-calculated items) |
| M3 | Data quality checks run and documented | All checks PASS or FLAG with action recorded | Met (19 checks; 6 FLAG, all with actions) |
| M4 | Filters work across pages | Date, category and region slicers affect every visual on both pages | Met after the changes in `04_powerbi_build_checklist.md` |
| M5 | Insights tied to numbers | Each action cites at least one figure | Met (`03_executive_summary.md`) |

## 5. Requirements mapped to evidence

| Brief requirement | How it was met | Evidence file / location | Status |
|---|---|---|---|
| KPI definitions | Written definitions with formulas and assumptions | `KPI_Dictionary` sheet | Met |
| Data validation | Structural, arithmetic, range, coverage and reconciliation checks | `Validation_Log` sheet | Met |
| Interactive filters | Date, category and region slicers, synced across pages | Power BI, both pages | Met (see checklist) |
| Trend and segment analysis | Monthly trend with partial months excluded; category and region breakdowns | `Monthly`, `Category`, `Region` sheets | Met |
| Executive summary with actions | Three actions with figures | `03_executive_summary.md` | Met |
| Handle edge cases and invalid inputs | Partial months, returned orders, loss-making orders, negative profit values, near-unique product IDs | `Validation_Log` and `02_decision_log.md` | Met |
| Document limitations and next steps | Six limitations and four next steps | `README.md` section 3; `03_executive_summary.md` section 4 | Met |
| Reproducibility | Rebuild script and expected headline values | `build_workbook.py`, `README.md` section 5 | Met |

## 6. Assumptions

1. The source file is a complete record of completed orders for the stated period.
2. `total_amount` is the order value after discount and includes returned orders.
3. `profit_margin` is a dollar amount per order. Its values reach 1,536 and never exceed the order's `total_amount` in any row, which a percentage field could not satisfy. Treating it as a percentage would be wrong.
4. A returned order's profit should not count toward net profit. The source does not adjust for this. This is the main analytical assumption and it is stated in the KPI dictionary.
5. September 2023 (from 12 Sep) and September 2025 (to 11 Sep) are partial months.

## 7. Acceptance criteria (self-assessment)

- [x] Requirements and assumptions are documented.
- [x] A mentor can reproduce the headline numbers from the included script and file.
- [x] Validation checks are documented, with FLAG items disclosed.
- [x] The package is named and organised consistently.
- [x] Key decisions, trade-offs, limitations and next steps are explained in the README and the decision log.
