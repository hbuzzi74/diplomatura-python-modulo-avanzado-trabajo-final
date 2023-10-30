
from utilidades import *
from peewee import *

import random

db = SqliteDatabase(utilidades().obtener_nombre_base_de_datos())


class BaseModel(Model):

    class Meta:
        database = db


class Materiales(BaseModel):
    descripcion = CharField(unique=True)
    stock_actual = IntegerField()
    stock_reposicion = IntegerField()
    demora_reposicion = IntegerField()


# Abrir la base de datos y crear las tablas si no existen
db.connect()
db.create_tables([Materiales])

################################################################################
# GESTOR DE BASE DE DATOS
################################################################################


class gestor_base_de_datos_sqlite3():

    # Este diccionario se utiliza para intercambiar datos entre
    # los objetos de la GUI (ejemplo: Tkinter) y la tabla 'Materiales',
    # de forma tal que las claves del diccionario pueden 'conectarse'
    # con campos en pantalla y de esa forma solo pasar el diccionario
    # como argumento a los métodos de alta y modificación de esta clase.
    campos_material = {
        "id": 0,
        "descripcion": "",
        "stock_actual": 0,
        "stock_reposicion": 0,
        "demora_reposicion": 0
    }

    # Este diccionario lleva cuenta de la cantidad de altas, bajas, modificaciones y consultas realizadas en la base de datos
    actualizaciones = {
        'altas': 0,
        'bajas': 0,
        'modificaciones': 0,
        'consultas': 0
    }

    # La siguiente variable guarda la referencia al observador de la base de datos
    observador_base_de_datos = None

    # ----------------------------------------------------------------------------------------------------------------------------
    # Obtiene el id de registro de un material buscándolo por su descripción.
    # Si el material no es encontrado se retorna el valor -1.
    # ----------------------------------------------------------------------------------------------------------------------------
    def obtener_id_material(self, descripcion):
        consulta = Materiales.select().where(Materiales.descripcion ==
                                             descripcion)
        consulta.execute()
        if consulta.count() == 0:   # Si no se encontró un registro coincidente
            return -1

        self.observador_base_de_datos.registrar_actualizacion(
            self.observador_base_de_datos.ACTUALIZACION_CONSULTA)

        # Devolver el id de registro (entero)
        return consulta.first().__dict__['__data__']['id']

    # ----------------------------------------------------------------------------------------------------------------------------
    # Agregar un registro a la tabla 'Materiales'.
    # El campo 'campos_material' contiene las mismas claves que el diccionario
    # homónimo declarado como variable de clase.
    # ----------------------------------------------------------------------------------------------------------------------------

    def agregar_material(self, diccionario_material):

        materiales = Materiales()
        materiales.descripcion = diccionario_material["descripcion"]
        materiales.stock_actual = diccionario_material["stock_actual"]
        materiales.stock_reposicion = diccionario_material["stock_reposicion"]
        materiales.demora_reposicion = diccionario_material["demora_reposicion"]
        try:
            materiales.save()
            utilidades().mostrar_mensaje(utilidades.INFO, f"Se agregó el material [{diccionario_material['descripcion']}]"
                                         + " a la tabla 'Materiales'")
        except IntegrityError:
            utilidades().mostrar_mensaje(utilidades.ERROR, "No se puede escribir en la tabla 'Materiales': "
                                         + f"el material [{diccionario_material['descripcion']}] ya existe en la tabla!")
            return False

        self.observador_base_de_datos.registrar_actualizacion(
            self.observador_base_de_datos.ACTUALIZACION_ALTA)

        return True

    # ----------------------------------------------------------------------------------------------------------------------------
    # Obtiene el registro de la tabla 'Materiales' correspondiente a la descripción de material provista.
    # Este método devuelve un único registro en forma de diccionario.
    # Si el registro no fue encontrado, entonces se retorna None.
    # ----------------------------------------------------------------------------------------------------------------------------
    def consultar_material(self, id_material):
        consulta = Materiales.select().where(Materiales.id == id_material)
        consulta.execute()
        if consulta.count() == 0:   # Si no se encontró un registro coincidente
            return None

        # Devolver el registro en forma de diccionario
        return consulta.first().__dict__['__data__']

    # ----------------------------------------------------------------------------------------------------------------------------
    # Obtiene todos los registros de la tabla 'Materiales', devolviendo una lista
    # de diccionarios con los valores de cada registro.
    # Si no hay registros en la tabla, este método devuelve una lista vacía.
    # ----------------------------------------------------------------------------------------------------------------------------
    def consultar_todos_los_materiales(self):
        registros = []
        consulta = Materiales.select().order_by(Materiales.descripcion.desc())
        consulta.execute()
        utilidades().mostrar_mensaje(utilidades.INFO, f"Se leyeron [{consulta.count()}] registro(s)"
                                     + " de la tabla 'Materiales'")

        self.observador_base_de_datos.registrar_actualizacion(
            self.observador_base_de_datos.ACTUALIZACION_CONSULTA)

        for registro_actual in consulta:
            registros.append(registro_actual.__dict__['__data__'])

        return registros

    # ----------------------------------------------------------------------------------------------------------------------------
    # Este método busca un registro en la tabla 'Materiales' por su campo descripcion.
    # Si el registro es encontrado, se reemplazan sus valores por los del argumento
    # nuevo_diccionario_material, el cual es un diccionario con el formato de
    # self.campos_material
    # ----------------------------------------------------------------------------------------------------------------------------
    def actualizar_material(self, id_material, nuevo_diccionario_material):

        if not isinstance(id_material, int):
            id_material = id_material.get()
        actualizacion = Materiales.update(
            nuevo_diccionario_material).where(Materiales.id == id_material)
        registros_modificados = actualizacion.execute()
        if registros_modificados == 1:
            utilidades().mostrar_mensaje(utilidades.INFO, "Se actualizó el registro de la tabla 'Materiales'"
                                         + f" con id=[{id_material}]. Nuevos valores: {nuevo_diccionario_material}")
        else:
            utilidades().mostrar_mensaje(utilidades.ERROR, "No se pudo actualizar el registro de la tabla 'Materiales'"
                                         + f" con id=[{id_material}]: el registro no fue encontrado.")
            return False

        self.observador_base_de_datos.registrar_actualizacion(
            self.observador_base_de_datos.ACTUALIZACION_MODIFICACION)

        return True

    # ----------------------------------------------------------------------------------------------------------------------------
    # Este método elimina el material cuyo id de material fue provisto.
    # Si el registro es encontrado y eliminado, el método devuelte True, de
    # otra forma devuelve False.
    # ----------------------------------------------------------------------------------------------------------------------------
    def eliminar_material(self, id_material):
        eliminar = Materiales.delete().where(Materiales.id == id_material)
        filas_eliminadas = eliminar.execute()
        if filas_eliminadas == 1:
            utilidades().mostrar_mensaje(utilidades.INFO, "Se eliminó un registro de la tabla 'Materiales'"
                                         + f" con id={id_material}.")
        else:
            utilidades().mostrar_mensaje(utilidades.ERROR, "No se pudo eliminar el registro de la tabla 'Materiales'"
                                         + f" con id={id_material}: el registro no fue encontrado.")
            return False

        self.observador_base_de_datos.registrar_actualizacion(
            self.observador_base_de_datos.ACTUALIZACION_BAJA)

        return True

    # ----------------------------------------------------------------------------------------------------------------------------
    # Este método guarda una referencia a la instancia de la clase observador que registra las altas,
    # bajas, modificaciones y consultas de la base de datos.
    # ----------------------------------------------------------------------------------------------------------------------------
    def guardar_observador_base_de_datos(self, observador_base_de_datos):
        self.observador_base_de_datos = observador_base_de_datos


# --------------------------------------------------------------------------------------------------------------------------------
# Este main se utiliza para cargar masivamente la tabla Materiales con información
# aleatoria y poder realizar pruebas
# --------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Este main se utiliza para cargar masivamente la tabla Materiales con información de prueba
    clase_base_de_datos = gestor_base_de_datos_sqlite3()
    registro = clase_base_de_datos.campos_material.copy()
    for indice in range(1, 101):
        # Generar una cadena random de 5 caracteres
        cadena_random = ""
        for indice in range(0, 5):
            cadena_random += chr(int(random.randrange(65, 90)))
        registro['descripcion'] = "Material " + cadena_random
        registro['stock_actual'] = int(random.randrange(0, 100))
        registro['stock_reposicion'] = int(random.randrange(0, 20))
        registro['demora_reposicion'] = int(random.randrange(0, 10))
        clase_base_de_datos.agregar_material(registro)
