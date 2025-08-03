// Fixed Recipe Selector with better error handling and fallback mechanisms
class RecipeSelector {
    constructor() {
        this.selectedRecipes = [];
        this.allRecipes = [];
        this.maxSelections = 4;
        this.apiRetryCount = 0;
        this.maxRetries = 3;
        this.init();
    }

    async init() {
        console.log('🍳 Initializing Recipe Selector...');
        this.showLoading('🍳 Loading your weekly recipe collection...');
        
        // Add event listeners first
        this.setupEventListeners();
        
        // Then try to load recipes
        await this.loadRecipes();
        this.hideLoading();
        this.showWelcomeMessage();
    }

    showWelcomeMessage() {
        const header = document.querySelector('header');
        if (header) {
            header.style.transform = 'translateY(-20px)';
            header.style.opacity = '0';
            
            setTimeout(() => {
                header.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
                header.style.transform = 'translateY(0)';
                header.style.opacity = '1';
            }, 100);
        }
    }

    async loadRecipes() {
        try {
            console.log('📡 Fetching recipes from API...');
            const response = await fetch('/api/recipe/weekly-suggestions?fresh=true&timestamp=' + Date.now(), {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('✅ API Response:', data);
            
            if (data.success && data.suggestions && data.suggestions.length > 0) {
                this.allRecipes = data.suggestions;
                this.renderRecipes();
                this.showNotification(`🎉 Loaded ${this.allRecipes.length} fresh recipes!`, 'success');
            } else {
                throw new Error(data.error || 'No recipes returned from server');
            }
        } catch (error) {
            console.error('❌ Error loading recipes:', error);
            this.handleLoadError(error);
        }
    }

    handleLoadError(error) {
        if (this.apiRetryCount < this.maxRetries) {
            this.apiRetryCount++;
            console.log(`🔄 Retrying API call (${this.apiRetryCount}/${this.maxRetries})...`);
            setTimeout(() => this.loadRecipes(), 2000 * this.apiRetryCount);
            return;
        }

        // Show fallback recipes if API fails
        this.showFallbackRecipes();
        this.showError('🍽️ We had trouble connecting to our recipe service. Showing sample recipes instead. Please refresh to try again.');
    }

    showFallbackRecipes() {
        // Fallback recipes in case API fails
        this.allRecipes = [
            {
                id: "fallback_001",
                name: "Mediterranean Grilled Chicken",
                protein: "chicken",
                vegetables: ["zucchini", "bell peppers"],
                starch_grain: "quinoa",
                prep_time: "35 minutes",
                difficulty: "easy",
                cuisine: "mediterranean",
                cooking_method: "grill",
                ingredients: ["chicken", "zucchini", "bell peppers", "quinoa"],
                is_favorite: true
            },
            {
                id: "fallback_002",
                name: "Asian Beef Stir-Fry",
                protein: "beef",
                vegetables: ["broccoli", "carrots"],
                starch_grain: "rice",
                prep_time: "25 minutes",
                difficulty: "medium",
                cuisine: "asian",
                cooking_method: "stove",
                ingredients: ["beef", "broccoli", "carrots", "rice"],
                is_favorite: false
            },
            {
                id: "fallback_003",
                name: "Pan-Seared Salmon",
                protein: "salmon",
                vegetables: ["asparagus", "tomatoes"],
                starch_grain: "quinoa",
                prep_time: "30 minutes",
                difficulty: "medium",
                cuisine: "american",
                cooking_method: "stove",
                ingredients: ["salmon", "asparagus", "tomatoes", "quinoa"],
                is_favorite: true
            },
            {
                id: "fallback_004",
                name: "Cajun Shrimp Skewers",
                protein: "shrimp",
                vegetables: ["bell peppers", "onions"],
                starch_grain: "rice",
                prep_time: "25 minutes",
                difficulty: "easy",
                cuisine: "american",
                cooking_method: "grill",
                ingredients: ["shrimp", "bell peppers", "onions", "rice"],
                is_favorite: false
            }
        ];
        this.renderRecipes();
    }

    async generateFreshRecipes() {
        const button = document.getElementById('generateRecipesBtn');
        if (!button) {
            console.error('❌ Generate button not found!');
            return;
        }

        const originalText = button.innerHTML;
        
        // Disable button and show loading state
        button.disabled = true;
        button.innerHTML = '🔄 Generating Fresh Recipes...';
        
        this.showLoading('🌐 Searching for fresh gluten-free recipes...');
        
        try {
            console.log('🔄 Generating fresh recipes...');
            
            // Force fresh recipe generation
            const response = await fetch(`/api/recipe/weekly-suggestions?include_web=true&fresh=true&timestamp=${Date.now()}`, {
                method: 'GET',
                headers: { 
                    'Content-Type': 'application/json',
                    'Cache-Control': 'no-cache'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('✅ Fresh recipes response:', data);
            
            if (data.success && data.suggestions && data.suggestions.length > 0) {
                this.allRecipes = data.suggestions;
                this.renderRecipes();
                this.updateUI();
                
                const totalCount = this.allRecipes.length;
                this.showNotification(
                    `🎉 Generated ${totalCount} fresh recipes! Ready for meal planning!`, 
                    'success'
                );
                
                // Scroll to recipes section
                const recipesSection = document.querySelector('.recipes-section');
                if (recipesSection) {
                    recipesSection.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start' 
                    });
                }
            } else {
                throw new Error(data.error || 'No recipes returned from server');
            }
        } catch (error) {
            console.error('❌ Error generating fresh recipes:', error);
            this.showError('🍽️ Unable to generate fresh recipes. Please try again in a moment.');
        } finally {
            // Re-enable button
            button.disabled = false;
            button.innerHTML = originalText;
            this.hideLoading();
        }
    }

    renderRecipes(recipesToRender = null) {
        const recipesGrid = document.getElementById('recipesGrid');
        if (!recipesGrid) {
            console.error('❌ Recipes grid not found!');
            return;
        }

        const recipes = recipesToRender || this.allRecipes;
        
        if (recipes.length === 0) {
            recipesGrid.innerHTML = `
                <div class="no-recipes">
                    <p>🍽️ No recipes available. Click "Generate Fresh Recipes" to get started!</p>
                </div>
            `;
            return;
        }

        recipesGrid.innerHTML = recipes.map(recipe => {
            const isSelected = this.selectedRecipes.some(r => r.id === recipe.id);
            const favoriteIcon = recipe.is_favorite ? '⭐' : '';
            
            return `
                <div class="recipe-card ${isSelected ? 'selected' : ''}" data-recipe-id="${recipe.id}">
                    <div class="recipe-header">
                        <h3>${recipe.name} ${favoriteIcon}</h3>
                        <div class="recipe-meta">
                            <span class="protein">${this.getProteinEmoji(recipe.protein)} ${recipe.protein}</span>
                            <span class="time">⏱️ ${recipe.prep_time}</span>
                            <span class="difficulty">${this.getDifficultyDisplay(recipe.difficulty)}</span>
                        </div>
                    </div>
                    <div class="recipe-details">
                        <div class="cuisine">${this.getCuisineEmoji(recipe.cuisine)} ${recipe.cuisine}</div>
                        <div class="method">${this.getMethodEmoji(recipe.cooking_method)} ${recipe.cooking_method}</div>
                        <div class="vegetables">🥬 ${recipe.vegetables.join(', ')}</div>
                        <div class="starch">🌾 ${recipe.starch_grain}</div>
                    </div>
                    <button class="select-btn ${isSelected ? 'selected' : ''}" onclick="recipeSelector.toggleRecipe('${recipe.id}')">
                        ${isSelected ? '✅ Selected' : '➕ Select Recipe'}
                    </button>
                </div>
            `;
        }).join('');
    }

    getProteinEmoji(protein) {
        const emojis = {
            'chicken': '🐔',
            'beef': '🥩',
            'fish': '🐟',
            'salmon': '🍣',
            'shrimp': '🦐',
            'turkey': '🦃',
            'pork': '🐷',
            'lamb': '🐑',
            'duck': '🦆'
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

    toggleRecipe(recipeId) {
        const recipe = this.allRecipes.find(r => r.id === recipeId);
        if (!recipe) {
            console.error('❌ Recipe not found:', recipeId);
            return;
        }

        const existingIndex = this.selectedRecipes.findIndex(r => r.id === recipeId);
        
        if (existingIndex >= 0) {
            this.selectedRecipes.splice(existingIndex, 1);
            this.showNotification(`🗑️ Removed "${recipe.name}" from your menu`, 'info');
        } else if (this.selectedRecipes.length < this.maxSelections) {
            this.selectedRecipes.push(recipe);
            this.showNotification(`✅ Added "${recipe.name}" to your menu!`, 'success');
        } else {
            this.showNotification(`⚠️ You can only select ${this.maxSelections} recipes`, 'warning');
            return;
        }

        this.updateUI();
        this.renderRecipes(); // Re-render to update selection state
    }

    updateUI() {
        this.updateProgressBar();
        this.updateSelectedRecipes();
        this.updateGroceryButton();
    }

    updateProgressBar() {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        if (progressFill && progressText) {
            const percentage = (this.selectedRecipes.length / this.maxSelections) * 100;
            progressFill.style.width = `${percentage}%`;
            progressText.textContent = `Select 4 delicious recipes for your week (${this.selectedRecipes.length}/4 selected)`;
        }
    }

    updateSelectedRecipes() {
        const selectedContainer = document.getElementById('selectedRecipes');
        if (!selectedContainer) return;

        if (this.selectedRecipes.length === 0) {
            selectedContainer.innerHTML = `
                <div class="empty-selection">
                    <p>Start building your delicious week by selecting recipes from the collection!</p>
                </div>
            `;
        } else {
            selectedContainer.innerHTML = this.selectedRecipes.map((recipe, index) => `
                <div class="selected-recipe">
                    <div class="recipe-number">${index + 1}</div>
                    <div class="recipe-info">
                        <h4>${recipe.name}</h4>
                        <p>${recipe.prep_time} • ${recipe.cuisine}</p>
                    </div>
                    <button class="remove-btn" onclick="recipeSelector.toggleRecipe('${recipe.id}')">❌</button>
                </div>
            `).join('');
        }
    }

    updateGroceryButton() {
        const groceryBtn = document.getElementById('generateGroceryBtn');
        if (groceryBtn) {
            groceryBtn.disabled = this.selectedRecipes.length !== 4;
        }
    }

    async generateGroceryList() {
        if (this.selectedRecipes.length !== 4) {
            this.showNotification('⚠️ Please select exactly 4 recipes first', 'warning');
            return;
        }

        this.showLoading('🛒 Generating your smart grocery list...');

        try {
            console.log('🛒 Generating grocery list for:', this.selectedRecipes);
            
            const response = await fetch('/api/recipe/grocery-list', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    selected_recipes: this.selectedRecipes,
                    recipe_ids: this.selectedRecipes.map(r => r.id)
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('✅ Grocery list response:', data);

            if (data.success) {
                this.displayGroceryList(data.formatted_list || data.raw_data);
                this.showNotification('🛒 Grocery list generated successfully!', 'success');
            } else {
                throw new Error(data.error || 'Failed to generate grocery list');
            }
        } catch (error) {
            console.error('❌ Error generating grocery list:', error);
            this.showError('🛒 Unable to generate grocery list. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    displayGroceryList(groceryData) {
        const modal = document.getElementById('groceryModal');
        const content = document.getElementById('groceryListContent');
        
        if (!modal || !content) {
            console.error('❌ Grocery modal elements not found!');
            return;
        }

        const groceryList = groceryData.grocery_list || groceryData;
        
        content.innerHTML = Object.entries(groceryList).map(([department, items]) => `
            <div class="grocery-department">
                <h3>${department}</h3>
                <ul>
                    ${items.map(item => `<li>• ${item}</li>`).join('')}
                </ul>
            </div>
        `).join('');

        modal.style.display = 'block';
    }

    setupEventListeners() {
        console.log('🔧 Setting up event listeners...');
        
        // Generate fresh recipes button
        const generateBtn = document.getElementById('generateRecipesBtn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => this.generateFreshRecipes());
            console.log('✅ Generate button listener added');
        } else {
            console.error('❌ Generate button not found!');
        }

        // Grocery list generation
        const groceryBtn = document.getElementById('generateGroceryBtn');
        if (groceryBtn) {
            groceryBtn.addEventListener('click', () => this.generateGroceryList());
        }

        // Modal controls
        const closeModal = document.getElementById('closeModal');
        if (closeModal) {
            closeModal.addEventListener('click', () => {
                document.getElementById('groceryModal').style.display = 'none';
            });
        }

        const downloadBtn = document.getElementById('downloadBtn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => this.downloadGroceryList());
        }

        // Close modal when clicking outside
        const modal = document.getElementById('groceryModal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target.id === 'groceryModal') {
                    modal.style.display = 'none';
                }
            });
        }
    }

    showLoading(message) {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.querySelector('p').textContent = message;
            overlay.style.display = 'flex';
        }
    }

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = 'none';
        }
    }

    showNotification(message, type = 'info') {
        console.log(`📢 ${type.toUpperCase()}: ${message}`);
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            transform: translateX(400px);
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            max-width: 350px;
            font-family: 'Inter', sans-serif;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : type === 'warning' ? '#f59e0b' : '#3b82f6'};
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

    downloadGroceryList() {
        // Simple download functionality
        this.showNotification('📥 Download feature coming soon!', 'info');
    }
}

// Initialize the application when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('🚀 DOM loaded, initializing Recipe Selector...');
        window.recipeSelector = new RecipeSelector();
    });
} else {
    console.log('🚀 DOM already loaded, initializing Recipe Selector...');
    window.recipeSelector = new RecipeSelector();
}

