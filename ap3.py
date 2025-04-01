import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Page Configuration
st.set_page_config(page_title="Market Basket Analysis", layout="wide")

# Custom Styles
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .stApp {
        background-color: #f7f7f9;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #ff5733;
        text-align: center;
    }
    .stButton>button {
        background-color: #ff5733;
        color: white;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>🛒 Market Basket Analysis</h1>", unsafe_allow_html=True)
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

    # Format Data into Transactions and Convert to Strings
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

    # Enhanced Visualization with Plotly - Sales Trend Over Time
    if "Date" in df.columns:
        st.write("### 📈 Sales Trend Over Time")
        sales_trend = df["Date"].value_counts().sort_index()
        fig = px.line(x=sales_trend.index, y=sales_trend.values, labels={'x': 'Date', 'y': 'Number of Transactions'},
                      title="🛍️ Sales Trend Over Time", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    # Enhanced Product Frequency Visualization with Plotly
    st.write("### 🔥 Most Frequently Purchased Products")
    all_products = pd.concat([df["Product 1"], df["Product 2"], df["Product 3"]])
    product_counts = all_products.value_counts().reset_index()
    product_counts.columns = ["Product", "Count"]

    fig = px.bar(product_counts, x="Count", y="Product", orientation='h',
                 title="📊 Most Frequent Products", template="plotly_dark", color="Count")
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
