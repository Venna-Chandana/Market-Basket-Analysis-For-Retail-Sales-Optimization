import streamlit as st
import pandas as pd
import plotly.express as px
import re
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Page Configuration with Tailwind CSS
st.set_page_config(page_title="Market Basket Analysis", layout="wide")
st.markdown(
    """
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .form-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .btn-primary {
            background-color: #3b82f6;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.375rem;
            width: 100%;
        }
        .btn-primary:hover {
            background-color: #2563eb;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize Session State
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "users" not in st.session_state:
    st.session_state["users"] = {}
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# Email validation regex
EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Login Page
def login():
    st.markdown("""
    <div class="form-container bg-white">
        <h2 class="text-2xl font-bold text-center mb-6 text-blue-600">🔐 Login</h2>
    """, unsafe_allow_html=True)
    
    email = st.text_input("📧 Email", placeholder="abc@gmail.com", key="login_email")
    password = st.text_input("🔑 Password", type="password", placeholder="********", key="login_password")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Login", key="login_btn"):
            if not email or not password:
                st.error("⚠️ Please fill in all fields")
            elif not re.match(EMAIL_REGEX, email):
                st.error("⚠️ Invalid email format! Use example@domain.com")
            elif email not in st.session_state["users"]:
                st.error("❌ You are not registered! Please register first.")
            elif st.session_state["users"][email] != password:
                st.error("❌ Incorrect password!")
            else:
                st.session_state["authenticated"] = True
                st.session_state["page"] = "analysis"
                st.success("✅ Login successful!")
    
    with col2:
        if st.button("Register", key="go_to_register"):
            st.session_state["page"] = "register"
    
    st.markdown("</div>", unsafe_allow_html=True)

# Registration Page
def register():
    st.markdown("""
    <div class="form-container bg-white">
        <h2 class="text-2xl font-bold text-center mb-6 text-blue-600">📝 Register</h2>
    """, unsafe_allow_html=True)
    
    email = st.text_input("📧 Email", placeholder="abc@gmail.com", key="reg_email")
    password = st.text_input("🔑 Password", type="password", placeholder="******** (min 8 chars)", key="reg_password")
    confirm_password = st.text_input("✅ Confirm Password", type="password", placeholder="********", key="reg_confirm_password")
    
    if st.button("Register", key="register_btn"):
        if not email or not password or not confirm_password:
            st.error("⚠️ Please fill in all fields")
        elif not re.match(EMAIL_REGEX, email):
            st.error("⚠️ Invalid email format! Use example@domain.com")
        elif len(password) < 8:
            st.error("⚠️ Password must be at least 8 characters")
        elif password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif email in st.session_state["users"]:
            st.warning("⚠️ Email already registered. Please login.")
        else:
            st.session_state["users"][email] = password
            st.success("✅ Registration successful! Please login.")
            st.session_state["page"] = "login"
    
    if st.button("Back to Login", key="go_to_login"):
        st.session_state["page"] = "login"
    
    st.markdown("</div>", unsafe_allow_html=True)

# Market Basket Analysis Page
def market_basket_analysis():
    st.markdown("<h1 class='text-3xl font-bold mb-6'>🛒 Market Basket Analysis</h1>", unsafe_allow_html=True)
    st.write("**Upload your dataset to analyze customer buying patterns and optimize sales.**")
    
    # File Upload
    uploaded_file = st.file_uploader("📂 Upload Your Transaction Dataset (CSV)", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.fillna("Unknown", inplace=True)
        
        # Convert Date to datetime if it exists
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df = df.dropna(subset=["Date"])
        
        st.write("### 📜 Dataset Preview:")
        st.write(df.head(50))
        
        # Format Data into Transactions
        transactions = df[['Product 1', 'Product 2', 'Product 3']].astype(str).values.tolist()
        te = TransactionEncoder()
        encoded_data = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(encoded_data, columns=te.columns_)
        
        # Apply Apriori Algorithm
        frequent_itemsets = apriori(df_encoded, min_support=0.05, use_colnames=True)
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
        
        # Display Association Rules
        st.write("### 🔗 Generated Association Rules:")
        st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
        
        # Product Recommendation System
        st.write("### 🎯 Product Recommendation System")
        selected_product = st.selectbox("🔍 Select a Product for Recommendations:", df_encoded.columns)
        
        def recommend_products(product):
            product = frozenset([product])
            filtered_rules = rules[rules["antecedents"].apply(lambda x: product.issubset(x))]
            return filtered_rules[['consequents', 'lift']].sort_values(by='lift', ascending=False)
        
        if selected_product:
            recommendations = recommend_products(selected_product)
            if recommendations.empty:
                st.write("⚠️ No strong associations found for this product.")
            else:
                st.write("### ✅ Recommended Products:")
                st.dataframe(recommendations)
        
        # Cross-Selling Strategy
        st.write("### 💰 Cross-Selling Strategy")
        if not recommendations.empty:
            top_product = recommendations.iloc[0]["consequents"]
            st.write(f"🎯 **Special Offer:** Buy **{selected_product}** & Get **{top_product}** at 10% Off! 🚀")
        
        # Sales Trend Over Time
        if "Date" in df.columns:
            st.write("### 📈 Sales Trend Over Time")
            sales_trend = df["Date"].value_counts().sort_index()
            fig = px.line(x=sales_trend.index, y=sales_trend.values, 
                          labels={'x': 'Date', 'y': 'Number of Transactions'},
                          title="🛍️ Sales Trend Over Time", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        # Product Frequency Visualization
        st.write("### 🔥 Most Frequently Purchased Products")
        all_products = pd.concat([df["Product 1"], df["Product 2"], df["Product 3"]])
        product_counts = all_products.value_counts().reset_index()
        product_counts.columns = ["Product", "Count"]
        
        fig = px.bar(product_counts, x="Count", y="Product", orientation='h',
                     title="📊 Most Frequent Products", template="plotly_dark", color="Count")
        st.plotly_chart(fig, use_container_width=True)

# Navigation Logic
if st.session_state["page"] == "login":
    login()
elif st.session_state["page"] == "register":
    register()
elif st.session_state["authenticated"]:
    market_basket_analysis()
else:
    st.session_state["page"] = "login"
    login()
