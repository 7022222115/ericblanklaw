"""
wp_to_md.py — WordPress export (WXR/XML) -> Astro Markdown converter.

Archived / reusable. Converts selected posts (by slug) from a WordPress
export XML into Markdown files for the Astro `blog` content collection.

Usage:
    cd "C:\\Users\\HK Yoon\\Development\\ericblanklaw"
    python scripts/wp_to_md.py

Edit SLUG_MAP below to control which posts are converted. Run on one post to
verify, then expand SLUG_MAP for the full batch later.

Deps:  pip install markdownify lxml
"""

import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

from bs4 import BeautifulSoup
from markdownify import markdownify as md

# --- Configuration ---------------------------------------------------------

XML_PATH = r"C:\Users\H.K. Yoon\Downloads\ericblanklaw.WordPress.2026-06-16.xml"

# Output directory for the Astro blog content collection (relative to project root).
OUT_DIR = os.path.join("src", "content", "blog")

# { wordpress_slug : new_astro_slug }
# Full batch — all 35 posts.
SLUG_MAP = {
    "motorcycle-sweepstakes": "motorcycle-sweepstakes",
    "las-vegas-city-council-greenlights-new-regulations-for-e-bikes-scooters": "las-vegas-city-council-greenlights-new-regulations-e-bikes-scooters",
    "international-students-in-us-colleges-face-new-challenges-under-trump-administration": "international-students-us-colleges-face-new-challenges-under-trump-administ",
    "daca-renewal-assistance": "daca-renewal-assistance",
    "eric-blank-injury-attorneys-and-pfas-litigation": "eric-blank-injury-attorneys-pfas-litigation",
    "google-chrome-incognito-lawsuit": "google-chrome-incognito-lawsuit",
    "the-steps-to-filing-a-car-accident-claim-in-nevada": "steps-filing-car-accident-claim-nevada",
    "i-slipped-and-fell-at-a-restaurant-in-nevada": "i-slipped-fell-restaurant-nevada",
    "motorcycle-accident-in-nevada": "motorcycle-accident-nevada",
    "las-vegas-motorcycle-giveaway": "las-vegas-motorcycle-giveaway",
    "las-vegas-road-conditions-and-causing-accidents": "las-vegas-road-conditions-causing-accidents",
    "can-you-sue-uber-for-an-accident-in-las-vegas-nevada": "can-sue-uber-accident-las-vegas-nevada",
    "what-happens-if-your-lyft-gets-in-an-accident-in-las-vegas": "what-happens-if-lyft-gets-accident-las-vegas",
    "what-are-the-five-things-you-must-do-whenever-youre-involved-in-an-accident": "what-five-things-must-do-whenever-youre-involved-accident",
    "understanding-the-baby-food-tylenol-autism-lawsuit": "understanding-baby-food-tylenol-autism-lawsuit",
    "protecting-yourself-and-your-rights-after-a-car-accident": "protecting-yourself-rights-after-car-accident",
    "what-you-need-to-know-about-nevada-dog-bite-laws": "what-need-know-about-nevada-dog-bite-laws",
    "did-you-suffer-slip-and-fall-injury-in-las-vegas-casino": "did-suffer-slip-fall-injury-las-vegas-casino",
    "workers-compensation-in-nevada": "workers-compensation-nevada",
    "social-media-can-harm-your-case": "social-media-can-harm-case",
    "what-you-must-know-about-dui-accidents-in-nevada": "what-must-know-about-dui-accidents-nevada",
    "school-bullying-its-prevalence-and-the-legal-options-available-for-victims": "school-bullying-its-prevalence-legal-options-available-victims",
    "bair-hugger-warning-blanket-lawsuits-legal-options-with-eric-blank": "bair-hugger-warning-blanket-lawsuits-legal-options-eric-blank",
    "chemical-hair-relaxers-a-guide-to-lawsuits-and-compensation-with-eric-blank": "chemical-hair-relaxers-guide-lawsuits-compensation-eric-blank",
    "nursing-home-negligence-and-remedies-in-nevada": "nursing-home-negligence-remedies-nevada",
    "bed-bug-hotel": "bed-bug-hotel",
    "aqueous-film-forming-foam-afff-and-cancer-risks": "aqueous-film-forming-foam-afff-cancer-risks",
    "ccsd-mom-speaks-publicly-for-first-time-since-suing-school-district": "ccsd-mom-speaks-publicly-first-time-since-suing-school-district",
    "dog-bites-in-nevada": "dog-bites-nevada",
    "nevadas-alarming-rate-of-uninsured-motorists": "nevadas-alarming-rate-uninsured-motorists",
    "handling-bus-injury-claims": "handling-bus-injury-claims",
    "life-altering-injuries-and-the-compensation-you-deserve": "life-altering-injuries-compensation-deserve",
    "what-to-do-after-a-slip-and-fall-injury-in-a-las-vegas-casino": "what-do-after-slip-fall-injury-las-vegas-casino",
    "how-to-know-if-your-car-insurance-company-is-acting-in-bad-faith": "how-know-if-car-insurance-company-acting-bad-faith",
    "new-utah-law-aimed-at-improving-motorcycle-safety": "new-utah-law-aimed-improving-motorcycle-safety",
}

NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
}

SHORTCODE_RE = re.compile(r"\[/?(?:gravityform|wpcode)[^\]]*\]")
DESC_MAX = 152


# --- Helpers ---------------------------------------------------------------

def get_postmeta(item, key):
    """Return the <wp:meta_value> for a given <wp:meta_key>, or None."""
    for meta in item.findall("wp:postmeta", NS):
        k = meta.find("wp:meta_key", NS)
        if k is not None and k.text == key:
            v = meta.find("wp:meta_value", NS)
            return v.text if v is not None else None
    return None


def yaml_quote(value):
    """Return a safely double-quoted YAML scalar."""
    if value is None:
        value = ""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return '"' + escaped + '"'


def to_iso_date(wp_date):
    """WordPress post_date 'YYYY-MM-DD HH:MM:SS' -> 'YYYY-MM-DD'."""
    if not wp_date:
        return ""
    try:
        return datetime.strptime(wp_date.strip(), "%Y-%m-%d %H:%M:%S").date().isoformat()
    except ValueError:
        # Fallback: take the date portion before any space.
        return wp_date.strip().split(" ")[0]


def autogen_description(html):
    """Strip HTML, collapse whitespace, truncate to ~DESC_MAX at a word boundary."""
    text = BeautifulSoup(html or "", "html.parser").get_text(" ")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= DESC_MAX:
        return text
    truncated = text[:DESC_MAX]
    if " " in truncated:
        truncated = truncated.rsplit(" ", 1)[0]
    return truncated.rstrip() + "…"


def html_to_markdown(html):
    """Strip target shortcodes, convert HTML->Markdown, normalize blank lines."""
    cleaned = SHORTCODE_RE.sub("", html or "")
    body = md(cleaned, heading_style="ATX", strip=["span"])
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


# --- Main ------------------------------------------------------------------

def main():
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    # Build a dict of post-type items keyed by slug (<wp:post_name>).
    items_by_slug = {}
    for item in root.iter("item"):
        post_type = item.find("wp:post_type", NS)
        if post_type is None or post_type.text != "post":
            continue
        name = item.find("wp:post_name", NS)
        slug = name.text if name is not None else None
        if slug:
            items_by_slug[slug] = item

    os.makedirs(OUT_DIR, exist_ok=True)

    for wp_slug, new_slug in SLUG_MAP.items():
        item = items_by_slug.get(wp_slug)
        if item is None:
            print(f"MISSING: '{wp_slug}' not found among post-type items — skipped.")
            continue

        title_el = item.find("title")
        title = title_el.text if title_el is not None and title_el.text else ""

        content_el = item.find("content:encoded", NS)
        content_html = content_el.text if content_el is not None else ""

        # Description: rank_math_description if present & non-empty, else autogen.
        rm_desc = get_postmeta(item, "rank_math_description")
        if rm_desc and rm_desc.strip():
            description = rm_desc.strip()
            desc_source = "rankmath"
        else:
            description = autogen_description(content_html)
            desc_source = "AUTOGEN"
            print(f"AUTOGEN DESC: {new_slug}")

        date_el = item.find("wp:post_date", NS)
        pub_date = to_iso_date(date_el.text if date_el is not None else "")

        body = html_to_markdown(content_html)

        frontmatter = (
            "---\n"
            f"title: {yaml_quote(title)}\n"
            f"description: {yaml_quote(description)}\n"
            f"pubDate: {pub_date}\n"
            f'author: "Eric Blank Injury Attorneys"\n'
            f"draft: false\n"
            "---\n\n"
        )

        out_path = os.path.join(OUT_DIR, f"{new_slug}.md")
        contents = frontmatter + body + "\n"
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(contents)

        print(f"WROTE: {new_slug}  |  body {len(body)} chars  |  desc: {desc_source}")


if __name__ == "__main__":
    main()
