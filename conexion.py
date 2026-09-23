import mysql.connector
from mysql.connector import Error


class Conexion:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "db_sistema_impuestos"
        print("Conectando a la base de datos...")

        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conexion.is_connected():
                print("Conexion exitosa")
            else:
                print("No se pudo conectar a la base de datos")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def consultar(self, sql):
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"Error al consultar la base de datos: {e}")
            return None

    def ejecutar(self, sql, datos):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, datos)
            self.conexion.commit()
            return 'ok'
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return f'Error: {e}'


class connector(Conexion):
    """Conector concreto con operaciones de ciclo de vida y ejecución."""

    def connect(self):
        """Abre la conexión si está cerrada y la devuelve."""
        if not getattr(self, "conexion", None) or not self.conexion.is_connected():
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        return self.conexion

    def disconnect(self):
        """Cierra la conexión activa."""
        if getattr(self, "conexion", None) and self.conexion.is_connected():
            self.conexion.close()

    def execute(self, sql, datos=None):
        """Ejecuta una consulta parametrizada y devuelve sus filas."""
        cursor = self.connect().cursor(dictionary=True)
        try:
            cursor.execute(sql, datos or ())
            if cursor.with_rows:
                return cursor.fetchall()
            self.conexion.commit()
            return []
        except Error:
            self.conexion.rollback()
            raise
        finally:
            cursor.close()

    def close(self):
        """Alias estándar para cerrar el conector."""
        self.disconnect()
    
        
    