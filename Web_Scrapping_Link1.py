from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def tienda1(paginas):
    driver_path = ChromeDriverManager().install()
    s = Service(driver_path)
    opc = Options()
    opc.add_argument('--start-maximized')
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get("https://ev-database.org/")  # Tienda 1
    time.sleep(5)

    productos = []

    for pagina in range(1, paginas + 1):
        soup = BeautifulSoup(navegador.page_source, "html.parser")
        items = soup.find_all("div", class_="list-item")

        for item in items[:10]:
            titulo = item.find("a", class_="title")
            if titulo:
                spans = titulo.find_all("span")
                marca = spans[0].text.strip()
                modelo = spans[1].text.strip()
                Marca = marca
                Modelo = modelo
            else:
                Marca = "No disponible"
                Modelo = "No diponible"

            #Precio = item.find("div", class_="price_buy archive", style="vertical-align: inherit; )#cambie este VC

            # Obtener todos los divs de clase 'price_buy archive'
            precios_divs = item.find_all("div", class_="price_buy archive")

            # Diccionario para guardar los precios por país
            precios_por_pais = {
                "Alemania (€)": "No disponible",
                "Países Bajos (€)": "No disponible",
                "Reino Unido (£)": "No disponible"
            }

            # Recorrer todos los divs de precio por país
            for div in precios_divs:
                if div.find("span", class_="country_de"):
                    precio = div.find("span", class_="country_de").text.strip()
                    precios_por_pais["Alemania (€)"] = precio
                elif div.find("span", class_="country_nl"):
                    precio = div.find("span", class_="country_nl").text.strip()
                    precios_por_pais["Países Bajos (€)"] = precio
                elif div.find("span", class_="country_uk"):
                    precio = div.find("span", class_="country_uk").text.strip()
                    precios_por_pais["Reino Unido (£)"] = precio


            Precio_Rango = item.find("span", class_="priceperrange hidden") # En Euro (aleman)/ Km
            Precio_Rango = Precio_Rango.text.strip() if Precio_Rango else "No disponible"

            Rango = item.find("span", class_="erange_real")
            Rango = Rango.text.strip() if Rango else "No disponible"

            Bateria = item.find("span", class_="battery_p")
            Bateria = Bateria.text.strip() if Bateria else "No disponible"

            Eficiencia = item.find("span", class_="efficiency")
            Eficiencia = Eficiencia.text.strip() if Eficiencia else "No disponible"

            Peso = item.find("span", class_="weight_p")
            Peso = Peso.text.strip() if Peso else "No disponible"

            Remolque = item.find("span", class_="towweight hidden") # En kilos
            Remolque = Remolque.text.strip() if Remolque else "No disponible"

            Carga_Rapida = item.find("span", class_="fastcharge_speed hidden") # En kw
            Carga_Rapida = Carga_Rapida.text.strip() if Carga_Rapida else "No disponible"

            Carga_Vol = item.find("span", class_="cargosort hidden") # En L
            Carga_Vol = Carga_Vol.text.strip() if Carga_Vol else "No disponible"

            Rango_1_parada = item.find("span", class_="long_distance_total_sort hidden") # En Km
            Rango_1_parada = Rango_1_parada.text.strip() if Rango_1_parada else "No disponible"

            Traccion_trasera = item.find("span", class_="achter far fa-circle", style="margin-right: -3px;") # Es una figura, revisar
            Traccion_trasera = Traccion_trasera.text.strip() if Traccion_trasera else "No disponible"

            Traccion_delantera = item.find("span", class_="achter fas fa-circle")
            Traccion_delantera = Traccion_delantera.text.strip() if Traccion_delantera else "No disponible"

            Segmento_mercado = item.find("span", class_="size-d", style="vertical-align: inherit;")
            Segmento_mercado = Segmento_mercado.text.strip() if Segmento_mercado else "No disponible"

            Clasificacion_seguridad = item.find("span", class_="safety hidden")
            Clasificacion_seguridad = Clasificacion_seguridad.text.strip() if Clasificacion_seguridad else "No disponible"

            Numero_asientos = item.find("span", class_="seats-5 fas fa-user", style="vertical-align: inherit;")
            Numero_asientos = Numero_asientos.text.strip() if Numero_asientos else "No disponible"

            Bomba_calor = item.find("span", class_="heatpump hidden")
            Bomba_calor = Bomba_calor.text.strip() if Bomba_calor else "No disponible"

            Carga_bidireccional = item.find("span", {"data-tooltip": True, "class": "icons-row-2"})
            Carga_bidireccional = Carga_bidireccional.text.strip() if Carga_bidireccional else "No disponible"

            # Funcion de imagen
            imagen_tag = item.find("img", {"src": True})
            if imagen_tag:
                imagen_srl = imagen_tag["src"]
                imagen_Url = f"https://ev-database.org/{imagen_srl}"
            else:
                imagen_Url = "No disponible"

            productos.append([
                Marca, Modelo,
                precios_por_pais["Alemania (€)"],
                precios_por_pais["Países Bajos (€)"],
                precios_por_pais["Reino Unido (£)"],
                Precio_Rango, Rango, Bateria, Eficiencia, Peso,
                Remolque, Carga_Rapida, Carga_Vol, Rango_1_parada,
                Traccion_trasera, Traccion_delantera, Segmento_mercado,
                Clasificacion_seguridad, Numero_asientos, Bomba_calor,
                Carga_bidireccional, imagen_Url, "https://ev-database.org/"
            ])

        try:
            btnSiguiente = navegador.find_element(By.CSS_SELECTOR, ".pagination-nav-nextlast")
            btnSiguiente.click()
            time.sleep(5)
        except:
            break

    navegador.quit()
    return productos



