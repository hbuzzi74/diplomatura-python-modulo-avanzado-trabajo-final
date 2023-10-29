'''
Este módulo provee el punto de entrada a la aplicación de gestión de materiales.
'''
from modelo import clase_modelo
from controlador import clase_controlador
from vista import clase_vista
from gestor_base_de_datos_sqlite3 import gestor_base_de_datos_sqlite3

if __name__ == '__main__':

    db = gestor_base_de_datos_sqlite3()
    # registros = db.consultar_todos_los_materiales()
    # for registro in registros:
    #     print(registro)

    # Se crea el modelo, el cual guarda el objeto de base de datos
    modelo = clase_modelo(db)

    # Se crea el controlador, el cual guarda el objeto modelo para
    #  invocar sus métodos si aplica gestionar la base de datos
    controlador = clase_controlador(modelo)

    # Finalmente se crea la clase vista, la cual recibe una instancia
    # del controlador cuyos métodos puede invocar en caso de que el usuario
    # interactúe con los componentes visuales.
    vista = clase_vista(controlador)
