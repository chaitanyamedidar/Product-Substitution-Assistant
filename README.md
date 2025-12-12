# 🛒 Shopkeeper Product Substitution Assistant

A Streamlit web application that suggests alternative products when requested items are out of stock, using **Knowledge Graph** reasoning and **classical AI** techniques (no ML/LLMs).

## 🌐 Live Demo

**Deployed App:** https://appuct-substitution-assistant-uedxypcm2cpexpqmlexyk9.streamlit.app/

## 📋 Table of Contents

- [Overview](#overview)
- [Knowledge Graph Design](#knowledge-graph-design)
- [Search Algorithm](#search-algorithm)
- [Rule-Based Explanations](#rule-based-explanations)
- [Local Setup](#local-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)

<a name="overview"></a>
## 🎯 Overview

This application helps shopkeepers suggest alternative products to customers when their requested item is unavailable. It uses:

- **Knowledge Graph**: Products, categories, brands, and attributes connected by relationships
- **Graph Traversal**: BFS-based search to find similar products
- **Rule-Based Reasoning**: Explicit rules for filtering, scoring, and explaining suggestions
- **No ML/AI Models**: Pure classical AI approach with transparent logic
<a name="Knowledge Graph Design"></a>
## 🧠 Knowledge Graph Design

### Node Types

1. **Products**: Individual items with properties
   - Properties: `id`, `name`, `category`, `brand`, `price`, `in_stock`, `attributes[]`
   - Example: `"Amul Milk (1L)"` with price ₹60, category "Milk"

2. **Categories**: Product classifications in a hierarchy
   - Example: `Dairy → Milk → Plant-Based Milk`

3. **Brands**: Manufacturer/brand names
   - Example: `Amul`, `Mother Dairy`, `Britannia`

4. **Attributes**: Product characteristics
   - Example: `lactose_free`, `sugar_free`, `veg_only`, `gluten_free`

### Edge Types

1. **IS_A**: Product → Category
   - Links products to their category
   - Example: `"Amul Milk"` IS_A `"Milk"`

2. **HAS_BRAND**: Product → Brand
   - Links products to their brand
   - Example: `"Amul Milk"` HAS_BRAND `"Amul"`

3. **HAS_ATTRIBUTE**: Product → Attribute
   - Links products to their characteristics
   - Example: `"Amul Lactose-Free Milk"` HAS_ATTRIBUTE `"lactose_free"`

4. **SIMILAR_TO**: Category ↔ Category
   - Defines category similarity relationships
   - Example: `"Milk"` SIMILAR_TO `"Plant-Based Milk"`

### Graph Representation

```
Products (50 items)
    ↓ IS_A
Categories (Hierarchical)
    - Dairy
        - Milk
        - Plant-Based Milk
        - Butter
        - Cheese
        - Curd
    - Beverages
        - Soft Drinks
        - Juice
        - Tea
        - Coffee
    - Snacks
        - Chips
        - Namkeen
        - Biscuits
    - Grains
        - Rice
        - Flour
        - Pulses
    - Condiments
        - Ketchup
        - Mayonnaise
        - Spices
        - Cooking Oil
```
<a name="overview"></a>
## 🔍 Search Algorithm

### Approach: Modified BFS with Scoring

The search algorithm follows these steps:

#### 1. **Graph Traversal** (BFS-based)

Starting from the requested product, explore the graph in order of priority:

```
Priority 1: Same Category Products
    ↓
Priority 2: Similar Category Products (via SIMILAR_TO edges)
    ↓
Priority 3: Sibling Category Products (same parent category)
```

**Pseudocode:**
```python
def find_alternatives(requested_product):
    candidates = []
    
    # Priority 1: Same category
    for product in same_category(requested_product.category):
        candidates.add(product, priority=1)
    
    # Priority 2: Similar categories
    for similar_cat in get_similar_categories(requested_product.category):
        for product in category(similar_cat):
            candidates.add(product, priority=2)
    
    # Priority 3: Sibling categories
    for sibling_cat in get_sibling_categories(requested_product.category):
        for product in category(sibling_cat):
            candidates.add(product, priority=3)
    
    return candidates
```

#### 2. **Filtering** (Hard Constraints)

Apply mandatory filters to remove invalid candidates:

- ✅ **In Stock**: Must be available
- ✅ **Price Limit**: Must be ≤ max_price (if specified)
- ✅ **Required Tags**: Must have ALL required attributes

#### 3. **Scoring** (Ranking)

Score each candidate using weighted factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Category Closeness** | 50% | Same (50pts) > Similar (35pts) > Sibling (5pts) |
| **Brand Match** | 20% | Preferred brand (20pts) or same brand (15pts) |
| **Attribute Overlap** | 20% | Percentage of matching attributes |
| **Price Proximity** | 10% | Closer to original price = higher score |

**Scoring Formula:**
```
score = (category_score × 0.5) + 
        (brand_score × 0.2) + 
        (attribute_score × 0.2) + 
        (price_score × 0.1)
```

#### 4. **Return Top 3**

Sort by score (descending) and return the top 3 alternatives.

### Complexity Analysis

- **Time Complexity**: O(V + E) where V = vertices, E = edges
  - BFS traversal visits each node once
  - Efficient for small-medium product catalogs (50-1000 products)

- **Space Complexity**: O(V)
  - Stores visited nodes and candidate list

## 📝 Rule-Based Explanations

Each suggestion includes a **transparent, rule-based explanation** derived from explicit conditions.

### Rule Categories

#### 1. Category Rules
- `same_category_same_brand`: "✓ Same category, same brand"
- `same_category_diff_brand`: "✓ Same category, different brand"
- `similar_category_same_brand`: "✓ Similar category, same brand"
- `similar_category_diff_brand`: "✓ Similar category, different brand"
- `sibling_category`: "✓ Related category"

#### 2. Attribute Rules
- `all_required_tags_matched`: "✓ Matches all original attributes"
- `lactose_free`: "✓ Lactose-free option"
- `sugar_free`: "✓ Sugar-free option"
- `gluten_free`: "✓ Gluten-free option"

#### 3. Price Rules
- `cheaper_option`: "✓ Cheaper option (₹X less)"
- `premium_alternative`: "✓ Premium alternative (₹X more)"
- `same_price`: "✓ Same price point"

#### 4. Brand Rules
- `preferred_brand_match`: "✓ Matches your preferred brand"

### Example Explanation

**Requested:** Mother Dairy Milk (1L) - Out of Stock  
**Suggested:** Amul Milk (1L)

**Explanation:**
```
✓ Same category, different brand | 
✓ Matches all original attributes | 
✓ Cheaper option (₹2 less)
```

**Rule Tags:** `same_category_diff_brand`, `all_required_tags_matched`, `cheaper_option`

## 🚀 Local Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Assignment
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in terminal

## 💡 Usage

### Step-by-Step Guide

1. **Select a Product**: Choose from the dropdown (50 products available)

2. **Set Filters** (Optional):
   - **Max Price**: Set maximum price limit (₹)
   - **Required Attributes**: Check boxes for dietary requirements
     - Veg Only
     - Lactose Free
     - Sugar Free
     - Gluten Free
   - **Preferred Brand**: Enter brand name for prioritization

3. **Click "Find Alternatives"**

4. **View Results**:
   - If **in stock**: Shows exact product details
   - If **out of stock**: Shows up to 3 alternatives with:
     - Product details (name, price, brand, category)
     - Attributes
     - Rule-based explanation
     - Technical rule tags

### Example Scenarios

**Scenario 1: Basic Search**
- Product: "Mother Dairy Milk (1L)" (out of stock)
- Result: Suggests "Amul Milk (1L)", "Amul Lactose-Free Milk (1L)"

**Scenario 2: With Price Constraint**
- Product: "Daawat Basmati Rice (1kg)" (out of stock)
- Max Price: ₹100
- Result: Suggests "Fortune Sona Masoori Rice (1kg)" (₹80)

**Scenario 3: With Dietary Requirements**
- Product: "Mother Dairy Milk (1L)" (out of stock)
- Required: Lactose Free
- Result: Suggests "Epigamia Almond Milk", "Goodmylk Soy Milk"

## 📁 Project Structure

```
Assignment/
│
├── app.py                  # Main Streamlit application
├── knowledge_graph.py      # KG data structure and queries
├── search_engine.py        # Graph traversal and scoring
├── rule_explainer.py       # Rule-based explanation generator
├── products.json           # Product database (50 items)
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── DESIGN.md              # Detailed technical design
```

## 🔧 Technical Details

### Dependencies

- **streamlit**: Web UI framework
- **pandas**: Data manipulation (minimal usage)

**No ML libraries** (no scikit-learn, tensorflow, transformers, etc.)

### Data Format

Products are stored in JSON format:

```json
{
  "id": "p1",
  "name": "Amul Milk (1L)",
  "category": "Milk",
  "brand": "Amul",
  "price": 60,
  "in_stock": true,
  "attributes": ["veg_only"]
}
```

### Key Design Decisions

1. **Graph Representation**: Adjacency list using Python dictionaries
   - Fast lookups: O(1) for product retrieval
   - Memory efficient for small-medium datasets

2. **Search Strategy**: BFS with priority levels
   - Ensures closest matches are found first
   - Prevents unnecessary exploration of distant categories

3. **Scoring System**: Weighted multi-factor scoring
   - Balances multiple criteria (category, brand, price, attributes)
   - Transparent and tunable weights

4. **Rule Engine**: Template-based explanations
   - Each rule has clear trigger conditions
   - No random or generated text

## 📊 Dataset

- **50 Products** across 6 major categories
- **Realistic Indian grocery items** (Amul, Britannia, Haldiram, etc.)
- **Multiple attributes** (veg_only, lactose_free, sugar_free, gluten_free)
- **Varied price range**: ₹10 - ₹250

## 🎓 Assignment Compliance

✅ Knowledge Graph implementation (not flat lists)  
✅ Graph-based search (BFS traversal)  
✅ Rule-based explanations (explicit rules)  
✅ Streamlit UI with all required inputs  
✅ Constraint handling (price, tags, stock, brand)  
✅ No ML/LLMs/embeddings used  
✅ Clean, commented, organized code  
✅ Comprehensive documentation  

## 📄 License

This project is created as an assignment submission.

## 👤 Author

Chaitanya Medidar

---

**Note**: This is a demonstration project using classical AI techniques for educational purposes.
