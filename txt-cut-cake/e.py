import re
import sys
import argparse
from pathlib import Path
import html


def get_flags() -> argparse.Namespace:
    x = argparse.ArgumentParser(description='Convert markdown table to 3D cake-styled HTML')
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
    x.add_argument('--rotation', type=int, default=15,
                   help='Rotation angle in degrees (default: 15)')
    x.add_argument('--extrusion', type=int, default=25,
                   help='Extrusion depth in pixels (default: 25)')
    return x.parse_args()


def parse_markdown_table(md_content):
    """Extract and parse markdown table into header and rows"""
    header_line, _, *row_texts = md_content.strip().split('\n')
    
    # Parse header
    headers = [h.strip() for h in header_line.split('|') if h.strip()]
    
    # Parse rows
    rows = []
    for row_line in row_texts:
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


def generate_html(title, headers, rows, dark_bg, text_color, table_bg, rotation_angle, extrusion_depth):
    """Generate HTML with styled table that has 3D perspective"""
    # Process header cells
    header_cells = ''.join([f'<th>{html.escape(header)}</th>' for header in headers])
    
    # Process body rows
    table_rows = []
    for i, row in enumerate(rows):
        cells = []
        for j, cell in enumerate(row):
            # Process the cell content (stars, etc.)
            processed_cell = process_cell_content(cell)
            # Add specific class based on position for enhanced 3D effect
            cell_class = f'cell-{i}-{j}'
            cells.append(f'<td class="{cell_class}">{processed_cell}</td>')
        table_rows.append(f'<tr class="row-{i}">{"".join(cells)}</tr>')
    
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
            perspective: 1200px;
            overflow-x: hidden;
        }}
        
        .container {{
            padding: 40px;
            max-width: 100%;
            background-color: {dark_bg};
            min-height: 100%;
            position: relative;
            overflow-x: hidden;
        }}
        
        h1 {{
            text-align: center;
            text-shadow: 0 0 20px white;
            font-size: 4em;
            color: white;
            font-weight: normal;
            letter-spacing: 1px;
            margin-top: 50px;
            margin-bottom: -10px;
            transform: translateZ(50px);
            position: relative;
        }}

        h2 {{
            text-align: center;
            font-style: italic;
            color: #fea;
            text-shadow: 0 0 20px #fa4;
            transform: translateZ(30px);
            position: relative;
            margin-bottom: 60px;
        }}
        
        .scene {{
            width: 95%;
            height: auto;
            margin: 50px auto;
            perspective: 1200px;
            transform-style: preserve-3d;
            position: relative;
        }}
        
        .cake-table-container {{
            width: 100%;
            transform-style: preserve-3d;
            transform: rotateX({rotation_angle}deg);
            position: relative;
            transform-origin: center top;
            box-shadow: 
                0 {extrusion_depth}px 30px rgba(0, 0, 0, 0.5),
                0 0 15px rgba(255, 255, 255, 0.3),
                0 0 30px rgba(255, 255, 255, 0.2),
                0 0 45px rgba(255, 255, 255, 0.1);
            transition: transform 0.5s ease;
        }}
        
        .cake-table-container:hover {{
            transform: rotateX(({rotation_angle} - 5)deg);
        }}
        
        .cake-table {{
            border-collapse: separate;
            border-spacing: 0;
            width: 100%;
            background: radial-gradient(ellipse at center, {table_bg} 0%, #e6e6e6 100%);
            border-radius: 15px 15px 0 0;
            overflow: hidden;
            position: relative;
            transform-style: preserve-3d;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
        }}
        
        /* Create the extruded cake bottom effect */
        .cake-bottom {{
            position: absolute;
            width: 100%;
            height: {extrusion_depth}px;
            background: linear-gradient(to bottom, #d9d9d9, #999);
            bottom: -{extrusion_depth}px;
            left: 0;
            transform-origin: top;
            transform: rotateX(-90deg);
            border-radius: 0 0 15px 15px;
            box-shadow: inset 0 5px 20px rgba(0,0,0,0.2);
        }}
        
        /* Create side walls for the cake */
        .cake-side-left, .cake-side-right {{
            position: absolute;
            width: {extrusion_depth}px;
            height: 100%;
            background: linear-gradient(to right, #d9d9d9, #bbb);
            top: 0;
            transform-origin: left;
        }}
        
        .cake-side-left {{
            left: 0;
            transform: rotateY(90deg) translateX(-{extrusion_depth}px);
            border-radius: 15px 0 0 0;
        }}
        
        .cake-side-right {{
            right: -{extrusion_depth}px;
            transform: rotateY(90deg);
            background: linear-gradient(to left, #d9d9d9, #bbb);
            border-radius: 0 15px 0 0;
        }}
        
        .cake-side-bottom {{
            position: absolute;
            width: 100%;
            height: {extrusion_depth}px;
            background: linear-gradient(to top, #d9d9d9, #bbb);
            bottom: 0;
            left: 0;
            transform-origin: bottom;
            transform: rotateX(90deg) translateY({extrusion_depth}px);
        }}
        
        .cake-table th, .cake-table td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            border-right: 1px solid rgba(0, 0, 0, 0.1);
            color: {text_color};
            position: relative;
            transform-style: preserve-3d;
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
            transform: translateZ(2px);
            box-shadow: 0 5px 10px rgba(0,0,0,0.05);
        }}
        
        /* Subtle row elevation effect for 3D appearance */
        .cake-table tr {{
            transform-style: preserve-3d;
            position: relative;
        }}
        
        .cake-table tr:nth-child(odd) td {{
            background-color: rgba(255, 255, 255, 0.6);
            transform: translateZ(1px);
        }}
        
        .cake-table tr:nth-child(even) td {{
            background-color: rgba(248, 248, 248, 0.8);
            transform: translateZ(0.5px);
        }}
        
        .cake-table tr:hover td {{
            background-color: rgba(255, 245, 220, 0.9);
            transform: translateZ(3px);
            box-shadow: 0 0 10px rgba(255, 180, 60, 0.2);
            transition: all 0.3s ease;
        }}
        
        .cake-table tr:first-child th:first-child {{
            border-top-left-radius: 15px;
        }}
        
        .cake-table tr:first-child th:last-child {{
            border-top-right-radius: 15px;
        }}
        
        .cake-table td:first-child {{
            font-weight: bold;
            z-index: 2;
            background-color: rgba(255, 255, 255, 0.9);
            box-shadow: 2px 0 5px rgba(0,0,0,0.05);
        }}
        
        .cake-table tr:nth-child(4n+1) td:first-child {{
            border-left: 3px solid rgba(255, 100, 100, 0.7);
        }}
        
        .cake-table tr:nth-child(4n+2) td:first-child {{
            border-left: 3px solid rgba(100, 100, 255, 0.7);
        }}
        
        .cake-table tr:nth-child(4n+3) td:first-child {{
            border-left: 3px solid rgba(100, 255, 100, 0.7);
        }}
        
        .cake-table tr:nth-child(4n+4) td:first-child {{
            border-left: 3px solid rgba(255, 255, 100, 0.7);
        }}
        
        .rating {{
            color: gold;
            letter-spacing: -2px;
            text-shadow: 1px 1px 1px rgba(0,0,0,0.3);
            display: inline-block;
            transform: translateZ(1px);
        }}
        
        /* Cake frosting effect */
        .cake-frosting {{
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
            border-radius: 15px 15px 0 0;
        }}
        
        /* Add cake texture */
        .cake-texture {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: radial-gradient(circle at 10% 10%, 
                rgba(255, 255, 255, 0.1) 10%, 
                transparent 10.5%),
                radial-gradient(circle at 20% 30%, 
                rgba(255, 255, 255, 0.1) 5%, 
                transparent 5.5%),
                radial-gradient(circle at 30% 50%, 
                rgba(255, 255, 255, 0.1) 8%, 
                transparent 8.5%),
                radial-gradient(circle at 60% 20%, 
                rgba(255, 255, 255, 0.1) 7%, 
                transparent 7.5%),
                radial-gradient(circle at 70% 40%, 
                rgba(255, 255, 255, 0.1) 4%, 
                transparent 4.5%),
                radial-gradient(circle at 90% 90%, 
                rgba(255, 255, 255, 0.1) 6%, 
                transparent 6.5%);
            pointer-events: none;
            opacity: 0.8;
            border-radius: 15px 15px 0 0;
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
            
            .scene {{
                width: 98%;
            }}
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 3em;
            }}
            
            .cake-table-container {{
                transform: rotateX({rotation_angle/2}deg);
            }}
        }}
        
        /* Add a shadow under the cake */
        .cake-shadow {{
            position: absolute;
            width: 90%;
            height: 20px;
            background: radial-gradient(ellipse at center, rgba(0,0,0,0.3) 0%, transparent 70%);
            bottom: -{extrusion_depth - 10}px;
            left: 5%;
            border-radius: 50%;
            filter: blur(8px);
            z-index: -1;
            transform: rotateX({rotation_angle}deg) scale(1, 0.3);
        }}
        
        /* Wrapper to help with scrolling in 3D environment */
        .table-scroll-wrapper {{
            width: 100%;
            overflow-x: auto;
            transform-style: preserve-3d;
            -webkit-mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
            mask-image: linear-gradient(to right, transparent, black 5%, black 95%, transparent);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{html.escape(title)}</h1>
        <h2 class="description">A comprehensive analysis of cake cutting techniques across all dimensions, rendered as an elegant cake-like surface.</h2>
        
        <div class="scene">
            <div class="cake-table-container">
                <div class="table-scroll-wrapper">
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
                
                <!-- 3D cake elements -->
                <div class="cake-frosting"></div>
                <div class="cake-texture"></div>
                <div class="cake-bottom"></div>
                <div class="cake-side-left"></div>
                <div class="cake-side-right"></div>
                <div class="cake-shadow"></div>
            </div>
        </div>
    </div>
    
    <script>
        // Optional: Add a slight movement to the cake based on mouse position
        document.addEventListener('DOMContentLoaded', function() {{
            const cakeContainer = document.querySelector('.cake-table-container');
            const scene = document.querySelector('.scene');
            
            if (cakeContainer && scene) {{
                scene.addEventListener('mousemove', function(e) {{
                    const rect = scene.getBoundingClientRect();
                    const x = e.clientX - rect.left; // x position within the scene
                    const y = e.clientY - rect.top;  // y position within the scene
                    
                    const rotateY = (x - rect.width / 2) * 0.01; // Subtle rotation
                    const rotateX = {rotation_angle} + (y - rect.height / 2) * 0.01;
                    
                    cakeContainer.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
                }});
                
                // Reset when mouse leaves
                scene.addEventListener('mouseleave', function() {{
                    cakeContainer.style.transform = `rotateX({rotation_angle}deg) rotateY(0deg)`;
                }});
            }}
        }});
    </script>
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
            flags.dark_bg, flags.text_color, flags.table_bg,
            flags.rotation, flags.extrusion
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
