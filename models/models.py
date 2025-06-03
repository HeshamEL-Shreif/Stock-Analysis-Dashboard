import os
import joblib
import pickle
from sklearn.linear_model import LinearRegression
import numpy as np
from prophet import Prophet
import pandas as pd
from data.data_handeler import get_data
from data.data_handeler import get_prophet_df

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def save_model(model, filename):
    filepath = os.path.join(MODEL_DIR, filename)
    with open(filepath, "wb") as f:
        pickle.dump(model, f)

def load_model(filename):
    filepath = os.path.join(MODEL_DIR, filename)
    with open(filepath, "rb") as f:
        return pickle.load(f)
    
def train_volume_model(df, ticker):
    X = np.array(df.index).reshape(-1, 1)
    y = df[f'Volume_{ticker}'].values.reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    save_model(model, f"volume_model_{ticker}.pkl")
    return model


def train_prophet_model(prophet_df, ticker):
    model = Prophet()
    model.fit(prophet_df)

    save_model(model, f"prophet_model_{ticker}.pkl")
    return model

def train_models_for_all_tickers(tickers):
    prophet_models = {}
    volume_models = {}  
    for ticker in tickers:
        df, _, _ = get_data(ticker)
        print(f"Training models for {ticker}...")
        volume_models[ticker] = train_volume_model(df, ticker)
        
        prophet_df = get_prophet_df(df, ticker)
        
        prophet_models[ticker] = train_prophet_model(prophet_df, ticker)
    return prophet_models, volume_models
        
def load_volume_model(ticker):
    if os.path.exists(f"volume_model_{ticker}.pkl"):
        return load_model(f"volume_model_{ticker}.pkl")
    return None

def load_prophet_model(ticker):
    if os.path.exists(f"prophet_model_{ticker}.pkl"):
        return load_model(f"prophet_model_{ticker}.pkl")
    return None

def forecast(model):
    future = model.make_future_dataframe(periods=60)
    forecast_data = model.predict(future)
    return forecast_data


def load_models_for_all_tickers(df, tickers):
    prophet_models = {}
    volume_models = {}  
    for ticker in tickers:
        print(f"loading models for {ticker}...")
        volume_model = load_volume_model(ticker)  
        if volume_model:
            volume_models[ticker] = volume_model 
        else:
            
             volume_models[ticker] =  train_volume_model(df[ticker][0], ticker)
        
        prophet_model = load_prophet_model(ticker)
        if prophet_model:
            prophet_models[ticker] = prophet_model
        else:
            prophet_df = get_prophet_df(df[ticker][0], ticker)
            prophet_models[ticker] = train_prophet_model(prophet_df, ticker)
            
    return prophet_models, volume_models