import requests
from bs4 import BeautifulSoup
import json
import time

# URL actualizada del Top 250
url = "https://www.imdb.com/chart/top/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("❌ Error al acceder a IMDb.")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

# Selector actualizado para títulos (noviembre 2025)
items = soup.select('ul.ipc-metadata-list li.ipc-metadata-list-summary-item')
if not items:
    print("⚠️ No se encontraron títulos. IMDb puede haber cambiado su estructura.")
    exit()

peliculas = []

print("\n🎬 ─── MEJORES 10 PELÍCULAS SEGÚN IMDb ───\n")

for i, item in enumerate(items[:10], start=1):
    titulo_tag = item.select_one('a.ipc-title-link-wrapper')
    if not titulo_tag:
        continue

    titulo_texto = titulo_tag.get_text(strip=True)
    url_pelicula = "https://www.imdb.com" + titulo_tag['href'].split('?')[0]

    # Obtener página individual
    pelicula_response = requests.get(url_pelicula, headers=headers)
    if pelicula_response.status_code != 200:
        print(f"⚠️ No se pudo acceder a {url_pelicula}")
        continue

    pelicula_soup = BeautifulSoup(pelicula_response.content, 'html.parser')

    # Puntuación
    puntuacion_tag = pelicula_soup.select_one('[data-testid="hero-rating-bar__aggregate-rating__score"] span')
    puntuacion = puntuacion_tag.get_text(strip=True) if puntuacion_tag else 'N/A'

    # Descripción
    descripcion_tag = pelicula_soup.find('span', {'data-testid': 'plot-xl'})
    if not descripcion_tag:
        descripcion_tag = pelicula_soup.find('span', {'data-testid': 'plot-l'})
    descripcion = descripcion_tag.get_text(strip=True) if descripcion_tag else 'Sin descripción disponible'

    # Imagen
    imagen_tag = pelicula_soup.select_one('.ipc-media img')
    imagen_url = imagen_tag['src'] if imagen_tag else ''

    peliculas.append({
        'titulo': titulo_texto,
        'url': url_pelicula,
        'puntuacion': puntuacion,
        'descripcion': descripcion,
        'imagen': imagen_url
    })

    # Mostrar en terminal
    print(f"{i}. 🎞️ {titulo_texto}")
    print(f"   ⭐ Puntuación: {puntuacion}")
    print(f"   📝 Descripción: {descripcion[:100]}...")
    print(f"   🔗 URL: {url_pelicula}")
    print("   " + "-" * 60)
    time.sleep(1)

# Guardar en JSON
if peliculas:
    with open('peliculas.json', 'w', encoding='utf-8', errors='replace') as archivo:
        json.dump(peliculas, archivo, indent=4, ensure_ascii=False)
    print(f"\n✅ Se guardaron {len(peliculas)} películas en 'peliculas.json'")
else:
    print("\n⚠️ No se extrajo ninguna película.")
