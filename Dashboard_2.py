import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, html, dcc

"""
El codigo extrae los valores numéricos y en la parte de eficiencia, comienza a limpiar los datos.
Diseñar, limpiar, filtrar datos
A su vez que diseña la pagina dashboard para mostrar los KPIs
"""
def clean_numeric(value):

    if pd.isna(value) or value == "No disponible":
        return None
    try:
        return float(''.join(filter(lambda x: x.isdigit() or x == '.', str(value))))
    except:
        return None


def eficiencia():
    try:
        df = pd.read_csv("Dataset/carros_limpio.csv")

        numeric_cols = {
            'Eficiencia': 'Eficiencia_num',
            'Peso': 'Peso_num',
            'Rango': 'Rango_num',
            'Bateria': 'Bateria_num',
            'Carga_Rapida': 'Carga_Rapida_num'
        }

        for col, new_col in numeric_cols.items():
            df[new_col] = df[col].apply(clean_numeric)

        df = df.dropna(subset=['Eficiencia_num', 'Peso_num'])

        marcas = sorted(df['Marca'].dropna().unique())

    except Exception as e:
        print(f"Error al cargar datos: {e}")
        marcas = []
        df = pd.DataFrame()


    return dbc.Container([
        html.H1("Análisis de Eficiencia Energética", className="text-center my-4"),


        dbc.Card([
            dbc.CardHeader("Filtros", className="bg-dark text-white"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Rango de Eficiencia (Wh/km):"),
                        dcc.RangeSlider(
                            id='eficiencia-slider',
                            min=100 if df.empty else int(df['Eficiencia_num'].min()),
                            max=250 if df.empty else int(df['Eficiencia_num'].max()),
                            step=5,
                            value=[100, 250] if df.empty else [
                                int(df['Eficiencia_num'].quantile(0.1)),
                                int(df['Eficiencia_num'].quantile(0.9))
                            ],
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ], md=8),
                    dbc.Col([
                        dbc.Label("Marca:"),
                        dcc.Dropdown(
                            id='marca-filter',
                            options=[{'label': marca, 'value': marca} for marca in marcas],
                            multi=True,
                            placeholder="Todas las marcas"
                        )
                    ], md=4)
                ])
            ])
        ], className="mb-4 shadow"),

        # KPIs
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Eficiencia Promedio", className="bg-primary text-white"),
                    dbc.CardBody([
                        html.H4(id='kpi-eficiencia-promedio', className="card-title"),
                        html.P("Wh/km", className="card-text")
                    ])
                ], className="h-100 shadow"),
                md=4
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Vehículo Más Eficiente", className="bg-success text-white"),
                    dbc.CardBody([
                        html.H4(id='kpi-modelo-eficiente', className="card-title"),
                        html.P(id='kpi-valor-eficiente', className="card-text")
                    ])
                ], className="h-100 shadow"),
                md=4
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Relación Peso-Eficiencia", className="bg-info text-white"),
                    dbc.CardBody([
                        html.H4(id='kpi-correlacion', className="card-title"),
                        html.P("Coeficiente de correlación", className="card-text")
                    ])
                ], className="h-100 shadow"),
                md=4
            )
        ], className="mb-4"),


        dbc.Row([
            dbc.Col(
                dcc.Graph(id='scatter-eficiencia-peso'),
                md=6
            ),
            dbc.Col(
                dcc.Graph(id='scatter-eficiencia-rango'),
                md=6
            )
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(
                dcc.Graph(id='histograma-eficiencia'),
                md=12
            )
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
def update_dashboard(eficiencia_range, marcas_seleccionadas):
    try:
        df = pd.read_csv("Dataset/carros_limpio.csv")

        df['Eficiencia_num'] = df['Eficiencia'].apply(clean_numeric)
        df['Peso_num'] = df['Peso'].apply(clean_numeric)
        df['Rango_num'] = df['Rango'].apply(clean_numeric)
        df['Bateria_num'] = df['Bateria'].apply(clean_numeric)

        mask = (df['Eficiencia_num'] >= eficiencia_range[0]) & (df['Eficiencia_num'] <= eficiencia_range[1])

        if marcas_seleccionadas:
            mask &= df['Marca'].isin(marcas_seleccionadas)

        df_filtered = df[mask].copy()

        if df_filtered.empty:
            raise ValueError("No hay datos con los filtros seleccionados")

        eficiencia_promedio = f"{df_filtered['Eficiencia_num'].mean():.1f}"

        idx_min = df_filtered['Eficiencia_num'].idxmin()
        modelo_eficiente = f"{df_filtered.loc[idx_min, 'Marca']} {df_filtered.loc[idx_min, 'Modelo']}"
        valor_eficiente = f"{df_filtered.loc[idx_min, 'Eficiencia_num']:.1f} Wh/km"

        correlacion = f"{df_filtered['Eficiencia_num'].corr(df_filtered['Peso_num']):.2f}"

        fig_scatter_peso = px.scatter(
            df_filtered,
            x='Peso_num',
            y='Eficiencia_num',
            color='Marca',
            hover_name='Modelo',
            hover_data=['Rango', 'Bateria'],
            labels={
                'Peso_num': 'Peso (kg)',
                'Eficiencia_num': 'Eficiencia (Wh/km)'
            },
            title='Relación Peso vs Eficiencia'
        )

        fig_scatter_rango = px.scatter(
            df_filtered,
            x='Rango_num',
            y='Eficiencia_num',
            color='Marca',
            size='Bateria_num',
            hover_name='Modelo',
            labels={
                'Rango_num': 'Rango (km)',
                'Eficiencia_num': 'Eficiencia (Wh/km)',
                'Bateria_num': 'Capacidad Batería (kWh)'
            },
            title='Relación Rango vs Eficiencia'
        )

        fig_hist = px.histogram(
            df_filtered,
            x='Eficiencia_num',
            nbins=15,
            color='Marca',
            labels={'Eficiencia_num': 'Eficiencia (Wh/km)'},
            title='Distribución de Eficiencia Energética'
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
        return (
            "N/A", "N/A", "N/A", "N/A",
            empty_fig, empty_fig, empty_fig
        )