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
    
    fig.update_layout(
        title="Gráfico de Velas - Datos Históricos",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        xaxis_rangeslider_visible=False,
        template="plotly_white"
    )
    
    return fig

def plot_forecast_with_confidence(history, forecast, conf):
    forecast_index = pd.date_range(start=history.index[-1], periods=len(forecast)+1, freq='D')[1:]
    
    fig = go.Figure()
    
    # Datos históricos
    fig.add_trace(go.Scatter(
        x=history.index,
        y=history,
        name='Histórico',
        line=dict(color='blue', width=2)
    ))
    
    # Predicción
    fig.add_trace(go.Scatter(
        x=forecast_index,
        y=forecast,
        name='Predicción',
        line=dict(color='green', width=2)
    ))
    
    # Intervalos de confianza
    fig.add_trace(go.Scatter(
        x=forecast_index,
        y=conf.iloc[:, 0],
        name='Confianza Baja',
        line=dict(dash='dot', color='lightblue'),
        fill=None
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_index,
        y=conf.iloc[:, 1],
        name='Confianza Alta',
        line=dict(dash='dot', color='lightblue'),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title="Predicción de Precios con Intervalos de Confianza",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        template="plotly_white",
        showlegend=True
    )
    
    return fig
