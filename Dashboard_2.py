import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, html, dcc

# Colores y estilos para que la app se vea cool y moderna
colors = {
    "background": "#0A0F24",
    "primary": "#00BFFF",
    "secondary": "#1E90FF",
    "accent": "#8A2BE2",
    "text_light": "#F0F8FF",
    "card_bg": "#11182F",
    "shadow": "0 0 18px #00BFFF"
}

styles = {
    "header": {
        "fontFamily": "'Orbitron', sans-serif",
        "color": colors["primary"],
        "fontSize": "2.5rem",
        "textAlign": "center",
        "marginBottom": "1rem",
        "textShadow": "0 0 15px #00BFFF",
        "letterSpacing": "1.5px"
    },
    "card": {
        "backgroundColor": colors["card_bg"],
        "borderRadius": "15px",
        "boxShadow": colors["shadow"],
        "padding": "20px",
        "marginBottom": "1.5rem",
        "color": colors["text_light"],
        "fontSize": "1.1rem",
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    },
    "label": {
        "color": colors["primary"],
        "fontWeight": "600",
        "fontFamily": "'Orbitron', sans-serif",
        "fontSize": "1.1rem"
    },
    "dropdown": {
        "backgroundColor": "#11182F",
        "color": "#1E3A8A",
        "borderRadius": "8px",
        "boxShadow": "0 0 12px #00BFFF"
    }
}

def eficiencia():
    try:
        df = pd.read_csv("Dataset/carros_limpio.csv")
        df = df.dropna(subset=['Eficiencia(Wh/km)', 'Peso(kg)'])
        marcas = sorted(df['Marca'].dropna().unique())
        min_eficiencia = int(df['Eficiencia(Wh/km)'].min())
        max_eficiencia = int(df['Eficiencia(Wh/km)'].max())

    except Exception as e:
        print(f"Error al cargar datos: {e}")
        marcas = []
        df = pd.DataFrame()
        min_eficiencia = 100
        max_eficiencia = 250

    return dbc.Container([
        html.H1("Análisis de Eficiencia Energética", style=styles["header"]),

        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Rango de Eficiencia (Wh/km):", style=styles["label"]),
                        dcc.RangeSlider(
                            id='eficiencia-slider',
                            min=min_eficiencia,
                            max=max_eficiencia,
                            step=5,
                            value=[min_eficiencia, max_eficiencia],
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], md=8),
                    dbc.Col([
                        html.Label("Marca:", style=styles["label"]),
                        dcc.Dropdown(
                            id='marca-filter',
                            options=[{'label': marca, 'value': marca} for marca in marcas],
                            placeholder="Todas las marcas",
                            style=styles["dropdown"]
                        )
                    ], md=4)
                ])
            ])
        ], style=styles["card"]),

        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("➕ Eficiencia Promedio", style=styles["label"]),
                        html.H2(id='kpi-eficiencia-promedio', style=styles["header"])
                    ])
                ], style=styles["card"]),
                md=4
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🚗 Vehículo Más Eficiente", style=styles["label"]),
                        html.H5(id='kpi-modelo-eficiente', style={"color": colors["text_light"]}),
                        html.P(id='kpi-valor-eficiente', style={"color": colors["primary"]})
                    ])
                ], style=styles["card"]),
                md=4
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H4("⚖️ Relación Peso-Eficiencia", style=styles["label"]),
                        html.H2(id='kpi-correlacion', style=styles["header"])
                    ])
                ], style=styles["card"]),
                md=4
            )
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id='scatter-eficiencia-peso'), md=6),
            dbc.Col(dcc.Graph(id='scatter-eficiencia-rango'), md=6)
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id='histograma-eficiencia'), md=12)
        ])
    ], fluid=True)

@callback(
    [Output('kpi-eficiencia-promedio', 'children'),
     Output('kpi-modelo-eficiente', 'children'),
     Output('kpi-valor-eficiente', 'children'),
     Output('kpi-correlacion', 'children'),
     Output('scatter-eficiencia-peso', 'figure'),
     Output('scatter-eficiencia-rango', 'figure'),
     Output('histograma-eficiencia', 'figure')],
    [Input('eficiencia-slider', 'value'),
     Input('marca-filter', 'value')]
)
def update_dashboard(eficiencia_range, marca_seleccionada):
    try:
        df = pd.read_csv("Dataset/carros_limpio.csv")
        df = df.dropna(subset=['Eficiencia(Wh/km)', 'Peso(kg)'])

        min_val = int(df['Eficiencia(Wh/km)'].min())
        max_val = int(df['Eficiencia(Wh/km)'].max())
        eficiencia_range = [
            max(eficiencia_range[0], min_val),  # No menor que el mínimo real
            min(eficiencia_range[1], max_val)  # No mayor que el máximo real
        ]

        mask = (df['Eficiencia(Wh/km)'] >= eficiencia_range[0]) & (df['Eficiencia(Wh/km)'] <= eficiencia_range[1])
        if marca_seleccionada:
            mask &= df['Marca'] == marca_seleccionada

        df_filtered = df[mask].copy()

        if df_filtered.empty:
            raise ValueError("No hay datos con los filtros seleccionados")

        eficiencia_promedio = f"{df_filtered['Eficiencia(Wh/km)'].mean():.1f}"
        idx_min = df_filtered['Eficiencia(Wh/km)'].idxmin()
        modelo_eficiente = f"{df_filtered.loc[idx_min, 'Marca']} {df_filtered.loc[idx_min, 'Modelo']}"
        valor_eficiente = f"{df_filtered.loc[idx_min, 'Eficiencia(Wh/km)']:.1f} Wh/km"
        correlacion = f"{df_filtered['Eficiencia(Wh/km)'].corr(df_filtered['Peso(kg)']):.2f}"

        fig_scatter_peso = px.scatter(
            df_filtered,
            x='Peso(kg)',
            y='Eficiencia(Wh/km)',
            color='Marca',
            hover_name='Modelo',
            template="plotly_dark",
            hover_data=['Rango(Km)', 'Bateria(kWh)'],
            labels={'Peso(kg)': 'Peso (kg)', 'Eficiencia(Wh/km)': 'Eficiencia (Wh/km)'},
            title='⚖️ Peso vs Eficiencia'
        )

        fig_scatter_rango = px.scatter(
            df_filtered,
            x='Rango(Km)',
            y='Eficiencia(Wh/km)',
            color='Marca',
            size='Bateria(kWh)',
            hover_name='Modelo',
            template="plotly_dark",
            labels={'Rango(Km)': 'Rango (km)', 'Eficiencia(Wh/km)': 'Eficiencia (Wh/km)', 'Bateria(kWh)': 'Batería (kWh)'},
            title='🏁 Rango vs Eficiencia'
        )

        fig_hist = px.histogram(
            df_filtered,
            x='Eficiencia(Wh/km)',
            nbins=15,
            color='Marca',
            template="plotly_dark",
            labels={'Eficiencia(Wh/km)': 'Eficiencia (Wh/km)'},
            title='🚙 Distribución de Eficiencia'
        )

        return (
            eficiencia_promedio,
            modelo_eficiente,
            valor_eficiente,
            correlacion,
            fig_scatter_peso,
            fig_scatter_rango,
            fig_hist
        )

    except Exception as e:
        print(f"Error: {e}")
        empty_fig = px.scatter(title="No hay datos disponibles")
        return ("N/A", "N/A", "N/A", "N/A", empty_fig, empty_fig, empty_fig)
