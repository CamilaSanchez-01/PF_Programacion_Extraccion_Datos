import tkinter as tk
from tkinter import messagebox
import os
import pandas as pd
from Web_Scrapping_Link1 import tienda1
from Limpieza_CSV import limpieza1
from Dashboards_base import dashboard_estructura
from mysql.connector import connect, Error
from PIL import Image, ImageTk

""" 
    ¿Para que PIL?
        Hemos descubierto esta libreria por medio de internet para poder mejorar nuestra interfaz TK, nuestro menu,
        con el fin de ambientarlo, mejorarlo y crear calidad dentro de este.
        PIL o Pillow, es una libreria que permite la edición de imágenes directamente desde Python. 
        Soporta una variedad de formatos, incluídos los más utilizados como GIF, JPEG y PNG. 
        Una gran parte del código está escrito en C, por cuestiones de rendimiento.
"""

class WebScraping:
    def __init__(self, paginas):
        self.paginas = paginas

class SitiosWeb:
    def __init__(self, master):
        self.master =  master
        self.master.title("WebScrapping")
        self.master.geometry("480x480")
        self.master.config()

        # Aqui se hace uso de PIL
        gif_p = "assets/imagenes/carro.gif"
        self.frames = []
        gif = Image.open(gif_p)

        try:
            while True:
                frame = ImageTk.PhotoImage(gif.copy().convert("RGBA"))
                self.frames.append(frame)
                gif.seek(len(self.frames)) # aqui busca por cuadros dentro del gif
        except:
            pass # aqui es el final de la busqueda

        self.frame_index = 0
        self.label_fondo = tk.Label(self.master)
        self.label_fondo.place(x=0,y=0,relwidth=1,relheight=1)
        self.animar_gif()



        self.labelNombre = tk.Label(self.master, text="WebScrapping", fg="white", bg="#FF10F0",
                                    font=("Helvetica", 35, "bold"))
        self.labelNombre.pack(pady=20)

        def brillo(): #Configurar labelNombre
            current_color = self.labelNombre.cget("fg")
            new_color = "#FF10F0" if  current_color == "white" else "white"
            self.labelNombre.config(fg = new_color)
            root.after(900,brillo)

        brillo()

        self.menucontrol = tk.Menubutton(master, text="Opciones",
                                             pady=10, padx=10, bg="white",
                                             font=("Cascadia Code", 10, "bold"), fg="#FF10F0")
        self.menucontrol.place(x= 20,y= 100)

        self.menuOpciones = tk.Menu(self.menucontrol, tearoff=0, fg="White", bg="#FF10F0",
                                        font=("Cascadia Code", 10))

        self.menuOpciones.add_command(label="Iniciar Web Scrapping", command=self.buscar_tienda1)
        self.menuOpciones.add_command(label="Conexión con SQL", command=self.opc_conexion_sql)
        self.menuOpciones.add_command(label="Guardar Datos en CSV", command=self.opc_guardar_csv)
        self.menuOpciones.add_command(label="Limpiar Datos", command=self.opc_limpiar_datos)
        self.menuOpciones.add_command(label="Ver Dashboard", command=self.opc_ver_dashboard)
        self.menuOpciones.add_separator()
        self.menuOpciones.add_command(label="Salir",command=master.destroy)
        self.menucontrol["menu"] = self.menuOpciones


        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Salir","¿Seguro que quieres salir?"):
            self.master.destroy()

    def guardar_csv(self,productos):
        if not os.path.exists("Dataset"):
            os.makedirs("Dataset")

        df = pd.DataFrame(productos, columns=[
            "Marca", "Modelo",
            "Alemania (€)", "Países Bajos (€)", "Reino Unido (£)",  # ← NUEVAS columnas
            "Precio_Rango", "Rango", "Bateria", "Eficiencia",
            "Peso", "Remolque", "Carga_Rapida", "Carga_Vol", "Rango_1_parada",
            "Traccion_trasera", "Traccion_delantera", "Segmento_mercado",
            "Clasificacion_seguridad", "Numero_asientos", "Bomba_calor",
            "Carga_bidireccional", "Imagen_tag", "Sitio"
        ])

        df.to_csv("Dataset/carros.csv", index=False, mode='a',
                  header=not os.path.exists("Dataset/carros.csv"))
    def buscar_tienda1(self):
        try:
            messagebox.showinfo("Buscando . . . ", f"Buscado en Tienda ")
            productos = tienda1(32) #<-- Aqui se ajusta la cantidad de datos 300
            if productos:
                self.guardar_csv(productos)
                messagebox.showinfo("EXITO","Datos guardados correctamente")
            else:
                messagebox.showwarning("Sin Resultados", "No se encontraron productos")
        except:
            messagebox.showwarning("Advertencia","No se ha podido realizar Web Scrapping correctamente")

    def opc_conexion_sql(self):
        try:
            dbConexion = connect(
                host="localhost",
                user="root",
                password="12345678",
                database="ev_db"
            )
            messagebox.showinfo("Informacion", "Conexion exitosa !!")
            return dbConexion
        except Error as e:
            print(e)
            return False

    def opc_guardar_csv(self):
        messagebox.showinfo("Informacion", "Datos guardados al realizar Web Scrapping")

    def opc_limpiar_datos(self):
        try:
            limpieza1()
            messagebox.showinfo("Informacion", "Datos limpiados correctamente")
        except Exception as e:
            messagebox.showerror("ERROR", f"Ocurrio un error al limpiar los datos:\n{str(e)}")

    def opc_ver_dashboard(self):
        try:
            dashboard_estructura()
        except Exception as e:
            print(e)
            messagebox.showerror("ERROR", f"Ocurrio un error al abrir el dashboard:\n{str(e)}")

    # Aqui se hace uso de la animacion del gif, para que este funcione
    def animar_gif(self):
        self.label_fondo.config(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.master.after(100, self.animar_gif)

if __name__  == "__main__":
    root = tk.Tk()
    app = SitiosWeb(root)
    root.mainloop()

