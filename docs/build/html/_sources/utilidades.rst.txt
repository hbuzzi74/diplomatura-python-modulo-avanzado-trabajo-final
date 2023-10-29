Utilidades
==========

Esta clase permite realizar tareas comunes de soporte a los objetos de la aplicación. Sus métodos no están relacionados con la gestión en sí de los materiales.


.. list-table:: utilidades
   :widths: 50 120
   :header-rows: 1

   * - Método
     - Uso
   * - mostrar_mensaje
     - Escribe un texto en pantalla (consola), anteponiendo un tipo de mensaje (información o error) y la fecha y hora en la cual se escribe el texto
   * - obtener_nombre_base_de_datos
     - Accede al archivo de configuración cuyo nombre es recibido como argumento (formato JSON), y tras leerlo identifica el valor de la clave 'nombre_base_de_datos'
   * - leer_archivo_configuracion
     - Devuelve una lista con todos los pares clave/valor del archivo con formato JSON cuyo nombre es recibido como argumento.
   * - es_expresion_regular
     - Dada una cadena recibida como argumento conteniendo una expresión regular, y otra cadena recibida como argumento conteniendo un valor, verificar si dicho valor cumple con la expresión regular recibida
   * - es_solo_alfabetico
     - Verifica si el valor recibido como argumento cumple con la expresión regular indicada por la constante EXPRESION_REGULAR_SOLO_LETRAS de la clase
   * - es_solo_numerico
     - Verifica si el valor recibido como argumento cumple con la expresión regular indicada por la constante EXPRESION_REGULAR_SOLO_NUMEROS de la clase
