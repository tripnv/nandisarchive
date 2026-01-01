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
from scripts.date_utils import determine_dates, format_date

# Setup
posts_dir = 'posts'
templates_dir = 'templates'
output_dir = 'docs' 

# Create output directories if they don't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(os.path.join(output_dir, 'posts'), exist_ok=True)

env = Environment(loader=FileSystemLoader(templates_dir))

def build():
    posts = []
    
    # 1. Process Markdown files
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            post_data = frontmatter.load(filepath)
            
            # Get dates using outsourced logic
            created_date, modified_date, show_modified = determine_dates(filepath)

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
