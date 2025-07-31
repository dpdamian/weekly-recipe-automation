#!/usr/bin/env python3
"""
Simple Recipe Generator
Provides reliable recipe suggestions without complex web scraping
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Any

class SimpleRecipeGenerator:
    def __init__(self):
        self.recipe_templates = {
            'chicken': [
                {
                    'name': 'Honey Garlic Chicken with Broccoli and Rice',
                    'protein': 'chicken',
                    'cuisine': 'asian',
                    'cooking_method': 'stove',
                    'prep_time': 15,
                    'cook_time': 25,
                    'difficulty': 'easy',
                    'ingredients': [
                        '1 lb chicken breast, cubed',
                        '2 cups broccoli florets',
                        '1 cup jasmine rice',
                        '3 tbsp honey',
                        '3 cloves garlic, minced',
                        '2 tbsp gluten-free soy sauce',
                        '1 tbsp olive oil',
                        'Salt and pepper to taste'
                    ],
                    'url': 'https://example.com/honey-garlic-chicken'
                },
                {
                    'name': 'Mediterranean Chicken with Vegetables and Quinoa',
                    'protein': 'chicken',
                    'cuisine': 'mediterranean',
                    'cooking_method': 'oven',
                    'prep_time': 20,
                    'cook_time': 30,
                    'difficulty': 'easy',
                    'ingredients': [
                        '1 lb chicken thighs',
                        '1 cup quinoa',
                        '1 zucchini, sliced',
                        '1 bell pepper, chopped',
                        '2 tbsp olive oil',
                        '1 tsp oregano',
                        '1 lemon, juiced',
                        'Salt and pepper to taste'
                    ],
                    'url': 'https://example.com/mediterranean-chicken'
                },
                {
                    'name': 'Buffalo Chicken Rice Bowl',
                    'protein': 'chicken',
                    'cuisine': 'american',
                    'cooking_method': 'air_fryer',
                    'prep_time': 10,
                    'cook_time': 20,
                    'difficulty': 'easy',
                    'ingredients': [
                        '1 lb chicken breast',
                        '1 cup brown rice',
                        '1 cup mixed vegetables',
                        '3 tbsp buffalo sauce (gluten-free)',
                        '1 tbsp olive oil',
                        '1 avocado, sliced',
                        'Ranch dressing (gluten-free)',
                        'Salt and pepper to taste'
                    ],
                    'url': 'https://example.com/buffalo-chicken-bowl'
                }
            ],
            'beef': [
                {
                    'name': 'Mongolian Beef with Snap Peas and Rice',
                    'protein': 'beef',
                    'cuisine': 'asian',
                    'cooking_method': 'stove',
                    'prep_time': 15,
                    'cook_time': 20,
                    'difficulty': 'medium',
                    'ingredients': [
                        '1 lb beef sirloin, sliced thin',
                        '1 cup snap peas',
                        '1 cup jasmine rice',
                        '2 tbsp gluten-free soy sauce',
                        '1 tbsp brown sugar',
                        '2 cloves garlic, minced',
                        '1 tbsp cornstarch',
                        '2 tbsp vegetable oil'
                    ],
                    'url': 'https://example.com/mongolian-beef'
                },
                {
                    'name': 'Mediterranean Beef and Vegetable Skillet',
                    'protein': 'beef',
                    'cuisine': 'mediterranean',
                    'cooking_method': 'stove',
                    'prep_time': 15,
                    'cook_time': 25,
                    'difficulty': 'easy',
                    'ingredients': [
                        '1 lb ground beef',
                        '1 cup quinoa',
                        '1 eggplant, diced',
                        '1 tomato, chopped',
                        '2 tbsp olive oil',
                        '1 tsp oregano',
                        '1/2 cup feta cheese',
                        'Salt and pepper to taste'
                    ],
                    'url': 'https://example.com/mediterranean-beef-skillet'
                }
            ],
            'salmon': [
                {
                    'name': 'Teriyaki Salmon with Asparagus and Rice',
                    'protein': 'salmon',
                    'cuisine': 'asian',
                    'cooking_method': 'oven',
                    'prep_time': 10,
                    'cook_time': 20,
                    'difficulty': 'easy',
                    'ingredients': [
                        '4 salmon fillets',
                        '1 lb asparagus',
                        '1 cup brown rice',
                        '3 tbsp gluten-free teriyaki sauce',
                        '1 tbsp sesame oil',
                        '1 tbsp sesame seeds',
                        'Salt and pepper to taste'
                    ],
                    'url': 'https://example.com/teriyaki-salmon'
                },
                {
                    'name': 'Lemon Herb Salmon with Sweet Potato',
                    'protein': 'salmon',
                    'cuisine': 'american',
                    'cooking_method': 'oven',
                    'prep_time': 15,
                    'cook_time': 25,
                    'difficulty': 'easy',
                    'ingredients': [
                        '4 salmon fillets',
                        '2 large sweet potatoes, cubed',
                        '1 cup green beans',
                        '2 tbsp olive oil',
                        '1 lemon, juiced',
                        '1 tsp dried herbs',
                        'Salt and pepper to taste'
                    ],
                    'url': 'https://example.com/lemon-herb-salmon'
                }
            ],
            'turkey': [
                {
                    'name': 'Turkey and Sweet Potato Bowl',
                    'protein': 'turkey',
                    'cuisine': 'american',
                    'cooking_method': 'stove',
                    'prep_time': 15,
                    'cook_time': 20,
                    'difficulty': 'easy',
                    'ingredients': [
                        '1 lb ground turkey',
                        '2 sweet potatoes, cubed',
                        '1 cup spinach',
                        '1 onion, diced',
                        '2 tbsp olive oil',
                        '1 tsp cumin',
                        '1 tsp paprika',
                        'Salt and pepper to taste'
                    ],
                    'url': 'https://example.com/turkey-sweet-potato-bowl'
                }
            ],
            'shrimp': [
                {
                    'name': 'Coconut Shrimp Curry with Rice',
                    'protein': 'shrimp',
                    'cuisine': 'thai',
                    'cooking_method': 'stove',
                    'prep_time': 15,
                    'cook_time': 20,
                    'difficulty': 'medium',
                    'ingredients': [
                        '1 lb large shrimp',
                        '1 cup jasmine rice',
                        '1 can coconut milk',
                        '1 bell pepper, sliced',
                        '1 tbsp curry paste',
                        '1 tbsp fish sauce (gluten-free)',
                        '1 lime, juiced',
                        'Fresh cilantro'
                    ],
                    'url': 'https://example.com/coconut-shrimp-curry'
                }
            ],
            'pork': [
                {
                    'name': 'Pork Tenderloin with Roasted Vegetables',
                    'protein': 'pork',
                    'cuisine': 'american',
                    'cooking_method': 'oven',
                    'prep_time': 20,
                    'cook_time': 30,
                    'difficulty': 'medium',
                    'ingredients': [
                        '1 lb pork tenderloin',
                        '2 cups mixed vegetables',
                        '1 cup quinoa',
                        '2 tbsp olive oil',
                        '1 tsp rosemary',
                        '1 tsp thyme',
                        'Salt and pepper to taste'
                    ],
                    'url': 'https://example.com/pork-tenderloin'
                }
            ]
        }
    
    def generate_recipes(self, count: int = 15) -> List[Dict[str, Any]]:
        """Generate a diverse set of reliable recipes"""
        all_recipes = []
        
        # Collect all recipe templates
        for protein_recipes in self.recipe_templates.values():
            all_recipes.extend(protein_recipes)
        
        # Ensure protein variety
        selected_recipes = []
        protein_counts = {}
        
        # First pass: ensure each protein is represented
        for protein in self.recipe_templates.keys():
            if len(selected_recipes) < count:
                recipe = random.choice(self.recipe_templates[protein]).copy()
                recipe['id'] = f"{protein}_{len(selected_recipes) + 1}"
                recipe['source'] = 'curated_collection'
                recipe['suggested_date'] = datetime.now().isoformat()
                selected_recipes.append(recipe)
                protein_counts[protein] = protein_counts.get(protein, 0) + 1
        
        # Second pass: fill remaining slots with variety
        remaining_recipes = [r for r in all_recipes if r not in [sr for sr in selected_recipes]]
        
        while len(selected_recipes) < count and remaining_recipes:
            # Prefer proteins that have been used less
            min_count = min(protein_counts.values()) if protein_counts else 0
            preferred_proteins = [p for p, c in protein_counts.items() if c <= min_count + 1]
            
            # Filter recipes by preferred proteins
            preferred_recipes = [r for r in remaining_recipes if r['protein'] in preferred_proteins]
            
            if preferred_recipes:
                recipe = random.choice(preferred_recipes).copy()
            else:
                recipe = random.choice(remaining_recipes).copy()
            
            recipe['id'] = f"{recipe['protein']}_{len(selected_recipes) + 1}"
            recipe['source'] = 'curated_collection'
            recipe['suggested_date'] = datetime.now().isoformat()
            
            selected_recipes.append(recipe)
            protein_counts[recipe['protein']] = protein_counts.get(recipe['protein'], 0) + 1
            
            # Remove from remaining to avoid duplicates
            remaining_recipes = [r for r in remaining_recipes if r != recipe]
        
        # Shuffle for variety
        random.shuffle(selected_recipes)
        
        return selected_recipes[:count]

if __name__ == "__main__":
    generator = SimpleRecipeGenerator()
    recipes = generator.generate_recipes(15)
    
    print(f"Generated {len(recipes)} recipes:")
    for recipe in recipes:
        print(f"- {recipe['name']} ({recipe['protein']}, {recipe['cuisine']})")

