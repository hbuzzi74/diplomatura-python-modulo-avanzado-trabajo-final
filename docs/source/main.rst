Main
====

El módulo main es el encargado de dar inicio a la ejecución del programa. Su función es instanciar los objetos indicados en esta documentación, según el siguiente orden:
1) Crear la instancia de manejo de la base de datos (gestor_base_de_datos_sqlite3)
2) Instanciar la clase del modelo y adjuntarle la instancia de base de datos 
3) Instanciar la clase del controlador y adjuntarle la instancia del modelo
4) Instanciar la clase de la vista y adjuntarle la instancia del controlador 

De esta forma se lanza la aplicación, estableciendo la correcta comunicación entre todas las clases.
