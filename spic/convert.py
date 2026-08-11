import re
import os
import subprocess

def convert_md_to_html(md_path, html_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    lines = md_text.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        
        # Handle horizontal rule
        if stripped == '---':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<hr>')
            continue
            
        # Handle headings
        match_h = re.match(r'^(#{1,6})\s+(.*)$', line)
        if match_h:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            level = len(match_h.group(1))
            heading_text = match_h.group(2).strip()
            
            # Add page break class for specific headings to make PDF print nicely
            if level == 3 and heading_text.startswith('Paper '):
                html_lines.append(f'<h{level} class="page-break">{heading_text}</h{level}>')
            elif level == 2 and heading_text.startswith('Part 2:'):
                html_lines.append(f'<h{level} class="page-break">{heading_text}</h{level}>')
            else:
                html_lines.append(f'<h{level}>{heading_text}</h{level}>')
            continue
            
        # Handle lists
        match_l = re.match(r'^(\*|\-|\d+\.)\s+(.*)$', line)
        if match_l:
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = match_l.group(2).strip()
            # inline bold
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            # inline italic
            content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
            # links
            content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
            html_lines.append(f'<li>{content}</li>')
            continue
            
        # If not a list item, close list if open
        if in_list and stripped != '' and not match_l:
            html_lines.append('</ul>')
            in_list = False
            
        # Handle empty line
        if stripped == '':
            continue
            
        # Regular paragraph
        content = line.strip()
        # inline bold
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        # inline italic
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        # links
        content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
        html_lines.append(f'<p>{content}</p>')
            
    if in_list:
        html_lines.append('</ul>')
        
    html_body = '\n'.join(html_lines)
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Exam Preparation Guide: SPIC</title>
<style>
    body {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        line-height: 1.6;
        color: #2d3748;
        max-width: 850px;
        margin: 40px auto;
        padding: 0 40px;
        font-size: 15px;
    }}
    h1, h2, h3, h4 {{
        color: #1a365d;
        font-weight: bold;
    }}
    h1 {{
        font-size: 2.2em;
        border-bottom: 3px solid #3182ce;
        padding-bottom: 12px;
        margin-top: 40px;
        margin-bottom: 20px;
        text-align: center;
    }}
    h2 {{
        font-size: 1.7em;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 8px;
        margin-top: 35px;
        color: #2b6cb0;
    }}
    h3 {{
        font-size: 1.3em;
        margin-top: 25px;
        border-bottom: 1px solid #edf2f7;
        padding-bottom: 6px;
        color: #2d3748;
    }}
    h4 {{
        font-size: 1.1em;
        margin-top: 20px;
        color: #4a5568;
    }}
    p {{
        margin-bottom: 16px;
        text-align: justify;
    }}
    ul {{
        margin-bottom: 20px;
        padding-left: 25px;
    }}
    li {{
        margin-bottom: 8px;
    }}
    hr {{
        border: 0;
        height: 1px;
        background: #cbd5e0;
        margin: 40px 0;
    }}
    strong {{
        color: #1a202c;
    }}
    code {{
        font-family: Menlo, Monaco, Consolas, monospace;
        background-color: #f7fafc;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.9em;
        border: 1px solid #e2e8f0;
    }}
    .page-break {{
        page-break-before: always;
        margin-top: 0;
        padding-top: 20px;
    }}
    @media print {{
        body {{
            margin: 20px;
            padding: 0;
            font-size: 12pt;
        }}
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    workspace_dir = '/home/s_goto/Documents/Mid/spic'
    md_file = os.path.join(workspace_dir, 'preparation.md')
    html_file = os.path.join(workspace_dir, 'preparation.html')
    pdf_file = os.path.join(workspace_dir, 'preparation.pdf')
    
    print("Converting Markdown to HTML...")
    convert_md_to_html(md_file, html_file)
    
    print("Converting HTML to PDF via LibreOffice...")
    cmd = [
        'libreoffice',
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', workspace_dir,
        html_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("PDF Conversion Successful!")
        # Clean up temporary HTML file
        if os.path.exists(html_file):
            os.remove(html_file)
            print("Cleaned up temporary HTML file.")
    else:
        print("Error during PDF conversion:")
        print(result.stderr)
        print(result.stdout)

if __name__ == '__main__':
    main()
