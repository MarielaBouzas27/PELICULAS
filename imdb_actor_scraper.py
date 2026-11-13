

import requests
from bs4 import BeautifulSoup
import json
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36"
}

def buscar_actor(nombre):
    """Busca el ID de un actor o actriz en IMDb."""
    nombre = nombre.strip()
    url = f"https://v2.sg.media-imdb.com/suggestion/{nombre[0].lower()}/{nombre.replace(' ', '_')}.json"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print("❌ Error al buscar el actor.")
        return None
    data = res.json()
    for r in data.get("d", []):
        if r.get("id", "").startswith("nm"):
            return {"id": r["id"], "nombre": r.get("l", nombre)}
    return None

def obtener_peliculas(actor_id):
    """Obtiene la filmografía del actor desde IMDb."""
    url = f"https://www.imdb.com/search/title/?role={actor_id}&sort=year,desc"
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        print("❌ Error al obtener la filmografía.")
        return []

    soup = BeautifulSoup(res.text, "html.parser")

    # Selector actualizado (noviembre 2025)
    items = soup.select("li.ipc-metadata-list-summary-item")
    if not items:
        items = soup.select(".lister-item")

    peliculas = []

    for item in items[:10]:
        titulo_tag = item.select_one("a.ipc-title-link-wrapper")
        if not titulo_tag:
            titulo_tag = item.select_one(".lister-item-header a")
        if not titulo_tag:
            continue

        titulo = titulo_tag.text.strip()
        href = titulo_tag.get("href", "")
        url_peli = f"https://www.imdb.com{href.split('?')[0]}"

        # Año
        year_tag = item.select_one("span.ipc-metadata-list-summary-item__li")
        if not year_tag:
            year_tag = item.select_one(".lister-item-year")
        year = year_tag.text.strip("()") if year_tag else "N/A"

        peliculas.append({
            "titulo": titulo,
            "año": year,
            "url": url_peli
        })

    return peliculas

# --- Ejecución principal ---
nombre_actor = input("🎭 Ingresá el nombre del actor o actriz: ").strip()
actor = buscar_actor(nombre_actor)

if not actor:
    print("❌ No se encontró ningún actor con ese nombre.")
    exit()

print(f"\n✅ Actor encontrado: {actor['nombre']} (ID: {actor['id']})")
print("\n🎬 ─── FILMOGRAFÍA DESTACADA ───\n")

peliculas = obtener_peliculas(actor["id"])

if not peliculas:
    print("⚠️ No se encontraron películas en la filmografía.")
else:
    for i, peli in enumerate(peliculas, start=1):
        print(f"{i}. 🎞️ {peli['titulo']}")
        print(f"   🔗 URL: {peli['url']}")
        print("   " + "-" * 60)
        time.sleep(0.5)

# Guardar en JSON
if peliculas:
    with open("peliculas_actor.json", "w", encoding="utf-8", errors="replace") as f:
        json.dump(peliculas, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Se guardaron {len(peliculas)} películas de {actor['nombre']} en 'peliculas_actor.json'")
else:
    print("\n⚠️ No se pudo guardar nada porque no se extrajo contenido.")
