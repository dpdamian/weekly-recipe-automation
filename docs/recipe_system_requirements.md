# Weekly Dinner Recipe System - Requirements & Architecture

## Core Requirements

### Weekly Recipe Suggestions
- Provide 15+ gluten-free dinner recipe ideas every Sunday
- Each meal must include: protein + vegetable + rice/grain/starch
- Recipes must have online links
- Present as numbered list

### User Preference Management
- Accept user's folder of liked recipes
- Use past preferences to suggest similar recipes
- Expand on liked recipes to find new ones
- Remember previous week suggestions to avoid repetition

### Interactive Selection Process
- User selects 4 dinners total for the week
- After each selection, refresh list with ingredient-optimized suggestions
- Optimize for ingredient overlap to reduce shopping complexity
- Ensure protein variety (max 2 times per week per protein type)

### Grocery List Generation
- Combine all selected recipe ingredients
- Sort by grocery store departments
- Optimize for shopping efficiency

## System Architecture

### Data Storage
1. **Recipe Database** (JSON/SQLite)
   - Recipe ID, name, URL, ingredients, protein type, cuisine
   - Gluten-free flag, difficulty, prep time
   - User rating/preference score

2. **User History** (JSON)
   - Past week selections
   - Liked/disliked recipes
   - Ingredient preferences
   - Protein rotation tracking

3. **Ingredient Database** (JSON)
   - Ingredient categories
   - Grocery store departments
   - Common substitutions

### Core Components

1. **Recipe Search Engine**
   - Web scraping for gluten-free recipes
   - API integration (if available)
   - Recipe validation and parsing

2. **Recommendation Algorithm**
   - Content-based filtering (similar to liked recipes)
   - Ingredient overlap optimization
   - Protein variety enforcement
   - Novelty vs familiarity balance

3. **Interactive Selection Interface**
   - Web-based UI for recipe browsing
   - Real-time list updates after selections
   - Ingredient overlap visualization

4. **Grocery List Generator**
   - Ingredient consolidation
   - Department categorization
   - Quantity optimization

### Automation Schedule
- Every Sunday: Generate new recipe suggestions
- Interactive selection process throughout the week
- Grocery list generation after 4 selections

## Technical Implementation Plan

### Phase 1: Core Data Structures
- Recipe database schema
- User preference tracking
- Ingredient categorization

### Phase 2: Recipe Collection
- Web scraping popular gluten-free recipe sites
- Manual curation of high-quality recipes
- Integration with user's existing recipe folder

### Phase 3: Recommendation Engine
- Similarity algorithms
- Ingredient optimization logic
- Protein rotation enforcement

### Phase 4: User Interface
- Web application for recipe selection
- Real-time updates and filtering
- Grocery list display and export

### Phase 5: Automation
- Scheduled task for weekly suggestions
- Email/notification system
- Data persistence and backup

