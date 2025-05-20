import tkinter as tk
from tkinter import messagebox
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class WebScraping:
    def __init__(self,paginas,busqueda):
        self.paginas = paginas
        self.busqueda =  busqueda

class SitiosWeb:
    def __init__(self, master):
        self.master =  master
        self.master.title("WebScrapping")
        self.master.geometry("1200x600")
        self.master.config(bg="#77ACF1")

        def brillo():
            current_color = labelNombre.cget("fg")
            new_color = "#3E00FF" if  current_color == "white" else "white"
            labelNombre.config(fg = new_color)
            root.after(900,brillo)
        labelNombre = tk.Label(root,text="¡WEB SCRAPING",fg="white",bg="#77acf1",
                               font=("Cheddar",60,"bold"))

        labelNombre.pack(pady = 10)

        brillo()

        self.labelBusqueda = tk.Label(master,text="Escribe tu marca favorita:\n",
                                      fg="#0E185F", bg="#77ACF1",
                                      font=("Dank Mono", 25, "bold")
                                      )
        self.labelBusqueda.pack(pady=10)
        self.busqueda = self.entryBusqueda = tk.Entry(master,font=("Cascada Code",20))
        self.entryBusqueda.pack(pady=10)

        self.labelMensaje = tk.Label(master, text="Escoge tu tienda favorita:",
                                     fg="#0E185F", bg="#77ACF1",
                                     font=("Dank Mono", 25, "bold"))

        self.labelMensaje.pack(pady=10)

        self.menucontrol = tk.Menubutton(master, text="Opciones",
                                         pady=10, padx=10, bg="white",
                                         font=("Cascadia Code", 15, "bold"), fg="#241b3c")

        self.menucontrol.pack(pady =10)

        self.menuOpciones = tk.Menu(self.menucontrol, tearoff=0, fg="White", bg="#77ACF1",
                                    font=("Cascadia Code", 15))

        self.menuOpciones.add_command(label="Tienda1", command=self.buscar_tienda1)
        self.menuOpciones.add_command(label="Tienda2", command=self.buscar_tienda2)
        self.menuOpciones.add_command(label="Tienda3", command=self.buscar_tienda3)
        self.menuOpciones.add_command(label="Tienda4", command=self.buscar_tienda4)
        self.menuOpciones.add_command(label="Tienda5", command=self.buscar_tienda5)
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
        df = pd.DataFrame(productos, columns=["Sitio", "Nombre", "Precio", "Ranking", "Fecha de entrega"])# Aqui se debe cambiar
        df.to_csv("Dataset/carros.csv", index=False, mode='a',
                  header=not os.path.exists("Dataset/carros.csv")) # Aqui tambien

    def buscar_tienda1(self):
        busqueda = self.entryBusqueda.get()
        if busqueda.strip() != "":
            messagebox.showinfo("Buscando . . . ", f"Buscado { busqueda} en Tienda 1")#Se cambia
            self.tienda1(2,busqueda)

        else:
            messagebox.showwarning("Advertencia","El campo esta vacio, por favor escriba algo ")

    def buscar_tienda2(self):
        busqueda = self.entryBusqueda.get()
        if busqueda.strip() != "":
            messagebox.showinfo("Buscando . . . ", f"Buscado {busqueda} en Tienda 2")  # Se cambia
            self.tienda2(2, busqueda)

        else:
            messagebox.showwarning("Advertencia", "El campo esta vacio, por favor escriba algo ")

    def buscar_tienda3(self):
        busqueda = self.entryBusqueda.get()
        if busqueda.strip() != "":
            messagebox.showinfo("Buscando . . . ", f"Buscado {busqueda} en Tienda 3")  # Se cambia
            self.tienda3(2, busqueda)

        else:
            messagebox.showwarning("Advertencia", "El campo esta vacio, por favor escriba algo ")

    def buscar_tienda4(self):
        busqueda = self.entryBusqueda.get()
        if busqueda.strip() != "":
            messagebox.showinfo("Buscando . . . ", f"Buscado {busqueda} en Tienda 4")  # Se cambia
            self.tienda4(2, busqueda)

        else:
            messagebox.showwarning("Advertencia", "El campo esta vacio, por favor escriba algo ")

    def buscar_tienda5(self):
        busqueda = self.entryBusqueda.get()
        if busqueda.strip() != "":
            messagebox.showinfo("Buscando . . . ", f"Buscado {busqueda} en Tienda 5")  # Se cambia
            self.tienda5(2, busqueda)

        else:
            messagebox.showwarning("Advertencia", "El campo esta vacio, por favor escriba algo ")


    def tienda1(self,paginas,busqueda):
        pass
    def tienda2(self,paginas,busqueda):
        pass
    def tienda3(self,paginas,busqueda):
        pass

    def tienda4(self,paginas,busqueda):
        pass

    def tienda5(self,paginas,busqueda):
        pass

if __name__  == "__main__":
    root = tk.Tk()
    app = SitiosWeb(root)
    root.mainloop()
