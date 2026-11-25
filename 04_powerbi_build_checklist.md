# 04. Power BI build checklist

Changes to make in `ecommerce_sales_project2.pbix` so it matches this package. Each step ends with a test value you can check on screen. Do these in order.

## Step 1: Add the net measures

Add these in the `ecommerce_sales_project2` table (New measure), or in a `_Measures` table.

```dax
Net Revenue =
CALCULATE ( SUM ( ecommerce_sales_project2[total_amount] ),
            ecommerce_sales_project2[returned] = "No" )

Returned Revenue =
CALCULATE ( SUM ( ecommerce_sales_project2[total_amount] ),
            ecommerce_sales_project2[returned] = "Yes" )

Net Profit =
CALCULATE ( SUM ( ecommerce_sales_project2[profit_margin] ),
            ecommerce_sales_project2[returned] = "No" )

Net Profit Margin % = DIVIDE ( [Net Profit], [Net Revenue] )

Return Rate (orders) =
DIVIDE ( CALCULATE ( COUNTROWS ( ecommerce_sales_project2 ),
                     ecommerce_sales_project2[returned] = "Yes" ),
         COUNTROWS ( ecommerce_sales_project2 ) )
```

**Test:** with no filters, the card for Net Revenue shows **5,476,537** and Net Profit shows **908,214** (about 908.2K). Net Profit Margin % shows **16.6%**.

## Step 2: Fix the headline visuals

1. Replace the Total Revenue card with **Net Revenue**. Keep a Gross Revenue card with the label "Gross revenue (incl. returns)" if you want the reconciliation visible.
2. Replace the Total Profit card with **Net Profit**. Rename any remaining "Total Profit" visual to "Profit as reported (incl. returns)", or remove it.
3. Replace the Profit Margin % measure everywhere with **Net Profit Margin %**.
4. Replace Return Rate with the order-based measure above, and label it "Return rate (% of orders)".

## Step 3: Add the slicers

Add three slicers and place them in the same position on both pages:

- **Date:** use the Calendar table, not the raw order_date column. Set it to "Between" style.
- **Region:** one slicer, dropdown or list.
- **Category:** one slicer, list.

Then:

1. **View > Sync slicers.** Tick "Sync" for all three on both pages, and "Visible" only on the page where each should show.
2. **Format > Edit interactions.** On each visual, check that the slicers filter it. Turn off interactions only where a visual should ignore a filter (for example, the category share chart should not ignore the category slicer).

**Test:** select Region = North. Net Revenue shows **1,192,987**. Clear the region and select Category = Electronics: Net Profit shows **318,931**. With Region = North and Category = Electronics together, Net Profit shows **70,071**. Clear all filters before saving.

## Step 4: Handle the partial months

1. On the trend visuals, add a visual-level filter on the Calendar month field: exclude Sep 2023 and Sep 2025.
2. Keep the Sep 2023 and Sep 2025 rows in the total cards, as the README states.
3. Add a footnote under the trend chart: "September 2023 (from 12 Sep) and September 2025 (to 11 Sep) are partial months and excluded from the trend."

**Test:** the trend chart shows 23 points, peaking at December 2024 (about $278K).

## Step 5: Remove or relabel the customer demographics

- Delete any visual that charts age or gender by customer, or any "customers by gender" visual.
- If you keep a demographic visual, rename it "Orders by customer age group (per order, not per customer)" and add a footnote explaining the limitation (README L3).
- Do not use `customer_id` to count "top customers by age" or similar.

## Step 6: Add the Data Quality page

Add a third page named **Data Quality**, with cards and a table. Use the values from `Validation_Log`:

| Card / table | Value |
|---|---|
| Rows | 34,500 |
| Blank cells | 0 |
| Duplicate order IDs | 0 |
| Arithmetic check (total_amount) | 0 mismatches |
| Negative profit rows | 6,104 (17.7%) |
| Profit on returned orders | $61,805 (excluded from net profit) |
| Customer IDs with varying gender | 6,391 of 7,903 |
| Unique product IDs | 24,912 of 34,500 rows |
| Conversion data | Not in source (limitation L1) |

**Test:** the table matches the FLAG rows in `Validation_Log`.

## Step 7: Footnotes on every page

Add a text box at the bottom of each page with: source file name, date range, and "Net basis: returned orders excluded from revenue and profit."

## Step 8: Update the Arabic report

The report uses profit that includes returned orders for category margins. Update three sentences:

1. Replace "ارتفاع ديسمبر يتكرر في السنتين" (December's rise repeats in both years) with a statement that December 2024 was the peak and 2023 does not show the same pattern.
2. Switch the headline profit and margin to net basis ($908K, 16.6%).
3. Update the Electronics profit share to 35.1% and the Grocery profit figure to -$9,067.

## Step 9: Final save and evidence

1. Save as `Project1_Dashboard.pbix`.
2. Take screenshots of each page with the filters in their default state, and one with Region = North. Save them to a folder named `evidence/`.
3. Add these screenshots to the README evidence index.

## Verification summary

| Check | Expected |
|---|---|
| Net Revenue, no filter | 5,476,537 |
| Net Profit, no filter | 908,214 |
| Net Profit Margin % | 16.6% |
| Net Revenue, Region = North | 1,192,987 |
| Net Profit, Category = Electronics, Region = North | 70,071 |
| Trend points | 23 |
| Sep 2025 gross revenue (in totals) | 91,848 |
