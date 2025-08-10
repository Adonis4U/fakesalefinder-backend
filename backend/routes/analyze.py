from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx, re, time
from selectolax.parser import HTMLParser

router = APIRouter()

class AnalyzeIn(BaseModel):
    url: str

def extract_text(html: str, selectors):
    tree = HTMLParser(html)
    for sel in selectors:
        node = tree.css_first(sel)
        if node and node.text():
            return node.text().strip()
    return None

def extract_price(html: str):
    # Try common patterns
    price_regex = re.compile(r"(?:€|EUR|\$)\s?([0-9]+[\.,]?[0-9]*)")
    m = price_regex.search(html)
    if m:
        try:
            return float(m.group(1).replace(',', '.'))
        except:
            return None
    return None

def fake_market_reference(title: str):
    # Pretend we looked up a reference price from trusted marketplaces
    # In MVP, this can be replaced by a real price-compare
    base = 79.99
    if 'smart' in (title or '').lower():
        base = 99.0
    return base

def risk_label(score: int):
    if score >= 65: return "Alto"
    if score >= 35: return "Medio"
    return "Basso"

@router.post("/analyze")
async def analyze(payload: AnalyzeIn):
    url = payload.url
    headers = {"User-Agent": "Mozilla/5.0 FakeSaleFinder/0.1"}

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True, headers=headers) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            html = resp.text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Fetch error: {e}")

    title = extract_text(html, ["h1", "meta[property='og:title']", "title"]) or "Prodotto"
    price = extract_price(html)
    ref = fake_market_reference(title)

    proofs = []
    score = 0

    if price is not None and ref is not None:
        if price < ref * 0.6:
            score += 20
            proofs.append("Prezzo anomalo (>40% sotto media stimata)")

    # Very naive shipping detection
    if "giorni" in html.lower() or "days" in html.lower():
        # Not accurate; placeholder
        score += 10
        proofs.append("Spedizione indicata potenzialmente lunga")

    # Domain age placeholder (real: use WHOIS)
    proofs.append("Età dominio non verificata (MVP)")
    score += 10

    return {
        "product": {
            "title": title,
            "price_site": price,
            "price_ref": ref,
            "risk_score": score,
            "risk_label": risk_label(score),
            "proofs": proofs
        }
    }
