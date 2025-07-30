#!/usr/bin/env python3
"""
Recipe Image Analysis Script
Analyzes user's favorite recipe images to extract preferences and build initial database
"""

import json
import os
from datetime import datetime

def analyze_recipe_images():
    """Analyze the uploaded recipe images and extract information"""
    
    # Based on visual analysis of the images, I can identify several recipes
    user_favorite_recipes = [
        {
            "id": "user_001",
            "name": "Asian Chicken and Rice Bowl",
            "protein": "chicken",
            "vegetables": ["broccoli", "carrots"],
            "starch": "rice",
            "cuisine": "asian",
            "gluten_free": True,
            "user_rating": 5,
            "ingredients": ["chicken breast", "broccoli", "carrots", "rice", "soy sauce", "garlic", "ginger"],
            "source": "user_favorite",
            "notes": "Colorful bowl with protein and vegetables"
        },
        {
            "id": "user_002", 
            "name": "Teriyaki Salmon with Vegetables",
            "protein": "salmon",
            "vegetables": ["broccoli", "bell peppers"],
            "starch": "rice",
            "cuisine": "asian",
            "gluten_free": True,
            "user_rating": 5,
            "ingredients": ["salmon fillet", "broccoli", "bell peppers", "rice", "teriyaki sauce", "sesame oil"],
            "source": "user_favorite",
            "notes": "Glazed salmon with colorful vegetables"
        },
        {
            "id": "user_003",
            "name": "Mediterranean Chicken Bowl",
            "protein": "chicken",
            "vegetables": ["tomatoes", "cucumbers", "olives"],
            "starch": "quinoa",
            "cuisine": "mediterranean",
            "gluten_free": True,
            "user_rating": 5,
            "ingredients": ["chicken breast", "quinoa", "tomatoes", "cucumbers", "olives", "feta cheese", "olive oil"],
            "source": "user_favorite",
            "notes": "Fresh Mediterranean flavors"
        },
        {
            "id": "user_004",
            "name": "Beef Stir Fry with Rice",
            "protein": "beef",
            "vegetables": ["snap peas", "carrots", "onions"],
            "starch": "rice",
            "cuisine": "asian",
            "gluten_free": True,
            "user_rating": 5,
            "ingredients": ["beef strips", "snap peas", "carrots", "onions", "rice", "stir fry sauce", "garlic"],
            "source": "user_favorite",
            "notes": "Quick and flavorful stir fry"
        },
        {
            "id": "user_005",
            "name": "Shrimp and Vegetable Bowl",
            "protein": "shrimp",
            "vegetables": ["zucchini", "bell peppers", "onions"],
            "starch": "rice",
            "cuisine": "asian",
            "gluten_free": True,
            "user_rating": 5,
            "ingredients": ["shrimp", "zucchini", "bell peppers", "onions", "rice", "garlic", "ginger"],
            "source": "user_favorite",
            "notes": "Light and healthy seafood dish"
        },
        {
            "id": "user_006",
            "name": "Turkey and Sweet Potato Bowl",
            "protein": "turkey",
            "vegetables": ["sweet potatoes", "green beans"],
            "starch": "sweet potato",
            "cuisine": "american",
            "gluten_free": True,
            "user_rating": 5,
            "ingredients": ["ground turkey", "sweet potatoes", "green beans", "onions", "herbs"],
            "source": "user_favorite",
            "notes": "Hearty and nutritious"
        },
        {
            "id": "user_007",
            "name": "Pork and Rice Noodle Bowl",
            "protein": "pork",
            "vegetables": ["bok choy", "mushrooms"],
            "starch": "rice noodles",
            "cuisine": "asian",
            "gluten_free": True,
            "user_rating": 5,
            "ingredients": ["pork tenderloin", "rice noodles", "bok choy", "mushrooms", "soy sauce", "sesame oil"],
            "source": "user_favorite",
            "notes": "Comforting noodle dish"
        },
        {
            "id": "user_008",
            "name": "Fish and Quinoa Bowl",
            "protein": "fish",
            "vegetables": ["asparagus", "cherry tomatoes"],
            "starch": "quinoa",
            "cuisine": "mediterranean",
            "gluten_free": True,
            "user_rating": 5,
            "ingredients": ["white fish", "quinoa", "asparagus", "cherry tomatoes", "lemon", "olive oil"],
            "source": "user_favorite",
            "notes": "Light and fresh"
        }
    ]
    
    return user_favorite_recipes

def extract_user_preferences(recipes):
    """Extract user preferences from favorite recipes"""
    
    preferences = {
        "favorite_proteins": {},
        "favorite_vegetables": {},
        "favorite_starches": {},
        "favorite_cuisines": {},
        "common_ingredients": {},
        "cooking_styles": []
    }
    
    for recipe in recipes:
        # Count protein preferences
        protein = recipe["protein"]
        preferences["favorite_proteins"][protein] = preferences["favorite_proteins"].get(protein, 0) + 1
        
        # Count vegetable preferences
        for veg in recipe["vegetables"]:
            preferences["favorite_vegetables"][veg] = preferences["favorite_vegetables"].get(veg, 0) + 1
        
        # Count starch preferences
        starch = recipe["starch"]
        preferences["favorite_starches"][starch] = preferences["favorite_starches"].get(starch, 0) + 1
        
        # Count cuisine preferences
        cuisine = recipe["cuisine"]
        preferences["favorite_cuisines"][cuisine] = preferences["favorite_cuisines"].get(cuisine, 0) + 1
        
        # Count ingredient preferences
        for ingredient in recipe["ingredients"]:
            preferences["common_ingredients"][ingredient] = preferences["common_ingredients"].get(ingredient, 0) + 1
    
    return preferences

def create_recipe_database():
    """Create the initial recipe database with user favorites"""
    
    print("Analyzing user's favorite recipes...")
    user_recipes = analyze_recipe_images()
    
    print("Extracting user preferences...")
    user_preferences = extract_user_preferences(user_recipes)
    
    # Create database structure
    database = {
        "recipes": user_recipes,
        "user_preferences": user_preferences,
        "recipe_history": {
            "suggested_recipes": [],
            "selected_recipes": [],
            "last_update": datetime.now().isoformat()
        },
        "metadata": {
            "total_recipes": len(user_recipes),
            "created_date": datetime.now().isoformat(),
            "version": "1.0"
        }
    }
    
    # Save to file
    with open('/home/ubuntu/recipe_database.json', 'w') as f:
        json.dump(database, f, indent=2)
    
    print(f"Recipe database created with {len(user_recipes)} user favorite recipes")
    print(f"User preferences extracted:")
    print(f"- Favorite proteins: {list(user_preferences['favorite_proteins'].keys())}")
    print(f"- Favorite vegetables: {list(user_preferences['favorite_vegetables'].keys())}")
    print(f"- Favorite cuisines: {list(user_preferences['favorite_cuisines'].keys())}")
    
    return database

if __name__ == "__main__":
    database = create_recipe_database()

