import re
from typing import Dict, Optional
import pdfplumber
from datetime import datetime


class CreditCardParser:
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = self._extract_text()
        self.issuer = self._detect_issuer()
    
    def _extract_text(self) -> str:
        text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text(x_tolerance=1, y_tolerance=1)
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error extracting text: {e}")
        text = re.sub(r'\n{2,}', '\n', text)
        return text
    
    def _detect_issuer(self) -> str:
        text_lower = self.text.lower()
        
        if "hdfc bank" in text_lower or "hdfcbank" in text_lower:
            return "HDFC"
        elif "icici bank" in text_lower or "icicibank" in text_lower:
            return "ICICI"
        elif "idfc first bank" in text_lower or "idfcbank" in text_lower:
            return "IDFC_FIRST"
        elif "axis bank" in text_lower or "axisbank" in text_lower:
            return "AXIS"
        elif "chase" in text_lower and "chase.com" in text_lower:
            return "CHASE"
        else:
            return "UNKNOWN"
    
    def parse(self) -> Dict[str, any]:
        if self.issuer == "ICICI":
            return self._parse_icici()
        elif self.issuer == "IDFC_FIRST":
            return self._parse_idfc()
        elif self.issuer == "AXIS":
            return self._parse_axis()
        elif self.issuer == "CHASE":
            return self._parse_chase()
        elif self.issuer == "HDFC":
            return self._parse_hdfc()
        else:
            return {"error": "Unknown issuer", "issuer": "UNKNOWN"}
    
    def _parse_icici(self) -> Dict[str, any]:
        data = {
            "issuer": "ICICI Bank",
            "statement_period": None,
            "due_date": None,
            "total_amount_due": None,
            "card_last_4": None,
            "previous_balance": None
        }
        
        period_patterns = [
            r'Statement Period\s*:?\s*From\s+(\d{2}/\d{2}/\d{4})\s+to\s+(\d{2}/\d{2}/\d{4})',
            r'From\s+(\d{2}/\d{2}/\d{4})\s+to\s+(\d{2}/\d{2}/\d{4})',
        ]
        for pattern in period_patterns:
            period_match = re.search(pattern, self.text, re.IGNORECASE)
            if period_match:
                data["statement_period"] = f"{period_match.group(1)} - {period_match.group(2)}"
                break
        
        due_patterns = [
            r'Due Date\s*:?\s*(\d{2}/\d{2}/\d{4})',
            r'Payment Due Date\s*:?\s*(\d{2}/\d{2}/\d{4})',
        ]
        for pattern in due_patterns:
            due_match = re.search(pattern, self.text, re.IGNORECASE)
            if due_match:
                data["due_date"] = due_match.group(1)
                break
        
        amount_patterns = [
            r'Your Total Amount Due\s*[\r\n]+\s*\d{2}/\d{2}/\d{4}\s*\|\s*[\d,]+\.?\d*\s*[\r\n]+\s*\|\s*([\d,]+\.?\d*)',
            r'Minimum Amount Due\s+Your Total Amount Due\s*[\r\n]+\s*\d{2}/\d{2}/\d{4}\s*\|\s*[\d,]+\.?\d*\s*[\r\n]+\s*\|\s*([\d,]+\.?\d*)',
        ]
        for pattern in amount_patterns:
            amount_match = re.search(pattern, self.text, re.IGNORECASE)
            if amount_match:
                amount_str = amount_match.group(1).replace(',', '')
                data["total_amount_due"] = float(amount_str)
                break
        
        card_patterns = [
            r'Card Account No\s*[\r\n]+\s*\w+.*?\s+(\d{4})\s+XXXX\s+XXXX\s+(\d{4})',
            r'(\d{4})\s+XXXX\s+XXXX\s+(\d{4})',
        ]
        for pattern in card_patterns:
            card_match = re.search(pattern, self.text)
            if card_match:
                data["card_last_4"] = card_match.group(2)
                break
        
        prev_patterns = [
            r'Previous Balance.*?Summary\s+([\d,]+\.?\d*)',
            r'Statement\s+Summary\s+([\d,]+\.?\d*)',
        ]
        for pattern in prev_patterns:
            prev_match = re.search(pattern, self.text, re.IGNORECASE | re.DOTALL)
            if prev_match:
                prev_str = prev_match.group(1).replace(',', '')
                data["previous_balance"] = float(prev_str)
                break
        
        return data
    
    def _parse_idfc(self) -> Dict[str, any]:
        data = {
            "issuer": "IDFC FIRST Bank",
            "statement_period": None,
            "due_date": None,
            "total_amount_due": None,
            "card_last_4": None,
            "previous_balance": None
        }
        
        period_patterns = [
            r'From:\s*(\d{2}/\d{2}/\d{4})\s*To:\s*(\d{2}/\d{2}/\d{4})',
            r'Statement Period\s*From:\s*(\d{2}/\d{2}/\d{4})\s*To:\s*(\d{2}/\d{2}/\d{4})',
        ]
        for pattern in period_patterns:
            period_match = re.search(pattern, self.text, re.IGNORECASE)
            if period_match:
                data["statement_period"] = f"{period_match.group(1)} - {period_match.group(2)}"
                break
        
        due_patterns = [
            r'Statement Date\s+Payment Due Date\s*[\r\n]+.*?(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})',
            r'(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})\s*[\r\n]+.*?Nursing Home',
        ]
        for pattern in due_patterns:
            due_match = re.search(pattern, self.text, re.IGNORECASE | re.DOTALL)
            if due_match:
                data["due_date"] = due_match.group(2)
                break
        
        amount_patterns = [
            r'Total Amount Due\s+Minimum Amount Due\s*[\r\n]+.*?r\s*([\d,]+\.?\d*)',
            r'Total Amount Due.*?r\s*([\d,]+\.?\d*)\s+r\s*[\d,]+\.?\d*',
        ]
        for pattern in amount_patterns:
            amount_match = re.search(pattern, self.text, re.IGNORECASE | re.DOTALL)
            if amount_match:
                amount_str = amount_match.group(1).replace(',', '')
                data["total_amount_due"] = float(amount_str)
                break
        
        card_patterns = [
            r'(\d{6})\*{6}(\d{4})',
            r'Card Number\s*:?\s*\d{6}\*{6}(\d{4})',
        ]
        for pattern in card_patterns:
            card_match = re.search(pattern, self.text)
            if card_match:
                if len(card_match.groups()) == 2:
                    data["card_last_4"] = card_match.group(2)
                else:
                    data["card_last_4"] = card_match.group(1)
                break
        
        prev_patterns = [
            r'Opening\s+Balance\s+Purchase.*?r[\d,]+\.?\d*\s+r([\d,]+\.?\d*)',
            r'SUMMARY\s+r[\d,]+\.?\d*\s+r([\d,]+\.?\d*)',
        ]
        for pattern in prev_patterns:
            prev_match = re.search(pattern, self.text, re.IGNORECASE | re.DOTALL)
            if prev_match:
                prev_str = prev_match.group(1).replace(',', '')
                data["previous_balance"] = float(prev_str)
                break
        
        return data
    
    def _parse_axis(self) -> Dict[str, any]:
        data = {
            "issuer": "Axis Bank",
            "statement_period": None,
            "due_date": None,
            "total_amount_due": None,
            "card_last_4": None,
            "previous_balance": None
        }
        
        period_patterns = [
            r'(\d{2}/\d{2}/\d{4})\s*-\s*(\d{2}/\d{2}/\d{4})\s+\d{2}/\d{2}/\d{4}',
            r'Statement Period\s*(\d{2}/\d{2}/\d{4})\s*-?\s*(\d{2}/\d{2}/\d{4})',
        ]
        for pattern in period_patterns:
            period_match = re.search(pattern, self.text, re.IGNORECASE)
            if period_match:
                data["statement_period"] = f"{period_match.group(1)} - {period_match.group(2)}"
                break
        
        due_patterns = [
            r'\d{2}/\d{2}/\d{4}\s*-\s*\d{2}/\d{2}/\d{4}\s+(\d{2}/\d{2}/\d{4})',
            r'Payment Due Date\s*(\d{2}/\d{2}/\d{4})',
        ]
        for pattern in due_patterns:
            due_match = re.search(pattern, self.text, re.IGNORECASE)
            if due_match:
                data["due_date"] = due_match.group(1)
                break
        
        amount_patterns = [
            r'Total Payment Due\s+[\w\s]+\s+([\d,]+\.?\d*)\s+Dr',
            r'Total Payment Due.*?([\d,]+\.?\d*)\s+Dr',
        ]
        for pattern in amount_patterns:
            amount_match = re.search(pattern, self.text, re.IGNORECASE | re.DOTALL)
            if amount_match:
                amount_str = amount_match.group(1).replace(',', '')
                data["total_amount_due"] = float(amount_str)
                break
        
        card_patterns = [
            r'(\d{8})\*{4}(\d{4})',
            r'Card\s+No[:\.]?\s*(\d{8})\*{4}(\d{4})',
        ]
        for pattern in card_patterns:
            card_match = re.search(pattern, self.text)
            if card_match:
                data["card_last_4"] = card_match.group(2)
                break
        
        prev_patterns = [
            r'Previous Balance\s*-\s*Payments.*?[\r\n]+\s*([\d,]+\.?\d*)\s+Dr',
            r'Account Summary.*?[\r\n]+.*?[\r\n]+\s*([\d,]+\.?\d*)\s+Dr\s+[\d,]+\.?\d*\s+Dr',
        ]
        for pattern in prev_patterns:
            prev_match = re.search(pattern, self.text, re.IGNORECASE | re.DOTALL)
            if prev_match:
                prev_str = prev_match.group(1).replace(',', '')
                data["previous_balance"] = float(prev_str)
                break
        
        return data
    
    def _parse_chase(self) -> Dict[str, any]:
        data = {
            "issuer": "Chase",
            "statement_period": None,
            "due_date": None,
            "total_amount_due": None,
            "card_last_4": None,
            "previous_balance": None
        }
        
        period_patterns = [
            r'Opening/Closing Date\s*(\d{2}/\d{2}/\d{2,4})\s*-\s*(\d{2}/\d{2}/\d{2,4})',
        ]
        for pattern in period_patterns:
            period_match = re.search(pattern, self.text, re.IGNORECASE)
            if period_match:
                data["statement_period"] = f"{period_match.group(1)} - {period_match.group(2)}"
                break
        
        due_patterns = [
            r'Payment Due Date\s*:?\s*(\d{2}/\d{2}/\d{2,4})',
            r'Payment Due Date\s*[\r\n]+\s*(\d{2}/\d{2}/\d{2,4})',
        ]
        for pattern in due_patterns:
            due_match = re.search(pattern, self.text, re.IGNORECASE)
            if due_match:
                data["due_date"] = due_match.group(1)
                break
        
        amount_patterns = [
            r'New Balance\s*\$\s*([\d,]+\.?\d*)',
            r'New Balance.*?\$\s*([\d,]+\.?\d*)',
        ]
        for pattern in amount_patterns:
            amount_match = re.search(pattern, self.text, re.IGNORECASE)
            if amount_match:
                amount_str = amount_match.group(1).replace(',', '')
                data["total_amount_due"] = float(amount_str)
                break
        
        card_patterns = [
            r'Account Number\s*:?\s*XXXX\s+XXXX\s+XXXX\s+(\d{4})',
            r'Account number\s*:?\s*\d{4}\s+\d{4}\s+\d{4}\s+(\d{4})',
            r'XXXX\s+XXXX\s+XXXX\s+(\d{4})',
        ]
        for pattern in card_patterns:
            card_match = re.search(pattern, self.text, re.IGNORECASE)
            if card_match:
                data["card_last_4"] = card_match.group(1)
                break
        
        prev_patterns = [
            r'Previous Balance\s*\$\s*([\d,]+\.?\d*)',
            r'Previous Balance.*?\$\s*([\d,]+\.?\d*)',
        ]
        for pattern in prev_patterns:
            prev_match = re.search(pattern, self.text, re.IGNORECASE)
            if prev_match:
                prev_str = prev_match.group(1).replace(',', '')
                data["previous_balance"] = float(prev_str)
                break
        
        return data
    
    def _parse_hdfc(self) -> Dict[str, any]:
        data = {
            "issuer": "HDFC Bank",
            "statement_date": None,
            "due_date": None,
            "total_amount_due": None,
            "card_last_4": None,
            "credit_limit": None
        }
        
        date_match = re.search(r'Statement Date:\s*(\d{2}/\d{2}/\d{4})', self.text, re.IGNORECASE | re.DOTALL)
        if date_match:
            data["statement_date"] = date_match.group(1)
            
        due_table_match = re.search(
            r'Payment Due Date\s+Total Dues\s+Minimum Amount Due.*?(\d{2}/\d{2}/\d{4})\s+([\d,]+\.\d{2})',
            self.text, re.IGNORECASE | re.DOTALL
        )
        if due_table_match:
            data["due_date"] = due_table_match.group(1)
            amount_str = due_table_match.group(2).replace(',', '')
            data["total_amount_due"] = float(amount_str)

        card_match = re.search(r'Card No:\s*\d{4}\s+\d{2}XX\s+XXXX\s+(\d{4})', self.text, re.IGNORECASE | re.DOTALL)
        if card_match:
            data["card_last_4"] = card_match.group(1)
            
        credit_limit_match = re.search(
            r'Credit Limit\s+Available Credit Limit\s+Available Cash Limit.*?([\d,]+)',
            self.text, re.IGNORECASE | re.DOTALL
        )
        if credit_limit_match:
            limit_str = credit_limit_match.group(1).replace(',', '')
            data["credit_limit"] = float(limit_str)
            
        return data


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python parser.py <pdf_file_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    try:
        parser = CreditCardParser(pdf_path)
        print(f"\nDetected Issuer: {parser.issuer}")
        print("\nExtracted Data:")
        print("-" * 50)
        
        result = parser.parse()
        
        for key, value in result.items():
            if key == "statement_period" and result.get("issuer") == "HDFC Bank":
                continue
            if key == "statement_date" and result.get("issuer") != "HDFC Bank":
                continue
            if key == "previous_balance" and result.get("issuer") == "HDFC Bank":
                continue
            if key == "credit_limit" and result.get("issuer") != "HDFC Bank":
                continue
                
            print(f"{key:20}: {value}")
        
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

