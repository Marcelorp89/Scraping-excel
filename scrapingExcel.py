import requests
from bs4 import BeautifulSoup
import pandas as pd

#Lista para almacenar libros
libros = []

#Scraping primera pagina 
start_url = "https://books.toscrape.com/"
response = requests.get(start_url)


response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

print("\n Página 1: Inicio")
books = soup.find_all("article", class_="product_pod")
for book in books:
    titulo = book.h3.a["title"]
    precio = book.find("p", class_="price_color").text.strip()
    stock = book.find("p", class_="instock availability").text.strip()

    libros.append({"Título": titulo, "Precio": precio,"Stock": stock})

    

#Scraping del resto de las paginas (de la 2 en adelante)
page = 2
base_url = "https://books.toscrape.com/catalogue/page-{}.html"


while True:
    url = base_url.format(page)
    print(f"\n Pagina {page}: {url}")

    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    if not books:
        print("No hay mas libros. Fin del scraping.")
        break
    
    for book in books:
        titulo = book.h3.a["title"]
        precio = book.find("p", class_="price_color").text.strip()
        stock = book.find("p", class_="instock availability").text.strip()

        libros.append({"Título": titulo, "Precio": precio,"Stock": stock})
    
    page += 1

#Crear dataframe y ordenar
df = pd.DataFrame(libros)

#Guardar en excel
df.to_excel("libros.xlsx", index=False, engine="openpyxl")

print("Archivo 'libros.xlsx' creado con éxito, con títulos, precios y stock")


