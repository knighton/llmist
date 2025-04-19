import re
import sys
import argparse
from pathlib import Path
import html


def get_flags() -> argparse.Namespace:
    x = argparse.ArgumentParser(description='Convert markdown table to styled HTML')
    x.add_argument('input_file', type=str, help='Path to markdown file with table')
    x.add_argument('--output', '-o', type=str, help='Output HTML file path')
    x.add_argument('--title', '-t', type=str, default='The Ultimate Cake Cutting Compendium',
                   help='Title for the HTML page')
    x.add_argument('--dark-bg', type=str, default='#212121', 
                   help='Dark background color (default: #212121)')
    x.add_argument('--text-color', type=str, default='#000000', 
                   help='Text color (default: black)')
    x.add_argument('--table-bg', type=str, default='#f5f5f5', 
                   help='Table background color (default: off-white)')
    return x.parse_args()


def parse_markdown_table(md_content):
    """Extract and parse markdown table into header and rows"""
    # Find the table in the markdown content
    #table_pattern = r'\|\s*(.*?)\s*\|\n\|\s*:?-+:?\s*\|\s*:?-+:?\s*\|.*\n((?:\|.*\|\n?)+)'
    #table_match = re.search(table_pattern, md_content, re.DOTALL)
    
    #if not table_match:
    #    raise ValueError("No markdown table found in the input file")
    
    #header_line = table_match.group(1)
    #rows_text = table_match.group(2)

    header_line, _, *row_texts = md_content.strip().split('\n')
    
    # Parse header
    headers = [h.strip() for h in header_line.split('|') if h.strip()]
    
    # Parse rows
    rows = []
    for row_line in row_texts: #rows_text.strip().split('\n'):
        if row_line.strip():
            # Extract cell content between pipes
            cells = [cell.strip() for cell in row_line.split('|')[1:-1]]
            if cells:
                rows.append(cells)
    
    return headers, rows


def process_cell_content(cell_content):
    """Process cell content to handle stars and HTML"""
    # Replace stars with styled spans
    processed = cell_content.replace("★", '<span class="rating">★</span>')
    processed = processed.replace("☆", '<span class="rating">☆</span>')
    return processed


def generate_html(title, headers, rows, dark_bg, text_color, table_bg):
    """Generate HTML with styled table"""
    # Process header cells
    header_cells = ''.join([f'<th>{html.escape(header)}</th>' for header in headers])
    
    # Process body rows
    table_rows = []
    for row in rows:
        cells = []
        for cell in row:
            # Process the cell content (stars, etc.)
            processed_cell = process_cell_content(cell)
            cells.append(f'<td>{processed_cell}</td>')
        table_rows.append(f'<tr>{"".join(cells)}</tr>')
    
    table_body = '\n                        '.join(table_rows)
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color: {dark_bg};
            color: {text_color};
            font-family: 'Georgia', 'Times New Roman', serif;
        }}
        
        .container {{
            padding: 40px;
            max-width: 100%;
            overflow-x: auto;
            background-color: {dark_bg};
            min-height: 100%;
        }}
        
        h1 {{
            text-align: center;
            text-shadow: 0 0 20px white;
            font-size: 4em;
            color: {text_color};
            font-weight: normal;
            letter-spacing: 1px;
            color: white;
            margin-top: 50px;
            margin-bottom: -10px;
        }}

        h2 {{
            text-align: center;
            font-style: italic;
            color: #fea;
            text-shadow: 0 0 20px #fa4;
        }}
        
        .cake-table-container {{
            width: 95%;
            margin: 0 auto;
            overflow-x: auto;
            border-radius: 15px;
            box-shadow: 
                0 0 15px rgba(255, 255, 255, 0.3),
                0 0 30px rgba(255, 255, 255, 0.2),
                0 0 45px rgba(255, 255, 255, 0.1);
            position: relative;
        }}
        
        .cake-table {{
            border-collapse: separate;
            border-spacing: 0;
            width: 100%;
            background: radial-gradient(ellipse at center, {table_bg} 0%, #e6e6e6 100%);
            border-radius: 15px;
            overflow: hidden;
            transform-style: preserve-3d;
            perspective: 1000px;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
        }}
        
        .cake-table th, .cake-table td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            border-right: 1px solid rgba(0, 0, 0, 0.1);
            color: {text_color};
            position: relative;
        }}
        
        .cake-table th {{
            background-color: rgba(245, 245, 245, 0.9);
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 1px;
            border-bottom: 2px solid rgba(0, 0, 0, 0.2);
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        
        .cake-table tr:nth-child(even) td {{
            background-color: rgba(0, 0, 0, 0.03);
        }}
        
        .cake-table tr:hover td {{
            background-color: rgba(0, 0, 0, 0.05);
        }}
        
        .cake-table tr:first-child th:first-child {{
            border-top-left-radius: 15px;
        }}
        
        .cake-table tr:first-child th:last-child {{
            border-top-right-radius: 15px;
        }}
        
        .cake-table tr:last-child td:first-child {{
            border-bottom-left-radius: 15px;
        }}
        
        .cake-table tr:last-child td:last-child {{
            border-bottom-right-radius: 15px;
        }}
        
        .cake-table td:first-child {{
            font-weight: bold;
        }}
        
        .cake-table tr:nth-child(4n+1) td:first-child {{
            border-left: 3px solid rgba(255, 100, 100, 0.5);
        }}
        
        .cake-table tr:nth-child(4n+2) td:first-child {{
            border-left: 3px solid rgba(100, 100, 255, 0.5);
        }}
        
        .cake-table tr:nth-child(4n+3) td:first-child {{
            border-left: 3px solid rgba(100, 255, 100, 0.5);
        }}
        
        .cake-table tr:nth-child(4n+4) td:first-child {{
            border-left: 3px solid rgba(255, 255, 100, 0.5);
        }}
        
        .rating {{
            color: gold;
            letter-spacing: -2px;
            text-shadow: 1px 1px 1px rgba(0,0,0,0.3);
        }}
        
        /* Cake frosting effect */
        .cake-table::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(45deg, 
                    transparent 65%, 
                    rgba(255, 255, 255, 0.1) 70%, 
                    transparent 75%);
            pointer-events: none;
        }}
        
        /* Make the scrollbar cake-themed */
        ::-webkit-scrollbar {{
            width: 12px;
            height: 12px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {dark_bg};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(to bottom, #f5f5f5, #e6e6e6);
            border-radius: 6px;
            border: 2px solid {dark_bg};
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(to bottom, #ffffff, #f0f0f0);
        }}
        
        /* Make the table responsive */
        @media (max-width: 1200px) {{
            .cake-table th, .cake-table td {{
                padding: 8px 10px;
                font-size: 0.9em;
            }}
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            .cake-table-container {{
                width: 98%;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{html.escape(title)}</h1>
        <h2 class="description">A comprehensive analysis of cake cutting techniques across all dimensions, rendered as an elegant cake-like surface.</h2>
        
        <div class="cake-table-container">
            <table class="cake-table">
                <thead>
                    <tr>
                        {header_cells}
                    </tr>
                </thead>
                <tbody>
                        {table_body}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
    return html_template


def main(flags):
    try:
        # Read markdown file
        input_path = Path(flags.input_file)
        if not input_path.exists():
            print(f"Error: Input file '{flags.input_file}' not found", file=sys.stderr)
            return 1
            
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Parse the markdown table
        headers, rows = parse_markdown_table(md_content)
        
        # Generate HTML
        html_content = generate_html(
            flags.title, headers, rows, 
            flags.dark_bg, flags.text_color, flags.table_bg
        )
        
        # Write HTML to output file
        if flags.output:
            output_path = Path(flags.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"HTML table saved to: {output_path}")
        else:
            # If no output file specified, print to stdout
            print(html_content)
        
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main(get_flags()))
