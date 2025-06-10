import pandas as pd
from Web_Scrapping_Link1 import tienda1

def limpieza1():
    # Cargar el archivo CSV
    df = pd.read_csv("Dataset/carros.csv", sep=",")

    # 1. Reemplazar celdas vacías, espacios o valores nulos por "No disponible"
    df.replace(["", " ", None], "No disponible", inplace=True)

    # 2. Configurar columnas de precios por país
    columnas_precio = ["Alemania (€)", "Países Bajos (€)", "Reino Unido (£)"]
    tasa_euro_usd = 1.08
    tasa_gbp_usd = 1.27
    columnas_usd = []

    for columna in columnas_precio:
        if columna in df.columns:
            col_usd = columna.replace("€", "USD").replace("£", "USD")

            df[columna + "_num"] = df[columna].str.replace("€", "", regex=False)\
                                              .str.replace("£", "", regex=False)\
                                              .str.replace(".", "", regex=False)\
                                              .str.replace(",", "")\
                                              .str.strip()
            df[columna + "_num"] = pd.to_numeric(df[columna + "_num"], errors="coerce")

            tasa = tasa_euro_usd if "€" in columna else tasa_gbp_usd
            df[col_usd] = (df[columna + "_num"] * tasa).round(2)
            df[col_usd] = df[col_usd].fillna("No disponible")
            columnas_usd.append(col_usd)

            df.drop([columna, columna + "_num"], axis=1, inplace=True)
        else:
            print(f"Columna '{columna}' no encontrada en el archivo CSV.")
            
#Renombre de columnas y tipos de datos por problemas de formato
    df.rename(columns={
        "Rango": "Rango(Km)",
        "Eficiencia": "Eficiencia(Wh/km)",
        "Bateria": "Bateria(kWh)",
        "Peso": "Peso(kg)"
    }, inplace=True)

    df["Rango(Km)"] = df["Rango(Km)"].str.replace("km", "", regex=False)
    df["Rango(Km)"] = pd.to_numeric(df["Rango(Km)"], errors="coerce")

    df["Eficiencia(Wh/km)"] = df["Eficiencia(Wh/km)"].str.replace("Wh/km", "", regex=False)
    df["Eficiencia(Wh/km)"] = pd.to_numeric(df["Eficiencia(Wh/km)"], errors="coerce")

    df["Bateria(kWh)"] = df["Bateria(kWh)"].str.replace("kWh", "", regex=False)
    df["Bateria(kWh)"] = pd.to_numeric(df["Bateria(kWh)"], errors="coerce")

    df["Peso(kg)"] = df["Peso(kg)"].str.replace("kg", "", regex=False)
    df["Peso(kg)"] = pd.to_numeric(df["Peso(kg)"], errors="coerce")

    # 3. Reordenar columnas
    columnas_orden = [
        "Marca", "Modelo",
        "Alemania (USD)", "Países Bajos (USD)", "Reino Unido (USD)",
        "Precio_Rango", "Rango(Km)", "Bateria(kWh)", "Eficiencia(Wh/km)",
        "Peso(kg)", "Remolque", "Carga_Rapida", "Carga_Vol", "Rango_1_parada",
        "Traccion_trasera", "Traccion_delantera", "Segmento_mercado",
        "Clasificacion_seguridad", "Numero_asientos", "Bomba_calor",
        "Carga_bidireccional", "Imagen_tag", "Sitio"
    ]

    df = df[columnas_orden]

    # 4. Guardar el archivo limpio
    df.to_csv("Dataset/carros_limpio.csv", index=False)

    print("Limpieza completada - Archivo limpio guardado:")
    print(df.head())

    return df
