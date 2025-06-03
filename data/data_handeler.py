import pandas as pd
import yfinance as yf

def get_data(ticker_string):
    df = yf.download(ticker_string)
    market_df = yf.download('^GSPC')
    ticker = yf.Ticker(ticker_string)
    df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
    df = df.reset_index()
    df = df[['Date', f'High_{ticker_string}', f'Open_{ticker_string}', f'Close_{ticker_string}', f'Low_{ticker_string}', f'Volume_{ticker_string}']].copy()
    df['Date'] = pd.to_datetime(df['Date']) 
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df, market_df, ticker


def get_cumm_ret_data(df, market_df, ticker_string):
    
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    market_df = market_df.copy()
    market_df = market_df[['Close']].rename(columns={'Close': 'S&P 500'})

    stock_df = df[[f'Close_{ticker_string}']].rename(columns={f'Close_{ticker_string}': ticker_string})

    stock_df['SMA_20'] = stock_df[ticker_string].rolling(window=20).mean()
    stock_df['SMA_50'] = stock_df[ticker_string].rolling(window=50).mean()
    stock_df['Volatility_20'] = stock_df[ticker_string].rolling(window=20).std()
    stock_df['Daily Return'] = stock_df[ticker_string].pct_change()
    market_df['Daily Return'] = market_df['S&P 500'].pct_change()

    stock_df['Cumulative Return'] = (1 + stock_df['Daily Return']).cumprod()
    market_df['Cumulative Return'] = (1 + market_df['Daily Return']).cumprod()

    combined = pd.concat([
        stock_df['Cumulative Return'],
        market_df['Cumulative Return']
    ], axis=1)
    
    return combined

def get_prophet_df(df, ticker):
    prophet_df = df[['Date', f'Close_{ticker}']].copy()
    prophet_df.columns = ['ds', 'y']
    prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])
    return prophet_df

def get_all_data(tickers):
    data = {}
    for ticker_string in tickers:
        df, market_df, ticker = get_data(ticker_string)
        data[ticker_string] = df, market_df, ticker
    return data