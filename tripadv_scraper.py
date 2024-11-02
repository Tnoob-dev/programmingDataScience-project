from utils.response_utils import HavanaRestaurantScraper
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
        for tag in list(set(tag_a)):
            if tag["href"] not in utils.excluded:
                tags.append(str(utils.url + tag["href"]))
        
        restaurants = []
        for scraped_tag in tags:
            try:
                url_tag_response = utils.make_session(scraped_tag)
                url_tag_soup = BeautifulSoup(url_tag_response.text, "html.parser")
                
                print(f"Checking {scraped_tag}")
                
                restaurant_title = url_tag_soup.find("h1", attrs={"class": "biGQs _P egaXP rRtyp"})
                restaurant_ubication = url_tag_soup.find("div", attrs={"class": "biGQs _P pZUbB hmDzD"})
                food_type = url_tag_soup.find("div", attrs={"class": "biGQs _P pZUbB alXOW oCpZu GzNcM nvOhm UTQMg ZTpaU W hmDzD"})            
                            
                if food_type.text.split(", ")[0] in utils.foods:
                    food_type = food_type.text.split(", ")
                else:
                    food_type = url_tag_soup.find_all("div", attrs={"class": "biGQs _P pZUbB alXOW oCpZu GzNcM nvOhm UTQMg ZTpaU W hmDzD"})[1].text.split(", ")
                
                restaurants.append({
                    "scraped_link": scraped_tag,
                    "title": restaurant_title.text.strip() if restaurant_title else None,
                    "ubication": restaurant_ubication.text.strip() if restaurant_ubication else None,
                    "food_type": food_type,
                })
            except Exception as e:
                print(f"Error al obtener información de {scraped_tag}: {e}")
    except RequestException as e:
        print(f"Algo ocurrio cuando se hacia el requests -> {e}")
    
    utils.export_json_file(restaurants)
    
main()