import os
import re

# Paths to search
template_dir = "./templates"

# Blueprint prefixes to check for
blueprints = {
    'team_': 'team.',
    'player_': 'player.',
    'match_': 'match.',
    'main_': 'main.'
}

def scan_templates():
    issues_found = []
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Find all url_for calls
                    url_for_pattern = r"url_for\('([^']+)'[^)]*\)"
                    matches = re.findall(url_for_pattern, content)
                    
                    for match in matches:
                        # Check if any route might need a blueprint prefix
                        for prefix, replacement in blueprints.items():
                            if match.startswith(prefix) and not match.startswith(replacement):
                                issues_found.append(f"File: {filepath}\n  Found: url_for('{match}')\n  Should be: url_for('{replacement}{match[len(prefix):]}')")
    
    return issues_found

if __name__ == "__main__":
    issues = scan_templates()
    if issues:
        print(f"Found {len(issues)} potential issues:")
        for issue in issues:
            print(f"\n{issue}")
    else:
        print("No issues found!")