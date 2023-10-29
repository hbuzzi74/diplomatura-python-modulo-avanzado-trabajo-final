Vista
=====

La clase de la vista crea los componentes visuales de la aplicación. Es la encargada de proveer al usuario una interfaz que le permita interactuar con 
la base de datos, así como establecer la gestión de eventos tales como presionar un botón o ingresar texto desde el teclado para que dichos eventos sean 
correctamente manejados por la clase del controlador.

Los métodos de esta clase son:

.. list-table:: vista
   :widths: 50 120
   :header-rows: 1

   * - Método
     - Uso
   * - crear_interfaz
     - Crea el contenedor gráfico de la aplicación y todos sus elementos visibles. Adicionalmente, asocia a los elementos de tipo Button con los métodos de la clase controlador que se encargaran de realizar las acciones de alta, baja y borrado de registros. Por último, adjunta a los campos de edición (elementos de tipo Entry) aquellos métodos de control de expresiones regulares para aceptar solamente los caracteres apropiados (alfabéticos o numéricos, según el campo) cuando el usuario presiona una tecla.
