#!/usr/bin/env python3
"""
Ingredient Database Creation
Creates categorized ingredient database for grocery list organization
"""

import json

def create_ingredient_database():
    """Create comprehensive ingredient database with grocery store categories"""
    
    ingredient_db = {
        "categories": {
            "produce": {
                "vegetables": [
                    "broccoli", "carrots", "bell peppers", "tomatoes", "cucumbers", 
                    "snap peas", "onions", "zucchini", "sweet potatoes", "green beans",
                    "bok choy", "mushrooms", "asparagus", "cherry tomatoes", "spinach",
                    "kale", "cauliflower", "brussels sprouts", "cabbage", "lettuce",
                    "celery", "garlic", "ginger", "jalapeños", "avocado"
                ],
                "fruits": [
                    "lemons", "limes", "oranges", "apples", "bananas", "berries",
                    "grapes", "pineapple", "mango", "papaya"
                ],
                "herbs": [
                    "basil", "cilantro", "parsley", "thyme", "rosemary", "oregano",
                    "sage", "dill", "mint", "chives"
                ]
            },
            "meat_seafood": {
                "poultry": [
                    "chicken breast", "chicken thighs", "ground chicken", "turkey breast",
                    "ground turkey", "duck"
                ],
                "beef": [
                    "beef strips", "ground beef", "beef tenderloin", "sirloin",
                    "ribeye", "chuck roast"
                ],
                "pork": [
                    "pork tenderloin", "pork chops", "ground pork", "bacon",
                    "ham", "sausage"
                ],
                "seafood": [
                    "salmon fillet", "white fish", "shrimp", "scallops", "cod",
                    "tilapia", "tuna", "mahi mahi"
                ]
            },
            "pantry": {
                "grains": [
                    "rice", "quinoa", "brown rice", "wild rice", "rice noodles",
                    "gluten-free pasta", "oats", "millet"
                ],
                "oils_vinegars": [
                    "olive oil", "sesame oil", "coconut oil", "avocado oil",
                    "rice vinegar", "apple cider vinegar", "balsamic vinegar"
                ],
                "condiments": [
                    "soy sauce", "teriyaki sauce", "stir fry sauce", "hot sauce",
                    "mustard", "mayo", "ketchup"
                ],
                "spices": [
                    "salt", "pepper", "garlic powder", "onion powder", "paprika",
                    "cumin", "chili powder", "turmeric", "ginger powder"
                ],
                "canned_goods": [
                    "coconut milk", "diced tomatoes", "tomato paste", "broth",
                    "beans", "lentils"
                ]
            },
            "dairy": {
                "cheese": [
                    "feta cheese", "mozzarella", "parmesan", "cheddar", "goat cheese"
                ],
                "dairy_products": [
                    "eggs", "butter", "milk", "yogurt", "cream cheese"
                ]
            },
            "frozen": {
                "vegetables": [
                    "frozen broccoli", "frozen peas", "frozen corn", "frozen spinach"
                ],
                "proteins": [
                    "frozen shrimp", "frozen fish fillets"
                ]
            },
            "other": {
                "nuts_seeds": [
                    "almonds", "walnuts", "cashews", "sesame seeds", "chia seeds"
                ],
                "olives": [
                    "olives", "kalamata olives", "green olives"
                ]
            }
        },
        "substitutions": {
            "rice": ["quinoa", "cauliflower rice", "brown rice"],
            "soy sauce": ["coconut aminos", "tamari"],
            "regular pasta": ["gluten-free pasta", "rice noodles", "zucchini noodles"]
        },
        "gluten_free_alternatives": {
            "wheat flour": "almond flour",
            "bread crumbs": "gluten-free bread crumbs",
            "soy sauce": "tamari",
            "regular pasta": "gluten-free pasta"
        }
    }
    
    # Save to file
    with open('/home/ubuntu/ingredient_database.json', 'w') as f:
        json.dump(ingredient_db, f, indent=2)
    
    print("Ingredient database created with grocery store categories")
    print(f"Categories: {list(ingredient_db['categories'].keys())}")
    
    return ingredient_db

def categorize_ingredient(ingredient, ingredient_db):
    """Categorize an ingredient for grocery list organization"""
    
    ingredient_lower = ingredient.lower()
    
    for category, subcategories in ingredient_db['categories'].items():
        for subcategory, items in subcategories.items():
            if ingredient_lower in [item.lower() for item in items]:
                return category
    
    # Default category if not found
    return "other"

if __name__ == "__main__":
    create_ingredient_database()

