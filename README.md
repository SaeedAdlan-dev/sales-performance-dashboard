# Project 1: Sales Performance Dashboard (Arrowstack Data Analytics Internship)

**Author:** Saeed Ibrahim
**Document date:** 25 November 2026
**Status:** Final package. Requirements, KPIs and validation were documented after the analysis was done. This is stated openly in the requirements file; it is not a week-1 artifact.

## 1. What this project does

A KPI dashboard for an e-commerce order dataset covering revenue, return rate, net profit and margin, average order value, category and region performance, and monthly trend. It ends with an executive summary and three actions tied to specific numbers.

## 2. Data source

- File: `ecommerce_sales_project.xlsx` (copy included in this folder, unchanged)
- 34,500 order rows, 17 columns, 12 Sep 2023 to 11 Sep 2025
- Origin: not confirmed as real company data. The distributions and the per-order customer attributes suggest a public or synthetic dataset. Results describe this dataset only.

## 3. Scope and limitations (read before judging the dashboard)

| ID | Limitation | Why | What was done instead |
|---|---|---|---|
| L1 | Conversion rate not calculated | No visitor or session data in the source | Documented as out of scope. Order-based KPIs only. |
| L2 | Product-level analysis not done | `product_id` is unique on 24,912 of 34,500 rows | Analysis at category level |
| L3 | Customer age and gender not used as customer attributes | For 6,391 of 7,903 customer IDs, gender varies across orders; for 7,411, age varies | Demographics treated as per-order values and excluded from the dashboard |
| L4 | Returned orders still carry profit in the source | Profit on refunded orders is 61.8k | Headline uses net profit (non-returned orders only). Assumption stated in the KPI dictionary. |
| L5 | Cause of losses is not established | No cost-of-goods or return-reason data | Findings are associations. Cost and return-reason data are the next step. |
| L6 | Two years of data | Seasonality cannot be confirmed | December and January/February patterns are flagged as possible, not proven. |

## 4. Files

| File | Purpose |
|---|---|
| `README.md` | This handoff document |
| `01_requirements_and_acceptance.md` | Stakeholder, scope, success metrics, requirements mapped to evidence |
| `02_decision_log.md` | Every significant decision, the alternative considered, and the reason |
| `03_executive_summary.md` | Findings and three actions with numbers |
| `04_powerbi_build_checklist.md` | Changes made to the Power BI file and how to verify them |
| `05_presentation_outline.md` | Slide-by-slide outline for the final presentation |
| `Project1_KPI_Validation.xlsx` | KPI dictionary, live KPI formulas, category/region/monthly breakdowns, validation log |
| `build_workbook.py` | Script that rebuilds the workbook from the source file |
| `ecommerce_sales_project2.xlsx` | Source data, unchanged |

## 5. How to reproduce

1. Put `ecommerce_sales_project.xlsx` and `build_workbook.py` in the same folder.
2. Install the libraries if needed: `pip install pandas openpyxl`
3. Run `python build_workbook.py`. This creates `Project1_KPI_Validation.xlsx`.
4. Open the workbook. Headline numbers are on `KPI_Summary`, and the checks are on `Validation_Log`. Every check should show PASS, or FLAG with the action recorded.

Expected headline values (for checking your rebuild): gross revenue $5,865,293.05; net revenue $5,476,537.08; net profit $908,213.95; net margin 16.6%; return rate 5.5% of orders.

The Power BI file (`ecommerce_sales_project.pbix`) is built on the same data. The changes made to it are listed in `04_powerbi_build_checklist.md`.

## 6. Evidence index

| Requirement (from the brief) | Evidence |
|---|---|
| KPI definitions | `KPI_Dictionary` sheet; dashboard KPI cards |
| Data validation | `Validation_Log` sheet (19 checks); Power BI validation page |
| Interactive filters | Date, category and region slicers (see Power BI checklist) |
| Trend and segment analysis | `Monthly`, `Category`, `Region` sheets; trend and category visuals |
| Executive summary with actions | `03_executive_summary.md` |
