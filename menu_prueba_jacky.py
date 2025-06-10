import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, html, dcc

# Leer el dataset
df = pd.read_csv("/Users/jackymongenunez/Downloads/Ejemplosdeclase/Dataset/carros_limpio.csv")

# Crear app con tema oscuro base
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

neon_blue = "#00FFFF"
dark_bg = "#0B0C10"
card_bg = "#1F2833"
border_color = "#45A29E"
text_color = "#66FCF1"

styles = {
    "header": {
        "font-family": "'Orbitron', sans-serif",
        "color": neon_blue,
        "textAlign": "center",
        "marginTop": "30px",
        "marginBottom": "20px",
        "textShadow": "0 0 8px #00FFFF"
    },
    "card": {
        "backgroundColor": card_bg,
        "border": f"2px solid {border_color}",
        "borderRadius": "15px",
        "boxShadow": f"0 0 15px {neon_blue}",
        "padding": "25px",
        "marginBottom": "30px",
        "color": text_color,
        "fontFamily": "'Orbitron', sans-serif"
    },
    "list_item": {
        "marginBottom": "10px",
        "fontSize": "18px",
    },
    "tabs": {
        "backgroundColor": dark_bg,
        "borderBottom": f"2px solid {border_color}",
        "fontFamily": "'Orbitron', sans-serif",
        "color": text_color
    },
    "tab_style": {
        "color": neon_blue,
        "fontWeight": "bold",
        "border": "none",
        "padding": "10px 20px",
        "fontSize": "18px",
        "textShadow": "0 0 5px #00FFFF"
    },
    "tab_selected_style": {
        "color": "#39FF14",
        "backgroundColor": "#062A3E",
        "borderRadius": "10px 10px 0 0",
        "fontWeight": "bold",
        "textShadow": "0 0 10px #39FF14",
        "padding": "10px 20px",
        "fontSize": "18px"
    },
    "img_mascota": {
        "display": "block",
        "marginLeft": "auto",
        "marginRight": "auto",
        "width": "180px",
        "marginBottom": "15px",

    }
}

intro_tab = dbc.Container([
    # Imagen de la mascota
    html.Img(src="assets/imagenes/Cima-informaticos.png", style=styles["img_mascota"],
             alt="Mascota UABC"),

    html.Div([
        html.H2("🔋 Proyecto Final: Extracción de Datos de Autos Eléctricos", style=styles["header"]),
        html.P(
            "El mercado de autos eléctricos crece rápido y no siempre se tiene acceso a datos claros sobre precios, autonomía y carga.",
            style=styles["card"]),
        html.H4("🎯 Objetivo General", style={"color": neon_blue, "fontFamily": "'Orbitron', sans-serif"}),
        html.P("Crear una app en Python para recolectar, limpiar y visualizar datos de vehículos eléctricos en Europa.",
               style=styles["card"]),
        html.H4("❓ Preguntas a Responder", style={"color": neon_blue, "fontFamily": "'Orbitron', sans-serif"}),
        html.Ul([
            html.Li("💰 ¿Cuál es el rango de precios de autos eléctricos?", style=styles["list_item"]),
            html.Li("🔌 ¿Qué modelos tienen la mejor eficiencia energética?", style=styles["list_item"]),
            html.Li("⚡ ¿Qué autos ofrecen mejor carga rápida?", style=styles["list_item"]),
        ], style=styles["card"]),
        html.Hr(style={"borderColor": neon_blue}),
        html.P(
            "👥 Equipo: Cuevas Cortes Viridiana, Garnica Mendoza Jesús Alexis, Monge Núñez Jackeline, Saavedra Palacios Ana Fernanda, Sánchez Parra Camila.",
            style=styles["card"]),
        html.P("👨‍🏫 Profesor: Josué Miguel Flores Parra", style=styles["card"])
    ], style={"maxWidth": "900px", "margin": "auto"})
])

# (El resto de pestañas igual que antes...)

dashboard_tab = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                figure=px.box(df, y="Alemania (USD)",
                              title="💸 Rango de Precios de Autos Eléctricos",
                              template="plotly_dark",
                              color_discrete_sequence=[neon_blue])
            )
        ], md=6),
        dbc.Col([
            dcc.Graph(
                figure=px.scatter(df, x="Alemania (USD)", y="Eficiencia",
                                  title="⚡ Eficiencia vs Precio en Alemania",
                                  labels={"Alemania (USD)": "Precio (USD)", "Eficiencia": "Eficiencia"},
                                  template="plotly_dark",
                                  color_discrete_sequence=[neon_blue])
            )
        ], md=6)
    ], justify="center")
], style={"maxWidth": "1000px", "margin": "auto"})

conclusiones_tab = dbc.Container([
    html.Div([
        html.H2("🔹 Conclusiones", style=styles["header"]),
        html.P("Usamos Selenium y BeautifulSoup para extraer datos reales del mercado europeo.", style=styles["card"]),
        html.P("Visualizamos datos con Dash y trabajamos en equipo para responder preguntas clave.",
               style=styles["card"]),
        html.P("Reforzamos habilidades en programación, análisis de datos y colaboración.", style=styles["card"])
    ], style={"maxWidth": "900px", "margin": "auto"})
])

referencias_tab = dbc.Container([
    html.Div([
        html.H2("📄 Referencias y Repositorio GitHub", style=styles["header"]),
        html.Ul([
            html.Li(html.A("EV Database", href="https://ev-database.org", target="_blank",
                           style={"color": neon_blue, "textDecoration": "none"}), style=styles["list_item"]),
            html.Li(html.A("BeautifulSoup", href="https://www.crummy.com/software/BeautifulSoup/", target="_blank",
                           style={"color": neon_blue, "textDecoration": "none"}), style=styles["list_item"]),
            html.Li(html.A("Selenium", href="https://www.selenium.dev/", target="_blank",
                           style={"color": neon_blue, "textDecoration": "none"}), style=styles["list_item"]),
            html.Li(html.A("Pandas", href="https://pandas.pydata.org/", target="_blank",
                           style={"color": neon_blue, "textDecoration": "none"}), style=styles["list_item"]),
            html.Li(html.A("Matplotlib", href="https://matplotlib.org/", target="_blank",
                           style={"color": neon_blue, "textDecoration": "none"}), style=styles["list_item"]),
            html.Li(html.A("Repositorio GitHub",
                           href="https://github.com/CamilaSanchez-01/PF_Programacion_Extraccion_Datos", target="_blank",
                           style={"color": neon_blue, "textDecoration": "none"}), style=styles["list_item"]),
        ], style=styles["card"])
    ], style={"maxWidth": "900px", "margin": "auto"})
])

tabs = dbc.Tabs([
    dbc.Tab(intro_tab, label="🏠 Inicio", tab_style=styles["tab_style"],
            active_label_style=styles["tab_selected_style"]),
    dbc.Tab(dashboard_tab, label="📊 Visualización", tab_style=styles["tab_style"],
            active_label_style=styles["tab_selected_style"]),
    dbc.Tab(conclusiones_tab, label="🔐 Conclusiones", tab_style=styles["tab_style"],
            active_label_style=styles["tab_selected_style"]),
    dbc.Tab(referencias_tab, label="📖 Referencias", tab_style=styles["tab_style"],
            active_label_style=styles["tab_selected_style"]),
], style=styles["tabs"])

app.layout = dbc.Container([
    html.Link(href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap", rel="stylesheet"),
    html.H1("🚗 Dashboard Autos Eléctricos 🌍", style=styles["header"]),
    tabs
], fluid=True, style={"backgroundColor": dark_bg, "minHeight": "100vh", "paddingBottom": "50px"})

if __name__ == "__main__":
    app.run(debug=True)