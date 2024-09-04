import psycopg2

def get_connection(dbname=None):
    return psycopg2.connect(
        dbname=dbname if dbname else 'postgres',
        user='Usuario',
        password='yContraseña',
        host='direccionIP',
        port='puerto'
    )

def list_databases():
    # Conectar al servidor sin especificar una base de datos específica
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT datname FROM pg_database WHERE datallowconn = true;
            """)
            databases = cur.fetchall()
            return [db[0] for db in databases]
    finally:
        conn.close()

def connect_to_database(dbname):
    # Conectar a una base de datos específica
    return get_connection(dbname=dbname)
