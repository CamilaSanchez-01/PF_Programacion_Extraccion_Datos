import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, html, dcc

def carga_rapida():
    df = pd.read_csv("Dataset/carros_limpio.csv")
    df["Bateria"] = df["Bateria"].str.replace("kWh","",regex=False).astype(float)

    body = dbc.Container([
        html.H2("Carga Rápida 🔌 "),
        dbc.Card([
            dbc.CardHeader("Filtro"),
            dbc.CardBody([
                dbc.Label("Marca: ", style={"color": "white"}),
                dcc.Dropdown(options=[{"label": m, "value": m} for m in sorted(df["Marca"].dropna().unique())],
                             value=None, id= "ddMarca", style={"backgroundColor": "#111", "color":"#515c63"})
            ])
        ], className="md-7", style={"backgroundColor": "#1a1a1a"}),
        dbc.Row([
            html.Img(src="assets/imagenes/carrot.png", style={"width": "160px", "height": "140px"}),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🚘 Promedio de Carga Rápida (kw)", className="card-title"),
                        html.H4(id="kpi-carga",className="card-text")
                    ])
                ],color = "primary",inverse=True)
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6(" 🚙 Auto con Mayor Carga rápida", className="card-title"),
                        html.H4(id="kpi-auto", className="card-text")
                    ])
                ], color="success", inverse=True)
            ]),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🚗 Promedio de Bateria (kwh)", className="card-title"),
                        html.H4(id="kpi-bateria", className="card-text")
                    ])
                ], color="info", inverse=True)
        ])
    ]),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id= "barras-mayor", style={"height": "400px"}),md = 6
            ),
            dbc.Col(
                dcc.Graph(id="barras-menor", style={"height": "400px"}), md=6
            ),
            dbc.Col(
                dcc.Graph(id="barras-rendi", style={"height": "400px"}), md=6
            ),
            dbc.Col(
                dcc.Graph(id="barras-carga", style={"height": "400px"}), md=6
            )

        ])
    ])
    return body

@callback(
    Output("kpi-carga","children"),
    Output("kpi-bateria","children"),
    Output("kpi-auto","children"),
    Output("barras-mayor","figure"),
    Output("barras-menor","figure"),
    Output("barras-rendi","figure"),
    Output("barras-carga","figure"),
    Input("ddMarca","value")

)
def figuras(Marca):
    df = pd.read_csv("Dataset/carros_limpio.csv")

    df["Bateria"] = df["Bateria"].str.replace("kWh","",regex=False).astype(float)
    if Marca:
        df_marca = df[df.Marca == Marca]
    else:
        df_marca = df

    kpi_carga = f"{df_marca['Carga_Rapida'].mean():2f} KW"
    kpi_bateria = f"{df_marca['Bateria'].mean():2f} KW"
    kpi_auto = df_marca.sort_values(by = "Carga_Rapida",ascending=False).iloc[0]["Modelo"]
    top_mayor  = df_marca.sort_values(by="Carga_Rapida", ascending=False).head(5)
    top_menor = df_marca.sort_values(by="Carga_Rapida", ascending=False).tail(5)


    fig_mayor = px.bar(top_mayor, x= "Modelo", y= "Carga_Rapida", color="Modelo",title="🔋 Top 5 Autos con Mayor Capacidad de Carga (KW)",
                       template="plotly_dark", hover_name="Marca", color_discrete_sequence= ["#E0E0E0", "#1A3C64", "#2E7D32", "#F5F5F5", "#FBC02D"])

    fig_mayor.update_layout(xaxis = dict( showticklabels=False))

    fig_menor  = px.bar(top_menor, x="Modelo", y="Carga_Rapida", color="Modelo",
                       title="🔋 Top 5 Autos con Menor Capacidad de Carga (KW)",
                       template="plotly_dark", hover_name="Marca",
                       color_discrete_sequence=["#FBC02D", "#2E7D32", "#E0E0E0", "#1A3C64", "#F5F5F5"])

    fig_menor.update_layout(xaxis=dict(showticklabels=False))

    fig_rendi = px.scatter(df_marca, x= "Carga_Vol", y= "Bateria", color= "Carga_Rapida",template="plotly_dark",title="🗺️🌍Mapa de Rendimiento en Carga Rápida",
                           hover_name="Modelo",size="Carga_Rapida",labels={"Carga_Vol": "Tamaño total de carga  (Kwh)"})


    fig_carga  = px.scatter(df_marca, x="Rango_1_parada", y="Modelo", color="Marca", template="plotly_dark",
                           title="🚏 Modelos con mejor rendimiento por carga parcial",
                           labels={"Rango_1_parada": "Rendimiento por parada (km)"})

    return kpi_carga,kpi_bateria,kpi_auto,fig_mayor,fig_menor,fig_rendi,fig_carga




