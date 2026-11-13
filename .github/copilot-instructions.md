## Purpose

This file gives concise, actionable guidance for an AI coding agent to be productive in this small IMDb scraping repo.

## Quick summary
- Language: Python 3 scripts (no framework). Main files: `imdb_scraper.py`, `imdb_top_genre_scraper.py`, `imdb_top_year_scraper.py`, `imdb_actor_scraper.py`.
- Run: scripts are interactive CLI programs (they prompt for input). Typical commands are in `comandos para usar el programa.txt` (e.g. `python imdb_top_genre_scraper.py`).
- Outputs: JSON files produced in repo root: `peliculas.json`, `peliculas_por_genero.json`, `peliculas_por_anio.json`, `peliculas_actor.json`.

## Architecture & data flow (big picture)
- Each script: performs HTTP requests (synchronous) using `requests`, parses HTML with `BeautifulSoup`, extracts a short list (top 10) and writes a JSON file.
- Flow: user input -> build URL -> requests.get(HEADERS) -> BeautifulSoup parse -> select list items -> extract fields (title, url, rating, description, image) -> save JSON.

## Project-specific patterns and conventions
- Spanish UI/messages and variable names (e.g. `peliculas`, `titulo`, `año`). Keep translations consistent when editing.
- Robust selector strategy: scripts try a primary modern selector then fall back to legacy ones. Example from `imdb_top_genre_scraper.py`:

  - Primary: `items = soup.select("li.ipc-metadata-list-summary-item")`
  - Fallback: `if not items: items = soup.select(".lister-item")`

- Standard HTTP header is centralized as `HEADERS` / `headers` with a realistic User-Agent string. Preserve or extend this when adding requests.
- Rate limiting: scripts use `time.sleep(0.5)` or `1` between requests; follow this pattern to avoid scraping throttling.
- JSON writing uses `json.dump(..., ensure_ascii=False, indent=4, errors='replace')` — preserve to maintain UTF-8 Spanish output.

## Selectors and resilience (what to change when IMDb HTML changes)
- Primary selectors in late-2025 use `ipc-*` classes; legacy fallback uses `.lister-item` and `.lister-item-header a`.
- When a selector breaks, update these locations:
  - `titulo_tag = item.select_one("a.ipc-title-link-wrapper")` (fallback: `.lister-item-header a`)
  - Rating: check `span.ipc-rating-star` or `<strong>`
  - Description: `span.ipc-metadata-list-summary-item__tl` or `.text-muted`
- Tests to run after selector changes: run the script locally with a known input and confirm the JSON output contains expected keys (`titulo`, `url`, `puntuacion`). The easiest smoke test is to run one script and inspect the top of the produced JSON.

## Dependencies & environment
- Required Python packages: `requests`, `beautifulsoup4`.
- No `requirements.txt` or virtualenv in repo — create one if adding CI. Suggest minimal contents:

  requests
  beautifulsoup4

- Run on Windows PowerShell with the commands from `comandos para usar el programa.txt` (examples present). Example: `python imdb_actor_scraper.py`.

## Debugging tips specific to this repo
- If a script prints no items: check for selector mismatch (inspect `soup.prettify()` and adapt selectors). The scripts already print warnings when no items are found.
- If requests return non-200: validate `HEADERS` and consider small delays or retries around `requests.get`.
- To add automated checks, add a small smoke test that runs a script for a deterministic static HTML sample (store sample under `tests/fixtures/`) and asserts extracted keys.

## Files to inspect when making changes
- `imdb_scraper.py` — Top 10 globally (Top 250).
- `imdb_top_genre_scraper.py` — Genre-based top list and `GENERO_TRADUCIDO` mapping.
- `imdb_top_year_scraper.py` — Year-based top list.
- `imdb_actor_scraper.py` — Uses IMDb suggestion JSON endpoint to resolve actor `nm...` IDs and then scrapes filmography.
- `comandos para usar el programa.txt` — canonical CLI examples.

## Non-goals / things not to add without discussion
- Do not switch to headless browsers or Selenium unless necessary; these scripts are intentionally simple synchronous scrapers.
- Avoid changing the interactive UX to a silent mode without adding equivalent documented CLI flags.

If anything here is unclear or you'd like more detail (example patch for making selectors configurable or adding a `requirements.txt` and a tiny smoke test), tell me which part to expand.
