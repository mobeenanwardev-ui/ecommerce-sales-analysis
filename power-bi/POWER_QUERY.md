# Power Query — Import and clean the Online Retail data

## 1. Download the source
Download the Excel workbook from:
https://archive.ics.uci.edu/dataset/352/online+retail
Save it as Online Retail.xlsx.

## 2. Import
In Power BI Desktop: Home → Get data → Excel workbook. Select the workbook, select the transaction worksheet, and choose Transform Data. Rename the query OnlineRetail.

## 3. Apply transformations
The M query below assumes the worksheet is named OnlineRetail. If Navigator shows a different sheet name (for example, Year 2009-2010), replace the Item value with the actual name.

    let
        Source = Excel.Workbook(File.Contents("C:\YOUR_FOLDER\Online Retail.xlsx"), null, true),
        RetailSheet = Source{[Item="OnlineRetail", Kind="Sheet"]}[Data],
        PromotedHeaders = Table.PromoteHeaders(RetailSheet, [PromoteAllScalars=true]),
        ChangedTypes = Table.TransformColumnTypes(
            PromotedHeaders,
            {
                {"InvoiceNo", type text},
                {"StockCode", type text},
                {"Description", type text},
                {"Quantity", Int64.Type},
                {"InvoiceDate", type datetime},
                {"UnitPrice", Currency.Type},
                {"CustomerID", type text},
                {"Country", type text}
            },
            "en-GB"
        ),
        TrimmedText = Table.TransformColumns(
            ChangedTypes,
            {
                {"InvoiceNo", each Text.Trim(_), type text},
                {"StockCode", each Text.Trim(_), type text},
                {"Country", each Text.Trim(_), type text}
            }
        ),
        RemovedDuplicates = Table.Distinct(TrimmedText),
        ExcludedCancellations = Table.SelectRows(
            RemovedDuplicates,
            each not Text.StartsWith([InvoiceNo], "C")
        ),
        PositiveQuantity = Table.SelectRows(
            ExcludedCancellations,
            each [Quantity] > 0
        ),
        PositiveUnitPrice = Table.SelectRows(
            PositiveQuantity,
            each [UnitPrice] > 0
        ),
        AddedRevenue = Table.AddColumn(
            PositiveUnitPrice,
            "Revenue",
            each Number.From([Quantity]) * Number.From([UnitPrice]),
            Currency.Type
        ),
        AddedInvoiceDateDate = Table.AddColumn(
            AddedRevenue,
            "InvoiceDate_Date",
            each Date.From([InvoiceDate]),
            type date
        )
    in
        AddedInvoiceDateDate

## 4. Check the result
- Confirm no errors in Quantity, UnitPrice, InvoiceDate, or Revenue.
- Confirm cancelled invoices (InvoiceNo beginning with C) are excluded.
- Confirm Quantity and UnitPrice are positive.
- Keep missing CustomerID rows in overall sales; exclude blanks only from customer counts.
- Select Close & Apply.

## 5. Model relationship
Create DateTable using the DAX in DAX_MEASURES.dax, then relate DateTable[Date] to OnlineRetail[InvoiceDate_Date]. Use one-to-many cardinality and single cross-filter direction.

The source contains transaction lines, not one row per order. Use DISTINCTCOUNT(InvoiceNo) for orders.
