import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def plot_candlestick(df):
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    
    fig.update_layout(
        title="Gráfico de Velas - Datos Históricos (Días Laborables)",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        xaxis=dict(
            type='date',
            tickformat='%Y-%m-%d',
            tickmode='auto',
            nticks=10,
            tickangle=45
        )
    )
    
    return fig

def plot_forecast_with_confidence(history, forecast, conf):
    # Generar fechas solo para días laborables
    last_date = history.index[-1]
    forecast_dates = []
    current_date = last_date + timedelta(days=1)
    days_added = 0
    
    while days_added < len(forecast):
        if current_date.dayofweek < 5:  # 0-4 son lunes a viernes
            forecast_dates.append(current_date)
            days_added += 1
        current_date += timedelta(days=1)
    
    forecast_index = pd.DatetimeIndex(forecast_dates)
    
    # Calcular el 10% del precio actual
    current_price = history.iloc[-1]
    confidence_range = current_price * 0.10
    
    # Crear nuevos intervalos de confianza
    lower_bound = forecast[:len(forecast_index)] - confidence_range
    upper_bound = forecast[:len(forecast_index)] + confidence_range
    
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
        y=forecast[:len(forecast_index)],
        name='Predicción',
        line=dict(color='green', width=2)
    ))
    
    # Nuevos intervalos de confianza
    fig.add_trace(go.Scatter(
        x=forecast_index,
        y=lower_bound,
        name='Confianza Baja (-10%)',
        line=dict(dash='dot', color='lightblue'),
        fill=None
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_index,
        y=upper_bound,
        name='Confianza Alta (+10%)',
        line=dict(dash='dot', color='lightblue'),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title="Predicción de Precios con Intervalos de Confianza (±10%) - Días Laborables",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        template="plotly_white",
        showlegend=True,
        hovermode='x unified',
        xaxis=dict(
            type='date',
            tickformat='%Y-%m-%d',
            tickmode='auto',
            nticks=10,
            tickangle=45
        )
    )
    
    # Agregar anotación con el rango de confianza
    fig.add_annotation(
        x=forecast_index[0],
        y=upper_bound[0],
        text=f"Rango de confianza: ±${confidence_range:.2f}",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    
    return fig

def plot_price_line(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['close'],
        mode='lines',
        line=dict(color='purple', width=2),
        name='Precio de Cierre'
    ))

    fig.update_layout(
        title="Precio Histórico de Cierre",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        template="plotly_dark",  # Fondo oscuro
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            showgrid=False,
            tickformat='%b %Y'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)'
        )
    )
    return fig
