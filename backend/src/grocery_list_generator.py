#!/usr/bin/env python3
"""
Advanced Grocery List Generator
Creates optimized grocery lists with ingredient consolidation and smart organization
"""

import json
import re
from collections import defaultdict, Counter
from fractions import Fraction

class GroceryListGenerator:
    def __init__(self):
        self.load_ingredient_database()
        self.load_cooking_preferences()
        
        # Common ingredient conversions and equivalents
        self.ingredient_equivalents = {
            "chicken breast": ["chicken breasts", "boneless chicken breast"],
            "ground turkey": ["turkey ground", "ground turkey meat"],
            "bell peppers": ["bell pepper", "sweet peppers"],
            "cherry tomatoes": ["cherry tomato", "grape tomatoes"],
            "green beans": ["fresh green beans", "string beans"],
            "snap peas": ["sugar snap peas", "snow peas"],
            "gluten-free soy sauce": ["tamari", "coconut aminos"],
            "olive oil": ["extra virgin olive oil", "EVOO"]
        }
        
        # Quantity parsing patterns
        self.quantity_patterns = [
            r'(\d+(?:\.\d+)?)\s*(cups?|cup)',
            r'(\d+(?:\.\d+)?)\s*(tbsp|tablespoons?|tablespoon)',
            r'(\d+(?:\.\d+)?)\s*(tsp|teaspoons?|teaspoon)',
            r'(\d+(?:\.\d+)?)\s*(lbs?|pounds?|pound)',
            r'(\d+(?:\.\d+)?)\s*(oz|ounces?|ounce)',
            r'(\d+(?:\.\d+)?)\s*(pieces?|piece|fillets?|fillet)',
            r'(\d+(?:\.\d+)?)\s*(cloves?|clove)',
            r'(\d+(?:\.\d+)?)\s*(bunches?|bunch)'
        ]
    
    def load_ingredient_database(self):
        """Load ingredient categorization database"""
        try:
            with open('/home/ubuntu/ingredient_database.json', 'r') as f:
                self.ingredient_db = json.load(f)
        except FileNotFoundError:
            self.ingredient_db = {"categories": {}}
    
    def load_cooking_preferences(self):
        """Load cooking method preferences"""
        try:
            with open('/home/ubuntu/cooking_preferences.json', 'r') as f:
                self.cooking_prefs = json.load(f)
        except FileNotFoundError:
            self.cooking_prefs = {"available_equipment": []}
    
    def generate_grocery_list(self, selected_recipes, optimize_quantities=True):
        """Generate comprehensive grocery list from selected recipes"""
        
        # Extract all ingredients with quantities
        raw_ingredients = self.extract_ingredients_with_quantities(selected_recipes)
        
        # Consolidate similar ingredients
        consolidated_ingredients = self.consolidate_ingredients(raw_ingredients)
        
        # Optimize quantities if requested
        if optimize_quantities:
            consolidated_ingredients = self.optimize_quantities(consolidated_ingredients)
        
        # Categorize by grocery store sections
        categorized_list = self.categorize_ingredients(consolidated_ingredients)
        
        # Add cooking equipment reminders
        equipment_reminders = self.get_equipment_reminders(selected_recipes)
        
        # Generate shopping tips
        shopping_tips = self.generate_shopping_tips(selected_recipes, consolidated_ingredients)
        
        return {
            "grocery_list": categorized_list,
            "equipment_reminders": equipment_reminders,
            "shopping_tips": shopping_tips,
            "total_recipes": len(selected_recipes),
            "estimated_cost_range": self.estimate_cost_range(consolidated_ingredients)
        }
    
    def extract_ingredients_with_quantities(self, recipes):
        """Extract ingredients with quantities from recipes"""
        ingredients_with_quantities = []
        
        for recipe in recipes:
            recipe_name = recipe.get('name', 'Unknown Recipe')
            ingredients = recipe.get('ingredients', [])
            
            for ingredient in ingredients:
                # Try to parse quantity from ingredient string
                quantity, unit, clean_ingredient = self.parse_ingredient_quantity(ingredient)
                
                ingredients_with_quantities.append({
                    'original': ingredient,
                    'clean_name': clean_ingredient,
                    'quantity': quantity,
                    'unit': unit,
                    'recipe': recipe_name,
                    'cooking_method': recipe.get('cooking_method', 'stove')
                })
        
        return ingredients_with_quantities
    
    def parse_ingredient_quantity(self, ingredient_string):
        """Parse quantity, unit, and ingredient name from ingredient string"""
        ingredient_lower = ingredient_string.lower().strip()
        
        # Try to match quantity patterns
        for pattern in self.quantity_patterns:
            match = re.search(pattern, ingredient_lower)
            if match:
                quantity = float(match.group(1))
                unit = match.group(2)
                # Remove the quantity and unit from the ingredient name
                clean_ingredient = re.sub(pattern, '', ingredient_lower).strip()
                return quantity, unit, clean_ingredient
        
        # If no quantity found, assume 1 piece/item
        return 1, 'item', ingredient_lower
    
    def consolidate_ingredients(self, ingredients_with_quantities):
        """Consolidate similar ingredients and sum quantities"""
        consolidated = defaultdict(lambda: {'total_quantity': 0, 'unit': 'item', 'recipes': [], 'cooking_methods': set()})
        
        for ingredient in ingredients_with_quantities:
            clean_name = self.normalize_ingredient_name(ingredient['clean_name'])
            
            # Find the best unit to use (prefer more specific units)
            current_unit = consolidated[clean_name]['unit']
            new_unit = ingredient['unit']
            
            if self.is_better_unit(new_unit, current_unit):
                consolidated[clean_name]['unit'] = new_unit
            
            # Add quantity (convert if necessary)
            quantity_to_add = self.convert_quantity(
                ingredient['quantity'], 
                ingredient['unit'], 
                consolidated[clean_name]['unit']
            )
            
            consolidated[clean_name]['total_quantity'] += quantity_to_add
            consolidated[clean_name]['recipes'].append(ingredient['recipe'])
            consolidated[clean_name]['cooking_methods'].add(ingredient['cooking_method'])
        
        return dict(consolidated)
    
    def normalize_ingredient_name(self, ingredient_name):
        """Normalize ingredient names to consolidate similar items"""
        # Remove common descriptors
        ingredient_name = re.sub(r'\\b(fresh|frozen|organic|raw|cooked|diced|chopped|sliced)\\b', '', ingredient_name)
        ingredient_name = re.sub(r'\\s+', ' ', ingredient_name).strip()
        
        # Check for equivalents
        for standard_name, equivalents in self.ingredient_equivalents.items():
            if ingredient_name in equivalents or ingredient_name == standard_name:
                return standard_name
        
        return ingredient_name
    
    def is_better_unit(self, new_unit, current_unit):
        """Determine if new unit is better than current unit"""
        unit_priority = {
            'item': 1, 'piece': 1, 'fillet': 1, 'clove': 1, 'bunch': 1,
            'tsp': 2, 'teaspoon': 2,
            'tbsp': 3, 'tablespoon': 3,
            'cup': 4,
            'oz': 5, 'ounce': 5,
            'lb': 6, 'pound': 6
        }
        
        return unit_priority.get(new_unit, 1) > unit_priority.get(current_unit, 1)
    
    def convert_quantity(self, quantity, from_unit, to_unit):
        """Convert quantity between units (basic conversions)"""
        # For now, only convert within the same unit type
        # More complex conversions would require ingredient density data
        
        conversions = {
            ('tsp', 'tbsp'): 1/3,
            ('tbsp', 'tsp'): 3,
            ('tbsp', 'cup'): 1/16,
            ('cup', 'tbsp'): 16,
            ('oz', 'lb'): 1/16,
            ('lb', 'oz'): 16
        }
        
        conversion_key = (from_unit, to_unit)
        if conversion_key in conversions:
            return quantity * conversions[conversion_key]
        
        # If no conversion available, return original quantity
        return quantity
    
    def optimize_quantities(self, consolidated_ingredients):
        """Optimize quantities for practical shopping"""
        optimized = {}
        
        for ingredient, data in consolidated_ingredients.items():
            quantity = data['total_quantity']
            unit = data['unit']
            
            # Round to practical quantities
            if unit in ['cup', 'cups']:
                # Round to nearest 1/4 cup
                quantity = round(quantity * 4) / 4
            elif unit in ['tbsp', 'tablespoon', 'tablespoons']:
                # Round to nearest 1/2 tablespoon
                quantity = round(quantity * 2) / 2
            elif unit in ['tsp', 'teaspoon', 'teaspoons']:
                # Round to nearest 1/2 teaspoon
                quantity = round(quantity * 2) / 2
            elif unit in ['lb', 'pound', 'pounds']:
                # Round to nearest 0.25 lb
                quantity = round(quantity * 4) / 4
            elif unit in ['oz', 'ounce', 'ounces']:
                # Round to nearest 0.5 oz
                quantity = round(quantity * 2) / 2
            else:
                # Round to nearest whole number for items/pieces
                quantity = round(quantity)
            
            # Ensure minimum quantity of 1
            quantity = max(quantity, 1)
            
            optimized[ingredient] = {
                **data,
                'total_quantity': quantity,
                'display_quantity': self.format_quantity(quantity, unit)
            }
        
        return optimized
    
    def format_quantity(self, quantity, unit):
        """Format quantity for display"""
        if quantity == int(quantity):
            quantity_str = str(int(quantity))
        else:
            # Try to display as fraction for common cooking measurements
            try:
                frac = Fraction(quantity).limit_denominator(16)
                if frac.denominator <= 16:
                    quantity_str = str(frac)
                else:
                    quantity_str = f"{quantity:.2f}".rstrip('0').rstrip('.')
            except:
                quantity_str = f"{quantity:.2f}".rstrip('0').rstrip('.')
        
        # Handle plural units
        if quantity > 1:
            if unit == 'item':
                return f"{quantity_str} items"
            elif unit in ['piece', 'fillet', 'clove', 'bunch']:
                return f"{quantity_str} {unit}s"
            else:
                return f"{quantity_str} {unit}"
        else:
            return f"{quantity_str} {unit}"
    
    def categorize_ingredients(self, consolidated_ingredients):
        """Categorize ingredients by grocery store sections"""
        categorized = defaultdict(list)
        
        for ingredient, data in consolidated_ingredients.items():
            category = self.get_ingredient_category(ingredient)
            
            categorized[category].append({
                'name': ingredient,
                'quantity': data['display_quantity'],
                'recipes': list(set(data['recipes'])),
                'cooking_methods': list(data['cooking_methods'])
            })
        
        # Sort categories by typical shopping order
        category_order = [
            'produce', 'meat_seafood', 'dairy', 'pantry', 
            'frozen', 'condiments', 'spices', 'other'
        ]
        
        ordered_list = {}
        for category in category_order:
            if category in categorized:
                # Sort items within category alphabetically
                ordered_list[category] = sorted(categorized[category], key=lambda x: x['name'])
        
        return ordered_list
    
    def get_ingredient_category(self, ingredient):
        """Get grocery store category for ingredient"""
        ingredient_lower = ingredient.lower()
        
        for category, subcategories in self.ingredient_db['categories'].items():
            for subcategory, items in subcategories.items():
                if ingredient_lower in [item.lower() for item in items]:
                    return category
        
        # Special handling for common ingredients
        if any(word in ingredient_lower for word in ['sauce', 'oil', 'vinegar']):
            return 'condiments'
        elif any(word in ingredient_lower for word in ['spice', 'herb', 'seasoning']):
            return 'spices'
        
        return 'other'
    
    def get_equipment_reminders(self, recipes):
        """Generate equipment reminders based on selected recipes"""
        equipment_needed = set()
        cooking_methods = set()
        
        for recipe in recipes:
            equipment_needed.update(recipe.get('equipment', []))
            cooking_methods.add(recipe.get('cooking_method', 'stove'))
        
        reminders = []
        
        if 'grill' in equipment_needed:
            reminders.append("🔥 Check grill propane/charcoal levels")
        if 'air_fryer' in equipment_needed:
            reminders.append("🍳 Clean air fryer basket")
        if 'instant_pot' in equipment_needed:
            reminders.append("⚡ Ensure Instant Pot sealing ring is clean")
        if 'sheet_pan' in equipment_needed:
            reminders.append("🍪 Have parchment paper or cooking spray ready")
        
        return reminders
    
    def generate_shopping_tips(self, recipes, ingredients):
        """Generate helpful shopping tips"""
        tips = []
        
        # Protein tips
        proteins = [r.get('protein') for r in recipes]
        protein_count = Counter(proteins)
        
        if len(set(proteins)) >= 3:
            tips.append("💡 You're buying multiple proteins - check for bulk discounts")
        
        # Vegetable tips
        vegetables = []
        for recipe in recipes:
            vegetables.extend(recipe.get('vegetables', []))
        
        if 'broccoli' in vegetables and 'carrots' in vegetables:
            tips.append("🥕 Consider buying pre-cut vegetable mix if available")
        
        # Cooking method tips
        cooking_methods = [r.get('cooking_method') for r in recipes]
        if 'grill' in cooking_methods:
            tips.append("🔥 Summer grilling season - check for seasonal vegetable sales")
        
        # Quantity tips
        total_ingredients = len(ingredients)
        if total_ingredients > 20:
            tips.append("🛒 Large shopping list - consider using grocery pickup/delivery")
        
        return tips
    
    def estimate_cost_range(self, ingredients):
        """Estimate cost range for grocery list"""
        # Basic cost estimation based on ingredient categories
        category_costs = {
            'produce': 3,
            'meat_seafood': 8,
            'dairy': 4,
            'pantry': 2,
            'frozen': 3,
            'condiments': 3,
            'spices': 2,
            'other': 3
        }
        
        total_low = 0
        total_high = 0
        
        for ingredient, data in ingredients.items():
            category = self.get_ingredient_category(ingredient)
            base_cost = category_costs.get(category, 3)
            
            # Adjust for quantity
            quantity = data['total_quantity']
            if quantity > 2:
                multiplier = 1.5
            else:
                multiplier = 1.0
            
            total_low += base_cost * 0.8 * multiplier
            total_high += base_cost * 1.5 * multiplier
        
        return f"${total_low:.0f} - ${total_high:.0f}"

# Test the grocery list generator
if __name__ == "__main__":
    generator = GroceryListGenerator()
    
    # Test with sample recipes
    sample_recipes = [
        {
            "name": "Chicken Stir Fry",
            "ingredients": ["1 lb chicken breast", "2 cups broccoli", "1 cup rice", "2 tbsp soy sauce"],
            "cooking_method": "stove",
            "equipment": ["pan"]
        },
        {
            "name": "Salmon Bowl",
            "ingredients": ["1 lb salmon fillet", "1 cup quinoa", "1 cup broccoli", "1 tbsp olive oil"],
            "cooking_method": "oven",
            "equipment": ["oven"]
        }
    ]
    
    grocery_list = generator.generate_grocery_list(sample_recipes)
    
    print("Generated grocery list:")
    for category, items in grocery_list['grocery_list'].items():
        print(f"\\n{category.upper()}:")
        for item in items:
            print(f"  - {item['quantity']} {item['name']}")
    
    print(f"\\nEstimated cost: {grocery_list['estimated_cost_range']}")
    print(f"Equipment reminders: {grocery_list['equipment_reminders']}")
    print(f"Shopping tips: {grocery_list['shopping_tips']}")

