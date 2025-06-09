import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, Dash
from Dashboard_1 import carga_rapida
from Dashboard_2 import eficiencia
from Dashboard_3 import distribucion_precios


app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Dashboard Autos Eléctricos"

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
        [
            html.H2("EV", className="display-4"),
            html.Hr(),
            html.P("Objetivo: Mostrar datos", className="lead"),
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Dashboard 1", href="/dash1", active="exact"),
                    dbc.NavLink("Dashboard 2", href="/dash2", active="exact"),
                    dbc.NavLink("Dashboard 3", href="/dash3", active="exact"),
                    dbc.NavLink("GitHub", href="https://github.com/CamilaSanchez-01/PF_Programacion_Extraccion_Datos",
                                active="exact", target="_blank"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="SIDEBAR_STYLE",
    )

content = html.Div(id="page-content", className="CONTENT_STYLE")

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@callback(Output("page-content", "children"),
              [Input("url", "pathname")])

def dashboard_estructura(pathname):
    if pathname == "/":
        return eficiencia()
    elif pathname == "/dash1":
        return distribucion_precios()
    elif pathname == "/dash2":
        return eficiencia()
    elif pathname == "/dash3":
        return carga_rapida()
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__ == "__main__":
    app.layout = html.Div([dcc.Location(id="url"), sidebar, content])
    app.run(debug=True)


