# Nandi's Archive

A minimalist, static personal website built with Python.

## 🚀 Quick Start

1.  **Install Dependencies:**
    Ensure you have `uv` installed (or use standard pip with `requirements.txt` if you prefer).
    ```bash
    # Run the build script (automatically installs dependencies)
    uv run build.py
    ```

2.  **Preview Locally:**
    Serve the `public/` folder to see your site.
    ```bash
    # Serve on http://localhost:8000
    python3 -m http.server 8000 --directory public
    ```

## ✍️ How to Write

### Adding a New Post
1.  Create a Markdown file in `posts/` (e.g., `posts/my-thought.md`).
2.  Add the optional frontmatter (metadata) at the top:
    ```markdown
    ---
    title: "My New Post"
    date: "2025-01-01"  # Optional: Defaults to file creation date
    ---
    
    Write your content here...
    ```
3.  The build script will automatically generate the HTML and add it to the Archive list.

### Adding Images
1.  Place your image in `public/static/images/`.
2.  Reference it in your Markdown using an absolute path:
    ```markdown
    ![My Image](/static/images/photo.jpg)
    ```

### Editing Static Pages
*   **Archive (Home):** Edit `templates/index.html`.
*   **About Me:** Edit `templates/about.html`.
*   **Post Layout:** Edit `templates/post.html`.

## 🛠 How It Works

This project uses a custom Python script (`build.py`) as a Static Site Generator (SSG).

*   **Logic:**
    1.  Reads Markdown files from `posts/`.
    2.  Extracts metadata (Title, Date).
    3.  **Dates:** It attempts to fetch the *Creation Date* and *Last Modified Date* from Git history. If the file is new (untracked), it uses the file system timestamp. You can override this by adding a `date` field to the frontmatter.
    4.  Injects content into Jinja2 templates (`templates/`).
    5.  Outputs the final site to the `public/` directory.

*   **Automation:**
    A `pre-commit` hook is configured to run the build automatically when you commit.
    *   To set it up manually: `uv tool run pre-commit install`
    *   What it does: Runs `build.py` and stages the `public/` folder so your deployed site is always in sync with your source code.

## 📂 Structure

*   `posts/`: Your source content (Markdown).
*   `templates/`: HTML designs (Jinja2 templates).
*   `public/`: **The Website.** This is what gets published.
    *   `static/`: Images and assets live here.
*   `build.py`: The generator script.

## 🚢 Deployment

The `public/` folder contains the full, standalone website.
To deploy, simply push the `public/` folder to your hosting provider (e.g., GitHub Pages).
