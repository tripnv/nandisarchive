# Nandi's Archive

A minimalist static site generator.

## Usage

Build the site:
```bash
uv run build.py
```

Preview locally:
```bash
python3 -m http.server 8000 --directory public
```

## Writing

1. Add Markdown files to `posts/`.
2. (Optional) Add frontmatter:
   ```markdown
   ---
   title: "Post Title"
   date: "2025-01-01"
   ---
   ```
3. Run the build script to generate HTML in `public/`.

## Structure

- `posts/`: Markdown source.
- `templates/`: Jinja2 templates.
- `public/`: Generated website.
- `build.py`: Generator script.

## Deployment

Push the `public/` folder to your host (e.g., GitHub Pages).