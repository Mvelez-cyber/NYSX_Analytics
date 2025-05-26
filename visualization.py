# visualization.py
import plotly.graph_objects as go

def plot_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candlestick'
    )])
    return fig

def plot_forecast_with_confidence(series, forecast, conf_int):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series.index, y=series, mode='lines', name='Actual'))
    future_dates = pd.date_range(start=series.index[-1], periods=len(forecast)+1, freq='D')[1:]
    fig.add_trace(go.Scatter(x=future_dates, y=forecast, mode='lines', name='Forecast'))
    fig.add_trace(go.Scatter(x=future_dates, y=conf_int.iloc[:, 0], fill=None, mode='lines', line=dict(color='lightgrey'), name='Lower Bound'))
    fig.add_trace(go.Scatter(x=future_dates, y=conf_int.iloc[:, 1], fill='tonexty', mode='lines', line=dict(color='lightgrey'), name='Upper Bound'))
    return fig
