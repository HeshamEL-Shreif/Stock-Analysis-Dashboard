from dash import  html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash
from dash import callback_context


from UI.ui_components import get_header, ticker_dropdown, update_button, \
                             get_forecast_plot, get_numbers_bar, get_forecast_gauge, get_stock_plot, \
                             get_today_change_guage, get_volume_plot, plot_vs_index_gauge, closing_price_plot, \
                             plot_predicted_volume_gauge, plot_cumulative_returns
                        
from data.data_handeler import get_data, get_cumm_ret_data, get_prophet_df, get_all_data

from models.models import load_volume_model, load_prophet_model, forecast, train_models_for_all_tickers
from utils.utils import get_financial_metrics


tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META"]

prophet_models, volume_models = train_models_for_all_tickers(tickers)
data = get_all_data(tickers)


initial_ticker = "AAPL"


left_content = get_header(initial_ticker)

right_content = html.Div(
        [ticker_dropdown, update_button],
        style={"display": "flex", "alignItems": "center", "gap": "10px", "justifyContent": "flex-end"}
    )

df, market_df, ticker = data[initial_ticker]
closing_price = closing_price_plot(ticker)
today_change_guage = get_today_change_guage(ticker)
volume_model = volume_models[initial_ticker]
volume_plot = get_volume_plot(df, initial_ticker)
volume_gauge = plot_predicted_volume_gauge(volume_model, df, initial_ticker)
combined = get_cumm_ret_data(df, market_df, initial_ticker)
cumulative_returns_plot = plot_cumulative_returns(initial_ticker, combined)
cumulative_returns_gauge = plot_vs_index_gauge(combined, initial_ticker)
prophet_model = prophet_models[initial_ticker]
prophet_df = get_prophet_df(df, initial_ticker)
forecast_data = forecast(prophet_model)
forecast_gauge = get_forecast_gauge(prophet_df, forecast_data)
forecast_plot = get_forecast_plot(forecast_data, prophet_df)
row_1 = get_stock_plot(df, initial_ticker)
revenue, net_income, profit_margin, fcf, eps, pe, dividend = get_financial_metrics(ticker)
bar_row = get_numbers_bar(revenue, net_income, profit_margin, fcf, eps, pe, dividend)

row_2 = dbc.Row([
    dbc.Col([
        dbc.Row([
            dbc.Col(closing_price, width=9),
            dbc.Col(today_change_guage, width=3)
        ]),
        dbc.Row([
            dbc.Col(volume_plot, width=9),
            dbc.Col(volume_gauge, width=3)
        ])
    ], width=6),
    dbc.Col([
        dbc.Row([
            dbc.Col(cumulative_returns_gauge, width=3),
            dbc.Col(cumulative_returns_plot, width=9)
        ]),
        dbc.Row([
            dbc.Col(forecast_gauge, width=3),
            dbc.Col(forecast_plot, width=9)
        ])
    ], width=6)
])

initial_dashboard = html.Div([bar_row, row_1, row_2])



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Stock Time Series Dashboard"

app.layout = html.Div([
    html.Div( dbc.Row([
        dbc.Col(left_content,id="header-section", width=6),
        dbc.Col(right_content, width=6)
    ], align="center", className="px-3 my-2")),
    
    html.Div(initial_dashboard, id="dashboard-content")
])


@app.callback(
    [Output("header-section", "children"),
     Output("dashboard-content", "children"),
     Output('ticker-dropdown', 'options'),
     Output('ticker-dropdown', 'value')],
    [Input("ticker-dropdown", "value"),
     Input("update-button", "n_clicks")]
)
def update_dashboard(ticker_string, n_clicks):
    triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    global data, prophet_models, volume_models
    
    if not ticker_string:
        raise PreventUpdate
    
    if triggered_id == "update-button":
        
        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META"]
        prophet_models, volume_models = train_models_for_all_tickers(tickers)
        data = get_all_data(tickers)
        
    df, market_df, ticker = data[ticker_string]

    closing_price = closing_price_plot(ticker)
    today_change_guage = get_today_change_guage(ticker)

    volume_model = volume_models[ticker_string]
    volume_plot = get_volume_plot(df, ticker_string)
    volume_gauge = plot_predicted_volume_gauge(volume_model, df, ticker_string)

    combined = get_cumm_ret_data(df, market_df, ticker_string)
    cumulative_returns_plot = plot_cumulative_returns(ticker_string, combined)
    cumulative_returns_gauge = plot_vs_index_gauge(combined, ticker_string)

    prophet_model = prophet_models[ticker_string]
    prophet_df = get_prophet_df(df, ticker_string)
    forecast_data = forecast(prophet_model)
    forecast_gauge = get_forecast_gauge(prophet_df, forecast_data)
    forecast_plot = get_forecast_plot(forecast_data, prophet_df)

    row_1 = get_stock_plot(df, ticker_string)

    row_2 = dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(closing_price, width=9),
                dbc.Col(today_change_guage, width=3)
            ]),
            dbc.Row([
                dbc.Col(volume_plot, width=9),
                dbc.Col(volume_gauge, width=3)
            ])
        ], width=6),
        dbc.Col([
            dbc.Row([
                dbc.Col(cumulative_returns_gauge, width=3),
                dbc.Col(cumulative_returns_plot, width=9)
            ]),
            dbc.Row([
                dbc.Col(forecast_gauge, width=3),
                dbc.Col(forecast_plot, width=9)
            ])
        ], width=6)
    ])
    
    revenue, net_income, profit_margin, fcf, eps, pe, dividend = get_financial_metrics(ticker)
    bar_row = get_numbers_bar(revenue, net_income, profit_margin, fcf, eps, pe, dividend)

    dashboard = html.Div([bar_row, row_1, row_2])
    header = get_header(ticker_string)

    new_options = [
        {'label': 'Apple', 'value': 'AAPL'},
        {'label': 'Microsoft', 'value': 'MSFT'},
        {'label': 'Google.', 'value': 'GOOGL'},
        {'label': 'Amazon', 'value': 'AMZN'},
        {'label': 'Tesla', 'value': 'TSLA'},
        {'label': 'Meta', 'value': 'META'},
    ]

    return header, dashboard, new_options, ticker_string


app.run(port=8080)