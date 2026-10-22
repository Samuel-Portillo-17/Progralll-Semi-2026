from mysql.connector.errors import Error
import conexion

db = conexion.Conexion()

class crud_usuario_usss006125:
    def consultar(self, buscar):
        return db.consultar(f"SELECT * FROM usuario_usss006125 WHERE nombre LIKE '%{buscar}%' OR Usuario LIKE '%{buscar}%'")

    def validar_login(self, usuario, clave):
        sql = f"SELECT * FROM usuario_usss006125 WHERE Usuario = '{usuario}' AND clave = '{clave}'"
        return db.consultar(sql)

    def administrar(self, datos):
        try:
            if datos['accion'] == 'nuevo':
                sql = """
                    INSERT INTO usuario_usss006125(Usuario, clave, nombre, direccion, telefono)
                    VALUES(%s, %s, %s, %s, %s)
                """
                valores = (datos['Usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'])
            elif datos['accion'] == 'modificar':
                sql = """
                    UPDATE usuario_usss006125 SET Usuario=%s, clave=%s, nombre=%s, direccion=%s, telefono=%s
                    WHERE IdUsuario=%s
                """
                valores = (datos['Usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'], datos['IdUsuario'])
            else:
                sql = """
                    DELETE FROM usuario_usss006125 WHERE IdUsuario=%s
                """
                valores = (datos['IdUsuario'],)
            return db.ejecutar(sql, valores)
        except Error as e:
            return f"Error al guardar el usuario: {e}"