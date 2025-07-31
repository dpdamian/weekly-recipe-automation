#!/usr/bin/env python3
"""
Script to add unique IDs to all recipes in real_time_recipe_search.py
"""

import re

def generate_id(name):
    """Generate a unique ID from recipe name"""
    return name.lower().replace(' ', '_').replace('-', '_').replace('&', 'and').replace('(', '').replace(')', '').replace(',', '').replace("'", '')

def add_ids_to_recipes():
    """Add IDs to all recipes in the file"""
    
    # Read the current file
    with open('real_time_recipe_search.py', 'r') as f:
        content = f.read()
    
    # Find all recipe dictionaries and add IDs
    lines = content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Look for recipe name lines
        if "'name':" in line and "'" in line:
            # Extract the recipe name
            name_match = re.search(r"'name':\s*'([^']+)'", line)
            if name_match:
                recipe_name = name_match.group(1)
                recipe_id = generate_id(recipe_name)
                
                # Check if ID already exists in the previous line
                if i > 0 and "'id':" not in lines[i-1]:
                    # Insert ID line before the name line
                    indent = len(line) - len(line.lstrip())
                    id_line = ' ' * indent + f"'id': '{recipe_id}',"
                    new_lines.insert(-1, id_line)  # Insert before the current line
        
        i += 1
    
    # Write the updated content
    with open('real_time_recipe_search.py', 'w') as f:
        f.write('\n'.join(new_lines))
    
    print("Added IDs to all recipes in real_time_recipe_search.py")

if __name__ == "__main__":
    add_ids_to_recipes()

