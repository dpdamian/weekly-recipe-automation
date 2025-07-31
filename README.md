# 🍽️ Weekly Recipe Automation System

An intelligent meal planning system that automatically generates 15+ gluten-free dinner recipe suggestions every week, helps you select 4 recipes, and creates organized grocery lists to streamline your shopping experience.

![Recipe Selection Interface](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Flask](https://img.shields.io/badge/Flask-3.1+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 🤖 **On-Demand Recipe Generation**
- **15+ Recipe Suggestions** generated instantly with one click
- **Fresh Web Recipes** - Searches top cooking websites for new ideas
- **Gluten-Free Guarantee** - All recipes are verified gluten-free
- **Protein Variety** - Never more than 2 of the same protein per week
- **Smart Learning** - Adapts to your preferences over time

### 🎯 **Intelligent Recipe Selection**
- **Interactive Web Interface** - Beautiful, responsive design
- **Real-time Filtering** - By protein, cuisine, cooking method
- **Ingredient Optimization** - Suggests recipes with overlapping ingredients
- **Equipment Integration** - Recipes for grill, stove, oven, air fryer, Instant Pot

### 🛒 **Smart Grocery Lists**
- **Department Organization** - Items sorted by store section
- **Cost Estimation** - Budget planning for grocery shopping
- **Shopping Tips** - Money-saving and efficiency recommendations
- **Equipment Reminders** - What cooking tools you'll need

### 📱 **User Experience**
- **Mobile Responsive** - Works perfectly on all devices
- **One-Click Selection** - Easy recipe choosing interface
- **Downloadable Lists** - Take grocery lists shopping
- **Progress Tracking** - Visual selection progress

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dpdamian/weekly-recipe-automation.git
   cd weekly-recipe-automation
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python src/main.py
   ```

4. **Access the web interface**
   - Open your browser to `http://localhost:5000`
   - Start selecting your weekly recipes!

### Quick Demo
```bash
cd backend
python demo_test.py
```

## 📁 Project Structure

```
weekly-recipe-automation/
├── README.md                 # This file
├── backend/                  # Flask backend application
│   ├── src/                  # Source code
│   │   ├── main.py          # Flask application entry point
│   │   ├── routes/          # API endpoints
│   │   ├── models/          # Database models
│   │   └── static/          # Frontend files (HTML, CSS, JS)
│   ├── recipe_manager.py    # Core recipe management
│   ├── weekly_suggestion_generator.py  # Weekly automation
│   ├── integrated_grocery_system.py    # Grocery list generation
│   ├── requirements.txt     # Python dependencies
│   └── *.json              # Recipe and ingredient databases
├── docs/                    # Documentation
│   ├── USER_GUIDE.md       # Comprehensive user manual
│   ├── SYSTEM_SUMMARY.md   # Technical overview
│   └── recipe_system_requirements.md  # System specifications
└── frontend/               # Future frontend separation (if needed)
```

## 🎯 How It Works

### Weekly Workflow
1. **Sunday 9:00 AM**: System automatically generates 15+ recipe suggestions
2. **Recipe Selection**: Use web interface to select 4 recipes for the week
3. **Grocery List**: Generate organized shopping list by store department
4. **Shopping**: Use the optimized list for efficient grocery shopping
5. **Cooking**: Prepare your selected recipes throughout the week
6. **Rating**: Rate recipes to improve future suggestions

### Smart Features
- **Variety Enforcement**: Automatic protein and cuisine diversity
- **Preference Learning**: Improves suggestions based on your ratings
- **Ingredient Optimization**: Maximizes shopping efficiency
- **Equipment Matching**: Recipes suited to your available cooking tools

## 🔧 Configuration

### Cooking Equipment
The system supports recipes for:
- **Stove** - Traditional stovetop cooking
- **Oven** - Baking and roasting
- **Grill** - Outdoor grilling
- **Air Fryer** - Quick, crispy cooking
- **Instant Pot** - Pressure and slow cooking

### Dietary Requirements
- **100% Gluten-Free** - All recipes are verified gluten-free
- **Complete Meals** - Every recipe includes protein, vegetables, and starch
- **Balanced Nutrition** - Variety across food groups

## 📊 System Capabilities

### Recipe Database
- **50+ Curated Recipes** from trusted sources
- **Continuous Learning** from user preferences
- **Quality Assurance** - All recipes tested and verified

### Automation Features
- **Weekly Scheduling** - Runs every Sunday automatically
- **Preference Tracking** - Learns from your selections
- **Variety Algorithms** - Ensures diverse meal planning

### Web Interface
- **Responsive Design** - Works on desktop, tablet, mobile
- **Real-time Updates** - Live ingredient overlap analysis
- **Interactive Selection** - Easy recipe choosing
- **Progress Tracking** - Visual selection indicators

## 🛠️ API Endpoints

### Recipe Management
- `GET /api/recipe/weekly-suggestions` - Get weekly recipe suggestions
- `POST /api/recipe/update-suggestions` - Update suggestions after selection
- `POST /api/recipe/ingredient-overlap` - Calculate ingredient overlap
- `POST /api/recipe/grocery-list` - Generate grocery list
- `GET /api/recipe/recipe/<id>` - Get specific recipe details

### User Preferences
- `GET /api/recipe/user-preferences` - Get user preferences
- `POST /api/recipe/rate-recipe` - Rate a recipe
- `GET /api/recipe/cooking-equipment` - Get available equipment

## 🧪 Testing

### Run System Tests
```bash
cd backend
python demo_test.py
```

### Expected Output
- ✅ 15+ recipe suggestions generated
- ✅ 7+ different protein types
- ✅ 5+ different cuisine types
- ✅ Grocery list generation
- ✅ Web interface functionality

## 📚 Documentation

- **[User Guide](docs/USER_GUIDE.md)** - Complete user manual
- **[System Summary](docs/SYSTEM_SUMMARY.md)** - Technical overview
- **[Requirements](docs/recipe_system_requirements.md)** - System specifications

## 🚀 Deployment Options

### Local Development
```bash
python src/main.py
```

### Production Deployment
1. **Cloud Platforms**: Deploy to Heroku, AWS, Google Cloud
2. **VPS Hosting**: Deploy to any Linux server
3. **Docker**: Containerized deployment (Dockerfile included)

### Environment Variables
```bash
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Success Metrics

The system is designed to achieve:
- **95%+ User Satisfaction** with recipe suggestions
- **30%+ Reduction** in meal planning time
- **20%+ Savings** on grocery costs through optimization
- **100% Gluten-Free** compliance
- **Zero Repetition** of recipes within 4 weeks

## 📞 Support

### Getting Help
- **Issues**: Open a GitHub issue for bugs or feature requests
- **Documentation**: Check the comprehensive user guide
- **Demo**: Run `python demo_test.py` to verify functionality

### System Requirements
- **Python**: 3.11 or higher
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB for application and databases
- **Network**: Internet connection for recipe suggestions

## 🌟 Acknowledgments

- Built with Flask and modern web technologies
- Responsive design for all devices
- Automated scheduling for weekly convenience
- Smart algorithms for meal planning optimization

---

**Transform your meal planning experience with intelligent automation!** 🍽️✨

*Created with ❤️ for efficient, healthy, and stress-free meal planning*

