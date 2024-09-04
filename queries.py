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
            SELECT schemaname, tablename, indexname FROM pg_indexes;


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
            SELECT 
                t.relname AS table_name,
                a.attname AS foreign_key_column
            FROM 
                pg_constraint c
            JOIN 
                pg_class t ON c.conrelid = t.oid
            JOIN 
                pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = t.oid
            WHERE 
                c.contype = 'f'  -- 'f' indica clave foránea
                AND t.relkind = 'r'  -- 'r' indica tabla
            ORDER BY 
                t.relname, a.attnum;

        """,
        "Obtener detalles de las secuencias.": """
            SELECT
                n.nspname AS schema_name,
                s.relname AS sequence_name,
                s.relkind AS type
            FROM
                pg_catalog.pg_class s
            JOIN
                pg_catalog.pg_namespace n ON s.relnamespace = n.oid
            WHERE
                s.relkind = 'S'  -- 'S' indica secuencias
            ORDER BY
                schema_name,
                sequence_name;

        """,
        "Obtener la definición de un índice. ": """
                SELECT * FROM pg_indexes 
        """,
    },
    "Grupo IV. Obtener detalles de privilegios de los objetos.": {
        "Obtener los privilegios de una tabla.": """
            SELECT 
                r.rolname AS usuario,
                c.relname AS tabla,
                CASE 
                    WHEN has_table_privilege(r.rolname, c.oid, 'SELECT') THEN 'SELECT'
                    WHEN has_table_privilege(r.rolname, c.oid, 'INSERT') THEN 'INSERT'
                    WHEN has_table_privilege(r.rolname, c.oid, 'UPDATE') THEN 'UPDATE'
                    WHEN has_table_privilege(r.rolname, c.oid, 'DELETE') THEN 'DELETE'
                    ELSE 'SIN PERMISO'
                END AS permiso
            FROM 
                pg_class c
            JOIN 
                pg_roles r ON has_table_privilege(r.rolname, c.oid, 'SELECT')
                OR has_table_privilege(r.rolname, c.oid, 'INSERT')
                OR has_table_privilege(r.rolname, c.oid, 'UPDATE')
                OR has_table_privilege(r.rolname, c.oid, 'DELETE')
            JOIN 
                pg_namespace n ON n.oid = c.relnamespace
            WHERE 
                n.nspname = 'public' -- puedes cambiarlo por otro schema si es necesario
                AND c.relname = 'nombre_de_la_tabla';

        """,
        "Obtener los privilegios de las funciones. ": """
            SELECT 
                r.rolname AS usuario,
                n.nspname AS esquema,
                p.proname AS funcion,
                CASE 
                    WHEN has_function_privilege(r.rolname, p.oid, 'EXECUTE') THEN 'EXECUTE'
                    ELSE 'SIN PERMISO'
                END AS permiso
            FROM 
                pg_proc p
            JOIN 
                pg_roles r ON has_function_privilege(r.rolname, p.oid, 'EXECUTE')
            JOIN 
                pg_namespace n ON n.oid = p.pronamespace
            WHERE 
                n.nspname = 'public' -- Cambia esto por el esquema que desees
            ORDER BY 
                r.rolname, p.proname;
 
        """,
    },
        "Grupo V. Monitoreo.": {
        "Usuarios conectados, IP y consulta": """
            SELECT
                usename AS usuario,
                client_addr AS ip_cliente,
                query AS consulta
            FROM
                pg_stat_activity
            WHERE
                state = 'active';

        """,
        "Tamaño de las bases de datos del servidor. ": """
            SELECT
                d.datname AS base_de_datos,
                pg_size_pretty(pg_database_size(d.datname)) AS tamaño
            FROM
                pg_database d
            ORDER BY
                pg_database_size(d.datname) DESC;

        """,
        "Tamaño de una tabla. ": """
            SELECT pg_size_pretty(pg_total_relation_size('nombre_tabla')) AS tamaño
 
        """,
        "Tamaño de todas las tablas de un esquema. ": """
            SELECT
                schemaname AS esquema,
                tablename AS tabla,
                pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS tamaño
            FROM
                pg_tables
            WHERE
                schemaname = 'public'  
            ORDER BY
                pg_total_relation_size(schemaname || '.' || tablename) DESC;

            
        """,
        "Listado por BBDD del tamaño total de la BBDD, el nombre del esquema, el nombre de la tabla, el tamaño  total de la tabla, el tamaño de la tabla y el tamaño del índice.": """
            SELECT
                pg_size_pretty(pg_database_size(current_database())) AS tamaño_total_bd,
                schemaname AS esquema,
                relname AS tabla,
                pg_size_pretty(pg_total_relation_size(relid)) AS tamaño_total,
                pg_size_pretty(pg_relation_size(relid)) AS tamaño_tabla,
                pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) AS tamaño_indices
            FROM
                pg_stat_user_tables
            ORDER BY
                pg_total_relation_size(relid) DESC;
 
        """,
    },
    # Agrega más grupos y consultas aquí...
}
