import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, html, dcc, callback

# Colores chidos para que todo se vea uniforme y moderno
theme_colors = {
    "background": "#0A0F24",
    "primary": "#00BFFF",
    "secondary": "#1E90FF",
    "accent": "#8A2BE2",
    "text_light": "#F0F8FF",
    "card_bg": "#11182F",
    "shadow": "0 0 18px #00BFFF"
}

# Estilos para que los textos, tarjetas y dropdowns tengan buena pinta
styles = {
    "header": {
        "fontFamily": "'Orbitron', sans-serif",
        "color": theme_colors["primary"],
        "fontSize": "2.5rem",
        "textAlign": "center",
        "marginBottom": "1rem",
        "textShadow": "0 0 15px #00BFFF",
        "letterSpacing": "1.5px"
    },
    "card": {
        "backgroundColor": theme_colors["card_bg"],
        "borderRadius": "15px",
        "boxShadow": theme_colors["shadow"],
        "padding": "20px",
        "marginBottom": "1.5rem",
        "color": theme_colors["text_light"],
        "fontSize": "1.1rem",
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    },
    "label": {
        "color": theme_colors["primary"],
        "fontWeight": "600",
        "fontFamily": "'Orbitron', sans-serif",
        "fontSize": "1.1rem"
    },
    "dropdown": {
        "backgroundColor": theme_colors["card_bg"],
        "color": "#1E3A8A",
        "borderRadius": "8px",
        "boxShadow": "0 0 12px #00BFFF"
    }
}

def distribucion_precios():
    # Primero intentamos abrir el archivo con los datos
    try:
        df = pd.read_csv("Dataset/carros_limpio.csv")
    except FileNotFoundError:
        raise Exception("❌ No encuentro el archivo 'carros_limpio.csv', checa que la ruta esté bien")

    # Añadimos columna con el año actual para usar en gráficos
    df["año"] = pd.to_datetime("today").year

    # Asegurarnos que la columna de precios sea numérica (por si hay datos raros)
    df["Alemania (USD)"] = pd.to_numeric(df["Alemania (USD)"], errors="coerce")

    # Quitamos filas que no tengan precio o rango para que no den problemas
    df.dropna(subset=["Alemania (USD)", "Rango(Km)"], inplace=True)

    # Sacamos los valores mínimo y máximo del rango para el slider
    try:
        min_autonomia = int(df["Rango(Km)"].min())
        max_autonomia = int(df["Rango(Km)"].max())
    except (ValueError, TypeError):
        min_autonomia = 0
        max_autonomia = 600  # fallback por si hay datos raros

    # Creamos las marcas para el slider cada 50 km
    marks = {i: str(i) for i in range(min_autonomia, max_autonomia + 1, 50)}

    # Configuramos la app Dash con tema oscuro (Cyborg)
    app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
    app.title = "Dashboard Autos Eléctricos"

    # Armamos el layout con filtros, KPIs y gráficos
    layout = dbc.Container([
        html.H1("Precios de Autos Eléctricos", style=styles["header"]),

        # Aquí van los filtros para que puedas elegir marca y autonomía
        dbc.Card([
            dbc.CardHeader("Filtros", style=styles["label"]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Marca:", style=styles["label"]),
                        dcc.Dropdown(
                            options=[{"label": m, "value": m} for m in sorted(df["Marca"].dropna().unique())],
                            value=None,
                            id="filtro_marca",
                            placeholder="Selecciona una marca",
                            style=styles["dropdown"]
                        ),
                    ], md=6),
                    dbc.Col([
                        dbc.Label("Autonomía (km):", style=styles["label"]),
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
        ], className="mb-4", style=styles["card"]),

        # Tarjetas con números importantes para que veas rápido la info clave
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("💵 Precio Promedio (USD)", className="card-title"),
                    html.H4(id="kpi_precio", className="card-text")
                ])
            ], style=styles["card"]), md=4),

            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("🚀 Auto Más Caro", className="card-title"),
                    html.H4(id="kpi_mas_caro", className="card-text")
                ])
            ], style=styles["card"]), md=4),

            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H6("💲 Auto Más Barato", className="card-title"),
                    html.H4(id="kpi_mas_barato", className="card-text")
                ])
            ], style=styles["card"]), md=4),
        ], className="mb-4"),

        # Gráficos para que veas visualmente la info
        dbc.Row([
            dbc.Col(dcc.Graph(id="graf_precio_eficiencia"), md=6),
            dbc.Col(dcc.Graph(id="graf_dist_precios"), md=6),
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id="graf_precio_rango"), md=12),
        ]),
    ], fluid=True)

    return layout

@callback(
    # Aquí actualizamos todo cuando cambias algún filtro
    Output("kpi_precio", "children"),
    Output("kpi_mas_caro", "children"),
    Output("kpi_mas_barato", "children"),
    Output("graf_precio_eficiencia", "figure"),
    Output("graf_dist_precios", "figure"),
    Output("graf_precio_rango", "figure"),
    Input("filtro_marca", "value"),
    Input("filtro_autonomia", "value")
)
def figuras(marca, autonomia):
    # Volvemos a cargar los datos para tenerlos frescos al actualizar filtros
    try:
        df = pd.read_csv("Dataset/carros_limpio.csv")
    except FileNotFoundError:
        raise Exception("❌ No encuentro el archivo 'carros_limpio.csv', checa que la ruta esté bien")


    df["Alemania (USD)"] = pd.to_numeric(df["Alemania (USD)"], errors="coerce")
    df.dropna(subset=["Alemania (USD)", "Rango(Km)"], inplace=True)

    # Filtramos según lo que elegiste en la app
    df_filtrado = df
    if marca:
        df_filtrado = df_filtrado[df_filtrado["Marca"] == marca]
    if autonomia:
        min_auto, max_auto = autonomia
        df_filtrado = df_filtrado[(df_filtrado["Rango(Km)"] >= min_auto) & (df_filtrado["Rango(Km)"] <= max_auto)]

    # KPIs que mostramos arriba, con chequeo por si no hay datos
    precio_prom = f"${df_filtrado['Alemania (USD)'].mean():,.0f}" if not df_filtrado.empty else "N/A"


    mas_caro = (
        df_filtrado.loc[df_filtrado["Alemania (USD)"].idxmax(), "Modelo"]
        if not df_filtrado.empty else "N/A"
    )

    mas_barato = (
        df_filtrado.loc[df_filtrado["Alemania (USD)"].idxmin(), "Modelo"]
        if not df_filtrado.empty else "N/A"
    )

    # Gráfico para ver precio vs eficiencia
    fig1 = px.scatter(
        df_filtrado,
        x="Eficiencia(Wh/km)",
        y="Alemania (USD)",
        color="Marca",
        template="plotly_dark",
        title="💵🏁 Relación Precio vs Eficiencia",labels={"Alemania (USD)": "Precio" },
        hover_data=["Modelo", "Rango(Km)"]
    ) if not df_filtrado.empty else {}

    # Histograma para ver cómo se distribuyen los precios
    fig2 = px.histogram(
        df_filtrado,
        x="Alemania (USD)",
        nbins=20,color="Marca",
        template="plotly_dark",labels={"Alemania (USD)": "Precio" },
        title="⚖️💸 Distribución de Precios"
    ) if not df_filtrado.empty else {}

    # Gráfico para ver el rango de precios vs el rango
    fig3 = px.scatter(
        df_filtrado,
        x="Precio_Rango",
        y="Rango(Km)",
        color="Modelo",hover_name="Modelo",
        template="plotly_dark", labels={"Precio_Rango": "Rango_Precio (USD)"},
        title="➕💵 Relación de Precio y Rango"
    ) if not df_filtrado.empty else {}
    # Regresamos
    return precio_prom, mas_caro, mas_barato, fig1, fig2, fig3
