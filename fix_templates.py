import os
import re
import shutil
from datetime import datetime

# Paths to search
template_dir = "./templates"

# Blueprint prefixes to check for
blueprints = {
    'team_': 'team.',
    'player_': 'player.',
    'match_': 'match.',
    'main_': 'main.'
}

def backup_templates():
    """Create a backup of the templates directory"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"./templates_backup_{timestamp}"
    
    if os.path.exists(template_dir):
        shutil.copytree(template_dir, backup_dir)
        print(f"Backup created at: {backup_dir}")
        return True
    return False

def update_templates():
    """Find and update all url_for calls in template files"""
    files_updated = 0
    issues_fixed = 0
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                updated_content = content
                file_updated = False
                
                # Update url_for calls
                for prefix, replacement in blueprints.items():
                    # This pattern matches url_for('prefix_something', ...) 
                    pattern = r"url_for\('(" + prefix + r"[^']+)'([^)]*)\)"
                    
                    def replace_url(match):
                        nonlocal file_updated, issues_fixed
                        endpoint = match.group(1)
                        args = match.group(2)
                        
                        # Only update if it doesn't already have the blueprint prefix
                        if not endpoint.startswith(replacement):
                            # Replace prefix_ with blueprint.
                            new_endpoint = replacement + endpoint[len(prefix):]
                            issues_fixed += 1
                            file_updated = True
                            return f"url_for('{new_endpoint}'{args})"
                        return match.group(0)
                    
                    updated_content = re.sub(pattern, replace_url, updated_content)
                
                if file_updated:
                    files_updated += 1
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    print(f"Updated: {filepath}")
    
    return files_updated, issues_fixed

if __name__ == "__main__":
    print("This script will update all Flask url_for calls in your templates to use blueprint prefixes.")
    response = input("Do you want to proceed? (y/n): ").strip().lower()
    
    if response == 'y':
        # Create backup first
        if backup_templates():
            # Update templates
            files_updated, issues_fixed = update_templates()
            print(f"\nComplete! {issues_fixed} issues fixed across {files_updated} files.")
        else:
            print("Error creating backup. Operation cancelled.")
    else:
        print("Operation cancelled.")