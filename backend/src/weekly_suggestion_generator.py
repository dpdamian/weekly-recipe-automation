#!/usr/bin/env python3
"""
Weekly Recipe Suggestion Generator
Generates 15+ recipe suggestions every week with optimization for variety and preferences
"""

import json
import random
from datetime import datetime, timedelta
from recipe_manager import RecipeManager
from recipe_search_engine import RecipeSearchEngine

class WeeklySuggestionGenerator:
    def __init__(self):
        self.recipe_manager = RecipeManager()
        self.search_engine = RecipeSearchEngine()
        self.min_suggestions = 15
    
    def generate_weekly_suggestions(self, week_date=None):
        """Generate weekly recipe suggestions"""
        if week_date is None:
            week_date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"Generating weekly suggestions for week of {week_date}")
        
        # Get user preferences and history
        user_preferences = self.recipe_manager.recipe_db.get('user_preferences', {})
        recent_selections = self.recipe_manager.get_recent_selections(weeks=4)
        user_favorites = self.recipe_manager.get_user_favorites()
        
        # Get new recipe recommendations
        new_recommendations = self.search_engine.get_recipe_recommendations(
            user_preferences, 
            recent_selections=[r['name'] for r in user_favorites]
        )
        
        # Combine user favorites with new recommendations
        suggestions = []
        
        # Include some user favorites (30% of suggestions)
        favorite_count = max(3, int(self.min_suggestions * 0.3))
        selected_favorites = random.sample(user_favorites, min(favorite_count, len(user_favorites)))
        suggestions.extend(selected_favorites)
        
        # Add new recommendations (70% of suggestions)
        new_count = self.min_suggestions - len(suggestions)
        suggestions.extend(new_recommendations[:new_count])
        
        # Ensure we have enough suggestions
        while len(suggestions) < self.min_suggestions:
            remaining_recipes = [r for r in new_recommendations if r not in suggestions]
            if remaining_recipes:
                suggestions.append(remaining_recipes[0])
            else:
                break
        
        # Shuffle to mix favorites with new recipes
        random.shuffle(suggestions)
        
        # Add metadata
        for i, recipe in enumerate(suggestions, 1):
            recipe['suggestion_number'] = i
            recipe['week_date'] = week_date
            recipe['suggested_date'] = datetime.now().isoformat()
        
        # Save suggestions to history
        self.save_weekly_suggestions(suggestions, week_date)
        
        return suggestions
    
    def save_weekly_suggestions(self, suggestions, week_date):
        """Save weekly suggestions to database"""
        if 'recipe_history' not in self.recipe_manager.recipe_db:
            self.recipe_manager.recipe_db['recipe_history'] = {}
        
        if 'weekly_suggestions' not in self.recipe_manager.recipe_db['recipe_history']:
            self.recipe_manager.recipe_db['recipe_history']['weekly_suggestions'] = []
        
        suggestion_record = {
            'week_date': week_date,
            'suggestions': suggestions,
            'generated_date': datetime.now().isoformat()
        }
        
        self.recipe_manager.recipe_db['recipe_history']['weekly_suggestions'].append(suggestion_record)
        self.recipe_manager.save_database()
    
    def format_suggestions_for_user(self, suggestions):
        """Format suggestions as numbered list for user"""
        formatted_list = []
        formatted_list.append("# Weekly Dinner Recipe Suggestions\\n")
        formatted_list.append(f"Generated on: {datetime.now().strftime('%B %d, %Y')}\\n")
        formatted_list.append("All recipes are gluten-free and include protein + vegetables + starch\\n")
        
        for recipe in suggestions:
            num = recipe.get('suggestion_number', len(formatted_list))
            name = recipe.get('name', 'Unknown Recipe')
            url = recipe.get('url', '#')
            protein = recipe.get('protein', 'protein').title()
            vegetables = ', '.join(recipe.get('vegetables', []))
            starch = recipe.get('starch', 'starch').title()
            cuisine = recipe.get('cuisine', 'various').title()
            
            formatted_list.append(f"{num}. **{name}**")
            formatted_list.append(f"   - Link: {url}")
            formatted_list.append(f"   - Protein: {protein}")
            formatted_list.append(f"   - Vegetables: {vegetables}")
            formatted_list.append(f"   - Starch: {starch}")
            formatted_list.append(f"   - Cuisine: {cuisine}")
            
            if recipe.get('source') == 'user_favorite':
                formatted_list.append(f"   - ⭐ *One of your favorites!*")
            
            formatted_list.append("")
        
        return "\\n".join(formatted_list)
    
    def update_suggestions_after_selection(self, selected_recipe, remaining_suggestions):
        """Update suggestions after user selects a recipe"""
        # Remove selected recipe from suggestions
        updated_suggestions = [r for r in remaining_suggestions if r.get('name') != selected_recipe.get('name')]
        
        # Get selected proteins this week to ensure variety
        selected_proteins = [selected_recipe.get('protein')]
        
        # Filter remaining suggestions for protein variety
        filtered_suggestions = []
        protein_counts = {selected_recipe.get('protein'): 1}
        
        for recipe in updated_suggestions:
            protein = recipe.get('protein')
            if protein_counts.get(protein, 0) < 2:  # Max 2 per protein type
                filtered_suggestions.append(recipe)
                protein_counts[protein] = protein_counts.get(protein, 0) + 1
        
        # Get additional recommendations if needed
        if len(filtered_suggestions) < 10:  # Keep at least 10 options
            user_preferences = self.recipe_manager.recipe_db.get('user_preferences', {})
            additional_recipes = self.search_engine.get_recipe_recommendations(
                user_preferences,
                selected_this_week=[selected_recipe]
            )
            
            # Add new recipes that aren't already in the list
            for recipe in additional_recipes:
                if recipe not in filtered_suggestions and len(filtered_suggestions) < 15:
                    filtered_suggestions.append(recipe)
        
        # Optimize for ingredient overlap with selected recipe
        if len(filtered_suggestions) > 10:
            optimized_suggestions = self.search_engine.optimize_for_ingredient_overlap(
                [selected_recipe] + filtered_suggestions[:10], 
                target_count=4
            )[1:]  # Remove the selected recipe from the result
            
            # Add remaining suggestions
            remaining = [r for r in filtered_suggestions if r not in optimized_suggestions]
            filtered_suggestions = optimized_suggestions + remaining
        
        # Re-number suggestions
        for i, recipe in enumerate(filtered_suggestions, 1):
            recipe['suggestion_number'] = i
        
        return filtered_suggestions

# Test the weekly suggestion generator
if __name__ == "__main__":
    generator = WeeklySuggestionGenerator()
    suggestions = generator.generate_weekly_suggestions()
    
    print(f"Generated {len(suggestions)} weekly suggestions")
    print("Sample suggestions:")
    for i, recipe in enumerate(suggestions[:3], 1):
        print(f"{i}. {recipe['name']} ({recipe['protein']} + {recipe['starch']})")
    
    # Test formatting
    formatted = generator.format_suggestions_for_user(suggestions[:5])
    print("\\nFormatted output preview:")
    print(formatted[:300] + "...")

