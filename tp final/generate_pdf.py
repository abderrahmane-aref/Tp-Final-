import markdown2
import pdfkit
import os

# Read the markdown file
with open('COMPREHENSIVE_PROJECT_REPORT_EN.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Convert markdown to HTML
html = markdown2.markdown(markdown_content, extras=['tables', 'fenced-code-blocks'])

# Create complete HTML document
html_doc = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Comprehensive Project Report: Electronic Medical Records System</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }}
        h1, h2, h3 {{
            color: #2b5876;
        }}
        h1 {{
            border-bottom: 3px solid #2b5876;
            padding-bottom: 10px;
        }}
        h2 {{
            border-bottom: 2px solid #4e4376;
            padding-bottom: 5px;
            margin-top: 30px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        table, th, td {{
            border: 1px solid #ddd;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #2b5876;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .toc {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .page-break {{
            page-break-before: always;
        }}
    </style>
</head>
<body>
    <h1>Comprehensive Project Report: Electronic Medical Records System</h1>
    {html}
</body>
</html>
"""

# Write HTML to file
with open('report.html', 'w', encoding='utf-8') as f:
    f.write(html_doc)

print("HTML report generated successfully!")
print("Please convert the HTML to PDF using an online converter or install wkhtmltopdf for direct PDF generation.")