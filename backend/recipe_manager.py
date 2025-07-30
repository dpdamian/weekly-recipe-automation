#!/usr/bin/env python3
"""
Recipe Management System
Core system for managing weekly recipe suggestions, user selections, and preferences
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter

class RecipeManager:
    def __init__(self):
        self.recipe_db_path = '/home/ubuntu/recipe_database.json'
        self.ingredient_db_path = '/home/ubuntu/ingredient_database.json'
        self.load_databases()
    
    def load_databases(self):
        """Load recipe and ingredient databases"""
        try:
            with open(self.recipe_db_path, 'r') as f:
                self.recipe_db = json.load(f)
        except FileNotFoundError:
            self.recipe_db = {"recipes": [], "user_preferences": {}, "recipe_history": {}}
        
        try:
            with open(self.ingredient_db_path, 'r') as f:
                self.ingredient_db = json.load(f)
        except FileNotFoundError:
            self.ingredient_db = {"categories": {}}
    
    def save_database(self):
        """Save recipe database to file"""
        with open(self.recipe_db_path, 'w') as f:
            json.dump(self.recipe_db, f, indent=2)
    
    def add_recipe(self, recipe):
        """Add a new recipe to the database"""
        recipe['id'] = f"recipe_{len(self.recipe_db['recipes']) + 1:03d}"
        recipe['added_date'] = datetime.now().isoformat()
        self.recipe_db['recipes'].append(recipe)
        self.save_database()
        return recipe['id']
    
    def get_user_favorites(self):
        """Get user's favorite recipes"""
        return [r for r in self.recipe_db['recipes'] if r.get('source') == 'user_favorite']
    
    def track_selection(self, recipe_id, week_date):
        """Track a recipe selection for a specific week"""
        if 'recipe_history' not in self.recipe_db:
            self.recipe_db['recipe_history'] = {'selected_recipes': []}
        
        selection = {
            'recipe_id': recipe_id,
            'week_date': week_date,
            'selected_date': datetime.now().isoformat()
        }
        
        self.recipe_db['recipe_history']['selected_recipes'].append(selection)
        self.save_database()
    
    def get_recent_selections(self, weeks=4):
        """Get recipes selected in recent weeks"""
        if 'recipe_history' not in self.recipe_db:
            return []
        
        cutoff_date = datetime.now() - timedelta(weeks=weeks)
        recent_selections = []
        
        for selection in self.recipe_db['recipe_history'].get('selected_recipes', []):
            selection_date = datetime.fromisoformat(selection['selected_date'])
            if selection_date >= cutoff_date:
                recent_selections.append(selection['recipe_id'])
        
        return recent_selections
    
    def calculate_ingredient_overlap(self, recipe_ids):
        """Calculate ingredient overlap between recipes"""
        if not recipe_ids:
            return {}
        
        all_ingredients = []
        recipe_ingredients = {}
        
        for recipe_id in recipe_ids:
            recipe = self.get_recipe_by_id(recipe_id)
            if recipe:
                ingredients = recipe.get('ingredients', [])
                recipe_ingredients[recipe_id] = ingredients
                all_ingredients.extend(ingredients)
        
        ingredient_counts = Counter(all_ingredients)
        overlap_score = sum(count - 1 for count in ingredient_counts.values() if count > 1)
        
        return {
            'overlap_score': overlap_score,
            'shared_ingredients': [ing for ing, count in ingredient_counts.items() if count > 1],
            'total_unique_ingredients': len(set(all_ingredients))
        }
    
    def get_recipe_by_id(self, recipe_id):
        """Get recipe by ID"""
        for recipe in self.recipe_db['recipes']:
            if recipe['id'] == recipe_id:
                return recipe
        return None
    
    def filter_by_protein_variety(self, recipe_ids, max_per_protein=2):
        """Filter recipes to ensure protein variety"""
        protein_counts = defaultdict(int)
        filtered_recipes = []
        
        for recipe_id in recipe_ids:
            recipe = self.get_recipe_by_id(recipe_id)
            if recipe:
                protein = recipe.get('protein', 'unknown')
                if protein_counts[protein] < max_per_protein:
                    filtered_recipes.append(recipe_id)
                    protein_counts[protein] += 1
        
        return filtered_recipes
    
    def generate_grocery_list(self, recipe_ids):
        """Generate organized grocery list from selected recipes"""
        all_ingredients = []
        
        # Collect all ingredients
        for recipe_id in recipe_ids:
            recipe = self.get_recipe_by_id(recipe_id)
            if recipe:
                all_ingredients.extend(recipe.get('ingredients', []))
        
        # Remove duplicates and categorize
        unique_ingredients = list(set(all_ingredients))
        categorized_list = defaultdict(list)
        
        for ingredient in unique_ingredients:
            category = self.categorize_ingredient(ingredient)
            categorized_list[category].append(ingredient)
        
        # Sort categories by typical shopping order
        category_order = ['produce', 'meat_seafood', 'dairy', 'pantry', 'frozen', 'other']
        
        organized_list = {}
        for category in category_order:
            if category in categorized_list:
                organized_list[category] = sorted(categorized_list[category])
        
        return organized_list
    
    def categorize_ingredient(self, ingredient):
        """Categorize ingredient for grocery list"""
        ingredient_lower = ingredient.lower()
        
        for category, subcategories in self.ingredient_db['categories'].items():
            for subcategory, items in subcategories.items():
                if ingredient_lower in [item.lower() for item in items]:
                    return category
        
        return "other"
    
    def update_user_preferences(self, recipe_id, rating):
        """Update user preferences based on recipe rating"""
        recipe = self.get_recipe_by_id(recipe_id)
        if not recipe:
            return
        
        if 'user_preferences' not in self.recipe_db:
            self.recipe_db['user_preferences'] = {}
        
        # Update preferences based on rating
        preferences = self.recipe_db['user_preferences']
        
        # Update protein preferences
        protein = recipe.get('protein')
        if protein:
            if 'favorite_proteins' not in preferences:
                preferences['favorite_proteins'] = {}
            preferences['favorite_proteins'][protein] = preferences['favorite_proteins'].get(protein, 0) + rating
        
        # Update cuisine preferences
        cuisine = recipe.get('cuisine')
        if cuisine:
            if 'favorite_cuisines' not in preferences:
                preferences['favorite_cuisines'] = {}
            preferences['favorite_cuisines'][cuisine] = preferences['favorite_cuisines'].get(cuisine, 0) + rating
        
        self.save_database()

# Test the system
if __name__ == "__main__":
    manager = RecipeManager()
    print("Recipe Manager initialized successfully")
    print(f"Total recipes in database: {len(manager.recipe_db['recipes'])}")
    print(f"User favorite recipes: {len(manager.get_user_favorites())}")
    
    # Test grocery list generation with user favorites
    user_favorites = manager.get_user_favorites()
    if len(user_favorites) >= 2:
        test_recipe_ids = [user_favorites[0]['id'], user_favorites[1]['id']]
        grocery_list = manager.generate_grocery_list(test_recipe_ids)
        print(f"Sample grocery list categories: {list(grocery_list.keys())}")

