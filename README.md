# Credit Card Statement Parser

## 1. Project Overview

This project is a Python-based solution designed to parse PDF credit card statements from 5 different major issuers and automatically extract key financial data points.
The parser reads a directory of PDF statements, intelligently identifies the issuing bank for each file, and applies a set of bank-specific rules to extract 5 key data points. The final, structured data is then exported to both JSON and Excel for easy analysis.

### Core Features:
- Multi-Issuer Support: Parses statements from Chase, Axis Bank, ICICI Bank, IDFC First Bank, and HDFC Bank.
- Intelligent Detection: Automatically detects the issuer from the PDF's text content.
-	Flexible Data Extraction: Handles the unique formatting of each bank, including different key fields (e.g., statement_period vs. statement_date).
-	Robust Parsing: Built to handle common PDF text extraction issues, such as garbled text and inconsistent line breaks.
-	Batch Processing: Capable of processing an entire folder of statements in one run.
-	Report Generation: Outputs a clean, timestamped JSON and Excel file with all extracted data.

## 2. Functionality & Live Demonstration

This section covers how to set up and run the project to demonstrate its functionality live.
### Requirements
The project requires the following Python libraries:
- pdfplumber: For extracting text from PDF files.
- pandas: For generating the Excel report.
-	openpyxl: Required by pandas to write .xlsx files.
You can install them using pip:
pip install pdfplumber pandas openpyxl

## Directory Structure
```
credit_card_parser/
│
├── statements/
│   ├── chase_sample.pdf
│   ├── hdfc_sample.pdf
│   ├── axis_sample.pdf
│   └── ... (other sample PDFs)
│
├── parser.py     # Core parser class
└── batch_test.py    # Batch test runner
```

How to Run the Demonstration
The batch_test.py script is the entry point for demonstrating the solution.
1.	Place all your sample PDF statements (for all 5 banks) into the statements/ directory.
2.	Open your terminal or command prompt.
3.	Navigate to the credit_card_parser/ directory.
4.	Run the batch test script, passing the statements/ directory as an argument:

```
python batch_test.py statements/
```
### Understanding the Output

Running the script provides two forms of output, demonstrating the successful extraction:

1.Console Output (Live Progress): The terminal will print the results for each file as it's processed, followed by a final summary. This shows the parser's logic in real-time.
```
======================================================================
CREDIT CARD STATEMENT PARSER - BATCH TEST
======================================================================

Found 5 PDF file(s) to process


[1/5] Processing: 452877250-CreditCardStatement-9.pdf
----------------------------------------------------------------------
✓ Issuer: ICICI Bank
  Due Date: 30/11/2018
  Total Amount Due: None
  Card Last 4: 9007
  Statement Period: 13/10/2018 - 12/11/2018
  Previous Balance: 5139.3

[2/5] Processing: 531906783-IDFC-FIRST-Bank-Credit-Card-Statement-24082021.pdf
----------------------------------------------------------------------
✓ Issuer: IDFC FIRST Bank
  Due Date: 11/09/2021
  Total Amount Due: 29147.25
  Card Last 4: 9388
  Statement Period: 25/07/2021 - 24/08/2021
  Previous Balance: 29235.08

[3/5] Processing: 636483454-credit-card-statement.pdf
----------------------------------------------------------------------
✓ Issuer: HDFC Bank
  Due Date: 01/04/2023
  Total Amount Due: 22935.0
  Card Last 4: 3458
  Statement Date: 12/03/2023
  Credit Limit: 30000.0

[4/5] Processing: axis.pdf
----------------------------------------------------------------------
✓ Issuer: Axis Bank
  Due Date: 04/06/2021
  Total Amount Due: 1289.0
  Card Last 4: 1060
  Statement Period: 16/04/2021 - 15/05/2021
  Previous Balance: 2334.0

[5/5] Processing: paperless_statements_chase_sample.pdf
----------------------------------------------------------------------
✓ Issuer: Chase
  Due Date: 01/25/19
  Total Amount Due: 1245.0
  Card Last 4: 0000
  Statement Period: 12/03/18 - 01/01/19
  Previous Balance: 1270.0

======================================================================
SUMMARY
======================================================================

Total Statements Processed: 5
✓ Successful: 5
❌ Failed: 0

Issuers Detected:
  • ICICI Bank: 1 statement(s)
  • IDFC FIRST Bank: 1 statement(s)
  • HDFC Bank: 1 statement(s)
  • Axis Bank: 1 statement(s)
  • Chase: 1 statement(s)

Data Extraction Completeness:
  • due_date (All): 5/5 (100.0%)
  • total_amount_due (All): 4/5 (80.0%)

Total Statements Processed: 5
✓ Successful: 5
❌ Failed: 0

Issuers Detected:
  • ICICI Bank: 1 statement(s)
  • IDFC FIRST Bank: 1 statement(s)
  • HDFC Bank: 1 statement(s)
  • Axis Bank: 1 statement(s)
  • Chase: 1 statement(s)

Data Extraction Completeness:
  • due_date (All): 5/5 (100.0%)
  • total_amount_due (All): 4/5 (80.0%)
✓ Successful: 5
❌ Failed: 0

Issuers Detected:
  • ICICI Bank: 1 statement(s)
  • IDFC FIRST Bank: 1 statement(s)
  • HDFC Bank: 1 statement(s)
  • Axis Bank: 1 statement(s)
  • Chase: 1 statement(s)

Data Extraction Completeness:
  • due_date (All): 5/5 (100.0%)
  • total_amount_due (All): 4/5 (80.0%)
Issuers Detected:
  • ICICI Bank: 1 statement(s)
  • IDFC FIRST Bank: 1 statement(s)
  • HDFC Bank: 1 statement(s)
  • Axis Bank: 1 statement(s)
  • Chase: 1 statement(s)

Data Extraction Completeness:
  • due_date (All): 5/5 (100.0%)
  • total_amount_due (All): 4/5 (80.0%)
  • IDFC FIRST Bank: 1 statement(s)
  • HDFC Bank: 1 statement(s)
  • Axis Bank: 1 statement(s)
  • Chase: 1 statement(s)

Data Extraction Completeness:
  • due_date (All): 5/5 (100.0%)
  • total_amount_due (All): 4/5 (80.0%)
  • HDFC Bank: 1 statement(s)
  • Axis Bank: 1 statement(s)
  • Chase: 1 statement(s)

Data Extraction Completeness:
  • due_date (All): 5/5 (100.0%)
  • total_amount_due (All): 4/5 (80.0%)
  • Chase: 1 statement(s)

Data Extraction Completeness:
  • due_date (All): 5/5 (100.0%)
  • total_amount_due (All): 4/5 (80.0%)
Data Extraction Completeness:
  • due_date (All): 5/5 (100.0%)
  • total_amount_due (All): 4/5 (80.0%)
  • due_date (All): 5/5 (100.0%)
  • total_amount_due (All): 4/5 (80.0%)
  • total_amount_due (All): 4/5 (80.0%)
  • card_last_4 (All): 5/5 (100.0%)
  • statement_period (Others): 4/4 (100.0%)
  • previous_balance (Others): 4/4 (100.0%)
  • statement_date (HDFC): 1/1 (100.0%)
  • credit_limit (HDFC): 1/1 (100.0%)

✓ Results exported to: parser_results_20251102_125653.json
✓ Results exported to: parser_results_20251102_125653.xlsx
```

### 2. Generated Reports (The Deliverable):
The script also generates two files, parser_results_...json and parser_results_...xlsx, which contain the full structured data for all processed statements. This is the final product.


## 3. Implementation Quality & Design

This solution is designed to be robust, maintainable, and extensible.
### Core Components
-	parser.py: This file contains the CreditCardParser class. This class is the "engine" of the solution. It is responsible for opening the PDF, extracting text, identifying the issuer, and routing the text to the correct internal parsing method.
-	batch_test.py: This is the "driver" script. It's responsible for finding all the PDF files, feeding them to the CreditCardParser, and generating the final summary reports. It's designed to be the main entry point for using the parser.
### The Parsing Pipeline
The extraction process for each PDF follows a 4-step pipeline:
1.	Text Extraction (_extract_text): The PDF is opened with pdfplumber and all text is extracted. Tolerances are set to help pdfplumber better connect words that are part of the same line, and excess newlines are cleaned up.
2.	Issuer Detection (_detect_issuer): The extracted text is converted to lowercase and scanned for unique keywords ("hdfc bank", "idfc first bank", "chase.com", etc.). The detection logic is prioritized to check for more specific banks (like HDFC) first, preventing misidentification.
3.	Parser Routing (parse): Based on the detected issuer, the main parse method acts as a router, calling the correct bank-specific private method (e.g., _parse_hdfc, _parse_axis).
4.	Regex Extraction (_parse_... methods): Each bank-specific method contains a set of highly-tuned Regular Expressions (Regex). These patterns are designed to find the exact data points within the (often messy) extracted text.
### Handling Real-World Variations
A key part of the implementation quality is its robustness to "real-world" PDF issues.
- Garbled Text: The HDFC statement, for example, produced heavily garbled text with random line breaks. The regex for HDFC was written using the re.DOTALL flag and flexible whitespace matching (\s+) to find the data patterns even when they are broken across multiple lines.
-	Different Date Formats: The parser handles multiple date formats, such as MM/DD/YY (Chase) and DD/MM/YYYY (Axis).
-	Different Key Fields: The parser correctly identifies that HDFC provides a Statement Date and Credit Limit, while the other banks provide a Statement Period and Previous Balance. The batch_test.py script is also designed to understand and correctly report on this difference in its final summary.
-	Maintainability: By separating each bank's logic into its own method (e.g., _parse_icici), the solution is easy to maintain. If a bank changes its statement format, only that one method needs to be updated. Adding a new bank (e.g., Amex) is as simple as adding one more elif to the detector and a new _parse_amex method.

