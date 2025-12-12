# Technical Design Document

## Knowledge Graph Modeling

### Design Rationale

The Knowledge Graph is designed to capture product relationships in a way that enables intuitive similarity reasoning without machine learning.

#### Why Graph-Based?

1. **Natural Relationships**: Products naturally form hierarchies (categories) and associations (similar items)
2. **Explainable Traversal**: Graph paths directly translate to explanations ("same category", "similar category")
3. **Efficient Queries**: Graph structure allows fast neighbor lookups
4. **Extensible**: Easy to add new relationship types (e.g., "COMPLEMENTARY_TO" for product bundles)

### Node Design

#### Product Nodes
```python
{
    "id": str,           # Unique identifier
    "name": str,         # Display name
    "category": str,     # Category membership
    "brand": str,        # Brand name
    "price": float,      # Price in rupees
    "in_stock": bool,    # Availability status
    "attributes": list   # Tags like ['veg_only', 'lactose_free']
}
```

**Design Choice**: Store category and brand as strings (not IDs) for simplicity. In a production system, these would be normalized with separate Brand/Category nodes.

#### Category Hierarchy
```python
{
    "parent_category": ["child1", "child2", ...]
}
```

**Design Choice**: Two-level hierarchy (parent → children) is sufficient for grocery products. Deeper hierarchies would require recursive traversal.

### Edge Design

#### IS_A (Product → Category)
- **Purpose**: Classify products
- **Implementation**: Implicit via `product.category` field
- **Query**: O(1) lookup via `products_by_category` index

#### HAS_ATTRIBUTE (Product → Attribute)
- **Purpose**: Filter by dietary/quality requirements
- **Implementation**: List field `product.attributes`
- **Query**: Set intersection for matching

#### SIMILAR_TO (Category ↔ Category)
- **Purpose**: Enable cross-category suggestions
- **Implementation**: List of category pairs
- **Example**: `["Milk", "Plant-Based Milk"]` allows lactose-free alternatives

**Design Choice**: Bidirectional similarity (if A similar to B, then B similar to A). Stored as unordered pairs to avoid duplication.

### Graph Representation

**Choice**: Adjacency list using Python dictionaries

**Alternatives Considered**:
1. ❌ **NetworkX library**: Overkill for simple graph, adds dependency
2. ❌ **Neo4j database**: Too heavy for 50 products, deployment complexity
3. ✅ **Custom dict-based**: Lightweight, fast, no external dependencies

**Implementation**:
```python
{
    "products": {id: product_dict},
    "products_by_category": {category: [product_ids]},
    "category_hierarchy": {parent: [children]},
    "similar_categories": [[cat1, cat2], ...]
}
```

## Search Algorithm

### Algorithm Choice: Modified BFS

**Why BFS?**
- Explores neighbors level-by-level (same category → similar → siblings)
- Guarantees finding closest matches first
- Simple to implement and understand

**Modifications**:
1. **Priority Levels**: Not pure BFS; we explore in priority order
2. **Early Termination**: Could stop after finding N candidates (not implemented for completeness)
3. **Scoring**: Rank results instead of returning first N found

### Search Flow

```
1. START: Requested Product
   ↓
2. EXPAND: Collect Candidates
   ├─ Same Category (Priority 1)
   ├─ Similar Categories (Priority 2)
   └─ Sibling Categories (Priority 3)
   ↓
3. FILTER: Apply Hard Constraints
   ├─ Must be in stock
   ├─ Must be ≤ max_price
   └─ Must have all required_tags
   ↓
4. SCORE: Rank by Weighted Factors
   ├─ Category closeness (40%)
   ├─ Brand match (25%)
   ├─ Attribute overlap (20%)
   └─ Price proximity (15%)
   ↓
5. RETURN: Top 3 Alternatives
```

### Scoring Function Design

#### Factor 1: Category Closeness (50%)
```python
if same_category: score += 50
elif similar_category: score += 35
elif sibling_category: score += 5
```

**Rationale**: Category is the strongest signal of substitutability. Same category products are most likely to satisfy the same need.

#### Factor 2: Brand Match (20%)
```python
if preferred_brand: score += 20
elif same_brand_as_requested: score += 15
```

**Rationale**: Brand loyalty is important. Customers often prefer familiar brands.

#### Factor 3: Attribute Overlap (20%)
```python
overlap_ratio = len(common_attrs) / len(requested_attrs)
score += overlap_ratio * 20
```

**Rationale**: Matching attributes (lactose-free, organic) ensures dietary/quality requirements are met.

#### Factor 4: Price Proximity (15%)
```python
price_diff = abs(product.price - requested.price)
normalized_diff = price_diff / requested.price
score += max(0, 15 - normalized_diff * 15)
```

**Rationale**: Price sensitivity varies, so it's weighted lower. Closer prices are preferred but not critical.

**Weight Justification**:
- Total = 100%
- Category (50%) dominates because it's the primary substitution criterion - ensures same/similar categories always rank above siblings
- Brand (20%) is secondary - reduced to prevent brand bonus from overriding category importance
- Attributes (20%) ensure dietary compliance
- Price (10%) is least critical (customers may accept price variance for availability)

### Complexity Analysis

**Time Complexity**: O(V + E)
- V = number of products
- E = number of category relationships
- BFS visits each node once
- For 50 products: ~50 operations (very fast)

**Space Complexity**: O(V)
- Candidate list: O(V) in worst case
- Visited set: O(V)
- For 50 products: negligible memory

**Scalability**:
- ✅ Works well for 50-500 products
- ⚠️ For 1000+ products, consider:
  - Indexing by multiple attributes
  - Caching frequent queries
  - Limiting BFS depth

## Constraint Handling

### Hard Constraints (Filters)

#### 1. Stock Availability
```python
if not product['in_stock']:
    continue  # Skip
```
**Type**: Boolean filter  
**Rationale**: Out-of-stock products cannot be suggested

#### 2. Price Limit
```python
if max_price and product['price'] > max_price:
    continue  # Skip
```
**Type**: Numeric threshold  
**Rationale**: Budget constraints are non-negotiable

#### 3. Required Attributes
```python
if not required_tags.issubset(product_tags):
    continue  # Skip
```
**Type**: Set inclusion  
**Rationale**: Dietary restrictions must be strictly enforced

### Soft Constraints (Scoring)

#### 1. Brand Preference
- Preferred brand gets bonus score
- Not a hard filter (allows other brands if preferred unavailable)

#### 2. Price Proximity
- Closer prices score higher
- Not a hard filter (allows price variance)

## Rule-Based Explanation System

### Design Philosophy

**Goal**: Every explanation must be **traceable to explicit rules**, not generated text.

### Rule Template System

Each rule has:
1. **Condition**: When the rule triggers
2. **Tag**: Machine-readable identifier
3. **Message**: Human-readable explanation

**Example**:
```python
Rule: same_category_same_brand
Condition: product.category == requested.category AND 
           product.brand == requested.brand
Tag: "same_category_same_brand"
Message: "✓ Same category, same brand"
```

### Rule Categories

#### Category Rules (5 rules)
- `same_category_same_brand`
- `same_category_diff_brand`
- `similar_category_same_brand`
- `similar_category_diff_brand`
- `sibling_category`

#### Attribute Rules (4 rules)
- `all_required_tags_matched`
- `lactose_free` (special attribute)
- `sugar_free` (special attribute)
- `gluten_free` (special attribute)

#### Price Rules (3 rules)
- `cheaper_option`
- `premium_alternative`
- `same_price`

#### Brand Rules (1 rule)
- `preferred_brand_match`

**Total**: 13 distinct rules

### Explanation Generation Process

```python
def generate_explanation(alternative, requested, preferred_brand):
    parts = []
    
    # Check each rule category
    parts.append(check_category_rules(...))
    parts.append(check_attribute_rules(...))
    parts.append(check_price_rules(...))
    parts.append(check_brand_rules(...))
    
    # Combine triggered rules
    return " | ".join(parts)
```

**Output Example**:
```
✓ Same category, different brand | 
✓ Matches all original attributes | 
✓ Cheaper option (₹2 less)
```

### Transparency

The system provides two levels of explanation:

1. **User-Facing**: Natural language ("Same category, different brand")
2. **Technical**: Rule tags (`same_category_diff_brand`)

This allows:
- Users to understand suggestions
- Developers to debug and verify logic
- Auditors to validate reasoning

## Edge Cases and Solutions

### Case 1: No Alternatives Found
**Scenario**: All products filtered out by constraints  
**Solution**: Show friendly message suggesting to relax filters

### Case 2: Requested Product Not Found
**Scenario**: Invalid product name  
**Solution**: Return error message (shouldn't happen with dropdown UI)

### Case 3: All Same-Category Products Out of Stock
**Scenario**: Need to expand to similar categories  
**Solution**: BFS automatically explores similar categories (Priority 2)

### Case 4: Price Limit Too Restrictive
**Scenario**: No products under max_price  
**Solution**: Return empty alternatives with suggestion to increase budget

### Case 5: Conflicting Attributes
**Scenario**: Required tags that no product has together  
**Solution**: Filter returns empty, user sees "no alternatives" message

### Case 6: Exact Product In Stock
**Scenario**: Requested product is available  
**Solution**: Return exact match immediately (no search needed)

## Performance Optimizations

### 1. Caching
```python
@st.cache_resource
def load_system():
    # Load KG only once
```
**Benefit**: Avoid reloading JSON on every interaction

### 2. Reverse Indexes
```python
products_by_category = {category: [product_ids]}
```
**Benefit**: O(1) category lookup instead of O(N) scan

### 3. Early Filtering
Filter candidates before scoring (cheaper operation first)

### 4. Limited Results
Return only top 3 (avoid sorting entire list)

## Future Enhancements

### 1. Additional Edge Types
- `COMPLEMENTARY_TO`: Suggest related products (chips → dip)
- `SUBSTITUTE_FOR`: Explicit substitution relationships

### 2. User Feedback Loop
- Track which suggestions users accept
- Adjust scoring weights based on feedback

### 3. Temporal Patterns
- Consider time-of-day, seasonal preferences
- "People who bought X also bought Y"

### 4. Multi-Attribute Scoring
- Weighted attribute importance (lactose_free > organic)
- User-specific attribute preferences

### 5. Explanation Customization
- Verbose vs. concise modes
- Language localization

## Testing Strategy

### Unit Tests (Recommended)
```python
def test_same_category_search():
    # Request out-of-stock milk
    # Expect other milk products
    
def test_price_filter():
    # Set max_price = 50
    # Expect no products > 50
    
def test_required_tags():
    # Require lactose_free
    # Expect only lactose_free products
```

### Integration Tests
- Full search flow with various inputs
- UI interaction testing

### Edge Case Tests
- Empty results
- Single result
- All filters active

## Deployment Considerations

### Streamlit Cloud
- **Pros**: Free, easy deployment, auto-updates from GitHub
- **Cons**: Limited resources, cold start delays

### Configuration
- No secrets needed (public data)
- No database required (JSON file)
- Minimal dependencies

### Monitoring
- Track search queries
- Monitor response times
- Log empty result cases

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Author**: Chaitanya Medidar
