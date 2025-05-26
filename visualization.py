import plotly.graph_objects as go
import pandas as pd

def plot_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    fig.update_layout(title="Candlestick Chart", xaxis_rangeslider_visible=False)
    return fig

def plot_forecast_with_confidence(history, forecast, conf):
    forecast_index = pd.date_range(start=history.index[-1], periods=len(forecast)+1, freq='D')[1:]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=history.index, y=history, name='Histórico'))
    fig.add_trace(go.Scatter(x=forecast_index, y=forecast, name='Predicción'))
    fig.add_trace(go.Scatter(x=forecast_index, y=conf.iloc[:, 0], name='Confianza Baja',
                             line=dict(dash='dot'), marker=dict(color="lightblue")))
    fig.add_trace(go.Scatter(x=forecast_index, y=conf.iloc[:, 1], name='Confianza Alta',
                             line=dict(dash='dot'), fill='tonexty', marker=dict(color="lightblue")))
    fig.update_layout(title="Predicción con Intervalos de Confianza")
    return fig
