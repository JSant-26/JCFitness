# --- START OF FILE app/database_manager.py (VERSIÓN SEGURA Y COMPLETA) ---

import psycopg2
import os
import sys
from psycopg2 import sql
from dotenv import load_dotenv

# Cargar las variables desde el archivo .env al entorno de la aplicación
load_dotenv()

try:
    from werkzeug.security import generate_password_hash, check_password_hash
except ImportError:
    print("Error Crítico: La librería 'Werkzeug' no está instalada. Por favor, ejecuta 'python -m pip install Werkzeug'")
    sys.exit(1)

# --- Configuración de la Conexión a PostgreSQL ---
# Ahora se lee de forma segura desde las variables de entorno.
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}
DB_NAME = os.getenv("DB_NAME", "jcfitness_main")
# ----------------------------------------------------

# Verificación de que las variables de entorno están cargadas
if not DB_CONFIG["user"] or not DB_CONFIG["password"]:
    print("Error Crítico: Las credenciales de la base de datos (DB_USER, DB_PASSWORD) no están configuradas.")
    print("Por favor, crea un archivo '.env' en la raíz del proyecto y define estas variables.")
    sys.exit(1)


class DatabaseManager:
    def __init__(self, sql_scripts_path='sql'):
        self.sql_scripts_path = sql_scripts_path
        self._ensure_database_exists()
        self._initialize_master_schema()

    def _get_server_connection(self):
        """Conexión al servidor PostgreSQL sin especificar una base de datos."""
        try:
            server_config = DB_CONFIG.copy()
            server_config['dbname'] = 'postgres'
            conn = psycopg2.connect(**server_config)
            conn.autocommit = True
            return conn
        except psycopg2.OperationalError as e:
            print(f"Error Crítico: No se pudo conectar al servidor de PostgreSQL.")
            print(f"Detalle: {e}")
            print("\nPor favor, asegúrate de que:")
            print("1. El servicio de PostgreSQL está corriendo.")
            print("2. Los datos en tu archivo .env son correctos.")
            return None

    def _ensure_database_exists(self):
        """Asegura que la base de datos principal (ej. jcfitness_main) exista."""
        conn = self._get_server_connection()
        if not conn:
            sys.exit(1)
            
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        if not cursor.fetchone():
            print(f"La base de datos '{DB_NAME}' no existe. Creándola...")
            try:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
                print(f"Base de datos '{DB_NAME}' creada exitosamente.")
            except psycopg2.Error as e:
                print(f"Error al crear la base de datos: {e}")
        
        cursor.close()
        conn.close()

    def _get_main_db_connection(self):
        """Obtiene una conexión a nuestra base de datos principal (jcfitness_main)."""
        main_db_config = DB_CONFIG.copy()
        main_db_config['dbname'] = DB_NAME
        try:
            return psycopg2.connect(**main_db_config)
        except psycopg2.OperationalError as e:
            print(f"Error al conectar a la base de datos '{DB_NAME}': {e}")
            return None

    def _execute_script_from_file(self, connection, file_path, replacements=None):
        """Ejecuta un script SQL desde un archivo en una conexión dada."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                script = f.read()
            
            if replacements:
                script = script.format(**replacements)
            
            cursor = connection.cursor()
            cursor.execute(script)
            connection.commit()
            cursor.close()
            return True
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo de script en '{file_path}'")
        except psycopg2.Error as e:
            print(f"Error al ejecutar el script '{os.path.basename(file_path)}': {e}")
            connection.rollback()
        except Exception as e:
            print(f"Un error inesperado ocurrió al ejecutar el script: {e}")
            connection.rollback()
        return False

    def _initialize_master_schema(self):
        """Asegura que la tabla 'Usuarios' exista en el esquema 'public'."""
        conn = self._get_main_db_connection()
        if not conn:
            sys.exit(1)
        
        script_path = os.path.join(self.sql_scripts_path, 'master_schema.sql')
        self._execute_script_from_file(conn, script_path)
        conn.close()

    # --- Métodos Públicos para la Lógica de la Aplicación ---

    def create_tenant(self, username, password, gym_name):
        """Crea un nuevo tenant: un esquema y un usuario admin."""
        schema_name = f"tenant_{username.lower().replace(' ', '_')}"
        conn = self._get_main_db_connection()
        if not conn:
            return False, "No se pudo conectar a la base de datos principal."

        cursor = conn.cursor()
        try:
            cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema_name)))
            conn.commit()
            print(f"Esquema '{schema_name}' creado.")

            tenant_script_path = os.path.join(self.sql_scripts_path, 'tenant_schema.sql')
            if not self._execute_script_from_file(conn, tenant_script_path, replacements={"schema_name": schema_name}):
                raise Exception("Fallo al ejecutar el script del tenant.")
            
            print(f"Tablas creadas en el esquema '{schema_name}'.")

            password_hash = generate_password_hash(password)
            cursor.execute(
                """
                INSERT INTO public.Usuarios (nombre_usuario, contrasena_hash, rol, nombre_gym, nombre_esquema)
                VALUES (%s, %s, 'admin', %s, %s)
                """,
                (username, password_hash, gym_name, schema_name)
            )
            conn.commit()
            print(f"Usuario '{username}' registrado como admin del gimnasio '{gym_name}'.")
            
            return True, "Gimnasio registrado exitosamente."

        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            return False, f"El nombre de usuario '{username}' o el esquema '{schema_name}' ya existen."
        except Exception as e:
            print(f"Error al crear el tenant: {e}")
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()

    def validate_user(self, username, password):
        """Valida las credenciales de un usuario y devuelve su información."""
        conn = self._get_main_db_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id_usuario, contrasena_hash, rol, nombre_gym, nombre_esquema FROM public.Usuarios WHERE nombre_usuario = %s",
                (username,)
            )
            user_data = cursor.fetchone()

            if user_data and check_password_hash(user_data[1], password):
                return {
                    "id": user_data[0],
                    "role": user_data[2],
                    "gym_name": user_data[3],
                    "schema": user_data[4]
                }
            return None
        except psycopg2.Error as e:
            print(f"Error al validar usuario: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def get_tenant_connection(self, schema_name):
        """
        Obtiene una conexión a la BD principal, pero configura la ruta de búsqueda
        para que apunte al esquema de un tenant específico.
        """
        if not schema_name:
            return None
            
        conn = self._get_main_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor()
        try:
            cursor.execute(sql.SQL("SET search_path TO {}, public").format(sql.Identifier(schema_name)))
            print(f"Conexión establecida. Ruta de búsqueda configurada para el esquema: {schema_name}")
            return conn
        except psycopg2.Error as e:
            print(f"Error al establecer la conexión para el tenant '{schema_name}': {e}")
            conn.close()
            return None
        finally:
            cursor.close()