import os
import json
from parser import CreditCardParser
import pandas as pd
from datetime import datetime


class BatchTester:
    
    def __init__(self, statements_dir: str):
        self.statements_dir = statements_dir
        self.results = []
    
    def test_all_statements(self):
        print("=" * 70)
        print("CREDIT CARD STATEMENT PARSER - BATCH TEST")
        print("=" * 70)
        print()
        
        pdf_files = [f for f in os.listdir(self.statements_dir) 
                         if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print(f"No PDF files found in {self.statements_dir}")
            return
        
        print(f"Found {len(pdf_files)} PDF file(s) to process\n")
        
        for idx, pdf_file in enumerate(pdf_files, 1):
            pdf_path = os.path.join(self.statements_dir, pdf_file)
            print(f"\n[{idx}/{len(pdf_files)}] Processing: {pdf_file}")
            print("-" * 70)
            
            try:
                parser = CreditCardParser(pdf_path)
                result = parser.parse()
                result['filename'] = pdf_file
                result['status'] = 'SUCCESS'
                
                self._display_result(result)
                self.results.append(result)
                
            except Exception as e:
                error_result = {
                    'filename': pdf_file,
                    'status': 'ERROR',
                    'error_message': str(e),
                    'issuer': 'UNKNOWN'
                }
                print(f"❌ Error: {str(e)}")
                self.results.append(error_result)
        
        self._generate_summary()
        
        self._export_results()
    
    def _display_result(self, result: dict):
        print(f"✓ Issuer: {result.get('issuer', 'N/A')}")
        
        print(f"  Due Date: {result.get('due_date', 'N/A')}")
        print(f"  Total Amount Due: {result.get('total_amount_due', 'N/A')}")
        print(f"  Card Last 4: {result.get('card_last_4', 'N/A')}")
        
        if result.get('issuer') == 'HDFC Bank':
            print(f"  Statement Date: {result.get('statement_date', 'N/A')}")
            print(f"  Credit Limit: {result.get('credit_limit', 'N/A')}")
        else:
            print(f"  Statement Period: {result.get('statement_period', 'N/A')}")
            print(f"  Previous Balance: {result.get('previous_balance', 'N/A')}")
    
    def _generate_summary(self):
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        
        successful = sum(1 for r in self.results if r['status'] == 'SUCCESS')
        failed = sum(1 for r in self.results if r['status'] == 'ERROR')
        
        if len(self.results) == 0:
            print("No statements were processed.")
            return
            
        print(f"\nTotal Statements Processed: {len(self.results)}")
        print(f"✓ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        
        issuers = {}
        for r in self.results:
            if r['status'] == 'SUCCESS':
                issuer = r.get('issuer', 'Unknown')
                issuers[issuer] = issuers.get(issuer, 0) + 1
        
        if issuers:
            print("\nIssuers Detected:")
            for issuer, count in issuers.items():
                print(f"  • {issuer}: {count} statement(s)")
        
        if successful > 0:
            print("\nData Extraction Completeness:")
            
            common_fields = ['due_date', 'total_amount_due', 'card_last_4']
            other_bank_fields = ['statement_period', 'previous_balance']
            hdfc_fields = ['statement_date', 'credit_limit']
            
            hdfc_successful = sum(1 for r in self.results 
                                if r['status'] == 'SUCCESS' and r.get('issuer') == 'HDFC Bank')
            other_successful = successful - hdfc_successful
            
            for field in common_fields:
                extracted = sum(1 for r in self.results 
                                if r['status'] == 'SUCCESS' and r.get(field) is not None)
                percentage = (extracted / successful) * 100
                print(f"  • {field} (All): {extracted}/{successful} ({percentage:.1f}%)")

            if other_successful > 0:
                for field in other_bank_fields:
                    extracted = sum(1 for r in self.results 
                                    if r['status'] == 'SUCCESS' 
                                    and r.get('issuer') != 'HDFC Bank' 
                                    and r.get(field) is not None)
                    percentage = (extracted / other_successful) * 100
                    print(f"  • {field} (Others): {extracted}/{other_successful} ({percentage:.1f}%)")

            if hdfc_successful > 0:
                for field in hdfc_fields:
                    extracted = sum(1 for r in self.results 
                                    if r['status'] == 'SUCCESS' 
                                    and r.get('issuer') == 'HDFC Bank' 
                                    and r.get(field) is not None)
                    percentage = (extracted / hdfc_successful) * 100
                    print(f"  • {field} (HDFC): {extracted}/{hdfc_successful} ({percentage:.1f}%)")
    
    def _export_results(self):
        if not self.results:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        json_filename = f"parser_results_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n✓ Results exported to: {json_filename}")
        
        try:
            df = pd.DataFrame(self.results)
            excel_filename = f"parser_results_{timestamp}.xlsx"
            df.to_excel(excel_filename, index=False)
            print(f"✓ Results exported to: {excel_filename}")
        except Exception as e:
            print(f"⚠ Could not export to Excel: {e}")


def main():
    import sys
    
    statements_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    if not os.path.isdir(statements_dir):
        print(f"Error: Directory '{statements_dir}' not found")
        sys.exit(1)
    
    tester = BatchTester(statements_dir)
    tester.test_all_statements()


if __name__ == "__main__":
    main()

