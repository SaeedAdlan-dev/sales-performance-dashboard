# 05. Presentation outline (about 10 minutes plus questions)

| Slide | Time | Content | Source |
|---|---|---|---|
| 1. Title and question | 0:30 | Sales Performance Dashboard. The question: where does this business make and lose money, and what should we do first? | README |
| 2. Stakeholder and decision | 0:45 | Who uses the dashboard (category and sales lead), what decision it supports, and the success measures | `01_requirements_and_acceptance.md` section 2 and 4 |
| 3. Data and scope | 1:00 | 34,500 orders over two years. Validation found no blanks or duplicates. Three out-of-scope items named up front: conversion, product level, customer demographics. | `README.md` section 3; `Validation_Log` |
| 4. Headline KPIs | 0:45 | Net revenue $5.48M, net profit $908K, margin 16.6%, return rate 5.5% of orders | `KPI_Summary` sheet; dashboard Overview page |
| 5. The Electronics finding | 1:00 | 56% of revenue, 35% of profit, 10.4% margin, 63% of returned value. Chart: revenue share against profit share by category. | `Category` sheet |
| 6. The small-order finding | 1:00 | Grocery: $20.21 average order, shipping 19% of revenue, 95.5% of orders loss-making. Toys shows the same pattern. | `Category` sheet; dashboard Profit and Returns page |
| 7. Trend and seasonality | 1:00 | Monthly trend with partial months excluded. December 2024 peak. Two years of data, so seasonality is possible, not proven. | `Monthly` sheet |
| 8. Three actions | 1:30 | Electronics margin, small-order shipping policy (test first), Fashion returns. Each has a success measure. | `03_executive_summary.md` section 3 |
| 9. What I could not answer | 1:00 | Conversion, product performance, customer demographics, causes of losses. Why each is missing and what data would fix it. | README section 3 |
| 10. Data-source disclosure and next steps | 0:45 | Source origin, what I changed after validation (net profit, dropped customer page), and the next data requests | `03_executive_summary.md` section 4 |

## Talking points for the hard questions

**"Why did you use net profit instead of the total in the file?"**
Refunded orders still show profit in the source. Keeping that profit would overstate the business. The difference is $61,805, and the decision is in the decision log (D2).

**"Why no conversion rate?"**
The file has only completed orders. There are no visitor or session counts, so any conversion number would be invented. I would need that data before calculating it.

**"Why no product analysis?"**
Almost every order has its own product ID (24,912 IDs for 34,500 orders). A product ranking would be one order per product. Category is the most detailed level the data supports.

**"Why did you drop the customer age and gender page?"**
The same customer ID appears with different genders and ages on different orders. For 6,391 of 7,903 customers, gender changes. Any age or gender result would describe orders, not people.

**"Is this real company data?"**
Not confirmed. The distributions and the per-order customer attributes suggest a public or synthetic dataset. The results describe this dataset only.

**"What would you do with more time?"**
Get cost-of-goods and return-reason data. That turns the Electronics and Grocery findings from associations into a full margin analysis.

## Before you present

- Re-check every number on the slides against `Project1_KPI_Validation.xlsx`.
- Have the README open. Mentors often ask to see the validation log.
- Bring the decision log. The question "why did you choose X" is the most common one in the rubric's viva section.
