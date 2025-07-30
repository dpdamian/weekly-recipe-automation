#!/usr/bin/env python3
"""
Recipe Search and Suggestion Engine
Finds new gluten-free recipes and creates personalized recommendations
"""

import json
import random
from datetime import datetime
from collections import defaultdict, Counter

class RecipeSearchEngine:
    def __init__(self):
        self.recipe_sources = [
            "https://www.mamaknowsglutenfree.com/",
            "https://theloopywhisk.com/",
            "https://meaningfuleats.com/",
            "https://www.healthygffamily.com/",
            "https://www.skinnytaste.com/",
            "https://www.flavourandsavour.com/",
            "https://www.jessicagavin.com/",
            "https://kaynutrition.com/",
            "https://www.faithfullyglutenfree.com/",
            "https://grainfreetable.com/"
        ]
        
        # Curated gluten-free recipes based on search results
        self.curated_recipes = [
            {
                "name": "Coconut Chicken Rice Bowl",
                "url": "https://www.skinnytaste.com/coconut-chicken-rice-bowl/",
                "protein": "chicken",
                "vegetables": ["broccoli", "carrots", "snap peas"],
                "starch": "rice",
                "cuisine": "asian",
                "gluten_free": True,
                "ingredients": ["chicken breast", "coconut milk", "rice", "broccoli", "carrots", "snap peas", "garlic", "ginger"],
                "prep_time": 30,
                "difficulty": "easy"
            },
            {
                "name": "Teriyaki Chicken Rice Bowl",
                "url": "https://www.flavourandsavour.com/teriyaki-chicken-rice-bowls-gluten-free/",
                "protein": "chicken",
                "vegetables": ["broccoli", "bell peppers"],
                "starch": "rice",
                "cuisine": "asian",
                "gluten_free": True,
                "ingredients": ["chicken breast", "rice", "broccoli", "bell peppers", "teriyaki sauce", "sesame oil"],
                "prep_time": 25,
                "difficulty": "easy"
            },
            {
                "name": "Mediterranean Salmon Quinoa Bowl",
                "url": "https://www.jessicagavin.com/mediterranean-spiced-salmon-and-vegetable-quinoa/",
                "protein": "salmon",
                "vegetables": ["zucchini", "cherry tomatoes", "olives"],
                "starch": "quinoa",
                "cuisine": "mediterranean",
                "gluten_free": True,
                "ingredients": ["salmon fillet", "quinoa", "zucchini", "cherry tomatoes", "olives", "lemon", "olive oil"],
                "prep_time": 35,
                "difficulty": "medium"
            },
            {
                "name": "Salmon Quinoa Bowl with Kale",
                "url": "https://feedmephoebe.com/salmon-quinoa-bowls-recipe/",
                "protein": "salmon",
                "vegetables": ["kale", "cucumber", "avocado"],
                "starch": "quinoa",
                "cuisine": "healthy",
                "gluten_free": True,
                "ingredients": ["salmon fillet", "quinoa", "kale", "cucumber", "avocado", "tahini", "lemon"],
                "prep_time": 30,
                "difficulty": "easy"
            },
            {
                "name": "Gluten-Free Beef and Broccoli Stir Fry",
                "url": "https://www.faithfullyglutenfree.com/gluten-free-beef-and-broccoli-stir-fry/",
                "protein": "beef",
                "vegetables": ["broccoli", "onions"],
                "starch": "rice",
                "cuisine": "asian",
                "gluten_free": True,
                "ingredients": ["beef strips", "broccoli", "onions", "rice", "gluten-free soy sauce", "garlic", "ginger"],
                "prep_time": 20,
                "difficulty": "easy"
            },
            {
                "name": "Spicy Beef and Vegetable Stir Fry",
                "url": "https://glutenfreeandmore.com/gluten-free-spicy-beef-vegetable-stir-fry/",
                "protein": "beef",
                "vegetables": ["bell peppers", "snap peas", "carrots"],
                "starch": "rice",
                "cuisine": "asian",
                "gluten_free": True,
                "ingredients": ["beef strips", "bell peppers", "snap peas", "carrots", "rice", "chili sauce", "garlic"],
                "prep_time": 25,
                "difficulty": "medium"
            },
            {
                "name": "Buffalo Chicken Rice Bowl",
                "url": "https://www.maryswholelife.com/buffalo-chicken-rice-bowls/",
                "protein": "chicken",
                "vegetables": ["celery", "carrots", "tomatoes"],
                "starch": "rice",
                "cuisine": "american",
                "gluten_free": True,
                "ingredients": ["chicken breast", "rice", "celery", "carrots", "tomatoes", "buffalo sauce", "blue cheese"],
                "prep_time": 30,
                "difficulty": "easy"
            },
            {
                "name": "Honey Lime Salmon Quinoa Bowl",
                "url": "https://www.maryswholelife.com/fresh-salmon-quinoa-bowl-with-honey-lime-dressing/",
                "protein": "salmon",
                "vegetables": ["spinach", "cherry tomatoes", "cucumber"],
                "starch": "quinoa",
                "cuisine": "healthy",
                "gluten_free": True,
                "ingredients": ["salmon fillet", "quinoa", "spinach", "cherry tomatoes", "cucumber", "honey", "lime"],
                "prep_time": 25,
                "difficulty": "easy"
            },
            {
                "name": "Mongolian Beef with Broccoli",
                "url": "https://unboundwellness.com/mongolian-beef-stir-fry/",
                "protein": "beef",
                "vegetables": ["broccoli", "green onions"],
                "starch": "rice",
                "cuisine": "asian",
                "gluten_free": True,
                "ingredients": ["beef strips", "broccoli", "green onions", "rice", "coconut aminos", "garlic", "ginger"],
                "prep_time": 20,
                "difficulty": "easy"
            },
            {
                "name": "Mediterranean Turkey Meatballs with Quinoa",
                "url": "https://meaningfuleats.com/mediterranean-turkey-meatballs/",
                "protein": "turkey",
                "vegetables": ["zucchini", "tomatoes", "spinach"],
                "starch": "quinoa",
                "cuisine": "mediterranean",
                "gluten_free": True,
                "ingredients": ["ground turkey", "quinoa", "zucchini", "tomatoes", "spinach", "herbs", "olive oil"],
                "prep_time": 40,
                "difficulty": "medium"
            },
            {
                "name": "Thai Basil Chicken with Rice",
                "url": "https://www.mamaknowsglutenfree.com/thai-basil-chicken/",
                "protein": "chicken",
                "vegetables": ["bell peppers", "onions", "basil"],
                "starch": "rice",
                "cuisine": "thai",
                "gluten_free": True,
                "ingredients": ["chicken breast", "rice", "bell peppers", "onions", "thai basil", "fish sauce", "chili"],
                "prep_time": 25,
                "difficulty": "medium"
            },
            {
                "name": "Lemon Herb Cod with Sweet Potato",
                "url": "https://www.healthygffamily.com/lemon-herb-cod/",
                "protein": "cod",
                "vegetables": ["asparagus", "cherry tomatoes"],
                "starch": "sweet potato",
                "cuisine": "mediterranean",
                "gluten_free": True,
                "ingredients": ["cod fillet", "sweet potato", "asparagus", "cherry tomatoes", "lemon", "herbs"],
                "prep_time": 35,
                "difficulty": "easy"
            },
            {
                "name": "Shrimp and Vegetable Curry with Rice",
                "url": "https://theloopywhisk.com/shrimp-curry/",
                "protein": "shrimp",
                "vegetables": ["bell peppers", "spinach", "onions"],
                "starch": "rice",
                "cuisine": "indian",
                "gluten_free": True,
                "ingredients": ["shrimp", "rice", "bell peppers", "spinach", "onions", "coconut milk", "curry spices"],
                "prep_time": 30,
                "difficulty": "medium"
            },
            {
                "name": "Pork Tenderloin with Quinoa Pilaf",
                "url": "https://grainfreetable.com/pork-tenderloin-quinoa/",
                "protein": "pork",
                "vegetables": ["brussels sprouts", "carrots"],
                "starch": "quinoa",
                "cuisine": "american",
                "gluten_free": True,
                "ingredients": ["pork tenderloin", "quinoa", "brussels sprouts", "carrots", "herbs", "olive oil"],
                "prep_time": 45,
                "difficulty": "medium"
            },
            {
                "name": "Tuna Poke Bowl with Brown Rice",
                "url": "https://kaynutrition.com/tuna-poke-bowl/",
                "protein": "tuna",
                "vegetables": ["cucumber", "avocado", "edamame"],
                "starch": "brown rice",
                "cuisine": "hawaiian",
                "gluten_free": True,
                "ingredients": ["tuna", "brown rice", "cucumber", "avocado", "edamame", "sesame oil", "nori"],
                "prep_time": 20,
                "difficulty": "easy"
            }
        ]
    
    def get_recipe_recommendations(self, user_preferences, recent_selections=None, selected_this_week=None):
        """Generate recipe recommendations based on user preferences"""
        if recent_selections is None:
            recent_selections = []
        if selected_this_week is None:
            selected_this_week = []
        
        # Filter out recently selected recipes
        available_recipes = [r for r in self.curated_recipes 
                           if r.get('name') not in recent_selections]
        
        # Score recipes based on user preferences
        scored_recipes = []
        for recipe in available_recipes:
            score = self.calculate_recipe_score(recipe, user_preferences)
            scored_recipes.append((recipe, score))
        
        # Sort by score (highest first)
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        
        # Apply protein variety filter for weekly selections
        if selected_this_week:
            scored_recipes = self.filter_protein_variety(scored_recipes, selected_this_week)
        
        return [recipe for recipe, score in scored_recipes]
    
    def calculate_recipe_score(self, recipe, user_preferences):
        """Calculate recommendation score for a recipe"""
        score = 0
        
        # Protein preference scoring
        protein_prefs = user_preferences.get('favorite_proteins', {})
        recipe_protein = recipe.get('protein', '')
        if recipe_protein in protein_prefs:
            score += protein_prefs[recipe_protein] * 2
        
        # Cuisine preference scoring
        cuisine_prefs = user_preferences.get('favorite_cuisines', {})
        recipe_cuisine = recipe.get('cuisine', '')
        if recipe_cuisine in cuisine_prefs:
            score += cuisine_prefs[recipe_cuisine] * 1.5
        
        # Vegetable preference scoring
        veg_prefs = user_preferences.get('favorite_vegetables', {})
        recipe_vegetables = recipe.get('vegetables', [])
        for veg in recipe_vegetables:
            if veg in veg_prefs:
                score += veg_prefs[veg] * 0.5
        
        # Ingredient overlap scoring
        ingredient_prefs = user_preferences.get('common_ingredients', {})
        recipe_ingredients = recipe.get('ingredients', [])
        for ingredient in recipe_ingredients:
            if ingredient in ingredient_prefs:
                score += ingredient_prefs[ingredient] * 0.3
        
        # Difficulty preference (easier recipes get slight boost)
        if recipe.get('difficulty') == 'easy':
            score += 1
        
        return score
    
    def filter_protein_variety(self, scored_recipes, selected_this_week, max_per_protein=2):
        """Filter recipes to ensure protein variety"""
        protein_counts = defaultdict(int)
        
        # Count proteins already selected this week
        for selected_recipe in selected_this_week:
            protein = selected_recipe.get('protein', 'unknown')
            protein_counts[protein] += 1
        
        filtered_recipes = []
        for recipe, score in scored_recipes:
            protein = recipe.get('protein', 'unknown')
            if protein_counts[protein] < max_per_protein:
                filtered_recipes.append((recipe, score))
                # Don't increment count here, as we're just filtering candidates
        
        return filtered_recipes
    
    def optimize_for_ingredient_overlap(self, recipes, target_count=4):
        """Optimize recipe selection for ingredient overlap"""
        if len(recipes) <= target_count:
            return recipes
        
        best_combination = None
        best_overlap_score = -1
        
        # Try different combinations to find best ingredient overlap
        from itertools import combinations
        
        for combo in combinations(recipes[:min(15, len(recipes))], target_count):
            overlap_score = self.calculate_ingredient_overlap_score(combo)
            if overlap_score > best_overlap_score:
                best_overlap_score = overlap_score
                best_combination = combo
        
        return list(best_combination) if best_combination else recipes[:target_count]
    
    def calculate_ingredient_overlap_score(self, recipes):
        """Calculate ingredient overlap score for a set of recipes"""
        all_ingredients = []
        for recipe in recipes:
            all_ingredients.extend(recipe.get('ingredients', []))
        
        ingredient_counts = Counter(all_ingredients)
        overlap_score = sum(count - 1 for count in ingredient_counts.values() if count > 1)
        
        return overlap_score

# Test the search engine
if __name__ == "__main__":
    search_engine = RecipeSearchEngine()
    print(f"Recipe search engine initialized with {len(search_engine.curated_recipes)} curated recipes")
    
    # Test with sample user preferences
    sample_preferences = {
        'favorite_proteins': {'chicken': 3, 'salmon': 2, 'beef': 2},
        'favorite_cuisines': {'asian': 4, 'mediterranean': 2},
        'favorite_vegetables': {'broccoli': 3, 'carrots': 2}
    }
    
    recommendations = search_engine.get_recipe_recommendations(sample_preferences)
    print(f"Generated {len(recommendations)} recipe recommendations")
    print(f"Top 3 recommendations: {[r['name'] for r in recommendations[:3]]}")

