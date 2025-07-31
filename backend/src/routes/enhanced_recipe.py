from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import sys
import os

# Add the backend directory to the path for imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, backend_dir)

from enhanced_weekly_suggestion_generator import EnhancedWeeklySuggestionGenerator
from integrated_grocery_system import IntegratedGrocerySystem
from recipe_manager import RecipeManager
from recipe_search_engine import RecipeSearchEngine
from enhanced_web_recipe_search import EnhancedWebRecipeSearcher

enhanced_recipe_bp = Blueprint('enhanced_recipe', __name__)

# Initialize enhanced systems
enhanced_suggestion_generator = EnhancedWeeklySuggestionGenerator()
grocery_system = IntegratedGrocerySystem()
recipe_manager = RecipeManager()
search_engine = RecipeSearchEngine()
web_searcher = EnhancedWebRecipeSearcher()

@enhanced_recipe_bp.route('/weekly-suggestions', methods=['GET'])
@cross_origin()
def get_weekly_suggestions():
    """Get enhanced weekly recipe suggestions with web recipes"""
    try:
        week_date = request.args.get('week_date')
        include_web = request.args.get('include_web', 'true').lower() == 'true'
        
        suggestions = enhanced_suggestion_generator.generate_weekly_suggestions(
            week_date=week_date,
            include_web_recipes=include_web
        )
        
        # Add summary statistics
        protein_counts = {}
        cuisine_counts = {}
        source_counts = {}
        
        for recipe in suggestions:
            protein = recipe.get('protein', 'unknown')
            cuisine = recipe.get('cuisine', 'unknown')
            source = recipe.get('source', 'unknown')
            
            protein_counts[protein] = protein_counts.get(protein, 0) + 1
            cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
            source_counts[source] = source_counts.get(source, 0) + 1
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'total_count': len(suggestions),
            'summary': {
                'protein_variety': protein_counts,
                'cuisine_variety': cuisine_counts,
                'source_breakdown': source_counts,
                'web_recipes_included': include_web,
                'generation_date': suggestions[0].get('suggested_date') if suggestions else None
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_recipe_bp.route('/update-suggestions', methods=['POST'])
@cross_origin()
def update_suggestions_after_selection():
    """Update suggestions after user selects a recipe with web recipe integration"""
    try:
        data = request.get_json()
        selected_recipe = data.get('selected_recipe')
        remaining_suggestions = data.get('remaining_suggestions', [])
        
        updated_suggestions = enhanced_suggestion_generator.update_suggestions_after_selection(
            selected_recipe, remaining_suggestions
        )
        
        # Add summary for updated suggestions
        protein_counts = {}
        for recipe in updated_suggestions:
            protein = recipe.get('protein', 'unknown')
            protein_counts[protein] = protein_counts.get(protein, 0) + 1
        
        return jsonify({
            'success': True,
            'updated_suggestions': updated_suggestions,
            'remaining_count': len(updated_suggestions),
            'protein_variety': protein_counts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_recipe_bp.route('/search-recipes', methods=['POST'])
@cross_origin()
def search_web_recipes():
    """Search cooking websites for specific recipe criteria"""
    try:
        data = request.get_json()
        protein = data.get('protein')
        cuisine = data.get('cuisine')
        cooking_method = data.get('cooking_method')
        count = data.get('count', 10)
        
        # Search web recipes
        web_recipes = web_searcher.search_by_criteria(
            protein=protein,
            cuisine=cuisine,
            cooking_method=cooking_method,
            count=count
        )
        
        # Also get matching user favorites and existing recipes
        user_recipes = enhanced_suggestion_generator.get_recipe_suggestions_by_criteria(
            protein=protein,
            cuisine=cuisine,
            cooking_method=cooking_method,
            count=count
        )
        
        # Combine results
        all_recipes = web_recipes + user_recipes
        
        # Remove duplicates
        unique_recipes = []
        seen_names = set()
        
        for recipe in all_recipes:
            name_key = recipe.get('name', '').lower()
            if name_key not in seen_names:
                unique_recipes.append(recipe)
                seen_names.add(name_key)
        
        return jsonify({
            'success': True,
            'recipes': unique_recipes[:count],
            'search_criteria': {
                'protein': protein,
                'cuisine': cuisine,
                'cooking_method': cooking_method
            },
            'total_found': len(unique_recipes),
            'web_recipes_count': len(web_recipes),
            'user_recipes_count': len(user_recipes)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_recipe_bp.route('/fresh-web-recipes', methods=['GET'])
@cross_origin()
def get_fresh_web_recipes():
    """Get fresh recipes from cooking websites"""
    try:
        max_recipes = int(request.args.get('max_recipes', 15))
        
        web_recipes = web_searcher.search_cooking_websites(max_recipes=max_recipes)
        
        # Save the recipes for future use
        filename = web_searcher.save_recipes(web_recipes)
        
        return jsonify({
            'success': True,
            'recipes': web_recipes,
            'total_count': len(web_recipes),
            'saved_to': filename,
            'search_timestamp': web_recipes[0].get('added_date') if web_recipes else None
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_recipe_bp.route('/ingredient-overlap', methods=['POST'])
@cross_origin()
def calculate_ingredient_overlap():
    """Calculate ingredient overlap for selected recipes"""
    try:
        data = request.get_json()
        recipe_ids = data.get('recipe_ids', [])
        
        # Get recipes from various sources
        recipes = []
        for recipe_id in recipe_ids:
            recipe = recipe_manager.get_recipe_by_id(recipe_id)
            if recipe:
                recipes.append(recipe)
        
        if len(recipes) < 2:
            return jsonify({
                'success': False,
                'error': 'At least 2 recipes required for overlap calculation'
            }), 400
        
        # Calculate overlap using the search engine
        overlap_info = search_engine.calculate_ingredient_overlap(recipes)
        
        return jsonify({
            'success': True,
            'shared_ingredients': overlap_info.get('shared_ingredients', []),
            'total_unique_ingredients': overlap_info.get('total_unique_ingredients', 0),
            'overlap_percentage': overlap_info.get('overlap_percentage', 0),
            'recipes_analyzed': len(recipes)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_recipe_bp.route('/grocery-list', methods=['POST'])
@cross_origin()
def generate_grocery_list():
    """Generate enhanced grocery list for selected recipes"""
    try:
        data = request.get_json()
        selected_recipe_ids = data.get('recipe_ids', [])
        week_date = data.get('week_date')
        
        if len(selected_recipe_ids) != 4:
            return jsonify({
                'success': False,
                'error': 'Exactly 4 recipes must be selected'
            }), 400
        
        result = grocery_system.generate_final_grocery_list(selected_recipe_ids, week_date)
        
        return jsonify({
            'success': True,
            'raw_data': result['raw_data'],
            'formatted_list': result['formatted_list'],
            'selected_recipes': result['selected_recipes'],
            'generation_date': result.get('generation_date'),
            'week_date': week_date
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_recipe_bp.route('/recipe/<recipe_id>', methods=['GET'])
@cross_origin()
def get_recipe_details(recipe_id):
    """Get detailed information about a specific recipe"""
    try:
        recipe = recipe_manager.get_recipe_by_id(recipe_id)
        
        if not recipe:
            return jsonify({
                'success': False,
                'error': 'Recipe not found'
            }), 404
        
        # Add additional context if it's a web recipe
        if recipe.get('source') == 'web_search':
            recipe['is_web_recipe'] = True
            recipe['website'] = recipe.get('website', 'cooking website')
        
        return jsonify({
            'success': True,
            'recipe': recipe
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_recipe_bp.route('/user-preferences', methods=['GET'])
@cross_origin()
def get_user_preferences():
    """Get user preferences and favorite recipes"""
    try:
        user_favorites = recipe_manager.get_user_favorites()
        preferences = recipe_manager.recipe_db.get('user_preferences', {})
        
        # Add statistics about recipe sources
        total_recipes = len(recipe_manager.recipe_db.get('recipes', []))
        web_recipes = len([r for r in recipe_manager.recipe_db.get('recipes', []) 
                          if r.get('source') == 'web_search'])
        
        return jsonify({
            'success': True,
            'favorites': user_favorites,
            'preferences': preferences,
            'statistics': {
                'total_recipes': total_recipes,
                'web_recipes': web_recipes,
                'user_favorites': len(user_favorites)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_recipe_bp.route('/rate-recipe', methods=['POST'])
@cross_origin()
def rate_recipe():
    """Rate a recipe to update user preferences"""
    try:
        data = request.get_json()
        recipe_id = data.get('recipe_id')
        rating = data.get('rating', 3)  # Default to neutral rating
        
        recipe_manager.update_user_preferences(recipe_id, rating)
        
        return jsonify({
            'success': True,
            'message': 'Recipe rating updated',
            'recipe_id': recipe_id,
            'rating': rating
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_recipe_bp.route('/cooking-equipment', methods=['GET'])
@cross_origin()
def get_cooking_equipment():
    """Get available cooking equipment and methods"""
    try:
        # Default equipment based on user requirements
        default_equipment = [
            'grill', 'stove', 'oven', 'air_fryer', 'instant_pot'
        ]
        
        equipment_info = {
            'available_equipment': default_equipment,
            'method_preferences': {
                'stove': 'Stovetop cooking',
                'oven': 'Oven baking/roasting',
                'grill': 'Outdoor grilling',
                'air_fryer': 'Air fryer cooking',
                'instant_pot': 'Pressure cooking'
            },
            'equipment_descriptions': {
                'grill': 'Outdoor gas or charcoal grill',
                'stove': 'Stovetop with multiple burners',
                'oven': 'Standard kitchen oven',
                'air_fryer': 'Countertop air fryer',
                'instant_pot': 'Electric pressure cooker'
            }
        }
        
        return jsonify({
            'success': True,
            'equipment': equipment_info['available_equipment'],
            'method_preferences': equipment_info['method_preferences'],
            'descriptions': equipment_info['equipment_descriptions']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_recipe_bp.route('/recipe-sources', methods=['GET'])
@cross_origin()
def get_recipe_sources():
    """Get information about recipe sources"""
    try:
        # Get statistics about recipe sources
        all_recipes = recipe_manager.recipe_db.get('recipes', [])
        
        source_stats = {}
        website_stats = {}
        
        for recipe in all_recipes:
            source = recipe.get('source', 'unknown')
            source_stats[source] = source_stats.get(source, 0) + 1
            
            if source == 'web_search':
                website = recipe.get('website', 'unknown')
                website_stats[website] = website_stats.get(website, 0) + 1
        
        return jsonify({
            'success': True,
            'source_statistics': source_stats,
            'website_statistics': website_stats,
            'total_recipes': len(all_recipes),
            'supported_sources': [
                'user_favorite',
                'web_search',
                'recipe_database'
            ]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

