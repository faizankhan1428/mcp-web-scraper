import httpx
from bs4 import BeautifulSoup

def scrape_website(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = httpx.get(url, headers=headers, timeout=10.0, follow_redirects=True)
        
        if response.status_code != 200:
            return f"Error: Failed to fetch website. Status code: {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        return f"An error occurred: {str(e)}"