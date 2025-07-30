class RecipeSelector {
    constructor() {
        this.selectedRecipes = [];
        this.allRecipes = [];
        this.currentSuggestions = [];
        this.maxSelections = 4;
        
        this.init();
    }
    
    async init() {
        this.bindEvents();
        await this.loadWeeklySuggestions();
    }
    
    bindEvents() {
        // Filter controls
        document.getElementById('proteinFilter').addEventListener('change', () => this.filterRecipes());
        document.getElementById('cuisineFilter').addEventListener('change', () => this.filterRecipes());
        document.getElementById('cookingMethodFilter').addEventListener('change', () => this.filterRecipes());
        
        // Grocery list button
        document.getElementById('generateGroceryList').addEventListener('click', () => this.generateGroceryList());
        
        // Modal controls
        document.querySelector('.close').addEventListener('click', () => this.closeModal());
        document.getElementById('downloadGroceryList').addEventListener('click', () => this.downloadGroceryList());
        
        // Close modal when clicking outside
        window.addEventListener('click', (event) => {
            const modal = document.getElementById('groceryModal');
            if (event.target === modal) {
                this.closeModal();
            }
        });
    }
    
    async loadWeeklySuggestions() {
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/recipe/weekly-suggestions');
            const data = await response.json();
            
            if (data.success) {
                this.allRecipes = data.suggestions;
                this.currentSuggestions = [...this.allRecipes];
                this.renderRecipes();
            } else {
                this.showError('Failed to load recipes: ' + data.error);
            }
        } catch (error) {
            this.showError('Error loading recipes: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    renderRecipes() {
        const grid = document.getElementById('recipesGrid');
        grid.innerHTML = '';
        
        this.currentSuggestions.forEach(recipe => {
            const card = this.createRecipeCard(recipe);
            grid.appendChild(card);
        });
    }
    
    createRecipeCard(recipe) {
        const card = document.createElement('div');
        card.className = 'recipe-card';
        card.dataset.recipeId = recipe.id;
        
        const isSelected = this.selectedRecipes.some(r => r.id === recipe.id);
        const isDisabled = this.selectedRecipes.length >= this.maxSelections && !isSelected;
        
        if (isSelected) card.classList.add('selected');
        if (isDisabled) card.classList.add('disabled');
        
        const cookingMethod = recipe.cooking_method ? recipe.cooking_method.replace('_', ' ') : 'stove';
        const prepTime = recipe.prep_time || 30;
        const difficulty = recipe.difficulty || 'medium';
        
        card.innerHTML = `
            <h3>${recipe.name}</h3>
            <div class="recipe-info">
                <p><strong>Protein:</strong> ${recipe.protein || 'N/A'}</p>
                <p><strong>Vegetables:</strong> ${(recipe.vegetables || []).join(', ')}</p>
                <p><strong>Starch:</strong> ${recipe.starch || 'N/A'}</p>
                <p><strong>Prep Time:</strong> ${prepTime} minutes</p>
                <p><strong>Difficulty:</strong> ${difficulty}</p>
            </div>
            <div class="recipe-tags">
                <span class="tag protein">${recipe.protein || 'protein'}</span>
                <span class="tag cuisine">${recipe.cuisine || 'various'}</span>
                <span class="tag method">${cookingMethod}</span>
                ${recipe.source === 'user_favorite' ? '<span class="tag favorite">⭐ Favorite</span>' : ''}
            </div>
            ${recipe.url ? `<a href="${recipe.url}" target="_blank" class="recipe-link">View Recipe →</a>` : ''}
        `;
        
        if (!isDisabled) {
            card.addEventListener('click', () => this.toggleRecipeSelection(recipe));
        }
        
        return card;
    }
    
    async toggleRecipeSelection(recipe) {
        const isSelected = this.selectedRecipes.some(r => r.id === recipe.id);
        
        if (isSelected) {
            // Remove from selection
            this.selectedRecipes = this.selectedRecipes.filter(r => r.id !== recipe.id);
        } else {
            // Add to selection (if not at max)
            if (this.selectedRecipes.length < this.maxSelections) {
                this.selectedRecipes.push(recipe);
                
                // Update suggestions after selection
                await this.updateSuggestionsAfterSelection(recipe);
            }
        }
        
        this.updateUI();
    }
    
    async updateSuggestionsAfterSelection(selectedRecipe) {
        try {
            const response = await fetch('/api/recipe/update-suggestions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    selected_recipe: selectedRecipe,
                    remaining_suggestions: this.currentSuggestions.filter(r => r.id !== selectedRecipe.id)
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Update current suggestions with optimized list
                this.currentSuggestions = [
                    ...this.selectedRecipes,
                    ...data.updated_suggestions
                ];
                this.filterRecipes(); // Re-apply current filters
            }
        } catch (error) {
            console.error('Error updating suggestions:', error);
        }
    }
    
    updateUI() {
        this.updateProgress();
        this.renderSelectedRecipes();
        this.renderRecipes();
        this.updateIngredientOverlap();
        this.updateGroceryButton();
    }
    
    updateProgress() {
        const progress = (this.selectedRecipes.length / this.maxSelections) * 100;
        document.getElementById('progressFill').style.width = progress + '%';
        document.getElementById('selectedCount').textContent = this.selectedRecipes.length;
    }
    
    renderSelectedRecipes() {
        const container = document.getElementById('selectedRecipes');
        
        if (this.selectedRecipes.length === 0) {
            container.innerHTML = `
                <div class="empty-selection">
                    <p>Select recipes to see them here</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = this.selectedRecipes.map(recipe => `
            <div class="selected-recipe-item">
                <button class="remove-btn" onclick="recipeSelector.removeRecipe('${recipe.id}')">×</button>
                <h4>${recipe.name}</h4>
                <p>${recipe.protein} • ${recipe.cuisine} • ${recipe.cooking_method?.replace('_', ' ')}</p>
            </div>
        `).join('');
    }
    
    removeRecipe(recipeId) {
        this.selectedRecipes = this.selectedRecipes.filter(r => r.id !== recipeId);
        this.updateUI();
    }
    
    async updateIngredientOverlap() {
        const overlapContainer = document.getElementById('ingredientOverlap');
        
        if (this.selectedRecipes.length < 2) {
            overlapContainer.style.display = 'none';
            return;
        }
        
        try {
            const response = await fetch('/api/recipe/ingredient-overlap', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    recipe_ids: this.selectedRecipes.map(r => r.id)
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                const overlap = data.overlap_info;
                const efficiency = Math.round((overlap.overlap_score / overlap.total_unique_ingredients) * 100);
                
                document.getElementById('overlapInfo').innerHTML = `
                    <div class="overlap-stat">
                        <span>Shared Ingredients:</span>
                        <span><strong>${overlap.shared_ingredients.length}</strong></span>
                    </div>
                    <div class="overlap-stat">
                        <span>Total Unique:</span>
                        <span><strong>${overlap.total_unique_ingredients}</strong></span>
                    </div>
                    <div class="overlap-stat">
                        <span>Efficiency Score:</span>
                        <span><strong>${efficiency}%</strong></span>
                    </div>
                    ${overlap.shared_ingredients.length > 0 ? `
                        <p style="margin-top: 10px; font-size: 12px; color: #4a5568;">
                            <strong>Shared:</strong> ${overlap.shared_ingredients.slice(0, 3).join(', ')}
                            ${overlap.shared_ingredients.length > 3 ? '...' : ''}
                        </p>
                    ` : ''}
                `;
                
                overlapContainer.style.display = 'block';
            }
        } catch (error) {
            console.error('Error calculating ingredient overlap:', error);
        }
    }
    
    updateGroceryButton() {
        const button = document.getElementById('generateGroceryList');
        button.disabled = this.selectedRecipes.length !== this.maxSelections;
    }
    
    filterRecipes() {
        const proteinFilter = document.getElementById('proteinFilter').value;
        const cuisineFilter = document.getElementById('cuisineFilter').value;
        const methodFilter = document.getElementById('cookingMethodFilter').value;
        
        this.currentSuggestions = this.allRecipes.filter(recipe => {
            const matchesProtein = !proteinFilter || recipe.protein === proteinFilter;
            const matchesCuisine = !cuisineFilter || recipe.cuisine === cuisineFilter;
            const matchesMethod = !methodFilter || recipe.cooking_method === methodFilter;
            
            return matchesProtein && matchesCuisine && matchesMethod;
        });
        
        this.renderRecipes();
    }
    
    async generateGroceryList() {
        if (this.selectedRecipes.length !== this.maxSelections) {
            alert('Please select exactly 4 recipes first.');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/recipe/grocery-list', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    recipe_ids: this.selectedRecipes.map(r => r.id),
                    week_date: new Date().toISOString().split('T')[0]
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.displayGroceryList(data);
            } else {
                this.showError('Failed to generate grocery list: ' + data.error);
            }
        } catch (error) {
            this.showError('Error generating grocery list: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    displayGroceryList(data) {
        const content = document.getElementById('groceryContent');
        
        let html = `
            <div style="margin-bottom: 20px;">
                <p><strong>Estimated Cost:</strong> ${data.estimated_cost}</p>
                <p><strong>Total Recipes:</strong> ${data.selected_recipes.length}</p>
            </div>
        `;
        
        // Equipment reminders
        if (data.equipment_reminders && data.equipment_reminders.length > 0) {
            html += `
                <div style="margin-bottom: 20px; padding: 15px; background: #fff5f5; border-radius: 8px;">
                    <h3>⚙️ Equipment Reminders</h3>
                    <ul>
                        ${data.equipment_reminders.map(reminder => `<li>${reminder}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        // Shopping tips
        if (data.shopping_tips && data.shopping_tips.length > 0) {
            html += `
                <div style="margin-bottom: 20px; padding: 15px; background: #f0fff4; border-radius: 8px;">
                    <h3>💡 Shopping Tips</h3>
                    <ul>
                        ${data.shopping_tips.map(tip => `<li>${tip}</li>`).join('')}
                    </ul>
                </div>
            `;
        }
        
        // Grocery list by department
        const departmentEmojis = {
            'produce': '🥬',
            'meat_seafood': '🥩',
            'dairy': '🥛',
            'pantry': '🏺',
            'frozen': '🧊',
            'condiments': '🍯',
            'spices': '🌿',
            'other': '📦'
        };
        
        Object.entries(data.grocery_list).forEach(([department, items]) => {
            const emoji = departmentEmojis[department] || '📦';
            const deptName = department.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            html += `
                <div class="grocery-department">
                    <h3>${emoji} ${deptName}</h3>
                    ${items.map(item => `
                        <div class="grocery-item">
                            <input type="checkbox" id="item_${item.name.replace(/\s+/g, '_')}">
                            <label for="item_${item.name.replace(/\s+/g, '_')}">
                                <strong>${item.quantity}</strong> ${item.name}
                                ${item.recipes.length > 1 ? `<br><small>Used in: ${item.recipes.join(', ')}</small>` : ''}
                            </label>
                        </div>
                    `).join('')}
                </div>
            `;
        });
        
        content.innerHTML = html;
        this.currentGroceryData = data;
        document.getElementById('groceryModal').style.display = 'flex';
    }
    
    downloadGroceryList() {
        if (!this.currentGroceryData) return;
        
        const content = this.currentGroceryData.formatted_list;
        const blob = new Blob([content], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `grocery_list_${new Date().toISOString().split('T')[0]}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    closeModal() {
        document.getElementById('groceryModal').style.display = 'none';
    }
    
    showLoading(show) {
        document.getElementById('loadingSpinner').style.display = show ? 'flex' : 'none';
    }
    
    showError(message) {
        alert(message); // Simple error handling - could be improved with a proper modal
    }
}

// Initialize the recipe selector when the page loads
let recipeSelector;
document.addEventListener('DOMContentLoaded', () => {
    recipeSelector = new RecipeSelector();
});

