#!/usr/bin/env python3
"""
Integrated Grocery List System
Combines recipe manager with grocery list generator for complete functionality
"""

import json
from datetime import datetime
from recipe_manager import RecipeManager
from grocery_list_generator import GroceryListGenerator

class IntegratedGrocerySystem:
    def __init__(self):
        self.recipe_manager = RecipeManager()
        self.grocery_generator = GroceryListGenerator()
    
    def generate_final_grocery_list(self, selected_recipe_ids, week_date=None):
        """Generate final grocery list after all 4 recipes are selected"""
        if week_date is None:
            week_date = datetime.now().strftime('%Y-%m-%d')
        
        # Get recipe details
        selected_recipes = []
        for recipe_id in selected_recipe_ids:
            recipe = self.recipe_manager.get_recipe_by_id(recipe_id)
            if recipe:
                selected_recipes.append(recipe)
        
        if len(selected_recipes) != 4:
            raise ValueError(f"Expected 4 recipes, got {len(selected_recipes)}")
        
        # Generate grocery list
        grocery_data = self.grocery_generator.generate_grocery_list(selected_recipes)
        
        # Track selections in recipe manager
        for recipe_id in selected_recipe_ids:
            self.recipe_manager.track_selection(recipe_id, week_date)
        
        # Format for user display
        formatted_list = self.format_grocery_list_for_user(grocery_data, selected_recipes, week_date)
        
        # Save grocery list
        self.save_grocery_list(grocery_data, selected_recipes, week_date)
        
        return {
            'formatted_list': formatted_list,
            'raw_data': grocery_data,
            'selected_recipes': selected_recipes
        }
    
    def format_grocery_list_for_user(self, grocery_data, selected_recipes, week_date):
        """Format grocery list for user-friendly display"""
        lines = []
        
        # Header
        lines.append("# 🛒 Weekly Grocery List")
        lines.append(f"**Week of:** {week_date}")
        lines.append(f"**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        lines.append(f"**Total Recipes:** {len(selected_recipes)}")
        lines.append(f"**Estimated Cost:** {grocery_data['estimated_cost_range']}")
        lines.append("")
        
        # Selected recipes summary
        lines.append("## 📋 This Week's Dinner Menu")
        for i, recipe in enumerate(selected_recipes, 1):
            cooking_method = recipe.get('cooking_method', 'stove').replace('_', ' ').title()
            lines.append(f"{i}. **{recipe['name']}** ({cooking_method})")
            lines.append(f"   - Protein: {recipe.get('protein', 'N/A').title()}")
            lines.append(f"   - Vegetables: {', '.join(recipe.get('vegetables', []))}")
            lines.append(f"   - Starch: {recipe.get('starch', 'N/A').title()}")
            if recipe.get('url'):
                lines.append(f"   - Recipe: {recipe['url']}")
            lines.append("")
        
        # Grocery list by department
        lines.append("## 🛍️ Shopping List by Department")
        lines.append("*Organized for efficient grocery store navigation*")
        lines.append("")
        
        department_emojis = {
            'produce': '🥬',
            'meat_seafood': '🥩',
            'dairy': '🥛',
            'pantry': '🏺',
            'frozen': '🧊',
            'condiments': '🍯',
            'spices': '🌿',
            'other': '📦'
        }
        
        for department, items in grocery_data['grocery_list'].items():
            emoji = department_emojis.get(department, '📦')
            dept_name = department.replace('_', ' ').title()
            lines.append(f"### {emoji} {dept_name}")
            
            for item in items:
                lines.append(f"- [ ] **{item['quantity']} {item['name']}**")
                if len(item['recipes']) > 1:
                    lines.append(f"  *Used in: {', '.join(item['recipes'])}*")
            lines.append("")
        
        # Equipment reminders
        if grocery_data['equipment_reminders']:
            lines.append("## ⚙️ Equipment Reminders")
            for reminder in grocery_data['equipment_reminders']:
                lines.append(f"- {reminder}")
            lines.append("")
        
        # Shopping tips
        if grocery_data['shopping_tips']:
            lines.append("## 💡 Shopping Tips")
            for tip in grocery_data['shopping_tips']:
                lines.append(f"- {tip}")
            lines.append("")
        
        # Ingredient overlap analysis
        lines.append("## 🔄 Ingredient Efficiency")
        overlap_analysis = self.analyze_ingredient_overlap(selected_recipes)
        lines.append(f"- **Shared ingredients:** {overlap_analysis['shared_count']}")
        lines.append(f"- **Total unique ingredients:** {overlap_analysis['total_unique']}")
        lines.append(f"- **Efficiency score:** {overlap_analysis['efficiency_score']:.1f}/10")
        
        if overlap_analysis['shared_ingredients']:
            lines.append(f"- **Most shared:** {', '.join(overlap_analysis['shared_ingredients'][:3])}")
        lines.append("")
        
        # Footer
        lines.append("---")
        lines.append("*Happy cooking! 👨‍🍳👩‍🍳*")
        
        return "\\n".join(lines)
    
    def analyze_ingredient_overlap(self, recipes):
        """Analyze ingredient overlap for efficiency scoring"""
        all_ingredients = []
        for recipe in recipes:
            all_ingredients.extend(recipe.get('ingredients', []))
        
        from collections import Counter
        ingredient_counts = Counter(all_ingredients)
        
        shared_ingredients = [ing for ing, count in ingredient_counts.items() if count > 1]
        total_unique = len(set(all_ingredients))
        shared_count = len(shared_ingredients)
        
        # Calculate efficiency score (0-10)
        if total_unique > 0:
            efficiency_score = (shared_count / total_unique) * 10
        else:
            efficiency_score = 0
        
        return {
            'shared_ingredients': shared_ingredients,
            'shared_count': shared_count,
            'total_unique': total_unique,
            'efficiency_score': efficiency_score
        }
    
    def save_grocery_list(self, grocery_data, selected_recipes, week_date):
        """Save grocery list to file"""
        grocery_record = {
            'week_date': week_date,
            'selected_recipes': [r['id'] for r in selected_recipes],
            'grocery_data': grocery_data,
            'generated_date': datetime.now().isoformat()
        }
        
        # Save to recipe manager database
        if 'grocery_history' not in self.recipe_manager.recipe_db:
            self.recipe_manager.recipe_db['grocery_history'] = []
        
        self.recipe_manager.recipe_db['grocery_history'].append(grocery_record)
        self.recipe_manager.save_database()
        
        # Also save formatted list to file
        formatted_list = self.format_grocery_list_for_user(grocery_data, selected_recipes, week_date)
        filename = f"/home/ubuntu/grocery_list_{week_date}.md"
        
        with open(filename, 'w') as f:
            f.write(formatted_list)
        
        return filename

# Test the integrated system
if __name__ == "__main__":
    system = IntegratedGrocerySystem()
    
    # Test with user's favorite recipes
    user_favorites = system.recipe_manager.get_user_favorites()
    if len(user_favorites) >= 4:
        test_recipe_ids = [recipe['id'] for recipe in user_favorites[:4]]
        
        try:
            result = system.generate_final_grocery_list(test_recipe_ids)
            print("Integrated grocery system test successful!")
            print(f"Generated grocery list with {len(result['raw_data']['grocery_list'])} departments")
            print(f"Estimated cost: {result['raw_data']['estimated_cost_range']}")
        except Exception as e:
            print(f"Test failed: {e}")
    else:
        print("Not enough user favorite recipes for testing")

