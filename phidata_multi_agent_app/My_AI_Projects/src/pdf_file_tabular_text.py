import pdfplumber
import pandas as pd


# Specify the PDF file path
pdf_path = './global_test_files/WeatherTable.pdf'

# Extract tables from PDF using pdfplumber
tables = []

try:
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extract tables from each page
            page_tables = page.extract_tables()
            if page_tables:
                for j, table in enumerate(page_tables):
                    # Convert to DataFrame
                    df = pd.DataFrame(table[1:], columns=table[0]) if table else pd.DataFrame()
                    tables.append(df)
                    print(f"Page {i+1}, Table {j+1}:")
                    print(df.head())
                    print("\n" + "="*50 + "\n")
    
    if not tables:
        print("No tables found in the PDF.")
        
except Exception as e:
    print(f"Error reading PDF: {e}")
    print("Please check if the PDF file exists and is accessible.")



