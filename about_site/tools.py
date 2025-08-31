import requests
from bs4 import BeautifulSoup
from strands import tool


@tool
def fetch_url_metadata(url: str, timeout: int = 10) -> dict:
    """
    Efficiently fetch metadata (title, description, keywords, og tags) from a URL.
    Only downloads until </head> is found to avoid fetching the entire body.
    """
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MetaScraper/1.0)"}
    response = requests.get(url, headers=headers, stream=True, timeout=timeout)
    response.raise_for_status()

    content = []
    for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
        if chunk:
            content.append(chunk)
            joined = "".join(content)
            if "</head>" in joined.lower():
                break

    html_head = "".join(content)
    soup = BeautifulSoup(html_head, "html.parser")

    metadata = {
        "title": soup.title.string.strip() if soup.title else None,
        "description": None,
        "keywords": None,
        "og_title": None,
        "og_description": None,
        "og_image": None
    }

    # Standard meta tags
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        metadata["description"] = desc_tag["content"].strip()

    keywords_tag = soup.find("meta", attrs={"name": "keywords"})
    if keywords_tag and keywords_tag.get("content"):
        metadata["keywords"] = keywords_tag["content"].strip()

    # OpenGraph tags
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        metadata["og_title"] = og_title["content"].strip()

    og_desc = soup.find("meta", property="og:description")
    if og_desc and og_desc.get("content"):
        metadata["og_description"] = og_desc["content"].strip()

    og_img = soup.find("meta", property="og:image")
    if og_img and og_img.get("content"):
        metadata["og_image"] = og_img["content"].strip()

    return metadata