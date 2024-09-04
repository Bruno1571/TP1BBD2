# queries.py
queries = {
    "Grupo I. Obtener objetos del servidor": {
        "Obtener las bases de datos disponibles": """
            SELECT datname FROM pg_database WHERE datallowconn = true;
        """,
        "Obtener los Roles que se pueden conectar al servidor": """
            SELECT rolname FROM pg_roles WHERE rolcanlogin = true;
        """,
        "Obtener los Grupos que existen en el servidor": """
            SELECT rolname FROM pg_roles WHERE rolcanlogin = false;
        """,
        "Obtener los lenguajes del servidor": """
            SELECT lanname FROM pg_language;
        """,
    },
    "Grupo II. Obtener objetos de la BBDD": {
        "Obtener los esquemas": """
            SELECT nspname AS esquema FROM pg_catalog.pg_namespace ORDER BY nspname;
        """,
        "Obtener las tablas de un esquema": """
            SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';
        """,
        "Obtener las vistas": """
            SELECT viewname FROM pg_catalog.pg_views;
        """,
        "Obtener las funciones": """
            SELECT routine_name FROM information_schema.routines WHERE routine_type='FUNCTION';

        """,
        "Obtener las funciones": """
            SELECT routine_name FROM information_schema.routines WHERE routine_type='FUNCTION';

        """,
        "Obtener los triggers": """
            SELECT tgname FROM pg_trigger JOIN pg_proc ON pg_trigger.tgfoid = pg_proc.oid WHERE NOT tgisinternal;

        """,
        "Obtener las secuencias": """
            SELECT sequence_name FROM information_schema.sequences

        """,
        "Obtener las reglas": """
            SELECT r.rulename AS rule_name,
                c.relname AS table_name
            FROM pg_rewrite r
            JOIN pg_class c ON r.ev_class = c.oid
            WHERE c.relkind = 'r';

        """,
        "Obtener los tipos de datos": """
            SELECT DISTINCT format_type(atttypid, atttypmod) AS data_type
            FROM pg_attribute
            JOIN pg_class ON pg_attribute.attrelid = pg_class.oid
            JOIN pg_namespace ON pg_class.relnamespace = pg_namespace.oid
            WHERE pg_namespace.nspname = 'public'
            AND pg_attribute.attnum > 0
            AND NOT pg_attribute.attisdropped;

        """,
        "Obtener índices.": """
            SELECT indexname FROM pg_indexes WHERE schemaname = 'elegir_nombre_del_esquema';

        """,
    },
    "Grupo III. Obtener objetos del servidor": {
        "Detalles de los esquemas-Privilegios de acceso.": """
            SELECT 
                n.nspname AS esquema,
                c.relname AS tabla,
                pg_catalog.array_to_string(c.relacl, ',') AS privilegios
            FROM 
                pg_catalog.pg_class c
            JOIN 
                pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE 
                n.nspname = 'public'
                AND c.relkind = 'r';  -- 'r' indica tablas regulares

        """,
        "Obtener detalles de las tablas. Orden de los campos, nombre y tipo de dato.": """
            SELECT 
                c.relname AS table_name,
                a.attname AS column_name,
                t.typname AS data_type,
                a.attnum AS column_order
            FROM 
                pg_class c
            JOIN 
                pg_attribute a ON a.attrelid = c.oid
            JOIN 
                pg_type t ON a.atttypid = t.oid
            WHERE 
                c.relkind = 'r'  
                AND a.attnum > 0  
                AND NOT a.attisdropped  
                AND c.relnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public') 
            ORDER BY 
                c.relname,
                a.attnum;

        """,
        "Obtener detalles de las tablas. Clave primaria.": """
            SELECT pg_get_constraintdef(pg_constraint.oid),  pg_class.relname AS tabla, pg_constraint.conname 
            FROM pg_constraint, pg_class 
            WHERE ((pg_constraint.contype = 'p'::"char") AND
                (pg_constraint.conrelid = pg_class.oid)) AND 
            relname= 'tabla';

        """,
        "Obtener detalles de las tablas. Claves foráneas.": """
            SELECT lanname FROM pg_language;
        """,
        "Obtener los lenguajes del servidor": """
            SELECT lanname FROM pg_language;
        """,
        "Obtener los lenguajes del servidor": """
            SELECT lanname FROM pg_language;
        """,
    },
    # Agrega más grupos y consultas aquí...
}
