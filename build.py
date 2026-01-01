# /// script
# dependencies = [
#   "markdown",
#   "jinja2",
#   "python-frontmatter",
#   "gitpython",
# ]
# ///

import os
import markdown
import frontmatter
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import git

# Setup
posts_dir = 'posts'
templates_dir = 'templates'
output_dir = 'docs' 

# Create output directories if they don't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(os.path.join(output_dir, 'posts'), exist_ok=True)

env = Environment(loader=FileSystemLoader(templates_dir))

def get_git_dates(filepath):
    try:
        repo = git.Repo('.', search_parent_directories=True)
        # Get relative path for git
        rel_path = os.path.relpath(filepath, repo.working_dir)
        
        # Get all commits for this file
        commits = list(repo.iter_commits(paths=rel_path))
        
        if not commits:
            return None, None

        # Last commit = Last modified
        last_modified = commits[0].committed_datetime
        # First commit = Created
        created = commits[-1].committed_datetime
        
        return created, last_modified
    except Exception:
        return None, None

def format_date(dt):
    if dt is None:
        return ""
    return dt.strftime('%Y-%m-%d')

def build():
    posts = []
    
    # 1. Process Markdown files
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            post_data = frontmatter.load(filepath)
            
            # Get dates
            git_created, git_modified = get_git_dates(filepath)
            
            # Helper to make naive for comparison
            def to_naive(dt):
                if dt and dt.tzinfo:
                    return dt.replace(tzinfo=None)
                return dt

            git_created = to_naive(git_created)
            git_modified = to_naive(git_modified)

            # Determine Creation Date (Git > Filesystem)
            if git_created:
                created_date = git_created
            else:
                created_date = datetime.fromtimestamp(os.path.getctime(filepath))

            # Determine Modified Date
            # Check if file is dirty (modified locally but not committed)
            is_dirty = False
            try:
                repo = git.Repo('.', search_parent_directories=True)
                if repo.is_dirty(path=filepath):
                    is_dirty = True
            except:
                pass

            if is_dirty:
                modified_date = datetime.fromtimestamp(os.path.getmtime(filepath))
            elif git_modified:
                modified_date = git_modified
            else:
                modified_date = datetime.fromtimestamp(os.path.getmtime(filepath))
            
            # Allow frontmatter override (optional, but requested not to rely on it)
            if 'date' in post_data:
                 date_obj = post_data['date']
                 if isinstance(date_obj, str):
                    try:
                        date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
                    except ValueError:
                        pass
                 if isinstance(date_obj, datetime):
                     created_date = date_obj

            # Logic for showing modified date
            show_modified = False
            # Compare just the dates (ignoring time) to avoid noise
            if modified_date.date() > created_date.date():
                 show_modified = True

            # Convert Markdown to HTML
            content_html = markdown.markdown(post_data.content, extensions=['fenced_code', 'tables'])
            
            # Create a URL for the post
            post_url = os.path.join('posts', filename.replace('.md', '.html'))
            
            post_info = {
                'title': post_data.get('title', 'Untitled'),
                'date': format_date(created_date), # For the Archive list
                'created_display': format_date(created_date),
                'modified_display': format_date(modified_date) if show_modified else None,
                'url': post_url,
                'content': content_html
            }
            posts.append(post_info)
            
            # 2. Render individual post page
            template = env.get_template('post.html')
            output_post = template.render(**post_info)
            
            # Use absolute path for writing file
            write_path = os.path.join(output_dir, post_url)
            with open(write_path, 'w') as f:
                f.write(output_post)

    # Sort posts by creation date descending
    posts.sort(key=lambda x: x['date'], reverse=True)

    # 3. Render Index page
    index_template = env.get_template('index.html')
    output_index = index_template.render(posts=posts)
    with open(os.path.join(output_dir, 'index.html'), 'w') as f:
        f.write(output_index)

    # 4. Handle About page
    about_template = env.get_template('about.html')
    output_about = about_template.render()
    with open(os.path.join(output_dir, 'about.html'), 'w') as f:
        f.write(output_about)

    print(f"Build complete. Processed {len(posts)} posts.")

if __name__ == "__main__":
    build()
