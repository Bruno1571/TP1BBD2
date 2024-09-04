# db_admin.py
import psycopg2
from queries import queries

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="tu_base_de_datos",
        user="tu_usuario",
        password="tu_contraseña"
    )

def ejecutar_consulta(consulta):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(consulta)
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados
