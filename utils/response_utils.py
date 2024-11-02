from requests import Response
import requests
import random
import json

class HavanaRestaurantScraper:
    """
    Clase para almacenar variables y funciones, para la 
    utilizacion y reutilizacion de las mismas
    """
    def __init__(self) -> None:
        """
        Constructor inicial
        """
        self.url = "https://www.tripadvisor.es"
        self.user_agents =  [
            "Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 11; Mobile; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (Linux; Android 11; SM-G965U Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4387.116 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 11; en-US; SM-G965U Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4387.116 Mobile Safari/537.36"
        ]
        self.excluded = [
            "/Restaurants-g147271-zfp16-Havana_Ciudad_de_la_Habana_Province_Cuba.html", 
            "/Restaurants-g147271-zfp10955-Havana_Ciudad_de_la_Habana_Province_Cuba.html",
            "/Restaurants-g147271-zfp10954-Havana_Ciudad_de_la_Habana_Province_Cuba.html",
            "/Restaurants-g147271-zft10613-Havana_Ciudad_de_la_Habana_Province_Cuba.html"]
        
        self.foods = [
            "Caribeña", "Latina", "Saludable", "Francesa", 
            "Internacional", "Europea", "Saludable", "Cubana",
            "Marisco", "Española", "Bar", "Mediterráanea",
            "Centroamericana", "Café", "Japonesa", "Sushi",
            "Fusión", "Italiana", "Libanesa", "De Oriente Medio",
            "Árabe", "Pizza"]

        self.session = requests.Session()
        
        self.headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }

    def make_session(self, url: str) -> Response:
        """
        Funcion para crear la session y hacer 
        el get a la pagina principal (https://www.tripadvisor.es)
        """
        return self.session.get(url, headers=self.headers, stream=True)
    
    def obtain_responses(self) -> Response | str:
        """
        Funcion para obtener las respuestas,
        en caso de que tenga un status 200, retornar 
        el response para proseguir con lo demas, sino,
        parar el programa
        """
        response = self.make_session(str(self.url + "/Restaurants-g147271-Havana_Ciudad_de_la_Habana_Province_Cuba.html"))
        
        if response.status_code == 200:
            return response
        else:
            raise "Not Authorized :/"
        
    def export_json_file(self, data: list) -> None:
        """
        Exportar a el JSON final con todos los datos ya extraidos
        """
        try:
            with open("./restaurants.json", "w") as file:
                file.write(json.dumps({"data": data}, indent=4))
        except Exception as e:
            print(f"Error al intentar guardar el archivo JSON -> {e}")