# ─── IMPORTACIÓN DE LIBRERÍAS ───
import requests  # Para hacer solicitudes HTTP a páginas web
from bs4 import BeautifulSoup  # Para analizar y extraer datos del HTML
import json  # Para guardar los resultados en un archivo JSON
import time  # Para pausar la impresión y mejorar la experiencia visual

# ─── CABECERA HTTP PERSONALIZADA ───
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36"
}
# Simula un navegador real para evitar bloqueos por parte de IMDb

# ─── DICCIONARIO DE GÉNEROS TRADUCIDOS ───
GENERO_TRADUCIDO = {
    "action": "Acción",
    "adventure": "Aventura",
    "animation": "Animación",
    "biography": "Biografía",
    "comedy": "Comedia",
    "crime": "Crimen",
    "documentary": "Documental",
    "drama": "Drama",
    "family": "Familiar",
    "fantasy": "Fantasía",
    "film-noir": "Cine negro",
    "history": "Historia",
    "horror": "Terror",
    "music": "Música",
    "musical": "Musical",
    "mystery": "Misterio",
    "romance": "Romance",
    "sci-fi": "Ciencia ficción",
    "sport": "Deporte",
    "thriller": "Suspenso",
    "war": "Guerra",
    "western": "Occidental"
}
GENERO_DISPONIBLES = list(GENERO_TRADUCIDO.keys())  # Lista de géneros en inglés para usar en la URL

# ─── FUNCIÓN PRINCIPAL DE SCRAPING ───
def obtener_peliculas_por_genero(genero):
    # Construcción de la URL con el género elegido
    url = f"https://www.imdb.com/search/title/?genres={genero}&title_type=feature&sort=user_rating,desc"
    res = requests.get(url, headers=HEADERS)  # Solicitud HTTP con cabecera personalizada

    if res.status_code != 200:
        print("❌ Error al obtener las películas.")
        return []

    soup = BeautifulSoup(res.text, "html.parser")  # Parseo del HTML

    peliculas = []

    # Selección de elementos contenedores de películas (dos opciones por compatibilidad)
    items = soup.select("li.ipc-metadata-list-summary-item")
    if not items:
        items = soup.select(".lister-item")

    # Iteración sobre los primeros 10 resultados
    for item in items[:10]:
        # Extracción del título y URL
        titulo_tag = item.select_one("a.ipc-title-link-wrapper")
        if not titulo_tag:
            titulo_tag = item.select_one(".lister-item-header a")
        if not titulo_tag:
            continue

        titulo = titulo_tag.text.strip()
        href = titulo_tag.get("href", "")
        url_peli = f"https://www.imdb.com{href.split('?')[0]}"

        # Extracción de la puntuación
        rating_tag = item.select_one("span.ipc-rating-star")
        if not rating_tag:
            rating_tag = item.select_one("strong")
        rating = rating_tag.text.strip() if rating_tag else "N/A"

        # Extracción de la descripción
        descripcion_tag = item.select_one("span.ipc-metadata-list-summary-item__tl")
        if not descripcion_tag:
            descripcion_tag = item.select_one(".text-muted")
        descripcion = descripcion_tag.text.strip() if descripcion_tag else "Sin descripción disponible"

        # Guardado de los datos en un diccionario
        peliculas.append({
            "titulo": titulo,
            "genero": GENERO_TRADUCIDO[genero],
            "puntuacion": rating,
            "descripcion": descripcion,
            "url": url_peli
        })

    return peliculas

# ─── EJECUCIÓN PRINCIPAL ───

# Mostrar géneros disponibles en consola
print("🎭 Géneros disponibles:")
for i, g in enumerate(GENERO_DISPONIBLES, start=1):
    print(f" {i}. {GENERO_TRADUCIDO[g]}")

# Entrada del usuario
opcion = input("\n📝 Escribí el número del género que querés buscar: ").strip()

# Validación de la opción ingresada
if not opcion.isdigit() or not (1 <= int(opcion) <= len(GENERO_DISPONIBLES)):
    print("⚠️ Opción inválida. Elegí un número de la lista.")
    exit()

# Traducción del género seleccionado
genero = GENERO_DISPONIBLES[int(opcion) - 1]
nombre_genero = GENERO_TRADUCIDO[genero]

print(f"\n🔎 Buscando las 10 mejores películas de género '{nombre_genero}' en IMDb...\n")

# Llamado a la función de scraping
peliculas = obtener_peliculas_por_genero(genero)

# Mostrar resultados en consola
if not peliculas:
    print("⚠️ No se encontraron películas para ese género.")
else:
    print("\n🎬 ─── MEJORES PELÍCULAS ───\n")
    for i, peli in enumerate(peliculas, start=1):
        print(f"{i}. 🎞️ {peli['titulo']}")
        print(f"   🎭 Género: {peli['genero']}")
        print(f"   ⭐ Puntuación: {peli['puntuacion']}")
        print(f"   🔗 URL: {peli['url']}")
        print("   " + "-" * 60)
        time.sleep(0.5)  # Pausa para mejorar la experiencia visual

# ─── GUARDADO EN ARCHIVO JSON ───
if peliculas:
    with open("peliculas_por_genero.json", "w", encoding="utf-8", errors="replace") as f:
        json.dump(peliculas, f, indent=4, ensure_ascii=False)  # Guardado con formato legible
    print(f"\n✅ Se guardaron {len(peliculas)} películas del género '{nombre_genero}' en 'peliculas_por_genero.json'")
else:
    print("\n⚠️ No se pudo guardar nada porque no se extrajo contenido.")