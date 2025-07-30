from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.weekly_suggestion_generator import WeeklySuggestionGenerator
from src.integrated_grocery_system import IntegratedGrocerySystem
from src.recipe_manager import RecipeManager
from src.recipe_search_engine import RecipeSearchEngine

recipe_bp = Blueprint('recipe', __name__)

# Initialize systems
suggestion_generator = WeeklySuggestionGenerator()
grocery_system = IntegratedGrocerySystem()
recipe_manager = RecipeManager()
search_engine = RecipeSearchEngine()

@recipe_bp.route('/weekly-suggestions', methods=['GET'])
@cross_origin()
def get_weekly_suggestions():
    """Get weekly recipe suggestions"""
    try:
        week_date = request.args.get('week_date')
        suggestions = suggestion_generator.generate_weekly_suggestions(week_date)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'total_count': len(suggestions)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recipe_bp.route('/update-suggestions', methods=['POST'])
@cross_origin()
def update_suggestions_after_selection():
    """Update suggestions after user selects a recipe"""
    try:
        data = request.get_json()
        selected_recipe = data.get('selected_recipe')
        remaining_suggestions = data.get('remaining_suggestions', [])
        
        updated_suggestions = suggestion_generator.update_suggestions_after_selection(
            selected_recipe, remaining_suggestions
        )
        
        return jsonify({
            'success': True,
            'updated_suggestions': updated_suggestions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recipe_bp.route('/ingredient-overlap', methods=['POST'])
@cross_origin()
def calculate_ingredient_overlap():
    """Calculate ingredient overlap for selected recipes"""
    try:
        data = request.get_json()
        recipe_ids = data.get('recipe_ids', [])
        
        overlap_info = recipe_manager.calculate_ingredient_overlap(recipe_ids)
        
        return jsonify({
            'success': True,
            'overlap_info': overlap_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recipe_bp.route('/grocery-list', methods=['POST'])
@cross_origin()
def generate_grocery_list():
    """Generate final grocery list for selected recipes"""
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
            'grocery_list': result['raw_data']['grocery_list'],
            'formatted_list': result['formatted_list'],
            'equipment_reminders': result['raw_data']['equipment_reminders'],
            'shopping_tips': result['raw_data']['shopping_tips'],
            'estimated_cost': result['raw_data']['estimated_cost_range'],
            'selected_recipes': result['selected_recipes']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recipe_bp.route('/recipe/<recipe_id>', methods=['GET'])
@cross_origin()
def get_recipe_details():
    """Get detailed information about a specific recipe"""
    try:
        recipe_id = request.view_args['recipe_id']
        recipe = recipe_manager.get_recipe_by_id(recipe_id)
        
        if not recipe:
            return jsonify({
                'success': False,
                'error': 'Recipe not found'
            }), 404
        
        return jsonify({
            'success': True,
            'recipe': recipe
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recipe_bp.route('/user-preferences', methods=['GET'])
@cross_origin()
def get_user_preferences():
    """Get user preferences and favorite recipes"""
    try:
        user_favorites = recipe_manager.get_user_favorites()
        preferences = recipe_manager.recipe_db.get('user_preferences', {})
        
        return jsonify({
            'success': True,
            'favorites': user_favorites,
            'preferences': preferences
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recipe_bp.route('/rate-recipe', methods=['POST'])
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
            'message': 'Recipe rating updated'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recipe_bp.route('/cooking-equipment', methods=['GET'])
@cross_origin()
def get_cooking_equipment():
    """Get available cooking equipment and methods"""
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'cooking_preferences.json'), 'r') as f:
            import json
            cooking_prefs = json.load(f)
        
        return jsonify({
            'success': True,
            'equipment': cooking_prefs.get('available_equipment', []),
            'method_preferences': cooking_prefs.get('method_preferences', {})
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

