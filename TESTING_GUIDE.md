# Testing Guide - Product Substitution Assistant

## 🧪 Complete Test Cases with Examples

This guide provides specific examples to test every feature of the app.

---

## Test Case 1: **Exact Match (Product In Stock)**

### Example 1A: Basic In-Stock Product
- **Product**: `Amul Milk (1L)`
- **Expected Result**: ✅ Shows "Product is available!" with exact product details
- **What to verify**: 
  - Green success message
  - Product name, price (₹60), brand (Amul)
  - Attributes shown

### Example 1B: Another In-Stock Product
- **Product**: `Lays Classic (50g)`
- **Expected Result**: ✅ Shows exact match
- **Price**: ₹20

---

## Test Case 2: **Out of Stock - Basic Alternatives**

### Example 2A: Milk Category
- **Product**: `Mother Dairy Milk (1L)` ⚠️ OUT OF STOCK
- **Expected Result**: Shows 3 alternatives from same/similar categories
- **Expected Alternatives**:
  1. `Amul Milk (1L)` - Same category, different brand, ₹60
  2. `Amul Lactose-Free Milk (1L)` - Same category, same attributes, ₹75
  3. `Epigamia Almond Milk (1L)` or `Goodmylk Soy Milk (1L)` - Similar category (Plant-Based Milk)

### Example 2B: Soft Drinks
- **Product**: `Pepsi (1L)` ⚠️ OUT OF STOCK
- **Expected Result**: Shows Coca Cola products and other soft drinks
- **Expected Alternatives**:
  1. `Coca Cola (1L)` - Same category, ₹40
  2. `Sprite (1L)` - Same category, ₹40

### Example 2C: Instant Noodles
- **Product**: `Maggi Noodles (70g)` ⚠️ OUT OF STOCK
- **Expected Result**: Shows other noodle brands
- **Expected Alternatives**:
  1. `Yippee Noodles (70g)` - ₹12
  2. `Top Ramen (70g)` - ₹12

---

## Test Case 3: **Price Constraint**

### Example 3A: Strict Price Limit
- **Product**: `Daawat Basmati Rice (1kg)` ⚠️ OUT OF STOCK (Original: ₹160)
- **Max Price**: `100`
- **Expected Result**: Only shows cheaper alternatives
- **Expected Alternatives**:
  1. `Fortune Sona Masoori Rice (1kg)` - ₹80 ✓ Under budget
- **What to verify**: NO products above ₹100 should appear

### Example 3B: Very Low Price Limit
- **Product**: `Saffola Gold Oil (1L)` ⚠️ OUT OF STOCK (Original: ₹180)
- **Max Price**: `150`
- **Expected Result**: Shows only `Fortune Sunflower Oil (₹150)` and `Sundrop Oil (₹145)`
- **What to verify**: `Saffola Gold` alternatives within budget

### Example 3C: No Price Limit
- **Product**: `Mother Dairy Milk (1L)` ⚠️ OUT OF STOCK
- **Max Price**: `0` (or leave blank)
- **Expected Result**: Shows all alternatives regardless of price
- **What to verify**: May include expensive options like Almond Milk (₹150)

---

## Test Case 4: **Veg Only Attribute**

### Example 4A: All Products Are Veg
- **Product**: `Amul Milk (1L)` (any product)
- **Check**: ✅ Veg Only
- **Expected Result**: All products in our database are veg, so this won't filter anything
- **What to verify**: All results show `veg_only` in attributes

**Note**: All 50 products in our database are vegetarian, so this filter won't exclude anything. It's included for demonstration purposes.

---

## Test Case 5: **Lactose-Free Attribute**

### Example 5A: Lactose-Free Milk Alternatives
- **Product**: `Mother Dairy Milk (1L)` ⚠️ OUT OF STOCK
- **Check**: ✅ Lactose Free
- **Expected Result**: Only lactose-free options
- **Expected Alternatives**:
  1. `Amul Lactose-Free Milk (1L)` - ₹75
  2. `Epigamia Almond Milk (1L)` - ₹150
  3. `Goodmylk Soy Milk (1L)` - ₹120
- **What to verify**: 
  - NO regular milk products
  - All results have `lactose_free` in attributes
  - Explanations mention "Lactose-free option"

### Example 5B: Lactose-Free with Price Limit
- **Product**: `Mother Dairy Milk (1L)` ⚠️ OUT OF STOCK
- **Check**: ✅ Lactose Free
- **Max Price**: `100`
- **Expected Result**: May show NO alternatives (all lactose-free options are >₹100)
- **What to verify**: Error message "No alternatives found matching your criteria"

---

## Test Case 6: **Gluten-Free Attribute**

### Example 6A: Gluten-Free Rice
- **Product**: `Daawat Basmati Rice (1kg)` ⚠️ OUT OF STOCK
- **Check**: ✅ Gluten Free
- **Expected Result**: Shows other rice products (all rice is gluten-free)
- **Expected Alternatives**:
  1. `India Gate Basmati Rice (1kg)` - ₹150
  2. `Fortune Sona Masoori Rice (1kg)` - ₹80
- **What to verify**: All results have `gluten_free` in attributes

### Example 6B: Gluten-Free Pulses
- **Product**: Any rice product
- **Check**: ✅ Gluten Free
- **Expected Result**: May also show pulses (Toor Dal, Moong Dal) as they're gluten-free
- **What to verify**: Only gluten-free products appear

---

## Test Case 7: **Sugar-Free Attribute**

### Example 7A: Sugar-Free Juice
- **Product**: `Paper Boat Aam Panna (250ml)` ⚠️ OUT OF STOCK
- **Check**: ✅ Sugar Free
- **Expected Result**: May show NO alternatives (most juices have sugar)
- **What to verify**: 
  - Either shows sugar-free alternatives
  - Or shows "No alternatives found" message

**Note**: Only `Paper Boat Aam Panna` is marked sugar-free in our database, so this filter is very restrictive.

---

## Test Case 8: **Multiple Attributes Combined**

### Example 8A: Veg + Lactose-Free
- **Product**: `Mother Dairy Milk (1L)` ⚠️ OUT OF STOCK
- **Check**: ✅ Veg Only, ✅ Lactose Free
- **Expected Result**: Same as lactose-free only (all products are veg)
- **Expected Alternatives**: Plant-based milks and lactose-free milk

### Example 8B: Veg + Gluten-Free
- **Product**: `Daawat Basmati Rice (1kg)` ⚠️ OUT OF STOCK
- **Check**: ✅ Veg Only, ✅ Gluten Free
- **Expected Result**: Rice and pulses
- **What to verify**: All results have both `veg_only` AND `gluten_free`

---

## Test Case 9: **Brand Preference**

### Example 9A: Prefer Amul Brand
- **Product**: `Mother Dairy Milk (1L)` ⚠️ OUT OF STOCK
- **Preferred Brand**: `Amul`
- **Expected Result**: Amul products ranked higher
- **Expected Top Alternative**: `Amul Milk (1L)` should be #1
- **What to verify**: 
  - Explanation shows "✓ Matches your preferred brand" for Amul products
  - Amul products appear before other brands

### Example 9B: Prefer Coca Cola Brand
- **Product**: `Pepsi (1L)` ⚠️ OUT OF STOCK
- **Preferred Brand**: `Coca Cola`
- **Expected Result**: Coca Cola products ranked higher
- **Expected Top Alternative**: `Coca Cola (1L)` should be #1
- **What to verify**: Brand preference reflected in ranking

### Example 9C: Prefer Non-Existent Brand
- **Product**: `Amul Milk (1L)` (in stock)
- **Preferred Brand**: `RandomBrand123`
- **Expected Result**: Still shows exact match (brand preference doesn't affect in-stock items)

---

## Test Case 10: **Complex Filters (Multiple Constraints)**

### Example 10A: Price + Lactose-Free
- **Product**: `Mother Dairy Milk (1L)` ⚠️ OUT OF STOCK
- **Max Price**: `130`
- **Check**: ✅ Lactose Free
- **Expected Result**: Only `Goodmylk Soy Milk (₹120)` and `Amul Lactose-Free Milk (₹75)`
- **What to verify**: 
  - NO Epigamia Almond Milk (₹150 - too expensive)
  - All results are lactose-free AND under ₹130

### Example 10B: Price + Brand + Attribute
- **Product**: `Mother Dairy Milk (1L)` ⚠️ OUT OF STOCK
- **Max Price**: `80`
- **Preferred Brand**: `Amul`
- **Check**: ✅ Veg Only
- **Expected Result**: `Amul Milk (1L)` - ₹60
- **What to verify**: Meets all three constraints

### Example 10C: Impossible Constraints
- **Product**: `Amul Milk (1L)` (any product)
- **Max Price**: `10`
- **Check**: ✅ Lactose Free, ✅ Gluten Free, ✅ Sugar Free
- **Expected Result**: "No alternatives found matching your criteria"
- **What to verify**: Graceful handling of impossible constraints

---

## Test Case 11: **Explanation Verification**

### Example 11A: Same Category, Different Brand
- **Product**: `Mother Dairy Milk (1L)` ⚠️ OUT OF STOCK
- **Expected Explanation for Amul Milk**:
  - ✓ Same category, different brand
  - ✓ Matches all original attributes
  - ✓ Cheaper option (₹2 less)

### Example 11B: Similar Category
- **Product**: `Mother Dairy Milk (1L)` ⚠️ OUT OF STOCK
- **Expected Explanation for Almond Milk**:
  - ✓ Similar category, different brand
  - ✓ Lactose-free option
  - ✓ Premium alternative (₹90 more)

### Example 11C: Same Price Point
- **Product**: `Pepsi (1L)` ⚠️ OUT OF STOCK (₹40)
- **Expected Explanation for Coca Cola**:
  - ✓ Same category, different brand
  - ✓ Same price point

---

## Test Case 12: **Edge Cases**

### Example 12A: Product with Many Alternatives
- **Product**: `Oreo Cookies (120g)` ⚠️ OUT OF STOCK
- **Expected Result**: Shows 3 alternatives from Biscuits category
- **What to verify**: Exactly 3 alternatives (not more)

### Example 12B: Product with Few Alternatives
- **Product**: `Bru Instant Coffee (50g)` ⚠️ OUT OF STOCK
- **Expected Result**: Shows `Nescafe Classic Coffee (50g)`
- **What to verify**: May show fewer than 3 alternatives

### Example 12C: Cheapest Product Out of Stock
- **Product**: `Maggi Noodles (70g)` ⚠️ OUT OF STOCK (₹14)
- **Expected Result**: Shows cheaper alternatives (₹12)
- **What to verify**: Explanation shows "Cheaper option"

---

## 📊 Quick Reference Table

| Test Scenario | Product to Select | Filters to Apply | Expected Outcome |
|---------------|-------------------|------------------|------------------|
| **In Stock** | Amul Milk (1L) | None | Exact match shown |
| **Out of Stock** | Mother Dairy Milk (1L) | None | 3 alternatives |
| **Price Filter** | Daawat Basmati Rice (1kg) | Max Price: 100 | Only Fortune Sona Masoori |
| **Lactose-Free** | Mother Dairy Milk (1L) | ✅ Lactose Free | Plant-based milks only |
| **Gluten-Free** | Daawat Basmati Rice (1kg) | ✅ Gluten Free | Other rice products |
| **Brand Preference** | Pepsi (1L) | Preferred: Coca Cola | Coca Cola ranked #1 |
| **Complex Filter** | Mother Dairy Milk (1L) | Max: 130, ✅ Lactose Free | 2 alternatives under budget |
| **No Results** | Any product | Max Price: 10 | "No alternatives found" |

---

## 🎯 Recommended Testing Sequence

1. **Start Simple**: Test in-stock product (Amul Milk)
2. **Basic Out of Stock**: Test Mother Dairy Milk with no filters
3. **Add Price Filter**: Same product, max price 70
4. **Add Attribute**: Same product, add Lactose Free
5. **Brand Preference**: Test Pepsi with Coca Cola preference
6. **Complex Scenario**: Combine multiple filters
7. **Edge Case**: Test with impossible constraints

---

## ✅ What to Verify in Each Test

- [ ] Correct number of alternatives (0-3)
- [ ] All alternatives meet filter criteria
- [ ] Explanations are relevant and accurate
- [ ] Rule tags match the explanations
- [ ] Prices are within limits (if specified)
- [ ] Attributes are present (if required)
- [ ] Brand preference affects ranking
- [ ] UI shows appropriate messages (success/warning/error)

---

**Happy Testing!** 🚀

Use this guide to demonstrate all features of your app during the interview or presentation.
