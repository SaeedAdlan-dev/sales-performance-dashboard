"""
Builds Project1_KPI_Validation.xlsx from the source file.
Run: python build_workbook.py  (expects ecommerce_sales_project2.xlsx in the same folder)
Formulas are live; only the three values that Excel cannot compute simply
(unique counts, duplicate count) are hardcoded in blue and labelled with their method.
"""
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter

SRC = "ecommerce_sales_project2.xlsx"
OUT = "Project1_KPI_Validation.xlsx"

df = pd.read_excel(SRC)
N = len(df)
LAST = N + 1  # last data row in Data sheet

F = "Arial"
H = Font(name=F, bold=True, color="FFFFFF")
HFILL = PatternFill("solid", fgColor="1F3864")
BLUE = Font(name=F, color="0000FF")          # hardcoded inputs / python results
BLACK = Font(name=F)                          # formulas
BOLD = Font(name=F, bold=True)
TITLE = Font(name=F, bold=True, size=13)
FLAG_FILL = PatternFill("solid", fgColor="FFF2CC")

def header(ws, row, values):
    for c, v in enumerate(values, 1):
        cell = ws.cell(row=row, column=c, value=v)
        cell.font = H; cell.fill = HFILL
        cell.alignment = Alignment(wrap_text=True, vertical="center")

def widths(ws, w):
    for i, x in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(i)].width = x

wb = Workbook()

# ---------------- README ----------------
ws = wb.active; ws.title = "README"
rows = [
    ("Project 1 - Sales Performance Dashboard: KPI and validation workbook", TITLE),
    ("Source file: ecommerce_sales_project2.xlsx (34,500 order rows, 17 columns, 12 Sep 2023 - 11 Sep 2025)", BLACK),
    ("Document status: consolidated and documented on 25 Nov 2026. Analysis was done before this workbook; it is not a week-1 artifact.", BLACK),
    ("", BLACK),
    ("Sheet guide", BOLD),
    ("Data - copy of the source rows, unchanged. Do not edit.", BLACK),
    ("KPI_Dictionary - every KPI, its definition, and the Excel formula used.", BLACK),
    ("KPI_Summary - headline KPIs, all live formulas on the Data sheet.", BLACK),
    ("Category / Region / Monthly - breakdowns used in the dashboard and the executive summary.", BLACK),
    ("Validation_Log - every data check, its result, its status, and the action taken.", BLACK),
    ("", BLACK),
    ("Colour legend", BOLD),
    ("Black text = formula.  Blue text = value computed in Python and typed in (method stated next to it).  Yellow fill = flagged issue.", BLACK),
    ("", BLACK),
    ("Scope limits (stated, not hidden)", BOLD),
    ("Conversion rate is NOT calculated: the source has no visitor or session data.", BLACK),
    ("Product-level analysis is NOT done: product_id is unique on almost every row, so only category is analysed.", BLACK),
    ("Customer demographics (age, gender) are NOT used as customer attributes: they vary per order for the same customer_id.", BLACK),
    ("Data source is not confirmed as real company data; treat results as analysis of this dataset only.", BLACK),
]
for i, (t, f) in enumerate(rows, 1):
    c = ws.cell(row=i, column=1, value=t); c.font = f
ws.column_dimensions["A"].width = 130

# ---------------- Data ----------------
wd = wb.create_sheet("Data")
cols = list(df.columns)
header(wd, 1, cols)
for r, rec in enumerate(df.itertuples(index=False), 2):
    for c, v in enumerate(rec, 1):
        if isinstance(v, pd.Timestamp):
            v = v.to_pydatetime()
        wd.cell(row=r, column=c, value=v)
for r in range(2, LAST + 1):
    wd.cell(row=r, column=9).number_format = "yyyy-mm-dd"
wd.freeze_panes = "A2"
widths(wd, [11, 11, 11, 13, 9, 9, 9, 14, 12, 12, 9, 10, 13, 12, 13, 12, 14])
# col letters used below
COL = {name: get_column_letter(i + 1) for i, name in enumerate(cols)}
def rng(name):
    c = COL[name]
    return f"Data!${c}$2:${c}${LAST}"

REV, RET, PROF = rng("total_amount"), rng("returned"), rng("profit_margin")
CAT, REG, DATE = rng("category"), rng("region"), rng("order_date")
SHIP, ORDER = rng("shipping_cost"), rng("order_id")

# ---------------- KPI_Dictionary ----------------
wk = wb.create_sheet("KPI_Dictionary")
header(wk, 1, ["KPI", "Definition (business)", "Excel formula used", "Notes / assumption"])
kpis = [
    ("Gross revenue", "Sum of order value including returned orders", f"=SUM({REV})", "total_amount includes returned orders; shown for reconciliation only"),
    ("Orders", "Count of order rows (order_id is unique)", f"=COUNTA({ORDER})", "Validated: no duplicate order_id"),
    ("Returned orders", "Orders with returned = Yes", f'=COUNTIF({RET},"Yes")', ""),
    ("Return rate", "Returned orders / all orders", "Returned orders / Orders", "Order-count basis"),
    ("Returned revenue", "Value of returned orders", f'=SUMIFS({REV},{RET},"Yes")', "Treated as reversed in net revenue"),
    ("Net revenue", "Gross revenue minus returned revenue", f'=SUMIFS({REV},{RET},"No")', "Headline revenue KPI in this project"),
    ("Net profit", "profit_margin on non-returned orders only", f'=SUMIFS({PROF},{RET},"No")', "ASSUMPTION: profit on returned orders is reversed. Source value is not adjusted for returns."),
    ("Net profit margin", "Net profit / Net revenue", "Net profit / Net revenue", "Headline margin KPI"),
    ("Average order value (AOV)", "Gross revenue / Orders", "Gross revenue / Orders", "Gross basis, to match the order count"),
    ("Unique customers", "Distinct customer_id", "Python: 7,903 (hardcoded, blue)", "Excel has no COUNTUNIQUE without dynamic arrays"),
    ("Category revenue share", "Category net revenue / total net revenue", "See Category sheet", "Used for Electronics headline"),
    ("Category net margin", "Category net profit / category net revenue", "See Category sheet", ""),
    ("Shipping as % of revenue", "Shipping cost / gross revenue, per category", "See Category sheet", "Driver of Grocery and Toys losses"),
    ("Month-over-month growth", "(Month - previous month) / previous month", "See Monthly sheet", "Partial months (Sep 2023, Sep 2025) excluded from growth"),
    ("NOT CALCULATED: Conversion rate", "Orders / sessions", "n/a", "No visitor or session data in source. Limitation L1."),
    ("NOT CALCULATED: Product performance", "Revenue / profit per product_id", "n/a", "product_id unique on 24,912 of 34,500 rows. Limitation L2."),
]
for i, row in enumerate(kpis, 2):
    for j, v in enumerate(row, 1):
        c = wk.cell(row=i, column=j, value=v); c.font = BLACK
        c.alignment = Alignment(wrap_text=True, vertical="top")
    if str(row[0]).startswith("NOT"):
        for j in range(1, 5): wk.cell(row=i, column=j).fill = FLAG_FILL
widths(wk, [30, 46, 46, 60])

# ---------------- KPI_Summary ----------------
ks = wb.create_sheet("KPI_Summary")
ks["A1"] = "Headline KPIs (live formulas on Data sheet)"; ks["A1"].font = TITLE
header(ks, 3, ["KPI", "Value", "Format note"])
summary = [
    ("Gross revenue ($)", f"=SUM({REV})", "$#,##0.00"),
    ("Orders", f"=COUNTA({ORDER})", "#,##0"),
    ("Returned orders", f'=COUNTIF({RET},"Yes")', "#,##0"),
    ("Return rate (orders)", "=B6/B5", "0.0%"),
    ("Returned revenue ($)", f'=SUMIFS({REV},{RET},"Yes")', "$#,##0.00"),
    ("Net revenue ($)", f'=SUMIFS({REV},{RET},"No")', "$#,##0.00"),
    ("Profit as reported in source, all orders ($)", f"=SUM({PROF})", "$#,##0.00"),
    ("Profit on returned orders ($)", f'=SUMIFS({PROF},{RET},"Yes")', "$#,##0.00"),
    ("Net profit, non-returned orders ($)", f'=SUMIFS({PROF},{RET},"No")', "$#,##0.00"),
    ("Net profit margin", "=B12/B9", "0.0%"),
    ("Average order value, gross ($)", "=B4/B5", "$#,##0.00"),
    ("Average shipping cost per order ($)", f"=AVERAGE({SHIP})", "$#,##0.00"),
    ("Unique customers (Python, see KPI_Dictionary)", 7903, "#,##0"),
    ("Unique product_ids (Python)", 24912, "#,##0"),
]
for i, (k, f, fmt) in enumerate(summary, 4):
    ks.cell(row=i, column=1, value=k).font = BLACK
    c = ks.cell(row=i, column=2, value=f)
    c.font = BLUE if isinstance(f, (int, float)) else BLACK
    c.number_format = fmt
    ks.cell(row=i, column=3, value=fmt).font = BLACK
widths(ks, [48, 20, 16])

# ---------------- Category ----------------
wc = wb.create_sheet("Category")
wc["A1"] = "Category performance (net = non-returned orders)"; wc["A1"].font = TITLE
header(wc, 3, ["Category", "Orders", "Gross revenue ($)", "Returned revenue ($)", "Net revenue ($)",
               "Net profit ($)", "Net margin", "Share of net revenue", "Share of net profit",
               "Return rate (orders)", "Share of returned value", "Shipping % of gross revenue",
               "Loss-making share of orders"])
cats = sorted(df["category"].unique(), key=lambda x: -df.loc[df.category == x, "total_amount"].sum())
first = 4
last = first + len(cats) - 1
tot = last + 1
for i, cat in enumerate(cats):
    r = first + i
    wc.cell(row=r, column=1, value=cat)
    wc.cell(row=r, column=2, value=f'=COUNTIF({CAT},A{r})')
    wc.cell(row=r, column=3, value=f'=SUMIFS({REV},{CAT},A{r})')
    wc.cell(row=r, column=4, value=f'=SUMIFS({REV},{CAT},A{r},{RET},"Yes")')
    wc.cell(row=r, column=5, value=f'=C{r}-D{r}')
    wc.cell(row=r, column=6, value=f'=SUMIFS({PROF},{CAT},A{r},{RET},"No")')
    wc.cell(row=r, column=7, value=f'=IFERROR(F{r}/E{r},0)')
    wc.cell(row=r, column=8, value=f'=E{r}/$E${tot}')
    wc.cell(row=r, column=9, value=f'=F{r}/$F${tot}')
    wc.cell(row=r, column=10, value=f'=COUNTIFS({CAT},A{r},{RET},"Yes")/B{r}')
    wc.cell(row=r, column=11, value=f'=D{r}/$D${tot}')
    wc.cell(row=r, column=12, value=f'=SUMIFS({SHIP},{CAT},A{r})/C{r}')
    wc.cell(row=r, column=13, value=f'=COUNTIFS({CAT},A{r},{PROF},"<0")/B{r}')
wc.cell(row=tot, column=1, value="Total").font = BOLD
for col in "BCDEF":
    wc[f"{col}{tot}"] = f"=SUM({col}{first}:{col}{last})"
wc[f"G{tot}"] = f"=F{tot}/E{tot}"
for col in "HIK":
    wc[f"{col}{tot}"] = f"=SUM({col}{first}:{col}{last})"
wc[f"J{tot}"] = f'=COUNTIF({RET},"Yes")/B{tot}'
wc[f"L{tot}"] = f"=SUM({SHIP})/C{tot}"
wc[f"M{tot}"] = f'=COUNTIF({PROF},"<0")/B{tot}'
r = tot + 2
wc.cell(row=r, column=1, value="Check: category net revenue equals KPI_Summary net revenue (should be 0)").font = BLACK
wc.cell(row=r, column=5, value=f"=ROUND(E{tot}-KPI_Summary!B9,2)")
for row in wc.iter_rows(min_row=first, max_row=tot):
    for c in row:
        c.font = BOLD if c.row == tot else BLACK
        if c.column in (3, 4, 5, 6): c.number_format = "$#,##0"
        if c.column in (2,): c.number_format = "#,##0"
        if c.column in (7, 8, 9, 10, 11, 12, 13): c.number_format = "0.0%"
widths(wc, [16, 10, 16, 18, 16, 14, 12, 14, 14, 14, 16, 18, 18])

# ---------------- Region ----------------
wr = wb.create_sheet("Region")
wr["A1"] = "Region performance"; wr["A1"].font = TITLE
header(wr, 3, ["Region", "Orders", "Net revenue ($)", "Return rate (orders)"])
regions = sorted(df["region"].unique())
for i, reg in enumerate(regions):
    r = 4 + i
    wr.cell(row=r, column=1, value=reg).font = BLACK
    wr.cell(row=r, column=2, value=f'=COUNTIF({REG},A{r})').number_format = "#,##0"
    wr.cell(row=r, column=3, value=f'=SUMIFS({REV},{REG},A{r},{RET},"No")').number_format = "$#,##0"
    wr.cell(row=r, column=4, value=f'=COUNTIFS({REG},A{r},{RET},"Yes")/B{r}').number_format = "0.0%"
widths(wr, [14, 12, 18, 20])

# ---------------- Monthly ----------------
wm = wb.create_sheet("Monthly")
wm["A1"] = "Monthly trend (gross revenue, as in dashboard). Partial months flagged and excluded from growth."; wm["A1"].font = TITLE
header(wm, 3, ["Month start", "Status", "Orders", "Gross revenue ($)", "MoM growth", "YoY growth"])
months = pd.period_range("2023-09", "2025-09", freq="M")
for i, p in enumerate(months):
    r = 4 + i
    wm.cell(row=r, column=1, value=p.to_timestamp().to_pydatetime()).number_format = "mmm yyyy"
    wm.cell(row=r, column=2, value=f'=IF(OR(A{r}=DATE(2023,9,1),A{r}=DATE(2025,9,1)),"Partial","Full")')
    wm.cell(row=r, column=3, value=f'=COUNTIFS({DATE},">="&A{r},{DATE},"<"&EDATE(A{r},1))').number_format = "#,##0"
    wm.cell(row=r, column=4, value=f'=SUMIFS({REV},{DATE},">="&A{r},{DATE},"<"&EDATE(A{r},1))').number_format = "$#,##0"
    if i >= 1:
        wm.cell(row=r, column=5, value=f'=IF(OR(B{r}="Partial",B{r-1}="Partial"),"",D{r}/D{r-1}-1)').number_format = "0.0%"
    if i >= 12:
        wm.cell(row=r, column=6, value=f'=IF(OR(B{r}="Partial",B{r-12}="Partial"),"",D{r}/D{r-12}-1)').number_format = "0.0%"
    for c in range(1, 7): wm.cell(row=r, column=c).font = BLACK
widths(wm, [14, 12, 10, 18, 14, 14])

# ---------------- Validation_Log ----------------
wv = wb.create_sheet("Validation_Log")
wv["A1"] = "Data validation log"; wv["A1"].font = TITLE
header(wv, 3, ["#", "Check", "Method", "Result", "Status", "Action taken"])
checks = [
    ("Row count", "COUNTA of order_id", f"=COUNTA({ORDER})", "PASS if 34500", "Expected count confirmed."),
    ("Blank cells in data", "COUNTBLANK over all 17 columns", f"=COUNTBLANK(Data!A2:Q{LAST})", "PASS if 0", "No imputation needed."),
    ("Duplicate order_id", "Python: duplicated() on order_id", 0, "PASS if 0", "No deduplication needed. Hardcoded from Python."),
    ("Arithmetic: total_amount = price x (1 - discount) x quantity", "SUMPRODUCT, tolerance 0.02",
        f"=SUMPRODUCT(--(ABS(Data!E2:E{LAST}*(1-Data!F2:F{LAST})*Data!G2:G{LAST}-Data!M2:M{LAST})>0.02))", "PASS if 0", "Max difference 0.01 (rounding). Field is internally consistent."),
    ("Quantity range", "MIN of quantity", f"=MIN(Data!G2:G{LAST})", "PASS if >= 1", "No zero or negative quantities."),
    ("Discount range", "MAX of discount", f"=MAX(Data!F2:F{LAST})", "PASS if <= 0.3", "Discount ranges 0 to 0.30. Average 5%, similar across categories."),
    ("Date range", "MIN of order_date", f"=MIN({DATE})", "Info", "Starts 12 Sep 2023. Sep 2023 is a partial month (19 days)."),
    ("Date range end", "MAX of order_date", f"=MAX({DATE})", "Info", "Ends 11 Sep 2025. Sep 2025 is a partial month (11 days)."),
    ("profit_margin is currency, not %", "Count of profit_margin > total_amount", f"=SUMPRODUCT(--(Data!O2:O{LAST}>Data!M2:M{LAST}))", "PASS if 0", "Values are dollar amounts. Dashboard labels changed to $ and percentages are computed, not read."),
    ("Negative profit rows", "COUNTIF profit_margin < 0", f'=COUNTIF({PROF},"<0")', "FLAG", "17.7% of orders are loss-making. Kept: real loss signal, not an error."),
    ("Profit on returned orders", "SUMIFS profit where returned = Yes", f'=SUMIFS({PROF},{RET},"Yes")', "FLAG", "Refunded orders still carry profit, and their margin is higher on average. Headline uses net profit (non-returned only). Assumption in KPI_Dictionary."),
    ("Customer attributes inconsistent", "Python: customer_ids with >1 gender value", 6391, "FLAG", "Of 7,903 customers, 6,391 have more than one gender. Customer-level age/gender excluded. Limitation L3."),
    ("Customer age inconsistent", "Python: customer_ids with >1 age value", 7411, "FLAG", "Same issue. Demographics reported per order only."),
    ("product_id granularity", "Python: unique product_id count", 24912, "FLAG", "Almost every order has its own product_id. Product-level analysis not possible. Limitation L2."),
    ("Category coverage", "Sum of category order counts equals total", f"=SUM(Category!B4:B10)-COUNTA({ORDER})", "PASS if 0", "7 categories, all rows mapped."),
    ("Region coverage", "Sum of region order counts equals total", f"=SUM(Region!B4:B8)-COUNTA({ORDER})", "PASS if 0", "5 regions, all rows mapped."),
    ("Revenue reconciliation: category vs KPI", "Category net revenue minus KPI net revenue", f"=Category!E{tot}-KPI_Summary!B9", "PASS if 0", "Breakdown ties back to headline."),
    ("Monthly reconciliation: monthly sum vs total", "Sum of monthly gross revenue minus total", f"=ROUND(SUM(Monthly!D4:D28)-KPI_Summary!B4,2)", "PASS if 0", "All rows fall inside the 25 monthly buckets."),
    ("Conversion data available?", "Check source columns for visitors/sessions", "No such column", "FLAG", "Conversion rate not calculated. Limitation L1."),
]
for i, (name, method, res, status, action) in enumerate(checks, 4):
    wv.cell(row=i, column=1, value=i - 3).font = BLACK
    wv.cell(row=i, column=2, value=name).font = BLACK
    wv.cell(row=i, column=3, value=method).font = BLACK
    rc = wv.cell(row=i, column=4, value=res)
    rc.font = BLUE if isinstance(res, (int, float)) else BLACK
    wv.cell(row=i, column=5, value=status).font = BLACK
    wv.cell(row=i, column=6, value=action).font = BLACK
    for c in range(1, 7):
        wv.cell(row=i, column=c).alignment = Alignment(wrap_text=True, vertical="top")
    if status == "FLAG":
        for c in range(1, 7): wv.cell(row=i, column=c).fill = FLAG_FILL
widths(wv, [5, 40, 36, 16, 14, 70])

for rr in (10, 11):
    wv.cell(row=rr, column=4).number_format = "dd mmm yyyy"
wb.save(OUT)
print("saved", OUT, "rows", N)
