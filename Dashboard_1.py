import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, html, dcc

# Paleta de colores para mantener consistencia
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
        "color": colors["text_light"],
        "borderRadius": "8px",
        "boxShadow": "0 0 12px #00BFFF"
    },
    "img_style": {
        "width": "160px",
        "height": "140px",
        "borderRadius": "15px",
        "boxShadow": "0 0 20px #00BFFF",
        "marginBottom": "1rem"
    }
}

def carga_rapida():
    # Esta funcion carga el archivo CSV de datos limpios de carros electricos
    # Y genera la estructura visual principal con los filtros y graficos para mostrar info sobre carga rapida y bateria
    df = pd.read_csv("Dataset/carros_limpio.csv")

    body = dbc.Container([
        html.H2("Carga Rápida 🔌", style=styles["header"]),
        dbc.Card([

            dbc.CardBody([
                dbc.Label("Marca:", style=styles["label"]),
                dcc.Dropdown(
                    options=[{"label": m, "value": m} for m in sorted(df["Marca"].dropna().unique())],
                    value=None,
                    id="ddMarca",
                    style=styles["dropdown"],
                    clearable=True,
                    placeholder="Selecciona una marca"
                )
            ])
        ], style=styles["card"]),
        dbc.Row([
            html.Img(src="assets/imagenes/carrot.png", style=styles["img_style"]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🚘 Promedio de Carga Rápida (kW)", className="card-title", style={"color": colors["primary"], "fontFamily": "'Orbitron', sans-serif"}),
                        html.H4(id="kpi-carga", className="card-text", style={"color": colors["text_light"]})
                    ])
                ], style=styles["card"])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🚙 Auto con Mayor Carga Rápida", className="card-title", style={"color": colors["primary"], "fontFamily": "'Orbitron', sans-serif"}),
                        html.H4(id="kpi-auto", className="card-text", style={"color": colors["text_light"]})
                    ])
                ], style=styles["card"])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🚗 Promedio de Batería (kWh)", className="card-title", style={"color": colors["primary"], "fontFamily": "'Orbitron', sans-serif"}),
                        html.H4(id="kpi-bateria", className="card-text", style={"color": colors["text_light"]})
                    ])
                ], style=styles["card"])
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(id="barras-mayor", style={"height": "400px"}), md=6),
            dbc.Col(dcc.Graph(id="barras-menor", style={"height": "400px"}), md=6),
            dbc.Col(dcc.Graph(id="barras-rendi", style={"height": "400px"}), md=12),
            dbc.Col(dcc.Graph(id="barras-carga", style={"height": "400px"}), md=12),
        ])
    ], fluid=True, style={"backgroundColor": colors["background"], "paddingTop": "2rem"})

    return body

# Callback que actualiza los indicadores y graficos con base en la marca seleccionada en el dropdown
@callback(
    Output("kpi-carga", "children"),
    Output("kpi-bateria", "children"),
    Output("kpi-auto", "children"),
    Output("barras-mayor", "figure"),
    Output("barras-menor", "figure"),
    Output("barras-rendi", "figure"),
    Output("barras-carga", "figure"),
    Input("ddMarca", "value")
)
def figuras(Marca):
    # Leer el CSV con los datos limpios
    df = pd.read_csv("Dataset/carros_limpio.csv")

    # Filtrar por marca si se selecciono alguna
    if Marca:
        df_marca = df[df.Marca == Marca]
    else:
        df_marca = df

    # Calculo de indicadores principales
    kpi_carga = f"{df_marca['Carga_Rapida'].mean():.2f} kW"
    kpi_bateria = f"{df_marca['Bateria(kWh)'].mean():.2f} kW"
    kpi_auto = df_marca.sort_values(by="Carga_Rapida", ascending=False).iloc[0]["Modelo"]

    # Top 5 autos con mayor y menor carga rapida
    top_mayor = df_marca.sort_values(by="Carga_Rapida", ascending=False).head(5)
    top_menor = df_marca.sort_values(by="Carga_Rapida").tail(5)

    # Graficos de barras para top autos con mayor carga rapida
    fig_mayor = px.bar(
        top_mayor,
        x="Modelo",
        y="Carga_Rapida",
        color="Modelo",
        title="🔋 Top 5 Autos con Mayor Capacidad de Carga (kW)",
        template="plotly_dark",
        color_discrete_sequence=[colors["primary"], colors["secondary"], colors["accent"], "#8A2BE2", "#00BFFF"]
    )
    fig_mayor.update_layout(xaxis=dict(showticklabels=False))

    # Graficos de barras para top autos con menor carga rapida
    fig_menor = px.bar(
        top_menor,
        x="Modelo",
        y="Carga_Rapida",
        color="Modelo",
        title="🪫Top 5 Autos con Menor Capacidad de Carga (kW)",
        template="plotly_dark",
        color_discrete_sequence=[colors["accent"], colors["secondary"], colors["primary"], "#1E90FF", "#8A2BE2"]
    )
    fig_menor.update_layout(xaxis=dict(showticklabels=False))

    # Grafico de dispersion que muestra el rendimiento en carga rapida con tamaño y color segun carga
    fig_rendi = px.scatter(
        df_marca,
        x="Carga_Vol",
        y="Bateria(kWh)",
        color="Carga_Rapida",
        template="plotly_dark",
        title="🗺️🌍 Mapa de Rendimiento en Carga Rápida",
        hover_name="Modelo",
        size="Carga_Rapida",
        labels={"Carga_Vol": "Tamaño total de carga (kWh)"}
    )

    # Grafico de dispersion para mostrar modelos con mejor rendimiento por parada de carga
    fig_carga = px.scatter(
        df_marca,
        x="Rango_1_parada",
        y="Modelo",
        color="Marca",
        template="plotly_dark",
        title="🚏 Modelos con Mejor Rendimiento por Carga Parcial",
        labels={"Rango_1_parada": "Rendimiento por Parada (km)"}
    )

    return kpi_carga, kpi_bateria, kpi_auto, fig_mayor, fig_menor, fig_rendi, fig_carga
