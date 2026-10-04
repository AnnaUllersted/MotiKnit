"""
Motif library for MotiKnit: one page per motif, plus sitemap.xml, feed.xml and robots.txt.

Served in Danish on motiknit.dk and English everywhere else, matching app.py's
get_language_from_domain().

Add to app.py:
    from motif_pages import motif_pages
    app.register_blueprint(motif_pages)
"""
import json
import os
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

from flask import Blueprint, Response, abort, current_app, render_template, request, url_for

motif_pages = Blueprint("motif_pages", __name__)

MOTIFS_FILE = os.path.join(os.path.dirname(__file__), "motifs.json")

UI_TEXT = {
    "en": {
        "html_lang": "en",
        "index_title": "Free knitting charts and colourwork motifs | MotiKnit",
        "index_meta_description": "Free colourwork knitting charts: animals, letters, food and more. Adjust any motif to your own size and gauge.",
        "page_heading": "Free knitting charts",
        "all_motifs": "All motifs",
        "title_suffix": "– free pattern | MotiKnit",
        "need_different": "Need a different size or gauge? Make your own version in the generator.",
        "open_generator": "Open the generator",
        "cookie_message": "We use cookies (Google Analytics and Pinterest) to measure traffic and improve the site. You can accept or decline them.",
        "cookie_accept": "Accept",
        "cookie_decline": "Decline",
    },
    "da": {
        "html_lang": "da",
        "index_title": "Gratis strikkeopskrifter og farvestrikningsmotiver | MotiKnit",
        "index_meta_description": "Gratis strikkeopskrifter til farvestrikning: dyr, bogstaver, mad og meget mere. Tilpas ethvert motiv til din egen størrelse og strikkefasthed.",
        "page_heading": "Gratis strikkeopskrifter",
        "all_motifs": "Alle motiver",
        "title_suffix": "– gratis opskrift | MotiKnit",
        "need_different": "Har du brug for en anden størrelse eller strikkefasthed? Lav din egen version i generatoren.",
        "open_generator": "Åbn generatoren",
        "cookie_message": "Vi bruger cookies (Google Analytics og Pinterest) til at måle trafik og forbedre siden. Du kan acceptere eller afvise dem.",
        "cookie_accept": "Accepter",
        "cookie_decline": "Afvis",
    },
}


def get_language():
    return "da" if "motiknit.dk" in request.host else "en"


def site_url():
    """Base URL (scheme + host) of whichever domain served this request."""
    return f"{request.scheme}://{request.host}"


def load_motifs():
    """All motifs, newest first."""
    with open(MOTIFS_FILE, encoding="utf-8") as f:
        motifs = json.load(f)
    return sorted(motifs, key=lambda m: m["published"], reverse=True)


def get_motif(slug):
    return next((m for m in load_motifs() if m["slug"] == slug), None)


def localize_motif(motif, lang):
    """Motif dict with language-specific text resolved, falling back to English."""
    title = motif.get(f"title_{lang}") or motif["title"]
    description = motif.get(f"description_{lang}") or motif["description"]
    method = motif.get(f"method_{lang}") or motif["method"]

    if lang == "da":
        size_line = f"Størrelse: {motif['stitches']} masker × {motif['rows']} pinde (ca. {motif['height_cm']} cm høj)"
        gauge_line = f"Strikkefasthed: {motif['gauge_stitches']} masker × {motif['gauge_rows']} pinde per 10 cm"
        method_line = f"Metode: {method}"
        chart_alt = f"Strikkediagram af et {title.lower()}, {motif['stitches']} masker x {motif['rows']} pinde"
        photo_alt = f"Strikket eksempel af {title.lower()}"
    else:
        size_line = f"Size: {motif['stitches']} stitches × {motif['rows']} rows (about {motif['height_cm']} cm tall)"
        gauge_line = f"Gauge: {motif['gauge_stitches']} stitches × {motif['gauge_rows']} rows per 10 cm"
        method_line = f"Method: {method}"
        chart_alt = f"Knitting chart of a {title.lower()}, {motif['stitches']} stitches by {motif['rows']} rows"
        photo_alt = f"Knitted sample of the {title.lower()}"

    return {
        **motif,
        "title": title,
        "description": description,
        "method": method,
        "size_line": size_line,
        "gauge_line": gauge_line,
        "method_line": method_line,
        "chart_alt": chart_alt,
        "photo_alt": photo_alt,
    }


def absolute(endpoint, **values):
    """Full URL for the domain that served the current request (Pinterest, Google, Open Graph)."""
    return site_url() + url_for(endpoint, **values)


# ---------- Pages ----------

@motif_pages.route("/motifs")
def motif_index():
    lang = get_language()
    motifs = [localize_motif(m, lang) for m in load_motifs()]
    return render_template(
        "motif_index.html",
        motifs=motifs,
        lang=lang,
        t=UI_TEXT[lang],
        page_url=absolute("motif_pages.motif_index"),
    )


@motif_pages.route("/motif/<slug>")
def motif_page(slug):
    motif = get_motif(slug)
    if motif is None:
        abort(404)
    lang = get_language()
    return render_template(
        "motif.html",
        motif=localize_motif(motif, lang),
        lang=lang,
        t=UI_TEXT[lang],
        page_url=absolute("motif_pages.motif_page", slug=slug),
        image_url=absolute("static", filename=motif["chart_image"]),
    )


# ---------- For Google ----------

@motif_pages.route("/sitemap.xml")
def sitemap():
    base = site_url()
    entries = [(base + "/", None), (absolute("motif_pages.motif_index"), None)]
    for m in load_motifs():
        entries.append((absolute("motif_pages.motif_page", slug=m["slug"]), m["published"]))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(loc)}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return Response("\n".join(lines), mimetype="application/xml")


@motif_pages.route("/robots.txt")
def robots():
    # Remove this route if you already serve a robots.txt file.
    body = f"User-agent: *\nAllow: /\n\nSitemap: {site_url()}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


# ---------- For Pinterest ----------

@motif_pages.route("/feed.xml")
def feed():
    lang = get_language()
    t = UI_TEXT[lang]
    items = []
    for m in load_motifs()[:50]:
        localized = localize_motif(m, lang)
        link = absolute("motif_pages.motif_page", slug=m["slug"])
        image = absolute("static", filename=m["chart_image"])
        image_path = os.path.join(current_app.static_folder, m["chart_image"])
        size = os.path.getsize(image_path) if os.path.exists(image_path) else 0
        published = datetime.fromisoformat(m["published"]).replace(tzinfo=timezone.utc)

        items.append(f"""    <item>
      <title>{escape(localized["title"])}</title>
      <link>{escape(link)}</link>
      <guid>{escape(link)}</guid>
      <description>{escape(localized["description"])}</description>
      <pubDate>{format_datetime(published)}</pubDate>
      <enclosure url="{escape(image)}" length="{size}" type="image/png"/>
      <media:content url="{escape(image)}" medium="image"/>
    </item>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>MotiKnit – {t["page_heading"]}</title>
    <link>{site_url()}/motifs</link>
    <description>{t["index_meta_description"]}</description>
{chr(10).join(items)}
  </channel>
</rss>"""
    return Response(xml, mimetype="application/rss+xml")
