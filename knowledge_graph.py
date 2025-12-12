import json


class KnowledgeGraph:
    
    def __init__(self, data_file='products.json'):
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        self.products = {p['id']: p for p in data['products']}
        self.category_hierarchy = data['category_hierarchy']
        self.similar_categories = data['similar_categories']
        
        self.products_by_category = {}
        for product_id, product in self.products.items():
            category = product['category']
            if category not in self.products_by_category:
                self.products_by_category[category] = []
            self.products_by_category[category].append(product_id)
    
    def get_product(self, product_id):
        return self.products.get(product_id)
    
    def get_product_by_name(self, name):
        for product in self.products.values():
            if product['name'].lower() == name.lower():
                return product
        return None
    
    def get_all_product_names(self):
        return sorted([p['name'] for p in self.products.values()])
    
    def get_products_in_category(self, category):
        return self.products_by_category.get(category, [])
    
    def get_similar_categories(self, category):
        similar = []
        for cat_pair in self.similar_categories:
            if category in cat_pair:
                similar.append(cat_pair[0] if cat_pair[1] == category else cat_pair[1])
        return similar
    
    def get_parent_category(self, category):
        for parent, children in self.category_hierarchy.items():
            if category in children:
                return parent
        return None
    
    def get_sibling_categories(self, category):
        parent = self.get_parent_category(category)
        if parent:
            siblings = self.category_hierarchy[parent]
            return [cat for cat in siblings if cat != category]
        return []
