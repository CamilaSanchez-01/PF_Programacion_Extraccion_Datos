from Base_programa import SitiosWeb


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def tienda1(self, paginas, busqueda):
    driver_path = ChromeDriverManager().install()
    s = Service(driver_path)
    opc = Options()
    opc.add_argument('--start-maximized')
    navegador = webdriver.Chrome(service=s, options=opc)
    navegador.get("https://ev-database.org/")  # Tienda 1
    time.sleep(5)

    productos = []

    # Faltaria funcion para imagenes

    for pagina in range(1, paginas + 1):
        soup = BeautifulSoup(navegador.page_source, "html.parser")
        items = soup.find_all("div", class_="list-item")

        for item in items[:2]:
            titulo = item.find("a", class_="title")
            if titulo:
                spans = titulo.find_all("span")
                Marca = spans[0].text.strip()
                Modelo = spans[1].text.strip()
                continue
            else:
                Marca = "No disponible"
                Modelo = "No diponible"
        Rango_Precio = item.find("span", class_="priceperrange_p")
        Rango_Precio = Rango_Precio.text.strip() if Rango_Precio else "No disponible"

        Volumen_carga = item.find("span", class_="cargo")
        Volumen_carga = Volumen_carga.text.strip() if Volumen_carga else "No disponible"

        Batería = item.find("span", class_="battery_p")
        Batería = Batería.text.strip() if Batería else "No disponible"

        Peso = item.find("span", class_="weight_p")
        Peso = Peso.text.strip() if Peso else "No disponible"

        Eficiencia = item.find("span", class_="efficiency")
        Eficiencia = Eficiencia.text.strip() if Eficiencia else "No disponible"

        Kilometraje = item.find("span", class_="a-text-bold")
        Kilometraje = Kilometraje.text.strip() if Kilometraje else "No disponible"

        productos.append(
            [Marca, Modelo, "No disponible", Rango_Precio, "No disponible", "No disponible", "No disponible",
             Volumen_carga, Batería, Peso, Eficiencia, Kilometraje, "https://ev-database.org/"])

    try:
        btnSiguiente = navegador.find_element(By.CSS_SELECTOR, "pagination-nav-nextlast")
        btnSiguiente.click()
        time.sleep(5)
    except:
        pass




