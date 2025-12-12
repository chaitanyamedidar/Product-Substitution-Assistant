class SearchEngine:
    
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph
    
    def find_alternatives(self, product_name, max_price=None, required_tags=None, preferred_brand=None):
        requested_product = self.kg.get_product_by_name(product_name)
        if not requested_product:
            return {'error': 'Product not found'}
        
        # Return exact match if in stock
        if requested_product['in_stock']:
            return {'exact_match': requested_product}
        
        # Product out of stock - find alternatives via graph traversal
        category = requested_product['category']
        candidates = []
        
        # Priority 1: Same category products
        same_category_products = self.kg.get_products_in_category(category)
        for prod_id in same_category_products:
            product = self.kg.get_product(prod_id)
            if product['id'] != requested_product['id']:
                candidates.append({
                    'product': product,
                    'source': 'same_category',
                    'priority': 1
                })
        
        # Priority 2: Similar category products
        similar_categories = self.kg.get_similar_categories(category)
        for sim_cat in similar_categories:
            sim_products = self.kg.get_products_in_category(sim_cat)
            for prod_id in sim_products:
                product = self.kg.get_product(prod_id)
                candidates.append({
                    'product': product,
                    'source': 'similar_category',
                    'priority': 2
                })
        
        # Priority 3: Sibling category products
        sibling_categories = self.kg.get_sibling_categories(category)
        for sib_cat in sibling_categories:
            sib_products = self.kg.get_products_in_category(sib_cat)
            for prod_id in sib_products:
                product = self.kg.get_product(prod_id)
                candidates.append({
                    'product': product,
                    'source': 'sibling_category',
                    'priority': 3
                })
        
        # Filter by constraints and score
        filtered = self._filter_candidates(candidates, max_price, required_tags)
        scored = self._score_candidates(filtered, requested_product, preferred_brand)
        top_alternatives = scored[:3]
        
        return {
            'requested_product': requested_product,
            'alternatives': top_alternatives
        }
    
    def _filter_candidates(self, candidates, max_price, required_tags):
        # Apply hard constraints: stock, price, required attributes
        filtered = []
        
        for candidate in candidates:
            product = candidate['product']
            
            if not product['in_stock']:
                continue
            
            if max_price is not None and product['price'] > max_price:
                continue
            
            if required_tags:
                product_attrs = set(product['attributes'])
                required_attrs = set(required_tags)
                if not required_attrs.issubset(product_attrs):
                    continue
            
            filtered.append(candidate)
        
        return filtered
    
    def _score_candidates(self, candidates, requested_product, preferred_brand):
        # Score based on: category (50%), brand (20%), attributes (20%), price (10%)
        scored_candidates = []
        
        for candidate in candidates:
            product = candidate['product']
            score = 0
            
            # Category closeness (highest weight)
            if candidate['source'] == 'same_category':
                score += 50
            elif candidate['source'] == 'similar_category':
                score += 35
            elif candidate['source'] == 'sibling_category':
                score += 5
            
            # Brand match
            if preferred_brand and product['brand'] == preferred_brand:
                score += 20
            elif product['brand'] == requested_product['brand']:
                score += 15
            
            # Attribute overlap
            requested_attrs = set(requested_product['attributes'])
            product_attrs = set(product['attributes'])
            common_attrs = requested_attrs.intersection(product_attrs)
            if requested_attrs:
                attr_score = (len(common_attrs) / len(requested_attrs)) * 20
                score += attr_score
            
            # Price proximity
            price_diff = abs(product['price'] - requested_product['price'])
            max_diff = requested_product['price']
            if max_diff > 0:
                price_score = max(0, 15 - (price_diff / max_diff) * 15)
                score += price_score
            
            scored_candidates.append({
                'product': product,
                'score': score,
                'source': candidate['source']
            })
        
        scored_candidates.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_candidates
