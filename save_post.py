#!/usr/bin/env python3
import sqlite3
import yaml
import sys
import os

# --- 1. Get the Markdown file ---
if len(sys.argv) < 2:
    print("Usage: python3 save_post.py <markdown_file>")
    sys.exit(1)

md_file = sys.argv[1]
if not os.path.exists(md_file):
    print(f"File not found: {md_file}")
    sys.exit(1)

# --- 2. Read the frontmatter ---
with open(md_file, 'r') as f:
    lines = f.read().split('---')
    if len(lines) < 3:
        print("No frontmatter found in the Markdown file!")
        sys.exit(1)
    frontmatter = yaml.safe_load(lines[1])

# --- 3. Connect to SQLite ---
conn = sqlite3.connect('tace.db')
cur = conn.cursor()

# --- 4. Insert metadata ---
cur.execute("""
INSERT INTO posts (title, subtitle, banner, tags, source_local, source_url, briefing)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    frontmatter.get('title'),
    frontmatter.get('subtitle'),
    frontmatter.get('banner'),
    ','.join(frontmatter.get('tags', [])),
    frontmatter.get('source', {}).get('local'),
    frontmatter.get('source', {}).get('url'),
    frontmatter.get('briefing')
))

conn.commit()
conn.close()
print(f"Metadata for '{frontmatter.get('title')}' saved in tace.db")
