#!/usr/bin/env python3
"""
Convert XHTML files to Markdown for Emma's Story 3.
"""

import os
import re
from html import unescape

def xhtml_to_md(xhtml_content):
    """Convert XHTML content to Markdown."""
    # Extract title from <title> tag
    title_match = re.search(r'<title>(.*?)</title>', xhtml_content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Untitled"
    
    # Extract story text from <div class="story-text">
    story_match = re.search(r'<div class="story-text">(.*?)</div>\s*</body>', xhtml_content, re.DOTALL)
    if not story_match:
        # Fallback: try to get body content
        story_match = re.search(r'<body[^>]*>(.*?)</body>', xhtml_content, re.DOTALL)
    
    if not story_match:
        return f"# {title}\n\nNo content found."
    
    content = story_match.group(1)
    
    # Convert <h1> to markdown header
    content = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n', content, flags=re.DOTALL)
    
    # Convert <h2> to markdown header
    content = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n', content, flags=re.DOTALL)
    
    # Convert <hr> to markdown horizontal rule
    content = re.sub(r'<hr\s*/?>', '\n---\n', content)
    
    # Convert blockquotes: <p class="quotation">
    content = re.sub(r'<p class="quotation">(.*?)</p>', r'> \1\n', content, flags=re.DOTALL)
    
    # Convert <em> to italic
    content = re.sub(r'<em>(.*?)</em>', r'*\1*', content, flags=re.DOTALL)
    
    # Convert <strong> to bold
    content = re.sub(r'<strong>(.*?)</strong>', r'**\1**', content, flags=re.DOTALL)
    
    # Convert <p> tags to paragraphs
    content = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', content, flags=re.DOTALL)
    
    # Remove remaining HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    
    # Unescape HTML entities
    content = unescape(content)
    
    # Clean up multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Clean up whitespace
    content = content.strip()
    
    return f"# {title}\n\n{content}"

def process_directory(directory):
    """Process all XHTML files in the directory."""
    md_dir = os.path.join(directory, "md")
    os.makedirs(md_dir, exist_ok=True)
    
    xhtml_files = [f for f in os.listdir(directory) if f.endswith('.xhtml')]
    xhtml_files.sort()
    
    for filename in xhtml_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        md_content = xhtml_to_md(content)
        
        md_filename = filename.replace('.xhtml', '.md')
        md_filepath = os.path.join(md_dir, md_filename)
        
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"Converted {filename} to {md_filename}")
    
    print(f"\nConverted {len(xhtml_files)} files to {md_dir}")

if __name__ == "__main__":
    target_dir = r"d:\code ai\to-the-stars\books\艾玛的故事3"
    process_directory(target_dir)
