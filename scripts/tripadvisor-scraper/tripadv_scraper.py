from utils.response_utils import HavanaRestaurantScraper, Data
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

utils = HavanaRestaurantScraper()

def main():
    """
    Funcion principal, ejecuta todo el programa,
    desde el scraping a la pagina principal, hasta obtener
    los tipos de comida del restaurante scrapeado
    """
    try:
        response = utils.obtain_responses()
        
        soup = BeautifulSoup(response.text, "html.parser")
        tag_a = soup.find_all("a", attrs={"class": "BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS"})

        tags = []
        # Usamos set para evitar elementos repetidos, solo tiene un inconveniente
        # y es que pone los resultados en la lista de forma desordenada pero
        # en este caso, no es algo que importe mucho
        for tag in tag_a:
            if tag["href"] not in utils.excluded:
                tags.append(str(utils.url + tag["href"]))
        
        restaurants = []
        for scraped_tag in set(tags):
            try:
                url_tag_response = utils.make_session(scraped_tag)
                url_tag_soup = BeautifulSoup(url_tag_response.text, "html.parser")
                
                data = Data(url_tag_soup)
                
                print(f"Checking {scraped_tag}")
                
                restaurants.append({
                    "scraped_link": scraped_tag,
                    "title": data.get_title().text.strip() if data.get_title() else None,
                    "ubication": data.get_ubication().text.strip() if data.get_ubication() else None,
                    "phone_number": data.get_phone_number().text.strip() if data.get_phone_number() else None,
                    "food_type": data.get_food_type(),
                    "rating": data.get_ratings()
                })
                
            except Exception as e:
                print(f"Error al obtener información de {scraped_tag}: {e}")
    except RequestException as e:
        print(f"Algo ocurrio cuando se hacia el requests -> {e}")

    utils.export_json_file(restaurants)

main()