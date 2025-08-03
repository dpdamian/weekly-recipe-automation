from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import random
from datetime import datetime
import json

recipe_fix_bp = Blueprint('recipe_fix', __name__)

# Sample recipe database for immediate functionality
SAMPLE_RECIPES = [
    {
        "id": "recipe_001",
        "name": "Mediterranean Grilled Chicken with Roasted Vegetables",
        "protein": "chicken",
        "vegetables": ["zucchini", "bell peppers", "red onion"],
        "starch_grain": "quinoa",
        "prep_time": "35 minutes",
        "difficulty": "easy",
        "cuisine": "mediterranean",
        "cooking_method": "grill",
        "recipe_link": "https://example.com/mediterranean-grilled-chicken",
        "ingredients": ["chicken breast", "zucchini", "bell peppers", "red onion", "quinoa", "olive oil", "lemon", "herbs"],
        "is_favorite": True,
        "source": "user_favorite"
    },
    {
        "id": "recipe_002",
        "name": "One-Pan Lemon Herb Chicken with Sweet Potatoes",
        "protein": "chicken",
        "vegetables": ["brussels sprouts", "carrots"],
        "starch_grain": "sweet potatoes",
        "prep_time": "45 minutes",
        "difficulty": "easy",
        "cuisine": "american",
        "cooking_method": "oven",
        "recipe_link": "https://example.com/lemon-herb-chicken-sweet-potatoes",
        "ingredients": ["chicken thighs", "sweet potatoes", "brussels sprouts", "carrots", "lemon", "herbs", "olive oil"],
        "is_favorite": True,
        "source": "user_favorite"
    },
    {
        "id": "recipe_003",
        "name": "Asian Beef Stir-Fry with Broccoli",
        "protein": "beef",
        "vegetables": ["broccoli", "snow peas", "carrots"],
        "starch_grain": "jasmine rice",
        "prep_time": "25 minutes",
        "difficulty": "medium",
        "cuisine": "asian",
        "cooking_method": "stove",
        "recipe_link": "https://example.com/asian-beef-stir-fry",
        "ingredients": ["beef sirloin", "broccoli", "snow peas", "carrots", "jasmine rice", "soy sauce", "ginger", "garlic"],
        "is_favorite": False,
        "source": "web_search"
    },
    {
        "id": "recipe_004",
        "name": "Pan-Seared Salmon with Lemon Dill Quinoa",
        "protein": "salmon",
        "vegetables": ["green beans", "zucchini"],
        "starch_grain": "quinoa",
        "prep_time": "25 minutes",
        "difficulty": "medium",
        "cuisine": "mediterranean",
        "cooking_method": "stove",
        "recipe_link": "https://example.com/pan-seared-salmon-quinoa",
        "ingredients": ["salmon fillets", "green beans", "zucchini", "quinoa", "lemon", "dill", "olive oil"],
        "is_favorite": True,
        "source": "user_favorite"
    },
    {
        "id": "recipe_005",
        "name": "Air Fryer Pork Tenderloin with Roasted Root Vegetables",
        "protein": "pork",
        "vegetables": ["parsnips", "carrots", "brussels sprouts"],
        "starch_grain": "mashed cauliflower",
        "prep_time": "40 minutes",
        "difficulty": "medium",
        "cuisine": "american",
        "cooking_method": "air_fryer",
        "recipe_link": "https://example.com/air-fryer-pork-tenderloin",
        "ingredients": ["pork tenderloin", "parsnips", "carrots", "brussels sprouts", "cauliflower", "herbs", "olive oil"],
        "is_favorite": False,
        "source": "web_search"
    },
    {
        "id": "recipe_006",
        "name": "Cajun Shrimp and Vegetable Skewers",
        "protein": "shrimp",
        "vegetables": ["bell peppers", "zucchini", "red onion"],
        "starch_grain": "coconut rice",
        "prep_time": "25 minutes",
        "difficulty": "easy",
        "cuisine": "american",
        "cooking_method": "grill",
        "recipe_link": "https://example.com/cajun-shrimp-skewers",
        "ingredients": ["shrimp", "bell peppers", "zucchini", "red onion", "coconut rice", "cajun seasoning", "olive oil"],
        "is_favorite": False,
        "source": "web_search"
    },
    {
        "id": "recipe_007",
        "name": "Greek Lamb Chops with Lemon Potatoes",
        "protein": "lamb",
        "vegetables": ["green beans", "tomatoes"],
        "starch_grain": "roasted potatoes",
        "prep_time": "50 minutes",
        "difficulty": "medium",
        "cuisine": "mediterranean",
        "cooking_method": "oven",
        "recipe_link": "https://example.com/greek-lamb-chops",
        "ingredients": ["lamb chops", "green beans", "tomatoes", "potatoes", "lemon", "oregano", "olive oil"],
        "is_favorite": False,
        "source": "web_search"
    },
    {
        "id": "recipe_008",
        "name": "Slow Cooker Beef and Vegetable Stew",
        "protein": "beef",
        "vegetables": ["potatoes", "carrots", "celery"],
        "starch_grain": "gluten-free bread rolls",
        "prep_time": "20 minutes (6 hours cook)",
        "difficulty": "easy",
        "cuisine": "american",
        "cooking_method": "instant_pot",
        "recipe_link": "https://example.com/slow-cooker-beef-stew",
        "ingredients": ["beef chuck", "potatoes", "carrots", "celery", "beef broth", "tomato paste", "herbs"],
        "is_favorite": False,
        "source": "web_search"
    },
    {
        "id": "recipe_009",
        "name": "Mediterranean Turkey Meatballs with Zucchini Noodles",
        "protein": "turkey",
        "vegetables": ["zucchini", "cherry tomatoes"],
        "starch_grain": "polenta",
        "prep_time": "35 minutes",
        "difficulty": "medium",
        "cuisine": "mediterranean",
        "cooking_method": "oven",
        "recipe_link": "https://example.com/turkey-meatballs-zucchini",
        "ingredients": ["ground turkey", "zucchini", "cherry tomatoes", "polenta", "herbs", "olive oil", "garlic"],
        "is_favorite": False,
        "source": "web_search"
    },
    {
        "id": "recipe_010",
        "name": "Garlic Butter Shrimp with Cauliflower Rice",
        "protein": "shrimp",
        "vegetables": ["broccoli", "snap peas"],
        "starch_grain": "cauliflower rice",
        "prep_time": "20 minutes",
        "difficulty": "easy",
        "cuisine": "american",
        "cooking_method": "stove",
        "recipe_link": "https://example.com/garlic-butter-shrimp",
        "ingredients": ["shrimp", "broccoli", "snap peas", "cauliflower", "garlic", "butter", "lemon"],
        "is_favorite": True,
        "source": "user_favorite"
    },
    {
        "id": "recipe_011",
        "name": "Blackened Cod with Roasted Sweet Potato Wedges",
        "protein": "fish",
        "vegetables": ["asparagus", "cherry tomatoes"],
        "starch_grain": "sweet potato wedges",
        "prep_time": "35 minutes",
        "difficulty": "medium",
        "cuisine": "american",
        "cooking_method": "oven",
        "recipe_link": "https://example.com/blackened-cod-sweet-potato",
        "ingredients": ["cod fillets", "asparagus", "cherry tomatoes", "sweet potatoes", "cajun seasoning", "olive oil"],
        "is_favorite": False,
        "source": "web_search"
    },
    {
        "id": "recipe_012",
        "name": "Honey Glazed Salmon with Asparagus",
        "protein": "salmon",
        "vegetables": ["asparagus", "cherry tomatoes"],
        "starch_grain": "wild rice",
        "prep_time": "30 minutes",
        "difficulty": "medium",
        "cuisine": "american",
        "cooking_method": "oven",
        "recipe_link": "https://example.com/honey-glazed-salmon",
        "ingredients": ["salmon fillets", "asparagus", "cherry tomatoes", "wild rice", "honey", "soy sauce", "garlic"],
        "is_favorite": False,
        "source": "web_search"
    },
    {
        "id": "recipe_013",
        "name": "Five-Spice Duck Breast with Asian Vegetables",
        "protein": "duck",
        "vegetables": ["bok choy", "snow peas", "carrots"],
        "starch_grain": "brown rice",
        "prep_time": "45 minutes",
        "difficulty": "hard",
        "cuisine": "asian",
        "cooking_method": "stove",
        "recipe_link": "https://example.com/five-spice-duck-breast",
        "ingredients": ["duck breast", "bok choy", "snow peas", "carrots", "brown rice", "five-spice", "soy sauce", "ginger"],
        "is_favorite": False,
        "source": "web_search"
    },
    {
        "id": "recipe_014",
        "name": "Cuban Mojo Pork with Black Beans and Rice",
        "protein": "pork",
        "vegetables": ["bell peppers", "onions"],
        "starch_grain": "brown rice",
        "prep_time": "50 minutes",
        "difficulty": "medium",
        "cuisine": "american",
        "cooking_method": "oven",
        "recipe_link": "https://example.com/cuban-mojo-pork",
        "ingredients": ["pork shoulder", "bell peppers", "onions", "brown rice", "black beans", "citrus", "garlic", "cumin"],
        "is_favorite": False,
        "source": "web_search"
    },
    {
        "id": "recipe_015",
        "name": "Herb-Crusted Turkey Breast with Roasted Vegetables",
        "protein": "turkey",
        "vegetables": ["sweet potatoes", "green beans"],
        "starch_grain": "quinoa pilaf",
        "prep_time": "60 minutes",
        "difficulty": "hard",
        "cuisine": "american",
        "cooking_method": "oven",
        "recipe_link": "https://example.com/herb-crusted-turkey-breast",
        "ingredients": ["turkey breast", "sweet potatoes", "green beans", "quinoa", "herbs", "olive oil", "lemon"],
        "is_favorite": False,
        "source": "web_search"
    }
]

@recipe_fix_bp.route('/weekly-suggestions', methods=['GET'])
@cross_origin()
def get_weekly_suggestions_fixed():
    """Fixed endpoint for weekly recipe suggestions"""
    try:
        # Get query parameters
        count = int(request.args.get('count', 15))
        include_web = request.args.get('include_web', 'true').lower() == 'true'
        fresh = request.args.get('fresh', 'false').lower() == 'true'
        
        # Shuffle recipes for variety
        available_recipes = SAMPLE_RECIPES.copy()
        random.shuffle(available_recipes)
        
        # Ensure protein variety (max 2 of same protein)
        selected_recipes = []
        protein_count = {}
        
        # First add favorites
        favorites = [r for r in available_recipes if r.get('is_favorite', False)]
        for recipe in favorites[:3]:  # Max 3 favorites
            selected_recipes.append(recipe)
            protein = recipe['protein']
            protein_count[protein] = protein_count.get(protein, 0) + 1
        
        # Then add variety
        remaining = [r for r in available_recipes if not r.get('is_favorite', False)]
        for recipe in remaining:
            if len(selected_recipes) >= count:
                break
            protein = recipe['protein']
            if protein_count.get(protein, 0) < 2:
                selected_recipes.append(recipe)
                protein_count[protein] = protein_count.get(protein, 0) + 1
        
        # Fill remaining slots if needed
        for recipe in remaining:
            if len(selected_recipes) >= count:
                break
            if recipe not in selected_recipes:
                selected_recipes.append(recipe)
        
        # Limit to requested count
        selected_recipes = selected_recipes[:count]
        
        # Generate summary
        source_breakdown = {}
        for recipe in selected_recipes:
            source = recipe.get('source', 'unknown')
            source_breakdown[source] = source_breakdown.get(source, 0) + 1
        
        return jsonify({
            'success': True,
            'suggestions': selected_recipes,
            'total_count': len(selected_recipes),
            'summary': {
                'total_recipes': len(selected_recipes),
                'source_breakdown': source_breakdown,
                'protein_variety': len(set(r['protein'] for r in selected_recipes)),
                'cuisine_variety': len(set(r['cuisine'] for r in selected_recipes)),
                'generation_timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        print(f"Error in weekly-suggestions: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'suggestions': []
        }), 500

@recipe_fix_bp.route('/grocery-list', methods=['POST'])
@cross_origin()
def generate_grocery_list_fixed():
    """Fixed endpoint for grocery list generation"""
    try:
        data = request.get_json()
        selected_recipes = data.get('selected_recipes', [])
        
        if len(selected_recipes) != 4:
            return jsonify({
                'success': False,
                'error': 'Exactly 4 recipes must be selected'
            }), 400
        
        # Organize ingredients by department
        departments = {
            "Proteins": [],
            "Vegetables": [],
            "Grains & Starches": [],
            "Pantry": [],
            "Dairy": []
        }
        
        all_ingredients = []
        for recipe in selected_recipes:
            ingredients = recipe.get('ingredients', [])
            all_ingredients.extend(ingredients)
        
        # Remove duplicates while preserving order
        unique_ingredients = list(dict.fromkeys(all_ingredients))
        
        # Categorize ingredients
        protein_keywords = ['chicken', 'beef', 'salmon', 'shrimp', 'turkey', 'pork', 'lamb', 'duck', 'cod', 'fish']
        vegetable_keywords = ['zucchini', 'bell peppers', 'onion', 'broccoli', 'carrots', 'asparagus', 'tomatoes', 'green beans', 'brussels sprouts', 'spinach', 'bok choy', 'snow peas', 'snap peas', 'eggplant', 'parsnips', 'celery']
        grain_keywords = ['quinoa', 'rice', 'potatoes', 'sweet potatoes', 'bread', 'couscous', 'polenta', 'cauliflower']
        dairy_keywords = ['butter', 'cheese', 'milk', 'cream']
        
        for ingredient in unique_ingredients:
            ingredient_lower = ingredient.lower()
            categorized = False
            
            for keyword in protein_keywords:
                if keyword in ingredient_lower:
                    departments["Proteins"].append(ingredient.title())
                    categorized = True
                    break
            
            if not categorized:
                for keyword in vegetable_keywords:
                    if keyword in ingredient_lower:
                        departments["Vegetables"].append(ingredient.title())
                        categorized = True
                        break
            
            if not categorized:
                for keyword in grain_keywords:
                    if keyword in ingredient_lower:
                        departments["Grains & Starches"].append(ingredient.title())
                        categorized = True
                        break
            
            if not categorized:
                for keyword in dairy_keywords:
                    if keyword in ingredient_lower:
                        departments["Dairy"].append(ingredient.title())
                        categorized = True
                        break
            
            if not categorized:
                departments["Pantry"].append(ingredient.title())
        
        # Remove empty departments
        grocery_list = {dept: items for dept, items in departments.items() if items}
        
        return jsonify({
            'success': True,
            'formatted_list': {
                'grocery_list': grocery_list,
                'total_items': len(unique_ingredients),
                'generation_date': datetime.now().isoformat()
            },
            'raw_data': grocery_list,
            'selected_recipes': selected_recipes,
            'generation_method': 'fixed_simple_categorization'
        })
        
    except Exception as e:
        print(f"Error in grocery-list: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

