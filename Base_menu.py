import tkinter as tk
from tkinter import messagebox
import os
import pandas as pd
import subprocess
import sys
import subprocess
import sys
import webbrowser
import time
from Web_Scrapping_Link1 import tienda1
from Limpieza_CSV import limpieza1
from Dashboards_base import dashboard_estructura
from mysql.connector import connect, Error
from PIL import Image, ImageTk

# Paleta de colores y estilos con tema neón azul para darle un toque moderno
colors = {
    "background": "#0A0F24",
    "primary": "#00BFFF",
    "secondary": "#1E90FF",
    "accent": "#8A2BE2",
    "text_light": "#F0F8FF",
    "highlight": "#FF10F0",
    "card_bg": "#11182F"
}

styles = {
    "title": ("Orbitron", 35, "bold"),
    "menu_button": ("Cascadia Code", 12, "bold"),
    "menu_items": ("Cascadia Code", 11),
    "label": ("Segoe UI", 12),
    "text_color": colors["primary"],
    "menu_bg": colors["card_bg"],
    "menu_fg": colors["text_light"]
}

class SitiosWeb:
    # Clase principal que controla la interfaz gráfica y las funcionalidades de la app
    def __init__(self, master):
        self.master = master
        self.master.title("WebScraping Neón")
        self.master.geometry("500x500")
        self.master.configure(bg=colors["background"])

        # Aquí se carga y prepara un GIF animado para usarlo como fondo animado
        gif_p = "assets/imagenes/carro.gif"
        self.frames = []
        gif = Image.open(gif_p)
        try:
            while True:
                frame = ImageTk.PhotoImage(gif.copy().convert("RGBA"))
                self.frames.append(frame)
                gif.seek(len(self.frames))
        except:
            pass

        self.frame_index = 0
        self.label_fondo = tk.Label(self.master)
        self.label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        self.animar_gif()

        # Título principal con un efecto de brillo que cambia colores para simular neón
        self.labelNombre = tk.Label(self.master, text="WebScraping", fg="white", bg=colors["highlight"],
                                    font=styles["title"], relief="flat")
        self.labelNombre.pack(pady=20)

        # Función interna para alternar el color del texto y dar efecto de brillo
        def brillo():
            current_color = self.labelNombre.cget("fg")
            new_color = colors["highlight"] if current_color == "white" else "white"
            self.labelNombre.config(fg=new_color)
            root.after(700, brillo)

        brillo()

        # Botón tipo menú que despliega opciones para ejecutar distintas funciones
        self.menucontrol = tk.Menubutton(master, text="⚙ Opciones",
                                         pady=10, padx=12, bg=colors["card_bg"], fg=colors["primary"],
                                         font=styles["menu_button"], relief="raised")
        self.menucontrol.place(x=20, y=110)

        # Opciones dentro del menú, cada una llama a un método para su función respectiva
        self.menuOpciones = tk.Menu(self.menucontrol, tearoff=0,
                                    fg=colors["text_light"], bg=colors["secondary"],
                                    font=styles["menu_items"])

        self.menuOpciones.add_command(label="Iniciar Web Scraping", command=self.buscar_tienda1)
        self.menuOpciones.add_command(label="Conexión con SQL", command=self.opc_conexion_sql)
        self.menuOpciones.add_command(label="Guardar Datos en CSV", command=self.opc_guardar_csv)
        self.menuOpciones.add_command(label="Limpiar Datos", command=self.opc_limpiar_datos)
        self.menuOpciones.add_command(label="Ver Dashboard", command=self.opc_ver_dashboard)
        self.menuOpciones.add_separator()
        self.menuOpciones.add_command(label="Salir", command=master.destroy)
        self.menucontrol["menu"] = self.menuOpciones

        # Método que controla qué pasa si el usuario intenta cerrar la ventana
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Pregunta de confirmación para salir de la aplicación
        if messagebox.askokcancel("Salir", "¿Seguro que quieres salir?"):
            self.master.destroy()

    def guardar_csv(self, productos):
        # Guarda los productos extraídos en un archivo CSV dentro de la carpeta Dataset
        if not os.path.exists("Dataset"):
            os.makedirs("Dataset")
        df = pd.DataFrame(productos, columns=[
            "Marca", "Modelo", "Alemania (€)", "Países Bajos (€)", "Reino Unido (£)",
            "Precio_Rango", "Rango", "Bateria", "Eficiencia", "Peso", "Remolque", "Carga_Rapida",
            "Carga_Vol", "Rango_1_parada", "Traccion_trasera", "Traccion_delantera",
            "Segmento_mercado", "Clasificacion_seguridad", "Numero_asientos", "Bomba_calor",
            "Carga_bidireccional", "Imagen_tag", "Sitio"
        ])
        # El modo 'a' agrega datos si ya existe el archivo, si no lo crea
        df.to_csv("Dataset/carros.csv", index=False, mode='a',
                  header=not os.path.exists("Dataset/carros.csv"))

    def buscar_tienda1(self):
        # Función para iniciar el scraping en la primera tienda y guardar los resultados
        try:
            messagebox.showinfo("Buscando", "Buscando en tienda...")
            productos = tienda1(1)
            if productos:
                self.guardar_csv(productos)
                messagebox.showinfo("Éxito", "Datos guardados correctamente")
            else:
                messagebox.showwarning("Sin resultados", "No se encontraron productos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al hacer scraping:\n{str(e)}")

    def opc_conexion_sql(self):
        # Intenta conectar con la base de datos MySQL y muestra mensaje de éxito o error
        try:
            dbConexion = connect(
                host="localhost",
                user="root",
                password="123456789",
                database="ev_db"
            )
            messagebox.showinfo("Conexión", "¡Conexión exitosa con SQL!")
            return dbConexion
        except Error as e:
            messagebox.showerror("Error SQL", str(e))
            return False

    def opc_guardar_csv(self):
        # Mensaje informativo de que los datos ya se encuentran guardados en CSV
        messagebox.showinfo("Info", "Datos ya guardados en el CSV.")

    def opc_limpiar_datos(self):
        # Llama al script que limpia los datos para dejarlos listos para análisis
        try:
            limpieza1()
            messagebox.showinfo("Limpieza", "Datos limpiados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al limpiar los datos:\n{str(e)}")

    def opc_ver_dashboard(self):
        # Ejecuta el dashboard desarrollado en Dash y abre la URL local en el navegador
        try:
            # Ejecutar el dashboard
            subprocess.Popen([sys.executable, "Dashboards_base.py"])

            # Esperar un momento para que el servidor se inicie
            time.sleep(2)

            # Abrir el navegador en la URL
            webbrowser.open("http://127.0.0.1:8050/")
        except Exception as e:
            messagebox.showerror("Dashboard", f"Ocurrió un error:\n{str(e)}")

    def animar_gif(self):
        # Animar el GIF de fondo cambiando el frame cada 100 ms
        self.label_fondo.config(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.master.after(100, self.animar_gif)

if __name__ == "__main__":
    # Se inicia la ventana principal y se corre la aplicación
    root = tk.Tk()
    app = SitiosWeb(root)
    root.mainloop()
