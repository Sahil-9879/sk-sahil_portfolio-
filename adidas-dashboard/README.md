# 👟 Adidas Interactive Sales Analytics Dashboard

A professional, portfolio-ready **business intelligence dashboard** for analyzing Adidas sales performance. Built with **Python, Pandas, Plotly, and Streamlit**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-purple?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Screenshots

> *Add screenshots of the running dashboard here.*

---

## ✨ Features

### 📊 Overview Dashboard
- Real-time KPI cards (Revenue, Units Sold, Profit, Avg. Price, Transactions)
- Revenue trend over time (line chart)
- Revenue by region (bar chart)
- Sales by retailer (horizontal bar chart)
- Product category breakdown (donut chart)
- Operating profit trend
- Dynamic business insights

### 📈 Sales Analysis
- Metric selector (Revenue, Units, Profit, Price)
- Dynamic charts that respond to selected metric
- Region comparison, retailer performance, sales method analysis
- Monthly performance breakdown
- Normalized multi-metric comparison

### 👟 Product & Region Analysis
- Top products by revenue, profit, and units
- Price vs. units sold scatter plot
- Region performance comparison (revenue, profit, units)
- Regional drill-down: Region → State → City
- Interactive data exploration

### 🎛️ Global Features
- Sidebar filters (Date, Region, State, City, Product, Retailer, Sales Method)
- Reset filters button
- Expandable data tables
- Responsive dark-themed UI
- Error handling for missing columns/empty data

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core language |
| **Pandas** | Data processing & analysis |
| **NumPy** | Numerical operations |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Web dashboard framework |

---

## 📁 Dataset

The dashboard uses the **Adidas US Sales Dataset** with the following columns:

| Column | Description |
|--------|-------------|
| Retailer | Store name |
| Invoice Date | Sale date |
| Region | Geographic region |
| State | US state |
| City | City |
| Product | Product category |
| Price per Unit | Selling price |
| Units Sold | Quantity sold |
| Total Sales | Revenue |
| Operating Profit | Profit |
| Operating Margin | Profit margin |
| Sales Method | Sales channel |

---

## 🚀 Installation

```bash
# Clone the repository
git clone <repository-url>
cd adidas-dashboard

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Running

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

---

## 📂 Project Structure

```
adidas-dashboard/
├── app.py                  # Main Streamlit application
├── data/
│   └── adidas_sales.csv    # Sales dataset
├── src/
│   ├── __init__.py
│   ├── data_processing.py  # Data loading, cleaning, filtering
│   ├── charts.py           # Plotly chart creation functions
│   └── insights.py         # Dynamic business insights generator
├── assets/
│   └── logo/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔮 Future Improvements

- [ ] Export filtered data as CSV/Excel
- [ ] Add forecasting with time-series models
- [ ] Implement user authentication
- [ ] Add geographic map visualization
- [ ] Dark/Light theme toggle
- [ ] Comparison mode between time periods
- [ ] PDF report generation

---

## 📄 License

This project is for educational and portfolio purposes.
