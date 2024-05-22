import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# Crear el directorio de imágenes si no existe
def create_directory(directory='imagenes'):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Descargar una imagen desde la URL y guardarla en el directorio especificado
def download_image(image_url, directory='imagenes'):
    try:
        # Obtener el contenido de la imagen
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa

        # Extraer el nombre de la imagen de la URL
        filename = os.path.join(directory, image_url.split('/')[-1])

        # Guardar la imagen en el directorio
        with open(filename, 'wb') as image_file:
            for chunk in response.iter_content(1024):
                image_file.write(chunk)
        print(f"Imagen guardada en {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar {image_url}: {e}")

# Verificar si el src es una URL completa o relativa, y convertirla a URL completa si es necesario
def get_full_image_url(src, base_url):
    return urljoin(base_url, src)

# Función principal para el web scraping de imágenes
def scrape_images(url, directory='imagenes'):
    # Crear el directorio de imágenes
    create_directory(directory)
    try:
        # Realizar la solicitud HTTP GET
        response = requests.get(url)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa

        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todas las etiquetas <img> y sus atributos src
        img_tags = soup.find_all('img')

        # Filtrar y descargar imágenes con formatos permitidos
        for img in img_tags:
            img_url = img.get('src')
            if img_url:
                img_url = get_full_image_url(img_url, url)
                if img_url.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    download_image(img_url, directory)

    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a {url}: {e}")

if __name__ == "__main__":
    # URL inicial para comenzar el proceso de scraping de imágenes
    initial_url = 'https://es.wikipedia.org/wiki/Kimetsu_no_Yaiba' 
    # Iniciar el scraping de imágenes
    scrape_images(initial_url)
