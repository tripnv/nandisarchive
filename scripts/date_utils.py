import os
import git
from datetime import datetime

def get_git_dates(filepath):
    """
    Retrieves the creation and modification dates from git history.
    Returns (created_datetime, modified_datetime) or (None, None).
    """
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

def to_naive(dt):
    """Removes timezone information for consistent comparison."""
    if dt and dt.tzinfo:
        return dt.replace(tzinfo=None)
    return dt

def determine_dates(filepath, post_data=None):
    """
    Determines the creation and modification dates for a file,
    using Git history, filesystem status (dirty check), and optional frontmatter overrides.
    
    Returns:
        (created_date, modified_date, show_modified_boolean)
    """
    # Get dates from Git
    git_created, git_modified = get_git_dates(filepath)
    git_created = to_naive(git_created)
    git_modified = to_naive(git_modified)

    # 1. Determine Creation Date (Git > Filesystem)
    if git_created:
        created_date = git_created
    else:
        created_date = datetime.fromtimestamp(os.path.getctime(filepath))

    # 2. Determine Modified Date
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
    
    # 3. Allow frontmatter override (optional)
    if post_data and 'date' in post_data:
        date_obj = post_data['date']
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.strptime(date_obj, '%Y-%m-%d')
            except ValueError:
                pass
        if isinstance(date_obj, datetime):
            created_date = date_obj

    # 4. Logic for showing modified date
    show_modified = False
    # Compare just the dates (ignoring time)
    if modified_date.date() > created_date.date():
            show_modified = True

    return created_date, modified_date, show_modified

def format_date(dt):
    if dt is None:
        return ""
    return dt.strftime('%Y-%m-%d')
