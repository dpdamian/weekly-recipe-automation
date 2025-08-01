#!/usr/bin/env python3
"""
Intelligent Grocery List Combiner
Combines ingredient quantities from multiple recipes into a consolidated shopping list
"""

import re
from typing import List, Dict, Any, Tuple
from fractions import Fraction
from collections import defaultdict

class IntelligentGroceryCombiner:
    def __init__(self):
        # Common unit conversions to standardize measurements
        self.unit_conversions = {
            # Volume conversions to cups
            'cup': 1.0,
            'cups': 1.0,
            'c': 1.0,
            'tablespoon': 1/16,
            'tablespoons': 1/16,
            'tbsp': 1/16,
            'tsp': 1/48,
            'teaspoon': 1/48,
            'teaspoons': 1/48,
            'pint': 2.0,
            'pints': 2.0,
            'quart': 4.0,
            'quarts': 4.0,
            'gallon': 16.0,
            'gallons': 16.0,
            'fluid ounce': 1/8,
            'fluid ounces': 1/8,
            'fl oz': 1/8,
            'ml': 1/236.588,  # ml to cups
            'liter': 4.22675,  # liters to cups
            'liters': 4.22675,
            
            # Weight conversions to pounds
            'pound': 1.0,
            'pounds': 1.0,
            'lb': 1.0,
            'lbs': 1.0,
            'ounce': 1/16,
            'ounces': 1/16,
            'oz': 1/16,
            'gram': 1/453.592,  # grams to pounds
            'grams': 1/453.592,
            'g': 1/453.592,
            'kilogram': 2.20462,  # kg to pounds
            'kilograms': 2.20462,
            'kg': 2.20462,
            
            # Count units (no conversion needed)
            'piece': 1.0,
            'pieces': 1.0,
            'item': 1.0,
            'items': 1.0,
            'clove': 1.0,
            'cloves': 1.0,
            'head': 1.0,
            'heads': 1.0,
            'bunch': 1.0,
            'bunches': 1.0,
            'package': 1.0,
            'packages': 1.0,
            'can': 1.0,
            'cans': 1.0,
            'jar': 1.0,
            'jars': 1.0,
            'bottle': 1.0,
            'bottles': 1.0,
        }
        
        # Grocery store departments for organization
        self.departments = {
            'produce': [
                'onion', 'onions', 'garlic', 'ginger', 'lemon', 'lemons', 'lime', 'limes',
                'tomato', 'tomatoes', 'bell pepper', 'bell peppers', 'broccoli', 'carrots',
                'celery', 'spinach', 'lettuce', 'cucumber', 'zucchini', 'asparagus',
                'green onions', 'scallions', 'cilantro', 'parsley', 'basil', 'thyme',
                'oregano', 'rosemary', 'avocado', 'avocados', 'potato', 'potatoes',
                'sweet potato', 'sweet potatoes', 'corn', 'peas', 'green beans',
                'bok choy', 'snap peas', 'mushrooms', 'jalapeño', 'jalapeños'
            ],
            'meat_seafood': [
                'chicken', 'beef', 'salmon', 'fish', 'shrimp', 'turkey', 'pork',
                'ground beef', 'chicken breast', 'chicken thighs', 'flank steak',
                'sirloin', 'white fish', 'cod', 'tilapia'
            ],
            'dairy': [
                'milk', 'cheese', 'butter', 'eggs', 'yogurt', 'cream cheese',
                'sour cream', 'heavy cream', 'cheddar cheese', 'parmesan cheese',
                'mozzarella cheese', 'feta cheese'
            ],
            'pantry': [
                'rice', 'quinoa', 'pasta', 'flour', 'sugar', 'salt', 'pepper',
                'olive oil', 'vegetable oil', 'sesame oil', 'soy sauce', 'honey',
                'vinegar', 'baking powder', 'baking soda', 'vanilla extract',
                'cornstarch', 'brown sugar', 'garlic powder', 'onion powder',
                'paprika', 'cumin', 'chili powder', 'red pepper flakes',
                'coconut milk', 'chicken broth', 'vegetable broth', 'beef broth',
                'canned tomatoes', 'tomato paste', 'coconut oil', 'teriyaki sauce'
            ],
            'frozen': [
                'frozen vegetables', 'frozen peas', 'frozen corn', 'frozen broccoli',
                'frozen mixed vegetables', 'ice'
            ],
            'bakery': [
                'bread', 'rolls', 'tortillas', 'pita bread'
            ],
            'canned_goods': [
                'canned beans', 'black beans', 'kidney beans', 'chickpeas',
                'canned corn', 'canned tomatoes', 'tomato sauce', 'coconut milk',
                'chicken soup', 'cream of chicken soup'
            ]
        }
    
    def parse_ingredient(self, ingredient_text: str) -> Tuple[float, str, str]:
        """
        Parse an ingredient string to extract quantity, unit, and ingredient name
        Returns: (quantity, unit, ingredient_name)
        """
        # Clean up the ingredient text
        ingredient_text = ingredient_text.strip().lower()
        
        # Pattern to match quantity, unit, and ingredient
        # Examples: "2 cups rice", "1 lb chicken breast", "3 cloves garlic"
        pattern = r'^(\d+(?:\.\d+)?|\d+/\d+|\d+\s+\d+/\d+)?\s*([a-zA-Z\s]*?)\s+(.+)$'
        
        match = re.match(pattern, ingredient_text)
        
        if match:
            quantity_str, unit_str, ingredient_name = match.groups()
            
            # Parse quantity (handle fractions)
            if quantity_str:
                quantity = self._parse_quantity(quantity_str.strip())
            else:
                quantity = 1.0
            
            # Clean up unit and ingredient name
            unit = unit_str.strip() if unit_str else ''
            ingredient_name = ingredient_name.strip()
            
            return quantity, unit, ingredient_name
        else:
            # If parsing fails, treat as 1 unit of the whole ingredient
            return 1.0, 'item', ingredient_text
    
    def _parse_quantity(self, quantity_str: str) -> float:
        """Parse quantity string that may contain fractions"""
        try:
            # Handle mixed numbers like "1 1/2"
            if ' ' in quantity_str:
                parts = quantity_str.split()
                if len(parts) == 2:
                    whole = float(parts[0])
                    fraction = Fraction(parts[1])
                    return whole + float(fraction)
            
            # Handle simple fractions like "1/2"
            if '/' in quantity_str:
                return float(Fraction(quantity_str))
            
            # Handle decimal numbers
            return float(quantity_str)
        except:
            return 1.0
    
    def normalize_ingredient_name(self, ingredient_name: str) -> str:
        """Normalize ingredient names for better matching"""
        # Remove common descriptors that don't affect shopping
        descriptors_to_remove = [
            'fresh', 'dried', 'chopped', 'diced', 'sliced', 'minced',
            'crushed', 'ground', 'whole', 'large', 'medium', 'small',
            'boneless', 'skinless', 'trimmed', 'cooked', 'uncooked',
            'raw', 'organic', 'free-range', 'extra virgin'
        ]
        
        words = ingredient_name.split()
        filtered_words = [word for word in words if word not in descriptors_to_remove]
        
        return ' '.join(filtered_words).strip()
    
    def get_department(self, ingredient_name: str) -> str:
        """Determine which grocery department an ingredient belongs to"""
        ingredient_lower = ingredient_name.lower()
        
        for department, items in self.departments.items():
            for item in items:
                if item in ingredient_lower or ingredient_lower in item:
                    return department
        
        return 'other'  # Default department
    
    def combine_quantities(self, ingredients_list: List[Tuple[float, str, str]]) -> Dict[str, Dict]:
        """Combine quantities of the same ingredients"""
        combined = defaultdict(lambda: {'quantity': 0.0, 'unit': '', 'original_units': []})
        
        for quantity, unit, ingredient_name in ingredients_list:
            normalized_name = self.normalize_ingredient_name(ingredient_name)
            
            # Track original units for reference
            combined[normalized_name]['original_units'].append(f"{quantity} {unit}".strip())
            
            # Try to convert to standard units for combination
            if unit in self.unit_conversions:
                # Convert to standard unit
                if unit in ['cup', 'cups', 'c', 'tablespoon', 'tablespoons', 'tbsp', 'tsp', 'teaspoon', 'teaspoons']:
                    # Volume units - convert to cups
                    standard_quantity = quantity * self.unit_conversions[unit]
                    standard_unit = 'cups'
                elif unit in ['pound', 'pounds', 'lb', 'lbs', 'ounce', 'ounces', 'oz', 'gram', 'grams', 'g']:
                    # Weight units - convert to pounds
                    standard_quantity = quantity * self.unit_conversions[unit]
                    standard_unit = 'lbs'
                else:
                    # Count units - keep as is
                    standard_quantity = quantity
                    standard_unit = unit or 'items'
                
                # Combine with existing quantity
                if combined[normalized_name]['unit'] == '' or combined[normalized_name]['unit'] == standard_unit:
                    combined[normalized_name]['quantity'] += standard_quantity
                    combined[normalized_name]['unit'] = standard_unit
                else:
                    # Different unit types - can't combine, keep separate
                    combined[normalized_name]['quantity'] += quantity
                    combined[normalized_name]['unit'] = f"{combined[normalized_name]['unit']}, {unit}"
            else:
                # Unknown unit - just add quantity
                combined[normalized_name]['quantity'] += quantity
                combined[normalized_name]['unit'] = unit or 'items'
        
        return dict(combined)
    
    def format_quantity(self, quantity: float, unit: str) -> str:
        """Format quantity for display"""
        if quantity == int(quantity):
            quantity_str = str(int(quantity))
        else:
            # Try to convert to fraction for common cooking measurements
            frac = Fraction(quantity).limit_denominator(16)
            if abs(float(frac) - quantity) < 0.01:  # Close enough to a simple fraction
                if frac.numerator > frac.denominator:
                    whole = frac.numerator // frac.denominator
                    remainder = frac.numerator % frac.denominator
                    if remainder == 0:
                        quantity_str = str(whole)
                    else:
                        quantity_str = f"{whole} {remainder}/{frac.denominator}"
                else:
                    quantity_str = str(frac)
            else:
                quantity_str = f"{quantity:.1f}"
        
        return f"{quantity_str} {unit}".strip()
    
    def generate_combined_grocery_list(self, selected_recipes: List[Dict]) -> Dict:
        """Generate a combined grocery list from selected recipes"""
        try:
            all_ingredients = []
            recipe_summaries = []
            
            # Extract ingredients from all recipes
            for recipe in selected_recipes:
                ingredients = recipe.get('ingredients', [])
                recipe_summaries.append({
                    'name': recipe.get('name', 'Unknown Recipe'),
                    'ingredient_count': len(ingredients),
                    'protein': recipe.get('protein', 'Unknown'),
                    'cuisine': recipe.get('cuisine', 'Unknown')
                })
                
                # Parse each ingredient
                for ingredient_text in ingredients:
                    if isinstance(ingredient_text, str) and ingredient_text.strip():
                        quantity, unit, ingredient_name = self.parse_ingredient(ingredient_text)
                        all_ingredients.append((quantity, unit, ingredient_name))
            
            # Combine quantities
            combined_ingredients = self.combine_quantities(all_ingredients)
            
            # Organize by department
            grocery_list_by_department = defaultdict(list)
            
            for ingredient_name, details in combined_ingredients.items():
                department = self.get_department(ingredient_name)
                formatted_quantity = self.format_quantity(details['quantity'], details['unit'])
                
                grocery_list_by_department[department].append({
                    'name': ingredient_name,
                    'quantity': formatted_quantity,
                    'original_entries': details['original_units']
                })
            
            # Sort ingredients within each department
            for department in grocery_list_by_department:
                grocery_list_by_department[department].sort(key=lambda x: x['name'])
            
            # Calculate statistics
            total_unique_ingredients = len(combined_ingredients)
            total_original_ingredients = len(all_ingredients)
            combination_efficiency = round((1 - total_unique_ingredients / max(total_original_ingredients, 1)) * 100)
            
            return {
                'success': True,
                'grocery_list': dict(grocery_list_by_department),
                'recipe_summaries': recipe_summaries,
                'statistics': {
                    'total_recipes': len(selected_recipes),
                    'total_unique_ingredients': total_unique_ingredients,
                    'total_original_ingredients': total_original_ingredients,
                    'combination_efficiency': combination_efficiency,
                    'departments_needed': len(grocery_list_by_department)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'grocery_list': {},
                'recipe_summaries': [],
                'statistics': {}
            }

if __name__ == "__main__":
    # Test the intelligent grocery combiner
    combiner = IntelligentGroceryCombiner()
    
    # Sample recipes for testing
    test_recipes = [
        {
            'name': 'Chicken and Rice',
            'ingredients': [
                '1 lb chicken breast',
                '2 cups jasmine rice',
                '1 onion, diced',
                '2 cloves garlic',
                '1 tbsp olive oil'
            ]
        },
        {
            'name': 'Beef Stir Fry',
            'ingredients': [
                '1.5 lbs beef sirloin',
                '1 cup jasmine rice',
                '1/2 onion, sliced',
                '3 cloves garlic',
                '2 tbsp olive oil',
                '1 bell pepper'
            ]
        }
    ]
    
    print("Testing Intelligent Grocery Combiner...")
    print("=" * 50)
    
    result = combiner.generate_combined_grocery_list(test_recipes)
    
    if result['success']:
        print("✅ Successfully generated combined grocery list!")
        print(f"\nStatistics:")
        stats = result['statistics']
        print(f"- Total recipes: {stats['total_recipes']}")
        print(f"- Original ingredients: {stats['total_original_ingredients']}")
        print(f"- Combined to: {stats['total_unique_ingredients']} unique items")
        print(f"- Combination efficiency: {stats['combination_efficiency']}%")
        print(f"- Departments needed: {stats['departments_needed']}")
        
        print(f"\nCombined Grocery List:")
        for department, items in result['grocery_list'].items():
            print(f"\n📍 {department.upper().replace('_', ' ')}:")
            for item in items:
                print(f"  • {item['quantity']} {item['name']}")
                if len(item['original_entries']) > 1:
                    print(f"    (Combined from: {', '.join(item['original_entries'])})")
    else:
        print(f"❌ Error: {result['error']}")

