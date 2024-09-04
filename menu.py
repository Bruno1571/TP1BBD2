# menu.py
from db_admin import ejecutar_consulta
from queries import queries

def mostrar_menu():
    print("Menú de Administración de BBDD:")
    print("1. Obtener Bases de Datos")
    print("2. Obtener Roles con Conexión")
    # Agrega más opciones aquí...

    opcion = input("Elige una opción: ")

    if opcion == '1':
        resultados = ejecutar_consulta(queries["obtener_bases_de_datos"])
        for r in resultados:
            print(r)
    elif opcion == '2':
        resultados = ejecutar_consulta(queries["obtener_roles_conexion"])
        for r in resultados:
            print(r)
    # Agrega más opciones aquí...

if __name__ == "__main__":
    mostrar_menu()
