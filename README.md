# 📈 Stock Time Series Dashboard

A real-time interactive dashboard built with **Dash** and **Plotly** for visualizing financial metrics, forecasts, and volume predictions for major tech stocks using **Prophet** and machine learning models.

## Demo

![demo](demo.gif)


## 🚀 Features

- 📊 **Interactive visualizations** for stock closing prices, volume, and returns.
- 🔮 **Time series forecasting** using Facebook Prophet.
- 🤖 **Volume prediction** using pre-trained machine learning models.
- 📉 **Performance comparison** against market index.
- 💼 **Fundamental metrics**: Revenue, EPS, Net Income, P/E, Dividend Yield, and more.
- ⚙️ **Live model retraining** triggered by the user.

## 🏗️ Components

- `update_button`: Triggers model retraining and dashboard data refresh.
- `ticker_dropdown`: Select stock ticker (AAPL, MSFT, GOOGL, etc).
- `get_header`: Displays selected stock info in the header.
- `get_forecast_plot`, `get_forecast_gauge`: Forecasted closing prices.
- `get_stock_plot`, `get_volume_plot`: Visualizes historical data.
- `plot_predicted_volume_gauge`: Predicts and shows today's expected volume.
- `plot_vs_index_gauge`: Compares stock returns vs market.
- `get_numbers_bar`: Displays key financial ratios in a bar format.

## 📂 Project Structure
```

├── main.py                     # Main Dash app
├── UI/
│   └── ui_components.py       # All reusable dashboard UI components
├── data/
│   └── data_handeler.py       # Data loading and processing functions
├── models/
│   └── models.py              # Volume and Prophet model training + inference
├── utils/
│   └── utils.py               # Financial metric calculations
└── README.md
```
## 🛠️ Setup Instructions

1. **Install Dependencies**

```bash
pip install dash dash-bootstrap-components pandas plotly prophet scikit-learn

```

2.	**Run the App**

```bash
python main.py
```

**Visit http://localhost:8080 in your browser.**

## 📌 Notes

- Initial models are trained on app start.
- Press “Update” to retrain models and refresh data.
- All plots and gauges dynamically update based on the selected ticker.

## 📈 Supported Tickers
- Apple (AAPL)
- Microsoft (MSFT)
- Google (GOOGL)
- Amazon (AMZN)
- Tesla (TSLA)
- Meta (META)




