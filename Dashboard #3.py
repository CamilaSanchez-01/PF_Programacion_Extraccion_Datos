import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, html, dcc

# Primero leemos el archivo csv, si no lo encuentra da error
try:
    df = pd.read_csv("/Users/jackymongenunez/Downloads/Ejemplosdeclase/Dataset/carros_limpio.csv")
except FileNotFoundError:
    raise Exception("❌ Archivo 'carros_limpio.csv' no se encuentra, checa bien la ruta porfa")

# Aqui limpiamos los nombres de las columnas para que no den problemas despues
df.columns = df.columns.str.strip().str.lower()

# Cambiamos los nombres de algunas columnas, porque al principio pusimos la columna equivocada de precios,
# aqui ya se usa la de Alemania (USD)
df.rename(columns={
    "segmento_mercado": "segmento",
    "alemania (usd)": "precio",
    "rango": "autonomia",
    "eficiencia": "eficiencia",
    "modelo": "modelo",
    "marca": "marca"
}, inplace=True)

# Convertimos la columna de precio y autonomia a numerico, pa poder graficar y hacer calculos
df["precio"] = pd.to_numeric(df["precio"], errors="coerce")
df["autonomia"] = df["autonomia"].str.replace(" km", "", regex=False)  # quitamos el " km" si viene
df["autonomia"] = pd.to_numeric(df["autonomia"], errors="coerce")

# Creamos una columna temporal de año con el año actual (nomás pa que se vea)
df["año"] = pd.to_datetime("today").year

# Quitamos los renglones que no tienen precio ni autonomia
df.dropna(subset=["precio", "autonomia"], inplace=True)

# Aquí vemos el rango minimo y maximo de autonomia, pa el slider de filtro
try:
    min_autonomia = int(df["autonomia"].min())
    max_autonomia = int(df["autonomia"].max())
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
app.layout = dbc.Container([
    html.H1(" Precios de Autos Eléctricos", className="my-3 text-center"),

    dbc.Card([
        dbc.CardHeader("Filtros"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Marca:"),
                    dcc.Dropdown(
                        options=[{"label": m, "value": m} for m in sorted(df["marca"].dropna().unique())],
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

# Función que se llama cuando cambian los filtros
@app.callback(
    Output("kpi_precio", "children"),
    Output("kpi_anios", "children"),
    Output("kpi_segmentos", "children"),
    Output("graf_precio_eficiencia", "figure"),
    Output("graf_dist_precios", "figure"),
    Output("graf_precio_anio", "figure"),
    Input("filtro_marca", "value"),
    Input("filtro_autonomia", "value")
)
def actualizar_dashboard(marca, autonomia):
    df_filtrado = df.copy()

    # Filtramos si se elige una marca
    if marca:
        df_filtrado = df_filtrado[df_filtrado["marca"] == marca]

    # Filtro por autonomia (rango del slider)
    if autonomia:
        min_auto, max_auto = autonomia
        df_filtrado = df_filtrado[(df_filtrado["autonomia"] >= min_auto) & (df_filtrado["autonomia"] <= max_auto)]

    # KPIs
    precio_prom = f"${df_filtrado['precio'].mean():,.0f}" if not df_filtrado.empty else "N/A"
    anios = df_filtrado["año"].nunique() if not df_filtrado.empty else "N/A"
    segmentos = df_filtrado["segmento"].nunique() if not df_filtrado.empty else "N/A"

    # Gráfica de eficiencia vs precio
    fig1 = px.scatter(
        df_filtrado,
        x="eficiencia",
        y="precio",
        color="marca",
        title="Relación Precio vs Eficiencia",
        hover_data=["modelo", "autonomia", "segmento"]
    ) if not df_filtrado.empty else {}

    # Histograma de precios
    fig2 = px.histogram(
        df_filtrado,
        x="precio",
        nbins=20,
        title="Distribución de Precios"
    ) if not df_filtrado.empty else {}

    # Promedio por año (aunque todos son del mismo año en este dataset jaja)
    df_agrupado = df_filtrado.groupby("año")["precio"].mean().reset_index()
    fig3 = px.bar(
        df_agrupado,
        x="año",
        y="precio",
        title="Precio Promedio por Año"
    ) if not df_filtrado.empty else {}

    return precio_prom, anios, segmentos, fig1, fig2, fig3


# Ejecutamos la app
if __name__ == "__main__":
    app.run(debug=True)
