import streamlit as st
from knowledge_graph import KnowledgeGraph
from search_engine import SearchEngine
from rule_explainer import RuleExplainer


st.set_page_config(
    page_title="Product Substitution Assistant",
    page_icon="🛒",
    layout="wide"
)

# Load KG and search components (cached for performance)
@st.cache_resource
def load_system():
    kg = KnowledgeGraph('products.json')
    search = SearchEngine(kg)
    explainer = RuleExplainer()
    return kg, search, explainer


kg, search_engine, explainer = load_system()


# UI Layout
st.title("🛒 Shopkeeper Product Substitution Assistant")
st.markdown("Find alternative products when your requested item is out of stock")

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Product Search")
    
    product_name = st.selectbox(
        "Select Product",
        options=kg.get_all_product_names(),
        help="Choose the product you're looking for"
    )

with col2:
    st.subheader("Filters")
    
    max_price = st.number_input(
        "Max Price (₹)",
        min_value=0,
        max_value=1000,
        value=0,
        step=10,
        help="Set to 0 for no price limit"
    )
    
    if max_price == 0:
        max_price = None

# Required attributes
st.subheader("Required Attributes")
col3, col4, col5, col6 = st.columns(4)

with col3:
    veg_only = st.checkbox("Veg Only", value=False)
with col4:
    lactose_free = st.checkbox("Lactose Free", value=False)
with col5:
    sugar_free = st.checkbox("Sugar Free", value=False)
with col6:
    gluten_free = st.checkbox("Gluten Free", value=False)

required_tags = []
if veg_only:
    required_tags.append('veg_only')
if lactose_free:
    required_tags.append('lactose_free')
if sugar_free:
    required_tags.append('sugar_free')
if gluten_free:
    required_tags.append('gluten_free')

# Optional brand preference
preferred_brand = st.text_input(
    "Preferred Brand (optional)",
    placeholder="e.g., Amul, Britannia",
    help="If available, alternatives from this brand will be prioritized"
)

if not preferred_brand:
    preferred_brand = None

st.divider()

# Search execution
if st.button("🔍 Find Alternatives", type="primary", use_container_width=True):
    
    with st.spinner("Searching for alternatives..."):
        result = search_engine.find_alternatives(
            product_name=product_name,
            max_price=max_price,
            required_tags=required_tags if required_tags else None,
            preferred_brand=preferred_brand
        )
    
    st.divider()
    
    # Case 1: Product in stock
    if 'exact_match' in result:
        product = result['exact_match']
        st.success("✅ Product is available!")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Product", product['name'])
        with col_b:
            st.metric("Price", f"₹{product['price']}")
        with col_c:
            st.metric("Brand", product['brand'])
        
        if product['attributes']:
            st.write("**Attributes:**", ", ".join(product['attributes']))
    
    # Case 2: Product out of stock - show alternatives
    elif 'alternatives' in result:
        requested = result['requested_product']
        alternatives = result['alternatives']
        
        st.warning(f"⚠️ **{requested['name']}** is currently out of stock")
        st.write(f"Original Price: ₹{requested['price']} | Brand: {requested['brand']}")
        
        if alternatives:
            st.success(f"✨ Found {len(alternatives)} alternative(s):")
            st.divider()
            
            for idx, alt in enumerate(alternatives, 1):
                product = alt['product']
                
                with st.expander(f"**Option {idx}: {product['name']}**", expanded=(idx==1)):
                    
                    col_x, col_y, col_z = st.columns(3)
                    with col_x:
                        st.metric("Price", f"₹{product['price']}")
                    with col_y:
                        st.metric("Brand", product['brand'])
                    with col_z:
                        st.metric("Category", product['category'])
                    
                    if product['attributes']:
                        st.write("**Attributes:**", ", ".join(product['attributes']))
                    
                    # Generate rule-based explanation
                    explanation = explainer.generate_explanation(
                        alt, 
                        requested, 
                        preferred_brand
                    )
                    st.info(f"**Why this suggestion?**\n\n{explanation}")
                    
                    # Show technical rule tags
                    rule_tags = explainer.get_rule_tags(alt, requested, preferred_brand)
                    with st.expander("🔍 View Rule Tags (Technical)"):
                        st.code(", ".join(rule_tags))
        
        else:
            st.error("❌ No alternatives found matching your criteria")
            st.write("Try relaxing some filters (price limit or required attributes)")
    
    # Case 3: Error
    elif 'error' in result:
        st.error(f"❌ {result['error']}")


# Sidebar information
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This app uses **Knowledge Graph** reasoning to suggest product alternatives.
    
    **How it works:**
    1. Builds a graph of products, categories, and attributes
    2. Uses graph traversal (BFS-based) to find similar products
    3. Filters by your constraints (price, tags, stock)
    4. Ranks alternatives using a scoring algorithm
    5. Provides rule-based explanations
    
    
    """)
    
    st.divider()
    
    st.header("📊 System Stats")
    st.metric("Total Products", len(kg.products))
    st.metric("Categories", len(kg.category_hierarchy))
    st.metric("Similar Category Pairs", len(kg.similar_categories))
