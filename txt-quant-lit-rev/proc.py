import re
import sys

def proc(x):
    """Clean up markdown by removing injected HTML and fixing links/fmts."""
    # Remove span tags while preserving their content.
    x = re.sub(r'<span[^>]*>', '', x)
    x = re.sub(r'</span>', '', x)
    
    # Replace any cashtag links with backticked symbol (including subscripts).
    x = re.sub(
        r'<a[^>]*href="/search\?q=%24([^&]+)[^>]*>\$\1</a>((?:_\d+)?)', 
        r'`\1\2`', 
        x
    )
    
    # Handle doubly-wrapped markdown links (especially arxiv links).
    x = re.sub(
        r'\[(.*?)\]\(\[(.*?)\]\(.*?\)\)', 
        lambda m: (
            f'[{m.group(1)}](https://arxiv.org/abs/'
            f'{m.group(2).split("] ")[0]})'
                if 'arxiv.org' in m.group(0) else
            m.group(0)
        ),
        x
    )
    
    # Clean up any remaining markdown-wrapped links.
    x = re.sub(
        r'\[(.*?)\]\(<a[^>]*>([^<]*?)(?:#[^<]*?)?(?:…)?</a>\)', 
        lambda m:
            f'[{m.group(1)}]({m.group(2).replace("…", "").split("#")[0]})'
        ,
        x
    )
    
    # Convert remaining LaTeX expressions to backticks (note subscripts).
    x = re.sub(r'\$([^$]+?(?:_[^$]+?)?)\$', r'`\1`', x)
    
    # Replace double backticks with single backticks.
    x = x.replace('``', '`')
    
    # Ensure bullets are preceded by newlines, but not inside markdown links.
    def post(match):
        # If we're inside square brackets, don't add newline.
        pos = match.start()
        open_brackets = x[:pos].count('[') - x[:pos].count(']')
        if open_brackets > 0:
            return match.group(0)
        return f'{match.group(1)}\n{match.group(2)}'
    
    x = re.sub(r'([^\n])(- )', post, x)
    
    return x

def main(g, h):
    """Process a markdown file to clean it up."""
    try:
        with open(g, 'r') as f:
            x = f.read()
        
        # Clean up the x
        y = proc(x)
        
        with open(h, 'w') as f:
            f.write(y)

    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean.py input.md output.md")
        sys.exit(1)

    _, g, h = sys.argv
    main(g, h)
