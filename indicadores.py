import json
import urllib.request
import ssl
from datetime import datetime

class GestorIndicadores:
    def __init__(self):
        self.api_url = "https://mindicador.cl/api"

    def obtener_indicador(self, tipo_indicador, fecha=None):
        try:
            url = f"{self.api_url}/{tipo_indicador}"
            if fecha:
                url = f"{url}/{fecha}"
            
            print(f"Conectando a : {url}")


            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            

            req = urllib.request.Request(
                url, 
                data=None, 
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                if response.getcode() != 200:
                    return {"error": f"Error del servidor: {response.getcode()}"}

                data = json.loads(response.read().decode('utf-8'))

                if fecha:
                    if 'serie' in data and len(data['serie']) > 0:
                        valor = data['serie'][0]['valor']
                        return {
                            "indicador": data['nombre'],
                            "valor": valor,
                            "fecha": fecha,
                            "origen": "mindicador.cl"
                        }
                    else:
                        return {"error": "No hay datos para esa fecha."}
                
                elif 'serie' in data and len(data['serie']) > 0:
                     valor = data['serie'][0]['valor']
                     fecha_recibida = data['serie'][0]['fecha'][:10] 
                     return {
                            "indicador": data['nombre'],
                            "valor": valor,
                            "fecha": fecha_recibida,
                            "origen": "mindicador.cl"
                        }

            return {"error": "Formato desconocido."}

        except urllib.error.URLError as e:
            return {"error": f"Error de conexión: {e.reason}"}
        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}

if __name__ == "__main__":
    gestor = GestorIndicadores()
    print("Probando con urllib...")
    print(gestor.obtener_indicador("uf"))