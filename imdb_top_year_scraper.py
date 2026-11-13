import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36"
}

def obtener_mejores_peliculas(anio):
    """Obtiene las 10 mejores películas del año dado desde IMDb."""
    url = f"https://www.imdb.com/search/title/?year={anio}&title_type=feature&sort=user_rating,desc"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print("❌ Error al obtener las películas.")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    peliculas = []

    # Selector actualizado (noviembre 2025)
    items = soup.select("li.ipc-metadata-list-summary-item")
    if not items:
        items = soup.select(".lister-item")

    for item in items[:10]:
        titulo_tag = item.select_one("a.ipc-title-link-wrapper")
        if not titulo_tag:
            titulo_tag = item.select_one(".lister-item-header a")
        if not titulo_tag:
            continue

        titulo = titulo_tag.text.strip()
        href = titulo_tag.get("href", "")
        url_peli = f"https://www.imdb.com{href.split('?')[0]}"

        # Extraer rating
        rating_tag = item.select_one("span.ipc-rating-star")
        if not rating_tag:
            rating_tag = item.select_one("strong")
        rating = rating_tag.text.strip() if rating_tag else "N/A"

        # Extraer descripción
        descripcion_tag = item.select_one("span.ipc-metadata-list-summary-item__tl")
        if not descripcion_tag:
            descripcion_tag = item.select_one(".text-muted")
        descripcion = descripcion_tag.text.strip() if descripcion_tag else "Sin descripción disponible"

        peliculas.append({
            "titulo": titulo,
            "año": anio,
            "puntuacion": rating,
            "descripcion": descripcion,
            "url": url_peli
        })

    return peliculas

# --- Ejecución principal ---
anio = input("📅 Ingresá el año que querés buscar: ").strip()

if not anio.isdigit():
    print("⚠️ El año debe ser un número, por ejemplo 2023.")
    exit()

print(f"\n🔎 Buscando las 10 mejores películas de {anio} en IMDb...\n")

peliculas = obtener_mejores_peliculas(anio)

if not peliculas:
    print("⚠️ No se encontraron películas para ese año.")
else:
    print("🎬 ─── MEJORES PELÍCULAS ───\n")
    for i, peli in enumerate(peliculas, start=1):
        print(f"{i}. 🎞️ {peli['titulo']}")
        print(f"   ⭐ Puntuación: {peli['puntuacion']}")
        print(f"   🔗 URL: {peli['url']}")
        print("   " + "-" * 60)
        time.sleep(0.5)

# Guardar en JSON
if peliculas:
    with open("peliculas_por_anio.json", "w", encoding="utf-8", errors="replace") as f:
        json.dump(peliculas, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Se guardaron {len(peliculas)} películas del año {anio} en 'peliculas_por_anio.json'")
else:
    print("\n⚠️ No se pudo guardar nada porque no se extrajo contenido.")
