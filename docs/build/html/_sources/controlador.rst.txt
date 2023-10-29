Controlador
===========

La clase del controlador es responsable por definir qué acciones deben realizarse sobre los materiales. Utiliza una referencia al modelo a través del cual
se accede a la base de datos de la aplicación.

Los métodos de esta clase son:

.. list-table:: controlador
   :widths: 50 120
   :header-rows: 1

   * - Método
     - Uso
   * - obtener_treeview_materiales
     - Guarda una referencia a los objetos de tipo TreeView creado por la vista para realizar futuras actualizaciones de su contenido
   * - obtener_campos_material
     - Guarda una referencia a los objetos de tipo Entry en los cuales se intercambian datos, ya sea con el usuario al teclear información como desde la base de datos
   * - validar_campos_material
     - Dado un diccionario recibido como argumento, verifica que todos sus campos tengan un valor (ningún campo de material en pantalla vacío)
   * - solicitud_agregar_material
     - Este método es invocado desde la interfaz gráfica cuando el usuario hace click en el botón **Agregar**. El método inicia la validación de los campos del material a guardar, y encarga al modelo realizar el alta del mismo.
   * - solicitud_modificar_material
     - Este método es invocado desde la interfaz gráfica cuando el usuario hace click en el botón **Modificar**. El método inicia la validación de los campos del material a guardar, y encarga al modelo realizar el actualización del registro correspondiente al material.
   * - solicitud_eliminar_material
     - Este método es invocado desde la interfaz gráfica cuando el usuario hace click en el botón **Eliminar**. El método obtiene el id del material cuya descripción coincide con la del diccionario recibido como argumento, e invoca el método de borrado del registro a través de la clase del modelo.
   * - click_en_material
     - Este método es invocado cuando se produce el evento correspondiente al usuario haciendo doble click sobe la lista de materiales, para lo cual se cargan en los campos de edición de material aquellos valores del material elegido por el usuario.
   * - refrescar_treeview_materiales
     - Remueve todas las filas del componente TreeView con la lista de materiales, obtiene del modelo la lista actualizada de todos los materiales y los vuelve a insertar en el componente TreeView.
   * - workaround_validacion_de_campos
     - Este método se utiliza como caso especial para la validación de campos en pantalla, verificando que los datos del material que se quiere agregar o modificar se ajustan a las reglas de expresiones regulares de la aplicación.
