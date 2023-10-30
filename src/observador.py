from utilidades import *

# observador_generico es la clase padre de los observadores usados en la aplicación.
# Requiere implementar el método registrar_actualizacion en la clase hija.


class observador_generico():

    def registrar_actualizacion(self,):
        # Este método se ejecuta solamente si la clase hija del observador, quien hereda de observador_generico, no fue implementada
        utilidades.escribir_archivo_de_logs(texto=utilidades.formatear_mensaje(
            utilidades.ERROR, 'No se puede implementar el patrón observador: clase hija de observador_generico no implementada'))


class observador_base_de_datos(observador_generico):

    ACTUALIZACION_ALTA = 0
    ACTUALIZACION_BAJA = 1
    ACTUALIZACION_MODIFICACION = 2
    ACTUALIZACION_CONSULTA = 3

    def __init__(self, gestor_base_de_datos_sqlite3):
        self.gestor_base_de_datos_sqlite3 = gestor_base_de_datos_sqlite3

    # El método registrar_actualizacion es invocada cada vez que se inserta, elimina o modifica un registro en la base de datos de la aplicación.
    def registrar_actualizacion(self, tipo_de_actualizacion):

        if tipo_de_actualizacion == self.ACTUALIZACION_ALTA:
            self.gestor_base_de_datos_sqlite3.actualizaciones['altas'] += 1
        elif tipo_de_actualizacion == self.ACTUALIZACION_MODIFICACION:
            self.gestor_base_de_datos_sqlite3.actualizaciones['modificaciones'] += 1
        elif tipo_de_actualizacion == self.ACTUALIZACION_BAJA:
            self.gestor_base_de_datos_sqlite3.actualizaciones['bajas'] += 1
        elif tipo_de_actualizacion == self.ACTUALIZACION_CONSULTA:
            self.gestor_base_de_datos_sqlite3.actualizaciones['consultas'] += 1
        else:
            # tipo de actualización incorrecto
            pass

        utilidades.escribir_archivo_de_logs(
            texto=('Observador - Accesos a la base de datos: ' + str(self.get_actualizaciones())))

    def get_actualizaciones(self,):
        return self.gestor_base_de_datos_sqlite3.actualizaciones
