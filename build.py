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
            
            # Determine Creation Date (Frontmatter > Git > Filesystem)
            if 'date' in post_data:
                date_obj = post_data['date']
                if isinstance(date_obj, str):
                    try:
                        date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
                    except ValueError:
                        date_obj = datetime.now() # Fallback
                created_date = date_obj
            elif git_created:
                created_date = git_created
            else:
                created_date = datetime.fromtimestamp(os.path.getctime(filepath))

            # Determine Modified Date (Git > Filesystem)
            if git_modified:
                modified_date = git_modified
            else:
                modified_date = datetime.fromtimestamp(os.path.getmtime(filepath))

            # Only show modified if it's significantly different (e.g. diff days or explicit logic)
            # For simplicity, if they are identical (same commit), we hide modified
            show_modified = False
            if git_created and git_modified and git_created != git_modified:
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
