'''
Este módulo provee los métodos en los cuales se toman decisiones,
tales como transformar información, mostrar mensajes, etc.
'''

from modelo import clase_modelo
from utilidades import *
from tkinter.messagebox import *


class clase_controlador():

    def __init__(self, modelo):
        self.modelo = modelo

    # ----------------------------------------------------------------------------------------------------------------------------
    # Guarda una referencia al TreeView de materiales para gestionar
    # el vaciado y nueva carga de datos cuando se modifique información
    # en la tabla 'Materiales'
    # ----------------------------------------------------------------------------------------------------------------------------
    def obtener_treeview_materiales(self, treeview_materiales):
        self.treeview_materiales = treeview_materiales

    # ----------------------------------------------------------------------------------------------------------------------------
    # Guarda una referencia a los obtejos Entry (text fields) de tkinter para poder
    # leer valores de ellos sin requerir acceder a la clase de la vista.
    # ----------------------------------------------------------------------------------------------------------------------------
    def obtener_campos_material(self, campos_material):
        self.campos_material = campos_material

    # ----------------------------------------------------------------------------------------------------------------------------
    # Este método valida si los cuatro campos del marco superior
    # fueron completados (ninguno vacío)
    # ----------------------------------------------------------------------------------------------------------------------------
    def validar_campos_material(self, campos_material):
        if len(campos_material['descripcion'].get()) == 0:
            utilidades().mostrar_mensaje(utilidades.ERROR,
                                         "La descripción del material es mandatoria")
            return False

        for clave in campos_material:
            try:
                # Intentar leer el valor del campo. Si está vacío
                # se genera una excepción.
                valor_actual = campos_material[clave].get()
            except:
                clave = clave.replace('_', ' ')
                utilidades().mostrar_mensaje(utilidades.ERROR,
                                             "Valor inválido en campos de material"
                                             + f" - El campo '{clave}' es requerido y debe ser válido.")
                return False

        return True

    # ----------------------------------------------------------------------------------------------------------------------------
    # Este método es llamado (callback) cuando se presiona el botón 'Agregar'
    # El método valida que se hayan completado todos los campos del material, e
    # intenta agregar el material a la tabla 'Materiales.
    # Si el material ya existe, se muestra un error.
    # ----------------------------------------------------------------------------------------------------------------------------
    def solicitud_agregar_material(self, campos_material):
        # Se valida que los campos del marco superior fueron completados
        # apropiadamente
        if not self.validar_campos_material(campos_material):
            showinfo("No se puede agregar el material",
                     "Todos los campos deben completarse para agregar un nuevo material")
            return False
        nuevo_material = {
            "descripcion": campos_material['descripcion'].get(),
            "stock_actual": campos_material['stock_actual'].get(),
            "stock_reposicion": campos_material['stock_reposicion'].get(),
            "demora_reposicion": campos_material['demora_reposicion'].get()
        }
        if not self.workaround_validacion_de_campos(nuevo_material):
            return False
        if not self.modelo.db.agregar_material(nuevo_material):
            showinfo("No se puede agregar el material",
                     "El material ya existe en la tabla 'Materiales'")
            return False
        else:
            showinfo("Operación completada",
                     "El material fue agregado correctamente a la tabla 'Materiales'")

        self.refrescar_treeview_materiales()
        return True

    # ----------------------------------------------------------------------------------------------------------------------------
    # Este método es llamado (callback) cuando se presiona el botón 'Modificar'
    # El método valida que se hayan completado todos los campos del material, e
    # intenta actualizar el material en la tabla 'Materiales.
    # ----------------------------------------------------------------------------------------------------------------------------
    def solicitud_modificar_material(self, campos_material):
        # Se valida que los campos del marco superior fueron completados
        # apropiadamente
        if not self.validar_campos_material(campos_material):
            showinfo("No se puede modificar el material",
                     "Todos los campos deben completarse para modificar el material")
            return False
        modificacion_material = {
            "descripcion": campos_material['descripcion'].get(),
            "stock_actual": campos_material['stock_actual'].get(),
            "stock_reposicion": campos_material['stock_reposicion'].get(),
            "demora_reposicion": campos_material['demora_reposicion'].get()
        }
        if not self.workaround_validacion_de_campos(modificacion_material):
            return False
        if not self.modelo.db.actualizar_material(campos_material['id'], modificacion_material):
            showinfo("No se puede modificar el material",
                     f"Error intentando actualizar el material con id [{campos_material['id'].get()}]")
            return False
        else:
            showinfo("Operación completada",
                     f"El material con id [{campos_material['id'].get()}] fue actualizado correctamente en la tabla 'Materiales'")

        self.refrescar_treeview_materiales()
        return True

    # ----------------------------------------------------------------------------------------------------------------------------
    # Elimina el registro de la tabla 'Materiales' cuya descripción coincida con
    # la del campo Descripción del marco superior
    # ----------------------------------------------------------------------------------------------------------------------------
    def solicitud_eliminar_material(self, campos_material):
        if not self.modelo.db.eliminar_material([campos_material['id'].get()]):
            showinfo("No se puede eliminar el material",
                     f"Error intentando eliminar el material con id [{campos_material['id'].get()}]")
            return False
        else:
            showinfo("Operación completada",
                     f"El material con id [{campos_material['id'].get()}] fue eliminado correctamente de la tabla 'Materiales'")

        self.refrescar_treeview_materiales()
        return True

    # ----------------------------------------------------------------------------------------------------------------------------
    # Este método se dispara ante el evento de un usuario que hace doble
    # click en la lista (TreeView) de materiales, moviendo al marco superior
    # de la pantalla los valores de la fila seleccionada en el marco inferior.
    # ----------------------------------------------------------------------------------------------------------------------------
    def click_en_material(self, event):

        if len(self.treeview_materiales.selection()) == 0:
            # Se hizo doblel click en un área del treeview donde no hay un material
            return

        material = self.treeview_materiales.selection()[0]
        campos_fila_treeview = self.treeview_materiales.item(material)[
            'values']
        self.campos_material["id"].set(
            self.modelo.db.obtener_id_material(campos_fila_treeview[0]))
        self.campos_material["descripcion"].set(campos_fila_treeview[0])
        self.campos_material["stock_actual"].set(int(campos_fila_treeview[1]))
        self.campos_material["stock_reposicion"].set(
            int(campos_fila_treeview[2]))
        self.campos_material["demora_reposicion"].set(
            int(campos_fila_treeview[3]))

    # ----------------------------------------------------------------------------------------------------------------------------
    # Si se ha definido un TreeView de materiales, se invoca al método (de modelo.py) que
    # colecta la lista actualizada de materiales desde la tabla 'Materiales', vacía dicho elemento
    # TreeView y agrega todos los materiales obtenidos durante la consulta.
    # ----------------------------------------------------------------------------------------------------------------------------
    def refrescar_treeview_materiales(self):
        if self.treeview_materiales is None:
            return False
        self.modelo.refrescar_treeview_materiales(self.treeview_materiales)

    # ----------------------------------------------------------------------------------------------------------------------------
    # Este método verifica que se haya cumplido con las expresiones regulares de los campos:
    # Descripción: solo caracteres alfabéticos
    # Stock y demora: solo dígitos numéricos
    # Lo agregué ya que por algún motivo deja de funcionar la validación adjunta a los campos
    # en la clase vista cuando se hace un validatecommand() sobre un elemento Entry()
    # de tkinter.
    # ----------------------------------------------------------------------------------------------------------------------------
    def workaround_validacion_de_campos(self, campos_material):
        if not utilidades().es_solo_alfabetico(campos_material['descripcion']):
            showinfo("Error de datos en campo 'Descripción'",
                     "El campo 'Descripción' solo debe contener caracteres alfabéticos")
            return False
        elif not utilidades().es_solo_numerico(campos_material['stock_actual']):
            showinfo("Error de datos en campo 'Stock Actual'",
                     "El campo 'Stock Actual' solo debe contener dígitos numéricos")
            return False
        elif not utilidades().es_solo_numerico(campos_material['stock_reposicion']):
            showinfo("Error de datos en campo 'Stock Reposición'",
                     "El campo 'Stock Reposición' solo debe contener dígitos numéricos")
            return False
        elif not utilidades().es_solo_numerico(campos_material['demora_reposicion']):
            showinfo("Error de datos en campo 'Demora Reposición'",
                     "El campo 'Demora Reposición' solo debe contener dígitos numéricos")
            return False
        return True
