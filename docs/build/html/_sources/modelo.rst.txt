Modelo
======

La clase del modelo implementa la actualización del componente TreeView de materiales mostrado en la interfaz gráfica de la aplicación, así como gestionar la 
referencia a la instancia de clase encargada de manejar la base de datos.

Los métodos de esta clase son:

.. list-table:: modelo
   :widths: 50 120
   :header-rows: 1

   * - Método
     - Uso
   * - refrescar_treeview_materiales
     - Dado cualquier cambio realizado en la base de datos (alta, baja o modificación de un registro) este método obtiene la lista actualizada de materiales y la muestra en el componente TreeView de materiales.
