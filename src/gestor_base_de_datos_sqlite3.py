
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
# DECORADORES
################################################################################


def decorador_agregar_material(metodo):

    def envoltura(*args):
        print(
            "Función 'decorador_agregar_material' - se va a insertar un registro con la siguiente información", args[1])
        return metodo(*args)
    return envoltura


def decorador_modificar_material(metodo):

    def envoltura(*args):
        print(
            "Función 'decorador_modificar_material' - se va a modificar un registro de material con id ", args[1])
        return metodo(*args)
    return envoltura


def decorador_eliminar_material(metodo):

    def envoltura(*args):
        print(
            "Función 'decorador_eliminar_material' - se va a eliminar un registro de material con id ", args[1])
        return metodo(*args)
    return envoltura

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

        # Devolver el id de registro (entero)
        return consulta.first().__dict__['__data__']['id']

    # ----------------------------------------------------------------------------------------------------------------------------
    # Agregar un registro a la tabla 'Materiales'.
    # El campo 'campos_material' contiene las mismas claves que el diccionario
    # homónimo declarado como variable de clase.
    # ----------------------------------------------------------------------------------------------------------------------------

    @decorador_agregar_material
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
        for registro_actual in consulta:
            registros.append(registro_actual.__dict__['__data__'])

        return registros

    # ----------------------------------------------------------------------------------------------------------------------------
    # Este método busca un registro en la tabla 'Materiales' por su campo descripcion.
    # Si el registro es encontrado, se reemplazan sus valores por los del argumento
    # nuevo_diccionario_material, el cual es un diccionario con el formato de
    # self.campos_material
    # ----------------------------------------------------------------------------------------------------------------------------
    @decorador_modificar_material
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
        return True

    # ----------------------------------------------------------------------------------------------------------------------------
    # Este método elimina el material cuyo id de material fue provisto.
    # Si el registro es encontrado y eliminado, el método devuelte True, de
    # otra forma devuelve False.
    # ----------------------------------------------------------------------------------------------------------------------------
    @decorador_eliminar_material
    def eliminar_material(self, id_material):
        eliminar = Materiales.delete().where(Materiales.id == id_material)
        filas_eliminadas = eliminar.execute()
        if filas_eliminadas == 1:
            utilidades().mostrar_mensaje(utilidades.INFO, "Se eliminó un registro de la tabla 'Materiales'"
                                         + f" con id=[{id_material}].")
        else:
            utilidades().mostrar_mensaje(utilidades.ERROR, "No se pudo eliminar el registro de la tabla 'Materiales'"
                                         + f" con id=[{id_material}]: el registro no fue encontrado.")
            return False

        return True


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

    # Código agregado para la tarea del módulo 1 - unidad 3 de Python Avanzado
    # El decorador de alta de registros ya fue utilizado en le última línea del ciclo for
    # Se agrega a continuación el uso de decoradores para modificación y eliminación de registros
    print("=" * 80)
    print("Tarea del módulo 1 - unidad 3 de Python Avanzado (decoradores)")

    # Obtener y modificar un registro de prueba
    registros = clase_base_de_datos.consultar_todos_los_materiales()
    registro_de_prueba = registros[-1]
    print("Registro de prueba: " + str(registro_de_prueba))
    print("Incrementando el stock actual en 10 unidades")
    registro_de_prueba['stock_actual'] += 10

    # Actualizar el registro
    clase_base_de_datos.actualizar_material(
        int(registro_de_prueba['id']), registro_de_prueba)

    # Eliminar el registro
    registro_de_prueba = registros[-2]
    clase_base_de_datos.eliminar_material(int(registro_de_prueba['id']))
