'''
This program uses a Windows based tool (already installed) to convert HTML to PDF.
It is called: wkhtmltopdf
While installing, it was made sure to add it to the System PATH.
On Power Shell, check if it is installed by typing: wkhtmltopdf --version and 
Verify the path by searching for it: $env:Path -split ';' | Select-String 'wkhtmltopdf'
'''


import pdfkit

# Define the path to your wkhtmltopdf executable if it's not in your system's PATH
# Example for Windows: 
#path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# If wkhtmltopdf is in your PATH, you don't need the config line
config = None 

# Convert the webpage from a URL or an HTML file
# For a URL:
url = 'https://www.patronus.ai/ai-agent-development/agentic-rag'
file_name_to_store = '08_URL_converted_page.pdf'
output_pdf = rf'C:\Users\pegop\OneDrive\Desktop\Patronus Agentic AI Tutorial\{file_name_to_store}'

print(f"URL: {url}")
print(f"Output PDF: {output_pdf}")

# Options to tell wkhtmltopdf to use print media type and potentially disable smart shrinking
options = {
    'print-media-type': True,
    'disable-smart-shrinking': True,
    'orientation': 'Landscape', # Force landscape mode for wide tables
}

pdfkit.from_url(url, output_pdf, options=options, configuration=config)

print(f"Successfully created PDF: {output_pdf}")

# Alternatively, convert from a local HTML file
# with open('your_local_file.html', 'r') as f:
#     html_content = f.read()
# pdfkit.from_string(html_content, output_pdf, options=options, configuration=config)
