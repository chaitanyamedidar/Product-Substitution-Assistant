class RuleExplainer:
    
    def generate_explanation(self, alternative, requested_product, preferred_brand=None):
        # Generate human-readable explanation based on predefined rules
        product = alternative['product']
        source = alternative['source']
        explanation_parts = []
        
        # Rule: Category relationship
        if source == 'same_category':
            if product['brand'] == requested_product['brand']:
                explanation_parts.append("✓ Same category, same brand")
            else:
                explanation_parts.append("✓ Same category, different brand")
        elif source == 'similar_category':
            if product['brand'] == requested_product['brand']:
                explanation_parts.append("✓ Similar category, same brand")
            else:
                explanation_parts.append("✓ Similar category, different brand")
        elif source == 'sibling_category':
            explanation_parts.append("✓ Related category")
        
        # Rule: Attribute matching
        requested_attrs = set(requested_product['attributes'])
        product_attrs = set(product['attributes'])
        common_attrs = requested_attrs.intersection(product_attrs)
        
        if common_attrs == requested_attrs and len(requested_attrs) > 0:
            explanation_parts.append("✓ Matches all original attributes")
        
        # Rule: Price comparison
        if product['price'] < requested_product['price']:
            savings = requested_product['price'] - product['price']
            explanation_parts.append(f"✓ Cheaper option (₹{savings} less)")
        elif product['price'] > requested_product['price']:
            extra = product['price'] - requested_product['price']
            explanation_parts.append(f"✓ Premium alternative (₹{extra} more)")
        else:
            explanation_parts.append("✓ Same price point")
        
        # Rule: Brand preference
        if preferred_brand and product['brand'] == preferred_brand:
            explanation_parts.append("✓ Matches your preferred brand")
        
        # Rule: Special attributes
        special_attrs = product_attrs - requested_attrs
        if 'lactose_free' in special_attrs:
            explanation_parts.append("✓ Lactose-free option")
        if 'sugar_free' in special_attrs:
            explanation_parts.append("✓ Sugar-free option")
        if 'gluten_free' in special_attrs:
            explanation_parts.append("✓ Gluten-free option")
        if 'organic' in special_attrs:
            explanation_parts.append("✓ Organic option")
        
        return " | ".join(explanation_parts)
    
    def get_rule_tags(self, alternative, requested_product, preferred_brand=None):
        # Return machine-readable rule tags for transparency
        product = alternative['product']
        source = alternative['source']
        tags = []
        
        if source == 'same_category':
            if product['brand'] == requested_product['brand']:
                tags.append('same_category_same_brand')
            else:
                tags.append('same_category_diff_brand')
        elif source == 'similar_category':
            if product['brand'] == requested_product['brand']:
                tags.append('similar_category_same_brand')
            else:
                tags.append('similar_category_diff_brand')
        
        requested_attrs = set(requested_product['attributes'])
        product_attrs = set(product['attributes'])
        if requested_attrs.issubset(product_attrs):
            tags.append('all_required_tags_matched')
        
        if product['price'] < requested_product['price']:
            tags.append('cheaper_option')
        elif product['price'] > requested_product['price']:
            tags.append('premium_alternative')
        else:
            tags.append('same_price')
        
        if preferred_brand and product['brand'] == preferred_brand:
            tags.append('preferred_brand_match')
        
        return tags
