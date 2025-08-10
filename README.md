# FakeSaleFinder — Backend (FastAPI) + Render + Hostinger DNS

Dominio: **adonisgagliardi.com**  
API: **https://api.adonisgagliardi.com**

## Deploy con Render (Blueprint)
1. Connetti questo repo a **Render** (Settings → Blueprints → New → seleziona questo repo che contiene `render.yaml`).
2. Render creerà:
   - `fsf-api` (Web Service, Docker, health `/api/health`)
   - `fsf-postgres` (DB gestito)
   - `fsf-redis` (Redis gestito)
3. Primo deploy: al termine avrai un URL tipo `https://fsf-api-XXXX.onrender.com` funzionante.

## DNS su Hostinger (hPanel)
1. Vai a **Zone DNS** del dominio `adonisgagliardi.com`.
2. Crea un record **CNAME**:
   - **Nome (Host)**: `api`
   - **Target**: `<NOME-SERVIZIO>.onrender.com` (lo trovi nella pagina del servizio su Render)
   - **TTL**: 300 (default OK)
3. In Render → `fsf-api` → **Custom Domains** → `api.adonisgagliardi.com` → Verify → abilita SSL automatico (Let's Encrypt).
4. Test: `https://api.adonisgagliardi.com/api/health` → `{"status":"ok"}`

## GitHub Actions → Deploy automatico
- Vai su **Settings → Secrets and variables → Actions** nel repo, aggiungi:
  - `RENDER_DEPLOY_HOOK` = URL del Deploy Hook del servizio `fsf-api` (Render → Service → Deploy Hooks → Copy URL).
- Ogni push su `main` lancia la CI e **chiama il Deploy Hook** per aggiornare l'app su Render.

## API principali
- `GET /api/health` — health check
- `POST /api/analyze` — body: `{"url":"https://.../product"}` → ritorna titolo, prezzo stimato, risk score + prove (MVP).

## Run locale (senza Docker)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000
# http://localhost:8000/api/health
```

## Run con Docker (locale)
```bash
docker build -t fsf-api .
docker run -p 8000:8000 fsf-api
```

## Postman
Importa `POSTMAN_collection.json` e imposta `api_base = https://api.adonisgagliardi.com`.

---
### Nota
`/api/analyze` è MVP: usa regole basilari (prezzo anomalo, shipping indicativa) e placeholder per età dominio. 
Per produzione collegare: WHOIS, reverse-image, price-compare e logging.
