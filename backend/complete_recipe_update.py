#!/usr/bin/env python3
"""
Complete Recipe Update Script
Updates all recipes in simple_recipe_generator.py with vegetables, starch, instructions, and real URLs
"""

import re

# Read the current file
with open('simple_recipe_generator.py', 'r') as f:
    content = f.read()

# Define the complete updated recipes with all required fields
updated_recipes = '''            'salmon': [
                {
                    'name': 'Teriyaki Salmon with Asparagus and Rice',
                    'protein': 'salmon',
                    'vegetables': 'asparagus',
                    'starch': 'brown rice',
                    'cuisine': 'asian',
                    'cooking_method': 'oven',
                    'prep_time': 10,
                    'cook_time': 20,
                    'difficulty': 'easy',
                    'ingredients': [
                        '4 salmon fillets',
                        '1 lb asparagus',
                        '1 cup brown rice',
                        '3 tbsp gluten-free teriyaki sauce',
                        '1 tbsp sesame oil',
                        '1 tbsp sesame seeds',
                        'Salt and pepper to taste'
                    ],
                    'instructions': [
                        'Preheat oven to 400°F (200°C).',
                        'Cook brown rice according to package directions.',
                        'Line a baking sheet with parchment paper.',
                        'Trim asparagus ends and place on baking sheet.',
                        'Season salmon fillets with salt and pepper.',
                        'Place salmon on the baking sheet with asparagus.',
                        'Brush salmon with teriyaki sauce and drizzle asparagus with sesame oil.',
                        'Bake for 12-15 minutes until salmon flakes easily.',
                        'Sprinkle with sesame seeds before serving.',
                        'Serve salmon and asparagus over brown rice.'
                    ],
                    'url': 'https://www.wellplated.com/teriyaki-salmon/'
                },
                {
                    'name': 'Lemon Herb Salmon with Sweet Potato',
                    'protein': 'salmon',
                    'vegetables': 'green beans',
                    'starch': 'sweet potato',
                    'cuisine': 'american',
                    'cooking_method': 'oven',
                    'prep_time': 15,
                    'cook_time': 25,
                    'difficulty': 'easy',
                    'ingredients': [
                        '4 salmon fillets',
                        '2 large sweet potatoes, cubed',
                        '1 cup green beans',
                        '2 tbsp olive oil',
                        '1 lemon, juiced',
                        '1 tsp dried herbs',
                        'Salt and pepper to taste'
                    ],
                    'instructions': [
                        'Preheat oven to 425°F (220°C).',
                        'Cube sweet potatoes and toss with 1 tbsp olive oil.',
                        'Roast sweet potatoes for 15 minutes.',
                        'Add green beans to the baking sheet.',
                        'Season salmon with salt, pepper, and herbs.',
                        'Place salmon on the baking sheet with vegetables.',
                        'Drizzle remaining olive oil and lemon juice over everything.',
                        'Bake for 12-15 minutes until salmon is cooked through.',
                        'Check that salmon flakes easily with a fork.',
                        'Serve immediately with roasted vegetables.'
                    ],
                    'url': 'https://www.eatingwell.com/recipe/276265/lemon-herb-salmon-with-caramelized-fennel-sweet-potatoes/'
                }
            ],
            'turkey': [
                {
                    'name': 'Turkey and Sweet Potato Bowl',
                    'protein': 'turkey',
                    'vegetables': 'spinach and onion',
                    'starch': 'sweet potato',
                    'cuisine': 'american',
                    'cooking_method': 'stove',
                    'prep_time': 15,
                    'cook_time': 20,
                    'difficulty': 'easy',
                    'ingredients': [
                        '1 lb ground turkey',
                        '2 sweet potatoes, cubed',
                        '1 cup spinach',
                        '1 onion, diced',
                        '2 tbsp olive oil',
                        '1 tsp cumin',
                        '1 tsp paprika',
                        'Salt and pepper to taste'
                    ],
                    'instructions': [
                        'Cube sweet potatoes and boil for 12-15 minutes until tender.',
                        'Heat 1 tbsp olive oil in a large skillet over medium heat.',
                        'Add diced onion and cook for 3-4 minutes until softened.',
                        'Add ground turkey and cook until browned, breaking it up.',
                        'Season with cumin, paprika, salt, and pepper.',
                        'Add cooked sweet potatoes to the skillet.',
                        'Cook for 3-4 minutes, stirring gently to combine.',
                        'Add spinach and cook until wilted.',
                        'Drizzle with remaining olive oil.',
                        'Serve in bowls and enjoy!'
                    ],
                    'url': 'https://www.budgetbytes.com/turkey-sweet-potato-skillet/'
                }
            ],
            'shrimp': [
                {
                    'name': 'Coconut Shrimp Curry with Rice',
                    'protein': 'shrimp',
                    'vegetables': 'bell pepper',
                    'starch': 'jasmine rice',
                    'cuisine': 'thai',
                    'cooking_method': 'stove',
                    'prep_time': 15,
                    'cook_time': 20,
                    'difficulty': 'medium',
                    'ingredients': [
                        '1 lb large shrimp',
                        '1 cup jasmine rice',
                        '1 can coconut milk',
                        '1 bell pepper, sliced',
                        '1 tbsp curry paste',
                        '1 tbsp fish sauce (gluten-free)',
                        '1 lime, juiced',
                        'Fresh cilantro'
                    ],
                    'instructions': [
                        'Cook jasmine rice according to package directions.',
                        'Peel and devein shrimp, pat dry.',
                        'Heat a large skillet over medium-high heat.',
                        'Add curry paste and cook for 1 minute until fragrant.',
                        'Add coconut milk and bring to a simmer.',
                        'Add sliced bell pepper and cook for 3-4 minutes.',
                        'Add shrimp and cook for 3-4 minutes until pink.',
                        'Stir in fish sauce and lime juice.',
                        'Remove from heat and garnish with cilantro.',
                        'Serve over jasmine rice.'
                    ],
                    'url': 'https://www.recipetineats.com/thai-red-curry-with-prawns/'
                }
            ],
            'pork': [
                {
                    'name': 'Pork Tenderloin with Roasted Vegetables',
                    'protein': 'pork',
                    'vegetables': 'mixed vegetables (carrots, Brussels sprouts)',
                    'starch': 'quinoa',
                    'cuisine': 'american',
                    'cooking_method': 'oven',
                    'prep_time': 20,
                    'cook_time': 30,
                    'difficulty': 'medium',
                    'ingredients': [
                        '1 lb pork tenderloin',
                        '2 cups mixed vegetables (carrots, Brussels sprouts)',
                        '1 cup quinoa',
                        '2 tbsp olive oil',
                        '1 tsp rosemary',
                        '1 tsp thyme',
                        'Salt and pepper to taste'
                    ],
                    'instructions': [
                        'Preheat oven to 425°F (220°C).',
                        'Cook quinoa according to package directions.',
                        'Season pork tenderloin with salt, pepper, rosemary, and thyme.',
                        'Heat 1 tbsp olive oil in an oven-safe skillet over high heat.',
                        'Sear pork tenderloin on all sides until browned.',
                        'Toss vegetables with remaining olive oil, salt, and pepper.',
                        'Add vegetables around the pork in the skillet.',
                        'Transfer to oven and roast for 15-20 minutes.',
                        'Check that pork reaches 145°F internal temperature.',
                        'Let rest for 5 minutes before slicing and serving over quinoa.'
                    ],
                    'url': 'https://www.foodnetwork.com/recipes/ellie-krieger/herb-crusted-pork-tenderloin-with-roasted-vegetables-recipe-1946783'
                }
            ]'''

# Replace the salmon section and everything after it
pattern = r"            'salmon': \[.*"
replacement = updated_recipes + '''
        }
    
    def generate_recipes(self, count=15):
        """Generate a diverse set of recipes"""
        recipes = []
        recipe_id = 1
        
        # Get recipes from each protein category
        for protein, protein_recipes in self.recipe_templates.items():
            for recipe_template in protein_recipes:
                recipe = recipe_template.copy()
                recipe['id'] = f"simple_{recipe_id:03d}"
                recipe['source'] = 'curated'
                recipes.append(recipe)
                recipe_id += 1
        
        # Shuffle and return requested count
        import random
        random.shuffle(recipes)
        return recipes[:count]

if __name__ == "__main__":
    generator = SimpleRecipeGenerator()
    recipes = generator.generate_recipes(15)
    
    print(f"Generated {len(recipes)} recipes:")
    for recipe in recipes:
        print(f"- {recipe['name']} ({recipe['protein']}, {recipe['vegetables']}, {recipe['starch']})")'''

# Apply the replacement
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write the updated content back
with open('simple_recipe_generator.py', 'w') as f:
    f.write(new_content)

print("✅ Updated all recipes with vegetables, starch, instructions, and real URLs!")

