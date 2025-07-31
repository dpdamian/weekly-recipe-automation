#!/usr/bin/env python3
"""
Simple Grocery List Generator
Works directly with recipe data to generate grocery lists
"""

import json
from datetime import datetime
from typing import List, Dict, Any

class SimpleGroceryGenerator:
    def __init__(self):
        self.department_mapping = {
            # Proteins
            'chicken': 'meat_seafood',
            'beef': 'meat_seafood', 
            'salmon': 'meat_seafood',
            'shrimp': 'meat_seafood',
            'turkey': 'meat_seafood',
            'pork': 'meat_seafood',
            'fish': 'meat_seafood',
            
            # Vegetables
            'broccoli': 'produce',
            'bell pepper': 'produce',
            'zucchini': 'produce',
            'asparagus': 'produce',
            'spinach': 'produce',
            'snap peas': 'produce',
            'carrots': 'produce',
            'onion': 'produce',
            'garlic': 'produce',
            'lemon': 'produce',
            'lime': 'produce',
            'tomato': 'produce',
            'eggplant': 'produce',
            'sweet potato': 'produce',
            'avocado': 'produce',
            'green beans': 'produce',
            'mixed vegetables': 'frozen',
            
            # Grains/Starches
            'rice': 'pantry',
            'quinoa': 'pantry',
            'brown rice': 'pantry',
            'jasmine rice': 'pantry',
            'cauliflower rice': 'frozen',
            'rice noodles': 'pantry',
            
            # Dairy
            'feta cheese': 'dairy',
            'ranch dressing': 'dairy',
            
            # Pantry items
            'olive oil': 'pantry',
            'vegetable oil': 'pantry',
            'sesame oil': 'pantry',
            'honey': 'pantry',
            'brown sugar': 'pantry',
            'cornstarch': 'pantry',
            
            # Condiments
            'soy sauce': 'condiments',
            'teriyaki sauce': 'condiments',
            'buffalo sauce': 'condiments',
            'fish sauce': 'condiments',
            'curry paste': 'condiments',
            
            # Spices
            'salt': 'spices',
            'pepper': 'spices',
            'oregano': 'spices',
            'cumin': 'spices',
            'paprika': 'spices',
            'rosemary': 'spices',
            'thyme': 'spices',
            'sesame seeds': 'spices',
            'cilantro': 'produce'
        }
    
    def generate_grocery_list(self, selected_recipes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate grocery list from selected recipes"""
        
        # Collect all ingredients
        all_ingredients = []
        for recipe in selected_recipes:
            ingredients = recipe.get('ingredients', [])
            for ingredient in ingredients:
                all_ingredients.append(self._parse_ingredient(ingredient))
        
        # Consolidate ingredients
        consolidated = self._consolidate_ingredients(all_ingredients)
        
        # Organize by department
        grocery_list = self._organize_by_department(consolidated)
        
        # Generate equipment reminders
        equipment_reminders = self._get_equipment_reminders(selected_recipes)
        
        # Calculate shopping tips
        shopping_tips = self._generate_shopping_tips(consolidated, selected_recipes)
        
        return {
            'grocery_list': grocery_list,
            'equipment_reminders': equipment_reminders,
            'shopping_tips': shopping_tips,
            'total_items': sum(len(items) for items in grocery_list.values()),
            'total_recipes': len(selected_recipes),
            'generation_date': datetime.now().isoformat()
        }
    
    def _parse_ingredient(self, ingredient_text: str) -> Dict[str, str]:
        """Parse ingredient text into components"""
        # Simple parsing - extract quantity and name
        parts = ingredient_text.strip().split(' ', 2)
        
        if len(parts) >= 3:
            quantity = f"{parts[0]} {parts[1]}"
            name = parts[2]
        elif len(parts) == 2:
            quantity = parts[0]
            name = parts[1]
        else:
            quantity = "1"
            name = ingredient_text
        
        # Clean up name (remove descriptions after commas)
        name = name.split(',')[0].strip()
        
        return {
            'quantity': quantity,
            'name': name,
            'original': ingredient_text
        }
    
    def _consolidate_ingredients(self, ingredients: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Consolidate duplicate ingredients"""
        ingredient_map = {}
        
        for ingredient in ingredients:
            name = ingredient['name'].lower()
            
            if name in ingredient_map:
                # For now, just keep the first occurrence
                # In a more sophisticated version, we'd add quantities
                continue
            else:
                ingredient_map[name] = ingredient
        
        return list(ingredient_map.values())
    
    def _organize_by_department(self, ingredients: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        """Organize ingredients by grocery store department"""
        departments = {
            'produce': [],
            'meat_seafood': [],
            'dairy': [],
            'pantry': [],
            'frozen': [],
            'condiments': [],
            'spices': []
        }
        
        for ingredient in ingredients:
            name = ingredient['name'].lower()
            
            # Find department
            department = 'pantry'  # default
            for key, dept in self.department_mapping.items():
                if key in name:
                    department = dept
                    break
            
            departments[department].append(ingredient)
        
        # Remove empty departments
        return {dept: items for dept, items in departments.items() if items}
    
    def _get_equipment_reminders(self, recipes: List[Dict[str, Any]]) -> List[str]:
        """Generate equipment reminders based on cooking methods"""
        equipment_needed = set()
        
        for recipe in recipes:
            method = recipe.get('cooking_method', 'stove')
            
            if method == 'oven':
                equipment_needed.add('Preheat oven as needed')
            elif method == 'grill':
                equipment_needed.add('Prepare grill for cooking')
            elif method == 'air_fryer':
                equipment_needed.add('Have air fryer ready')
            elif method == 'instant_pot':
                equipment_needed.add('Set up Instant Pot')
            elif method == 'stove':
                equipment_needed.add('Large skillet or pan needed')
        
        return list(equipment_needed)
    
    def _generate_shopping_tips(self, ingredients: List[Dict[str, str]], recipes: List[Dict[str, Any]]) -> List[str]:
        """Generate helpful shopping tips"""
        tips = []
        
        # Ingredient count tip
        total_items = len(ingredients)
        if total_items <= 20:
            tips.append(f"🎯 Efficient shopping! Only {total_items} unique ingredients needed")
        elif total_items <= 30:
            tips.append(f"📝 Moderate list: {total_items} ingredients for 4 delicious meals")
        else:
            tips.append(f"🛒 Full shopping trip: {total_items} ingredients for variety")
        
        # Protein variety tip
        proteins = [recipe.get('protein', 'unknown') for recipe in recipes]
        unique_proteins = len(set(proteins))
        tips.append(f"🥩 Great protein variety: {unique_proteins} different proteins this week")
        
        # Cuisine variety tip
        cuisines = [recipe.get('cuisine', 'unknown') for recipe in recipes]
        unique_cuisines = len(set(cuisines))
        tips.append(f"🌍 Culinary adventure: {unique_cuisines} different cuisine styles")
        
        return tips

if __name__ == "__main__":
    # Test the grocery generator
    generator = SimpleGroceryGenerator()
    
    test_recipes = [
        {
            'name': 'Honey Garlic Chicken',
            'protein': 'chicken',
            'cuisine': 'asian',
            'cooking_method': 'stove',
            'ingredients': [
                '1 lb chicken breast, cubed',
                '2 cups broccoli florets',
                '1 cup jasmine rice',
                '3 tbsp honey'
            ]
        }
    ]
    
    result = generator.generate_grocery_list(test_recipes)
    print(json.dumps(result, indent=2))

