import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, html, dcc,callback


def distribucion_precios ():

    # Primero leemos el archivo csv, si no lo encuentra da error
    try:
        df = pd.read_csv("Dataset/carros_limpio.csv")
    except FileNotFoundError:
        raise Exception("❌ Archivo 'carros_limpio.csv' no se encuentra, checa bien la ruta porfa")


    # Creamos una columna temporal de año con el año actual (nomás pa que se vea)
    df["año"] = pd.to_datetime("today").year

    df["Alemania (USD)"] = pd.to_numeric(df["Alemania (USD)"], errors="coerce")

    # Quitamos los renglones que no tienen precio ni autonomia
    df.dropna(subset=["Alemania (USD)", "Rango(Km)"], inplace=True)

    # Aquí vemos el rango minimo y maximo de autonomia, pa el slider de filtro
    try:
        min_autonomia = int(df["Rango(Km)"].min())
        max_autonomia = int(df["Rango(Km)"].max())
    except (ValueError, TypeError):
        print("⚠️ Problemas con la autonomia, se van a usar valores default")
        min_autonomia = 0
        max_autonomia = 600

    # Creamos las marcas del slider (cada 50km)
    marks = {i: str(i) for i in range(min_autonomia, max_autonomia + 1, 50)}

    # Creamos la app de Dash con tema oscuro (cyborg se ve chido jeje)
    app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
    app.title = "Dashboard Autos Eléctricos"

    # Layout de toda la app
    layout = dbc.Container([
        html.H1(" Precios de Autos Eléctricos", className="my-3 text-center"),

        dbc.Card([
            dbc.CardHeader("Filtros"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Marca:"),
                        dcc.Dropdown(
                            options=[{"label": m, "value": m} for m in sorted(df["Marca"].dropna().unique())],
                            value=None,
                            id="filtro_marca",
                            placeholder="Selecciona una marca"
                        ),
                    ], md=6),

                    dbc.Col([
                        dbc.Label("Autonomía (km):"),
                        dcc.RangeSlider(
                            id="filtro_autonomia",
                            min=min_autonomia,
                            max=max_autonomia,
                            step=1,
                            value=[min_autonomia, max_autonomia],
                            marks=marks,
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ], md=6)
                ])
            ])
        ], className="mb-4"),

        # KPIs principales
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Precio Promedio (USD)", className="card-title"),
                    html.H4(id="kpi_precio", className="card-text")
                ])
            ], color="info", inverse=True), md=4),

            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Años Analizados", className="card-title"),
                    html.H4(id="kpi_anios", className="card-text")
                ])
            ], color="primary", inverse=True), md=4),

            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("Segmentos Detectados", className="card-title"),
                    html.H4(id="kpi_segmentos", className="card-text")
                ])
            ], color="secondary", inverse=True), md=4),
        ], className="mb-4"),

        # Graficas
        dbc.Row([
            dbc.Col(dcc.Graph(id="graf_precio_eficiencia"), md=6),
            dbc.Col(dcc.Graph(id="graf_dist_precios"), md=6),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id="graf_precio_anio"), md=12),
        ]),
    ], fluid=True)
    return layout

    # Función que se llama cuando cambian los filtros
@callback(
        Output("kpi_precio", "children"),
        Output("kpi_anios", "children"),
        Output("kpi_segmentos", "children"),
        Output("graf_precio_eficiencia", "figure"),
        Output("graf_dist_precios", "figure"),
        Output("graf_precio_anio", "figure"),
        Input("filtro_marca", "value"),
        Input("filtro_autonomia", "value")
    )

def figuras(marca, autonomia):
    # Primero leemos el archivo csv, si no lo encuentra da error
    try:
        df = pd.read_csv("Dataset/carros_limpio.csv")
    except FileNotFoundError:
        raise Exception("❌ Archivo 'carros_limpio.csv' no se encuentra, checa bien la ruta porfa")

 # Creamos una columna temporal de año con el año actual (nomás pa que se vea)
    df["año"] = pd.to_datetime("today").year
    df["Alemania (USD)"] = pd.to_numeric(df["Alemania (USD)"], errors="coerce")

    # Quitamos los renglones que no tienen precio ni autonomia
    df.dropna(subset=["Alemania (USD)", "Rango(Km)"], inplace=True)

    df_filtrado = df

    # Filtramos si se elige una marca
    if marca:
        df_filtrado = df_filtrado[df_filtrado["Marca"] == marca]

    # Filtro por autonomia (rango del slider)
    if autonomia:
        min_auto, max_auto = autonomia
        df_filtrado = df_filtrado[(df_filtrado["Rango(Km)"] >= min_auto) & (df_filtrado["Rango(Km)"] <= max_auto)]

    # KPIs
    precio_prom = f"${df_filtrado['Alemania (USD)'].mean():,.0f}" if not df_filtrado.empty else "N/A"
    anios = df_filtrado["año"].nunique() if not df_filtrado.empty else "N/A"
    segmentos = df_filtrado["Segmento_mercado"].nunique() if not df_filtrado.empty else "N/A"

    # Gráfica de eficiencia vs precio
    fig1 = px.scatter(
        df_filtrado,
        x="Eficiencia(Wh/km)",
        y="Alemania (USD)",
        color="Marca", template="plotly_dark",
        title="Relación Precio vs Eficiencia",
        hover_data=["Modelo", "Rango(Km)", "Segmento_mercado"]
        ) if not df_filtrado.empty else {}

    # Histograma de precios
    fig2 = px.histogram(
            df_filtrado,
            x="Alemania (USD)",
            nbins=20, template="plotly_dark",
            title="Distribución de Precios"
        ) if not df_filtrado.empty else {}

    # Promedio por año (aunque todos son del mismo año en este dataset jaja)
    df_agrupado = df_filtrado.groupby("año")["Alemania (USD)"].mean().reset_index()
    fig3 = px.bar(
            df_agrupado,
            x="año",
            y="Alemania (USD)",template="plotly_dark",
            title="Precio Promedio por Año"
        ) if not df_filtrado.empty else {}


    return precio_prom, anios, segmentos, fig1, fig2, fig3



