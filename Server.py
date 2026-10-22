from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse 
from urllib.parse import urlparse, parse_qs
import json

# Importación obligatoria con tu código de estudiante exacto
import crud_usuario_usss006125
    
port = 3000
# Inicializamos la clase (asegúrate de que la clase dentro de tu archivo se llame crud_usuario_usss06125)
crudUsuarios = crud_usuario_usss006125.crud_usuario_usss006125()

class miServidor(SimpleHTTPRequestHandler):
    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud)
        datos = datos.decode("utf-8")
        datos = parse.unquote(datos)
        datos = json.loads(datos)
        
        if datos["modulo"] == "usuario":
            respuesta = {'msg': crudUsuarios.administrar(datos)}
        elif datos["modulo"] == "login":
            usuario = datos.get("usuario")
            clave = datos.get("clave")
            res = crudUsuarios.validar_login(usuario, clave)
            if res and len(res) > 0:
                respuesta = {'msg': 'ok', 'usuario': res[0]}
            else:
                respuesta = {'msg': 'Acceso denegado: Usuario o contraseña incorrectos'}

        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)
       
        if urlParse.path == "/usuarios":
            buscar = qs.get('buscar', [''])[0]
            datos = crudUsuarios.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type","text/json")
            self.end_headers()
            self.wfile.write(json.dumps(datos).encode("utf-8"))
        
        elif self.path == "/":
            self.path = "/Login.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif urlParse.path == "/vistas":
            self.path = f"/modulos/{qs.get('form', [''])[0]}.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

print(f"Servidor corriendo en el puerto {port}")
server = HTTPServer(("localhost",port),miServidor)
server.serve_forever()