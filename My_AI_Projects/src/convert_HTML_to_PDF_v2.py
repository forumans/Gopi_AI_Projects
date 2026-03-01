'''
This program reads the HTML content from a URL and converts it to a PDF file.
It uses the wkhtmltopdf tool to convert the HTML to PDF.
It downloads the HTML content first to avoid network issues.
It uses the requests library to download the HTML content, and
the pdfkit library to convert the HTML to PDF.
'''

import pdfkit
import requests

# Since wkhtmltopdf is installed and in PATH, use None for config
config = None

# Convert webpage from a URL or an HTML file
# For a URL:
url = 'https://www.patronus.ai/ai-agent-development/ai-agent-development'
file_name_to_store = '01_ai-agent-development.pdf'
output_pdf = rf'C:\Users\pegop\OneDrive\Desktop\Patronus Agentic AI Tutorial\{file_name_to_store}'

print(f"URL: {url}")
print(f"Output PDF: {output_pdf}")

# Download the HTML content first to avoid network issues
try:
    print("Downloading HTML content...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    html_content = response.text
    print("HTML content downloaded successfully!")
except Exception as e:
    print(f"Error downloading HTML: {e}")
    exit(1)

# Options to tell wkhtmltopdf to use print media type and potentially disable smart shrinking
options = {
    'print-media-type': True,
    'disable-smart-shrinking': True,
    'orientation': 'Landscape', # Force landscape mode for wide tables
}

# Convert from HTML string instead of URL
try:
    print("Converting to PDF...")
    pdfkit.from_string(html_content, output_pdf, options=options, configuration=config)
    print(f"Successfully created PDF: {output_pdf}")
except Exception as e:
    print(f"Error converting to PDF: {e}")
    exit(1)
