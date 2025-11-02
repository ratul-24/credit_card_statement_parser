import pdfplumber
import re
import sys


def debug_pdf(pdf_path):
    
    print("="*80)
    print(f"DEBUGGING: {pdf_path}")
    print("="*80)
    
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    print("\n" + "="*80)
    print("EXTRACTED TEXT (First 2000 characters)")
    print("="*80)
    print(text[:2000])
    print("\n...\n")
    
    
    text_lower = text.lower()
    if "icici" in text_lower:
        issuer = "ICICI"
    elif "idfc" in text_lower:
        issuer = "IDFC"
    elif "axis" in text_lower:
        issuer = "AXIS"
    elif "chase" in text_lower:
        issuer = "CHASE"
    else:
        issuer = "UNKNOWN"
    
    print(f"\nDetected Issuer: {issuer}")
    

    print("\n" + "="*80)
    print("SEARCHING FOR KEY PATTERNS")
    print("="*80)
    
    
    print("\n1. ALL DATES FOUND:")
    dates = re.findall(r'\d{2}/\d{2}/\d{4}', text)
    for i, date in enumerate(dates[:10], 1):
        
        idx = text.find(date)
        context = text[max(0, idx-40):idx+40].replace('\n', ' ')
        print(f"   {i}. {date} | Context: ...{context}...")
    

    print("\n2. AMOUNTS WITH SYMBOLS:")
    
    
    dollar_amounts = re.findall(r'\$\s*([\d,]+\.?\d*)', text)
    if dollar_amounts:
        print("   $ Amounts:", dollar_amounts[:10])
    

    rupee_amounts = re.findall(r'(?:r|Rs\.?|₹)\s*([\d,]+\.?\d*)', text, re.IGNORECASE)
    if rupee_amounts:
        print("   Rupee Amounts:", rupee_amounts[:10])

    print("\n3. CARD NUMBER PATTERNS:")
    
    card_patterns = [
        (r'\d{4}\s+XXXX\s+XXXX\s+\d{4}', 'XXXX XXXX XXXX format'),
        (r'\d{8}\*{4}\d{4}', '********1234 format'),
        (r'\d{6}\*{6}\d{4}', '******1234 format'),
    ]
    
    for pattern, desc in card_patterns:
        matches = re.findall(pattern, text)
        if matches:
            print(f"   {desc}: {matches}")
    

    print("\n4. KEY PHRASES:")
    key_phrases = [
        'Total Amount Due',
        'Payment Due Date',
        'Statement Period',
        'Previous Balance',
        'Opening Balance',
        'New Balance',
        'Your Total Amount Due',
    ]
    
    for phrase in key_phrases:
        if phrase.lower() in text_lower:
            idx = text_lower.find(phrase.lower())
            context = text[idx:idx+100].replace('\n', ' | ')
            print(f"   ✓ Found '{phrase}': {context}...")
    
    output_file = f"debug_{pdf_path.split('/')[-1].replace('.pdf', '.txt')}"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"\n✓ Full text saved to: {output_file}")
    
    return text, issuer


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_debug.py <pdf_file>")
        print("\nExample: python quick_debug.py statements/icici.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    debug_pdf(pdf_path)