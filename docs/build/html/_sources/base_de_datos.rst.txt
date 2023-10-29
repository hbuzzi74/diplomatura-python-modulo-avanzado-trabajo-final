Base de datos
=============

El módulo gestor_base_de_datos_sqlite3.py contiene a la clase de nombre homónimo, la cual se encarga de interactuar con la base de datos de la aplicación.

Los métodos de esta clase son:

.. list-table:: gestor_base_de_datos_sqlite3
   :widths: 50 120
   :header-rows: 1

   * - Método
     - Uso
   * - obtener_id_material
     - Dada una descripción recibida como argumento, devuelve el id del registro conteniendo al material  
   * - agregar_material
     - Inserta un nuevo registro en la tabla Materiales con los valores del diccionario recibido como argumento
   * - consultar_material
     - Devuelve el registro correspondiente al material cuyo id es provisto como argumento
   * - consultar_todos_los_materiales
     - Retorna una lista de diccionarios con los registros de todos los materiales existentes en la base de datos
   * - actualizar_material
     - A partir de un registro de material identificado por el id provisto como argumento, actualiza los valores del registro usando aquellos del diccionario recibido como argumento
   * - eliminar_material
     - Elimina el registro identificado por el id recibido como argumento
   * - __main__
     - Al ejecutar esta función desde el módulo gestor_base_de_datos_sqlite3.py se popula la tabla 'Materiales' con valores aleatorios para realizar pruebas

