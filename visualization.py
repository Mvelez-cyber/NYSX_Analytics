import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def plot_candlestick(df):
    # Filtrar para eliminar sábados (5) y domingos (6)
    if isinstance(df.index, pd.DatetimeIndex):
        df_filtrado = df[df.index.dayofweek < 5]
    else:
        # Si el índice no es DatetimeIndex, intentar convertirlo
        df = df.copy()
        df.index = pd.to_datetime(df.index)
        df_filtrado = df[df.index.dayofweek < 5]

    # Eliminar filas con datos faltantes en OHLC
    df_filtrado = df_filtrado.dropna(subset=['open', 'high', 'low', 'close'])

    fig = go.Figure(data=[go.Candlestick(
        x=df_filtrado.index,
        open=df_filtrado['open'],
        high=df_filtrado['high'],
        low=df_filtrado['low'],
        close=df_filtrado['close']
    )])
    
    fig.update_layout(
        title="Gráfico de Velas - Datos Históricos (Días Laborables)",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        xaxis=dict(
            type='date',
            tickformat='%Y-%m-%d',
            tickmode='auto',
            nticks=10,
            tickangle=45,
            color='white'
        ),
        yaxis=dict(
            color='white'
        )
    )
    
    return fig

def plot_forecast_with_confidence(history, forecast, conf):
    # Limitar la predicción a los próximos 7 días laborables
    dias_prediccion = 7

    # Generar fechas solo para días laborables
    last_date = history.index[-1]
    forecast_dates = []
    current_date = last_date + timedelta(days=1)
    days_added = 0

    while days_added < dias_prediccion:
        if current_date.dayofweek < 5:  # 0-4 son lunes a viernes
            forecast_dates.append(current_date)
            days_added += 1
        current_date += timedelta(days=1)

    forecast_index = pd.DatetimeIndex(forecast_dates)

    # Limitar el forecast a los próximos 7 días laborables
    forecast = np.array(forecast[:dias_prediccion])

    # Calcular el 10% del precio actual
    current_price = history.iloc[-1]
    confidence_range = current_price * 0.10

    # Crear nuevos intervalos de confianza
    lower_bound = forecast - confidence_range
    upper_bound = forecast + confidence_range

    # --- Estilo similar al gráfico de la imagen proporcionada ---
    fig = go.Figure()

    # Línea histórica (color púrpura, igual que la imagen)
    fig.add_trace(go.Scatter(
        x=history.index,
        y=history,
        mode='lines',
        line=dict(color='purple', width=2),
        name='Histórico'
    ))

    # Línea de predicción (púrpura, pero con mayor grosor y dash para diferenciar)
    fig.add_trace(go.Scatter(
        x=forecast_index,
        y=forecast,
        mode='lines',
        line=dict(color='purple', width=3, dash='dash'),
        name='Predicción'
    ))

    # Banda de confianza (relleno suave, color púrpura claro, sin bordes)
    fig.add_trace(go.Scatter(
        x=np.concatenate([forecast_index, forecast_index[::-1]]),
        y=np.concatenate([upper_bound, lower_bound[::-1]]),
        fill='toself',
        fillcolor='rgba(128, 0, 128, 0.18)',  # púrpura claro y translúcido
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=True,
        name='Intervalo de Confianza (±10%)'
    ))

    # Configuración del layout para fondo negro y estilo similar a la imagen
    fig.update_layout(
        title="Predicción de Precios con Intervalos de Confianza (±10%) - Próximos 7 Días Laborables",
        xaxis_title="Fecha",
        yaxis_title="Precio (USD)",
        template="plotly_dark",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color='white')
        ),
        hovermode='x unified',
        xaxis=dict(
            type='date',
            tickformat='%b\n%Y',
            showgrid=False,
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            mirror=True,
            color='white'
        ),
        yaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            mirror=True,
            color='white'
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
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
        template="plotly_dark",
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        xaxis=dict(
            showgrid=False,
            tickformat='%b %Y',
            color='white'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            color='white'
        )
    )
    return fig
