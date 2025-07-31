// Weekly Recipe Automation - Enhanced Cooking Site Experience
class RecipeSelector {
    constructor() {
        this.selectedRecipes = [];
        this.allRecipes = [];
        this.maxSelections = 4;
        this.init();
    }

    async init() {
        this.showLoading('🍳 Loading your weekly recipe collection...');
        await this.loadRecipes();
        this.setupEventListeners();
        this.hideLoading();
        this.showWelcomeMessage();
    }

    showWelcomeMessage() {
        // Add a subtle welcome animation
        const header = document.querySelector('header');
        header.style.transform = 'translateY(-20px)';
        header.style.opacity = '0';
        
        setTimeout(() => {
            header.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            header.style.transform = 'translateY(0)';
            header.style.opacity = '1';
        }, 100);
    }

    async loadRecipes() {
        try {
            const response = await fetch('/api/recipe/weekly-suggestions');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            this.allRecipes = data.suggestions || [];
            this.renderRecipes();
        } catch (error) {
            console.error('Error loading recipes:', error);
            this.showError('🍽️ Oops! We had trouble loading your recipes. Please refresh the page to try again.');
        }
    }

    async generateFreshRecipes() {
        const button = document.getElementById('generateRecipesBtn');
        const originalText = button.innerHTML;
        
        // Disable button and show loading state
        button.disabled = true;
        button.innerHTML = '🔄 Generating Fresh Recipes...';
        
        // Clear current selections
        this.selectedRecipes = [];
        
        this.showLoading('🌐 Searching cooking websites for fresh gluten-free recipes...');
        
        try {
            const response = await fetch('/api/recipe/weekly-suggestions?include_web=true');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            if (data.success) {
                this.allRecipes = data.suggestions || [];
                this.renderRecipes();
                this.updateUI();
                
                // Show success message with statistics
                const summary = data.summary || {};
                const webCount = summary.source_breakdown?.web_search || 0;
                const favoriteCount = summary.source_breakdown?.user_favorite || 0;
                
                this.showNotification(
                    `🎉 Generated ${this.allRecipes.length} fresh recipes! ` +
                    `(${webCount} new from cooking websites, ${favoriteCount} favorites)`, 
                    'success'
                );
                
                // Scroll to recipes section
                document.querySelector('.recipes-section').scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'start' 
                });
            } else {
                throw new Error(data.error || 'Failed to generate recipes');
            }
        } catch (error) {
            console.error('Error generating fresh recipes:', error);
            this.showError('🍽️ Sorry, we had trouble generating fresh recipes. Please try again in a moment.');
        } finally {
            // Re-enable button
            button.disabled = false;
            button.innerHTML = originalText;
            this.hideLoading();
        }
    }

    renderRecipes(filteredRecipes = null) {
        const recipesToRender = filteredRecipes || this.allRecipes;
        const grid = document.getElementById('recipesGrid');
        
        if (recipesToRender.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: var(--soft-gray);">
                    <div style="font-size: 4em; margin-bottom: 20px;">🔍</div>
                    <h3 style="font-family: 'Playfair Display', serif; margin-bottom: 10px;">No recipes found</h3>
                    <p>Try adjusting your filters to discover more delicious options!</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = recipesToRender.map(recipe => this.createRecipeCard(recipe)).join('');
    }

    createRecipeCard(recipe) {
        const isSelected = this.selectedRecipes.some(r => r.id === recipe.id);
        const isDisabled = !isSelected && this.selectedRecipes.length >= this.maxSelections;
        
        // Enhanced recipe card with cooking-themed styling
        return `
            <div class="recipe-card ${isSelected ? 'selected' : ''} ${isDisabled ? 'disabled' : ''}" 
                 data-recipe-id="${recipe.id}" 
                 onclick="${isDisabled ? '' : `recipeSelector.toggleRecipe('${recipe.id}')`}">
                
                <h3>${recipe.name}</h3>
                
                <div class="recipe-tags">
                    <span class="tag protein">${this.getProteinEmoji(recipe.protein)} ${recipe.protein}</span>
                    <span class="tag cuisine">${this.getCuisineEmoji(recipe.cuisine)} ${recipe.cuisine}</span>
                    <span class="tag method">${this.getMethodEmoji(recipe.cooking_method)} ${recipe.cooking_method}</span>
                    ${recipe.source === 'user_favorite' ? '<span class="tag favorite">⭐ Favorite</span>' : ''}
                </div>
                
                <div class="recipe-info">
                    <p><strong>🥬 Vegetables:</strong> ${recipe.vegetables}</p>
                    <p><strong>🌾 Starch:</strong> ${recipe.starch}</p>
                    <p><strong>⏱️ Prep Time:</strong> ${recipe.prep_time} minutes</p>
                    <p><strong>👨‍🍳 Difficulty:</strong> ${this.getDifficultyDisplay(recipe.difficulty)}</p>
                </div>
                
                ${recipe.url ? `<a href="${recipe.url}" target="_blank" class="recipe-link">View Full Recipe</a>` : ''}
            </div>
        `;
    }

    getProteinEmoji(protein) {
        const emojis = {
            'chicken': '🐔',
            'beef': '🥩',
            'fish': '🐟',
            'salmon': '🍣',
            'shrimp': '🦐',
            'turkey': '🦃',
            'pork': '🐷'
        };
        return emojis[protein] || '🍖';
    }

    getCuisineEmoji(cuisine) {
        const emojis = {
            'asian': '🥢',
            'mediterranean': '🫒',
            'american': '🇺🇸',
            'indian': '🍛',
            'thai': '🌶️',
            'mexican': '🌮'
        };
        return emojis[cuisine] || '🌍';
    }

    getMethodEmoji(method) {
        const emojis = {
            'stove': '🔥',
            'oven': '🔥',
            'grill': '🔥',
            'air_fryer': '💨',
            'instant_pot': '⚡'
        };
        return emojis[method] || '👨‍🍳';
    }

    getDifficultyDisplay(difficulty) {
        const levels = {
            'easy': '⭐ Easy',
            'medium': '⭐⭐ Medium',
            'hard': '⭐⭐⭐ Hard'
        };
        return levels[difficulty] || '⭐ Easy';
    }

    async toggleRecipe(recipeId) {
        const recipe = this.allRecipes.find(r => r.id === recipeId);
        if (!recipe) return;

        const existingIndex = this.selectedRecipes.findIndex(r => r.id === recipeId);
        
        if (existingIndex >= 0) {
            // Remove recipe with animation
            this.selectedRecipes.splice(existingIndex, 1);
            this.showNotification(`🗑️ Removed "${recipe.name}" from your menu`, 'info');
        } else if (this.selectedRecipes.length < this.maxSelections) {
            // Add recipe with animation
            this.selectedRecipes.push(recipe);
            this.showNotification(`✅ Added "${recipe.name}" to your menu!`, 'success');
        }

        this.updateUI();
        this.updateIngredientOverlap();
        
        // Update recipe suggestions for ingredient optimization
        await this.updateRecipeSuggestions();
    }

    async updateRecipeSuggestions() {
        if (this.selectedRecipes.length === 0) {
            return; // No need to update if no recipes selected
        }

        try {
            // Show loading state
            this.showLoading('🔄 Finding recipes with shared ingredients...');
            
            // Get remaining unselected recipes
            const selectedIds = this.selectedRecipes.map(r => r.id);
            const remainingRecipes = this.allRecipes.filter(r => !selectedIds.includes(r.id));
            
            // Call API to get optimized suggestions
            const response = await fetch('/api/recipe/update-suggestions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    selected_recipe: this.selectedRecipes[this.selectedRecipes.length - 1], // Last selected
                    remaining_suggestions: remainingRecipes
                })
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success && data.updated_suggestions) {
                    // Update the recipe list with optimized suggestions
                    const selectedIds = this.selectedRecipes.map(r => r.id);
                    const newSuggestions = data.updated_suggestions.filter(r => !selectedIds.includes(r.id));
                    
                    // Keep selected recipes and add new optimized suggestions
                    this.allRecipes = [...this.selectedRecipes, ...newSuggestions];
                    
                    // Re-render the recipe list
                    this.renderRecipes();
                    
                    this.showNotification(
                        `🎯 Updated recipes to optimize ingredient overlap! Found ${newSuggestions.length} recipes with shared ingredients.`, 
                        'success'
                    );
                }
            }
        } catch (error) {
            console.error('Error updating recipe suggestions:', error);
            // Don't show error to user as this is an enhancement feature
        } finally {
            this.hideLoading();
        }
    }

    updateUI() {
        this.updateProgress();
        this.updateSelectedRecipes();
        this.renderRecipes();
        this.updateGroceryButton();
    }

    updateProgress() {
        const progress = (this.selectedRecipes.length / this.maxSelections) * 100;
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        progressFill.style.width = `${progress}%`;
        
        const messages = [
            "Select 4 delicious recipes for your week (0/4 selected)",
            "Great start! Keep building your menu (1/4 selected) 🍽️",
            "You're halfway there! (2/4 selected) 👨‍🍳",
            "Almost ready for a fantastic week! (3/4 selected) 🌟",
            "Perfect! Your weekly menu is complete! (4/4 selected) 🎉"
        ];
        
        progressText.textContent = messages[this.selectedRecipes.length];
    }

    updateSelectedRecipes() {
        const container = document.getElementById('selectedRecipes');
        
        if (this.selectedRecipes.length === 0) {
            container.innerHTML = `
                <div class="empty-selection">
                    <p>Start building your delicious week by selecting recipes from the collection!</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.selectedRecipes.map((recipe, index) => `
            <div class="selected-recipe-item" style="animation: slideIn 0.5s ease ${index * 0.1}s both;">
                <button class="remove-btn" onclick="recipeSelector.toggleRecipe('${recipe.id}')" title="Remove recipe">×</button>
                <h4>${recipe.name}</h4>
                <p>${this.getProteinEmoji(recipe.protein)} ${recipe.protein} • ${this.getCuisineEmoji(recipe.cuisine)} ${recipe.cuisine} • ${this.getMethodEmoji(recipe.cooking_method)} ${recipe.cooking_method}</p>
            </div>
        `).join('');
    }

    async updateIngredientOverlap() {
        if (this.selectedRecipes.length < 2) {
            document.getElementById('ingredientOverlap').style.display = 'none';
            return;
        }

        try {
            const response = await fetch('/api/recipe/ingredient-overlap', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    recipe_ids: this.selectedRecipes.map(r => r.id)
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.displayIngredientOverlap(data);
            }
        } catch (error) {
            console.error('Error calculating ingredient overlap:', error);
        }
    }

    displayIngredientOverlap(data) {
        const container = document.getElementById('ingredientOverlap');
        const statsContainer = document.getElementById('overlapStats');
        
        const efficiency = Math.round((data.shared_ingredients.length / data.total_unique_ingredients) * 100);
        const efficiencyEmoji = efficiency >= 70 ? '🌟' : efficiency >= 50 ? '👍' : '💡';
        
        statsContainer.innerHTML = `
            <div class="overlap-stat">
                <span>🔄 Shared Ingredients:</span>
                <span>${data.shared_ingredients.length}</span>
            </div>
            <div class="overlap-stat">
                <span>📦 Total Unique Items:</span>
                <span>${data.total_unique_ingredients}</span>
            </div>
            <div class="overlap-stat">
                <span>${efficiencyEmoji} Shopping Efficiency:</span>
                <span>${efficiency}%</span>
            </div>
        `;
        
        container.style.display = 'block';
    }

    updateGroceryButton() {
        const button = document.getElementById('generateGroceryBtn');
        const isComplete = this.selectedRecipes.length === this.maxSelections;
        
        button.disabled = !isComplete;
        
        if (isComplete) {
            button.textContent = '🛒 Generate Smart Grocery List';
            button.style.background = 'var(--warm-gradient)';
        } else {
            button.textContent = `🛒 Select ${this.maxSelections - this.selectedRecipes.length} more recipe${this.maxSelections - this.selectedRecipes.length !== 1 ? 's' : ''}`;
            button.style.background = 'var(--soft-gray)';
        }
    }

    async generateGroceryList() {
        if (this.selectedRecipes.length !== this.maxSelections) return;

        this.showLoading('🛒 Creating your personalized grocery list...');

        try {
            const response = await fetch('/api/recipe/grocery-list', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    recipe_ids: this.selectedRecipes.map(r => r.id),
                    selected_recipes: this.selectedRecipes, // Send full recipe data as fallback
                    week_date: new Date().toISOString().split('T')[0]
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.success) {
                this.displayGroceryList(data);
                this.showNotification('🎉 Your grocery list is ready!', 'success');
            } else {
                throw new Error(data.error || 'Unknown error generating grocery list');
            }
            
            this.hideLoading();
        } catch (error) {
            console.error('Error generating grocery list:', error);
            this.hideLoading();
            this.showError(`🛒 Sorry, we had trouble creating your grocery list: ${error.message}`);
        }
    }

    displayGroceryList(data) {
        const modal = document.getElementById('groceryModal');
        const content = document.getElementById('groceryListContent');
        
        const groceryList = data.raw_data.grocery_list;
        const selectedRecipes = data.selected_recipes || this.selectedRecipes;
        const departmentEmojis = {
            'produce': '🥬',
            'meat_seafood': '🥩',
            'dairy': '🥛',
            'pantry': '🏺',
            'frozen': '🧊',
            'condiments': '🍯',
            'spices': '🌿'
        };

        let html = '';
        
        // Selected recipes with cooking instructions
        html += `
            <div class="grocery-section">
                <h2>🍽️ Your Weekly Menu</h2>
                <div class="selected-recipes-summary">
                    ${selectedRecipes.map((recipe, index) => `
                        <div class="recipe-summary-card">
                            <div class="recipe-summary-header">
                                <h4>${recipe.name}</h4>
                                <span class="recipe-meta">
                                    ${this.getProteinEmoji(recipe.protein)} ${recipe.protein} • 
                                    ${this.getCuisineEmoji(recipe.cuisine)} ${recipe.cuisine} • 
                                    ${this.getMethodEmoji(recipe.cooking_method)} ${recipe.cooking_method}
                                </span>
                            </div>
                            ${recipe.instructions ? `
                                <div class="cooking-instructions">
                                    <h5>👨‍🍳 Cooking Instructions:</h5>
                                    <ol>
                                        ${recipe.instructions.map(step => `<li>${step}</li>`).join('')}
                                    </ol>
                                    <p class="cook-time">⏱️ Prep: ${recipe.prep_time || 15} min • Cook: ${recipe.cook_time || 25} min</p>
                                </div>
                            ` : `
                                <div class="cooking-instructions">
                                    <p>📖 <a href="${recipe.url || '#'}" target="_blank">View full recipe and instructions</a></p>
                                </div>
                            `}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        // Grocery list by department
        html += `<div class="grocery-section"><h2>🛒 Shopping List</h2>`;
        
        for (const [department, items] of Object.entries(groceryList)) {
            const emoji = departmentEmojis[department] || '🛒';
            const deptName = department.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            html += `
                <div class="grocery-department">
                    <h3>${emoji} ${deptName} (${items.length} items)</h3>
                    ${items.map(item => `
                        <div class="grocery-item">
                            <input type="checkbox" id="item-${item.name.replace(/\s+/g, '-')}">
                            <label for="item-${item.name.replace(/\s+/g, '-')}">${item.quantity} ${item.name}</label>
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        html += `</div>`;

        // Additional information
        if (data.raw_data.equipment_reminders?.length > 0) {
            html += `
                <div class="grocery-section">
                    <h3>⚙️ Equipment Reminders</h3>
                    ${data.raw_data.equipment_reminders.map(reminder => `
                        <div class="grocery-item">
                            <span style="margin-left: 30px;">• ${reminder}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        if (data.raw_data.shopping_tips?.length > 0) {
            html += `
                <div class="grocery-section">
                    <h3>💡 Shopping Tips</h3>
                    ${data.raw_data.shopping_tips.map(tip => `
                        <div class="grocery-item">
                            <span style="margin-left: 30px;">• ${tip}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }

        content.innerHTML = html;
        modal.style.display = 'block';
    }

    closeGroceryModal() {
        document.getElementById('groceryModal').style.display = 'none';
    }

    downloadGroceryList() {
        if (!this.formattedGroceryList) return;

        const blob = new Blob([this.formattedGroceryList], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `weekly-grocery-list-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        this.showNotification('📥 Grocery list downloaded successfully!', 'success');
    }

    setupEventListeners() {
        // Generate fresh recipes button
        document.getElementById('generateRecipesBtn').addEventListener('click', () => this.generateFreshRecipes());
        
        // Filter controls
        ['proteinFilter', 'cuisineFilter', 'methodFilter'].forEach(filterId => {
            document.getElementById(filterId).addEventListener('change', () => this.applyFilters());
        });

        // Grocery list generation
        document.getElementById('generateGroceryBtn').addEventListener('click', () => this.generateGroceryList());

        // Modal controls
        document.getElementById('closeModal').addEventListener('click', () => {
            document.getElementById('groceryModal').style.display = 'none';
        });

        document.getElementById('downloadBtn').addEventListener('click', () => this.downloadGroceryList());

        // Close modal when clicking outside
        document.getElementById('groceryModal').addEventListener('click', (e) => {
            if (e.target.id === 'groceryModal') {
                document.getElementById('groceryModal').style.display = 'none';
            }
        });
    }

    applyFilters() {
        const proteinFilter = document.getElementById('proteinFilter').value;
        const cuisineFilter = document.getElementById('cuisineFilter').value;
        const methodFilter = document.getElementById('methodFilter').value;

        let filtered = this.allRecipes;

        if (proteinFilter) {
            filtered = filtered.filter(recipe => recipe.protein === proteinFilter);
        }

        if (cuisineFilter) {
            filtered = filtered.filter(recipe => recipe.cuisine === cuisineFilter);
        }

        if (methodFilter) {
            filtered = filtered.filter(recipe => recipe.cooking_method === methodFilter);
        }

        this.renderRecipes(filtered);
    }

    showLoading(message = '🍳 Preparing your culinary adventure...') {
        const overlay = document.getElementById('loadingOverlay');
        const text = overlay.querySelector('p');
        text.textContent = message;
        overlay.style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? 'var(--sage-green)' : type === 'error' ? 'var(--warm-red)' : 'var(--primary-orange)'};
            color: white;
            padding: 15px 25px;
            border-radius: 12px;
            font-weight: 600;
            z-index: 3000;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            transform: translateX(400px);
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            max-width: 350px;
            font-family: 'Inter', sans-serif;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Animate out and remove
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 400);
        }, 3000);
    }

    showError(message) {
        this.showNotification(message, 'error');
    }
}

// Add CSS animation for slide-in effect
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// Initialize the application
const recipeSelector = new RecipeSelector();

