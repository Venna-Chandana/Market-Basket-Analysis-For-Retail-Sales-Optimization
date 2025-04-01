# 🛒 Market Basket Analysis using Streamlit

## 📌 Overview
Market Basket Analysis (MBA) is a data mining technique used to uncover relationships between items purchased together in transactions. This project implements an MBA system using the **Apriori Algorithm** and **Association Rule Mining** to analyze transaction data and provide product recommendations.

The application is built using **Streamlit** and deployed on **Streamlit Cloud**, allowing users to upload transaction datasets and explore insights through interactive visualizations.

---

## ⚡ Features
✅ Upload CSV transaction dataset for analysis  
✅ Data preprocessing (handling missing values, encoding categorical data)  
✅ Implementation of **Apriori Algorithm** for frequent itemset mining  
✅ Generate **association rules** to discover relationships between products  
✅ Product recommendation system based on association rules  
✅ Interactive **visualizations**:
   - Sales Trends Over Time 📈
   - Top-Selling Products 🔥
   - Frequently Bought-Together Products 🔄
   - Cross-Selling Opportunities 💰
✅ User-friendly **Streamlit Web App** interface 🎨

---

## 🔧 Installation
To run this project locally, follow these steps:

### **1️⃣ Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/market-basket-analysis.git
cd market-basket-analysis
```

### **2️⃣ Create a virtual environment (Optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

### **3️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the Streamlit app**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501/` 🚀

---

## 🌐 Deployment (Streamlit Cloud)
To deploy this app on **Streamlit Cloud**, follow these steps:

1. Push your code to **GitHub**.
2. Go to **[Streamlit Cloud](https://share.streamlit.io/)** and log in.
3. Click **"New App"** → Select your GitHub repo.
4. Enter `app.py` as the main script and click **Deploy**.
5. Share the **public URL** of your app!

For a detailed guide, refer to [Streamlit Deployment Steps](https://docs.streamlit.io/streamlit-cloud/get-started).

---

## 📊 Data Requirements
Your dataset should be in **CSV format** with transaction records. Example:

| Transaction ID | Product 1 | Product 2 | Product 3 |
|---------------|-----------|-----------|-----------|
| 1001          | Bread     | Butter    | Jam       |
| 1002          | Milk      | Cereal    |           |
| 1003          | Bread     | Butter    |           |

---

## 📚 Technologies Used
- **Python** 🐍
- **Streamlit** (Web App Framework)
- **Pandas** (Data Manipulation)
- **Plotly & Seaborn** (Data Visualization)
- **mlxtend** (Apriori & Association Rules)

---

## 🤝 Contribution
Want to improve this project? Contributions are welcome!

### **Steps to contribute:**
1. **Fork** this repository
2. Create a **new branch** (`feature-branch`)
3. **Commit** your changes (`git commit -m "Added new feature"`)
4. **Push** to GitHub (`git push origin feature-branch`)
5. Submit a **Pull Request** 🚀

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 📞 Contact
For any queries or feedback, feel free to reach out:
📧 Email: vennachandana1@gmail.com   
💼 LinkedIn: [Venna Chandana](https://linkedin.com/in/venna-chandana-007baa278/)

