# Austrian Wareneingangsbuch

This addon adds a dedicated `Wareneingangsbuch` report for Austrian accounting in Odoo 18.

## Features

- Dedicated Wareneingangsbuch report under Accounting reporting
- Chronological line numbering
- Supplier name and address
- Generic goods description per product or category
- Gross, tax, and net amounts
- Clickable vendor bill reference
- Category-level inclusion flag for qualifying goods
- Service exclusion for cleaner Wareneingangsbuch reporting

## Usage

1. Install the module.
2. Open the relevant product categories and enable `Include in Wareneingangsbuch`.
3. Optionally set a generic `Wareneingangsbuch Label` on categories or products.
4. Open `Accounting > Reporting > Wareneingangsbuch`.

## Notes

- The report is based on posted vendor bill lines.
- Receipt date is used when a linked purchase receipt is available; otherwise the invoice date is used.
- Products without a product record are excluded in the current implementation.
