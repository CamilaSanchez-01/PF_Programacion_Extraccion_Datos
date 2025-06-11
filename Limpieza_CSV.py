import pandas as pd
from Web_Scrapping_Link1 import tienda1

def limpieza1():
    try:
        # Cargar el archivo CSV
        df = pd.read_csv("Dataset/carros.csv", sep=",")
    except FileNotFoundError:
        print("❌ Error: El archivo 'carros.csv' no se encontró.")
        return None
    except Exception as e:
        print(f"❌ Error al cargar el archivo: {e}")
        return None

    # Reemplazar valores vacíos, nulos o solo espacios
    df.replace(["", " ", None], "No disponible", inplace=True)
    df.fillna("No disponible", inplace=True)

    # Columnas de precio y ajuste del tipo de cambio
    columnas_precio = ["Alemania (€)", "Países Bajos (€)", "Reino Unido (£)"]
    tasa_euro_usd = 1.08
    tasa_gbp_usd = 1.27
    columnas_usd = []

    for columna in columnas_precio:
        if columna in df.columns:
            col_usd = columna.replace("€", "USD").replace("£", "USD")
            df[columna + "_num"] = df[columna].str.replace("€", "", regex=False) \
                                               .str.replace("£", "", regex=False) \
                                               .str.replace(".", "", regex=False) \
                                               .str.replace(",", "") \
                                               .str.strip()
            df[columna + "_num"] = pd.to_numeric(df[columna + "_num"], errors="coerce")
            tasa = tasa_euro_usd if "€" in columna else tasa_gbp_usd
            df[col_usd] = (df[columna + "_num"] * tasa).round(2)
            df[col_usd] = df[col_usd].fillna("No disponible")
            columnas_usd.append(col_usd)
            df.drop([columna, columna + "_num"], axis=1, inplace=True)
        else:
            print(f"⚠️ Columna '{columna}' no encontrada en el archivo CSV.")

    # Renombrar columnas
    df.rename(columns={
        "Rango": "Rango(Km)",
        "Eficiencia": "Eficiencia(Wh/km)",
        "Bateria": "Bateria(kWh)",
        "Peso": "Peso(kg)"
    }, inplace=True)

    # Limpieza y conversión de valores numéricos
    for col, unidad in [
        ("Rango(Km)", "km"),
        ("Eficiencia(Wh/km)", "Wh/km"),
        ("Bateria(kWh)", "kWh"),
        ("Peso(kg)", "kg")
    ]:
        if col in df.columns:
            df[col] = df[col].str.replace(unidad, "", regex=False).str.strip()
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Eliminar filas con nulos críticos
    df.dropna(subset=["Rango(Km)", "Bateria(kWh)", "Eficiencia(Wh/km)"], inplace=True)

    # Validación de rango lógico
    df = df[df["Rango(Km)"] <= 1500]
    df = df[df["Bateria(kWh)"] <= 200]
    df = df[df["Eficiencia(Wh/km)"] <= 300]

    # Eliminar duplicados
    df.drop_duplicates(subset=["Marca", "Modelo"], keep="first", inplace=True)

    # Validar si existen las columnas antes de reordenar
    columnas_orden = [
        "Marca", "Modelo",
        "Alemania (USD)", "Países Bajos (USD)", "Reino Unido (USD)",
        "Precio_Rango", "Rango(Km)", "Bateria(kWh)", "Eficiencia(Wh/km)",
        "Peso(kg)", "Remolque", "Carga_Rapida", "Carga_Vol", "Rango_1_parada",
        "Traccion_trasera", "Traccion_delantera", "Segmento_mercado",
        "Clasificacion_seguridad", "Numero_asientos", "Bomba_calor",
        "Carga_bidireccional", "Imagen_tag", "Sitio"
    ]

    columnas_existentes = [col for col in columnas_orden if col in df.columns]
    df = df[columnas_existentes]

    # Guardar archivo limpio
    df.to_csv("Dataset/carros_limpio.csv", index=False, encoding="utf-8-sig")

    # Reportes finales
    print("✅ Limpieza completada.")
    print("🔍 Primeras filas:")
    print(df.head())
    print("\n🔎 Tipos de datos:")
    print(df.dtypes)
    print("\n🚨 Nulos por columna:")
    print(df.isna().sum())

    return df
