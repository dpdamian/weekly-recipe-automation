#!/usr/bin/env python3
"""
Endless Recipe Generator
Uses real-time web searches for unlimited recipe variety
Excludes mushrooms per user preference
"""

import random
from typing import List, Dict, Any
from real_time_recipe_search import RealTimeRecipeSearch

class EndlessRecipeGenerator:
    def __init__(self):
        self.web_searcher = RealTimeRecipeSearch()
        self.recent_selections = []  # Track recent selections to avoid repetition
        self.generation_history = []  # Track what was generated to ensure variety
        
    def generate_endless_recipes(self, count=20, force_fresh=True):
        """Generate endless recipes using real-time web searches"""
        try:
            # Get fresh recipes from web search
            fresh_recipes = self.web_searcher.search_fresh_recipes(count=count * 2)
            
            if not fresh_recipes:
                return {
                    'success': False,
                    'error': 'No recipes found from web search',
                    'suggestions': []
                }
            
            # Filter out recently selected recipes if not forcing fresh
            if not force_fresh and self.recent_selections:
                filtered_recipes = [r for r in fresh_recipes if r.get('name') not in self.recent_selections]
                if len(filtered_recipes) >= count:
                    fresh_recipes = filtered_recipes
            
            # Filter out recently generated recipes for more variety
            if self.generation_history:
                recent_names = set()
                for gen in self.generation_history[-3:]:  # Last 3 generations
                    recent_names.update([r.get('name') for r in gen])
                
                varied_recipes = [r for r in fresh_recipes if r.get('name') not in recent_names]
                if len(varied_recipes) >= count:
                    fresh_recipes = varied_recipes
            
            # Shuffle for true randomization
            random.shuffle(fresh_recipes)
            
            # Select final recipes with variety constraints
            selected_recipes = self._ensure_maximum_variety(fresh_recipes, count)
            
            # Add generation metadata
            for recipe in selected_recipes:
                recipe['generation_id'] = len(self.generation_history) + 1
                recipe['freshness'] = 'real_time_web_search'
                recipe['variety_score'] = 'high'
            
            # Track this generation
            self.generation_history.append(selected_recipes)
            
            # Keep only last 5 generations in history
            if len(self.generation_history) > 5:
                self.generation_history = self.generation_history[-5:]
            
            # Calculate variety statistics
            stats = self.web_searcher.get_recipe_stats(selected_recipes)
            
            return {
                'success': True,
                'suggestions': selected_recipes,
                'summary': {
                    'total_count': len(selected_recipes),
                    'source_breakdown': {
                        'real_time_web_search': len(selected_recipes),
                        'cached_database': 0
                    },
                    'protein_variety': stats['protein_variety'],
                    'cuisine_variety': stats['cuisine_variety'],
                    'cooking_methods': stats['cooking_methods'],
                    'excluded_ingredients': stats['excluded_ingredients'],
                    'generation_number': len(self.generation_history),
                    'variety_level': 'maximum'
                }
            }
            
        except Exception as e:
            print(f"Error generating endless recipes: {e}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': []
            }
    
    def _ensure_maximum_variety(self, recipes: List[Dict], count: int) -> List[Dict]:
        """Ensure maximum variety in protein, cuisine, and cooking methods"""
        selected = []
        protein_counts = {}
        cuisine_counts = {}
        method_counts = {}
        
        # Sort recipes by variety potential (prefer less common combinations)
        recipes_with_scores = []
        for recipe in recipes:
            protein = recipe.get('protein', 'unknown')
            cuisine = recipe.get('cuisine', 'unknown')
            method = recipe.get('cooking_method', 'unknown')
            
            # Calculate variety score (lower is more unique)
            variety_score = (
                protein_counts.get(protein, 0) +
                cuisine_counts.get(cuisine, 0) +
                method_counts.get(method, 0)
            )
            recipes_with_scores.append((recipe, variety_score))
        
        # Sort by variety score (most unique first)
        recipes_with_scores.sort(key=lambda x: x[1])
        
        # Select recipes with variety constraints
        for recipe, _ in recipes_with_scores:
            if len(selected) >= count:
                break
                
            protein = recipe.get('protein', 'unknown')
            cuisine = recipe.get('cuisine', 'unknown')
            method = recipe.get('cooking_method', 'unknown')
            
            protein_count = protein_counts.get(protein, 0)
            cuisine_count = cuisine_counts.get(cuisine, 0)
            method_count = method_counts.get(method, 0)
            
            # More generous limits for maximum variety
            if protein_count < 4 and cuisine_count < 5 and method_count < 8:
                selected.append(recipe)
                protein_counts[protein] = protein_count + 1
                cuisine_counts[cuisine] = cuisine_count + 1
                method_counts[method] = method_count + 1
        
        # Fill remaining slots if needed
        if len(selected) < count:
            remaining = [r for r, _ in recipes_with_scores if r not in selected]
            random.shuffle(remaining)
            selected.extend(remaining[:count - len(selected)])
        
        return selected[:count]
    
    def update_recent_selections(self, selected_recipe_names: List[str]):
        """Update recent selections to avoid repetition"""
        self.recent_selections.extend(selected_recipe_names)
        # Keep only last 30 selections to allow some repetition over time
        self.recent_selections = self.recent_selections[-30:]
    
    def get_generation_stats(self) -> Dict:
        """Get statistics about generation history"""
        if not self.generation_history:
            return {'total_generations': 0, 'total_unique_recipes': 0}
        
        all_recipe_names = set()
        for generation in self.generation_history:
            for recipe in generation:
                all_recipe_names.add(recipe.get('name', ''))
        
        return {
            'total_generations': len(self.generation_history),
            'total_unique_recipes': len(all_recipe_names),
            'recent_selections_count': len(self.recent_selections),
            'variety_tracking': 'active'
        }

if __name__ == "__main__":
    generator = EndlessRecipeGenerator()
    
    print("Testing Endless Recipe Generator...")
    print("=" * 60)
    
    # Test multiple generations to verify endless variety
    for i in range(3):
        print(f"\nGeneration {i+1}:")
        result = generator.generate_endless_recipes(count=15, force_fresh=True)
        
        if result['success']:
            recipes = result['suggestions']
            summary = result['summary']
            
            print(f"Generated {len(recipes)} recipes:")
            print(f"Protein variety: {summary['protein_variety']}")
            print(f"Cuisine variety: {summary['cuisine_variety']}")
            print(f"Cooking methods: {summary['cooking_methods']}")
            print(f"Excluded ingredients: {summary['excluded_ingredients']}")
            print(f"Generation number: {summary['generation_number']}")
            
            print("\nSample recipes:")
            for j, recipe in enumerate(recipes[:3]):
                print(f"{j+1}. {recipe['name']} ({recipe['protein']}, {recipe['cuisine']}, {recipe['cooking_method']})")
            
            # Simulate user selecting some recipes
            selected_names = [r['name'] for r in recipes[:2]]
            generator.update_recent_selections(selected_names)
            print(f"Simulated selection: {selected_names}")
        else:
            print(f"Error: {result['error']}")
        
        print("-" * 40)
    
    # Show generation statistics
    stats = generator.get_generation_stats()
    print(f"\nGeneration Statistics:")
    print(f"Total generations: {stats['total_generations']}")
    print(f"Total unique recipes: {stats['total_unique_recipes']}")
    print(f"Recent selections tracked: {stats['recent_selections_count']}")
    print(f"Variety tracking: {stats['variety_tracking']}")

