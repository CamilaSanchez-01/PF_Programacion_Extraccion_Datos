import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, Dash
from Dashboard_1 import carga_rapida
from Dashboard_2 import eficiencia
from Dashboard_3 import distribucion_precios

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)

# Colores para un look azul neón, moderno y techie
colors = {
    "background": "#0A0F24",
    "primary": "#00BFFF",
    "secondary": "#1E90FF",
    "accent": "#8A2BE2",
    "text_light": "#F0F8FF",
    "card_bg": "#11182F",
    "shadow": "0 0 18px #00BFFF"
}

# Aquí están los estilos que vamos a usar en toda la app para que todo se vea chévere y consistente
styles = {
    "header": {
        "fontFamily": "'Orbitron', sans-serif",
        "color": colors["primary"],
        "fontSize": "3rem",
        "textAlign": "center",
        "marginBottom": "1rem",
        "textShadow": "0 0 20px #00BFFF",
        "letterSpacing": "2px"
    },
    "subheader": {
        "color": colors["secondary"],
        "fontSize": "1.8rem",
        "fontWeight": "bold",
        "textAlign": "center",
        "marginBottom": "2rem",
        "textShadow": "0 0 12px #1E90FF"
    },
    "card": {
        "backgroundColor": colors["card_bg"],
        "borderRadius": "15px",
        "boxShadow": colors["shadow"],
        "padding": "30px",
        "marginBottom": "2rem",
        "color": colors["text_light"],
        "fontSize": "1.2rem",
        "lineHeight": "1.6rem",
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    },
    "list_item": {
        "marginBottom": "12px",
        "fontSize": "1.1rem",
        "paddingLeft": "1rem",
        "textIndent": "-1rem",
        "color": colors["primary"],
        "fontWeight": "600"
    },
    "sidebar": {
        "backgroundColor": "#09132D",
        "width": "18rem",
        "height": "100vh",
        "position": "fixed",
        "top": 0,
        "left": 0,
        "padding": "2rem 1rem",
        "boxShadow": f"2px 0 10px {colors['primary']}",
        "fontFamily": "'Orbitron', sans-serif"
    },
    "sidebar_title": {
        "color": colors["primary"],
        "fontSize": "2.8rem",
        "textAlign": "center",
        "marginBottom": "2rem",
        "textShadow": "0 0 15px #00BFFF"
    },
    "nav_link": {
        "fontSize": "1.3rem",
        "padding": "12px 15px",
        "color": colors["text_light"],
        "borderRadius": "8px",
        "marginBottom": "8px",
        "transition": "all 0.3s ease"
    },
    "content": {
        "marginLeft": "20rem",
        "marginRight": "2rem",
        "padding": "3rem 2rem",
        "minHeight": "100vh",
        "background": f"linear-gradient(135deg, {colors['background']} 0%, #0D1A3A 100%)",
        "color": colors["text_light"],
        "fontFamily": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "overflowY": "auto"
    },
    "image": {  # Imagen tipo banner con estilo para que se vea cool
        "width": "100%",
        "height": "250px",
        "objectFit": "cover",
        "borderRadius": "15px",
        "boxShadow": "0 0 25px #00BFFF",
        "marginBottom": "2rem",
        "cursor": "pointer"
    },
    "logo_pequeño": {  # Logo pequeño para el sidebar, que se vea limpio y con estilo
        "width": "200px",
        "height": "200px",
        "margin": "0 auto 1rem auto",
        "display": "block",
        "borderRadius": "50%",
        "boxShadow": "0 0 12px #00BFFF"
    }
}

home_tab = html.Div([
    html.Img(
        src="assets/imagenes/carro.png",
        style=styles["image"],
        alt="Carro Eléctrico Futurista",
        id="hero-image",
        n_clicks=0
    ),
    html.H1("Proyecto Final: Explorando Datos de Autos Eléctricos", style=styles["header"]),
    html.H3("Impulsando la movilidad sostenible con datos reales", style=styles["subheader"]),
    html.Div([
        html.Div("Hoy en día, los autos eléctricos son el futuro, y tener buena data nos ayuda a entender mejor precios, eficiencia y carga rápida.", style=styles["card"]),
        html.H4("Qué buscamos", style={"color": colors["primary"], "fontWeight": "700", "marginBottom": "1rem"}),
        html.Ul([
            html.Li("Juntar datos frescos y detallados del mercado europeo de autos eléctricos.", style=styles["list_item"]),
            html.Li("Mostrar cómo es la eficiencia energética y las opciones de carga rápida.", style=styles["list_item"]),
            html.Li("Ayudar a compradores y fabricantes a tomar mejores decisiones.", style=styles["list_item"])
        ]),
        html.Hr(style={"borderColor": colors["primary"], "marginTop": "2rem", "marginBottom": "2rem"}),
        html.P("Equipo: Cuevas Cortes Viridiana, Garnica Mendoza Jesús Alexis, Monge Núñez Jackeline, Saavedra Palacios Ana Fernanda, Sánchez Parra Camila.", style=styles["card"]),
        html.P("Profesor: Josué Miguel Flores Parra", style=styles["card"]),
    ], style={"maxWidth": "850px", "margin": "auto"})
])

tabs_content = {
    "/": home_tab,
    "/dash1": carga_rapida(),
    "/dash2": eficiencia(),
    "/dash3": distribucion_precios(),
    "/conclusiones": html.Div([
        html.H2("Conclusiones Clave", style=styles["header"]),
        html.Div([
            html.P("• Usamos Selenium y BeautifulSoup para agarrar datos reales del mercado europeo.", style=styles["card"]),
            html.P("• Los dashboards muestran precios, eficiencia y carga rápida de varios modelos.", style=styles["card"]),
            html.P("• Aprendimos a programar, analizar datos y a trabajar en equipo.", style=styles["card"])
        ], style={"maxWidth": "850px", "margin": "auto"})
    ]),
    "/referencias": html.Div([
        html.H2("Referencias y Repositorio GitHub", style=styles["header"]),
        html.Ul([
            html.Li(html.A("EV Database", href="https://ev-database.org", target="_blank", style={"color": colors["primary"]}), style=styles["list_item"]),
            html.Li(html.A("BeautifulSoup", href="https://www.crummy.com/software/BeautifulSoup/", target="_blank", style={"color": colors["primary"]}), style=styles["list_item"]),
            html.Li(html.A("Selenium", href="https://www.selenium.dev/", target="_blank", style={"color": colors["primary"]}), style=styles["list_item"]),
            html.Li(html.A("Pandas", href="https://pandas.pydata.org/", target="_blank", style={"color": colors["primary"]}), style=styles["list_item"]),
            html.Li(html.A("GitHub Repo", href="https://github.com/CamilaSanchez-01/PF_Programacion_Extraccion_Datos", target="_blank", style={"color": colors["primary"]}), style=styles["list_item"])
        ], style=styles["card"])
    ], style={"maxWidth": "850px", "margin": "auto"})
}

sidebar = html.Div([
    html.Img(src="assets/imagenes/Cima-informaticos.png", style=styles["logo_pequeño"]),
    html.H1("⚡ EV Data", style=styles["sidebar_title"]),
    dbc.Nav([
        dbc.NavLink("Inicio 🏠", href="/", active="exact", style=styles["nav_link"]),
        dbc.NavLink("Carga Rápida ⚡", href="/dash1", active="exact", style=styles["nav_link"]),
        dbc.NavLink("Eficiencia 🔋", href="/dash2", active="exact", style=styles["nav_link"]),
        dbc.NavLink("Precios 💸", href="/dash3", active="exact", style=styles["nav_link"]),
        dbc.NavLink("Conclusiones 🔐", href="/conclusiones", active="exact", style=styles["nav_link"]),
        dbc.NavLink("Referencias 📖", href="/referencias", active="exact", style=styles["nav_link"])
    ], vertical=True, pills=True)
], style=styles["sidebar"])

content = html.Div(id="page-content", style=styles["content"])

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
], style={"backgroundColor": colors["background"], "minHeight": "100vh"})

@callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    return tabs_content.get(pathname, html.Div([
        html.H1("404: Página no encontrada", style={"color": "red", "textAlign": "center", "marginTop": "3rem"}),
        html.P(f"Oops, la ruta '{pathname}' no existe.", style=styles["card"])
    ]))

@callback(
    Output("hero-image", "style"),
    Input("hero-image", "n_clicks")
)
def zoom_image(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        new_style = styles["image"].copy()
        new_style["transform"] = "scale(1.15)"
        new_style["boxShadow"] = "0 0 25px #00BFFF"
        return new_style
    return styles["image"]

def dashboard_estructura():
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=True)
