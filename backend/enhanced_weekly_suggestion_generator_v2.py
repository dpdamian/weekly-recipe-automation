#!/usr/bin/env python3
"""
Enhanced Weekly Suggestion Generator v2 with Expanded Recipe Database
Provides 20+ diverse recipes with true randomization and variety
"""

import random
from typing import List, Dict, Any
from expanded_recipe_generator import ExpandedRecipeGenerator

class EnhancedWeeklySuggestionGeneratorV2:
    def __init__(self):
        self.expanded_generator = ExpandedRecipeGenerator()
        self.recent_selections = []  # Track recent selections to avoid repetition
        
    def generate_weekly_suggestions(self, count=20, include_web=True):
        """Generate diverse weekly recipe suggestions with true randomization"""
        try:
            # Get recipes from expanded database (get more than needed for variety)
            all_recipes = self.expanded_generator.generate_recipes(count * 2)
            
            # Filter out recently selected recipes to ensure variety
            if self.recent_selections:
                filtered_recipes = [r for r in all_recipes if r.get('name') not in self.recent_selections]
                if len(filtered_recipes) >= count:
                    all_recipes = filtered_recipes
            
            # Shuffle for true randomization
            random.shuffle(all_recipes)
            
            # Ensure protein and cuisine variety
            selected_recipes = self._ensure_variety(all_recipes, count)
            
            # Add variety metadata
            for recipe in selected_recipes:
                recipe['source'] = 'expanded_database'
                recipe['freshness'] = 'high'
                
            return {
                'success': True,
                'suggestions': selected_recipes,
                'summary': {
                    'total_count': len(selected_recipes),
                    'source_breakdown': {
                        'expanded_database': len(selected_recipes),
                        'web_search': 0,
                        'user_favorite': 0
                    },
                    'protein_variety': self._get_protein_distribution(selected_recipes),
                    'cuisine_variety': self._get_cuisine_distribution(selected_recipes),
                    'cooking_methods': self._get_cooking_methods(selected_recipes)
                }
            }
            
        except Exception as e:
            print(f"Error generating suggestions: {e}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': []
            }
    
    def _ensure_variety(self, recipes: List[Dict], count: int) -> List[Dict]:
        """Ensure protein and cuisine variety in recipe selection"""
        selected = []
        protein_counts = {}
        cuisine_counts = {}
        
        # First pass: select recipes with variety constraints
        for recipe in recipes:
            if len(selected) >= count:
                break
                
            protein = recipe.get('protein', 'unknown')
            cuisine = recipe.get('cuisine', 'unknown')
            
            protein_count = protein_counts.get(protein, 0)
            cuisine_count = cuisine_counts.get(cuisine, 0)
            
            # Limit each protein to max 3 recipes and each cuisine to max 4
            if protein_count < 3 and cuisine_count < 4:
                selected.append(recipe)
                protein_counts[protein] = protein_count + 1
                cuisine_counts[cuisine] = cuisine_count + 1
        
        # Second pass: fill remaining slots if needed
        if len(selected) < count:
            remaining = [r for r in recipes if r not in selected]
            random.shuffle(remaining)
            selected.extend(remaining[:count - len(selected)])
        
        return selected[:count]
    
    def _get_protein_distribution(self, recipes: List[Dict]) -> Dict[str, int]:
        """Get protein distribution in selected recipes"""
        distribution = {}
        for recipe in recipes:
            protein = recipe.get('protein', 'unknown')
            distribution[protein] = distribution.get(protein, 0) + 1
        return distribution
    
    def _get_cuisine_distribution(self, recipes: List[Dict]) -> Dict[str, int]:
        """Get cuisine distribution in selected recipes"""
        distribution = {}
        for recipe in recipes:
            cuisine = recipe.get('cuisine', 'unknown')
            distribution[cuisine] = distribution.get(cuisine, 0) + 1
        return distribution
    
    def _get_cooking_methods(self, recipes: List[Dict]) -> Dict[str, int]:
        """Get cooking method distribution in selected recipes"""
        distribution = {}
        for recipe in recipes:
            method = recipe.get('cooking_method', 'unknown')
            distribution[method] = distribution.get(method, 0) + 1
        return distribution
    
    def update_recent_selections(self, selected_recipe_names: List[str]):
        """Update recent selections to avoid repetition"""
        self.recent_selections.extend(selected_recipe_names)
        # Keep only last 20 selections to allow some repetition over time
        self.recent_selections = self.recent_selections[-20:]

if __name__ == "__main__":
    generator = EnhancedWeeklySuggestionGeneratorV2()
    
    print("Testing Enhanced Weekly Suggestion Generator V2...")
    print("=" * 60)
    
    # Test multiple generations to verify variety
    for i in range(3):
        print(f"\nGeneration {i+1}:")
        result = generator.generate_weekly_suggestions(20)
        
        if result['success']:
            recipes = result['suggestions']
            summary = result['summary']
            
            print(f"Generated {len(recipes)} recipes:")
            print(f"Protein variety: {summary['protein_variety']}")
            print(f"Cuisine variety: {summary['cuisine_variety']}")
            print(f"Cooking methods: {summary['cooking_methods']}")
            
            print("\nSample recipes:")
            for j, recipe in enumerate(recipes[:5]):
                print(f"{j+1}. {recipe['name']} ({recipe['protein']}, {recipe['cuisine']}, {recipe['cooking_method']})")
            
            # Update recent selections for next generation
            generator.update_recent_selections([r['name'] for r in recipes[:4]])
        else:
            print(f"Error: {result['error']}")
        
        print("-" * 40)

