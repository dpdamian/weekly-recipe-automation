#!/usr/bin/env python3
"""
Enhanced Weekly Recipe Suggestion Generator
Integrates web recipe search with user favorites for diverse weekly suggestions
"""

import json
import random
from datetime import datetime, timedelta
from recipe_manager import RecipeManager
from recipe_search_engine import RecipeSearchEngine
from enhanced_web_recipe_search import EnhancedWebRecipeSearcher

class EnhancedWeeklySuggestionGenerator:
    def __init__(self):
        self.recipe_manager = RecipeManager()
        self.search_engine = RecipeSearchEngine()
        self.web_searcher = EnhancedWebRecipeSearcher()
        self.min_suggestions = 15
        self.max_suggestions = 20
    
    def generate_weekly_suggestions(self, week_date=None, include_web_recipes=True):
        """Generate enhanced weekly recipe suggestions with web recipes"""
        if week_date is None:
            week_date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"🍽️ Generating enhanced weekly suggestions for week of {week_date}")
        
        # Get user data
        user_preferences = self.recipe_manager.recipe_db.get('user_preferences', {})
        recent_selections = self.recipe_manager.get_recent_selections(weeks=4)
        user_favorites = self.recipe_manager.get_user_favorites()
        
        suggestions = []
        
        # 1. Include user favorites (25% of suggestions)
        favorite_count = max(3, int(self.min_suggestions * 0.25))
        if user_favorites:
            selected_favorites = random.sample(user_favorites, min(favorite_count, len(user_favorites)))
            suggestions.extend(selected_favorites)
            print(f"   ⭐ Added {len(selected_favorites)} user favorites")
        
        # Get existing recipe recommendations (25% of suggestions)
        existing_count = max(3, int(self.min_suggestions * 0.25))
        
        # Handle recent_selections data structure
        recent_names = []
        if recent_selections:
            for item in recent_selections:
                if isinstance(item, dict):
                    recent_names.append(item.get('name', ''))
                elif isinstance(item, str):
                    recent_names.append(item)
        
        existing_recommendations = self.search_engine.get_recipe_recommendations(
            user_preferences, 
            recent_selections=recent_names
        )
        suggestions.extend(existing_recommendations[:existing_count])
        print(f"   📚 Added {min(existing_count, len(existing_recommendations))} existing recipe recommendations")
        
        # 3. Search web for fresh recipes (50% of suggestions)
        if include_web_recipes:
            web_count = self.max_suggestions - len(suggestions)
            web_recipes = self.web_searcher.search_cooking_websites(max_recipes=web_count + 5)
            
            # Filter web recipes to ensure variety
            filtered_web_recipes = self._filter_web_recipes_for_variety(
                web_recipes, 
                existing_suggestions=suggestions,
                target_count=web_count
            )
            
            suggestions.extend(filtered_web_recipes)
            print(f"   🌐 Added {len(filtered_web_recipes)} fresh recipes from cooking websites")
        
        # 4. Ensure protein variety and balance
        suggestions = self._ensure_protein_variety(suggestions)
        
        # 5. Optimize for ingredient overlap
        suggestions = self._optimize_ingredient_overlap(suggestions)
        
        # 6. Limit to target number and shuffle
        suggestions = suggestions[:self.max_suggestions]
        random.shuffle(suggestions)
        
        # 7. Add metadata
        for i, recipe in enumerate(suggestions, 1):
            recipe['suggestion_number'] = i
            recipe['week_date'] = week_date
            recipe['suggested_date'] = datetime.now().isoformat()
        
        # 8. Save suggestions
        self.save_weekly_suggestions(suggestions, week_date)
        
        print(f"✅ Generated {len(suggestions)} diverse weekly suggestions")
        self._print_suggestion_summary(suggestions)
        
        return suggestions
    
    def _filter_web_recipes_for_variety(self, web_recipes, existing_suggestions, target_count):
        """Filter web recipes to ensure variety and avoid duplicates"""
        
        # Get existing proteins and cuisines
        existing_proteins = [r.get('protein') for r in existing_suggestions]
        existing_cuisines = [r.get('cuisine') for r in existing_suggestions]
        existing_names = set(r.get('name', '').lower() for r in existing_suggestions)
        
        filtered_recipes = []
        protein_counts = {}
        cuisine_counts = {}
        
        # Count existing proteins and cuisines
        for protein in existing_proteins:
            protein_counts[protein] = protein_counts.get(protein, 0) + 1
        for cuisine in existing_cuisines:
            cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1
        
        # Filter web recipes for variety
        for recipe in web_recipes:
            if len(filtered_recipes) >= target_count:
                break
            
            # Skip if duplicate name
            recipe_name = recipe.get('name', '').lower()
            if recipe_name in existing_names:
                continue
            
            protein = recipe.get('protein')
            cuisine = recipe.get('cuisine')
            
            # Prefer recipes that add variety
            protein_count = protein_counts.get(protein, 0)
            cuisine_count = cuisine_counts.get(cuisine, 0)
            
            # Allow up to 3 of each protein type across all suggestions
            if protein_count < 3:
                filtered_recipes.append(recipe)
                existing_names.add(recipe_name)
                protein_counts[protein] = protein_count + 1
                cuisine_counts[cuisine] = cuisine_count + 1
        
        return filtered_recipes
    
    def _ensure_protein_variety(self, suggestions):
        """Ensure good protein variety across suggestions"""
        
        # Count proteins
        protein_counts = {}
        for recipe in suggestions:
            protein = recipe.get('protein')
            protein_counts[protein] = protein_counts.get(protein, 0) + 1
        
        # If any protein is over-represented, try to balance
        max_per_protein = max(2, len(suggestions) // 4)  # Max 25% of any single protein
        
        balanced_suggestions = []
        current_protein_counts = {}
        
        # First pass: add recipes up to the limit per protein
        for recipe in suggestions:
            protein = recipe.get('protein')
            current_count = current_protein_counts.get(protein, 0)
            
            if current_count < max_per_protein:
                balanced_suggestions.append(recipe)
                current_protein_counts[protein] = current_count + 1
        
        # Second pass: add remaining recipes if we're under the minimum
        if len(balanced_suggestions) < self.min_suggestions:
            remaining_recipes = [r for r in suggestions if r not in balanced_suggestions]
            needed = self.min_suggestions - len(balanced_suggestions)
            balanced_suggestions.extend(remaining_recipes[:needed])
        
        return balanced_suggestions
    
    def _optimize_ingredient_overlap(self, suggestions):
        """Optimize suggestions for ingredient overlap to reduce shopping complexity"""
        
        if len(suggestions) <= self.min_suggestions:
            return suggestions
        
        # Use existing optimization from search engine
        try:
            optimized = self.search_engine.optimize_for_ingredient_overlap(
                suggestions, 
                target_count=self.max_suggestions
            )
            return optimized
        except Exception as e:
            print(f"   Warning: Could not optimize ingredient overlap: {str(e)}")
            return suggestions
    
    def _print_suggestion_summary(self, suggestions):
        """Print summary of generated suggestions"""
        
        proteins = {}
        cuisines = {}
        sources = {}
        cooking_methods = {}
        
        for recipe in suggestions:
            protein = recipe.get('protein', 'unknown')
            cuisine = recipe.get('cuisine', 'unknown')
            source = recipe.get('source', 'unknown')
            method = recipe.get('cooking_method', 'unknown')
            
            proteins[protein] = proteins.get(protein, 0) + 1
            cuisines[cuisine] = cuisines.get(cuisine, 0) + 1
            sources[source] = sources.get(source, 0) + 1
            cooking_methods[method] = cooking_methods.get(method, 0) + 1
        
        print(f"   📊 Protein variety: {dict(proteins)}")
        print(f"   🌍 Cuisine variety: {dict(cuisines)}")
        print(f"   📖 Recipe sources: {dict(sources)}")
        print(f"   👨‍🍳 Cooking methods: {dict(cooking_methods)}")
    
    def save_weekly_suggestions(self, suggestions, week_date):
        """Save weekly suggestions to database"""
        if 'recipe_history' not in self.recipe_manager.recipe_db:
            self.recipe_manager.recipe_db['recipe_history'] = {}
        
        if 'weekly_suggestions' not in self.recipe_manager.recipe_db['recipe_history']:
            self.recipe_manager.recipe_db['recipe_history']['weekly_suggestions'] = []
        
        suggestion_record = {
            'week_date': week_date,
            'suggestions': suggestions,
            'generated_date': datetime.now().isoformat(),
            'total_count': len(suggestions),
            'web_recipe_count': len([r for r in suggestions if r.get('source') == 'web_search']),
            'favorite_count': len([r for r in suggestions if r.get('source') == 'user_favorite'])
        }
        
        self.recipe_manager.recipe_db['recipe_history']['weekly_suggestions'].append(suggestion_record)
        self.recipe_manager.save_database()
    
    def format_suggestions_for_user(self, suggestions):
        """Format suggestions as numbered list for user"""
        formatted_list = []
        formatted_list.append("# 🍽️ Weekly Dinner Recipe Suggestions\\n")
        formatted_list.append(f"Generated on: {datetime.now().strftime('%B %d, %Y')}\\n")
        formatted_list.append("All recipes are gluten-free and include protein + vegetables + starch\\n")
        formatted_list.append("Mix of your favorites and fresh discoveries from top cooking websites!\\n")
        
        for recipe in suggestions:
            num = recipe.get('suggestion_number', len(formatted_list))
            name = recipe.get('name', 'Unknown Recipe')
            url = recipe.get('url', '#')
            protein = recipe.get('protein', 'protein').title()
            vegetables = recipe.get('vegetables', 'vegetables')
            starch = recipe.get('starch', 'starch').title()
            cuisine = recipe.get('cuisine', 'various').title()
            prep_time = recipe.get('prep_time', 30)
            cooking_method = recipe.get('cooking_method', 'stove').replace('_', ' ').title()
            
            formatted_list.append(f"{num}. **{name}**")
            formatted_list.append(f"   - 🔗 Recipe Link: {url}")
            formatted_list.append(f"   - 🥩 Protein: {protein}")
            formatted_list.append(f"   - 🥬 Vegetables: {vegetables}")
            formatted_list.append(f"   - 🌾 Starch: {starch}")
            formatted_list.append(f"   - 🌍 Cuisine: {cuisine}")
            formatted_list.append(f"   - ⏱️ Prep Time: {prep_time} minutes")
            formatted_list.append(f"   - 👨‍🍳 Cooking Method: {cooking_method}")
            
            if recipe.get('source') == 'user_favorite':
                formatted_list.append(f"   - ⭐ *One of your favorites!*")
            elif recipe.get('source') == 'web_search':
                website = recipe.get('website', 'cooking website')
                formatted_list.append(f"   - 🌐 *Fresh from {website}*")
            
            formatted_list.append("")
        
        return "\\n".join(formatted_list)
    
    def update_suggestions_after_selection(self, selected_recipe, remaining_suggestions):
        """Update suggestions after user selects a recipe with web recipe integration"""
        
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
            print("   🔍 Getting additional recipe recommendations...")
            
            # Get both existing and web recipes
            user_preferences = self.recipe_manager.recipe_db.get('user_preferences', {})
            
            # Get existing recipe recommendations
            additional_existing = self.search_engine.get_recipe_recommendations(
                user_preferences,
                selected_this_week=[selected_recipe]
            )
            
            # Get fresh web recipes
            additional_web = self.web_searcher.search_cooking_websites(max_recipes=8)
            
            # Combine and filter additional recipes
            all_additional = additional_existing + additional_web
            
            # Add new recipes that aren't already in the list
            existing_names = set(r.get('name', '').lower() for r in filtered_suggestions)
            for recipe in all_additional:
                recipe_name = recipe.get('name', '').lower()
                if (recipe_name not in existing_names and 
                    len(filtered_suggestions) < 15 and
                    protein_counts.get(recipe.get('protein'), 0) < 2):
                    
                    filtered_suggestions.append(recipe)
                    existing_names.add(recipe_name)
                    protein = recipe.get('protein')
                    protein_counts[protein] = protein_counts.get(protein, 0) + 1
        
        # Optimize for ingredient overlap with selected recipe
        if len(filtered_suggestions) > 10:
            try:
                optimized_suggestions = self.search_engine.optimize_for_ingredient_overlap(
                    [selected_recipe] + filtered_suggestions[:10], 
                    target_count=4
                )[1:]  # Remove the selected recipe from the result
                
                # Add remaining suggestions
                remaining = [r for r in filtered_suggestions if r not in optimized_suggestions]
                filtered_suggestions = optimized_suggestions + remaining
            except Exception as e:
                print(f"   Warning: Could not optimize ingredient overlap: {str(e)}")
        
        # Re-number suggestions
        for i, recipe in enumerate(filtered_suggestions, 1):
            recipe['suggestion_number'] = i
        
        print(f"   ✅ Updated suggestions: {len(filtered_suggestions)} recipes available")
        return filtered_suggestions
    
    def get_recipe_suggestions_by_criteria(self, protein=None, cuisine=None, cooking_method=None, count=10):
        """Get recipe suggestions matching specific criteria"""
        
        suggestions = []
        
        # Get user favorites matching criteria
        user_favorites = self.recipe_manager.get_user_favorites()
        matching_favorites = []
        
        for recipe in user_favorites:
            if ((protein is None or recipe.get('protein') == protein) and
                (cuisine is None or recipe.get('cuisine') == cuisine) and
                (cooking_method is None or recipe.get('cooking_method') == cooking_method)):
                matching_favorites.append(recipe)
        
        # Add some favorites
        favorite_count = min(3, len(matching_favorites), count // 3)
        suggestions.extend(random.sample(matching_favorites, favorite_count))
        
        # Get web recipes matching criteria
        remaining_count = count - len(suggestions)
        if remaining_count > 0:
            web_recipes = self.web_searcher.search_by_criteria(
                protein=protein,
                cuisine=cuisine, 
                cooking_method=cooking_method,
                count=remaining_count + 2
            )
            
            # Filter out duplicates
            existing_names = set(r.get('name', '').lower() for r in suggestions)
            for recipe in web_recipes:
                if (len(suggestions) < count and 
                    recipe.get('name', '').lower() not in existing_names):
                    suggestions.append(recipe)
                    existing_names.add(recipe.get('name', '').lower())
        
        return suggestions[:count]

def main():
    """Test the enhanced weekly suggestion generator"""
    generator = EnhancedWeeklySuggestionGenerator()
    
    print("🔍 Testing Enhanced Weekly Suggestion Generator")
    print("=" * 60)
    
    # Generate weekly suggestions
    suggestions = generator.generate_weekly_suggestions()
    
    print(f"\\n📋 Generated {len(suggestions)} weekly suggestions")
    
    if suggestions:
        print(f"\\n🍽️ Sample Suggestions:")
        for i, recipe in enumerate(suggestions[:5], 1):
            source_emoji = "⭐" if recipe.get('source') == 'user_favorite' else "🌐" if recipe.get('source') == 'web_search' else "📚"
            name = recipe.get('name', 'Unknown Recipe')
            protein = recipe.get('protein', 'protein')
            vegetables = recipe.get('vegetables', 'vegetables')
            starch = recipe.get('starch', 'starch')
            cuisine = recipe.get('cuisine', 'various')
            cooking_method = recipe.get('cooking_method', 'stove')
            
            print(f"{i}. {source_emoji} {name}")
            print(f"   {protein} + {vegetables} + {starch}")
            print(f"   {cuisine} cuisine, {cooking_method} cooking")
        
        # Test formatting
        formatted = generator.format_suggestions_for_user(suggestions[:3])
        print(f"\\n📄 Formatted Output Preview:")
        print(formatted[:400] + "...")
        
        # Test criteria-based search
        print(f"\\n🎯 Testing Criteria-Based Search:")
        chicken_recipes = generator.get_recipe_suggestions_by_criteria(protein='chicken', count=5)
        print(f"Found {len(chicken_recipes)} chicken recipes")
        
        asian_recipes = generator.get_recipe_suggestions_by_criteria(cuisine='asian', count=5)
        print(f"Found {len(asian_recipes)} Asian recipes")
    
    print("\\n✅ Enhanced Weekly Suggestion Generator test completed!")

if __name__ == "__main__":
    main()

