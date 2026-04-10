#!/usr/bin/env python3
"""Convert Markdown files to HTML with Chinese-friendly styling."""

import re

def convert_markdown_to_html(markdown_content, title):
    """Convert markdown content to HTML with styling."""

    html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "Helvetica Neue", sans-serif;
            line-height: 1.8;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            color: #333;
            background-color: #f5f5f5;
        }}
        .document-container {{
            background: white;
            padding: 60px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1a1a1a;
            border-bottom: 3px solid #1890ff;
            padding-bottom: 15px;
            margin-top: 0;
            font-size: 28px;
        }}
        h2 {{
            color: #1a1a1a;
            border-left: 4px solid #1890ff;
            padding-left: 15px;
            margin-top: 40px;
            font-size: 22px;
        }}
        h3 {{
            color: #333;
            margin-top: 30px;
            font-size: 18px;
            font-weight: 600;
        }}
        h4 {{
            color: #555;
            margin-top: 20px;
            font-size: 16px;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e8e8e8;
            margin: 30px 0;
        }}
        p {{
            margin: 15px 0;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
        strong {{
            color: #c7254e;
            font-weight: 600;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 14px;
        }}
        th, td {{
            border: 1px solid #e8e8e8;
            padding: 12px 15px;
            text-align: left;
        }}
        th {{
            background-color: #fafafa;
            font-weight: 600;
            color: #333;
        }}
        tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        code {{
            background-color: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "SF Mono", "Consolas", "Monaco", monospace;
            font-size: 14px;
            color: #c7254e;
        }}
        pre {{
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 13px;
            line-height: 1.5;
            margin: 20px 0;
        }}
        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}
        .mermaid {{
            background-color: #fafafa;
            padding: 20px;
            border-radius: 6px;
            text-align: center;
            margin: 20px 0;
        }}
        blockquote {{
            border-left: 4px solid #1890ff;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #f0f7ff;
            color: #555;
        }}
        a {{
            color: #1890ff;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="document-container">
{content}
    </div>
</body>
</html>'''

    content = convert_content(markdown_content)
    return html_template.format(title=title, content=content)

def convert_content(markdown):
    """Convert markdown content to HTML."""
    lines = markdown.split('\n')
    result = []
    i = 0
    in_code_block = False
    code_block_content = []

    while i < len(lines):
        line = lines[i]

        # Code block handling
        if line.strip().startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_block_content = []
            else:
                # End code block
                result.append('<pre><code>' + '\n'.join(code_block_content) + '</code></pre>')
                in_code_block = False
            i += 1
            continue

        if in_code_block:
            code_block_content.append(escape_html(line))
            i += 1
            continue

        # Headers
        if line.startswith('# '):
            result.append('<h1>' + line[2:] + '</h1>')
        elif line.startswith('## '):
            result.append('<h2>' + line[3:] + '</h2>')
        elif line.startswith('### '):
            result.append('<h3>' + line[4:] + '</h3>')
        elif line.startswith('#### '):
            result.append('<h4>' + line[5:] + '</h4>')

        # Horizontal rule
        elif line.strip() == '---':
            result.append('<hr>')

        # Table handling
        elif line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            result.append(convert_table(table_lines))
            continue

        # List items
        elif line.strip().startswith('- [ ]'):
            result.append('<li><input type="checkbox" disabled> ' + line.strip()[6:] + '</li>')
        elif line.strip().startswith('- '):
            result.append('<li>' + line.strip()[2:] + '</li>')
        elif re.match(r'^\d+\. ', line.strip()):
            match = re.match(r'^(\d+)\. (.*)', line.strip())
            if match:
                result.append('<li>' + match.group(2) + '</li>')

        # Empty line
        elif line.strip() == '':
            result.append('')

        # Regular paragraph
        else:
            result.append('<p>' + convert_inline(line) + '</p>')

        i += 1

    # Wrap consecutive <li> items in <ul>
    output = '\n'.join(result)
    output = wrap_lists(output)

    return output

def convert_table(lines):
    """Convert markdown table to HTML."""
    if len(lines) < 2:
        return ''

    html = '<table>'

    for idx, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]

        if idx == 0:  # Header
            html += '<thead><tr>'
            for cell in cells:
                cell_content = cell.replace('**', '').replace(':', '')
                html += '<th>' + cell_content + '</th>'
            html += '</tr></thead><tbody>'
        elif idx == 1:  # Separator
            continue  # Skip separator
        else:  # Body
            html += '<tr>'
            for cell in cells:
                html += '<td>' + convert_inline(cell) + '</td>'
            html += '</tr>'

    html += '</tbody></table>'
    return html

def convert_inline(text):
    """Convert inline markdown elements to HTML."""
    # Bold: **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

    # Inline code: `code`
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

    return text

def wrap_lists(text):
    """Wrap consecutive list items in <ul> tags."""
    lines = text.split('\n')
    result = []
    in_list = False
    list_items = []

    for line in lines:
        if line.startswith('<li>'):
            if not in_list:
                in_list = True
                list_items = []
            list_items.append(line)
        else:
            if in_list:
                result.append('<ul>' + '\n'.join(list_items) + '</ul>')
                in_list = False
                list_items = []
            result.append(line)

    if in_list:
        result.append('<ul>' + '\n'.join(list_items) + '</ul>')

    return '\n'.join(result)

def escape_html(text):
    """Escape HTML special characters."""
    return (text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#39;'))

if __name__ == '__main__':
    import os

    files = [
        ('02_需求概要设计文档.md', '02_需求概要设计文档.html', '智能招投标审查平台 - 需求概要设计文档'),
        ('03_项目里程碑计划.md', '03_项目里程碑计划.html', '智能招投标审查平台 - 项目里程碑计划'),
        ('04_产品交付设计图.md', '04_产品交付设计图.html', '智能招投标审查平台 - 产品交付设计图'),
        ('05_LLM推理私有化硬件清单.md', '05_LLM推理私有化硬件清单.html', 'LLM推理硬件清单'),
    ]

    for md_file, html_file, title in files:
        md_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), md_file)
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), html_file)

        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        html_content = convert_markdown_to_html(md_content, title)

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f'Converted: {md_file} -> {html_file}')