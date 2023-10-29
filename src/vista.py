'''
Este módulo provee los métodos para consutrir y manejar objetos visuales
'''
from tkinter import Tk
from tkinter import Label
from tkinter import LabelFrame
from tkinter import Entry
from tkinter import Button
from tkinter import ttk
from tkinter import StringVar
from tkinter import IntVar
from tktooltip import ToolTip

from utilidades import *
from controlador import *


class clase_vista():

    root = Tk()

    campos_material = {
        "id": IntVar(),
        "descripcion": StringVar(),
        "stock_actual": IntVar(),
        "stock_reposicion": IntVar(),
        "demora_reposicion": IntVar()
    }

    # ----------------------------------------------------------------------------------------------------------------------------
    # Constructor: guarda la referencia al controlador para invocar métodos conforme el
    # usuario interactúe con los elementos visuales
    # ----------------------------------------------------------------------------------------------------------------------------

    def __init__(self, controlador):
        self.controlador = controlador

        self.crear_interfaz()

    # ----------------------------------------------------------------------------------------------------------------------------
    # Crear la interfaz visual que el usuario utiliza para gestionar los materiales
    # ----------------------------------------------------------------------------------------------------------------------------

    def crear_interfaz(self):

        # Crear la pantalla de interacción con el usuario
        self.root.title("Gestor de materiales")
        self.root.geometry("720x400")

        # Se crean dos marcos (uno para el material que se edita, y otro para
        # el treeview donde se muestran todos los materiales)
        marco_superior = LabelFrame(
            self.root, text="Material actual", width=670, height=130)
        marco_superior.place(x=20, y=10)
        self.root.update()

        # Se agregan los elementos que se ubican en el marco superior de la pantalla
        # También se incorporan expresiones regulares para que "Descripción" solo acepte
        # caracteres alfabéticos, y los demás campos (cantidades) solo numéricos.
        etiqueta_descripcion = Label(marco_superior, text="Descripción")
        etiqueta_descripcion.place(x=10, y=10)
        texto_descripcion = Entry(
            marco_superior, textvariable=self.campos_material["descripcion"], justify="left", width=75)
        texto_descripcion.place(x=100, y=10)
        texto_descripcion.configure(validate="key", validatecommand=(
            marco_superior.register(utilidades().es_solo_alfabetico), "%S"))
        ToolTip(texto_descripcion, msg="Descripción del material, la cual debe ser única. Este campo solo admite letras y símbolos.", delay=1)

        etiqueta_stock_actual = Label(marco_superior, text="Stock actual")
        etiqueta_stock_actual.place(x=10, y=60)
        texto_stock_actual = Entry(
            marco_superior, textvariable=self.campos_material["stock_actual"], justify="center", width=8)
        texto_stock_actual.place(x=100, y=60)
        texto_stock_actual.configure(validate="key", validatecommand=(
            marco_superior.register(utilidades().es_solo_numerico), "%S"))
        ToolTip(texto_stock_actual,
                msg="Unidades en existencia del material (número entero)", delay=1)

        etiqueta_stock_reposicion = Label(
            marco_superior, text="Stock reposición")
        etiqueta_stock_reposicion.place(x=180, y=60)
        texto_stock_reposicion = Entry(
            marco_superior, textvariable=self.campos_material["stock_reposicion"], justify="center", width=8)
        texto_stock_reposicion.place(x=280, y=60)
        texto_stock_reposicion.configure(validate="key", validatecommand=(
            marco_superior.register(utilidades().es_solo_numerico), "%S"))
        ToolTip(texto_stock_reposicion,
                msg="Nivel inferior de stock, el cual dispara un pedido de reposición (número entero)", delay=1)

        etiqueta_demora_reposicion = Label(
            marco_superior, text="Demora reposición")
        etiqueta_demora_reposicion.place(x=390, y=60)
        texto_demora_reposicion = Entry(
            marco_superior, textvariable=self.campos_material["demora_reposicion"], justify="center", width=8)
        texto_demora_reposicion.place(x=500, y=60)
        texto_demora_reposicion.configure(validate="key", validatecommand=(
            marco_superior.register(utilidades().es_solo_numerico), "%S"))
        ToolTip(texto_demora_reposicion,
                msg="Cantidad de días que debe esperarse para que el proveedor del material entregue un pedido de reposicón (número entero)", delay=1)

        boton_agregar = Button(marco_superior, text="Agregar",
                               command=lambda: self.controlador.solicitud_agregar_material(self.campos_material))
        boton_agregar.configure(width=8, height=1)
        boton_agregar.place(x=580, y=0)
        ToolTip(boton_agregar, msg="Agrega un nuevo material con la descripción y cantidades indicadas en esta sección. Si la descripción ya existe, el material no es agregado.", delay=1)

        boton_modificar = Button(marco_superior, text="Modificar",
                                 command=lambda: self.controlador.solicitud_modificar_material(self.campos_material))
        boton_modificar.configure(width=8, height=1)
        boton_modificar.place(x=580, y=35)
        ToolTip(boton_modificar, msg="Elimina el material que fue seleccionado en la lista inferior de materiales, y que se encuentra visible en esta sección.", delay=1)

        boton_eliminar = Button(marco_superior, text="Eliminar",
                                command=lambda: self.controlador.solicitud_eliminar_material(self.campos_material))
        boton_eliminar.configure(width=8, height=1)
        boton_eliminar.place(x=580, y=70)
        ToolTip(boton_eliminar, msg="Elimina el material que fue seleccionado en la lista inferior de materiales, y que se encuentra visible en esta sección.", delay=1)

        # Se agregan los elementos que se ubican en el marco inferior de la pantalla
        marco_inferior = LabelFrame(
            self.root, text="Lista de materiales", width=670, height=220)
        marco_inferior.place(x=20, y=(marco_superior.winfo_height() + 30))
        self.root.update()

        treeview_materiales = ttk.Treeview(marco_inferior)
        treeview_materiales["columns"] = ("col1", "col2", "col3", "col4")
        treeview_materiales.heading("#0", text="ID")
        treeview_materiales.heading("col1", text="Descripción")
        treeview_materiales.heading("col2", text="Stock Actual")
        treeview_materiales.heading("col3", text="Nivel de Reposición")
        treeview_materiales.heading("col4", text="Demora Reposición")
        treeview_materiales.column("#0", width=30, minwidth=30, anchor='c')
        treeview_materiales.column("col1", width=200, minwidth=200, anchor='w')
        treeview_materiales.column("col2", width=100, minwidth=50, anchor='c')
        treeview_materiales.column("col3", width=100, minwidth=50, anchor='c')
        treeview_materiales.column("col4", width=100, minwidth=50, anchor='c')
        treeview_materiales.pack()
        treeview_materiales.place(x=10, y=5, width=640, height=190)
        treeview_materiales.bind(
            "<Double-1>", self.controlador.click_en_material)

        treeview_materiales.bind(
            '<FocusOut>', self.controlador.click_en_material)
        treeview_materiales.bind('<Leave>', self.controlador.click_en_material)
        treeview_materiales.bind(
            '<Return>', self.controlador.click_en_material)

        ToolTip(treeview_materiales, msg="Muestra todos los materiales de la tabla 'Materiales'."
                + " Con doble click se ingresa al modo edición/borrado del material.", delay=1)

        self.controlador.obtener_treeview_materiales(treeview_materiales)
        self.controlador.obtener_campos_material(self.campos_material)

        # Cargar la lista inicial de materiales existentes
        self.controlador.refrescar_treeview_materiales()

        self.root.mainloop()
