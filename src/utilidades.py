'''
Esta clase provee funcionalidades comunes a todas las demas, siendo su
principal función:
- Mostrar mensajes en consola
- Leer el archivo de configuración y obtener información del mismo
- Verificar si un valor cumple con una determinada expresión regular
'''
import json
import os
import datetime
import re

NOMBRE_ARCHIVO_LOGS = 'logs.txt'

# Este decorador es invocado cuando se llama el método mostrar_mensaje de la clase utilidades.
# Su función es escribir en el archivo logs.txt aquella información que se está enviando a la consola,
# de forma tal de disponer de un archivo con fecha, hora y texto de cada mensaje dentro del archivo de logs.


def decorador_mostrar_mensaje(metodo):

    def envoltura(*args):

        nombre_archivo_logs = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            NOMBRE_ARCHIVO_LOGS
        )

        try:
            texto_formateado = utilidades.formatear_mensaje(
                args[1], args[2]) + '\n'
            archivo_logs = open(nombre_archivo_logs, 'a')
            archivo_logs.write(texto_formateado)
            archivo_logs.close()

        except Exception as e:
            print(
                f"Error escribiendo el archivo {NOMBRE_ARCHIVO_LOGS}: {e.args[0]}")

        return metodo(*args)
    return envoltura


class utilidades():

    # Nombre por defecto del archivo de configuración de la aplicación
    NOMBRE_ARCHIVO_CONFIGURACION = "configuracion.json"

    # Tipos de mensajes usados por el método mostrar_mensaje():
    INFO = 1
    ERROR = 2

    # Expresiones regulares por tipo de campo
    # La expresion regular correspondiente a letras incluye caracteres
    # especiales definidos en la consigna del trabajo final.
    EXPRESION_REGULAR_SOLO_LETRAS = "^[A-Za-z ]+(?:[ _-][A-Za-z]+)*$"
    EXPRESION_REGULAR_SOLO_NUMEROS = "^[0-9]+$"

    @classmethod
    def escribir_archivo_de_logs(self, nombre_archivo_logs=NOMBRE_ARCHIVO_LOGS, texto=""):

        nombre_archivo_logs = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            NOMBRE_ARCHIVO_LOGS
        )

        try:
            texto_formateado = utilidades.formatear_mensaje(
                utilidades.INFO, texto) + '\n'
            print(texto_formateado)
            archivo_logs = open(nombre_archivo_logs, 'a')
            archivo_logs.write(texto_formateado)
            archivo_logs.close()

        except Exception as e:
            print(
                f"Error escribiendo el archivo {NOMBRE_ARCHIVO_LOGS}: {e.args[0]}")

    # ----------------------------------------------------------------------------------------------------------------------------
    # Formatear un text de forma tal de anteponer el itpo de mensaje (información o error)
    # y un timestamp indicando cuándo se generó el mismo
    # ----------------------------------------------------------------------------------------------------------------------------

    @classmethod
    def formatear_mensaje(self, tipo_mensaje, texto_mensaje):

        if tipo_mensaje == self.INFO:
            tipo_mensaje = "[INFO]  "
        elif tipo_mensaje == self.ERROR:
            tipo_mensaje = "[ERROR] "
        else:
            tipo_mensaje = ""

        fecha_actual = datetime.datetime.now()
        fecha_formateada = ("{}/{:02}/{:02} {}:{:02}:{:02}".format(fecha_actual.year,
                                                                   fecha_actual.month,
                                                                   fecha_actual.day,
                                                                   fecha_actual.hour,
                                                                   fecha_actual.minute,
                                                                   fecha_actual.second))
        timestamp = "[" + fecha_formateada + "]"
        return (timestamp + tipo_mensaje + texto_mensaje)

    # ----------------------------------------------------------------------------------------------------------------------------
    # Mostrar un mensaje en consola de tipo informativo o de error, incluyendo
    # la fecha y hora. Este método no devuelve ningún valor.
    # ----------------------------------------------------------------------------------------------------------------------------
    @decorador_mostrar_mensaje
    def mostrar_mensaje(self, tipo_mensaje, texto_mensaje):

        mensaje_formateado = utilidades.formatear_mensaje(
            tipo_mensaje, texto_mensaje)
        print(mensaje_formateado)

    # ----------------------------------------------------------------------------------------------------------------------------
    # Obtener el nombre de la base dedatos que será utilizada por la
    # aplicación desde el archivo de configuración.
    # El archivo debe ser de tipo JSON y la clave correspondiente al
    # nombre de la base de datos es "nombre_base_de_datos".
    # Si el nombre del archivo de configuración no fue provisto como argumento,
    # se utilida el nombre por defecto indicado en
    # NOMBRE_ARCHIVO_CONFIGURACION.
    # ----------------------------------------------------------------------------------------------------------------------------
    def obtener_nombre_base_de_datos(self, nombre_archivo_configuracion=None):

        # Obtener el nombre de la base de datos usada por la aplicación
        try:
            archivo_cfg = self.leer_archivo_configuracion(
                nombre_archivo_configuracion)
            nombre_base_de_datos = archivo_cfg["nombre_base_de_datos"]
            return nombre_base_de_datos
        except Exception:
            self.mostrar_mensaje(self.ERROR, "Error en el archivo de "
                                 + "configuración "
                                 + f"{nombre_archivo_configuracion}: el nombre"
                                 + " de la base de datos no fue encontrado. "
                                 + "Cancelando la ejecuón de la aplicación.")

        return None

    # ----------------------------------------------------------------------------------------------------------------------------
    # Leer el archivo de configuración (formato JSON) y retornar todos los
    # pares de clave-valor encontrados.
    # ----------------------------------------------------------------------------------------------------------------------------
    def leer_archivo_configuracion(self, nombre_archivo_configuracion=None):
        # Si no se provee un nombre de archivo de configuración, entonces se
        # utiliza el nombre por defecto
        if nombre_archivo_configuracion is None:
            nombre_archivo_configuracion = self.NOMBRE_ARCHIVO_CONFIGURACION

        archivo_cfg = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            nombre_archivo_configuracion
        )

        try:
            archivo_cfg = json.loads(open(archivo_cfg).read())
        except FileNotFoundError:
            self.mostrar_mensaje(self.ERROR, "El archivo de configuración"
                                 + f" {nombre_archivo_configuracion} no fue encontrado!")
            quit()

        return archivo_cfg

    # ----------------------------------------------------------------------------------------------------------------------------
    # Verificar si un texto cumple con una determinada expresión regular
    # - expresion_regular es una cadena conteniendo cualquier expresión regular
    # válida. Se pueden usar las constantes EXPRESION_REGULAR_SOLO_NUMEROS y
    # EXPRESION_REGULAR_SOLO_LETRAS o personalizar el patrón.
    # - valor_a_revisar es una cadena o valor numérico a verificar si cumple
    # con la expresión regular.
    # El método retorna True o False según se cumpla o no con la expresión
    # regular respectivamente.
    # ----------------------------------------------------------------------------------------------------------------------------
    def es_expresion_regular(self, expresion_regular, valor_a_revisar):
        if type(valor_a_revisar) != str:
            valor_a_revisar = str(valor_a_revisar)
        expresion_regular = re.compile(expresion_regular)
        resultado = expresion_regular.match(valor_a_revisar)
        if resultado is None:
            return False
        return True

    # ----------------------------------------------------------------------------------------------------------------------------
    # Verifica que la variable 'texto' recibida como argumento se ajusta a una
    # expersión regular que acepta solamente caracteres alfabéticos (no numéricos)
    # ----------------------------------------------------------------------------------------------------------------------------
    def es_solo_alfabetico(self, texto):
        return self.es_expresion_regular(self.EXPRESION_REGULAR_SOLO_LETRAS, texto)

    # ----------------------------------------------------------------------------------------------------------------------------
    # Verifica que la variable 'valor' recibida como argumento se ajusta a una
    # expersión regular que acepta solamente dígitos numéricos
    # ----------------------------------------------------------------------------------------------------------------------------
    def es_solo_numerico(self, valor):
        return self.es_expresion_regular(self.EXPRESION_REGULAR_SOLO_NUMEROS, valor)
