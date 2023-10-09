'''
Este módulo provee los métodos de procesamiento de datos, incluyendo el intercambio
de datos con la base de datos.
'''
from tkinter import ttk


class clase_modelo():

    def __init__(self, db):
        self.db = db

    # ----------------------------------------------------------------------------------------------------------------------------
    # Vaciar todas las filas del TreeView de materiales y volver a cargarlas
    # con la información actualizada de la tabla 'Materiales' obtenida de
    # la clase de gestión de base de datos.
    # ----------------------------------------------------------------------------------------------------------------------------
    def refrescar_treeview_materiales(self, treeview_materiales):

        # 1) Obtener la lista completa de materiales
        lista_materiales = self.db.consultar_todos_los_materiales()

        # 2) Limpiar el objeto TreeView y volver a cargarle valores
        filas_treeview = treeview_materiales.get_children()
        for elemento in filas_treeview:
            treeview_materiales.delete(elemento)
        for material in lista_materiales:
            treeview_materiales.insert("", 0, text=str(material['id']), values=(
                material["descripcion"], material["stock_actual"], material["stock_reposicion"], material["demora_reposicion"]))
